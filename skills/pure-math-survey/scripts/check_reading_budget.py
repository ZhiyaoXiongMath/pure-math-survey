#!/usr/bin/env python3
"""Count every page of requested PDFs. No mathematical or visual quality verdict."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

CONCISE = {1: 5, 2: 6, 3: 6, 4: 5, 5: 10}
STANDARD = {1: 8, 2: 10, 3: 10, 4: 8, 5: 16}

def safe_file(root: Path, value: str) -> Path:
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError('Expected a nonempty relative PDF path')
    p = (root / value).resolve()
    if not p.is_relative_to(root.resolve()) or p.suffix.lower() != '.pdf':
        raise ValueError('PDF must be within the project')
    if not p.is_file():
        raise FileNotFoundError(p)
    return p

def check(root: Path) -> dict:
    import fitz
    root = root.resolve()
    manifest = json.loads((root / 'project-manifest.json').read_text())
    rows = []
    seen = set()
    documents = manifest['documents']
    if not isinstance(documents, list):
        raise ValueError('documents must be a list')
    for doc in documents:
        if not isinstance(doc, dict):
            raise ValueError('Each document must be an object')
        part, edition = doc['part'], doc['edition']
        if isinstance(part, bool) or not isinstance(part, int) or part not in CONCISE or edition not in ('concise', 'standard'):
            raise ValueError('Unknown part or edition')
        if (part, edition) in seen:
            raise ValueError('Repeated part/edition')
        seen.add((part, edition))
        limit = doc.get('page_review_limit', (CONCISE if edition == 'concise' else STANDARD)[part])
        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 1:
            raise ValueError('Page review limit must be a positive integer')
        path = safe_file(root, doc['pdf_file'])
        with fitz.open(path) as pdf:
            if pdf.is_encrypted or pdf.page_count < 1:
                raise ValueError('Expected a nonempty, readable PDF')
            pages = pdf.page_count
        rows.append({'part': part, 'edition': edition, 'pdf': doc['pdf_file'],
                     'pages': pages, 'page_review_limit': limit,
                     'status': 'WITHIN_BUDGET' if pages <= limit else 'OVER_BUDGET'})
    if not rows:
        raise ValueError('No requested documents')
    requested = manifest.get('requested_documents')
    if requested is not None:
        if not isinstance(requested, list) or any(not isinstance(d, dict) for d in requested):
            raise ValueError('requested_documents must be a list of objects')
        pairs = [(d['part'], d['edition']) for d in requested]
        if len(pairs) != len(set(pairs)) or seen != set(pairs):
            raise ValueError('Document selection differs from requested_documents or is repeated')
    return {'scope': 'Total PDF pages including references; not a content or visual grade',
            'status': 'WITHIN_BUDGET' if all(r['status'] == 'WITHIN_BUDGET' for r in rows) else 'OVER_BUDGET',
            'documents': rows}

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('project', type=Path)
    args = p.parse_args()
    try:
        report = check(args.project)
    except (OSError, ValueError, KeyError, TypeError, ImportError) as exc:
        print(json.dumps({'status': 'ERROR', 'error': str(exc)}))
        return 2
    print(json.dumps(report, indent=2))
    return 0 if report['status'] == 'WITHIN_BUDGET' else 1

if __name__ == '__main__':
    raise SystemExit(main())

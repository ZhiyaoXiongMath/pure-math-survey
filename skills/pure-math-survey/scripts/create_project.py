#!/usr/bin/env python3
"""Create an explicitly selected, unverified scaffold; never overwrite a project."""
from __future__ import annotations
import argparse
import csv
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STEMS = {1: 'foundations', 2: 'results', 3: 'methods', 4: 'boundaries', 5: 'integrated'}


def parse_selection(value: str) -> list[tuple[int, str]]:
    if value == 'suite':
        return [(p, 'concise') for p in STEMS]
    if value == 'all':
        return [(p, e) for p in STEMS for e in ('concise', 'standard')]
    result = []
    for raw in value.split(','):
        match = re.fullmatch(r'([1-5]):(concise|standard)', raw.strip())
        if not match:
            raise ValueError('Use a selection such as 5:standard, a comma-separated list, suite, or all.')
        item = (int(match.group(1)), match.group(2))
        if item in result:
            raise ValueError('Repeated part/edition selection.')
        result.append(item)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--topic', required=True)
    parser.add_argument('--documents', default='5:concise', help='Default 5:concise; suite gives I–V concise; all explicitly gives ten.')
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.topic):
        parser.error('Topic must be a lowercase alphanumeric filename slug separated by hyphens.')
    try:
        selection = parse_selection(args.documents)
    except ValueError as exc:
        parser.error(str(exc))
    out = args.output.expanduser().resolve()
    if out == ROOT or out.is_relative_to(ROOT):
        parser.error('Destination must be outside the skill.')
    if out.exists():
        parser.error('Destination already exists; no files were overwritten.')
    out.mkdir(parents=True)
    documents = []
    for part, edition in selection:
        name = f'part{part}-{STEMS[part]}-{edition}'
        stem = f'{args.topic}-{name}'
        shutil.copy2(ROOT / 'assets/templates' / (name + '.tex'), out / (stem + '.tex'))
        documents.append({'part': part, 'edition': edition, 'tex_file': stem + '.tex', 'pdf_file': stem + '.pdf', 'page_review_limit': ({1:5,2:6,3:6,4:5,5:10} if edition == 'concise' else {1:8,2:10,3:10,4:8,5:16})[part]})
    (out / 'evidence').mkdir()
    for doc in documents:
        review_path = 'evidence/' + Path(doc['tex_file']).stem + '-structure-review.json'
        doc['structure_review'] = review_path
        (out / review_path).write_text(json.dumps({'schema_version':'1.0.0', 'tex_file':doc['tex_file'], 'source_sha256':'PENDING', 'reviewer_mode':'PENDING', 'reviewed_on':'PENDING', 'sections':[], 'results':[]}, indent=2) + '\n')
    shutil.copy2(ROOT / 'assets/templates/math-review.sty', out / 'math-review.sty')
    manifest = {'schema_version': '1.0.0', 'skill_version': '1.5.0', 'language': 'en', 'topic': args.topic,
                'literature_cutoff': '[Set from actual source verification]',
                'requested_documents': [{'part': p, 'edition': e} for p, e in selection],
                'documents': documents}
    (out / 'project-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    names = ['bibliographic-identity', 'proof-mechanism-registry', 'publication-map']
    if any(p in (4, 5) for p, _ in selection):
        names += ['frontier-claim-registry', 'frontier-reverse-search']
    for name in names:
        with (ROOT / f'assets/registries/{name}-template.csv').open(newline='', encoding='utf-8') as f:
            header = next(csv.reader(f))
        with (out / (name + '.csv')).open('w', newline='', encoding='utf-8') as f:
            csv.writer(f, lineterminator='\n').writerow(header)
    shutil.copy2(ROOT / 'assets/registries/release-audit-template.csv', out / 'release-audit.csv')
    (out / 'architecture.md').write_text(
        '# Unverified draft architecture\n\nRecord the actual task, scope, selected documents and sources.\n'
        'Identify organizing questions and principal conclusions before local refinements.\n'
        'Set the page budget; remove side branches before drafting; do not omit selected core results.\n'
        'Map each principal body result to its substantive Introduction statement.\n'
        'Record Introduction-only reading, hypothesis consistency and actual verification.\n'
        'Plan explicit body results and key lemmas before prose; then perform statement-only and dependency readings.\n'
        'Concise retains that structure; standard deepens proof interiors. Evidence starts pending.\n'
        'These are pending tasks, not completed research or PASS evidence.\n')
    (out / 'README.md').write_text(
        '# Unverified survey scaffold\n\nReplace all insertion text and metadata with actual mathematics.\n'
        'No research, PDF, source sample or completed verification is supplied.\n'
        'The Introduction must state the actual main conclusions, not a roadmap.\n'
        'Read the skill validation contract before publishing.\n')
    print(f'Created {len(documents)} unverified template source(s): {out}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

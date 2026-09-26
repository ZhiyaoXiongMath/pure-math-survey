#!/usr/bin/env python3
"""Generate bibliography companions and build the standalone review.

Usage: python3 build.py
Requires Python >=3.9 and pdflatex with the packages in math-review.sty.
No network or BibTeX binary is needed. references.json is the single
bibliographic data source; references.bib and references.bbl are regenerated.
SOURCE_DATE_EPOCH makes the PDF reproducible with a fixed TeX installation.
"""
from pathlib import Path
import json, os, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parent

def bibliographies() -> None:
    refs = json.loads((ROOT / 'references.json').read_text(encoding='utf-8'))
    keys = [r['key'] for r in refs]
    if len(set(keys)) != len(keys):
        raise ValueError('Duplicate bibliography keys')
    bib = ['% Generated from references.json by build.py.\n']
    bbl = [r'\begin{thebibliography}{99}']
    fields = ('author','title','journal','volume','number','year','pages','eid','doi','url','note')
    for r in refs:
        kind = 'article' if r.get('journal') else 'misc'
        entries = [f"  {f} = {{{r[f]}}}" for f in fields if r.get(f)]
        if r.get('arxiv'):
            entries.extend([f"  eprint = {{{r['arxiv']}}}", '  archivePrefix = {arXiv}'])
        bib.append('@' + kind + '{' + r['key'] + ',\n' + ',\n'.join(entries) + '\n}\n')
        text = r'\bibitem{' + r['key'] + '} ' + r['display_author'] + ', '
        text += r'\emph{' + r['title'] + '}.'
        if r.get('journal'):
            text += ' ' + r['journal'] + ' \\textbf{' + r['volume'] + '} (' + r['year'] + ')'
            if r.get('number'): text += ', no. ' + r['number']
            if r.get('pages'): text += ', ' + r['pages']
            if r.get('eid'): text += ', article ' + r['eid']
            text += '.'
        else:
            text += ' Preprint (' + r['year'] + ').'
        # Exact controlling preprint is the useful public locator; publisher DOI
        # is retained in the machine-readable .bib without duplicating long URLs.
        if r.get('arxiv'):
            text += r' \href{https://arxiv.org/abs/' + r['arxiv'] + '}{arXiv:' + r['arxiv'] + '}.'
        elif r.get('doi'):
            text += r' \href{https://doi.org/' + r['doi'] + '}{doi:' + r['doi'] + '}.'
        elif r.get('url'):
            text += r' \href{' + r['url'] + '}{Publisher record}.'
        text += ' ' + r['note']
        bbl.append(text)
    bbl.append(r'\end{thebibliography}')
    (ROOT/'references.bib').write_text('\n'.join(bib), encoding='utf-8')
    (ROOT/'references.bbl').write_text('\n\n'.join(bbl)+'\n', encoding='utf-8')

def main() -> int:
    if not shutil.which('pdflatex'):
        print('ERROR: pdflatex is required on PATH.', file=sys.stderr)
        return 2
    bibliographies()
    env = os.environ.copy()
    env.setdefault('SOURCE_DATE_EPOCH', '1790294400') # 2026-09-25 00:00 UTC
    env['FORCE_SOURCE_DATE'] = '1'
    outputs = []
    for i in range(3):
        result = subprocess.run(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error',
                                 '-file-line-error','dhym-standard.tex'], cwd=ROOT,
                                env=env, text=True, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        outputs.append(f'===== PASS {i+1} =====\n{result.stdout}')
        if result.returncode:
            (ROOT/'build-transcript.txt').write_text('\n'.join(outputs))
            print(result.stdout[-6000:])
            return result.returncode
    (ROOT/'build-transcript.txt').write_text('\n'.join(outputs))
    log = (ROOT/'dhym-standard.log').read_text(errors='replace')
    bad = ('undefined references', 'undefined citations', 'Overfull \\hbox',
           'Overfull \\vbox', 'multiply defined', 'multiply-defined', 'Missing character:',
           'There were undefined references', 'Rerun to get cross-references right')
    findings = [x for x in bad if x in log]
    print('\n'.join(x for x in outputs[-1].splitlines() if 'Output written' in x))
    if findings:
        print('CHECK REQUIRED:', ', '.join(findings))
        return 1
    print('Build complete; no unresolved citations/references or overfull boxes.')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())

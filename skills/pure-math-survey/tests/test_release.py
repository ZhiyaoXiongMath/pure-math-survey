"""v1.1.0 maintenance regressions: wiring and offline helpers, not semantic grading."""
from __future__ import annotations
import hashlib
import importlib.util
import json
import re
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def module(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    assert spec and spec.loader
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value

build = module('build_checks')
pack = module('package_release')

def text(relative: str) -> str:
    return (ROOT / relative).read_text(encoding='utf-8')

def intro(source: str) -> str:
    return source.split(r'\section{Introduction}',1)[1].split(r'\section{',1)[0]


class IntroductionAndBenchmarkTests(unittest.TestCase):
    def test_required_conclusion_not_optional_narrative(self):
        s=text('SKILL.md')
        for phrase in ('must directly state every selected principal mathematical conclusion',
                       'Narrative and roadmaps are optional; principal-result content is not',
                       'introduction-only reading test', 'check coverage in both directions',
                       'Missing selected conclusions or material conditions fail'):
            self.assertIn(phrase,s)

    def test_benchmark_loaded_before_part_v_drafting(self):
        s=text('SKILL.md')
        self.assertIn('For every V request, read',s)
        self.assertIn('references/part-v-benchmark.md',s)
        self.assertIn('before drafting',s)
        self.assertIn('Both V editions must attain',s)

    def test_benchmark_does_not_enforce_subject_or_counts(self):
        s=text('references/part-v-benchmark.md')
        for phrase in ('not quotas','not the union of I–IV obligations',
                       'not a claim that every future output automatically matches it'):
            self.assertIn(phrase,s)
        self.assertIn('Do not add the Thomas--Yau problem to unrelated topics',s)

    def test_all_ten_introductions_require_actual_knowledge(self):
        paths=list((ROOT/'assets/templates').glob('part*.tex'))
        self.assertEqual(len(paths),10)
        for p in paths:
            s=p.read_text(); i=intro(s)
            self.assertIn('state every selected principal conclusion',s,p.name)
            self.assertIn('quantifiers',i,p.name)
            self.assertTrue('actual' in i or 'actual' in s,p.name)
            self.assertIn('body-to-introduction reverse coverage',s,p.name)

    def test_part_v_statement_slots_are_really_in_introduction(self):
        for edition in ('concise','standard'):
            s=text(f'assets/templates/part5-integrated-{edition}.tex');i=intro(s)
            self.assertIn(r'\begin{theorem}\label{thm:principal}',i)
            self.assertIn(r'\begin{theorem}\label{thm:second}',i)
            self.assertIn(r'\PrincipalStatement',i)
            self.assertIn(r'\SecondStatement',i)
            self.assertIn(r'\begin{theoremrecall}{thm:principal}',s)
            self.assertIn(r'\begin{theoremrecall}{thm:second}',s)
            self.assertEqual(s.count(r'\label{thm:principal}'),1)
            self.assertEqual(s.count(r'\label{thm:second}'),1)

    def test_part_ii_has_intro_statement_and_body_recall(self):
        for edition in ('concise','standard'):
            s=text(f'assets/templates/part2-results-{edition}.tex')
            self.assertIn(r'\begin{theorem}\label{thm:principal}',intro(s))
            self.assertIn(r'\begin{theoremrecall}{thm:principal}',s)

    def test_no_invented_optional_titles_in_templates_and_fixture(self):
        paths=[*(ROOT/'assets/templates').glob('part*.tex'),*(ROOT/'tests/fixtures').glob('*.tex')]
        pattern=r'\\begin\{(?:theorem|definition|lemma|proposition|corollary|problem|conjecture)\}\['
        for p in paths:
            self.assertIsNone(re.search(pattern,p.read_text()),p.name)

    def test_rules_examples_do_not_reintroduce_old_titles(self):
        old=('Quadratic minimization','A principal answer','The principal answer',
             'A principal result','A descriptive mathematical title','A core unresolved target')
        for p in (ROOT/'references').glob('*.md'):
            s=p.read_text()
            for title in old:
                self.assertNotIn('['+title+']',s,p.name)

    def test_two_independent_fixture_bodies_and_primary_labels(self):
        s=text('tests/fixtures/exposition-smoke.tex');i=intro(s)
        for name,label in (('quadratic','quadratic'),('gradient','gradient')):
            command=r'\input{'+name+'-body.tex}'
            self.assertIn(command,i)
            self.assertEqual(s.count(command),2)
            self.assertEqual(s.count(r'\label{thm:'+label+'}'),1)
            body=text(f'tests/fixtures/{name}-body.tex')
            self.assertNotIn(r'\label',body)
            self.assertNotIn(r'\begin{theorem}',body)

    def test_fixture_preserves_range_initial_data_rate(self):
        s=text('tests/fixtures/gradient-body.tex')
        for piece in (r'0<\tau<\frac{2}{\lambda_{\max}(A)}',
                      r'For every $x_0\in\mathbb R^m$',r'q^j',r'q=\max_',r'<1'):
            self.assertIn(piece,s)
        self.assertIn(r'$x_j=(-1)^j$',intro(text('tests/fixtures/exposition-smoke.tex')))

    def test_adversarial_cases_cover_known_failures_without_semantic_score(self):
        s=text('tests/fixtures/semantic-cases.md')
        for phrase in ('Only minimization in introduction','Both names, citations',
                       'every positive step size','Move the step-size range',
                       'change just one step-size condition','genuine minimization-only',
                       'right style but leave only result names','broken formulas',
                       'not their arbitrary semantic classification'):
            self.assertIn(phrase,s)

    def test_organizing_question_precedes_local_problems(self):
        s=text('references/research-and-evidence.md')
        self.assertIn('Before choosing local Problems',s)
        self.assertIn('not establish present openness',s)
        self.assertIn('or a new literature cutoff',s)

    def test_no_new_research_schema_or_status(self):
        s=text('references/records-and-delivery.md')
        self.assertIn('schema remains `1.0.0`',s)
        self.assertIn('not the schema',s)
        self.assertIn('not a separate V audit table',text('SKILL.md'))
        self.assertFalse((ROOT/'assets/registries/introduction-pass.csv').exists())

    def test_v6_layout_parameters_and_tools(self):
        s=text('assets/templates/math-review.sty')
        for phrase in ('v1.2.0 Pure Math Survey style','textwidth=6.1in',
                       'top=1.2in,bottom=1.2in',r'\linespread{1.1}',
                       r'\emergencystretch=1.2em',r'\widowpenalty=10000',
                       r'\clubpenalty=10000',r'\pagestyle{plain}',
                       'topsep=0.35\\baselineskip,itemsep=0.15\\baselineskip',
                       r'\RequirePackage{enumitem,needspace}','bookmarksdepth=2'):
            self.assertIn(phrase,s)
        self.assertNotIn(r'\sloppy',s)

    def test_no_subject_macros_leak_into_generic_style(self):
        s=text('assets/templates/math-review.sty')
        for phrase in ('SurfaceCriterionStatement','ddbar','Thomas','dHYM'):
            self.assertNotIn(phrase,s)

    def test_reference_hashes_match_frozen_provenance(self):
        root=ROOT/'assets/reference-samples/dhym-v6'
        provenance=(root/'provenance.toml').read_text()
        for ext in ('tex','pdf'):
            section=provenance.split('[files.'+ext+']',1)[1].split('[files.',1)[0]
            digest=re.search(r'sha256 = "([0-9a-f]{64})"',section).group(1)
            self.assertEqual(hashlib.sha256((root/f'dhym-survey-polished-v6.{ext}').read_bytes()).hexdigest(),digest)
        self.assertIn('frozen = true',provenance)

    def test_known_reference_uses_original_seven_bodies(self):
        s=text('assets/reference-samples/dhym-v6/dhym-survey-polished-v6.tex')
        bodies=re.findall(r'\\newcommand\{\\([A-Za-z]+Statement)\}',s)
        self.assertEqual(len(bodies),7) # This frozen exemplar, not arbitrary output.
        self.assertIn('Version 6',s)

    def test_reference_adapter_preserves_mathematical_body(self):
        s=text('assets/reference-samples/dhym-v6/dhym-survey-polished-v6.tex')
        adapted=build.shared_style_source(s)
        marker=r'\newcommand{\ddbar}'
        self.assertEqual(s[s.index(marker):],adapted[adapted.index(marker):])
        self.assertIn(r'\usepackage{math-review}',adapted)
        self.assertNotIn(r'\usepackage[T1]{fontenc}',adapted)
        self.assertIn('pdfsubject={Version 6:',adapted)

    def test_reference_adapter_fails_closed_on_unknown_input(self):
        with self.assertRaises(ValueError):
            build.shared_style_source(r'\documentclass{article}\begin{document}X\end{document}')

    def test_log_helper_flags_technical_failures(self):
        cases={'undefined_reference':"LaTeX Warning: Reference `x' on page 1 undefined",
               'duplicate_label':'LaTeX Warning: There were multiply-defined labels.',
               'missing_glyph':'Missing character: There is no X in font nullfont!',
               'overflow':r'Overfull \hbox (4.0pt too wide)',
               'fatal':'! Undefined control sequence.',
               'unstable_references':'LaTeX Warning: Label(s) may have changed. Rerun to get cross-references right.'}
        for kind,s in cases.items():
            self.assertIn(kind,build.log_issues(s))

    def test_underfull_is_not_an_overflow_or_semantic_verdict(self):
        self.assertEqual(build.log_issues(r'Underfull \hbox (badness 1292)'),{})

    def test_build_runs_no_shell_escape_and_explains_limits(self):
        s=text('scripts/build_checks.py')
        self.assertIn('"-no-shell-escape"',s)
        self.assertIn('NOT_PERFORMED_BY_THIS_SCRIPT',s)
        self.assertIn('not new research-survey generation',s)


class PackageReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.work=Path(self.temp.name)
        self.root=self.work/'source';self.root.mkdir()
        (self.root/'SKILL.md').write_text('---\nname: pure-math-survey\n---\nFixture\n')
        (self.root/'a.txt').write_text('Synthetic package fixture\n')
        self.output=self.work/'release.zip'

    def test_safe_paths_reject_traversal_and_windows_forms(self):
        for bad in ('','/abs','../x','a/../x','a//x','a\\x','C:/x','a:x','a/./x'):
            self.assertFalse(pack.safe_name(bad),bad)
        self.assertTrue(pack.safe_name('assets/sample.tex'))

    def test_reopen_archive_hashes_and_source_unchanged(self):
        before={p.name:p.read_bytes() for p in self.root.iterdir()}
        r=pack.package(self.root,self.output)
        self.assertEqual(r['verified_member_hashes'],2)
        self.assertEqual(r['members'],3)
        self.assertEqual(pack.verify_archive(self.output),r)
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.root.iterdir()})
        self.assertTrue(self.output.with_suffix('.zip.sha256').is_file())

    def test_deterministic_package(self):
        a=pack.package(self.root,self.output)
        b=pack.package(self.root,self.work/'again.zip')
        self.assertEqual(a['archive_sha256'],b['archive_sha256'])

    def test_reject_existing_output_without_explicit_force(self):
        pack.package(self.root,self.output)
        with self.assertRaises(FileExistsError):
            pack.package(self.root,self.output)

    def test_reject_archive_inside_skill_tree(self):
        with self.assertRaises(ValueError):
            pack.package(self.root,self.root/'inside.zip')

    def test_reject_font_files(self):
        for suffix in pack.FONT_SUFFIXES:
            p=self.root/('font'+suffix);p.write_bytes(b'fixture')
            with self.assertRaisesRegex(ValueError,'Font file'):
                pack.selected_files(self.root)
            p.unlink()

    def test_reject_symlinks(self):
        p=self.root/'link';p.symlink_to(self.root/'a.txt')
        with self.assertRaisesRegex(ValueError,'Symlink'):
            pack.selected_files(self.root)

    def test_generated_auxiliaries_are_excluded(self):
        for name in ('a.aux','a.log','a.toc','a.pyc','a.synctex.gz'):
            (self.root/name).write_text('fixture')
        self.assertEqual(set(pack.selected_files(self.root)),{'SKILL.md','a.txt'})

    def test_corrupted_member_fails_checksum(self):
        pack.package(self.root,self.output)
        with zipfile.ZipFile(self.output) as z:
            entries={info.filename:z.read(info.filename) for info in z.infolist()}
        entries['pure-math-survey/a.txt']=b'changed'
        with zipfile.ZipFile(self.output,'w') as z:
            for name,data in entries.items():z.writestr(name,data)
        with self.assertRaisesRegex(ValueError,'Checksum mismatch'):
            pack.verify_archive(self.output)

    def test_unsafe_archive_member_rejected(self):
        with zipfile.ZipFile(self.output,'w') as z:z.writestr('../escape','x')
        with self.assertRaisesRegex(ValueError,'Unsafe'):
            pack.verify_archive(self.output)

if __name__=='__main__':
    unittest.main()

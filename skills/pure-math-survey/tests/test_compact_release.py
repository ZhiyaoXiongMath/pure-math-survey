"""1.2 regressions: scope, template wiring and page reporting, not mathematical truth."""
from pathlib import Path
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import fitz
ROOT=Path(__file__).resolve().parents[1]
def load(name):
 spec=importlib.util.spec_from_file_location(name,ROOT/'scripts'/f'{name}.py')
 mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
create=load('create_project');budget=load('check_reading_budget')
class SelectionTests(unittest.TestCase):
 def test_suite(self):self.assertEqual(create.parse_selection('suite'),[(p,'concise') for p in range(1,6)])
 def test_explicit_all(self):self.assertEqual(len(create.parse_selection('all')),10)
 def test_single(self):self.assertEqual(create.parse_selection('5:standard'),[(5,'standard')])
 def test_mixed(self):self.assertEqual(create.parse_selection('1:concise, 3:standard'),[(1,'concise'),(3,'standard')])
 def test_duplicates(self):
  with self.assertRaises(ValueError):create.parse_selection('5:concise,5:concise')
 def test_invalid(self):
  for value in ('','0:concise','6:standard','5:short','../suite','all,5:concise'):
   with self.subTest(value=value),self.assertRaises(ValueError):create.parse_selection(value)
 def run_cli(self,out,*extra):return subprocess.run([sys.executable,str(ROOT/'scripts/create_project.py'),'--output',str(out),'--topic','example',*extra],capture_output=True,text=True)
 def test_default_is_v_only_pending(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'project';x=self.run_cli(out);self.assertEqual(x.returncode,0,x.stderr)
   m=json.loads((out/'project-manifest.json').read_text());self.assertEqual(m['requested_documents'],[{'part':5,'edition':'concise'}])
   self.assertEqual(len(list(out.glob('*.tex'))),1);self.assertFalse(list(out.glob('*.pdf')))
   self.assertIn('PENDING',(out/'release-audit.csv').read_text());self.assertNotIn(',PASS,',(out/'release-audit.csv').read_text())
 def test_suite_cli(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'p';x=self.run_cli(out,'--documents','suite');self.assertEqual(x.returncode,0,x.stderr);self.assertEqual(len(list(out.glob('*.tex'))),5)
 def test_no_overwrite(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'p';out.mkdir();(out/'sentinel').write_text('keep');self.assertNotEqual(self.run_cli(out).returncode,0);self.assertEqual((out/'sentinel').read_text(),'keep')
 def test_refuse_skill_child(self):self.assertNotEqual(self.run_cli(ROOT/'unwanted-generated-project').returncode,0)
 def test_all_templates_real_shared_wiring(self):
  files=list((ROOT/'assets/templates').glob('part*.tex'));self.assertEqual(len(files),10)
  for f in files:
   t=f.read_text();intro=t.split(r'\section{Introduction}',1)[1].split(r'\section{',1)[0]
   for name in ('principal','second'):
    self.assertIn(r'\label{thm:'+name+'}',intro);self.assertIn(r'\begin{theoremrecall}{thm:'+name+'}',t)
   self.assertNotIn(r'\tableofcontents',t)
 def test_compact_style_is_canonical(self):self.assertEqual((ROOT/'assets/templates/math-review.sty').read_bytes(),(ROOT/'assets/reference-samples/dhym-compact/math-review.sty').read_bytes())
class TemplateDepthTests(unittest.TestCase):
 def test_standard_has_substantive_depth_prompt(self):
  for p in range(1,6):
   f=next((ROOT/'assets/templates').glob(f'part{p}-*-standard.tex'))
   self.assertIn(r'\label{sec:standard-depth}',f.read_text())
 def test_frontier_templates_have_actual_optional_core_problem(self):
  for p in (4,5):
   for f in (ROOT/'assets/templates').glob(f'part{p}-*.tex'):
    t=f.read_text();intro=t.split(r'\section{Introduction}',1)[1].split(r'\section{',1)[0]
    self.assertIn(r'\begin{problem}\label{prob:core-target}',intro)
    self.assertIn(r'\CoreProblemStatement',intro)
    self.assertIn('not a Problem quota',t)
class BudgetTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);doc=fitz.open();doc.new_page();doc.save(self.root/'a.pdf');doc.close()
  self.man={'requested_documents':[{'part':5,'edition':'concise'}],'documents':[{'part':5,'edition':'concise','pdf_file':'a.pdf'}]}
 def tearDown(self):self.tmp.cleanup()
 def check(self):
  (self.root/'project-manifest.json').write_text(json.dumps(self.man));return budget.check(self.root)
 def test_normal(self):self.assertEqual(self.check()['status'],'WITHIN_BUDGET')
 def test_counts_references_too(self):
  doc=fitz.open();[doc.new_page() for _ in range(11)];doc.save(self.root/'b.pdf');doc.close();self.man['documents'][0]['pdf_file']='b.pdf';self.assertEqual(self.check()['status'],'OVER_BUDGET')
 def test_explicit_limit(self):self.man['documents'][0]['page_review_limit']=1;self.assertEqual(self.check()['documents'][0]['page_review_limit'],1)
 def test_invalid_limit(self):
  for v in (True,False,0,-1,2.5,'5'):
   with self.subTest(value=v):
    self.man['documents'][0]['page_review_limit']=v
    with self.assertRaises(ValueError):self.check()
 def test_traversal(self):
  self.man['documents'][0]['pdf_file']='../a.pdf'
  with self.assertRaises(ValueError):self.check()
 def test_absolute(self):
  self.man['documents'][0]['pdf_file']=str(self.root/'a.pdf')
  with self.assertRaises(ValueError):self.check()
 def test_missing(self):
  self.man['documents'][0]['pdf_file']='missing.pdf'
  with self.assertRaises(FileNotFoundError):self.check()
 def test_empty(self):
  self.man['documents']=[]
  with self.assertRaises(ValueError):self.check()
 def test_mismatch(self):
  self.man['requested_documents'][0]['part']=4
  with self.assertRaises(ValueError):self.check()
 def test_duplicate_documents(self):
  self.man['documents']*=2
  with self.assertRaises(ValueError):self.check()
 def test_duplicate_requests(self):
  self.man['requested_documents']*=2
  with self.assertRaises(ValueError):self.check()
 def test_boolean_part(self):
  self.man['documents'][0]['part']=True
  with self.assertRaises(ValueError):self.check()
 def test_unknown_edition(self):
  self.man['documents'][0]['edition']='short'
  with self.assertRaises(ValueError):self.check()
 def test_corrupt_pdf(self):
  (self.root/'a.pdf').write_text('not a PDF')
  with self.assertRaises(Exception):self.check()
 def test_no_semantic_pass_claim(self):self.assertIn('not a content or visual grade',self.check()['scope'])
if __name__=='__main__':unittest.main()

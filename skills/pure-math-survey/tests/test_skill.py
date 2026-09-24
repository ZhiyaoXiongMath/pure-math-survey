"""Offline source/structural regression tests, not mathematical review.

Run from the skill root: python -B -m unittest discover -s tests -v
All project/PDF fixtures are synthetic and generated in temporary directories.
No TeX build, source verification, PDF rendering or editorial scoring occurs.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_project.py"
spec = importlib.util.spec_from_file_location("project_validator", SCRIPT)
assert spec is not None and spec.loader is not None
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


def dump_csv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def change_row(path: Path, key: str, value: str, updates: dict[str, str]) -> None:
    fields, rows = load_csv(path)
    matched = [row for row in rows if row.get(key) == value]
    if len(matched) != 1:
        raise AssertionError(f"Expected one row {key}={value!r} in {path}")
    matched[0].update(updates)
    dump_csv(path, fields, rows)


def remove_rows(path: Path, key: str, values: set[str]) -> None:
    fields, rows = load_csv(path)
    dump_csv(path, fields, [row for row in rows if row.get(key) not in values])


def hashes(root: Path) -> dict[str, str]:
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob("*")) if p.is_file()}


def make_project(root: Path, selection: list[tuple[int, str]] | None = None,
                 explicit: bool = True) -> dict:
    """Small parser fixtures: PASS strings and PDF signatures are not evidence."""
    if selection is None:
        selection = [(5, "standard")]
    requested = set(selection)
    owner = 2 if any(p == 2 for p, _ in selection) else next(
        (p for p, _ in selection if p != 5), 2)
    root.mkdir(parents=True, exist_ok=True)
    (root / "canonical").mkdir()
    (root / "canonical" / "result.tex").write_text(
        "A synthetic statement used only to exercise file placement.\n", encoding="utf-8")
    documents = []
    for part, edition in selection:
        stem = f"part{part}-{edition}"
        body = r"\section{A structural fixture}\label{sec:fixture}" + "\n"
        if part in {owner, 5}:
            body += r"\label{thm:main}\input{canonical/result.tex}" + "\n"
        (root / f"{stem}.tex").write_text(
            "\\documentclass{article}\n\\begin{document}\n" + body + "\\end{document}\n",
            encoding="utf-8")
        # Only the validator's signature test is exercised; this is not a PDF build.
        (root / f"{stem}.pdf").write_bytes(b"%PDF-1.4\n% synthetic signature-only fixture\n")
        documents.append({"part": part, "edition": edition,
                          "tex_file": stem + ".tex", "pdf_file": stem + ".pdf"})
    manifest = {"schema_version": validator.SCHEMA_VERSION, "language": "en", "documents": documents}
    if explicit:
        manifest["requested_documents"] = [{"part": p, "edition": e} for p, e in selection]
    (root / "project-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    dump_csv(root / "bibliographic-identity.csv", ["source_id", "title"],
             [{"source_id": "S001", "title": "Synthetic identity, not a research source"}])
    dump_csv(root / "proof-mechanism-registry.csv", ["proof_id", "source_ids"], [])
    fields = sorted(validator.MAP_FIELDS | validator.INTEGRATED_MAP_FIELDS)
    row = {key: "" for key in fields}
    row.update(node_id="T001", kind="theorem", owner_part=str(owner),
               canonical_component="canonical/result.tex", source_ids="S001")
    for part, prefix in [(owner, ""), (5, "integrated_")]:
        for edition in sorted(validator.EDITIONS):
            slot = prefix + edition
            if (part, edition) in requested:
                row.update({slot + "_file": f"part{part}-{edition}.tex",
                            slot + "_label": "thm:main", slot + "_treatment": "FULL_STATEMENT"})
            else:
                row[slot + "_treatment"] = "NOT_REQUESTED"
    dump_csv(root / "publication-map.csv", fields, [row])
    checks = validator.REQUIRED_AUDITS | validator.REQUESTED_DOCUMENT_AUDITS
    if any(p == 3 for p, _ in selection):
        checks |= validator.PART_III_AUDITS
    dump_csv(root / "release-audit.csv", ["check", "status", "evidence", "note"], [
        {"check": check, "status": "PASS", "evidence": "synthetic-evidence.md",
         "note": "Synthetic parser fixture; no actual research or review is certified."}
        for check in sorted(checks)])
    (root / "synthetic-evidence.md").write_text(
        "Synthetic parser fixture only. No source, mathematical, build or visual review occurred.\n",
        encoding="utf-8")
    return manifest


class SkillPackageTests(unittest.TestCase):
    def test_package_identity_release_and_schema_versions(self) -> None:
        entry = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue(entry.startswith("---\nname: pure-math-survey\n"))
        version = re.search(r"\*\*Version:\*\* (\d+\.\d+\.\d+)", entry)
        self.assertIsNotNone(version)
        self.assertEqual(version.group(1), "1.2.0")
        # An editorial release does not force an unchanged data schema to migrate.
        self.assertEqual(validator.SCHEMA_VERSION, "1.0.0")
        style = (ROOT / "assets/templates/math-review.sty").read_text(encoding="utf-8")
        self.assertIn("v" + version.group(1) + " Pure Math Survey style", style)
        metadata = (ROOT / "agents/openai.yaml").read_text(encoding="utf-8")
        display_name = re.search(r'^\s*display_name:\s*"([^"\n]+)"\s*$', metadata, re.M)
        self.assertIsNotNone(display_name)
        self.assertEqual(display_name.group(1), "Pure Math Survey")
        self.assertIn("$pure-math-survey", metadata)

    def test_ten_templates_and_manifest_agree(self) -> None:
        manifest = json.loads((ROOT / "assets/project-manifest-template.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], validator.SCHEMA_VERSION)
        self.assertEqual({(d["part"], d["edition"]) for d in manifest["documents"]},
                         validator.COMBINATIONS)
        templates = sorted((ROOT / "assets/templates").glob("part*.tex"))
        self.assertEqual(len(templates), 10)
        for document in manifest["documents"]:
            name = document["tex_file"].removeprefix("[topic]-")
            text = (ROOT / "assets/templates" / name).read_text(encoding="utf-8")
            self.assertIn(r"\usepackage{math-review}", text)
            self.assertIn(r"\documentclass[12pt,reqno]{amsart}", text)
            self.assertIn("% Edition check:", text)
            self.assertLess(text.index(r"\begin{abstract}"), text.index(r"\maketitle"))

    def test_registry_formats_parse_without_prefilled_pass(self) -> None:
        for path in (ROOT / "assets").rglob("*.json"):
            with self.subTest(path=path.name):
                record = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(record["schema_version"], validator.SCHEMA_VERSION)
        for path in (ROOT / "assets").rglob("*.jsonl"):
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if line.strip():
                    with self.subTest(path=path.name, line=number):
                        record = json.loads(line)
                        self.assertEqual(record["schema_version"], validator.SCHEMA_VERSION)
        for path in (ROOT / "assets/registries").glob("*.csv"):
            fields, rows = load_csv(path)
            self.assertEqual(len(fields), len(set(fields)), path.name)
            self.assertTrue(fields, path.name)
            for row in rows:
                self.assertNotIn(None, row, path.name)
                self.assertNotIn(None, row.values(), path.name)
        fields, rows = load_csv(ROOT / "assets/registries/release-audit-template.csv")
        self.assertEqual(fields, ["check", "status", "evidence", "note"])
        self.assertEqual(len(rows), 12)
        self.assertTrue(all(row["status"] == "PENDING" and not row["evidence"] for row in rows))

    def test_relative_markdown_links_and_fragments(self) -> None:
        # This package uses literal inline Markdown links and simple ASCII heading slugs.
        for path in ROOT.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            for destination in re.findall(r"\[[^]\n]+\]\(([^)\s]+)\)", text):
                url = urlsplit(destination)
                if url.scheme or url.netloc:
                    continue
                target = (path.parent / unquote(url.path)).resolve() if url.path else path
                with self.subTest(file=path.name, destination=destination):
                    self.assertTrue(target.is_relative_to(ROOT), destination)
                    self.assertTrue(target.exists(), destination)
                    if url.fragment and target.suffix == ".md":
                        headings = re.findall(r"(?m)^#{1,6}\s+(.+)$", target.read_text(encoding="utf-8"))
                        slugs = {re.sub(r"\s", "-", re.sub(r"[^\w\- ]", "", h.lower()))
                                 for h in headings}
                        self.assertIn(unquote(url.fragment), slugs)

    def test_instruction_sources_are_text_only_and_nonempty(self) -> None:
        for relative in ("SKILL.md", "agents/openai.yaml", "references/validation.md"):
            text = (ROOT / relative).read_text(encoding="utf-8")
            self.assertTrue(text.strip(), relative)
            self.assertNotIn("\x00", text, relative)
        for path in list((ROOT / "references").glob("*.md")) + list((ROOT / "assets/templates").glob("*.tex")):
            text = path.read_bytes().decode("utf-8")
            self.assertNotIn("\r", text, path.name)
            self.assertNotIn("\x00", text, path.name)


    def test_writing_contract_covers_all_requested_preferences(self) -> None:
        text = (ROOT / "references/writing-style.md").read_text(encoding="utf-8")
        for phrase in ("deletion test", "self-contained", "itemize", "enumerate",
                       "secondary consequences", "Repetition is allowed", "quantifiers",
                       "An introduction may consist of definitions", "theoremrecall"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)
        self.assertTrue((ROOT / "references/exposition-examples.md").is_file())

    def test_all_templates_embed_editorial_contract(self) -> None:
        for path in (ROOT / "assets/templates").glob("part*.tex"):
            text = path.read_text(encoding="utf-8")
            with self.subTest(template=path.name):
                self.assertIn("delete trivial transitions", text)
                self.assertIn("useful self-contained repetition", text)
                self.assertIn("itemize/enumerate", text)
                self.assertIn("put secondary consequences afterward", text)
                self.assertIn("definitions and theorems are valid without a narrative roadmap", text)
                self.assertNotIn("state a full result once locally", text)
                introduction = text.split(r"\section{Introduction}", 1)[1].split(r"\section{", 1)[0]
                self.assertIn("Delete transitions", introduction)
                self.assertNotIn("Explain how Section~", introduction)
                if re.search(r"\\begin\{(?:theorem|proposition|problem)\}", text):
                    self.assertIn(r"\begin{itemize}", text)
                    self.assertIn("quantifiers", text)

    def test_no_compulsory_transition_or_single_occurrence_policy(self) -> None:
        banned = ("Each section opens with a short transition",
                  "Introductions must explain the central problem and perspective, then",
                  "Give a full statement one local home",
                  "exactly one input of the canonical body",
                  "Reuse canonical full statements once",
                  "Give each full statement one local home")
        paths = [ROOT / "SKILL.md", *(ROOT / "references").glob("*.md")]
        for path in paths:
            for phrase in banned:
                with self.subTest(file=path.name, phrase=phrase):
                    self.assertNotIn(phrase, path.read_text(encoding="utf-8"))

    def test_smoke_fixture_uses_one_body_and_original_number_recall(self) -> None:
        path = ROOT / "tests/fixtures/exposition-smoke.tex"
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text.count(r"\input{quadratic-body.tex}"), 2)
        self.assertEqual(text.count(r"\label{thm:quadratic}"), 1)
        self.assertIn(r"\begin{theoremrecall}{thm:quadratic}", text)
        self.assertIn(r"\begin{enumerate}", text)
        body = (path.parent / "quadratic-body.tex").read_text(encoding="utf-8")
        self.assertIn(r"\begin{itemize}", body)
        self.assertNotIn(r"\label", body)
        style = (ROOT / "assets/templates/math-review.sty").read_text(encoding="utf-8")
        self.assertIn(r"\newtheorem*{mathreviewrecalledtheorem}", style)
        self.assertIn(r"\newenvironment{theoremrecall}[1]", style)


class ProjectValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory(prefix="pure-math-survey-test-")
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "project"

    def valid(self, **kwargs) -> dict:
        manifest = make_project(self.root, **kwargs)
        self.assertEqual(validator.validate(self.root)[0], [])
        return manifest

    def rejected(self, fragment: str, **kwargs) -> None:
        errors, _ = validator.validate(self.root, **kwargs)
        self.assertTrue(errors, "Expected structural rejection, not a mathematical verdict")
        self.assertIn(fragment, "\n".join(errors))

    def edit_manifest(self, callback) -> None:
        path = self.root / "project-manifest.json"
        manifest = json.loads(path.read_text(encoding="utf-8"))
        callback(manifest)
        path.write_text(json.dumps(manifest), encoding="utf-8")

    def edit_tex(self, text: str, part: int = 5, edition: str = "standard") -> None:
        path = self.root / f"part{part}-{edition}.tex"
        old = path.read_text(encoding="utf-8")
        path.write_text(old.replace(r"\end{document}", text + "\n" + r"\end{document}"), encoding="utf-8")

    def test_v_only_standard_valid_and_read_only(self) -> None:
        self.valid()
        before = hashes(self.root)
        self.assertEqual(validator.validate(self.root)[0], [])
        self.assertEqual(before, hashes(self.root))
        self.assertEqual(len(list(self.root.glob("part*.tex"))), 1)

    def test_each_single_part_edition(self) -> None:
        for part, edition in sorted(validator.COMBINATIONS):
            with self.subTest(part=part, edition=edition):
                root = Path(self.tmp.name) / f"single-{part}-{edition}"
                make_project(root, selection=[(part, edition)])
                self.assertEqual(validator.validate(root)[0], [])

    def test_current_default_is_ten(self) -> None:
        self.valid(selection=sorted(validator.COMBINATIONS), explicit=False)

    def test_current_default_does_not_infer_single_scope(self) -> None:
        make_project(self.root, explicit=False)
        self.rejected("the default ten part/edition combinations")

    def test_eight_documents_require_an_explicit_request(self) -> None:
        selection = [(p, e) for p, e in sorted(validator.COMBINATIONS) if p < 5]
        self.valid(selection=selection)
        self.edit_manifest(lambda m: m.pop("requested_documents"))
        self.rejected("the default ten part/edition combinations")

    def test_eight_document_request_uses_requested_document_checks(self) -> None:
        selection = [(p, e) for p, e in sorted(validator.COMBINATIONS) if p < 5]
        self.valid(selection=selection)
        audit = self.root / "release-audit.csv"
        for prefix in ("build", "visual"):
            change_row(audit, "check", prefix + "_requested_documents",
                       {"check": prefix + "_all_eight"})
        self.rejected("missing required checks")
        self.rejected("build_requested_documents")
        self.rejected("visual_requested_documents")

    def test_empty_or_duplicate_selection_is_rejected(self) -> None:
        for value in ([], [{"part": 5, "edition": "standard"}] * 2):
            make = Path(self.tmp.name) / ("empty" if not value else "duplicate")
            make_project(make)
            path = make / "project-manifest.json"
            data = json.loads(path.read_text(encoding="utf-8")); data["requested_documents"] = value
            path.write_text(json.dumps(data))
            self.assertTrue(validator.validate(make)[0])

    def test_extra_document_does_not_change_request(self) -> None:
        self.valid(selection=[(2, "standard"), (5, "standard")])
        self.edit_manifest(lambda m: m.update(requested_documents=[{"part": 5, "edition": "standard"}]))
        self.rejected("documents must match requested_documents exactly")

    def test_boolean_part_is_rejected(self) -> None:
        self.valid()
        self.edit_manifest(lambda m: m["requested_documents"][0].update(part=True))
        self.rejected("invalid requested_documents")

    def test_missing_or_unsupported_project_version_is_rejected(self) -> None:
        self.valid()
        self.edit_manifest(lambda m: m.pop("schema_version"))
        self.rejected("schema_version must be 1.0.0")
        for value in (None, True, 1, "", "unsupported"):
            with self.subTest(version=value):
                self.edit_manifest(lambda m: m.update(schema_version=value))
                self.rejected("schema_version must be 1.0.0")

    def test_integrated_publication_fields_are_required_without_part_v(self) -> None:
        self.valid(selection=[(2, "standard")])
        path = self.root / "publication-map.csv"
        fields, rows = load_csv(path)
        fields = [field for field in fields if field not in validator.INTEGRATED_MAP_FIELDS]
        dump_csv(path, fields, [{field: row[field] for field in fields} for row in rows])
        self.rejected("missing columns")

    def test_v_does_not_require_iii_rows(self) -> None:
        self.valid()
        _, rows = load_csv(self.root / "release-audit.csv")
        self.assertFalse(validator.PART_III_AUDITS & {row["check"] for row in rows})

    def test_v_accepts_reasoned_iii_nonapplicability(self) -> None:
        self.valid()
        path = self.root / "release-audit.csv"
        fields, rows = load_csv(path)
        rows += [{"check": check, "status": "NOT_APPLICABLE", "evidence": "",
                  "note": "No Part III requested."} for check in sorted(validator.PART_III_AUDITS)]
        dump_csv(path, fields, rows)
        self.assertEqual(validator.validate(self.root)[0], [])
        change_row(path, "check", "proof_framework", {"note": ""})
        self.rejected("not an accepted completed status")

    def test_mixed_iii_v_requires_iii_review(self) -> None:
        self.valid(selection=[(3, "concise"), (5, "standard")])
        remove_rows(self.root / "release-audit.csv", "check", validator.PART_III_AUDITS)
        self.rejected("missing required checks")

    def test_requested_iii_cannot_waive_mechanism_review(self) -> None:
        self.valid(selection=[(3, "standard")])
        change_row(self.root / "release-audit.csv", "check", "decisive_mechanisms",
                   {"status": "NOT_APPLICABLE", "note": "Attempted waiver"})
        self.rejected("decisive_mechanisms is NOT_APPLICABLE")

    def test_frontier_scope_waiver(self) -> None:
        self.valid(selection=[(1, "concise")])
        change_row(self.root / "release-audit.csv", "check", "frontier_status",
                   {"status": "NOT_APPLICABLE", "note": "No frontier in this foundations-only scope."})
        self.assertEqual(validator.validate(self.root)[0], [])
        for part in (4, 5):
            root = Path(self.tmp.name) / f"frontier-{part}"
            make_project(root, selection=[(part, "standard")])
            change_row(root / "release-audit.csv", "check", "frontier_status",
                       {"status": "NOT_APPLICABLE", "note": "No list found; invalid waiver."})
            self.assertIn("frontier_status is NOT_APPLICABLE", "\n".join(validator.validate(root)[0]))

    def test_pending_audit_and_no_evidence_rejected(self) -> None:
        self.valid()
        audit = self.root / "release-audit.csv"
        change_row(audit, "check", "edition_depth", {"status": "PENDING"})
        self.rejected("edition_depth is PENDING")
        change_row(audit, "check", "edition_depth", {"status": "PASS", "evidence": ""})
        self.rejected("completed status but no evidence")

    def test_unmet_check_not_passed_by_limitation_note(self) -> None:
        self.valid()
        change_row(self.root / "release-audit.csv", "check", "visual_requested_documents",
                   {"status": "PENDING", "note": "Only a sample was seen; not a full-page review."})
        self.rejected("visual_requested_documents is PENDING")

    def test_no_new_completed_status(self) -> None:
        self.valid()
        change_row(self.root / "release-audit.csv", "check", "reader_outcomes",
                   {"status": "PASS_WITH_WARNINGS"})
        self.rejected("not an accepted completed status")

    def test_template_mode_is_explicitly_not_publication(self) -> None:
        self.valid()
        self.edit_tex(r"\placeholder{Insert mathematics here.}")
        change_row(self.root / "release-audit.csv", "check", "reader_outcomes", {"status": "PENDING"})
        self.rejected("unresolved manuscript placeholder")
        errors, notes = validator.validate(self.root, template_mode=True)
        self.assertEqual(errors, [])
        self.assertTrue(any("PENDING" in note for note in notes))

    def test_repeated_full_statement_is_allowed(self) -> None:
        self.valid()
        self.edit_tex(r"\begin{theoremrecall}{thm:main}\input{canonical/result.tex}\end{theoremrecall}")
        errors, notes = validator.validate(self.root)
        self.assertEqual(errors, [])
        self.assertTrue(any("useful local recalls are allowed" in note for note in notes))

    def test_repeated_full_statement_does_not_permit_duplicate_labels(self) -> None:
        self.valid()
        self.edit_tex(r"\label{thm:main}\input{canonical/result.tex}")
        self.rejected("duplicate labels")

    def test_repeated_body_is_allowed_in_every_single_part_edition(self) -> None:
        for part, edition in sorted(validator.COMBINATIONS):
            with self.subTest(part=part, edition=edition):
                root = Path(self.tmp.name) / f"recall-{part}-{edition}"
                make_project(root, selection=[(part, edition)])
                path = root / f"part{part}-{edition}.tex"
                text = path.read_text(encoding="utf-8")
                text = text.replace(r"\end{document}",
                                    r"\input{canonical/result.tex}\end{document}")
                path.write_text(text, encoding="utf-8")
                self.assertEqual(validator.validate(root)[0], [])

    def test_full_statement_still_requires_a_canonical_input(self) -> None:
        self.valid()
        path = self.root / "part5-standard.tex"
        path.write_text(path.read_text(encoding="utf-8").replace(r"\input{canonical/result.tex}", ""),
                        encoding="utf-8")
        self.rejected("canonical component input count 0; expected at least 1")

    def test_reference_only_still_rejects_full_body_inputs(self) -> None:
        self.valid()
        change_row(self.root / "publication-map.csv", "node_id", "T001",
                   {"integrated_standard_treatment": "REFERENCE_ONLY",
                    "limitation_note": "Not permission to include a full statement."})
        self.rejected("canonical component input count 1; expected 0")
        self.edit_tex(r"\input{canonical/result.tex}")
        self.rejected("canonical component input count 2; expected 0")

    def test_canonical_body_must_not_contain_labels(self) -> None:
        self.valid()
        (self.root / "canonical/result.tex").write_text(
            r"\label{eq:unsafe}A body with a label.", encoding="utf-8")
        self.rejected("canonical component must be label-free")

    def test_canonical_body_must_not_contain_recall_wrapper(self) -> None:
        self.valid()
        (self.root / "canonical/result.tex").write_text(
            r"\begin{theoremrecall}{thm:main}A body.\end{theoremrecall}", encoding="utf-8")
        self.rejected("canonical component must contain mathematical body only")

    def test_listed_hypotheses_in_canonical_body_are_allowed(self) -> None:
        self.valid()
        (self.root / "canonical/result.tex").write_text(
            r"Assume both: \begin{itemize}\item $a>0$.\item $b>0$.\end{itemize}"
            r"Then $a+b>0$.", encoding="utf-8")
        self.assertEqual(validator.validate(self.root)[0], [])

    def test_v_standard_reference_only_is_valid(self) -> None:
        self.valid()
        path = self.root / "part5-standard.tex"
        path.write_text(path.read_text(encoding="utf-8").replace(r"\input{canonical/result.tex}", "A located synthetic reference."))
        change_row(self.root / "publication-map.csv", "node_id", "T001",
                   {"integrated_standard_treatment": "REFERENCE_ONLY",
                    "limitation_note": "Synthetic treatment test, not a quality judgment."})
        self.assertEqual(validator.validate(self.root)[0], [])
        change_row(self.root / "publication-map.csv", "node_id", "T001", {"limitation_note": ""})
        self.rejected("REFERENCE_ONLY needs a limitation_note")

    def test_owner_standard_still_requires_full_statement(self) -> None:
        self.valid(selection=[(2, "standard")])
        path = self.root / "part2-standard.tex"
        path.write_text(path.read_text(encoding="utf-8").replace(r"\input{canonical/result.tex}", "A reference."))
        change_row(self.root / "publication-map.csv", "node_id", "T001",
                   {"standard_treatment": "REFERENCE_ONLY", "limitation_note": "Not allowed here."})
        self.rejected("standard edition must use FULL_STATEMENT")

    def test_v_omission_requires_no_input_and_another_actual_placement(self) -> None:
        self.valid(selection=[(2, "standard"), (5, "standard")])
        changes = {"integrated_standard_treatment": "OMITTED_WITH_REASON",
                   "integrated_standard_file": "", "integrated_standard_label": "",
                   "limitation_note": "Supplement outside the selected V thread."}
        change_row(self.root / "publication-map.csv", "node_id", "T001", changes)
        self.rejected("omitted integrated_standard node still inputs")
        path = self.root / "part5-standard.tex"
        path.write_text(path.read_text(encoding="utf-8").replace(r"\label{thm:main}\input{canonical/result.tex}", ""))
        self.assertEqual(validator.validate(self.root)[0], [])

    def test_completely_unused_node_is_rejected(self) -> None:
        self.valid()
        path = self.root / "part5-standard.tex"
        path.write_text(path.read_text(encoding="utf-8").replace(r"\label{thm:main}\input{canonical/result.tex}", ""))
        change_row(self.root / "publication-map.csv", "node_id", "T001",
                   {"integrated_standard_treatment": "OMITTED_WITH_REASON",
                    "integrated_standard_file": "", "integrated_standard_label": "",
                    "limitation_note": "No placement remains."})
        self.rejected("no public placement")

    def test_not_requested_is_not_omitted(self) -> None:
        self.valid()
        change_row(self.root / "publication-map.csv", "node_id", "T001",
                   {"integrated_standard_treatment": "NOT_REQUESTED"})
        self.rejected("requested integrated_standard cannot use NOT_REQUESTED")

    def test_unknown_source_and_proof_ids(self) -> None:
        self.valid()
        change_row(self.root / "publication-map.csv", "node_id", "T001",
                   {"source_ids": "S999", "proof_ids": "P999"})
        self.rejected("unknown source_ids")
        self.rejected("unknown proof_ids")

    def test_canonical_body_cannot_contain_wrapper(self) -> None:
        self.valid()
        (self.root / "canonical/result.tex").write_text(r"\begin{theorem}A claim.\end{theorem}")
        self.rejected("canonical component must contain mathematical body only")

    def test_portable_path_policy(self) -> None:
        for path in ("../outside.tex", "/outside.tex", "C:/file.tex", "x\\y.tex", "a//b", "./file", "a/../b", "a:b", ""):
            with self.subTest(path=path):
                self.assertFalse(validator.safe_relative(path))
        for path in ("canonical/result.tex", "parts/part-1.tex", "file with spaces.tex"):
            self.assertTrue(validator.safe_relative(path))
        self.valid()
        self.edit_manifest(lambda m: m["documents"][0].update(tex_file="../outside.tex"))
        self.rejected("unsafe relative path")

    def test_escaping_symlink_rejected_where_supported(self) -> None:
        self.valid()
        outside = Path(self.tmp.name) / "outside.tex"
        outside.write_text("Outside the project.")
        link = self.root / "escape.tex"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"Symlink creation unavailable on this host: {exc}")
        self.edit_manifest(lambda m: m["documents"][0].update(tex_file="escape.tex"))
        self.rejected("path escapes project root")

    def test_input_cycle_and_dynamic_input_rejected(self) -> None:
        self.valid()
        (self.root / "canonical/result.tex").write_text(r"\input{canonical/result.tex}")
        self.rejected("cyclic TeX input")
        (self.root / "canonical/result.tex").write_text("Synthetic body.")
        self.edit_tex(r"\input canonical/result.tex")
        self.rejected("unsupported input syntax")

    def test_internal_audit_metadata_not_printed(self) -> None:
        self.valid()
        self.edit_tex(r"\section{T001 internal record}")
        self.rejected("reader-facing internal T/P/S coordinate")

    def test_legitimate_mathematical_symbol_is_not_an_audit_id(self) -> None:
        self.valid()
        self.edit_tex(r"The symbol $T12$ is just a mathematical label in this parser fixture.")
        self.assertEqual(validator.validate(self.root)[0], [])

    def test_signature_and_missing_file_checks(self) -> None:
        self.valid()
        pdf = self.root / "part5-standard.pdf"
        pdf.write_bytes(b"Not a PDF")
        self.rejected("PDF does not have a PDF signature")
        pdf.unlink()
        self.rejected("missing file part5-standard.pdf")

    def test_csv_width_and_duplicate_header_checks(self) -> None:
        self.valid()
        path = self.root / "bibliographic-identity.csv"
        path.write_text("source_id,title\nS001,Title,Unexpected field\n")
        self.rejected("row width does not match header")
        path.write_text("source_id,source_id\nS001,S001\n")
        self.rejected("duplicate CSV columns")

    def test_cli_verdict_and_no_certification(self) -> None:
        self.valid()
        process = subprocess.run([sys.executable, "-B", str(SCRIPT), str(self.root)],
                                 capture_output=True, text=True, timeout=20, check=False)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertIn("no mathematical or publication-readiness certification", process.stdout)
        (self.root / "project-manifest.json").unlink()
        process = subprocess.run([sys.executable, "-B", str(SCRIPT), str(self.root)],
                                 capture_output=True, text=True, timeout=20, check=False)
        self.assertEqual(process.returncode, 1)
        self.assertIn("PROJECT STRUCTURAL VALIDATION FAILED", process.stderr)


if __name__ == "__main__":
    unittest.main()

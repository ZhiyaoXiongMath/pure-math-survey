#!/usr/bin/env python3
"""Focused positive/negative regression fixtures; synthetic metadata is not evidence."""
from __future__ import annotations

import csv
import itertools
import json
import os
import shutil
import stat
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
REPOSITORY = Path(__file__).resolve().parents[2]
ROOT = Path(os.environ.get("PMSR_SKILL_ROOT", str(REPOSITORY / "skills/pure-math-systematic-review"))).resolve()
sys.path.insert(0, str(REPOSITORY / "dev"))
sys.path.insert(0, str(ROOT / "scripts"))
import validate_project as project  # noqa: E402
import validate_skill as skill  # noqa: E402


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def make_project(root: Path, requested: set[tuple[int, str]] | None = None,
                 schema_version: str = "0.8.0", owner_part: int | None = None) -> None:
    documents = []
    legacy = schema_version == project.LEGACY_SCHEMA_VERSION
    defaults = project.LEGACY_COMBINATIONS if legacy else project.COMBINATIONS
    combinations = defaults if requested is None else requested
    owner = owner_part or (2 if any(part in {2, 5} for part, _ in combinations)
                           else min(part for part, _ in combinations))
    component = root / "generated/group-order.tex"
    component.parent.mkdir()
    component.write_text("Let $G$ be a finite group and $H$ a subgroup of $G$. Then $|H|$ divides $|G|$.\n", encoding="utf-8")
    for part, edition in sorted(combinations):
        stem = f"part{part}-{edition}"
        content = "\\section{Introduction}\nThis algebra example tests structural validation.\n"
        if part in {owner, 5}:
            content += "\\begin{theorem}\\label{thm:group-order}\n\\input{generated/group-order.tex}\n\\end{theorem}\n"
        (root / (stem + ".tex")).write_text("\\documentclass{article}\n\\begin{document}\n" + content + "\\end{document}\n", encoding="utf-8")
        # Only the signature/existence gate is tested; these are not readable PDFs.
        (root / (stem + ".pdf")).write_bytes(b"%PDF-1.4\n% synthetic fixture, not a publication\n")
        documents.append({"part": part, "edition": edition, "tex_file": stem + ".tex", "pdf_file": stem + ".pdf"})
    manifest = {"schema_version": schema_version, "language": "en", "documents": documents}
    if requested is not None:
        manifest["requested_documents"] = [{"part": part, "edition": edition} for part, edition in sorted(requested)]
    (root / "project-manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    write_csv(root / "bibliographic-identity.csv", ["source_id", "title"], [{"source_id": "S01", "title": "Synthetic algebra fixture identity"}])
    write_csv(root / "proof-mechanism-registry.csv", ["proof_id", "source_ids"], [{"proof_id": "P01", "source_ids": "S01"}])
    row = {"node_id": "T01", "kind": "theorem", "owner_part": str(owner), "canonical_component": "generated/group-order.tex",
           "source_ids": "S01", "proof_ids": "P01", "limitation_note": ""}
    placements = [(owner, edition, edition) for edition in project.EDITIONS]
    if not legacy:
        placements += [(5, edition, f"integrated_{edition}") for edition in project.EDITIONS]
    for part, edition, prefix in placements:
        selected = (part, edition) in combinations
        row.update({f"{prefix}_file": f"part{part}-{edition}.tex" if selected else "",
                    f"{prefix}_label": "thm:group-order" if selected else "",
                    f"{prefix}_treatment": "FULL_STATEMENT" if selected else "NOT_REQUESTED"})
    fields = project.MAP_FIELDS if legacy else project.MAP_FIELDS | project.INTEGRATED_MAP_FIELDS
    write_csv(root / "publication-map.csv", sorted(fields), [row])
    audits = set(project.REQUIRED_AUDITS)
    if any(part == 3 for part, _ in combinations):
        audits |= project.PART_III_AUDITS
    if requested is not None or not legacy:
        audits -= {"build_all_eight", "visual_all_eight"}
        audits |= project.REQUESTED_DOCUMENT_AUDITS
    write_csv(root / "release-audit.csv", ["check", "status", "evidence", "note"], [
        {"check": check, "status": "PASS", "evidence": "Synthetic parser fixture only", "note": "This does not certify mathematics."}
        for check in sorted(audits)])


class ProjectChecks(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="pmreview-project-fixture-")
        self.root = Path(self.temporary.name)
        make_project(self.root)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def assert_rejected(self, fragment: str) -> None:
        errors, _ = project.validate(self.root)
        self.assertTrue(errors, "negative fixture unexpectedly passed")
        self.assertIn(fragment.lower(), "\n".join(errors).lower())

    def edit_csv(self, filename: str, edit) -> None:
        path = self.root / filename
        with path.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            fields, rows = reader.fieldnames, list(reader)
        edit(rows)
        write_csv(path, fields, rows)

    def edit_manifest(self, edit) -> None:
        path = self.root / "project-manifest.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        edit(data)
        path.write_text(json.dumps(data), encoding="utf-8")

    def select_documents(self, requested: set[tuple[int, str]]) -> None:
        """Restrict the existing fixture; unrequested files are absent, not faked."""
        def update_manifest(data):
            data["requested_documents"] = [{"part": part, "edition": edition} for part, edition in sorted(requested)]
            kept = []
            for document in data["documents"]:
                if (document["part"], document["edition"]) in requested:
                    kept.append(document)
                else:
                    for field in ("tex_file", "pdf_file"):
                        (self.root / document[field]).unlink()
            data["documents"] = kept
        self.edit_manifest(update_manifest)
        def update_mapping(rows):
            for row in rows:
                for edition in project.EDITIONS:
                    if (int(row["owner_part"]), edition) not in requested:
                        row.update({f"{edition}_file": "", f"{edition}_label": "", f"{edition}_treatment": "NOT_REQUESTED"})
        self.edit_csv("publication-map.csv", update_mapping)
        self.edit_csv("release-audit.csv", lambda rows: [
            row.update(check=row["check"].replace("all_eight", "requested_documents")) for row in rows])
        if not any(part == 3 for part, _ in requested):
            self.edit_csv("release-audit.csv", lambda rows: rows.__setitem__(
                slice(None), [row for row in rows if row["check"] not in project.PART_III_AUDITS]))

    def test_algebra_does_not_require_pde_or_display_count(self) -> None:
        self.assertEqual(project.validate(self.root)[0], [])

    def test_every_single_document_can_be_requested(self) -> None:
        for key in sorted(project.COMBINATIONS):
            with self.subTest(document=key):
                root = self.root / f"single-{key[0]}-{key[1]}"
                root.mkdir()
                make_project(root, {key}, schema_version="0.9.0")
                self.assertEqual(project.validate(root)[0], [])

    def test_every_legacy_nonempty_document_subset_is_supported(self) -> None:
        combinations = sorted(project.LEGACY_COMBINATIONS)
        for size in range(1, len(combinations) + 1):
            for number, selection in enumerate(itertools.combinations(combinations, size)):
                with self.subTest(selection=selection):
                    root = self.root / f"selection-{size}-{number}"
                    root.mkdir()
                    make_project(root, set(selection))
                    self.assertEqual(project.validate(root)[0], [])

    def test_single_concise_does_not_require_standard_artifacts(self) -> None:
        self.select_documents({(2, "concise")})
        self.assertFalse((self.root / "part2-standard.tex").exists())
        self.assertEqual(project.validate(self.root)[0], [])

    def test_single_standard_does_not_require_concise_artifacts(self) -> None:
        self.select_documents({(2, "standard")})
        self.assertFalse((self.root / "part2-concise.pdf").exists())
        self.assertEqual(project.validate(self.root)[0], [])

    def test_mixed_partial_delivery(self) -> None:
        self.select_documents({(1, "concise"), (2, "concise"), (2, "standard"), (4, "standard")})
        self.assertEqual(project.validate(self.root)[0], [])

    def test_explicit_full_selection_accepts_legacy_audits(self) -> None:
        self.edit_manifest(lambda data: data.update(requested_documents=[
            {"part": part, "edition": edition} for part, edition in sorted(project.LEGACY_COMBINATIONS)]))
        self.assertEqual(project.validate(self.root)[0], [])

    def test_full_delivery_accepts_generic_audits(self) -> None:
        self.edit_csv("release-audit.csv", lambda rows: [
            row.update(check=row["check"].replace("all_eight", "requested_documents")) for row in rows])
        self.assertEqual(project.validate(self.root)[0], [])

    def test_partial_missing_requested_document(self) -> None:
        self.select_documents({(2, "concise"), (2, "standard")})
        self.edit_manifest(lambda data: data["documents"].pop())
        self.assert_rejected("missing=[(2, 'standard')]")

    def test_partial_extra_document_is_rejected(self) -> None:
        self.edit_manifest(lambda data: data.update(requested_documents=[{"part": 2, "edition": "standard"}]))
        self.assert_rejected("extra=[")

    def test_partial_duplicate_document_is_rejected(self) -> None:
        self.select_documents({(2, "standard")})
        self.edit_manifest(lambda data: data["documents"].append(dict(data["documents"][0])))
        self.assert_rejected("duplicate document combination")

    def test_invalid_requested_document_selections(self) -> None:
        selections = [
            [], None, {}, "all", [None],
            [{"part": 2}], [{"part": 2, "edition": "concise", "extra": True}],
            [{"part": 0, "edition": "concise"}], [{"part": 5, "edition": "standard"}],
            [{"part": True, "edition": "concise"}], [{"part": "2", "edition": "concise"}],
            [{"part": 2, "edition": "brief"}], [{"part": 2, "edition": []}],
            [{"part": 2, "edition": "concise"}, {"part": 2, "edition": "concise"}],
        ]
        for selection in selections:
            with self.subTest(selection=selection):
                self.edit_manifest(lambda data: data.update(requested_documents=selection))
                self.assert_rejected("requested_documents")

    def test_not_requested_cannot_skip_a_requested_mapping(self) -> None:
        self.select_documents({(2, "concise")})
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            concise_treatment="NOT_REQUESTED", concise_file="", concise_label=""))
        self.assert_rejected("requested concise cannot use NOT_REQUESTED")

    def test_unrequested_mapping_requires_marker_and_empty_coordinates(self) -> None:
        self.select_documents({(2, "standard")})
        invalid = [
            {"concise_treatment": "OMITTED_WITH_REASON", "limitation_note": "Unrequested."},
            {"concise_treatment": "FULL_STATEMENT"},
            {"concise_treatment": "NOT_REQUESTED", "concise_file": "part2-concise.tex"},
            {"concise_treatment": "NOT_REQUESTED", "concise_file": "", "concise_label": "thm:group-order"},
        ]
        for update in invalid:
            with self.subTest(update=update):
                self.edit_csv("publication-map.csv", lambda rows: rows[0].update(update))
                self.assert_rejected("unrequested concise must use NOT_REQUESTED with empty file/label")

    def test_mapping_owned_by_unrequested_part_is_rejected(self) -> None:
        self.select_documents({(1, "concise")})
        self.assert_rejected("owner_part has no requested document")

    def test_omitted_only_mapping_is_unrelated_to_delivery(self) -> None:
        self.select_documents({(2, "concise")})
        path = self.root / "part2-concise.tex"
        path.write_text(path.read_text().replace("\\input{generated/group-order.tex}", ""))
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            concise_treatment="OMITTED_WITH_REASON", concise_file="", concise_label="",
            limitation_note="This result only belongs to the unrequested standard edition."))
        self.assert_rejected("no public placement in a requested document")

    def test_partial_concise_reference_only_remains_supported(self) -> None:
        self.select_documents({(2, "concise")})
        path = self.root / "part2-concise.tex"
        path.write_text(path.read_text().replace("\\input{generated/group-order.tex}", "See the statement in the cited source, Theorem 1."))
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            concise_treatment="REFERENCE_ONLY", limitation_note="Full statement is in the located source."))
        self.assertEqual(project.validate(self.root)[0], [])

    def test_partial_requested_pair_allows_justified_concise_omission(self) -> None:
        self.select_documents({(2, "concise"), (2, "standard")})
        path = self.root / "part2-concise.tex"
        path.write_text(path.read_text().replace("\\input{generated/group-order.tex}", ""))
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            concise_treatment="OMITTED_WITH_REASON", concise_file="", concise_label="",
            limitation_note="Supplementary result in the requested standard edition."))
        self.assertEqual(project.validate(self.root)[0], [])

    def test_partial_standard_still_requires_full_statement(self) -> None:
        self.select_documents({(2, "standard")})
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            standard_treatment="REFERENCE_ONLY", limitation_note="Deferred to a source."))
        self.assert_rejected("standard edition must use FULL_STATEMENT")

    def test_partial_cannot_reuse_all_eight_audit_names(self) -> None:
        self.select_documents({(2, "standard")})
        self.edit_csv("release-audit.csv", lambda rows: [
            row.update(check=row["check"].replace("requested_documents", "all_eight")) for row in rows])
        self.assert_rejected("build_requested_documents")
        self.assert_rejected("visual_requested_documents")

    def test_partial_build_and_visual_cannot_be_not_applicable(self) -> None:
        self.select_documents({(2, "standard")})
        for check in sorted(project.REQUESTED_DOCUMENT_AUDITS):
            with self.subTest(check=check):
                self.edit_csv("release-audit.csv", lambda rows: [
                    row.update(status="NOT_APPLICABLE", note="Only one document requested.")
                    for row in rows if row["check"] == check])
                self.assert_rejected(f"{check} is NOT_APPLICABLE")
                self.edit_csv("release-audit.csv", lambda rows: [
                    row.update(status="PASS") for row in rows if row["check"] == check])

    def test_single_edition_does_not_bypass_semantic_audit(self) -> None:
        self.select_documents({(2, "standard")})
        self.edit_csv("release-audit.csv", lambda rows: [
            row.update(status="NOT_APPLICABLE", note="Only one edition requested.")
            for row in rows if row["check"] == "edition_semantic_consistency"])
        self.assert_rejected("edition_semantic_consistency is NOT_APPLICABLE")

    def test_partial_still_checks_source_and_proof_ids(self) -> None:
        self.select_documents({(2, "standard")})
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(source_ids="S99", proof_ids="P99"))
        self.assert_rejected("unknown source_ids")
        self.assert_rejected("unknown proof_ids")

    def test_missing_edition(self) -> None:
        path = self.root / "project-manifest.json"
        data = json.loads(path.read_text())
        data["documents"].pop()
        path.write_text(json.dumps(data))
        self.assert_rejected("eight")

    def test_empty_documents(self) -> None:
        path = self.root / "project-manifest.json"
        data = json.loads(path.read_text())
        data["documents"] = []
        path.write_text(json.dumps(data))
        self.assert_rejected("nonempty")

    def test_unknown_source(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(source_ids="S99"))
        self.assert_rejected("unknown source_ids")

    def test_unknown_proof(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(proof_ids="P99"))
        self.assert_rejected("unknown proof_ids")

    def test_changed_canonical_reference(self) -> None:
        source = self.root / "part2-concise.tex"
        source.write_text(source.read_text().replace("generated/group-order.tex", "generated/changed.tex"))
        (self.root / "generated/changed.tex").write_text("An altered statement missing the subgroup hypothesis.")
        self.assert_rejected("canonical component input count")

    def test_unsafe_component_path(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(canonical_component="../outside.tex"))
        self.assert_rejected("unsafe relative path")

    def test_windows_drive_path(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(canonical_component="C:/outside.tex"))
        self.assert_rejected("unsafe relative path")

    def test_reader_audit_card(self) -> None:
        path = self.root / "part4-standard.tex"
        path.write_text(path.read_text().replace("\\end{document}", "\\begin{theoremdossierbox}Verification depth: pending\\end{theoremdossierbox}\n\\end{document}"))
        self.assert_rejected("reader-facing audit card")

    def test_public_internal_id(self) -> None:
        path = self.root / "part3-standard.tex"
        path.write_text(path.read_text().replace("\\end{document}", "\\paragraph{Mechanism P01}Proof details.\\end{document}"))
        self.assert_rejected("internal T/P/S")

    def test_legitimate_mathematical_symbol(self) -> None:
        path = self.root / "part3-standard.tex"
        path.write_text(path.read_text().replace("\\end{document}", "Write $P01$ for this polynomial.\\end{document}"))
        self.assertEqual(project.validate(self.root)[0], [])

    def test_title_author_date_placeholders(self) -> None:
        for placeholder in ("[Review topic]", "[Author name]", "[Prepared date; literature cutoff date]"):
            path = self.root / "part1-concise.tex"
            original = path.read_text()
            path.write_text(original.replace("\\end{document}", placeholder + "\\end{document}"))
            self.assert_rejected("placeholder")
            path.write_text(original)

    def test_reference_template_macro(self) -> None:
        path = self.root / "part1-concise.tex"
        path.write_text(path.read_text().replace("\\end{document}", "\\templatereferences\\end{document}"))
        self.assert_rejected("placeholder")

    def test_placeholder_is_template_only(self) -> None:
        path = self.root / "part1-concise.tex"
        path.write_text(path.read_text().replace("\\end{document}", "\\placeholder{topic}\\end{document}"))
        self.assert_rejected("placeholder")
        self.assertEqual(project.validate(self.root, template_mode=True)[0], [])

    def test_pending_audit_is_not_a_pass(self) -> None:
        self.edit_csv("release-audit.csv", lambda rows: rows[0].update(status="PENDING"))
        self.assert_rejected("not an accepted completed status")
        self.assertEqual(project.validate(self.root, template_mode=True)[0], [])

    def test_arbitrary_status_is_not_a_pass(self) -> None:
        self.edit_csv("release-audit.csv", lambda rows: rows[0].update(status="LOOKS_FINE"))
        self.assert_rejected("not an accepted completed status")

    def test_missing_human_audit(self) -> None:
        (self.root / "release-audit.csv").unlink()
        self.assert_rejected("missing release-audit")

    def test_concise_reference_only(self) -> None:
        path = self.root / "part2-concise.tex"
        path.write_text(path.read_text().replace("\\input{generated/group-order.tex}", "See the full statement in the standard edition."))
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(concise_treatment="REFERENCE_ONLY", limitation_note="Statement deferred to the standard edition."))
        self.assertEqual(project.validate(self.root)[0], [])

    def test_concise_omission_with_reason(self) -> None:
        path = self.root / "part2-concise.tex"
        path.write_text(path.read_text().replace("\\input{generated/group-order.tex}", ""))
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(concise_treatment="OMITTED_WITH_REASON", concise_file="", concise_label="", limitation_note="Auxiliary result outside the frozen concise core."))
        self.assertEqual(project.validate(self.root)[0], [])

    def test_omission_without_reason_fails(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(concise_treatment="OMITTED_WITH_REASON", concise_file="", concise_label=""))
        self.assert_rejected("requires a concise or Part V placement, empty file/label and a limitation_note")

    def test_claimed_omission_still_inputs_body(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(concise_treatment="OMITTED_WITH_REASON", concise_file="", concise_label="", limitation_note="Declared omitted."))
        self.assert_rejected("omitted concise node still inputs")

    def test_reference_only_without_note(self) -> None:
        path = self.root / "part2-concise.tex"
        path.write_text(path.read_text().replace("\\input{generated/group-order.tex}", "See the standard edition."))
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(concise_treatment="REFERENCE_ONLY"))
        self.assert_rejected("REFERENCE_ONLY needs a limitation_note")

    def test_missing_release_check(self) -> None:
        self.edit_csv("release-audit.csv", lambda rows: rows.pop())
        self.assert_rejected("missing required checks")

    def test_frontier_not_applicable_needs_note(self) -> None:
        self.select_documents({(2, "standard")})
        self.edit_csv("release-audit.csv", lambda rows: [row.update(status="NOT_APPLICABLE", note="No frontier assertions in the frozen scope.") for row in rows if row["check"] == "frontier_status"])
        self.assertEqual(project.validate(self.root)[0], [])
        self.edit_csv("release-audit.csv", lambda rows: [row.update(note="") for row in rows if row["check"] == "frontier_status"])
        self.assert_rejected("not an accepted completed status")

    def test_completed_audit_requires_evidence(self) -> None:
        self.edit_csv("release-audit.csv", lambda rows: rows[0].update(evidence=""))
        self.assert_rejected("no evidence record")

    def test_ragged_publication_map_reports_errors_without_crashing(self) -> None:
        path = self.root / "publication-map.csv"
        fields = sorted(project.MAP_FIELDS)
        with path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(fields)
            writer.writerow(["generated/group-order.tex"])
        self.assert_rejected("row width does not match header")

    def test_old_schema_needs_new_reviews_without_manifest_migration(self) -> None:
        path = self.root / "release-audit.csv"
        completed = path.read_text(encoding="utf-8")
        new_checks = {"reader_outcomes", "edition_depth"} | project.PART_III_AUDITS
        self.edit_csv("release-audit.csv", lambda rows: rows.__setitem__(
            slice(None), [row for row in rows if row["check"] not in new_checks]))
        self.assert_rejected("missing required checks")
        path.write_text(completed, encoding="utf-8")
        self.assertEqual(json.loads((self.root / "project-manifest.json").read_text())["schema_version"], "0.8.0")
        self.assertEqual(project.validate(self.root)[0], [])

    def test_explanation_audits_require_records_status_and_evidence(self) -> None:
        path = self.root / "release-audit.csv"
        original = path.read_text(encoding="utf-8")
        checks = {"reader_outcomes", "edition_depth"} | project.PART_III_AUDITS
        for check in sorted(checks):
            for defect in ("missing", "empty_status", "pending", "incomplete", "limited", "limited_delivery", "empty_evidence"):
                with self.subTest(check=check, defect=defect):
                    path.write_text(original, encoding="utf-8")
                    def mutate(rows):
                        if defect == "missing":
                            rows[:] = [row for row in rows if row["check"] != check]
                            return
                        row = next(row for row in rows if row["check"] == check)
                        if defect == "empty_evidence":
                            row["evidence"] = " "
                        else:
                            row["status"] = {"empty_status": "", "pending": "PENDING", "incomplete": "INCOMPLETE",
                                             "limited": "WITH_LIMITATIONS", "limited_delivery": "DELIVERABLE_WITH_LIMITATIONS"}[defect]
                    self.edit_csv("release-audit.csv", mutate)
                    self.assert_rejected(check)
        path.write_text(original, encoding="utf-8")

    def test_part_iii_audits_cannot_be_waived_when_selected(self) -> None:
        self.select_documents({(2, "standard"), (3, "concise")})
        self.edit_csv("release-audit.csv", lambda rows: [
            row.update(status="NOT_APPLICABLE", note="A completed short argument was supplied.")
            for row in rows if row["check"] in project.PART_III_AUDITS])
        self.assert_rejected("proof_framework is NOT_APPLICABLE")
        self.assert_rejected("decisive_mechanisms is NOT_APPLICABLE")

    def test_closed_short_proof_does_not_override_incomplete_core_reviews(self) -> None:
        self.select_documents({(2, "standard"), (3, "concise")})
        self.edit_csv("release-audit.csv", lambda rows: [
            row.update(status="INCOMPLETE", evidence="The core route has not been explained.")
            for row in rows if row["check"] in project.PART_III_AUDITS])
        # proof_depth remains PASS; the two explanation judgments still fail.
        errors, _ = project.validate(self.root)
        self.assertEqual(len(errors), 2)
        self.assertTrue(all("is INCOMPLETE" in error for error in errors))

    def test_partial_part_iii_requires_both_explanation_audits(self) -> None:
        self.select_documents({(2, "standard"), (3, "concise")})
        self.edit_csv("release-audit.csv", lambda rows: rows.__setitem__(
            slice(None), [row for row in rows if row["check"] not in project.PART_III_AUDITS]))
        self.assert_rejected("missing required checks")
        self.assert_rejected("proof_framework")
        self.assert_rejected("decisive_mechanisms")

    def test_no_part_iii_allows_reasoned_nonapplicable_audits(self) -> None:
        self.select_documents({(2, "standard")})
        self.edit_csv("release-audit.csv", lambda rows: rows.extend([
            {"check": check, "status": "NOT_APPLICABLE", "evidence": "", "note": "Part III was not requested."}
            for check in sorted(project.PART_III_AUDITS)]))
        self.assertEqual(project.validate(self.root)[0], [])
        self.edit_csv("release-audit.csv", lambda rows: [
            row.update(note="") for row in rows if row["check"] == "proof_framework"])
        self.assert_rejected("not an accepted completed status")

    def test_single_edition_still_requires_reader_and_depth_reviews(self) -> None:
        self.select_documents({(2, "standard")})
        self.edit_csv("release-audit.csv", lambda rows: [
            row.update(status="NOT_APPLICABLE", note="No concise counterpart was requested.")
            for row in rows if row["check"] in {"reader_outcomes", "edition_depth"}])
        self.assert_rejected("reader_outcomes is NOT_APPLICABLE")
        self.assert_rejected("edition_depth is NOT_APPLICABLE")

    def test_explanation_quality_is_not_inferred_from_declared_passes(self) -> None:
        # The synthetic manuscripts contain no explanatory proof framework. The
        # parser checks declared review records, not whether their claims are true.
        errors, notes = project.validate(self.root)
        self.assertEqual(errors, [])
        self.assertTrue(any("not explanatory quality" in note for note in notes))

    def test_canonical_content_edit_requires_human_review(self) -> None:
        # Both editions use the same body. Structural validation cannot know whether
        # its mathematics has become false; it must not claim semantic verification.
        (self.root / "generated/group-order.tex").write_text("A deliberately unverified algebra statement.")
        errors, notes = project.validate(self.root)
        self.assertEqual(errors, [])
        self.assertTrue(any("do not establish mathematical truth" in note for note in notes))


    def test_problem_wrapper_is_valid_in_manuscript_but_not_component(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(kind="problem"))
        for edition in project.EDITIONS:
            path = self.root / f"part2-{edition}.tex"
            path.write_text(path.read_text().replace(r"\begin{theorem}", r"\begin{problem}[A structural target]")
                            .replace(r"\end{theorem}", r"\end{problem}"))
        self.assertEqual(project.validate(self.root)[0], [])
        path = self.root / "generated/group-order.tex"
        path.write_text("\\begin{problem}[A target]\n" + path.read_text() + "\\end{problem}\n")
        self.assert_rejected("canonical component must contain mathematical body only")

    def test_problem_and_counterexample_titles_cannot_expose_internal_coordinate(self) -> None:
        path = self.root / "part2-standard.tex"
        original = path.read_text()
        for environment in ("problem", "counterexample"):
            with self.subTest(environment=environment):
                path.write_text(original.replace(r"\begin{theorem}", rf"\begin{{{environment}}}[T01 target]")
                                .replace(r"\end{theorem}", rf"\end{{{environment}}}"))
                self.assert_rejected("internal T/P/S coordinate")

    def test_standalone_standard_omission_is_not_relaxed(self) -> None:
        path = self.root / "part2-standard.tex"
        path.write_text(path.read_text().replace(r"\input{generated/group-order.tex}", ""))
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            standard_treatment="OMITTED_WITH_REASON", standard_file="", standard_label="",
            limitation_note="This rule only permits standard omission in V, not II."))
        self.assert_rejected("requires a concise or Part V placement")


class IntegratedProjectChecks(unittest.TestCase):
    """Focused Part V contracts alongside the retained subset regression."""
    edit_csv = ProjectChecks.edit_csv
    edit_manifest = ProjectChecks.edit_manifest
    assert_rejected = ProjectChecks.assert_rejected

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="pmreview-integrated-fixture-")
        self.root = Path(self.temporary.name)
        make_project(self.root, schema_version="0.9.0")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def reset(self, requested=None, owner_part=None, schema_version="0.9.0") -> None:
        for path in self.root.iterdir():
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
        make_project(self.root, requested, schema_version, owner_part)

    def test_new_default_is_ten_documents(self) -> None:
        data = json.loads((self.root / "project-manifest.json").read_text())
        self.assertNotIn("requested_documents", data)
        self.assertEqual(len(data["documents"]), 10)
        self.assertEqual(project.validate(self.root)[0], [])

    def test_legacy_default_and_map_are_read_without_modification(self) -> None:
        self.reset(schema_version="0.8.0")
        before = {p.name: p.read_bytes() for p in self.root.glob("*.csv")}
        manifest_before = (self.root / "project-manifest.json").read_bytes()
        self.assertEqual(project.validate(self.root)[0], [])
        self.assertEqual(len(json.loads(manifest_before)["documents"]), 8)
        self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.glob("*.csv")})
        self.assertEqual(manifest_before, (self.root / "project-manifest.json").read_bytes())
        self.assertNotIn(b"integrated_", before["publication-map.csv"])

    def test_legacy_explicit_selection_is_not_expanded(self) -> None:
        self.reset({(4, "standard")}, schema_version="0.8.0")
        before = (self.root / "project-manifest.json").read_bytes()
        self.assertEqual(project.validate(self.root)[0], [])
        self.assertEqual(before, (self.root / "project-manifest.json").read_bytes())
        self.assertFalse((self.root / "part5-standard.tex").exists())

    def test_schema_upgrade_can_preserve_original_eight_explicitly(self) -> None:
        self.reset(project.LEGACY_COMBINATIONS)
        self.assertEqual(project.validate(self.root)[0], [])
        self.edit_csv("release-audit.csv", lambda rows: [
            row.update(check=row["check"].replace("requested_documents", "all_eight")) for row in rows])
        self.assertEqual(project.validate(self.root)[0], [])

    def test_v_only_accepts_all_four_mathematical_owners(self) -> None:
        for selection in ({(5, "concise")}, {(5, "standard")}, {(5, "concise"), (5, "standard")}):
            for owner in range(1, 5):
                with self.subTest(selection=selection, owner=owner):
                    self.reset(selection, owner)
                    self.assertEqual(project.validate(self.root)[0], [])
                    self.assertFalse(any(self.root.glob(f"part{owner}-*.tex")))

    def test_mixed_selections_use_distinct_slots(self) -> None:
        for selection, owner in [({(4, "standard"), (5, "concise"), (5, "standard")}, 4),
                                 ({(1, "concise"), (5, "standard")}, 1),
                                 ({(2, "standard"), (3, "concise"), (5, "concise")}, 2)]:
            with self.subTest(selection=selection):
                self.reset(selection, owner)
                self.assertEqual(project.validate(self.root)[0], [])

    def test_missing_requested_v_document_record(self) -> None:
        self.edit_manifest(lambda data: data["documents"].pop())
        self.assert_rejected("default ten")
        self.assert_rejected("missing=[(5, 'standard')]")

    def test_missing_requested_v_files(self) -> None:
        for suffix in ("tex", "pdf"):
            with self.subTest(suffix=suffix):
                self.reset({(5, "standard")})
                (self.root / f"part5-standard.{suffix}").unlink()
                self.assert_rejected(f"missing file part5-standard.{suffix}")

    def test_v_is_not_a_mathematical_owner(self) -> None:
        self.reset({(5, "standard")})
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(owner_part="5"))
        self.assert_rejected("owner_part must be 1, 2, 3 or 4")

    def test_new_schema_requires_all_six_integrated_columns(self) -> None:
        path = self.root / "publication-map.csv"
        with path.open(newline="") as handle:
            rows = list(csv.DictReader(handle))
        for row in rows:
            for field in project.INTEGRATED_MAP_FIELDS:
                row.pop(field)
        write_csv(path, sorted(project.MAP_FIELDS), rows)
        self.assert_rejected("missing columns")
        self.assert_rejected("integrated_standard_label")

    def test_legacy_schema_rejects_v_selection(self) -> None:
        self.edit_manifest(lambda data: data.update(schema_version="0.8.0", requested_documents=[
            {"part": 5, "edition": "standard"}]))
        self.assert_rejected("invalid requested_documents")

    def test_unknown_schema_is_rejected(self) -> None:
        self.edit_manifest(lambda data: data.update(schema_version="0.10.0"))
        self.assert_rejected("schema_version must be 0.8.0 or 0.9.0")

    def test_new_schema_does_not_allow_part_six(self) -> None:
        self.edit_manifest(lambda data: data.update(requested_documents=[{"part": 6, "edition": "standard"}]))
        self.assert_rejected("invalid requested_documents")

    def test_integrated_slot_cannot_point_to_standalone_part(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(integrated_standard_file="part2-standard.tex"))
        self.assert_rejected("integrated_standard_file does not match Part V")

    def test_integrated_slot_cannot_point_to_wrong_edition(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(integrated_concise_file="part5-standard.tex"))
        self.assert_rejected("integrated_concise_file does not match Part V")

    def test_original_slot_cannot_point_to_v(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(standard_file="part5-standard.tex"))
        self.assert_rejected("standard_file does not match owner part")

    def test_missing_integrated_label(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(integrated_standard_label="thm:absent"))
        self.assert_rejected("integrated_standard semantic label 'thm:absent' must occur exactly once")

    def test_empty_integrated_label(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(integrated_concise_label=""))
        self.assert_rejected("integrated_concise needs a semantic label")

    def test_duplicate_label_in_integrated_document(self) -> None:
        path = self.root / "part5-standard.tex"
        path.write_text(path.read_text().replace(r"\end{document}", r"\label{thm:group-order}\end{document}"))
        self.assert_rejected("part5-standard.tex: duplicate labels")

    def test_integrated_body_must_be_imported_once(self) -> None:
        path = self.root / "part5-standard.tex"
        path.write_text(path.read_text().replace(r"\input{generated/group-order.tex}", ""))
        self.assert_rejected("integrated_standard canonical component input count 0; expected 1")

    def test_repeated_integrated_body_is_rejected(self) -> None:
        path = self.root / "part5-standard.tex"
        path.write_text(path.read_text().replace(r"\end{document}", r"\input{generated/group-order.tex}\end{document}"))
        self.assert_rejected("integrated_standard canonical component input count 2; expected 1")

    def test_requested_integrated_slot_cannot_be_not_requested(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            integrated_concise_file="", integrated_concise_label="", integrated_concise_treatment="NOT_REQUESTED"))
        self.assert_rejected("requested integrated_concise cannot use NOT_REQUESTED")

    def test_unrequested_integrated_slot_must_be_empty(self) -> None:
        self.reset({(5, "standard")})
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(integrated_concise_file="part5-concise.tex"))
        self.assert_rejected("unrequested integrated_concise must use NOT_REQUESTED with empty file/label")

    def test_integrated_standard_reference_only_is_supported(self) -> None:
        path = self.root / "part5-standard.tex"
        path.write_text(path.read_text().replace(r"\input{generated/group-order.tex}",
            "For a finite group and a subgroup, the order of the latter divides the former; see the source, Theorem 1."))
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            integrated_standard_treatment="REFERENCE_ONLY", limitation_note="Located supplementary input; semantic adequacy requires review."))
        self.assertEqual(project.validate(self.root)[0], [])

    def test_integrated_concise_reference_only_for_located_supplement(self) -> None:
        self.reset({(5, "concise")})
        path = self.root / "part5-concise.tex"
        path.write_text(path.read_text().replace(r"\input{generated/group-order.tex}", "See the cited source, Theorem 1, for this supplementary fact."))
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            integrated_concise_treatment="REFERENCE_ONLY", limitation_note="Supplementary input with a located source; semantic adequacy is not tested."))
        self.assertEqual(project.validate(self.root)[0], [])

    def test_integrated_concise_supplementary_omission(self) -> None:
        self.reset({(5, "concise"), (5, "standard")})
        path = self.root / "part5-concise.tex"
        path.write_text(path.read_text().replace(r"\input{generated/group-order.tex}", ""))
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            integrated_concise_treatment="OMITTED_WITH_REASON", integrated_concise_file="", integrated_concise_label="",
            limitation_note="Synthetic standard-only supplement, not a core omission."))
        self.assertEqual(project.validate(self.root)[0], [])

    def test_omitted_integrated_node_cannot_still_import_body(self) -> None:
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            integrated_concise_treatment="OMITTED_WITH_REASON", integrated_concise_file="", integrated_concise_label="",
            limitation_note="Synthetic omitted supplement."))
        self.assert_rejected("omitted integrated_concise node still inputs")


    def test_v_standard_omission_checks_its_own_edition(self) -> None:
        # Concise still imports the body: it must not be mistaken for standard.
        path = self.root / "part5-standard.tex"
        path.write_text(path.read_text().replace(r"\input{generated/group-order.tex}", ""))
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            integrated_standard_treatment="OMITTED_WITH_REASON",
            integrated_standard_file="", integrated_standard_label="",
            limitation_note="Technical node outside V standard's selected core; owner and V concise place it."))
        self.assertEqual(project.validate(self.root)[0], [])

    def test_v_standard_omission_cannot_hide_its_own_input(self) -> None:
        # Concise does not import the body, so a concise-only check would miss this.
        path = self.root / "part5-concise.tex"
        path.write_text(path.read_text().replace(r"\input{generated/group-order.tex}", ""))
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            integrated_concise_treatment="REFERENCE_ONLY",
            integrated_standard_treatment="OMITTED_WITH_REASON",
            integrated_standard_file="", integrated_standard_label="",
            limitation_note="Synthetic omission must still be checked in its actual standard file."))
        self.assert_rejected("omitted integrated_standard node still inputs its canonical component")

    def test_v_standard_omission_requires_empty_coordinates_and_reason(self) -> None:
        for defect in ("reason", "file", "label"):
            with self.subTest(defect=defect):
                self.reset()
                path = self.root / "part5-standard.tex"
                path.write_text(path.read_text().replace(r"\input{generated/group-order.tex}", ""))
                change = dict(integrated_standard_treatment="OMITTED_WITH_REASON",
                              integrated_standard_file="", integrated_standard_label="",
                              limitation_note="Outside this V's own core.")
                if defect == "reason": change["limitation_note"] = ""
                if defect == "file": change["integrated_standard_file"] = "part5-standard.tex"
                if defect == "label": change["integrated_standard_label"] = "thm:group-order"
                self.edit_csv("publication-map.csv", lambda rows: rows[0].update(change))
                self.assert_rejected("empty file/label and a limitation_note")

    def test_v_standard_reference_requires_note_location_and_no_input(self) -> None:
        for defect, fragment in (("note", "REFERENCE_ONLY needs a limitation_note"),
                                 ("label", "semantic label 'thm:absent' must occur exactly once"),
                                 ("file", "integrated_standard_file does not match Part V"),
                                 ("input", "canonical component input count 1; expected 0")):
            with self.subTest(defect=defect):
                self.reset()
                path = self.root / "part5-standard.tex"
                if defect != "input":
                    path.write_text(path.read_text().replace(r"\input{generated/group-order.tex}",
                        "A located supplementary input is summarized here."))
                change = dict(integrated_standard_treatment="REFERENCE_ONLY",
                              limitation_note="This checks structure, not the accuracy of the summary.")
                if defect == "note": change["limitation_note"] = ""
                if defect == "label": change["integrated_standard_label"] = "thm:absent"
                if defect == "file": change["integrated_standard_file"] = "part2-standard.tex"
                self.edit_csv("publication-map.csv", lambda rows: rows[0].update(change))
                self.assert_rejected(fragment)

    def test_v_only_omission_in_both_editions_has_no_public_placement(self) -> None:
        self.reset({(5, "concise"), (5, "standard")})
        for edition in project.EDITIONS:
            path = self.root / f"part5-{edition}.tex"
            path.write_text(path.read_text().replace(r"\input{generated/group-order.tex}", ""))
            self.edit_csv("publication-map.csv", lambda rows, ed=edition: rows[0].update({
                f"integrated_{ed}_treatment": "OMITTED_WITH_REASON", f"integrated_{ed}_file": "",
                f"integrated_{ed}_label": "", "limitation_note": "Unused node."}))
        self.assert_rejected("no public placement in a requested document")

    def test_v_no_proof_nodes_does_not_require_fabricated_full_proof(self) -> None:
        self.reset({(5, "standard")})
        write_csv(self.root / "proof-mechanism-registry.csv", ["proof_id", "source_ids"], [])
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(proof_ids=""))
        self.edit_csv("release-audit.csv", lambda rows: [row.update(
            evidence="Synthetic record: method account only, no complete proof claimed.")
            for row in rows if row["check"] == "proof_depth"])
        self.assertEqual(project.validate(self.root)[0], [])
        self.edit_csv("release-audit.csv", lambda rows: rows.__setitem__(slice(None),
            [row for row in rows if row["check"] not in {"reader_outcomes", "edition_depth"}]))
        self.assert_rejected("reader_outcomes")
        self.assert_rejected("edition_depth")

    def test_v_only_row_needs_an_actual_placement(self) -> None:
        self.reset({(5, "concise")})
        path = self.root / "part5-concise.tex"
        path.write_text(path.read_text().replace(r"\input{generated/group-order.tex}", ""))
        self.edit_csv("publication-map.csv", lambda rows: rows[0].update(
            integrated_concise_treatment="OMITTED_WITH_REASON", integrated_concise_file="", integrated_concise_label="",
            limitation_note="There is no other selected placement."))
        self.assert_rejected("no public placement in a requested document")

    def test_v_only_proof_explanation_reviews_are_optional(self) -> None:
        self.reset({(5, "standard")})
        self.assertEqual(project.validate(self.root)[0], [])
        self.edit_csv("release-audit.csv", lambda rows: rows.extend([
            {"check": check, "status": "NOT_APPLICABLE", "evidence": "",
             "note": "No Part III requested; V method ideas reviewed under reader_outcomes and edition_depth."}
            for check in sorted(project.PART_III_AUDITS)]))
        self.assertEqual(project.validate(self.root)[0], [])
        self.edit_csv("release-audit.csv", lambda rows: [row.update(note="")
            for row in rows if row["check"] == "proof_framework"])
        self.assert_rejected("proof_framework is NOT_APPLICABLE")

    def test_mixed_iii_v_still_requires_proof_explanation_reviews(self) -> None:
        self.reset({(3, "concise"), (5, "standard")}, owner_part=3)
        self.edit_csv("release-audit.csv", lambda rows: rows.__setitem__(slice(None),
            [row for row in rows if row["check"] not in project.PART_III_AUDITS]))
        self.assert_rejected("proof_framework")
        self.assert_rejected("decisive_mechanisms")
        self.edit_csv("release-audit.csv", lambda rows: rows.extend([
            {"check": check, "status": "NOT_APPLICABLE", "evidence": "", "note": "V is a survey."}
            for check in sorted(project.PART_III_AUDITS)]))
        self.assert_rejected("proof_framework is NOT_APPLICABLE")

    def test_iv_or_v_cannot_waive_frontier_search(self) -> None:
        for selection in ({(4, "standard")}, {(5, "concise")}, {(5, "standard")}):
            for reason in ("No published open-problem list was found.", "The narrow subject is settled."):
                with self.subTest(selection=selection, reason=reason):
                    self.reset(selection)
                    self.edit_csv("release-audit.csv", lambda rows: [
                        row.update(status="NOT_APPLICABLE", note=reason) for row in rows if row["check"] == "frontier_status"])
                    self.assert_rejected("frontier_status is NOT_APPLICABLE")

    def test_v_frontier_missing_or_pending_is_incomplete(self) -> None:
        for defect in ("missing", "PENDING", "INCOMPLETE"):
            self.reset({(5, "standard")})
            def mutate(rows):
                if defect == "missing":
                    rows[:] = [row for row in rows if row["check"] != "frontier_status"]
                else:
                    next(row for row in rows if row["check"] == "frontier_status")["status"] = defect
            self.edit_csv("release-audit.csv", mutate)
            self.assert_rejected("frontier_status")

    def test_settled_scope_uses_completed_frontier_review_not_waiver(self) -> None:
        self.reset({(5, "standard")})
        self.edit_csv("release-audit.csv", lambda rows: [
            row.update(status="PASS", evidence="Synthetic scope-and-settlement note, Section 3.",
                       note="Tests declaration structure, not the settlement's truth.")
            for row in rows if row["check"] == "frontier_status"])
        self.assertEqual(project.validate(self.root)[0], [])

    def test_legacy_all_eight_aliases_do_not_certify_ten(self) -> None:
        self.edit_csv("release-audit.csv", lambda rows: [
            row.update(check=row["check"].replace("requested_documents", "all_eight")) for row in rows])
        self.assert_rejected("build_requested_documents")
        self.assert_rejected("visual_requested_documents")

    def test_legacy_all_eight_aliases_do_not_certify_v_only(self) -> None:
        self.reset({(5, "standard")})
        self.edit_csv("release-audit.csv", lambda rows: [
            row.update(check=row["check"].replace("requested_documents", "all_eight")) for row in rows])
        self.assert_rejected("build_requested_documents")
        self.assert_rejected("visual_requested_documents")

    def test_default_template_manifest_matches_new_contract(self) -> None:
        manifest = json.loads((ROOT / "assets/project-manifest-template.json").read_text())
        errors = []
        self.assertEqual(manifest["schema_version"], "0.9.0")
        self.assertEqual(project.requested_combinations(manifest, errors), project.COMBINATIONS)
        self.assertEqual(errors, [])
        self.assertEqual({(d["part"], d["edition"]) for d in manifest["documents"]}, project.COMBINATIONS)
        with (ROOT / "assets/registries/publication-map-template.csv").open(newline="") as handle:
            fields = next(csv.reader(handle))
        self.assertEqual(set(fields), project.MAP_FIELDS | project.INTEGRATED_MAP_FIELDS)
        self.assertEqual(len(project.INTEGRATED_MAP_FIELDS), 6)


def make_skill(root: Path, version: str = skill.VERSION) -> None:
    """Minimal parseable source fixture, never used as a distributable skill."""
    root.mkdir(parents=True, exist_ok=True)
    (root / "SKILL.md").write_text(
        f"---\nname: {skill.NAME}\ndescription: Synthetic release-validator fixture.\n---\n"
        f"**Version:** {version}\n", encoding="utf-8")
    files = {name: "Synthetic runtime reference.\n" for name in skill.REQUIRED_FILES if name != "SKILL.md"}
    files.update({"agents/openai.yaml": "interface:\n  display_name: Synthetic fixture\n",
                  "assets/project-manifest-template.json": "{}\n"})
    for filename in files:
        if filename.endswith(".csv"):
            files[filename] = "field\n"
    for filename, content in files.items():
        path = root / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


class SkillChecks(unittest.TestCase):
    def test_release_version_requires_exact_match(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pmreview-version-fixture-") as temporary:
            root = Path(temporary)
            make_skill(root)
            self.assertEqual(skill.validate(root)[0], [])
            for version in (f"{skill.VERSION}-draft", f"{skill.VERSION}-rc1", f"{skill.VERSION}.1",
                            f"{skill.VERSION}0", "0.10.0"):
                with self.subTest(version=version):
                    make_skill(root, version)
                    self.assertTrue(any("must declare **Version:**" in error for error in skill.validate(root)[0]))

    def test_both_integrated_templates_are_required(self) -> None:
        for edition in ("concise", "standard"):
            with self.subTest(edition=edition), tempfile.TemporaryDirectory(prefix="pmreview-template-fixture-") as temporary:
                root = Path(temporary)
                make_skill(root)
                (root / f"assets/templates/part5-integrated-{edition}.tex").unlink()
                self.assertTrue(any(f"part5-integrated-{edition}.tex" in error for error in skill.validate(root)[0]))

    def test_historical_versions_do_not_invalidate_release_metadata(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pmreview-version-history-fixture-") as temporary:
            root = Path(temporary)
            make_skill(root)
            (root / "references/records-and-delivery.md").write_text("Record format 0.8.0; controlling source version v2.\n", encoding="utf-8")
            self.assertEqual(skill.validate(root)[0], [])


    def test_install_tree_excludes_development_and_preview_files(self) -> None:
        for filename in ("CHANGELOG.md", "scripts/run_regression.py", "dev/check.py", "preview.pdf"):
            with self.subTest(filename=filename), tempfile.TemporaryDirectory(prefix="pmreview-clean-fixture-") as temporary:
                root = Path(temporary)
                make_skill(root)
                path = root / filename
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("Synthetic non-runtime file.\n")
                self.assertTrue(skill.validate(root)[0])


class ZipChecks(unittest.TestCase):
    def packaged_skill(self, temporary: str, wrapper: str, extras: list[tuple[str, str]] = ()) -> Path:
        root = Path(temporary)
        source = root / "source"
        make_skill(source)
        archive = root / "fixture.zip"
        with zipfile.ZipFile(archive, "w") as handle:
            for path in source.rglob("*"):
                if path.is_file():
                    handle.write(path, wrapper + path.relative_to(source).as_posix())
            for name, content in extras:
                handle.writestr(name, content)
        return archive

    def test_install_archive_uses_exact_named_root(self) -> None:
        for wrapper in ("", "nested/" + skill.NAME + "/", skill.NAME + "/"):
            with self.subTest(wrapper=wrapper), tempfile.TemporaryDirectory(prefix="pmreview-layout-fixture-") as temporary:
                archive = self.packaged_skill(temporary, wrapper)
                errors, _ = skill.validate_zip(archive)
                if wrapper == skill.NAME + "/":
                    self.assertEqual(errors, [])
                else:
                    self.assertTrue(any("single top-level directory" in error for error in errors))

    def test_file_outside_wrapped_skill_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pmreview-extra-fixture-") as temporary:
            archive = self.packaged_skill(temporary, skill.NAME + "/", [("private-notes.txt", "Not part of the skill.")])
            self.assertTrue(any("outside skill root: private-notes.txt" in error for error in skill.validate_zip(archive)[0]))

    def test_generated_artifact_inside_skill_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pmreview-cache-fixture-") as temporary:
            archive = self.packaged_skill(temporary, skill.NAME + "/", [(skill.NAME + "/scratch/build.log", "Build output.")])
            self.assertTrue(any("generated build/cache artifact" in error for error in skill.validate_zip(archive)[0]))

    def rejection(self, entries: list[tuple[str, str]], fragment: str) -> None:
        with tempfile.TemporaryDirectory(prefix="pmreview-zip-fixture-") as temporary:
            root = Path(temporary)
            archive = root / "fixture.zip"
            with zipfile.ZipFile(archive, "w") as handle:
                for name, data in entries:
                    handle.writestr(name, data)
            destination = root / "unpacked"
            destination.mkdir()
            errors = skill.unpack_zip(archive, destination)
            self.assertIn(fragment, "\n".join(errors))
            self.assertEqual(list(destination.iterdir()), [], "unsafe ZIP must not extract any member")

    def test_parent_traversal(self) -> None:
        self.rejection([("../escape.txt", "x")], "unsafe ZIP member")

    def test_windows_ads(self) -> None:
        self.rejection([("safe.txt:stream", "x")], "unsafe ZIP member")

    def test_case_collision(self) -> None:
        self.rejection([("file.txt", "x"), ("FILE.txt", "y")], "case-colliding")

    def test_windows_device(self) -> None:
        self.rejection([("CON.txt", "x")], "unsafe ZIP member")

    def test_file_directory_conflict(self) -> None:
        self.rejection([("folder", "x"), ("folder/file.txt", "y")], "path conflict")

    def test_zip_symlink(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pmreview-symlink-fixture-") as temporary:
            root = Path(temporary)
            archive = root / "fixture.zip"
            with zipfile.ZipFile(archive, "w") as handle:
                info = zipfile.ZipInfo("link")
                info.create_system = 3
                info.external_attr = (stat.S_IFLNK | 0o777) << 16
                handle.writestr(info, "../../outside")
            destination = root / "unpacked"
            destination.mkdir()
            self.assertTrue(any("nonregular ZIP member" in error for error in skill.unpack_zip(archive, destination)))
            self.assertEqual(list(destination.iterdir()), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)

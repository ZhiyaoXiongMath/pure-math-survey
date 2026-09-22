#!/usr/bin/env python3
"""Validate the English-only 1.0.1 skill directory or safely inspect its ZIP."""
from __future__ import annotations

import argparse
import csv
import json
import re
import stat
import sys
import tempfile
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import unquote

VERSION = "1.0.1"
NAME = "pure-math-systematic-review"
PARTS = ("part1-foundations", "part2-results", "part3-methods", "part4-boundaries", "part5-integrated")
TEMPLATES = tuple(f"{part}-{edition}.tex" for part in PARTS for edition in ("concise", "standard"))
MAX_FILES = 800
MAX_MEMBER = 16 * 1024 * 1024
MAX_TOTAL = 100 * 1024 * 1024
TEXT_SUFFIXES = {".md", ".tex", ".sty", ".txt", ".csv", ".json", ".jsonl", ".yaml", ".yml", ".py"}
BUILD_SUFFIXES = {".aux", ".log", ".out", ".toc", ".fls", ".fdb_latexmk", ".pyc",
                  ".pdf", ".png", ".jpg", ".jpeg", ".webp", ".zip"}
REFERENCES = ("architecture.md", "editions.md", "proofs-and-boundaries.md",
              "records-and-delivery.md", "research-and-evidence.md",
              "validation.md", "writing-style.md")
REQUIRED_FILES = {"SKILL.md", "agents/openai.yaml", "assets/templates/math-review.sty",
                  "assets/project-manifest-template.json", "scripts/validate_project.py"}
REQUIRED_FILES.update(f"references/{name}" for name in REFERENCES)
REQUIRED_FILES.update(f"assets/templates/{name}" for name in TEMPLATES)
REQUIRED_FILES.update(f"assets/registries/{name}-template.csv" for name in
                      ("bibliographic-identity", "publication-map", "proof-mechanism-registry",
                       "canonical-theorem-registry", "release-audit"))
LINK_RE = re.compile(r"!?\[[^]]*\]\(([^)]+)\)")


def safe_zip_path(name: str) -> bool:
    value = name.rstrip("/")
    if not value or "\\" in value or ":" in value or "\x00" in value:
        return False
    path = PurePosixPath(value)
    if path.is_absolute() or any(x in {"", ".", ".."} for x in value.split("/")):
        return False
    devices = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}
    return all(not p.endswith((".", " ")) and p.split(".")[0].lower() not in devices for p in path.parts)


def unpack_zip(source: Path, destination: Path) -> list[str]:
    errors: list[str] = []
    if source.stat().st_size > MAX_TOTAL:
        return ["ZIP exceeds compressed size limit"]
    with zipfile.ZipFile(source) as archive:
        infos = archive.infolist()
        if len(infos) > MAX_FILES:
            errors.append("ZIP exceeds member count limit")
        if sum(info.file_size for info in infos) > MAX_TOTAL:
            errors.append("ZIP exceeds total uncompressed size limit")
        names: set[str] = set()
        for info in infos:
            if not safe_zip_path(info.filename):
                errors.append(f"unsafe ZIP member: {info.filename!r}")
            key = info.filename.rstrip("/").casefold()
            if key in names:
                errors.append(f"duplicate/case-colliding ZIP member: {info.filename}")
            names.add(key)
            if info.flag_bits & 1:
                errors.append(f"encrypted ZIP member: {info.filename}")
            if info.file_size > MAX_MEMBER:
                errors.append(f"oversized ZIP member: {info.filename}")
            file_type = stat.S_IFMT(info.external_attr >> 16)
            if file_type not in (0, stat.S_IFREG, stat.S_IFDIR):
                errors.append(f"nonregular ZIP member (including symlink): {info.filename}")
        if errors:
            return errors
        regular_names = {info.filename.casefold() for info in infos if not info.is_dir()}
        for info in infos:
            for parent in PurePosixPath(info.filename).parents:
                if parent.as_posix().casefold() in regular_names:
                    errors.append(f"ZIP file/directory path conflict: {info.filename}")
        if errors:
            return errors
        # Validate every member first, then extract manually below a fresh temp root.
        for info in infos:
            target = destination.joinpath(*PurePosixPath(info.filename).parts)
            target.resolve().relative_to(destination.resolve())
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info) as reader, target.open("xb") as writer:
                total = 0
                while block := reader.read(1024 * 1024):
                    total += len(block)
                    if total > MAX_MEMBER:
                        raise ValueError(f"ZIP member exceeds extraction limit: {info.filename}")
                    writer.write(block)
    return errors


def validate(root: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []
    root = root.resolve()
    skill = root / "SKILL.md"
    if not skill.is_file():
        return [f"missing SKILL.md at {root}"], notes
    text = skill.read_text(encoding="utf-8-sig")
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not frontmatter:
        errors.append("SKILL.md has no YAML frontmatter")
    else:
        metadata = frontmatter.group(1)
        if not re.search(rf"(?m)^name:\s*[\"']?{re.escape(NAME)}[\"']?\s*$", metadata):
            errors.append(f"frontmatter name must be {NAME}")
        if not re.search(r"(?m)^description:\s*\S", metadata):
            errors.append("frontmatter needs a nonempty description")
    if not re.search(rf"(?m)^\*\*Version:\*\*[^\S\r\n]*{re.escape(VERSION)}[^\S\r\n]*$", text):
        errors.append(f"SKILL.md must declare **Version:** {VERSION}")
    for filename in sorted(REQUIRED_FILES):
        path = root / filename
        if not path.is_file() or path.stat().st_size == 0:
            errors.append(f"missing/empty required file: {filename}")

    try:
        import yaml
    except ImportError:
        yaml = None
        notes.append("PyYAML unavailable: YAML was not fully parsed; install PyYAML for release validation.")

    files = list(root.rglob("*"))
    regular_files = [p for p in files if p.is_file()]
    if len(regular_files) > MAX_FILES or sum(p.stat().st_size for p in regular_files) > MAX_TOTAL:
        errors.append("skill exceeds file count or total size limit")
    case_names: set[str] = set()
    for path in files:
        rel = path.relative_to(root).as_posix()
        if path.is_symlink():
            errors.append(f"symlinks are not permitted: {rel}")
            continue
        try:
            path.resolve().relative_to(root)
        except ValueError:
            errors.append(f"path escapes skill root: {rel}")
            continue
        if not path.is_file():
            continue
        if rel.casefold() in case_names:
            errors.append(f"case-colliding filename: {rel}")
        case_names.add(rel.casefold())
        if path.stat().st_size > MAX_MEMBER:
            errors.append(f"oversized file: {rel}")
        if path.suffix.lower() in BUILD_SUFFIXES or "__pycache__" in path.parts or path.name.endswith(".synctex.gz"):
            errors.append(f"generated build/cache artifact: {rel}")
        if (path.relative_to(root).parts[0] not in {"SKILL.md", "agents", "references", "assets", "scripts"}
                or rel.startswith("assets/fixtures/")
                or rel in {"scripts/validate_skill.py", "scripts/run_regression.py"}
                or path.name.upper().startswith(("CHANGELOG", "RELEASE-NOTES"))):
            errors.append(f"non-runtime/development file in installable skill: {rel}")
        if "chinese" in path.name.lower() or "bilingual" in path.name.lower():
            errors.append(f"obsolete bilingual asset name: {rel}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            content = path.read_text(encoding="utf-8-sig")
            if re.search(r"[\u3400-\u4dbf\u4e00-\u9fff]", content):
                errors.append(f"CJK text in English-only skill source: {rel}")
            if path.suffix == ".json":
                json.loads(content)
            elif path.suffix == ".jsonl":
                for number, line in enumerate(content.splitlines(), 1):
                    if line.strip():
                        value = json.loads(line)
                        if not isinstance(value, dict):
                            errors.append(f"{rel}:{number}: JSONL row must be an object")
            elif path.suffix == ".csv":
                with path.open(newline="", encoding="utf-8-sig") as handle:
                    rows = list(csv.reader(handle))
                if not rows or not rows[0] or len(rows[0]) != len(set(rows[0])):
                    errors.append(f"{rel}: empty or duplicate CSV header")
                elif any(len(row) != len(rows[0]) for row in rows[1:] if row):
                    errors.append(f"{rel}: CSV row width differs from header")
            elif path.suffix in {".yaml", ".yml"} and yaml:
                if not isinstance(yaml.safe_load(content), dict):
                    errors.append(f"{rel}: YAML must be a mapping")
            elif path.suffix == ".md":
                unfenced = re.sub(r"```.*?```", "", content, flags=re.S)
                for raw in LINK_RE.findall(unfenced):
                    target = raw.strip().strip("<>")
                    if "://" in target or target.startswith(("#", "mailto:", "data:")):
                        continue
                    target = unquote(target.split("#", 1)[0])
                    if not target:
                        continue
                    if "\\" in target or ":" in target or PurePosixPath(target).is_absolute():
                        errors.append(f"{rel}: unsafe Markdown link {raw!r}")
                        continue
                    linked = (path.parent / target).resolve()
                    try:
                        linked.relative_to(root)
                    except ValueError:
                        errors.append(f"{rel}: Markdown link escapes skill root: {raw}")
                        continue
                    if not linked.exists():
                        errors.append(f"{rel}: broken relative link: {raw}")
        except (OSError, UnicodeError, ValueError, csv.Error) as exc:
            errors.append(f"{rel}: cannot parse source: {exc}")
        except Exception as exc:
            # PyYAML raises its own parser exceptions; preserve a clear filename.
            errors.append(f"{rel}: parse failure: {exc}")
    if yaml and frontmatter:
        try:
            metadata = yaml.safe_load(frontmatter.group(1))
            if not isinstance(metadata, dict):
                errors.append("SKILL.md frontmatter is not a mapping")
            elif metadata.get("name") != NAME or not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
                errors.append("SKILL.md parsed frontmatter needs the expected name and nonempty description")
        except Exception as exc:
            errors.append(f"SKILL.md invalid YAML frontmatter: {exc}")
    return errors, notes


def validate_zip(source: Path) -> tuple[list[str], list[str]]:
    """Inspect an installation ZIP with exactly one named top-level skill root."""
    with tempfile.TemporaryDirectory(prefix="pmreview-skill-check-") as temporary:
        extracted = Path(temporary)
        errors = unpack_zip(source, extracted)
        if errors:
            return errors, []
        roots = list(extracted.rglob("SKILL.md"))
        if len(roots) != 1:
            return [f"ZIP must contain exactly one SKILL.md, found {len(roots)}"], []
        root = roots[0].parent
        if root != extracted / NAME:
            errors.append(f"ZIP must use the single top-level directory {NAME}/")
        for path in extracted.rglob("*"):
            if path != root and root not in path.parents and path not in root.parents:
                errors.append(f"ZIP member outside skill root: {path.relative_to(extracted).as_posix()}")
        structure_errors, notes = validate(root)
        return errors + structure_errors, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--require-yaml", action="store_true", help="Fail if PyYAML is unavailable")
    args = parser.parse_args()
    try:
        if args.source.is_dir():
            errors, notes = validate(args.source)
        else:
            errors, notes = validate_zip(args.source)
        if args.require_yaml and any("PyYAML unavailable" in note for note in notes):
            errors.append("full YAML validation requires PyYAML")
    except (OSError, ValueError, zipfile.BadZipFile, RuntimeError) as exc:
        errors, notes = [str(exc)], []
    for note in notes:
        print(f"NOTE: {note}")
    if errors:
        print("SKILL VALIDATION FAILED", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    suffix = " (YAML parsing incomplete)" if notes else ""
    print(f"SKILL STRUCTURAL VALIDATION PASSED: {NAME} {VERSION}{suffix}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

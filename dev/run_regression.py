#!/usr/bin/env python3
"""Run structural fixtures and build all ten English templates in an isolated copy.

This is a template/tool regression, not a mathematical content evaluation.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True
from validate_skill import TEMPLATES, VERSION  # noqa: E402

BAD_LOG = (
    r"Missing character:", r"LaTeX Warning: Reference .* undefined",
    r"LaTeX Warning: Citation .* undefined", r"There were undefined references",
    r"There were undefined citations", r"Label\(s\) may have changed",
    r"multiply defined", r"Overfull \\hbox", r"Overfull \\vbox",
    r"Undefined control sequence", r"LaTeX Error:", r"Package .* Error:",
)


def run(command: list[str], cwd: Path | None = None, env: dict[str, str] | None = None) -> str:
    proc = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                          encoding="utf-8", errors="replace", timeout=180)
    if proc.returncode:
        raise RuntimeError(f"Command failed ({proc.returncode}): {' '.join(command)}\n{proc.stdout[-12000:]}")
    return proc.stdout


def reference_state(out: Path, stem: str) -> str:
    digest = hashlib.sha256()
    for suffix in (".aux", ".toc", ".out"):
        path = out / (stem + suffix)
        digest.update(path.read_bytes() if path.exists() else b"")
    return digest.hexdigest()


def compile_template(engine: str, tex: Path, out: Path) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    command = [engine, "-no-shell-escape", "-interaction=nonstopmode", "-halt-on-error",
               "-file-line-error", f"-output-directory={out}", tex.name]
    previous = None
    stable = False
    for pass_number in range(1, 6):
        run(command, cwd=tex.parent)
        state = reference_state(out, tex.stem)
        if pass_number >= 2 and state == previous:
            stable = True
            break
        previous = state
    if not stable:
        raise RuntimeError(f"References did not stabilize within five passes: {tex.name}")
    log = (out / (tex.stem + ".log")).read_text(encoding="utf-8", errors="replace")
    failures = [pattern for pattern in BAD_LOG if re.search(pattern, log, re.I)]
    if failures:
        raise RuntimeError(f"{tex.name}: TeX log checks failed: {failures}")
    pdf = out / (tex.stem + ".pdf")
    if not pdf.is_file() or pdf.stat().st_size == 0:
        raise RuntimeError(f"{tex.name}: no PDF produced")
    if shutil.which("pdftotext"):
        text_path = out / (tex.stem + ".txt")
        run(["pdftotext", "-layout", str(pdf), str(text_path)])
        if not text_path.read_text(encoding="utf-8", errors="replace").strip():
            raise RuntimeError(f"{tex.name}: extracted PDF text is empty")
    print(f"TEMPLATE BUILD PASSED: {tex.name}; passes={pass_number}")
    return {"template": tex.name, "pdf": str(pdf), "passes": pass_number,
            "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "log_checks": "PASS", "visual_inspection": "PENDING"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path, default=Path(__file__).resolve().parents[1] / "skills/pure-math-systematic-review")
    parser.add_argument("--require-tex", action="store_true", help="Fail, rather than report partial checks, when pdflatex is missing")
    parser.add_argument("--keep-build", type=Path, help="Retain isolated template sources, PDFs, logs and report here")
    args = parser.parse_args()
    root = args.root.resolve()
    temporary = None
    try:
        dev = Path(__file__).resolve().parent
        print(run([sys.executable, "-B", str(dev / "validate_skill.py"), str(root)]).rstrip())
        print(run([sys.executable, "-B", str(dev / "tests/test_validation.py")],
                  env={**os.environ, "PMSR_SKILL_ROOT": str(root)}).rstrip())
        engine = shutil.which("pdflatex")
        if engine is None:
            if args.require_tex:
                raise RuntimeError("pdflatex unavailable; all-ten-template build is required")
            print("PARTIAL REGRESSION: structural fixtures passed; 10 PDF builds NOT RUN (pdflatex unavailable).")
            return 0
        if args.keep_build:
            build = args.keep_build.resolve()
            for protected in (root, Path(__file__).resolve().parents[1]):
                try:
                    build.relative_to(protected)
                except ValueError:
                    pass
                else:
                    raise RuntimeError("--keep-build must be outside the repository and skill root")
            build.mkdir(parents=True, exist_ok=True)
        else:
            temporary = tempfile.TemporaryDirectory(prefix="pmreview-regression-")
            build = Path(temporary.name)
        source_copy = build / "template-sources"
        shutil.copytree(root / "assets/templates", source_copy, dirs_exist_ok=True)
        results = []
        for filename in TEMPLATES:
            tex = source_copy / filename
            results.append(compile_template(engine, tex, build / tex.stem))
        report = {"schema_version": "0.9.0", "skill_version": VERSION, "structural_fixtures": "PASS",
                  "template_build_count": len(results), "template_builds": results,
                  "mathematical_review": "NOT_PERFORMED", "visual_inspection": "PENDING"}
        (build / "regression-report.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print("REGRESSION PASSED: structural fixtures and all 10 template builds. Mathematical and visual review are separate.")
        if args.keep_build:
            print(f"Build artifacts: {build}")
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(f"REGRESSION FAILED: {exc}", file=sys.stderr)
        return 1
    finally:
        if temporary is not None:
            temporary.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())

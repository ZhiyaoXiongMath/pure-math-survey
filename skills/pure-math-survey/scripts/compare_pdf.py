#!/usr/bin/env python3
"""Render every page and report pixel differences; never grade mathematical quality.

Optional dependencies: PyMuPDF and Pillow. Inputs are read-only. Exit 0 = exact
render match, 1 = differences, 2 = unavailable/invalid comparison. Differences
need visual adjudication; exact equality is not a universal typography gate.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path


def compare_pdfs(reference: Path, candidate: Path, output: Path, dpi: int = 120) -> dict:
    if dpi < 36 or dpi > 600:
        raise ValueError("dpi must lie in 36..600")
    try:
        import fitz
        from PIL import Image, ImageChops, ImageDraw
    except ImportError as exc:
        raise RuntimeError("PDF comparison requires PyMuPDF and Pillow; no pages were rendered") from exc
    for p in (reference, candidate):
        if not p.is_file():
            raise FileNotFoundError(p)
    if output.exists() and any(output.iterdir()):
        raise FileExistsError("Comparison output must be new or empty")
    output.mkdir(parents=True, exist_ok=True)
    thumbs = []
    with fitz.open(reference) as a, fitz.open(candidate) as b:
        report = {"reference": str(reference), "candidate": str(candidate), "dpi": dpi,
                  "reference_sha256": hashlib.sha256(reference.read_bytes()).hexdigest(),
                  "candidate_sha256": hashlib.sha256(candidate.read_bytes()).hexdigest(),
                  "renderer": f"PyMuPDF {fitz.VersionBind}",
                  "reference_pages": len(a), "candidate_pages": len(b), "pages": [],
                  "scope": "rendered pixels and page boxes only; no mathematical/content quality verdict"}
        matrix = fitz.Matrix(dpi / 72, dpi / 72)
        for index in range(max(len(a), len(b))):
            images = []
            for doc, prefix in ((a, "reference"), (b, "candidate")):
                if index >= len(doc):
                    images.append(None)
                    continue
                pix = doc[index].get_pixmap(matrix=matrix, colorspace=fitz.csRGB, alpha=False)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.save(output / f"{prefix}-{index+1:03}.png")
                images.append(img)
                if prefix == "candidate":
                    thumb = img.copy(); thumb.thumbnail((300, 425))
                    tile = Image.new("RGB", (320, 455), "white")
                    tile.paste(thumb, ((320 - thumb.width)//2, 8))
                    ImageDraw.Draw(tile).text((10, 435), f"Page {index+1}", fill="black")
                    thumbs.append(tile)
            ia, ib = images
            same_box = (index < min(len(a), len(b)) and
                        tuple(a[index].rect) == tuple(b[index].rect))
            equal = False
            changed = None
            if ia is not None and ib is not None and ia.size == ib.size:
                diff = ImageChops.difference(ia, ib)
                equal = diff.getbbox() is None
                red, green, blue = diff.split()
                maximum = ImageChops.lighter(ImageChops.lighter(red, green), blue)
                changed = sum(maximum.histogram()[1:])
                if not equal:
                    diff.save(output / f"difference-{index+1:03}.png")
            report["pages"].append({"page": index+1, "same_box": same_box,
                                    "pixel_equal": equal, "changed_pixels": changed})
        for offset in range(0, len(thumbs), 9):
            batch = thumbs[offset:offset+9]
            sheet = Image.new("RGB", (960, 455 * math.ceil(len(batch)/3)), "white")
            for j, thumb in enumerate(batch):
                sheet.paste(thumb, ((j%3)*320, (j//3)*455))
            sheet.save(output / f"contact-sheet-{offset//9+1:02}.png")
        report["all_pages_pixel_equal"] = (len(a) == len(b) and
              all(p["same_box"] and p["pixel_equal"] for p in report["pages"]))
        report["status"] = "EXACT_RENDER_MATCH" if report["all_pages_pixel_equal"] else "RENDER_DIFFERENCES"
    (output / "comparison.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--dpi", type=int, default=120)
    args = parser.parse_args()
    try:
        report = compare_pdfs(args.reference.resolve(), args.candidate.resolve(), args.output.resolve(), args.dpi)
    except Exception as exc:
        print(f"Comparison unavailable: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({k:report[k] for k in ("status", "reference_pages", "candidate_pages", "dpi")}, indent=2))
    return 0 if report["all_pages_pixel_equal"] else 1

if __name__ == "__main__":
    raise SystemExit(main())

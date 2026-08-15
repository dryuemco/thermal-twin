"""Find pages whose ink leaves the text block, or whose folio touches the text.

Neither fault produces an overfull box, so pdflatex reports nothing and the
source checks cannot see them. A centred \\includegraphics wider than the line
just protrudes, and a float tall enough to reach the footer prints the page
number through its own caption. This measures the rendered pages instead.

Usage:  python paper/tex/page_geometry_check.py [manuscript.pdf] [dpi]
"""
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

MGS = Path(r"C:\Users\CORSAIR\AppData\Local\Programs\Python").parent  # placeholder, resolved below
GS = Path(r"C:\Users\CORSAIR\AppData\Local\Programs\MiKTeX\miktex\bin\x64\mgs.exe")

PDF = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("paper/tex/manuscript.pdf")
DPI = int(sys.argv[2]) if len(sys.argv) > 2 else 100

# A4 at DPI, and the elsarticle preprint text block measured from the class.
MM = DPI / 25.4
PAGE_W_MM, PAGE_H_MM = 210.0, 297.0
TEXT_W_MM = 135.0                      # \textwidth 390pt
# Tolerance: figures are deliberately allowed a small symmetric overhang.
ALLOWED_OVERHANG_MM = 4.0
FOLIO_BAND_MM = 18.0                   # band above the page bottom holding the folio
GAP_REQUIRED_MM = 3.0                  # clear space expected above the folio


def render(pdf: Path, out_dir: Path) -> list[Path]:
    subprocess.run(
        [str(GS), "-dNOPAUSE", "-dBATCH", "-sDEVICE=pnggray", f"-r{DPI}",
         f"-sOutputFile={out_dir}/p%04d.png", str(pdf)],
        check=True, capture_output=True)
    return sorted(out_dir.glob("p*.png"))


def ink_columns(im: Image.Image, top: int, bottom: int) -> tuple[int, int] | None:
    """Leftmost and rightmost inked column between two rows."""
    crop = im.crop((0, top, im.width, bottom))
    bbox = crop.point(lambda v: 255 if v < 200 else 0).getbbox()
    return (bbox[0], bbox[2]) if bbox else None


def row_has_ink(im: Image.Image, y0: int, y1: int) -> bool:
    crop = im.crop((0, y0, im.width, y1))
    return crop.point(lambda v: 255 if v < 200 else 0).getbbox() is not None


def main() -> None:
    if not PDF.exists():
        raise SystemExit(f"missing {PDF}")
    with tempfile.TemporaryDirectory() as td:
        pages = render(PDF, Path(td))
        margin_mm = (PAGE_W_MM - TEXT_W_MM) / 2
        left_limit = (margin_mm - ALLOWED_OVERHANG_MM) * MM
        right_limit = (PAGE_W_MM - margin_mm + ALLOWED_OVERHANG_MM) * MM

        wide, folio = [], []
        for i, p in enumerate(pages, 1):
            im = Image.open(p).convert("L")
            cols = ink_columns(im, 0, im.height)
            if cols:
                l, r = cols
                if l < left_limit or r > right_limit:
                    over_l = max(0.0, (left_limit - l) / MM)
                    over_r = max(0.0, (r - right_limit) / MM)
                    wide.append((i, round(over_l, 1), round(over_r, 1)))
            # folio collision: ink in the folio band with no clear gap above it
            band_top = im.height - int(FOLIO_BAND_MM * MM)
            gap_top = band_top - int(GAP_REQUIRED_MM * MM)
            if row_has_ink(im, band_top, im.height) and row_has_ink(im, gap_top, band_top):
                folio.append(i)

        print(f"  {len(pages)} pages at {DPI} dpi; text block {TEXT_W_MM:.0f} mm, "
              f"overhang tolerated {ALLOWED_OVERHANG_MM:.0f} mm")
        print(f"  ink outside the margins: {len(wide)}")
        for i, ol, orr in wide[:25]:
            print(f"    page {i:4d}  left +{ol} mm  right +{orr} mm")
        print(f"  folio with no clear gap above it: {len(folio)}")
        for i in folio[:25]:
            print(f"    page {i}")
        if not wide and not folio:
            print("  CLEAN")


if __name__ == "__main__":
    main()

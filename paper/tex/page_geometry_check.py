"""Find pages whose ink leaves the text block, or whose folio touches the text.

Neither fault produces an overfull box, so pdflatex reports nothing and the
source checks cannot see them. A centred \\includegraphics wider than the line
just protrudes; a tabularx whose X column has been starved overflows on the
right; a float tall enough to reach the footer prints the page number through
its own caption. This measures the rendered pages instead of trusting the log.

The right-hand text edge is measured, not assumed: it is the median of the
per-page rightmost ink, which is where justified prose ends. Assuming a centred
text block instead reported every page as overfull, because the review option
sets line numbers in the left margin and elsarticle's margins are not symmetric.

Usage:  python paper/tex/page_geometry_check.py [manuscript.pdf] [dpi]
Exit:   0 clean, 1 something protrudes
"""
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image

GS = Path(r"C:\Users\CORSAIR\AppData\Local\Programs\MiKTeX\miktex\bin\x64\mgs.exe")
PDF = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("paper/tex/manuscript.pdf")
DPI = int(sys.argv[2]) if len(sys.argv) > 2 else 100
MM = DPI / 25.4

# Figures are deliberately allowed a small symmetric overhang; anything past
# this is a fault worth looking at.
TOLERANCE_MM = 2.0
FOLIO_BAND_MM = 18.0      # band at the foot of the page holding the number
GAP_REQUIRED_MM = 3.0     # clear space expected between text and folio
INK = 200                 # grey level below which a pixel counts as ink


def ink_bbox(im: Image.Image):
    return im.point(lambda v: 255 if v < INK else 0).getbbox()


def has_ink(im: Image.Image, y0: int, y1: int) -> bool:
    return ink_bbox(im.crop((0, max(0, y0), im.width, min(im.height, y1)))) is not None


def main() -> None:
    if not PDF.exists():
        raise SystemExit(f"missing {PDF}")
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(
            [str(GS), "-dNOPAUSE", "-dBATCH", "-sDEVICE=pnggray", f"-r{DPI}",
             f"-sOutputFile={td}/p%04d.png", str(PDF)],
            check=True, capture_output=True)
        pages = sorted(Path(td).glob("p*.png"))

        rights, folio = [], []
        for i, p in enumerate(pages, 1):
            im = Image.open(p).convert("L")
            bb = ink_bbox(im)
            if bb:
                rights.append((bb[2] / MM, i))
            band_top = im.height - int(FOLIO_BAND_MM * MM)
            if has_ink(im, band_top, im.height) and \
               has_ink(im, band_top - int(GAP_REQUIRED_MM * MM), band_top):
                folio.append(i)

        edge = sorted(r for r, _ in rights)[len(rights) // 2]
        over = sorted(((r - edge, i) for r, i in rights if r - edge > TOLERANCE_MM),
                      reverse=True)

        print(f"  {len(pages)} pages at {DPI} dpi")
        print(f"  right text edge measured at {edge:.1f} mm; tolerance {TOLERANCE_MM} mm")
        print(f"  pages whose ink passes it: {len(over)}")
        for mm, i in over[:25]:
            print(f"    page {i:4d}  +{mm:.1f} mm")
        print(f"  folio with no clear gap above it: {len(folio)}")
        for i in folio[:25]:
            print(f"    page {i}")
        if not over and not folio:
            print("  CLEAN")
        sys.exit(1 if (over or folio) else 0)


if __name__ == "__main__":
    main()

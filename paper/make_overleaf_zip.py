"""Assemble an Overleaf-ready zip from the generated LaTeX.

The generated .tex files live in paper/tex/ and reach outward for their inputs:
the bibliography is \\bibliography{../REFERENCES} and the figures resolve through
a \\graphicspath that includes ../ and ../figures/. Overleaf projects are flat,
so this script restages everything at the project root and rewrites the one path
that would otherwise break.

Nothing is edited in place: manuscript.tex is a generated file and any edit to it
would be discarded by the next build_tex.mjs run, so the rewrite happens on the
copy inside the zip.

Usage:  python paper/make_overleaf_zip.py [output.zip]
"""
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent          # paper/
TEX = ROOT / "tex"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "overleaf" / "thermal-twin-overleaf.zip"
STAGE = ROOT / "overleaf" / "_stage"

DOCS = ["manuscript.tex", "supplementary.tex"]
BIB = ROOT / "REFERENCES.bib"
FIGDIR = ROOT / "figures"

README = """# Overleaf package

Two independent documents. In Overleaf, Menu -> Main document selects which one
compiles; switch between them to build both.

  manuscript.tex     the paper
  supplementary.tex  the supplement

Both use the Elsevier `elsarticle` class, which Overleaf provides. No local
class or style files are bundled. Compile with pdfLaTeX; the bibliography is
BibTeX (`elsarticle-harv`), which Overleaf runs automatically.

  REFERENCES.bib     48 entries, shared by both documents
  figures/           eight vector figures, PDF

Both .tex files are GENERATED from the Markdown sources by
`paper/tex/build_tex.mjs`. Edit the Markdown in the repository and re-run the
generator; edits made here will be overwritten on the next build. The only
difference between these copies and the repository originals is the
bibliography path, rewritten from `../REFERENCES` to `REFERENCES` so it
resolves in a flat project.
"""


def stage() -> list[str]:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    written = []

    for name in DOCS:
        src = TEX / name
        if not src.exists():
            raise SystemExit(f"missing {src} — run paper/tex/build_tex.mjs first")
        text = src.read_text(encoding="utf-8")
        new, n = re.subn(r"\\bibliography\{\.\./REFERENCES\}",
                         r"\\bibliography{REFERENCES}", text)
        if n != 1:
            raise SystemExit(f"{name}: expected exactly one ../REFERENCES bibliography, found {n}")
        (STAGE / name).write_text(new, encoding="utf-8")
        written.append(name)

    if not BIB.exists():
        raise SystemExit(f"missing {BIB}")
    shutil.copy2(BIB, STAGE / BIB.name)
    written.append(BIB.name)

    figs = sorted(FIGDIR.glob("*.pdf"))
    if not figs:
        raise SystemExit(f"no figures found in {FIGDIR}")
    (STAGE / "figures").mkdir()
    for f in figs:
        shutil.copy2(f, STAGE / "figures" / f.name)
        written.append(f"figures/{f.name}")

    (STAGE / "README.md").write_text(README, encoding="utf-8")
    written.append("README.md")
    return written


def check_every_figure_is_present() -> None:
    """Every \\includegraphics target must exist in the staged tree."""
    missing = []
    for name in DOCS:
        text = (STAGE / name).read_text(encoding="utf-8")
        for target in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", text):
            stem = Path(target)
            candidates = [STAGE / target, STAGE / f"{target}.pdf",
                          STAGE / "figures" / stem.name, STAGE / "figures" / f"{stem.name}.pdf"]
            if not any(c.exists() for c in candidates):
                missing.append(f"{name}: {target}")
    if missing:
        raise SystemExit("figures referenced but not staged:\n  " + "\n  ".join(missing))


def main() -> None:
    written = stage()
    check_every_figure_is_present()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for rel in written:
            z.write(STAGE / rel, rel)
    shutil.rmtree(STAGE)
    size = OUT.stat().st_size / 1024
    print(f"wrote {OUT} ({size:.0f} KB, {len(written)} files)")
    for rel in written:
        print(f"   {rel}")


if __name__ == "__main__":
    main()

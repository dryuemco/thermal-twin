"""Fail if a value that holds only under the original (pre-correction) Manavgat label appears in the
manuscript or the supplement without being labelled as such (readiness audit F02, WS1 tool).

A hit is allowed when the words "original label" (or "Under the original") occur within 400
characters before it in the same file, which is how the text marks an original-label value.

Usage: python paper/code/check_stale_values.py      exits 1 on any unlabelled hit.
"""
import re
import sys
from pathlib import Path

P = Path(__file__).resolve().parents[1]
FILES = ["00_abstract.md", "01_introduction.md", "02_related_work.md", "03_methods.md", "04_results.md",
         "05_discussion.md", "06_conclusions.md", "07_declarations.md", "supplementary.md", "figure_captions.tex"]
# value -> what it was under the original label (from labelfix_rerun/CHANGES.md and round5/E1_CHANGELIST.md)
STALE = {
    r"0\.888": "within-region thermal mean, original label",
    r"(?<![\d.])0\.541(?!\d)": "as-drawn transfer mean, original label",
    r"\+0\.004(?!\d)": "as-drawn paired contribution, original label",
    r"14 of 20": "directions above chance, original label",
    r"(?<![\d.])0\.537(?!\d)": "baseline transfer mean, original label",
    r"−0\.081": "feature-removal cost, original label",
    r"(?<![\d.])0\.616(?!\d)": "equalised transfer mean, original label",
    r"\+0\.143|0\.143 \[": "frame cost, original label",
    r"\+0\.155(?!\d)": "matched shortfall / negative-pool effect, original label",
    r"ρ = \+0\.84|\+0\.84 \[": "conditional diagnostic, original label",
    r"0\.797(?!\d)": "Manavgat 10-cell ceiling, original label",
    r"85 to 89 %|51 to 57 %": "few-shot recovery, original label",
    r"0\.326(?!\d)": "Manavgat to Bejís raw, original label",
    r"(?<![\d.])0\.444(?!\d)": "Bejís to Manavgat raw, original label",
    r"\+0\.022 \[−0\.032": "LOSO increment, original label",
}
OK = re.compile(r"original label|Under the original|under the original", re.I)
# Reviewed 2026-09-29: the same digits occurring as a different quantity. Table rows and interval
# bounds are skipped; the prose contexts below were each checked against their source.
REVIEWED = ["runs from 0.541 to 0.561", "+0.155 [+0.108, +0.202] more", "baseline's\n0.797 and the full",
            r"0.527 $\rightarrow$ 0.541"]
bad = []
for f in FILES:
    text = (P / f).read_text(encoding="utf-8")
    for pat, what in STALE.items():
        for m in re.finditer(pat, text):
            if OK.search(text[max(0, m.start() - 400):m.start()]):
                continue
            ls = text.rfind("\n", 0, m.start()) + 1
            if text.startswith("|", ls):                         # a table cell: a different quantity
                continue
            if re.search(r"\[[^\]]*$", text[ls:m.start()]):         # inside an interval [lo, hi]
                continue
            ctx = text[max(0, m.start() - 40):m.end() + 40]
            if any(r in ctx for r in REVIEWED):
                continue
            line = text.count("\n", 0, m.start()) + 1
            bad.append(f"{f}:{line}: {m.group(0)!r} ({what}): {text[max(0, m.start() - 60):m.end() + 40]!r}")
print("\n".join(bad) if bad else "no unlabelled original-label values")
sys.exit(1 if bad else 0)

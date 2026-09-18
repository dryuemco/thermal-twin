#!/usr/bin/env python3
"""Graphical abstract, required by Environmental Modelling & Software.

Every number is parsed from paper/04_results.md at build time rather than typed
here, so the figure cannot drift from the Results: if a value moves or its
sentence is reworded, a parse or an assert fails and nothing is written.

Left panel: the thermal block's ROC-AUC increment under holdouts of increasing
hardness (Section 4.3). Right panel: the evaluation-geometry result (Section 4.4)
and the baseline control.

Elsevier sizing: at least 1328 x 531 px, legible at 13 x 5 cm. Written at
130 x 60 mm, 300 dpi.
"""
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
RESULTS = (HERE.parent / "04_results.md").read_text(encoding="utf-8")
M = "−"  # the Results use a true minus

BLUE, ORANGE, GREY = "#0072B2", "#E69F00", "#666666"
MM = 1 / 25.4


def num(s):
    return float(s.replace(M, "-").replace("+", ""))


# ---- within region, 5 km blocking: Table 1, block = 10 cells ----------------
# Continuation rows leave the region cell empty ("| | 10 | ..."), so the region
# cell is matched with optional whitespace and carried forward.
ROW = re.compile(r"^\|\s*([^|]*?)\s*\| (\d+) \| [\d.]+ \| [\d.]+ \| ([+−][\d.]+) \| "
                 r"\[([+−][\d.]+), ([+−][\d.]+)\] \|")
rows, region = {}, None
for line in RESULTS.splitlines():
    m = ROW.match(line)
    if not m:
        continue
    region = m.group(1) or region
    if m.group(2) == "10":
        rows[region] = tuple(num(g) for g in m.groups()[2:])
assert len(rows) == 5, f"expected 5 regions at 10 cells, got {sorted(rows)}"
within = sorted(rows.values())
assert abs(within[0][0] - 0.045) < 1e-9 and abs(within[-1][0] - 0.148) < 1e-9

# ---- the hardening ladder: the Section 4.3 summary sentence -----------------
m = re.search(r"\+0\.027 on\s+a within-region half-split, \*\*\+0\.022 \[(\S+), (\S+)\]\*\* under "
              r"leave-one-scar-out, and \+0\.004\s+\[(\S+), (\S+)\] across regions", RESULTS)
assert m, "Section 4.3 hardening sentence not found verbatim"
half = 0.027
loso = (0.022, num(m.group(1)), num(m.group(2)))
xreg = (0.004, num(m.group(3)), num(m.group(4)))
assert loso[1:] == (-0.032, 0.077) and xreg[1:] == (-0.028, 0.036)

# ---- evaluation geometry and the baseline control ----------------------------
m = re.search(r"That change alone costs \*\*0\.143 \[\+(\S+), \+(\S+)\]\*\*", RESULTS)
assert m, "Section 4.4 frame-cost sentence not found verbatim"
frame = (0.143, float(m.group(1)), float(m.group(2)))
for s in ("0.541", "0.616", "0.537"):
    assert s in RESULTS, s

# ---- figure -----------------------------------------------------------------
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 8})
fig = plt.figure(figsize=(130 * MM, 60 * MM))
ax = fig.add_axes([0.255, 0.27, 0.36, 0.56])

labels = ["Within region\n(5 km blocks, 5 regions)", "Within-region\nhalf-split",
          "Whole burn scar\nwithheld", "Across regions\n(20 directions)"]
ys = [3, 2, 1, 0]
lo, hi = within[0][0], within[-1][0]
ax.plot([lo, hi], [3, 3], color=BLUE, lw=5, solid_capstyle="butt", alpha=0.35)
for v, a, b in within:
    ax.plot(v, 3, "o", color=BLUE, ms=3.5, zorder=3)
ax.plot(half, 2, "o", color=BLUE, ms=4.5, zorder=3)
for y, (v, a, b) in ((1, loso), (0, xreg)):
    ax.plot([a, b], [y, y], color=GREY, lw=1.2)
    ax.plot(v, y, "o", color=ORANGE, ms=4.5, zorder=3)
ax.axvline(0, color="black", lw=0.8, ls=(0, (3, 2)))
ax.set_yticks(ys, labels, fontsize=7)
ax.set_ylim(-0.6, 3.6)
ax.set_xlim(-0.05, 0.17)
ax.set_xlabel("Thermal-block gain (Δ ROC-AUC)", fontsize=7.5)
ax.tick_params(axis="x", labelsize=7)
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.tick_params(axis="y", length=0)
ax.set_title("Local skill does not travel", fontsize=9, fontweight="bold",
             loc="left", x=-0.62)
ax.text(0.092, 0.5, "both intervals\nspan zero", fontsize=6.5, color=GREY, va="center")

tx = fig.add_axes([0.665, 0.20, 0.33, 0.72]); tx.axis("off")
tx.text(0, 0.97, "Evaluation geometry", fontsize=9, fontweight="bold", va="top")
tx.text(0, 0.80, "Same model, scored on the\nburn scar and its 2 km collar\ninstead of region-wide, costs",
        fontsize=7, va="top")
tx.text(0, 0.50, f"{frame[0]:.3f} AUC", fontsize=11, fontweight="bold", color=ORANGE,
        va="top")
tx.text(0, 0.36, f"95% CI [{frame[1]:.3f}, {frame[2]:.3f}]", fontsize=7, color=GREY, va="top")
tx.text(0, 0.22, "Equal 10 km frames lift mean\ntransfer 0.541 → 0.616; the\nstatic baseline transfers no\n"
        "better (0.537 vs 0.541 as drawn).", fontsize=7, va="top")
fig.text(0.02, 0.025, "Measure transfer skill on the target region before relying on a model there.",
         fontsize=7, style="italic", color=GREY)

out = HERE / "graphical_abstract"
fig.savefig(out.with_suffix(".png"), dpi=300)
fig.savefig(out.with_suffix(".pdf"))
(HERE / "graphical_abstract_provenance.json").write_text(json.dumps({
    "figure": "Graphical abstract (EMS requirement)",
    "script": "paper/figures/graphical_abstract.py",
    "data": "parsed at build time from paper/04_results.md: Table 1 (block 10), the Section 4.3 "
            "hardening sentence, the Section 4.4 frame-cost sentence",
    "within_region_5km": {k: v[0] for k, v in rows.items()},
    "half_split": half, "leave_one_scar_out": loso, "across_regions": xreg,
    "frame_cost": frame, "canvas_mm": [130, 60], "dpi": 300,
}, indent=1, ensure_ascii=False), encoding="utf-8")
print("wrote", out.with_suffix(".png").name, out.with_suffix(".pdf").name)

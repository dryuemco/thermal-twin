# Muğla, the fifth row of the compositing table

Run 2026-08-14, completing the four-region audit reported in `compositing_second_region.md`.

**Scene inventory (current window), from `scene_manifest.csv`:**

| Quantity | Value |
|---|---|
| WRS tiles | 179/34, 179/35, 180/34, 180/35, 181/34 |
| Distinct WRS paths | 3 |
| Distinct WRS rows | **2** |
| Scenes | 18 |
| Distinct acquisition dates | 11 |
| Scenes per distinct date | **1.6** |

**Boundary audit (positive = the date-balanced chain lowers the discontinuity):**

| Boundary type | Status | Point estimate | 95 % interval |
|---|---|---:|---|
| same-day multiplicity edge | supported reduction | **+0.194** | [+0.172, +0.221] |
| scene-count edge | supported reduction | +0.022 | [+0.009, +0.036] |
| source scene path/row | supported reduction | +0.002 | [+0.000, +0.003] |
| unique-date-count edge | **supported increase** | −0.031 | [−0.046, −0.016] |
| export tile boundary | insufficient evidence | −0.000 | [−0.001, +0.001] |

**Reading.** Muğla confirms the rule and strengthens its mechanism. It spans two WRS **rows**, so a
single overpass delivers two scenes bearing the same date, and scenes per date is therefore above
one. The intervention can act, and it does: the largest reduction in the cohort, +0.194, falls on
the same-day multiplicity edge, which is exactly the discontinuity the date-balanced chain targets.

The verdict is nevertheless **uncertain**, for the same reason as Bejís: the chain improves the
boundary it targets and makes the unique-date-count edge worse. Two of the three regions where the
intervention can act therefore give mixed results, and only Manavgat improves consistently.

**The downstream comparison is not admissible here.** The run reports
`canonical_reproduction: not_available` and `final_status: canonical_reproduction_failed`, the known
consequence of absolute paths recorded by another operator in `predictor_export_metadata.json`. The
±0.02 AUC tolerance therefore still rests on Manavgat alone, as `compositing_second_region.md` states.

**Effect on the companion paper.** Section 4.3's table gains a fifth row and its summary sentence
changes: scenes per date is above one in **three** regions of five, not two of four, and the
intervention acts in all three while improving consistently in only one. The rule itself is
unchanged and now rests on five regions rather than four.

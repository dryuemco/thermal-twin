# The compositing intervention does not replicate in a second region

Section 5.11(xi) records that the Landsat compositing tolerance of about ±0.02 AUC "was audited for
one region only; the other four are unaudited on this axis". With Earth Engine access obtained on
2026-08-14 the audit was extended to a second region, Bejís, chosen because it carries the highest
gap-filled share of the five (9.70 %) and is therefore the most exposed to how the composite is
built.

Run with the pipeline's own `landsat_composite_counterfactual_audit` at `48b56e7`, 152 source scenes,
60 exported diagnostic rasters, project `thermaltwin`. No code was modified: the Manavgat-only gate
in the downstream tool is a waiver for the zero-filled MODIS signature, and Bejís needs no waiver
because it carries no exact zeros at all.

## The reference chain reproduces

Before any comparison, the diagnostic's scene-weighted chain was checked against the frozen canonical
products. **Eight of the nine semantic checks pass and six of those are exact**: `current_lst_median`,
`current_lst_valid_count` and the four annual baselines all reproduce with a maximum absolute
difference of 0, and the two derived products at 2.7×10⁻⁵ and 2.2×10⁻⁵, which is float32 recomputation
noise. The gate's overall verdict is `pass`.

## The intervention's premise does not hold in Bejís

`reduction = absolute_jump_scene_weighted - absolute_jump_date_balanced`, so a positive value means
date-balanced compositing lowers the discontinuity. Current LST, paired bootstrap over boundary
segments:

| Boundary type | Manavgat 2021 | Bejís 2022 |
|---|---|---|
| `scene_count_edge` | **supported_reduction**, +0.125 | uncertain, +0.004 [−0.023, +0.033] |
| `unique_date_count_edge` | **supported_reduction**, +0.095 | **supported_increase**, −0.067 [−0.095, −0.041] |
| `same_day_multiplicity_edge` | **supported_reduction**, +0.597 | **supported_reduction**, +0.378 [+0.278, +0.483] |
| `source_scene_path_row` | **supported_reduction**, +0.004 | uncertain, −0.001 [−0.004, +0.001] |
| **Overall** | **supported_reduction** | **uncertain** |

In Manavgat every boundary type improves. In Bejís only the one the intervention directly targets
improves, same-day duplication, while unique-date-count edges get **worse** with interval support,
and the scene-count and path/row boundaries are indistinguishable from no effect. The overall verdict
is therefore `uncertain`.

This is not a difference in how many Landsat paths each AOI spans. Both span two: Manavgat 177 and
178, Bejís 198 and 199. What differs is the balance. Manavgat's current window draws 3, 3, 4 and 4
scenes from its four path/row tiles, so support is uneven between the overlap and the single-path
zones; Bejís draws 4, 4, 4 and 4 over 8 distinct dates.

## The downstream A/B is refused, correctly

The downstream tool stops with `source counterfactual final_status must be 'supported_reduction', got
'uncertain'`. That is its decision rule working as designed rather than a failure: with no established
net seam improvement upstream, there is no intervention effect to propagate into a ΔAUC comparison.
The ±0.02 figure therefore has no Bejís counterpart, and cannot acquire one until the upstream
premise is met.

## What this changes in the manuscript

The compositing tolerance should not be described as a quantity awaiting measurement in four more
regions. In the one further region now audited, **the intervention that produces it does not
replicate**, so ±0.02 is a Manavgat-specific sensitivity rather than a cohort-wide tolerance. That is
a stronger and more useful statement than "unaudited", and it is also more cautious: it removes any
implication that the other four regions would show the same spread.

## Provenance

`repo/outputs/diagnostics/landsat_composite_counterfactual/bejis_2022/` holds the run, with
`paired_boundary_comparison.csv`, `canonical_reproduction.json`, `counterfactual_summary.md` and
`manifest.json`. Manavgat's frozen comparator is
`drive_new/diagnostics/landsat_composite_counterfactual/manavgat_2021/`. Canonical comparators for
Bejís were staged into the pipeline's own gitignored `outputs/` tree from `drive_new/`; nothing under
version control was modified and `repo/` remained clean throughout.

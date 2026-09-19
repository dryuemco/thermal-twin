# Pilot frozen — 2026-09-19

The five-region manuscript in this folder is **not being submitted**. On 2026-09-19 the authors decided
to redesign the study from scratch as a generalisable research infrastructure (about ten regions × 3–5
fire seasons, weather and other drivers, a new tested pipeline, a committed pre-registration) and to
write a short EMS paper from that. This folder is frozen as the pilot that motivated the redesign.
Git tag: `pilot-v1-frozen`.

## State at freeze

**Done and verified**
- Hash-verified inputs (`paper/code/_canonical.py`); leakage assertion at every fit.
- Manavgat label corrected (`paper/data/manavgat_2021/LABEL_CORRECTION.md`) and made primary.
- Re-runs on the corrected label: the paper's own scripts (`paper/labelfix_rerun/{code,geometry,
  inference,labels,step10}`, `CHANGES.md`) and every upstream pipeline producer
  (`paper/labelfix_rerun/pipeline/`, `RUN_LOG.md`; controls reproduce the frozen outputs).
- Referee-round-5 analyses (`paper/ems_analyses/`) and their corrected re-runs.

**Stopped, not results**
- Round 3 (`paper/labelfix_rerun/round3/`, git-ignored, partial): B-dependent scripts (anomaly-only,
  feature drop, distance curve, collar increment, diagnostics), few-shot recovery, marginal AoA, window
  closure. The CORAL λ sweep on the corrected label did not complete.
- The manuscript text was never rewritten to the corrected numbers: `0*.md` still carry frozen-label
  values in many places. **Do not quote numbers from the manuscript text; quote the CHANGES/RUN_LOG files.**

## What the pilot established (corrected label)
- Within-region thermal increment is real under spatial blocking (Manavgat +0.067 / +0.062 / +0.047 at
  1 / 5 / 10 km; all five regions' intervals exclude zero).
- Evaluation extent moves ROC-AUC by as much as the predictors: frame cost 0.133 [0.059, 0.207]; it
  survives edge exclusion and is not reproduced by placebo collars (near-field effect).
- Cross-region transfer of the thermal block is small and unstable (paired +0.007 as drawn; +0.024 on
  equalised frames, excluding zero under 2 of 5 resampling units); label-free adaptation mostly moves
  transfer towards chance.
- With the corrected label, bootstrap-supported sign reversals rise from 3 to 14, including Manavgat's
  elevation, LST and TVDI channels.

## Design lessons carried into the redesign
1. **Frames by rule, before any predictor or label is seen.** Hand-drawn AOIs made the headline results
   partly a property of how five rectangles were drawn.
2. **More than one fire season per region.** Region and event meteorology were confounded.
3. **Weather and human drivers as predictors**, not only as a limitation.
4. **Tested pipeline.** The Manavgat label defect (month-aligned query bug, export before the fix) and the
   overwritten inputs of 2026-08-14 would both have been caught by simple tests and hash checks.
5. **Pre-register estimands, resampling units, margins and multiplicity before computing anything.**
   Most controls here were added after results were seen.
6. **Non-redundant predictors.** The six thermal channels are two dimensions.
7. **Prevalence-robust metrics and label-quality sensitivity** (burned fraction, pre-label and
   earlier-year burns, a second burned-area product) from the start.

# Supplementary S1. Target-label recovery curve: what a small labelled budget buys

> Drafting note. Source: the frozen diagnostic
> `drive_new/diagnostics/few_shot_recovery/7e4ca051c3e83074391652e28a163138129c1cb6610f8826248a90cd3d19409a/`
> (`recovery_curve.csv`, `summary.json`, `config.json`, `target_block_inventory.csv`,
> `validation_report.json`). No model was refitted for this supplement; every number below is read
> from that export. Referenced from Discussion §5.5.
>
> Consistency pass 2026-08-13. One change, no numbers added or altered. The lead sentence of S1.3
> called the top budget "a modest labelled budget", which contradicts limit 4 in S1.4. It now names
> the budget for what it is and points at that limit. The Conclusions were corrected in the same
> pass and no longer claim that a modest burned-area record suffices.
>
> Blocking-scale pass 2026-08-13. Swept for claims of interval support on a named transfer
> direction, after `paper/transfer_ci_blocksize.md`. None was found and nothing was changed. The
> two places that mention raw transfer above chance, S1.1 and the third observation of S1.3, name
> Bejís to Muğla at its point estimate of 0.618. That direction is CI-supported above chance at both
> the 1 km and the 5 km blocking, so no qualifier is owed. The selection intervals of this supplement
> are a separate quantity and are unaffected: they are drawn over block selections, not over a
> spatial-block bootstrap, as S1.2 states.

## S1.1 Purpose and status

The main text establishes that label-free alignment does not close the residual transfer gap, and
that the part of that gap not attributable to contiguous spatial holdout is conditional. CORAL and per-region standardisation
recover a minority of the gap at best, and degrade most of the directions that transfer above chance
without them (§4.5, §4.8, §5.5). Within the six directions covered here, the direction that
transfers above chance raw is Bejís to Muğla, and it is the direction that both interventions help
least. The natural constructive question is therefore what a *small number of target labels* buys,
since that is the resource label-free machinery cannot substitute for.

The headline of this analysis is in the main text at §4.12. Its ceilings and denominators are
computed on the frames as drawn, which §4.4 shows are not comparable across regions; the recovery
fractions should be read as within-frame quantities. The full design, the per-budget table
and the limits are here, for two reasons. It covers three of the five regions, so it cannot carry a
claim at the paper's stated scope; and it requires labelled target cells, so it is not an
alternative transfer protocol but a quantification of the price of the failure the main text
documents. It is a supplementary sensitivity result, not a proposed method.

## S1.2 Design

**Regions and directions.** Three experiments are used in all six ordered directions: Manavgat 2021,
Bejís 2022 and Muğla 2021. Evia is excluded by the frozen configuration on two recorded grounds
(`evia_2021`: out of scope for this analysis; `evia_2021_extended`: a high-prevalence,
different-regime sensitivity control rather than an equal-prevalence primary transfer AOI), and
Montiferru does not appear in it. Population, feature sets, forbidden-column set and classifier are
the manuscript's primary choices throughout: natural vegetation (`burnable_tree_shrub_grass` ∧
`valid_for_modeling`), the ten-feature thermal set as the primary family with the four-feature
baseline set as secondary, and the canonical random forest (300 trees, `min_samples_leaf = 3`,
`class_weight = "balanced"`, `random_state = 42`).

**Labelled budget.** The unit of labelling effort is a 10-cell (≈ 5 km) spatial block, assigned
before population filtering, identical to the large-block machinery of §3.7. The configuration
records why the canonical 2-cell block is not used here: at ≈ 1 km a block holds a median of about
four cells, which is neither a plausible unit of survey effort nor separable from the evaluation
blocks adjacent to it. Budgets are 0, 1, 2, 4, 8, 16 and 32 blocks. Budget 0 is the raw transfer
endpoint, which is the source-only model with no target labels. The ceiling is the target-only model
evaluated under the same folds.

**Selection and evaluation.** Blocks are drawn under a fixed tier order (blocks containing both
classes, then burned-only, then unburned-only), shuffled within tier by a seed derived as
`blake2b(schema|source|target|outer_fold|repeat)`. The seed is independent of the budget, of the
model family and of any result, so no branch of the selection can react to an outcome. Budgets are
nested: the 32-block set contains the 16-block set. Evaluation is 5-fold `StratifiedGroupKFold`
grouped on the target's large blocks, in strict mode. Each budget is repeated 10 times with
different block draws (the raw and ceiling endpoints once each, being deterministic), for 3,642
unique fits, matching the configuration's own expected count.

**Uncertainty.** The interval reported is a **selection interval**: the 2.5th and 97.5th percentiles
across the 10 block-selection repeats. It expresses sensitivity to *which* blocks were labelled and
nothing else. It is not a bootstrap, it is not a confidence interval, and no *p*-values are
produced; the diagnostic enforces this distinction with a forbidden-terminology check. There is
consequently no comparable interval on the raw endpoint, which is a single deterministic fit.

**Recovery fraction.** Defined as (few-shot − raw) / (ceiling − raw), neither clipped nor
absolute-valued, so a budget that leaves the model worse than raw transfer reports a negative
fraction rather than zero.

## S1.3 Result

**Table S1. Few-shot recovery of target ROC-AUC, thermal model, natural-vegetation population.** Raw
= source-only transfer (budget 0); ceiling = target-only model at the same 10-cell blocking. Values
are the mean over 10 block-selection repeats. Read from `recovery_curve.csv`.

| Direction | Raw | 1 blk | 2 blk | 4 blk | 8 blk | 16 blk | 32 blk | Ceiling | Recovered at 32 |
|---|---|---|---|---|---|---|---|---|---|
| Manavgat → Bejís | 0.326 | 0.475 | 0.500 | 0.607 | 0.659 | 0.724 | 0.772 | 0.824 | 89 % |
| Muğla → Bejís | 0.583 | 0.578 | 0.603 | 0.625 | 0.666 | 0.743 | 0.789 | 0.824 | 85 % |
| Bejís → Manavgat | 0.444 | 0.454 | 0.435 | 0.504 | 0.575 | 0.637 | 0.743 | 0.797 | 85 % |
| Muğla → Manavgat | 0.401 | 0.413 | 0.420 | 0.447 | 0.471 | 0.517 | 0.626 | 0.797 | 57 % |
| Manavgat → Muğla | 0.470 | 0.483 | 0.495 | 0.510 | 0.539 | 0.589 | 0.627 | 0.777 | 51 % |
| Bejís → Muğla | 0.618 | 0.576 | 0.577 | 0.578 | 0.598 | 0.637 | 0.666 | 0.777 | 30 % |

Selection intervals are wide at the smallest budgets and narrow at the largest. For Bejís → Manavgat
they run [0.392, 0.484] at one block against [0.733, 0.748] at 32. See the caution in S1.4 on why
the upper-budget intervals are narrow.

Three observations follow, and only the first is comfortable.

**The largest budget tested recovers most of the gap in three of six directions.** Thirty-two blocks
carry on average 2,700 to 3,000 labelled cells, roughly 7 to 20 % of the target's natural-vegetation
population depending on the region. At that budget three directions stand at 85 to 89 % of their
target-only ceiling: Manavgat → Bejís and Bejís → Manavgat started below chance, Muğla → Bejís at
0.583, above it. The residual the main text documents is
therefore expensive but not structural: it is a shortage of target-conditional information, and
target labels supply exactly that. That budget should not be described as modest. Limit 4 below
gives the reason: for these AOIs the top budget already contains most of the target's burned cells.

**The recovery is slow where the transfer is worst.** The two directions into Muğla and Manavgat
from Muğla reach only 51 to 57 % at the top budget. These are the directions whose raw transfer sits
furthest below the ceiling, and Muğla → Manavgat is still below 0.5 AUC after 8 labelled blocks. A
larger concept gap costs more labels, not the same labels.

**Small budgets actively hurt the one direction that already transfers.** Bejís → Muğla is the pair
that transfers above chance raw (0.618), and it is the pair few-shot recalibration helps least: the
curve is *negative* at 1, 2, 4 and 8 blocks (−0.043 to −0.021 AUC), only overtakes raw at 16, and
reaches 30 % at 32, the worst of the six. This is the same asymmetry the main text reports for
label-free adaptation (§4.5): where the source model already carries a usable conditional
relationship, a small target sample perturbs it before it can replace it. The mechanism differs,
since here the target labels are real information rather than a covariate rescaling. The direction
of the effect is nevertheless the same, and it is the one direction where the intervention is a
liability at every budget a field campaign would plausibly afford.

## S1.4 Methodological limits

These are stated so the analysis is not read as more than it is.

1. **Three regions, six directions.** Evia and Montiferru are absent, so this covers six of the
   twenty directed pairs in the main analysis and cannot speak to the five-region scope.
2. **It requires labelled target cells.** The budget axis is labels in the target region. Nothing
   here is a label-free method and nothing here weakens the paper's negative result about
   label-free alignment. It prices that result.
3. **No joint analysis with the conditional index.** Whether the labelled budget needed to reach a
   given recovery fraction is predicted by the conditional sign-agreement index of §3.11 was not
   computed. With six directions it would in any case be a description rather than a test.
4. **The interval is a selection interval, and it narrows for a reason that is not precision.**
   Bejís holds only 15 blocks containing both classes and 19 containing any burned cell; Manavgat
   26 and 28; Muğla 60 and 70. At 16 and 32 blocks the tiered draw has nearly exhausted the
   both-class blocks, so repeats select almost the same set. The mean labelled-positive count into
   Bejís is identically 860.0 at 16 blocks and 880.0 at 32 across both source regions. The narrow
   upper-budget intervals therefore reflect a saturated selection pool, not a well-estimated
   quantity, and the top budget is not a small budget for these AOIs: 880 of Bejís's 1,100 burned
   cells are inside it.
5. **The ceiling is the 10-cell-block target-only value**, not the ≈ 1 km within-region headline of
   Table 3, and is correspondingly lower (0.777 to 0.824 against 0.859 to 0.918). Recovery fractions are
   only interpretable against this matched-blocking ceiling.
6. **Ceiling reproduction verified for all three targets.** Manavgat, Bejís and Muğla all reproduce
   the frozen large-block artefacts exactly, at an absolute difference of 0.0 against a 10⁻⁹
   tolerance in both families. An earlier draft of this supplement recorded Muğla as unverified,
   because at that time no frozen block-10 artefact had been located for it; one is now referenced
   in the export and the corresponding validator check passes.
7. **Provenance.** The export of record was regenerated on 2026-08-14 at commit `6d7a6a71` under
   scikit-learn 1.9.0, pandas 3.0.2 and NumPy 2.4.4 — the same scikit-learn version to which every
   other number in this paper is fixed. Its validator reports **67 PASS, 0 FAIL and 0 SKIPPED**.
   Two files in the export directory, `repeat_metrics.csv` and `oof_predictions.parquet`, retain
   their 2026-08-03 timestamps and were not regenerated; every value quoted in Table S1 was checked
   against the regenerated export.

## S1.5 Figure

A recovery curve is the natural presentation, and it is prepared from `recovery_curve.csv` (thermal
family, `metric = roc_auc`). Budget goes on a log-2 axis and target ROC-AUC on the ordinate. Each
direction is one line, the selection interval is drawn as a band, and each direction's ceiling is a
horizontal reference. Numbers are as in Table S1.

# Results inventory — what the archives actually contain

**This is a data catalogue, not the Results section.** It records what was found in the four
`stdt-*.zip` archives, read on 2026-07-23 without extracting anything into the project tree
(extraction went to the session scratchpad). Numbers here are transcribed directly from the JSON
outputs. Results and Discussion remain unwritten.

Provenance of every number below: `experiments/<region>/step8a/step8a_dataset_stats.json`,
`experiments/<region>/step8c/step8c_bootstrap_metrics.json`,
`cross_region/<pair>/step9b/cross_region_transfer_metrics.json`,
`cross_region/<pair>/step10/step10_metrics.json` and `step10_bootstrap_summary.json`.
Pipeline git commit recorded in the transfer outputs: `c648486d823faf1b6d9f39ea84c0dec4e9d7f8c2`.

---

## 0. Archive completeness — READ THIS FIRST

The four archives are Google Drive multi-part downloads named `-1-002`, `-1-006`, `-1-007`,
`-1-008`. **Parts 001, 003, 004 and 005 are absent.** These are not split-volume archives — each
zip is independently readable and holds a distinct subset of files — so the consequence is that
roughly half of the exported file set is simply not present locally.

Known casualties:

- `experiments/evia_2021/step8b/` and `experiments/evia_2021/step8e/` appear as **empty directory
  entries**. Evia's within-region model comparison report is therefore missing, even though its
  Step8C bootstrap metrics (which depend on Step8B predictions) *are* present.
- `experiments/evia_2021/validation/labels/burned_landcover_gate.json` is missing, so Evia's gate
  verdict could not be read.
- No Step10 (adaptation) outputs exist for any Evia pair — see §3.

Everything needed for the four-region within-region analysis and the twelve-pair raw transfer
matrix **is** present. What is missing is Evia's Step8E report, Evia's gate verdict, and adaptation
for the Evia pairs.

---

## 1. Regions and datasets

| Region | AOI (W,S,E,N) | Predictor window | Label window | Total cells | Burned cells | Burned rate | Natural-veg cells | Burned within natural veg | Prevalence in natural veg |
|---|---|---|---|---|---|---|---|---|---|
| Manavgat 2021 | 31.05, 36.72, 31.85, 37.35 | 2021-06-01 → 07-27 | 2021-07-28 → 08-31 | 24 150 | 796 | 3.30 % | 20 555 | 784 | **3.82 %** |
| Bejís 2022 | −1.05, 39.68, −0.35, 40.15 | 2022-06-15 → 08-14 | 2022-08-15 → 09-30 | 15 759 | 1 103 | 7.00 % | 15 190 | 1 100 | **7.24 %** |
| Muğla 2021 | 27.10, 36.60, 28.90, 37.45 | 2021-06-01 → 07-28 | 2021-07-29 → 09-15 | 73 098 | 3 073 | 4.21 % | 41 772 | 2 911 | **6.98 %** |
| North Evia 2021 | 23.12, 38.68, 23.52, 39.08 | 2021-06-05 → 08-02 | 2021-08-03 → 09-30 | 7 744 | 2 789 | **36.09 %** | 3 957 | 2 663 | **67.29 %** |

`out_of_window_burndate_cells = 0` in all four regions. Cropland is excluded from the primary
burnable mask in all four.

**Gate verdicts** (Evia's file is in a missing archive part):

| Region | Burned cells assessed | Natural-vegetation fraction | Cropland fraction |
|---|---|---|---|
| Manavgat | 796 | 0.9837 | 0.0025 |
| Bejís | 1 103 | 0.9909 | 0.0091 |
| Muğla | 3 026 | 0.9584 | 0.0129 |
| North Evia | — | `[MISSING]` | `[MISSING]` |

The three readable regions pass the natural-vegetation gate comfortably.

### 1.1 `[BLOCKING PROBLEM]` North Evia is not comparable to the other three

Evia's AOI is 0.40° × 0.40° — by far the smallest of the four, roughly 35 × 44 km — and the 2021
North Evia fire burned a large fraction of it. The result is a burned rate of **36.1 % over all
cells and 67.3 % within the natural-vegetation population**, against 3.8–7.2 % in the other three
regions. The AOI is, in effect, the fire scar plus a thin margin.

This is not a minor imbalance difference; it changes what the metrics mean.

- **PR-AUC becomes uninterpretable across regions.** A random classifier scores 0.67 on Evia and
  0.04–0.07 elsewhere. Every reported PR-AUC for transfers *into* Evia (0.79–0.82) is close to the
  no-skill baseline, not evidence of skill.
- **ROC-AUC into Evia is inflated by the negative class being small and atypical.** The 1 283
  unburned natural-vegetation cells are a thin, spatially peripheral rim rather than a
  representative sample of unburned landscape.
- **Evia's own within-region baseline is suspiciously strong** — 0.9445 ROC-AUC on `all_valid` from
  terrain, greenness and land cover alone, the highest baseline of any region — which is exactly
  what one expects when the label is nearly coextensive with a geographically compact patch.
- The pipeline's own Step8A sanity check treats `burned_rate > 0.5` as fatal. Evia passes only
  because the *overall* rate is 0.36; the population actually modelled sits at 0.67.

**Recommendation:** either enlarge the Evia AOI substantially and re-run from Step1, or drop Evia
from the manuscript and present a three-region study. Reporting Evia alongside the others without
addressing this will draw a well-founded reviewer objection. A defensible middle path is to keep
Evia only as a within-region replication and exclude it from the transfer matrix, stating why.

---

## 2. Within-region results — the thermal increment replicates in all four regions

Natural-vegetation population, spatial-block CV, spatial-block bootstrap 95 % CI (1000 replicates,
paired delta). Source: `step8c_bootstrap_metrics.json`.

| Region | Population | Baseline AUC | Thermal AUC | ΔAUC | ΔAUC 95 % CI | Verdict |
|---|---|---|---|---|---|---|
| Manavgat | natural veg | 0.8027 | 0.8696 | **+0.0669** | [+0.0546, +0.0786] | positive support |
| Bejís | natural veg | 0.8617 | 0.9178 | **+0.0561** | [+0.0479, +0.0653] | positive support |
| Muğla | natural veg | 0.7433 | 0.8590 | **+0.1157** | [+0.1059, +0.1249] | positive support |
| North Evia | natural veg | 0.8136 | 0.8984 | **+0.0848** | [+0.0721, +0.1002] | positive support |
| Manavgat | all valid | 0.8277 | 0.8866 | +0.0589 | [+0.0490, +0.0684] | positive support |
| Bejís | all valid | 0.8688 | 0.9171 | +0.0482 | [+0.0398, +0.0571] | positive support |
| Muğla | all valid | 0.8410 | 0.9132 | +0.0722 | [+0.0667, +0.0776] | positive support |
| North Evia | all valid | 0.9445 | 0.9667 | +0.0222 | [+0.0179, +0.0268] | positive support |

**Every ΔAUC interval excludes zero, in both populations, in all four regions.** Core finding 1 is
now a four-region replication (three, if Evia is dropped). Muğla shows the largest increment of any
region, roughly twice Bejís's.

Reproduction note: Manavgat 0.8027 / 0.8696 and Bejís 0.8617 / 0.9178 match the numbers already in
`CLAUDE.md` to the reported precision, so this archive is consistent with the earlier two-region
analysis.

---

## 3. Cross-region transfer — full 12-pair matrix, raw (no adaptation)

Thermal feature set, natural-vegetation population, source-only fitting, target ROC-AUC.
Source: `step9b/cross_region_transfer_metrics.json`. **Rows = source, columns = target.**

| source ↓ / target → | Manavgat | Bejís | Muğla | Evia* |
|---|---|---|---|---|
| **Manavgat** | — | **0.3258** | **0.4702** | 0.6623 |
| **Bejís** | 0.4435 | — | **0.6185** | 0.3970 |
| **Muğla** | **0.4010** | **0.5832** | — | 0.6300 |
| **Evia*** | 0.6697 | 0.3778 | 0.5719 | — |

\* Evia columns and rows are compromised by the prevalence problem in §1.1 and should not be
interpreted alongside the others.

Baseline-feature-set transfers, for comparison: Man→Bej 0.3322, Man→Muğ 0.5079, Bej→Man 0.4209,
Bej→Muğ 0.5922, Muğ→Man 0.5215, Muğ→Bej 0.4507.

### 3.1 The proximity result, with bootstrap intervals

Restricting to the three comparable regions, the six ordered pairs split cleanly, and the split is
the opposite of what similarity would predict. Intervals from `step10_bootstrap_summary.json`
(thermal, raw, 1000 valid replicates each).

| Pair | Relationship | Direction | Raw ROC-AUC | 95 % CI | Position vs chance |
|---|---|---|---|---|---|
| **Manavgat ↔ Muğla** | same country, same fire year, ~200 km, similar bioclimate | Man→Muğ | 0.4699 | [0.4515, 0.4881] | **entirely below 0.5** |
| | | Muğ→Man | 0.4016 | [0.3778, 0.4259] | **entirely below 0.5** |
| **Bejís ↔ Muğla** | different country, different year, ~2500 km | Bej→Muğ | 0.6185 | [0.6008, 0.6346] | **entirely above 0.5** |
| | | Muğ→Bej | 0.5827 | [0.5607, 0.6073] | **entirely above 0.5** |
| Manavgat ↔ Bejís | different country, different year | Man→Bej | 0.3257 | [0.3045, 0.3489] | entirely below 0.5 |
| | | Bej→Man | 0.4429 | [0.4078, 0.4799] | entirely below 0.5 |

**This is stronger than the claim as previously drafted.** It is not merely that the similar pair
performs worse on a point estimate: all four relevant intervals are disjoint from 0.5, and they fall
on opposite sides in the two pairs, in both directions of each pair. The sufficiency claim —
geographic and bioclimatic similarity are not sufficient for transfer — is supported by four
interval-separated directions, not by a single point comparison.

Note also that Manavgat↔Bejís also fails, so the pattern is not "distance helps". The honest
summary is that similarity does not determine the outcome in either direction, and that Muğla is the
only region that participates in any successful transfer.

---

## 4. Effect of label-blind adaptation — it degrades the pair that works

Thermal set, natural vegetation. Source: `step10_metrics.json` / `step10_bootstrap_summary.json`.
Adaptation exists only for the Manavgat / Bejís / Muğla pairs.

| Direction | within (target) | raw | region-wise z | CORAL |
|---|---|---|---|---|
| Man→Bej | 0.9178 | 0.3257 | 0.4764 | 0.5103 |
| Bej→Man | 0.8696 | 0.4429 | 0.4565 | 0.5562 |
| Man→Muğ | 0.8590 | 0.4699 | 0.4300 | 0.4423 |
| Muğ→Man | 0.8696 | 0.4016 | 0.5596 | 0.5596 |
| **Bej→Muğ** | 0.8590 | **0.6185** | **0.5176** | **0.5063** |
| **Muğ→Bej** | 0.9178 | **0.5827** | **0.5349** | **0.5603** |

**New finding the two-region analysis could not see: adaptation behaves as a regression toward
chance, not as a recovery of skill.** It improves the strongly anti-predictive directions
(Man→Bej +0.18, Muğ→Man +0.16) and *damages* both directions of the only pair that transfers
(Bej→Muğ −0.11, Muğ→Bej −0.02 to −0.05). After adaptation, every one of the six directions sits in
0.43–0.56 — a narrow band around 0.5.

The natural reading is that region-wise standardisation and covariance alignment are destroying
between-region structure indiscriminately, including the structure that carried genuine transferable
signal in the Bejís–Muğla pair. This materially complicates the existing "recovered = adapted −
raw" decomposition: with a negative recovered term for the working pair, the covariate/concept split
as currently defined is not meaningful for every direction, and the framing in
`03_methods.md` §3.12 will need a stated convention for negative recovery.

`[DECISION REQUIRED]` How to report decomposition when `adapted < raw`. Options: report the
recovered fraction as negative and say so plainly; restrict the decomposition to directions where
adaptation helps and report the others separately; or reframe the whole section around the
regression-toward-chance observation, which is arguably the more interesting result.

---

## 5. What is present, by pair

| Pair directory | step9a | step9b | step9c | step9d | step9e | step10 |
|---|---|---|---|---|---|---|
| manavgat_2021__bejis_2022 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| manavgat_2021__mugla_2021 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| mugla_2021__manavgat_2021 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| bejis_2022__mugla_2021 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| mugla_2021__bejis_2022 | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| manavgat_2021__evia_2021 | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| bejis_2022__evia_2021 | ✓ | ✓ | ✓ | ✓ | ✓ | — |
| mugla_2021__evia_2021 | ✓ | ✓ | ✓ | ✓ | ✓ | — |

Also present and not yet examined in detail: `step9e` distribution-shift audits including
`relationship_direction_flips.csv` and `label_conditional_feature_relationships.csv` for all eight
pair directories — these are the concept-shift evidence for the new regions and should be read
next; `diagnostics/`, `robustness/` and `teshis_sonuclari.xlsx` in archive part 002.

---

## 5b. Direction reversals — the conditional mechanism, read at n = 4

Source: `cross_region/<pair>/step9e/relationship_direction_flips.csv`, natural-vegetation
population. These are **signed** univariate AUCs against `burned`, so a value above 0.5 means higher
predictor values go with burning and below 0.5 means the opposite. Because each region's value is
the same in every pair it appears in, the eight pair files collapse to one per-region table — which
is itself a useful consistency check, and it holds.

| Feature | Manavgat | Bejís | Muğla | Evia* |
|---|---|---|---|---|
| `current_lst_mean` | **0.538** | 0.477 | **0.325** | 0.416 |
| `current_tvdi_mean` | **0.552** | 0.517 | **0.336** | 0.375 |
| `downscaled_lst_mean` | **0.552** | 0.484 | **0.307** | 0.415 |
| `fused_lst_mean` | **0.540** | 0.481 | **0.325** | 0.414 |
| `lst_anomaly_mean` | 0.482 | 0.418 | 0.485 | 0.549 |
| `tvdi_difference_mean` | 0.449 | 0.513 | 0.490 | 0.521 |
| `elevation_mean` | **0.374** | 0.643 | 0.611 | 0.647 |
| `ndvi_mean` | 0.636 | 0.559 | 0.662 | 0.531 |
| `slope_mean` | 0.531 | 0.521 | 0.637 | 0.521 |

\* Evia subject to the prevalence problem in §1.1.

**(a) The elevation reversal is Manavgat-specific, not a general regional phenomenon.** At n = 2 the
finding was "elevation reverses between Manavgat and Bejís". At n = 4 the picture is different:
Bejís, Muğla and Evia all agree that burned cells sit *higher* (0.61–0.65) and only Manavgat says
they sit *lower* (0.374). The correct statement is that three regions agree and Manavgat dissents —
which is a weaker claim about elevation as a general reversing feature, and a stronger, more
specific claim about Manavgat.

**(b) The static predictors never reverse; the thermal ones do.** `ndvi_mean` (0.531–0.662) and
`slope_mean` (0.521–0.637) stay on the same side of 0.5 in all four regions. The absolute thermal
channels span 0.307–0.552 — that is, they cross 0.5 — and `current_tvdi_mean` spans 0.336–0.552.
**This is the paper's thesis observed at the level of individual features:** the block that gains
the most within region is exactly the block whose predictor–response direction is not stable
between regions, while the static baseline block keeps its direction everywhere.

**(c) The anomaly-referenced channels are the least unstable thermal features.**
`lst_anomaly_mean` (0.418–0.549) and `tvdi_difference_mean` (0.449–0.521) sit close to 0.5
everywhere — weak, but not wildly reversing — whereas the absolute channels swing hardest. This is
consistent with the argument that referencing a variable to its own local baseline buys stability at
the cost of strength, and it is a natural hook for the Discussion.

**(d) TVDI's theoretical portability advantage does not materialise.** TVDI is internally normalised
by construction, which the Introduction flags as a reason to expect it to travel better than raw
LST. It does not: `current_tvdi_mean` reverses as hard as the absolute channels (0.552 in Manavgat,
0.336 in Muğla). Report this plainly — an internally normalised index is still statistically, not
physically, normalised.

### 5b.1 `[KEY RESULT]` Direction agreement orders transfer where similarity does not

Counting, per region pair, how many of the nine features fall on the **same side of 0.5** in both
regions:

| Pair | Features agreeing (of 9) | Mean raw transfer AUC (both directions) | Geographic / bioclimatic similarity |
|---|---|---|---|
| **Bejís ↔ Muğla** | **7** | **0.601** | lowest (different country, different year, ~2500 km) |
| Manavgat ↔ Muğla | 4 | 0.436 | **highest** (same country, same year, ~200 km) |
| Manavgat ↔ Bejís | 4 | 0.384 | low |

**The conditional diagnostic separates the working pair from the failing pairs; similarity does
not — it ranks them in exactly the wrong order.** Bejís and Muğla share the direction of nearly
every predictor despite being the most distant pair; Manavgat disagrees with both of its partners
on elevation and on all four absolute thermal channels. That is a complete mechanistic account of
the proximity result in §3.1, and it is the C4 contribution demonstrated with data already in hand.

**Stated precisely, with its limits.** The agreement count discriminates the transferring pair from
the non-transferring ones; it does **not** discriminate between the two failing pairs, which tie at
4/9 while their transfer scores differ (0.436 versus 0.384). So the claim supported is "direction
agreement separates transfer from non-transfer", not "direction agreement predicts transfer
magnitude". Caveat: three pairs is a small basis.

**Intervals now computed — see `signed_auc_bootstrap.md`.** The "point estimates with no intervals"
caveat that stood here is discharged for the three regions with available parquets. Signed
univariate AUCs were re-derived from the step8a datasets with a ~5 km spatial-block bootstrap (1000
replicates, seed 42), independently reproducing the pipeline's frozen `run_c` CIs to ~0.01. The
reversal picture is now interval-backed and **stronger than at n=2**:

- **Manavgat vs Muğla:** five bootstrap-supported reversals (disjoint 95% CIs), four of them sign
  flips across 0.5 — and critically, all four absolute thermal channels (`current_lst`,
  `current_tvdi`, `downscaled_lst`, `fused_lst`) sign-flip with support. At n=2 these were "point
  reversals, CIs overlap"; Muğla establishes them, sitting at 0.31–0.34 with CIs entirely below 0.5.
- **Bejís vs Muğla:** `current_tvdi` sign-flips with support; three other thermal channels differ
  significantly in magnitude but stay on the same side of 0.5.
- **Manavgat vs Bejís:** only `elevation` — the original n=2 result, unchanged.
- **Static baseline never reverses:** `ndvi_mean` and `slope_mean` stay ≥0.5 in all three regions
  with no bootstrap-supported reversal; `elevation` reverses only in the two Manavgat comparisons
  (Bejís and Muğla agree with each other), so it is a Manavgat-specific dissent, not a general
  reversing feature.

Still outstanding: Evia (parquet in a missing archive part) and the marginal-side
area-of-applicability index, which must be computed before the full marginal-versus-conditional
contrast in the Introduction and Related Work can be claimed.

## 6. Consequences for the manuscript

1. **Core finding 1 strengthens** to a four-region (or three-region) replication, all ΔAUC intervals
   above zero in both populations. Muğla adds the largest increment observed.
2. **Core finding 4 strengthens substantially and can be stated with intervals**, not just as a
   counterexample. Four directions with CIs disjoint from 0.5, splitting by pair rather than by
   similarity.
3. **Core finding 3 needs rework.** "Label-blind adaptation recovers ~27–31 % of the gap" was
   derived from two regions in which adaptation always helped. With Muğla in the set, adaptation
   *hurts* the working pair. The decomposition needs a stated convention for negative recovery, and
   the more defensible headline may be that adaptation compresses all transfers toward chance.
4. **Evia must be resolved before Results are written** — enlarge the AOI and re-run, drop the
   region, or restrict it to within-region replication only.
5. **Re-download archive parts 001, 003, 004, 005** to recover Evia's Step8B/Step8E outputs and gate
   verdict, and to confirm nothing else material is missing.

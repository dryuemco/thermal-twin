# Referee round 3 — consolidated dossier

**Date:** 2026-08-14. **Panel:** three independent readers, each given the manuscript files and the
frozen evidence base, none shown the others' reports. Each read the manuscript first and opened
`REFEREE_ROUND_2.md` only at the end, to mark findings NEW versus RECURRENCE and to audit whether
the round-2 fixes actually landed.

**The editorial lens was deliberately excluded this round.** No finding here concerns length, table
or figure counts, section order, title, abstract word limit, LaTeX compilation, front matter or
house style. Round 2's Tier 3 stands unaltered and undischarged; this round is substance only.

| | Lens | Verdict |
|---|---|---|
| R1 | Statistics and inference | major revision |
| R2 | Remote sensing, fire ecology, data provenance | major revision |
| R3 | Claim–evidence alignment and internal consistency | major revision |

Unanimous, again. No referee proposed rejection. **Nothing in this dossier overturns the negative
result** — several findings strengthen it — and none of the Tier 0 fixes needs a model re-run.

**Application status, 2026-08-14.** The eight ✅ items below have been **applied to the manuscript**
and the LaTeX regenerated (`verify_tex.mjs` 12/12 PASS). Applied: 0.1, 0.7, 0.12, 0.13, 0.14, 1.1,
1.2, the compositing-attribution resolution and the +0.085 → +0.084 half of 3.3. `STATUS.md` was
corrected to stop reporting round 2 as applied in full. **Everything else in this dossier is
outstanding**, including all of Tier 2 and the four heaviest Tier 0 items — 0.2 (the ~10 km blocking
claim), 0.3/0.4 (the surviving "every direction" forms), 0.5 (the Muğla two-event population) and
0.6 (the Manavgat MODIS retraction).

**Verification status.** Items marked ✅ were re-derived from the frozen artefacts in this session,
independently of the referee that filed them; the check is named in place. Eight were checked and
**eight held exactly**, including the one point on which two referees disagreed. Everything unmarked
is the referee's claim as filed, with its source path so it can be checked the same way. Where two
referees reached the same finding independently the entry says so — that is corroboration, not
verification.

---

## The headline of this round

Round 2 was applied at the lines it cited and not swept through the rest of the manuscript, and
three of its own instructions produced new errors. The regression audit below is the most
consequential section of this dossier: **five of the round-2 repairs are now themselves defects.**

One round-2 finding is retracted outright. Round-2 item 2.3 reported that Manavgat's downscaled and
fused LST were built from a four-year summer-mean MODIS layer; the manuscript adopted it in §3.4 and
built §5.11(xiii) on it as the leading candidate explanation for Manavgat's unexplained transfer
behaviour. R2 now shows the string is a stale hardcoded literal and the exporting run's own metadata
says the opposite. The paper currently offers a non-existent difference as its explanation for its
one acknowledged anomaly.

---

## Tier 0 — statements the paper's own evidence contradicts

### 0.1 ✅ "Four of six directions" recover 85–89 %. It is three. **[R1 + R3, independently]**

*Verified.* `recovery_curve.csv` filtered to thermal / roc_auc / 32 blocks returns six rows with
recovery fractions 0.8452, 0.3000, 0.8941, 0.5106, 0.8523, 0.5680 — **three** in the 85–89 % band,
and **two** of those three with raw below 0.5 (0.4435, 0.3258; Muğla→Bejís raw 0.5832). The §4.10
paragraph also refutes itself without any file: it announces four, then lists three, then adds the
51 % and 57 % pair, and gives the 30 % sixth ten lines later.

`00_abstract.md:79`, `01_introduction.md:285-286`, `04_results.md:930-933`, `05_discussion.md:520-522`,
`06_conclusions.md:65-66`, `S1_few_shot_recovery.md:98-101`, `tex/manuscript.tex:68,150,1147,1274,1299`,
`tex/supplementary.tex:56`.

`drive_new/diagnostics/few_shot_recovery/7e4ca051…/recovery_curve.csv` (`model_family=thermal`,
`metric=roc_auc`, `budget_blocks=32`) gives recovery fractions **0.894, 0.852, 0.845, 0.568, 0.511,
0.300**. Three fall in the 85–89 % band. The paper's own Table S1 (`S1:85-90`) prints 89/85/85/57/51/30,
and §4.10 names only three before jumping to the 51/57 pair.

Two further defects ride in the same sentence:
- "from starting points at or below chance" is false for Muğla→Bejís, whose raw is **0.583**
  (`recovery_curve.csv`, `raw_value`; Table S1; Table 4).
- Contribution 6's accounting ("four directions … and only 51 to 57 % in the two where the concept
  gap is widest") sums to six and so deletes the 30 % direction — which is the paper's own
  "small budgets hurt the direction that already works" case.

**Replacement:** "…recovered 85 to 89 % of the target ceiling in three of six directions
(Manavgat→Bejís 89 %, Muğla→Bejís 85 %, Bejís→Manavgat 85 %), 51 to 57 % in two more and 30 % in the
sixth. Two of the three started below chance; the third started at 0.583."

This claim was promoted to the abstract and the Introduction thesis **by round-2 item 3.5**, and it
arrived with the miscount. It now stands in nine places.

### 0.2 The increment has no usable interval at ~10 km, and the paper says so itself two paragraphs apart. **[R1 + R3, independently]**

`04_results.md:70-72` and `:112-114`, propagated to `01_introduction.md:275`, `05_discussion.md:15-16`,
`05_discussion.md:60`, `06_conclusions.md:33`, `figure_captions.tex:89-90`,
`tex/manuscript.tex:642,1160,1291`.

> `04_results.md:70-72` "the increment's bootstrap interval excludes zero at every block size tested"
> `06_conclusions.md:33` "The gain survived spatial blocking at about 10 km."
> `figure_captions.tex:89-90` "its interval excludes zero in **all fifteen** region–block-size combinations"

The table note added **by round-2 item 1.3** (`04_results.md:96-108`) says the opposite about the same
rows: positive-carrying block counts at B = 20 are 12/6/33/15/6, "an equal-tailed percentile interval
built on six positive-carrying blocks has no meaningful coverage", "**the 20-cell row of this table
should be read as indicative rather than as an interval**", and "the 10-cell row … is the coarsest
blocking this design supports properly". Every "~10 km" support claim rests on exactly the row the
note disavows.

**Replacement:** support holds at 1 km and 5 km blocking in all five regions; at 10 km the point
estimates remain +0.048 to +0.154 but the intervals rest on 6 to 33 positive-carrying blocks and are
indicative only. Conclusions: "survived spatial blocking at about 5 km, the coarsest scale this
design supports as an interval." Fig. 3's caption re-scoped to the ten 2- and 10-cell combinations.

### 0.3 "Adaptation only/every direction toward chance" survives in four places. **[R1 + R3; RECURRENCE of round-2 0.1]**

`00_abstract.md:76-77` ("**only** pushed transfer towards chance"), `04_results.md:298-299`
("compresses **all** directions"), `05_discussion.md:517-519` ("moved **every** direction towards
chance"), `figure_captions.tex:147-149`, `tex/manuscript.tex:68,1274`.

Table 4 has five directions the better adaptation moves *away* from 0.5 upward: Montiferru→Manavgat
0.567→0.606, Montiferru→Bejís 0.548→0.574, Montiferru→Evia 0.586→0.630, Manavgat→Montiferru
0.533→0.592, Muğla→Montiferru 0.531→0.587. Inside the twelve decomposed directions the universal
also fails downward: Manavgat→Muğla 0.470→0.443 moves away from chance. §4.3:257-266 and §5.1:29-32
state this correctly; the abstract, §4.3's own summary sentence, §5.10 and Fig. 5's caption carry the
retired form.

`05_discussion.md:518` contradicts itself inside one sentence: "moved every direction towards chance
… and the one family of directions they improved is the smallest region in the set." (The second
clause is also a category error: a family of directions is not a region.)

Fig. 5's caption asserts a pattern its own twelve directions contradict: "directions starting below
chance are pushed up and directions starting above chance are pushed down" — Manavgat→Muğla starts
at 0.470, below chance, and is pushed further down (`04_results.md:296-297` says so).

**Replacement:** "compresses the matrix toward chance in fifteen of twenty directions; the five
exceptions all involve Montiferru, the smallest region."

### 0.4 Introduction C2 says "inside the twelve decomposed directions there is no exception". Table 5 has five. **[R3]**

`01_introduction.md:233-234`, `tex/manuscript.tex:145`. Table 5 shows five of the twelve decomposed
directions with positive recovery. §4.3:261-263 and §5.1:31-32 scope the claim correctly — to *the
six above-chance directions inside the four-AOI subset*. The Introduction dropped the scope when the
round-2 fix was transcribed.

**Replacement:** "…and of the six above-chance directions inside the four-AOI decomposition, all six
are degraded without exception."

### 0.5 The Muğla two-event control does not hold the population fixed, and one arm's source training set excludes the other's entire positive class. **[R1 + R2, independently, by different routes — the most serious finding of this round]**

`04_results.md:758-759` ("Region, bounding box, cell definition, feature registry and processing
chain are the same; **only the event differs**"), `04_results.md:837-874`, `05_discussion.md:115`
("only the fire differs"), `03_methods.md:964-968`, `00_abstract.md:68-70`.

**R2, from the registry.** `repo/core/regions.py:576-582` sets, for `mugla_2022_event_relative`
alone, `exclude_historical_burns: True`, source `mugla_2021`, expected count 3073. Confirmed in
`drive_new/experiments/mugla_2022_event_relative/validation/labels/burned_landcover_gate.json`:
`historical_burn_excluded_count: 3073`, of which `tree_shrub_grass: 2941` — exactly the 41,730 →
38,790 TSG drop printed in Table R8. The 2022 arm's `pre_label_burn_excluded_count` is **0**, so the
safeguard §3.16.4 does name removed nothing and the one that removed 7 % of the primary population
is unmentioned. The removed cells are the 2021 scar: median burned elevation 563 m, maximum 1,975 m
(Table R7), and the headline result is an elevation reversal.

**R1, from the per-cell tables.** `drive_new/experiments/mugla_2021/step8a/…csv`,
`…/mugla_2022_event_relative/step8a/…csv` and
`paper/mugla_transfer_raw/mugla_2021__mugla_2022_event_relative/step9b/cross_region_transfer_predictions.csv`:
the two arms share **38,789 of 38,790** target cells, and `elevation_mean`, `slope_mean` and
`landcover_dominant` are **byte-identical across all 73,098 cells** — only NDVI and the six thermal
channels differ. For the **2022 → 2021** arm, all 2,911 target positives are absent from the source
training population and 38,789 of 38,819 target negatives are present in it: training-set membership
separates the target's classes at **AUC 0.9996**. For 2021 → 2022, all 331 target positives were in
the source training set, labelled 0.

R1 states plainly that it could **not** demonstrate this drives the numbers — the only available
control, the 30 out-of-source negatives, points the other way, and the sign of any bias on the
*paired* delta is not obvious. R2 notes the bias direction on the elevation AUC runs in the paper's
favour: the removed cells are high and unburned in 2022, so removing them *raises* the 2022 elevation
AUC and the reversal is understated, not manufactured.

But the design is not comparable to the twenty between-region directions, where source and target
share no cells, and §4.8 compares them directly ("Transfer between the two events behaves unlike any
between-region direction in the matrix").

**Fix (text; a re-run would be better):** delete "only the event differs" and "only the fire
differs". Name the exclusion with its count and elevation composition in §3.16.4. State in §4.8 and
§5.11(ii) that the two arms share 38,789 of 38,790 cells and three byte-identical static predictors,
that the 2022 population is defined by removing the 2021 scar, and that these two numbers are
therefore not directly comparable to the twenty between-region directions. Add the structural
asymmetry as a competing explanation alongside the elevation reversal.

### 0.6 The Manavgat "four-year summer-mean MODIS layer" is a stale hardcoded string. **[R2 — retracts round-2 item 2.3]**

`03_methods.md:249-256`; `05_discussion.md:598-604` (§5.11(xiii)) makes it the leading candidate
explanation for Manavgat's unexplained transfer behaviour.

The sentence exists verbatim at
`drive_new/experiments/manavgat_2021/step7c/downscaling_model_metadata.json:93`, so the paper reports
the metadata accurately. **The metadata is wrong and the export refutes it.**
`drive_new/experiments/manavgat_2021/data/modis/modis_metadata.json`, written by the same run
(metadata `created_at` 2026-07-09T12:26:16, raster `modified_at` 2026-07-09T12:26:15), records
`predictor_start_date: 2021-06-01`, `predictor_end_date: 2021-07-27`, and `aggregation_window:
"experiment predictor window (single-season mean/std over daily MODIS scenes within the window),
NOT a multi-year baseline"`. The same block is embedded as `frozen_modis_metadata` in
`repo/config/legacy_modis_compatibility_attestation.json`.

The step7c note is provably not evidence about Manavgat: at `48b56e7` it is emitted only when
`ctx.get("is_kozan")` (`repo/src/step7c_train_downscaling_model.py:637-649`), with `is_kozan =
(experiment_id == "kozan_2023")` (`repo/core/experiment_context.py:103`); that conditional was
introduced in commit `7b1c8ac` on 2026-07-10, **the day after** Manavgat's step7c ran (`created_at`
2026-07-09T15:28:31), and at the commit then in force
(`93ffc7c:src/step7c_train_downscaling_model.py:736-741`) the string was an unconditional literal
inherited from the legacy Kozan four-year path (`core/config.py:31-32`, `src/step2_modis_5year_mean.py`).

All five regions used single-season predictor-window MOD11A1 mean/std.

**Fix:** delete the four-year claim from §3.4 and §5.11(xiii). Replace it with the real heterogeneity
(Tier 2.2 below). If a provenance point is wanted, the genuine one is that the frozen export carries
two mutually contradictory descriptions of the same raster, and the `modis_metadata.json` record is
the one written by the exporting run.

### 0.7 ✅ Table R1's `Burned` and `Prevalence` columns are pre-exclusion counts for three of five regions. **[R2]**

*Verified, and the table is internally inconsistent.* Top-level `burned_cell_count` versus
`pre_label_exclusion.final_modeling_counts_after_predictor_validity.burned`: Muğla 3,073 vs **3,026**,
Evia 2,803 vs **2,788**, Montiferru 748 vs **697**. The row's own `Valid cells` column is already the
post-filter number — 3,026 + 70,019 = 73,045; 2,788 + 20,118 = 22,906; 697 + 2,476 = 3,173, each
matching the printed value exactly — so each of these three rows divides a pre-filter numerator by a
post-filter denominator. Montiferru 697 / 3,173 = **0.220**, not the printed 0.236.

`04_results.md:32-34`. Top-level `burned_cell_count` / `burned_rate` in
`drive_new/experiments/<region>/step8a/step8a_dataset_stats.json` are counted over all grid rows
before eligibility and validity filtering. The modelling-population field is
`pre_label_exclusion.final_modeling_counts_after_predictor_validity.burned` = **3,026 (Muğla), 2,788
(Evia), 697 (Montiferru)**, matching a direct count over `step8a_500m_modeling_dataset.csv` and each
region's `validation/labels/burned_landcover_gate.json → burned_count`.

Corrected: Muğla 3,026 / 0.041; Evia 2,788 / 0.122; **Montiferru 697 / 0.220** — the printed 0.236
is wrong by 1.6 points. §4.1's Evia AOI comparison "2,789 → 2,803" is the raw pair; the modelling
pair is 2,774 → 2,788. Manavgat and Bejís have no exclusion and are unaffected. No modelled number
moves. This is the same class of error as the legacy-TSG-field mistake §4.1 already documents, one
column to the left.

### 0.8 The label rule §5.11(xiv) is built on is not the rule the code implements. **[R2]**

`03_methods.md:102` ("a single in-window positive sub-pixel is sufficient to label the cell burned");
`05_discussion.md:605` builds a limitation on it.

`repo/src/step8a_prepare_500m_modeling_dataset.py:1231-1244` takes the **mode** of the positive DOY
values in the block and tests only that modal value against the label window. A block whose positives
are {200, 300, 300} with only 200 in-window is labelled **unburned**. There is no "any positive" rule.
The statement is operationally true for this export only because the label raster is pre-clipped:
`label_raster_diagnostics` in each `step8a_dataset_stats.json` gives `count_positive ==
count_in_label_doy_range` exactly, all five regions.

**Replacement:** "The cell's representative burn date is the modal positive sub-pixel value. Because
the exported raster contains no out-of-window positives, in this dataset any positive sub-pixel makes
the cell burned." §5.11(xiv)'s fringe-contamination argument survives but must be restated against
the mode.

### 0.9 "Historical burning is screened for the Muğla pair" — it is screened for no study region. **[R2]**

`03_methods.md:123`, repeated at `05_discussion.md:616`. `exclude_historical_burns` appears exactly
once in `repo/core/regions.py`, inside `mugla_2022_event_relative` (default `False` at
`repo/core/experiment_context.py:70,156` and `repo/src/historical_burn_exclusion.py:140`). Muğla 2021
is the *source* of that mask, not a beneficiary — its `step8a_dataset_stats.json` has no
`historical_burn_exclusion` key. Muğla 2022 is not one of the five regions of Table 1.

**Replacement:** "Prior-year burning is screened for no region in the five-AOI cohort. The only
historical-burn exclusion in the study removes the 2021 Muğla scar from the 2022 event-relative
experiment of Section 3.16.4."

### 0.10 The analysis cell is not square and is ~17 % smaller in area than a MODIS 500 m cell. **[R2]**

`03_methods.md:75-77` ("square blocks of 17 × 17 pixels … a nominal cell edge of 510 m"), `:333`,
`:941`, `05_discussion.md:556`, and every "≈ 1, 5 and 10 km" block label (`03_methods.md:402`,
`04_results.md:76`).

`drive_new/experiments/<region>/predictor_export_metadata.json` records every raster exported at
`"scale": 30, "crs": "EPSG:4326"`, so the reference pixel is a **degree** step: 30 / 111 319.49 =
0.000269494°, and the cell is 17 × that = 0.00458140° in both axes. On the ground: ≈509 m
north–south, but 0.0045814 × 111 320 × cos(lat) east–west = **407 m** at Manavgat and Muğla, 397 m at
Evia, 391 m at Bejís, 390 m at Montiferru. Area 0.199–0.207 km² against MODIS's 0.25 km².

R2 calls this arithmetically certain rather than inferred: dividing each AOI's span by 0.0045814 and
rounding up reproduces every frozen cell count exactly — Manavgat 175 × 138 = 24,150; Bejís
153 × 103 = 15,759; Muğla 393 × 186 = 73,098; Evia 175 × 131 = 22,925; Montiferru 66 × 49 = 3,234.

**Two consequences to state.** The "≈ 10 km" blocking is ≈10.2 × 7.8–8.1 km, so blocking is
systematically weaker in longitude — in a paper whose central robustness argument is blocking scale.
And because the cell is smaller than and offset from the MODIS cell, each cell overlaps more than one
MODIS cell on average, so the labelled burned footprint is *dilated* relative to MCD64A1, which is
the quantitative form of the §5.11(xiv) worry.

### 0.11 "AOIs fixed before any burned-area label was inspected" is contradicted by the released registry. **[R2]**

`03_methods.md:12`. `repo/core/regions.py:382-387` (Bejís): *"Initial Bejís candidate bbox; refine
after AOI preview and MCD64A1 burned-landcover gate."* Same formula for Muğla (`:435-436`). More
decisively, the canonical Evia AOI is a replacement: `evia_2021` carries `superseded_by:
"evia_2021_extended"` with the comparison recorded in a file the registry names
`docs/evia_2021_prevalence_audit.json` (`regions.py:637`), and §4.1 justifies the swap in terms of
prevalence (0.361 → 0.122).

The extended geometry may well not have been tuned — `regions.py:704-711` asserts exactly that — but
the *decision to supersede* was label-informed.

**Replacement:** "Each AOI is defined from place coverage rather than from a fire perimeter, and is
not tuned on burned prevalence, gate outcome or any model metric. The North Evia AOI was extended
after the legacy box was found to carry an atypically high prevalence; the extended geometry was
defined from place anchors and the legacy variant is retained as a sensitivity (Section 3.16.1)."

### 0.12 ✅ "The thermal block is what carries transfer above chance in both directions" of Bejís–Muğla. **[R3]**

`04_results.md:234-235`, `tex/manuscript.tex:746`. *Verified* in
`paper/baseline_vs_thermal_transfer.csv`: `bejis_2022_to_mugla_2021` **baseline** 0.5922
[0.5749, 0.6088] — above chance with no thermal predictor. Only `mugla_2021_to_bejis_2022` (0.4507 → 0.5832) is lifted across the line. The sentence
also contradicts its own immediate predecessor, which says the block "lifts **one** from below to
above".

### 0.13 ✅ The CORAL λ-sweep spread is 0.014, not 0.008. **[R2; introduced by the round-2 revision]**

*Verified:* grouping `metrics.csv` by direction × family over the nine λ gives a maximum ROC-AUC
spread of **0.01387** overall and **0.00750** within the thermal family; the three widest are all
baseline-family rows.

`03_methods.md:528`, `04_results.md:631`. From
`drive_new/diagnostics/coral_lambda_sensitivity/b74d643e…/metrics.csv`, max−min ROC-AUC over the nine
λ within each direction × family: mugla→bejis baseline **0.01387**, manavgat→mugla baseline 0.01109,
bejis→mugla baseline 0.01008; thermal maximum 0.00750. The export's own `sensitivity_summary.csv`
flags `mugla_2021_to_bejis_2022, baseline, roc_auc, 0.012468, modest_lambda_sensitivity`. §3.11 states
the sweep covered both families, so the bound must cover both.

**Corrected:** "at most 0.014 within any direction, and at most 0.008 within the thermal family."

### 0.14 ✅ The Evia coordinate-importance figure is 0.097, not 0.101. **[R2; introduced by the round-2 revision]**

*Verified:* the six coordinate features sum to **0.097170** (col_norm 0.023258, lon 0.022423, col
0.022305, lat 0.009875, row 0.009717, row_norm 0.009593) in a file totalling 1.000000.

`03_methods.md:242-243`. Summing `lon + lat + row + col + row_norm + col_norm` in
`drive_new/experiments/evia_2021_extended/step7c/feature_importance.csv` gives **0.097170**; the file
sums to 1.000000. The other four values verify exactly (0.122975, 0.121983, 0.066380, 0.034678). The
legacy `evia_2021` run gives 0.1208, also not 0.101, and no permutation-importance record exists in
the export. The error runs in the paper's favour, but it sits in the one paragraph whose purpose is
disclosing a leakage-adjacent pathway.

### 0.15 Line citations do not resolve at the pinned commit, and two point at unrelated code. **[R2]**

`03_methods.md:695-697` names the repository "the authoritative source for the file and line
references cited throughout this section", with Table 1 pinning `48b56e7`.

- Every `step8a:` range in §3.2/§3.5/§3.6 is one line low, and 13 lines low after ~1,150: label
  assignment is `:1217-1261` not `:1204-1248`; the burnable definition is `:1339-1342` not
  `:1326-1329`, which at `48b56e7` is the bare/built-up/water fractions.
- **`step8a:2592 to 2605` is not the pre-label exclusion** in either `48b56e7` or its parent — it is
  metadata date-consistency assertion code. The real sites are `:967-1025`, `:3059-3072`, `:1179-1188`.
- The LST-anomaly formula cited as `step5_preprocess_timeseries.py:837 to 847` is at **`:899-905`**.
- The scale/offset range cited as `core/config.py:89 to 103` excludes the two constants it is cited
  for: `LANDSAT_SCALE` and `LANDSAT_OFFSET` are at **`:86-87`**.
- §3.3's `step6b:172 to 211` is off; the verdict rules are at `:198-219`, rule 4 outside the range.
- `step3_landsat_lst.py:67 to 98` is exact.

Regenerate the rest against `48b56e7`, or §3.13's verifiability claim is not one the paper is
entitled to make.

---

## Tier 1 — statistical claims that must be restated (R1)

**1.1 ✅ The 6:1 exchange rate has a numerator indistinguishable from zero.** *Verified:* the 20
`kind=transfer, config=drop_both` rows give mean **+0.0142**, SD **0.0457**, range −0.058 to +0.102;
the five within-region `drop_both` deltas are −0.060, −0.130, −0.073, −0.063, −0.079 (mean −0.081).
`00_abstract.md:65-66`,
`01_introduction.md:70` ("an exchange of about six to one"), `:223`, `04_results.md:567-568`,
`05_discussion.md:344`, `06_conclusions.md:42-44` ("which is the exchange rate of the trade-off"),
`tex/manuscript.tex:94,142,150`.

§4.3:206-219 argues at length that a mean over 20 non-independent directions is meaningless without a
cluster-aware interval. The same round then promoted a *second* such mean — the feature-removal
transfer gain — to the abstract, the Introduction thesis and the Conclusions with no interval
anywhere. R1 recomputed from `paper/feature_drop_transfer.csv` (`kind=transfer`, `config=drop_both`,
`delta_vs_full`): mean **+0.0142**, SD 0.0457, range −0.058 to +0.102; collapsed to the ten unordered
pairs, t interval **[−0.017, +0.045]** — spans zero. Per direction: 5 CI-supported positive, 3
CI-supported negative, 12 uncertain. The within-region cost is by contrast solid: all five per-region
`drop_both` within deltas have intervals entirely below zero (−0.060, −0.130, −0.074, −0.063, −0.079;
mean −0.081).

**Replacement:** "Removing the two reversing predictors costs −0.081 of mean within-region AUC,
bootstrap-supported in every region, and changes mean transfer AUC by +0.014, an estimate whose
pair-clustered interval [−0.017, +0.045] spans zero. The debit is measured; the credit is not, so no
exchange rate is claimed." **Note:** round-2 editorial item 3.4 asked for the trade-off to be
re-anchored on this exchange. On the frozen numbers that anchor does not hold; the honest re-anchor
is the sign instability, not the exchange.

**1.2 ✅ Round-2 item 1.8 was not applied, and the missing number nearly halves the headline range.**
*Verified* against both `step8c_bootstrap_metrics.json` files, `burnable_tree_shrub_grass`,
`bootstrap_unit: spatial_block_id`: legacy `delta_auc` **0.084809** [0.072147, 0.100226] against
extended **0.153285**. `04_results.md:584-590`, `00_abstract.md:60`, `06_conclusions.md:30`, Table 3.

| Evia AOI | baseline | thermal | ΔAUC [95 % CI] | source |
|---|---|---|---|---|
| extended (canonical) | 0.7590 | 0.9122 | **+0.1533 [+0.1422, +0.1658]** | `drive_new/experiments/evia_2021_extended/step8c/step8c_bootstrap_metrics.json` |
| legacy | 0.8136 | 0.8984 | **+0.0848 [+0.0721, +0.1002]** | `drive_new/experiments/evia_2021/step8c/step8c_bootstrap_metrics.json` |

Same fire, same windows, different AOI extent; the increment falls by 45 %. §4.7a's "leaves every
qualitative conclusion unchanged" is scoped to the transfer arms and is fine as written, but the
headline within-region range is AOI-choice-dependent at its upper end and nowhere says so. Both
intervals exclude zero, so the qualitative claim survives; the *magnitude* claim does not travel.
Arithmetic only. `STATUS.md:44` should stop reporting the round-2 dossier as applied in full.

**1.3 The single positive diagnostic's lower bound is decided by a discard convention and the seed.**
`04_results.md:318`, `:354-356`, `00_abstract.md:73-74`, `05_discussion.md:259-260`,
`03_methods.md:735-737`.

`paper/conditional_similarity_transfer.json`, `agree_fraction_supported`: `n_valid_replicates = 1956`,
`n_degenerate_replicates = 44` of 2000. The index takes value 1 on 5 of the 8 pairs, so an all-tied
resample has probability (5/8)⁸ = **2.33 %** — 46.6 expected, 44 observed. The dropped replicates are
precisely those in which the diagnostic carries **no** ordering information, so discarding them
conditions the interval on informativeness. R1 reimplemented the pair bootstrap and reproduced the
published interval exactly at seed 42 ([0.5765, 0.8764] against the stored [0.57649, 0.87636]), then
assigned degenerate replicates ρ = 0 instead:

| seed | degenerate | published rule (drop) | degenerate → 0 |
|---|---|---|---|
| 42 | 49 | [0.5765, 0.8764] | [0.5756, 0.8764] |
| 1 | 52 | [0.5765, 0.8755] | **[0.0000, 0.8755]** |
| 7 | 41 | [0.5765, 0.8764] | [0.5756, 0.8764] |
| 123 | 41 | [0.5765, 0.8757] | [0.5756, 0.8755] |
| 2024 | 52 | [0.5765, 0.8757] | **[0.0000, 0.8757]** |

The flip occurs when the degenerate count exceeds 2.5 % of replicates, probability ≈ 0.3 under this
tie structure. §3.9:425-426 and §3.14.1:736 disclose the discard rule but nowhere say it is decisive
for this row. **Fix:** one sentence in §4.4's "how strong is it" paragraph. The companion
`cosine_supported` row is unaffected (3 degenerate of 2000), so the "exactly two of twenty" headline
survives; only the abstract's naming of the agreement fraction as "the stronger" needs the caveat.

**1.4 "ρ = 0.84 over eight pairs" mislabels the estimator.** `00_abstract.md:73-74`,
`tex/manuscript.tex:68`. Per `referee2_numbers.md` block B, 0.8404 is the **16-direction** Spearman;
the **8-pair** value is 0.8660. Write "over sixteen directions from eight pairs", or quote 0.87.

**1.5 §4.6b attributes drop-*elevation* deltas to the drop-*both* configuration.**
`04_results.md:567-577`. "Dropping both reversal features buys +0.014…" is followed by the three
CI-supported gains (Manavgat→Bejís +0.118, Evia→Bejís +0.075, Montiferru→Manavgat +0.057) and the
five CI-supported losses. `feature_drop_transfer.md:41-46` labels both lists **`drop_elev`**.

**1.6 Round-2 item 1.4 was only half-applied.** §4.7g ranges and §5.11(x) are in and good; no
sentence in §3.9 or §3.14.1 acknowledges that the 12/6/2, 9/4/7, 10/7/3 and 6/4/10 tallies apply the
same 95 % rule 40 times and then count outcomes, and §4.3:150-152 and §5.1:26-27 still quote exact
counts. One sentence in §3.9 closes it.

**1.7 Smaller statistical items.**
- **"No bootstrap replicate was invalid at any block size" is false.** `04_results.md:101`.
  `drive_new/robustness/step8_large_block/manavgat_2021__bejis_2022/bejis_2022/block_20_cells/step8c_large_block_bootstrap_summary.csv`
  records `valid_replicates = 995`, `invalid_single_class_replicates = 5`. Every other region/block
  is 1000/0. Saying so strengthens the note's own point.
- **Round-2 item 1.5 (percentile vs BCa; ratio with estimated denominator) is unaddressed.**
  `03_methods.md:424-425` unchanged; Table 5's Evia→Manavgat −0.86 [−1.18, −0.60] on a denominator of
  0.184 carries no distributional caveat. In mitigation,
  `four_aoi_decomposition_bootstrap_summary.csv` records `n_replicates_ratio_degenerate = 0` for all
  rows — worth stating.
- **"Best adapted" in Table 5 is a max over two correlated estimators taken outside the bootstrap**
  (`04_results.md:268-289`, `03_methods.md:568-572`). Disclosed as a design choice, not as a source of
  upward bias in the recovered fraction. The bias runs in the paper's favour, so one sentence suffices.
- **Table R11 compares bootstrapped PR-AUC intervals to a fixed prevalence** (`04_results.md:186-196`).
  Under block resampling the no-skill line varies too; the paired quantity would be the right
  interval. The three verdicts (11/5/4) are exactly right against a fixed line.
- **§4.7e overstates the interval's coverage of implementation noise.** `04_results.md:642-643`: the
  measured shifts are +0.021 and +0.026 while several Table 4 intervals are only 0.030–0.037 wide, and
  the transfer bootstrap resamples target blocks only. Say "comparable to, not covered by".
- **Table 5's Evia→Muğla recovered fraction prints −0.17 where the frozen ratio is −0.164**
  (`04_results.md:287` against `four_aoi_decomposition_bootstrap_summary.csv`, −0.046312/0.282552).
  The other eleven rows match to the printed digit; this one appears recomputed from rounded cells.

---

## Tier 2 — the observational layer, second pass (R2)

**2.1 Sea water is inside the AOIs, inside the LST composites, and inside the TVDI edges — the
strongest available competing explanation for the TVDI reversals.** §3.4 states at
`03_methods.md:173` that the water bit is deliberately preserved (verified at
`repo/src/step3_landsat_lst.py:73-97`) and draws no consequence.

Water-dominant cells as a share of the AOI, from `validation/labels/burned_landcover_gate.json`:
**Evia 13,210 / 22,925 = 57.6 %**, **Muğla 28,412 / 73,098 = 38.9 %**, Manavgat 2,002 / 24,150 = 8.3 %,
Montiferru 236 = 7.3 %, **Bejís 21 = 0.13 %**. These cells pass `valid_for_modeling` (elevation, slope
and NDVI are finite over sea; class 80 is a valid land-cover pixel).

*First consequence:* the secondary `all_valid` population is **58 % seawater in Evia and 39 % in
Muğla**. §4.7f attributes its higher baseline AUC (0.827–0.910) to "land-cover composition
contributing separable but non-thermal discrimination"; the honest version is that most of the extra
separability in two regions is land versus sea.

*Second and more serious:* `repo/src/step5c_tvdi.py` fits wet and dry edges as 2nd/98th LST
percentiles within each NDVI bin over the whole scene, and sea occupies the lowest bins.
`drive_new/experiments/<region>/step5c/tvdi_edge_diagnostics.csv`:

| Region (water share) | bin 0 dry edge | bin 1 | bin 2 | bins 2–4 span |
|---|---|---|---|---|
| Evia ext. (57.6 %) | 29.9 °C | 28.8 | 29.7 | 4.3–20.7 °C |
| Muğla (38.9 %) | 33.1 | 41.9 | 45.6 | 23.3–26.7 |
| Manavgat (8.3 %) | 34.5 | 44.2 | 46.7 | 21.6–23.5 |
| Montiferru (7.3 %) | 31.1 | 32.4 | 33.6 | 12.7–26.4 |
| **Bejís (0.13 %)** | **49.0** | **48.8** | **49.1** | **15.2–20.9** |

Bejís, the only inland AOI, has a genuine bare-soil dry edge near 49 °C in the low-NDVI bins. Evia's
is 29–30 °C with a 2nd-to-98th span of 3.95 °C — Aegean sea-surface temperature, not a land dry edge.
A dry, sparsely vegetated *land* pixel in Evia or Muğla is normalised against a seawater dry edge and
saturates at the [0,1] clamp; the same pixel in Bejís is not. TVDI's normalisation is not merely
"scene-fitted" as §3.4 and §5.2 say — it is **a function of each AOI's sea fraction, which ranges from
0.1 % to 58 %**. And §4.7h identifies the TVDI pair as the best subgroup in three of five regions.

**Re-run asked for:** mask the water bit (or restrict the edge fit to land-cover classes
10/20/30/40/60), refit the edges, recompute the TVDI channels' signed univariate AUCs. Same order of
effort as the common-edge TVDI already promised in §5.11, and a sharper test.

**2.2 The real MODIS heterogeneity is a 3-versus-2 split in QC screening and nodata encoding**
(replaces the retracted round-2 2.3 framing). Per
`drive_new/experiments/<region>/data/modis/modis_metadata.json`, cross-checked against
`step7b/downscaling_dataset_stats.json → alignment_diagnostics`:

| region | export date | `QC_Day` applied | min valid obs | nodata sentinel | `source_nodata` / valid px |
|---|---|---|---|---|---|
| Manavgat 2021 | 2026-07-09 | **no** | — | **none** | `null`, 6390/6390 |
| Bejís 2022 | 2026-07-10 | **no** | — | **none** | `null`, 4187/4187 |
| Muğla 2021 | 2026-07-20 | **no** | — | **none** | `null`, 19190/19190 |
| Evia ext. 2021 | 2026-07-28 | yes | 3 | −9999.0 | `-9999`, 2614/6120 |
| Montiferru 2021 | 2026-08-05 | yes | 3 | −9999.0 | `-9999`, 797/875 |

QC_Day masking (`repo/scripts/prepare_modis_for_step7.py:182-183`, rule at
`repo/core/config.py:390-404`; `STEP7_MODIS_MIN_VALID_OBSERVATIONS = 3` at `:413`) was added in commit
`4745230` on 2026-07-23, **after** three of the five regions had been exported. The legacy path
applies no QC at all. So `downscaled_lst` and `fused_lst` — which carry 68–86 % of the thermal
increment (2.3 below) — rest on quality-screened MODIS in two regions and unscreened MODIS in three,
with the cohort split **by export date rather than by design**.

The zero-fill defect is **not Manavgat-only**: all three unscreened regions declare `source_nodata:
null` with 100 % of pixels valid, so no-observation and sea cells are encoded as exact 0.0 °C in
Manavgat, Bejís and Muğla alike. Only Manavgat is quantified —
`repo/config/legacy_modis_compatibility_attestation.json` gives `exact_zero_count: 518 / 6390 = 8.1 %`,
`default_guard_would_reject: true` against `STEP7B_MODIS_SUSPICIOUS_ZERO_FRACTION = 0.05`. The Bejís
and Muğla zero fractions are a two-line query and should be reported. (R2 could not read those two
GeoTIFFs — no Python on this machine — so their zero-fill claim rests on the `source_nodata: null` /
100 %-valid signature rather than a measured count.)

One phrasing correction: §3.4 attributes the warning to "the same Manavgat run". It was not written by
that run — the canonical step7b output records the symptom silently (`warnings: []`,
`modis_source_validation_recorded: false`); the explicit warning came from a separate diagnostic on
2026-07-26 (`src.landsat_composite_downstream_ab.build_legacy_modis_attestation_declaration`).

**2.3 The two coordinate-bearing channels recover 68–86 % of the thermal increment, and Table R14
does not report it** (RECURRENCE — the unmet half of round-2 2.6). Round 2 asked explicitly to "show
the increment without those two channels (Step 8D has the pieces)". Table R14 reports only the best
subgroup, which is the TVDI pair in three of five regions — the physically reassuring answer. From
`drive_new/experiments/<region>/step8d/step8d_ablation_delta_auc_by_population.csv`, primary
population:

| Region | full block | `downscaled_only` | share | `fused_downscaled_group` | share |
|---|---|---|---|---|---|
| Manavgat | 0.0669 | 0.0585 | 87 % | 0.0575 | 86 % |
| Bejís | 0.0561 | 0.0398 | 71 % | 0.0401 | 71 % |
| Muğla | 0.1157 | 0.0749 | 65 % | 0.0823 | 71 % |
| Evia ext. | 0.1533 | 0.1014 | 66 % | 0.1045 | 68 % |
| Montiferru | 0.1014 | 0.0744 | 73 % | 0.0714 | 70 % |

Every printed value in Table R14 verifies exactly against these CSVs. The reader needs to see that the
single fitted RF surface carrying a 3.5–12.3 % coordinate share accounts for two thirds to seven
eighths of the increment. It overturns nothing — the downscaler never sees a fire label — but §3.13's
leakage paragraph is emphatic about coordinates, and this is the number that prices the caveat.

**2.4 The ERA5 window maxima were computed, are in the frozen file, and are not reported** — in the
section whose purpose is testing extremity. §3.17 (`03_methods.md:1053-1056`) says the diagnostic
produces window mean *and maximum*; Table R10 reports means only. From
`paper/era5_raw/4850c165…/era5_land_regional_summary.json`: Manavgat T 34.71 °C (**+0.38**), wind
3.76 m s⁻¹ (**−0.52**, most negative in the set); Bejís 36.12 (+0.83), 6.56 (+1.09); Muğla 35.87
(+0.37), 6.60 (+0.63); Evia **38.55 (+3.12)**, 5.42 (−0.93); Montiferru 36.47 (+1.12), 6.37 (−0.12).
The maxima **strengthen** §5.7 and change the ranking elsewhere. Reporting only means in the section
that tests extremity is selective, and costlessly so.

**2.5 TVDI is not the Sandholt construction, and the densest-vegetation bins receive no TVDI at all.**
`repo/src/step5c_tvdi.py:245-246` takes per-bin percentiles directly; no `polyfit`, `linregress` or
least-squares call exists in the file, so no dry-edge line is fitted across bins. The paper describes
the code accurately, but a reader who knows Sandholt et al. (2002) will assume a fitted edge — say so
in a clause. Bins with fewer than 30 pixels are left NaN with no interpolation (`:239-242`) and their
pixels become no-data (`:398-402`): bins 18–19 (**NDVI ≥ 0.9**) are `insufficient_pixels` in both
Manavgat and Bejís, so the dryness index is undefined over the densest canopy in at least two regions.
Third, the edges are fitted on the **current-window** scatter only (`main()` at `:662`) and applied to
every baseline year, while the baseline LST raster is a single window-invariant mean (`:480-486`,
`:528-530`). §3.4 states the second half of this; state the first half too.

**2.6 The land-cover epoch is contemporaneous with the fire in four of five regions, and the paper
flags only the harmless case.** `03_methods.md:270-271` singles out Bejís, where the 2021 map precedes
the 2022 fire. But `ESA/WorldCover/v200` (`repo/src/step4_export_geotiff.py:724`) is the **2021**
annual product built from full-calendar-year 2021 Sentinel-1/2 data — so for Manavgat, Muğla, Evia and
Montiferru the map is derived partly from post-fire observations of the fires being predicted. This is
the risky direction, unflagged, in a variable that is a baseline predictor, the definition of the
primary population, and the gate's admissibility criterion. Burned natural-vegetation fractions remain
0.723–0.991, so the effect is likely modest, but a burnt stand reclassified from tree cover to
grassland or bare/sparse would put label information into `landcover_dominant`.

**2.7 The downscaling validation is reported without the two caveats its own files carry**
(RECURRENCE, round-2 2.7 incomplete). The five RMSE/R² pairs at `03_methods.md:239-241` verify exactly
against `step7c/downscaling_model_metrics.json`. Omitted: **all five carry a pipeline-generated
overfitting warning** (Manavgat: "Train RMSE is much lower than test RMSE (train=0.606, test=2.038)"),
and the "MODIS-baseline control" the paper invokes is weak — baseline R² is **−1.332 (Manavgat),
−0.262 (Bejís), −2.791 (Muğla)**, +0.050 (Evia), +0.570 (Montiferru), with MODIS biases of −5.26 °C
and −11.41 °C. Most of the headline RMSE improvement is offset removal, not added spatial detail.

**2.8 MCD64A1's own quality layers are never read, and no second label product is used**
(RECURRENCE, round-2 2.9 partly unmet). `repo/core/validation_burned_area.py:63-68`, `:192-202` and
`repo/src/step6_validate_fire_relation.py:705-750` select `BurnDate` only; the `QA` and `Uncertainty`
bands are not selected anywhere in `repo/`. The consequence is visible in the frozen gate: **10 burned
cells in Manavgat, 75 in Muğla and 74 in Evia are `permanent_water`-dominant** — commission over water
the product's own QA would have flagged. `FIRECCI51_COLLECTION` is configured
(`core/config.py:212`) and never used.

**2.9 The label window is 35 to 59 days long and varies by 1.7× across regions**, so a "region" is a
window, not a fire. From `repo/core/regions.py`: Manavgat 35 d, Montiferru 39 d, Bejís 47 d, Muğla
49 d, Evia 59 d; predictor windows 57–61 d. A 59-day label window admits ignitions up to two months
after the predictor window closes, whose pre-fire state is not what the predictors describe. Muğla's
Table R7 shows the consequence — a ten-component "event" that is a season of separate fires — but the
paper treats this as a Muğla property rather than a cohort-wide design parameter.

**2.10 Copernicus GLO-30 is a digital *surface* model, and slope is the variable that suffers.**
`03_methods.md:259` calls it a "30 m global digital surface model" once, in passing. Over closed canopy
a DSM's elevation carries canopy height (harmless to a tree ensemble) but its **slope** carries canopy
roughness — and `slope` is the dominant downscaler input in Muğla at importance 0.777.
`grep -rni "geoid|egm2008|ellipsoid|DSM|canopy"` over `repo/**/*.py` returns zero hits, so no
vertical-datum handling exists. Table 2 labels `elevation_mean` "m a.s.l."; nothing in the code
establishes an orthometric datum. Either substantiate it or write "elevation (m)", and add one
limitation sentence on DSM slope over forest.

**2.11 The Landsat composites use a predictor window one day shorter than Table 1 declares.**
`drive_new/diagnostics/landsat_current_support_harmonization/manavgat_2021/daily/daily_inventory.json`
records `"end_semantics": "exclusive"`, `"effective_last_included_date": "2021-07-26"`,
`"window_days": 56`; `predictor_export_metadata.json` independently gives `current_period_days: 56`
(from `repo/core/config.py:334`, a `timedelta.days` difference). §3.4's "57-day window" and Table R10's
`Window (days)` column use the inclusive count, which is what the ERA5 arm computes. No scene is lost
for Manavgat, but the two arms describe different windows, and §3.1's "It ends the day before the label
window opens" holds only for the meteorological arm.

**2.12 Two small Step 5 corrections.** `STEP5_MIN_CURRENT_VALID_COUNT = 2` is applied per **30 m
pixel** (`repo/src/step5_preprocess_timeseries.py:883`), not per cell — the cell-level rule is the
separate `STEP8A_MIN_30M_VALID_FRACTION = 0.3` — so `03_methods.md:180-181` should read "a pixel's
median". And `step5:875-880` contains a live fallback that silently sets the valid-count to the
threshold itself when the current-period raster lacks its count band; the band is present in all five
frozen runs, so nothing is affected, but the path exists.

**2.13 Smaller provenance items.**
- **The 9.70 % gap-fill figure is a 30 m raster statistic attached to a 500 m claim.**
  `step7e/fused_lst_stats.json → gapfilled_pct_of_fused` gives 9.7002 % for Bejís; the 500 m
  modelling-cell mean (`step8a_dataset_stats.json → gapfilled_fraction_summary.mean`) is 9.66 %.
- **QA_RADSAT** (RECURRENCE, round-2 2.2): `repo/core/source_scene_provenance_config.py:32-53` states
  the rule as "QA_PIXEL … + QA_RADSAT"; `step3_landsat_lst.py:67-98` applies QA_PIXEL only, and
  `repo/src/landsat_composite_counterfactual_audit.py:365-369` records the discrepancy verbatim. The
  corrected wording reached only the Manavgat diagnostic; the frozen Muğla and Montiferru
  `qa/source_scene_provenance/v1/provenance_summary.json` still carry the wrong claim.
- **`downstream_authorized: False` is absent from three frozen gate outputs.** `03_methods.md:147` says
  it "always" carries the field; true of the code at `48b56e7`, false of the Manavgat, Bejís and Kozan
  artefacts, which predate it.
- **`landcover` enters the Step 7C regressor as a raw integer class code**, not one-hot
  (`repo/src/step7c_train_downscaling_model.py:96-109`) — an ordinal encoding of a nominal variable
  inside the model that produces two of the six thermal channels.
- **The Kozan control validates the gate, not the study.** One sentence acknowledging that a stronger
  negative control would fit the thermal model on Kozan and show the increment is an
  agricultural-calendar artefact there.
- **`StratifiedGroupKFold` silently retries at `n_splits=3`** if fewer than two folds carry a positive
  (`step8b:400-407`). `n_splits_used` is 5 in every frozen run; disclose the ladder and report the field.
- **`WITHIN_REGION_REPRODUCTION_TOLERANCE` is reported, not enforced.** Only
  `RAW_REPRODUCTION_TOLERANCE` is behind a `raise` (`step10c:373`); the within-region check returns its
  verdict and the caller never branches on it, failing soft to `{"checked": False}` if the metrics file
  is missing (`:170-198`). The achieved difference is exactly zero, so nothing is at stake, but §3.13
  overstates the mechanism.
- **The two Evia AOIs are nested**, so §3.16.1's sensitivity compares a box with its own superset and
  the added area is entirely unburned context.
- **A stale docstring at `repo/src/step3_landsat_lst.py:103`** says "Landsat 8/9 C2L2" while the code
  reads `LANDSAT_COLLECTION` only.
- **Missing remote-sensing literature is still missing** (RECURRENCE, round-2 2.10, half applied). The
  blocked-CV trio **was** added and is cited at `02_related_work.md:177-179` with all three in the bib.
  None of the remote-sensing references was: burned-area validation beyond Boschetti (Padilla 2015;
  Roteta 2019; Franquesa 2020/2022), the Ts–VI feature-space limitation literature for TVDI
  (Petropoulos 2009; Long 2012), LST validation (Wan 2014; Ermida 2020), Jain et al. 2020.

---

## Tier 3 — over-claims, inconsistencies and broken references (R3)

**3.1 Over-claims to restate.**
- `05_discussion.md:61-62` "It also **strengthens rather than weakens** when the predictor window is
  closed earlier." Table R5: Evia falls monotonically 0.156 → 0.149 → 0.135; Montiferru is 0.096 →
  0.091 → 0.100. §4.7c claims only "Nowhere does the increment shrink toward zero; in Manavgat and
  Bejís it increases." Restate to §4.7c's wording.
- "the one direction that already works" (`04_results.md:941`, `05_discussion.md:524`,
  `S1:27-29`). **Two** of the six few-shot directions transfer above chance raw (Bejís→Muğla 0.618,
  Muğla→Bejís 0.583; both CI-supported at both blockings, `transfer_ci_blocksize.md:126-127`).
  Restate as "the direction that transfers best raw".
- `highlights.md:10` "…**target labels repair it**." §4.10 / S1: 30 % in one direction, 51–57 % in two,
  negative at 1, 2, 4 and 8 blocks in the direction that already works. Restate as "32 labelled 5 km
  blocks recover 30–89 % of the target ceiling".
- `00_abstract.md:54` "Pre-fire thermal dryness **separates a fire year from a normal year**." No
  analysis in this paper compares a fire year with a normal year; the design is burned-versus-unburned
  cells inside one pre-fire window per region, and the two Muğla events show the associations
  *reversing*. Attribute to the cited literature or restate as "discriminates burned from unburned
  ground".
- `05_discussion.md:217-224` "the **highest weighted value in the matrix**", "**lowest value in the
  matrix**". The applicability audit covers 12 of 20 directions; §4.4:456-459 and §5.3:228-229 both say
  Montiferru carries no applicability number in any direction. Restate as "of the twelve directions the
  audit covers".
- `05_discussion.md:345-346` "**All three** interval-supported gains involve the reversal partners."
  §4.6b:570-572 names Manavgat→Bejís, Evia→Bejís, Montiferru→Manavgat; the CI-supported reversals are
  elevation Manavgat↔Bejís and Manavgat↔Muğla and `lst_anomaly` Bejís↔Evia
  (`conditional_similarity_transfer.md:49-51`). Montiferru–Manavgat is not one. §4.6b's own
  "Manavgat-involved" framing is defensible; §5.5's is not.
- `05_discussion.md:270-271` "leaves **six of eight** pairs with denominators of one or two features,
  and **the two Montiferru pairs** drop out entirely". `conditional_similarity_transfer.md:39-48`:
  denominators are 1, 2, 1, 1, 1, 5, 2, 1 → **seven** of eight; Montiferru has **four** pairs, two of
  them *inside* the 8-pair sample. The source report carries the same two slips.
- `04_results.md:645-649` "with smaller deltas … **for the three high-increment regions**". All five
  all-valid deltas are smaller than their TSG counterparts (0.059<0.067; 0.048<0.056; 0.072<0.116;
  0.053<0.153; 0.075<0.101). The restriction to three understates the paper's own result.
- `04_results.md:291-292` "In the **five** directions where raw transfer was below chance" — Table 5 has
  **six** (0.326, 0.444, 0.401, 0.383, 0.448 and 0.470), and four sentences later the same paragraph
  says so. Write "in five of the six".
- `figure_captions.tex:221-225` states both contrast-pair verdicts flat, with no "at the point
  estimate" qualifier and no note that neither Bejís–Montiferru direction carries a verdict at 5 km.
  The 2026-08-13 blocking-scale pass forced that qualifier into §4.5, Table R2, §5.3 and §6 but never
  swept the captions. RECURRENCE.

**3.2 The generated LaTeX truncated the only footnote in the paper and promoted its remainder into the
body, inverting a referent.** `02_related_work.md:326,332-337` → `tex/manuscript.tex:218,220`. The
`\footnote{}` captures only the first physical line and ends mid-clause at "…inconsistent with their
own". The remaining five lines became a free-standing Related Work paragraph beginning "Methods, where
no land surface temperature or TVDI variable appears…", which now reads as a statement about *this
paper's* Methods rather than Dimarco's. `tex/build_report.md` records the symptom ("definition
[^dimarco-lst] captured (82 chars)") without diagnosing it; `verify_tex.mjs` compares an unordered bag
of numeric tokens and cannot see it. **Everything else in the port is faithful:** 20 tables, 157 rows,
all numbers, all hedges (18/18 "at the point estimate", 46/46 "point estimate") matched exactly.

**3.3 Other inconsistencies and broken references.**
- `tex/supplementary.tex:71` emits `Table~\ref{tab:3}`, defined in `manuscript.tex` — a separate
  document, so S1 limit 5's pointer compiles to "Table ??". `verify_tex.mjs` never opens
  `supplementary.tex`.
- `04_results.md:262` cites "Section 4.3a". No such section exists. The only unresolvable §-pointer in
  the manuscript — all other 78 resolve.
- `05_discussion.md:202` cites §3.14.4 for a statement about niche overlap and regime structure, which
  are §3.14.3 and §3.14.5 (§4.4:360 cites them correctly).
- `figure_captions.tex:64` and `figures/fig2_schematic.py:190` print "spatial-block bootstrap (§3.13)".
  The bootstrap is §3.9. `fig2_provenance.json` lists 3.9 among the verified references, so the
  build-time assertion did not catch the mis-assignment.
- `04_results.md:834-835` calls `ndvi_mean` and `slope_mean` "the two remaining **static** predictors"
  while five other passages insist `ndvi_mean` is the baseline's one time-varying member. Use "baseline".
- `02_related_work.md:417` "**Five** contributions follow" against six in `01_introduction.md:205-296`;
  Contribution 6 was added in round 2 with no counterpart in Related work.
- `S1:142-143` limit 5: ceilings "0.777 to 0.824 against **0.87 to 0.94**". The three regions' 2-cell
  within-region thermal AUCs are 0.870, 0.918, 0.859 → 0.86 to 0.92. The 0.94 is Muğla **2022**'s value.
- `05_discussion.md:457-458` and `:584` give the date-balanced compositing increment as **+0.085**;
  `04_results.md:734` gives **+0.084**. Frozen: 0.0844551. (R2 flags the same pair.)
- `04_results.md:313-315` Table 6 caption: "the 16 directions (8 pairs) with at least one CI-supported
  feature". The criterion is *jointly* supported — interval excluding 0.5 in **both** regions. As
  written it would admit Bejís–Montiferru, the pair §4.5 and §5.4 make a point of excluding.
- `04_results.md:304` "Twenty candidate diagnostics … were each rank-correlated" against `:344-347`,
  "twenty were specified and **nineteen** were computed". The same sentence pair repeats
  "rank-correlated with the same target quantity" twice in three sentences — residue of the round-2
  0.10 verb repair.
- `04_results.md:229-230` "It is the swing factor at the chance line." Nearest antecedent is "the sign
  instability"; the subject is the block (`01_introduction.md:221`, `05_discussion.md:53`).
- `00_abstract.md:69-70` "Season and year are confounded there, **so** place is what the design holds
  fixed." Non-sequitur: place is fixed by construction and the confound survives *despite* that.
  §3.16.4 and §4.8:760-762 state it in the correct order.
- `S1:106-108` "These are the directions whose raw transfer sits **furthest below the ceiling**."
  Table S1 gaps: Manavgat→Bejís 0.498 (largest, recovers 89 %), Muğla→Manavgat 0.396, Bejís→Manavgat
  0.353, Manavgat→Muğla 0.307. The stated explanation is false as measured, and the subject "The two
  directions into Muğla and Manavgat from Muğla" is unparseable.
- `02_related_work.md:322` "Their predictor set comprises NDVI, and slope derived from the ASTER GDEM."
  A list member appears to have been deleted; the sentence misdescribes a competing paper's predictor
  set. RECURRENCE — round-2 0.10 flagged this location. Carried verbatim into `tex/manuscript.tex:218`.
- `03_methods.md:807-809` enumeration mismatch: "computed in two ways. **The first** is … and **(b)**
  on a 20 × 20 histogram…", with the second item left without a governing verb.

---

## The round-2 regression audit

Five round-2 repairs are now themselves defects. This is the section to read first.

| Round-2 item | What it produced | New defect |
|---|---|---|
| **3.5** promote the few-shot curve | §4.10, abstract, Introduction C6 | The "four of six / at or below chance" miscount, now in nine places (**0.1**) |
| **1.3** block-count note on Table 3 | `04_results.md:96-108` | The note disowns the intervals §4.2, §1.5, §5.1, §5.2, §6 and Fig. 3 still rely on (**0.2**); and it asserts a false "no invalid replicate" claim (**1.7**) |
| **0.1** re-scope the adaptation claim | §4.3, §5.1, Fig. 5 scope line | Not swept to the abstract, §4.3's own summary, §5.10 or Fig. 5's body (**0.3**); garbled in Introduction C2 (**0.4**) |
| **2.3** Manavgat MODIS contract | §3.4, §5.11(xiii) | The source is a stale literal; the paper now explains its one anomaly with a non-existent difference (**0.6**) |
| **3.4** re-anchor the trade-off on the exchange | abstract, C1, Conclusions | The numerator's pair-clustered interval spans zero, so no exchange rate is supported (**1.1**) |
| **2.1** compositing A/B | §4.7i, §5.11(xi) | +0.084 / +0.085 inconsistency (**3.3**); and a disputed reference-chain attribution (see disagreements) |
| **3.11 / 3.13** λ-sweep and coordinate figures | §3.11, §3.4 | Two new wrong numbers: λ spread 0.008 (**0.13**), Evia coordinates 0.101 (**0.14**) |

**Two round-2 items were never applied at all:** 1.5 (BCa / ratio denominators) and **1.8 (Evia
legacy-AOI within-region increment)**. The second is the one whose omission changes a headline number.
`STATUS.md:44-46` reports the dossier as applied in full except length and tables; that is not
accurate.

## Status of round-2 items

**Tier 0 (R3's audit).** 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8 — **fixed and verified**. 0.1 — **partial**
(see 0.3, 0.4 above). 0.9 — **partial**, survives at `02_related_work.md:422` ("the block gaining the
most locally"), where §2.5's own consistency note claims it was fixed. 0.10 — **mostly fixed**; two
sub-items survive (`02:322` ASTER GDEM, `03:807-809` enumeration). 0.11 — house style, out of scope
this round.

**Tier 1 (R1's audit).** 1.1 **applied, and better than asked** (four resampling units; R1 reproduced
all four, and notes the round-2 referee's own [−0.084, +0.093] was wrong and the authors were right to
overrule it). 1.2 **applied (a), (b), (c)**, all verified — but see the new 1.3 and 1.4 above. 1.3
**applied and it introduced 0.2**; the request to raise replicates above 1,000 was neither done nor
addressed. 1.4 **partial**. 1.5 **not applied**. 1.6 **applied as disclosure, not as computation** —
defensible, but it is a competing explanation for a *terrain* sign flip and cheap to settle. 1.7
**applied correctly** (both promises now say plainly they were not run). 1.8 **not applied**.

**Tier 2 (R2's audit).** 2.1 **applied correctly** (all three ΔAUC values verify; seam figures reported
with the source's caveats; still one AOI). 2.2 **partial** — §3.4's new paragraph is accurate on
collection, QA bits, ST_QA, the min-valid-count and MOD11A1/Terra/daytime, all verified bit by bit; the
requested supplementary table, the QA_RADSAT error and MODIS QC handling are not in, and QC turns out
to be the load-bearing part. 2.3 **applied but its source is wrong** → 0.6. 2.4 **applied; reporting
selective** → 2.3. 2.5 **partial** — mechanism named and the general claim retired, but the fitted
edges were not reported, and reporting them would have surfaced the sea-edge problem. 2.6 **partial;
one number wrong** → 0.14, 2.3. 2.7 **partial** → 2.7. 2.8 **applied correctly**. 2.9 **partial** →
0.8, 2.8. 2.10 **half applied** — blocked-CV trio in and verified; AoA label-blindness qualification
applied faithfully; remote-sensing references absent.

---

## Where the referees disagree, and what could not be verified

**The compositing A/B's second reference chain — ✅ RESOLVED in R3's favour.** R3 reported that
`04_results.md:736-738` attributes both paired comparisons to the production chain while the second
is referenced to the date-balanced chain; R2 reported round-2 2.1 as applied correctly. Both summaries
were read in this session:

- `landsat_composite_downstream_ab/manavgat_2021/downstream_ab_summary.md:3-4` — reference
  `scene_weighted_reference` (production), candidate `date_balanced_lst_only`; paired roc_auc
  **+0.0208635 [+0.0123931, +0.030768]**.
- `landsat_harmonization_downstream_ab/manavgat_2021/harmonization_downstream_ab_summary.md:3-4` —
  reference **`date_balanced_reference`**, candidate `overlap_harmonized_date_balanced`; paired
  roc_auc **−0.0394583 [−0.0498949, −0.0289177]**.

So the −0.040 is overlap-harmonised *minus date-balanced*, not minus production. The
production-referenced difference is 0.0449967 − 0.0635916 = **−0.019**. The manuscript's "both paired
comparisons **against the production chain**" is wrong for the second one; R2's reading that the
values verify is also right — the three chain ΔAUCs verify exactly (0.0635916, 0.0844551, 0.0449967
against the printed +0.064, +0.084, +0.045 and all three intervals) — the error is in the attribution,
not the arithmetic. This also settles Tier 3.3's +0.084 / +0.085 pair: the frozen value is 0.0844551,
so §4.7i's +0.084 is right and §5.8 / §5.11(xi)'s +0.085 is wrong.

**The Muğla two-event control.** Round 2 split on whether to downgrade it for the season/phase
confound. R2 holds that position and adds 0.5 as an independent second reason. R2 also **withdraws one
of its own round-2 objections**: the 2022 baseline climatology is 24 Apr – 20 Jun of 2018–2021
(`repo/core/regions.py:534-538`), which precedes the 2021 Muğla ignition of 29 July, so the anomaly
channels are **not** referenced to a post-fire baseline. That objection should be dropped.

**Not measured, only inferred.** R2 could not locate any file measuring per-cell date support for
Manavgat. The "seven dates inside the path overlap, three or four outside" figure at
`03_methods.md:182-185` is arithmetically correct as an *inference* from the frozen date × path table
(`daily_inventory.json`: 7 dates, 14 scenes, path 177 on 3 dates and 178 on 4, strictly alternating,
each date spanning rows 34 and 35), but the inventory does not map cells to the overlap polygon and a
cell must fall in the right *row* as well as the right path. Per-pixel `unique_date_valid_count`
products referenced in `support_invariance.json` could make the statement measured. Separately, the
"only region with a frozen acquisition inventory" claim is verified and **stronger** than stated, now
on an exhaustive rather than a targeted sweep: every path in `drive_new/` matching `*provenance*`,
`*scene*`, `*acquisition*`, `*inventory*`, `*seam*` or `*wrs*` returns only the two empty
`qa/source_scene_provenance/v1/` directories for Muğla and Montiferru
(`"status": "insufficient_boundary_metadata"`, `scene_count: 0`, `scene_manifest.json` = `[]`),
**nothing at all for Bejís 2022 or Evia 2021 extended** under any name at any depth, and otherwise only
Manavgat tile rasters under `diagnostics/landsat_composite_counterfactual/manavgat_2021/_tiles/`.

One gap recorded honestly: three directories could not be descended into (`File too large`) —
`drive_new/cross_region/mugla_2021__mugla_2022_event_relative/{step9d,step9e,step10}`. These are
cross-region transfer *result* namespaces with the same structure as the other sixteen `cross_region/*`
pairs, so a Landsat acquisition inventory hiding there is implausible, but they were not read.

---

## What all three told you to leave alone

- **§4.7g and `transfer_ci_blocksize.md`.** R1 recomputed the verdict counts, the widening factors
  (levels 2.10–3.55, median 2.81; deltas 1.52–3.41, median 2.30) and the −0.00045 bound from the JSON:
  all exact. R3 re-derived the 12/6/2, 9/4/7 and 10/7/3 splits direction by direction: all exact. Two
  referees called it the best statistical writing in the manuscript.
- **§4.3's interval paragraph on the +0.004 headline.** All four resampling units reproduce
  `referee2_numbers.md` block A exactly. The sentence "the correct reading of +0.004 is not 'a small
  positive contribution' but 'no contribution that this design can distinguish from zero'" is the right
  reading and the right register.
- **§4.4's "how strong is the supported-conditional result?" paragraph** — tie ceiling +0.861 against
  observed +0.840, exact permutation p 0.0060 against Bonferroni 0.0026, and the admission that the
  selection runs once outside the bootstrap. "The design has no headroom" is exactly right and is a
  stronger self-criticism than a correction would have been.
- **Signed AUCs never folded to max(AUC, 1−AUC)**, and below-chance transfer read as inversion
  (§3.10:468-470, §3.12:574-581).
- **The paired, blocked bootstrap** (`step8c:321-330`): one shared resampled index for both probability
  series inside each replicate, single-class replicates counted and excluded rather than silently
  redrawn.
- **The QA_PIXEL bitmask.** R2 read `step3_landsat_lst.py:67-98` line by line: bits 0–5 masked in
  exactly the paper's order; all four confidence pairs tested at bits 8-9/10-11/12-13/14-15, each
  required `< 2`, so "medium and high confidence treated as masked" is **exactly true, not high-only**.
  Description and line citation both exact.
- **The label export's month-alignment and per-image year masking**
  (`step6_validate_fire_relation.py:705-750`), and the paper's statement that the zero out-of-window
  count is "a property of the export rather than an empirical finding" — exactly right and rare to see
  stated.
- **`valid_for_modeling` and the thermal exclusion from it** (`step8a:1412-1435`): built from NDVI,
  elevation and slope only, with the label and all six thermal channels genuinely absent.
- **The CORAL implementation and its label-blind firewall** (`core/step10_shared.py:186-220`;
  `step10b:151-155`): the transform applied to the source only, `assert_label_blind` a real `raise`
  called before any fit.
- **The forbidden-column enforcement**: a real `raise` as the first statement of `build_pipeline`
  (`step8b:265-271`, `:450`), with the 18-column list stamped into every frozen run.
- **The gap-fill-only fusion** (`step7e:291-297`): observed and gap-fill writes provably disjoint, no
  blending. **The NDVI construction** (`step3:133-144`): both masks present, out-of-range values masked
  rather than clamped.
- **The gate numbers**, every verdict and fraction verifying to the printed digits, including
  Montiferru's 0.27403 and Kozan's 542 / 0.01661 / 0.98339. **The natural-vegetation population
  choice**, which removes the stubble-burning confound.
- **§5.2 stating outright that the sharpest supported reversal belongs to a static predictor**, and
  **§5.4 conceding the diagnostic is undefined on Bejís–Montiferru**, half of the paper's own headline
  counterexample. Both cut against the paper's framing and both are correct.
- **§5.9's fourth bounding difference** (baseline averages 0.5371, four directions entirely below
  chance). R1 verified all four; the paragraph costs the paper its cleanest narrative voluntarily.
- **Table R11 and its no-skill column**, and the concession that ROC and PR disagree on
  Montiferru→Manavgat and Bejís→Manavgat.
- **Table 3.** R1 traced all fifteen rows to the frozen metrics and bootstrap summaries: point
  estimates and bounds all correct, and consistently point estimates rather than bootstrap means.
- **S1's seven limits, especially limit 4** (880 of Bejís's 1,100 burned cells inside the top budget;
  confirmed at `mean_adaptation_positive_count = 880`). Once 0.1 is fixed, limit 4 is what keeps §4.10
  honest.
- **The two-arm reproduction record and the independent execution of the Muğla pair.** Whatever is
  said about that pair's design, the provenance work around it is exemplary.

---

## Suggested order of work

1. **The nine-place few-shot miscount (0.1)** and **the block-size sweep (0.2)**. Both are pure text,
   both are corroborated by two referees, and both currently stand in the abstract.
2. **The rest of Tier 0** — all text fixes against evidence in hand. 0.5, 0.6 and 0.11 change what
   Methods and Discussion claim; 0.7, 0.10, 0.13, 0.14 change printed numbers.
3. **Tier 1.1 and 1.2** — delete the exchange rate, add the Evia legacy row. Arithmetic on frozen
   numbers; 1.2's number is already computed above.
4. **Fix `STATUS.md`** to stop reporting round 2 as fully applied, and **re-sweep round-2 0.1, 0.9 and
   1.4** to every occurrence rather than the cited line. The lesson of this round is that
   line-scoped fixes do not hold.
5. **Settle the compositing reference chain** (disagreements section) — five minutes.
6. **Tier 2.3 and 2.4** — two extra Table R14 rows and two extra Table R10 columns, both from frozen
   files. Cheapest substantive gains available.
7. **Decide on Tier 2.1** (the sea-in-TVDI-edges re-run). It is the strongest competing mechanism on
   the table for the reversals, it is a genuine re-run, and it may strengthen the paper.
8. **Emrehan round** — `emrehan_mail_5.md` is still unsent. Add: the Manavgat step7c metadata
   contradiction (0.6), the MODIS QC 3-versus-2 split and the Bejís/Muğla zero fractions (2.2), the
   `48b56e7` line-citation regeneration (0.15), and whether a water-masked TVDI refit is runnable.

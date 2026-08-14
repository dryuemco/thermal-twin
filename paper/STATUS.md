# Manuscript status — one-page overview

**Snapshot 2026-08-08** (after the figure/typography round, the figure renumbering, the caption
round and the literature sweep). Word counts are whole-file (incl. tables/notes). Marker counts
distinguish the document **body** from housekeeping mentions inside DRAFT-NOTES comment blocks
and file headers.

**Updated 2026-08-11** — ERA5-Land block (§3.17, §4.9, §5.7) and the Muğla two-event block
(§3.16.4, §4.8, §5.2 addition) added from hash-verified raw files; ERA5 validator executed
(27/27 PASS); §3.1 and §3.16.3 TO VERIFY markers closed from source; discussion renumbered
(§5.7 inserted, former §5.7–§5.10 → §5.8–§5.11); results gained §4.8 and §4.9 with
Tables R7–R10.
The Muğla 2021↔2022 transfer arms, which had never been run, were computed here with the pipeline
author's unmodified step9b/step9c — the only transfer directions in the paper not from his export.

**Updated 2026-08-13 (internal referee round, Methods).** Three referee-anticipation edits were made
to `03_methods.md`, no number changed:
- **§3.11** now states the CORAL λ sweep exactly as it was run (nine values 0 to 10⁻¹, four
  directions, both model families, `contextual_only_not_rerun` for Manavgat↔Bejís) and gives the
  omission of λ = 1 as a reasoned choice rather than a gap. Verified against
  `drive_new/diagnostics/coral_lambda_sensitivity/b74d643e…/lambda_grid.csv` and `config.json`:
  **λ = 1 exists nowhere in the five-region export.** The only λ = 1 evidence is the superseded
  two-region run (`experiments/cross_region/step10/coral_lambda_sensitivity.csv`, λ ∈ {1e-5, 1e-3,
  1e-1, 1}), and §3.11 says so and labels it superseded.
- **§3.14.1** gained two paragraphs: provenance of the candidate set (what was fixed, where it is
  recorded, and the explicit statement that this is a project analysis log and **not** a formal
  pre-registration, with no independent timestamped public registration), and a multiplicity
  paragraph (20 variants, 1 not computable so 19 computed, effective n = 10 unordered pairs, no
  family-wise error control claimed).
- **§3.17** now points at §3.14.1 for that provenance instead of asserting it standalone.
- *For the Discussion agent:* §5.6's word "pre-registered" is not supported as a formal
  registration. §3.14.1 supplies the exact wording to align to.
- *For the Results agent:* §4.8 line 414 still cites `A07_...` as the guarantee. It is not.
  Confirmed in `repo/scripts/validate_era5_land_regional_diagnostic.py` at `48b56e7`: A07 (lines
  319 to 324) tests list membership of the literal string `mugla_2022` and cannot catch
  `mugla_2022_event_relative`; `A08_cohort_is_the_frozen_five` (lines 318, 325 to 326) is the real
  guarantee. §3.16.4 already carries the correct account.

**Updated 2026-08-14 (referee round 2).** A four-reader panel (statistics, remote sensing, claim
versus evidence, editorial) read the manuscript independently. All four returned *major revision*;
the editorial reader added *not submittable today*. The consolidated dossier is
`paper/REFEREE_ROUND_2.md` and the numbers it needed are in `paper/referee2_numbers.md` and
`.json`, produced by `paper/referee2_numbers.mjs` from frozen artefacts only.

**Correction, 2026-08-14 (referee round 3):** the claim below that the round-2 dossier was applied in
full apart from length and tables is **not accurate**. Round-3 auditing found that round-2 items
**1.5** (BCa / ratio denominators) and **1.8** (Evia legacy-AOI within-region increment) were never
applied, items 0.1, 0.9 and 1.4 were applied only at the lines they cited, and five round-2 repairs
introduced new defects. See `paper/REFEREE_ROUND_3.md`, "The round-2 regression audit".

**Everything in that dossier was applied except the length and table-load reduction**
(dossier §3.1 to §3.3), which the author deferred, and except the two items named above. What changed:
- **Four statements the paper's own evidence contradicted** were corrected. The largest was
  "adaptation degrades every direction that already transferred" (§4.3, §1.5, §5.1): of the twelve
  CI-supported above-chance directions, nine are degraded and three raised, all three with
  Montiferru as source. The label-free taxonomy was corrected throughout (niche overlap and regime
  structure need the target's labels too; only the marginal family is pre-deployment). The
  pre-label-exclusion parity claim in §3.16.4 was false and is now per region. The LORO ceiling gap
  is 0.28 to 0.50, not 0.22.
- **New numbers, all from frozen artefacts.** A cluster-aware interval on the +0.004 headline
  (pair-clustered [−0.028, +0.036], spans zero under every unit); the conditional index at its own
  design size (tie ceiling +0.861, exact permutation p = 0.0060 against a Bonferroni 0.0026);
  per-region spatial-block counts at 2/10/20 cells, which show the 20-cell row resting on six to
  twelve positive-carrying blocks; the Step 8D ablation, previously frozen and never cited; Step 7C
  downscaling validation; fused-LST gap-fill shares.
- **New content:** §4.7h (which thermal channel carries the increment), §4.7i (Landsat compositing
  sensitivity, ±0.02), §4.10 (the recovery curve promoted from S1), Table 2 (the feature dictionary,
  which was referenced but did not exist), five new limitations §5.11(xi) to (xv), an expanded
  §5.10 with the practitioner answer, and the blocked-CV dispute in §2.3 with three verified
  references (Wadoux 2021, Milà 2022, de Bruin 2022).
- **Title changed** to *Local skill, unstable portability: marginal diagnostics do not order the
  cross-region transfer of pre-fire thermal dryness in Mediterranean wildfire regions*. The previous
  title asserted more than §5.4 concedes.
- **Abstract 250 to 322 words**, deliberately, with a documented cut order if the limit is 250.
- **Front matter:** CRediT, competing interest, funding and data-availability blocks added;
  keywords finalised. Affiliation (Çukurova University, Adana), corresponding author
  (`ycogurcu@cu.edu.tr`) and funding (BAP project 17506) supplied by YEC 2026-08-14. Still open and
  optional: department or faculty, ORCIDs, and the project's full title in the funding sentence. The availability statement now names all three provenance gaps in plain terms and the
  "checked rather than taken on trust" claim has been narrowed to match.
- `build_tex.mjs` now strips horizontal rules (they were becoming em dashes, against the house
  style); `verify_tex.mjs` no longer counts whole-line LaTeX comments as unescaped percent signs.
  12/12 source checks pass. Compiled clean 2026-08-14 (see the compile entry below).
- `emrehan_mail_5.md` gained items 5 to 9 (Manavgat Step 7 MODIS contract, Bejís compositing A/B,
  per-region acquisition inventory, calendar-matched Muğla 2022, two QA one-liners).

**Updated 2026-08-14 (referee round 3).** A three-reader panel (statistics; remote sensing, fire
ecology and data provenance; claim versus evidence) re-read the manuscript independently. The
editorial lens was deliberately excluded, so round 2's Tier 3 (length, table load, figure count)
stands undischarged. All three returned *major revision*. The dossier is `paper/REFEREE_ROUND_3.md`:
15 Tier 0 items, 7 Tier 1, 13 Tier 2, 3 Tier 3, plus a regression audit of round 2.

Nothing in round 3 overturns the negative result, and several findings strengthen it. One round-2
finding is **retracted**: item 2.3 (Manavgat's "four-year summer-mean MODIS layer") rests on a stale
hardcoded literal that the exporting run's own `modis_metadata.json` contradicts, so §3.4 and
§5.11(xiii) currently explain the paper's one acknowledged anomaly with a difference that does not
exist. That is the first thing to fix and it is **not yet done**.

**Applied 2026-08-14, after independent re-derivation from the frozen artefacts** (eight spot-checks,
eight held exactly; see the ✅ marks in the dossier):
- **Few-shot recovery: "four of six" → three** (0.845, 0.852, 0.894 at 32 blocks), with the 51/57 and
  30 % directions now stated and the false "from starting points at or below chance" corrected —
  Muğla→Bejís starts at 0.583. Fixed in the abstract, §1 C6, §4.10, §5.10, §6 and S1.
- **Table R1's `Burned` and `Prevalence` columns** moved to the post-filter counts: Muğla 3,026,
  Evia 2,788, Montiferru 697 / 0.220 (was 0.236). The table had been dividing a pre-filter numerator
  by its own post-filter `Valid cells` denominator. No modelled number changes.
- **CORAL λ spread 0.008 → 0.014** overall, with 0.008 kept as the thermal-family bound (§3.11, §4.7d).
- **Evia coordinate importance 0.101 → 0.097** (§3.4).
- **Evia legacy-AOI within-region increment added** to §4.7a: +0.085 [+0.072, +0.100] against the
  extended AOI's +0.153, both excluding zero. This closes round-2 item 1.8 and states that the top of
  the paper's within-region range is specific to the extended AOI.
- **The 6:1 exchange rate deleted** from the abstract, §1.1, §1 C1, §4.6b, §5.5 and §6. The debit
  (−0.081 within-region, supported in every region) is measured; the +0.014 transfer side is a mean
  over twenty non-independent directions whose pair-clustered interval [−0.017, +0.045] spans zero.
- **§4.3's Bejís–Muğla sentence** corrected: the thermal block carries Muğla→Bejís above chance, but
  Bejís→Muğla already transferred above chance on the baseline alone (0.592 [0.575, 0.609]).
- **§4.7i's compositing attribution** corrected — the −0.040 comparison is referenced to the
  date-balanced chain, not production; production-referenced it is −0.019. §5.8 and §5.11(xi)'s
  +0.085 corrected to the frozen +0.084.

`build_tex.mjs` re-run; `verify_tex.mjs` 12/12 PASS, `check_style.mjs` 0 dashes.

**Updated 2026-08-14 (round 3 applied in full, submission pass).** Every remaining Tier 0 item was
re-derived from the frozen artefacts first, then applied. Two referee claims did **not** survive that
re-derivation and were not applied as written; both are recorded below. The abstract, highlights and
Fig. 3 / Fig. 5 captions were re-scoped to match. `build_tex.mjs` re-run; `verify_tex.mjs` 12/12
PASS; `check_style.mjs` 0 dashes.

- **0.6 Manavgat MODIS — retracted, with a stronger evidence base than the dossier had.** Verified:
  the four-year string is emitted only under `is_kozan` at `48b56e7`; the conditional arrived in
  `7b1c8ac` (2026-07-10T12:26:05+03:00), one day *after* Manavgat's Step 7C ran (2026-07-09T15:28:31);
  Manavgat's own `modis_metadata.json`, written three hours earlier, gives the single-season
  predictor window and the words "NOT a multi-year baseline". **New:** all five regions used
  single-season predictor-window layers, and Manavgat is the only region carrying the stale string,
  in Step 7C *and* Step 7D. §3.4's "the MODIS input is not the same quantity in every region" was
  therefore false too. Replaced with the real heterogeneity (Tier 2.2, verified): QC screening and
  nodata encoding split 2 versus 3, by export date, not by design.
- **0.5 Muğla two-event — applied; every per-cell number reproduced exactly.** 41,730 → 38,790 TSG;
  the arms share 38,789 of 38,790 cells; `elevation_mean`, `slope_mean` and `landcover_dominant` are
  byte-identical across all 73,098 cells; all 2,911 target positives are outside the 2022 source
  population and 38,789 of 38,819 negatives inside it, giving membership AUC 0.9996; all 331 of the
  2022 positives were in the 2021 training set. "Only the event differs" and "only the fire differs"
  are gone; §3.16.4 now names the exclusion and its elevation composition; §4.8 and §5.11(ii) carry
  the non-comparability.
- **0.2 ~10 km blocking — re-scoped everywhere** (§4.2, §1 C5, §5.1, §5.2, §6, Fig. 3 caption).
  Support is claimed at 1 km and 5 km only; 10 km is stated as indicative, with the 12/6/33/15/6
  positive-carrying block counts re-derived. Fig. 3 needs no rebuild: "all fifteen" lived only in the
  script's provenance string and stdout, never on the canvas.
- **0.3 / 0.4 — applied, but the dossier's own replacement text was wrong by one.** Recomputing all
  twenty directions from Table 4 (spot-checked against `step10_metrics.csv`) gives **six** directions
  ending further from chance, not five: the five upward Montiferru cases *and* Manavgat→Muğla moving
  downward, 0.470 → 0.443, which the dossier names in its prose and then omits from its fix. The
  paper now states 14 of 20 compressed, names all six exceptions, and flags that Bejís→Manavgat is
  counted as compressed on a margin of 0.001.
- **0.10 non-square cell — applied and independently confirmed.** 17 × (30 / 111,319.49) =
  0.0045814°; 510 m north-south, 390 to 407 m east-west; area 0.199 to 0.208 km² against 0.250. The
  derivation reproduces **all five** frozen cell counts exactly (175×138, 153×103, 393×186, 175×131,
  66×49). Both consequences are now stated: blocking is weaker in longitude, and the burned footprint
  is dilated relative to MCD64A1.
- **0.8 / 0.9 / 0.11 — applied.** The label rule is the mode of positive DOY values and coincides
  with "any positive" only because `count_positive == count_in_label_doy_range` in all five exports.
  `exclude_historical_burns` appears exactly once in the registry, so prior-year burning is screened
  for **no** study region. The Evia AOI supersession was label-informed and §3.1 now says so.
- **0.15 line citations — regenerated.** Six were wrong and are fixed (`step8a:1217-1261`,
  `step8a:967-1025`/`3059-3072`/`1179-1188`, `step8a:1339-1342`, `step6b:198-219`,
  `step5:899-905`, plus `core/config.py:86-87` added for the LST scale/offset). **The dossier was
  wrong on two counts here:** `core/config.py:89 to 103` is correct as cited, because the sentence
  cites it for the NDVI reflectance scale/offset (lines 91 to 92) and the NDVI validity bounds (line
  103), not for `LANDSAT_SCALE`; and the blanket "every step8a range is one line low" does not hold,
  the others resolve correctly.
- **Tier 2.1 sea in the TVDI edges — resolved without the raster re-run, against the dossier's
  conclusion.** Re-derived: water-dominant cells are 57.6 % of Evia's grid, 38.9 % of Muğla's, 0.1 %
  of Bejís's, and Evia's three lowest NDVI bins do carry sea-surface dry edges of 28.8 to 29.9 °C.
  But the modelled population does not occupy those bins: **no** primary-population cell in any region
  has mean NDVI below 0.15 (5th percentile 0.376 in Evia), there is no clamp saturation (0.5 % of
  Evia cells at the upper clamp against 0.1 % in Bejís), and in the vegetated bins the edges do not
  order by sea fraction at all, the lowest wet edge belonging to Montiferru at 7.4 % water and the
  highest to Bejís at 0.1 %. The half of the finding that *does* hold, that the secondary all-valid
  population is 57.7 % and 38.9 % seawater in two regions, is now stated in §4.7f. The land-only edge
  refit remains un-run and is stated as such.

**Updated 2026-08-14 (the pipeline now runs here).** `.venv-step10` was rebuilt and **verified**:
`step8b` re-run unmodified at `48b56e7` reproduces the archived metrics bit for bit (Manavgat 142
fields, max diff 6.9e-18; Montiferru 168 fields, max diff exactly 0). Recipe in `ENVIRONMENT.md`.
Note the trap: `requirements-lock.txt` pins NumPy 2.5.1 / pandas 3.0.3, which is **not** the
environment that produced the paper's numbers (2.4.4 / 3.0.2, from `reproduction_check_5region.json`).

**Every analysis the manuscript recorded as "not run" has since been run** (commit `82c18b8`), each
by driving the pipeline's own code and reproducing a frozen counterpart first. Reports:
`paper/tvdi_land_refit.md`, `paper/observational_sensitivities.md`.
- **TVDI land-only refit and pooled common edge** (§4.7k, Table R11): sea moves the index in
  proportion to sea fraction but changes no region's direction, and a common edge across all five
  regions leaves the reversal intact. The referee's strongest competing explanation fails.
- **High-agreement cells** (§4.7l, Table R12): the elevation reversal holds at every threshold.
- **Increment without the two coordinate-bearing channels** (§4.7h): 82 % to 103 % retained.
- **Low gap-fill** (§4.7m): support everywhere; Bejís moves most, +0.056 to +0.043.
- **CORAL λ = 1** (§3.11, §4.7d): no direction crosses chance; the largest move is an improvement,
  against what §3.11 predicted. Grid spread widens to 0.019 overall, 0.016 thermal.

Two corrections fell out, both against the paper's convenience: MODIS zero-fill is **38.29 % in
Muğla** and **none in Bejís** against Manavgat's 8.11 %, and tracks each AOI's water share, so it is
sea rather than missing observation; and the §5.11(xv) "cheap query" is unanswerable, because both
MCD64A1 rasters are clipped to the label window.

**Updated 2026-08-14 (first LaTeX compile).** MiKTeX installed; **both documents now compile clean**,
with no errors, no undefined references and no undefined citations. `manuscript.pdf` is 193 pages,
`supplementary.pdf` is 5. The compile was treated as a debugging pass and found four defects no
source check could see, all fixed in `build_tex.mjs`:
- the Unicode table was applied to prose but not to code spans, so a true minus inside
  `(current_median − baseline_mean)` stopped the run;
- a verbatim block carried λ, a true minus and a middle dot, none of which can be escaped inside
  verbatim, so that block is now ASCII in the Markdown and the builder folds and warns;
- figure paths resolved from `paper/` while the compile runs in `paper/tex/`, so all eight figures
  were missing;
- `l` columns cannot wrap, so the widest table ran 763 pt past a 390 pt text width. Tables now pick
  a font step from their estimated width and wrap prose columns through `tabularx`. The worst
  overfull is down to 178 pt and the count above 50 pt from 78 to 19.

Also fixed: `REFERENCES.bib` had three entries with `%` comments **inside** the braces, which BibTeX
reads as field names, so it skipped those entries; the comments were moved above their entries.
`lmodern` was added so the PDF carries scalable Type 1 fonts rather than the bitmap `ec` fonts
METAFONT was generating. Identifiers may now break after underscores and slashes but never at a
decimal point, which the number check caught when `500.0` came out as `500.` and `0`.

**Updated 2026-08-14 (Earth Engine obtained).** YEC registered Çukurova University for noncommercial
use and created project **`thermaltwin`**; the hardcoded `b7-thermal-digital-twin` in
`core/config.py:7` is the pipeline author's and is not accessible. The project is injected by
wrapping `ee.Initialize`, so `repo/` is untouched. `geemap` had to be added for the export paths.

**The calendar-matched Muğla 2022 arm is not a missing analysis, it is an impossible one**, and this
section previously called it the most valuable follow-up the paper could name. The two Muğla events
are 42 days apart in seasonal phase (median burn day-of-year 215 in 2021, 173 in 2022, read from each
experiment's frozen label raster), and neither year contains a second event at the other's phase.
Holding the calendar fixed at the 2021 window leaves **9 burned cells** against a gate minimum of 30;
the whole of 2022 in that AOI is 358 burned pixels against 3,206 in 2021. §5.2, §5.11(ii) and the
outstanding-analyses paragraph now state this as a limit of the fire record. Full working:
`paper/mugla_calendar_arm.md`.

*One methodological trap recorded there because it nearly changed the answer:* MCD64A1 is a monthly
composite stamped at the first of the month, so filtering the collection by the analysis window's own
dates drops the composite of the month the window opens in. The first probe did that and undercounted
the June 2022 event eightfold; it was caught only because the implied reconstruction ratio came out at
8.1 cells per pixel against 1.19 for the year before.

**One-line state:** round 3 is fully discharged and the submission package is assembled
(`COVER_LETTER.md` drafted, highlights re-checked at ≤85 characters, abstract 329 words). What
remains is outside this round: round 2's deferred length reduction (~31k words, 19 main-text tables),
the optional front-matter facts
(department, ORCIDs, funding project title), and the two reproducibility blockers that sit with the
pipeline author (`emrehan_mail_5.md`, still unsent).

## 1. Manuscript sections

| File | Status | Words | Open markers (body) |
|---|---|---|---|
| `00_abstract.md` | **draft complete** (trim to journal limit at submission) | 331 | none |
| `01_introduction.md` | **draft complete**; contributions filled with final numbers | 2 511 | none (1 UNVERIFIED mention is the header convention note) |
| `02_related_work.md` | **draft complete**; Dimarco §2.5 passage now confirmed against the full text (read by YEC 2026-08-08; 80/20 hold-out and NTL-log1p details added) | 5 267 | none — the Huang §2.4 marker was **closed 2026-08-08 by decision** (no coefficient quoted; §2.4 now says so explicitly, abstract suffices). *Correction: an earlier STATUS mislabelled this marker as Dimarco.* |
| `03_methods.md` | **draft complete** incl. §3.14–3.16; awaiting independent-description comparison | 9 388 | **none (was 1).** **Closed 2026-08-13:** the five-region reproduction-check quote — numbers read from the archived `reproduction_check.json`; §3.16.4 also gained the independent-execution paragraph for the Muğla pair. **Closed 2026-08-11:** regions.py registry lines (repo pulled to 48b56e7; core.regions imported and queried, all Table 1 values match, caption line numbers corrected) and window-closure block edge length (2 cells ~1 km, read from source). Gained §3.16.4 (Muğla two-event design) and §3.17 (ERA5-Land diagnostic, validator 27/27 PASS). **Closed 2026-08-08:** Kozan inclusion (now in — §3.1 pointer, §3.3 negative-control paragraph, §4.1 result); §3.3 gate-verdict marker (§3.3 now points to §4.1, where Table R1 carries the numbers); repository URL/DOI (data-and-code availability statement written, GitHub URL, no DOI) |
| `04_results.md` | **draft complete, audited**; Tables 3–6 + R1–R10 | 6 697 | none. §4.8 (two Muğla events, Tables R7–R9) and §4.9 (ERA5, Table R10) added 2026-08-11; the §4.8 [PENDING] was closed by running the transfer arms. |
| `05_discussion.md` | **draft complete, audited**; renumbered 2026-08-11 (§5.7 inserted; former §5.7–§5.10 → §5.8–§5.11) | 6 383 | **none (was 1).** **Closed 2026-08-13:** §5.5 few-shot supplementary inclusion — confirmed in, pointer now names Supplementary S1. §5.11(ii) now states the Muğla-2022 position from data rather than as a placeholder; an AoA per-pair number is conditional on a reviewer request (notes only) |
| `06_conclusions.md` | **draft complete** | 334 | none |
| `S1_few_shot_recovery.md` | **new 2026-08-13** — supplementary S1: target-label recovery curve, 3 regions / 6 directions, read from the frozen `few_shot_recovery` export; design, Table S1, seven stated methodological limits | 1 500 | none |
| `highlights.md` | **complete** (5 bullets, all ≤85 chars, verified) | 90 | none |
| `figure_captions.tex` | **complete** — Elsevier format, 8 captions in figure order, each self-contained (what is plotted, population, interval, meaning; panel letters explained inline). Every numeric value verified against the frozen outputs | 1 786 | none |
| `REFERENCES.bib` | **fully re-verified 2026-08-13** — 47 entries checked, **45 remain**: every DOI resolved, year/volume/pages machine-compared against Crossref; 1 broken DOI found and fixed (Cook2014); 3 entries completed; Soydan2022 and Varela2022 removed as uncited. No orphans in either direction. Previously: 2026-08-08 sweep added Crossref-verified Sun2016 DOI, Soydan2022 (Manavgat event), Varela2022 (Evia event); **second round 2026-08-08 removed Cosandal2022** (Muğla weak-fit, never cited) | — | **none.** GLO-30 closed (cited inline by product-page URL + access date, no DOI, no bib entry; GLO-30 confirmed as the DEM that ran). Bejís and Muğla event descriptions closed as deliberately uncited — no citable event-specific source exists, numbers come from MCD64A1 |

## 2. Analysis reports (frozen evidence base — all complete, no open markers)

| File | Words | Feeds |
|---|---|---|
| `regime_transfer_correlation.md` | 1 230 | §4.4, §5.6 |
| `conditional_similarity_transfer.md` (incl. 2026-08-08 scope correction) | 1 184 | §4.4–4.5, §5.4 |
| `loro_pooled_transfer.md` | 821 | §4.6a |
| `feature_drop_transfer.md` | 754 | §4.6b |
| `niche_overlap_transfer.md` | 843 | §4.4–4.5 |
| `niche_vs_conditional.md` | 790 | §4.4, §5.3 |
| `baseline_vs_thermal_transfer.md` | 672 | §4.3 Table R6, §5.1 |
| `all_diagnostics_vs_transfer.md` | 672 | Table 6 |
| `sklearn_version_sensitivity.md` | 364 | §4.7e, §3.13 |
| `signed_auc_bootstrap.md` | 1 135 | historical (3-region, partial export); superseded by the five-region feature-stability table but kept as independent validation |

## 3. Figures (`paper/figures/` — all built: vector PDF+SVG, provenance JSON, build-time asserts)

| Fig. | Content | File | Status |
|---|---|---|---|
| 1 | Study-region map + Kozan gate control (Natural Earth 1:50m, plain) | `fig1_study_map` | done |
| 2 | Methods schematic (gate branch, §3.12 decomposition, footer) | `fig2_schematic` | done |
| 3 | Within-region increment + block robustness (3 panels) | `fig3_within_robustness` | done |
| 4 | Transfer matrices raw/z/CORAL (diverging, chance-centred, below-chance hatched) | `fig4_transfer_matrix` | done |
| 5 | Label-blind adaptation compresses toward chance (12 directions) | `fig5_adaptation` | done |
| 6 | LORO pooling never beats the best single source | `fig6_loro` | done |
| 7 | Feature removal is a zero-sum trade-off | `fig7_feature_drop` | done |
| 8 | **Main figure** — contrast pairs with per-region CI-support arrowheads | `fig8_contrast_pairs` | done |

**Figure standard (applies to all eight).** Double column 190 mm, body 9 pt, minimum 8 pt,
vector PDF + SVG, Okabe-Ito, no red–green pair. Numbering is consecutive integers; lettered
sub-numbers are reserved for panels of one figure and are not used.

*Build-time verification.* `figures/_layout_check.py` runs inside every figure script and fails
the build on: text–text overlap or sub-threshold gap, text over a data artist, text leaving its
axes or the canvas, a legend leaving its own axes, a label overflowing its container box, or any
text below the minimum point size. All eight currently report **no problems**, minimum text gap
3.02–9.78 pt. Each script additionally asserts its own numbers against the frozen outputs; Fig. 2
asserts its 14 section references against the live `03_methods.md` heading list, and Fig. 7
asserts the monotone trade-off it depicts.

*Print safety.* Greyscale is measured, not assumed. Fig. 4 picks each cell label's colour by WCAG
contrast against that cell's rendered colour (worst case 4.7:1) and hatches below-chance cells,
because a diverging palette is symmetric in luminance and would otherwise lose the sign in
greyscale. Okabe-Ito blue vs orange measures only 2.30:1, so Figs 5 and 8 carry their two-class
distinction on line style as well as hue. Rendered greyscale proofs sit beside Figs 4, 5, 6, 7
and 8 (`*_greyscale.png`).

## 4. Process / historical documents

| File | Role |
|---|---|
| `POSITIONING.md` | authoritative direction document (thesis, C1–C5) — stable |
| `OUTLINE.md` | **stale in parts**: written pre-Evia/pre-Montiferru; §5 "missing before Results" is fully discharged; use only for figure/table budget and honesty constraints |
| `RESULTS_INVENTORY.md` | historical catalogue of the July partial export — superseded by drive_new numbers |
| `LITERATURE.md` | working literature notes; **swept twice on 2026-08-08**. First sweep closed A4/D2/Deep-CORAL/arXiv-2103.05898/Manavgat/Evia/Dimarco. Second sweep closed four of the five consolidated items by decision — GLO-30, Bejís event, Muğla candidate, Huang full text — each with its reasoning recorded. **One item remains open: WildfireGenome (arXiv preprint only; re-check for a peer-reviewed version before submission).** |
| `emrehan_mail.md`, `INTERN_REQUESTS.md` | historical correspondence — delivered |
| `emrehan_mail_4.md` | sent 2026-08-13 (4 items; the manifest-commit item was omitted from it) |
| `emrehan_mail_5.md` | **drafted 2026-08-13, not sent** — 4 items: reproduction-check push, `19d825b`, CORAL λ = 1 arm, manifest commit |
| `STATUS.md` | this file |

## 5. Waiting on external input (coordinated by YEC)

1. **Emrehan's independent Methods narrative** — to be compared against §3.1–3.16; the ten
   candidate discrepancy points are pre-listed in 03_methods' METHODS ROUND NOTES.
2. ~~**Few-shot × conditional-index joint analysis**~~ — **closed 2026-08-13 by decision.** The
   few-shot curve is IN, as `S1_few_shot_recovery.md` (3 regions, 6 directions, Table S1). The
   joint analysis against the conditional index was **not** run and S1 says so explicitly
   (limit 3): with six directions it would be a description, not a test. §5.5 marker removed.
3. ~~**Muğla 2022**~~ — **closed 2026-08-11.** Both frozen diagnostics arrived
   (`paper/mugla_temporal_raw/`, `paper/step9g_raw/`) and the transfer arms, which had never
   been run, were computed here with the pipeline author's unmodified step9b/step9c at 48b56e7
   in a shadow project root (`paper/mugla_transfer_raw/`). §3.16.4, §4.8 (Tables R7–R9) and the
   §5.2 addition are written from them; §5.11(ii) rewritten. **Note the provenance:** these are
   the only two transfer directions in the paper not produced by the pipeline author. The design
   is same-geography event-to-event, not clean temporal transfer (year × seasonal phase
   confounded; see §3.16.4).
4. ~~**Updated `repo/core/regions.py`**~~ — **closed 2026-08-11.** `repo/` is at `48b56e7`, which
   contains all five regions plus `mugla_2022_event_relative`; `core.regions` was imported and
   queried with `get_experiment()` and every Table 1 value matches. `repo/` is now wired into this
   repository as a git submodule pinned at that commit.
5. **Two ERA5-Land follow-ups for the pipeline author** (new 2026-08-11):
   (a) ~~*Reproduction tolerances for the five-region set.*~~ — **closed 2026-08-13.**
   `reproduction_check.json` arrived, is archived at `paper/reproduction_check/`, and §3.13 now
   quotes the five-region figures (within-region max |Δ| = 0 over 20 comparisons; CORAL
   1.6×10⁻⁷ over 20 directions / 80 comparisons). Independently checked: all 20 referenced
   frozen artefacts hash-match locally and all 100 `frozen_value` fields match the numbers
   inside those files. `03_methods.md` now has no open marker.
   (b) *Manifest commit discrepancy.* **STILL OPEN — and it was NOT included in the mail sent
   2026-08-13**, which is an omission: it is the same class of problem as items 6.1/6.2 below
   (published repo vs production commit) and should have been bundled with them. Ask it in the
   next round. `manifest.git_commit` is `a07ea33`, but the diagnostic
   source does not exist at that commit (first committed in `48b56e7`), so the production run used
   an uncommitted working tree. Every contract semantics string matches `48b56e7` verbatim and the
   validator passes, so the output is consistent with the described code, but bit-identity is not
   established. Recorded in §3.17 and `paper/era5_raw/SHA256SUMS.txt`; one question would close it.

6. **Requested 2026-08-13** (mail in `paper/emrehan_mail_4.md`, sent by YEC). Items 1–2 are the
   same issue: the released repository does not contain the code that produced two artefacts the
   paper relies on. Verified against main today — the GitHub zip's archive comment is `48b56e7`
   and its 334 files are content-identical to our pinned `repo/`, so nothing has been pushed
   since 2026-08-11.
   1. *Reproduction-check code absent from the repository.* `scripts/run_reproduction_check.py`
      and `src/reproduction_validation/` are recorded as untracked in the check's own
      `working_tree` field and are absent from `48b56e7` (`find -iname "*reproduction*"` returns
      nothing). §3.13 rests on this artefact and the paper names the repository authoritative, so
      a reviewer cannot re-run it. Asked him to commit, push, and give the hash.
   2. *Few-shot commit `19d825b` unreachable* — not in a full 92-commit clone, so S1's provenance
      line points at something a reader cannot fetch. Either push/tag it, or confirm in one line
      that `src/few_shot_recovery.py` is unchanged between `19d825b` and `48b56e7` (it is present
      at `48b56e7` and last modified 2026-07-31, before the run, so almost certainly identical).
   3. *(Optional)* Muğla block-10 ceiling artefact, which would turn S1's
      `FSR-35[mugla_2021]` SKIPPED into a PASS and close limit 6 of S1.
   4. *Two one-liners:* the Python version of his 2026-08-09 Muğla run (artefacts record
      numpy/pandas/sklearn but not Python), and which validator his self-reference fix touched —
      our frozen few-shot report (2026-08-02) already reads 64 PASS / 1 SKIPPED.

   **Re-verified 2026-08-13 (referee round). Both blockers are STILL OPEN and both undercut the
   manuscript's claim that the repository is authoritative and the negative result re-checkable.**
   `repo/` is wired in as a submodule pinned at `48b56e7` and its worktree is clean.
   - **(1) Reproduction-check code absent.** `git ls-tree -r --name-only HEAD | grep -i reproduction`
     at `48b56e7` returns **nothing**. `scripts/run_reproduction_check.py` and
     `src/reproduction_validation/` are not in the released tree. §3.13 rests entirely on
     `reproduction_check.json`, which no reader can regenerate. This is the single weakest point in
     the reproducibility claim.
   - **(2) Few-shot commit `19d825b` unreachable.** `git cat-file -t 19d825b` in the full clone
     returns `fatal: Not a valid object name`; the clone holds 92 commits and none is that one.
     `src/few_shot_recovery.py` **is** present at `48b56e7`, so the one-line equivalence
     confirmation would close this without a push.
   - Also still open and now bundled with these: the **ERA5-Land manifest commit discrepancy**
     (item 5(b) above), `manifest.git_commit = a07ea33` while the diagnostic source first appears in
     `48b56e7`.
   - A fifth mail drafted for these, plus a request for a λ = 1 arm: **`paper/emrehan_mail_5.md`
     (drafted 2026-08-13, NOT sent).**

   *Repository URL / DOI is no longer waiting:* **closed 2026-08-08** — the data-and-code
   availability statement now names Emrehan's public repository
   `https://github.com/emrehann17/satellite-thermal-digital-twin` (verified reachable
   unauthenticated, MIT licence) and states that **no DOI is minted**. No Zenodo deposit.

## 6. Remaining internal work (no external dependency)

Mechanical only — no analysis, no new numbers, no open judgement calls.

1. **Assembly round.** *(2026-08-13: the mechanical half is done — `paper/tex/` now holds a
   generated `manuscript.tex` + `supplementary.tex` in Elsevier `elsarticle` format, built from
   the Markdown by `build_tex.mjs` and checked by `verify_tex.mjs`, 12/12 source checks passing.
   **Compiled clean 2026-08-14 with MiKTeX.** Remaining: affiliation, keyword confirmation,
   and Table 2.)* Merge the section files into one document; renumber the lettered
   R-tables (R1–R10) into the final sequence alongside Tables 3–6; drop the DRAFT-NOTES comment
   blocks; apply the journal template. Main-text figure numbering is already final and consistent
   across `figure_captions.tex`, §4 and §5. **Added 2026-08-13:** `S1_few_shot_recovery.md` must
   be carried through as supplementary material, with its Table S1 kept out of the main-text
   table sequence.
2. ~~**Abstract trim**~~ — **done 2026-08-13: 271 -> 250 words**, and the same-geography
   two-event control (§4.8) was added, which the previous version omitted. **The journal limit
   was NOT verified**: both the Elsevier and ScienceDirect guide-for-authors pages return HTTP
   403 to automated fetching, and a search result reporting 400 words was not corroborated. 250
   is a deliberately safe target under either limit. Confirm the guide before submission; if 400
   holds there is room to restore the per-region robustness detail and the domain-classifier
   ceiling. (The 331 figure in the old entry counted the drafting note; prose was 271.)
3. ~~**WildfireGenome re-check**~~ — **done 2026-08-13.** Still a preprint: Crossref has zero
   works titled "WildfireGenome" and no matching Liu/Mostafavi journal article; the arXiv record
   carries no `journal-ref`. Kept as `@misc`, now with the arXiv DOI. Its substantive claims were
   re-confirmed against the abstract and are as described in §2.4/§2.5/§5.4. One residual action
   at proof stage: check again, since a late-2025 preprint may appear in press by then
   (`LITERATURE.md` item E2).
4. ~~**Decide on Soydan2022 / Varela2022**~~ — **done 2026-08-13: both removed.** They were the
   only two uncited entries, added 2026-08-08 for the §3.1 event descriptions but never cited,
   and both were recorded as full text unread. Removed rather than cited, matching the Bejís and
   Muğla events; no event-description citation appears anywhere in the paper. The bibliography
   is now 45 entries with **no orphans in either direction**. Rationale kept in `REFERENCES.bib`
   Block H and `LITERATURE.md`.
5. **Optional: graphical abstract** (Elsevier), from a Fig. 8 + Fig. 4 composite.
6. **Supplementary figure S1** (new 2026-08-13, not built). The recovery curve described in
   S1.5: budget on a log-2 axis, target ROC-AUC on the ordinate, one line per direction,
   selection interval as a band, each direction's ceiling as a reference line. Data are ready in
   the frozen `recovery_curve.csv` (thermal family, `metric = roc_auc`); Table S1 already carries
   the numbers, so the figure is presentation only and the supplement stands without it.

### Closed this round (kept for the audit trail)

- ~~Kozan inclusion decision~~ — **in**: §3.3 negative-control paragraph, §4.1 result, and shown
  on Fig. 1 in a deliberately distinct style.
- ~~Repository URL / archival DOI~~ — data-and-code availability statement written; public GitHub
  repository named, **no DOI, no Zenodo deposit**, stated explicitly.
- ~~GLO-30 DEM citation route~~ — verified rather than assumed (frozen `used_fallback: false`);
  cited by ESA product-page URL + access date; SRTM deliberately not cited.
- ~~Bejís / Muğla event sources~~ — left uncited after no citable event-specific source was
  found; extents and dates come from MCD64A1. `Cosandal2022` removed from the bibliography.
- ~~Huang et al. full text~~ — closed by decision; no coefficient of theirs is quoted and §2.4
  now says so. ~~Dimarco full text~~ — read by YEC, §2.5 confirmed.
- ~~§3.3 gate-verdict marker~~ — resolved by pointing §3.3 at §4.1, where Table R1 carries the
  per-region verdicts and fractions.
- ~~Figure typography, greyscale safety, captions, numbering~~ — all eight figures rebuilt to the
  standard in §3; `figure_captions.tex` written and number-checked against the frozen outputs.

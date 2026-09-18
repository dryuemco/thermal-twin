# Referee round 5 — simulated EMS panel, consolidated and verified (2026-09-19)

**Panel.** Four independent simulated reviews of the EMS-retargeted manuscript (commit 34b2803), each
barred from the earlier referee rounds and positioning notes: handling editor; R2 model evaluation and
spatial statistics; R3 thermal remote sensing and wildfire science; R4 reproducibility and software
(with code and artefact access). These are simulations for the authors' benefit, not journal reviews.

**Verdicts.** Editor: **return to authors before review** (not a desk reject). R2, R3, R4: **major
revision**. Consistent message: the arithmetic holds (R2 recomputed ~15 quantities, R4 traced 25; all
matched or were off in the last digit), but framing, estimand definitions, release and provenance do not
yet meet EMS's bar.

**The rule applied.** As in rounds 3–4, a referee claim enters "confirmed" only after it was re-derived
here. Unverified items are marked as such.

## A. Confirmed defects — fix before any submission

| # | Defect | Source | Verified how |
|---|---|---|---|
| A1 | **Manavgat input is non-canonical.** `repo/outputs/.../manavgat_2021` parquet SHA-256 `10af6847…`; canonical record and `drive_new` = `054a1961…`. Thermal columns differ. A(w) and the Data paragraph ("one region's file") are wrong. R4's re-run: per-direction values move ≤0.037, headline means ≤0.003 | R4 | hashes computed here; record in `canonical_inputs.csv`, `coral_lambda_sensitivity.py:79` |
| A2 | **§3.2 false statement**: pre-label exclusion "none arising in Manavgat or Bejís"; supplement C.1 says not run for Manavgat, no status for Bejís. Introduced 2026-09-14 | R3 | grep, both files |
| A3 | **Collar frames are label-defined and the paper never says so.** 0.541 → 0.616 (abstract) reads as recoverable skill | R2, R3, editor | no statement found in 0*.md / A3 |
| A4 | **Hardening ladder mixes holdout and scoring frame.** Blocked CV scored region-wide; leave-one-scar-out on scar + 2 km (§3 l.167). On a 5 km collar the blocked increment already halves, +0.086 → +0.041 | R2 | `collar_increment_and_cosine.csv` means recomputed |
| A5 | **Graphical abstract left panel shows that ladder** (added 2026-09-19) | follows A4 | — |
| A6 | Ten keys cited in `supplementary_appendices.md` absent from `REFERENCES.bib` (Meyer2021, Meyer2022, Ludwig2023, Mila2022, Wadoux2021, deBruin2022, Yates2018, Schoener1968, Warren2008, Marino2024) | R3 | grep |
| A7 | §4.6 duplicated fragment "The two bearing directly. The two bearing directly…", also typeset; "Three are plotted" names two | all | md l.291, tex l.495 |
| A8 | §4.3 "Contribution 1 is about the paired thermal-minus-baseline difference" (md l.123) | editor, R3 | grep |
| A9 | "eleven limitations" (A2, supplement) vs "all ten" (A3, §5.7) | all | grep |
| A10 | §4.5 "pre-registered protocol" vs §2.4 "not a formal pre-registration" | all | grep |
| A11 | C.5(x) headed "One classifier family" while reporting four estimators | editor | read |
| A12 | Availability section cites §3.14 for the reproduction check; it is §3.13 | R4 | tex labels |
| A13 | No equations anywhere: CORAL, decomposition, bootstrap estimators undocumented (EMS asks for algorithmic foundations) | editor | 0 equation environments |
| A14 | Analysis repository private, no licence; inputs (step8a parquets, drive_new) released nowhere | R4 | `gh repo view`; .gitignore |
| A15 | "Bejis" without accent, twice in §4 | editor, R3 | grep |

## B. Refuted or reframed

- **Editor: C.5(viii) 10/7/3 contradicts 12/6.** Refuted as a contradiction: two different quantities
  (paired-delta verdicts vs above-chance AUC counts; supplement l.660). But C.5(viii) should name its
  quantity (R2 says the same).
- **Editor: PDF swaps Fig. 6 and Fig. 7.** Not reproduced: the tex refers to `fig:loro` for pooling,
  which is `fig6_loro`. Not a defect as far as checked.

## C. Substantive critiques — author decisions, not bookkeeping

1. **Scope for EMS** (editor): reframe §1/§6 around evaluation design for any spatial model moved
   between regions; engage the spatial-validation and transferability literature.
2. **Estimands** (R2, R3): scar + collar AUC answers "which cells burn given fire arrived nearby",
   not a corrected region-wide AUC; "upper bound" language should go.
3. **Prevalence control cannot fail** (R2): a random subsample at matched prevalence leaves AUC
   unchanged in expectation, so −0.000 is guaranteed. Argument is sound; reword as a sanity check.
4. **Label-free frame equalisation** (R2, R3): repeat with a rule that uses no labels.
5. **Edge label noise** (R2, R3): distance-band AUCs with edge cells excluded; burned-fraction threshold.
6. **Nulls as absence** (R2): equivalence tests or an interval on (within − transfer) on matched frames.
7. **Resampling** (R2): dyadic dependence; target-cluster unit excludes zero on the equalised frame.
8. **Thermal block as "dryness"** (R3): effectively two dimensions; non-standard TVDI; no weather.
9. **Length** (editor): about 40 pages main text; present the corrected analysis directly, withdrawn
   claims in one robustness subsection.

## D. Not yet verified here

R4's minor provenance items (bootstrap replicate counts per artefact, the +0.155 lower bound 0.092 vs
0.093, the positives-only sign, the unlocated [−0.028, +0.036] source), R3's burned-cell dilation claim
in `step8a`, and R2's `pool_decomposition` vs `matched_holdout` Manavgat row B (0.597 vs 0.589) —
the last is likely a consequence of A1.

# Requests for Emrehan — prioritised

Consolidated from the drafting session on 2026-07-23. Ordered by how much each blocks the paper.
Items marked **[BLOCKING]** must be done before Results can be written; **[STRENGTHENS]** items make
the new thesis defensible or upgrade a negative result into a constructive one.

The manuscript's thesis has shifted since the last export: it is now the **local-skill / portability
trade-off** — the dynamic pre-fire thermal block is the feature set that gains the most within a
region and loses the most between regions. Several requests below exist to support that framing
specifically. See `POSITIONING.md`.

---

## Tier 1 — blocking

**1. [BLOCKING] Re-upload the complete result archive.** The four `stdt-*.zip` parts I received are
`-1-002`, `-1-006`, `-1-007`, `-1-008`. **Parts 001, 003, 004, 005 are missing.** Because each zip
is an independent subset (not a split volume), roughly half the export is absent. Confirmed
casualties:
- `experiments/evia_2021/step8b/` and `step8e/` are empty directory entries — Evia's within-region
  model comparison report is gone.
- `experiments/evia_2021/validation/labels/burned_landcover_gate.json` — Evia's gate verdict is
  missing.
- `experiments/evia_2021/step8a/step8a_500m_modeling_dataset.parquet` — Evia's dataset is missing,
  which is why the signed-AUC bootstrap I ran covers only three regions.
Please re-upload the full set (or just the missing parts) and confirm nothing else is truncated.

**2. [BLOCKING] Decide and act on Evia.** Evia's AOI (23.12, 38.68, 23.52, 39.08 — only 0.40° × 0.40°)
is essentially the fire scar plus a thin margin: burned rate is **36% over all cells and 67% within
natural vegetation**, against 3.8–7.2% in the other three regions. At that prevalence its PR-AUC and
ROC-AUC are not comparable to the others (`RESULTS_INVENTORY.md` §1.1). Three options — your call,
but I need to know which:
- (a) **Enlarge the Evia AOI substantially** and re-run Step1→Step10 so its prevalence lands in the
  normal range. Strongest outcome; gives a four-region matrix.
- (b) **Drop Evia from the transfer analysis**, keep it only as a within-region replication, and
  state the exclusion reason. Viable; the six-pair interval separation already holds without it.
- (c) If it re-runs but behaves as a different fire regime, we treat it as a second control.
Whichever you pick, please tell me — the manuscript structure branches on it.

---

## Tier 2 — needed to make the new thesis fully defensible

**3. [BLOCKING for one section] Marginal area-of-applicability index per ordered region pair.** The
Introduction (§1.3) and Related Work (§2.3) now commit *in print* to showing that marginal,
predictor-space-distance diagnostics fail to order the transfer outcomes while a conditional
diagnostic succeeds. I have the conditional half (signed-AUC reversals with bootstrap CIs); the
**marginal half is not computed yet**. Please produce, for each ordered pair:
- an area-of-applicability-style dissimilarity index in predictor space (Meyer & Pebesma
  construction: importance-weighted, scaled predictor-space distance of target cells to the source
  training distribution — your RF already yields the importances);
- a simple climatic distance and a geographic (centroid) distance.
The test is whether any of these order the observed transfer AUCs. Our expectation is that they do
not. **If this is not produced, two sentences in §1.3 and §2.3 must be softened** — so this is
effectively blocking for that argument.

**4. [STRENGTHENS] Signed-AUC spatial-block bootstrap for Evia.** Once Evia's parquet arrives
(item 1) I can extend the three-region table in `signed_auc_bootstrap.md` myself — I just need the
parquet. Alternatively you can run `run_c` for Evia in the pipeline; either works. The three-region
result is already strong (four absolute thermal channels sign-flip Manavgat↔Muğla with disjoint
CIs), but the fourth region completes it.

**5. [STRENGTHENS] Pre-fire window-closing sensitivity.** Every region's predictor window closes one
day before its label window opens (Manavgat 07-27 / 07-28, etc.). A reviewer will ask whether early
fire signal — smoke, pre-ignition heat — leaks into the thermal composite. Please re-composite the
thermal predictors with the **final 7 and 14 days of each predictor window excluded**, re-run the
within-region baseline-vs-thermal ΔAUC, and confirm the increment survives. Cheap, and it closes an
obvious line of attack before it opens.

---

## Tier 3 — turns the negative result into a constructive one

**6. [STRENGTHENS] Few-shot recovery curve.** Since the residual gap is concept shift and label-free
alignment provably cannot close it (and, we now see, *degrades* the pair that transfers), the
constructive experiment is: recalibrate the transferred model with a small, **spatially blocked**
sample of target-region labels, and plot how many labelled cells recover a given fraction of the
target's within-region ceiling. This is the strongest candidate for the paper's final figure and is
what upgrades "transfer fails" to "transfer fails, and here is the labelled-cell budget to fix it".

**7. [STRENGTHENS] Decomposition recompute with a negative-recovery convention.** With Muğla in the
set, `recovered = adapted − raw` is **negative** for the pair that transfers (Bejís↔Muğla, where
adaptation *hurts*). The old ~27–31% / ~69–73% split was two-region and assumed adaptation always
helps. Please recompute the decomposition across all directions and adopt an explicit convention for
`adapted < raw` (report the negative sign, or reframe around the regression-toward-chance
observation — my recommendation is the latter; see `RESULTS_INVENTORY.md` §4).

**8. [STRENGTHENS] Disentangle Muğla's special role.** Muğla is the only region participating in a
successful transfer *and* has the largest within-region increment *and* the largest AOI / most cells.
Before the Discussion attributes anything to fire regime, we need to know whether its behaviour is
region-driven or data-volume-driven — e.g. subsample Muğla to Manavgat's cell count and re-check.

**9. [STRENGTHENS] CORAL λ sensitivity for the new pairs.** The existing λ sweep covers only
Manavgat↔Bejís. Please extend it to the Muğla pairs — especially Bejís↔Muğla, the one direction that
transfers — so we can report whether the adaptation behaviour there is λ-robust.

---

## Small confirmations (quick)

- **Environment of the final export:** scikit-learn / pandas / numpy versions and the git commit, so
  the reproducibility statement is exact. (The transfer JSONs I have record commit
  `c648486d823faf1b6d9f39ea84c0dec4e9d7f8c2` — confirm the final export matches or note the diff.)
- **Evia gate verdict and `out_of_window_burndate` count** (both in the missing archive part).
- **ETA on the last region**, and whether the Evia AOI can be enlarged, so I can pick the manuscript
  branch.

---

## What I do NOT need

- Dimarco et al. predictor table — resolved, you read it (no LST/TVDI; ERA5 static climatology).
- Reference verification — all 44 citations are Crossref-verified in `REFERENCES.bib`.
- The three-region signed-AUC bootstrap — done, reproduces your `run_c` CIs to ~0.01
  (`signed_auc_bootstrap.md`).

**Golden rule for anything that will enter the manuscript:** no number goes into the paper from the
current partial export — every figure must come from the final complete run and be re-verified.

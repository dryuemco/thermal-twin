# Inference analyses requested in referee round 5 — report (2026-09-19)

Specification written before any run: `SPEC.md`. Code: `paper/code/ems_inference_{common,ladder,
ladder_stats,units,equivalence,multiplicity}.py`. Inputs via `_canonical.py`. All analyses here are
**post hoc**, added in response to review.

**Reproduction.** Table 1 to printed precision; LOSO matches `scar_increment.json` to 1e-4; row B
matches `matched_holdout.json` to 5e-5; half-split +0.027 with 13 of 18 positive; pair-cluster,
target-cluster and jackknife intervals reproduce. One change: Muğla's collar increment is +0.0875, not
+0.0906 (the published file used the overwritten Muğla parquet), so the collar mean is +0.076, not +0.077.

## 1. Matched hardening ladder (`ladder_*`) — the decline is the scoring frame
Every rung scored on scar + 2 km, 8 scars in 4 regions, thermal-minus-baseline increment:
blocked CV at 5 km **+0.019** (the same predictions scored region-wide: +0.089); leave-one-scar-out
+0.022; foreign region +0.008. **Blocked − LOSO at 5 km (primary) = −0.004**: scar-level t
[−0.060, +0.052], region-clustered CR1 t(3) [−0.092, +0.084], region-cluster bootstrap [−0.064, +0.027].
By the pre-stated rule the decline does not appear on a matched frame. Rescoring the same predictions
on scar cells alone costs +0.071. At 1 km blocking, blocked − LOSO = +0.031, every interval spanning
zero; the only matched contrast excluding zero is blocked (1 km) − foreign, +0.045 (CR1 [+0.008, +0.083]).
On the 10 km collar the ladder is not monotone: blocked +0.076, half-split +0.036, LOSO +0.000
[−0.042, +0.042], cross-region +0.023. **The monotone decline exists only on the frames as drawn.**

## 2. Equivalence (`equivalence.json`) — margins ±0.02 and ±0.05 fixed in SPEC
Equalised transfer increment +0.023: equivalent within ±0.05 under 5 of 7 dependence-aware units
(fails under pigeonhole bootstrap and jackknife), within ±0.02 under none; "no transfer gain larger than
X" holds for X = 0.045 (pair-cluster), 0.030–0.070 across units; the 90 % interval lies wholly above
zero under 6 of 8 units. As-drawn increment +0.004: equivalent within ±0.05 under every defined unit,
within ±0.02 only under target clustering.

Within − transfer on matched frames, 5 km blocking, t(4) over target regions:

| Frame | W − T | 95 % CI | one-sided 95 % lower bound |
|---|---:|---|---:|
| 10 km collar | +0.053 | [+0.004, +0.101] | 0.016 |
| 5 km collar | +0.025 | [−0.001, +0.052] | 0.005 |
| full frame | +0.081 | — | — |

On the scar frame LOSO − foreign = +0.014, CR1 [−0.083, +0.112]. **"Does not travel" holds only in
bounded form and cannot be stated as equivalence at ±0.02.** Accurate: a small positive transfer
increment, bounded near 0.05, smaller than the within-region increment on the 10 km collar.

## 3. Resampling units (`units.json`), 95 % intervals

| Unit | as-drawn Δ +0.004 | equalised Δ +0.023 | equalised mean 0.616 |
|---|---|---|---|
| pair-cluster (paper) | [−0.027, +0.035] | [−0.004, +0.049] | [0.575, 0.658] |
| target-region cluster | [−0.007, +0.018] | **[+0.016, +0.031]** | excludes 0.5 |
| source-region cluster | [−0.014, +0.031] | **[+0.003, +0.052]** | excludes 0.5 |
| pigeonhole two-way bootstrap | [−0.034, +0.045] | [−0.011, +0.060] | excludes 0.5 |
| CGM two-way, t(4) | undefined (V < 0) | **[+0.007, +0.039]** | excludes 0.5 |
| dyadic-robust (Aronow et al. 2015), t(4) | undefined (V < 0) | **[+0.006, +0.040]** | excludes 0.5 |
| LORO jackknife, t(4) | [−0.037, +0.046] | [−0.038, +0.084] | [0.505, 0.728] |

As-drawn Δ spans zero under every unit (dropping Evia flips its sign). The equalised Δ is
unit-dependent: **four of seven units exclude zero, including both formal two-way estimators**; §4.4's
"only under target clustering" understates this. At most five independent units (regions), df ≤ 4.

## 4. Planned versus post-hoc register (git archaeology)
First transfer numbers: repo `f4baf1d`, 2026-07-11. The only preregistration file: repo `bccc258`,
07-13, covering **two directions**, written after the first transfer and first z-score/CORAL results.
No file pre-registers the 20-direction matrix (`d0b20af`, 08-08). Planned before any transfer result:
the Kozan gate, the two feature sets, the RF configuration and the 2-cell within-region protocol. CORAL
became the headline on 07-17 after it beat z-score; the λ sweep, capped at 0.1, was designed after
λ = 1 was known to erase the Bejís→Manavgat result. Every control the central claim rests on
(half-split, LOSO, foreign scar, collars, prevalence, capacity, the pair-cluster/jackknife/target units)
is post hoc, dated 08-14/15. Wording to change: "committed-in-advance CORAL arm" (§4.5) → "specified
before the five-region matrix"; "stated in advance" for the regime hypothesis (§5.4) cannot be dated.

## 5. Multiplicity (`reversal_family_holm.csv`, `diagnostics_bh.csv`)
Collar-frame reversals, 90 difference tests: **Holm 0 of 90** (BH 0); closest lst_anomaly Bejís–Evia,
Holm p 0.050 (normal) / 0.072 (percentile). As drawn, same 90: Holm keeps 11 (normal) or 6
(percentile). Strict criterion as an intersection-union test with Holm: 0 survive on either frame.
Diagnostics, BH over 19: agreement-fraction-supported (ρ +0.84, adjusted p 0.001) and cosine-supported
(+0.81, adjusted p 0.0095) survive; next adjusted p 0.75. Both are post-hoc selections on 16 directions
and dissolve on the collar (already reported).

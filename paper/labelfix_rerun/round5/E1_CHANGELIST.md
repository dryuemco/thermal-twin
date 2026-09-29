# E1: what changes in the text (list only; nothing edited), 2026-09-23

## Scope
Rows 1–119 are the line-by-line inventory in `paper/MANAVGAT_RERUN_PLAN.md` §1. "New" values come from the
official re-freeze or from the 09-19 corrected re-runs, which the official outputs reproduce exactly (round 5).
Sources: `labelfix_rerun/CHANGES.md` §2, `round4/REPORT.md`, `round5/`, `refreeze/_runners/matrix8_official.csv`,
`round5/matrix20_official.csv`.

## Status codes
- **CH**: the number or verdict changes; the new value is given.
- **=**: unchanged, or the Manavgat value moves inside an unchanged range.
- **V**: changes, and the value still has to be read from an existing official output before E2. No new run.
- **R**: needs a run that has not been done.
- **B**: blocked or pending a decision.

## 0. What the current text actually contains (it differs from the E3 premise)
- **Contributions:** the frozen pilot has two (§1.3: C1 evaluation frame; C2 local skill does not travel).
  C3 was withdrawn on 2026-08-16 (commit `0d6abc3`) and there is no C4 section.
- **Abstract** (`00_abstract.md:133`): no conditional-similarity sentence and no contrast-pair sentence.
- **Highlights:** item 4 is the frame equalisation (0.541 → 0.616), not conditional similarity. No highlight is
  C4-based.
- **Where C4 content lives:** §4.4 (04:170–175, the collar dissolves "the diagnostic that best ordered transfer";
  04:217, "the sign-agreement diagnostic" as a frame property), Appendix D and Appendix A(y) (Tables 5 and B1).
  §5.3 has no C4 claim (05:43, "missing conditional information", is about the interventions). §5.4 is the regime
  hypothesis, and §6 has no C4 claim.
- **Consequence for E3:** the removals are §4.4, App D and A(y). Nothing C4-based needs to come out of the
  abstract, highlights, contributions or conclusions. The contrast-pair sentence would be a NEW abstract sentence
  (§E3 draft), not a restored one.

## 1. Headline quantities (abstract, highlights, intro, conclusions)
| # | Printed | New | Status | Where |
|---|---|---|---|---|
| 1 | frame cost 0.143 [+0.077, +0.208] | **0.133 [+0.059, +0.207]** | CH | Abs, HL1, 1.3, 4.3, A(z), 6, GA |
| 2 | +0.155 against −0.000 | **+0.149 against −0.002** | CH | HL2, 4.3, A(i), A(z) |
| 3 | equalised transfer 0.541 → 0.616 | **0.527 → 0.589** | CH | Abs, HL4, 6, 4.4 |
| 4 | +0.045 to +0.148 at 5 km | Man +0.062 inside | = | Abs |
| 5 | +0.06 to +0.15 at 1 km | Man +0.067 inside | = | HL3 |
| 6 | +0.004 [−0.028, +0.036] (step9b, B=20000) | **+0.007 [−0.021, +0.037]** | CH | Abs, HL5, 4.3, 4.5, A(o), A(z), GA |
| 7 | static baseline 0.537 vs 0.541 | **0.519 vs 0.527** | CH | Abs, 4.5, 5.2, 5.5, A(ix), A(f) |
| 8 | "falls 0.155 short"; "withdraws five claims" | **0.197**; the count of withdrawn claims must be re-derived (rows 10–12, 36 change) | CH / V | 1.3, 5.1, 6 |
| 9 | normalised channels "transfer no better than absolute" (A(f)) | from `round3/no_coord_channels.json` | V | 1.2 |
| 10 | "hotter pre-fire surfaces burned less in **every** region" | **false**: Manavgat LST 0.665 full / 0.522 collar; now four of five. "Greenness reverses in two" = | CH (verdict) | 6, 4.4, A(k), A(o), A(w) |
| 11 | "leaves no sign reversal supported between regions" (collar) | **false**: elevation Man 0.376 [0.300, 0.465] vs Muğ 0.606 and Evia 0.648, strict-supported | CH (verdict) | 6, 4.4 |
| 12 | below-chance directions 6 → 1 | **7 → 5** | CH | 6, 4.4 |

## 2. Methods
| # | Printed | New | Status |
|---|---|---|---|
| 13 | pre-label: none in Manavgat | unchanged | = |
| 14 | positive-carrying blocks 192–843 / 16–70 / 6–33 | Man 814 / 47 inside; 20-cell Man count to read | V |
| 15 | λ sweep "at most 0.014" | round 4: max deviation 0.0125 in both arms (not Manavgat) | V (re-derive what 0.014 measured) |
| 16 | "within 1.6×10⁻⁷" | E4 sentence: 1.3×10⁻⁸, same-side disclosure | CH |
| 17 | "two of twenty verdicts not stable across seeds" | seed sweep BSEED 43–46 not re-run on official | **R** |
| new | Label-correction paragraph (stale export, 8 Jul / 11 Jul / 183be42, re-freeze, three-arm reproduction check) | E4 | CH |

## 3. Results §4.1–4.2, Table 1, Fig. 3
| # | Printed | New | Status |
|---|---|---|---|
| 18 | gate 0.723–0.991 | Man 0.955 inside | = |
| 19 | Man block 2: 0.803 / 0.870 / +0.067 [+0.055, +0.079] | **0.841 / 0.908 / +0.067 [+0.060, +0.073]** | CH |
| 20 | Man block 10: 0.748 / 0.797 / +0.050 [+0.023, +0.077] | **0.820 / 0.882 / +0.062 [+0.040, +0.082]** | CH |
| 21 | Man block 20: 0.683 / 0.731 / +0.048 [+0.014, +0.085] | **0.798 / 0.845 / +0.047 [+0.016, +0.081]** | CH |
| 22 | "+0.048 to +0.154" at 10 km | **+0.047 to +0.154**; "excludes zero in all five at 1 and 5 km" = | CH |
| 23 | Fig. 3 | regenerate (E5) | CH |

## 4. Results §4.3, Table 2
| # | Printed | New | Status |
|---|---|---|---|
| 24 | Table 2, 8 scars; A 0.776, B 0.634, C 0.552, D 0.555 | **7 scars in 3 regions** (Manavgat has no row C); A 0.773 [0.729, 0.818], B 0.640 [0.544, 0.736], C 0.546 [0.488, 0.604], D 0.553 [0.495, 0.611] | CH |
| 25 | A−C +0.225; region-clustered A−B +0.155 / A−C +0.251; "2.3 times"; "two thirds" | A−C **+0.227 [+0.147, +0.308]**; A−B **+0.137 [+0.048, +0.226] (G=3)**; A−C **+0.266 [−0.022, +0.553], now spans zero**; **3.6**; 0.586 | CH (verdict) |
| 26 | B−C +0.082; C−D −0.003; "about 0.18" | **+0.094 [−0.012, +0.200]; −0.007 [−0.070, +0.057]; about 0.20** | CH |
| 27 | "eight scars … four in Muğla, two in Montiferru"; "three starved" | **seven scars**; **two of seven starved** | CH |
| 28 | prevalence control 0.782 / 0.782 / 0.627; −0.000; +0.155 | **0.791 / 0.793 / 0.644; −0.002 [−0.005, +0.001]; +0.149 [+0.087, +0.211]** | CH |
| 29 | negatives-only 0.147; positives-only 0.002 | **0.139 [0.098, 0.181]; −0.002 [−0.055, +0.051]**; per-scar range to read | CH / V |
| 30 | half-split +0.027 (13/18) | **+0.028 (13/18)** | CH |
| 31 | LOSO +0.022 [−0.032, +0.077] (6/8) | **+0.024 [−0.040, +0.089] (5/7)** | CH |
| 32 | +0.056 to +0.153; "falls monotonically" | range =; ladder +0.028 / +0.024 / +0.007 still monotone | = |
| 33 | 306–2,802 km | = | = |

## 5. Results §4.4, Table 3
| # | Printed | New | Status |
|---|---|---|---|
| 34 | Man far-field 60.1 %, 13.4 km | **58.5 %, 13.1 km**; range = | CH |
| 35 | Man elevation by band 472 / 955 / 1,273; burned 512 m | **330 / 723 / 995 / 1,273; burned 287 m** | CH |
| 36 | "all five agree in sign on elevation, LST, TVDI" on the collar; "both elevation reversals disappear"; "no reversal supported" | **false on all three**: Manavgat is opposite on all three; its elevation reversal survives the collar and is supported | CH (verdict) |
| 37 | lst_anomaly opposite pairs: four; "nine of ninety" | **three** (Man–Evia −0.097 [−0.210, +0.021] loses support); collar family 9 → 27 differences excluding 0 | CH |
| 38 | supported-in-both features 1.20 → 3.40 per direction | to read from `round3/diagnostics_collar_frame.csv` | V |
| 39 | "crosses 0.5 in Manavgat (0.505)" | **0.454**; the direction of the crossing reverses (collar LST above 0.5, below within distance) | CH |
| 40 | collar diagnostic "1.0 in all eighteen, variance zero"; cosine +0.81 → −0.06 | **not unanimous**: 16 defined directions, values 0 and 1, variance 0.79; cosine **+0.70 → +0.40 (p = 0.12)**. ⚠ Inconsistency: full-frame cosine is +0.698 in `verify_collar_increment` but +0.493 in `all_diagnostics` (the frozen label agreed at +0.805). Resolve before E2/E3 | CH + **check** |
| 41 | collar increment +0.077 vs +0.086; Man +0.041 | **+0.083 vs +0.087; Man +0.073**; 5 km **+0.042 (Man +0.035)**; positive in all five = | CH |
| 42 | Table 3, five rows | full 0.527 · 13 · 7 · 9/6 · +0.007; full/10 0.559 · 14 · 6 · 10/2 · +0.008; 10/full 0.546 · 14 · 6 · 10/5 · +0.014; **10/10 0.589 · 15 · 5 · 13/2 · +0.024**; 5/5 0.591 · 16 · 4 · 11/0 · +0.017 | CH |
| 43 | provenance paragraph ("forty of a hundred values …") | a separate known inaccuracy; rewrite | CH |
| 44 | baseline 0.593 vs 0.616; "six times"; "four times at 5 km"; "four to one"; 9/4 → 15/1 | **0.565 vs 0.589; about three times (3.3); about two (2.3); six to two; 9/6 → 13/2** | CH |
| 45 | equalised Δ +0.023 [−0.004, +0.048]; target cluster excludes 0 | **+0.024 [−0.004, +0.049]**; target cluster **[+0.011, +0.040]** still excludes | CH |
| 46 | matched reference 0.772; shortfall +0.155 [+0.094, +0.217]; 0.25 | **0.786; +0.197 [+0.091, +0.303]; 0.29**; Manavgat is now the largest per-region shortfall (+0.319) | CH |
| 04:214–219 | "Five quantities … are properties of the frames": six → one; elevation/LST/TVDI reversal; sign-agreement diagnostic; same-geography arm; +0.004 vs +0.023 | **paragraph no longer holds**: 7 → 5; the elevation reversal survives the collar for Manavgat; the diagnostic does not dissolve (row 40) | CH (verdict) |

## 6. Results §4.5–4.6
| # | Printed | New | Status |
|---|---|---|---|
| 47 | raw range 0.326–0.686 | **0.314 (Bej→Man) – 0.677 (Evia→Man)** | CH |
| 48 | support 12/6 (2-cell), 9/4/7 (10-cell); "only Man→Bej survives"; "Bej→Man and Man→Muğ lose support" | **11/7; 9/6/5**. Below at 10-cell: Man→Bej, **Bej→Man**, Muğ→Man, Bej→Evia, Evia→Bej, **Mont→Man** | CH (verdict) |
| 49 | target within 0.870; raw deficit 0.184–0.592 | **0.908**; deficit to compute | CH / V |
| 50 | PR 0.156 vs 0.136; six below; "only one exceeds twice" (Evia→Man 2.45) | **0.181 vs 0.157; seven below (all interval-supported); Evia→Man 2.24**; "exception Bej→Man" to check | CH / V |
| 51 | Δ spread −0.148 to +0.133, 12/8; "thirty times the mean" | spread and 12/8 =; mean 0.004 → 0.007, so the multiple falls (re-derive) | CH / V |
| 52 | units [−0.027, +0.034] … ; jackknife; "dropping Evia reverses its sign" | refit units **[−0.023, +0.037] / [−0.028, +0.043] / [−0.018, +0.033]**; LOO **+0.0148 / +0.0050 / +0.0072 / +0.0010 / +0.0087**; Evia flip **false** | CH |
| 53 | z 0.431–0.630, CORAL 0.443–0.624; "fourteen of twenty move closer"; "five of six … Montiferru, sixth Man→Muğ"; "Bej→Man margin 0.001" | **z 0.302–0.630, CORAL 0.406–0.624** (lower endpoints now Bej→Man); **sixteen**; the rest to check | CH / V |
| 54 | CORAL mean 0.552; oracle 0.556 | **0.517; 0.523** | CH |
| 55 | "at most 34 % (Muğ→Man)"; seven negative | **28 % (Bej→Evia)**; seven = | CH |
| 56 | interventions: local −0.081; transfer +0.014 [−0.017, +0.045] | **−0.076**; +0.014 (CI to read). ⚠ The dropped features (elevation, lst_anomaly) were chosen from the FROZEN supported reversals; the set stays fixed by design | CH / V |
| 57 | label budget 85–89 % (three) / 30–57 % / 7–20 % | **83–89 % / 30–52 %**; 7–20 % to check | CH / V |
| 58–61 | Figs. 4–7 | regenerate (E5) | CH |
| 62 | graphical abstract | regenerate after 04 is edited (it parses 04) | CH |

## 7. Discussion and Appendix C.5
| # | Printed | New | Status |
|---|---|---|---|
| 63 | window closure "positive and supported everywhere" (Manavgat included) | **Manavgat window closure not re-run** (decision 2: blocked) | **B** |
| 64 | §5.4 regime: wrong sign; most similar pair fails both ways; most different above chance | all three hold. ρ +0.290 → **+0.109**; the most similar pair is now **Bej–Man** (0.396 / 0.314), not Bej–Evia; the most different is Bej–Muğ (0.618 / 0.583) = | CH (pair name) |
| 65 | §5.4 "subsampling Muğla to Manavgat's cell count **and positive count**" | the positive-count arm is withdrawn (decision 5); cell-count subsampling needs a re-run (possible now without a shim) | **R** + CH |
| 66 | "about 0.14 ROC-AUC" | **about 0.13** | CH |
| 67 | 5 km vs 10 km 0.608 vs 0.616; "−0.00045"; ten pairs | **0.591 vs 0.589 (5 km now higher)**; boundary value to read; ten pairs = | CH / V |
| 68 | C.5(iv) prevalence "0.038 to 0.072 in three of the others" | Man is now 0.143, so the sentence changes | CH |
| 69 | C.5(vii) "Manavgat … remains unexplained …" | **full rewrite (E2)** | CH |
| 70 | C.5(viii) 10/7/3; −0.00045 | **12/7/1**; boundary to read | CH / V |
| 71 | model capacity 0.510–0.556, 14/20 for all four | **0.481–0.527, 11–13 of 20** | CH |

## 8. Appendix B tables
| # | Table | New | Status |
|---|---|---|---|
| 72 | B2 Manavgat column | S4a values (0.564 / 0.232 / 0.400 / 0.509 / 0.665 / 0.677 / 0.460 / 0.683 / 0.666, with 10-cell CIs) | CH |
| 73 | B3 reversals: "three pair-level reversals across two features"; elevation rows | **14 supported** (elevation Man–Bej, Man–Muğ; slope Man–Muğ, Man–Mont; three LST channels Man vs Muğ and Evia; TVDI Man vs Muğ, Evia, Mont; lst_anomaly Bej–Evia); point-only 33 → 26 | CH |
| 74 | B4, 8 Manavgat directions + mean | `matrix8_official.csv` | CH |
| 75 | B6 Manavgat row | **2,935 / 13.1 km / 58.5 %** | CH |
| 76 | B7 Manavgat column | 0.232 / 0.400 / 0.564 / 0.665 / 0.509 / 0.677 / 0.460 / 0.683 / 0.666; straddles column changes | CH |
| 77 | B8 Manavgat row 796 / 0.033 / 784 / 0.038 / 0.984 | **3,046 / 0.126 / 2,935 / 0.143 / 0.955** (read exact values from gate/step8a stats) | CH / V |
| 78 | B9, 8 directions × raw/z/CORAL | `matrix8_official.csv` (A-stage table) | CH |

## 9. Supplement A (rows 79–115)
- **CH, value known:**
  - Rows 81, 82 and 87–91: λ table (Bej→Man 0.408, below chance at every λ); model capacity; Tables A1–A4.
  - Row 93: A(k) Manavgat 0.522 / 0.556 / 0.551 / 0.550 / 0.454.
  - Row 94: A6 0.487 vs 0.584, −0.097 [−0.210, +0.021], loses support.
  - Row 95: LORO Man 0.426, Bej 0.458.
  - Row 100: A(s), see below.
  - Row 102: holds.
  - Row 103: ceiling range 0.777–**0.882**.
  - Row 104: TSG +0.045 to +0.067; all-valid +0.048 to +0.061.
  - Row 105: Bej→Man 0.314 → 0.452.
  - Row 106: gap table 0.814 / 0.527 / 0.287; 0.786 / 0.589 / 0.197; 0.759 / 0.591 / 0.169; per region +0.081 / +0.319 / +0.172 / +0.202 / +0.211.
  - Row 107: 11/7; Evia→Man 0.677 vs 0.908; Man→Bej on the collar is 0.407 and now excludes chance.
  - Row 109: the 2,802 km pair 0.396 / 0.314.
  - Row 113: sweep 0.541–0.561, nine to six.
  - Row 114: ladder.
- **V, to read:** rows 79 (legacy Evia), 85–86 (A(f), A(g)), 92 (Table A5), 96 (feature-drop table), 97–98, 101 (distance bins), 108 (common subset, p, unselected), 110–111 (AoA 0.875 / 0.531, Table B10 ranks), 115.
- **B / R:**
  - Row 80: A(b) λ = 1 on four directions comes from `coral_lambda1.csv`, whose producer is missing. Recompute from `coral_lambda_sensitivity` or withdraw.
  - Row 83: window closure (as row 63).
  - Row 84: QC arm (A(e)/A(v)), whose label-dependent parts were computed on the frozen label; re-run or restate.
- **A(s), row 100 (E2):**
  - "same side 0.561 vs 0.606" → **Man 0.376 vs Muğ 0.606, opposite sides**.
  - "below chance as drawn, above under the collar" → **below on both frames (0.438 / 0.345; 0.493 / 0.433; Muğ→Man collar CI excludes 0.5)**.
  - "weakest Man→Bej 0.417" → 0.407; strongest Muğ→Evia 0.728 =.
  - "five of nine point opposite" → **seven**.
- **Fig. 8, row 112:** D̄ 0.83 → **0.80**; supported set to read; transfer 0.470 / 0.401 → **0.438 / 0.345**; sign agreement **2/9** in the title (E5).

## 10. Supplement S1 (rows 116–119)
- Table S1: new values from ANSWERS.md S3. CH.
- S1.3: "two directions reach only 51 to 57 %" → **39 to 52 %**. The one-block and 32-block selection intervals and "Muğ→Man below 0.5 after 8 blocks" are to read. CH / V.
- S1.4: ceiling 0.777–**0.882** vs within 0.859–0.918; block counts to read; validator PASS and 3,642 fits =.

## 11. New findings to add (S4–S7)
| Finding | Where it goes | Framing |
|---|---|---|
| S4a: Manavgat's outlier status sharpens. Elevation 0.232; four LST/TVDI channels 0.67–0.68, interval-supported and opposite to all other regions. Worst target (0.435), no longer worst source | Results (new paragraph), B2 | result |
| S4a: within-region Manavgat strengthens (CIs narrow; block 10 +0.062) | Results §4.2 | result |
| S4b: the Manavgat-target collapse concentrates in the first four days. Early-phase cells are low (219 m) and hot. Elevation and temperature cannot be separated | Results (short, flagged exploratory), Discussion, Limitations | mechanism proposal, one region, one event |
| S5: paired Δ 10/7/3 → 12/7/1, mean +0.004 → +0.007; Evia→Man turns negative; 10-cell 6/5/9 | §4.5, A(c), C.5(viii) | result |
| S6: no interpretable diagnostic excludes zero (0 of 19); C4 loses support; vector_spearman_supported flagged in Table B1 (6 directions, degenerate, not interpreted); one text sentence | App D, A(y), Table B1, §4.4 | result |
| S7: contrast pair holds; niche ranks 1 / 10 on all five measures; Man–Muğ sign agreement 2/9 | App D, A(s), Fig. 8, possibly the abstract (E3) | ordinal, point-estimate |

## 12. Before E2: open items needing a decision or run
1. **Row 40 inconsistency:** two computations of the full-frame supported-feature cosine disagree under the
   corrected label (+0.698 vs +0.493) but agreed when frozen. Find the cause first.
2. **Rows 63 and 83, window closure:** blocked. The text can say Manavgat's window closure was not re-run on the
   corrected label, or it can wait.
3. **Row 65, Muğla subsampling:** a re-run is possible now without a shim (stage A built the folder).
4. **Row 17, seed stability:** the BSEED 43–46 sweep on the official outputs is not run.
5. **Row 80:** A(b) λ = 1 has no producer script; recompute or withdraw.
6. **Row 84, QC arm:** the label-dependent parts are frozen-label only.
7. **"V" rows:** values still to read (about 30); every one is from an existing official output, and no new
   model is needed.

---

## 13. Update after round 6 (2026-09-23): the seven open points are resolved

This section supersedes the V / R / B statuses above. Every "new" value is read from an official output.
Where a frozen recomputation was possible, it reproduces the printed value, which confirms that the
definition used here is the one the text used.

### Open points
| # | Item | Result |
|---|---|---|
| 1 | **Cosine inconsistency** (row 40) | **Resolved.** See §1 below. |
| 2 | **Window closure** (rows 63, 83) | **Run; the claim is verified.** See §2. |
| 3 | **Muğla subsampling** (row 65) | **Run.** See §3. |
| 4 | **Seed stability, BSEED 42–46** (rows 17, 67, 70, 82) | **Run.** See §4. |
| 5 | **A(b) λ = 1** (row 80) | **Withdrawn** (`paper/coral_lambda1_WITHDRAWN.md`). A(b) is limited to the λ ≤ 0.1 sweep. |
| 6 | **QC arm** (row 84) | **Re-run on the corrected label.** See §6. |
| 7 | **V rows** | Read; see the table below. |

#### §1. Cosine inconsistency
- **What agrees.** Both codes compute identical signed AUCs (to 5.6e-17).
- **What differs.** One knife-edge support flag: Manavgat ndvi_mean (AUC 0.564).
  - verify_collar_increment's own bootstrap gives [0.5022, 0.6237] and counts it as supported.
  - The pipeline's Step9G gives [0.4993, 0.6278] and does not.
  - That single flag changes the supported set in 8 Manavgat directions and moves ρ from 0.493 to 0.698.
- **Which is correct.** Step9G: it is the source of Table B2 and of the registered 20-measure table.
- **The fix.**
  - paper/code/verify_collar_increment.py now takes its full-frame support flags from Step9G.
  - The collar side keeps its own bootstrap, because there is no Step9G collar run.
- **After the fix.**
  - The full-frame ρ is +0.4935, equal to the table.
  - The control arm still reproduces canonical_rerun exactly.
  - Only the full-frame cosine row moved.
- **Fragility note.** Five to six Step9G CI bounds lie within 0.01 of 0.5 under both labels. The
  supported-feature measures are therefore sensitive to Monte Carlo noise by construction.

#### §2. Window closure
- **One-line module patch.** historical_burn_excluded is added to STEP8A_POPULATION_COLUMNS (diff in
  refreeze/_runners/patches/).
- **G1.** The control arm reproduces the drive_new compare tables to ≤ 1e-16, so the patch introduces no
  drift.
- **Manavgat on the corrected label** (thermal ΔROC, all bootstrap-supported increases):
  - canonical: +0.066 [+0.059, +0.072]
  - 7 days earlier: +0.082 [+0.075, +0.090]
  - 14 days earlier: +0.058 [+0.051, +0.065]
- **Result.** "Positive and supported everywhere" holds for five of five regions.

#### §3. Muğla subsampling
- **Checks.** G1: control = drive_new to ≤ 1.1e-16. Validator PASS; L5 was skipped because it runs only
  with --deep.
- **What holds.** The within-Muğla arm does not depend on Manavgat and is unchanged (thermal 0.760). So
  "subsampling Muğla to Manavgat's cell count leaves it inside the range" still holds.
- **What goes.** The "and positive count" clause, because that arm is withdrawn (decision 5).
- **What moves.** Muğ→Man subsampled thermal goes from 0.395 to 0.330.

#### §4. Seed stability, BSEED 42–46
- **Frozen label.** The control arm reproduces the published sweep exactly. Its unstable verdicts are:
  - 10-cell level: Evia→Bej
  - 10-cell Δ: Man→Muğ and Evia→Mont
  - 2-cell Δ: Bej→Man
- **Corrected label.**
  - The 2-cell level and 2-cell Δ verdicts are stable across all five seeds. The Bej→Man 2-cell Δ is no
    longer borderline: its lower bound is now +0.0065.
  - 10-cell level: Evia→Bej only.
  - 10-cell Δ: Man→Muğ and Evia→Mont.
- **Consequence.** The "−0.00045" split disappears, and 12/7/1 is seed-stable.

#### §6. QC arm
- **Arm B input.** The pipeline's own prepare_modis_for_step7 --export regenerated the screened MODIS (EE
  project thermaltwin). It is pixel-identical to the 2026-08-14 screened raster.
- **Signed AUCs, A → B.**
  - elevation: 0.232 → 0.232 (+0.0000)
  - every other feature: ±0.0000, except downscaled LST 0.683 → 0.679 (−0.0044)
- **Within-region increment.** A +0.067 [+0.061, +0.073] → B +0.068 [+0.062, +0.074].
- **Result.** The elevation-artefact candidate stays closed. "No signed AUC moves by more than +0.0003"
  becomes "none by more than 0.005, and that one is downscaled LST".
- **Design note.**
  - Repo HEAD's step7B refuses the unscreened MODIS: the raster has no nodata tag and 8.1 % exact zeros
    (guard 4745230, 2026-07-23).
  - Arm A is therefore the frozen step7 (export-time code) plus step8 on the corrected label; arm B is the
    HEAD step7.
  - The 2026-08-14 arm A was almost certainly the same: its step7 hit the same guard, and its signed AUCs
    equal the frozen ones.
  - Its description "both arms rebuilt" was therefore inaccurate, and the code-version confound was present
    then too.

### V rows now read
| # | Printed | New | Note |
|---|---|---|---|
| 8 | "withdraws five claims" | re-derive in E2 from rows 10–12, 36 and 04:214–219 | text |
| 9 | normalised transfers no better than absolute | holds: −0.0063 (was −0.0037); 11/20 (was 12/20) | = |
| 14 | block counts 192–843 / 16–70 / 6–33 | Man 814 / 47 / 17, all inside | = |
| 15 | λ sweep "at most 0.014 … 0.008" | 0.0139 (Muğ→Bej baseline, non-Man), unchanged; 4-direction mean range ≤ 0.005 | = |
| 29 | "per scar −0.12 to +0.12" | not in the current text | drop |
| 38 | supported-in-both "rise from 1.20 to 3.40" | **2.5 → 2.2: now falls**. Frozen recompute gives 1.4 → 3.4; match the aggregation in E2 | CH (verdict) |
| 49 | within 0.870; deficit 0.184–0.592 | **0.908; 0.231 (Evia→Man) – 0.594 (Bej→Man)** | CH |
| 50 | 6 below no-skill (5 with intervals); exception Bej→Man; one above 2× (Evia→Man 2.45) | **7 below, all with intervals; no exception.** Bej→Man PR 0.098 [0.090, 0.105] vs no-skill 0.143. Evia→Man is still the only one above 2× (2.24) | CH |
| 51 | "thirty times the mean" (max \|Δ\| / mean = 0.148 / 0.0042 ≈ 35) | **about twenty times** (0.148 / 0.0073) | CH |
| 53 | "five of six … Montiferru"; margin 0.001 | not in the current text; ranges as in row 53 | drop |
| 56 | "[−0.017, +0.045]" | not in the current text; local −0.076, transfer +0.014 | CH |
| 57 | 7–20 % of target population | 6.6–19.5 %, still "7 to 20 %" | = |
| 77 | B8: 796 / 0.033 / 784 / 0.038 / 0.984 | **3,046 / 0.126 / 2,935 / 0.143 / 0.955** | CH |
| 79 | A(a) legacy Evia: "up to 0.07, no side changes" | **up to 0.13** (Evia→Man 0.677 vs legacy 0.543); still no side change | CH |
| 85 | A(f) table: 0.5371 / 0.5442 / 0.5479 / 0.5414; 16 / 15 / 13 / 14; within 0.7896 … 0.8883; −0.0037, 12/20, −0.099 to +0.094 | **0.5194 / 0.5245 / 0.5308 / 0.5267; 13 / 14 / 13 / 13; within 0.7973 … 0.8959; −0.0063, 11/20, −0.099 to +0.087** | CH |
| 86 | A(g) Man +0.067 / +0.063 / 94 %; mean +0.099 / +0.091 / 92 %; 82–103 % | **Man +0.067 / +0.064 / 95 %**; mean and range unchanged | CH (Man) |
| 92 | Table A5, 6 Manavgat directions | official four_aoi_decomposition.csv (= 09-19 corrected; e.g. Bej→Man recovered +0.26 → +0.15; max recovered 28 %, Bej→Evia) | CH |
| 96 | A(n) per-region within cost, Man −0.060; configuration table | **Man −0.035**, others unchanged; configurations 0.896 / 0.840 / 0.883 / 0.820 and 0.527 / 0.533 / 0.529 / 0.541 | CH |
| 97 | Bej→Man PR 0.034 [0.029, 0.042] vs 0.038; Evia→Man 0.094 vs 0.038 | **0.098 [0.090, 0.105] vs 0.143; Evia→Man 0.321 [0.295, 0.351] vs 0.143** | CH |
| 98 | "ρ = +0.86 over fourteen … +0.84 over sixteen" | C4 content, rewritten in E3 (S6 table) | E3 |
| 101 | A(t) bins 0.692 / 0.519 / 0.499 / 0.445 / 0.541 / 0.421 | **0.709 / 0.570 / 0.519 / 0.499 / 0.541 / 0.421**; the decline with distance weakens | CH |
| 108 | App D permutation p 0.0060, ceiling +0.861, common subset +0.87 / +0.85 | C4 content, rewritten in E3; common-subset agree_fraction_supported +0.870 → **+0.410** | E3 |
| 110 | Man→Muğ 0.875 inside AoA | 0.876 | = |
| 111 | B10 AoA 0.875 / 0.531 | 0.876 / 0.531; transfer and D̄ as in S7 | CH (transfer, D̄) |
| 112 | Fig. 8 supported set {NDVI, elevation} | **{elevation, slope, current LST, current TVDI, downscaled LST, fused LST}** (6); D̄ 0.80; agreement 2/9 | CH |
| 115 | A(aa): −0.081, +0.014, 85–89 %, 30–57 %, 7–20 % | **−0.076, +0.014, 83–89 %, 30–52 %, 7–20 %** | CH |
| 117 | S1.3: Bej→Man [0.392, 0.484] at 1 block, [0.733, 0.748] at 32; Muğ→Man below 0.5 after 8 blocks | **[0.353, 0.582] at 1; [0.815, 0.824] at 32.** Muğ→Man at 8 blocks is 0.437 [0.420, 0.480], so the claim holds | CH |
| 118 | S1.4 "Manavgat 26 and 28" blocks | **36 and 47** | CH |

### Still for E2/E3 (text only; no run is outstanding)
- Rows 8, 36 and 38, and 04:214–219: the "frame property" narrative has to be rebuilt.
- App D / A(y) C4 passages: supplementary_appendices.md lines 1060–1085, 1400, 1473, 1515–1526 and 1606.
- The A(e)/A(v) QC wording, including the correction to the arm-A description.
- A(b), to be limited to λ ≤ 0.1.

## 14. Queued during E5 (2026-09-23), to apply after E5
- **05 Discussion, adaptation narrative.** Bejís→Manavgat moves further from chance under z-scoring
  (raw 0.314 → z 0.302), so "adaptation compresses toward chance" is no longer absolute. Scan 05 for
  that framing (§5.6 "regressing the matrix onto it", and any "compresses") and add the Manavgat
  exception. The Fig. 4 caption already carries it.
- **Supplement:** line ~973 "…0.686 (Fig. 4)" is the frozen raw range; it is now 0.314–0.677.
- **E1 omission, found in E5 (Fig. 6 assert): LORO was not checked per target.** Row 96 updated A(n)
  for Manavgat's within-region cost only. On the corrected label the pooled model beats the best
  single source for Evia, 0.715 [0.668, 0.757] against 0.654 (Manavgat), so "pooling never beats the
  best single source for any target" was false in 04 §4.6, 05 §5.3, the Fig. 6 caption and A(n)(a).
  All four were corrected in one commit. The other LORO numbers were re-read at the same time:
  Manavgat 0.426 [0.369, 0.486], now the target whose interval lies below chance; Bejís 0.458
  [0.396, 0.522]; shortfalls 0.09 to 0.25; ceiling gaps 0.20 to 0.48.
- **Scan for other per-target universals** ("for any target", "every target", "no target", "all
  targets", "never beats") in 00, 01, 04, 05, 06, A2, A3, the supplement, S1, the highlights and the
  captions. The only other hit, supplement l. 1302 ("every target positive lies outside the source
  training population"), concerns the Muğla two-event arm and is label-independent.
- **Re-run exception (corresponding author, 2026-09-23): the frame-transfer matrix.**
  `regen_transfer_ci.py` and `frozen_mugla_verify_aoi_transfer.py` were re-run unchanged into
  `round5/collar/`, so that every number printed in this round traces to round5. The criterion was
  3 dp identical and |Δ| < 1e-5. Both pass; the largest difference is 1.9e-6, from RF n_jobs=4
  thread nondeterminism, shown by two runs in the same environment. The 09-19 `frozen_mugla` file
  is a renamed copy of regen's output. Table B10 and A(s) are rebuilt from round5 and asserted in
  `fig8_contrast_pairs.py`.
- **Appendix tables B1–B10 and A1–A6 rebuilt from source (2026-09-23).** `paper/code/appendix_tables.py`
  builds every row from a source file; 49 corrected sources are pinned in
  `round5/tables/SOURCES.sha256`; `check_all.py` runs the check. The `--frozen` mode built each table
  from the frozen sources and reproduced the frozen text, which validates the method. It also exposed
  these **pre-existing errors, independent of the label**:
  - B4: Bejís→Muğla ROC 0.619 (source 0.6185) and Montiferru→Manavgat PR 0.043 (source 0.0425).
  - A2: Muğla component 10 AUC 0.616 (source 0.6167).
  - A4: the source stores 4 dp, so the frozen 3 dp table could not be reproduced unambiguously
    (double rounding in two cells). A4 is now printed at 4 dp.
  - B3 note: "twenty-nine" point-only pairs where the frozen data give 33 (found in the B1–B3 step).
  - B1: the six n = 12 rows' intervals came from an earlier bootstrap run (found in the B1–B3 step).

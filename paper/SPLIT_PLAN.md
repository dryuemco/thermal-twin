# Split plan: one 50k-word manuscript into two papers

Decided 2026-08-14 by YEC. The manuscript reached 50,462 words, 22 main tables and 8 figures against
an *Ecological Informatics* norm of 9 to 11k words. Rather than delete the excess, it is split, and
the cut falls almost exactly along the seam between the transfer science and the observational layer.

**Nothing is deleted.** Everything leaving Paper 1 either moves to Paper 2 or stays in `paper/` as a
supporting report published with the repository. The full pre-split text remains in git history at
the commit before the cut.

---

## Paper 1: the transfer result

**Target 9 to 10k words, 6 tables, 5 figures.** Three findings carry it, chosen by YEC:

1. **The trade-off, measured per direction.** The pre-fire thermal block adds +0.056 to +0.153
   ROC-AUC inside every one of five regions and +0.004 across twenty ordered directions with an
   interval spanning zero, with an unstable sign. Dropping the two reversing predictors costs −0.081
   of within-region skill, supported in every region, and buys +0.014 of transfer whose interval
   spans zero: the debit is measured and the credit is not.
2. **Marginal diagnostics do not order transfer; a conditional one does.** Twenty candidate
   diagnostics; only two have bootstrap intervals excluding zero and both are conditional, the
   stronger being sign agreement at ρ = +0.84 [+0.58, +0.88]. The marginal, area-of-applicability
   family is the only one runnable before deployment, and it is the one that fails. Reported with its
   own limit: exact permutation p = 0.0060 against a Bonferroni threshold of 0.0026 on eight pairs.
3. **The failure is conditional, and the mechanism is a sign reversal.** Predictors reverse the
   direction of their association with burning between regions, and the reversal persists inside a
   single study area across two fires with disjoint bootstrap intervals.

Supporting, not leading: label-free adaptation (CORAL and z-score) compressing the matrix toward
chance in fourteen of twenty directions, and the recovery curve pricing the failure in target labels.

### Kept in Paper 1

| Section | Keep | Words now | Target |
|---|---|---:|---:|
| Abstract | rewritten to three findings | 337 | 250 |
| Introduction | three contributions, not six | 2,966 | 1,200 |
| Related work | AoA / transferability / fire transfer only | 5,246 | 1,200 |
| Methods | regions, cell, populations, model, spatial CV, transfer variants, diagnostic families, bootstrap | 15,407 | 2,500 |
| Results | 4.1 (compressed), 4.2, 4.3, 4.4, 4.5, 4.6, 4.8, 4.10 | 14,841 | 3,200 |
| Discussion | the three findings, the practitioner answer, limitations that bear on them | 9,372 | 1,500 |
| Conclusions | unchanged in substance | 610 | 350 |

Tables kept: study regions; within-region increment with block sizes; the 20-direction transfer
matrix; the diagnostic rank-correlation table; the contrast pair; the transfer-gap decomposition.
Figures kept: study map, within-region robustness, transfer matrix, adaptation, contrast pairs.

---

## Paper 2: the preprocessing budget

**Working title.** *How much of a satellite fire-susceptibility result is decided before the model is
fitted? A preprocessing uncertainty budget across five Mediterranean regions.*

**Framing.** Not an audit of one pipeline, which a referee would dismiss as our own bugs, but a
protocol: eight preprocessing decisions that must be reported, and how much each moves the answer.
Every item below is measured on five regions with the same data and the same model, which is what
makes it a budget rather than a list of caveats.

### Material moving out of Paper 1

| Item | Now in | Evidence |
|---|---|---|
| TVDI edges are a function of the AOI's sea fraction; the common-edge index does not remove the reversal | §3.4, §4.7k, §5.2 | `tvdi_land_refit.md` |
| Landsat compositing: the intervention's benefit scales with WRS path overlap and replicates in one of three regions tested | §4.7i, §5.11(xi) | `compositing_second_region.md` |
| MODIS QC provenance splits by export date, and the induced change correlates with elevation at +0.615 in Manavgat | §3.4, §5.11(xiii) | `modis_qc_probe.json`, `modis_qc_structure.json` |
| Zero-fill encodes sea as 0.0 °C, 8.1 % to 38.3 % of pixels | §3.4, §5.11(xiii) | `observational_sensitivities.md` |
| The analysis cell is not square and is 17 to 20 % smaller than a MODIS cell; blocking is weaker in longitude | §3.2, §5.11(iv) | measured in `03_methods` |
| Label omission tested against an independent fire observation | §5.11(xiv) | `label_omission_control.md` |
| Gap-filled thermal cells; the increment without the two coordinate-bearing channels | §4.7h, §4.7m | `observational_sensitivities.md` |
| Library-version tolerance of ±0.02 to 0.03, and a bit-identical rebuild on a different operating system | §3.13, §4.7e | `sklearn_version_sensitivity.md` |
| Population size and positive count, matched | §4.7j | `mugla_positive_matched.md` |
| Blocking scale: which verdicts survive 1, 5 and 10 km | §4.7g | `transfer_ci_blocksize.md` |

### Staying in `paper/` as published supporting reports

The remaining analysis reports stay where they are and are published with the repository: the
diagnostic-versus-transfer correlations, niche overlap, LORO pooling, conditional similarity,
regime structure, the referee-round number checks, and the Muğla calendar-arm impossibility.

---

## Order of work

1. Branch the pre-split state so the full text is recoverable by name, not only by commit hash.
2. Build Paper 2's skeleton and move the material into it, section by section, with its tables.
3. Cut Paper 1 to target, section by section, verifying after each that every number still traces.
4. Rebuild and recompile both.
5. Re-run `check_numbers` against the pre-split text to prove nothing was silently altered on the
   way out, as opposed to deliberately removed.

# Positioning — where this paper should aim

**Status:** direction document. Written 2026-07-23, before the final Evia results. It fixes the
**thesis, the contribution ranking and the target framing**; the section structure will be rebuilt
in `OUTLINE.md` once Evia is resolved. Results and Discussion remain unwritten.

---

## 1. The problem with the current framing

The paper as currently outlined leads with *"pre-fire thermal dryness improves burned-area
discrimination"*. That finding is solid, replicated and well-validated — and it is the least novel
thing in the dataset. Comparable results exist for the same provinces (Iban and Sekertekin, 2022;
Alkan Akıncı and Akıncı, 2023) and the broader claim that thermal/dryness indicators inform fire
prediction is established (Maffei et al., 2018, 2021; Gelabert et al., 2025). Led with, it invites
the reviewer question we cannot answer well: *what is new here?*

Meanwhile the genuinely new material — that this same signal does not travel, that similarity does
not save it, and that label-free alignment actively damages the one case where it does travel — is
currently distributed across Sections 4.3–4.8 as a sequence of secondary results.

**The fix is not to add material. It is to change which finding is the thesis and which is the
evidence.**

---

## 2. The thesis

> **Adding dynamic state predictors buys local skill at the cost of portability, and this loss is
> invisible to the marginal, predictor-space-distance diagnostics the field currently relies on,
> because the failure is conditional rather than marginal.**

Stated for the fire application: the pre-fire thermal block is simultaneously the feature set that
contributes the most within-region skill and the one that destroys the most cross-region skill. The
relationship between thermal dryness and burning is *locally reparameterised* — it exists everywhere
and points in different directions in different places.

Three properties make this the right thesis.

**It is general.** It is a claim about predictor classes in environmental machine learning, not
about Mediterranean fire. Fire is the demonstration. That is what lifts the paper above a case
study.

**It is exactly what our data show, and only what they show.** We are not claiming thermal
predictors are useless, nor that transfer never works. We are claiming a trade-off, and we have the
paired static-versus-dynamic contrast to quantify it per direction.

**It engages the field's two live positions simultaneously.** Dimarco et al. (2026) transfer
spatially stationary predictors successfully; Meyer and Pebesma (2021) and Ludwig et al. (2023)
diagnose transferability through dissimilarity in predictor space. Our thesis explains the first and
identifies a blind spot in the second. Neither is contradicted carelessly; both are extended.

---

## 3. The sharpest single claim in the paper

Of everything available, this is the one with the highest novelty-to-risk ratio, and it should carry
the abstract:

> **The feature block that gains the most within region is the block that loses the most between
> regions.**

**Amended 2026-08-13 (referee round).** This sentence was retired from the manuscript. It is a
comparative claim, and no other block's portability was measured on the same footing, so it was
never tested. What the five-region data support is that the block buys +0.056 to +0.153 within every
region, contributes +0.004 on average across the twenty ordered directions, and has a sign-unstable
contribution that is a property of the source-target pair rather than of the block. The abstract,
Introduction §1 and §1.5, Related work §2.5 and Conclusions were rewritten accordingly. The
trade-off framing in Section 2 above is unchanged and remains the thesis. Note also that the single
sharpest bootstrap-supported reversal belongs to elevation, a static predictor, so the manuscript now
states in §1.3 that the thermal block is where the trade-off is costly rather than where instability
is worst.

We can show this directly, per direction, from numbers already in hand: in the Manavgat–Muğla pair
the static baseline transfers at roughly chance and adding the thermal block pushes it *below*
chance, while in the Bejís–Muğla pair the thermal block is what lifts transfer above chance. The
thermal block is the swing factor in both directions — it is where both the local gain and the
transfer failure live.

This single sentence unifies what are currently four separate findings, and it is the reason the
within-region result belongs in the paper: not as the headline, but as the *first half of a
trade-off*.

---

## 4. Contribution ranking (new)

| # | Contribution | Novelty | Role |
|---|---|---|---|
| **C1** | The local-skill / portability trade-off, quantified by a paired static-versus-dynamic transfer contrast across all ordered region pairs | **Highest** | Thesis |
| **C2** | Unsupervised alignment (region-wise z-score, CORAL) does not recover transfer — it compresses every direction toward chance and *degrades* the one pair that transfers | **Highest** | First application of covariance alignment to fire models; a negative result with a mechanism |
| **C3** | Geographic and bioclimatic similarity are not sufficient for transfer, demonstrated with bootstrap intervals disjoint from chance on both directions of two contrasting pairs | High in fire | Refutes the operational rule of thumb; aligns with SDM findings, contradicts the fire literature |
| **C4** | A conditional transferability diagnostic — signed univariate association reversal, plus label-free adaptation performance as an operational instrument for splitting recoverable from irreducible shift | High | The constructive contribution; what makes this more than a negative result |
| **C5** | Within-region replication of the thermal increment across regions, robust to block size, with spatial-block bootstrap intervals | Low | Evidence for the first half of C1 |

**Demoted or cut:**

- The *"self-calibrating satellite thermal digital twin"* framing. It is the project's motivation,
  not a result. One sentence in the Introduction, one paragraph in future work. It must not appear
  in the title or abstract — the paper demonstrates the opposite of self-calibration working.
- The `~27–31 % covariate / ~69–73 % concept` split as a headline number. It was derived from two
  regions in which adaptation always helped; with Muğla in the set, recovery is negative for the
  working pair. Report it as a per-direction quantity with its sign, inside C2's regression-toward-
  chance framing, not as a global constant.
- Kozan 2023 negative control → supplementary material.
- Block-size robustness → supporting subsection under C5, not its own headline.

---

## 5. The one experiment that makes the thesis defensible

The claim *"transfer failure is invisible to predictor-space-distance diagnostics"* is currently an
assertion. To make it a result we must **compute the diagnostic and show it fails**:

1. For each ordered region pair, compute an area-of-applicability-style dissimilarity index in
   predictor space (the Meyer–Pebesma construction: distances in scaled, importance-weighted
   predictor space between target cells and the source training distribution), plus a simple
   climatic distance and a geographic distance.
2. Show whether these indices order the observed transfer performance. Our expectation, from the
   pattern already visible, is that they do not.
3. Then show that the **conditional** diagnostic — signed univariate association reversal between
   source and target — does track it.

That sequence converts the paper's critique into a constructive methodological claim: *marginal
dissimilarity is the wrong instrument for this failure mode; here is one that works.* Without step
3 the paper is a complaint; with it, the paper offers a tool.

**This is the highest-value remaining analysis and should be prioritised over anything else.**

`[TEXT DEPENDENCY — track this]` Section 2.3 of `02_related_work.md` and Section 1.3 of
`01_introduction.md` already commit to this analysis in print. Two sentences in particular are
forward references that the analysis must redeem: that the failure mode we document *is* conditional,
and that a model may sit well inside its nominal area of applicability and still perform at or below
chance. **If the predictor-space dissimilarity index is not computed, both passages must be softened
to conditional phrasing before submission.** Do not leave them standing on an unperformed analysis.

**Partial credit already in hand.** The conditional half of the diagnostic is further along than
this section assumes. Signed univariate association directions are available for all four regions
from the `step9e` outputs, and counting how many predictors fall on the same side of 0.5 in each
region pair already separates the transferring pair from the non-transferring ones, in the order
that geographic and bioclimatic similarity get wrong (see `RESULTS_INVENTORY.md` §5b.1). What is
still missing is the marginal side — the AoA-style index — and spatial-block bootstrap intervals on
the signed AUCs in all four regions, without which no reversal may be called bootstrap-supported.

---

## 6. Supporting analyses still required

Ordered by priority.

1. **Predictor-space / climatic distance versus transfer** — Section 5 above. Blocking for the
   thesis.
2. **Resolve Evia.** See the decision branches in Section 8.
3. **Pre-fire window-closing sensitivity.** Every region's predictor window closes one day before
   its label window opens. A reviewer will ask whether early fire signal contaminates the thermal
   composite. Re-run with the final 7 and 14 days of the predictor window excluded and show the
   within-region increment survives. Cheap, and it closes an obvious line of attack pre-emptively.
4. **Few-shot recovery curve.** How many spatially blocked target labels are needed to recover a
   given fraction of the target's within-region ceiling? This is what turns C2 from a negative
   finding into an actionable one, and it follows directly from the concept-shift diagnosis. Strong
   candidate for the paper's final figure.
5. **Concept-shift mechanism at n > 2.** Read the `step9e` direction-flip outputs for all pairs.
   At two regions only elevation's reversal was bootstrap-supported; with three or four the
   LST/TVDI reversals may become statistically established, which would substantially strengthen C4.
6. **Muğla-specific check.** Muğla is the only region participating in successful transfer and also
   has the largest within-region increment. Establish whether this reflects the region or its data
   volume (largest AOI, most cells) before the Discussion attributes it to fire regime.

---

## 7. Framing details

**Working title candidates** (thesis-first, not application-first):

- *Local skill, poor portability: dynamic pre-fire thermal predictors improve burned-area
  discrimination within regions but do not transfer between them*
- *The transferability cost of dynamic predictors in fire susceptibility modelling*
- *Marginal diagnostics miss conditional failures: cross-region transfer of pre-fire thermal
  dryness in Mediterranean wildfire regions*

The third is the highest-novelty framing and the most demanding to defend; it becomes available only
if the analysis in Section 5 is completed.

**Abstract skeleton** (no numbers until Results close): context — susceptibility models are rarely
tested outside their training region, and dynamic pre-fire state is under-used; what we did — N
Mediterranean regions, spatially blocked validation, all ordered transfer pairs, label-free
adaptation; finding 1 — the thermal block adds robust within-region skill, replicated; finding 2 —
the same block is where transfer skill is lost, and naive transfer falls to or below chance;
finding 3 — similarity does not save it; finding 4 — label-free alignment does not recover it and
degrades the case that works; finding 5 — the failure is conditional, invisible to marginal
distance diagnostics, and detectable by a reversal test; implication — transferability must be
measured, and dynamic-state models need target labels rather than better unsupervised alignment.

**Journal fit.** *Ecological Informatics* remains the right primary target: it publishes
methodological transferability work and the AoA literature is familiar to its readership. Two
genuine alternatives worth holding in reserve — *Environmental Modelling & Software*, which fits the
diagnostic-protocol framing and the AoA critique particularly well, and *Remote Sensing of
Environment*, which would require Evia resolved plus the few-shot curve to clear its bar.

---

## 8. Decision branches once Evia lands

**Branch A — Evia AOI enlarged and re-run cleanly (prevalence in the normal range, gate passes).**
Four regions, twelve ordered pairs, full transfer matrix. The strongest version. C1 and C3 gain a
second independent similar-versus-dissimilar contrast. Proceed with the third title candidate.

**Branch B — Evia remains unusable and is excluded from transfer.** Three regions, six ordered
pairs. Still viable, and the C3 interval separation already holds on those six. Report Evia's
within-region replication and state plainly why it is excluded from the transfer analysis — a
documented exclusion for a stated methodological reason reads as rigour, not as weakness. Use the
first or second title candidate.

**Branch C — Evia re-runs but behaves as a different fire regime (gate marginal, or transfer
patterns incoherent).** Treat it as a second control alongside Kozan and discuss regime typology
(Archibald et al., 2013) as a candidate explanation for concept shift. This is the most interesting
failure mode and would strengthen the Discussion.

In all three branches the thesis in Section 2, the contribution ranking in Section 4 and the
required analysis in Section 5 stay unchanged. **Evia changes the evidence base, not the argument.**

---

## 9. Standing constraints

Unchanged from the project's rules and reaffirmed here: no result number enters the manuscript
except from the final complete export; no citation is invented; every claim is stated at the
strength its interval supports; the transfer failure is reported as a primary finding, not buried in
limitations; and the digital-twin framing stays in future work until something actually
self-calibrates.

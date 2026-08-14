# 5. Discussion

## 5.1 The budget assembled

Eight axes, measured on one cohort with everything else fixed, do not carry equal weight. Ordering
them by how much they move a reported association gives a shape worth having in front of a reader
(Table 4).

**Table 4. The budget assembled: eight axes ordered by how much they move a reported association.**
Every effect is measured on the same cohort with everything else held fixed, so the rows are
comparable with each other and with the within-region effect these models report (+0.056 to +0.153
ROC-AUC, interval about ±0.010 wide at 1 km blocking). The final column marks the axes whose
relevance a reader can settle from their own inputs before fitting anything.

| Axis | Effect on the reported association | Predictable in advance? |
|---|---|---|
| Compositing chain | ±0.02 AUC where it acts; **exactly zero where it cannot** | **yes**, from scenes per date |
| Library version | ±0.02 to 0.03 on cross-region estimates; ~10⁻⁴ within region | yes, from the pinned version |
| Blocking scale | verdict counts move substantially; no sign changes | yes, by construction |
| Index normalisation (sea) | +0.002 to +0.017 on a signed association; no direction changes | **yes**, from water fraction and index range |
| Population size and positives | +0.018 on a within-region increment; none on transfer | yes, from population counts |
| Gap-filled cells | up to −0.013 on an increment; support retained | yes, from the gap-fill share |
| Label omission | moves the sharpest association *away* from chance | partly |
| Coordinate-bearing channels | 0 to 18 % of an increment | yes, from feature-importance records |

Two axes are missing from that table because their effect could not be measured, only bounded: the
quality-screening split, which would need the whole downstream chain rebuilt for three regions, and
the cell geometry, which is not a variation at all but a description of what the grid is.

## 5.2 What should be reported

The practical output of a budget is a reporting list. Six items cost nothing to report and would let
a reader judge most of the above without repeating any of it.

1. **Scenes per distinct acquisition date**, per region and window. This alone decides whether the
   compositing choice can matter.
2. **Water-dominant fraction of the AOI**, and the range of the binning variable that the modelled
   population occupies, for any scene-fitted index.
3. **The quality-screening rule actually applied to each input, per region**, with the date it was
   applied. A cohort split by export date is invisible otherwise.
4. **The nodata convention**, explicitly. A product that declares none and writes zeros is
   indistinguishable in the output from one that observed a physical zero.
5. **The analysis cell's ground dimensions in both axes**, not its nominal name, and the axis that
   block-size labels refer to.
6. **The pinned library versions**, since the cross-region tolerance here exceeds several of the
   effects in the table above.

## 5.3 What generalises and what does not

The magnitudes are this cohort's. Two things are not.

The **rules** of Section 4.3 and 4.4 are statements about inputs. Any user can count scenes per date
and any user can compare their modelled population's index range against the bins where water sits.
Both answer "can this decision matter here" before any computation, and in this cohort both answered
no for half the regions.

The **failure modes** of Section 4.2 are structural. A quality rule added to an export script partway
through a project will split any cohort by export date, and nothing downstream records it. A nodata
convention that writes zeros will encode sea as a physical temperature in any coastal AOI. Neither
depends on this code being unusual; both depend only on the ordinary way such projects accumulate.

What does not generalise is the direction of any specific effect. We report, for instance, that
correcting label omission sharpens the association rather than dissolving it. That is a fact about
these five regions, and the opposite result elsewhere would not contradict it.

## 5.4 Relation to the companion paper

Every axis that bears on the companion paper's findings was tested against them, and in every case
the finding survived: the sign reversal that carries that paper holds under land-only index edges,
under a pooled common edge, under both label-agreement thresholds, under an over-corrected omission
relabelling, and under population and positive-count matching. Two axes could not be pushed that far.
The quality-screening split remains an untested candidate for one region's unexplained behaviour,
with a measured mechanism and the right sign; and the cell geometry means that paper's blocking
argument is weaker in longitude than its labels imply.

That is the honest relationship between the two papers. This one does not rescue the other, and it
was not run to. It reports what the observations are made of, and where that touches a claim, it says
whether the claim holds.

## 5.5 Limitations

(i) **One pipeline.** Every magnitude here is measured on one implementation over one cohort. The
rules and the failure modes are offered as general; the numbers are not.

(ii) **Five regions, and not a sample of anything.** They were selected for the companion paper's
question, not to span a preprocessing design space, so the axes are exercised over whatever range
those five happen to provide. The compositing axis, for instance, has two regions on each side of its
dividing line, which is enough to establish the rule and not enough to characterise its distribution.

(iii) **Two axes bounded rather than measured.** The quality-screening split was measured at the
input and not propagated through the downstream chain, which would require rebuilding three regions'
derived products. The cell geometry is a description, not a variation: we cannot report what a truly
square cell would have given.

(iv) **The independent fire observation is a different quantity.** Active-fire detections are not a
burned-area product, the relabelling built from them is deliberately crude, and no claim is made
that the relabelled cells burned. It probes the omission mechanism; it does not measure omission.

(v) **The compositing comparison is upstream of performance for three regions.** Where the seam
verdict is uncertain or the intervention is inert, the released tool declines the downstream ROC-AUC
comparison by design, so the ±0.02 tolerance has one region's evidence behind it and the rule has
four regions' evidence behind it.

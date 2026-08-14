# 1. Introduction

Satellite fire-susceptibility models are published with a cross-validated skill figure and a
description of the classifier. Between the satellite and that figure sits a chain of decisions:
which pixels to accept, how to composite them, how to normalise an index, how to aggregate to an
analysis cell, which cells to admit, and which library to run it all in. Each is defensible. Few are
reported in enough detail to be repeated, and almost none are reported with a number attached to
what they cost.

This paper attaches those numbers. It takes one pipeline, five Mediterranean wildfire regions, one
label product and one classifier, holds all of them fixed, and varies eight preprocessing decisions
in turn. The result is a budget rather than a caveat list: the effects are measured on the same data
and are therefore comparable with each other, and with the effect size the models themselves report.

## 1.1 Why a budget and not a caveat list

A caveat list says that a choice could matter. A budget says how much, on data the reader can see.
The difference matters because preprocessing decisions are not equally consequential, and treating
them as a uniform fog of uncertainty is as unhelpful as ignoring them. Two of the eight axes here
move a reported association by more than the interval width that the same paper's headline result
carries. Two others cannot move it at all, for reasons that are visible in the inputs before any
model is fitted. Knowing which is which is worth more than knowing that preprocessing is hard.

## 1.2 What makes a preprocessing finding generalisable

The obvious objection to an audit of one pipeline is that its findings are that pipeline's bugs. We
take that seriously and answer it in three ways.

First, wherever possible an axis is converted into a **rule stated in terms of the inputs**, not of
our outputs. Whether the compositing choice can move a result is decided by how many scenes share an
acquisition date, which any user can count before running anything. Whether sea water contaminates a
scene-fitted dryness index is decided by the AOI's water fraction and by where the modelled
population sits in the index's binning variable.

Second, the failure modes we document are structural rather than incidental. A quality-screening rule
added to an export script partway through a project splits a cohort **by export date rather than by
design**, and nothing in the outputs records that. An analysis grid built by aggregating a fixed
number of reference pixels in a geographic coordinate system is square in degrees and not on the
ground. Neither is specific to this code.

Third, the axes that did **not** move the result are reported alongside those that did. A budget in
which everything matters is not a budget.

## 1.3 Relation to the companion paper

The companion paper asks whether a fitted relationship between pre-fire thermal dryness and burning
transfers between regions, and reports that it does not, that the diagnostics available before
deployment do not order the failure, and that the mechanism is a reversal in the sign of the
predictor-burning association. This paper shares that cohort and pipeline and asks a different
question: what the observations on both sides of that comparison are made of. Where an axis here
bears on a claim there, it is noted, and in every case tested the companion paper's finding survives
the variation. Neither paper's conclusion depends on the other's.

## 1.4 Contributions

1. **A measured preprocessing budget** over eight axes on five regions, with data, model and
   validation held fixed, so the axes are comparable with each other and with the reported effect.
2. **Two decisions whose relevance is predictable at no cost**, from the scene inventory and from the
   land-cover and index distributions respectively.
3. **Two provenance splits that leave no trace in the outputs**: a quality-screening rule applied to
   part of a cohort by export date, whose induced change correlates with terrain rather than being a
   uniform offset, and a nodata convention that encodes sea as a physical temperature of exactly
   0.0 °C in the same regions.
4. **A quantified statement of what the analysis cell actually is**, with the derivation reproducing
   every frozen cell count in the cohort exactly.
5. **Four axes tested and found not to threaten the result**, one of which corrects in the direction
   opposite to the convenient one.
6. **A reproducibility floor**: bit-identical rebuild of the within-region results on a different
   operating system from released code and archived data, against a ±0.02 to 0.03 tolerance across
   library versions for the cross-region estimates.

Section 2 places the work against the reproducibility and sensitivity literature. Section 3 describes
the cohort and the protocol by which each axis is varied. Section 4 reports the budget axis by axis.
Section 5 assembles it and states what should be reported as a result. Section 6 concludes.

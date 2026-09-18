# Appendix C. Limitations

Section 5.7 states the four limitations that bind the conclusions; all ten are here. The rest of
this appendix, which specifies the protocol, is released with the supplementary appendices rather
than printed here.

## C.5 Limitations, in full

Section 5.7 states the four that bind the conclusions; all ten are here.

(i) **No meteorological covariates** enter the models, so we cannot say how local skill and
portability behave for a mixed thermal-plus-weather predictor set.

(ii) **The same-geography comparison covers one region only**, and even there year and seasonal phase
are confounded. That confound cannot be resolved in this study area, and the reason is specific: the
two events sit 42 days apart in median burn day-of-year, neither year contains a second event at the
other's phase, and a calendar-matched arm would carry nine burned cells against this design's gate
minimum of thirty. The positive-block count for the 2022 arm is separately below the floor this
design sets itself, at eleven against sixteen (Appendix A(m)). Its 331 burned cells also leave the thermal reversals unresolved at interval level, and
the pair holds place fixed but not population. Those two arms are additionally the only transfer
directions here computed by us rather than read from the pipeline author's frozen export, with his
unmodified code and the same pinned environment.

(iii) **All labels derive from a single burned-area product**, MCD64A1 [@Giglio2018], whose omission
and commission characteristics [@Boschetti2019] bound every model evaluated here. No second
burned-area product covers 2021 and 2022 at this resolution; the companion paper reports what an
independent active-fire observation says about the omission concern.

(iv) **Evia remains the most imbalance-atypical population** even after the AOI extension, at a TSG
prevalence of 0.287 against 0.038 to 0.072 in three of the others.

(v) **Each region contributes one fire season**, so regional concept shift is confounded with event
meteorology, and distinguishing them requires multi-year labels.

(vi) **Cross-region point estimates carry an implementation tolerance** of roughly ±0.02 to 0.03
across scikit-learn versions. All reported numbers are fixed to one verified version, but exact
reproduction elsewhere requires the archived environment.

(vii) **Manavgat's atypical transfer behaviour remains unexplained.** It is where the conditional
diagnosis bites hardest and where feature removal recovers most. Three candidates have now been tested and none survives: its meteorology, which was not extreme;
the quality screening of its coarse thermal input, which propagates widely but moves no signed
association by more than +0.0003 (Appendix A(v), Appendix A(e)); and the evaluation frame, which
explains its elevation figure but not its transfer behaviour (Section 4.4). With one fire season per
region the remaining candidates are not separable in this design.

(viii) **The interval-support counts are less stable than the point estimates behind them.** Several
verdicts sit within a thousandth of their reference value, and at 1 km blocking the published split
of the paired thermal-minus-baseline deltas, ten positive, seven negative and three uncertain, turns on a lower bound of −0.00045. The point
estimates and the sign pattern are stable; the counts are not. Every sentence in this paper that
leans on an exact count of supported directions should be read at that precision.
(ix) **The five areas of interest are not comparable frames, and this cohort cannot fully repair it**
(Section 4.4). We report the equalised arm alongside the frame-as-drawn arm rather than replacing one
with the other, because the collar radius is itself a choice and 5 km and 10 km do not agree exactly
(0.608 against 0.616). The deeper limitation is that the frames were fixed upstream of this work, in
`repo/`, so we can restrict them but not extend them; a region whose rectangle is already fire-scale,
Montiferru, cannot be given a far field for symmetry. Nor can their independence from outcomes be
fully documented: only Montiferru's box is derived by a rule, and for Manavgat, Bejís and Muğla the
version history cannot show the box fixed before the first gate result (Section 3.1). Any future cohort should fix the frame by an
explicit accessible-area rule [@Barve2011] before any predictor is computed, and we treat that as the
main design lesson of this paper.

(x) **Other classifiers are compared by point estimate only.** The headline numbers use a random forest with unlimited depth, the
configuration most able to encode local structure and least able to extrapolate. Appendix A(h) shows the transfer result is not an artefact of that
choice: three further estimators, including a penalised linear one, all land between 0.510 and 0.556
and all place fourteen of twenty directions above chance. Those are point estimates without
intervals, so the ordering among them is not claimed as a result. Estimator classes beyond these four were not
tried, and a different inductive bias might behave differently, but across the four tried the negative
result is a property of the predictors rather than of an unregularised estimator.

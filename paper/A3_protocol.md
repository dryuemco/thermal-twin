# Appendix C. Limitations

Section 5.7 states the seven limitations that bind the conclusions; all thirteen are here. The rest
of this appendix, which specifies the protocol, is released with the supplementary appendices rather
than printed here.

> **Updated 2026-09-23 for the corrected Manavgat label (Section 3.2).** Item (vii) is rewritten, and
> it now carries the one-region, one-event limitation. Items (xi) to (xiii) are new. Item (xiii)
> existed only in Section 5.7 before, which is why the earlier count of four binding and six
> remaining did not add to ten. Items (ii), (iv), (viii), (ix) and (x) carry corrected values.

## C.5 Limitations, in full

Section 5.7 states the seven that bind the conclusions: (v), (vii), (viii), (ix), (xi), (xii) and
(xiii). All thirteen are here. The other six, (i) to (iv), (vi) and (x), bear on scope.

(i) **No meteorological covariates** enter the models, so we cannot say how local skill and
portability behave for a mixed thermal-plus-weather predictor set.

(ii) **The same-geography comparison covers one region only**, and even there year and seasonal phase
are confounded. That confound cannot be resolved in this study area, and the reason is specific: the
two events sit 42 days apart in median burn day-of-year, neither year contains a second event at the
other's phase, and a calendar-matched arm would carry nine burned cells against this design's gate
minimum of thirty. The positive-block count for the 2022 arm is separately below the floor this
design sets itself, at eleven against sixteen (Appendix A(m)). Its 331 burned cells also leave the thermal reversals unresolved at interval level, and
the pair holds place fixed but not population. Those two arms were computed by us rather than read
from the pipeline author's frozen export, with his unmodified code and the same pinned environment.
Since the label correction, every Manavgat quantity is computed by us as well (Section 3.13).

(iii) **All labels derive from a single burned-area product**, MCD64A1 [@Giglio2018], whose omission
and commission characteristics [@Boschetti2019] bound every model evaluated here. No second
burned-area product covers 2021 and 2022 at this resolution; the companion paper reports what an
independent active-fire observation says about the omission concern.

(iv) **Evia remains the most imbalance-atypical population** even after the AOI extension. Its TSG
prevalence is 0.287, the highest in the cohort, against 0.070 to 0.212 in the other four.

(v) **Each region contributes one fire season**, so regional concept shift is confounded with event
meteorology, and distinguishing them requires multi-year labels.

(vi) **Cross-region point estimates carry an implementation tolerance** of roughly ±0.02 to 0.03
across scikit-learn versions. All reported numbers are fixed to one verified version, but exact
reproduction elsewhere requires the archived environment.

(vii) **Manavgat's atypical transfer is localised, not explained, and the localisation rests on one
region and one event.** Manavgat is the weakest target (0.435), carries the largest matched shortfall
(+0.319) and has the most outlying univariate profile in the cohort. Three candidates have been
tested and none accounts for it. Its meteorology was not extreme. The quality screening of its
coarse thermal input moves no signed association by more than 0.005 (Appendix A(v), Appendix A(e)).
The evaluation frame leaves its elevation reversal supported (Section 4.4). An exploratory split by
fire phase places the collapse in the cells that burned in the first four days, and Section 5.4
offers a mechanism proposal from it. That split was not registered and concerns one region and one
event. It cannot be generalised until other events that burn across the elevation gradient are
examined.

(viii) **The interval-support measures are less stable than the point estimates behind them.** Five
to six of the pipeline's interval bounds lie within 0.01 of 0.5, under both labels. A single such
flag, Manavgat's NDVI, moved the full-frame supported-feature cosine from ρ = 0.49 to 0.70 when two
equally valid bootstrap streams disagreed on it (Section 5.4). The transfer verdicts are steadier.
Across five bootstrap seeds, every verdict at 1 km blocking is stable, and the paired split of twelve
positive, seven negative and one uncertain holds on every seed. At 5 km blocking, one level verdict
and two paired-delta verdicts change with the seed. Every sentence in this paper that leans on an
exact count of supported directions should be read at that precision.

(ix) **The five areas of interest are not comparable frames, and this cohort cannot fully repair it**
(Section 4.4). We report the equalised arm alongside the frame-as-drawn arm rather than replacing one
with the other, because the collar radius is itself a choice and 5 km and 10 km do not agree exactly
(0.591 against 0.589). The deeper limitation is that the frames were fixed upstream of this work, in
`repo/`, so we can restrict them but not extend them; a region whose rectangle is already fire-scale,
Montiferru, cannot be given a far field for symmetry. Nor can their independence from outcomes be
fully documented: only Montiferru's box is derived by a rule, Manavgat's is dated before its first gate result, and for Bejís and Muğla the
version history cannot show the box fixed before the first gate result (Section 3.1). Any future cohort should fix the frame by an
explicit accessible-area rule [@Barve2011] before any predictor is computed, and we treat that as the
main design lesson of this paper.

(x) **Other classifiers are compared by point estimate only.** The headline numbers use a random forest with unlimited depth, the
configuration most able to encode local structure and least able to extrapolate. Appendix A(h) shows the transfer result is not an artefact of that
choice: three further estimators, including a penalised linear one, all land between 0.481 and 0.527
and place eleven to thirteen of twenty directions above chance. Those are point estimates without
intervals, so the ordering among them is not claimed as a result. Estimator classes beyond these four were not
tried, and a different inductive bias might behave differently, but across the four tried the negative
result is a property of the predictors rather than of an unregularised estimator.

(xi) **The phase split cannot separate elevation from temperature.** The cells that burned in
Manavgat's first four days lie at a median of 219 m, against 512 m for the later burns and 1,004 m
for unburned cells. They also carry the region's strongest LST signal, at AUC 0.70 to 0.72 against
0.57 to 0.58 later. Low ground is hot ground here. The proposal of Section 5.4 is therefore
confounded in this data by construction. Separating the two needs predictors that decouple terrain
from surface temperature, or events in which the hot surfaces are not the low ones.

(xii) **The quality-screening comparison differs in code version as well as in screening.** The
current pipeline's step7 refuses the unscreened MODIS input, because the raster carries no nodata tag
and 8.1 % exact zeros. The unscreened arm therefore uses the step7 of export time, and the screened
arm the current one. The two agree on elevation to four decimals and on every other signed AUC to
within 0.005, the largest move being downscaled LST at −0.0044. The within-region increment moves
from +0.067 to +0.068. The confound could therefore have hidden an effect only if two effects had
cancelled. An earlier description of both arms as rebuilt was inaccurate: the earlier unscreened arm
almost certainly met the same refusal, since its signed AUCs equal the frozen ones (Appendix A(e)).

(xiii) **The diagnostic correlations rest on an effective sample of ten region pairs.** Five regions
give twenty ordered directions, but the two directions of a pair share both regions and are not
independent. The diagnostic results of Appendix D, successes and failures alike, read at that power.

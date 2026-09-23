# 5. Discussion

> **Rewritten 2026-08-14 in the split.** This section was 9,372 words, of which 5,409 were
> limitations. It now discusses the four contributions of Section 1.4 and carries the limitations that
> bear on them. Six limitations concerning the observational layer, meaning cell geometry,
> compositing, predictor redundancy and the coordinate channels, MODIS quality screening, label
> noise and the safeguards, move with their evidence to the companion paper.
>
> **Updated 2026-09-23 for the corrected Manavgat label (Section 3.2).** Values follow
> `paper/labelfix_rerun/round5/E1_CHANGELIST.md` §7 and §13. Section 5.2 now states that the
> transfer shortfall has no region-level support. Section 5.4 gains a paragraph on Manavgat and one on
> measures built from interval support. Section 5.7 gains three limitations.

## 5.1 Reading the two findings together

Section 1.3 states the two findings and Section 4 establishes them; this section argues from them.
The relation between them is what makes the paper cohere. The first is not a caveat attached to the
second; it is the instrument that sets its size. Applied to our own matrix, it identified four
quantities as properties of the frames rather than of the relationship between predictors and
burning. What it left standing is a shortfall in transferred skill and one reversed relationship,
Manavgat's elevation.

## 5.2 Why the thermal increment is real but local

The within-region increment and the transfer failure are measured at different separations, and
Section 4.3 shows most of the difference is already present inside a single region. The increment is
local in a specific sense. It holds where held-out cells are interleaved with training cells, and
most of it is gone once they are not, before the fire or the region changes. It is not an artefact to
be explained away: it survives every sensitivity arm of Appendix A(a)–(h), and window closure stays
positive and supported in all five regions on the corrected label. But it is established under
interleaved validation and not beyond it. Even there the window-closure arm **weakens monotonically
in Evia**, so what holds everywhere is survival, not improvement.

**That comparison is established at the scar, not at the region, and this weakens the claim.**
Section 4.3 measures the fall from a blocked within-region figure to an unseen scar over seven scars
in three regions. Clustered by region, the frame cost stays clear of zero at +0.137 [+0.048, +0.226].
The whole fall to an unseen scar does not: it is +0.266 [−0.022, +0.553]. On the region as the unit,
then, only the frame cost is established. The shortfall itself is supported at the scar level only,
and this cohort gives it no region-level support.

The natural objection is that Mediterranean regions are simply different systems, so a predictor
meaning one thing in one place and another elsewhere compares two systems rather than showing
instability. **We designed the two-Muğla-events arm to answer that objection and it does not answer
it**: Section 4.4 shows it is the most extreme frame artefact in the cohort. Three further confounds
were never resolved in any case. Season and year **cannot be resolved in this study area**, the
population is not fixed, and the positive-block count is below this design's own floor (Appendix
C.5(ii)). With one fire per region everywhere else and that arm withdrawn, **this cohort provides no
evidence that the transfer shortfall is regional rather than event-specific**. Appendix A(t) adds a
length scale for the within-region decay but cannot turn it into an attribution either.

One conclusion survives from the other direction. The static baseline transfers no better than the
dynamic block, at a mean of 0.519 against 0.527, so whatever the shortfall is, it is not the thermal
block's peculiarity.

## 5.3 What the two interventions do and do not show

Both interventions show the same shape. Pooling four regions never beats the best single-source
transfer for any target and stays well below the within-region ceiling (Appendix A(n)). It does not
manufacture the missing conditional information. Removing the reversing predictors costs −0.076 of
within-region skill with interval support in every region, and returns +0.014 [−0.028, +0.056] in
mean transfer.

That pair of numbers is easy to read as an exchange, and it is not one. Both arms are null on the
portability axis. The thermal block's own contribution is +0.007 and removal returns +0.014, both
with intervals spanning zero, so they measure a local cost and no compensating gain. That is not a
conservation law and not a rate at which local skill can be sold for portability; no such rate is
estimated here.

## 5.4 The regime hypothesis, reported as it happened

A regime-structure explanation was stated in advance and the data confirmed the null. The
regime-distance correlation has the wrong sign at the point estimate (ρ = +0.109). The most
regime-similar pair, Bejís and Manavgat, fails in both directions (0.396 and 0.314). The most
regime-different pair, Bejís and Muğla, transfers above chance in both (0.618 and 0.583). One mundane
explanation can be set aside: subsampling Muğla, much the largest population, to Manavgat's cell
count leaves its transfer behaviour inside the subsampling range in both roles. The error was in the
hypothesised grouping, not in the data, and with ten pairs this cannot refute regime typology
[@Archibald2013] in general.

**Manavgat is where the matrix fails most, and three indicators point there.** It has the most
outlying univariate profile in the cohort, with elevation at 0.232 and the three LST channels near
0.67, all interval-supported and all opposite to the other four regions. It also carries the largest
matched shortfall (+0.319) and is the weakest target (0.435). The three point at the same region, and
that is not a coincidence. A model trained where burned cells sit higher and cooler than their
surroundings is asked to rank a fire that burned low and hot. The exploratory phase split of Section
4.5 suggests where the collapse sits. The cells that burned in the fire's first four days lie at a
median of 219 m, and their LST signal is the strongest in the region (AUC 0.70 to 0.72 with interval
support, against 0.57 to 0.58 later). Transfer into these early cells is lower from every source,
and the static baseline collapses there too. Elevation is reversed in both phases (0.197 and 0.328).
With this data, elevation and temperature cannot be separated, because the low ground is also the hot
ground.

We therefore offer a mechanism proposal, not a finding. The sign of elevation, and with it the sign
of the thermal channels, may be set by which part of the elevation gradient an event burns relative
to its frame, rather than by the region. Muğla shows the same pattern across its 2021 and 2022
events. The 2021 fire burned high relative to its frame (elevation AUC 0.611), the 2022 fire low
(0.297), and the reversal is interval-supported inside a single study area. The link has a limit
that belongs with it. Muğla's reversal is carried by the 2022 arm's far field and the collar removes
it (0.606 against 0.565), whereas Manavgat's survives the collar (0.376). The two cases therefore share
the pattern on the frames as drawn but differ in how much of it the frame explains. Testing the
proposal needs several events per region spread along the elevation gradient, and predictors that
separate terrain from surface temperature.

**Measures built from interval support carry a warning for future work.** Measures that count or
weight only interval-supported features are structurally sensitive to flags on a knife edge. Under
both labels, five to six of the pipeline's interval bounds lie within 0.01 of 0.5. A single such flag,
Manavgat's NDVI, moved the full-frame supported-feature cosine from ρ = 0.49 to 0.70 when two equally
valid bootstrap streams disagreed on it. A threshold on the interval turns small shifts in the inputs
into discrete changes in the feature set. This partly explains why the conditional-similarity result
fell from +0.84 to +0.52 [−0.27, +0.87] under the corrected label. Work that uses such measures should
report how many bounds lie near the threshold, and should repeat the calculation across bootstrap
streams before reading a correlation.

## 5.5 The empirical contrast with Dimarco et al.

Dimarco et al. [@Dimarco2026] transfer successfully across a comparable Mediterranean design and we
do not, and the two results are not in conflict. Their predictors are attributes of a place, ours
the state of a surface in one season. That suggests the relation between domain similarity and
transfer success depends on the predictor class.

That reading is one of at least two, and we cannot separate them here. Their response variable is
human-driven **ignition**, dominated by access and activity, while ours is burned **area**, dominated
by spread. A predictor-class explanation and a response-variable explanation are therefore confounded
in this comparison. Our own data speak against a simple predictor-class reading in any case: the
static baseline transfers at a mean of 0.519 here, so within this cohort the place-attribute class
does not travel either.

## 5.6 Implications

In precision-recall terms, which is how a susceptibility surface is used, transferred models average
a PR-AUC of 0.181 against a no-skill baseline of 0.157 **on the frames as drawn**. Seven of twenty
fall below their own baseline, all seven with intervals entirely below it (Section 4.5). Whatever
the ROC figures suggest, a model moved to a region it was not fitted in does not usefully rank burned
cells there.

The paper supports one concrete change in reporting: alongside a spatially blocked within-region
figure, report skill on a held-out burn scar and its surroundings. On these five regions the two
differ by about 0.13 ROC-AUC on the same model, the size of the effect such papers usually claim, and
this frame cost holds with the region as the unit (Section 5.2). **A blocked figure alone should
therefore be read as an upper bound.** Transfer skill likewise has to be *measured* on the target
region rather than assumed from a within-region figure. Where a model must be moved, the resource
that closes the gap is target labels (Appendix A(u)): a real answer, but not a cheap one.

The results also bound what unsupervised alignment can be asked to do. Even the oracle selection,
which uses the target labels the protocol forbids, only reaches the reference a model can reach on an
unseen scar (Section 4.5). Alignment is not failing far below an achievable target; it is regressing
the matrix onto it, at the cost of the directions that already worked. A sign reversal is not a
distribution mismatch that realigning inputs repairs.

## 5.7 Limitations

Appendix C.5 states the limitations in full, and seven bind the conclusions above. **The frames are
not comparable and this cohort cannot fully repair it** (Section 4.4). The collar radius is itself a
choice, with 5 km and 10 km giving 0.591 against 0.589, and the frames were fixed upstream, so we can
restrict them but not extend them. Any future cohort should fix the frame by an explicit
accessible-area rule [@Barve2011] before any predictor is computed; that is the main design lesson
of this paper. **Each region contributes one fire season**, so regional concept shift is confounded
with event meteorology and the shortfall cannot be attributed to region rather than event (Section
5.2). **The diagnostic correlations rest on an effective sample of ten region pairs**, so the
diagnostic results of Appendix D, successes and failures alike, read at that power.

**The interval-support measures are less stable than the point estimates behind them.** Five to six
interval bounds lie within 0.01 of 0.5, so one flag can move a diagnostic correlation by about 0.2
(Section 5.4). The transfer verdicts are steadier: at 2-cell blocking every verdict is stable across
five bootstrap seeds, and at 10 cells one level verdict and two paired-delta verdicts are not.

**The phase split cannot separate elevation from temperature.** The cells that burned first are both
the lowest and the hottest, so the proposal of Section 5.4 is confounded in this data by
construction. **It also rests on one region and one event.** The split was not registered, and it
cannot be generalised until other events that burn across the elevation gradient are examined.

**The quality-screening comparison also changes the code.** The current pipeline's step7 refuses the
unscreened MODIS input, so the unscreened arm uses the step7 of export time and the screened arm the
current one. The two arms therefore differ in code version as well as in screening. They agree on
elevation to four decimals and on every other signed AUC to within 0.005, so the confound could only
have hidden an effect if two effects cancelled. It is stated because an earlier description of both
arms as rebuilt was inaccurate.

The remaining six, from the absent meteorological covariates to the classifier comparison made by
point estimate only (Appendix A(h)), bear on scope rather than on the conclusions above.

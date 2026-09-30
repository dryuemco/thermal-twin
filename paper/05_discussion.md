# 5. Discussion

## 5.1 The three findings together

The first finding sets the size of the second. When the study areas were made comparable, four
between-region results changed (Section 4.4). Two results remained: transfer stayed well below within-region skill, and the elevation association
of Manavgat stayed reversed against other regions. The supported pairs, however, change between the
frames, and none survives multiplicity correction (Section 4.4).
The third finding closes an obvious way around the second. If transfer cannot be assumed, it might
still be predicted from the similarity of two regions, but none of the twenty measures did this on
the original study areas.

## 5.2 What the within-region score measures

The thermal gain within regions is robust, with one exception. It was supported in all five regions
under blocked validation and when the predictor window was closed up to two weeks earlier (Section
S1.4). It stayed positive in every region at the point estimates without the coordinate-informed
channels (Section S1.7) and with VNP64A1 labels (Section S1.23). Once terrain aspect was added,
however, the gain in Montiferru was no longer supported (Section 4.2). In addition, on the scar
frame the same gain fell to
+0.021 and was not established, and withholding the scar did not change it. The fall is therefore
caused by the cells that are scored, not by the choice of held-out cells.

The within-region score also describes skill close to the training cells. Inside one region, skill
fell from 0.709 within 5 km of the training cells to 0.519 at 10 to 20 km (Section S1.18). The
within-region reference therefore measures how well a model fills gaps inside an observed fire
season. Part of the transfer shortfall is thus a matter of distance, and a model of this kind is best
described as having short-range skill.

Each region also contributes one fire season, dominated by one large fire. The negative class
therefore contains cells that could have burned but were not reached, and ignition, wind and
suppression decided much of this. Burned-area patterns have different controls at different scales
[@ParisienMoritz2009], and a pre-fire surface predictor can only rank cells by their condition
before the fire. The shortfall can therefore not be attributed to the region rather than to the
event. The two Muğla fires were included to separate these effects, but this comparison was mainly
affected by the study area (Section 4.4). The conclusions are stated for large single-season events.

## 5.3 The two interventions

Pooling four source regions was better than the mean single-source model only for Evia, where it
reached 0.715 [0.668, 0.757] against 0.569 (Section S1.14). For all five targets it stayed well
below the within-region ceiling. Removing the two reversing predictors lowered within-region skill
by 0.076, most of it from elevation, with interval support in every region, and changed mean transfer
by +0.014 [−0.018, +0.049] (pair-t, as plotted in Fig. 7: +0.014 [−0.028, +0.056]).

These two numbers should not be read as an exchange of local skill for transfer. The thermal
contribution to transfer is +0.007, and removal returns +0.014, and both intervals include zero. A
local cost is therefore measured, but no gain in transfer.

## 5.4 What the thermal predictors measured

The thermal predictors were chosen as a measure of pre-fire dryness, but they did not behave as one.
At the point estimates, hotter surfaces burned less in four of five regions, and in Manavgat once
elevation was held; the Manavgat result has interval support only on the collar (Section 4.4). In summer, land surface temperature is strongly shaped by canopy cover, exposed soil
and terrain. Dense, cooler vegetation carries more fuel, so a negative association is consistent with LST acting
as a land-surface descriptor. In Montiferru, most of the within-region thermal gain disappeared once
terrain aspect was added, which fits this reading. Descriptively, across only five regions, the mean LST anomaly also followed the ERA5-Land
[@MunozSabater2021] air-temperature anomaly of the predictor window, but not its relative-humidity
anomaly (Section S1.23). The normalised channels did not transfer better than
the absolute ones either (Section S1.6). In Mediterranean ecosystems, the link between fire and
climate also depends on fuel and productivity [@PausasPaula2012], so the sign of a surface predictor
may differ between landscapes. Whether a fire becomes very large depends mostly on fire weather
acting on drought-stressed fuel [@Ghasemiazma2026], which no surface predictor measured before the
fire can carry; the surface component tested here would complement, not replace, weather-driven
danger rating [@Vitolo2020], as in products that combine susceptibility with pre-season weather
[@Bergonse2021].

Dimarco et al. [@Dimarco2026] found good transfer in a similar Mediterranean design, while transfer
failed here. The two studies differ in two ways. Their predictors are static attributes of a place,
and their response is a record of human-caused ignitions. Here the predictors describe the surface in
one season, and the response is the footprint of one fire season per region. These two differences
cannot be separated in this comparison. In this cohort the static baseline also did not transfer
(mean 0.519), so predictor class alone does not explain the difference.

## 5.5 Implications for practice

Mediterranean fire policy is urged to shift from suppression towards prevention and landscape
management [@Moreira2020], and region-wide susceptibility maps serve this prevention planning. Four
changes in practice are supported by these results.

**Report the evaluation frame, and name the question it answers.** A region-wide score describes
where in a landscape fire occurred, which is the question behind prevention planning. A scar-frame
score describes which cells next to a fire burned. On the same model the two differed by 0.160
ROC-AUC with the region as the unit, which is larger than the thermal gain within most regions (Table
1). Both numbers are needed to judge a model.

**Measure transfer in the target region.** A within-region score does not show how a model will work
elsewhere, and no similarity measure tested here could replace the measurement. On average, a model moved to a new region did not usefully rank the burned cells there: its
highest-scored 10 % of cells contained about as many burned cells as a random choice, although the
best direction reached 27 % (Table S35). Target
labels from the predicted fire closed much of the gap (Section S4), but they are not available in
advance. Where a burned-area record of earlier fires exists for the target region, it offers a way to
check a transferred model before use; this option was not tested here.

**Fix the study area by a stated rule before the predictors are computed.** The study areas used
here were not comparable, and this changed four between-region results (Section 4.4). An
accessible-area rule [@Barve2011] is one option.

**Do not expect label-free adaptation to repair transfer.** Both methods tested moved most directions
toward chance, including those that had worked (Section 4.5). A reversed association cannot be seen
without target labels, so aligning the predictor distributions cannot correct it.

## 5.6 Limitations

The limitations are given in full in Section S3.5. The following ones affect the conclusions.

- **Each region contributes one fire season,** so region and event effects cannot be separated
  (S3.5(v)).
- **The study areas were not comparable.** They could be restricted but not extended, because they
  were fixed earlier in the processing pipeline (Section 4.4; S3.5(ix)).
- **The frame cost rests on few scars.** The full comparison is defined on seven scars in three
  regions, so the region-level estimates should be quoted (Section 4.3).
- **Point estimates depend on the software version.** Under another scikit-learn version, single
  directions moved by up to 0.047; across ten random-forest seeds, single directions moved by up to
  0.049 and mean transfer by at most 0.003. Direction-level intervals do not include this variation
  (Section 3.13; S1.23; S3.5(vi)).
- **Spatial dependence reaches beyond the 5 km blocks.** Residual correlation falls below 0.05
  only at 10 to 20 km in three regions and at 20 to 40 km in North Evia, so intervals at 5 km
  blocking may be too narrow, especially in North Evia (Section 3.7; S1.23).
- **The thermal contribution to transfer depends on the estimator.** It was +0.007 for the random
  forest used here but negative for a shallower forest, a forest with large leaves and a penalised
  logistic regression (−0.011 to −0.021, point estimates only; Table S25).
- **The similarity tests rest on ten independent region pairs,** so both positive and negative
  results have low power (S3.5(xiii)).
- **Measures based on interval support are unstable.** Five to six interval bounds lie within 0.01
  of 0.5, and one changed flag moved a correlation by about 0.2 (Section S1.20; S3.5(viii)).
- **The reversal test is marginal.** A reversal of a single predictor can also come from different
  predictor distributions, so it does not prove a change in the predictor-burning relationship
  (Section 3.10).
- **The low transfer into Manavgat is located but not explained.** Weather, quality screening and the
  study area were tested, and none explained it. Terrain was held through elevation and aspect only, and in Manavgat burn timing and elevation are
  confounded (S3.5(vii), S3.5(xi)).
- **All labels come from one burned-area product,** MCD64A1 [@Giglio2018], with known omission and
  commission errors [@Boschetti2019; @Katagis2022], which are concentrated at scar edges. With VIIRS VNP64A1 labels [@VNP64A1], which overlap MCD64A1
  by 87 % to 98 %, no conclusion changed; independent fire perimeters were not used (S1.23;
  S3.5(iii)).
- **The land-cover map is post-fire for four events.** With the 2020 map, mean transfer was 0.513
  instead of 0.527, and no conclusion changed; in Montiferru, however, the 2021 map left out about a
  fifth of the burned natural vegetation (Section 3.4; S1.23).
- **No weather predictors were used** (S3.5(i)), and other classifiers were compared by point
  estimate only (Section S1.8; S3.5(x)).

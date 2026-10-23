# 4. Discussion

## 4.1 The three findings together

The first finding sets the size of the second. When the study areas were made comparable, three
between-region results changed (Section 3.4): mean transfer, which elevation reversals have interval
support, and the correlation of one similarity measure with transfer. Two results remained: transfer
stayed well below within-region skill, and the elevation association of Manavgat stayed reversed
against other regions. The supported pairs, however, changed between the frames, and none survived
multiplicity correction. The third finding closes an obvious way around the second: none of the
twenty similarity measures predicted transfer on the original study areas.

## 4.2 What the within-region score measures

The thermal gain within regions held in every check, including the removal of the
coordinate-informed channels (Section S1.7), except terrain aspect in Montiferru (Section 3.2). On
the scar frame it fell to +0.021 and was not established, mainly because the scored cells changed,
although an effect of withholding the scar cannot be excluded (Section 3.3).

The within-region score also describes skill close to the training cells. Inside one region, skill
was close to chance 10 to 20 km from the training cells (Section 3.5). The
within-region reference therefore measures interpolation, how well a model fills gaps inside an
observed fire season, whereas transfer is extrapolation to a new one. Part of the transfer shortfall
is thus a matter of distance, and a model of this kind is best described as having short-range skill.

Each region also contributed one fire season, dominated by one large fire. The negative class
therefore contains cells that could have burned but were not reached, and ignition, wind and
suppression decided much of this. Burned-area patterns have different controls at different scales
[@ParisienMoritz2009], and a pre-fire surface predictor can only rank cells by their condition before
the fire. The shortfall therefore cannot be split into a region effect and an event effect. A
second Muğla fire was examined for this purpose, but that comparison is confounded by overlapping
populations and the study area and is reported only in Section S1.13.

## 4.3 The two interventions

Pooling four source regions helped only Evia, and for all five targets it stayed well below the
within-region ceiling (Section S1.14). Removing the two reversing predictors cost 0.076 of
within-region skill, mostly from elevation and supported in every region, and changed mean transfer
by +0.014 [−0.018, +0.049] (pair-t interval in Fig. 7: +0.014 [−0.028, +0.056]). This is not an
exchange of local skill for transfer: the change, like the thermal contribution to transfer (+0.007),
includes zero, so a local cost was measured but no transfer gain.

## 4.4 What the thermal predictors measured

The thermal predictors were chosen as a measure of pre-fire dryness, but they did not behave as one.
At the point estimates, hotter surfaces burned less in four of five regions, and in Manavgat once
elevation was held; the Manavgat result has interval support only on the collar (Section 3.4). In
summer, land surface temperature is strongly shaped by canopy cover, exposed soil and terrain. Dense,
cooler vegetation carries more fuel, so a negative association fits LST acting as a descriptor of
the land surface; a dryness index should show the opposite sign. In Montiferru, most of the within-region
thermal gain disappeared once terrain aspect was added, which fits this reading. Descriptively,
across only five regions, the mean LST anomaly also followed the ERA5-Land [@MunozSabater2021]
air-temperature anomaly of the predictor window, but not its relative-humidity anomaly (Section
S1.23). The normalised channels did not transfer better than the absolute ones either (Section 3.5).
In Mediterranean ecosystems, the link between fire and climate also depends on fuel and productivity
[@PausasPaula2012], so the sign of a surface predictor may differ between landscapes. Whether a fire
becomes very large depends mostly on fire weather acting on drought-stressed fuel [@Ghasemiazma2026],
which no surface predictor measured before the fire can carry; the surface component tested here
would be added to weather-driven danger rating [@Vitolo2020], as in products that combine
susceptibility with pre-season weather [@Bergonse2021].

Dimarco et al. [@Dimarco2026] found good transfer in a similar Mediterranean design, while transfer
failed here. Their predictors are static attributes of a place, and their response is a record of
human-caused ignitions; here the predictors describe the surface in one season, and the response is
the footprint of one fire season per region. These two differences cannot be separated in this
comparison, but in this cohort the static baseline also did not transfer (mean 0.519), so predictor
class alone does not explain the difference.

## 4.5 Implications for fire management

Region-wide susceptibility maps are used for prevention planning, and these results support four
changes in practice.

First, report the evaluation frame and the question it answers (Section 2.12). On the same model,
the region-wide and scar-frame scores differed by 0.160 ROC-AUC with the region as the unit, more
than the thermal gain within most regions (Table 2), so both are needed to judge a model.

Second, measure transfer in the target region. A within-region score does not show how a model will work
elsewhere, and no similarity measure tested here could replace the measurement. On average, a model
moved to a new region did not usefully rank the burned cells there: its highest-scored 10 % of cells
contained about as many burned cells as a random choice, although the best direction reached 27 %
(Table S35). Where a burned-area record of earlier fires exists for the target region, it can be used
to check a transferred model before use; this option was not tested here.

Third, fix the study area by a stated rule before the predictors are computed. The study areas used here
were not comparable, and this changed three between-region results (Section 3.4). An accessible-area
rule [@Barve2011] is one option.

Fourth, do not expect label-free adaptation to repair transfer. Both methods tested moved most directions
toward chance, including those that had worked (Section 3.5). A reversed association cannot be seen
without target labels, so aligning the predictor distributions cannot correct it.

## 4.6 Limitations

Section S3.5 lists every limitation; these affect the conclusions.

- Each region contributes one fire season, so region and event effects cannot be separated
  (S3.5(v)).
- The study areas were not comparable. They could be restricted but not extended, because they
  were fixed earlier in the processing pipeline (Section 3.4; S3.5(ix)).
- The frame cost rests on few scars. The full comparison is defined on seven scars in three
  regions, so the region-level estimates should be quoted (Section 3.3).
- Point estimates depend on the software version and the seed. Single directions moved by up to
  0.047 under another scikit-learn version and by up to 0.049 across ten random-forest seeds, and
  direction-level intervals do not include this variation (Section 2.13; S1.23; S3.5(vi)).
- Spatial dependence reaches beyond the 5 km blocks, so intervals at 5 km blocking may be too
  narrow, especially in North Evia (Section 2.7; S1.23).
- The sign of the thermal contribution to transfer depends on the estimator. It was +0.007 for the
  random forest used here but negative for the three simpler models (−0.011 to −0.021), although every
  interval includes zero (Section 3.5).
- The similarity tests rest on ten independent region pairs, so both positive and negative
  results have low power, and measures based on interval support are unstable: five to six interval
  bounds lie within 0.01 of 0.5, and one changed flag moved a correlation by about 0.2 (Section S1.20;
  S3.5(viii), S3.5(xiii)).
- The reversal test is marginal. A reversal of a single predictor can also come from different
  predictor distributions, so it does not prove a change in the predictor-burning relationship
  (Section 2.10).
- The low transfer into Manavgat is located but not explained. Weather, quality screening and the
  study area were tested, and none explained it. Terrain was held through elevation and aspect only,
  and in Manavgat burn timing and elevation are confounded (S3.5(vii), S3.5(xi)).
- All labels come from one burned-area product, MCD64A1 [@Giglio2018], with known omission and
  commission errors [@Boschetti2019; @Katagis2022], which are concentrated at scar edges. With VIIRS
  VNP64A1 labels [@VNP64A1], which overlap MCD64A1 by 87 % to 98 %, no conclusion changed; independent
  fire perimeters were not used (S1.23; S3.5(iii)).
- The land-cover map is post-fire for four events. With the 2020 map, mean transfer was 0.513
  instead of 0.527, and no conclusion changed; in Montiferru, however, the 2021 map left out about a
  fifth of the burned natural vegetation (Section 2.4; S1.23).
- No weather predictors were used (S3.5(i)), and only four estimators were compared (S3.5(x)).

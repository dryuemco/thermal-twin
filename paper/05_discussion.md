# 5. Discussion

## 5.1 The three findings together

The first finding sets the size of the second. When the study areas were made comparable, four
between-region quantities were shown to depend on the study areas and not on the relationship
between predictors and burning (Section 4.4). Two results remained. Transfer stayed well below
within-region skill, and one reversed relationship remained: the elevation association of Manavgat.
This reversal is supported under the per-comparison criterion but not after multiplicity
correction. The third finding closes an obvious way around the second. If transfer cannot be
assumed, it might still be predicted from the similarity of two regions. None of the twenty measures
did this on the original study areas.

## 5.2 The thermal gain within regions and at the fire

The thermal gain within regions is robust. It was supported in all five regions under blocked
validation, in all sensitivity analyses (Sections S1.1 to S1.8), and when the predictor window was
closed up to two weeks earlier (Section S1.4). At the burn scar, the same gain fell to +0.021 and was
not established. Withholding the scar did not change it. The fall is therefore caused by the cells
that are scored, not by the choice of held-out cells. These comparisons rest on seven scars in three
regions. With the region as the unit, only the frame cost is established (Section 4.3).

Each region contributes one fire season. The shortfall in transfer can therefore not be attributed
to the region rather than to the event. The two Muğla fires were included to separate these two
effects, but this comparison was mainly affected by the study area (Section 4.4). Each burned area
is also a single outcome of ignition, wind and suppression, which are not observed here. A pre-fire
surface predictor can only rank cells by their condition before the fire. The five fires were large
events, so the conclusions are stated for large events.

## 5.3 The two interventions

Pooling four source regions was better than the mean single-source model only for Evia, where it
reached 0.715 [0.668, 0.757] against 0.569 (Section S1.14). For all five targets it stayed well
below the within-region ceiling. Removing the two reversing predictors cost −0.076 of within-region
skill, with interval support in every region. It changed mean transfer by +0.014 [−0.028, +0.056].

These two numbers should not be read as an exchange of local skill for transfer. The thermal
contribution to transfer is +0.007, and removal returns +0.014. Both intervals include zero. A local
cost is therefore measured, but no gain in transfer.

## 5.4 Comparison with earlier work

Dimarco et al. [@Dimarco2026] found good transfer in a similar Mediterranean design, while transfer
failed here. The two studies differ in two ways. Their predictors are static attributes of a place,
and their response is human-caused ignition. Here the predictors describe the surface in one season,
and the response is burned area. These two differences cannot be separated in this comparison. In
this cohort the static baseline also did not transfer (mean 0.519), so predictor class alone does not
explain the difference.

Hotter pre-fire surfaces burned less in four of five regions, and in Manavgat once elevation was held
constant (Section 4.4). In this cohort, the absolute thermal channels therefore behaved as
land-surface descriptors and not as a dryness index. The normalised channels did not transfer better
(Section S1.6).

## 5.5 Implications for practice

Three changes in reporting are supported by these results.

**Report skill at the fire, together with the region-wide score.** On the same model, the two scores
differed by 0.133 ROC-AUC over seven scars and by 0.160 with the region as the unit. This is larger
than the thermal gain within most regions (Table 1). A region-wide blocked score should
therefore be read as an upper bound.

**Measure transfer in the target region.** A within-region score does not show how a model will work
elsewhere, and no similarity measure tested here could replace the measurement. In precision terms,
a model moved to a new region did not usefully rank the burned cells there (Section 4.5). Target
labels closed much of the gap (Section S5), but they come from the fire that is being predicted.

**Fix the study area by a stated rule before the predictors are computed.** The study areas used
here were not comparable, and this changed four between-region results (Section 4.4). An
accessible-area rule [@Barve2011] is one option.

Label-blind domain adaptation should not be expected to repair transfer. It moved most directions
toward chance, including those that had worked (Section 4.5). A reversed association is not corrected
by aligning the predictor distributions.

## 5.6 Limitations

The limitations are given in full in Section S3.5. The following ones affect the conclusions.

- **The study areas were not comparable.** They could be restricted but not extended, because they
  were fixed earlier in the pipeline (Section 4.4; S3.5(ix)).
- **The frame cost rests on few scars.** The full comparison is defined on seven scars in three
  regions. The region-level estimates should be quoted (Section 4.3).
- **Each region contributes one fire season,** so region and event effects cannot be separated
  (S3.5(v)).
- **The similarity tests rest on ten independent region pairs,** so both positive and negative
  results have low power (S3.5(xiii)).
- **Measures based on interval support are unstable.** Five to six interval bounds lie within 0.01
  of 0.5, and one changed flag moved a correlation by about 0.2 (Section S1.21; S3.5(viii)).
- **The low transfer into Manavgat is located but not explained.** Weather, quality screening and the
  study area were tested, and none explained it. Terrain was held only through elevation (S3.5(vii)).
- **Point estimates depend on the software version.** Under another scikit-learn version, single
  directions moved by up to 0.047, so exact reproduction needs the archived environment (Section 3.13;
  S3.5(vi)).
- **All labels come from one burned-area product,** MCD64A1 [@Giglio2018], with known omission and
  commission errors [@Boschetti2019; @Katagis2022]. VIIRS VNP64A1 [@VNP64A1] was not used as a label
  sensitivity (S3.5(iii)).
- **No weather predictors were used** (S3.5(i)). Other classifiers were compared by point estimate
  only (Section S1.8; S3.5(x)).

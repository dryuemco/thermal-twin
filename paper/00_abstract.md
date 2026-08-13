# Abstract


Pre-fire thermal dryness separates a fire year from a normal year. It is measured by land surface
temperature, its anomalies against a climatology, and thermal and optical dryness indices. Models
built on these predictors are rarely tested outside their training region.

Five Mediterranean wildfire regions were analysed on about 500 m cells, with MCD64A1 labels and
spatially blocked validation. Six pre-fire thermal predictors were added to a static
terrain and fuel baseline. Within every region, ROC-AUC was raised by +0.06 to +0.15. The gain
survived coarser blocks and an earlier predictor window.

The predictors were then transferred between regions. Their mean contribution over twenty ordered
directions was only +0.004. Ten directions were improved with bootstrap support and seven
were degraded. Local skill and portability are therefore traded.

The failure is conditional, not distributional, and not caused by comparing different places.
Inside one identical study area, two fires eleven months apart reversed the link between elevation
and burning, with no overlap in their bootstrap intervals.

Twenty candidate diagnostics were tested before transfer. None ordered transfer
performance. The pair with the highest burned-niche overlap failed in both directions. The pair
with the lowest overlap transferred in both. Only the agreement in the sign of each predictor's
association tracked transfer (Spearman ρ = 0.84). Label-blind adaptation, by region-wise
standardisation and CORAL, only pushed the directions towards chance. Signed associations need
burned labels in both regions, so the test is a labelled probe, not a label-free screen.
Transferability must therefore be measured, and measured conditionally.

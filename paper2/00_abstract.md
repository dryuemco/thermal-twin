# Abstract

Satellite fire-susceptibility models are published with a cross-validated skill figure. Between the
satellite and that figure sits a chain of preprocessing decisions, each defensible, few reported in
enough detail to repeat and almost none reported with a number attached to what they cost.

This paper attaches those numbers. One pipeline, five Mediterranean wildfire regions, one label
product and one classifier are held fixed while eight preprocessing decisions are varied in turn, so
that their effects are comparable with each other and with the +0.056 to +0.153 ROC-AUC effect the
models themselves report.

Two decisions turn out to be predictable in advance at no cost. Whether the choice of compositing
chain can move a result at all is decided by scenes per distinct acquisition date, which is 2.0 in
two regions and 1.0 in two others; where it is 1.0 the two chains produce identical rasters and every
boundary estimate is exactly zero. Whether sea contaminates a scene-fitted dryness index is decided
by the area's water fraction and by where the modelled population sits in the index's binning
variable; here the contamination is real, with dry edges of 28.8 to 29.9 °C in a marine area against
49 °C inland, and does not reach the modelled population.

Two provenance splits leave no trace in the outputs. The coarse thermal input is quality-screened in
two regions and unscreened in three, split by export date rather than by design, and the induced
change is not a uniform offset but correlates with elevation at +0.615 in one region. The same three
regions encode sea as exactly 0.0 °C, at 8.1 % and 38.3 % of pixels in two of them and not at all in
the third.

The analysis cell is also not the cell it is called: built by aggregating a fixed count of reference
pixels in a geographic coordinate system, it is 510 m north to south and 390 to 407 m east to west,
17 to 20 % smaller in area than the cell it approximates, so spatial blocking is weaker in longitude
than every block-size label suggests.

Four axes were tested and did not threaten the result, including label omission, which corrects in
the direction opposite to the convenient one. The within-region results rebuild bit for bit on a
different operating system, while cross-region estimates carry a ±0.02 to 0.03 tolerance across
library versions. We close with six items that cost nothing to report and would let a reader judge
most of this budget without repeating any of it.

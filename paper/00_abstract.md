# Abstract



Pre-fire thermal dryness separates a fire year from a normal year, but models built on it are rarely
tested outside the region where they were fitted. Five Mediterranean wildfire regions were analysed
on about 500 m cells, with MCD64A1 labels and spatially blocked validation, adding six thermal
predictors to a terrain, fuel and greenness baseline. The first result is about **evaluation
geometry**: holding the model, its predictors and its fitting fixed and changing only which cells are
scored, moving from the whole region to the burn scar and its 2 km collar costs **0.143 ROC-AUC
[+0.077, +0.208]**, which exceeds the predictor-block increments this literature reports as findings.
A control isolates the cause as the composition of the negative pool rather than class balance:
matching prevalence costs −0.000 [−0.003, +0.002] while substituting fire-adjacent negatives costs
+0.155 [+0.093, +0.217]. Applied between regions the same effect withdrew three of our own claims.
The five study areas enclose very unequal far fields, and restricting each to a 10 km collar, which
drops no burned cells, lifts mean transfer from 0.540 to 0.617, leaves no sign reversal
bootstrap-supported, and makes the surviving agreed direction the opposite of the one dryness
physics predicts, hotter pre-fire surfaces having burned less in every region even within elevation
and greenness strata. Local skill nonetheless does not travel: the thermal block adds +0.056 to
+0.153 within regions under blocked cross-validation but +0.022 [−0.032, +0.077] when a whole burn
scar is withheld and +0.004 [−0.028, +0.036] across twenty transfer directions, with a sign that
varies by pair, while the static baseline transfers no better, at 0.537 against 0.541. Of twenty
candidate diagnostics from five families, none was shown to order transfer: eighteen failed on the
frames as drawn, and the two that succeeded require target labels and become degenerate once the
frames are equalised. Transfer skill has to be measured, not inferred from similarity.

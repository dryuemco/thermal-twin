# Fire selection (pilot, 12 November 2026)

`scan_fires.py` lists large Mediterranean burned-area clusters from MCD64A1 on Earth Engine and writes
`candidates.json`; `make_registry.py` applies the filters and writes `batch_candidates.json` (26 fires) and
`repeat_candidates.json` (3 same-region repeat fires). Both scripts are kept as they were run in the pilot
folder; they write next to themselves and use a fixed Earth Engine project. The rule, with its constants:

1. Search area longitude -10 to 37 and latitude 30 to 46, years 2017 to 2023. Burned MCD64A1 pixels whose
   MCD12Q1 (IGBP) class is natural vegetation (classes 1 to 10) are counted on a 0.1 degree grid.
2. Grid cells with at least 15 such pixels are joined into 8-connected clusters; a cluster with at least 450
   pixels is a candidate (72 candidates).
3. The event of a candidate is the run of burn dates without a gap of more than 5 days that holds most
   pixels; its first date is the anchor. Predictor window: 58 days ending the day before the anchor; label
   window: 49 days from the anchor; rectangle: bounds of the pixels dated in the label window plus 0.15 degree.
4. Filters: anchor in May to October, the event holds at least 90% of the burned pixels of its box, the
   rectangle is at most 1.1 degree on a side (40 candidates pass). Taken largest first, a candidate whose
   rectangle overlaps a study area of the earlier manuscript or a candidate already kept is dropped (26 kept).
   A dropped candidate that overlaps a fire of another year is kept as a repeat fire (3).

# Session handoff, 16 November 2026 (PC)

## Where things stand

- Amendment 14 is in the plan (afeeaf2). Checkpoint 1 is done (b46bf31, plan 14.8): TMA-cell and the R* pre-check
  did not beat R1 by 0.01, so the stopping rule ended the method search.
- The register has the 11.4 timing table (721fcca): every 2024-2026 label file was created after the frozen-score
  push; only the two push times are independent evidence.
- Plan 14.9 and protocol_dev.py (617b0ff) implement checkpoint 2. The run started on 16 November 00:37 local time.
  Its table must NOT be used: the Codex review found label and kernel problems (below). Only the cached pooled
  forest + density rank scores (analysis/tma/dev/protocol_pooled_density_rank.parquet) are reusable.
- Codex reviews of 16 November: docs/scaleup/reviews/codex_20261116_round1.md (novelty, literature) and
  codex_20261116_round2.md (code audit and design). Novelty for EMS: modest, 2-3 of 5. Closest precedents:
  Preisler and Westerling 2007; Preisler et al. 2008 (IJWF 17:305, doi 10.1071/WF06162, spatially smoothed historic
  frequencies as baseline, verified); Moran et al. 2025; Gholami et al. 2021.

## Agreed, to be written as amendment 14.10 before checkpoint 2 is rerun (author said yes on 16 November)

1. G-B scar: the focal label, not every burn of the focal May-April year (also in tma_dev.later()).
2. Future labels independent of later population masks: from the burn-date layers, assigned to May-April years,
   with observation coverage.
3. Wildfire target in G-B: recurrence exclusion at the cut-off only; small-patch filter for future burns.
4. Isotropic 2 km kernel: the grids are EPSG:4326 square-degree cells, so the current kernel is about 2 km N-S and
   1.5 km E-W. One sigma per axis; recompute R1 and every density-based score.
5. G-B primary horizon: complete two years; horizon to 2026 as sensitivity with matched duration. Disclosed as a
   change made after the development G-B results were seen.
6. One declared exception to the stopping rule: a single R1-offset comparator (Platt R1 logit + penalised local
   environmental correction, penalty out of group), fixed before it runs, no follow-up tuning.
7. Honesty: cluster-bootstrap intervals; the G-B estimate from one-year AUC named as a proxy.
8. Names: "standard spatial" is persistent-only; R0 is recalibrated site climatology.
9. EFFIS as external validation (mainly G-C, 100 ha and more): feasibility audit on development data, frozen
   before the blind labels are opened.
10. Land cover: primary analysis called retrospective; fixed-2001 sensitivity (13.10).
11. Wording: "for the development-selected model the upper 95% limit of the AUC gain was below 0.01".

## Open question for the next session: the method

The diagnosis is the solid part: G1/G2 rules met and replicated on unseen 2024-2026 labels (11.4). The G1/G2/11.4
code uses the focal label and its own coverage-masked future export, so the label problems above do not touch it.
The weak point is the method: nothing built so far adds to 2 km burn density. Directions to discuss:

- R1 as the prior and environment as a correction (item 6), the first test of "value beyond density".
- Where versus when (Preisler et al. 2008: weather beat smoothed history in time): density for the spatial
  ranking, seasonal weather/fuel anomalies for the yearly level; shows up in BSS/LSS, not in within-site AUC.
- Fuel recovery: time since last burn interacting with density (reburn relative risk 6.3 in frequently burned
  cells, but fuel deficit right after a fire).
- Large summer events (G-C), where weather and fuel may matter more than history.

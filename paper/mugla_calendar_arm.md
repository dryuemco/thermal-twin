# The calendar-matched Muğla 2022 arm cannot be run, and why

The manuscript has been calling a calendar-matched 2022 arm "the single most valuable follow-up this
paper can name". With Earth Engine access obtained on 2026-08-14, the question was settled before any
export: **it is not a missing analysis, it is an impossible one.** Year and seasonal phase cannot be
separated inside Muğla by any choice of window.

Measured with `MODIS/061/MCD64A1` over `MUGLA_AOI_BBOX` (27.10, 36.60, 28.90, 37.45) at the product's
native scale, and against the frozen label rasters in the export.

## 1. The two events sit 42 days apart in seasonal phase

Read from each experiment's own frozen `validation/labels/mcd64a1_raw.tif`:

| Event | Positive sub-pixels | Burn day-of-year | Median | Busiest days |
|---|---:|---|---:|---|
| Muğla 2021 | 759,212 | 210 to 235 | **215** (3 August) | DOY 217 (21 %), 213 (15 %), 214 (11 %) |
| Muğla 2022 (event-relative) | 76,752 | 172 to 198 | **173** (22 June) | DOY 173 (50 %), 174 (27 %) |

The 2021 event is a high-summer fire and the 2022 event is a late-spring one, and the gap between
their medians is 42 days. That is the confound Section 5.2 describes.

## 2. Holding the calendar fixed at 2021's window leaves nothing to model

The registry's superseded `mugla_2022` record is exactly the calendar-shifted formulation: 2021's
windows moved forward one year, label window 2022-07-29 to 2022-09-15. Counting burned pixels in
that window:

| Window | Burned 500 m pixels |
|---|---:|
| 2021 label window, DOY 210 to 258 | 3,181 |
| **2022, same calendar window, DOY 210 to 258** | **9** |
| 2022 event-relative window, DOY 172 to 220 | 319 |

The count is validated against two frozen numbers: 3,181 pixels against `mugla_2021`'s 3,073 physical
burned cells, and 319 against `mugla_2022_event_relative`'s gate `burned_count` of 332, so the
reconstruction ratio is 0.97 and 1.04 cells per pixel respectively. The calendar-matched arm would
therefore carry about **nine burned cells**, against a gate minimum of 30
(`STEP6_BURNED_LANDCOVER_GATE_MIN_POSITIVES`) and a modelling minimum of 30 positives in the primary
population after the natural-vegetation mask and the pre-label exclusion.

## 3. Nor does the mirror pairing work

The obvious alternative is to hold the season at the 2022 event's phase and move 2021 there instead.
It fails for the same reason in reverse. Muğla 2021 on the window DOY 172 to 220 returns 3,127 burned
pixels, but those are not a late-spring event: they are the same late-July fire, caught because that
window runs to 8 August. The whole of 2021 in this AOI is 3,206 pixels and the whole of 2022 is 358,
so 2022 simply contains no high-summer event to pair with 2021's, and 2021 contains no late-spring
event to pair with 2022's.

## 4. What follows for the paper

Sections 5.2 and 5.11(ii) should no longer describe this as an analysis that was not run. The
separation of year from seasonal phase is **not obtainable from Muğla**, and the reason is a property
of the fire record rather than of the design or of the effort available. Obtaining it requires a
region with two events at a matching seasonal phase in different years, which no region in this
cohort has: each contributes one fire season, which is limitation (vi) already.

This does not change the reading of Section 4.8. It changes the status of the caveat attached to it,
from a gap that a further run would close to a limit of what this study area can answer.

## Provenance

`paper/mugla_calendar_arm.json`. Queries executed 2026-08-14 against Earth Engine project
`thermaltwin` with `earthengine-api` 1.7.34; frozen comparators are
`drive_new/experiments/mugla_2021/validation/labels/mcd64a1_raw.tif`, the same file for
`mugla_2022_event_relative`, and each region's `burned_landcover_gate.json`. One methodological note
for anyone repeating this: MCD64A1 is a monthly composite stamped at the first of the month, so
filtering the collection by the analysis window's own dates silently drops the composite of the month
the window opens in. The first run of this probe did that and undercounted the June 2022 event by a
factor of eight. The collection must be filtered by whole months and the day-of-year mask left to do
the selection.

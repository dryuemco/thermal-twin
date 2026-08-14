"""
Corrected feasibility probe.

MCD64A1 is a monthly composite stamped at the first of the month, and its BurnDate
band carries a day-of-year. Filtering the collection by the window's own dates
drops the composite of the month the window opens in, which is where most of an
event that ignites mid-month lives. The first attempt did exactly that and
undercounted the 21 June 2022 event by an order of magnitude.

Here the collection is filtered by whole months spanning the window, and the
day-of-year mask does the real selection.
"""
import ee

PROJECT = "thermaltwin"
BBOX = [27.10, 36.60, 28.90, 37.45]
SCALE = 463.3127165275

ee.Initialize(project=PROJECT)
aoi = ee.Geometry.Rectangle(BBOX)


def burned(y, m0, d0, m1, d1, label):
    start = ee.Date.fromYMD(y, m0, d0)
    end = ee.Date.fromYMD(y, m1, d1)
    doy0 = int(start.getRelative("day", "year").getInfo()) + 1
    doy1 = int(end.getRelative("day", "year").getInfo()) + 1
    # whole months covering the window, so no composite is lost
    col = (ee.ImageCollection("MODIS/061/MCD64A1")
           .filterDate(ee.Date.fromYMD(y, m0, 1), ee.Date.fromYMD(y, m1, 1).advance(1, "month"))
           .select("BurnDate"))
    n = col.size().getInfo()
    mask = col.map(lambda im: im.gte(doy0).And(im.lte(doy1))).max().unmask(0)
    s = mask.reduceRegion(ee.Reducer.sum(), aoi, SCALE, maxPixels=int(1e9)).getInfo()["BurnDate"]
    print(f"{label:<50} images={n}  DOY {doy0}-{doy1}  burned 500 m pixels = {int(s):,}")
    return int(s)


print("Mugla AOI, MCD64A1 burned pixels, whole-month collection filter")
print("=" * 100)
a = burned(2021, 7, 29, 9, 15, "2021 label window (canonical mugla_2021)")
b = burned(2022, 7, 29, 9, 15, "2022 SAME CALENDAR window (the arm 5.2 asks for)")
c = burned(2022, 6, 21, 8, 8, "2022 event-relative window (the arm in the paper)")
print("=" * 100)
print()
print("Known frozen counts on the reconstructed grid, for scale:")
print("  mugla_2021 physical burned cells            3,073")
print("  mugla_2022_event_relative gate burned_count   332")
print()
if c:
    print(f"reconstruction ratio, 2021: {3073/a:.2f} cells per MCD64A1 pixel")
    print(f"reconstruction ratio, 2022 event-relative: {332/c:.2f}")
    print(f"-> calendar-matched arm would give roughly {b*3073/a:.0f} to {b*332/c:.0f} burned cells")
print()
print("Gate minimum is 30 burned cells; step8b needs 30 positives in the primary")
print("population after the natural-vegetation mask and the pre-label exclusion.")

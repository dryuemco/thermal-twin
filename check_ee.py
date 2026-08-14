"""
Earth Engine readiness check.

Run after `earthengine authenticate`. Reports, in order, exactly which step is
missing, so there is no guessing about what to fix next.

    .\.venv-step10\Scripts\python.exe check_ee.py
"""
import sys
from pathlib import Path

CRED = Path.home() / ".config" / "earthengine" / "credentials"
PROJECT = "b7-thermal-digital-twin"   # core/config.py:7, hardcoded there

print("=" * 68)
print("Earth Engine readiness")
print("=" * 68)

# 1. library
try:
    import ee
    print(f"[1/4] earthengine-api installed        OK   (version {ee.__version__})")
except ImportError:
    print("[1/4] earthengine-api installed        MISSING")
    print("      fix: .\\.venv-step10\\Scripts\\python.exe -m pip install earthengine-api==1.7.34")
    sys.exit(1)

# 2. credentials on disk
if CRED.exists():
    print(f"[2/4] credentials file                 OK   ({CRED})")
else:
    print(f"[2/4] credentials file                 MISSING ({CRED})")
    print("      fix: .\\.venv-step10\\Scripts\\earthengine.exe authenticate")
    sys.exit(1)

# 3. can we initialise at all, on any project?
try:
    ee.Initialize(project=PROJECT)
    print(f"[3/4] ee.Initialize(project='{PROJECT}')")
    print("                                       OK")
except Exception as exc:
    msg = str(exc)
    print(f"[3/4] ee.Initialize(project='{PROJECT}')")
    print("                                       FAILED")
    print(f"      {msg[:400]}")
    print()
    low = msg.lower()
    if "not registered" in low or "not signed up" in low or "registration" in low:
        print("      Meaning: your Google account is not registered for Earth Engine.")
        print("      fix: https://code.earthengine.google.com/register  (free for academic use)")
    elif "permission" in low or "403" in low or "caller does not have" in low or "not found" in low:
        print(f"      Meaning: you are authenticated, but your account cannot use the project")
        print(f"      '{PROJECT}'. That is the pipeline author's Cloud project.")
        print("      Two ways forward:")
        print("        (a) ask him to add your account to it as an Earth Engine user, or")
        print("        (b) create your own Cloud project, register it for Earth Engine, and")
        print("            tell me its id; I will pass it explicitly at every call site,")
        print("            since core/config.py is read-only and hardcodes the current one.")
    else:
        print("      Meaning: unrecognised failure. Paste the message above and I will read it.")
    sys.exit(1)

# 4. a real, tiny query against the collection the pending analyses need
try:
    col = ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
    n = col.filterDate("2021-06-01", "2021-06-10").filterBounds(
        ee.Geometry.Rectangle([31.05, 36.72, 31.85, 37.35])).size().getInfo()
    print(f"[4/4] query LANDSAT/LC08/C02/T1_L2     OK   ({n} scenes over Manavgat, 1 to 10 June 2021)")
    print()
    print("Everything the two pending analyses need is in place.")
    print("  - calendar-matched Mugla 2022 arm")
    print("  - Landsat compositing A/B for a second region")
except Exception as exc:
    print("[4/4] query LANDSAT/LC08/C02/T1_L2     FAILED")
    print(f"      {str(exc)[:400]}")
    print()
    print("      Authentication works but the data request did not. Usually this means")
    print("      the Earth Engine API is not enabled on the project. Paste the message.")
    sys.exit(1)

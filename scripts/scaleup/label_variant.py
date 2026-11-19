"""Shared file naming and QA mask for the Amendment 15 label variants."""
import os
from pathlib import Path

SUFFIX = os.environ.get("THERMAL_TWIN_LABEL_SUFFIX", "")
if SUFFIX not in ("", "_qa1"):
    raise SystemExit("THERMAL_TWIN_LABEL_SUFFIX must be empty or '_qa1'")

QA_MASK = 2 if SUFFIX else 1


def variant_name(name):
    path = Path(name)
    return f"{path.stem}{SUFFIX}{path.suffix}"

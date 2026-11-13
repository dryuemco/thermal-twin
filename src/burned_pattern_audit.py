"""Generic, multi-experiment burned-area spatial-structure and descriptive
comparison audit ("the advisor's third diagnostic").

Scientific purpose
===================
For every resolved experiment, describes the frozen canonical Step8A
500 m modeling dataset's burned cells purely DESCRIPTIVELY:
    - number of 8-neighbour spatially connected burned-cell components
      ("spatially connected burned-cell components" -- NEVER "number of
      fires"; see LIMITATIONS below);
    - component/patch cell-count size distribution;
    - burned-cell elevation distribution;
    - burned-cell land-cover composition (reusing the canonical ESA
      WorldCover mapping already defined in
      src/step8a_prepare_500m_modeling_dataset.py).

This module:
    - NEVER fits a model, computes transfer performance, or reruns
      Step9/Step9G/Step10;
    - NEVER modifies Step8A (read-only input);
    - NEVER hard-codes an experiment ID, AOI name, or region -- every
      public function takes `experiment_id` as an ordinary string and
      resolves paths/registry membership through core.regions only;
    - is order-invariant: the analysis ID for a multi-experiment
      comparison does not depend on the order experiment IDs were
      supplied in.

LIMITATIONS (must appear in every generated report):
    "Connected components are a spatial fragmentation proxy. They must
    not be interpreted as a definitive count of independent wildfire
    events, because one event may appear as multiple disconnected
    components and multiple events may be spatially connected at the
    analysis resolution."
Additional limitations recorded in every manifest/report:
    - connected-component count is resolution-dependent;
    - results are sensitive to AOI clipping;
    - MCD64A1-scale cells are approximate spatial units;
    - component count is not a definitive fire-event count;
    - results are descriptive and do not explain transfer causally.
"""
from __future__ import annotations

import importlib.metadata
import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

from core.config import STEP8A_MCD64A1_NATIVE_CELL_SIZE_M
from core.paths import PROJECT_ROOT
from core.pipeline_orchestrator import LEGACY_EXPERIMENT_ID  # noqa: F401  (re-exported for callers/tests)
from core.regions import (
    VARIANT_STATUS_CANONICAL,
    VARIANT_STATUS_LEGACY_SUPERSEDED,
    get_experiment,
    get_experiment_output_root,
    list_experiments,
    validate_variant_record,
)
from src.step8_large_block_robustness import (
    _git_commit,
    canonical_json,
    sha256_bytes,
    sha256_file,
)
from src.step8a_prepare_500m_modeling_dataset import ESA_WORLDCOVER_CLASSES

# =============================================================================
# Frozen scientific/schema constants
# =============================================================================
ANALYSIS_SCHEMA_VERSION = "burned_pattern_audit.v2"

REQUIRED_COLUMNS = ("burned", "row_500m", "col_500m", "elevation_mean", "landcover_dominant")
OPTIONAL_COLUMNS = ("burn_date", "experiment_id", "region_key")

# Roles that are registered and canonical but are NOT part of a
# natural-vegetation burned-pattern cohort. Discovery mode (--all-enabled)
# reports them as excluded with this reason instead of silently dropping
# them; explicit --experiments selection of such an experiment is still
# honoured unchanged. Role-based, never ID-based: no real experiment_id
# appears anywhere in this module.
#
#   negative_control          cropland/stubble-burning control AOI; not a
#                             natural-vegetation wildfire population.
#   temporal_transfer_wildfire  same AOI as an existing cohort member, only
#                             the year differs. This cohort compares burned
#                             PATTERNS ACROSS SPACE, so admitting a second
#                             year of the SAME geography would silently make
#                             the comparison partly temporal and reuse one
#                             AOI twice. Such an experiment is still fully
#                             auditable via explicit --experiments selection.
#   scaleup_wildfire          fires of the November 2026 scale-up run
#                             (core.regions.SCALEUP_EXPERIMENT_IDS); analysed by
#                             their own scripts, kept out of the five-AOI cohort.
NON_COHORT_ROLES = ("negative_control", "temporal_transfer_wildfire", "scaleup_wildfire")

# Reused, UNMODIFIED, exact existing Step8 natural-vegetation population
# mask column (src/step8a_prepare_500m_modeling_dataset.py). This module
# does NOT recompute it from landcover_dominant/fractions.
BURNABLE_MASK_COLUMN = "burnable_tree_shrub_grass"

# Reused, UNMODIFIED, exact existing Step8B final-model row-eligibility flag
# (predictor validity AND label validity) as already materialised in the
# canonical Step8A dataset. Used ONLY by the third, advisor-specific
# final-model-population morphology comparison below; never recomputed, and
# never applied to the primary or natural-vegetation populations.
VALID_FOR_MODELING_COLUMN = "valid_for_modeling"

# Canonical LABEL-analysis eligibility mask, already computed by Step8A
# (src/step8a_prepare_500m_modeling_dataset.py: `analysis_eligible =
# not pre_label_burn_excluded`) and surfaced by Step8E's final report.
# This is DISTINCT from Step8B's stricter `valid_for_modeling` (which also
# requires predictor validity -- irrelevant to burned-label spatial
# structure). A cell burned BEFORE an experiment's label_start (a separate
# fire that falls inside that experiment's predictor window, configured
# per-experiment via exclude_pre_label_burns in core/regions.py) is never
# eligible for the burned label analysis universe, regardless of its raw
# `burned` value. Reused
# verbatim, never recomputed here. Experiments with no pre-label exclusion
# configured (exclude_pre_label_burns unset) simply lack this column, in
# which case every row is eligible by construction.
ANALYSIS_ELIGIBLE_COLUMN = "analysis_eligible"
PRE_LABEL_EXCLUDED_COLUMN = "pre_label_burn_excluded"

POPULATION_ALL_VALID_BURNED = "all_valid_burned"
POPULATION_BURNABLE_TSG_BURNED = "burnable_tree_shrub_grass_burned"
POPULATION_BURNABLE_TSG_VALID_MODEL_BURNED = "burnable_tree_shrub_grass_valid_for_modeling_burned"
POPULATIONS = (
    POPULATION_ALL_VALID_BURNED,
    POPULATION_BURNABLE_TSG_BURNED,
    POPULATION_BURNABLE_TSG_VALID_MODEL_BURNED,
)

POPULATION_DEFINITIONS = {
    POPULATION_ALL_VALID_BURNED: (
        "Canonical event-footprint population: Step8A rows that are "
        f"canonical-analysis-eligible (Step8A '{ANALYSIS_ELIGIBLE_COLUMN}' "
        "column, i.e. NOT pre-label-burn-excluded -- see "
        "resolve_analysis_eligible_mask) with burned == 1 and valid "
        "(non-null) row_500m/col_500m grid coordinates. No land-cover "
        "restriction. Primary population for component count, patch-size "
        "distribution, elevation distribution, and land-cover composition."
    ),
    POPULATION_BURNABLE_TSG_BURNED: (
        f"Natural-vegetation sensitivity population: the corrected primary "
        f"population further restricted to rows where the existing Step8A "
        f"'{BURNABLE_MASK_COLUMN}' boolean column is True. That frozen Step8A "
        f"column is a COMBINED per-cell fraction rule -- "
        f"(landcover_tree_cover_fraction + landcover_shrubland_fraction + "
        f"landcover_grassland_fraction) >= burnable_threshold "
        f"(STEP8A_BURNABLE_FRACTION_THRESHOLD) -- already computed in Step8A "
        f"and reused verbatim here, never recomputed. It is NOT a "
        f"dominant-land-cover selection: the 'landcover_dominant' column is "
        f"no part of the selection rule (it is used only for descriptive "
        f"land-cover composition reporting). A cell therefore qualifies "
        f"whenever the three fractions SUM to at least the threshold even if "
        f"its single dominant class is cropland/bare/other, and a cell whose "
        f"dominant class is tree, shrubland or grassland is excluded if that "
        f"sum falls below the threshold. Reported as a sensitivity analysis, "
        f"never substituted for the primary population."
    ),
    POPULATION_BURNABLE_TSG_VALID_MODEL_BURNED: (
        f"Advisor-specific final-model-population morphology comparison. "
        f"Selection contract, all conditions required simultaneously: "
        f"{ANALYSIS_ELIGIBLE_COLUMN} == True AND "
        f"{VALID_FOR_MODELING_COLUMN} == True AND "
        f"{BURNABLE_MASK_COLUMN} == True AND burned == 1 AND non-null "
        f"row_500m/col_500m. Both Step8A boolean columns are reused verbatim "
        f"and never recomputed here (see the "
        f"{POPULATION_BURNABLE_TSG_BURNED} definition for the combined "
        f"fraction rule behind '{BURNABLE_MASK_COLUMN}'). This population "
        f"describes the morphology of the rows that actually reach the final "
        f"model; it is an ADDITIONAL comparison only and does NOT replace, "
        f"redefine, or otherwise alter the '{POPULATION_ALL_VALID_BURNED}' "
        f"primary population or the '{POPULATION_BURNABLE_TSG_BURNED}' "
        f"sensitivity population."
    ),
}

# Frozen 8-neighbour raster connectivity. Not selected post hoc.
CONNECTIVITY_DEFINITION = {
    "name": "8_neighbour_raster_adjacency",
    "rule": "abs(delta_row) <= 1 and abs(delta_col) <= 1, excluding the cell itself",
    "neighbour_offsets": [
        [dr, dc]
        for dr in (-1, 0, 1)
        for dc in (-1, 0, 1)
        if not (dr == 0 and dc == 0)
    ],
    "frozen": True,
}
_NEIGHBOUR_OFFSETS = tuple(tuple(o) for o in CONNECTIVITY_DEFINITION["neighbour_offsets"])

LANDCOVER_MAPPING_SOURCE = "src.step8a_prepare_500m_modeling_dataset.ESA_WORLDCOVER_CLASSES"

# Provenance for the derived approximate per-cell area (never assumed
# without a documented source): core/config.py's own comment records that
# this is an approximation of the true native MODIS sinusoidal grid,
# anchored to the 30 m reference predictor grid.
CELL_AREA_KM2_SOURCE = (
    "core.config.STEP8A_MCD64A1_NATIVE_CELL_SIZE_M (documented as an "
    "APPROXIMATION of the true native MCD64A1 sinusoidal-grid cell size, "
    "anchored to the Landsat/EPSG:4326 30 m reference predictor grid -- "
    "see src/step8a_prepare_500m_modeling_dataset.py module docstring)."
)
APPROXIMATE_CELL_AREA_KM2 = (STEP8A_MCD64A1_NATIVE_CELL_SIZE_M / 1000.0) ** 2

SCIENTIFIC_LIMITATIONS = (
    "Connected components are a spatial fragmentation proxy. They must not "
    "be interpreted as a definitive count of independent wildfire events, "
    "because one event may appear as multiple disconnected components and "
    "multiple events may be spatially connected at the analysis resolution.",
    "Connected-component count is resolution-dependent (8-neighbour "
    "adjacency on the fixed 500 m Step8A grid); a coarser or finer grid "
    "would yield a different count for the same physical burned area.",
    "Results are sensitive to AOI clipping: a component that would be "
    "contiguous in a wider AOI can appear split, or vice versa, purely "
    "because of where the analysis extent was drawn.",
    "MCD64A1-scale cells are approximate spatial units, not exact "
    "ground-truth footprints (see CELL_AREA_KM2_SOURCE provenance).",
    "Component count is not a definitive fire-event count.",
    "Results are descriptive and do not explain cross-region transfer "
    "performance causally.",
)

PROHIBITED_ACTIONS = (
    "fit any model",
    "calculate transfer performance",
    "modify Step8A",
    "use target-label adaptation",
    "rerun Step9 or Step10",
    "call components confirmed independent fire events",
    "claim causality",
    "claim statistical significance",
    "choose a population or connectivity based on favorable results",
)

# Selection modes. "explicit_superseded_sensitivity" marks the ONLY selection
# in which a superseded legacy variant is permitted, and only alongside its
# canonical successor -- see resolve_experiments().
SELECTION_MODE_EXPLICIT = "explicit"
SELECTION_MODE_EXPLICIT_SUPERSEDED_SENSITIVITY = "explicit_superseded_sensitivity"
SELECTION_MODE_ALL_ENABLED = "all_enabled"

# Recorded verbatim in every artifact produced by a permitted legacy-variant
# selection, so no downstream reader can mistake it for cohort restoration.
SUPERSEDED_SENSITIVITY_NOTE = (
    "This selection deliberately includes a superseded legacy AOI variant "
    "ONLY as an explicitly permitted AOI-definition sensitivity comparator "
    "against its canonical successor (--allow-superseded-sensitivity). The "
    "legacy experiment is NOT restored to the canonical cohort: --all-enabled "
    "discovery still excludes it, the default explicit selection still "
    "refuses it, and no registry record, frozen output, or canonical "
    "comparison matrix is changed by this run. The comparison is descriptive "
    "AOI-definition sensitivity only -- it is not a model, a transfer result, "
    "or evidence that either AOI definition is correct."
)

#: The ONE canonical output root of this analysis family. Every other path in
#: this module is derived from it through `resolve_layout()`; no output path
#: string is spelled out a second time here or in the runner.
OUTPUT_ROOT = PROJECT_ROOT / "outputs" / "diagnostics" / "burned_pattern_audit"

#: Legacy FLAT layout, kept as the default for direct calls to
#: `analyze_experiment()` / `run_comparison()` so existing programmatic callers
#: and their monkeypatches keep working unchanged.
EXPERIMENTS_OUTPUT_ROOT = OUTPUT_ROOT / "experiments"
COMPARISON_OUTPUT_DIR = OUTPUT_ROOT / "comparison"


@dataclass(frozen=True)
class AuditLayout:
    """Resolved output paths for one run. The single path authority.

    Different analysis SCOPES (a five-AOI cohort run, a two-AOI sensitivity
    pair, ...) get their own namespace UNDER `root` instead of their own
    sibling root next to it. Sibling roots are what produced
    `burned_pattern_audit_mugla_2021__mugla_2022_event_relative/` and the
    hand-renamed `*_archive_*` directories: with no `--output-root` and a
    hardcoded default, preserving a previous result meant renaming the whole
    root by hand, and a second scope silently overwrote per-experiment
    outputs inside the first one's root.
    """

    root: Path
    experiments: Path
    comparison: Path
    scope: Optional[str] = None


def default_layout() -> AuditLayout:
    """The legacy flat layout, read from the module constants.

    Reads the constants at call time so an existing test that patches
    `EXPERIMENTS_OUTPUT_ROOT` / `COMPARISON_OUTPUT_DIR` still governs.
    """
    return AuditLayout(
        root=OUTPUT_ROOT,
        experiments=EXPERIMENTS_OUTPUT_ROOT,
        comparison=COMPARISON_OUTPUT_DIR,
        scope=None,
    )


def canonical_cohort_ids() -> tuple[str, ...]:
    """The experiment set `--all-enabled` currently resolves to, sorted.

    Derived from the registry through the same resolver the CLI uses, so a
    superseded, disabled, negative-control or otherwise non-cohort experiment
    can never enter it. Returns an empty tuple when the cohort cannot be
    resolved, which makes `scope_key` fall back to the explicit name rather
    than guess.
    """
    try:
        return tuple(sorted(resolve_experiments(all_enabled=True).resolved_ids))
    except BaseException:
        return ()


def scope_key(resolution: "ExperimentResolution") -> str:
    """Deterministic namespace name for one analysis scope.

    A selection that resolves to exactly the current `--all-enabled` cohort is
    named `all_enabled` NO MATTER how it was requested. Without this, naming
    the five canonical AOIs explicitly would create a second namespace holding
    scientifically identical content -- the same duplication the scoped layout
    exists to prevent. Comparison is set-based, so ordering is irrelevant.

    A genuine subset (or any selection including a superseded AOI) keeps its
    own deterministic name built from its sorted experiment IDs.
    """
    if resolution.selection_mode == "all_enabled":
        return "all_enabled"
    resolved = tuple(sorted(resolution.resolved_ids))
    canonical = canonical_cohort_ids()
    if canonical and resolved == canonical:
        return "all_enabled"
    return "__".join(resolved)


def resolve_layout(
    output_root: Optional[Path] = None, scope: Optional[str] = None,
) -> AuditLayout:
    """Resolve the output layout for a run. The ONLY place paths are built.

    `output_root=None, scope=None` reproduces the legacy flat layout exactly.
    """
    if output_root is None and scope is None:
        return default_layout()
    # The implicit base is the PARENT of the legacy experiments directory, not
    # `OUTPUT_ROOT`. In production the two are the same path, but callers that
    # redirect this analysis (tests, alternative namespaces) override the leaf
    # constants; deriving from `OUTPUT_ROOT` would silently escape their
    # sandbox and write into the real canonical root.
    base = Path(output_root) if output_root is not None else EXPERIMENTS_OUTPUT_ROOT.parent
    namespace = base / scope if scope else base
    return AuditLayout(
        root=base,
        experiments=namespace / "experiments",
        comparison=namespace / "comparison",
        scope=scope,
    )

STEP8A_RELATIVE_PATH = Path("step8a") / "step8a_500m_modeling_dataset.parquet"

# Canonical burned-landcover gate (src/step6b_burned_landcover_gate.py
# output), read-only, used ONLY to cross-validate this audit's analysis
# universe / burned count / pre-label-excluded count -- never joined,
# regenerated, or reinterpreted.
GATE_RELATIVE_PATH = Path("validation") / "labels" / "burned_landcover_gate.json"


class BurnedPatternAuditError(SystemExit):
    """Fail-fast error for the burned-pattern audit (same convention as
    other frozen/generic analysis modules in this repo)."""


# =============================================================================
# Experiment resolution (registry-driven; no directory scanning, no
# hard-coded experiment IDs anywhere in this module).
# =============================================================================
@dataclass(frozen=True)
class ExperimentResolution:
    requested_ids: tuple[str, ...]
    resolved_ids: tuple[str, ...]
    selection_mode: str
    excluded: dict[str, str] = field(default_factory=dict)
    # Backward-compatible defaults: every existing caller (including
    # src/domain_classifier_audit.py, which imports this resolver) keeps the
    # exact previous behaviour without passing or reading these.
    allow_superseded_sensitivity: bool = False
    superseded_pairs: tuple[tuple[str, str], ...] = ()


def canonical_step8a_path(experiment_id: str) -> Path:
    """`outputs/experiments/<output_namespace>/step8a/...` for `experiment_id`.

    Raises ValueError (via core.regions.get_experiment_output_root) if
    `experiment_id` is not a known registry entry.
    """
    return get_experiment_output_root(experiment_id) / STEP8A_RELATIVE_PATH


def canonical_gate_path(experiment_id: str) -> Path:
    """`outputs/experiments/<output_namespace>/validation/labels/burned_landcover_gate.json`
    for `experiment_id`. May not exist for every experiment (older Step6B
    runs); callers must treat absence as "gate unavailable", not an error."""
    return get_experiment_output_root(experiment_id) / GATE_RELATIVE_PATH


def resolve_analysis_eligible_mask(df: pd.DataFrame) -> pd.Series:
    """The canonical label-analysis eligibility mask already computed by
    Step8A (see ANALYSIS_ELIGIBLE_COLUMN docstring above). Falls back to
    "every row eligible" when the column is absent, which is exactly
    correct for any experiment without exclude_pre_label_burns configured
    -- no experiment name is branched on here."""
    if ANALYSIS_ELIGIBLE_COLUMN in df.columns:
        return df[ANALYSIS_ELIGIBLE_COLUMN].astype(bool)
    return pd.Series(True, index=df.index)


def gate_provenance(experiment_id: str) -> dict[str, Any]:
    """Read-only provenance snapshot of the canonical burned-landcover gate
    (path, SHA-256, exclusion rule), independent of any cross-validation."""
    path = canonical_gate_path(experiment_id)
    if not path.is_file():
        return {
            "gate_available": False,
            "gate_path": str(path),
            "gate_sha256": None,
            "pre_label_burn_exclusion_rule": None,
        }
    gate = json.loads(path.read_text())
    return {
        "gate_available": True,
        "gate_path": str(path),
        "gate_sha256": sha256_file(path),
        "pre_label_burn_exclusion_rule": gate.get("pre_label_burn_exclusion_rule"),
    }


def validate_against_gate(
    experiment_id: str,
    df: pd.DataFrame,
    analysis_eligible_mask: pd.Series,
    corrected_burned_count: int,
) -> dict[str, Any]:
    """Cross-validate the audit's corrected analysis universe / burned
    count / pre-label-excluded count against the canonical burned-landcover
    gate (when available). Raises BurnedPatternAuditError on any
    disagreement -- called BEFORE any output is written. Never joins,
    modifies, or regenerates the gate or Step8A; read-only comparison only.
    """
    provenance = gate_provenance(experiment_id)
    pre_label_excluded_count = (
        int((df[PRE_LABEL_EXCLUDED_COLUMN] == True).sum())  # noqa: E712
        if PRE_LABEL_EXCLUDED_COLUMN in df.columns else 0
    )
    provenance["pre_label_burn_excluded_count"] = pre_label_excluded_count
    provenance["validated"] = False

    if not provenance["gate_available"]:
        return provenance

    gate = json.loads(Path(provenance["gate_path"]).read_text())
    analysis_universe_gate = gate.get("analysis_universe_cells_after_exclusions")
    if analysis_universe_gate is None:
        analysis_universe_gate = gate.get("total_valid_cells_or_pixels_considered")
    analysis_universe_audit = int(analysis_eligible_mask.sum())
    if analysis_universe_gate is not None and int(analysis_universe_gate) != analysis_universe_audit:
        raise BurnedPatternAuditError(
            f"'{experiment_id}': audit analysis universe ({analysis_universe_audit}) disagrees "
            f"with canonical gate analysis universe ({analysis_universe_gate}) at "
            f"{provenance['gate_path']}."
        )

    burned_count_gate = gate.get("burned_count")
    if burned_count_gate is not None and int(burned_count_gate) != int(corrected_burned_count):
        raise BurnedPatternAuditError(
            f"'{experiment_id}': audit burned-cell count ({corrected_burned_count}) disagrees "
            f"with canonical gate burned_count ({burned_count_gate}) at {provenance['gate_path']}."
        )

    excluded_count_gate = gate.get("pre_label_burn_excluded_count")
    if excluded_count_gate is not None and int(excluded_count_gate) != pre_label_excluded_count:
        raise BurnedPatternAuditError(
            f"'{experiment_id}': audit pre-label-excluded count ({pre_label_excluded_count}) "
            f"disagrees with canonical gate pre_label_burn_excluded_count ({excluded_count_gate}) "
            f"at {provenance['gate_path']}."
        )

    provenance["analysis_universe_cells_gate"] = analysis_universe_gate
    provenance["burned_count_gate"] = burned_count_gate
    provenance["validated"] = True
    return provenance


def resolve_experiments(
    experiments: Optional[list[str]] = None,
    all_enabled: bool = False,
    allow_superseded_sensitivity: bool = False,
) -> ExperimentResolution:
    """Resolve the experiment ID set for this audit.

    Exactly one of `experiments` / `all_enabled` must be given.

    - explicit `experiments`: every ID must exist in the registry
      (core.regions.get_experiment), must NOT be a superseded legacy
      variant, and must have a canonical Step8A dataset on disk; missing
      input fails clearly (no silent skip). A superseded ID also fails
      closed, naming its successor -- it is never quietly dropped, because
      dropping it would silently change the requested cohort.
    - `all_enabled=True`: resolves every enabled registry experiment whose
      variant_status is "canonical" and whose role is a cohort role, then
      keeps only those with a canonical Step8A dataset present. Each
      dropped experiment is recorded in `excluded` with a machine-readable
      reason, never raised as an error:
          superseded_by_<successor>            legacy AOI variant
          negative_control                     canonical, non-cohort role
          temporal_transfer_wildfire           canonical, non-cohort role
          missing_canonical_step8a_dataset:... has not reached Step8A yet
      The reasons are checked in that order, so a legacy variant is
      reported as legacy even if its Step8A output is absent.

    Both branches are shared verbatim by src/domain_classifier_audit.py,
    which imports this resolver rather than filtering in parallel.

    `allow_superseded_sensitivity` (default False -- every existing caller,
    including src/domain_classifier_audit.py, keeps the exact previous
    behaviour) narrowly permits ONE thing: pairing a superseded legacy AOI
    variant with its canonical successor as a descriptive AOI-definition
    sensitivity comparison. It is fail-closed in every other direction:
        * with `all_enabled=True` it is an error, never a filter change --
          the discovery cohort is exactly what it was before;
        * a permitted superseded ID must have its registry `superseded_by`
          successor present in the SAME explicit request, and that successor
          must itself validate as a canonical variant;
        * requesting the permission without any superseded ID in the
          selection is an error, so an unnecessary special permission can
          never be granted silently;
        * `--force` never reaches this decision: it only governs overwriting
          outputs whose analysis_id differs, long after resolution.
    A permitted selection is reported as
    selection_mode="explicit_superseded_sensitivity" and carries the
    (superseded, successor) pairs, so every downstream artifact records that
    the legacy variant was a comparator, not a cohort member.
    """
    if bool(experiments) == bool(all_enabled):
        raise BurnedPatternAuditError(
            "Exactly one of --experiments or --all-enabled must be given "
            f"(got experiments={experiments!r}, all_enabled={all_enabled!r})."
        )

    # (A) The permission is meaningless for discovery and must never be able
    # to widen the canonical cohort, so it is rejected outright rather than
    # ignored.
    if all_enabled and allow_superseded_sensitivity:
        raise BurnedPatternAuditError(
            "--allow-superseded-sensitivity cannot be combined with "
            "--all-enabled: the discovery cohort is canonical-only by "
            "definition and a superseded legacy variant is never restored to "
            "it. Request the legacy variant and its canonical successor "
            "explicitly with --experiments instead."
        )

    if experiments:
        if len(experiments) != len(set(experiments)):
            seen: dict[str, int] = {}
            for entry in experiments:
                seen[entry] = seen.get(entry, 0) + 1
            duplicates = sorted(k for k, v in seen.items() if v > 1)
            raise BurnedPatternAuditError(f"Duplicate --experiments entries are not allowed: {duplicates}.")
        requested = tuple(experiments)
        requested_set = set(requested)
        superseded_pairs: list[tuple[str, str]] = []
        for experiment_id in requested:
            record = get_experiment(experiment_id)  # raises ValueError if unknown
            # Fail closed on superseded legacy variants BEFORE touching disk,
            # so the error names the successor instead of a confusing
            # missing-input message. Explicit selection of a canonical
            # negative-control experiment stays allowed and unchanged.
            status = validate_variant_record(record, experiment_id)
            if status == VARIANT_STATUS_LEGACY_SUPERSEDED:
                # (B) DEFAULT behaviour, unchanged verbatim.
                if not allow_superseded_sensitivity:
                    raise BurnedPatternAuditError(
                        f"burned-pattern audit --experiments: refusing superseded experiment "
                        f"'{experiment_id}' (superseded_by='{record['superseded_by']}'). "
                        "Only canonical experiments may enter a new selection; a superseded "
                        "ID is never silently dropped. Legacy outputs stay on disk and are "
                        "never deleted. Use the successor experiment_id instead."
                    )
                successor_id = record["superseded_by"]
                if successor_id not in requested_set:
                    raise BurnedPatternAuditError(
                        f"--allow-superseded-sensitivity: superseded experiment "
                        f"'{experiment_id}' may only be audited as an AOI-definition "
                        f"sensitivity comparator against its canonical successor, but "
                        f"'{successor_id}' (its registry superseded_by target) is not in "
                        f"the requested selection {sorted(requested_set)}. Request both "
                        "experiment IDs together."
                    )
                successor_record = get_experiment(successor_id)  # raises ValueError if unknown
                successor_status = validate_variant_record(successor_record, successor_id)
                if successor_status != VARIANT_STATUS_CANONICAL:
                    raise BurnedPatternAuditError(
                        f"--allow-superseded-sensitivity: the successor of superseded "
                        f"experiment '{experiment_id}' is '{successor_id}', whose "
                        f"variant_status is '{successor_status}', not "
                        f"'{VARIANT_STATUS_CANONICAL}'. A legacy variant may only be "
                        "compared against a valid canonical successor."
                    )
                superseded_pairs.append((experiment_id, successor_id))
            path = canonical_step8a_path(experiment_id)
            if not path.is_file():
                raise BurnedPatternAuditError(
                    f"Missing canonical Step8A dataset for '{experiment_id}': {path}. "
                    "Step8A must be generated (read-only for this audit) before "
                    "burned-pattern-audit can run for this experiment."
                )
        # (C) Never accept an unnecessary special permission silently.
        if allow_superseded_sensitivity and not superseded_pairs:
            raise BurnedPatternAuditError(
                "--allow-superseded-sensitivity was requested but the selection "
                f"{sorted(requested_set)} contains no superseded experiment. The "
                "permission exists solely to pair a superseded legacy AOI variant with "
                "its canonical successor; drop the flag for an ordinary canonical "
                "selection."
            )
        return ExperimentResolution(
            requested_ids=requested,
            resolved_ids=requested,
            selection_mode=(
                SELECTION_MODE_EXPLICIT_SUPERSEDED_SENSITIVITY
                if superseded_pairs else SELECTION_MODE_EXPLICIT
            ),
            excluded={},
            allow_superseded_sensitivity=allow_superseded_sensitivity,
            superseded_pairs=tuple(sorted(superseded_pairs)),
        )

    enabled = list_experiments(include_disabled=False)
    candidate_ids = tuple(sorted(enabled))
    resolved: list[str] = []
    excluded: dict[str, str] = {}
    for experiment_id in candidate_ids:
        record = enabled[experiment_id]
        # Fail-closed variant validation: a record with a missing/unknown
        # variant_status raises here rather than being assumed canonical.
        status = validate_variant_record(record, experiment_id)
        if status == VARIANT_STATUS_LEGACY_SUPERSEDED:
            excluded[experiment_id] = f"superseded_by_{record['superseded_by']}"
            continue
        if record.get("role") in NON_COHORT_ROLES:
            excluded[experiment_id] = str(record.get("role"))
            continue
        # Missing-input behaviour is UNCHANGED: discovery mode is expected to
        # skip experiments that have not reached Step8A yet.
        path = canonical_step8a_path(experiment_id)
        if path.is_file():
            resolved.append(experiment_id)
        else:
            excluded[experiment_id] = f"missing_canonical_step8a_dataset:{path}"
    # (D) Discovery is untouched by the sensitivity permission: reaching this
    # branch with the flag set is impossible (rejected above), so the result
    # always carries the default allow_superseded_sensitivity=False / no pairs.
    return ExperimentResolution(
        requested_ids=candidate_ids,
        resolved_ids=tuple(resolved),
        selection_mode=SELECTION_MODE_ALL_ENABLED,
        excluded=excluded,
    )


# =============================================================================
# Input validation
# =============================================================================
def dataset_schema_columns(path: Path) -> list[str]:
    """Column names only, via the parquet footer -- no row data is read.
    Used by --dry-run to validate columns "using metadata where practical"."""
    return list(pq.ParquetFile(path).schema_arrow.names)


def validate_required_columns(columns: list[str] | pd.Index, experiment_id: str) -> None:
    present = set(columns)
    missing = [c for c in REQUIRED_COLUMNS if c not in present]
    if missing:
        raise BurnedPatternAuditError(
            f"'{experiment_id}': canonical Step8A dataset is missing required column(s): {missing}."
        )
    if BURNABLE_MASK_COLUMN not in present:
        raise BurnedPatternAuditError(
            f"'{experiment_id}': canonical Step8A dataset is missing '{BURNABLE_MASK_COLUMN}', "
            "required to compute the natural-vegetation sensitivity population."
        )
    if VALID_FOR_MODELING_COLUMN not in present:
        raise BurnedPatternAuditError(
            f"'{experiment_id}': canonical Step8A dataset is missing "
            f"'{VALID_FOR_MODELING_COLUMN}', required to compute the "
            f"'{POPULATION_BURNABLE_TSG_VALID_MODEL_BURNED}' final-model-population "
            "comparison. The column is reused verbatim and never recomputed here."
        )


def validate_grid_uniqueness(df: pd.DataFrame, experiment_id: str) -> None:
    key = df[["row_500m", "col_500m"]]
    duplicated = key.duplicated(keep=False)
    if duplicated.any():
        n_dup = int(duplicated.sum())
        raise BurnedPatternAuditError(
            f"'{experiment_id}': (row_500m, col_500m) is not unique -- {n_dup} duplicated "
            "row(s) found. Refusing to silently deduplicate."
        )


def validate_burned_values(df: pd.DataFrame, experiment_id: str) -> pd.Series:
    burned = df["burned"]
    non_null = burned.dropna()
    valid_values = set(pd.unique(non_null.astype(float))) <= {0.0, 1.0}
    if burned.isna().any() or not valid_values:
        raise BurnedPatternAuditError(
            f"'{experiment_id}': 'burned' column must contain only binary values "
            f"(0/1, no missing); found unique values {sorted(pd.unique(burned))!r}."
        )
    return burned.astype(int)


# =============================================================================
# Connected components (deterministic 8-neighbour raster connectivity)
# =============================================================================
class _UnionFind:
    def __init__(self, n: int) -> None:
        self._parent = list(range(n))
        self._rank = [0] * n

    def find(self, x: int) -> int:
        root = x
        while self._parent[root] != root:
            root = self._parent[root]
        while self._parent[x] != root:
            self._parent[x], x = root, self._parent[x]
        return root

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self._rank[ra] < self._rank[rb]:
            ra, rb = rb, ra
        self._parent[rb] = ra
        if self._rank[ra] == self._rank[rb]:
            self._rank[ra] += 1


def _connected_component_roots(coords: list[tuple[int, int]]) -> list[int]:
    """8-neighbour connected-component root index per coordinate (order of
    `coords`). Purely a function of the coordinate SET -- independent of
    input ordering."""
    n = len(coords)
    index_of = {coord: i for i, coord in enumerate(coords)}
    uf = _UnionFind(n)
    for i, (row, col) in enumerate(coords):
        for delta_row, delta_col in _NEIGHBOUR_OFFSETS:
            neighbour = (row + delta_row, col + delta_col)
            j = index_of.get(neighbour)
            if j is not None:
                uf.union(i, j)
    return [uf.find(i) for i in range(n)]


def build_components(coords: list[tuple[int, int]]) -> tuple[list[dict[str, Any]], list[int]]:
    """Assign deterministic component IDs (starting at 1) to a list of
    (row, col) burned-cell coordinates.

    Deterministic ordering: components are sorted by (min_row, min_col,
    then descending size) before IDs are assigned, so the result does not
    depend on the order `coords` was supplied in.

    Returns:
        (components, membership) where `components` is a list of dicts
        (component_id, size, min_row, min_col, max_row, max_col, indices)
        and `membership[i]` is the component_id assigned to `coords[i]`.
    """
    if not coords:
        return [], []
    roots = _connected_component_roots(coords)
    groups: dict[int, list[int]] = {}
    for i, root in enumerate(roots):
        groups.setdefault(root, []).append(i)

    raw = []
    for indices in groups.values():
        rows = [coords[i][0] for i in indices]
        cols = [coords[i][1] for i in indices]
        raw.append({
            "indices": indices,
            "size": len(indices),
            "min_row": min(rows),
            "min_col": min(cols),
            "max_row": max(rows),
            "max_col": max(cols),
        })
    raw.sort(key=lambda c: (c["min_row"], c["min_col"], -c["size"]))

    membership = [0] * len(coords)
    for new_id, comp in enumerate(raw, start=1):
        comp["component_id"] = new_id
        for i in comp["indices"]:
            membership[i] = new_id
    return raw, membership


def compute_edge_touching(
    components: list[dict[str, Any]],
    coords: list[tuple[int, int]],
    valid_extent: set[tuple[int, int]],
) -> dict[int, bool]:
    """A component touches the analysis boundary if any of its cells has an
    8-neighbour position that falls outside the complete valid Step8A grid
    extent for the experiment (irregular-AOI-aware; not a bounding-box
    check). Descriptive only -- never used to remove components."""
    touching: dict[int, bool] = {}
    for comp in components:
        touches = False
        for i in comp["indices"]:
            row, col = coords[i]
            for delta_row, delta_col in _NEIGHBOUR_OFFSETS:
                if (row + delta_row, col + delta_col) not in valid_extent:
                    touches = True
                    break
            if touches:
                break
        touching[comp["component_id"]] = touches
    return touching


# =============================================================================
# Descriptive metric blocks
# =============================================================================
def component_population_metrics(components: list[dict[str, Any]], burned_cell_count: int) -> dict[str, Any]:
    sizes = np.array(sorted((c["size"] for c in components), reverse=True), dtype=np.int64)
    component_count = len(sizes)
    if component_count == 0:
        return {
            "total_burned_cells": int(burned_cell_count),
            "component_count": 0,
            "singleton_component_count": 0,
            "singleton_component_fraction": None,
            "largest_component_cells": 0,
            "largest_component_fraction": None,
            "second_largest_component_cells": 0,
            "second_largest_component_fraction": None,
            "top3_component_fraction": None,
            "component_share_hhi": None,
            "effective_component_count": None,
            "component_size_min": None,
            "component_size_q25": None,
            "component_size_median": None,
            "component_size_mean": None,
            "component_size_q75": None,
            "component_size_q90": None,
            "component_size_q95": None,
            "component_size_max": None,
            "largest_component_approximate_area_km2": None,
            "total_burned_approximate_area_km2": float(burned_cell_count) * APPROXIMATE_CELL_AREA_KM2,
        }
    singleton_count = int(np.sum(sizes == 1))
    largest = int(sizes[0])
    second_largest = int(sizes[1]) if component_count > 1 else 0
    top3 = int(sizes[:3].sum())
    quantiles = np.quantile(sizes, [0.25, 0.5, 0.75, 0.9, 0.95])
    # Concentration of burned area across components, descriptive only -- no
    # threshold and no concentration CLASS is defined anywhere in this module.
    #   shares_i                 = component_size_i / burned_cell_count
    #   component_share_hhi      = sum(shares_i ** 2)
    #   effective_component_count = 1 / component_share_hhi
    # A single component gives HHI 1.0 and an effective count of 1.0.
    if burned_cell_count:
        shares = sizes.astype(float) / float(burned_cell_count)
        hhi = float(np.sum(shares ** 2))
        effective_component_count = 1.0 / hhi if hhi > 0 else None
        second_largest_fraction = second_largest / burned_cell_count
    else:
        hhi = None
        effective_component_count = None
        second_largest_fraction = None
    return {
        "total_burned_cells": int(burned_cell_count),
        "component_count": component_count,
        "singleton_component_count": singleton_count,
        "singleton_component_fraction": singleton_count / component_count,
        "largest_component_cells": largest,
        "largest_component_fraction": largest / burned_cell_count if burned_cell_count else None,
        "second_largest_component_cells": second_largest,
        "second_largest_component_fraction": second_largest_fraction,
        "top3_component_fraction": top3 / burned_cell_count if burned_cell_count else None,
        "component_share_hhi": hhi,
        "effective_component_count": effective_component_count,
        "component_size_min": int(sizes.min()),
        "component_size_q25": float(quantiles[0]),
        "component_size_median": float(quantiles[1]),
        "component_size_mean": float(sizes.mean()),
        "component_size_q75": float(quantiles[2]),
        "component_size_q90": float(quantiles[3]),
        "component_size_q95": float(quantiles[4]),
        "component_size_max": int(sizes.max()),
        "largest_component_approximate_area_km2": largest * APPROXIMATE_CELL_AREA_KM2,
        "total_burned_approximate_area_km2": float(burned_cell_count) * APPROXIMATE_CELL_AREA_KM2,
    }


def edge_diagnostics(components: list[dict[str, Any]], touching: dict[int, bool]) -> dict[str, Any]:
    component_count = len(components)
    if component_count == 0:
        return {
            "edge_touching_component_count": 0,
            "edge_touching_component_fraction": None,
            "largest_component_touches_edge": None,
        }
    edge_count = sum(1 for v in touching.values() if v)
    # Components are sorted by (min_row, min_col, -size) at build time, not
    # globally by size, so the true largest component is picked explicitly.
    largest_component = max(components, key=lambda c: c["size"])
    return {
        "edge_touching_component_count": edge_count,
        "edge_touching_component_fraction": edge_count / component_count,
        "largest_component_touches_edge": bool(touching.get(largest_component["component_id"], False)),
    }


def elevation_summary(series: pd.Series) -> dict[str, Any]:
    valid = series.dropna().astype(float)
    missing = int(series.isna().sum())
    if len(valid) == 0:
        return {
            "valid_count": 0, "missing_count": missing,
            "min": None, "q05": None, "q25": None, "median": None, "mean": None,
            "q75": None, "q95": None, "max": None, "iqr": None, "range": None,
        }
    q = valid.quantile([0.05, 0.25, 0.5, 0.75, 0.95])
    return {
        "valid_count": int(len(valid)),
        "missing_count": missing,
        "min": float(valid.min()),
        "q05": float(q.loc[0.05]),
        "q25": float(q.loc[0.25]),
        "median": float(q.loc[0.5]),
        "mean": float(valid.mean()),
        "q75": float(q.loc[0.75]),
        "q95": float(q.loc[0.95]),
        "max": float(valid.max()),
        "iqr": float(q.loc[0.75] - q.loc[0.25]),
        "range": float(valid.max() - valid.min()),
    }


def landcover_label(code: Any) -> str:
    if code is None or (isinstance(code, float) and not np.isfinite(code)):
        return "unknown_class_missing"
    return ESA_WORLDCOVER_CLASSES.get(int(code), f"unknown_class_{int(code)}")


def landcover_mix(series: pd.Series) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    valid = series.dropna()
    missing = int(series.isna().sum())
    total_valid = int(len(valid))
    rows: list[dict[str, Any]] = []
    if total_valid:
        counts = valid.astype(int).value_counts().sort_values(ascending=False)
        for code, count in counts.items():
            rows.append({
                "class_code": int(code),
                "label": landcover_label(code),
                "count": int(count),
                "fraction": float(count) / total_valid,
            })
    dominant = rows[0] if rows else None
    summary = {
        "missing_count": missing,
        "valid_count": total_valid,
        "observed_landcover_class_count": len(rows),
        "dominant_landcover_code": dominant["class_code"] if dominant else None,
        "dominant_landcover_label": dominant["label"] if dominant else None,
        "dominant_landcover_fraction": dominant["fraction"] if dominant else None,
    }
    return rows, summary


def burn_date_component_summary(df_population: pd.DataFrame, membership: list[int]) -> Optional[list[dict[str, Any]]]:
    """Descriptive-only per-component BurnDate stats. NEVER used to split,
    join, or redefine components; absent if burn_date is unavailable."""
    if "burn_date" not in df_population.columns:
        return None
    working = df_population.copy()
    working["_component_id"] = membership
    rows: list[dict[str, Any]] = []
    for component_id, group in working.groupby("_component_id", sort=True):
        valid = group["burn_date"].dropna()
        rows.append({
            "component_id": int(component_id),
            "burn_date_min": float(valid.min()) if len(valid) else None,
            "burn_date_max": float(valid.max()) if len(valid) else None,
            "burn_date_span": float(valid.max() - valid.min()) if len(valid) else None,
            "burn_date_unique_valid_count": int(valid.nunique()),
        })
    return rows


# =============================================================================
# Per-experiment orchestration
# =============================================================================
def _package_versions() -> dict[str, str]:
    names = {"numpy": "numpy", "pandas": "pandas", "pyarrow": "pyarrow"}
    return {key: importlib.metadata.version(pkg) for key, pkg in names.items()}


def scientific_configuration(resolved_experiment_ids: tuple[str, ...], input_hashes: dict[str, str]) -> dict[str, Any]:
    return {
        "analysis_schema_version": ANALYSIS_SCHEMA_VERSION,
        "resolved_experiment_ids": sorted(resolved_experiment_ids),
        "connectivity": CONNECTIVITY_DEFINITION,
        "populations": POPULATION_DEFINITIONS,
        "burnable_mask_column": BURNABLE_MASK_COLUMN,
        "valid_for_modeling_column": VALID_FOR_MODELING_COLUMN,
        "landcover_mapping_source": LANDCOVER_MAPPING_SOURCE,
        "cell_area_km2_source": CELL_AREA_KM2_SOURCE,
        "approximate_cell_area_km2": APPROXIMATE_CELL_AREA_KM2,
        "input_step8a_sha256": dict(sorted(input_hashes.items())),
        "package_versions": _package_versions(),
        "prohibited_actions": list(PROHIBITED_ACTIONS),
        "limitations": list(SCIENTIFIC_LIMITATIONS),
    }


def build_analysis_id(resolved_experiment_ids: tuple[str, ...], input_hashes: dict[str, str]) -> str:
    content = scientific_configuration(resolved_experiment_ids, input_hashes)
    return sha256_bytes(canonical_json(content).encode("utf-8"))


def _existing_manifest_analysis_id(output_dir: Path) -> Optional[str]:
    manifest_path = output_dir / "manifest.json"
    if not manifest_path.is_file():
        return None
    try:
        return json.loads(manifest_path.read_text()).get("analysis_id")
    except (json.JSONDecodeError, OSError):
        return None


def _guard_force(output_dir: Path, analysis_id: str, force: bool, label: str) -> None:
    existing = _existing_manifest_analysis_id(output_dir)
    if existing is not None and existing != analysis_id and not force:
        raise BurnedPatternAuditError(
            f"{label}: existing output at {output_dir} was produced by a different "
            f"analysis_id ({existing} != {analysis_id}). Use --force to overwrite."
        )


def _analyze_population(
    df: pd.DataFrame,
    population_name: str,
    valid_extent: set[tuple[int, int]],
    eligible_mask: pd.Series,
) -> dict[str, Any]:
    base_mask = eligible_mask & (df["burned"] == 1) & df["row_500m"].notna() & df["col_500m"].notna()
    if population_name == POPULATION_ALL_VALID_BURNED:
        mask = base_mask
    elif population_name == POPULATION_BURNABLE_TSG_BURNED:
        mask = base_mask & (df[BURNABLE_MASK_COLUMN] == True)  # noqa: E712
    elif population_name == POPULATION_BURNABLE_TSG_VALID_MODEL_BURNED:
        # Additional final-model-population comparison ONLY: the extra
        # valid_for_modeling restriction is applied here and nowhere else, so
        # the primary and natural-vegetation populations are untouched.
        mask = (
            base_mask
            & (df[BURNABLE_MASK_COLUMN] == True)  # noqa: E712
            & (df[VALID_FOR_MODELING_COLUMN] == True)  # noqa: E712
        )
    else:
        raise BurnedPatternAuditError(f"Unknown population: {population_name}")

    population_df = df.loc[mask].reset_index(drop=True)
    burned_cell_count = int(len(population_df))
    coords = list(zip(population_df["row_500m"].astype(int), population_df["col_500m"].astype(int)))

    components, membership = build_components(coords)
    if components:
        assert sum(c["size"] for c in components) == burned_cell_count
        assert len(membership) == burned_cell_count

    touching = compute_edge_touching(components, coords, valid_extent)
    metrics = component_population_metrics(components, burned_cell_count)
    edge = edge_diagnostics(components, touching)
    elevation = elevation_summary(population_df["elevation_mean"])
    assert elevation["valid_count"] + elevation["missing_count"] == burned_cell_count
    landcover_rows, landcover_summary = landcover_mix(population_df["landcover_dominant"])
    if landcover_rows:
        assert sum(r["count"] for r in landcover_rows) == landcover_summary["valid_count"]
        assert abs(sum(r["fraction"] for r in landcover_rows) - 1.0) < 1e-9
    burn_date_rows = burn_date_component_summary(population_df, membership)

    membership_df = pd.DataFrame({
        "population": population_name,
        "row_500m": population_df["row_500m"].astype(int),
        "col_500m": population_df["col_500m"].astype(int),
        "component_id": membership,
    })
    component_rows = [
        {
            "population": population_name,
            "component_id": c["component_id"],
            "size_cells": c["size"],
            "min_row": c["min_row"],
            "min_col": c["min_col"],
            "max_row": c["max_row"],
            "max_col": c["max_col"],
            "touches_edge": touching.get(c["component_id"], False),
            "approximate_area_km2": c["size"] * APPROXIMATE_CELL_AREA_KM2,
        }
        for c in sorted(components, key=lambda c: c["component_id"])
    ]
    if burn_date_rows:
        burn_date_by_id = {r["component_id"]: r for r in burn_date_rows}
        for row in component_rows:
            extra = burn_date_by_id.get(row["component_id"], {})
            row.update({k: v for k, v in extra.items() if k != "component_id"})

    return {
        "population": population_name,
        "definition": POPULATION_DEFINITIONS[population_name],
        "total_input_rows": int(len(df)),
        "analysis_eligible_rows": int(eligible_mask.sum()),
        "metrics": metrics,
        "edge_diagnostics": edge,
        "elevation": elevation,
        "landcover": {"summary": landcover_summary, "classes": landcover_rows},
        "burn_date_available": burn_date_rows is not None,
        "component_rows": component_rows,
        "membership_df": membership_df,
    }


def analyze_experiment(
    experiment_id: str, dry_run: bool = False, force: bool = False,
    layout: Optional[AuditLayout] = None,
) -> dict[str, Any]:
    """Run (or dry-run-plan) the burned-pattern audit for a single resolved
    experiment_id. Step8A is read-only throughout.

    `layout=None` keeps the legacy flat default, so existing callers are
    unaffected.
    """
    layout = layout or default_layout()
    input_path = canonical_step8a_path(experiment_id)
    output_dir = layout.experiments / experiment_id
    planned_paths = {
        "burned_pattern_summary_json": str(output_dir / "burned_pattern_summary.json"),
        "component_summary_csv": str(output_dir / "component_summary.csv"),
        "component_membership_parquet": str(output_dir / "component_membership.parquet"),
        "elevation_summary_csv": str(output_dir / "elevation_summary.csv"),
        "landcover_mix_csv": str(output_dir / "landcover_mix.csv"),
        "burned_pattern_summary_md": str(output_dir / "burned_pattern_summary.md"),
        "manifest_json": str(output_dir / "manifest.json"),
    }

    if not input_path.is_file():
        raise BurnedPatternAuditError(f"Missing canonical Step8A dataset for '{experiment_id}': {input_path}.")

    if dry_run:
        columns = dataset_schema_columns(input_path)
        validate_required_columns(columns, experiment_id)
        input_hash = sha256_file(input_path)
        return {
            "ran": False,
            "dry_run": True,
            "experiment_id": experiment_id,
            "input_path": str(input_path),
            "input_sha256": input_hash,
            "columns_present": columns,
            "pre_label_gate": gate_provenance(experiment_id),
            "scientific_configuration": scientific_configuration((experiment_id,), {experiment_id: input_hash}),
            "planned_output_paths": planned_paths,
        }

    input_hash_before = sha256_file(input_path)
    df = pd.read_parquet(input_path)
    validate_required_columns(list(df.columns), experiment_id)
    validate_grid_uniqueness(df, experiment_id)
    df = df.assign(burned=validate_burned_values(df, experiment_id))

    valid_extent = set(
        zip(
            df.loc[df["row_500m"].notna() & df["col_500m"].notna(), "row_500m"].astype(int),
            df.loc[df["row_500m"].notna() & df["col_500m"].notna(), "col_500m"].astype(int),
        )
    )

    analysis_eligible_mask = resolve_analysis_eligible_mask(df)
    populations = {
        name: _analyze_population(df, name, valid_extent, analysis_eligible_mask) for name in POPULATIONS
    }

    # Cross-validate against the canonical gate BEFORE writing any output
    # (fail-fast if the corrected audit disagrees with Step6B's gate).
    gate_info = validate_against_gate(
        experiment_id, df, analysis_eligible_mask,
        populations[POPULATION_ALL_VALID_BURNED]["metrics"]["total_burned_cells"],
    )

    input_hashes = {experiment_id: input_hash_before}
    analysis_id = build_analysis_id((experiment_id,), input_hashes)
    _guard_force(output_dir, analysis_id, force, label=f"burned-pattern-audit[{experiment_id}]")

    manifest = {
        "analysis_id": analysis_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": _git_commit(),
        "requested_experiment_ids": [experiment_id],
        "resolved_experiment_ids": [experiment_id],
        "selection_mode": "single",
        "input_paths": {experiment_id: str(input_path)},
        "input_sha256": input_hashes,
        "pre_label_gate": gate_info,
        "scientific_configuration": scientific_configuration((experiment_id,), input_hashes),
    }

    summary = {
        "experiment_id": experiment_id,
        "analysis_id": analysis_id,
        "created_at": manifest["created_at"],
        "input_path": str(input_path),
        "pre_label_gate": gate_info,
        "populations": {
            name: {k: v for k, v in pop.items() if k not in ("membership_df", "component_rows")}
            for name, pop in populations.items()
        },
        "limitations": list(SCIENTIFIC_LIMITATIONS),
    }

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "burned_pattern_summary.json").write_text(json.dumps(summary, indent=2, default=str))
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str))

    component_rows_all = []
    membership_frames = []
    for pop in populations.values():
        component_rows_all.extend(pop["component_rows"])
        membership_frames.append(pop["membership_df"])
    pd.DataFrame(component_rows_all).to_csv(output_dir / "component_summary.csv", index=False)
    membership_all = pd.concat(membership_frames, ignore_index=True) if membership_frames else pd.DataFrame(
        columns=["population", "row_500m", "col_500m", "component_id"]
    )
    membership_all.to_parquet(output_dir / "component_membership.parquet", index=False)

    elevation_rows = [
        {"population": name, **pop["elevation"]} for name, pop in populations.items()
    ]
    pd.DataFrame(elevation_rows).to_csv(output_dir / "elevation_summary.csv", index=False)

    landcover_rows_all = [
        {"population": name, **cls}
        for name, pop in populations.items()
        for cls in pop["landcover"]["classes"]
    ]
    pd.DataFrame(landcover_rows_all).to_csv(output_dir / "landcover_mix.csv", index=False)

    (output_dir / "burned_pattern_summary.md").write_text(
        render_experiment_markdown(experiment_id, populations, manifest)
    )

    input_hash_after = sha256_file(input_path)
    if input_hash_after != input_hash_before:
        raise BurnedPatternAuditError(
            f"'{experiment_id}': Step8A input hash changed during the audit run "
            "(expected read-only)."
        )

    return {
        "ran": True,
        "dry_run": False,
        "experiment_id": experiment_id,
        "analysis_id": analysis_id,
        "output_dir": str(output_dir),
        "populations": populations,
        "manifest": manifest,
    }


# =============================================================================
# Markdown rendering
# =============================================================================
def _population_markdown(pop: dict[str, Any], heading: str) -> str:
    m = pop["metrics"]
    edge = pop["edge_diagnostics"]
    elevation = pop["elevation"]
    lc = pop["landcover"]["summary"]
    lines = [f"### {heading}", "", pop["definition"], ""]
    lines += [
        f"- Total input rows: {pop['total_input_rows']}",
        f"- Burned-cell count: {m['total_burned_cells']}",
        f"- Spatially connected burned-cell components: {m['component_count']}",
        f"- Singleton components: {m['singleton_component_count']} "
        f"({m['singleton_component_fraction']})",
        f"- Largest component: {m['largest_component_cells']} cells "
        f"(fraction {m['largest_component_fraction']})",
        f"- Second-largest component: {m['second_largest_component_cells']} cells "
        f"(fraction {m['second_largest_component_fraction']})",
        f"- Top-3 components combined fraction: {m['top3_component_fraction']}",
        f"- Component-share HHI (sum of squared component shares): "
        f"{m['component_share_hhi']}",
        f"- Effective component count (1 / HHI): {m['effective_component_count']}",
        f"- Component size (cells): min={m['component_size_min']}, "
        f"q25={m['component_size_q25']}, median={m['component_size_median']}, "
        f"mean={m['component_size_mean']}, q75={m['component_size_q75']}, "
        f"q90={m['component_size_q90']}, q95={m['component_size_q95']}, "
        f"max={m['component_size_max']}",
        f"- Approximate total burned area: {m['total_burned_approximate_area_km2']} km^2 "
        f"(source: {CELL_AREA_KM2_SOURCE})",
        "",
        "**AOI-edge diagnostics (descriptive only, never used to remove components):**",
        f"- Edge-touching components: {edge['edge_touching_component_count']} "
        f"({edge['edge_touching_component_fraction']})",
        f"- Largest component touches edge: {edge['largest_component_touches_edge']}",
        "",
        "**Elevation (elevation_mean, burned cells):**",
        f"- valid={elevation['valid_count']}, missing={elevation['missing_count']}, "
        f"min={elevation['min']}, q05={elevation['q05']}, q25={elevation['q25']}, "
        f"median={elevation['median']}, mean={elevation['mean']}, q75={elevation['q75']}, "
        f"q95={elevation['q95']}, max={elevation['max']}, iqr={elevation['iqr']}, "
        f"range={elevation['range']}",
        "",
        "**Land-cover composition (landcover_dominant, burned cells):**",
        f"- Observed classes: {lc['observed_landcover_class_count']}, "
        f"dominant: {lc['dominant_landcover_label']} (code {lc['dominant_landcover_code']}, "
        f"fraction {lc['dominant_landcover_fraction']})",
        "",
    ]
    if pop["burn_date_available"]:
        lines.append(
            "**BurnDate** (descriptive only; never used to split/join/redefine "
            "components or to claim distinct-event identification): available, "
            "see component_summary.csv for per-component min/max/span/unique_count."
        )
    else:
        lines.append("**BurnDate**: unavailable for this experiment (burn_date column absent).")
    lines.append("")
    return "\n".join(lines)


def render_experiment_markdown(experiment_id: str, populations: dict[str, Any], manifest: dict[str, Any]) -> str:
    gate = manifest.get("pre_label_gate", {})
    parts = [
        f"# Burned-pattern audit -- {experiment_id}",
        "",
        f"analysis_id: `{manifest['analysis_id']}`  ",
        f"created_at: {manifest['created_at']}  ",
        f"git_commit: {manifest.get('git_commit')}",
        "",
        "## Canonical burned-landcover gate cross-validation",
        "",
    ]
    if gate.get("gate_available"):
        parts += [
            f"- Gate path: `{gate.get('gate_path')}`",
            f"- Gate SHA-256: `{gate.get('gate_sha256')}`",
            f"- Pre-label-burn exclusion rule: {gate.get('pre_label_burn_exclusion_rule')!r}",
            f"- Pre-label-excluded cell count: {gate.get('pre_label_burn_excluded_count')}",
            f"- Cross-validated against audit analysis universe / burned count: {gate.get('validated', False)}",
            "",
        ]
    else:
        parts += ["No canonical burned-landcover gate found for this experiment; no pre-label exclusion applied.", ""]
    parts += [
        "## Primary population: all_valid_burned",
        "",
        _population_markdown(populations[POPULATION_ALL_VALID_BURNED], "all_valid_burned"),
        f"## Sensitivity analysis: {POPULATION_BURNABLE_TSG_BURNED}",
        "",
        _population_markdown(populations[POPULATION_BURNABLE_TSG_BURNED], POPULATION_BURNABLE_TSG_BURNED),
        f"## Final-model-population comparison: {POPULATION_BURNABLE_TSG_VALID_MODEL_BURNED}",
        "",
        _population_markdown(
            populations[POPULATION_BURNABLE_TSG_VALID_MODEL_BURNED],
            POPULATION_BURNABLE_TSG_VALID_MODEL_BURNED,
        ),
        "## Limitations",
        "",
    ]
    parts += [f"- {line}" for line in SCIENTIFIC_LIMITATIONS]
    parts.append("")
    return "\n".join(parts)


# =============================================================================
# Multi-experiment comparison
# =============================================================================
def comparison_row(experiment_id: str, population_name: str, pop: dict[str, Any]) -> dict[str, Any]:
    m, edge, elevation, lc = pop["metrics"], pop["edge_diagnostics"], pop["elevation"], pop["landcover"]["summary"]
    return {
        "experiment_id": experiment_id,
        "population": population_name,
        "analysis_eligible_rows": pop["analysis_eligible_rows"],
        "burned_cell_count": m["total_burned_cells"],
        "component_count": m["component_count"],
        "singleton_component_count": m["singleton_component_count"],
        "largest_component_cells": m["largest_component_cells"],
        "largest_component_fraction": m["largest_component_fraction"],
        "second_largest_component_cells": m["second_largest_component_cells"],
        "second_largest_component_fraction": m["second_largest_component_fraction"],
        "top3_component_fraction": m["top3_component_fraction"],
        "component_share_hhi": m["component_share_hhi"],
        "effective_component_count": m["effective_component_count"],
        "component_size_median": m["component_size_median"],
        "component_size_q90": m["component_size_q90"],
        "component_size_q95": m["component_size_q95"],
        "component_size_max": m["component_size_max"],
        "elevation_min": elevation["min"],
        "elevation_q05": elevation["q05"],
        "elevation_median": elevation["median"],
        "elevation_q95": elevation["q95"],
        "elevation_max": elevation["max"],
        "dominant_landcover_code": lc["dominant_landcover_code"],
        "dominant_landcover_label": lc["dominant_landcover_label"],
        "dominant_landcover_fraction": lc["dominant_landcover_fraction"],
        "observed_landcover_class_count": lc["observed_landcover_class_count"],
        "edge_touching_component_count": edge["edge_touching_component_count"],
        "largest_component_touches_edge": edge["largest_component_touches_edge"],
    }


def superseded_sensitivity_record(resolution: ExperimentResolution) -> dict[str, Any]:
    """Serialisable record of the legacy-variant sensitivity permission, so
    every manifest/result states both that the permission was used and that
    the legacy experiment was NOT restored to the canonical cohort."""
    return {
        "allow_superseded_sensitivity": resolution.allow_superseded_sensitivity,
        "superseded_pairs": [
            {
                "superseded_experiment_id": superseded_id,
                "canonical_successor_experiment_id": successor_id,
            }
            for superseded_id, successor_id in resolution.superseded_pairs
        ],
        "superseded_sensitivity_note": (
            SUPERSEDED_SENSITIVITY_NOTE if resolution.superseded_pairs else None
        ),
    }


def render_comparison_markdown(
    resolution: ExperimentResolution,
    results: dict[str, dict[str, Any]],
    manifest: dict[str, Any],
) -> str:
    parts = [
        "# Multi-AOI burned-pattern comparison",
        "",
        f"analysis_id: `{manifest['analysis_id']}` (order-invariant)  ",
        f"created_at: {manifest['created_at']}  ",
        f"selection_mode: {resolution.selection_mode}  ",
        f"requested_experiment_ids: {list(resolution.requested_ids)}  ",
        f"resolved_experiment_ids: {sorted(resolution.resolved_ids)}  ",
        f"allow_superseded_sensitivity: {resolution.allow_superseded_sensitivity}  ",
        f"superseded_pairs: {[list(pair) for pair in resolution.superseded_pairs]}",
        "",
    ]
    if resolution.superseded_pairs:
        parts.append("**Legacy AOI-definition sensitivity comparison**")
        parts.append("")
        for superseded_id, successor_id in resolution.superseded_pairs:
            parts.append(
                f"- `{superseded_id}` is included ONLY as a superseded legacy "
                f"AOI-definition sensitivity comparator against its canonical "
                f"successor `{successor_id}`."
            )
        parts.append("")
        parts.append(SUPERSEDED_SENSITIVITY_NOTE)
        parts.append("")
    if resolution.excluded:
        parts.append("**Excluded from resolution:**")
        for exp_id, reason in sorted(resolution.excluded.items()):
            parts.append(f"- {exp_id}: {reason}")
        parts.append("")
    gate_by_experiment = manifest.get("pre_label_gate", {})
    for experiment_id in sorted(results):
        populations = results[experiment_id]["populations"]
        gate = gate_by_experiment.get(experiment_id, {})
        parts.append(f"## {experiment_id}")
        parts.append("")
        if gate.get("gate_available"):
            parts.append(
                f"Canonical burned-landcover gate cross-validated: `{gate.get('gate_path')}` "
                f"(sha256 {gate.get('gate_sha256')}); pre-label-excluded cells: "
                f"{gate.get('pre_label_burn_excluded_count')}; exclusion rule: "
                f"{gate.get('pre_label_burn_exclusion_rule')!r}."
            )
        else:
            parts.append("No canonical burned-landcover gate found for this experiment; no pre-label exclusion applied.")
        parts.append("")
        parts.append(_population_markdown(populations[POPULATION_ALL_VALID_BURNED], f"{POPULATION_ALL_VALID_BURNED} (primary)"))
        parts.append(_population_markdown(populations[POPULATION_BURNABLE_TSG_BURNED], f"{POPULATION_BURNABLE_TSG_BURNED} (sensitivity)"))
        parts.append(_population_markdown(
            populations[POPULATION_BURNABLE_TSG_VALID_MODEL_BURNED],
            f"{POPULATION_BURNABLE_TSG_VALID_MODEL_BURNED} (final-model population)",
        ))
    parts.append("## Limitations")
    parts.append("")
    parts += [f"- {line}" for line in SCIENTIFIC_LIMITATIONS]
    parts.append("")
    return "\n".join(parts)


def run_comparison(
    resolution: ExperimentResolution, dry_run: bool, force: bool,
    layout: Optional[AuditLayout] = None,
) -> dict[str, Any]:
    layout = layout or default_layout()
    comparison_dir = layout.comparison
    planned_paths = {
        "multi_aoi_burned_pattern_comparison_json": str(comparison_dir / "multi_aoi_burned_pattern_comparison.json"),
        "multi_aoi_burned_pattern_comparison_csv": str(comparison_dir / "multi_aoi_burned_pattern_comparison.csv"),
        "component_size_distribution_long_csv": str(comparison_dir / "component_size_distribution_long.csv"),
        "landcover_mix_long_csv": str(comparison_dir / "landcover_mix_long.csv"),
        "multi_aoi_burned_pattern_comparison_md": str(comparison_dir / "multi_aoi_burned_pattern_comparison.md"),
        "manifest_json": str(comparison_dir / "manifest.json"),
    }

    if dry_run:
        input_hashes = {}
        for experiment_id in resolution.resolved_ids:
            path = canonical_step8a_path(experiment_id)
            if path.is_file():
                input_hashes[experiment_id] = sha256_file(path)
        return {
            "ran": False,
            "dry_run": True,
            "requested_experiment_ids": list(resolution.requested_ids),
            "resolved_experiment_ids": sorted(resolution.resolved_ids),
            "selection_mode": resolution.selection_mode,
            "excluded": resolution.excluded,
            **superseded_sensitivity_record(resolution),
            "scientific_configuration": scientific_configuration(resolution.resolved_ids, input_hashes),
            "planned_output_paths": planned_paths,
        }

    per_experiment_results: dict[str, dict[str, Any]] = {}
    input_hashes: dict[str, str] = {}
    pre_label_gates: dict[str, Any] = {}
    for experiment_id in resolution.resolved_ids:
        result = analyze_experiment(experiment_id, dry_run=False, force=force, layout=layout)
        per_experiment_results[experiment_id] = result
        input_hashes[experiment_id] = result["manifest"]["input_sha256"][experiment_id]
        pre_label_gates[experiment_id] = result["manifest"]["pre_label_gate"]

    analysis_id = build_analysis_id(resolution.resolved_ids, input_hashes)
    _guard_force(comparison_dir, analysis_id, force, label="burned-pattern-audit[comparison]")

    manifest = {
        "analysis_id": analysis_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": _git_commit(),
        "requested_experiment_ids": list(resolution.requested_ids),
        "resolved_experiment_ids": sorted(resolution.resolved_ids),
        "selection_mode": resolution.selection_mode,
        "excluded": resolution.excluded,
        **superseded_sensitivity_record(resolution),
        "input_paths": {eid: str(canonical_step8a_path(eid)) for eid in resolution.resolved_ids},
        "input_sha256": input_hashes,
        "pre_label_gate": pre_label_gates,
        "scientific_configuration": scientific_configuration(resolution.resolved_ids, input_hashes),
    }

    comparison_rows = [
        comparison_row(experiment_id, population_name, per_experiment_results[experiment_id]["populations"][population_name])
        for experiment_id in sorted(per_experiment_results)
        for population_name in POPULATIONS
    ]
    comparison_df = pd.DataFrame(comparison_rows)

    size_long_rows = [
        {"experiment_id": experiment_id, **{k: v for k, v in row.items() if k != "population"}, "population": row["population"]}
        for experiment_id in sorted(per_experiment_results)
        for population_name in POPULATIONS
        for row in per_experiment_results[experiment_id]["populations"][population_name]["component_rows"]
    ]
    size_long_df = pd.DataFrame(size_long_rows)

    landcover_long_rows = [
        {"experiment_id": experiment_id, "population": population_name, **cls}
        for experiment_id in sorted(per_experiment_results)
        for population_name in POPULATIONS
        for cls in per_experiment_results[experiment_id]["populations"][population_name]["landcover"]["classes"]
    ]
    landcover_long_df = pd.DataFrame(landcover_long_rows)

    comparison_json = {
        "analysis_id": analysis_id,
        "created_at": manifest["created_at"],
        "resolved_experiment_ids": sorted(per_experiment_results),
        "rows": comparison_rows,
        "limitations": list(SCIENTIFIC_LIMITATIONS),
    }

    comparison_dir.mkdir(parents=True, exist_ok=True)
    (comparison_dir / "multi_aoi_burned_pattern_comparison.json").write_text(
        json.dumps(comparison_json, indent=2, default=str)
    )
    comparison_df.to_csv(comparison_dir / "multi_aoi_burned_pattern_comparison.csv", index=False)
    size_long_df.to_csv(comparison_dir / "component_size_distribution_long.csv", index=False)
    landcover_long_df.to_csv(comparison_dir / "landcover_mix_long.csv", index=False)
    (comparison_dir / "multi_aoi_burned_pattern_comparison.md").write_text(
        render_comparison_markdown(resolution, per_experiment_results, manifest)
    )
    (comparison_dir / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str))

    return {
        "ran": True,
        "dry_run": False,
        "analysis_id": analysis_id,
        "requested_experiment_ids": list(resolution.requested_ids),
        "resolved_experiment_ids": sorted(resolution.resolved_ids),
        "selection_mode": resolution.selection_mode,
        **superseded_sensitivity_record(resolution),
        "output_dir": str(comparison_dir),
        "per_experiment_results": {eid: r["analysis_id"] for eid, r in per_experiment_results.items()},
    }


def run_analysis(
    experiments: Optional[list[str]] = None,
    all_enabled: bool = False,
    dry_run: bool = False,
    force: bool = False,
    allow_superseded_sensitivity: bool = False,
    output_root: Optional[Path] = None,
    scope: Optional[str] = None,
) -> dict[str, Any]:
    """Top-level entry point: resolve experiments, then run (or dry-run)
    per-experiment audits and the multi-experiment comparison in one pass.

    `output_root` overrides the canonical root. `scope` names the namespace
    under it; when left None it is DERIVED from the resolved selection, so two
    different analysis scopes get two namespaces under the one canonical root
    instead of two sibling roots beside it. Pass `scope=""` to opt back into
    the legacy flat layout.

    `allow_superseded_sensitivity` is forwarded to resolve_experiments() and
    governs selection ONLY (see that docstring); `force` is unrelated and
    cannot substitute for it -- resolution happens first and refuses a
    superseded ID regardless of `force`."""
    resolution = resolve_experiments(
        experiments=experiments,
        all_enabled=all_enabled,
        allow_superseded_sensitivity=allow_superseded_sensitivity,
    )
    layout = resolve_layout(
        output_root, scope_key(resolution) if scope is None else (scope or None),
    )

    if dry_run:
        per_experiment_plans = {
            experiment_id: analyze_experiment(
                experiment_id, dry_run=True, force=force, layout=layout,
            )
            for experiment_id in resolution.resolved_ids
        }
        comparison_plan = run_comparison(resolution, dry_run=True, force=force, layout=layout)
        return {
            "ran": False,
            "dry_run": True,
            "requested_experiment_ids": list(resolution.requested_ids),
            "resolved_experiment_ids": sorted(resolution.resolved_ids),
            "selection_mode": resolution.selection_mode,
            "excluded": resolution.excluded,
            **superseded_sensitivity_record(resolution),
            "per_experiment": per_experiment_plans,
            "comparison": comparison_plan,
        }

    comparison_result = run_comparison(resolution, dry_run=False, force=force, layout=layout)
    return {
        "ran": True,
        "dry_run": False,
        "requested_experiment_ids": list(resolution.requested_ids),
        "resolved_experiment_ids": sorted(resolution.resolved_ids),
        "selection_mode": resolution.selection_mode,
        "excluded": resolution.excluded,
        **superseded_sensitivity_record(resolution),
        "comparison": comparison_result,
    }

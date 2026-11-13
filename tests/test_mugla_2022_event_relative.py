"""
tests/test_mugla_2022_event_relative.py

Targeted tests for the `mugla_2022_event_relative` contract: the CANONICAL,
event-relative, SAME-GEOGRAPHY EVENT-TO-EVENT replacement for the provisional
calendar-shift record `mugla_2022`.

Read-only with respect to the project: no Earth Engine call, no network
access, no export, no gate/pipeline command, no model/bootstrap. The only
files written are tiny synthetic rasters inside a per-test temporary
directory, used to exercise the exclusion/union code paths directly.

Covers:
     1  mugla_2022 is superseded by mugla_2022_event_relative (record and
        frozen outputs preserved, never migrated)
     2  the new record's windows/baseline years are exact, and preserve the
        same-AOI 2021 durations (58-day predictor, 49-day label)
     3  the AOI is the SAME mugla_aoi geometry, reused not redefined
     4  event-to-event framing metadata is explicit and states the confound
     5  the role stays temporal_transfer_wildfire -> excluded from the
        generic five-AOI spatial/domain cohort and from discovery
     6  the superseded experiment's outputs are never selected as input for
        the new experiment
     7  the historical source mask is EXACTLY burned == 1, expected 3073
     8  manifest uniqueness / provenance / SHA / fail-closed checks
     9  pre-label only / historical only / both / neither eligibility cases
    10  union arithmetic and the partition assertion
    11  excluded cells never enter burned/unburned gate counts
    12  Step8A analysis_eligible union semantics + leakage assertions
    13  the global composition-gate min_positives is still 30
    14  the separate TSG threshold is 300 and only for this experiment
    15  TSG 299 -> STOP, TSG 300 -> PASS
    16  ordinary existing experiments are unchanged
    17  dry-run writes nothing

Run:
    python -m unittest tests.test_mugla_2022_event_relative
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import numpy as np
import pandas as pd
import rasterio
from rasterio.transform import from_origin

import core.regions as regions
import src.historical_burn_exclusion as hbe
from src.step6b_burned_landcover_gate import (
    PRIMARY_POPULATION_GATE_PASS,
    PRIMARY_POPULATION_GATE_STOP,
    PRIMARY_POPULATION_STOP,
    Step6BError,
    compute_gate,
    evaluate_primary_population_sample_size,
)
from src.step8a_prepare_500m_modeling_dataset import (
    LABEL_KIND_RAW,
    Step8AError,
    build_dataset,
    compute_block_size_pixels,
)

LEGACY_ID = "mugla_2022"
EVENT_ID = "mugla_2022_event_relative"
SOURCE_ID = "mugla_2021"
REGION_KEY = "mugla_aoi"
ROLE = "temporal_transfer_wildfire"

PREDICTOR_START = "2022-04-24"
PREDICTOR_END = "2022-06-20"
LABEL_START = "2022-06-21"
LABEL_END = "2022-08-08"
BASELINE_YEARS = [2018, 2019, 2020, 2021]

#: Frozen physical burned-cell count of the canonical mugla_2021 Step8A source.
EXPECTED_SOURCE_BURNED = 3073

#: The five canonical spatial AOIs. mugla_2022_event_relative must NEVER
#: silently become a sixth.
CANONICAL_FIVE_SPATIAL_AOIS = (
    "manavgat_2021",
    "bejis_2022",
    "mugla_2021",
    "evia_2021_extended",
    "montiferru_2021",
)


def assert_sibling_of_legacy_not_descendant(case: unittest.TestCase, path, label: str) -> None:
    """Assert namespace isolation with REAL pathlib ancestry semantics.

    A substring check is INVALID here: 'mugla_2022' is a lexical prefix of
    'mugla_2022_event_relative', so `str(legacy_root) in str(event_path)` is
    trivially true for every CORRECT path and would fail a compliant
    implementation. Directory containment is a parent/child relation, not a
    string relation -- so assert it as one, on resolved paths.

    Both directions are asserted, so isolation is not weakened:
        negative -- the path is neither the superseded root nor inside it;
        positive -- the path is the event-relative root or inside it.
    """
    legacy_root = regions.get_experiment_output_root(LEGACY_ID).resolve()
    event_root = regions.get_experiment_output_root(EVENT_ID).resolve()
    resolved = Path(path).resolve()

    case.assertNotEqual(resolved, legacy_root, label)
    case.assertNotIn(legacy_root, resolved.parents, label)
    case.assertTrue(
        resolved == event_root or event_root in resolved.parents,
        f"{label}: {resolved} is not under {event_root}",
    )


# =============================================================================
# 1-2. Supersession + exact windows
# =============================================================================
class TestSupersessionAndWindows(unittest.TestCase):
    def setUp(self):
        self.legacy = regions.get_experiment(LEGACY_ID)
        self.new = regions.get_experiment(EVENT_ID)
        self.source = regions.get_experiment(SOURCE_ID)

    def test_01_legacy_record_is_superseded_by_the_event_relative_one(self):
        self.assertEqual(self.legacy["variant_status"],
                         regions.VARIANT_STATUS_LEGACY_SUPERSEDED)
        self.assertEqual(self.legacy["superseded_by"], EVENT_ID)
        self.assertEqual(regions.get_superseded_by(LEGACY_ID), EVENT_ID)
        self.assertEqual(regions.get_variant_status(EVENT_ID),
                         regions.VARIANT_STATUS_CANONICAL)
        self.assertNotIn("superseded_by", self.new)

    def test_01_legacy_record_and_its_windows_are_preserved_verbatim(self):
        # The historical calendar-shift attempt keeps its own dates: it was
        # superseded, not rewritten.
        self.assertEqual(self.legacy["predictor_start_date"], "2022-06-01")
        self.assertEqual(self.legacy["predictor_end_date"], "2022-07-28")
        self.assertEqual(self.legacy["label_start_date"], "2022-07-29")
        self.assertEqual(self.legacy["label_end_date"], "2022-09-15")
        self.assertTrue(self.legacy["enabled"])
        self.assertEqual(self.legacy["output_namespace"], LEGACY_ID)

    def test_01_legacy_notes_state_the_supervisor_clarification(self):
        notes = self.legacy["notes"].lower()
        for fragment in ("supersed", "calendar-shift", "event-relative", "supervisor"):
            self.assertIn(fragment, notes)

    def test_02_new_record_is_registered_enabled_and_canonical(self):
        self.assertIn(EVENT_ID, regions.EXPERIMENTS)
        self.assertTrue(self.new["enabled"])
        self.assertIn(EVENT_ID, regions.list_experiments(include_disabled=False))
        self.assertEqual(self.new["display_name"], "Muğla 2022 -- event-relative")
        self.assertEqual(self.new["country"], "Turkey")
        self.assertEqual(self.new["output_namespace"], EVENT_ID)

    def test_02_predictor_and_label_dates_are_exact(self):
        self.assertEqual(self.new["predictor_start_date"], PREDICTOR_START)
        self.assertEqual(self.new["predictor_end_date"], PREDICTOR_END)
        self.assertEqual(self.new["label_start_date"], LABEL_START)
        self.assertEqual(self.new["label_end_date"], LABEL_END)

    def test_02_baseline_years_are_exact(self):
        self.assertEqual(self.new["baseline_years"], BASELINE_YEARS)

    def test_02_window_durations_are_58_and_49_days_inclusive(self):
        predictor_days = (date.fromisoformat(PREDICTOR_END)
                          - date.fromisoformat(PREDICTOR_START)).days + 1
        label_days = (date.fromisoformat(LABEL_END)
                      - date.fromisoformat(LABEL_START)).days + 1
        self.assertEqual(predictor_days, 58)
        self.assertEqual(label_days, 49)

    def test_02_durations_equal_the_same_aoi_2021_durations(self):
        def inclusive_days(start: str, end: str) -> int:
            return (date.fromisoformat(end) - date.fromisoformat(start)).days + 1

        self.assertEqual(
            inclusive_days(PREDICTOR_START, PREDICTOR_END),
            inclusive_days(self.source["predictor_start_date"],
                           self.source["predictor_end_date"]),
        )
        self.assertEqual(
            inclusive_days(LABEL_START, LABEL_END),
            inclusive_days(self.source["label_start_date"],
                           self.source["label_end_date"]),
        )

    def test_02_predictor_ends_one_day_before_ignition_and_label_starts_on_it(self):
        ignition = date.fromisoformat(self.new["event_anchor_date"])
        self.assertEqual(date.fromisoformat(PREDICTOR_END).toordinal(),
                         ignition.toordinal() - 1)
        self.assertEqual(date.fromisoformat(LABEL_START), ignition)

    def test_02_pre_label_window_equals_the_predictor_window(self):
        self.assertIs(self.new["exclude_pre_label_burns"], True)
        self.assertEqual(self.new["pre_label_burn_window"],
                         [PREDICTOR_START, PREDICTOR_END])


# =============================================================================
# 3-4. Same AOI, explicit event-to-event framing
# =============================================================================
class TestSameGeographyAndFraming(unittest.TestCase):
    def setUp(self):
        self.new = regions.get_experiment(EVENT_ID)

    def test_03_region_key_is_the_shared_mugla_aoi(self):
        self.assertEqual(self.new["region_key"], REGION_KEY)
        for other in (LEGACY_ID, SOURCE_ID):
            self.assertEqual(regions.get_experiment(other)["region_key"], REGION_KEY)

    def test_03_no_new_mugla_geometry_was_introduced(self):
        # build_regions() is never called here (it would need ee.Initialize);
        # the module source is read statically instead.
        source = (_PROJECT_ROOT / "core" / "regions.py").read_text(encoding="utf-8")
        self.assertEqual(source.count("ee.Geometry.BBox(*MUGLA_AOI_BBOX)"), 1)
        self.assertEqual(regions.MUGLA_AOI_BBOX, (27.10, 36.60, 28.90, 37.45))
        self.assertNotIn("MUGLA_2022_EVENT_RELATIVE_AOI_BBOX", source)
        self.assertNotIn("aoi_provenance", self.new)

    def test_03_all_three_mugla_experiments_resolve_to_one_geometry(self):
        sentinel = object()
        with patch.object(regions, "build_regions", return_value={REGION_KEY: sentinel}):
            for experiment_id in (SOURCE_ID, LEGACY_ID, EVENT_ID):
                self.assertIs(regions.get_region_for_experiment(experiment_id), sentinel)

    def test_03_static_aoi_provenance_hash_matches_the_source_experiment(self):
        from scripts.run_label_gate_only import _static_region_aoi_provenance

        new_prov = _static_region_aoi_provenance(REGION_KEY)
        self.assertIsNotNone(new_prov)
        self.assertEqual(list(new_prov["bounds"]), list(regions.MUGLA_AOI_BBOX))

    def test_04_event_to_event_framing_metadata_is_explicit(self):
        self.assertEqual(self.new["transfer_framing"], "same_geography_event_to_event")
        self.assertEqual(self.new["event_anchor_date"], "2022-06-21")
        self.assertEqual(
            self.new["event_anchor_basis"],
            "dominant MCD64A1 event identified independently before window revision",
        )
        self.assertEqual(
            self.new["event_window_rule"],
            "same-AOI 2021 duration preserved: 58-day predictor ending one day "
            "before ignition; 49-day label beginning on ignition",
        )

    def test_04_notes_state_the_confound_and_avoid_a_pure_temporal_claim(self):
        notes = self.new["notes"].lower()
        self.assertIn("not a pure temporal-transfer experiment", notes)
        self.assertIn("confounded", notes)
        self.assertIn("seasonal phase", notes)
        self.assertIn("same-geography event-to-event", notes)

    def test_04_framing_metadata_enters_the_gate_analysis_id(self):
        from scripts.run_label_gate_only import build_gate_manifest

        manifest = build_gate_manifest(EVENT_ID, self.new, {}, {"gate_result": {}})
        scientific = manifest["scientific"]
        self.assertEqual(scientific["transfer_framing"], "same_geography_event_to_event")
        self.assertEqual(scientific["event_anchor_date"], "2022-06-21")
        self.assertIn("event_anchor_basis", scientific)
        self.assertIn("event_window_rule", scientific)
        self.assertTrue(manifest["analysis_id"])
        self.assertFalse(manifest["downstream_authorized"])

    def test_04_ordinary_experiments_declare_no_framing_fields(self):
        for experiment_id in CANONICAL_FIVE_SPATIAL_AOIS + ("kozan_2023", LEGACY_ID):
            record = regions.get_experiment(experiment_id)
            for key in ("transfer_framing", "event_anchor_date",
                        "event_anchor_basis", "event_window_rule"):
                self.assertNotIn(key, record, f"{experiment_id}.{key}")


# =============================================================================
# 5-6. Cohort firewall + no reuse of the superseded namespace
# =============================================================================
class TestCohortFirewall(unittest.TestCase):
    def test_05_role_is_unchanged_and_non_cohort(self):
        from src.burned_pattern_audit import NON_COHORT_ROLES

        self.assertEqual(regions.get_experiment(EVENT_ID)["role"], ROLE)
        self.assertIn(ROLE, NON_COHORT_ROLES)
        self.assertIn("negative_control", NON_COHORT_ROLES)

    def test_05_role_does_not_leak_into_any_existing_role_cohort(self):
        for other_role in ("mediterranean_transfer_wildfire", "anchor_wildfire",
                           "same_country_same_year_transfer_wildfire",
                           "negative_control"):
            with self.subTest(role=other_role):
                self.assertNotIn(
                    EVENT_ID, regions.list_canonical_enabled_experiments(role=other_role))

    def test_05_discovery_excludes_it_even_with_a_step8a_dataset_present(self):
        import src.burned_pattern_audit as bpa

        present_path = Path(__file__).resolve()
        with patch.object(bpa, "canonical_step8a_path", return_value=present_path):
            resolution = bpa.resolve_experiments(all_enabled=True)

        self.assertNotIn(EVENT_ID, resolution.resolved_ids)
        self.assertEqual(resolution.excluded.get(EVENT_ID), ROLE)
        self.assertNotIn(LEGACY_ID, resolution.resolved_ids)

    def test_05_the_five_canonical_spatial_aois_are_unchanged(self):
        import src.burned_pattern_audit as bpa

        present_path = Path(__file__).resolve()
        with patch.object(bpa, "canonical_step8a_path", return_value=present_path):
            resolution = bpa.resolve_experiments(all_enabled=True)

        self.assertEqual(set(resolution.resolved_ids), set(CANONICAL_FIVE_SPATIAL_AOIS))

    def test_05_domain_classifier_discovery_excludes_it_too(self):
        # The domain-classifier audit reuses the SAME generic registry-driven
        # resolver, so the firewall holds there without a second rule.
        import src.burned_pattern_audit as bpa
        import src.domain_classifier_audit as dca

        present_path = Path(__file__).resolve()
        with patch.object(bpa, "canonical_step8a_path", return_value=present_path):
            resolution = dca.resolve_experiments(all_enabled=True)

        self.assertNotIn(EVENT_ID, resolution.resolved_ids)
        self.assertEqual(set(resolution.resolved_ids), set(CANONICAL_FIVE_SPATIAL_AOIS))
        # No six-region pair matrix: 5 AOIs -> 10 unordered pairs, unchanged.
        self.assertEqual(len(dca.generate_pairs(resolution.resolved_ids)), 10)

    def test_05_no_six_region_transfer_matrix_is_created(self):
        from src.era5_land_regional_diagnostic import DEFAULT_EXPERIMENTS
        from src.multi_region_window_closure.contract import ACTUAL_AOIS, REFERENCE_AOI

        self.assertEqual(DEFAULT_EXPERIMENTS, CANONICAL_FIVE_SPATIAL_AOIS)
        self.assertEqual(len(DEFAULT_EXPERIMENTS), 5)
        self.assertNotIn(EVENT_ID, DEFAULT_EXPERIMENTS)
        window_closure_aois = set(ACTUAL_AOIS) | {REFERENCE_AOI}
        self.assertNotIn(EVENT_ID, window_closure_aois)
        self.assertEqual(window_closure_aois, set(CANONICAL_FIVE_SPATIAL_AOIS))

    def test_06_output_namespace_is_disjoint_from_the_superseded_attempt(self):
        legacy_root = regions.get_experiment_output_root(LEGACY_ID).resolve()
        new_root = regions.get_experiment_output_root(EVENT_ID).resolve()
        self.assertEqual(new_root, (_PROJECT_ROOT / "outputs" / "experiments" / EVENT_ID).resolve())
        # Siblings: neither namespace contains the other.
        self.assertNotEqual(new_root, legacy_root)
        self.assertNotIn(legacy_root, new_root.parents)
        self.assertNotIn(new_root, legacy_root.parents)
        self.assertEqual(new_root.parent, legacy_root.parent)
        for step in ("gate_inputs", "validation", "step5", "step8a"):
            path = regions.get_step_output_dir(EVENT_ID, step)
            self.assertIn(EVENT_ID, path.parts)
            self.assertNotIn(LEGACY_ID, path.parts)
            assert_sibling_of_legacy_not_descendant(self, path, step)

    def test_06_no_planned_path_points_into_the_superseded_namespace(self):
        from scripts.run_label_gate_only import (
            _assert_paths_are_safely_namespaced,
            _namespaced_paths,
        )

        paths = _namespaced_paths(EVENT_ID)
        _assert_paths_are_safely_namespaced(EVENT_ID, paths)
        for name, value in paths.items():
            if value is None:
                continue
            assert_sibling_of_legacy_not_descendant(self, value, name)
            # LEGACY_ID may never appear as a whole path COMPONENT (a prefix
            # match inside 'mugla_2022_event_relative' is not a violation).
            self.assertNotIn(LEGACY_ID, Path(value).resolve().parts, name)

    def test_06_historical_source_is_the_2021_event_not_the_superseded_2022(self):
        contract = hbe.resolve_historical_burn_contract(regions.get_experiment(EVENT_ID))
        self.assertEqual(contract["source_experiment_id"], SOURCE_ID)
        self.assertNotEqual(contract["source_experiment_id"], LEGACY_ID)
        self.assertNotIn(f"/{LEGACY_ID}/", contract["source_step8a_parquet_path"])

    def test_06_path_resolution_creates_nothing(self):
        root = regions.get_experiment_output_root(EVENT_ID)
        existed = root.exists()
        regions.get_step_output_dir(EVENT_ID, "step8a")
        hbe.canonical_source_step8a_parquet(SOURCE_ID)
        self.assertEqual(root.exists(), existed)


# =============================================================================
# 7-8. Historical exclusion contract, source mask, manifest integrity
# =============================================================================
def _write_source_parquet(path: Path, burned_cells: list[str], extra_rows: int = 3) -> Path:
    """Minimal synthetic 'canonical Step8A' source dataset."""
    rows = []
    for index, cell_id in enumerate(burned_cells):
        row, col = cell_id[1:].split("_c")
        rows.append({
            "cell_id": cell_id, "row_500m": int(row), "col_500m": int(col),
            "burned": 1, "burn_date": f"2021-08-{(index % 28) + 1:02d}",
            "burn_day_of_year": 213 + index,
            # Deliberately varied so the mask can be shown NOT to depend on them.
            "analysis_eligible": index % 2 == 0,
            "valid_for_modeling": index % 3 == 0,
            "burnable_tree_shrub_grass": index % 2 == 1,
            "landcover_dominant": "cropland" if index % 2 else "tree_cover",
        })
    for index in range(extra_rows):
        rows.append({
            "cell_id": f"r9_c{index}", "row_500m": 9, "col_500m": index,
            "burned": 0, "burn_date": "0", "burn_day_of_year": 0.0,
            "analysis_eligible": True, "valid_for_modeling": True,
            "burnable_tree_shrub_grass": True, "landcover_dominant": "tree_cover",
        })
    path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_parquet(path, index=False)
    return path


class TestHistoricalContractResolution(unittest.TestCase):
    def test_07_registry_declares_the_generic_historical_fields(self):
        record = regions.get_experiment(EVENT_ID)
        self.assertIs(record["exclude_historical_burns"], True)
        self.assertEqual(record["historical_burn_source_experiment"], SOURCE_ID)
        self.assertEqual(record["historical_burn_source_kind"],
                         "canonical_step8a_physical_burned_cells")
        self.assertEqual(record["historical_burn_source_expected_count"],
                         EXPECTED_SOURCE_BURNED)

    def test_07_no_other_experiment_declares_historical_exclusion(self):
        for experiment_id, record in regions.EXPERIMENTS.items():
            if experiment_id == EVENT_ID:
                continue
            with self.subTest(experiment_id=experiment_id):
                self.assertNotIn("exclude_historical_burns", record)
                self.assertIsNone(hbe.resolve_historical_burn_contract(
                    regions.get_experiment(experiment_id)))

    def test_07_source_path_is_the_canonical_step8a_parquet(self):
        contract = hbe.resolve_historical_burn_contract(regions.get_experiment(EVENT_ID))
        self.assertTrue(contract["source_step8a_parquet_path"].endswith(
            f"outputs/experiments/{SOURCE_ID}/step8a/step8a_500m_modeling_dataset.parquet"))

    def test_07_mask_definition_is_burned_equals_one_and_nothing_else(self):
        contract = hbe.resolve_historical_burn_contract(regions.get_experiment(EVENT_ID))
        mask = contract["mask_definition"]
        self.assertIn("burned == 1", mask)
        for excluded_restriction in ("TSG", "analysis_eligible",
                                     "valid_for_modeling", "landcover"):
            self.assertIn(excluded_restriction, mask)
        self.assertIn("NOT restricted", mask)

    def test_07_mask_ignores_tsg_eligibility_and_landcover_columns(self):
        with tempfile.TemporaryDirectory() as tmp:
            burned = [f"r0_c{i}" for i in range(7)]
            source = _write_source_parquet(Path(tmp) / "src.parquet", burned)
            contract = {
                "target_experiment_id": "t", "source_experiment_id": "s",
                "source_step8a_parquet_path": str(source),
                "source_expected_physical_burned_count": len(burned),
            }
            burned_df, provenance = hbe.load_source_physical_burned_cells(contract)
            # Every burned==1 row is selected, regardless of the varied
            # analysis_eligible / valid_for_modeling / TSG / landcover values.
            self.assertEqual(sorted(burned_df["cell_id"]), sorted(burned))
            self.assertEqual(provenance["source_physical_burned_count"], len(burned))
            self.assertEqual(provenance["source_row_count"], len(burned) + 3)

    def test_07_frozen_expectation_mismatch_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = _write_source_parquet(Path(tmp) / "src.parquet",
                                           [f"r0_c{i}" for i in range(5)])
            contract = {
                "target_experiment_id": "t", "source_experiment_id": "s",
                "source_step8a_parquet_path": str(source),
                "source_expected_physical_burned_count": EXPECTED_SOURCE_BURNED,
            }
            with self.assertRaises(hbe.HistoricalBurnExclusionError) as raised:
                hbe.load_source_physical_burned_cells(contract)
            self.assertIn(str(EXPECTED_SOURCE_BURNED), str(raised.exception))

    def test_07_missing_source_fails_closed(self):
        contract = {
            "target_experiment_id": "t", "source_experiment_id": "s",
            "source_step8a_parquet_path": "/nonexistent/step8a.parquet",
            "source_expected_physical_burned_count": None,
        }
        with self.assertRaises(hbe.HistoricalBurnExclusionError):
            hbe.load_source_physical_burned_cells(contract)

    def test_07_missing_required_column_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "src.parquet"
            pd.DataFrame([{"cell_id": "r0_c0", "burned": 1}]).to_parquet(path, index=False)
            contract = {
                "target_experiment_id": "t", "source_experiment_id": "s",
                "source_step8a_parquet_path": str(path),
                "source_expected_physical_burned_count": None,
            }
            with self.assertRaises(hbe.HistoricalBurnExclusionError) as raised:
                hbe.load_source_physical_burned_cells(contract)
            self.assertIn("row_500m", str(raised.exception))

    def test_07_duplicate_or_null_source_cell_id_fails_closed(self):
        for rows, fragment in (
            ([{"cell_id": "r0_c0", "row_500m": 0, "col_500m": 0, "burned": 1},
              {"cell_id": "r0_c0", "row_500m": 0, "col_500m": 0, "burned": 1}], "duplicate"),
            ([{"cell_id": None, "row_500m": 0, "col_500m": 0, "burned": 1}], "null"),
        ):
            with self.subTest(fragment=fragment), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "src.parquet"
                pd.DataFrame(rows).to_parquet(path, index=False)
                contract = {
                    "target_experiment_id": "t", "source_experiment_id": "s",
                    "source_step8a_parquet_path": str(path),
                    "source_expected_physical_burned_count": None,
                }
                with self.assertRaises(hbe.HistoricalBurnExclusionError) as raised:
                    hbe.load_source_physical_burned_cells(contract)
                self.assertIn(fragment, str(raised.exception).lower())

    def test_07_unsupported_source_kind_fails_closed(self):
        record = dict(regions.get_experiment(EVENT_ID))
        record["historical_burn_source_kind"] = "something_else"
        with self.assertRaises(hbe.HistoricalBurnExclusionError):
            hbe.resolve_historical_burn_contract(record)

    def test_07_self_referential_source_fails_closed(self):
        record = dict(regions.get_experiment(EVENT_ID))
        record["historical_burn_source_experiment"] = EVENT_ID
        with self.assertRaises(hbe.HistoricalBurnExclusionError):
            hbe.resolve_historical_burn_contract(record)

    def test_07_real_source_yields_exactly_3073_physical_burned_cells(self):
        # Read-only inspection of the frozen canonical source artifact. It is
        # opened, never written. Skipped rather than failed if absent, so this
        # suite stays runnable on a checkout without the large outputs.
        contract = hbe.resolve_historical_burn_contract(regions.get_experiment(EVENT_ID))
        source_path = Path(contract["source_step8a_parquet_path"])
        if not source_path.is_file():
            self.skipTest(f"canonical source artifact absent: {source_path}")
        before = source_path.stat().st_mtime_ns
        burned_df, provenance = hbe.load_source_physical_burned_cells(contract)
        self.assertEqual(len(burned_df), EXPECTED_SOURCE_BURNED)
        self.assertEqual(provenance["source_physical_burned_count"], EXPECTED_SOURCE_BURNED)
        self.assertEqual(burned_df["cell_id"].nunique(), EXPECTED_SOURCE_BURNED)
        self.assertEqual(len(provenance["source_step8a_parquet_sha256"]), 64)
        # The source artifact must not be modified by reading it.
        self.assertEqual(source_path.stat().st_mtime_ns, before)


class TestHistoricalManifestIntegrity(unittest.TestCase):
    """Manifest construction against a synthetic source + grid, in a tmpdir."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.burned = ["r1_c0", "r1_c1", "r2_c3"]
        self.source_parquet = _write_source_parquet(
            self.tmp / "source" / "step8a.parquet", self.burned)
        self.grid = _write_reference_grid(self.tmp / "reference_30m.tif")
        self.record = {
            "experiment_id": "target_exp",
            "region_key": REGION_KEY,
            "exclude_historical_burns": True,
            "historical_burn_source_experiment": SOURCE_ID,
            "historical_burn_source_kind": "canonical_step8a_physical_burned_cells",
            "historical_burn_source_expected_count": len(self.burned),
        }
        self.labels_dir = self.tmp / "labels"

    def _patched_build(self, force: bool = False):
        """Build the manifest with the source parquet and BOTH reference grids
        redirected into the temporary directory."""
        contract_patch = patch.object(
            hbe, "canonical_source_step8a_parquet", return_value=self.source_parquet)
        grid_patch = patch.object(hbe, "_reference_grid_path", return_value=self.grid)
        source_record_patch = patch.object(
            hbe, "get_experiment", return_value={"region_key": REGION_KEY})
        with contract_patch, grid_patch, source_record_patch:
            return hbe.build_historical_burn_exclusion_manifest(
                self.record, output_dir=self.labels_dir, force=force)

    def test_08_manifest_triplet_is_written_with_expected_rows(self):
        result = self._patched_build()
        self.assertTrue(result["created"])
        self.assertEqual(result["excluded_cell_count"], len(self.burned))
        for key in ("parquet_path", "csv_path", "metadata_path"):
            self.assertTrue(Path(result[key]).is_file(), key)
        self.assertEqual(
            Path(result["parquet_path"]).name, "historical_burn_excluded_cells.parquet")
        self.assertEqual(
            Path(result["csv_path"]).name, "historical_burn_excluded_cells.csv")
        self.assertEqual(
            Path(result["metadata_path"]).name,
            "historical_burn_excluded_cells_metadata.json")

    def test_08_manifest_rows_carry_the_required_fields(self):
        result = self._patched_build()
        frame = pd.read_parquet(result["parquet_path"])
        for column in ("experiment_id", "source_experiment_id", "cell_id",
                       "row_500m", "col_500m", "source_burned",
                       "source_burn_date", "source_burn_day_of_year",
                       "exclusion_reason"):
            self.assertIn(column, frame.columns)
        self.assertEqual(set(frame["experiment_id"]), {"target_exp"})
        self.assertEqual(set(frame["source_experiment_id"]), {SOURCE_ID})
        self.assertEqual(set(frame["exclusion_reason"]), {"historical_burn_excluded"})
        self.assertTrue(frame["source_burned"].all())
        self.assertEqual(sorted(frame["cell_id"]), sorted(self.burned))
        self.assertTrue(frame["cell_id"].is_unique)

    def test_08_metadata_records_full_provenance(self):
        result = self._patched_build()
        metadata = json.loads(Path(result["metadata_path"]).read_text(encoding="utf-8"))
        self.assertEqual(metadata["experiment_id"], "target_exp")
        self.assertEqual(metadata["source_experiment_id"], SOURCE_ID)
        self.assertEqual(metadata["source_step8a_parquet_path"], str(self.source_parquet))
        self.assertEqual(metadata["source_step8a_parquet_sha256"],
                         hbe.sha256_file(self.source_parquet))
        self.assertEqual(len(metadata["source_step8a_parquet_sha256"]), 64)
        self.assertEqual(metadata["source_row_count"], len(self.burned) + 3)
        self.assertEqual(metadata["source_physical_burned_count"], len(self.burned))
        self.assertEqual(metadata["unique_historical_excluded_count"], len(self.burned))
        self.assertIn("burned == 1", metadata["mask_definition"])
        self.assertIn("r{row_500m}_c{col_500m}", metadata["cell_id_scheme"])
        self.assertEqual(metadata["target_region_key"], REGION_KEY)
        self.assertEqual(metadata["source_region_key"], REGION_KEY)
        compat = metadata["region_grid_compatibility"]
        self.assertTrue(compat["region_key_matches_source"])
        self.assertTrue(compat["grid_identity_verified"])

    def test_08_source_artifact_is_never_modified(self):
        before = (self.source_parquet.stat().st_mtime_ns,
                  hbe.sha256_file(self.source_parquet))
        self._patched_build()
        after = (self.source_parquet.stat().st_mtime_ns,
                 hbe.sha256_file(self.source_parquet))
        self.assertEqual(before, after)

    def test_08_reader_round_trips_the_exact_cell_id_set(self):
        result = self._patched_build()
        ids = hbe.read_historical_burn_exclusion_manifest(
            Path(result["parquet_path"]), experiment_id="target_exp")
        self.assertEqual(set(ids), set(self.burned))

    def test_08_reader_rejects_a_foreign_experiment_id(self):
        result = self._patched_build()
        with self.assertRaises(hbe.HistoricalBurnExclusionError) as raised:
            hbe.read_historical_burn_exclusion_manifest(
                Path(result["parquet_path"]), experiment_id="some_other_experiment")
        self.assertIn("MISMATCH", str(raised.exception))

    def test_08_reader_requires_the_sidecar_metadata(self):
        result = self._patched_build()
        Path(result["metadata_path"]).unlink()
        with self.assertRaises(hbe.HistoricalBurnExclusionError):
            hbe.read_historical_burn_exclusion_manifest(
                Path(result["parquet_path"]), experiment_id="target_exp")

    def test_08_reader_rejects_a_missing_manifest(self):
        with self.assertRaises(hbe.HistoricalBurnExclusionError):
            hbe.read_historical_burn_exclusion_manifest(
                self.labels_dir / "historical_burn_excluded_cells.parquet",
                experiment_id="target_exp")

    def test_08_reader_rejects_duplicate_cell_ids(self):
        result = self._patched_build()
        frame = pd.read_parquet(result["parquet_path"])
        pd.concat([frame, frame.iloc[[0]]]).to_parquet(result["parquet_path"], index=False)
        with self.assertRaises(hbe.HistoricalBurnExclusionError) as raised:
            hbe.read_historical_burn_exclusion_manifest(Path(result["parquet_path"]))
        self.assertIn("duplicate", str(raised.exception).lower())

    def test_08_partial_manifest_triplet_fails_closed(self):
        result = self._patched_build()
        Path(result["csv_path"]).unlink()
        with self.assertRaises(hbe.HistoricalBurnExclusionError) as raised:
            self._patched_build()
        self.assertIn("PARTIALLY", str(raised.exception))

    def test_08_existing_manifest_is_reused_when_the_contract_is_unchanged(self):
        first = self._patched_build()
        second = self._patched_build()
        self.assertTrue(first["created"])
        self.assertFalse(second["created"])
        self.assertTrue(second["reused_existing"])
        self.assertEqual(second["excluded_cell_count"], len(self.burned))

    def test_08_existing_manifest_fails_closed_when_the_source_drifts(self):
        self._patched_build()
        # Regenerate the source with a different burned set -> different SHA.
        self.burned = ["r1_c0", "r1_c1", "r2_c3", "r4_c4"]
        self.record["historical_burn_source_expected_count"] = len(self.burned)
        _write_source_parquet(self.source_parquet, self.burned)
        with self.assertRaises(hbe.HistoricalBurnExclusionError) as raised:
            self._patched_build()
        self.assertIn("no longer matches", str(raised.exception))
        # force regenerates deliberately.
        regenerated = self._patched_build(force=True)
        self.assertTrue(regenerated["created"])
        self.assertEqual(regenerated["excluded_cell_count"], len(self.burned))

    def test_08_region_mismatch_fails_closed(self):
        contract = {
            "target_experiment_id": "t", "source_experiment_id": "s",
            "target_region_key": "mugla_aoi", "source_region_key": "manavgat_aoi",
        }
        with self.assertRaises(hbe.HistoricalBurnExclusionError) as raised:
            hbe.verify_region_grid_compatibility(contract, require_target_grid=False)
        self.assertIn("region_key differs", str(raised.exception))

    def test_08_unresolvable_region_fails_closed(self):
        contract = {
            "target_experiment_id": "t", "source_experiment_id": "s",
            "target_region_key": None, "source_region_key": "mugla_aoi",
        }
        with self.assertRaises(hbe.HistoricalBurnExclusionError):
            hbe.verify_region_grid_compatibility(contract, require_target_grid=False)

    def test_08_grid_mismatch_fails_closed(self):
        other_grid = _write_reference_grid(self.tmp / "other_grid.tif", height=51)
        contract = {
            "target_experiment_id": "t", "source_experiment_id": "s",
            "target_region_key": REGION_KEY, "source_region_key": REGION_KEY,
        }

        def _grid_for(experiment_id):
            return self.grid if experiment_id == "s" else other_grid

        with patch.object(hbe, "_reference_grid_path", side_effect=_grid_for):
            with self.assertRaises(hbe.HistoricalBurnExclusionError) as raised:
                hbe.verify_region_grid_compatibility(contract, require_target_grid=True)
        self.assertIn("NOT identical", str(raised.exception))

    def test_08_missing_grid_fails_closed_when_required(self):
        contract = {
            "target_experiment_id": "t", "source_experiment_id": "s",
            "target_region_key": REGION_KEY, "source_region_key": REGION_KEY,
        }
        with patch.object(hbe, "_reference_grid_path",
                          return_value=self.tmp / "absent.tif"):
            with self.assertRaises(hbe.HistoricalBurnExclusionError) as raised:
                hbe.verify_region_grid_compatibility(contract, require_target_grid=True)
        self.assertIn("cannot be validated", str(raised.exception))


# =============================================================================
# Synthetic raster helpers (tiny, tmpdir-only; no project path is touched)
# =============================================================================
BLOCK = compute_block_size_pixels()
N_CELLS = 2
GRID_PIXELS = BLOCK * N_CELLS
GRID_TRANSFORM = from_origin(27.10, 37.45, 0.00027, 0.00027)
GRID_CRS = "EPSG:4326"

#: The four synthetic cells, one per eligibility case.
CELL_NEITHER = "r0_c0"
CELL_PRE_LABEL_ONLY = "r0_c1"
CELL_HISTORICAL_ONLY = "r1_c0"
CELL_BOTH = "r1_c1"
ALL_CELLS = (CELL_NEITHER, CELL_PRE_LABEL_ONLY, CELL_HISTORICAL_ONLY, CELL_BOTH)
HISTORICAL_IDS = frozenset({CELL_HISTORICAL_ONLY, CELL_BOTH})

#: In-label-window and in-pre-label-window day-of-year values for 2022.
LABEL_DOY = 190           # 2022-07-09, inside 2022-06-21..2022-08-08
PRE_LABEL_DOY = 150       # 2022-05-30, inside 2022-04-24..2022-06-20


def _write_grid(path: Path, values: np.ndarray, dtype: str = "float32") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(
        path, "w", driver="GTiff", width=GRID_PIXELS, height=GRID_PIXELS,
        count=1, dtype=dtype, crs=GRID_CRS, transform=GRID_TRANSFORM,
    ) as dst:
        dst.write(values.astype(dtype), 1)
    return path


def _write_reference_grid(path: Path, height: int | None = None) -> Path:
    """Reference-grid raster used only for identity comparison."""
    rows = height if height is not None else GRID_PIXELS
    path.parent.mkdir(parents=True, exist_ok=True)
    with rasterio.open(
        path, "w", driver="GTiff", width=GRID_PIXELS, height=rows, count=1,
        dtype="float32", crs=GRID_CRS, transform=GRID_TRANSFORM,
    ) as dst:
        dst.write(np.zeros((rows, GRID_PIXELS), dtype="float32"), 1)
    return path


def _cell_slice(cell_id: str) -> tuple[slice, slice]:
    row, col = cell_id[1:].split("_c")
    r, c = int(row), int(col)
    return slice(r * BLOCK, (r + 1) * BLOCK), slice(c * BLOCK, (c + 1) * BLOCK)


def _constant_grid(value: float) -> np.ndarray:
    return np.full((GRID_PIXELS, GRID_PIXELS), value, dtype="float32")


def _label_array(burned_cells) -> np.ndarray:
    array = np.zeros((GRID_PIXELS, GRID_PIXELS), dtype="float32")
    for cell_id in burned_cells:
        rows, cols = _cell_slice(cell_id)
        array[rows, cols] = LABEL_DOY
    return array


def _pre_label_array(pre_cells) -> np.ndarray:
    array = np.zeros((GRID_PIXELS, GRID_PIXELS), dtype="float32")
    for cell_id in pre_cells:
        rows, cols = _cell_slice(cell_id)
        array[rows, cols] = PRE_LABEL_DOY
    return array


class _SyntheticRasters:
    """Builds the shared raster set for the gate/Step8A exclusion tests."""

    def __init__(self, tmp: Path, burned_cells=ALL_CELLS, pre_cells=(CELL_PRE_LABEL_ONLY, CELL_BOTH)):
        self.dir = tmp
        # Every cell would be BURNED if it were not excluded -- this is what
        # makes "excluded cells never enter burned/unburned counts" testable.
        self.label = _write_grid(tmp / "mcd64a1_raw.tif", _label_array(burned_cells))
        self.pre_label = _write_grid(tmp / "prelabel_raw.tif", _pre_label_array(pre_cells))
        self.reference = _write_grid(tmp / "reference_30m.tif", _constant_grid(20.0))
        self.landcover = _write_grid(
            tmp / "landcover.tif", _constant_grid(10), dtype="uint8")  # tree_cover
        self.ndvi = _write_grid(tmp / "ndvi.tif", _constant_grid(0.4))
        self.elevation = _write_grid(tmp / "elevation.tif", _constant_grid(300.0))
        self.slope = _write_grid(tmp / "slope.tif", _constant_grid(5.0))


def _run_gate(rasters: _SyntheticRasters, out_dir: Path, **overrides) -> dict:
    kwargs = dict(
        label_path=rasters.label,
        label_kind=LABEL_KIND_RAW,
        reference_path=rasters.reference,
        landcover_path=rasters.landcover,
        label_start=LABEL_START,
        label_end=LABEL_END,
        output_dir=out_dir,
        min_positives=1,
        natural_threshold=0.5,
        cropland_threshold=0.5,
        exclude_pre_label_burns=True,
        pre_label_label_path=rasters.pre_label,
        predictor_start=PREDICTOR_START,
        predictor_end=PREDICTOR_END,
        experiment_id=EVENT_ID,
        exclude_historical_burns=True,
        historical_excluded_cell_ids=HISTORICAL_IDS,
    )
    kwargs.update(overrides)
    return compute_gate(**kwargs)


# =============================================================================
# 9-11. Gate: eligibility cases, union arithmetic, partition
# =============================================================================
class TestGateUnionExclusion(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.rasters = _SyntheticRasters(self.tmp)
        self.out = self.tmp / "out"
        self.out.mkdir()
        self.gate = _run_gate(self.rasters, self.out)

    def test_09_each_exclusion_reason_keeps_its_own_independent_count(self):
        # pre-label: r0_c1 + r1_c1 ; historical: r1_c0 + r1_c1
        self.assertEqual(self.gate["pre_label_burn_excluded_count"], 2)
        self.assertEqual(self.gate["historical_burn_excluded_count"], 2)
        self.assertEqual(self.gate["pre_label_historical_overlap_count"], 1)

    def test_09_manifest_rows_cover_the_pre_label_axis_only(self):
        rows = self.gate["pre_label_excluded_manifest_rows"]
        self.assertEqual(sorted(r["cell_id"] for r in rows),
                         sorted([CELL_PRE_LABEL_ONLY, CELL_BOTH]))
        # A both-excluded cell still appears in the PRE-LABEL manifest: the
        # two manifests stay independent and are never merged.
        self.assertIn(CELL_BOTH, {r["cell_id"] for r in rows})
        self.assertEqual({r["exclusion_reason"] for r in rows},
                         {"pre_label_burn_excluded"})

    def test_10_union_arithmetic_holds(self):
        self.assertEqual(self.gate["total_unique_excluded_count"], 3)
        self.assertEqual(
            self.gate["total_unique_excluded_count"],
            self.gate["pre_label_burn_excluded_count"]
            + self.gate["historical_burn_excluded_count"]
            - self.gate["pre_label_historical_overlap_count"],
        )

    def test_10_partition_assertion_holds(self):
        self.assertEqual(
            self.gate["total_unique_excluded_count"]
            + self.gate["burned_count"] + self.gate["unburned_count"],
            self.gate["total_valid_cells_or_pixels_considered"],
        )
        self.assertEqual(self.gate["total_valid_cells_or_pixels_considered"], len(ALL_CELLS))
        self.assertEqual(self.gate["analysis_universe_cells_after_exclusions"], 1)

    def test_11_excluded_cells_never_enter_burned_or_unburned_counts(self):
        # All four cells carry an in-window BurnDate, but only the
        # neither-excluded one may be counted.
        self.assertEqual(self.gate["burned_count"], 1)
        self.assertEqual(self.gate["unburned_count"], 0)

    def test_11_excluded_cells_are_in_no_gate_denominator(self):
        self.assertEqual(self.gate["burned_tree_shrub_grass_count"], 1)
        self.assertEqual(self.gate["burned_natural_vegetation_fraction"], 1.0)
        # The landcover breakdown of the excluded cells is reported but is
        # never part of the burned denominator.
        self.assertEqual(self.gate["pre_label_burn_excluded_breakdown"]["total"], 2)
        self.assertEqual(self.gate["historical_burn_excluded_breakdown"]["total"], 2)
        self.assertEqual(self.gate["burned_landcover_dominant_counts"], {"tree_cover": 1})

    def test_09_neither_excluded_cell_survives_into_the_analysis_universe(self):
        # Only CELL_NEITHER is left; with tree_cover landcover it is the sole
        # burned natural-vegetation cell.
        self.assertEqual(self.gate["decision"], "wildfire_candidate_pass")

    def test_09_historical_only_experiment_still_excludes_correctly(self):
        out = self.tmp / "hist_only"
        out.mkdir()
        gate = _run_gate(
            self.rasters, out,
            exclude_pre_label_burns=False, pre_label_label_path=None,
            predictor_start=None, predictor_end=None,
        )
        self.assertEqual(gate["pre_label_burn_excluded_count"], 0)
        self.assertEqual(gate["historical_burn_excluded_count"], 2)
        self.assertEqual(gate["pre_label_historical_overlap_count"], 0)
        self.assertEqual(gate["total_unique_excluded_count"], 2)
        self.assertEqual(gate["burned_count"], 2)
        self.assertEqual(gate["unburned_count"], 0)

    def test_09_pre_label_only_experiment_is_byte_compatible_with_before(self):
        out = self.tmp / "pre_only"
        out.mkdir()
        gate = _run_gate(
            self.rasters, out,
            exclude_historical_burns=False, historical_excluded_cell_ids=None,
        )
        self.assertEqual(gate["historical_burn_excluded_count"], 0)
        self.assertEqual(gate["pre_label_historical_overlap_count"], 0)
        # With no historical axis the union count collapses to the pre-label
        # count -- the pre-existing partition assertion, unchanged.
        self.assertEqual(gate["total_unique_excluded_count"],
                         gate["pre_label_burn_excluded_count"])
        self.assertEqual(gate["total_unique_excluded_count"], 2)
        self.assertEqual(gate["burned_count"], 2)
        self.assertIs(gate["exclude_historical_burns"], False)
        self.assertEqual(gate["historical_burn_exclusion_rule"], "not_applied")

    def test_09_neither_axis_leaves_every_cell_in_the_universe(self):
        out = self.tmp / "no_exclusion"
        out.mkdir()
        gate = _run_gate(
            self.rasters, out,
            exclude_pre_label_burns=False, pre_label_label_path=None,
            predictor_start=None, predictor_end=None,
            exclude_historical_burns=False, historical_excluded_cell_ids=None,
        )
        self.assertEqual(gate["total_unique_excluded_count"], 0)
        self.assertEqual(gate["burned_count"], len(ALL_CELLS))
        self.assertEqual(gate["analysis_universe_cells_after_exclusions"], len(ALL_CELLS))

    def test_10_enabled_historical_axis_without_a_set_fails_closed(self):
        out = self.tmp / "missing_set"
        out.mkdir()
        with self.assertRaises(Step6BError) as raised:
            _run_gate(self.rasters, out, historical_excluded_cell_ids=None)
        self.assertIn("historical_excluded_", str(raised.exception))


# =============================================================================
# 12. Step8A union semantics
# =============================================================================
class TestStep8AUnionEligibility(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.rasters = _SyntheticRasters(self.tmp)
        self.out = self.tmp / "step8a"
        self.out.mkdir()

    def _build(self, pre_ids=frozenset({CELL_PRE_LABEL_ONLY, CELL_BOTH}),
               hist_ids=HISTORICAL_IDS):
        return build_dataset(
            reference_path=self.rasters.reference,
            label_path=self.rasters.label,
            label_kind=LABEL_KIND_RAW,
            predictor_paths={
                "ndvi": self.rasters.ndvi,
                "elevation": self.rasters.elevation,
                "slope": self.rasters.slope,
            },
            landcover_path=self.rasters.landcover,
            source_mask_path=None,
            output_dir=self.out,
            min_valid_fraction=0.5,
            burnable_threshold=0.5,
            label_start=LABEL_START,
            label_end=LABEL_END,
            pre_label_excluded_cell_ids=pre_ids,
            historical_excluded_cell_ids=hist_ids,
        )

    def test_12_all_three_exclusion_columns_are_present(self):
        frame = self._build()["dataframe"].set_index("cell_id")
        for column in ("pre_label_burn_excluded", "historical_burn_excluded",
                       "analysis_eligible", "valid_for_modeling", "invalid_reason"):
            self.assertIn(column, frame.columns)

    def test_12_the_four_eligibility_cases_are_exact(self):
        frame = self._build()["dataframe"].set_index("cell_id")
        expected = {
            #                       pre,   historical, eligible
            CELL_NEITHER:          (False, False, True),
            CELL_PRE_LABEL_ONLY:   (True,  False, False),
            CELL_HISTORICAL_ONLY:  (False, True,  False),
            CELL_BOTH:             (True,  True,  False),
        }
        for cell_id, (pre, hist, eligible) in expected.items():
            with self.subTest(cell_id=cell_id):
                row = frame.loc[cell_id]
                self.assertEqual(bool(row["pre_label_burn_excluded"]), pre)
                self.assertEqual(bool(row["historical_burn_excluded"]), hist)
                self.assertEqual(bool(row["analysis_eligible"]), eligible)

    def test_12_valid_for_modeling_is_eligibility_and_predictor_validity(self):
        frame = self._build()["dataframe"].set_index("cell_id")
        # Predictors are finite everywhere, so eligibility alone decides.
        self.assertTrue(bool(frame.loc[CELL_NEITHER, "valid_for_modeling"]))
        for cell_id in (CELL_PRE_LABEL_ONLY, CELL_HISTORICAL_ONLY, CELL_BOTH):
            self.assertFalse(bool(frame.loc[cell_id, "valid_for_modeling"]), cell_id)

    def test_12_invalid_reason_preserves_both_exclusion_reasons(self):
        frame = self._build()["dataframe"].set_index("cell_id")
        # A cell with no invalid reason is written as Python None, but pandas
        # normalises that to its own missing sentinel (NaN/NA) when the column
        # is materialised. Assert MISSINGNESS, not object identity -- the
        # scientific claim is "no reason recorded", not "the object is None".
        self.assertTrue(pd.isna(frame.loc[CELL_NEITHER, "invalid_reason"]))
        # Cells WITH exclusions keep their exact reason strings, unweakened:
        # each axis is preserved on its own, and a both-excluded cell carries
        # BOTH reasons (pre-label first, then historical).
        self.assertEqual(frame.loc[CELL_PRE_LABEL_ONLY, "invalid_reason"],
                         "pre_label_burn_excluded")
        self.assertEqual(frame.loc[CELL_HISTORICAL_ONLY, "invalid_reason"],
                         "historical_burn_excluded")
        self.assertEqual(frame.loc[CELL_BOTH, "invalid_reason"],
                         "pre_label_burn_excluded;historical_burn_excluded")
        self.assertEqual(
            frame.loc[CELL_BOTH, "invalid_reason"].split(";"),
            ["pre_label_burn_excluded", "historical_burn_excluded"],
        )

    def test_12_raw_burned_labels_are_preserved_for_audit(self):
        # Exclusion changes eligibility, never the raw label column.
        frame = self._build()["dataframe"].set_index("cell_id")
        for cell_id in ALL_CELLS:
            self.assertEqual(int(frame.loc[cell_id, "burned"]), 1, cell_id)

    def test_12_counters_report_the_union_and_the_overlap(self):
        counters = self._build()["counters"]
        self.assertEqual(counters["pre_label_burn_excluded_count"], 2)
        self.assertEqual(counters["historical_burn_excluded_count"], 2)
        self.assertEqual(counters["pre_label_historical_overlap_count"], 1)
        self.assertEqual(counters["total_unique_excluded_count"], 3)
        self.assertEqual(counters["analysis_eligible_count"], 1)
        self.assertEqual(
            counters["analysis_eligible_count"] + counters["total_unique_excluded_count"],
            counters["total_500m_cells"],
        )

    def test_12_manifest_ids_outside_the_grid_fail_closed(self):
        with self.assertRaises(Step8AError) as raised:
            self._build(hist_ids=frozenset({CELL_BOTH, "r99_c99"}))
        self.assertIn("do not exist in this dataset's 500 m grid", str(raised.exception))

    def test_12_no_exclusion_sets_leaves_every_cell_eligible(self):
        result = self._build(pre_ids=None, hist_ids=None)
        frame = result["dataframe"]
        self.assertTrue(frame["analysis_eligible"].all())
        self.assertFalse(frame["pre_label_burn_excluded"].any())
        self.assertFalse(frame["historical_burn_excluded"].any())
        self.assertEqual(result["counters"]["total_unique_excluded_count"], 0)


# =============================================================================
# 13-15. The 30-burn gate vs the 300-TSG stop
# =============================================================================
class TestSampleSizeRules(unittest.TestCase):
    def test_13_global_composition_gate_min_positives_is_still_30(self):
        from core.config import STEP6_BURNED_LANDCOVER_GATE_MIN_POSITIVES

        self.assertEqual(STEP6_BURNED_LANDCOVER_GATE_MIN_POSITIVES, 30)

    def test_13_composition_gate_semantics_are_unchanged(self):
        from src.step6b_burned_landcover_gate import classify_gate_decision

        # min_positives applies to TOTAL burned across every landcover.
        decision, _ = classify_gate_decision(
            burned_count=29, natural_fraction=1.0, cropland_fraction=0.0,
            min_positives=30, natural_threshold=0.5, cropland_threshold=0.5)
        self.assertEqual(decision, "insufficient_burned_positives")
        decision, _ = classify_gate_decision(
            burned_count=30, natural_fraction=1.0, cropland_fraction=0.0,
            min_positives=30, natural_threshold=0.5, cropland_threshold=0.5)
        self.assertEqual(decision, "wildfire_candidate_pass")

    def test_14_the_300_threshold_is_declared_only_for_the_event_experiment(self):
        record = regions.get_experiment(EVENT_ID)
        self.assertEqual(record["primary_population"], "burnable_tree_shrub_grass")
        self.assertEqual(record["min_primary_population_burned"], 300)
        for experiment_id in regions.EXPERIMENTS:
            if experiment_id == EVENT_ID:
                continue
            with self.subTest(experiment_id=experiment_id):
                other = regions.EXPERIMENTS[experiment_id]
                self.assertNotIn("primary_population", other)
                self.assertNotIn("min_primary_population_burned", other)

    def test_14_the_300_threshold_is_not_a_global_config_constant(self):
        # The per-experiment TSG rule lives in the registry, never in
        # core/config.py -- otherwise it would silently apply project-wide.
        import core.config as config

        for forbidden in ("STEP6_MIN_PRIMARY_POPULATION_BURNED",
                          "MIN_PRIMARY_POPULATION_BURNED",
                          "STEP6_BURNED_LANDCOVER_GATE_MIN_PRIMARY_POPULATION"):
            self.assertFalse(hasattr(config, forbidden), forbidden)
        # Pre-existing, unrelated config constants stay exactly as they were.
        self.assertEqual(config.STEP8B_PRIMARY_POPULATION, "all_valid")
        self.assertEqual(config.STEP8B_MIN_POSITIVES_PER_POPULATION, 30)

    def test_14_undeclared_experiments_get_no_sample_size_structure(self):
        self.assertIsNone(evaluate_primary_population_sample_size(
            primary_population_burned_count=0, population=None, min_burned_required=None))

    def test_14_half_configured_rule_fails_closed(self):
        with self.assertRaises(Step6BError):
            evaluate_primary_population_sample_size(
                primary_population_burned_count=500,
                population="burnable_tree_shrub_grass", min_burned_required=None)

    def test_15_tsg_299_stops(self):
        result = evaluate_primary_population_sample_size(
            primary_population_burned_count=299,
            population="burnable_tree_shrub_grass", min_burned_required=300)
        self.assertEqual(result["decision"], PRIMARY_POPULATION_GATE_STOP)
        self.assertEqual(result["stop_state"], PRIMARY_POPULATION_STOP)
        self.assertEqual(result["stop_state"], "insufficient_primary_population_burned")
        self.assertEqual(result["population"], "burnable_tree_shrub_grass")
        self.assertEqual(result["burned_count"], 299)
        self.assertEqual(result["min_burned_required"], 300)
        self.assertFalse(result["downstream_authorized"])

    def test_15_tsg_300_passes_the_sample_size_rule(self):
        result = evaluate_primary_population_sample_size(
            primary_population_burned_count=300,
            population="burnable_tree_shrub_grass", min_burned_required=300)
        self.assertEqual(result["decision"], PRIMARY_POPULATION_GATE_PASS)
        self.assertIsNone(result["stop_state"])
        # Passing this rule still does NOT authorize downstream.
        self.assertFalse(result["downstream_authorized"])

    def test_15_stop_is_never_a_composition_gate_failure(self):
        result = evaluate_primary_population_sample_size(
            primary_population_burned_count=299,
            population="burnable_tree_shrub_grass", min_burned_required=300)
        self.assertNotIn(result["decision"],
                         {"insufficient_burned_positives", "cropland_dominated_control",
                          "mixed_or_uncertain", "wildfire_candidate_pass"})
        self.assertIn("NOT a natural/cropland composition gate failure",
                      result["reason"])

    def test_15_gate_reports_the_rule_separately_from_its_decision(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        rasters = _SyntheticRasters(tmp)
        out = tmp / "out"
        out.mkdir()
        gate = _run_gate(
            rasters, out,
            primary_population="burnable_tree_shrub_grass",
            min_primary_population_burned=300,
        )
        # One surviving burned TSG cell, far below 300.
        self.assertEqual(gate["burned_tree_shrub_grass_count"], 1)
        primary = gate["primary_population_sample_size_gate"]
        self.assertEqual(primary["decision"], PRIMARY_POPULATION_GATE_STOP)
        self.assertEqual(primary["burned_count"], 1)
        self.assertEqual(primary["min_burned_required"], 300)
        # The composition decision is reported independently and is unaffected.
        self.assertEqual(gate["decision"], "wildfire_candidate_pass")
        self.assertEqual(gate["thresholds"]["min_positives"], 1)

    def test_15_gate_without_the_rule_reports_none(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        rasters = _SyntheticRasters(tmp)
        out = tmp / "out"
        out.mkdir()
        gate = _run_gate(rasters, out)
        self.assertIsNone(gate["primary_population_sample_size_gate"])

    def test_15_unknown_primary_population_fails_closed(self):
        tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, tmp, ignore_errors=True)
        rasters = _SyntheticRasters(tmp)
        out = tmp / "out"
        out.mkdir()
        with self.assertRaises(Step6BError):
            _run_gate(rasters, out, primary_population="not_a_population",
                      min_primary_population_burned=300)


# =============================================================================
# Gate-manifest schema: additive ONLY for opted-in experiments
# =============================================================================
#: The exact pre-patch `scientific` key set. An experiment that opts into none
#: of the new contracts must still produce EXACTLY these keys -- `scientific`
#: is hashed into analysis_id, so an extra "not applied" placeholder key would
#: silently change every existing experiment's analysis_id.
PRE_PATCH_SCIENTIFIC_KEYS = frozenset({
    "experiment_id", "region_key", "aoi", "predictor_window", "label_window",
    "baseline_years", "primary_population", "modeling_grid_m",
    "exclude_pre_label_burns", "pre_label_burn_window",
    "pre_label_burn_exclusion_rule",
})

NEW_SCIENTIFIC_CONTRACT_KEYS = frozenset({
    "historical_burn_exclusion", "primary_population_sample_size_rule",
})


class TestManifestSchemaBackwardCompatibility(unittest.TestCase):
    """`build_gate_manifest` is a pure builder: resolved provenance is supplied
    BY THE CALLER, never fabricated internally.

    These tests therefore reproduce the production caller contract
    (scripts/run_label_gate_only.main) rather than calling the builder with
    less context than production gives it. Production resolves the historical
    description once and passes it in; omitting it here would exercise a
    code path production never takes.
    """

    def _historical_description(self, experiment_id: str) -> dict | None:
        """The SAME resolved description production passes to the builder.

        Read-only: `describe_historical_burn_contract` resolves the contract,
        the canonical source path/SHA/physical-burned count and region/grid
        identity without creating or writing anything. Nothing is hard-coded
        here -- the 3073 count and the source SHA come from the public
        resolver, exactly as they do in production.

        Returns None for every experiment that does not opt in, which is what
        production passes for them.
        """
        from scripts.run_label_gate_only import _namespaced_paths
        from src.historical_burn_exclusion import describe_historical_burn_contract

        return describe_historical_burn_contract(
            regions.get_experiment(experiment_id),
            output_dir=_namespaced_paths(experiment_id)["gate_output_dir"],
        )

    def _manifest(self, experiment_id: str, gate: dict | None = None) -> dict:
        from scripts.run_label_gate_only import _namespaced_paths, build_gate_manifest

        return build_gate_manifest(
            experiment_id,
            regions.get_experiment(experiment_id),
            _namespaced_paths(experiment_id),
            {"gate_result": gate if gate is not None else {
                "decision": "unknown", "burned_count": 0, "json_path": None}},
            historical_description=self._historical_description(experiment_id),
        )

    def test_legacy_experiments_keep_the_exact_pre_patch_scientific_schema(self):
        for experiment_id in ("mugla_2021", "manavgat_2021", "bejis_2022",
                              "evia_2021", "evia_2021_extended",
                              "montiferru_2021", LEGACY_ID):
            with self.subTest(experiment_id=experiment_id):
                scientific = self._manifest(experiment_id)["scientific"]
                self.assertEqual(set(scientific), PRE_PATCH_SCIENTIFIC_KEYS)

    def test_legacy_experiments_do_not_acquire_the_new_contract_keys(self):
        for experiment_id in ("mugla_2021", "montiferru_2021", LEGACY_ID):
            with self.subTest(experiment_id=experiment_id):
                manifest = self._manifest(experiment_id)
                for key in NEW_SCIENTIFIC_CONTRACT_KEYS:
                    self.assertNotIn(key, manifest["scientific"])
                # Top-level provenance keys are omitted too, not nulled.
                self.assertNotIn("historical_burn_provenance", manifest)
                self.assertNotIn("primary_population_sample_size_gate", manifest)
                # The pre-existing pre-label provenance block is retained.
                self.assertIn("pre_label_provenance", manifest)

    def test_event_relative_acquires_both_new_scientific_contract_keys(self):
        scientific = self._manifest(EVENT_ID)["scientific"]
        self.assertEqual(NEW_SCIENTIFIC_CONTRACT_KEYS - set(scientific), set())
        # Additive only: every pre-patch key survives unchanged alongside them.
        self.assertEqual(PRE_PATCH_SCIENTIFIC_KEYS - set(scientific), set())
        historical = scientific["historical_burn_exclusion"]
        self.assertTrue(historical["applied"])
        self.assertEqual(historical["source_experiment_id"], SOURCE_ID)
        self.assertIn("burned == 1", historical["mask_definition"])
        rule = scientific["primary_population_sample_size_rule"]
        self.assertTrue(rule["applied"])
        self.assertEqual(rule["population"], "burnable_tree_shrub_grass")
        self.assertEqual(rule["min_primary_population_burned"], 300)
        # The generic composition-gate threshold is recorded, not replaced.
        self.assertEqual(rule["distinct_from_composition_gate_min_positives"], 30)

    def test_event_relative_extra_scientific_keys_are_exactly_the_declared_ones(self):
        scientific = self._manifest(EVENT_ID)["scientific"]
        self.assertEqual(
            set(scientific) - PRE_PATCH_SCIENTIFIC_KEYS,
            NEW_SCIENTIFIC_CONTRACT_KEYS | {
                "transfer_framing", "event_anchor_date",
                "event_anchor_basis", "event_window_rule",
            },
        )

    def test_event_relative_emits_the_new_top_level_provenance_blocks(self):
        # Synthetic gate payload mirroring what Step6B actually returns for an
        # experiment with both exclusion axes plus the sample-size rule. The
        # manifest-result paths are None on purpose: this is a pure
        # manifest-CONSTRUCTION unit test, so no artifact is written or read.
        # The real source SHA / physical-burned count still reach the manifest
        # through the resolved historical description, not through this stub.
        manifest = self._manifest(EVENT_ID, gate={
            "decision": "unknown", "burned_count": 0, "json_path": None,
            "historical_burn_excluded_count": 7,
            "pre_label_historical_overlap_count": 2,
            "total_unique_excluded_count": 9,
            "historical_burn_exclusion_manifest": {
                "parquet_path": None,
                "csv_path": None,
                "metadata_path": None,
                "excluded_cell_count": EXPECTED_SOURCE_BURNED,
            },
            "primary_population_sample_size_gate": {
                "population": "burnable_tree_shrub_grass", "burned_count": 12,
                "min_burned_required": 300, "decision": "stop",
                "stop_state": "insufficient_primary_population_burned",
            },
        })
        historical = manifest["historical_burn_provenance"]
        self.assertTrue(historical["applied"])
        self.assertEqual(historical["source_experiment_id"], SOURCE_ID)
        self.assertEqual(historical["historical_burn_excluded_count"], 7)
        self.assertEqual(historical["pre_label_historical_overlap_count"], 2)
        self.assertEqual(historical["total_unique_excluded_count"], 9)
        # Counts/SHA of the SOURCE come from the resolved description.
        self.assertEqual(historical["source_physical_burned_count"],
                         EXPECTED_SOURCE_BURNED)
        self.assertEqual(len(historical["source_step8a_parquet_sha256"]), 64)
        # No artifact path was supplied, so no artifact hash is invented.
        self.assertIsNone(historical["exclusion_manifest_parquet_path"])
        self.assertIsNone(historical["exclusion_manifest_parquet_sha256"])
        self.assertEqual(manifest["primary_population_sample_size_gate"]["decision"], "stop")
        self.assertEqual(
            manifest["primary_population_sample_size_gate"]["stop_state"],
            "insufficient_primary_population_burned")
        # A STOP never authorizes downstream, and neither does anything else.
        self.assertFalse(manifest["downstream_authorized"])
        # The pre-label provenance block stays SEPARATE and is retained.
        self.assertIn("pre_label_provenance", manifest)
        self.assertNotIn("historical_burn_excluded_count", manifest["pre_label_provenance"])

    def test_builder_never_fabricates_historical_provenance_it_was_not_given(self):
        # API contract: build_gate_manifest is a PURE BUILDER. Resolved
        # provenance is supplied by the caller (production resolves it once in
        # run_label_gate_only.main and passes it in); the builder must never
        # reach out and resolve/invent it. Called WITHOUT the description --
        # even for the opted-in experiment -- it emits no historical fields at
        # all rather than a half-populated or self-resolved block.
        from scripts.run_label_gate_only import _namespaced_paths, build_gate_manifest

        manifest = build_gate_manifest(
            EVENT_ID,
            regions.get_experiment(EVENT_ID),
            _namespaced_paths(EVENT_ID),
            {"gate_result": {
                "decision": "unknown", "burned_count": 0, "json_path": None,
                # Even with gate-side historical counts present, absent caller
                # provenance means NO historical block is emitted.
                "historical_burn_excluded_count": 7,
                "total_unique_excluded_count": 9,
            }},
            historical_description=None,
        )
        self.assertNotIn("historical_burn_exclusion", manifest["scientific"])
        self.assertNotIn("historical_burn_provenance", manifest)
        # The registry-declared parts that do NOT need resolved provenance are
        # still emitted, so this is genuinely about missing caller context.
        self.assertIn("primary_population_sample_size_rule", manifest["scientific"])
        self.assertEqual(manifest["scientific"]["transfer_framing"],
                         "same_geography_event_to_event")
        # And supplying the description is what turns the block on.
        with_description = self._manifest(EVENT_ID)
        self.assertIn("historical_burn_exclusion", with_description["scientific"])
        self.assertNotEqual(with_description["analysis_id"], manifest["analysis_id"])

    def test_a_half_declared_rule_is_not_written_as_a_scientific_block(self):
        # Half-declarations must reach the gate, which fails closed on them --
        # never be pre-empted by a half-filled manifest block.
        from scripts.run_label_gate_only import declares_primary_population_rule

        half = dict(regions.get_experiment(EVENT_ID))
        half.pop("min_primary_population_burned")
        self.assertFalse(declares_primary_population_rule(half))
        self.assertTrue(declares_primary_population_rule(
            regions.get_experiment(EVENT_ID)))

    def test_legacy_analysis_id_does_not_depend_on_the_new_code_paths(self):
        # Deterministic and driven purely by the pre-patch payload: two builds
        # of an opted-out experiment agree, and its key set carries nothing new.
        first = self._manifest("mugla_2021")
        second = self._manifest("mugla_2021")
        self.assertEqual(first["analysis_id"], second["analysis_id"])
        self.assertEqual(len(first["analysis_id"]), 64)
        self.assertEqual(set(first["scientific"]), PRE_PATCH_SCIENTIFIC_KEYS)


# =============================================================================
# 16. Ordinary existing experiments unchanged
# =============================================================================
FROZEN_UNCHANGED = {
    "kozan_2023": {
        "variant_status": "canonical", "region_key": "kozan_aoi",
        "role": "negative_control",
        "predictor_start_date": "2023-06-01", "predictor_end_date": "2023-07-31",
        "label_start_date": "2023-08-01", "label_end_date": "2023-10-31",
        "baseline_years": [2019, 2020, 2021, 2022],
    },
    "manavgat_2021": {
        "variant_status": "canonical", "region_key": "manavgat_aoi",
        "role": "anchor_wildfire",
        "predictor_start_date": "2021-06-01", "predictor_end_date": "2021-07-27",
        "label_start_date": "2021-07-28", "label_end_date": "2021-08-31",
        "baseline_years": [2017, 2018, 2019, 2020],
    },
    "bejis_2022": {
        "variant_status": "canonical", "region_key": "bejis_aoi",
        "role": "mediterranean_transfer_wildfire",
        "predictor_start_date": "2022-06-15", "predictor_end_date": "2022-08-14",
        "label_start_date": "2022-08-15", "label_end_date": "2022-09-30",
        "baseline_years": [2018, 2019, 2020, 2021],
    },
    "mugla_2021": {
        "variant_status": "canonical", "region_key": "mugla_aoi",
        "role": "same_country_same_year_transfer_wildfire",
        "predictor_start_date": "2021-06-01", "predictor_end_date": "2021-07-28",
        "label_start_date": "2021-07-29", "label_end_date": "2021-09-15",
        "baseline_years": [2017, 2018, 2019, 2020],
    },
    "evia_2021_extended": {
        "variant_status": "canonical", "region_key": "north_evia_extended",
        "role": "mediterranean_transfer_wildfire",
        "predictor_start_date": "2021-06-05", "predictor_end_date": "2021-08-02",
        "label_start_date": "2021-08-03", "label_end_date": "2021-09-30",
        "baseline_years": [2017, 2018, 2019, 2020],
    },
    "montiferru_2021": {
        "variant_status": "canonical", "region_key": "montiferru_aoi",
        "role": "mediterranean_transfer_wildfire",
        "predictor_start_date": "2021-05-25", "predictor_end_date": "2021-07-23",
        "label_start_date": "2021-07-24", "label_end_date": "2021-08-31",
        "baseline_years": [2017, 2018, 2019, 2020],
    },
    "evia_2021": {
        "variant_status": "legacy_superseded", "region_key": "north_evia",
        "role": "mediterranean_transfer_wildfire",
        "predictor_start_date": "2021-06-05", "predictor_end_date": "2021-08-02",
        "label_start_date": "2021-08-03", "label_end_date": "2021-09-30",
        "baseline_years": [2017, 2018, 2019, 2020],
    },
}


class TestExistingExperimentsUnchanged(unittest.TestCase):
    def test_16_every_other_record_keeps_its_scientific_contract(self):
        for experiment_id, expected in FROZEN_UNCHANGED.items():
            record = regions.get_experiment(experiment_id)
            for key, value in expected.items():
                with self.subTest(experiment_id=experiment_id, key=key):
                    self.assertEqual(record[key], value)

    def test_16_mugla_2021_pre_label_contract_is_untouched(self):
        record = regions.get_experiment(SOURCE_ID)
        self.assertIs(record["exclude_pre_label_burns"], True)
        self.assertEqual(record["pre_label_burn_window"], ["2021-06-01", "2021-07-28"])
        self.assertEqual(record["pre_label_diagnostic_window"],
                         ["2021-06-21", "2021-06-25"])
        self.assertNotIn("superseded_by", record)

    def test_16_evia_supersession_is_untouched(self):
        self.assertEqual(regions.EXPERIMENTS["evia_2021"]["superseded_by"],
                         "evia_2021_extended")

    def test_16_registry_key_set_is_exactly_expected(self):
        self.assertEqual(
            set(regions.EXPERIMENTS),
            set(FROZEN_UNCHANGED) | {LEGACY_ID, EVENT_ID} | set(regions.SCALEUP_EXPERIMENT_IDS),
        )

    def test_16_default_experiment_is_still_kozan(self):
        self.assertEqual(regions.DEFAULT_EXPERIMENT_ID, "kozan_2023")
        self.assertEqual(regions.get_active_experiment()["experiment_id"], "kozan_2023")

    def test_16_output_namespaces_stay_unique(self):
        namespaces = [record["output_namespace"] for record in regions.EXPERIMENTS.values()]
        self.assertEqual(len(namespaces), len(set(namespaces)))

    def test_16_no_experiment_id_literal_leaked_into_generic_modules(self):
        for relative in ("src/step8a_prepare_500m_modeling_dataset.py",
                         "src/step6b_burned_landcover_gate.py",
                         "src/historical_burn_exclusion.py"):
            source = (_PROJECT_ROOT / relative).read_text(encoding="utf-8")
            with self.subTest(module=relative):
                self.assertNotIn(EVENT_ID, source)
                self.assertNotIn(LEGACY_ID, source)


# =============================================================================
# 17. Dry-run writes nothing
# =============================================================================
class TestDryRunWritesNothing(unittest.TestCase):
    def _snapshot(self) -> set[Path]:
        root = _PROJECT_ROOT / "outputs" / "experiments"
        return set(root.rglob("*")) if root.exists() else set()

    def test_17_dry_run_resolves_everything_and_creates_no_file(self):
        import scripts.run_label_gate_only as runner

        before = self._snapshot()
        with patch("core.gee_utils.init_gee",
                   side_effect=AssertionError("dry-run must not initialize Earth Engine")):
            result = runner.main(experiment_id=EVENT_ID, dry_run=True)
        after = self._snapshot()

        self.assertEqual(before, after, "dry-run created or removed a path")
        self.assertFalse(result["ran"])
        self.assertEqual(result["reason"], "dry_run")

    def test_17_dry_run_reports_the_resolved_historical_contract(self):
        import scripts.run_label_gate_only as runner

        result = runner.main(experiment_id=EVENT_ID, dry_run=True)
        historical = result["historical_burn_exclusion"]
        self.assertIsNotNone(historical)
        self.assertEqual(historical["source_experiment_id"], SOURCE_ID)
        self.assertEqual(historical["source_kind"],
                         "canonical_step8a_physical_burned_cells")
        self.assertEqual(historical["source_expected_physical_burned_count"],
                         EXPECTED_SOURCE_BURNED)
        self.assertIn("planned_artifacts", historical)
        for planned in historical["planned_artifacts"].values():
            self.assertFalse(Path(planned).exists(), planned)
            self.assertIn(EVENT_ID, planned)

    def test_17_dry_run_reports_the_primary_population_rule(self):
        import scripts.run_label_gate_only as runner

        result = runner.main(experiment_id=EVENT_ID, dry_run=True)
        rule = result["primary_population_sample_size_rule"]
        self.assertEqual(rule["population"], "burnable_tree_shrub_grass")
        self.assertEqual(rule["min_primary_population_burned"], 300)

    def test_17_dry_run_plans_the_three_historical_artifact_paths(self):
        import scripts.run_label_gate_only as runner

        result = runner.main(experiment_id=EVENT_ID, dry_run=True)
        planned = result["planned_paths"]
        for key, filename in (
            ("historical_excluded_parquet_path", "historical_burn_excluded_cells.parquet"),
            ("historical_excluded_csv_path", "historical_burn_excluded_cells.csv"),
            ("historical_excluded_metadata_path",
             "historical_burn_excluded_cells_metadata.json"),
        ):
            self.assertTrue(planned[key].endswith(filename), key)
        # The historical artifacts are SEPARATE files from the pre-label ones.
        self.assertNotEqual(planned["historical_excluded_parquet_path"],
                            str(Path(planned["gate_output_dir"])
                                / "pre_label_excluded_cells.parquet"))

    def test_17_dry_run_never_touches_the_superseded_namespace(self):
        import scripts.run_label_gate_only as runner

        result = runner.main(experiment_id=EVENT_ID, dry_run=True)
        for name, value in result["planned_paths"].items():
            if value is None:
                continue
            # Real ancestry, not substring matching: 'mugla_2022' is a lexical
            # prefix of 'mugla_2022_event_relative'.
            assert_sibling_of_legacy_not_descendant(self, value, name)
            self.assertNotIn(LEGACY_ID, Path(value).resolve().parts, name)


if __name__ == "__main__":
    unittest.main()

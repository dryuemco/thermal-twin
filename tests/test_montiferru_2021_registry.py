"""
tests/test_montiferru_2021_registry.py

Targeted tests for the frozen `montiferru_2021` registry entry and its
place-based Montiferru / Oristano AOI. Read-only: no Earth Engine call, no
network access, no export, no gate, no model, no raster/parquet read or
written.

Covers:
    1  montiferru_2021 is registered and enabled
    2  the frozen predictor/label dates are exact
    3  the baseline years are exact
    4  region_key resolves to a declared region of build_regions()
    5  output_namespace == experiment_id, and namespaces stay unique
    6  the bbox is correctly ordered and non-degenerate
    7  the four anchor municipality reference points fall inside the bbox
    8  the static (AST) bbox/provenance resolver recognises the module constant
    9  the pre-label burn window equals the predictor window
   10  every pre-existing experiment's metadata and AOI bbox is unchanged
   11  a dry-run performs no GEE initialization, network call or file write
   12  the registry-declared AOI derivation chain (aoi_provenance) is exact and
       internally consistent with MONTIFERRU_AOI_BBOX
   13  build_gate_manifest() carries that chain into scientific.aoi.derivation
       for Montiferru and adds NO such field for any other experiment

Run:
    python -m unittest tests.test_montiferru_2021_registry
"""

from __future__ import annotations

import json
import math
import socket
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import core.pipeline_orchestrator as orch
import core.regions as regions
from core.config import EXPORT_CRS

EXP_ID = "montiferru_2021"
REGION_KEY = "montiferru_aoi"

R_EARTH_KM = 6371.0088

# Place-based anchors only: published municipality (comune) centre coordinates.
# NEVER derived from burned labels, burned prevalence, gate outcome or any
# model metric. Documentation/verification use only.
MONTIFERRU_MUNICIPALITIES = {
    "Bonarcado": (8.650, 40.150),
    "Santu Lussurgiu": (8.650, 40.217),
    "Cuglieri": (8.567, 40.183),
    "Scano di Montiferro": (8.583, 40.233),
}


def _bbox_area_km2(bbox) -> float:
    """Spherical-Earth area of a lon/lat rectangle (no geospatial dependency)."""
    west, south, east, north = bbox
    dlon = math.radians(east - west)
    return R_EARTH_KM ** 2 * dlon * (math.sin(math.radians(north)) - math.sin(math.radians(south)))


# =============================================================================
# Registration (tests 1/2/3/5/9)
# =============================================================================
class TestMontiferruRegistration(unittest.TestCase):
    def setUp(self):
        self.exp = regions.get_experiment(EXP_ID)

    def test_01_registered_and_enabled(self):
        self.assertIn(EXP_ID, regions.EXPERIMENTS)
        self.assertTrue(self.exp["enabled"])
        self.assertIn(EXP_ID, regions.list_experiments(include_disabled=False))
        self.assertEqual(self.exp["experiment_id"], EXP_ID)

    def test_01_descriptive_metadata_is_frozen(self):
        self.assertEqual(self.exp["display_name"], "Montiferru / Oristano, Sardinia 2021")
        self.assertEqual(self.exp["role"], "mediterranean_transfer_wildfire")
        self.assertEqual(self.exp["country"], "Italy")

    def test_02_frozen_dates_are_exact(self):
        self.assertEqual(self.exp["predictor_start_date"], "2021-05-25")
        self.assertEqual(self.exp["predictor_end_date"], "2021-07-23")
        self.assertEqual(self.exp["label_start_date"], "2021-07-24")
        self.assertEqual(self.exp["label_end_date"], "2021-08-31")

    def test_02_label_window_starts_the_day_after_the_predictor_window(self):
        from datetime import date, timedelta

        pred_end = date.fromisoformat(self.exp["predictor_end_date"])
        label_start = date.fromisoformat(self.exp["label_start_date"])
        self.assertEqual(label_start, pred_end + timedelta(days=1))
        # 24 July 2021 Montiferru / Oristano wildfire = first label day.
        self.assertEqual(label_start, date(2021, 7, 24))
        self.assertLess(label_start, date.fromisoformat(self.exp["label_end_date"]))
        self.assertLess(date.fromisoformat(self.exp["predictor_start_date"]), pred_end)

    def test_03_baseline_years_are_exact(self):
        self.assertEqual(self.exp["baseline_years"], [2017, 2018, 2019, 2020])
        self.assertTrue(all(y < 2021 for y in self.exp["baseline_years"]),
                        "baseline years must precede the event year")

    def test_05_output_namespace_equals_experiment_id(self):
        self.assertEqual(self.exp["output_namespace"], EXP_ID)

    def test_05_output_namespaces_remain_unique(self):
        namespaces = [e["output_namespace"] for e in regions.EXPERIMENTS.values()]
        self.assertEqual(len(namespaces), len(set(namespaces)), "duplicate output_namespace")

    def test_05_output_root_resolves_under_its_own_namespace_without_creating_it(self):
        root = regions.get_experiment_output_root(EXP_ID)
        self.assertEqual(root, _PROJECT_ROOT / "outputs" / "experiments" / EXP_ID)
        existed = root.exists()
        path = regions.get_step_output_dir(EXP_ID, "step0")
        self.assertIn(EXP_ID, path.parts)
        self.assertEqual(root.exists(), existed, "path resolution must not create directories")

    def test_09_pre_label_window_equals_the_predictor_window(self):
        self.assertTrue(self.exp["exclude_pre_label_burns"])
        self.assertEqual(
            self.exp["pre_label_burn_window"],
            [self.exp["predictor_start_date"], self.exp["predictor_end_date"]],
        )
        self.assertEqual(self.exp["pre_label_burn_window"], ["2021-05-25", "2021-07-23"])

    def test_09_no_diagnostic_sub_window_is_declared(self):
        self.assertNotIn("pre_label_diagnostic_window", self.exp)


# =============================================================================
# AOI geometry (tests 4/6/7/8)
# =============================================================================
class TestMontiferruAOI(unittest.TestCase):
    def setUp(self):
        self.bbox = regions.MONTIFERRU_AOI_BBOX

    def test_06_bbox_is_frozen_and_well_ordered(self):
        self.assertEqual(self.bbox, (8.45, 40.05, 8.75, 40.27))
        west, south, east, north = self.bbox
        # ee.Geometry.BBox order = (lon_min, lat_min, lon_max, lat_max)
        self.assertLess(west, east)
        self.assertLess(south, north)
        self.assertEqual(EXPORT_CRS, "EPSG:4326")

    def test_06_bbox_is_non_degenerate_and_does_not_wrap(self):
        west, south, east, north = self.bbox
        self.assertGreater(_bbox_area_km2(self.bbox), 0.0)
        self.assertTrue(-180.0 <= west < east <= 180.0)
        self.assertTrue(-90.0 <= south < north <= 90.0)
        self.assertLess(east - west, 180.0, "bbox must not wrap the antimeridian")

    def test_07_four_anchor_municipalities_are_inside_the_bbox(self):
        west, south, east, north = self.bbox
        self.assertEqual(len(MONTIFERRU_MUNICIPALITIES), 4)
        for place, (lon, lat) in MONTIFERRU_MUNICIPALITIES.items():
            self.assertTrue(west <= lon <= east, f"{place} outside bbox in longitude")
            self.assertTrue(south <= lat <= north, f"{place} outside bbox in latitude")

    def test_07_bbox_leaves_margin_around_every_anchor(self):
        # A strictly-interior anchor set is what "place coverage, not a fire
        # perimeter" means: no edge is pinned to a municipality centre.
        west, south, east, north = self.bbox
        lons = [lon for lon, _ in MONTIFERRU_MUNICIPALITIES.values()]
        lats = [lat for _, lat in MONTIFERRU_MUNICIPALITIES.values()]
        self.assertLess(west, min(lons))
        self.assertGreater(east, max(lons))
        self.assertLess(south, min(lats))
        self.assertGreater(north, max(lats))

    def test_04_region_key_is_declared_by_build_regions(self):
        # build_regions() is never called here (it would need ee.Initialize);
        # the source is read statically instead.
        source = (_PROJECT_ROOT / "core" / "regions.py").read_text(encoding="utf-8")
        self.assertEqual(regions.get_experiment(EXP_ID)["region_key"], REGION_KEY)
        self.assertIn(f'"{REGION_KEY}": montiferru_aoi', source)
        self.assertIn('"montiferru_aoi_candidate_bbox": montiferru_aoi_candidate_bbox', source)
        self.assertIn("ee.Geometry.BBox(*MONTIFERRU_AOI_BBOX)", source)

    def test_08_static_bbox_resolver_recognises_the_module_constant(self):
        from scripts.run_label_gate_only import _static_region_bbox

        self.assertEqual(_static_region_bbox(REGION_KEY), self.bbox)
        self.assertEqual(_static_region_bbox("montiferru_aoi_candidate_bbox"), self.bbox)

    def test_08_static_aoi_provenance_is_resolvable_and_deterministic(self):
        from scripts.run_label_gate_only import _static_region_aoi_provenance

        prov = _static_region_aoi_provenance(REGION_KEY)
        self.assertIsNotNone(prov, "gate manifest could not resolve Montiferru AOI provenance")
        self.assertEqual(list(prov["bounds"]), list(self.bbox))
        self.assertEqual(prov, _static_region_aoi_provenance(REGION_KEY))
        # Distinct AOI => distinct geometry hash from every other experiment.
        for other in ("mugla_aoi", "north_evia", "north_evia_extended", "bejis_aoi"):
            self.assertNotEqual(prov["geometry_hash"],
                                _static_region_aoi_provenance(other)["geometry_hash"], other)


# =============================================================================
# AOI derivation provenance (test 12)
# =============================================================================
EXPECTED_MUNICIPALITIES = [
    "Bonarcado",
    "Cuglieri",
    "Santu Lussurgiu",
    "Scano di Montiferro",
]

EXPECTED_RAW_UNION_BOUNDS = [
    8.454041028057148,
    40.053824525866645,
    8.745509975002108,
    40.264205506896815,
]


class TestMontiferruAOIDerivationProvenance(unittest.TestCase):
    """core/regions.py is the single source of truth for HOW the bbox was
    derived. Fail-closed: every claim below is checked against the frozen
    MONTIFERRU_AOI_BBOX, not against a restatement of it."""

    def setUp(self):
        self.prov = regions.get_experiment(EXP_ID)["aoi_provenance"]
        self.bbox = regions.MONTIFERRU_AOI_BBOX

    def test_12_provenance_is_declared_and_json_serializable(self):
        self.assertIsInstance(self.prov, dict)
        # Must survive the exact round-trip the gate manifest performs.
        self.assertEqual(json.loads(json.dumps(self.prov, ensure_ascii=False)), self.prov)

    def test_12_source_authority_and_dataset_are_exact(self):
        self.assertEqual(self.prov["source_authority"], "ISTAT")
        self.assertEqual(self.prov["source_dataset"],
                         "2021 non-generalized administrative boundaries")
        self.assertEqual(self.prov["source_archive"], "Limiti2021.zip")
        self.assertEqual(self.prov["source_reference_date"], "2021-12-31")
        self.assertEqual(self.prov["administrative_level"], "municipality/comune")

    def test_12_exactly_four_municipalities_are_listed(self):
        self.assertEqual(self.prov["municipalities"], EXPECTED_MUNICIPALITIES)
        self.assertEqual(len(self.prov["municipalities"]), 4)
        self.assertEqual(sorted(self.prov["municipalities"]), EXPECTED_MUNICIPALITIES)
        # Same four comuni as the independently declared anchor set.
        self.assertEqual(set(self.prov["municipalities"]), set(MONTIFERRU_MUNICIPALITIES))

    def test_12_final_bbox_is_exactly_the_frozen_module_constant(self):
        self.assertEqual(self.prov["final_bbox_epsg4326"], list(self.bbox))
        self.assertEqual(tuple(self.prov["final_bbox_epsg4326"]), self.bbox)

    def test_12_raw_union_bounds_are_frozen(self):
        self.assertEqual(self.prov["raw_union_total_bounds_epsg4326"],
                         EXPECTED_RAW_UNION_BOUNDS)

    def test_12_raw_union_bounds_lie_entirely_inside_the_final_bbox(self):
        raw_w, raw_s, raw_e, raw_n = self.prov["raw_union_total_bounds_epsg4326"]
        west, south, east, north = self.bbox
        self.assertGreaterEqual(raw_w, west, "raw west edge falls outside the final bbox")
        self.assertGreaterEqual(raw_s, south, "raw south edge falls outside the final bbox")
        self.assertLessEqual(raw_e, east, "raw east edge falls outside the final bbox")
        self.assertLessEqual(raw_n, north, "raw north edge falls outside the final bbox")
        self.assertLess(raw_w, raw_e)
        self.assertLess(raw_s, raw_n)

    def test_12_rounding_contract_is_outward_at_two_decimals(self):
        self.assertEqual(self.prov["rounding"], {"mode": "outward", "decimal_places": 2})

    def test_12_declared_rounding_reproduces_the_final_bbox_exactly(self):
        mode = self.prov["rounding"]["mode"]
        dp = self.prov["rounding"]["decimal_places"]
        self.assertEqual(mode, "outward")
        scale = 10 ** dp
        raw_w, raw_s, raw_e, raw_n = self.prov["raw_union_total_bounds_epsg4326"]
        recomputed = [
            math.floor(raw_w * scale) / scale,
            math.floor(raw_s * scale) / scale,
            math.ceil(raw_e * scale) / scale,
            math.ceil(raw_n * scale) / scale,
        ]
        self.assertEqual(recomputed, list(self.bbox),
                         "outward-rounding the raw union bounds must reproduce "
                         "MONTIFERRU_AOI_BBOX exactly")
        # Outward, never inward: each edge is expanded (or unchanged), and by
        # strictly less than one rounding step.
        for value, raw in zip(recomputed, [raw_w, raw_s, raw_e, raw_n]):
            self.assertLess(abs(value - raw), 1.0 / scale)

    def test_12_selection_constraint_excludes_outcome_driven_tuning(self):
        constraint = self.prov["selection_constraint"]
        self.assertEqual(
            constraint,
            "Defined only from official municipal boundaries; not tuned using "
            "the fire footprint, MCD64A1 labels, prevalence, gate outcome or "
            "model metrics.",
        )

    def test_12_derivation_method_describes_the_four_step_chain(self):
        method = self.prov["derivation_method"]
        self.assertEqual(
            method,
            "Select the four official municipality polygons, transform to "
            "EPSG:4326, compute their union total bounds, then outward-round "
            "each edge to two decimal degrees.",
        )

    def test_12_provenance_key_set_is_frozen(self):
        self.assertEqual(set(self.prov), {
            "source_authority", "source_dataset", "source_archive",
            "source_reference_date", "administrative_level", "municipalities",
            "derivation_method", "raw_union_total_bounds_epsg4326", "rounding",
            "final_bbox_epsg4326", "selection_constraint",
        })

    def test_12_no_other_experiment_declares_aoi_provenance(self):
        for exp_id, exp in regions.EXPERIMENTS.items():
            # montiferru_2021_fullwindow (scale-up run) is a copy of this record with the
            # MODIS month filter off, so it carries the same provenance.
            if exp_id in (EXP_ID, "montiferru_2021_fullwindow"):
                continue
            self.assertNotIn("aoi_provenance", exp, exp_id)


# =============================================================================
# Gate manifest carries the derivation chain (test 13)
# =============================================================================
class TestGateManifestCarriesDerivation(unittest.TestCase):
    """Read-only: build_gate_manifest() is called with a synthetic gate_result
    and never writes anything (the runner, not the builder, does the I/O)."""

    def _manifest(self, exp_id: str, exp: dict | None = None) -> dict:
        from scripts.run_label_gate_only import build_gate_manifest, _namespaced_paths

        exp = regions.get_experiment(exp_id) if exp is None else exp
        return build_gate_manifest(
            exp_id, exp, _namespaced_paths(exp_id),
            {"gate_result": {"decision": "unknown", "burned_count": 0, "json_path": None}},
        )

    def test_13_montiferru_manifest_exposes_the_derivation_chain(self):
        aoi = self._manifest(EXP_ID)["scientific"]["aoi"]
        derivation = aoi["derivation"]
        self.assertEqual(derivation, regions.get_experiment(EXP_ID)["aoi_provenance"])
        self.assertEqual(derivation["source_authority"], "ISTAT")
        self.assertEqual(derivation["municipalities"], EXPECTED_MUNICIPALITIES)
        self.assertEqual(derivation["raw_union_total_bounds_epsg4326"],
                         EXPECTED_RAW_UNION_BOUNDS)
        self.assertEqual(derivation["rounding"], {"mode": "outward", "decimal_places": 2})
        self.assertEqual(derivation["final_bbox_epsg4326"],
                         list(regions.MONTIFERRU_AOI_BBOX))
        self.assertIn("not tuned", derivation["selection_constraint"])

    def test_13_derivation_agrees_with_the_static_aoi_bounds(self):
        aoi = self._manifest(EXP_ID)["scientific"]["aoi"]
        self.assertEqual(aoi["derivation"]["final_bbox_epsg4326"], list(aoi["bounds"]))
        self.assertEqual(aoi["crs"], "EPSG:4326")

    def test_13_static_aoi_source_field_is_unchanged(self):
        # scientific.aoi.source must keep describing the AST resolution; the
        # derivation chain is additive, never a replacement.
        aoi = self._manifest(EXP_ID)["scientific"]["aoi"]
        self.assertEqual(
            aoi["source"],
            "static AST read of core/regions.py build_regions() (no Earth Engine call)",
        )

    def test_13_manifest_is_json_serializable_and_does_not_alias_the_registry(self):
        manifest = self._manifest(EXP_ID)
        json.dumps(manifest, ensure_ascii=False)  # must not raise
        manifest["scientific"]["aoi"]["derivation"]["municipalities"].append("TAMPER")
        self.assertEqual(regions.EXPERIMENTS[EXP_ID]["aoi_provenance"]["municipalities"],
                         EXPECTED_MUNICIPALITIES)

    def test_13_derivation_is_part_of_the_analysis_id(self):
        baseline = self._manifest(EXP_ID)["analysis_id"]
        self.assertEqual(baseline, self._manifest(EXP_ID)["analysis_id"], "not deterministic")

        tampered = regions.get_experiment(EXP_ID)
        tampered["aoi_provenance"] = json.loads(json.dumps(tampered["aoi_provenance"]))
        tampered["aoi_provenance"]["source_authority"] = "SOMETHING_ELSE"
        self.assertNotEqual(self._manifest(EXP_ID, tampered)["analysis_id"], baseline)

        stripped = regions.get_experiment(EXP_ID)
        stripped.pop("aoi_provenance")
        self.assertNotEqual(self._manifest(EXP_ID, stripped)["analysis_id"], baseline)

    def test_13_experiments_without_provenance_gain_no_derivation_field(self):
        for exp_id in ("mugla_2021", "manavgat_2021", "bejis_2022",
                       "evia_2021", "evia_2021_extended"):
            aoi = self._manifest(exp_id)["scientific"]["aoi"]
            self.assertNotIn("derivation", aoi, exp_id)
            self.assertEqual(set(aoi), {
                "region_key", "kind", "geometry_type", "crs", "order", "bounds",
                "geodesic", "geometry_hash", "source",
            }, exp_id)

    def test_13_montiferru_aoi_key_set_is_the_baseline_plus_derivation_only(self):
        montiferru_aoi = self._manifest(EXP_ID)["scientific"]["aoi"]
        other_aoi = self._manifest("mugla_2021")["scientific"]["aoi"]
        self.assertEqual(set(montiferru_aoi) - set(other_aoi), {"derivation"})
        self.assertEqual(set(other_aoi) - set(montiferru_aoi), set())

    def test_13_scientific_block_schema_is_otherwise_unchanged(self):
        expected_keys = {
            "experiment_id", "region_key", "aoi", "predictor_window",
            "label_window", "baseline_years", "primary_population",
            "modeling_grid_m", "exclude_pre_label_burns",
            "pre_label_burn_window", "pre_label_burn_exclusion_rule",
        }
        for exp_id in (EXP_ID, "mugla_2021", "evia_2021"):
            self.assertEqual(set(self._manifest(exp_id)["scientific"]), expected_keys, exp_id)

    def test_13_scientific_values_are_unchanged_for_montiferru(self):
        scientific = self._manifest(EXP_ID)["scientific"]
        exp = regions.get_experiment(EXP_ID)
        self.assertEqual(scientific["predictor_window"], ["2021-05-25", "2021-07-23"])
        self.assertEqual(scientific["label_window"], ["2021-07-24", "2021-08-31"])
        self.assertEqual(scientific["baseline_years"], [2017, 2018, 2019, 2020])
        self.assertEqual(scientific["primary_population"], "burnable_tree_shrub_grass")
        self.assertEqual(scientific["modeling_grid_m"], 500)
        self.assertTrue(scientific["exclude_pre_label_burns"])
        self.assertEqual(scientific["pre_label_burn_window"], exp["pre_label_burn_window"])
        self.assertEqual(
            scientific["pre_label_burn_exclusion_rule"],
            "valid nonzero BurnDate calendar date < label_start (2021-07-24)",
        )
        self.assertEqual(scientific["aoi"]["bounds"], list(regions.MONTIFERRU_AOI_BBOX))
        self.assertFalse(self._manifest(EXP_ID)["downstream_authorized"])

    def test_13_declared_empty_provenance_fails_closed(self):
        from scripts.run_label_gate_only import _registry_aoi_derivation

        with self.assertRaisesRegex(
            ValueError,
            "must be a non-empty dict",
        ):
            _registry_aoi_derivation({
                "experiment_id": "synthetic_empty",
                "aoi_provenance": {},
            })

    def test_13_non_dict_provenance_fails_closed(self):
        from scripts.run_label_gate_only import _registry_aoi_derivation

        with self.assertRaisesRegex(
            ValueError,
            "must be a non-empty dict",
        ):
            _registry_aoi_derivation({
                "experiment_id": "synthetic_list",
                "aoi_provenance": ["not", "a", "dict"],
            })

    def test_13_non_serializable_provenance_fails_closed(self):
        from scripts.run_label_gate_only import _registry_aoi_derivation

        with self.assertRaisesRegex(
            ValueError,
            "is not JSON-serializable",
        ):
            _registry_aoi_derivation({
                "experiment_id": "synthetic_non_serializable",
                "aoi_provenance": {
                    "invalid_value": {1, 2},
                },
            })


# =============================================================================
# Pre-existing experiments untouched (test 10)
# =============================================================================
FROZEN_EXPERIMENTS = {
    "manavgat_2021": {
        "region_key": "manavgat_aoi", "role": "anchor_wildfire", "country": "Turkey",
        "predictor_start_date": "2021-06-01", "predictor_end_date": "2021-07-27",
        "label_start_date": "2021-07-28", "label_end_date": "2021-08-31",
        "baseline_years": [2017, 2018, 2019, 2020], "output_namespace": "manavgat_2021",
    },
    "bejis_2022": {
        "region_key": "bejis_aoi", "role": "mediterranean_transfer_wildfire", "country": "Spain",
        "predictor_start_date": "2022-06-15", "predictor_end_date": "2022-08-14",
        "label_start_date": "2022-08-15", "label_end_date": "2022-09-30",
        "baseline_years": [2018, 2019, 2020, 2021], "output_namespace": "bejis_2022",
    },
    "mugla_2021": {
        "region_key": "mugla_aoi", "role": "same_country_same_year_transfer_wildfire",
        "country": "Turkey",
        "predictor_start_date": "2021-06-01", "predictor_end_date": "2021-07-28",
        "label_start_date": "2021-07-29", "label_end_date": "2021-09-15",
        "baseline_years": [2017, 2018, 2019, 2020], "output_namespace": "mugla_2021",
    },
    "evia_2021": {
        "region_key": "north_evia", "role": "mediterranean_transfer_wildfire", "country": "Greece",
        "predictor_start_date": "2021-06-05", "predictor_end_date": "2021-08-02",
        "label_start_date": "2021-08-03", "label_end_date": "2021-09-30",
        "baseline_years": [2017, 2018, 2019, 2020], "output_namespace": "evia_2021",
    },
    "evia_2021_extended": {
        "region_key": "north_evia_extended", "role": "mediterranean_transfer_wildfire",
        "country": "Greece",
        "predictor_start_date": "2021-06-05", "predictor_end_date": "2021-08-02",
        "label_start_date": "2021-08-03", "label_end_date": "2021-09-30",
        "baseline_years": [2017, 2018, 2019, 2020], "output_namespace": "evia_2021_extended",
    },
    "kozan_2023": {
        "region_key": "kozan_aoi", "role": "negative_control", "country": "Turkey",
        "predictor_start_date": "2023-06-01", "predictor_end_date": "2023-07-31",
        "label_start_date": "2023-08-01", "label_end_date": "2023-10-31",
        "baseline_years": [2019, 2020, 2021, 2022], "output_namespace": "kozan_2023",
    },
}

FROZEN_BBOXES = {
    "MUGLA_AOI_BBOX": (27.10, 36.60, 28.90, 37.45),
    "NORTH_EVIA_AOI_BBOX": (23.12, 38.68, 23.52, 39.08),
    "NORTH_EVIA_EXTENDED_AOI_BBOX": (23.05, 38.55, 23.85, 39.15),
}


class TestExistingExperimentsUnchanged(unittest.TestCase):
    def test_10_existing_experiment_metadata_is_unchanged(self):
        for exp_id, expected in FROZEN_EXPERIMENTS.items():
            exp = regions.get_experiment(exp_id)
            self.assertTrue(exp["enabled"], exp_id)
            for key, value in expected.items():
                self.assertEqual(exp[key], value, f"{exp_id}.{key}")

    def test_10_existing_module_level_bboxes_are_unchanged(self):
        for name, value in FROZEN_BBOXES.items():
            self.assertEqual(getattr(regions, name), value, name)

    def test_10_existing_inline_aoi_bboxes_are_unchanged(self):
        from scripts.run_label_gate_only import _static_region_bbox

        self.assertEqual(_static_region_bbox("manavgat_aoi"), (31.05, 36.72, 31.85, 37.35))
        self.assertEqual(_static_region_bbox("bejis_aoi"), (-1.05, 39.68, -0.35, 40.15))

    def test_10_existing_pre_label_contracts_are_unchanged(self):
        self.assertEqual(regions.get_experiment("mugla_2021")["pre_label_burn_window"],
                         ["2021-06-01", "2021-07-28"])
        self.assertEqual(regions.get_experiment("mugla_2021")["pre_label_diagnostic_window"],
                         ["2021-06-21", "2021-06-25"])
        for exp_id in ("evia_2021", "evia_2021_extended"):
            self.assertEqual(regions.get_experiment(exp_id)["pre_label_burn_window"],
                             ["2021-06-05", "2021-08-02"])
        for exp_id in ("kozan_2023", "manavgat_2021", "bejis_2022"):
            self.assertNotIn("exclude_pre_label_burns", regions.get_experiment(exp_id), exp_id)

    def test_10_default_experiment_still_kozan(self):
        self.assertEqual(regions.DEFAULT_EXPERIMENT_ID, "kozan_2023")
        self.assertEqual(regions.get_active_experiment()["experiment_id"], "kozan_2023")

    def test_10_registry_keys_are_exactly_the_expected_explicit_set(self):
        # Explicit, exhaustive registry key set -- never a subset/permissive
        # check. Every key added after montiferru_2021 must be listed here
        # deliberately. Both extra keys reuse mugla_2021's AOI unchanged:
        #   mugla_2022                 provisional calendar-shift attempt,
        #                              now legacy_superseded but PRESERVED
        #                              (tests/test_mugla_2022_registry.py)
        #   mugla_2022_event_relative  its canonical event-relative successor
        #                              (tests/test_mugla_2022_event_relative.py)
        self.assertEqual(
            set(regions.EXPERIMENTS),
            set(FROZEN_EXPERIMENTS) | {EXP_ID, "mugla_2022", "mugla_2022_event_relative"}
            | set(regions.SCALEUP_EXPERIMENT_IDS),
        )


# =============================================================================
# Dry-run executes nothing (test 11)
# =============================================================================
class TestDryRunNoExecution(unittest.TestCase):
    def _snapshot(self) -> set[Path]:
        root = _PROJECT_ROOT / "outputs" / "experiments"
        return set(root.rglob("*")) if root.exists() else set()

    def test_11_dry_run_runs_no_stage_and_writes_no_file(self):
        before = self._snapshot()
        with patch("core.gee_utils.init_gee",
                   side_effect=AssertionError("dry-run must not initialize Earth Engine")), \
             patch.object(socket, "socket",
                          side_effect=AssertionError("dry-run must not open a network socket")), \
             patch.object(socket, "create_connection",
                          side_effect=AssertionError("dry-run must not open a network connection")):
            result = orch.run_experiment_plan(
                experiment_id=EXP_ID, from_stage="gate", to_stage="step8",
                predictor_mode="export", export_labels=False,
                dry_run=True, force=False,
            )
        after = self._snapshot()

        self.assertTrue(result["dry_run"])
        self.assertEqual(result["experiment_id"], EXP_ID)
        for stage, stage_result in result["stage_results"].items():
            self.assertFalse(stage_result.get("ran"), f"stage '{stage}' reported ran=True")

        new_files = {p for p in after - before if p.is_file()}
        self.assertEqual(new_files, set(), f"dry-run wrote files: {new_files}")

    def test_11_plan_description_is_namespaced_and_side_effect_free(self):
        before = self._snapshot()
        plan = orch.describe_experiment_plan(EXP_ID, "gate", "step8", "export", False)
        self.assertEqual(plan["experiment_id"], EXP_ID)
        self.assertFalse(plan["is_kozan"])
        self.assertIn(EXP_ID, Path(plan["output_root"]).parts)
        for other in FROZEN_EXPERIMENTS:
            self.assertNotIn(other, Path(plan["output_root"]).parts)
        self.assertEqual(self._snapshot(), before, "describe_experiment_plan wrote to outputs/")


if __name__ == "__main__":
    unittest.main()

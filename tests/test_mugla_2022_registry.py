"""
tests/test_mugla_2022_registry.py

Targeted tests for the `mugla_2022` registry entry: the PROVISIONAL
calendar-shift counterpart of `mugla_2021` (space frozen, time shifted by
exactly one calendar year).

SUPERSESSION NOTE
-----------------
`mugla_2022` is now `legacy_superseded`, replaced by
`mugla_2022_event_relative` after the supervisor clarified that the protocol
is EVENT-RELATIVE (windows anchored on the 2022 ignition date, not on 2021's
calendar dates). Its record, its scientific contract and its frozen outputs
under outputs/experiments/mugla_2022/ are all PRESERVED and still asserted
here verbatim -- only the variant status and the cohort-exclusion REASON
changed. See tests/test_mugla_2022_event_relative.py for the canonical
successor's contract.

Read-only: no Earth Engine call, no network access, no export, no gate, no
model, no raster/parquet is read or written.

Covers:
    1  mugla_2022 is registered, enabled and superseded by the event-relative
       experiment
    2  the output namespace is exactly mugla_2022 and stays isolated
    3  region_key is byte-identical to mugla_2021's (AOI reuse, not a copy)
    4  the resolved AOI/bbox/geometry contract is identical to mugla_2021's
    5  the predictor/label windows are the exact one-year shift
    6  the baseline years are exactly [2018, 2019, 2020, 2021]
    7  exclude_pre_label_burns is True and the pre-label burn window equals
       the 2022 predictor window
    8  pre_label_diagnostic_window is ABSENT (2021-only Bördübet/Marmaris
       diagnostic; never copied forward)
    9  the role is exactly temporal_transfer_wildfire; it enters no existing
       role-filtered cohort and is excluded from generic spatial burned-
       pattern discovery even once its Step8A dataset exists (now excluded
       one step earlier, by supersession)
   10  mugla_2021's scientific metadata is not mutated by the addition, and
       no other canonical registry record is silently modified
   11  no new hard-coded mugla_2022 date branch was added to Step8A

Run:
    python -m unittest tests.test_mugla_2022_registry
"""

from __future__ import annotations

import sys
import unittest
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import patch

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

import core.regions as regions

OLD_ID = "mugla_2021"
NEW_ID = "mugla_2022"
#: Canonical successor of the provisional calendar-shift record.
SUCCESSOR_ID = "mugla_2022_event_relative"
REGION_KEY = "mugla_aoi"
ROLE = "temporal_transfer_wildfire"

# Frozen AOI contract, shared by BOTH Muğla experiments (single source:
# core.regions.MUGLA_AOI_BBOX).
MUGLA_BBOX = (27.10, 36.60, 28.90, 37.45)


# =============================================================================
# Registration (1/2)
# =============================================================================
class TestMugla2022Registration(unittest.TestCase):
    def setUp(self):
        self.old = regions.get_experiment(OLD_ID)
        self.new = regions.get_experiment(NEW_ID)

    def test_01_registered_and_enabled(self):
        self.assertIn(NEW_ID, regions.EXPERIMENTS)
        self.assertTrue(self.new["enabled"])
        self.assertIn(NEW_ID, regions.list_experiments(include_disabled=False))
        self.assertEqual(self.new["experiment_id"], NEW_ID)

    def test_01_is_superseded_by_the_event_relative_experiment(self):
        # The calendar-shift formulation was superseded, not deleted: the
        # record stays registered and ENABLED (variant_status and enabled are
        # independent axes), and it points at its canonical successor.
        self.assertEqual(self.new["variant_status"],
                         regions.VARIANT_STATUS_LEGACY_SUPERSEDED)
        self.assertEqual(self.new["superseded_by"], SUCCESSOR_ID)
        self.assertEqual(regions.get_variant_status(NEW_ID),
                         regions.VARIANT_STATUS_LEGACY_SUPERSEDED)
        self.assertEqual(regions.get_superseded_by(NEW_ID), SUCCESSOR_ID)
        # The successor must itself be registered and canonical.
        self.assertIn(SUCCESSOR_ID, regions.EXPERIMENTS)
        self.assertEqual(regions.get_variant_status(SUCCESSOR_ID),
                         regions.VARIANT_STATUS_CANONICAL)

    def test_01_superseded_record_is_refused_by_canonical_selection(self):
        # Never silently dropped: an explicit request fails closed and names
        # the successor.
        with self.assertRaises(regions.VariantStatusError) as raised:
            regions.assert_not_superseded_experiments(
                [NEW_ID], "mugla_2022 registry test")
        self.assertIn(SUCCESSOR_ID, str(raised.exception))
        self.assertNotIn(NEW_ID, regions.list_canonical_enabled_experiments())
        self.assertIn(SUCCESSOR_ID, regions.list_canonical_enabled_experiments())

    def test_01_superseded_record_and_its_outputs_are_preserved(self):
        # Supersession must never delete or migrate the historical attempt.
        self.assertIn(NEW_ID, regions.EXPERIMENTS)
        self.assertTrue(self.new["enabled"])
        self.assertEqual(self.new["output_namespace"], NEW_ID)
        self.assertEqual(regions.get_experiment_output_root(NEW_ID),
                         _PROJECT_ROOT / "outputs" / "experiments" / NEW_ID)
        # The successor writes somewhere else entirely.
        self.assertNotEqual(regions.get_experiment_output_root(SUCCESSOR_ID),
                            regions.get_experiment_output_root(NEW_ID))

    def test_01_notes_record_the_supervisor_clarification(self):
        notes = self.new["notes"].lower()
        self.assertIn("supersed", notes)
        self.assertIn("calendar-shift", notes)
        self.assertIn("event-relative", notes)
        self.assertIn("supervisor", notes)

    def test_01_descriptive_metadata_is_frozen(self):
        self.assertEqual(self.new["display_name"], "Muğla 2022")
        self.assertEqual(self.new["country"], "Turkey")
        self.assertEqual(self.new["country"], self.old["country"])

    def test_02_output_namespace_is_exactly_mugla_2022(self):
        self.assertEqual(self.new["output_namespace"], NEW_ID)
        namespaces = [e["output_namespace"] for e in regions.EXPERIMENTS.values()]
        self.assertEqual(len(namespaces), len(set(namespaces)), "duplicate output_namespace")

    def test_02_output_root_resolves_under_its_own_namespace(self):
        root = regions.get_experiment_output_root(NEW_ID)
        self.assertEqual(root, _PROJECT_ROOT / "outputs" / "experiments" / NEW_ID)

    def test_02_no_step_path_leaks_into_the_mugla_2021_namespace(self):
        old_root = regions.get_experiment_output_root(OLD_ID)
        for step in ("step0", "step5", "step6a", "step6b", "step7", "step8a", "step8"):
            path = regions.get_step_output_dir(NEW_ID, step)
            self.assertIn(NEW_ID, path.parts)
            self.assertNotIn(old_root, path.parents)
            self.assertNotIn(f"/experiments/{OLD_ID}/", f"{path}/")

    def test_02_path_resolution_creates_nothing(self):
        root = regions.get_experiment_output_root(NEW_ID)
        existed = root.exists()
        regions.get_step_output_dir(NEW_ID, "step0")
        self.assertEqual(root.exists(), existed, "path resolution must not create directories")

    def test_02_step0_registry_validator_passes(self):
        from scripts.check_experiment_registry import main as check_registry

        result = check_registry(experiment_id=NEW_ID)
        self.assertTrue(result["valid"])
        self.assertEqual(result["experiment_id"], NEW_ID)
        self.assertEqual(result["region_key"], REGION_KEY)
        self.assertTrue(result["output_root"].endswith(f"experiments/{NEW_ID}"))


# =============================================================================
# Space is frozen: identical AOI contract (3/4)
# =============================================================================
class TestFrozenAOIContract(unittest.TestCase):
    def setUp(self):
        self.old = regions.get_experiment(OLD_ID)
        self.new = regions.get_experiment(NEW_ID)

    def test_03_region_key_is_byte_identical_to_mugla_2021(self):
        self.assertEqual(self.new["region_key"], REGION_KEY)
        self.assertEqual(self.new["region_key"], self.old["region_key"])

    def test_04_module_bbox_constant_is_unchanged_and_shared(self):
        self.assertEqual(regions.MUGLA_AOI_BBOX, MUGLA_BBOX)

    def test_04_no_second_mugla_geometry_was_introduced(self):
        # build_regions() is never called here (it would need ee.Initialize);
        # the source is read statically instead. The AOI must be REUSED, so
        # exactly ONE construction site may exist and it must consume the
        # module constant -- never a fresh literal bbox for 2022.
        source = (_PROJECT_ROOT / "core" / "regions.py").read_text(encoding="utf-8")
        self.assertEqual(source.count("ee.Geometry.BBox(*MUGLA_AOI_BBOX)"), 1)
        definitions = [line for line in source.splitlines()
                       if line.startswith("MUGLA_AOI_BBOX")]
        self.assertEqual(definitions,
                         ["MUGLA_AOI_BBOX = (27.10, 36.60, 28.90, 37.45)"])
        self.assertIn('"mugla_aoi": mugla_aoi', source)
        self.assertNotIn("MUGLA_2022_AOI_BBOX", source)

    def test_04_static_bbox_resolver_returns_the_shared_bbox(self):
        from scripts.run_label_gate_only import _static_region_bbox

        self.assertEqual(_static_region_bbox(REGION_KEY), MUGLA_BBOX)
        self.assertEqual(_static_region_bbox("mugla_aoi_candidate_bbox"), MUGLA_BBOX)

    def test_04_static_aoi_provenance_hash_is_identical_for_both_years(self):
        from scripts.run_label_gate_only import _static_region_aoi_provenance

        old_prov = _static_region_aoi_provenance(self.old["region_key"])
        new_prov = _static_region_aoi_provenance(self.new["region_key"])
        self.assertIsNotNone(new_prov)
        self.assertEqual(new_prov, old_prov)
        self.assertEqual(list(new_prov["bounds"]), list(MUGLA_BBOX))
        self.assertEqual(new_prov["geometry_hash"], old_prov["geometry_hash"])

    def test_04_both_experiments_resolve_to_the_same_geometry_object(self):
        sentinel = object()
        fake_regions = {REGION_KEY: sentinel}
        with patch.object(regions, "build_regions", return_value=fake_regions):
            self.assertIs(regions.get_region_for_experiment(NEW_ID), sentinel)
            self.assertIs(regions.get_region_for_experiment(OLD_ID),
                          regions.get_region_for_experiment(NEW_ID))

    def test_04_mugla_2022_declares_no_private_aoi_provenance(self):
        # The AOI is reused, so no separate derivation chain may be declared
        # (that would create a second, divergable source of truth).
        self.assertNotIn("aoi_provenance", self.new)
        self.assertNotIn("aoi_provenance", self.old)


# =============================================================================
# Time shifts by exactly one year (5/6)
# =============================================================================
class TestOneYearTemporalShift(unittest.TestCase):
    def setUp(self):
        self.old = regions.get_experiment(OLD_ID)
        self.new = regions.get_experiment(NEW_ID)

    def test_05_predictor_and_label_dates_are_exact(self):
        self.assertEqual(self.new["predictor_start_date"], "2022-06-01")
        self.assertEqual(self.new["predictor_end_date"], "2022-07-28")
        self.assertEqual(self.new["label_start_date"], "2022-07-29")
        self.assertEqual(self.new["label_end_date"], "2022-09-15")

    def test_05_every_window_bound_is_the_2021_bound_plus_one_year(self):
        for key in ("predictor_start_date", "predictor_end_date",
                    "label_start_date", "label_end_date"):
            old_day = date.fromisoformat(self.old[key])
            new_day = date.fromisoformat(self.new[key])
            self.assertEqual(new_day, old_day.replace(year=old_day.year + 1), key)

    def test_05_label_window_starts_the_day_after_the_predictor_window(self):
        pred_end = date.fromisoformat(self.new["predictor_end_date"])
        label_start = date.fromisoformat(self.new["label_start_date"])
        self.assertEqual(label_start, pred_end + timedelta(days=1))
        self.assertLess(date.fromisoformat(self.new["predictor_start_date"]), pred_end)
        self.assertLess(label_start, date.fromisoformat(self.new["label_end_date"]))

    def test_06_baseline_years_are_exact_and_precede_the_event_year(self):
        self.assertEqual(self.new["baseline_years"], [2018, 2019, 2020, 2021])
        self.assertEqual(self.new["baseline_years"],
                         [y + 1 for y in self.old["baseline_years"]])
        self.assertTrue(all(y < 2022 for y in self.new["baseline_years"]))


# =============================================================================
# Pre-label leakage contract (7/8)
# =============================================================================
class TestPreLabelContract(unittest.TestCase):
    def setUp(self):
        self.new = regions.get_experiment(NEW_ID)

    def test_07_exclude_pre_label_burns_is_true(self):
        self.assertIs(self.new["exclude_pre_label_burns"], True)

    def test_07_pre_label_burn_window_equals_the_2022_predictor_window(self):
        self.assertEqual(self.new["pre_label_burn_window"],
                         ["2022-06-01", "2022-07-28"])
        self.assertEqual(
            self.new["pre_label_burn_window"],
            [self.new["predictor_start_date"], self.new["predictor_end_date"]],
        )

    def test_08_pre_label_diagnostic_window_is_absent(self):
        # The 2021 field isolates the Bördübet/Marmaris fire (~2021-06-21..25)
        # and is Muğla-2021-specific; it must NOT be copied forward.
        self.assertNotIn("pre_label_diagnostic_window", self.new)
        self.assertNotIn("pre_label_diagnostic_window", regions.EXPERIMENTS[NEW_ID])
        self.assertIsNone(regions.EXPERIMENTS[NEW_ID].get("pre_label_diagnostic_window"))


# =============================================================================
# Role is exact and behaves as ordinary metadata (9)
# =============================================================================
class TestTemporalRole(unittest.TestCase):
    def setUp(self):
        self.new = regions.get_experiment(NEW_ID)

    def test_09_role_is_exactly_temporal_transfer_wildfire(self):
        self.assertEqual(self.new["role"], ROLE)
        self.assertEqual(regions.EXPERIMENTS[NEW_ID]["role"], ROLE)

    def test_09_role_differs_from_the_2021_same_year_role(self):
        self.assertEqual(regions.get_experiment(OLD_ID)["role"],
                         "same_country_same_year_transfer_wildfire")
        self.assertNotEqual(self.new["role"], regions.get_experiment(OLD_ID)["role"])

    def test_09_role_selects_only_the_canonical_successor(self):
        # The role is shared with the successor, but only CANONICAL records
        # enter a canonical selection -- the superseded record is filtered out
        # by variant_status, not by role.
        selected = regions.list_canonical_enabled_experiments(role=ROLE)
        self.assertEqual(set(selected), {SUCCESSOR_ID})
        self.assertNotIn(NEW_ID, selected)

    def test_09_role_does_not_leak_into_existing_role_cohorts(self):
        for other_role in ("mediterranean_transfer_wildfire", "anchor_wildfire",
                           "same_country_same_year_transfer_wildfire",
                           "negative_control"):
            with self.subTest(role=other_role):
                self.assertNotIn(
                    NEW_ID, regions.list_canonical_enabled_experiments(role=other_role))

    def test_09_role_is_excluded_from_generic_spatial_cohort_discovery(self):
        # The burned-pattern cohort compares burned patterns ACROSS SPACE.
        # A temporal counterpart reuses an AOI that is already represented,
        # so it must be a NON-cohort role -- otherwise reaching Step8A would
        # silently enrol it in the existing spatial cohort.
        from src.burned_pattern_audit import NON_COHORT_ROLES

        self.assertIn(ROLE, NON_COHORT_ROLES)
        # The pre-existing exclusion is preserved, not replaced.
        self.assertIn("negative_control", NON_COHORT_ROLES)

    def test_09_discovery_excludes_mugla_2022_even_with_step8a_present(self):
        # Treat EVERY experiment's canonical Step8A dataset as present by
        # pointing the resolver at this test file -- an existing, read-only
        # path. No file, directory or output is created.
        import src.burned_pattern_audit as bpa

        present_path = Path(__file__).resolve()
        with patch.object(bpa, "canonical_step8a_path", return_value=present_path):
            resolution = bpa.resolve_experiments(all_enabled=True)

        # Now excluded one step EARLIER than before -- by supersession rather
        # than by role. Either way it never enters the spatial cohort.
        self.assertNotIn(NEW_ID, resolution.resolved_ids)
        self.assertEqual(resolution.excluded.get(NEW_ID),
                         f"superseded_by_{SUCCESSOR_ID}")
        # The canonical successor is excluded by its (unchanged) role.
        self.assertNotIn(SUCCESSOR_ID, resolution.resolved_ids)
        self.assertEqual(resolution.excluded.get(SUCCESSOR_ID), ROLE)
        # Discovery still works for the spatial cohort members it should keep.
        self.assertIn(OLD_ID, resolution.resolved_ids)


# =============================================================================
# Pre-existing records untouched (10)
# =============================================================================
FROZEN_MUGLA_2021 = {
    "enabled": True,
    "variant_status": "canonical",
    "region_key": "mugla_aoi",
    "display_name": "Muğla 2021",
    "role": "same_country_same_year_transfer_wildfire",
    "country": "Turkey",
    "predictor_start_date": "2021-06-01",
    "predictor_end_date": "2021-07-28",
    "label_start_date": "2021-07-29",
    "label_end_date": "2021-09-15",
    "baseline_years": [2017, 2018, 2019, 2020],
    "output_namespace": "mugla_2021",
    "exclude_pre_label_burns": True,
    "pre_label_burn_window": ["2021-06-01", "2021-07-28"],
    "pre_label_diagnostic_window": ["2021-06-21", "2021-06-25"],
}

# Scientific contract of every OTHER registered experiment, frozen so the
# additive mugla_2022 patch cannot silently modify a neighbouring record.
FROZEN_OTHER_EXPERIMENTS = {
    "kozan_2023": {
        "variant_status": "canonical", "region_key": "kozan_aoi",
        "role": "negative_control", "country": "Turkey",
        "predictor_start_date": "2023-06-01", "predictor_end_date": "2023-07-31",
        "label_start_date": "2023-08-01", "label_end_date": "2023-10-31",
        "baseline_years": [2019, 2020, 2021, 2022], "output_namespace": "kozan_2023",
    },
    "manavgat_2021": {
        "variant_status": "canonical", "region_key": "manavgat_aoi",
        "role": "anchor_wildfire", "country": "Turkey",
        "predictor_start_date": "2021-06-01", "predictor_end_date": "2021-07-27",
        "label_start_date": "2021-07-28", "label_end_date": "2021-08-31",
        "baseline_years": [2017, 2018, 2019, 2020], "output_namespace": "manavgat_2021",
    },
    "bejis_2022": {
        "variant_status": "canonical", "region_key": "bejis_aoi",
        "role": "mediterranean_transfer_wildfire", "country": "Spain",
        "predictor_start_date": "2022-06-15", "predictor_end_date": "2022-08-14",
        "label_start_date": "2022-08-15", "label_end_date": "2022-09-30",
        "baseline_years": [2018, 2019, 2020, 2021], "output_namespace": "bejis_2022",
    },
    "evia_2021": {
        "variant_status": "legacy_superseded", "region_key": "north_evia",
        "role": "mediterranean_transfer_wildfire", "country": "Greece",
        "predictor_start_date": "2021-06-05", "predictor_end_date": "2021-08-02",
        "label_start_date": "2021-08-03", "label_end_date": "2021-09-30",
        "baseline_years": [2017, 2018, 2019, 2020], "output_namespace": "evia_2021",
    },
    "evia_2021_extended": {
        "variant_status": "canonical", "region_key": "north_evia_extended",
        "role": "mediterranean_transfer_wildfire", "country": "Greece",
        "predictor_start_date": "2021-06-05", "predictor_end_date": "2021-08-02",
        "label_start_date": "2021-08-03", "label_end_date": "2021-09-30",
        "baseline_years": [2017, 2018, 2019, 2020], "output_namespace": "evia_2021_extended",
    },
    "montiferru_2021": {
        "variant_status": "canonical", "region_key": "montiferru_aoi",
        "role": "mediterranean_transfer_wildfire", "country": "Italy",
        "predictor_start_date": "2021-05-25", "predictor_end_date": "2021-07-23",
        "label_start_date": "2021-07-24", "label_end_date": "2021-08-31",
        "baseline_years": [2017, 2018, 2019, 2020], "output_namespace": "montiferru_2021",
    },
}


class TestExistingRecordsUnchanged(unittest.TestCase):
    def test_10_mugla_2021_scientific_metadata_is_unmutated(self):
        exp = regions.get_experiment(OLD_ID)
        for key, value in FROZEN_MUGLA_2021.items():
            self.assertEqual(exp[key], value, f"{OLD_ID}.{key}")
        self.assertNotIn("superseded_by", exp)

    def test_10_mugla_2021_output_namespace_is_untouched(self):
        self.assertEqual(regions.get_experiment_output_root(OLD_ID),
                         _PROJECT_ROOT / "outputs" / "experiments" / OLD_ID)

    def test_10_every_other_canonical_record_is_unchanged(self):
        for exp_id, expected in FROZEN_OTHER_EXPERIMENTS.items():
            exp = regions.get_experiment(exp_id)
            self.assertTrue(exp["enabled"], exp_id)
            for key, value in expected.items():
                self.assertEqual(exp[key], value, f"{exp_id}.{key}")

    def test_10_default_experiment_is_still_kozan(self):
        self.assertEqual(regions.DEFAULT_EXPERIMENT_ID, "kozan_2023")
        self.assertEqual(regions.get_active_experiment()["experiment_id"], "kozan_2023")

    def test_10_registry_contains_exactly_the_expected_keys(self):
        self.assertEqual(
            set(regions.EXPERIMENTS),
            set(FROZEN_OTHER_EXPERIMENTS) | {OLD_ID, NEW_ID, SUCCESSOR_ID}
            | set(regions.SCALEUP_EXPERIMENT_IDS),
        )


# =============================================================================
# No new hard-coded date branch (11)
# =============================================================================
class TestNoHardCodedDateBranch(unittest.TestCase):
    def test_11_step8a_declares_no_mugla_2022_expected_date_branch(self):
        # Step8A pins expected dates only for MANUALLY verified experiments
        # (_EXPECTED_EXPERIMENT_DATES); an unlisted experiment is handled by
        # the generic registry/preregistration path. mugla_2022 must stay
        # generic -- no per-AOI literal anywhere in that module.
        source = (_PROJECT_ROOT / "src"
                  / "step8a_prepare_500m_modeling_dataset.py").read_text(encoding="utf-8")
        self.assertNotIn(NEW_ID, source)

    def test_11_registry_is_the_only_source_of_the_new_dates(self):
        source = (_PROJECT_ROOT / "core" / "regions.py").read_text(encoding="utf-8")
        self.assertEqual(source.count(f'"{NEW_ID}": {{'), 1)


if __name__ == "__main__":
    unittest.main()

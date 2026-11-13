"""
core/experiment_context.py

Step0D: Manavgat (ve gelecekteki deneyler) icin Step1-Step5/5C predictor
uretimini deney-farkinda (experiment-aware) hale getiren merkezi context
helper'i.

build_experiment_context(experiment_id) tek bir dict dondurur; bu dict,
step3/step4/step4b/step5/step5c'nin (deney-farkinda hale getirilen)
fonksiyonlarina ve scripts/run_predictors_only.py'a GIRDI olarak verilir.

ONEMLI:
    - kozan_2023 icin bu context'in kullanilmasi ZORUNLU DEGILDIR: Step1-Step8
      hala kendi legacy core/config.py sabitlerini kullanmaya devam eder.
      Context yalnizca "ctx=None ise legacy davranis" seklinde opsiyonel bir
      katmandir.
    - Kozan-disi deneyler icin (ctx verildiginde) TUM girdi/cikti dizinleri
      outputs/experiments/<experiment_id>/ ve data/experiments/<experiment_id>/
      altinda, namespaced olarak hesaplanir; legacy paylasilan yollara
      (data/current_period/, data/baseline_period/, outputs/step5/,
      outputs/step5c/, vb.) HICBIR ZAMAN yazilmaz/okunmaz.
"""

from __future__ import annotations

from pathlib import Path

from core.paths import PROJECT_ROOT
from core.regions import (
    get_active_experiment,
    get_experiment_output_root,
    get_region_for_experiment,
)

BASE_DIR = PROJECT_ROOT


def _current_period_days(predictor_start_date: str, predictor_end_date: str) -> int:
    """
    Current period pencere gunu sayisini, PROJENIN MEVCUT konvansiyonuyla
    (core/config.py CURRENT_PERIOD_DAYS) BIREBIR ayni sekilde hesaplar:

        current_period_days = (predictor_end_date - predictor_start_date).days

    Bu, basit bir tarih FARKIDIR -- "inclusive" (her iki ucu da sayan) bir
    gun sayimi DEGILDIR. Ornegin Kozan icin:
        2023-06-01 -> 2023-07-31  =>  60 gun (mevcut CURRENT_PERIOD_DAYS=60
        ile birebir eslesir)
    Manavgat icin:
        2021-06-01 -> 2021-07-27  =>  56 gun (BU FONKSIYONUN DONDURDUGU
        DEGER), 57 DEGIL -- 57, iki ucu da sayan "inclusive" bir sayimdir ve
        mevcut proje konvansiyonuyla (step3_landsat_lst.py:
        get_current_period_median: start_dt = end_dt - timedelta(days=window_days))
        TUTARSIZDIR. Bilerek 57 degil 56 kullaniyoruz; aksi halde current
        period penceresi 1 gun kayar (off-by-one).
    """
    from datetime import datetime

    start_dt = datetime.strptime(predictor_start_date, "%Y-%m-%d")
    end_dt = datetime.strptime(predictor_end_date, "%Y-%m-%d")
    return (end_dt - start_dt).days


def _resolve_historical_contract(exp: dict) -> dict | None:
    """Resolve the generic historical-burn exclusion contract, or None.

    Imported lazily so core.experiment_context keeps no hard dependency on
    src/ (and so experiments that do not opt in never load it at all).
    """
    if not exp.get("exclude_historical_burns", False):
        return None
    from src.historical_burn_exclusion import resolve_historical_burn_contract

    return resolve_historical_burn_contract(exp)


def build_experiment_context(experiment_id: str) -> dict:
    """
    Bir deney icin Step1-Step5/5C predictor uretiminde kullanilacak TUM
    yol/tarih/parametre bilgisini tek bir dict'te toplar.

    kozan_2023 icin de cagirilabilir (bilgilendirme/dry-run amacli), ama
    Step1-Step8 script'leri kozan_2023 icin bu context'i KULLANMAZ --
    kendi legacy core/config.py sabitlerini kullanmaya devam ederler.
    """
    exp = get_active_experiment(experiment_id)

    predictor_start_date = exp["predictor_start_date"]
    predictor_end_date = exp["predictor_end_date"]
    label_start_date = exp["label_start_date"]
    label_end_date = exp["label_end_date"]
    baseline_years = exp["baseline_years"]

    if predictor_start_date is None or predictor_end_date is None:
        raise ValueError(
            f"'{experiment_id}' deneyinin predictor penceresi tanimsiz "
            "(placeholder/disabled deney olabilir). Context olusturulamaz."
        )

    current_period_days = _current_period_days(predictor_start_date, predictor_end_date)
    current_period_end_date = predictor_end_date

    is_kozan = (experiment_id == "kozan_2023")
    output_root = get_experiment_output_root(experiment_id)

    if is_kozan:
        # Legacy, namespace'siz dizinler -- Kozan davranisi BIREBIR korunur.
        data_root = BASE_DIR / "data"
        outputs_root = BASE_DIR / "outputs"
        gate_labels_dir = BASE_DIR / "outputs" / "validation" / "labels"
        step4_metadata_path = BASE_DIR / "outputs" / "step4" / "step4_metadata.json"
        export_prefix = "landsat"
    else:
        # Kozan-disi (Manavgat vb.): TAMAMEN namespaced.
        data_root = output_root / "data"
        outputs_root = output_root
        gate_labels_dir = output_root / "validation" / "labels"
        # Manavgat icin henuz Step4 (Drive export) metadata akisi yok; step5
        # bu None gordugunde dizin taramasina duser (bkz. step5:
        # list_baseline_tifs_from_step4_metadata).
        step4_metadata_path = None
        export_prefix = f"{experiment_id}_landsat"

    ctx = {
        "experiment_id": experiment_id,
        "is_kozan": is_kozan,
        "region_key": exp["region_key"],
        "role": exp["role"],
        "display_name": exp["display_name"],
        # Region geometrisi lazy cozulur (GEE init gerektirir); yalnizca
        # cagiran taraf gercekten ihtiyac duyarsa cozulsun diye fonksiyon
        # olarak da erisilebilir birakiyoruz (bkz. get_region()).
        "region_key_resolved": exp["region_key"],
        "predictor_start_date": predictor_start_date,
        "predictor_end_date": predictor_end_date,
        "label_start_date": label_start_date,
        "label_end_date": label_end_date,
        "baseline_years": baseline_years,
        "baseline_start_date": f"{min(baseline_years)}-01-01",
        "baseline_end_date": f"{max(baseline_years)}-12-31",
        # Leakage-safe pre-label exclusion (opt-in per experiment; currently
        # only mugla_2021). Step8A reads this to decide whether the Step6B
        # gate's cell-level exclusion manifest is REQUIRED (fail-fast if
        # missing) -- see src/step8a_prepare_500m_modeling_dataset.py
        # read_pre_label_exclusion_manifest().
        "exclude_pre_label_burns": bool(exp.get("exclude_pre_label_burns", False)),
        # Historical burn exclusion (SEPARATE, independent axis; opt-in per
        # experiment). Same declarative pattern as above: Step8A reads these
        # to decide whether the gate's historical exclusion manifest is
        # REQUIRED (fail-fast if missing) -- see
        # src/historical_burn_exclusion.py. The resolved contract dict is
        # attached too so downstream provenance can record the source
        # experiment/kind without re-reading the registry. Resolution is
        # deferred to a helper so an invalid declaration fails closed here
        # rather than deep inside Step8A.
        "exclude_historical_burns": bool(exp.get("exclude_historical_burns", False)),
        # MODIS predictor month filter (opt-out per experiment). True (default, every experiment
        # of the manuscript) keeps only the SUMMER_MONTH_START..END days of the predictor window;
        # False uses every day of the window (scale-up fires whose window starts before June).
        "modis_predictor_month_filter": bool(exp.get("modis_predictor_month_filter", True)),
        "historical_burn_exclusion": _resolve_historical_contract(exp),
        "current_period_days": current_period_days,
        "current_period_end_date": current_period_end_date,
        "output_root": output_root,
        # --- Girdi (data) dizinleri ---
        "data_root": data_root,
        "baseline_input_dir": data_root / "landsat_timeseries",
        "qa_dir": data_root / "landsat_qa",
        "current_period_dir": data_root / "current_period",
        "modis_input_dir": data_root / "modis",
        "ndvi_baseline_dir": data_root / "ndvi_timeseries",
        "ndvi_current_dir": data_root / "ndvi_current_period",
        "enable_modis_context": False if not is_kozan else None,  # bkz. NOT asagida
        # DEM (elevation/slope): Kozan icin PAYLASILAN/SALT-OKUNUR global
        # asset (data/dem/elevation.tif + data/dem/slope.tif) -- legacy
        # davranis DEGISMEDI. Kozan-disi deneyler icin (or. manavgat_2021)
        # ARTIK TAMAMEN NAMESPACED: outputs/experiments/<experiment_id>/data/dem/
        # -- cunku paylasilan data/dem/ yalnizca Kozan'in AOI'sini kapsiyor ve
        # Manavgat ile COGRAFI OLARAK ORTUSMUYOR (bkz.
        # scripts/prepare_dem_for_experiment.py). Manavgat-turetilmis hicbir
        # DEM ciktisi Kozan'in paylasilan dizinine YAZILMAZ.
        "dem_input_dir": data_root / "dem",
        "dem_is_shared_read_only": is_kozan,
        # Landcover: Kozan-disi deneyler icin Step6A gate-input asamasinda
        # zaten uretilmis, referans gride hizali landcover reuse edilir
        # (bkz. src/step6a_prepare_gate_inputs.py). Kozan icin bu alan None
        # birakilir -- Kozan hala kendi legacy data/landcover/... yolunu
        # kullanir (Step7B/7D kendi legacy kesif mantiklarinda).
        "landcover_aligned_path": (
            None if is_kozan
            else output_root / "gate_inputs" / "landcover_esa_worldcover_v200_aligned_to_reference.tif"
        ),
        # --- Cikti dizinleri ---
        "step4_metadata_path": step4_metadata_path,
        "landsat_file_prefix": export_prefix,
        "step5_output_dir": outputs_root / "step5",
        "step5b_output_dir": outputs_root / "step5b",
        "step5c_output_dir": outputs_root / "step5c",
        "output_dir": outputs_root / "step5",  # step5.process_step5_windowed icin
        "step7a_output_dir": outputs_root / "step7a",
        "step7b_output_dir": outputs_root / "step7b",
        "step7c_output_dir": outputs_root / "step7c",
        "step7d_output_dir": outputs_root / "step7d",
        "step7e_output_dir": outputs_root / "step7e",
        "step8a_output_dir": outputs_root / "step8a",
        "step8b_output_dir": outputs_root / "step8b",
        "step8c_output_dir": outputs_root / "step8c",
        "step8d_output_dir": outputs_root / "step8d",
        "step8e_output_dir": outputs_root / "step8e",
        "gate_labels_dir": gate_labels_dir,
        "export_prefix": export_prefix,
    }

    if is_kozan:
        # Kozan icin enable_modis_context'i legacy core.config degerinden al
        # (bu deger None birakildi yukarida cunku core.config importu
        # dongusel olabilir; burada guvenle import edilebilir cunku
        # core.config core.regions'i import ETMEZ -- core.regions
        # core.config'i import eder, tersi degil, bkz. core/config.py Step0
        # koprusu).
        from core.config import ENABLE_MODIS_STEP5_CONTEXT

        ctx["enable_modis_context"] = ENABLE_MODIS_STEP5_CONTEXT

    return ctx


def get_region(ctx: dict):
    """ctx icin AOI geometrisini cozer (GEE init gerektirir)."""
    return get_region_for_experiment(ctx["experiment_id"])


def log_context_summary(ctx: dict, log) -> None:
    """Bir context'in tum onemli alanlarini standart formatta loglar."""
    log.info("[ExperimentContext] experiment_id: %s", ctx["experiment_id"])
    log.info("[ExperimentContext] region_key: %s", ctx["region_key"])
    log.info("[ExperimentContext] role: %s", ctx["role"])
    log.info(
        "[ExperimentContext] Predictor window: %s -> %s",
        ctx["predictor_start_date"], ctx["predictor_end_date"],
    )
    log.info(
        "[ExperimentContext] current_period_end_date=%s, current_period_days=%s "
        "(plain date-diff, NOT inclusive count)",
        ctx["current_period_end_date"], ctx["current_period_days"],
    )
    log.info(
        "[ExperimentContext] Label window: %s -> %s",
        ctx["label_start_date"], ctx["label_end_date"],
    )
    log.info("[ExperimentContext] Baseline years: %s", ctx["baseline_years"])
    log.info(
        "[ExperimentContext] Baseline date bounds (year-bounding, not exact window): %s -> %s",
        ctx["baseline_start_date"], ctx["baseline_end_date"],
    )
    log.info("[ExperimentContext] output_root: %s", ctx["output_root"])
    log.info("[ExperimentContext] data_root: %s", ctx["data_root"])
    log.info("[ExperimentContext] step5_output_dir: %s", ctx["step5_output_dir"])
    log.info("[ExperimentContext] step5c_output_dir: %s", ctx["step5c_output_dir"])
    log.info("[ExperimentContext] gate_labels_dir: %s", ctx["gate_labels_dir"])
    log.info(
        "[ExperimentContext] exclude_pre_label_burns=%s exclude_historical_burns=%s",
        ctx["exclude_pre_label_burns"], ctx["exclude_historical_burns"],
    )
    if ctx.get("historical_burn_exclusion"):
        contract = ctx["historical_burn_exclusion"]
        log.info(
            "[ExperimentContext] historical burn source: %s (kind=%s, "
            "expected physical burned cells=%s)",
            contract["source_experiment_id"], contract["source_kind"],
            contract["source_expected_physical_burned_count"],
        )
    log.info(
        "[ExperimentContext] dem_input_dir (%s): %s",
        "shared, read-only (Kozan legacy)" if ctx["is_kozan"] else "namespaced",
        ctx["dem_input_dir"],
    )
    log.info(
        "[ExperimentContext] landcover_aligned_path: %s",
        ctx["landcover_aligned_path"] if ctx["landcover_aligned_path"] else "(Kozan legacy discovery)",
    )
    log.info(
        "[ExperimentContext] step7 output dirs: a=%s b=%s c=%s d=%s e=%s",
        ctx["step7a_output_dir"], ctx["step7b_output_dir"], ctx["step7c_output_dir"],
        ctx["step7d_output_dir"], ctx["step7e_output_dir"],
    )
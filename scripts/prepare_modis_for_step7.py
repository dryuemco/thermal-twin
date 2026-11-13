"""
prepare_modis_for_step7.py

Step0F: Step7 (downscaling) icin gerekli MODIS LST mean/std/valid-count
girdisini, Kozan-disi bir deney icin (or. manavgat_2021, evia_2021) TAMAMEN
namespaced sekilde hazirlar.

Cikti:
    outputs/experiments/<experiment_id>/data/modis/modis_lst_mean_celsius.tif
    outputs/experiments/<experiment_id>/data/modis/modis_lst_std_celsius.tif
    outputs/experiments/<experiment_id>/data/modis/modis_valid_observation_count.tif
    outputs/experiments/<experiment_id>/data/modis/modis_metadata.json

MODIS GIRDI QA (bkz. core/config.py STEP7_MODIS_* sabitleri):
    - QC_Day maskesi: yalnizca mandatory QA (bit 0-1) == 00 VE data quality
      (bit 2-3) == 00 olan piksel-gunler kabul edilir (bkz. _qc_accept_mask).
      Ayrica ham LST_Day_1km DN > 0 sarti aranir (0, urunun kendi
      fill/no-retrieval degeridir; Celsius'a cevrilmeden ONCE elenir).
    - Bir pikselin mean/std'si, o pikselde predictor penceresi icinde
      STEP7_MODIS_MIN_VALID_OBSERVATIONS'tan AZ QC-kabul-edilmis gozlem
      varsa NODATA birakilir (istatistiksel destek esigi).
    - Maskeli/gozlemsiz pikseller HICBIR asamada (EE agregasyonu, direct
      export, tiled export/merge, nihai GeoTIFF) sayisal 0.0'a
      DONUSTURULMEZ: export ONCESI acikca STEP7_MODIS_NODATA_VALUE ile
      unmask edilir ve indirilen GeoTIFF'e AYNI deger nodata olarak
      damgalanir (bkz. scripts/run_predictors_only.py `nodata=` parametresi).

ONEMLI:
    - Kozan'in legacy data/modis/ dizini VE src/step2_modis_5year_mean.py
      (legacy Step2 MODIS baseline) bu script tarafindan ASLA
      degistirilmez/okunmaz/yazilmaz -- bu QA duzeltmesi SADECE bu
      script'in kendi (deney-farkinda) MODIS agregasyon fonksiyonuna
      (_build_qc_masked_modis_stack) uygulanir, process_summer_mean() artik
      REUSE EDILMEZ (QC/valid-count/nodata mantigi olmadigi icin).
    - GEE'nin senkron getPixels boyut limitini asan export'lar icin,
      scripts/run_predictors_only.py:export_image_direct_or_tiled()
      (direct -> 2x2 -> 4x4 -> 6x6 -> 8x8 tiled fallback) REUSE edilir --
      yeni bir tiled export mantigi YAZILMAZ; yalnizca genel `nodata=`
      parametresi (bkz. o dosyadaki degisiklik) kullanilir.
    - Bu script yalnizca MODIS girdisini HAZIRLAR; Step7B/7C/7D/7E'yi
      CALISTIRMAZ, Step8'i KESINLIKLE CALISTIRMAZ, hicbir model EGITMEZ.

CLI:
    python scripts/prepare_modis_for_step7.py --experiment manavgat_2021 --dry-run
    python scripts/prepare_modis_for_step7.py --experiment manavgat_2021 --export --force
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from core.experiment_context import build_experiment_context, get_region, log_context_summary
from core.io_utils import setup_logger

log, log_file = setup_logger("prepare_modis_for_step7")

BASE_DIR = _PROJECT_ROOT
MODIS_EXPORT_SCALE = 1000  # MOD11A1 native ~1 km

_LEGACY_MODIS_DIR = (BASE_DIR / "data" / "modis").resolve()


class ModisPrepError(SystemExit):
    """Fail-fast error for this script (diğer step'lerle aynı konvansiyon)."""


def resolve_modis_output_paths(ctx: dict) -> dict:
    """
    Bir deney icin MODIS cikti yollarini cozer.

    kozan_2023 icin (ctx["is_kozan"]) legacy data/modis/ dondurur (bu
    script'in Kozan icin kullanilmasi ONERILMEZ -- Kozan zaten
    scripts/main.py -> src/step2_modis_5year_mean.py + Step4/4B Drive
    export zinciriyle hazirlanir). Kozan-disi deneyler icin TAMAMEN
    namespaced (outputs/experiments/<experiment_id>/data/modis/) doner.
    """
    if ctx["is_kozan"]:
        modis_dir = BASE_DIR / "data" / "modis"
    else:
        modis_dir = ctx["modis_input_dir"]
    return {
        "modis_dir": modis_dir,
        "mean_path": modis_dir / "modis_lst_mean_celsius.tif",
        "std_path": modis_dir / "modis_lst_std_celsius.tif",
        "valid_count_path": modis_dir / "modis_valid_observation_count.tif",
        "metadata_path": modis_dir / "modis_metadata.json",
    }


#: Bir cagiran, kendi ADANMIS diagnostics namespace'ine MODIS uretmek icin
#: ctx'e EK bir izinli kok koyabilir (or. window-closure sensitivity varyant
#: namespace'i). Anahtar YOKSA davranis ESKISIYLE BIREBIR AYNIDIR.
NAMESPACE_ALLOWED_ROOTS_KEY = "namespace_allowed_roots"


def _resolve_allowed_output_roots(ctx: dict) -> list[Path]:
    """Bu ctx icin MODIS ciktilarinin yazilabilecegi izinli kokler.

    Varsayilan TEK kok, deneyin kendi canonical namespace'idir. Cagiran
    ctx[NAMESPACE_ALLOWED_ROOTS_KEY] ile EK kok(ler) verebilir; bunlar:
      * outputs/ altinda olmak,
      * outputs/experiments/ altinda OLMAMAK
    zorundadir. Boylece bir diagnostics namespace'i acikca izinli hale
    getirilebilirken, BASKA bir deneyin canonical namespace'i asla
    acilamaz.
    """
    experiment_id = ctx["experiment_id"]
    outputs_root = (BASE_DIR / "outputs").resolve()
    experiments_parent = (outputs_root / "experiments").resolve()
    roots = [(experiments_parent / experiment_id).resolve()]

    for extra in ctx.get(NAMESPACE_ALLOWED_ROOTS_KEY) or ():
        resolved = Path(extra).resolve()
        if resolved != outputs_root and outputs_root not in resolved.parents:
            raise ModisPrepError(
                f"GÜVENLİK İHLALİ: ek izinli kök ({resolved}) outputs/ dışında. "
                "İşlem DURDURULDU."
            )
        if resolved == experiments_parent or experiments_parent in resolved.parents:
            raise ModisPrepError(
                f"GÜVENLİK İHLALİ: ek izinli kök ({resolved}) canonical "
                "outputs/experiments/ ağacının içinde; başka bir deneyin "
                "namespace'i bu yolla açılamaz. İşlem DURDURULDU."
            )
        roots.append(resolved)
    return roots


def _assert_paths_are_safely_namespaced(ctx: dict, paths: dict) -> None:
    """
    GÜVENLİK KONTROLÜ (Kozan-dışı deneyler için ZORUNLU): tüm MODIS çıktı
    yolları izinli köklerden birinin (varsayılan:
    outputs/experiments/<experiment_id>/) altında olmalı ve legacy Kozan
    data/modis/ dizinine ASLA düşmemelidir.
    """
    experiment_id = ctx["experiment_id"]
    allowed_roots = _resolve_allowed_output_roots(ctx)

    for key in ("modis_dir", "mean_path", "std_path", "valid_count_path", "metadata_path"):
        resolved = Path(paths[key]).resolve()
        if resolved == _LEGACY_MODIS_DIR or _LEGACY_MODIS_DIR in resolved.parents:
            raise ModisPrepError(
                f"GÜVENLİK İHLALİ: '{experiment_id}' deneyi için '{key}' yolu "
                f"({resolved}) Kozan'ın legacy paylaşılan MODIS dizinine "
                f"({_LEGACY_MODIS_DIR}) düşüyor. İşlem DURDURULDU."
            )
        if not any(
            resolved == root or root in resolved.parents for root in allowed_roots
        ):
            raise ModisPrepError(
                f"GÜVENLİK İHLALİ: '{experiment_id}' deneyi için '{key}' yolu "
                f"({resolved}) izinli köklerin "
                f"({[str(r) for r in allowed_roots]}) dışında. İşlem DURDURULDU."
            )


def _qc_accept_mask(image):
    """
    MOD11A1 QC_Day conservative accept mask (bkz. core/config.py
    STEP7_MODIS_QC_* sabitleri + modul docstring'i icin bit tanimlari).

    Kabul kosulu: mandatory QA (bit 0-1) == 0 VE data quality (bit 2-3) == 0
    VE ham LST_Day_1km DN > 0 (urunun kendi fill/no-retrieval degeri).
    """
    from core.config import (
        STEP7_MODIS_QC_DATA_QUALITY_ACCEPT,
        STEP7_MODIS_QC_DATA_QUALITY_MASK,
        STEP7_MODIS_QC_DATA_QUALITY_SHIFT,
        STEP7_MODIS_QC_MANDATORY_QA_ACCEPT,
        STEP7_MODIS_QC_MANDATORY_QA_MASK,
    )

    lst_dn = image.select("LST_Day_1km")
    qc = image.select("QC_Day")
    mandatory_qa = qc.bitwiseAnd(STEP7_MODIS_QC_MANDATORY_QA_MASK)
    data_quality = (
        qc.rightShift(STEP7_MODIS_QC_DATA_QUALITY_SHIFT)
        .bitwiseAnd(STEP7_MODIS_QC_DATA_QUALITY_MASK)
    )
    qc_ok = mandatory_qa.eq(STEP7_MODIS_QC_MANDATORY_QA_ACCEPT).And(
        data_quality.eq(STEP7_MODIS_QC_DATA_QUALITY_ACCEPT)
    )
    dn_ok = lst_dn.gt(0)
    return qc_ok.And(dn_ok)


def _build_qc_masked_modis_stack(region, start: str, end: str, month_filter: bool = True):
    """
    Deney-farkinda MODIS mean/std/valid-count hesaplayan, QC-maskeli
    agregasyon fonksiyonu (src/step2_modis_5year_mean.py:process_summer_mean()
    REUSE EDILMEZ -- o fonksiyon QC/valid-count/nodata mantigi TASIMAZ ve
    Kozan'in legacy Step2 baseline'i icin DEGISMEDEN birakilmalidir).

    Ayni filterBounds/filterDate/calendarRange(SUMMER_MONTH_START..END)
    secim mantigini process_summer_mean() ile BIREBIR korur -- yalnizca
    QC maskesi, gozlem-sayisi esigi ve nodata-guvenli export'a hazirlik
    (unmask) EKLER.

    Doner: (mean_image, std_image, valid_count_image, source_meta)
        mean_image/std_image: STEP7_MODIS_MIN_VALID_OBSERVATIONS esiginin
            ALTINDAKI pikseller icin MASKELI (nodata) -- export'tan HEMEN
            ONCE caller tarafindan unmask(STEP7_MODIS_NODATA_VALUE) edilmesi
            BEKLENIR (bkz. prepare_modis_for_step7).
        valid_count_image: HER pikselde QC-kabul-edilmis gozlem sayisi
            (maskesiz -- 0 gecerli/gercek bir deger, nodata DEGIL).
    """
    import ee

    from core.config import MODIS_COLLECTION, SUMMER_MONTH_END, SUMMER_MONTH_START

    raw_collection = (
        ee.ImageCollection(MODIS_COLLECTION)
        .filterBounds(region)
        .filterDate(start, end)
    )
    # month_filter=False (experiment registry key modis_predictor_month_filter) uses every day
    # of the predictor window; the default keeps the summer-month filter unchanged.
    if month_filter:
        raw_collection = raw_collection.filter(
            ee.Filter.calendarRange(SUMMER_MONTH_START, SUMMER_MONTH_END, "month")
        )
        months_label = f"{SUMMER_MONTH_START}-{SUMMER_MONTH_END}"
    else:
        months_label = "all (full predictor window, no month filter)"
    image_count = raw_collection.size().getInfo()
    if image_count == 0:
        raise ModisPrepError(
            f"Predictor penceresinde ({start} -> {end}, ay araligi "
            f"{months_label}) hicbir MODIS sahnesi "
            "bulunamadi."
        )

    def _to_qc_masked_celsius(image):
        mask = _qc_accept_mask(image)
        celsius = (
            image.select("LST_Day_1km")
            .multiply(0.02)
            .subtract(273.15)
            .rename("LST_Celsius")
            .updateMask(mask)
        )
        return celsius.copyProperties(image, ["system:time_start"])

    masked_collection = raw_collection.map(_to_qc_masked_celsius)
    lst_only = masked_collection.select("LST_Celsius")

    from core.config import STEP7_MODIS_MIN_VALID_OBSERVATIONS

    valid_count_image = lst_only.reduce(ee.Reducer.count()).rename(
        "modis_valid_observation_count"
    )
    enough_obs = valid_count_image.gte(STEP7_MODIS_MIN_VALID_OBSERVATIONS)

    mean_image = (
        lst_only.mean()
        .updateMask(enough_obs)
        .rename("modis_lst_mean_celsius")
        .clip(region)
    )
    std_image = (
        lst_only.reduce(ee.Reducer.stdDev())
        .updateMask(enough_obs)
        .rename("modis_lst_std_celsius")
        .clip(region)
    )
    # Gozlem sayisi kendisi maskelenmez (0 gecerli/gercek bir deger).
    valid_count_image = valid_count_image.unmask(0).clip(region)

    source_meta = {
        "input_band": "LST_Day_1km",
        "qc_band": "QC_Day",
        "image_count": image_count,
        "months": months_label,
    }
    return mean_image, std_image, valid_count_image, source_meta


def _raster_summary_stats(path: Path) -> dict:
    """downscaling'den bagimsiz, salt-okunur bir GeoTIFF ozet (metadata icin):
    nodata, gecerli/gecersiz piksel sayisi, tam-sifir gecerli piksel sayisi,
    min/max/mean/median (yalnizca gecerli pikseller uzerinden)."""
    import numpy as np
    import rasterio

    with rasterio.open(path) as src:
        nodata = src.nodata
        arr = src.read(1)

    if nodata is None:
        valid_mask = np.ones(arr.shape, dtype=bool)
    elif isinstance(nodata, float) and np.isnan(nodata):
        valid_mask = np.isfinite(arr)
    else:
        valid_mask = arr != nodata
    valid_vals = arr[valid_mask]

    return {
        "nodata": None if nodata is None else float(nodata),
        "valid_pixel_count": int(valid_mask.sum()),
        "invalid_pixel_count": int((~valid_mask).sum()),
        "exact_zero_valid_pixel_count": int((valid_vals == 0.0).sum()) if valid_vals.size else 0,
        "min": float(valid_vals.min()) if valid_vals.size else None,
        "max": float(valid_vals.max()) if valid_vals.size else None,
        "mean": float(valid_vals.mean()) if valid_vals.size else None,
        "median": float(np.median(valid_vals)) if valid_vals.size else None,
    }


def _sha256_file(path: Path) -> str | None:
    if not path.exists():
        return None
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def prepare_modis_for_step7(ctx: dict, force: bool = False) -> dict:
    """
    Secili deney icin MODIS LST mean/std/valid-count'u (predictor penceresi
    icin) export eder ve metadata JSON'unu yazar.

    Kozan-disi deneyler icin (ctx["is_kozan"]=False) BASARISIZLIK durumunda
    (GEE erisimi yok, export basarisiz, vb.) HATA FIRLATIR (bu artik Step7
    icin ZORUNLU bir girdi -- bkz. run_step7_downscaling_only.py'nin
    fail-fast MODIS kontrolu). Kozan icin bu fonksiyon KULLANILMAMALIDIR
    (bkz. resolve_modis_output_paths docstring); yine de cagrilirsa
    basarisizlik durumunda da hata fırlatir (best-effort/sessiz yutma YOK).
    """
    paths = resolve_modis_output_paths(ctx)
    if not ctx["is_kozan"]:
        _assert_paths_are_safely_namespaced(ctx, paths)

    mean_path = paths["mean_path"]
    std_path = paths["std_path"]
    valid_count_path = paths["valid_count_path"]
    metadata_path = paths["metadata_path"]

    if mean_path.exists() and std_path.exists() and valid_count_path.exists() and not force:
        log.info(
            "MODIS zaten mevcut, atlanıyor: %s, %s, %s",
            mean_path, std_path, valid_count_path,
        )
        return {
            "status": "already_exists", "mean_path": str(mean_path), "std_path": str(std_path),
            "valid_count_path": str(valid_count_path),
            "metadata_path": str(metadata_path) if metadata_path.exists() else None,
        }

    import ee
    from core.config import (
        EXPORT_CRS,
        GEE_PROJECT,
        MODIS_COLLECTION,
        STEP7_MODIS_MIN_VALID_OBSERVATIONS,
        STEP7_MODIS_NODATA_VALUE,
        STEP7_MODIS_QC_DATA_QUALITY_ACCEPT,
        STEP7_MODIS_QC_DATA_QUALITY_MASK,
        STEP7_MODIS_QC_DATA_QUALITY_SHIFT,
        STEP7_MODIS_QC_MANDATORY_QA_ACCEPT,
        STEP7_MODIS_QC_MANDATORY_QA_MASK,
    )
    from core.gee_utils import init_gee
    from scripts.run_predictors_only import export_image_direct_or_tiled

    init_gee(GEE_PROJECT)
    region = get_region(ctx)
    paths["modis_dir"].mkdir(parents=True, exist_ok=True)

    log.info(
        "MODIS LST mean/std/valid-count hesaplanıyor (QC-maskeli): region=%s, "
        "pencere=%s -> %s (deneyin PREDICTOR penceresi; çoklu-yıl baseline "
        "DEĞİL)", ctx["region_key"], ctx["predictor_start_date"], ctx["predictor_end_date"],
    )
    mean_image, std_image, valid_count_image, source_meta = _build_qc_masked_modis_stack(
        region, ctx["predictor_start_date"], ctx["predictor_end_date"],
        month_filter=ctx.get("modis_predictor_month_filter", True),
    )

    # Export ONCESI acikca finite sentinel ile unmask: maskeli/gozlemsiz
    # pikseller export'a HICBIR ZAMAN sayisal 0.0 olarak GIRMEZ.
    mean_export_image = mean_image.unmask(STEP7_MODIS_NODATA_VALUE)
    std_export_image = std_image.unmask(STEP7_MODIS_NODATA_VALUE)

    tiles_dir_mean = paths["modis_dir"] / "_tiles" / "modis_lst_mean"
    tiles_dir_std = paths["modis_dir"] / "_tiles" / "modis_lst_std"
    tiles_dir_count = paths["modis_dir"] / "_tiles" / "modis_valid_observation_count"

    mean_result = export_image_direct_or_tiled(
        mean_export_image, mean_path, region, scale=MODIS_EXPORT_SCALE, crs=EXPORT_CRS,
        label="modis_lst_mean", force=force, tiles_dir=tiles_dir_mean,
        nodata=STEP7_MODIS_NODATA_VALUE,
    )
    std_result = export_image_direct_or_tiled(
        std_export_image, std_path, region, scale=MODIS_EXPORT_SCALE, crs=EXPORT_CRS,
        label="modis_lst_std", force=force, tiles_dir=tiles_dir_std,
        nodata=STEP7_MODIS_NODATA_VALUE,
    )
    # Gozlem sayisi rasterinde 0, gecerli/gercek bir deger oldugu icin nodata
    # etiketi KULLANILMAZ (tum piksellerin anlamli bir sayisi vardir).
    count_result = export_image_direct_or_tiled(
        valid_count_image, valid_count_path, region, scale=MODIS_EXPORT_SCALE, crs=EXPORT_CRS,
        label="modis_valid_observation_count", force=force, tiles_dir=tiles_dir_count,
    )
    log.info(
        "MODIS export tamamlandı: mean_transport=%s std_transport=%s count_transport=%s",
        mean_result["transport"], std_result["transport"], count_result["transport"],
    )

    mean_stats = _raster_summary_stats(mean_path)
    std_stats = _raster_summary_stats(std_path)
    count_stats = _raster_summary_stats(valid_count_path)

    metadata = {
        "experiment_id": ctx["experiment_id"],
        "region_key": ctx["region_key"],
        "predictor_start_date": ctx["predictor_start_date"],
        "predictor_end_date": ctx["predictor_end_date"],
        "modis_product": MODIS_COLLECTION,
        "modis_input_band": source_meta.get("input_band", "LST_Day_1km"),
        "modis_qc_band": source_meta.get("qc_band", "QC_Day"),
        "dn_to_celsius_formula": "LST_Day_1km * 0.02 - 273.15",
        "dn_valid_rule": "LST_Day_1km > 0 (product fill/no-retrieval value is 0)",
        "qc_bit_rule": {
            "description": (
                "Conservative MOD11A1 QC_Day accept rule: a pixel-day is "
                "accepted only if BOTH the mandatory QA field (bits 0-1) and "
                "the data quality field (bits 2-3) equal 0."
            ),
            "mandatory_qa_bitmask": STEP7_MODIS_QC_MANDATORY_QA_MASK,
            "mandatory_qa_accept_value": STEP7_MODIS_QC_MANDATORY_QA_ACCEPT,
            "mandatory_qa_meaning": "0 = LST produced, good quality",
            "data_quality_shift": STEP7_MODIS_QC_DATA_QUALITY_SHIFT,
            "data_quality_bitmask": STEP7_MODIS_QC_DATA_QUALITY_MASK,
            "data_quality_accept_value": STEP7_MODIS_QC_DATA_QUALITY_ACCEPT,
            "data_quality_meaning": "0 = good data quality",
        },
        "aggregation_window": (
            "experiment predictor window (single-season mean/std over daily "
            "MODIS scenes within the window), NOT a multi-year baseline"
        ),
        "earth_engine_image_count": source_meta.get("image_count"),
        "valid_observation_threshold": STEP7_MODIS_MIN_VALID_OBSERVATIONS,
        "valid_observation_threshold_justification": (
            "Conservative statistical-support floor (n>=2 needed for a "
            "non-degenerate sample stdDev, +1 margin); NOT tuned against any "
            "specific experiment's downstream model performance."
        ),
        "final_nodata_value": STEP7_MODIS_NODATA_VALUE,
        "nodata_strategy": (
            "Explicit finite sentinel (not 0.0, which is a physically valid "
            "Celsius value): masked/no-observation pixels are unmask()'d with "
            "this sentinel in Earth Engine before download, then the same "
            "value is stamped as the GeoTIFF `nodata` tag after download "
            "(direct or per-tile) and propagated through tiled merge."
        ),
        "output_files": {
            "mean": str(mean_path),
            "std": str(std_path),
            "valid_observation_count": str(valid_count_path),
        },
        "output_hashes_sha256": {
            "mean": _sha256_file(mean_path),
            "std": _sha256_file(std_path),
            "valid_observation_count": _sha256_file(valid_count_path),
        },
        "raster_stats": {
            "mean": mean_stats,
            "std": std_stats,
            "valid_observation_count": count_stats,
        },
        "scale_meters": MODIS_EXPORT_SCALE,
        "crs": EXPORT_CRS,
        "export_transport": {
            "mean": mean_result["transport"],
            "std": std_result["transport"],
            "valid_observation_count": count_result["transport"],
        },
        "tile_grid": {
            "mean": list(mean_result["tile_grid"]) if mean_result["tile_grid"] else None,
            "std": list(std_result["tile_grid"]) if std_result["tile_grid"] else None,
            "valid_observation_count": (
                list(count_result["tile_grid"]) if count_result["tile_grid"] else None
            ),
        },
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "exported",
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    log.info("MODIS metadata yazıldı: %s", metadata_path)

    return {
        "status": "exported",
        "mean_path": str(mean_path), "std_path": str(std_path),
        "valid_count_path": str(valid_count_path),
        "metadata_path": str(metadata_path),
        "mean_transport": mean_result["transport"], "std_transport": std_result["transport"],
        "count_transport": count_result["transport"],
    }


def _log_dry_run(ctx: dict, paths: dict) -> None:
    log.info("[dry-run] experiment_id: %s", ctx["experiment_id"])
    log.info("[dry-run] region_key: %s", ctx["region_key"])
    log.info(
        "[dry-run] predictor window (MODIS mean/std bu pencere için hesaplanacak): %s -> %s",
        ctx["predictor_start_date"], ctx["predictor_end_date"],
    )
    log.info("[dry-run] Planlanan MODIS çıktı dizini: %s", paths["modis_dir"])
    log.info("  %s %s", "[VAR]" if paths["mean_path"].exists() else "[EKSİK]", paths["mean_path"])
    log.info("  %s %s", "[VAR]" if paths["std_path"].exists() else "[EKSİK]", paths["std_path"])
    log.info(
        "  %s %s", "[VAR]" if paths["valid_count_path"].exists() else "[EKSİK]",
        paths["valid_count_path"],
    )
    log.info(
        "  %s %s", "[VAR]" if paths["metadata_path"].exists() else "[EKSİK]", paths["metadata_path"],
    )
    log.info("[dry-run] Hiçbir GEE export/dosya yazma ÇALIŞTIRILMADI.")


def main(experiment_id: str = "manavgat_2021", dry_run: bool = False, export: bool = False, force: bool = False) -> dict:
    ctx = build_experiment_context(experiment_id)
    log_context_summary(ctx, log)

    if ctx["is_kozan"]:
        log.warning(
            "'%s' Kozan'dır -- bu script Kozan-dışı deneyler için tasarlanmıştır "
            "(Kozan kendi legacy MODIS hazırlığını scripts/main.py -> "
            "src/step2_modis_5year_mean.py üzerinden yapar). Yine de devam "
            "ediliyor, ancak çıktılar legacy data/modis/'a gidecektir.",
            experiment_id,
        )

    paths = resolve_modis_output_paths(ctx)
    if not ctx["is_kozan"]:
        _assert_paths_are_safely_namespaced(ctx, paths)

    if dry_run:
        _log_dry_run(ctx, paths)
        return {"experiment_id": experiment_id, "ran": False, "reason": "dry_run"}

    if not export:
        raise ModisPrepError(
            "Ne --export ne --dry-run verildi; hangi modda çalışılacağı belirsiz."
        )

    result = prepare_modis_for_step7(ctx, force=force)
    log.info("TAMAMLANDI: %s", result)
    return {"experiment_id": experiment_id, "ran": True, "result": result}


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Step0F: Step7 downscaling için gerekli MODIS LST "
        "mean/std girdisini, Kozan-dışı bir deney için (namespaced) "
        "hazırlar. Step7B/7C/7D/7E'yi ÇALIŞTIRMAZ, Step8'i ÇALIŞTIRMAZ, "
        "model EĞİTMEZ."
    )
    parser.add_argument("--experiment", type=str, default="manavgat_2021")
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Hiçbir şey çalıştırma; planlanan MODIS çıktı yollarını + var/yok durumunu bas.",
    )
    parser.add_argument(
        "--export", action="store_true",
        help="MODIS LST mean/std'yi GEE'den export eder ve metadata yazar.",
    )
    parser.add_argument(
        "--force", action="store_true",
        help="MODIS çıktıları zaten varsa üzerine yaz.",
    )
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    main(
        experiment_id=args.experiment,
        dry_run=args.dry_run,
        export=args.export,
        force=args.force,
    )
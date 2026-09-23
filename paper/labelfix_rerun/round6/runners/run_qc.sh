#!/bin/bash
# QC arm on the corrected label (refreeze/_qc_manavgat, repo 6381f4c unchanged). Two arms rebuilt in the same tree,
# same code and environment; only the MODIS input differs.
#   A: unscreened MODIS -> FROZEN step7d/7e (repo HEAD's step7B refuses the unscreened raster: no nodata tag, 8.1 %
#      exact zeros, guard added 2026-07-23 in 4745230) -> step8 on the corrected label = the OFFICIAL re-freeze
#      outputs. This matches what the 2026-08-14 arm A was: its step7 hit the same guard, and step8 ran on the staged
#      frozen step7d/7e; its signed AUCs equal the frozen ones. Arm A therefore carries the export-time step7 code,
#      arm B the HEAD step7 code. That confound was present, undescribed, on 2026-08-14 too.
#   B: screened MODIS (pipeline's prepare_modis_for_step7 --export, EE project thermaltwin) -> step7 -> step8
RF=/c/Users/CORSAIR/projects/thermal-twin/refreeze; T=$RF/_qc_manavgat; W=$RF/_qc_work/manavgat_2021; L=$RF/_logs_qc; mkdir -p $W/armA $W/armB $L
source /c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix/_runners/_env.sh
export LOKY_MAX_CPU_COUNT=8 OMP_NUM_THREADS=8 MKL_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 PYTHONUNBUFFERED=1 PYTHONPATH=$T
st() { echo "$1 rc=$2 $(date +%H:%M:%S)" >> $L/status.txt; if [ "$2" != 0 ]; then echo "STOPPED at $1" >> $L/status.txt; exit 1; fi; }
M=$T/outputs/experiments/manavgat_2021
cd $T
[ -f $W/armA/step8a/step8a_500m_modeling_dataset.parquet ] || true
OFF=$RF/manavgat_2021/outputs/experiments/manavgat_2021
for s in step8a step8b step8c step8d step8e step7d step7e; do cp -r $OFF/$s $W/armA/; done; cp $OFF/data/modis/* $W/armA/; st A_captured_from_official 0
$PY $RF/_runners/modis_screened_export.py $T > $L/B_modis_export.log 2>&1; st B_modis_export $?
$PY $RF/_runners/qc_check_screened.py "$(cygpath -w $M/data/modis)" "$(cygpath -w /c/Users/CORSAIR/projects/thermal-twin/repo/outputs/experiments/manavgat_2021/data/modis)" >> $L/B_modis_export.log 2>&1; st B_screened_check $?
$PY -m scripts.run_step7_downscaling_only --experiment manavgat_2021 --force > $L/B_step7.log 2>&1; st B_step7 $?
$PY -m scripts.run_step8_modeling --experiment manavgat_2021 --force > $L/B_step8.log 2>&1; st B_step8 $?
for s in step8a step8b step8c step8d step8e step7d step7e; do cp -r $M/$s $W/armB/; done; cp $M/data/modis/* $W/armB/; st B_captured 0
st QC_DONE 0

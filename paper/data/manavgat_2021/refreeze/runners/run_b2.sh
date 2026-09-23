#!/usr/bin/env bash
# Stage B, second pass (one tree): copy the label-unaffected non-Manavgat Step9G reports from drive_new as INPUTS
# (8 v1 pair folders + integration_v2/bejis_2022__mugla_2021, as in the 2026-09-19 trees; the Manavgat v2
# integration report is not copied, so synthesis uses the regenerated v1), then synthesis x3 and the
# reproduction check. main.py exits 0 on failure, so its logs are also checked for "HATA".
source /c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix/_runners/_env.sh
export LOKY_MAX_CPU_COUNT=6 OMP_NUM_THREADS=6 MKL_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 PYTHONUNBUFFERED=1
TT=/c/Users/CORSAIR/projects/thermal-twin; RF=$TT/refreeze; T=$RF/$1; L=$RF/_logs_b/$1
st() { echo "$1 rc=$2 $(date +%H:%M:%S)" >> $L/status.txt; if [ "$2" != 0 ]; then echo "STOPPED at $1" >> $L/status.txt; exit 1; fi; }
ok() { [ "$1" = 0 ] && ! grep -q "HATA:" "$2" && echo 0 || echo 1; }
cd $T || exit 9
G=diagnostics/step9g_univariate_feature_auc_direction_reversal
for P in bejis_2022__evia_2021 bejis_2022__evia_2021_extended bejis_2022__mugla_2021 montiferru_2021__bejis_2022 montiferru_2021__evia_2021_extended montiferru_2021__mugla_2021 mugla_2021__evia_2021 mugla_2021__evia_2021_extended; do
  cp -r $TT/drive_new/$G/$P outputs/$G/ || st "copy step9g $P" 1
done
mkdir -p outputs/${G}_integration_v2 && cp -r $TT/drive_new/${G}_integration_v2/bejis_2022__mugla_2021 outputs/${G}_integration_v2/ || st "copy v2" 1
find outputs/diagnostics -name desktop.ini -delete; st copy_step9g_inputs 0
for SET in "bejis_2022 evia_2021_extended manavgat_2021 montiferru_2021 mugla_2021" "bejis_2022 evia_2021_extended manavgat_2021 mugla_2021" "bejis_2022 manavgat_2021 mugla_2021"; do
  A=""; for x in $SET; do A="$A --aoi $x"; done; N=$(echo $SET | wc -w)
  $PY scripts/main.py transfer-synthesis $A --force > $L/13_synthesis_$N.log 2>&1; st "synthesis $N-AOI" $(ok $? $L/13_synthesis_$N.log)
done
$PY scripts/run_reproduction_check.py > $L/20_reproduction_check.log 2>&1; st reproduction_check $?
st B_DONE 0

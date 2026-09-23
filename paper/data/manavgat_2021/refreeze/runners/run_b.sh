#!/usr/bin/env bash
# Stage B, one tree: (1) copy the 10 non-Manavgat pair folders from drive_new as INPUTS (label-unaffected,
# not rebuilt), (2) the 2026-09-19 post-processing (step9g x6, concept-shift-compare, 4-AOI decomposition,
# 5/4/3-AOI synthesis, burned-pattern audit), (3) scripts/run_reproduction_check.py.
# Usage: run_b.sh <tree_dir_name>
source /c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix/_runners/_env.sh
export LOKY_MAX_CPU_COUNT=6 OMP_NUM_THREADS=6 MKL_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 PYTHONUNBUFFERED=1
TT=/c/Users/CORSAIR/projects/thermal-twin; RF=$TT/refreeze; T=$RF/$1; L=$RF/_logs_b/$1; mkdir -p $L
st() { echo "$1 rc=$2 $(date +%H:%M:%S)" >> $L/status.txt; if [ "$2" != 0 ]; then echo "STOPPED at $1" >> $L/status.txt; exit 1; fi; }
cd $T || exit 9
for P in bejis_2022__evia_2021 bejis_2022__evia_2021_extended bejis_2022__mugla_2021 montiferru_2021__bejis_2022 montiferru_2021__evia_2021_extended montiferru_2021__mugla_2021 mugla_2021__bejis_2022 mugla_2021__evia_2021 mugla_2021__evia_2021_extended mugla_2021__mugla_2022_event_relative; do
  cp -r $TT/drive_new/cross_region/$P outputs/cross_region/ || st "copy $P" 1
done
find outputs/cross_region -name desktop.ini -delete; st copy_pairs 0
for P in manavgat_2021__bejis_2022 manavgat_2021__mugla_2021 manavgat_2021__evia_2021_extended mugla_2021__manavgat_2021 montiferru_2021__manavgat_2021 manavgat_2021__evia_2021; do
  S=${P%%__*}; G=${P##*__}
  $PY scripts/main.py concept-shift --source $S --target $G --force > $L/10_step9g_$P.log 2>&1; st "step9g $P" $?
done
$PY scripts/main.py concept-shift-compare --experiments bejis_2022 manavgat_2021 mugla_2021 --force > $L/11_compare.log 2>&1; st concept-shift-compare $?
$PY scripts/main.py transfer-decomposition --aoi bejis_2022 --aoi evia_2021_extended --aoi manavgat_2021 --aoi mugla_2021 --force > $L/12_decomp.log 2>&1; st transfer-decomposition $?
for SET in "bejis_2022 evia_2021_extended manavgat_2021 montiferru_2021 mugla_2021" "bejis_2022 evia_2021_extended manavgat_2021 mugla_2021" "bejis_2022 manavgat_2021 mugla_2021"; do
  A=""; for x in $SET; do A="$A --aoi $x"; done
  $PY scripts/main.py transfer-synthesis $A --force > $L/13_synthesis_$(echo $SET | wc -w).log 2>&1; st "synthesis $(echo $SET | wc -w)-AOI" $?
done
$PY scripts/run_burned_pattern_audit.py --all-enabled --scope "" --force > $L/14_bpa.json 2> $L/14_bpa.log; st burned-pattern-audit $?
$PY scripts/run_reproduction_check.py > $L/20_reproduction_check.log 2>&1; st reproduction_check $?
st B_DONE 0

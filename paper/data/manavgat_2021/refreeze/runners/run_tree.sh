#!/usr/bin/env bash
# Stage A, one tree end to end. Usage: run_tree.sh <tree_dir_name> <official|control>
source /c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix/_runners/_env.sh
export LOKY_MAX_CPU_COUNT=6 OMP_NUM_THREADS=6 MKL_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 PYTHONUNBUFFERED=1
RF=/c/Users/CORSAIR/projects/thermal-twin/refreeze; T=$RF/$1; L=$RF/_logs/$1; mkdir -p $L
st() { echo "$1 rc=$2 $(date +%H:%M:%S)" >> $L/status.txt; if [ "$2" != 0 ]; then echo "STOPPED at $1" >> $L/status.txt; exit 1; fi; }
cd $T || exit 9
if [ "$2" = official ]; then $PY $RF/_runners/step6_label.py $T > $L/01_step6_label.log 2>&1; st step6_label $?; fi
# Gate WITHOUT --force: Step6A then reuses the existing (frozen, label-free) gate inputs and never calls EE.
# The control arm drops its copied frozen gate files first, so its gate is recomputed and G1-checked.
if [ "$2" = control ]; then rm -f outputs/experiments/manavgat_2021/validation/labels/burned_landcover_gate.*; fi
$PY scripts/run_label_gate_only.py --experiment manavgat_2021 --skip-export > $L/02_gate.log 2>&1; st gate $?
$PY scripts/run_step8_modeling.py --experiment manavgat_2021 --force > $L/03_step8.log 2>&1; st step8a-e $?
$PY $RF/_runners/bigblock.py $T > $L/04_bigblock.log 2>&1; st bigblock $?
$PY $RF/_runners/largeblock.py $T > $L/05_largeblock.log 2>&1; st largeblock $?
for P in manavgat_2021__bejis_2022 manavgat_2021__mugla_2021 manavgat_2021__evia_2021_extended mugla_2021__manavgat_2021 montiferru_2021__manavgat_2021 manavgat_2021__evia_2021; do
  S=${P%%__*}; G=${P##*__}
  $PY scripts/run_cross_region_transfer.py --source $S --target $G --reverse --force > $L/06_${P}_step9.log 2>&1; st "step9a-d $P" $?
  $PY scripts/run_cross_region_shift_audit.py --source $S --target $G --force > $L/07_${P}_step9e.log 2>&1; st "step9e $P" $?
  $PY scripts/run_step10_self_calibrated_transfer.py --source $S --target $G --reverse --force --bootstrap-replicates 1000 --seed 42 > $L/08_${P}_step10.log 2>&1; st "step10 $P" $?
done
st TREE_DONE 0

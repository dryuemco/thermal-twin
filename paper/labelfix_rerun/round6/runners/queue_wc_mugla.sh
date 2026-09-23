#!/bin/bash
# Round 6 runs on both re-freeze trees: window closure (patched module; two phases as in round 3b) and Muğla subsampling.
RF=/c/Users/CORSAIR/projects/thermal-twin/refreeze; L=$RF/_logs_r6; mkdir -p $L
source /c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix/_runners/_env.sh
export LOKY_MAX_CPU_COUNT=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 PYTHONUNBUFFERED=1
wc() { (cd $1/ && $PY $RF/_runners/wc_driver.py "$1\\" $2 plan predictor-export > $L/wc_${2}_a.log 2>&1 && $PY $RF/_runners/wc_driver.py "$1\\" $2 local-downstream compare noresume > $L/wc_${2}_b.log 2>&1; echo "wc_$2 rc=$?" >> $L/status.txt); }
mg() { (cd $RF/$1 && $PY $RF/_runners/mugla_driver.py . > $L/mugla_$2.log 2>&1; echo "mugla_$2 rc=$?" >> $L/status.txt); }
wc R: official & wc S: control & mg manavgat_2021 official & mg _control_frozenlabel control & wait
echo R6_DONE >> $L/status.txt

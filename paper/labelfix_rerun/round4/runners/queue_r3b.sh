#!/bin/bash
# Round 3b: re-run the two jobs that did not complete on 2026-09-19 (window closure: path-portability failure;
# few-shot recovery: no output). Two chains in parallel, corrected tree (P:) first, then control (Q:).
RL=/c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix; L=$RL/_round3/logs/r3b
source $RL/_runners/_env.sh; export LOKY_MAX_CPU_COUNT=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 PYTHONUNBUFFERED=1
wc() { (cd $1/ && $PY $RL/_round3/runners/wc_driver.py "$1\\" $2 plan compare > $L/wc_$2.log 2>&1; echo "wc_$2 rc=$?" >> $L/status.txt); }
fs() { (bash $RL/_round3/runners/fsr.sh $1 $2 > $L/fsr_$2.log 2>&1; echo "fsr_$2 rc=$?" >> $L/status.txt); }
( wc P: corrected; wc Q: control ) &
( fs P: corrected; fs Q: control ) &
wait; echo R3B_DONE >> $L/status.txt

#!/bin/bash
# Round 3b window closure: reuse the completed plan..predictor-export stages (resume), then run
# local-downstream..compare fresh (no downstream exists yet, so --resume refuses by design).
RL=/c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix; L=$RL/_round3/logs/r3b
source $RL/_runners/_env.sh; export LOKY_MAX_CPU_COUNT=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 PYTHONUNBUFFERED=1
wc() { (cd $1/ && $PY $RL/_round3/runners/wc_driver.py "$1\\" $2 plan predictor-export > $L/wc_$2_a.log 2>&1 \
        && $PY $RL/_round3/runners/wc_driver.py "$1\\" $2 local-downstream compare noresume > $L/wc_$2_b.log 2>&1; echo "wc_$2 rc=$?" >> $L/status.txt); }
wc P: corrected; wc Q: control; echo WC_DONE >> $L/status.txt

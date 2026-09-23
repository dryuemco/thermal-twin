#!/usr/bin/env bash
# Few-shot recovery, round 3. $1 = P: (corrected tree via subst) or Q: (control tree via subst); $2 = arm
source /c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix/_runners/_env.sh
export LOKY_MAX_CPU_COUNT=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
cd "$1/" && $PY /c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix/_round3/runners/fsr_driver.py "$1\\" $2

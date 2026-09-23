#!/bin/bash
# Round 4: step8d (thermal ablation) for Manavgat in both trees, then the step8e report regenerated.
RL=/c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix; L=$RL/_round4/logs; mkdir -p $L
source $RL/_runners/_env.sh; export LOKY_MAX_CPU_COUNT=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4 PYTHONUNBUFFERED=1
one() { (cd $RL/$1 && $PY $RL/_round4/step8d.py $RL/$1 manavgat_2021 > $L/step8d_$1.log 2>&1; echo "step8d_$1 rc=$?" >> $L/status.txt
         $PY scripts/run_step8_modeling.py --experiment manavgat_2021 --report-only > $L/step8e_$1.log 2>&1; echo "step8e_$1 rc=$?" >> $L/status.txt); }
one control & one pipeline & wait; echo STEP8D_QUEUE_DONE >> $L/status.txt

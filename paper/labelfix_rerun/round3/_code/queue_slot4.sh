#!/bin/bash
# Round 3, job slot 4: waits for anomaly_only, then runs task-2 chain, feature_drop, step8e report-only
# (both trees), run_d. Sequential: one job at a time in this slot.
T=/c/Users/CORSAIR/projects/thermal-twin-main; O=$T/paper/labelfix_rerun/round3; R=$O/_code/run_one.sh
RL=/c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix
until grep -q "^anomaly_only rc=" $O/_logs/status.txt 2>/dev/null; do sleep 20; done
bash $O/_code/chain_task2.sh
bash $R "feature_drop|$T|paper/feature_drop.py $RL/_round3/stage_fd $O/_staging/staging/feature_drop.json"
source $RL/_runners/_env.sh
for TR in control pipeline; do
  (cd $RL/$TR && $PY scripts/run_step8_modeling.py --experiment manavgat_2021 --report-only > $RL/_round3/logs/step8e_$TR.log 2>&1; echo "step8e_report_only_$TR rc=$?" >> $O/_logs/status.txt)
done
X=$RL/_round3/step10_exp; mkdir -p $X/manavgat_2021/step8e $X/bejis_2022/step8e
cp $RL/pipeline/outputs/experiments/manavgat_2021/step8e/final_step8_report.json $X/manavgat_2021/step8e/
cp $T/experiments/bejis_2022/step8e/final_step8_report.json $X/bejis_2022/step8e/
bash $R "run_d_within_robustness|$T/step10|$O/_code/run_d_driver.py $X"
echo QUEUE_SLOT4_DONE >> $O/_logs/status.txt

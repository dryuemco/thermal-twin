#!/bin/bash
# Round 4, jobs 3-7 of PLAN_R4.md: the round-3 slot-4 queue verbatim, minus its wait (it waited for an
# "anomaly_only rc=" line in round3/_logs/status.txt that was never written; anomaly_only did complete).
T=/c/Users/CORSAIR/projects/thermal-twin-main; O=$T/paper/labelfix_rerun/round3; R=$O/_code/run_one.sh
RL=/c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix
bash $O/_code/chain_task2.sh
bash $R "feature_drop|$T|paper/feature_drop.py $RL/_round3/stage_fd $O/_staging/staging/feature_drop.json"
source $RL/_runners/_env.sh
for TR in control pipeline; do
  (cd $RL/$TR && $PY scripts/run_step8_modeling.py --experiment manavgat_2021 --report-only > $RL/_round3/logs/step8e_$TR.log 2>&1; echo "step8e_report_only_$TR rc=$?" >> $O/_logs/status.txt)
done
X=$RL/_round3/step10_exp; mkdir -p $X/manavgat_2021/step8e $X/bejis_2022/step8e
cp $RL/pipeline/outputs/experiments/manavgat_2021/step8e/final_step8_report.json $X/manavgat_2021/step8e/
cp $T/experiments/bejis_2022/step8e/final_step8_report.json $X/bejis_2022/step8e/
bash $O/_code/run_one.sh "run_d_within_robustness|$T/step10|$O/_code/run_d_driver.py $X"
echo QUEUE_R4_PAPER_DONE >> $O/_logs/status.txt

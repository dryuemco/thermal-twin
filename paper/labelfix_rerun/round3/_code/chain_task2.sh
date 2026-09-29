#!/bin/bash
# Round 3, task 2 chain (one job slot, sequential). Inputs: class-A artefacts (labelfix_rerun/code) + round-3
# B->M aggregates, merged in round3/_inputs. The two collar scripts read the hard-coded relative path
# paper/baseline_vs_thermal_transfer.csv, so they run with cwd = the round-3 overlay root whose paper/ is a
# junction to round3/ (no code edit), and PAPER_ARTEFACTS given as an absolute path.
R=/c/Users/CORSAIR/projects/thermal-twin-main/paper/labelfix_rerun/round3/_code/run_one.sh
T=/c/Users/CORSAIR/projects/thermal-twin-main
O=$T/paper/labelfix_rerun/round3
OV=/c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix/_round3/root
bash $R "distance_curve|$T|paper/code/distance_curve.py paper/labelfix_rerun/round3/_staging paper/labelfix_rerun/round3/distance_curve.json"
PAPER_ARTEFACTS=$O/_inputs bash $R "verify_diag_collar|$OV|$T/paper/code/verify_diag_collar.py $O/diagnostics_collar_frame.csv"
PAPER_ARTEFACTS=$O/_inputs bash $R "verify_collar_increment|$OV|$T/paper/code/verify_collar_increment.py $O/collar_increment_and_cosine.csv"
bash $R "ems_inference_units|$T/paper/code|ems_inference_units.py"
bash $R "ems_inference_equivalence|$T/paper/code|ems_inference_equivalence.py"
bash $R "ems_inference_multiplicity|$T/paper/code|ems_inference_multiplicity.py"
echo CHAIN_TASK2_DONE >> $O/_logs/status.txt

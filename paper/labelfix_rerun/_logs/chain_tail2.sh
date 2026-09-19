#!/bin/bash
L=/c/Users/CORSAIR/projects/thermal-twin-main/paper/labelfix_rerun/_logs
until grep -q "^ems_inference_equivalence" $L/status.txt; do sleep 5; done
bash $L/run_one.sh "labels_6_calibration|/c/Users/CORSAIR/projects/thermal-twin-main/paper/code|ems_labels_6_calibration.py"

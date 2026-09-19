#!/bin/bash
L=/c/Users/CORSAIR/projects/thermal-twin-main/paper/labelfix_rerun/_logs
until grep -q "^multiplicity_reversal" $L/status.txt; do sleep 5; done
PYTHONIOENCODING=utf-8 bash $L/run_one.sh "run_e_coral_lambda|/c/Users/CORSAIR/projects/thermal-twin-main/step10|$L/run_e_driver.py"

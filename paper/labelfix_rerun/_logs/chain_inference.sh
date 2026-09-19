#!/bin/bash
for s in ladder_stats units equivalence; do
  bash /c/Users/CORSAIR/projects/thermal-twin-main/paper/labelfix_rerun/_logs/run_one.sh "ems_inference_$s|/c/Users/CORSAIR/projects/thermal-twin-main/paper/code|ems_inference_$s.py"
done

#!/bin/bash
for s in 0_reproduce 1_bands 2_placebo 3_farfield 4_labelfree 5_metrics; do
  bash /c/Users/CORSAIR/projects/thermal-twin-main/paper/labelfix_rerun/_logs/run_one.sh "ems_geometry_$s|/c/Users/CORSAIR/projects/thermal-twin-main/paper/code|ems_geometry_$s.py"
done

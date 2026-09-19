#!/bin/bash
# usage: run_one.sh "<name>|<cwd>|<python args>"   (labelfix re-run, corrected Manavgat labels)
IFS='|' read -r name wd args <<< "$1"
T=/c/Users/CORSAIR/projects/thermal-twin-main
L=$T/paper/labelfix_rerun/_logs
export PAPER_ARTEFACTS=paper/labelfix_rerun/code EMS_OUT_ROOT=paper/labelfix_rerun \
       STEP10_OUT_DIR=$T/paper/labelfix_rerun/step10 THERMAL_TWIN_LABELS=corrected \
       PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
cd "$wd" || exit 9
t0=$(date +%s)
/c/Users/CORSAIR/projects/thermal-twin/.venv-step10/Scripts/python.exe $args > "$L/$name.log" 2>&1
rc=$?
echo "$name rc=$rc $(( $(date +%s) - t0 ))s" >> "$L/status.txt"

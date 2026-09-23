#!/bin/bash
# usage: run_one.sh "<name>|<cwd>|<python args>"   (round 3: corrected Manavgat labels, round-3 B inputs)
# PAPER_ARTEFACTS defaults to round3/_inputs (class-A artefacts of labelfix_rerun/code + round-3 B->M
# aggregates), relative to the tree root as ems_*_common expect; callers may preset an absolute path.
IFS='|' read -r name wd args <<< "$1"
T=/c/Users/CORSAIR/projects/thermal-twin-main
L=$T/paper/labelfix_rerun/round3/_logs
export PAPER_ARTEFACTS=${PAPER_ARTEFACTS:-paper/labelfix_rerun/round3/_inputs} EMS_OUT_ROOT=paper/labelfix_rerun/round3 \
       STEP10_OUT_DIR=$T/paper/labelfix_rerun/round3/step10 THERMAL_TWIN_LABELS=corrected \
       PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PYTHONIOENCODING=utf-8 \
       LOKY_MAX_CPU_COUNT=4 OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 OPENBLAS_NUM_THREADS=4
cd "$wd" || exit 9
t0=$(date +%s)
/c/Users/CORSAIR/projects/thermal-twin/.venv-step10/Scripts/python.exe $args > "$L/$name.log" 2>&1
rc=$?
echo "$name rc=$rc $(( $(date +%s) - t0 ))s" >> "$L/status.txt"

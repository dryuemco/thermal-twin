#!/bin/bash
# usage: run_one.sh <script> [args...]; run from the worktree root
cd /c/Users/CORSAIR/projects/thermal-twin-main
s=$1; shift
export PAPER_ARTEFACTS=paper/canonical_rerun PYTHONUNBUFFERED=1
t0=$(date +%s)
/c/Users/CORSAIR/projects/thermal-twin/.venv-step10/Scripts/python.exe paper/code/$s.py "$@" > paper/canonical_rerun/_logs/$s.log 2>&1
rc=$?
echo "$s rc=$rc $(( $(date +%s) - t0 ))s" >> paper/canonical_rerun/_logs/status.txt

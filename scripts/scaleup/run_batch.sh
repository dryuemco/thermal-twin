#!/usr/bin/env bash
# run_batch.sh: official scale-up run. Runs the pipeline of one clone (branch scaleup-31fires) for a list of
# experiments, one after another, and records the wall time of every step. A failure in one fire does not
# stop the batch. Same step order as the pilot (scratch/pilot_scaleup/run_batch.sh); the two preparation
# scripts are not called by the stage chain and run before step7.
# Usage: bash run_batch.sh <clone folder under D:/ThermalTwin/scaleup> id1 id2 ...
set -u
ROOT="/d/ThermalTwin/scaleup"
CLONE=$1; shift
cd "$ROOT/$CLONE"
PY="/c/Users/CORSAIR/projects/ThermalTwin/thermal-twin/.venv-step10/Scripts/python.exe"
export GEE_PROJECT=thermaltwin
mkdir -p "$ROOT/batch_logs"
SUMMARY="$ROOT/batch_times.csv"
[ -f "$SUMMARY" ] || echo "experiment,step,seconds,exit_code,finished,clone,commit" > "$SUMMARY"
COMMIT=$(git rev-parse --short HEAD)
for EXP in "$@"; do
  LOG="$ROOT/batch_logs/$EXP.log"
  : > "$LOG"
  echo "clone $CLONE commit $COMMIT GEE_PROJECT=$GEE_PROJECT started $(date '+%F %T')" >> "$LOG"
  ok=1
  step() {  # name, command...
    name=$1; shift
    start=$(date +%s)
    echo "===== $name started $(date +%H:%M:%S) =====" >> "$LOG"
    PYTHONIOENCODING=utf-8 "$@" >> "$LOG" 2>&1
    code=$?
    echo "$EXP,$name,$(( $(date +%s) - start )),$code,$(date '+%F %T'),$CLONE,$COMMIT" >> "$SUMMARY"
    return $code
  }
  stage() { step "$1" "$PY" scripts/main.py experiment --experiment "$EXP" --from-stage "$1" --to-stage "$1" --predictor-mode export ${2:-}; }
  stage gate --export-labels || ok=0
  [ $ok = 1 ] && { stage predictors || ok=0; }
  [ $ok = 1 ] && { stage scene-provenance || ok=0; }
  [ $ok = 1 ] && { step prepare_dem "$PY" scripts/prepare_dem_for_experiment.py --experiment "$EXP" --export || ok=0; }
  [ $ok = 1 ] && { step prepare_modis "$PY" scripts/prepare_modis_for_step7.py --experiment "$EXP" --export || ok=0; }
  [ $ok = 1 ] && { stage step7 || ok=0; }
  [ $ok = 1 ] && { stage seam-audit; stage seam-localization; stage step8 || ok=0; }
  echo "$EXP,ALL,0,$((1-ok)),$(date '+%F %T'),$CLONE,$COMMIT" >> "$SUMMARY"
done
echo "worker $CLONE finished $(date '+%F %T')"; grep ",ALL," "$SUMMARY"

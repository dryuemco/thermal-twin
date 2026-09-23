#!/usr/bin/env bash
# S6/S7 aggregator chain on one overlay, in the round-3 order, unchanged round-3 code.
# Usage: run_s6_chain.sh <official|control> <AOA_ID> <niche_measures.json>
set -u
R5=/c/Users/CORSAIR/projects/thermal-twin/rerun_labelfix/_round5; C=${CODE_DIR:-/c/Users/CORSAIR/projects/thermal-twin-main/paper/labelfix_rerun/round3/_code}
PY=/c/Users/CORSAIR/projects/thermal-twin/.venv-step10/Scripts/python.exe
A=$1; export R3ROOT=$R5/ov_$A; O=$R5/out_$A; L=$O/logs; mkdir -p $L $O/stage/staging; cp "$3" $O/stage/staging/niche_measures.json
st() { echo "$1 rc=$2" >> $L/status.txt; [ "$2" = 0 ] || { echo "STOPPED at $1" >> $L/status.txt; exit 1; }; }
cd $O
$PY $C/burned_components.py > $L/burned_components.log 2>&1; st burned_components $?
node $C/conditional_similarity.mjs > $L/conditional_similarity.log 2>&1; st conditional_similarity $?
$PY $C/build_comparison_inputs.py $O/stage/staging > $L/build_comparison_inputs.log 2>&1; st build_comparison_inputs $?
AOA_ID=$2 node $C/regime_correlation.mjs > $L/regime_correlation.log 2>&1; st regime_correlation $?
node $C/niche_corr.mjs $O/stage > $L/niche_corr.log 2>&1; st niche_corr $?
node $C/niche_vs_conditional.mjs > $L/niche_vs_conditional.log 2>&1; st niche_vs_conditional $?
node $C/diagnostics_common_subset.mjs > $L/diagnostics_common_subset.log 2>&1; st diagnostics_common_subset $?
st CHAIN_DONE 0

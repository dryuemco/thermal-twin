#!/usr/bin/env bash
# Stage A: build the two re-freeze trees from repo HEAD (6381f4c) and drive_new inputs.
#   manavgat_2021        = OFFICIAL corrected-label tree (label re-exported by the pipeline's step6)
#   _control_frozenlabel = control arm, frozen Manavgat label (G1)
# Nothing is written to repo/ or drive_new/. Manavgat-dependent outputs are NOT copied: they are rebuilt.
set -euo pipefail
TT=/c/Users/CORSAIR/projects/thermal-twin; DN=$TT/drive_new; RF=$TT/refreeze
test "$(git -C $TT/repo rev-parse HEAD)" = "6381f4cd752d77a3069fcaa2364d10109b5adaf7"
test -z "$(git -C $TT/repo status --porcelain)"
for T in manavgat_2021 _control_frozenlabel; do
  D=$RF/$T; rm -rf $D; mkdir -p $D/outputs/experiments $D/outputs/cross_region
  cp -r $TT/repo/core $TT/repo/src $TT/repo/scripts $TT/repo/config $D/
  git -C $TT/repo rev-parse HEAD > $D/REPO_COMMIT.txt
  for R in bejis_2022 evia_2021 evia_2021_extended montiferru_2021 mugla_2021; do
    mkdir -p $D/outputs/experiments/$R
    for s in gate_inputs predictor_export_metadata.json step0 step7e step8a step8b step8c step8e validation robustness qa; do
      [ -e $DN/experiments/$R/$s ] && cp -r $DN/experiments/$R/$s $D/outputs/experiments/$R/
    done
  done
  M=$D/outputs/experiments/manavgat_2021; mkdir -p $M
  for s in data gate_inputs validation step0 step5 step5b step5c step7d step7e predictor_export_metadata.json; do cp -r $DN/experiments/manavgat_2021/$s $M/; done
  find $D -name desktop.ini -delete; find $D -name __pycache__ -type d -prune -exec rm -rf {} +
done
# official tree: remove the frozen label + gate so they can only come from the pipeline's own re-export
L=$RF/manavgat_2021/outputs/experiments/manavgat_2021/validation/labels
rm -f $L/mcd64a1_raw.tif $L/mcd64a1_burned.tif $L/*.aux.xml $L/burned_landcover_gate.*
echo BUILD_DONE

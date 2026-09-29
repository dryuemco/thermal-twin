# Manavgat 2021 re-freeze on the corrected label (stage A, 2026-09-23)

The official Manavgat outputs now come from this re-freeze, not from the frozen drive_new export.
Start with `REFREEZE_MANIFEST.md`; it carries the provenance sentence for Methods.

- `REFREEZE_MANIFEST.{md,json}`: provenance (repo `6381f4c`; original export 2026-07-08; fix `183be42`,
  2026-07-11), GEE project, environment, 80-column schema and hash note, gate note, control-arm G1.
- `SHA256SUMS.txt`: 365 output files of the official tree, paths relative to the tree root.
- `runners/`: exactly what was run (`build_trees.sh`, then `run_tree.sh` per tree).
- `checks/`: the G1 record and the 8-direction matrices (official, control, frozen).
- `logs/`: per-step logs and status for both arms.
- `audit/`: G3 path/size/mtime listings of `repo/` and `drive_new/`, before and after. 0 differences.

The output tree itself (`thermal-twin/refreeze/manavgat_2021/`, about 1.3 GB including copied inputs) is
not in git. Verify it with `sha256sum -c SHA256SUMS.txt` from the tree root.

# Label-fix re-run, round 4 (2026-09-22/23)

Round 4 of the Manavgat label-correction re-run. It finishes the jobs that rounds 1–3 (2026-09-19) left
unrun or unchecked, and records the user's decisions on the jobs that are blocked.

- `PLAN_R4.md`: the jobs and the gates G1–G6.
- `REPORT.md`: every job's gate result, what moved from frozen to corrected, and the decisions.
- `ANSWERS.md`: answers to S1–S3 (label defect and scope, contrast pair, six-direction few-shot table).
- `checkers/`: G1 (control reproduces frozen) and G2 (non-Manavgat rows unchanged).
- `runners/`: drivers and queues as run.
- `logs/`: run logs.
- `tdci/`: transfer_delta_ci re-run against the regenerated step9b.
- `audit/`: G3 path/size/mtime listings of `repo/` and `drive_new/`, taken before, during and after the run.

Scratch trees (`thermal-twin/rerun_labelfix/{pipeline,control}`) are not versioned. The pipeline-side
outputs cited here live there until the Manavgat re-freeze (stage A) makes them official outputs.

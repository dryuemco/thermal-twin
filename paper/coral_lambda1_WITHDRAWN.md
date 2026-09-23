# `coral_lambda1.csv`: WITHDRAWN 2026-09-23

Appendix A(b) quoted a λ = 1 CORAL arm on four directions (thermal mean 0.519 → 0.522; values
0.510 / 0.444 / 0.559 / 0.575 against λ = 0.1). The values come from `coral_lambda1.csv`. **No script in
the project produces that file**: the Manavgat re-run audit (`MANAVGAT_RERUN_PLAN.md`, row 80) found none,
and `observational_sensitivities.md` only names it. A value whose producer cannot be run has no
verifiable source, so it is withdrawn under both labels, frozen and corrected. It is not re-specified.

Appendix A(b) is limited to the λ ≤ 0.1 sweep, which Methods already describes. That sweep comes from
the pipeline's `coral_lambda_sensitivity` (λ grid up to 0.1, re-run on the corrected label; control arm =
drive_new, round 4 N4) and from `step10/run_e_coral_lambda_sensitivity.py`.

The file is kept unchanged as the historical record and must not be cited. User decision, 2026-09-23.

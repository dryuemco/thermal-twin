"""S6: the 20 pre-fixed transfer diagnostics (all_diagnostics_vs_transfer.csv), frozen (control arm, = 09-19 frozen
arm exactly) vs corrected (official). No measure added.
vector_spearman_supported is one of the 20 pre-fixed candidates (conditional family). A fixed candidate cannot be
removed after its result is seen, so it STAYS IN THE TABLE, flagged (user decision 2026-09-23, reversing an earlier
instruction to drop it). Frozen: 2 directions, not computable. Corrected: 6 directions, rho 0.956, degenerate
interval (upper bound = point estimate): not interpreted and not comparable with the other 19."""
import pandas as pd
from pathlib import Path
R5 = Path(__file__).parent
o = pd.read_csv(R5 / "out_official/all_diagnostics_vs_transfer.csv"); c = pd.read_csv(R5 / "out_control/all_diagnostics_vs_transfer.csv")
m = c.merge(o, on=["measure", "side", "expected_sign"], suffixes=("_frozen", "_corrected"))
assert len(m) == 20
m.to_csv(R5 / "s6_diagnostics_20.csv", index=False)
L = ["| Measure | Family | n (frozen → corrected) | rho frozen [95% CI] | rho corrected [95% CI] | CI excludes 0 (frozen → corrected) |", "|---|---|---|---|---|---|"]
for _, r in m.iterrows():
    L.append(f"| {r.measure} | {r.side} | {r.n_directions_frozen} → {r.n_directions_corrected} | {r.spearman_rho_frozen:+.3f} [{r.spearman_ci_low_frozen:+.3f}, {r.spearman_ci_high_frozen:+.3f}] | "
             f"{r.spearman_rho_corrected:+.3f} [{r.spearman_ci_low_corrected:+.3f}, {r.spearman_ci_high_corrected:+.3f}] | {r.ci_excludes_zero_frozen} → {r.ci_excludes_zero_corrected} |"
             + (" ‡" if r.measure == "vector_spearman_supported" else ""))
L += ["", "‡ vector_spearman_supported: 6 directions, degenerate interval (upper bound = point estimate); not interpreted, "
      "not comparable with the other 19 measures. Frozen label: 2 directions, not computable. It is a member of the fixed "
      "candidate set and stays in the table."]
L = [x.replace("+nan [+nan, +nan]", "not computable") for x in L]
(R5 / "s6_diagnostics_20.md").write_text("\n".join(L) + "\n", encoding="utf-8")
print("\n".join(L))
k = m[m.measure != "vector_spearman_supported"]
print("of the 19 interpretable, CI excluding zero: frozen", int(k.ci_excludes_zero_frozen.sum()), "corrected", int(k.ci_excludes_zero_corrected.sum()))

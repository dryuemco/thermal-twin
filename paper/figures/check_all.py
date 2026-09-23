#!/usr/bin/env python3
"""Run every figure script's asserts and layout check in one command; print one report.

This is the last check before submission. Each script is run as it is built (its asserts tie
every printed number to the manuscript text, its layout check enforces the 8 pt minimum and
the minimum text gap), and the report gives, per figure: PASS / FAIL / SKIPPED, the number of
assert statements, the layout problems, the minimum gap and the minimum font size.

The scripts write their PDF/SVG/PNG/TIFF and provenance files as a side effect. A check must
not change the committed figures, so every non-.py file in this directory is snapshotted before
the run and written back byte for byte afterwards (files the run creates are removed). The
report says how many output files a run touched, so a script that stopped writing is visible.

Fig. 1 needs cartopy, which the project venv does not have. It runs in the WSL environment
that built it (default: Ubuntu-22.04, /home/yunus/mm-thermal/bin/python; override with
--fig1-wsl-distro / --fig1-python). If that environment is not available the row reads
"SKIPPED: cartopy env not available" and the exit status says so; it is never passed silently.

Usage (from the repository root or from paper/figures):
    python paper/figures/check_all.py            # all ten
    python paper/figures/check_all.py --only fig4_transfer_matrix graphical_abstract
    python paper/figures/check_all.py --skip-fig1
Exit status: 0 all PASS; 1 any FAIL; 2 no FAIL but something SKIPPED.
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCRIPTS = ["fig1_study_map", "fig2_schematic", "fig3_within_robustness", "fig4_transfer_matrix",
           "fig5_adaptation", "fig6_loro", "fig7_feature_drop", "fig8_contrast_pairs",
           "graphical_abstract"]
SHARED = {"fig5_adaptation", "fig6_loro", "fig7_feature_drop"}     # also run _conservation_common


def n_asserts(name):
    src = (HERE / f"{name}.py").read_text(encoding="utf-8")
    n = len(re.findall(r"^\s*assert\b", src, re.M)) + len(re.findall(r"\bassert_inside\(", src))
    if name in SHARED:
        n += len(re.findall(r"^\s*assert\b", (HERE / "_conservation_common.py").read_text(encoding="utf-8"), re.M))
    return n


def snapshot():
    return {p: p.read_bytes() for p in HERE.iterdir()
            if p.is_file() and p.suffix != ".py" and not p.name.startswith(".")}


def restore(before):
    touched = 0
    for p in list(HERE.iterdir()):
        if not p.is_file() or p.suffix == ".py" or p.name.startswith("."):
            continue
        if p not in before:
            p.unlink()
            touched += 1
        elif p.read_bytes() != before[p]:
            p.write_bytes(before[p])
            touched += 1
    for p, b in before.items():            # a file the run deleted
        if not p.exists():
            p.write_bytes(b)
            touched += 1
    return touched


def parse(out):
    g = lambda pat: (m.group(1) if (m := re.search(pat, out)) else None)
    probs = g(r"PROBLEMS \((\d+)\)")
    return {"min_font": g(r"min font size\s*:\s*([\d.]+) pt"),
            "min_gap": g(r"min text-text gap\s*:\s*(-?[\d.]+) pt"),
            "required_gap": g(r"min text-text gap\s*:.*required >= ([\d.]+)"),
            "problems": int(probs) if probs else (0 if "PROBLEMS: none" in out else None)}


def fig1_command(args):
    wsl = shutil.which("wsl")
    if not wsl:
        return None, "wsl not found"
    distro, py = args.fig1_wsl_distro, args.fig1_python
    probe = subprocess.run([wsl, "-d", distro, "-e", py, "-c", "import cartopy"],
                           capture_output=True, text=True)
    if probe.returncode != 0:
        return None, f"{distro}:{py} cannot import cartopy"
    wpath = subprocess.run([wsl, "-d", distro, "-e", "wslpath", "-a", str(HERE)],
                           capture_output=True, text=True).stdout.strip()
    return [wsl, "-d", distro, "--cd", wpath, "-e", py, "fig1_study_map.py"], None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--skip-fig1", action="store_true")
    ap.add_argument("--fig1-wsl-distro", default="Ubuntu-22.04")
    ap.add_argument("--fig1-python", default="/home/yunus/mm-thermal/bin/python")
    args = ap.parse_args()
    names = args.only or SCRIPTS
    rows = []
    for name in names:
        row = {"figure": name, "asserts": n_asserts(name)}
        if name == "fig1_study_map":
            cmd, why = (None, "--skip-fig1 given") if args.skip_fig1 else fig1_command(args)
            if cmd is None:
                row.update(status="SKIPPED", note=f"cartopy env not available ({why})")
                rows.append(row)
                continue
        else:
            cmd = [sys.executable, f"{name}.py"]
        before = snapshot()
        try:
            r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True, encoding="utf-8",
                               errors="replace", env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8"})
        finally:
            row["outputs_touched"] = restore(before)
        out = r.stdout + r.stderr
        row.update(parse(out))
        if r.returncode != 0:
            last = [l for l in out.strip().splitlines() if l.strip()]
            row.update(status="FAIL", note=(last[-1] if last else f"exit {r.returncode}")[:160])
        elif row["problems"] is None:
            row.update(status="FAIL", note="no layout-check report in the output")
        elif row["problems"] > 0:
            row.update(status="FAIL", note=f"{row['problems']} layout problem(s)")
        else:
            row.update(status="PASS", note="")
        rows.append(row)

    print(f"\n{'figure':24s} {'status':8s} {'asserts':>7s} {'layout':>6s} {'min gap':>12s} {'min font':>8s} {'files':>5s}  note")
    print("-" * 110)
    for r in rows:
        gap = f"{r.get('min_gap')}/{r.get('required_gap')}" if r.get("min_gap") else "-"
        lay = "-" if r.get("problems") is None else str(r["problems"])
        print(f"{r['figure']:24s} {r['status']:8s} {r['asserts']:>7d} {lay:>6s} {gap:>12s} "
              f"{(r.get('min_font') or '-'):>8s} {str(r.get('outputs_touched', '-')):>5s}  {r.get('note', '')}")
    n = {s: sum(r["status"] == s for r in rows) for s in ("PASS", "FAIL", "SKIPPED")}
    print(f"\n{n['PASS']} PASS, {n['FAIL']} FAIL, {n['SKIPPED']} SKIPPED of {len(rows)}. "
          "Asserts are assert statements in the script (and _conservation_common.py for Figs. 5-7). "
          "'files' is the number of output files the run rewrote; all were restored byte for byte.")
    sys.exit(1 if n["FAIL"] else 2 if n["SKIPPED"] else 0)


if __name__ == "__main__":
    main()

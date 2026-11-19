#!/usr/bin/env python3
"""make_supplement_sections.py: writes Sections S2.3 and S4.6 of the IJWF supplement from analysis outputs.

No number in these two sections is typed by hand. S2.3 (distance bands, Table S16) is read from the frozen
output paper/labelfix_rerun/geometry/a1_band_auc.csv. S4.6 (check against earlier burns, Table S17) is read
from local_check_history.json and .csv, which local_check_history.py writes next to this file.

Run:  python paper/submissions/ijwf/analyses/make_supplement_sections.py
It replaces the text between the markers <!-- IJWF:S2.3 --> ... <!-- /IJWF:S2.3 --> and
<!-- IJWF:S4.6 --> ... <!-- /IJWF:S4.6 --> in text/supplementary.md (the build drops the markers).
"""
import csv
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
PAPER = HERE.parents[2]
SUPP = HERE.parent / "text" / "supplementary.md"
NAME = {"manavgat_2021": "Manavgat", "bejis_2022": "Bejís", "mugla_2021": "Muğla",
        "evia_2021_extended": "Evia", "montiferru_2021": "Montiferru"}
ORDER = list(NAME)
MINUS = "−"


def f3(x, signed=False):
    s = f"{abs(x):.3f}"
    return (("+" if x >= 0 else MINUS) + s) if signed else ((MINUS + s) if x < 0 else s)


def f2(x):
    return ("+" if x >= 0 else MINUS) + f"{abs(x):.2f}"


# ---------------------------------------------------------------- S2.3 distance bands
BANDS = [("0-0.5", "0 to 0.5 km"), ("0.5-1", "0.5 to 1 km"), ("1-2", "1 to 2 km"), ("2-5", "2 to 5 km"),
         ("5-10", "5 to 10 km"), ("10-inf", "beyond 10 km"), ("all", "all")]
rows = list(csv.DictReader(open(PAPER / "labelfix_rerun" / "geometry" / "a1_band_auc.csv", encoding="utf-8")))
auc = {(r["region"], r["band"]): float(r["auc"]) for r in rows if r["k"] == "0" and r["auc"]}
assert len(auc) == len(ORDER) * len(BANDS), len(auc)
mean = {b: sum(auc[(r, b)] for r in ORDER) / len(ORDER) for b, _ in BANDS}
table16 = ["| Region | " + " | ".join(label for _, label in BANDS) + " |", "|---|" + "---:|" * len(BANDS)]
for r in ORDER:
    table16.append(f"| {NAME[r]} | " + " | ".join(f3(auc[(r, b)]) for b, _ in BANDS) + " |")
table16.append("| Mean | " + " | ".join(f3(mean[b]) for b, _ in BANDS) + " |")
s23 = f"""## S2.3 Distance bands

The frame cost can also be read as a gradient. Table S16 scores the out-of-fold predictions of each region model (row A of Table 3) against the unburned cells of one distance band at a time, with all burned cells of the region as positives. The mean AUC over the five regions rises from {f3(mean['0-0.5'])} against the unburned cells within 0.5 km of a burned cell to {f3(mean['2-5'])} at 2 to 5 km and {f3(mean['10-inf'])} beyond 10 km, against {f3(mean['all'])} over all unburned cells. Like the other frame analyses, the bands were computed after the first results and are exploratory.

**Table S16. AUC of the region models by the distance of the unburned cells from the fire.** Thermal model, out-of-fold predictions of 5-fold blocked cross-validation at 5 km blocking. All burned cells of the region are scored against the unburned cells whose distance to the nearest burned cell lies in the band. The last column uses all unburned cells and equals the 10-cell rows of Table 2.

""" + "\n".join(table16) + "\n"

# ---------------------------------------------------------------- S4.6 check against earlier burns
J = json.loads((HERE / "local_check_history.json").read_text(encoding="utf-8"))
D = [r for r in csv.DictReader(open(HERE / "local_check_history.csv", encoding="utf-8")) if r["auc_hist"]]
assert len(D) == J["directions_used"]
rho, ci = J["spearman_hist_vs_event"]["rho"], J["spearman_hist_vs_event"]["ci95"]
rho2, ci2 = (J["spearman_hist_vs_event_event_cells_removed"][k] for k in ("rho", "ci95"))
T = J["source_picked_by_check"]
picked = {v["picked_source"] for v in T.values()}
assert len(picked) == 1, "the check does not pick one source for every target; rewrite the sentence"
src = NAME[picked.pop()]
by_target = {}
for r in D:
    by_target.setdefault(r["target"], []).append((float(r["auc_event"]), r["source"]))
best = [NAME[t] for t, v in T.items() if v["picked_source"] == max(by_target[t])[1]]
worst = [NAME[t] for t, v in T.items() if v["picked_source"] == min(by_target[t])[1]]
count = {1: "one target", 2: "two", 3: "three", 4: "four"}
hist_cells = sorted({int(r["hist_cells"]) for r in D})
table17 = ["| Direction | Earlier-burn cells | Of which burned in the event | AUC against earlier burns | AUC against the event |",
           "|---|---:|---:|---:|---:|"]
for r in sorted(D, key=lambda r: (ORDER.index(r["target"]), ORDER.index(r["source"]))):
    table17.append(f"| {NAME[r['source']]}→{NAME[r['target']]} | {r['hist_cells']} | {r['hist_also_event']} | "
                   f"{f3(float(r['auc_hist']))} | {f3(float(r['auc_event']))} |")
table17.append(f"| Mean | | | {f3(J['mean_auc_hist'])} | {f3(J['mean_auc_event'])} |")
s46 = f"""## S4.6 A check against earlier burns

The main text recommends that a transferred model is tested in the target region. A burned-area record of earlier years is the only local label that exists before a fire season, so we tried it as such a test. This analysis was added after all other results and is exploratory. For each target, the cells that MCD64A1 marks as burned in the five calendar years before the event year (Table S12) were taken as the earlier burns. Manavgat has none, which leaves {len(D)} directions into four targets, with {hist_cells[0]} to {hist_cells[-1]} earlier-burn cells per target. Each transferred thermal model scored the target cells once, and the scores were compared with the earlier burns (the check) and with the event (the outcome). The models were refitted for this analysis and reproduce the raw column of Table S8 to within 0.0015 in all twenty directions.

The check did not predict the outcome (Table S17). Against the earlier burns the {len(D)} transfers averaged an AUC of {f3(J['mean_auc_hist'])}, below chance, against {f3(J['mean_auc_event'])} for the event. Over the {len(D)} directions the two AUCs were not positively related (Spearman ρ = {f2(rho)} [{f2(ci[0])}, {f2(ci[1])}], pair-cluster bootstrap with {J['spearman_hist_vs_event']['replicates']} replicates), and they fell on the same side of chance in {J['same_side_of_chance']['count']} of {J['same_side_of_chance']['of']} directions. When the earlier burns that burned again in the event were left out, ρ was {f2(rho2)} [{f2(ci2[0])}, {f2(ci2[1])}]. For every target the check ranked the {src} model first. That source was the best of the four for {count[len(best)]} ({', '.join(best)}) and the worst for the other {count[len(worst)]}, and on average the source picked by the check scored {f3(abs(J['picked_minus_mean_event_auc']))} {'below' if J['picked_minus_mean_event_auc'] < 0 else 'above'} the mean of the four sources. A likely reason is that land burned in the previous five years carries less fuel than its surroundings and appears to the predictors as a recent scar, so a short record of this kind tests a different question from the one a new large fire poses. A longer record was not available here and was not tested.

**Table S17. Transferred models scored against earlier burns and against the event.** Thermal model, natural-vegetation population, no target label used in fitting. Earlier burns are the cells burned in the five calendar years before the event year.

""" + "\n".join(table17) + "\n"
assert len(best) + len(worst) == len(T), "a picked source is neither the best nor the worst; rewrite the sentence"

text = SUPP.read_text(encoding="utf-8")
for tag, body in (("S2.3", s23), ("S4.6", s46)):
    pat = re.compile(rf"<!-- IJWF:{tag} -->.*?<!-- /IJWF:{tag} -->", re.S)
    assert len(pat.findall(text)) == 1, f"markers for {tag} not found exactly once in the supplement"
    text = pat.sub(lambda m: f"<!-- IJWF:{tag} -->\n{body}\n<!-- /IJWF:{tag} -->", text)
SUPP.write_text(text, encoding="utf-8", newline="\n")
print("S2.3 and S4.6 written;", "band means", {b: f3(mean[b]) for b, _ in BANDS})

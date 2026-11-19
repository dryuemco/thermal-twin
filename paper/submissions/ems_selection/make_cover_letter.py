"""make_cover_letter.py: writes cover_letter.docx with the numbers taken from values.tex (no number typed by hand).

Run:  python make_cover_letter.py   (needs python-docx)
"""
import re
from pathlib import Path

import docx
from docx.shared import Pt

HERE = Path(__file__).resolve().parent
v = {}
for f in ("values_frozen.tex", "values.tex"):
    v.update(re.findall(r"\\newcommand\{\\(\w+)\}\{(.*?)\}\s*$", (HERE / f).read_text(encoding="utf-8"), re.M))
title = re.search(r"\\title\{(.*?)\}", (HERE / "manuscript.tex").read_text(encoding="utf-8")).group(1)

paras = [
    "Department of Computer Engineering, Faculty of Engineering, Çukurova University, 01330 Sarıçam, Adana, Türkiye",
    "Dear Editors,",
    f"Please consider our manuscript \u201c{title}\u201d for publication as a research article in Environmental "
    "Modelling & Software.",
    "Wildfire susceptibility models are usually compared, and chosen, by their AUC under spatial block "
    "cross-validation inside mapped fires. The manuscript checks such choices retrospectively against the burning "
    f"that followed in the same areas. On {v['vnFires']} Mediterranean fires, a random forest given only cell "
    "coordinates had a higher within-event AUC than a forest on thermal and environmental predictors in "
    f"{v['sAllCoordChose']} of {v['sAllN']} fires. In the {v['sAElig']} fires with enough later burning to 2023, "
    f"that choice cost a mean of {v['sACrfLossAuc']} AUC on later burning. A replication on {v['sBElig']} fires "
    f"({v['sBOverlap']} of them also in the first set), scored on burning from January 2024 to September 2026 with "
    "focal scores frozen before the labels were exported but after that period had passed, gave a loss of "
    f"{v['sBCrfLossAuc']}. The distance-calibrated AUC of Hijmans (2012) made the same choice in {v['sACrfChCauc']} "
    f"of {v['sAElig']} fires, and in simulations tuned to the real fires every measure chose with a balanced "
    f"accuracy of about {v['sSimCalBalAuc']}. "
    "For forests that add coordinates or distance to training burns to the thermal predictors, the evidence was "
    "weaker. Only the distance hybrid met the rule we had declared, in one of the two windows and at the threshold, "
    "and the manuscript limits its claim to coordinate-only learners.",
    "We think the paper suits the journal because its contribution is to model evaluation, the theme of Bennett et "
    "al. (2013) and Meyer et al. (2018) in this journal. It does not propose a new fire model. The analysis code, "
    "the plan with its dated amendments and a register of when each decision rule was written relative to its "
    "results are public, and the selection measures and the later-burning loss can be computed for other sets of "
    "fires with the same code.",
    "The manuscript has not been published and is not under consideration elsewhere. Both authors approved the "
    "submission. We used generative AI tools for code, number checks and editing, as stated in the declaration "
    "before the references. There are no competing interests.",
    "Yours sincerely,",
    "Yunus Emre Cogurcu (corresponding author), on behalf of both authors\nycogurcu@cu.edu.tr",
]
d = docx.Document()
style = d.styles["Normal"]
style.font.name = "Times New Roman"
style.font.size = Pt(11)
for p in paras:
    d.add_paragraph(p)
d.save(HERE / "cover_letter.docx")
print(sum(len(p.split()) for p in paras), "words")

# Cover letter — Environmental Modelling & Software (draft, 2026-09-19)

> **Before sending, an author must check four things.** (1) The editor-in-chief's name on the
> journal's current masthead; the letter is addressed to the editors generically until then.
> (2) The originality and no-concurrent-submission statement: the companion manuscript on the
> preprocessing budget (`paper2/`) is not submitted; if it is submitted before this one is decided,
> the letter must name it and state how the two differ. (3) The availability sentence, which
> depends on how the private analysis repository is released (see `SUBMISSION_CHECKLIST.md`).
> (4) That both authors approve the final text.
>
> Every number below is in the current abstract or Results. The previous letter was retired
> because it advertised claims the paper has since withdrawn; it is in git history.

---

To the Editors, *Environmental Modelling & Software*

Dear Editors,

We submit the manuscript **"Evaluation geometry and the limits of cross-region transfer in
pre-fire thermal wildfire prediction"** for consideration as a Research Article in *Environmental
Modelling & Software*.

**What the paper reports.** Pre-fire thermal predictors of wildfire are rarely tested outside the
region they were fitted in. We add six thermal predictors to a terrain, fuel and greenness baseline
in five Mediterranean regions, with MCD64A1 labels and spatially blocked validation, and evaluate
the same model inside each region and across all twenty ordered region pairs.

The first result concerns evaluation design rather than wildfire. With the model held fixed, scoring
it on the burn scar and a 2 km collar instead of region-wide costs 0.143 ROC-AUC [+0.077, +0.208],
and a control attributes this to the composition of the negative pool, not to class balance. The
same effect operates between regions: our study areas enclose very unequal far fields, and
equalising them to a 10 km collar, which drops no burned cells, lifts mean transfer from 0.541 to
0.616. Applying that correction to our own analysis withdrew five of our earlier findings, and the
paper reports that plainly.

The second result is that local skill does not travel. The thermal block adds +0.045 to +0.148
ROC-AUC within regions at 5 km blocking, but +0.004 [−0.028, +0.036] across the twenty transfer
directions, and the static baseline transfers no better (0.537 against 0.541). On matched frames
and blocking, equalised transfer falls 0.155 short of the within-region reference. Label-free
alignment by standardisation and covariance alignment compresses most directions towards chance
rather than repairing them.

**Why we think it fits the journal.** The contribution is to model evaluation: it shows how much a
reported skill depends on the frame it is scored in, and it separates local skill from
transferability under a single, fixed modelling protocol. Both points generalise beyond wildfire to
any environmental model fitted in one region and applied in another, which we understand to be
central to the journal's interest in the generality and limits of modelling.

**On evidence and reproducibility.** Every number traces to a frozen artefact identified by hash,
and the analysis regenerates each table and figure. The upstream processing pipeline is public under
an MIT licence; the software and data availability section gives both repositories in the form the
journal requests. The limitations are stated in full in the manuscript, including those our own
checks turned up.

**Declarations.** The work is original, has not been published previously, and is not under
consideration elsewhere. Both authors have approved the submission. The funding, competing-interest,
CRediT and generative-AI declarations are included in the manuscript. The highlights, a graphical
abstract, eight figures and the supplementary material accompany the submission.

Yours sincerely,

Yunus Emre Coğurcu (corresponding author), on behalf of the authors
Çukurova University, Adana, Türkiye
ycogurcu@cu.edu.tr

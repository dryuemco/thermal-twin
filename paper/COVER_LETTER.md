# Cover letter — DRAFT, SUPERSEDED, DO NOT SEND

> **STOP. This letter predates the 2026-08-15 referee round and describes a claim set the manuscript
> has since retracted.** It carries the old title, and it advertises the sign-reversal mechanism and
> the six anti-predictive directions, both of which Section 4.9 withdraws as artefacts of the
> evaluation frames. Sending it would assert to an editor exactly what the paper now disclaims.
>
> It must be rewritten around what the manuscript currently says: the title in
> `paper/frontmatter.json`; the evaluation-geometry measurement (0.143 [+0.077, +0.208], mechanism
> isolated to the negative pool) as the lead; the transfer null restated on equalised frames (0.617
> against within-region ≈0.87); and the diagnostics result as "none was shown to order transfer once
> the frames are comparable". The self-correction is worth stating plainly to an editor — it is the
> strongest thing about the submission — rather than being hidden.
>
> Left in place, with this header, because the structure and the two author-checked statements below
> are still reusable. Rewrite before submission.

---

# (superseded draft follows)

> This is a draft. Two things must be checked by an author before it goes: the editor's name and
> title as they appear on the journal's current masthead, and the two statements made on the authors'
> behalf (originality and no concurrent submission). Nothing else in it asserts anything the
> manuscript does not.

---

To the Editors, *Ecological Informatics*

Dear Editors,

We submit for your consideration the manuscript **"Local skill, unstable portability: marginal
diagnostics do not order the cross-region transfer of pre-fire thermal dryness in Mediterranean
wildfire regions"** for publication in *Ecological Informatics*.

**What the paper reports.** Pre-fire thermal dryness, measured from land surface temperature, its
anomalies and dryness indices, is widely used to predict where fire will burn. It is rarely tested
outside the region it was fitted in. We analyse five Mediterranean wildfire regions on a common
~500 m grid with MCD64A1 labels and spatially blocked cross-validation, and we measure the same
predictor block twice: inside each region, and across all twenty ordered region pairs.

Inside every region the thermal block raises ROC-AUC by +0.06 to +0.15, with bootstrap support in
all five regions at both blocking scales the design supports as intervals. Across regions the same
block contributes +0.004 on average, with an interval spanning zero, and its sign is unstable. The
failure is conditional rather than marginal: predictors reverse the direction of their association
with burning between regions, and we show one such reversal inside a single study area, between two
fires eleven months apart, with disjoint bootstrap intervals.

The practical consequence is the part we think matters most to your readership. We rank-correlated
twenty candidate transferability diagnostics against observed transfer. Only two had bootstrap
intervals excluding zero, and both need labels in *both* regions. Every diagnostic that can actually
be run before deployment, the marginal predictor-space-distance family that underlies area-of-
applicability reasoning, fails to order the transfer matrix. Label-free domain adaptation by
standardisation and covariance alignment does not repair transfer either; it compresses it towards
chance in fourteen of the twenty directions. What does work is target labels, and we price that:
thirty-two labelled blocks recover 85 to 89 % of the target's own ceiling in three of six directions
tested.

**Why we think it fits the journal.** This is a negative result reported with a mechanism, not an
absence of one, and it is aimed squarely at the ecological-informatics practice of transferring a
fitted model to a new landscape and justifying the move with a similarity or applicability
diagnostic. We found no prior application of covariance alignment to fire susceptibility, fire
occurrence or burned-area prediction.

**On evidence and reproducibility.** Every number traces to a frozen artefact. The analysis code is
public (MIT licence) and is named in the data-and-code availability statement; three provenance gaps
are stated there in plain terms rather than glossed. The manuscript also carries an unusually full
limitations section, including several items an internal review turned up about the observational
layer. We would rather the reader see those than discover them.

**Declarations.** The work is original, has not been published previously, and is not under
consideration elsewhere. All authors have approved the submission. The CRediT statement, competing-
interest declaration, funding statement and data-and-code availability statement are included in the
manuscript. Highlights (five bullets) and eight figures in vector format accompany the submission,
together with one supplementary section.

We would be glad to respond to any questions.

Yours sincerely,

Yunus Emre Coğurcu (corresponding author), on behalf of the authors
Çukurova University, Adana, Türkiye
ycogurcu@cu.edu.tr

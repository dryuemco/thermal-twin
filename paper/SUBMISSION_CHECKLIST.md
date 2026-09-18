# Ecological Informatics — submission checklist (verified 2026-09-19)

The ScienceDirect guide for authors returns 403 to automated fetching. Each requirement below is
sourced as stated; "live" means the current guide text as quoted by a search engine index, "2024"
means the Wayback copy of 2024-01-03, "Elsevier" means a first-party elsevier.com page read directly.

## Journal facts

| Item | Value | Source |
|---|---|---|
| Business model | **Full Open Access** since 2024-01-01; APC is compulsory on acceptance | Elsevier APC list; journal news page (live) |
| APC (list) | **USD 3,190 / EUR 2,910**, excl. tax | `article-publishing-charge.xlsx`, prices as of 27-Aug-2026 |
| APC for this author group | **90 % of list ≈ USD 2,871** + tax: journal is in the GPOA pilot, Turkey is "Upper-middle income 3" | Elsevier GPOA pricing page + GPOA journals list |
| TÜBİTAK EKUAL cover | **Not found for Elsevier.** Current EKUAL Read & Publish: Springer Nature, Wiley, OUP, CUP, IOP, RSC | Sabancı Univ. library publisher list; ULAKBİM search |

## Manuscript requirements, and where this manuscript stands

| Requirement | Rule | Manuscript | Status |
|---|---|---|---|
| Abstract | ≤ 250 words (live; 2024 said 400) | 238 words | OK |
| Keywords | 1 to 7 (live; 2024 said 4 to 6) | 6 | OK |
| Highlights | 3 to 5 bullets, ≤ 85 characters each, separate editable file named "Highlights" | 5 bullets, 68 to 75 chars (`highlights.md`) | OK; upload as its own file |
| Graphical abstract | optional, encouraged | none | optional |
| Generative-AI declaration | heading "Declaration of generative AI and AI-assisted technologies in the manuscript preparation process", immediately before the references; AI use in the research process also described in Methods | **added 2026-09-19** | **authors to confirm the wording; Methods sentence not yet written** |
| Competing interests, funding, CRediT, data availability | required | present | see blockers |
| Structure | numbered sections, Introduction … Conclusions | yes | OK |

Policy source for the AI declaration: Elsevier, "Generative AI policies for journals", updated June 2026.

## Blockers before upload

1. **The data/code repository named in the declarations is private.** `github.com/dryuemco/thermal-twin`
   is PRIVATE (checked with `gh repo view`, 2026-09-19). Reviewers following the link get a 404.
   Options: make it public after removing private material (mail drafts, `methods_inventory_*`,
   `scratch/`), or deposit a cleaned snapshot (e.g. Zenodo) and cite that. Authors' decision.
2. **The funding statement says the APC is covered under an EKUAL agreement.** No such Elsevier
   agreement was found. Confirm with the Çukurova library, or name the real payer (e.g. the BAP
   project), or remove the sentence.
3. **Co-author approval of the final text**, and the pending answer on the Manavgat AOI timing
   (`emrehan_mail_7.md`). The answer does not block: §3.1 holds whichever way it goes.
4. **Generative-AI declaration wording**, confirmed by both authors (see above).

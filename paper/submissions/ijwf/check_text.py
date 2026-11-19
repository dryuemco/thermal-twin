"""check_text.py: compares the IJWF text in submissions/ijwf/text/ with the shared sources in paper/.

Run from anywhere:  python paper/submissions/ijwf/check_text.py

It reports the word count of the main text (Introduction to Conclusions, without tables, table legends
and notes), the numbers and citation keys that left the main text and where they are now, numbers that
exist in the new text but in no original source, table rows that changed, cross-references to the
supplement that have no target, and a few style counts (colons, semicolons, long forms of abbreviations).
Nothing is written. The shared sources in paper/ are read only.
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
NEW = HERE / "text"
ORIG = HERE.parent.parent
BODY = ["01_introduction", "03_methods", "04_results", "05_discussion", "06_conclusions"]
LIMIT = 6000

NUM = re.compile(r"[+−]?\d[\d,]*\.\d+|\d{1,3}(?:,\d{3})+|(?<![\w.])\d{3,}(?![\w.])")
CITE = re.compile(r"\[(@[^\]]+)\]")
NARR = re.compile(r"\b[A-Z][\wé-]+ (?:et al\.|and [A-Z][\wé-]+) \[@[\w-]+\]")


def read(folder, name, ext=".md"):
    return re.sub(r"<!--[\s\S]*?-->", "", (folder / f"{name}{ext}").read_text(encoding="utf-8"))


def prose(md):
    """Text that counts: no tables, table titles with legends, table notes or display equations."""
    md = re.sub(r"```math[\s\S]*?```", "", md)
    keep = []
    for block in re.split(r"\n\s*\n", md):
        b = block.strip()
        if not b or b.startswith(("|", "**Table ", "*Table note.*", "![")):
            continue
        keep.append(b)
    return "\n\n".join(keep)


def count(md):
    p = prose(md)
    keys = sum(len(g.split(";")) for g in CITE.findall(p))
    narrative = len(NARR.findall(p))
    bare = CITE.sub(" ", p)
    words = len(re.sub(r"[*_`#|]", " ", bare).split())
    return words, keys, narrative


def nums(text):
    return set(NUM.findall(text))


def keys(text):
    return {k.strip().lstrip("@") for g in CITE.findall(text) for k in g.split(";")}


def rows(md):
    return [l.rstrip() for l in md.splitlines() if l.lstrip().startswith("|")]


new_body = {f: read(NEW, f) for f in BODY}
orig_body = {f: read(ORIG, f) for f in BODY}
new_main = "\n\n".join(new_body.values())
orig_main = "\n\n".join(orig_body.values())
new_supp = read(NEW, "supplementary")
orig_supp = read(ORIG, "supplementary")
new_caps = read(NEW, "figure_captions", ".tex")
orig_caps = read(ORIG, "figure_captions", ".tex")
new_decl = read(NEW, "07_declarations")
orig_decl = read(ORIG, "07_declarations")
new_abs = read(NEW, "00_abstract_ijwf") if (NEW / "00_abstract_ijwf.md").exists() else ""
orig_abs = read(ORIG, "00_abstract") + read(ORIG, "00_abstract_fire_ecology")
orig_all = "\n".join([orig_main, orig_supp, orig_caps, orig_decl, orig_abs])
new_all = "\n".join([new_main, new_supp, new_caps, new_decl, new_abs])

print("== 1. Word count, Introduction to Conclusions (tables, legends, notes, equations excluded)")
tot_w = tot_k = tot_n = 0
for f in BODY:
    w, k, n = count(new_body[f])
    ow, ok, on = count(orig_body[f])
    tot_w, tot_k, tot_n = tot_w + w, tot_k + k, tot_n + n
    print(f"  {f:<16} words {w:>5} + {k:>3} citation keys   (original {ow} + {ok})")
low = tot_w + tot_k
high = tot_w + 4 * tot_k - 3 * tot_n
print(f"  total words {tot_w}, citation keys {tot_k}, narrative citations {tot_n}")
print(f"  counted with one word per citation key: {low}")
print(f"  counted with four words per key (Author et al. Year), the cautious figure: {high}")
print(f"  limit {LIMIT}: {'OK' if high < LIMIT else 'OVER'} (margin {LIMIT - high})")

print("\n== 2. Numbers of the original main text that are no longer in the new main text")
gone = sorted(nums(prose(orig_main)) - nums(new_main))
in_supp = [x for x in gone if x in nums(new_supp)]
in_caps = [x for x in gone if x not in in_supp and x in nums(new_caps + new_abs + new_decl)]
lost = [x for x in gone if x not in in_supp and x not in in_caps]
print(f"  moved to the supplement ({len(in_supp)}): {' '.join(in_supp)}")
print(f"  now only in captions, abstract or statements ({len(in_caps)}): {' '.join(in_caps)}")
print(f"  NOT FOUND anywhere in the new package ({len(lost)}): {' '.join(lost)}")

print("\n== 3. Numbers in the new text that no original source contains")
print("  main text:", " ".join(sorted(nums(new_main + new_abs) - nums(orig_all))) or "none")
print("  supplement:", " ".join(sorted(nums(new_supp) - nums(orig_all))) or "none")
print("  captions and statements:", " ".join(sorted(nums(new_caps + new_decl) - nums(orig_all))) or "none")

print("\n== 4. Citation keys")
bib = set(re.findall(r"@\w+\{([^,\s]+),", (NEW / "REFERENCES.bib").read_text(encoding="utf-8")))
dropped = sorted(keys(orig_main) - keys(new_main))
print(f"  left the main text ({len(dropped)}):")
print("    still cited in the supplement or statements:", " ".join(k for k in dropped if k in keys(new_supp + new_decl)) or "none")
print("    no longer cited anywhere:", " ".join(k for k in dropped if k not in keys(new_supp + new_decl)) or "none")
print("  cited but not in REFERENCES.bib:", " ".join(sorted(keys(new_all) - bib)) or "none")

print("\n== 5. Table rows")
missing = [r for r in rows(orig_main) if r not in rows(new_main)]
print(f"  main-text table rows changed or missing: {len(missing)}")
for r in missing:
    print("    ", r[:110])
norm = lambda r: re.sub(r" \((?:a\d|R8\w(?:, R8\w)*)\)", "", r)
new_rows = {norm(r) for r in rows(new_supp)}
missing = [r for r in rows(orig_supp) if norm(r) not in new_rows]
print(f"  supplement table rows changed or missing: {len(missing)}")
for r in missing:
    print("    ", r[:110])

print("\n== 6. Cross-references from the main text and captions to the supplement")
heads = set(re.findall(r"(?m)^#+ (S\d+(?:\.\d+)?) ", new_supp))
tabs = set(re.findall(r"\*\*Table (S\d+)\.", new_supp))
figs = set(re.findall(r"\*\*Fig\. (S\d+)\.", new_supp))
text = new_main + new_caps + new_decl
bad = []
for kind, pool, pat in (("Section", heads, r"Supplementary Sections? ((?:S\d+(?:\.\d+)?(?:, | and | to )?)+)"),
                        ("Table", tabs, r"Supplementary Tables? ((?:S\d+(?:, | and | to )?)+)"),
                        ("Fig", figs, r"Supplementary Figs?\.? ((?:S\d+(?:, | and | to )?)+)")):
    for m in re.finditer(pat, text):
        for x in re.findall(r"S\d+(?:\.\d+)?", m.group(1)):
            if x not in pool:
                bad.append(f"{kind} {x}")
print("  without a target:", ", ".join(sorted(set(bad))) or "none")
stray = re.findall(r"(?<!Supplementary )(?<!Supplementary Sections )\b(?:Section|Table|Fig\.|Figs) S\d[\d.]*", new_main)
print("  supplement items cited without the word Supplementary:", ", ".join(sorted(set(stray))) or "none")
numbered = re.findall(r"\bSections? \d(?:\.\d+)?", new_main + new_caps + new_supp + new_decl)
print("  references to numbered main-text sections (headings are unnumbered):", ", ".join(sorted(set(numbered))) or "none")
for label, pat, n in (("Fig", r"\bFigs?\. ?(\d)", 8), ("Table", r"\bTables? (\d)", 4)):
    order = []
    for m in re.finditer(pat, prose(new_main)):
        if int(m.group(1)) not in order:
            order.append(int(m.group(1)))
    print(f"  {label}s first cited in the order {order}: {'OK' if order == list(range(1, n + 1)) else 'CHECK'}")

print("\n== 7. Style counts in the main text prose")
p = CITE.sub("", prose(new_main))
print("  semicolons:", p.count(";"), " colons:", len(re.findall(r":(?!//)", p)), " em dashes:", p.count("—"),
      " section signs:", p.count("§"))
sent = [s for s in re.split(r"(?<=[.?!])\s+(?=[A-Z*])", re.sub(r"(?m)^#+ .*$", "", p)) if s.strip()]
lens = [len(s.split()) for s in sent]
print(f"  sentences {len(lens)}, mean length {sum(lens) / len(lens):.1f} words, longest {max(lens)}, "
      f"over 35 words: {sum(l > 35 for l in lens)}")
for long_form in ("land surface temperature", "area under the receiver operating", "ROC-AUC",
                  "Temperature-Vegetation Dryness Index", "normalised difference vegetation index",
                  "Moderate Resolution Imaging", "European Space Agency"):
    print(f"  '{long_form}' in main prose: {len(re.findall(long_form, p))}")
code = re.findall(r"`[^`\n]*\.(?:py|json|csv|mjs|parquet|md)`|`(?:paper|round\d|code|inference|labels|exports)/[^`\n]*`", new_all)
print("  file or script names left in the package text:", len(code))
for c in sorted(set(code))[:40]:
    print("    ", c)

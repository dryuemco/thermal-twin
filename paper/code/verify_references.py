"""Check paper/REFERENCES.bib against the registries and against the manuscript (2026-09-29).

For every entry with a DOI: resolve it at Crossref (journal articles) or DataCite (datasets, preprints)
and compare year, volume, pages or article number, and the first author's family name. Then check
that every key cited in the manuscript, the declarations and the supplement exists, and that no
entry is uncited. Prints one line per entry and exits non-zero on any mismatch.

Usage: python paper/code/verify_references.py      (needs network access)
"""
import json
import re
import sys
import unicodedata
import urllib.request
from pathlib import Path

P = Path(__file__).resolve().parents[1]
BIB = (P / "REFERENCES.bib").read_text(encoding="utf-8")
LATEX = {r"{\i}": "ı", r"\i": "ı", r"{\'e}": "é", r"{\'i}": "í", r"{\'a}": "á", r"{\'o}": "ó", r'{\"o}': "ö",
         r'{\"u}': "ü", r"{\c{s}}": "ş", r"{\c{S}}": "Ş", r"{\c{c}}": "ç", r"{\c{C}}": "Ç", r"{\u{g}}": "ğ",
         r"{\.I}": "İ", r"{\'E}": "É", r"{\~n}": "ñ", r"{\`a}": "à", r"{\`e}": "è"}


def plain(s):
    for k, v in LATEX.items():
        s = s.replace(k, v)
    s = re.sub(r"[{}\\]", "", s)
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower().strip()


def entries():
    for m in re.finditer(r"@(\w+)\{([^,]+),([\s\S]*?)\n\}", BIB):
        f = dict((k.lower(), v.strip()) for k, v in re.findall(r"(\w+)\s*=\s*\{((?:[^{}]|\{[^{}]*\})*)\}", m.group(3)))
        yield m.group(1).lower(), m.group(2).strip(), f


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "thermal-twin reference check (mailto:ycogurcu@cu.edu.tr)"})
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def check(key, f):
    doi = f.get("doi")
    if not doi:
        return "no DOI (not checked)", True
    first = plain(re.split(r"\s+and\s+", f.get("author", ""))[0].split(",")[0])
    try:
        m = get(f"https://api.crossref.org/works/{doi}")["message"]
        reg = "crossref"
        year = (m.get("published-print") or m.get("issued"))["date-parts"][0][0]
        issued = m["issued"]["date-parts"][0][0]
        fam = plain(m["author"][0].get("family", m["author"][0].get("name", ""))) if m.get("author") else ""
        vol, pages = m.get("volume"), m.get("page") or m.get("article-number")
    except Exception:
        try:
            a = get(f"https://api.datacite.org/dois/{doi}")["data"]["attributes"]
        except Exception as e:
            return f"DOI does not resolve at Crossref or DataCite ({e})", False
        reg, year = "datacite", a.get("publicationYear")
        issued = year
        c = a.get("creators") or [{}]
        fam = plain(c[0].get("familyName") or c[0].get("name", ""))
        vol, pages = None, None
    bad = []
    if str(f.get("year")) not in {str(year), str(issued)}:
        bad.append(f"year {f.get('year')} vs {year}")
    if vol and f.get("volume") and str(f["volume"]) != str(vol):
        bad.append(f"volume {f['volume']} vs {vol}")
    if pages and f.get("pages") and plain(f["pages"]).replace("--", "-") != str(pages).lower():
        bad.append(f"pages {f['pages']} vs {pages}")
    if fam and first and fam.split()[-1] not in first and first.split()[-1] not in fam:
        bad.append(f"first author {first!r} vs {fam!r}")
    return (f"{reg}: " + ("; ".join(bad) if bad else "OK")), not bad


text = "\n".join((P / f).read_text(encoding="utf-8") for f in
                 ["00_abstract.md", "01_introduction.md", "02_related_work.md", "03_methods.md", "04_results.md",
                  "05_discussion.md", "06_conclusions.md", "07_declarations.md", "supplementary.md"])
cited = set(re.findall(r"@([A-Za-z][A-Za-z0-9]+)", re.sub(r"`[^`]*`", "", text)))
cited -= {"Section"}
ok, keys = True, set()
for typ, key, f in entries():
    keys.add(key)
    msg, good = check(key, f)
    ok &= good
    print(f"{'PASS' if good else 'FAIL'}  {key:22s} {msg}")
missing = sorted(k for k in cited if k not in keys and not k.startswith("dryuemco"))
unused = sorted(keys - cited)
print(f"\n{len(keys)} entries; cited keys missing from the bib: {missing}; entries cited nowhere: {unused}")
ok &= not missing and not unused
sys.exit(0 if ok else 1)

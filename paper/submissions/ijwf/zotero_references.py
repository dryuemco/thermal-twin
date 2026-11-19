"""zotero_references.py: files the references the IJWF manuscript cites into a Zotero collection by DOI
and compares what the DOI resolves to with the entry in text/REFERENCES.bib.

Run:  python paper/submissions/ijwf/zotero_references.py <collection key>
Needs zotero-cli with a writable library. Items that already exist are reused (no duplicates), and no
PDF is attached. Writes reference_check.json next to this file: one record per cited key with the
Zotero item key, the fields that differ and the abstract Zotero stored (for checking how a work is
described in the text). A DOI that does not resolve is reported, never guessed.
"""
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
TEXT = HERE / "text"
COLLECTION = sys.argv[1]
SOURCES = ["01_introduction", "03_methods", "04_results", "05_discussion", "06_conclusions",
           "07_declarations", "supplementary"]


def bib_entries():
    bib = (TEXT / "REFERENCES.bib").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"@(\w+)\{([^,\s]+),(.*?)\n\}", bib, re.S):
        fields = {k.lower(): " ".join(v.split()) for k, v in
                  re.findall(r"(?m)^\s*(\w+)\s*=\s*\{(.*?)\},?\s*$(?=\n\s*\w+\s*=|\n?\Z)", m.group(3), re.S)}
        out[m.group(2)] = {"type": m.group(1).lower(), **fields}
    return out


def cited():
    keys = set()
    for f in SOURCES:
        for g in re.findall(r"\[(@[^\]]+)\]", (TEXT / f"{f}.md").read_text(encoding="utf-8")):
            keys |= {k.strip().lstrip("@") for k in g.split(";")}
    return sorted(keys)


def plain(s):
    s = re.sub(r"\\[`'^\"~=.uvHtcdbk]\s*\{?([A-Za-z])\}?", r"\1", s or "")      # LaTeX accents
    s = re.sub(r"\{\\([a-zA-Z]+)\}", r"\1", s).replace("{", "").replace("}", "").replace("\\&", "&")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c)).replace("ı", "i").replace("İ", "I")
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def cli(*args):
    r = subprocess.run(["zotero-cli", "--json", *args], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", shell=(sys.platform == "win32"))
    try:
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        return {"ok": False, "error": {"message": (r.stdout + r.stderr)[-300:]}}


bib, records = bib_entries(), []
for key in cited():
    e = bib[key]
    rec = {"key": key, "doi": e.get("doi"), "differs": {}}
    if not e.get("doi"):
        rec["status"] = "no DOI in the bibliography"
        records.append(rec)
        continue
    added = cli("add", "doi", e["doi"], "-c", COLLECTION, "--attach-mode", "none")
    text = (added.get("data") or {}).get("text", "")
    m = re.search(r"[Ii]tem key: `([A-Z0-9]{8})`", text) or re.search(r"`([A-Z0-9]{8})`", text)
    if not added.get("ok") or not m:
        rec["status"] = "DOI not added: " + (added.get("error", {}).get("message") or text)[:200]
        records.append(rec)
        print(f"{key:28} FAILED")
        continue
    rec["zotero"] = m.group(1)
    meta = (cli("get", "metadata", rec["zotero"]).get("data") or {}).get("data") or {}
    z_title, z_year = meta.get("title", ""), (re.search(r"\d{4}", meta.get("date", "")) or [""])[0]
    z_auth = [c.get("lastName") or c.get("name", "") for c in meta.get("creators", []) if c.get("creatorType") == "author"]
    b_auth = [a.split(",")[0].strip() for a in re.split(r"\s+and\s+", e.get("author", ""))]
    checks = {
        "title": (plain(e.get("title")), plain(z_title)),
        "year": (e.get("year", ""), z_year),
        "journal": (plain(e.get("journal") or e.get("booktitle") or e.get("institution")),
                    plain(meta.get("publicationTitle") or meta.get("proceedingsTitle") or meta.get("institution")
                          or meta.get("publisher") or meta.get("repository"))),
        "volume": (e.get("volume", ""), meta.get("volume", "") or ""),
        "pages": (re.sub(r"-+|–", "-", e.get("pages", "")), re.sub(r"-+|–", "-", meta.get("pages", "") or "")),
        "first author": (plain(b_auth[0]) if b_auth else "", plain(z_auth[0]) if z_auth else ""),
        "number of authors": (str(len(b_auth)), str(len(z_auth))),
    }
    for name, (b, z) in checks.items():
        if b != z and not (name in ("volume", "pages", "journal") and not b and not z):
            rec["differs"][name] = {"bibliography": b, "resolved": z}
    rec["status"] = "matches" if not rec["differs"] else "differs"
    rec["type"], rec["resolved_title"], rec["abstract"] = meta.get("itemType"), z_title, meta.get("abstractNote", "")
    records.append(rec)
    print(f"{key:28} {rec['zotero']}  {rec['status']}  {', '.join(rec['differs'])}")

(HERE / "reference_check.json").write_text(json.dumps(records, ensure_ascii=False, indent=1), encoding="utf-8")
n = {s: sum(r["status"].startswith(s) for r in records) for s in ("matches", "differs", "DOI not added", "no DOI")}
print("done:", len(records), "cited keys;", n)

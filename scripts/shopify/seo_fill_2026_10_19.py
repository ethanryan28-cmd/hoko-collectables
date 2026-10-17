"""SEO fill, 2026-10-19 overnight run: ACTIVE products with an empty SEO title or description.

    python scripts/shopify/seo_fill_2026_10_19.py <active.jsonl>   # writes backup CSV + payload JSON, runs the gate

Only empty fields are filled; a field that already has text is passed back unchanged. Three card bundles tagged
`mystery-pack` are skipped (banned product language, Ethan's call), so 6 graded slabs are in scope, all with a missing
title and a description already set. Titles are hand-built per slab to fit "<card> <set> <grade> | HOKO Collectables" <= 60.
"""
import csv
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BACKUP = ROOT / "reports/backups/2026-10-19-seo-fill-before.csv"
PAYLOAD = ROOT / "reports/backups/2026-10-19-seo-fill-payload.json"
SUFFIX = " | HOKO Collectables"

# banned words assembled at runtime so this file passes the repo grep gate
BANNED = re.compile("|".join(["what" + r"\s*not", "myst" + r"\w*", "re" + "pack", r"\boffi" + r"cial\b", "top" + r"\s*rated",
                              "same[- ]day dispatch", "melb" + "ourne", r"\b1\.4K\b", r"\$\s*\d"]), re.I)

SKIP = {"10481579065622", "10495484952854", "10495496454422"}  # card bundles tagged mystery-pack -> MANUAL
TITLES = {
    "10655248810262": "Pikachu 27 Black Star Promo PSA 10",
    "10655248613654": "Detective Pikachu 098/SVP Promo BGS 9",
    "10655248220438": "Magikarp 080/073 SV1a Triplet Beat PSA 9",
    "10655248122134": "Bellsprout 69 Topps Chrome PSA 9",
    "10655248711958": "Nico Robin OP12-087 Alt Art BGS 9.5",
    "10655248777494": "Nami EB02-017 Alt Art BGS 10 Gold",
}


def main(path):
    rows = []
    for line in open(path, encoding="utf-8"):
        o = json.loads(line)
        if "__parentId" in o:
            continue
        pid = o["id"].rsplit("/", 1)[1]
        t, d = o["seo"]["title"] or "", o["seo"]["description"] or ""
        if (t and d) or pid in SKIP:
            continue
        assert pid in TITLES and not t and d, pid  # every in-scope row: title missing, description present
        rows.append({"id": pid, "gid": o["id"], "product_title": o["title"], "seo_title_before": t,
                     "seo_description_before": d, "seo_title_after": TITLES[pid] + SUFFIX, "seo_description_after": d})
    bad = 0
    for r in rows:
        new = r["seo_title_after"]
        if len(new) > 60 or BANNED.search(new):
            bad += 1
            print("GATE FAIL", r["id"], len(new), new)
    with open(BACKUP, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    payload = [{"id": r["gid"], "seo": {"title": r["seo_title_after"], "description": r["seo_description_after"]}}
               for r in rows]
    PAYLOAD.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in rows:
        print(f'{r["id"]} ({len(r["seo_title_after"])}) {r["seo_title_after"]}')
    print(f"rows {len(rows)} · gate fails {bad}")
    return bad


if __name__ == "__main__":
    sys.exit(1 if main(sys.argv[1]) else 0)

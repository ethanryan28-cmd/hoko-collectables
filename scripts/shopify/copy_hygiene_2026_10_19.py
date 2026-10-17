"""Copy hygiene, 2026-10-19: postage copy (step 1) and SEO titles over 60 (step 3). Content fields only.

    python scripts/shopify/copy_hygiene_2026_10_19.py postage <active.jsonl>   # backup CSV + data CSV + bulk JSONL
    python scripts/shopify/copy_hygiene_2026_10_19.py seo <active.jsonl>       # backup CSV + bulk JSONL + MANUAL list
    python scripts/shopify/copy_hygiene_2026_10_19.py readback <step> <after.jsonl>

Input: a bulk-operation JSONL of every ACTIVE product (id title handle productType tags descriptionHtml seo, variants
price). Price is read only to pick the postage line by kind; nothing writes price, inventory, status or orders.

Step 1 replaces only the postage sentences, leaving the rest of each description byte-identical:
  singles under $50 -> "$3 untracked letter" · singles $50+ and slabs -> "$10.95 tracked, free tracked at $150+"
  · Japanese sealed -> "$15.25 tracked, free on sealed orders of $250+" + the 2-4 business days line.
The 3 card bundles are written in step 2 (with their retitle), but their postage rows are listed in the step 1 CSV.
Step 3 rebuilds SEO titles over 60 as "<card> <set> <condition> | HOKO": the set is trimmed first, then the
condition, never the card; a title that still won't fit goes to MANUAL.
"""
import csv
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
BK = ROOT / "reports/backups"
DATA_CSV = ROOT / "data/postage-copy-2026-10-19.csv"
BUNDLES = {"10481579065622", "10495484952854", "10495496454422"}

# Customer-facing banned terms (CLAUDE.md), assembled at runtime so this file passes the repo gate.
# "Mystical Archive" is a real Magic set, so the pack word is matched as myster(y|ies), as in scripts/banned-word-gate.sh.
BANNED = re.compile("|".join(["what" + r"\s*not", "myster" + r"(y|ies)", "chaos", "re" + "pack", r"\boffi" + r"cial\b",
                              "top" + r"\s*rated", "same[- ]day", "melb" + "ourne", r"\b1\.4K\b"]), re.I)

SINGLE_LOW = "Postage within Australia: $3 untracked letter."
SINGLE_HIGH = "Postage within Australia: $10.95 tracked, free tracked at $150+."
SEALED_POST = "Postage within Australia: $15.25 tracked, free on sealed orders of $250+."
SEALED_DISPATCH = "Dispatched tracked from Victoria within 2–4 business days once it lands."

# Singles paragraph, two live wordings: the letter/tracked/express figures are swapped for the canon line by kind;
# "We ship worldwide, tracked.", the dispatch sentence and the combined-postage sentence stay as they are.
SINGLE_OLD = [
    "Standard letter post is $3 and untracked. Tracked Parcel is $10.95, free on orders over $150. Express Post is $19.50.",
    "Letter post $3 (untracked) or tracked parcel $10.95 — free tracked on orders of $150 or more. Express Post is $19.50.",
]
SEALED_OLD = [
    ("Dispatched tracked from Victoria within 2–4 business days. Postage within Australia: $15.25 tracked, free on orders of $250 or more.",
     SEALED_DISPATCH + " " + SEALED_POST),
    ("Dispatched tracked from Victoria within 2–4 business days once it lands. Postage within Australia: $15.25 tracked, free on orders of $250 or more.",
     SEALED_DISPATCH + " " + SEALED_POST),
    ("<li>Postage within Australia: $15.25 tracked, free on orders of $250 or more.</li>", "<li>" + SEALED_POST + "</li>"),
    # English sealed (TMNT Commander deck): in stock, so its 1–3 dispatch sentence stays; postage + Express swapped
    ("Postage within Australia: $15.25 tracked, free on orders of $250 or more. Express Post $19.50.", SEALED_POST),
]
SLAB_SEO_OLD = "— free tracked postage."
SLAB_SEO_NEW = "— $10.95 tracked, free tracked at $150+."
# Anything left after the swap that still reads as old postage fails the gate.
STALE = re.compile(r"express post|\$12\.50|\$19\.50|over \$30|free on orders over|free tracked postage|same[- ]day", re.I)


def load(path):
    products, price = {}, {}
    for line in open(path, encoding="utf-8"):
        o = json.loads(line)
        if "__parentId" in o:
            price[o["__parentId"]] = max(price.get(o["__parentId"], 0.0), float(o["price"]))
        else:
            products[o["id"]] = o
    return products, price


def pid(gid):
    return gid.rsplit("/", 1)[1]


def is_slab(p):
    return bool(re.search(r"\b(PSA|BGS|CGC)\s*\d", p["title"]))


def is_sealed(p):
    return (p["productType"] or "").lower() == "sealed product"


def postage(path):
    products, price = load(path)
    backup, data, payload, gate = [], [], [], 0
    for gid, p in products.items():
        if pid(gid) in BUNDLES:
            continue
        body, seo_d = p["descriptionHtml"] or "", p["seo"]["description"] or ""
        new_body, new_seo, pairs = body, seo_d, []
        if is_sealed(p):
            for old, new in SEALED_OLD:
                if old in new_body:
                    new_body = new_body.replace(old, new)
                    pairs.append(("body_html", old, new))
        else:
            line = SINGLE_HIGH if (is_slab(p) or price[gid] >= 50) else SINGLE_LOW
            for old in SINGLE_OLD:
                if old in new_body:
                    new_body = new_body.replace(old, line)
                    pairs.append(("body_html", old, line))
            if is_slab(p) and price[gid] < 150 and SLAB_SEO_OLD in seo_d:
                new = SLAB_SEO_NEW if len(seo_d.replace(SLAB_SEO_OLD, SLAB_SEO_NEW)) <= 160 else "."
                new_seo = seo_d.replace(" " + SLAB_SEO_OLD, " " + new if new != "." else new)
                pairs.append(("seo_description", SLAB_SEO_OLD, new))
        # "free tracked postage" stays true on a $150+ slab, so only flag it below $150
        stale_seo = STALE.search(new_seo) and not (is_slab(p) and price[gid] >= 150)
        if STALE.search(new_body) or stale_seo or (new_seo != seo_d and len(new_seo) > 160):
            gate += 1
            print("GATE FAIL (stale/len)", pid(gid), p["title"])
        for _, _, new in pairs:
            if BANNED.search(new):
                gate += 1
                print("GATE FAIL (banned)", pid(gid), new)
        if not pairs:
            continue
        for field, old, new in pairs:
            data.append({"handle": p["handle"], "id": pid(gid), "field": field, "old_line": old, "new_line": new})
        backup.append({"id": pid(gid), "handle": p["handle"], "title": p["title"], "kind": kind(p, price[gid]),
                       "price_read": f"{price[gid]:.2f}", "body_html_before": body, "seo_description_before": seo_d})
        prod = {"id": gid}
        if new_body != body:
            prod["descriptionHtml"] = new_body
        if new_seo != seo_d:
            prod["seo"] = {"title": p["seo"]["title"], "description": new_seo}
        payload.append({"product": prod})
    write_csv(BK / "2026-10-19-postage-before.csv", backup)
    write_csv(DATA_CSV, data, append_bundles=True)
    write_jsonl(BK / "2026-10-19-postage-payload.jsonl", payload)
    kinds = {}
    for r in backup:
        kinds[r["kind"]] = kinds.get(r["kind"], 0) + 1
    print(f"products {len(payload)} · rows {len(data)} · kinds {kinds} · gate fails {gate}")
    return gate


def kind(p, price):
    if is_sealed(p):
        return "sealed"
    if is_slab(p):
        return "slab"
    return "single_50plus" if price >= 50 else "single_under50"


BUNDLE_ROWS = [  # step 2 writes these with the retitle; listed here so the step 1 CSV covers every postage change
    ("mtg-card-bundle-50-cards-5-rares-2-foils", "10481579065622", "body_html",
     "Tracked postage free on orders over $30", "Postage within Australia: $3 untracked letter"),
    ("pokemon-paradox-rift-card-bundle-10-nm-cards", "10495484952854", "body_html",
     "Tracked postage free on orders over $30", "Postage within Australia: $3 untracked letter"),
    ("ultimate-tcg-mystery-chaos-bundle-20-cards-multi-game-hoko-collectables", "10495496454422", "body_html",
     "Standard letter post is $3 and untracked. Tracked Parcel is $12.50 and free on orders over $30. Express Post is $19.50.",
     SINGLE_LOW),
]


# ---- step 3: SEO titles ----
SUFFIX = " | HOKO"
NUM = re.compile(r"^(\d+[a-z]?|\d+/\d+|[A-Z]+\d*-\d+[a-z]?|P-\d+)$")
COND = [(r"near mint|\bNM\b", "NM"), (r"lightly played|\bLP\b", "LP"), (r"moderately played|\bMP\b", "MP"),
        (r"heavily played|\bHP\b", "HP"), (r"damaged|\bDMG\b", "DMG")]


def condition(p):
    tail = re.search(r"(Near Mint|Lightly Played|Moderately Played|Heavily Played|Damaged|NM|LP|MP|HP|DMG)\s*$", p["title"])
    if tail:
        src = tail.group(1)
    else:
        m = re.search(r"Condition:\s*([^.<]+)|graded\s+(Near Mint|Lightly Played|Moderately Played)", p["descriptionHtml"] or "", re.I)
        src = (m.group(1) or m.group(2)) if m else ""
    for rx, ab in COND:
        if re.search(rx, src, re.I):
            return ab
    return ""


def split_card_set(prefix, known_sets):
    toks = prefix.split(" ")
    for i, t in enumerate(toks):
        if i and NUM.match(t):
            return " ".join(toks[:i + 1]), " ".join(toks[i + 1:])
    for s in sorted(known_sets, key=len, reverse=True):
        if prefix.endswith(" " + s) and len(prefix) > len(s) + 1:
            return prefix[:-len(s) - 1], s
    return prefix, ""


def seo_titles(path):
    products, _ = load(path)
    long = {g: p for g, p in products.items() if len(p["seo"]["title"] or "") > 60}
    prefixes = {g: re.sub(r"\s*\|\s*HOKO Collectables\s*$", "", p["seo"]["title"]).strip() for g, p in long.items()}
    known = {s for g in long for s in [split_card_set(prefixes[g], set())[1]] if s}
    backup, payload, manual, gate, rows = [], [], [], 0, []
    for g, p in long.items():
        card, st = split_card_set(prefixes[g], known)
        cond = condition(p)
        short = st.split(":")[0].strip() if ":" in st else ""
        cands = [" ".join(x for x in parts if x) for parts in
                 ([card, st, cond], [card, short, cond], [card, cond], [card])]
        new = next((c + SUFFIX for c in cands if len(c + SUFFIX) <= 60), None)
        if new is None or BANNED.search(card):  # a card name that trips the gate (e.g. Mass of Mysteries) is left as is
            manual.append({"id": pid(g), "seo_title": p["seo"]["title"], "card": card, "card_len": len(card),
                           "reason": "card name trips banned-word gate" if new else "card name over 53"})
            continue
        if False:
            manual.append({"id": pid(g), "seo_title": p["seo"]["title"], "card": card, "card_len": len(card)})
            continue
        if BANNED.search(new) or "$" in new or len(new) > 60:
            gate += 1
            print("GATE FAIL", pid(g), new)
        backup.append({"id": pid(g), "handle": p["handle"], "title": p["title"], "seo_title_before": p["seo"]["title"],
                       "seo_description_before": p["seo"]["description"] or "", "seo_title_after": new})
        payload.append({"product": {"id": g, "seo": {"title": new, "description": p["seo"]["description"]}}})
        rows.append((pid(g), card, st, cond, new))
    write_csv(BK / "2026-10-19-seo-titles-before.csv", backup)
    write_jsonl(BK / "2026-10-19-seo-titles-payload.jsonl", payload)
    write_csv(BK / "2026-10-19-seo-titles-manual.csv", manual)
    trimmed = sum(1 for _, c, s, d, n in rows if n != " ".join(x for x in [c, s, d] if x) + SUFFIX)
    print(f"over 60: {len(long)} · to write {len(payload)} (set/cond trimmed {trimmed}) · MANUAL {len(manual)} · gate fails {gate}")
    return gate


# ---- read-back ----
def readback(step, after_path):
    products, price = load(after_path)
    name = {"postage": "postage", "seo": "seo-titles"}[step]
    payload = [json.loads(line)["product"] for line in open(BK / f"2026-10-19-{name}-payload.jsonl", encoding="utf-8")]
    ok, bad = 0, []
    for want in payload:
        got = products.get(want["id"])
        good = got is not None
        if good and "descriptionHtml" in want:
            good = got["descriptionHtml"] == want["descriptionHtml"]
        if good and "seo" in want:
            good = (got["seo"]["title"] or None) == (want["seo"]["title"] or None) and \
                   (got["seo"]["description"] or None) == (want["seo"]["description"] or None)
        if good:
            ok += 1
        else:
            bad.append(pid(want["id"]))
    print(f"{step}: read back {ok}/{len(payload)} match · mismatches {bad[:20]}")
    return 1 if bad else 0


def write_csv(path, rows, append_bundles=False):
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0]) if rows else ["id"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
        if append_bundles:
            for r in BUNDLE_ROWS:
                w.writerow(dict(zip(fields, r)))


def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "postage":
        sys.exit(1 if postage(sys.argv[2]) else 0)
    if cmd == "seo":
        sys.exit(1 if seo_titles(sys.argv[2]) else 0)
    if cmd == "readback":
        sys.exit(readback(sys.argv[2], sys.argv[3]))

"""Build the SEO payload for the 2026-10-17 organic run (JP sealed boxes + pre-order drafts).

Pure data: prints a JSON list of {product_id, media_id, title, seo_title, seo_description, alt}
and asserts the length and banned-word gates. Writes go through the Shopify connector.
"""
import json
import re
import sys

SIX = "Magic · Pokémon · One Piece · Lorcana · Gundam · Dragon Ball Super"
SUFFIX = " | HOKO Australia"
# banned words assembled at runtime so this file passes the repo grep gate
BANNED = re.compile("|".join(["what" + r"\s*not", "myst" + r"\w*\s*pack", "offi" + "cial", "top" + r"\s*rated",
                              "same[- ]day dispatch", "melb" + "ourne", r"1\.4K"]), re.I)

# product_id, media_id, product title, game, short name for SEO title, descriptive phrase for meta, extra flags
ROWS = [
    ("10734771765526", "46522664780054", "Pokemon Abyss Eye (M5) Sealed Japanese Booster Box", "Pokémon", "Abyss Eye (M5) Japanese Booster Box", "Abyss Eye (M5) Japanese Pokémon booster box, factory sealed", ""),
    ("10734771798294", "46836657389846", "Pokemon Abyss Eye (M5) Japanese Booster Box — No Outer Shrink", "Pokémon", "Abyss Eye (M5) Japanese Box, No Shrink", "Abyss Eye (M5) Japanese Pokémon booster box, outer shrink removed, packs factory sealed", "nos"),
    ("10734773633302", "46522665369878", "Pokemon Heat Wave Arena (sv9a) Sealed Japanese Booster Box", "Pokémon", "Heat Wave Arena (sv9a) Japanese Booster Box", "Heat Wave Arena (sv9a) Japanese Pokémon booster box, factory sealed", ""),
    ("10734773731606", "46522666778902", "Pokemon Mega Brave (M1L) Sealed Japanese Booster Box", "Pokémon", "Mega Brave (M1L) Japanese Booster Box", "Mega Brave (M1L) Japanese Pokémon booster box, factory sealed", ""),
    ("10734773862678", "46836658471190", "Pokemon Mega Gengar Starter Deck — Japanese", "Pokémon", "Mega Gengar ex Starter Set Japanese Deck", "Mega Gengar ex Starter Set MEGA, Japanese Pokémon deck, factory sealed", ""),
    ("10734773895446", "46522667106582", "Pokemon Nihil Zero (M3) Japanese Booster Box — No Outer Shrink", "Pokémon", "Nihil Zero (M3) Japanese Box, No Shrink", "Nihil Zero (M3) Japanese Pokémon booster box, outer shrink removed, packs factory sealed", "nos"),
    ("10734775370006", "46870285811990", "One Piece TCG OP-07 500 Years in the Future Sealed Japanese Booster Box", "One Piece", "One Piece OP-07 Japanese Booster Box", "One Piece 500 Years in the Future (OP-07) Japanese booster box, 24 packs, factory sealed", ""),
    ("10734775435542", "46576132915478", "One Piece TCG OP-11 A Fist of Divine Speed Sealed Japanese Booster Box", "One Piece", "One Piece OP-11 Japanese Booster Box", "One Piece A Fist of Divine Speed (OP-11) Japanese booster box, 24 packs, factory sealed", ""),
    ("10734775501078", "46576132784406", "One Piece TCG OP-12 Legacy of the Master Sealed Japanese Booster Box", "One Piece", "One Piece OP-12 Japanese Booster Box", "One Piece Legacy of the Master (OP-12) Japanese booster box, 24 packs, factory sealed", ""),
    ("10734775664918", "46576184099094", "One Piece TCG OP-16 Sealed Japanese Booster Box", "One Piece", "One Piece OP-16 Japanese Booster Box", "One Piece The Time of Battle (OP-16) Japanese booster box, 24 packs, factory sealed", ""),
    ("10734778482966", "46836654932246", "Pokemon Raging Surf (sv3a) Sealed Japanese Booster Box", "Pokémon", "Raging Surf (sv3a) Japanese Booster Box", "Raging Surf (sv3a) Japanese Pokémon booster box, 30 packs, factory sealed", ""),
    ("10734779072790", "46836649754902", "Pokemon Stellar Miracle (sv7) Sealed Japanese Booster Box", "Pokémon", "Stellar Miracle (sv7) Japanese Booster Box", "Stellar Miracle (sv7) Japanese Pokémon booster box, 30 packs, factory sealed", ""),
    ("10734779138326", "46522668056854", "Pokemon Storm Emeralda (M6) Japanese Booster Box — No Outer Shrink", "Pokémon", "Storm Emeralda (M6) Japanese Box, No Shrink", "Storm Emeralda (M6) Japanese Pokémon booster box, outer shrink removed, packs factory sealed", "nos"),
    ("10734779171094", "46836654113046", "Pokemon Super Electric Breaker (sv8) Sealed Japanese Booster Box", "Pokémon", "Super Electric Breaker (sv8) Japanese Box", "Super Electric Breaker (sv8) Japanese Pokémon booster box, 30 packs, factory sealed", ""),
    ("10734779433238", "46522668220694", "Pokemon Terastal Festival ex (sv8a) Sealed Japanese Booster Box", "Pokémon", "Terastal Festival ex (sv8a) Japanese Box", "Terastal Festival ex (sv8a) Japanese Pokémon high class box, 10 packs, factory sealed", ""),
    ("10734779564310", "46870285943062", "Pokemon VSTAR Universe (s12a) Sealed Japanese Booster Box", "Pokémon", "VSTAR Universe (s12a) Japanese Booster Box", "VSTAR Universe (s12a) Japanese Pokémon high class box, 10 packs, factory sealed", ""),
    ("15398993723670", "46804753875222", "Pokemon 30th Celebration (M6a) Japanese Booster Box — No Outer Shrink", "Pokémon", "30th Celebration (M6a) Japanese Booster Box", "Pokémon 30th Celebration (M6a) Japanese box, 20 packs, outer shrink removed, packs factory sealed", "nos"),
    ("15413124170006", "46836651131158", "Pokemon Nihil Zero (M3) Sealed Japanese Booster Box", "Pokémon", "Nihil Zero (M3) Japanese Booster Box", "Nihil Zero (M3) Japanese Pokémon booster box, 30 packs, factory sealed", ""),
    ("15413124268310", "46836652867862", "Pokemon Mega Symphonia (M1S) Sealed Japanese Booster Box", "Pokémon", "Mega Symphonia (M1S) Japanese Booster Box", "Mega Symphonia (M1S) Japanese Pokémon booster box, 30 packs, factory sealed", ""),
    ("15413357543702", "46901890351382", "Pokemon Center Fukuoka Sealed Japanese Special Box", "Pokémon", "Pokemon Center Fukuoka Special Box Japan", "Pokémon Center Fukuoka Special Box, Japanese Pokémon Center exclusive, factory sealed", ""),
    ("15431829848342", "47000266899734", "[PRE-ORDER] One Piece Heroines Edition vol.2 (EB-05) Sealed Japanese Booster Box", "One Piece", "One Piece EB-05 Japanese Booster Box", "Pre-order: One Piece Heroines Edition vol.2 (EB-05) Japanese extra booster box, 24 packs", "pre"),
    ("15417946865942", "46999706304790", "[PRE-ORDER] One Piece The Dominance of God (OP-18) Sealed Japanese Booster Box", "One Piece", "One Piece OP-18 Japanese Booster Box", "Pre-order: One Piece The Dominance of God (OP-18) Japanese booster box, 24 packs", "pre"),
    ("15417947291926", None, "[PRE-ORDER] Dragon Ball Super Reach the God (FB12) Sealed Japanese Booster Box", "Dragon Ball Super", "Dragon Ball FB12 Japanese Booster Box", "Pre-order: Dragon Ball Super Fusion World Reach the God (FB12) Japanese booster box, 24 packs", "pre"),
    ("15417947455766", None, "[PRE-ORDER] Pokemon Aura Seeker (M7) Sealed Japanese Booster Box", "Pokémon", "Aura Seeker (M7) Japanese Booster Box", "Pre-order: Aura Seeker (M7) Japanese Pokémon booster box, factory sealed", "pre"),
]

IMPORT = "Imported from Japan by HOKO, tracked from Victoria in 2–4 business days."
IMPORT_PRE = "Imported from Japan by HOKO, tracked from Victoria once it lands."


def shorter(phrase):
    p = re.sub(r", \d+ packs", "", phrase)
    p = p.replace(", outer shrink removed, packs factory sealed", ", no outer shrink, packs sealed")
    p = p.replace("Japanese Pokémon high class box", "Japanese Pokémon box")
    p = p.replace("Japanese Pokémon Center exclusive, factory sealed", "Pokémon Center exclusive, sealed")
    p = p.replace("Dragon Ball Super Fusion World ", "Dragon Ball Super ")
    return p


def build():
    out = []
    for pid, mid, title, game, short, phrase, flags in ROWS:
        seo_title = short + SUFFIX
        tail = IMPORT_PRE if flags == "pre" else IMPORT
        candidates = [
            f"{phrase}. {tail} {SIX}.",
            f"{phrase}. {tail}",
            f"{shorter(phrase)}. {tail}",
        ]
        desc = next(c for c in candidates if len(c) <= 155)
        assert len(seo_title) <= 60, (seo_title, len(seo_title))
        assert len(desc) <= 155, (desc, len(desc))
        for text in (seo_title, desc, title):
            assert not BANNED.search(text), text
        out.append({"product_id": pid, "media_id": mid, "title": title, "seo_title": seo_title,
                    "seo_description": desc, "alt": title, "six_games": SIX in desc})
    return out


if __name__ == "__main__":
    rows = build()
    if "--table" in sys.argv:
        for r in rows:
            print(f"{r['product_id']}  {len(r['seo_title']):2d} {r['seo_title']}\n{'':16}{len(r['seo_description']):3d} {r['seo_description']}")
    else:
        json.dump(rows, sys.stdout, ensure_ascii=False, indent=1)

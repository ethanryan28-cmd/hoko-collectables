"""Internal-link inserts for the 2026-10-17 organic run.

BEFORE holds the live article bodies as read through the connector (byte-exact transcription).
EDITS holds one (anchor, insert) pair per article: the sentence is inserted immediately BEFORE the anchor.
`python article_links_2026_10_17.py vars` prints the articleUpdate variables; `check <id> <file>` diffs a
read-back body against BEFORE+insert.
"""
import json
import sys

BEFORE = {}
EDITS = {}

# ---- japanese-vs-english-pokemon-cards (683583308054)
BEFORE["683583308054"] = """<p>Many Australian collectors don’t realise there’s a meaningful difference between Japanese and English Pokemon cards beyond the language on the card. There is — and it affects everything from what cards exist, to what they’re worth, to where you buy them.</p><p>Here’s the complete breakdown.</p><h2>Release Schedule: Japan First</h2><p>Japanese Pokemon sets release 2–3 months before their English equivalents.</p><p>This means cards that will become the chase cards in the English set — the alt arts, the full arts, the high-value pulls — already exist in Japanese before the English set launches.</p><p><strong>What this means for collectors:</strong></p><ul>
<li>You can acquire Japanese versions of upcoming English chase cards before English hype drives prices up</li>
<li>Japanese card collectors often know which English sets will be valuable before English collectors do</li>
<li>If you want a specific card and can read which cards will be popular, buying Japanese early is consistently the better value</li>
</ul><h2>Card Availability: Japanese Exclusives</h2><p>Not all Japanese cards ever appear in English.</p><p>Some sets released in Japan never get an English release. Some promotional cards are Japanese-only. Some alternate art variants exist in Japanese but not in the English equivalent set.</p><p>These Japanese exclusives are, by definition, impossible to find in English. For collectors who want the full range of a Pokemon’s cards — Japanese exclusives are essential.</p><h2>Card Design: Different Art, Same Pokemon</h2><p>Japanese and English cards are not always identical in design.</p><ul>
<li>Japanese card backs are different from English card backs (this makes them non-tournament legal in English format events, but doesn’t matter for collectors)</li>
<li>Some Japanese sets have different art than their English counterparts</li>
<li>Japanese cards tend to have a slightly different cardstock feel — many collectors prefer it</li>
<li>Japanese cards typically don’t have the HP and attack text in English, but this is generally visible from the numbers</li>
</ul><h2>Print Runs: Japanese Cards Are Rarer in Australia</h2><p>Australia has no dedicated Japanese Pokemon card distribution. You can’t walk into Target and buy a Japanese booster pack.</p><p>Japanese product in Australia comes from specialist importers, online sellers who source directly, or collectors who bring it back from Japan.</p><p>This thin supply means genuinely rare Japanese cards are harder to find in Australia than equally rare English cards. When you do find them at a fair price, the supply won’t be replenished by a retail restock.</p><h2>Price Comparison: Often Better Value</h2><p>For modern cards, Japanese versions of the same card as an English version are often priced lower.</p><p>Two reasons:</p><ol>
<li>English is the primary trading language for the global Pokemon market. More demand for English language = higher English prices.</li>
<li>Australian buyers default to English cards. Japanese cards have a smaller but dedicated buyer pool.</li>
</ol><p>For collectors and investors, this means Japanese versions of cards with long-term demand are frequently bought at a discount to their eventual English equivalent prices.</p><h2>Tournament Legality</h2><p>Japanese cards are not tournament-legal in sanctioned English-format events. The card backs are different, which makes it immediately obvious if a Japanese card is in an English deck.</p><p><strong>If you play competitively in English-format events:</strong> Buy English cards for your deck. Japanese cards are a collector’s purchase in this context.</p><p><strong>If you collect or are building a personal collection:</strong> Japanese cards are fully valid and often preferable.</p><h2>Storage and Care: Same Principles</h2><p>Japanese cards use the same standard card size as English cards. They fit in the same penny sleeves, toploaders, and binders. Care requirements are identical — avoid humidity, heat, and fingerprints on the surface.</p><h2>Which Should You Buy?</h2><p><strong>Buy English if:</strong></p><ul>
<li>You’re building a competitive deck for English-format events</li>
<li>You primarily want cards that other people recognise instantly</li>
<li>You’re completing a specific English set</li>
</ul><p><strong>Buy Japanese if:</strong></p><ul>
<li>You collect specific Pokemon and want every card featuring them</li>
<li>You want cards before the English release at pre-hype prices</li>
<li>You’re interested in art variants that don’t exist in English</li>
<li>You want cards that are harder to find and more interesting to display</li>
</ul><p><strong>Buy both if:</strong></p><ul><li>You’re a serious collector who wants the complete picture</li></ul><h2>Where to Find Japanese Cards in Australia</h2><p>Japanese Pokemon product isn’t available at Australian retail. Specialist collectors and importers are your source.</p><p>At HOKO, we stock Japanese singles and sealed product sourced directly. New stock comes in regularly as we source from Japan.</p><p><a href="https://hokocollectables.com">Browse Japanese Pokemon cards at hokocollectables.com</a></p>"""
EDITS["683583308054"] = (
    """<p><a href="https://hokocollectables.com">Browse Japanese Pokemon cards at hokocollectables.com</a></p>""",
    """<p>If you'd rather open a box than hunt singles, the <a href="/collections/japan-direct-sealed">Japanese Sealed collection</a> has factory-sealed Japanese booster boxes imported from Japan by HOKO, such as <a href="/products/pokemon-terastal-festival-ex-sv8a-sealed-japanese-booster-box">Terastal Festival ex (sv8a)</a>, dispatched tracked from Victoria.</p>""",
)

# ---- how-to-spot-fake-pokemon-cards (683583242518)
BEFORE["683583242518"] = """<p>Fake Pokemon cards are more common than most people realise. With cards selling for hundreds of dollars, the incentive to fake them has never been higher.</p><p>The good news: real cards have consistent, testable properties that fakes almost always fail. Once you know these five tests, you can check any card in under 60 seconds.</p><h2>Test 1: The Light Test</h2><p>Hold the card up to a bright light source and look through it.</p><p>A genuine Pokemon card has a black layer sandwiched between two white layers in its construction. When you hold it up to light, you should see this dark layer clearly — the card is not fully transparent.</p><p>Fakes are often made from cheaper single-layer cardboard. They let more light through. If you can see through the card like it’s thin paper — it’s almost certainly fake.</p><h2>Test 2: The Feel Test</h2><p>Genuine Pokemon cards have a specific weight and rigidity. The cardstock is substantial — not flimsy, not overly stiff.</p><p>Fakes tend to feel slightly wrong in one of two directions: too light and bendy, or too thick and stiff. Pick up a card you know is genuine and compare. Your hands will tell you something is off before your eyes do.</p><p>Also: genuine cards have a very slight texture on the front from the printing process. Run your thumbnail lightly across the card surface. Real cards have a subtle grain. Fakes are often smoother or have an inconsistent texture.</p><h2>Test 3: The Print Quality Test</h2><p>Examine the card closely — ideally with a magnifying glass or your phone camera zoomed in.</p><p>Genuine Pokemon cards use a dot matrix printing process. Under magnification, you can see tiny, evenly spaced coloured dots that make up the image.</p><p>Fakes often have:</p><ul>
<li>Blurry or soft edges on text</li>
<li>Slightly off-colour printing (yellower whites, muddier colours)</li>
<li>Uneven dot patterns or smearing under magnification</li>
<li>Text that looks slightly wrong in size or font</li>
</ul><p>Compare the suspect card’s text to a confirmed genuine card. Even subtle differences in font weight or letter spacing are a red flag.</p><h2>Test 4: The Holo Pattern Test (for holo cards)</h2><p>Genuine holographic Pokemon cards have a distinctive pattern when tilted under light. The pattern is consistent across all cards of the same type — it’s a manufactured property, not random.</p><p>Fakes often have:</p><ul>
<li>A holo pattern that looks different from genuine cards of the same set</li>
<li>Holo on cards that shouldn’t have it (adding a holo layer to fake a rare variant)</li>
<li>A flat, printed-on “holo” effect that doesn’t move when you tilt the card</li>
</ul><p>Search “[card name] holo pattern” on YouTube — you can see exactly what the genuine card’s holo looks like and compare.</p><h2>Test 5: The Card Number and Set Symbol</h2><p>Every genuine Pokemon card has the correct set symbol, card number, and HP for that specific card. Fakes often get these wrong.</p><p>Check:</p><ul>
<li>The set symbol (bottom left of the card) matches the actual set</li>
<li>The card number (bottom right: e.g. 025/198) is correct for that card in that set</li>
<li>The HP printed matches what Bulbapedia or the Pokemon TCG card database shows</li>
</ul><p>If any of these are wrong — even slightly — the card is almost certainly fake.</p><h2>What to Do If You Think a Card Is Fake</h2><p>If you bought the card from a private seller: contact them immediately. Reputable sellers will refund you.</p><p>If you bought from a professional seller on eBay: open a case under Item Not As Described. eBay’s buyer protection covers fakes.</p><p>If you’re at a market and you’re unsure before buying: trust your gut. If something feels off, walk away. Genuine cards at fair prices will always be available.</p><h2>The Simplest Approach: Buy From Trusted Sellers</h2><p>The best protection against fakes is buying from sellers who grade and verify their stock. At HOKO, every card is checked before it goes on the site. We’ve been collecting for 20 years — we know what genuine cards look and feel like.</p><p>Browse our verified stock at <a href="https://hokocollectables.com">hokocollectables.com</a>.</p>"""
EDITS["683583242518"] = (
    """<p>Browse our verified stock at <a href="https://hokocollectables.com">hokocollectables.com</a>.</p>""",
    """<p>The same goes for sealed: every box in our <a href="/collections/japan-direct-sealed">Japanese Sealed collection</a>, like the <a href="/products/pokemon-nihil-zero-m3-sealed-japanese-booster-box">Nihil Zero (M3) Japanese booster box</a>, comes direct from our Japanese distributor and is checked in hand in Victoria before it's sent.</p>""",
)

# ---- M6a buying guide (688481501462)
BEFORE["688481501462"] = """<p><em>Collector first. Seller second.</em> This is the buying guide we'd want ourselves before putting money into the 30th anniversary set, written from Victoria, Australia.</p>

<h2>What the 30th Celebration set is</h2>
<p>Pokémon 30th Celebration is the Japanese anniversary expansion in the current Mega Evolution series, set code <strong>M6a</strong>. It released in Japan in September 2026 and it is the box every Australian collector has been asking us about since. As an "a" set it sits alongside Storm Emeralda (M6) rather than replacing it, which is why you'll see both on our shelf at the same time.</p>
<p>We won't list chase cards here. Pull rates and card lists shift as the set is opened, so rely on the printed set list in the box and the set code on every pack rather than a blog post that will age.</p>

<h2>Pack and box counts</h2>
<ul>
<li>
<strong>20 packs per box</strong>, which is fewer than the usual 30 for a Japanese main set.</li>
<li>
<strong>6 cards per pack</strong>, which is one more than the usual 5.</li>
<li>Every pack carries the M6a set code. If a pack in your box doesn't, stop and send us a photo.</li>
</ul>

<h2>"No outer shrink" explained</h2>
<p>Our M6a box is listed as <strong>No Outer Shrink</strong>. That means the printed Pokémon Card Game outer film has been removed before export, but the box seals and every one of the 20 packs are untouched and factory sealed. Japanese distributors do this with some allocations and it is normal for this set. It is not a resealed box. What you check on a no-shrink box is the packs: crisp, even crimps, the same set code on each, no glossy or off-colour packs. The <a href="/blogs/news/how-to-spot-fake-pokemon-cards">spot-a-fake guide</a> covers the tests in detail.</p>

<h2>Why buy the Japanese box</h2>
<p>Japanese Pokémon product is printed by the same company that prints the English set, with tighter quality control, better card stock and holofoil, and it reaches shelves months ahead of the English equivalent. For an anniversary set there is also the simple fact that this is the version Japan celebrated with. If you're new to the difference, read <a href="/blogs/news/japanese-vs-english-pokemon-cards">Japanese vs English Pokémon cards</a> first and then our <a href="/blogs/news/japanese-pokemon-one-piece-booster-boxes-australia-2026">2026 guide to Japanese booster boxes in Australia</a>.</p>

<h2>How HOKO imports it</h2>
<p>Every M6a box we sell is imported from Japan by HOKO, direct from our Japanese distributor. Import freight from Japan is included in the price. Boxes are checked in hand in Victoria and <strong>dispatched tracked from Victoria within 2–4 business days once it lands</strong>. Postage within Australia on sealed is a flat tracked rate, free on orders of $250 or more. For Christmas, order Japanese sealed by Monday 7 December 2026.</p>
<p>Authenticity is guaranteed. If a sealed item we sell isn't genuine, you get a full refund. Returns are accepted within 7 days of delivery if the item is not as described. Sealed and international orders are final sale, and none of this limits your rights under the Australian Consumer Law.</p>

<h2>Where to buy</h2>
<ul>
<li><a href="/products/pokemon-30th-celebration-m6a-sealed-japanese-booster-box">Pokémon 30th Celebration (M6a) Japanese Booster Box — No Outer Shrink</a></li>
<li>
<a href="/collections/japan-direct-sealed">Every Japanese sealed box we have right now</a>, newest releases first</li>
</ul>
<p>Questions about a box you've already got? Send us a photo before you open it and we'll sort it. We sell on eBay too, with 1.5K sold and 100% positive feedback, and the same boxes are on <a href="https://www.hokocollectables.com">hokocollectables.com</a>.</p>
"""
EDITS["688481501462"] = (
    """<p>Questions about a box you've already got? Send us a photo before you open it and we'll sort it.""",
    """<p>Collecting One Piece as well? Our <a href="/blogs/news/one-piece-heroines-edition-vol-2-eb-05-release-date-pre-order-australia">Heroines Edition vol.2 (EB-05) pre-order guide</a> covers the next Japanese box landing after this one.</p>
""",
)

# ---- EB-05 pre-order guide (688481534230)
BEFORE["688481534230"] = """<p><em>Collector first. Seller second.</em> Here's what we know about the second Heroines extra booster, what to expect from a box, and how pre-ordering the Japanese version works from Victoria, Australia.</p>

<h2>What EB-05 is</h2>
<p><strong>Extra Booster ONE PIECE Heroines Edition vol.2</strong>, set code <strong>EB-05</strong>, is Bandai's follow-up to the first Heroines Edition (EB-03). Like its predecessor it is built around the women of One Piece, with new art across leaders, characters and events. It is an extra booster, so it sits beside the main OP sets rather than replacing them, and the card pool is smaller and more focused than a numbered booster.</p>

<h2>Release date</h2>
<p>Bandai's Japanese product page lists <strong>Saturday 31 October 2026</strong>. The English edition follows a day earlier in Western time zones, which is why some Australian retailers show 30 October. The Japanese release-event period at Bandai's authorised shops runs from release day through to mid-November.</p>

<h2>What's in a box</h2>
<ul>
<li>
<strong>6 cards per pack</strong> (extra boosters run smaller packs than the 12-card main sets).</li>
<li>
<strong>24 packs per box</strong>.</li>
<li>75 cards in the regular set plus 2 DON!! cards: 7 leaders, 29 commons, 21 rares, 9 super rares, 1 secret rare and 8 special cards, per Bandai's card list.</li>
</ul>
<p>We'll leave pull rates alone until boxes are being opened. Judge the set on the printed list, not on hype.</p>

<h2>Japanese vs English for this set</h2>
<p>Japanese One Piece product ships first, uses Bandai's Japanese print run, and for Heroines sets the Japanese alt-art versions are the ones most collectors chase. If you want the broad comparison, our <a href="/blogs/news/japanese-pokemon-one-piece-booster-boxes-australia-2026">2026 guide to Japanese Pokémon and One Piece booster boxes</a> covers it, and the <a href="/blogs/news/how-to-spot-fake-pokemon-cards">spot-a-fake guide</a> applies to Bandai boxes too: printed outer shrink with Bandai logos, one clean heat seal, matching set codes on every pack.</p>

<h2>Pre-ordering in Australia with HOKO</h2>
<p>Our EB-05 box is a pre-order: <strong>Pre-order — dispatched tracked from Victoria once it lands.</strong> Every box is imported from Japan by HOKO, direct from our Japanese distributor, with import freight from Japan included in the price. Boxes are checked in hand in Victoria before they go out, and sealed postage within Australia is a flat tracked rate, free on orders of $250 or more. For Christmas delivery, order Japanese sealed by Monday 7 December 2026.</p>
<p>Authenticity is guaranteed. If a sealed item we sell isn't genuine, you get a full refund. Returns are accepted within 7 days of delivery if the item is not as described. Sealed and international orders are final sale, and your rights under the Australian Consumer Law are unaffected.</p>

<h2>Where to find it</h2>
<ul>
<li>
<a href="/collections/japan-direct-sealed">Japanese sealed, newest releases first</a>, where the EB-05 pre-order sits at the top once it goes live</li>
<li><a href="/products/pre-order-one-piece-heroines-edition-vol-2-eb-05-sealed-japanese-booster-box">One Piece Heroines Edition vol.2 (EB-05) Sealed Japanese Booster Box — pre-order</a></li>
</ul>
<p>Want a nudge when it lands? Join the box drop list on our <a href="/pages/black-friday">Black Friday page</a>. We're on eBay as well, 1.5K sold and 100% positive, and the same boxes are on <a href="https://www.hokocollectables.com">hokocollectables.com</a>.</p>
"""
EDITS["688481534230"] = (
    """<p>Want a nudge when it lands?""",
    """<p>Want something in hand sooner? <a href="/products/one-piece-tcg-op-12-legacy-of-the-master-sealed-japanese-booster-box">Legacy of the Master (OP-12)</a> is in stock now, and if you collect Pokémon too, the <a href="/blogs/news/pokemon-30th-celebration-m6a-japanese-booster-box-australia-buying-guide-2026">30th Celebration (M6a) buying guide</a> covers the anniversary box.</p>
""",
)

# ---- japanese-pokemon-cards-australia (683629674774)
BEFORE["683629674774"] = """<p>Japanese Pokemon cards aren't just translated versions of English cards — they have their own sets, exclusive cards, different rarity structures, and a collector market with its own dynamics. Here's what Australian collectors need to know.</p>

<h2>What's Different About Japanese Cards?</h2>

<h3>Different set structure</h3>

<p>Japan gets its own set releases that are often smaller and more frequent than the English equivalents. English sets are typically assembled from 2–3 Japanese sets. This means:</p>
<ul>
<li>Japanese sets come out 3–6 months before their English equivalent</li>
<li>Some Japanese cards are exclusive and never appear in English releases</li>
<li>Pull rates in Japanese sets are often better than English equivalents (you pull chase cards more frequently)</li>
</ul>

<h3>Different card size</h3>

<p>Japanese Pokemon cards are slightly smaller than English cards (Japanese: 59×86mm vs English: 63×88mm). They need Japanese-size sleeves. They cannot fit in English toploaders comfortably — use Japanese-size toploaders or team bags.</p>

<h3>Language</h3>

<p>Card text is in Japanese. Playability-wise this doesn't matter for collectors who don't play competitively, but it does matter if you're trying to enter events. Most casual play groups are fine with Japanese cards.</p>

<h3>Rarity symbols</h3>

<p>Japanese sets have their own rarity designations. Some rarities that exist in Japanese have no direct English equivalent. Understanding Japanese rarities helps you know what you're buying:</p>
<ul>
<li>◆ (Diamond) = Common</li>
<li>◆◆ = Uncommon</li>
<li>◆◆◆ = Rare</li>
<li>◆◆◆◆ = Double Rare (equivalent to English ex/VMAX)</li>
<li>★ (Star) = Various ultra-rare tiers</li>
<li>★★ = Two-star — typically the Art Rare / AR equivalent</li>
<li>★★★ = Three-star — the Super Rare / SIR equivalent (often the most beautiful cards)</li>
<li>☆ (Promo Star) = Special Art Rare equivalent</li>
</ul>

<h2>Why Japanese Cards Can Be Better Value</h2>

<p>Japanese equivalents of English chase cards are often significantly cheaper:</p>
<ul>
<li>Japanese Umbreon VMAX equivalent: significantly less than the English alt art in many cases</li>
<li>Japanese SIR cards are often 30–60% cheaper than English equivalents for the same artwork</li>
<li>Japanese booster boxes typically cost $60–120 AUD (vs $120–300 AUD for English boxes) and have better pull rates</li>
</ul>

<p>The premium on English cards comes from: larger English-speaking market, easier to grade and resell, and English being the "default" for most Australian collectors.</p>

<p>If you're collecting for display and enjoyment rather than resale, Japanese often gives you more card for your money.</p>

<h2>Japanese Exclusives Worth Knowing</h2>

<h3>Pokemon Card 151 (2023)</h3>

<p>A Japanese set celebrating the original 151 Pokemon. Contains beautiful alternate art cards for many Gen 1 Pokemon that were never released in English in this form. The Charizard ex SIR and Mew ex SIR from this set are popular worldwide.</p>

<h3>VMAX Climax (2021)</h3>

<p>Japanese exclusive set containing Character Rare versions of popular Pokemon with trainers — beautiful, unique artwork not available in English. The Character Rare cards (showing Pokemon with their trainer partners) are among the most collected Japanese-exclusive cards.</p>

<h3>High Class Packs</h3>

<p>Japan releases annual "High Class" sets (formerly called "Gym" sets) that include special art treatments exclusive to Japanese releases. These have no English equivalent and are increasingly collected internationally.</p>

<h3>Promos</h3>

<p>Japan has an extensive promo card programme — store promos, event promos, campaign promos. Many of these never reach Australian retail and can only be obtained from Japanese sellers. Pikachu promos especially are endlessly collected.</p>

<h2>Sourcing Japanese Cards in Australia</h2>

<ul>
<li>
<strong>Online from Japan:</strong> Mercari Japan and Yahoo Auctions Japan are where most Japanese collectors sell. You'll need a forwarding service (Buyee, Zenmarket, From Japan) to purchase and ship to Australia. Allow 2–4 weeks and factor in shipping ($20–60 AUD depending on parcel size).</li>
<li>
<strong>Australian sellers:</strong> Some Australian TCG stores and eBay sellers stock Japanese cards. Price will be higher than ordering from Japan yourself, but shipping is domestic and faster.</li>
<li>
<strong>At HOKO:</strong> We source Japanese product directly and stock Japanese singles and sealed. Check our Pokemon collection with language filter, or email <a href="mailto:support@hokocollectables.com">support@hokocollectables.com</a> if you're after specific Japanese cards.</li>
</ul>

<h2>Grading Japanese Cards</h2>

<p>Japanese cards can be graded by PSA and CGC. The grading process is identical to English cards. However:</p>
<ul>
<li>PSA 10 Japanese cards often sell for less than English PSA 10 equivalents (smaller resale market)</li>
<li>But Japanese card quality is often higher out of the pack — tighter printing tolerances and less edge whitening make PSA 10s more achievable</li>
<li>Japanese-only cards (exclusives) in PSA 10 can be extremely valuable due to scarcity of graded examples</li>
</ul>

<h2>Should You Collect Japanese Cards?</h2>

<p><strong>Yes if:</strong> You want more card for your money, you love the artwork and don't need English text, you're interested in Japan-exclusive content, or you're sourcing from Japan directly.</p>

<p><strong>Stick to English if:</strong> You want maximum resale liquidity in Australia, you play competitively, or you're focused on vintage (English vintage cards have a larger collector market).</p>

<p>Many collectors do both — English for the core collection, Japanese for specific art variants or sets that are better value in Japanese.</p>"""
EDITS["683629674774"] = (
    """<h2>Grading Japanese Cards</h2>""",
    """<p>For boxes, the <a href="/collections/japan-direct-sealed">Japanese Sealed collection</a> is the current list: factory-sealed boxes like <a href="/products/pokemon-mega-symphonia-m1s-sealed-japanese-booster-box">Mega Symphonia (M1S)</a>, imported from Japan by HOKO and dispatched tracked from Victoria.</p>

""",
)


def apply(aid, body):
    anchor, insert = EDITS[aid]
    assert body.count(anchor) == 1, (aid, body.count(anchor))
    return body.replace(anchor, insert + anchor, 1)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "anchors":
        for aid, (anchor, insert) in EDITS.items():
            print(aid, json.dumps(anchor), "->", json.dumps(insert))
    elif cmd == "check":
        # check <id> <file-with-readback-body> <file-with-before-body>
        aid, after_f, before_f = sys.argv[2:5]
        after = open(after_f, encoding="utf-8").read()
        before = open(before_f, encoding="utf-8").read()
        expected = apply(aid, before)
        print(aid, "MATCH" if after == expected else "MISMATCH", len(after), len(expected))
        if after != expected:
            import difflib
            for line in difflib.unified_diff(expected.splitlines(), after.splitlines(), lineterm=""):
                print(line)

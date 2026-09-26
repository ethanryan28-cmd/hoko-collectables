# Storybook — FormFinder progress log

A dated, screenshot-driven record of FormFinder app progress. One entry per
session/build worth remembering, each with the screenshots that prompted it.

**Not a HOKO Collectables doc.** FormFinder is a separate product (Australian
government form finder). This log lives here because it's the repo the owner
works out of from his phone. The marketing site is its own repo,
`ethanryan28-cmd/formfinder-landing` — the app itself is elsewhere.

---

## Entries

| Date | Entry | Covers |
|---|---|---|
| 2026-09-26 | [`2026-09-26-org-connect.md`](2026-09-26-org-connect.md) | Org space screen (connected state, reference code, suggested forms) + home screen org card |

---

## How to add an entry

1. Drop the screenshots in `images/` named `YYYY-MM-DD-<screen>.png`.
2. Create `YYYY-MM-DD-<topic>.md` using the structure of the existing entry:
   - **What's on screen** — one section per screenshot, describing only what is
     visibly there. Quote UI copy exactly.
   - **What this shows working** — the behaviour the screens demonstrate.
   - **Open questions / next** — anything unresolved, marked as a question, not
     a claim.
3. Add a row to the table above.

**Rule:** record only what the screenshots actually show. Don't infer backend
behaviour, data models, or roadmap from a UI screenshot — if it isn't on
screen, it goes under *Open questions*, not *What this shows working*.

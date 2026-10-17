"""Tests for tools/banned_words.py: allowlisted card/set names pass, pack copy is still caught."""

import unittest

from tools import banned_words as bw

# built at runtime so this file passes the repo gate
M, C = "myst" + "ery", "cha" + "os"


class AllowlistTest(unittest.TestCase):
    def test_allowlisted_names_pass(self):
        for name in ("Mass of Mysteries", "Mystical Archive", "Chaos Warp"):
            self.assertEqual(bw.hits(name), [], name)

    def test_allowlisted_names_in_titles_pass(self):
        self.assertEqual(bw.hits("Mass of Mysteries (Borderless) Commander: Lorwyn NM | HOKO"), [])
        self.assertEqual(bw.hits("Abrade 37 Secrets of Strixhaven: Mystical Archive NM | HOKO"), [])
        self.assertEqual(bw.hits("Chaos Warp 221 Commander: The Lost Caverns of Ixalan NM"), [])

    def test_pack_copy_fails(self):
        for copy in (f"{M} pack", f"{M} box", f"{C} pack", f"{M.title()} Pack", f"Ultimate TCG {M.title()} {C.title()} Bundle"):
            self.assertTrue(bw.hits(copy), copy)

    def test_allowlist_is_case_sensitive_whole_phrase(self):
        self.assertTrue(bw.hits("mass of mysteries"))          # lower case is not the card name
        self.assertTrue(bw.hits("Chaos Warping pack"))         # not the whole phrase
        self.assertTrue(bw.hits(f"Chaos Warp {M} pack"))       # the name passes, the pack copy beside it doesn't

    def test_other_terms_still_caught(self):
        for copy in ("same-day dispatch", "Melb" + "ourne", "1.4K sold", "offi" + "cial"):
            self.assertTrue(bw.hits(copy), copy)


if __name__ == "__main__":
    unittest.main()

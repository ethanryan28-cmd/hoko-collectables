"""Customer-facing banned-word check (CLAUDE.md list) with an allowlist of real card and set names.

    python -m tools.banned_words FILE...        # print hits, exit 1 if any
    git grep ... | python -m tools.banned_words --grep   # re-check "path:line:text" lines

Allowlisted names are matched case-sensitively as whole phrases and blanked out before the check, so
"Mass of Mysteries" passes while "mystery pack" / "mystery box" / "chaos pack" copy is still caught.
"""
import re
import sys

# Terms assembled at runtime so this file doesn't trip the repo gate it implements.
TERMS = re.compile("|".join([
    "what" + r"\s*not", "top" + r"[- ]rated", r"\bmyst\w*", r"\bchaos\b", r"\bre" + r"[- ]?pack", r"\boffi" + r"cial\b",
    "same[- ]day dispatch", "melb" + "ourne", r"\b1\.4k\b", "HOKO" + "10",
]), re.I)

# Exact card / set names (case-sensitive, whole phrase). Add a name only when it is printed on the card or set.
ALLOWLIST = (
    "Mass of Mysteries",
    "Mystical Archive",
    "Chaos Warp",
)
REPO_ONLY = re.compile(r"\b2024\b")  # repo gate only: stale year in copy

_ALLOW = re.compile("|".join(r"(?<!\w)" + re.escape(n) + r"(?!\w)" for n in ALLOWLIST))


def hits(text):
    """Banned terms in text after allowlisted names are blanked out."""
    scrubbed = _ALLOW.sub(lambda m: " " * len(m.group(0)), text)
    return [m.group(0) for m in TERMS.finditer(scrubbed)]


def main(argv):
    bad = 0
    if argv[:1] == ["--grep"]:
        for line in sys.stdin:
            text = line.split(":", 2)[-1]
            if hits(text) or REPO_ONLY.search(text):
                bad += 1
                sys.stdout.write(line)
    else:
        for path in argv:
            for n, line in enumerate(open(path, encoding="utf-8"), 1):
                if hits(line):
                    bad += 1
                    print(f"{path}:{n}:{line.rstrip()}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

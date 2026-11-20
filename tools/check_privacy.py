#!/usr/bin/env python3
"""Refuse to publish text that looks like personal data.

Scans git-tracked text files (or the paths given) for Korean phone numbers,
resident registration numbers and e-mail addresses. A safety net only: raw
interview and measurement data must never enter the repository at all
(docs/privacy.md). Images are not scanned -- strip EXIF and check faces by hand.

Usage: python3 tools/check_privacy.py [paths...]     exit 1 on any hit
"""
import re
import subprocess
import sys
from pathlib import Path

PATTERNS = {
    "phone": re.compile(r"(?<!\d)01[016789][-. ]?\d{3,4}[-. ]?\d{4}(?!\d)"),
    "resident-id": re.compile(r"(?<!\d)\d{6}-[1-8]\d{6}(?!\d)"),
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
}
# Addresses that are allowed to appear (licence texts, placeholders, bots).
ALLOWED_EMAIL = re.compile(r"(@example\.(com|org)|noreply@|@users\.noreply\.github\.com)$")
SKIP = {"LICENSE", "tools/LICENSE"}
TEXT_SUFFIXES = {".md", ".csv", ".txt", ".scad", ".py", ".yml", ".yaml", ".json", ".svg", ""}


def tracked_files():
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True)
    return [p for p in out.stdout.splitlines() if p]


def scan(paths):
    hits = []
    for p in paths:
        if p in SKIP or Path(p).suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = Path(p).read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
            continue
        for lineno, line in enumerate(text.splitlines(), 1):
            for kind, rx in PATTERNS.items():
                for m in rx.finditer(line):
                    if kind == "email" and ALLOWED_EMAIL.search(m.group(0)):
                        continue
                    hits.append((p, lineno, kind, m.group(0)))
    return hits


def main(argv):
    paths = argv[1:] or tracked_files()
    hits = scan(paths)
    for p, lineno, kind, value in hits:
        print(f"{p}:{lineno}: possible {kind}: {value}")
    if hits:
        print(f"\n{len(hits)} possible personal-data hit(s). Remove them before committing.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

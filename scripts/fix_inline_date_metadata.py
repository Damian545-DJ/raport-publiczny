#!/usr/bin/env python3
"""Split inline date metadata into modification and source-verification rows."""

from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE_RE = r"\d{4}-\d{2}-\d{2}"

LANGUAGES = {
    "pl": {
        "labels": ("Ostatnia aktualizacja", "Ostatnia zmiana"),
        "modified": "Ostatnia zmiana",
        "verified": "Ostatnia weryfikacja źródeł",
    },
    "en": {
        "labels": ("Last updated", "Last update", "Last modified"),
        "modified": "Last modified",
        "verified": "Sources last verified",
    },
    "nl": {
        "labels": ("Laatst bijgewerkt", "Laatste update", "Laatst gewijzigd"),
        "modified": "Laatst gewijzigd",
        "verified": "Bronnen laatst geverifieerd",
    },
}


def language_of(text: str) -> str | None:
    match = re.search(r'<html\b[^>]*\blang=["\'](pl|en|nl)["\']', text, re.IGNORECASE)
    return match.group(1).lower() if match else None


def normalize_file(path: Path, last_modified: str, sources_verified: str) -> bool:
    text = path.read_text(encoding="utf-8")
    language = language_of(text)
    if language not in LANGUAGES:
        return False

    config = LANGUAGES[language]
    labels = "|".join(re.escape(label) for label in config["labels"])
    pattern = re.compile(
        rf'(?P<indent>[ \t]*)<p\s+class=["\']meta["\']>'
        rf'<strong>(?:{labels}):</strong>\s*{DATE_RE}'
        rf'\s*·\s*(?P<suffix>.*?)</p>',
        re.IGNORECASE,
    )

    def replacement(match: re.Match[str]) -> str:
        indent = match.group("indent")
        suffix = match.group("suffix").strip()
        return (
            f'{indent}<p class="meta"><strong>{config["modified"]}:</strong> {last_modified}</p>\n'
            f'{indent}<p class="meta"><strong>{config["verified"]}:</strong> {sources_verified}</p>\n'
            f'{indent}<p class="meta">{suffix}</p>'
        )

    updated, count = pattern.subn(replacement, text)
    if count and updated != text:
        path.write_text(updated, encoding="utf-8", newline="\n")
        print(f"Inline HTML metadata: {path.relative_to(ROOT)} ({count} field(s) normalized)")
        return True
    return False


def main() -> None:
    last_modified = os.environ.get("LAST_MODIFIED", "2026-07-14")
    sources_verified = os.environ.get("SOURCES_VERIFIED", "2026-07-11")

    for value, name in ((last_modified, "LAST_MODIFIED"), (sources_verified, "SOURCES_VERIFIED")):
        if not re.fullmatch(DATE_RE, value):
            raise SystemExit(f"{name} must use YYYY-MM-DD format, got: {value!r}")

    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" not in path.parts:
            changed += int(normalize_file(path, last_modified, sources_verified))

    print(f"Completed inline metadata normalization. Files changed: {changed}")


if __name__ == "__main__":
    main()

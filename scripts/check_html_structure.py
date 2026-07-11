#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys
from dataclasses import dataclass

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE_URL = "https://damian545-dj.github.io/raport-publiczny/"

EXPECTED_HTML = {
    "pl": {
        "index.html",
        "najwazniejsze-ustalenia.html",
        "timeline.html",
        "dowody.html",
        "media.html",
        "dla-instytucji.html",
        "home-of-people.html",
    },
    "en": {
        "index.html",
        "key-findings.html",
        "timeline.html",
        "dowody.html",
        "media.html",
        "for-institutions.html",
        "home-of-people.html",
    },
    "nl": {
        "index.html",
        "belangrijkste-bevindingen.html",
        "timeline.html",
        "dowody.html",
        "media.html",
        "voor-instanties.html",
        "home-of-people.html",
    },
}

HREFLANG_GROUPS = [
    ("pl/index.html", "en/index.html", "nl/index.html"),
    ("pl/najwazniejsze-ustalenia.html", "en/key-findings.html", "nl/belangrijkste-bevindingen.html"),
    ("pl/timeline.html", "en/timeline.html", "nl/timeline.html"),
    ("pl/dowody.html", "en/dowody.html", "nl/dowody.html"),
    ("pl/media.html", "en/media.html", "nl/media.html"),
    ("pl/dla-instytucji.html", "en/for-institutions.html", "nl/voor-instanties.html"),
    ("pl/home-of-people.html", "en/home-of-people.html", "nl/home-of-people.html"),
]
HREFLANG_LOOKUP = {path: group for group in HREFLANG_GROUPS for path in group}

REQUIRED_META = (
    r'<meta\s+name="description"\s+content="[^"]+"\s*/?>',
    r'<meta\s+property="og:title"\s+content="[^"]+"\s*/?>',
    r'<meta\s+property="og:description"\s+content="[^"]+"\s*/?>',
    r'<meta\s+property="og:url"\s+content="[^"]+"\s*/?>',
    r'<meta\s+property="og:image"\s+content="(?:https://|/raport-publiczny/)[^"]+"\s*/?>',
)


@dataclass
class HtmlError:
    file: pathlib.Path
    message: str


def count(pattern: str, text: str) -> int:
    return len(re.findall(pattern, text, flags=re.IGNORECASE | re.DOTALL))


def check_expected_files(errors: list[HtmlError]) -> None:
    for lang, expected in EXPECTED_HTML.items():
        lang_dir = ROOT / lang
        actual = {p.name for p in lang_dir.glob("*.html")}
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        for name in missing:
            errors.append(HtmlError(lang_dir / name, "missing expected language HTML file"))
        for name in extra:
            errors.append(HtmlError(lang_dir / name, "extra HTML file in language directory; check if it is needed"))


def check_html_file(path: pathlib.Path, lang: str, errors: list[HtmlError]) -> None:
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8", errors="ignore")

    required_pairs = [
        (r"<!DOCTYPE html>", "missing <!DOCTYPE html>"),
        (rf'<html\s+lang="{lang}">', f'missing or wrong <html lang="{lang}">'),
        (r"<head>", "missing <head>"),
        (r"</head>", "missing </head>"),
        (r"<body>", "missing <body>"),
        (r"</body>", "missing </body>"),
        (r"</html>", "missing </html>"),
        (r"<title>[^<]+</title>", "missing non-empty <title>"),
        (rf'<link\s+rel="canonical"\s+href="{re.escape(BASE_URL + rel)}"\s*/?>', "missing or wrong canonical URL"),
    ]

    for pattern, message in required_pairs:
        if not re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(HtmlError(path, message))

    for pattern in REQUIRED_META:
        if not re.search(pattern, text, flags=re.IGNORECASE):
            errors.append(HtmlError(path, f"missing required SEO/Open Graph tag matching: {pattern}"))

    if count(r"<h1\b", text) != 1:
        errors.append(HtmlError(path, "page should contain exactly one <h1>"))

    if count(r"<title>", text) != 1:
        errors.append(HtmlError(path, "page should contain exactly one <title>"))

    if count(r'<meta\s+name="description"', text) != 1:
        errors.append(HtmlError(path, "page should contain exactly one meta description"))

    group = HREFLANG_LOOKUP.get(rel)
    if group:
        for code, target in zip(("pl", "en", "nl"), group):
            expected = BASE_URL + target
            pattern = rf'<link\s+rel="alternate"\s+hreflang="{code}"\s+href="{re.escape(expected)}"\s*/?>'
            if not re.search(pattern, text, flags=re.IGNORECASE):
                errors.append(HtmlError(path, f"missing hreflang {code} -> {expected}"))

    if "href=\"#" in text:
        for anchor in re.findall(r'href="#([^"]+)"', text):
            if not re.search(rf'id="{re.escape(anchor)}"', text):
                errors.append(HtmlError(path, f"anchor link #{anchor} has no matching id"))


def main() -> int:
    errors: list[HtmlError] = []
    check_expected_files(errors)

    for lang in EXPECTED_HTML:
        for path in sorted((ROOT / lang).glob("*.html")):
            check_html_file(path, lang, errors)

    if errors:
        print("HTML structure check failed:")
        for err in errors:
            rel = err.file.relative_to(ROOT).as_posix()
            print(f" - {rel}: {err.message}")
        print(f"\nSummary: {len(errors)} error(s) found")
        return 1

    total = sum(len(files) for files in EXPECTED_HTML.values())
    print(f"OK: checked {total} PL/EN/NL HTML file(s) for structure, SEO tags and duplicate/extra language pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
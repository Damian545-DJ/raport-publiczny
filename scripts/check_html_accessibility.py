#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTECTED_BLOCK = re.compile(r"<!--.*?-->|<(?:script|style)\b.*?</(?:script|style)>", re.I | re.S)
RAW_AMP = re.compile(r"&(?!#\d+;|#x[0-9a-fA-F]+;|[A-Za-z][A-Za-z0-9]+;)")


@dataclass(frozen=True)
class Issue:
    file: str
    message: str


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def add(issues: list[Issue], path: Path | str, message: str) -> None:
    issues.append(Issue(rel(path) if isinstance(path, Path) else path, message))


def markup_without_protected_blocks(text: str) -> str:
    return PROTECTED_BLOCK.sub("", text)


def check_html(path: Path, issues: list[Issue]) -> None:
    text = path.read_text(encoding="utf-8")
    clean = markup_without_protected_blocks(text)

    mains = re.findall(r"<main\b[^>]*>", clean, re.I)
    if len(mains) != 1:
        add(issues, path, f"must contain exactly one <main>; found {len(mains)}")
    elif not re.search(r'<main\b[^>]*\bid=["\']main-content["\']', mains[0], re.I):
        add(issues, path, "main landmark must use id=main-content")

    skip_links = re.findall(
        r'<a\b[^>]*\bclass=["\'][^"\']*\bskip-link\b[^"\']*["\'][^>]*\bhref=["\']#main-content["\'][^>]*>',
        clean,
        re.I,
    )
    if len(skip_links) != 1:
        add(issues, path, f"must contain exactly one skip link to #main-content; found {len(skip_links)}")

    footers = re.findall(r"<footer\b[^>]*>", clean, re.I)
    if len(footers) != 1:
        add(issues, path, f"must contain exactly one real <footer>; found {len(footers)}")

    for nav in re.findall(r"<nav\b[^>]*>", clean, re.I):
        if not re.search(r"\baria-label=|\baria-labelledby=", nav, re.I):
            add(issues, path, f"navigation landmark has no accessible name: {nav[:100]}")

    for element in re.findall(r"<(?:div|span)\b[^>]*\baria-label=[^>]*>", clean, re.I):
        if not re.search(r"\brole=", element, re.I):
            add(issues, path, f"generic element uses aria-label without role: {element[:100]}")

    raw_amp = RAW_AMP.search(clean)
    if raw_amp:
        line = clean.count("\n", 0, raw_amp.start()) + 1
        add(issues, path, f"raw ampersand must be encoded as &amp; near line {line}")

    if "accessibility.css" not in text:
        add(issues, path, "missing shared accessibility stylesheet")

    if path.name == "doc.html":
        if re.search(r"<(?:meta|link)\b[^>]*\s/>", text, re.I):
            add(issues, path, "doc.html still uses XHTML-style closing slashes on HTML void elements")
        if re.search(r'<article\b[^>]*\bid=["\']content["\']', text, re.I):
            add(issues, path, "doc.html must use the main landmark instead of an article placeholder")
        if 'getElementById("content")' in text:
            add(issues, path, "doc.html JavaScript still targets the removed content id")


def main() -> int:
    issues: list[Issue] = []
    html_files = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)

    for path in html_files:
        check_html(path, issues)

    css_path = ROOT / "assets" / "public-polish.css"
    css = css_path.read_text(encoding="utf-8")
    if re.search(r"body::after", css):
        add(issues, css_path, "legal information must not be generated through body::after")

    if issues:
        print("HTML accessibility audit failed:")
        for issue in sorted(issues, key=lambda item: (item.file, item.message)):
            print(f" - {issue.file}: {issue.message}")
        print(f"\nSummary: {len(issues)} issue(s) found")
        return 1

    print(
        "OK: checked "
        f"{len(html_files)} HTML file(s) for main landmarks, skip links, named navigation, "
        "real footers, ARIA use, encoded ampersands and doc-viewer markup"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
from __future__ import annotations

import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from urllib.parse import parse_qs, urlparse

ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE_URL = "https://damian545-dj.github.io/raport-publiczny/"
SITEMAP_NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}

STATIC_PUBLIC_URLS = {
    BASE_URL,
    BASE_URL + "press.html",
    BASE_URL + "sezer-duygulu/",
    BASE_URL + "pl/index.html",
    BASE_URL + "pl/najwazniejsze-ustalenia.html",
    BASE_URL + "pl/timeline.html",
    BASE_URL + "pl/dowody.html",
    BASE_URL + "pl/media.html",
    BASE_URL + "pl/dla-instytucji.html",
    BASE_URL + "pl/sezer-duygulu.html",
    BASE_URL + "en/index.html",
    BASE_URL + "en/key-findings.html",
    BASE_URL + "en/timeline.html",
    BASE_URL + "en/dowody.html",
    BASE_URL + "en/media.html",
    BASE_URL + "en/for-institutions.html",
    BASE_URL + "en/sezer-duygulu.html",
    BASE_URL + "nl/index.html",
    BASE_URL + "nl/belangrijkste-bevindingen.html",
    BASE_URL + "nl/timeline.html",
    BASE_URL + "nl/dowody.html",
    BASE_URL + "nl/media.html",
    BASE_URL + "nl/voor-instanties.html",
    BASE_URL + "nl/sezer-duygulu.html",
}

DOC_FILES = {
    "README.pl.md",
    "README.en.md",
    "README.nl.md",
    "TIMELINE.pl.md",
    "TIMELINE.en.md",
    "TIMELINE.nl.md",
    "EVIDENCE_INDEX.pl.md",
    "EVIDENCE_INDEX.en.md",
    "EVIDENCE_INDEX.nl.md",
    "ALLEGATIONS_AND_LAW.pl.md",
    "ALLEGATIONS_AND_LAW.en.md",
    "ALLEGATIONS_AND_LAW.nl.md",
    "ANONYMIZATION.pl.md",
    "ANONYMIZATION.en.md",
    "ANONYMIZATION.nl.md",
    "DISCLAIMER.pl.md",
    "DISCLAIMER.en.md",
    "DISCLAIMER.nl.md",
    "CONTRIBUTING.pl.md",
    "CONTRIBUTING.en.md",
    "CONTRIBUTING.nl.md",
    "UPDATES.md",
    "CODE_OF_CONDUCT.md",
    "sezer-duygulu/README.pl.md",
    "sezer-duygulu/README.en.md",
    "sezer-duygulu/README.nl.md",
}

EXPECTED_DOC_URLS = {BASE_URL + "doc.html?file=" + file for file in DOC_FILES}


@dataclass
class AuditIssue:
    file: str
    message: str


def read_text(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def add(issues: list[AuditIssue], file: str, message: str) -> None:
    issues.append(AuditIssue(file, message))


def rel(path: pathlib.Path) -> str:
    return path.relative_to(ROOT).as_posix()


def extract_attr(tag: str, attr: str) -> str | None:
    m = re.search(rf'{attr}\s*=\s*"([^"]*)"', tag, flags=re.IGNORECASE)
    return m.group(1) if m else None


def check_robots(issues: list[AuditIssue]) -> None:
    path = ROOT / "robots.txt"
    if not path.exists():
        add(issues, "robots.txt", "missing robots.txt")
        return
    text = read_text(path)
    if "User-agent: *" not in text:
        add(issues, "robots.txt", "missing User-agent: *")
    if "Allow: /" not in text:
        add(issues, "robots.txt", "missing Allow: /")
    if f"Sitemap: {BASE_URL}sitemap.xml" not in text:
        add(issues, "robots.txt", "missing correct sitemap URL")


def check_sitemap(issues: list[AuditIssue]) -> None:
    path = ROOT / "sitemap.xml"
    if not path.exists():
        add(issues, "sitemap.xml", "missing sitemap.xml")
        return
    try:
        tree = ET.parse(path)
    except ET.ParseError as exc:
        add(issues, "sitemap.xml", f"invalid XML: {exc}")
        return

    locs = [el.text.strip() for el in tree.findall(".//sm:loc", SITEMAP_NS) if el.text and el.text.strip()]
    loc_set = set(locs)
    if len(locs) != len(loc_set):
        add(issues, "sitemap.xml", "duplicate <loc> entries found")

    required = STATIC_PUBLIC_URLS | EXPECTED_DOC_URLS
    for url in sorted(required - loc_set):
        add(issues, "sitemap.xml", f"missing sitemap URL: {url}")

    # Avoid indexing a duplicate root representation when canonical is BASE_URL.
    if BASE_URL + "index.html" in loc_set:
        add(issues, "sitemap.xml", "contains duplicate root URL /index.html; use canonical root URL instead")

    for url in locs:
        if not url.startswith(BASE_URL):
            add(issues, "sitemap.xml", f"URL outside base domain: {url}")
        parsed = urlparse(url)
        if parsed.query:
            file_values = parse_qs(parsed.query).get("file", [])
            if file_values:
                file_path = file_values[0]
                if not (ROOT / file_path).is_file():
                    add(issues, "sitemap.xml", f"doc URL points to missing file: {file_path}")


def check_html_quality(issues: list[AuditIssue]) -> None:
    html_files = [p for p in ROOT.rglob("*.html") if ".git" not in p.parts]
    canonical_values: dict[str, str] = {}

    for path in html_files:
        path_rel = rel(path)
        text = read_text(path)

        if not re.search(r"<!doctype html>", text, flags=re.IGNORECASE):
            add(issues, path_rel, "missing <!doctype html>")
        if not re.search(r"<html\s+[^>]*lang=\"[a-z]{2}\"", text, flags=re.IGNORECASE):
            add(issues, path_rel, "missing two-letter html lang attribute")
        if not re.search(r"<meta\s+name=\"viewport\"", text, flags=re.IGNORECASE):
            add(issues, path_rel, "missing viewport meta tag")
        if len(re.findall(r"<title>", text, flags=re.IGNORECASE)) != 1:
            add(issues, path_rel, "must contain exactly one title tag")
        if len(re.findall(r"<h1\b", text, flags=re.IGNORECASE)) > 1:
            add(issues, path_rel, "contains more than one h1")
        if not re.search(r"<meta\s+name=\"description\"\s+content=\"[^\"]{50,220}\"", text, flags=re.IGNORECASE):
            add(issues, path_rel, "missing or weak meta description")

        canonical_match = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)"\s*/?>', text, flags=re.IGNORECASE)
        if canonical_match:
            canonical = canonical_match.group(1)
            if not canonical.startswith(BASE_URL):
                add(issues, path_rel, "canonical URL is outside the site base")
            if canonical in canonical_values:
                add(issues, path_rel, f"canonical URL duplicates {canonical_values[canonical]}")
            else:
                canonical_values[canonical] = path_rel
        elif path_rel != "doc.html":
            add(issues, path_rel, "missing canonical URL")

        for tag in re.findall(r"<img\b[^>]*>", text, flags=re.IGNORECASE):
            alt = extract_attr(tag, "alt")
            if alt is None:
                add(issues, path_rel, "image without alt attribute")

        for tag in re.findall(r"<a\b[^>]*>", text, flags=re.IGNORECASE):
            href = extract_attr(tag, "href")
            if href is None or href.strip() == "":
                add(issues, path_rel, "empty anchor href")
            target = extract_attr(tag, "target")
            if target == "_blank":
                rel_attr = (extract_attr(tag, "rel") or "").lower()
                if "noopener" not in rel_attr:
                    add(issues, path_rel, "target=_blank link without rel=noopener")

        # Insecure http links are not allowed, except standard sitemap namespace declarations.
        if re.search(r'(?<!xmlns=)"http://', text, flags=re.IGNORECASE):
            add(issues, path_rel, "contains insecure http:// URL")


def main() -> int:
    issues: list[AuditIssue] = []
    check_robots(issues)
    check_sitemap(issues)
    check_html_quality(issues)

    if issues:
        print("Complete site quality audit failed:")
        for issue in sorted(issues, key=lambda i: (i.file, i.message)):
            print(f" - {issue.file}: {issue.message}")
        print(f"\nSummary: {len(issues)} issue(s) found")
        return 1

    print("OK: complete site quality audit passed: sitemap, robots, HTML basics, accessibility, canonical URLs, and safe external-link handling")
    return 0


if __name__ == "__main__":
    sys.exit(main())

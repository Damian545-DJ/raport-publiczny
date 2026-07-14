#!/usr/bin/env python3
"""Synchronize visible modification and source-verification dates.

The script updates only explicit metadata labels in PL/EN/NL HTML and
Markdown files. Historical dates occurring in the substantive content are
left unchanged.
"""

from __future__ import annotations

import os
import re
from pathlib import Path

DATE_RE = r"\d{4}-\d{2}-\d{2}"
ROOT = Path(__file__).resolve().parents[1]

LANGUAGES = {
    "pl": {
        "update_labels": (
            "Ostatnia aktualizacja",
            "Ostatnia zmiana",
        ),
        "verification_labels": (
            "Ostatnia weryfikacja źródeł",
            "Weryfikacja źródeł",
            "Źródła ostatnio zweryfikowano",
        ),
        "output_update": "Ostatnia zmiana",
        "output_verification": "Ostatnia weryfikacja źródeł",
        "output_verification_short": "Weryfikacja źródeł",
    },
    "en": {
        "update_labels": (
            "Last updated",
            "Last update",
            "Last modified",
        ),
        "verification_labels": (
            "Sources last verified",
            "Last source verification",
            "Source verification",
        ),
        "output_update": "Last modified",
        "output_verification": "Sources last verified",
        "output_verification_short": "Sources verified",
    },
    "nl": {
        "update_labels": (
            "Laatst bijgewerkt",
            "Laatste update",
            "Laatst gewijzigd",
        ),
        "verification_labels": (
            "Bronnen laatst geverifieerd",
            "Laatste bronverificatie",
            "Bronverificatie",
        ),
        "output_update": "Laatst gewijzigd",
        "output_verification": "Bronnen laatst geverifieerd",
        "output_verification_short": "Bronnen geverifieerd",
    },
}


def replace_matches(text: str, pattern: re.Pattern[str], replacement_factory) -> tuple[str, int]:
    matches = list(pattern.finditer(text))
    if not matches:
        return text, 0

    parts: list[str] = []
    cursor = 0
    for index, match in enumerate(matches):
        parts.append(text[cursor : match.start()])
        if index == 0:
            parts.append(replacement_factory(match))
        cursor = match.end()
    parts.append(text[cursor:])
    return "".join(parts), len(matches)


def html_language(text: str) -> str | None:
    match = re.search(r'<html\b[^>]*\blang=["\'](pl|en|nl)["\']', text, re.IGNORECASE)
    return match.group(1).lower() if match else None


def update_html(path: Path, last_modified: str, sources_verified: str) -> bool:
    text = path.read_text(encoding="utf-8")
    language = html_language(text)
    if language not in LANGUAGES:
        return False

    config = LANGUAGES[language]
    all_labels = config["update_labels"] + config["verification_labels"]
    labels_pattern = "|".join(re.escape(label) for label in all_labels)
    total_fields = 0

    meta_pattern = re.compile(
        rf'(?P<indent>[ \t]*)<p\s+class=["\']meta["\']><strong>(?:{labels_pattern}):</strong>\s*{DATE_RE}</p>',
        re.IGNORECASE,
    )

    def meta_replacement(match: re.Match[str]) -> str:
        indent = match.group("indent")
        return (
            f'{indent}<p class="meta"><strong>{config["output_update"]}:</strong> {last_modified}</p>\n'
            f'{indent}<p class="meta"><strong>{config["output_verification"]}:</strong> {sources_verified}</p>'
        )

    text, count = replace_matches(text, meta_pattern, meta_replacement)
    total_fields += count

    plain_pattern = re.compile(
        rf'(?P<indent>[ \t]*)<p><strong>(?:{labels_pattern}):</strong>\s*{DATE_RE}</p>',
        re.IGNORECASE,
    )

    def plain_replacement(match: re.Match[str]) -> str:
        indent = match.group("indent")
        return (
            f'{indent}<p><strong>{config["output_update"]}:</strong> {last_modified}</p>\n'
            f'{indent}<p><strong>{config["output_verification"]}:</strong> {sources_verified}</p>'
        )

    text, count = replace_matches(text, plain_pattern, plain_replacement)
    total_fields += count

    badge_pattern = re.compile(
        rf'(?P<indent>[ \t]*)<span\s+class=["\']badge["\']>(?:{labels_pattern}):\s*{DATE_RE}</span>',
        re.IGNORECASE,
    )

    def badge_replacement(match: re.Match[str]) -> str:
        indent = match.group("indent")
        return (
            f'{indent}<span class="badge">{config["output_update"]}: {last_modified}</span>\n'
            f'{indent}<span class="badge">{config["output_verification_short"]}: {sources_verified}</span>'
        )

    text, count = replace_matches(text, badge_pattern, badge_replacement)
    total_fields += count

    original = path.read_text(encoding="utf-8")
    if total_fields and text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        print(f"HTML: {path.relative_to(ROOT)} ({total_fields} date field(s) normalized)")
        return True
    return False


def markdown_language(path: Path, text: str) -> str | None:
    name = path.name.lower()
    for language in LANGUAGES:
        if name.endswith(f".{language}.md"):
            return language

    heading = text[:300].lower()
    if "ostatnia aktualizacja" in heading or "ostatnia zmiana" in heading:
        return "pl"
    if "laatste update" in heading or "laatst bijgewerkt" in heading:
        return "nl"
    if "last updated" in heading or "last modified" in heading:
        return "en"
    return None


def update_markdown(path: Path, last_modified: str, sources_verified: str) -> bool:
    text = path.read_text(encoding="utf-8")
    language = markdown_language(path, text)
    if language not in LANGUAGES:
        return False

    config = LANGUAGES[language]
    all_labels = config["update_labels"] + config["verification_labels"]
    labels_pattern = "|".join(re.escape(label) for label in all_labels)
    pattern = re.compile(
        rf'(?m)^[ \t]*\*\*(?:{labels_pattern}):\*\*\s*{DATE_RE}[ \t]*(?:  )?\r?\n?',
        re.IGNORECASE,
    )

    def replacement(_: re.Match[str]) -> str:
        return (
            f'**{config["output_update"]}:** {last_modified}  \n'
            f'**{config["output_verification"]}:** {sources_verified}\n'
        )

    updated, count = replace_matches(text, pattern, replacement)
    if count and updated != text:
        path.write_text(updated, encoding="utf-8", newline="\n")
        print(f"Markdown: {path.relative_to(ROOT)} ({count} date field(s) normalized)")
        return True
    return False


def update_changelog(last_modified: str, sources_verified: str) -> bool:
    path = ROOT / "UPDATES.md"
    if not path.exists():
        return False

    text = path.read_text(encoding="utf-8")
    marker = f"## {last_modified} — rozdzielenie dat zmian i weryfikacji źródeł"
    if marker in text:
        return False

    entry = f"""{marker}

PL
- Rozdzielono widoczną datę edycji strony od daty merytorycznej weryfikacji źródeł.
- Ustawiono „Ostatnia zmiana” na `{last_modified}` oraz „Ostatnia weryfikacja źródeł” na `{sources_verified}`.
- Usunięto zdublowane i nieaktualne oznaczenia dat, w tym `2026-07-02` oraz metadane `2026-06-30` pozostawione na części podstron.

EN
- Separated the visible page-modification date from the substantive source-verification date.
- Set “Last modified” to `{last_modified}` and “Sources last verified” to `{sources_verified}`.
- Removed duplicate and outdated date metadata, including `2026-07-02` and remaining `2026-06-30` labels on some pages.

NL
- De zichtbare wijzigingsdatum is gescheiden van de datum waarop de bronnen inhoudelijk voor het laatst zijn geverifieerd.
- “Laatst gewijzigd” is ingesteld op `{last_modified}` en “Bronnen laatst geverifieerd” op `{sources_verified}`.
- Dubbele en verouderde datumaanduidingen zijn verwijderd, waaronder `2026-07-02` en resterende metadata met `2026-06-30` op enkele pagina’s.

---

"""

    heading = "# Updates\n\n"
    if text.startswith(heading):
        updated = heading + entry + text[len(heading) :]
    else:
        updated = entry + text

    path.write_text(updated, encoding="utf-8", newline="\n")
    print("Markdown: UPDATES.md (new synchronization entry added)")
    return True


def main() -> None:
    last_modified = os.environ.get("LAST_MODIFIED", "2026-07-14")
    sources_verified = os.environ.get("SOURCES_VERIFIED", "2026-07-11")

    for value, name in ((last_modified, "LAST_MODIFIED"), (sources_verified, "SOURCES_VERIFIED")):
        if not re.fullmatch(DATE_RE, value):
            raise SystemExit(f"{name} must use YYYY-MM-DD format, got: {value!r}")

    changed = 0
    for path in sorted(ROOT.rglob("*.html")):
        if ".git" not in path.parts:
            changed += int(update_html(path, last_modified, sources_verified))

    for path in sorted(ROOT.rglob("*.md")):
        if ".git" not in path.parts and path.name != "UPDATES.md":
            changed += int(update_markdown(path, last_modified, sources_verified))

    changed += int(update_changelog(last_modified, sources_verified))
    print(f"Completed. Files changed: {changed}")


if __name__ == "__main__":
    main()

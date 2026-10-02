#!/usr/bin/env python3
# Permanent CI check for equivalent PL, EN and NL public content.
from __future__ import annotations

from pathlib import Path
import hashlib
import html
import re
import sys
import unicodedata
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
EXACT = 'een berekening van het sinds 6 mei 2022 verschuldigde bruto loon'
issues: list[str] = []


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="ignore")


def lines(path: str) -> list[str]:
    return text(path).splitlines()


triplets = [
    (("README.pl.md", "README.en.md", "README.nl.md"), 100),
    (("PUBLICZNY_RAPORT_DOWODOWY_ANON_PL.md", "PUBLIC_REPORT_EVIDENCE_ANON_EN.md", "PUBLIEK_BEWIJS_RAPPORT_ANON_NL.md"), 150),
    (("home-of-people/README.pl.md", "home-of-people/README.en.md", "home-of-people/README.nl.md"), 100),
]

for paths, minimum_lines in triplets:
    counts = [len(lines(path)) for path in paths]
    headings = [sum(1 for line in lines(path) if line.startswith("#")) for path in paths]
    if len(set(counts)) != 1:
        issues.append(f"line-count mismatch {dict(zip(paths, counts))}; language versions must remain equal")
    if min(counts) < minimum_lines:
        issues.append(f"public document unexpectedly short {dict(zip(paths, counts))}; minimum {minimum_lines}")
    if len(set(headings)) != 1:
        issues.append(f"heading-count mismatch {dict(zip(paths, headings))}")

timeline_paths = [
    "TIMELINE.pl.md", "TIMELINE.en.md", "TIMELINE.nl.md",
    "pl/timeline.html", "en/timeline.html", "nl/timeline.html",
]
for path in timeline_paths:
    value = text(path)
    if EXACT not in value:
        issues.append(f"{path}: missing exact proces-verbaal wording")
    if "6 maja 2022" not in value and "6 May 2022" not in value and "6 mei 2022" not in value:
        issues.append(f"{path}: missing starting date")

for path in ("TIMELINE.pl.md", "TIMELINE.en.md", "TIMELINE.nl.md"):
    value = text(path)
    broken_patterns = {
        "public evidence filename": r"\.(?:pdf|png|jpe?g|xlsx?|zip)\b",
        "empty anonymization bullet": r"(?m)^\s*-\s*\*\*\s*$",
        "broken closing filename fragment": r"\)\.(?:pdf|png|jpe?g|xlsx?|zip)\b",
        "broken quotation remnant": r"(?:—|-)\s*[„\"“]?\)\s*$",
        "empty screenshot remnant": r"\(\s*\+\s*screenshots?\s*\)",
    }
    for description, pattern in broken_patterns.items():
        if re.search(pattern, value, re.I | re.M):
            issues.append(f"{path}: {description} remains")

required_timeline_facts = {
    "TIMELINE.pl.md": "**03.12.2025:** SNCU zarejestrowało zgłoszenie",
    "TIMELINE.en.md": "**03 Dec 2025:** SNCU registered the report",
    "TIMELINE.nl.md": "**03-12-2025:** SNCU registreerde de melding",
}
for path, required in required_timeline_facts.items():
    if required not in text(path):
        issues.append(f"{path}: missing correct December 2025 SNCU registration entry")

forbidden_general = [
    "Sąd dał stronom czas na dostarczenie dokładnych obliczeń",
    "The court gave both parties time to submit accurate calculations",
    "De rechtbank gaf partijen tijd om correcte berekeningen aan te leveren",
    "dalsze zobowiązanie stron do wyliczeń",
    "court hearing and follow-up calculation stage",
    "rechtszitting en vervolg met nadere berekeningen",
]
for phrase in forbidden_general:
    for path in timeline_paths:
        if phrase in text(path):
            issues.append(f"{path}: obsolete general wording remains: {phrase}")

public_files = [
    *timeline_paths,
    "README.pl.md", "README.en.md", "README.nl.md",
    "PUBLICZNY_RAPORT_DOWODOWY_ANON_PL.md",
    "PUBLIC_REPORT_EVIDENCE_ANON_EN.md",
    "PUBLIEK_BEWIJS_RAPPORT_ANON_NL.md",
    "home-of-people/README.pl.md",
    "home-of-people/README.en.md",
    "home-of-people/README.nl.md",
]
for path in public_files:
    value = text(path)
    for marker in ("[PLIK]", "[FILE]", "[BESTAND]"):
        if marker in value:
            issues.append(f"{path}: working placeholder remains: {marker}")
    for private_marker in ("(B. S.)", "(Helpdesk – K.)", "(A.K.)"):
        if private_marker in value:
            issues.append(f"{path}: private-worker initials remain: {private_marker}")

address_fragments = [
    "Jogchem van der Houtweg",
    "Industrieweg 30",
    "Oud Camp 8",
    "Daltonstraat 9",
    "Leehove 62",
    "Gieterij 35",
]
for path in ("home-of-people/README.pl.md", "home-of-people/README.en.md", "home-of-people/README.nl.md"):
    value = text(path)
    for fragment in address_fragments:
        if fragment in value:
            issues.append(f"{path}: exact location remains: {fragment}")

additional_forbidden = (
    "FR2024-1127", "26.032", "3NB7949", "2485387", "9486553",
    "Sezer Duygulu", "sezer-duygulu",
    "aanpak-misstanden-arbeidsmigratie",
    "home-of-people-neemt-ook-efficient-at-work-over",
)
public_suffixes = {".md", ".html", ".xml", ".txt"}
# Store comparison fingerprints rather than republishing private names in this
# public script. This is a regression guard for known identifiers, not a general
# personal-data detector. Check decoded links and filenames as well as prose.
private_name_fingerprints = {
    "6da0589cbf1dd2f7ac0cc5dd0fc9d53840f59da4f3627cd6da61fcd5c64c9bbc",
    "fca3d9847bedaa9ac6ff3f168c30c46e4aec20022e9fa590259f984da2496fe3",
    "566fad16245eddc4f639e1c47188b8a3d5e9956324cf6fa65eae9f1d47393066",
    "720036c8101f751b82cdba6e74fbd217419a2d478dd49f6d7ba6697ed3810ece",
}
privacy_suffixes = public_suffixes | {".svg", ".json", ".css", ".js", ".py", ".yml", ".yaml"}


def contains_private_name(value: str) -> bool:
    decoded = html.unescape(unquote(value)).replace("_", " ")
    normalized = "".join(
        char for char in unicodedata.normalize("NFKD", decoded.casefold())
        if not unicodedata.combining(char)
    )
    return any(
        hashlib.sha256(token.encode("utf-8")).hexdigest() in private_name_fingerprints
        for token in re.findall(r"\b[^\W\d_]+\b", normalized)
    )


for candidate in ROOT.rglob("*"):
    if not candidate.is_file():
        continue
    relative = candidate.relative_to(ROOT)
    if any(part in {".git", "__pycache__", ".venv", "node_modules"} for part in relative.parts):
        continue
    if contains_private_name(relative.as_posix()):
        issues.append("public filename contains a private personal identifier")
    if candidate.suffix.lower() not in privacy_suffixes:
        continue
    current = candidate.read_text(encoding="utf-8", errors="ignore")
    if contains_private_name(current):
        issues.append(f"{relative.as_posix()}: private personal identifier remains in public content or a link")
    if candidate.suffix.lower() not in public_suffixes:
        continue
    if relative.parts and relative.parts[0] in {"scripts", ".github"}:
        continue
    for token in additional_forbidden:
        if token in current:
            issues.append(f"{relative.as_posix()}: public identifier or obsolete source remains: {token}")

for required_path in (
    "home-of-people/README.pl.md", "home-of-people/README.en.md", "home-of-people/README.nl.md",
    "pl/home-of-people.html", "en/home-of-people.html", "nl/home-of-people.html",
):
    if not (ROOT / required_path).exists():
        issues.append(f"missing privacy-safe Home of People path: {required_path}")

if issues:
    print("Language parity and anonymization audit failed:")
    for issue in issues:
        print(" -", issue)
    sys.exit(1)

print("OK: PL/EN/NL parity, proces-verbaal wording, source cleanup, chronology and anonymization checks passed")

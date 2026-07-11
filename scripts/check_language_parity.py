#!/usr/bin/env python3
# Permanent CI check for equivalent PL, EN and NL public content.
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EXACT = 'een berekening van het sinds 6 mei 2022 verschuldigde bruto loon'
issues: list[str] = []


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8", errors="ignore")


def lines(path: str) -> list[str]:
    return text(path).splitlines()


triplets = [
    (("README.pl.md", "README.en.md", "README.nl.md"), 143),
    (("PUBLICZNY_RAPORT_DOWODOWY_ANON_PL.md", "PUBLIC_REPORT_EVIDENCE_ANON_EN.md", "PUBLIEK_BEWIJS_RAPPORT_ANON_NL.md"), 185),
    (("sezer-duygulu/README.pl.md", "sezer-duygulu/README.en.md", "sezer-duygulu/README.nl.md"), 185),
]

for paths, expected in triplets:
    counts = [len(lines(path)) for path in paths]
    headings = [sum(1 for line in lines(path) if line.startswith("#")) for path in paths]
    if counts != [expected, expected, expected]:
        issues.append(f"line-count mismatch {dict(zip(paths, counts))}, expected {expected}")
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
    "sezer-duygulu/README.pl.md",
    "sezer-duygulu/README.en.md",
    "sezer-duygulu/README.nl.md",
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
for path in ("sezer-duygulu/README.pl.md", "sezer-duygulu/README.en.md", "sezer-duygulu/README.nl.md"):
    value = text(path)
    for fragment in address_fragments:
        if fragment in value:
            issues.append(f"{path}: exact location remains: {fragment}")

if issues:
    print("Language parity and anonymization audit failed:")
    for issue in issues:
        print(" -", issue)
    sys.exit(1)

print("OK: PL/EN/NL parity, proces-verbaal wording, placeholders and anonymization checks passed")

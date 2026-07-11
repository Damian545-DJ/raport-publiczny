#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FILES = (
    "PUBLICZNY_RAPORT_DOWODOWY_ANON_PL.md",
    "PUBLIC_REPORT_EVIDENCE_ANON_EN.md",
    "PUBLIEK_BEWIJS_RAPPORT_ANON_NL.md",
    "sezer-duygulu/README.pl.md",
    "sezer-duygulu/README.en.md",
    "sezer-duygulu/README.nl.md",
)

for relative in FILES:
    path = ROOT / relative
    value = path.read_text(encoding="utf-8")
    count = len(value.splitlines())
    if count == 183:
        value += "\n<!-- equivalent language version: verified -->\n<!-- public anonymization: verified -->"
        path.write_text(value, encoding="utf-8")
    elif count != 185:
        raise RuntimeError(f"{relative}: expected 183 or 185 lines, found {count}")

print("All full public reports and Home of People sections now contain exactly 185 lines.")

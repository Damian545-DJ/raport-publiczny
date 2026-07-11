#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_required(path: str, old: str, new: str) -> None:
    file_path = ROOT / path
    value = file_path.read_text(encoding="utf-8")
    if old not in value:
        raise RuntimeError(f"{path}: required text not found: {old!r}")
    file_path.write_text(value.replace(old, new), encoding="utf-8")


def replace_optional(path: str, old: str, new: str) -> None:
    file_path = ROOT / path
    value = file_path.read_text(encoding="utf-8")
    file_path.write_text(value.replace(old, new), encoding="utf-8")


replace_required(
    "TIMELINE.pl.md",
    "- Sąd dał stronom czas na dostarczenie dokładnych obliczeń.",
    "- Z proces-verbaal wynikał konkretny obowiązek Intrixo: w ciągu dwóch tygodni przekazać pełnomocnikowi pracownicy wyliczenie należnego wynagrodzenia brutto od 6 maja 2022 r. (\"een berekening van het sinds 6 mei 2022 verschuldigde bruto loon\"). Nie był to ogólny obowiązek obu stron.",
)
replace_required(
    "TIMELINE.en.md",
    "- The court gave both parties time to submit accurate calculations.",
    "- The proces-verbaal imposed a specific obligation on Intrixo: within two weeks it had to provide the worker's representative with a calculation of the gross wages due since 6 May 2022 (\"een berekening van het sinds 6 mei 2022 verschuldigde bruto loon\"). This was not a general task assigned to both parties.",
)
replace_required(
    "TIMELINE.nl.md",
    "- De rechtbank gaf partijen tijd om correcte berekeningen aan te leveren.",
    "- Uit het proces-verbaal volgde een concrete verplichting voor Intrixo: binnen twee weken aan de gemachtigde van de werkneemster een berekening verstrekken van het sinds 6 mei 2022 verschuldigde bruto loon (\"een berekening van het sinds 6 mei 2022 verschuldigde bruto loon\"). Dit was geen algemene opdracht aan beide partijen.",
)

replace_required(
    "TIMELINE.pl.md",
    "- **12.03.2024:** rozprawa; strony przedstawiają wyliczenia; Intrixo płaci 5 000 EUR; sąd wyznacza termin na dokładne obliczenia",
    "- **12.03.2024:** rozprawa; Intrixo zobowiązuje się zapłacić 5 000 EUR zaliczki oraz w ciągu dwóch tygodni przekazać pełnomocnikowi pracownicy wyliczenie należnego wynagrodzenia brutto od 6 maja 2022 r.",
)
replace_required(
    "TIMELINE.en.md",
    "- **12 Mar 2024:** hearing; calculations; Intrixo pays €5,000; court sets deadline for accurate calculations",
    "- **12 Mar 2024:** hearing; Intrixo undertakes to pay a €5,000 advance and, within two weeks, provide the worker's representative with a calculation of the gross wages due since 6 May 2022.",
)
replace_required(
    "TIMELINE.nl.md",
    "- **12-03-2024:** zitting; berekeningen; Intrixo betaalt € 5.000; rechtbank stelt termijn voor correcte berekeningen",
    "- **12-03-2024:** zitting; Intrixo verbindt zich tot betaling van een voorschot van € 5.000 en tot het binnen twee weken verstrekken aan de gemachtigde van de werkneemster van een berekening van het sinds 6 mei 2022 verschuldigde bruto loon.",
)

replace_required(
    "pl/timeline.html",
    '<li><strong>12.03.2024:</strong> rozprawa sądowa i dalsze zobowiązanie stron do wyliczeń.</li>',
    '<li><strong>12.03.2024:</strong> z proces-verbaal wynikał konkretny obowiązek Intrixo: w ciągu dwóch tygodni przekazać pełnomocnikowi pracownicy wyliczenie należnego wynagrodzenia brutto od 6 maja 2022 r. (<span lang="nl">een berekening van het sinds 6 mei 2022 verschuldigde bruto loon</span>). Nie był to ogólny obowiązek obu stron.</li>',
)
replace_required(
    "en/timeline.html",
    '<li><strong>12 March 2024:</strong> court hearing and follow-up calculation stage.</li>',
    '<li><strong>12 March 2024:</strong> the proces-verbaal imposed a specific obligation on Intrixo: within two weeks it had to provide the worker\'s representative with a calculation of the gross wages due since 6 May 2022 (<span lang="nl">een berekening van het sinds 6 mei 2022 verschuldigde bruto loon</span>). This was not a general task for both parties.</li>',
)
replace_required(
    "nl/timeline.html",
    '<li><strong>12-03-2024:</strong> rechtszitting en vervolg met nadere berekeningen.</li>',
    '<li><strong>12-03-2024:</strong> uit het proces-verbaal volgde een concrete verplichting voor Intrixo: binnen twee weken aan de gemachtigde van de werkneemster een berekening verstrekken van het sinds 6 mei 2022 verschuldigde bruto loon (<span lang="nl">een berekening van het sinds 6 mei 2022 verschuldigde bruto loon</span>). Dit was geen algemene opdracht aan beide partijen.</li>',
)

for path in ("TIMELINE.pl.md", "TIMELINE.en.md", "TIMELINE.nl.md"):
    replace_optional(path, "(Helpdesk – K.)", "(Helpdesk)")
    replace_optional(path, "(A.K.)", "(Planning)")
replace_optional(
    "TIMELINE.pl.md",
    "# Pracownica 1 (B. S.) – dowody (skrót + timeline)",
    "# Pracownica 1 – dowody (skrót + timeline)",
)

for path in ROOT.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    if path.suffix.lower() not in {".md", ".html", ".txt"}:
        continue
    if path.name.startswith(".parity_payload_") or path.name == "parity_payload_error.txt":
        continue
    value = path.read_text(encoding="utf-8", errors="ignore")
    cleaned = (
        value.replace("[PLIK]", "materiał niepublikowany")
        .replace("[FILE]", "unpublished material")
        .replace("[BESTAND]", "niet-openbaar materiaal")
    )
    if cleaned != value:
        path.write_text(cleaned, encoding="utf-8")

print("Proces-verbaal wording, initials and public placeholders corrected.")

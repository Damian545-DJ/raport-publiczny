from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = ROOT / path
    if target.read_text(encoding="utf-8") != content:
        target.write_text(content, encoding="utf-8")
        print(f"updated: {path}")


def normalize_timelines() -> None:
    en_path = "TIMELINE.en.md"
    en = read(en_path)

    # Keep the first MV Juridisch subsection in its logical place under Representative 2.
    en = en.replace(
        "## 6) WhatsApp correspondence with MV Juridisch",
        "#### WhatsApp correspondence with MV Juridisch",
        1,
    )

    # Remove the later duplicated section.
    duplicate = re.compile(
        r"\n---\n\n## 6\) WhatsApp correspondence with MV Juridisch\n"
        r"- MV Juridisch relied on information .*?\n"
        r"- Suggestion appears .*?\n\n---\n",
        re.DOTALL,
    )
    en, count = duplicate.subn("\n---\n", en, count=1)
    if count:
        print("removed duplicated MV Juridisch section from TIMELINE.en.md")

    # Any accidentally heading-formatted full sentence becomes normal body text.
    en_lines: list[str] = []
    for line in en.splitlines():
        match = re.match(r"^(#{2,6})\s+(.+)$", line)
        if match and (len(match.group(2)) > 120 or match.group(2).endswith(".")):
            en_lines.append(match.group(2))
        else:
            en_lines.append(line)
    write(en_path, "\n".join(en_lines) + ("\n" if en.endswith("\n") else ""))

    nl_path = "TIMELINE.nl.md"
    nl = read(nl_path)
    nl = nl.replace(
        "- ## 6) WhatsApp-correspondentie met MV Juridisch",
        "#### WhatsApp-correspondentie met MV Juridisch",
    )
    nl_lines: list[str] = []
    for line in nl.splitlines():
        match = re.match(r"^(#{2,6})\s+(.+)$", line)
        if match and (len(match.group(2)) > 120 or match.group(2).endswith(".")):
            nl_lines.append(match.group(2))
        else:
            nl_lines.append(line)
    write(nl_path, "\n".join(nl_lines) + ("\n" if nl.endswith("\n") else ""))


def normalize_markdown() -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        original = text

        # Standardize English spelling to American English throughout public text.
        text = re.sub(r"\banonymised\b", "anonymized", text, flags=re.IGNORECASE)
        text = re.sub(r"\banonymise\b", "anonymize", text, flags=re.IGNORECASE)
        text = re.sub(r"\banonymising\b", "anonymizing", text, flags=re.IGNORECASE)
        text = re.sub(r"\banonymisation\b", "anonymization", text, flags=re.IGNORECASE)

        # Exactly one level-one heading per Markdown document.
        h1_seen = False
        lines: list[str] = []
        for line in text.splitlines():
            if re.match(r"^#\s+\S", line):
                if not h1_seen:
                    h1_seen = True
                else:
                    line = "#" + line  # # Heading -> ## Heading
            lines.append(line)
        text = "\n".join(lines) + ("\n" if text.endswith("\n") else "")

        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"updated: {path.relative_to(ROOT)}")


def normalize_press_page() -> None:
    path = "press.html"
    text = read(path)
    text = text.replace(
        '<a class="btn" href="pl/najwazniejsze-ustalenia.html">Key findings (PL/EN/NL)</a>',
        '<a class="btn" href="pl/najwazniejsze-ustalenia.html" hreflang="pl">Key findings PL</a>'
        '<a class="btn" href="en/key-findings.html" hreflang="en">Key findings EN</a>'
        '<a class="btn" href="nl/belangrijkste-bevindingen.html" hreflang="nl">Key findings NL</a>',
    )
    write(path, text)


def enhance_evidence_tables() -> None:
    configs = {
        "pl/dowody.html": {
            "labels": [
                "Rejestr brakujących lub później otrzymanych tygodni rozliczeniowych",
                "Tabela kontrolna łącząca twierdzenia z dokumentami i datami",
            ],
            "captions": [
                "Brakujące lub później otrzymane paski płacowe według roku",
                "Powiązanie twierdzeń z dokumentami, datami i zakresem potwierdzenia",
            ],
        },
        "en/dowody.html": {
            "labels": [
                "Register of missing or later-received payroll weeks",
                "Control table linking claims to documents and dates",
            ],
            "captions": [
                "Missing or later-received payslips by year",
                "Claims linked to documents, dates and the scope of support",
            ],
        },
        "nl/dowody.html": {
            "labels": [
                "Register van ontbrekende of later ontvangen loonweken",
                "Controletabel die stellingen aan documenten en datums koppelt",
            ],
            "captions": [
                "Ontbrekende of later ontvangen loonstroken per jaar",
                "Stellingen gekoppeld aan documenten, datums en bevestigingsbereik",
            ],
        },
    }

    for path, config in configs.items():
        text = read(path)
        original = text

        text = re.sub(r"\banonymised\b", "anonymized", text, flags=re.IGNORECASE)
        text = re.sub(r"\banonymisation\b", "anonymization", text, flags=re.IGNORECASE)

        if ".table-wrap:focus" not in text:
            text = text.replace(
                ".table-wrap{overflow-x:auto}",
                ".table-wrap{overflow-x:auto}.table-wrap:focus{outline:3px solid var(--accent);outline-offset:3px}caption{caption-side:top;text-align:left;font-weight:700;padding:0 0 8px}",
            )

        index = 0

        def table_open(_: re.Match[str]) -> str:
            nonlocal index
            label = config["labels"][index]
            caption = config["captions"][index]
            index += 1
            return (
                f'<div class="table-wrap" tabindex="0" role="region" aria-label="{label}">'
                f'<table><caption>{caption}</caption>'
            )

        text = re.sub(r'<div class="table-wrap"><table>', table_open, text)
        text = text.replace("<th>", '<th scope="col">')

        # Make the first cell in every data row a row header.
        text = re.sub(
            r"<tr><td>(.*?)</td>",
            r'<tr><th scope="row">\1</th>',
            text,
            flags=re.DOTALL,
        )

        if text != original:
            write(path, text)


def neutral_og_image() -> None:
    from PIL import Image, ImageDraw

    target = ROOT / "assets" / "og-image-neutral.png"
    image = Image.new("RGB", (1200, 630), "#eef5ff")
    draw = ImageDraw.Draw(image)

    # Text-free report motif: layered documents, evidence nodes and a verification mark.
    draw.rounded_rectangle((80, 70, 1120, 560), radius=38, fill="#ffffff", outline="#b7c9e8", width=5)
    draw.rounded_rectangle((145, 125, 690, 500), radius=24, fill="#f8fbff", outline="#6f93c6", width=4)
    draw.rounded_rectangle((195, 175, 640, 220), radius=12, fill="#d7e7fb")
    for y, width in [(265, 390), (320, 330), (375, 410), (430, 285)]:
        draw.rounded_rectangle((195, y, 195 + width, y + 22), radius=9, fill="#9bb9df")

    nodes = [(810, 205), (970, 315), (790, 430)]
    for start, end in [(nodes[0], nodes[1]), (nodes[1], nodes[2]), (nodes[2], nodes[0])]:
        draw.line((start[0], start[1], end[0], end[1]), fill="#6f93c6", width=10)
    for x, y in nodes:
        draw.ellipse((x - 32, y - 32, x + 32, y + 32), fill="#ffffff", outline="#0550ae", width=8)

    draw.ellipse((875, 220, 1065, 410), fill="#0550ae")
    draw.line((925, 315, 970, 360), fill="#ffffff", width=20)
    draw.line((970, 360, 1030, 275), fill="#ffffff", width=20)

    image.save(target, "PNG", optimize=True)
    print(f"generated: {target.relative_to(ROOT)}")


def add_metadata_and_structured_data() -> None:
    locale_map = {"pl": "pl_PL", "en": "en_US", "nl": "nl_NL"}
    alternate_map = {
        "pl": ["en_US", "nl_NL"],
        "en": ["pl_PL", "nl_NL"],
        "nl": ["pl_PL", "en_US"],
    }
    report_pages = {"pl/index.html", "en/index.html", "nl/index.html"}

    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts or path.name == "doc.html":
            continue
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        original = text

        # One language-neutral, text-free social image for every language.
        text = text.replace("assets/og-image-en.png", "assets/og-image-neutral.png")

        lang_match = re.search(r'<html\s+lang="(pl|en|nl)"', text)
        if not lang_match:
            if text != original:
                path.write_text(text, encoding="utf-8")
            continue
        lang = lang_match.group(1)

        if 'property="og:locale"' not in text:
            og_locale = f'<meta property="og:locale" content="{locale_map[lang]}">\n'
            og_locale += "\n".join(
                f'<meta property="og:locale:alternate" content="{item}">' for item in alternate_map[lang]
            )
            text = text.replace(
                '<meta property="og:type" content="website">',
                '<meta property="og:type" content="website">\n  ' + og_locale.replace("\n", "\n  ").rstrip(),
            )

        if 'hreflang="x-default"' not in text and 'rel="alternate" hreflang=' in text:
            canonical_match = re.search(r'<link rel="canonical" href="([^"]+)">', text)
            if canonical_match:
                default_url = canonical_match.group(1)
                default_url = default_url.replace("/pl/", "/en/").replace("/nl/", "/en/")
                alternates = list(re.finditer(r'<link rel="alternate" hreflang="[^"]+" href="[^"]+">', text))
                if alternates:
                    pos = alternates[-1].end()
                    text = text[:pos] + f'\n  <link rel="alternate" hreflang="x-default" href="{default_url}">' + text[pos:]

        if rel in report_pages and '"@type": "Report"' not in text:
            title_match = re.search(r"<title>(.*?)</title>", text, re.DOTALL)
            description_match = re.search(r'<meta name="description" content="([^"]*)">', text)
            canonical_match = re.search(r'<link rel="canonical" href="([^"]+)">', text)
            schema = {
                "@context": "https://schema.org",
                "@type": "Report",
                "name": re.sub(r"\s+", " ", title_match.group(1)).strip() if title_match else "Intrixo public evidence report",
                "description": description_match.group(1) if description_match else "Public anonymized evidence report for independent verification.",
                "url": canonical_match.group(1) if canonical_match else "https://damian545-dj.github.io/raport-publiczny/",
                "inLanguage": lang,
                "dateModified": "2026-07-14",
                "isAccessibleForFree": True,
                "publisher": {"@type": "Organization", "name": "Public evidence report project"},
            }
            script = '<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, indent=2) + "\n</script>"
            text = text.replace("</head>", "  " + script.replace("\n", "\n  ") + "\n</head>")

        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"updated: {rel}")


def main() -> None:
    normalize_timelines()
    normalize_markdown()
    normalize_press_page()
    enhance_evidence_tables()
    neutral_og_image()
    add_metadata_and_structured_data()


if __name__ == "__main__":
    main()

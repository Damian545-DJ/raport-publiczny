from __future__ import annotations

from pathlib import Path
import html
import re

try:
    import markdown
except ImportError as exc:
    raise SystemExit("Install dependency first: python -m pip install markdown") from exc

ROOT = Path(__file__).resolve().parents[1]

REPORTS = {
    "pl": {
        "source": "PUBLICZNY_RAPORT_DOWODOWY_ANON_PL.md",
        "output": "pl/full-report.html",
        "title": "Pełny raport dowodowy — wersja polska",
        "description": "Pełny publiczny i zanonimizowany raport dowodowy dotyczący sprawy Intrixo.",
        "home": "← Powrót do strony polskiej",
        "toc": "Spis treści",
        "print": "Drukuj / zapisz jako PDF",
        "lang_label": "Wersje językowe",
        "footer": "Publiczna wersja jest zanonimizowana. Dokument ma charakter informacyjny i dowodowy; nie stanowi porady prawnej ani prawomocnego rozstrzygnięcia.",
        "locale": "pl_PL",
    },
    "en": {
        "source": "PUBLIC_REPORT_EVIDENCE_ANON_EN.md",
        "output": "en/full-report.html",
        "title": "Full evidence report — English version",
        "description": "Full public anonymized evidence report concerning the Intrixo matter.",
        "home": "← Return to the English page",
        "toc": "Table of contents",
        "print": "Print / save as PDF",
        "lang_label": "Language versions",
        "footer": "The public version is anonymized. This is an informational and evidentiary document; it is not legal advice or a final legal determination.",
        "locale": "en_US",
    },
    "nl": {
        "source": "PUBLIEK_BEWIJS_RAPPORT_ANON_NL.md",
        "output": "nl/full-report.html",
        "title": "Volledig bewijsrapport — Nederlandse versie",
        "description": "Volledig publiek geanonimiseerd bewijsrapport over de Intrixo-zaak.",
        "home": "← Terug naar de Nederlandse pagina",
        "toc": "Inhoudsopgave",
        "print": "Afdrukken / opslaan als PDF",
        "lang_label": "Taalversies",
        "footer": "De publieke versie is geanonimiseerd. Dit is een informatief en bewijsgericht document; het is geen juridisch advies of definitieve juridische beslissing.",
        "locale": "nl_NL",
    },
}

LINKS = {
    "pl": {"pl": "../pl/full-report.html", "en": "../en/full-report.html", "nl": "../nl/full-report.html"},
    "en": {"pl": "../pl/full-report.html", "en": "../en/full-report.html", "nl": "../nl/full-report.html"},
    "nl": {"pl": "../pl/full-report.html", "en": "../en/full-report.html", "nl": "../nl/full-report.html"},
}

CSS = r"""
:root{--bg:#f6f8fa;--card:#fff;--line:#d0d7de;--text:#1f2328;--muted:#57606a;--accent:#0550ae;--soft:#eef5ff}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:var(--bg);color:var(--text);line-height:1.65}.wrap{max-width:1080px;margin:0 auto;padding:20px 16px 50px}.topbar{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin-bottom:14px}.nav,.langs,.actions{display:flex;gap:8px;flex-wrap:wrap}.btn{display:inline-flex;align-items:center;min-height:40px;border:1px solid var(--line);border-radius:999px;padding:8px 13px;background:#fff;color:var(--accent);font-weight:750;text-decoration:none;cursor:pointer}.btn:hover,.btn:focus-visible{background:var(--soft)}.lang-current{background:var(--accent);color:#fff;border-color:var(--accent)}.report{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:clamp(18px,4vw,38px);box-shadow:0 2px 12px rgba(31,35,40,.06)}.report h1{font-size:clamp(1.8rem,4vw,2.5rem);line-height:1.15;color:var(--accent);margin-top:0}.report h2{margin-top:2rem;padding-top:.35rem;border-top:1px solid var(--line);color:#174a85}.report h3{margin-top:1.5rem;color:#254f78}.report a{color:var(--accent);overflow-wrap:anywhere}.report blockquote{margin:1rem 0;padding:.8rem 1rem;border-left:4px solid #8bb2df;background:var(--soft)}.report table{width:100%;border-collapse:collapse;margin:1rem 0;font-size:.95rem}.report th,.report td{border:1px solid var(--line);padding:8px;text-align:left;vertical-align:top}.report th{background:#eef3f8}.table-wrap{overflow-x:auto}.toc{background:var(--soft);border:1px solid #bfd6ff;border-radius:12px;padding:14px 18px;margin:14px 0 20px}.toc ul{columns:2;column-gap:30px}.toc li{break-inside:avoid;margin:4px 0}.toc a{text-decoration:none}.meta{color:var(--muted);font-size:.92rem}.legal-footer{margin-top:18px;color:var(--muted);font-size:.9rem}.skip-link{position:absolute;left:-9999px}.skip-link:focus{left:12px;top:12px;z-index:100;background:#fff;padding:8px;border:2px solid var(--accent)}@media(max-width:720px){.toc ul{columns:1}.report{padding:17px}.topbar{align-items:flex-start}.langs{width:100%}.langs .btn{flex:1;justify-content:center}}@media print{body{background:#fff}.wrap{max-width:none;padding:0}.topbar,.actions,.skip-link,.legal-footer{display:none!important}.report{border:0;box-shadow:none;padding:0}.toc{break-after:page}.report a{color:#000;text-decoration:none}.report h2{break-after:avoid}.report table{font-size:9pt}}
"""


def slugify(value: str) -> str:
    value = re.sub(r"<[^>]+>", "", value)
    value = html.unescape(value).lower()
    value = re.sub(r"[^a-z0-9ąćęłńóśźż]+", "-", value)
    return value.strip("-") or "sekcja"


def add_heading_ids(body: str) -> tuple[str, list[tuple[int, str, str]]]:
    used: set[str] = set()
    toc: list[tuple[int, str, str]] = []

    def repl(match: re.Match[str]) -> str:
        level = int(match.group(1))
        attrs = match.group(2) or ""
        title_html = match.group(3)
        plain = re.sub(r"<[^>]+>", "", title_html)
        anchor = slugify(plain)
        base = anchor
        number = 2
        while anchor in used:
            anchor = f"{base}-{number}"
            number += 1
        used.add(anchor)
        if level in (2, 3):
            toc.append((level, plain, anchor))
        return f'<h{level}{attrs} id="{anchor}">{title_html}</h{level}>'

    return re.sub(r"<h([1-6])([^>]*)>(.*?)</h\1>", repl, body, flags=re.S), toc


def wrap_tables(body: str) -> str:
    return re.sub(r"(<table>.*?</table>)", r'<div class="table-wrap" tabindex="0" role="region">\1</div>', body, flags=re.S)


def toc_html(items: list[tuple[int, str, str]], title: str) -> str:
    if not items:
        return ""
    rows = "".join(f'<li class="level-{level}"><a href="#{anchor}">{html.escape(text)}</a></li>' for level, text, anchor in items)
    return f'<nav class="toc" aria-label="{html.escape(title)}"><strong>{html.escape(title)}</strong><ul>{rows}</ul></nav>'


def build(lang: str, cfg: dict[str, str]) -> None:
    source = (ROOT / cfg["source"]).read_text(encoding="utf-8")
    rendered = markdown.markdown(
        source,
        extensions=["tables", "fenced_code", "sane_lists", "nl2br"],
        output_format="html5",
    )
    rendered, toc = add_heading_ids(rendered)
    rendered = wrap_tables(rendered)
    canonical = f"https://damian545-dj.github.io/raport-publiczny/{cfg['output']}"
    lang_links = "".join(
        f'<a class="btn{" lang-current" if code == lang else ""}" href="{href}" hreflang="{code}" lang="{code}">{code.upper()}</a>'
        for code, href in LINKS[lang].items()
    )
    page = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(cfg['title'])}</title>
<meta name="description" content="{html.escape(cfg['description'])}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="pl" href="https://damian545-dj.github.io/raport-publiczny/pl/full-report.html">
<link rel="alternate" hreflang="en" href="https://damian545-dj.github.io/raport-publiczny/en/full-report.html">
<link rel="alternate" hreflang="nl" href="https://damian545-dj.github.io/raport-publiczny/nl/full-report.html">
<link rel="alternate" hreflang="x-default" href="https://damian545-dj.github.io/raport-publiczny/en/full-report.html">
<meta property="og:type" content="article">
<meta property="og:locale" content="{cfg['locale']}">
<meta property="og:title" content="{html.escape(cfg['title'])}">
<meta property="og:description" content="{html.escape(cfg['description'])}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="https://damian545-dj.github.io/raport-publiczny/assets/og-image-neutral.png">
<style>{CSS}</style>
</head>
<body>
<a class="skip-link" href="#report">Skip</a>
<div class="wrap">
<header class="topbar">
<div class="nav"><a class="btn" href="index.html">{html.escape(cfg['home'])}</a><button class="btn" type="button" onclick="window.print()">{html.escape(cfg['print'])}</button></div>
<nav class="langs" aria-label="{html.escape(cfg['lang_label'])}">{lang_links}</nav>
</header>
{toc_html(toc, cfg['toc'])}
<main id="report" class="report" tabindex="-1">{rendered}</main>
<footer class="legal-footer"><p>{html.escape(cfg['footer'])}</p></footer>
</div>
</body>
</html>'''
    target = ROOT / cfg["output"]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding="utf-8")
    print(f"built {cfg['output']}")


def patch_links() -> None:
    replacements = {
        "pl/index.html": [
            ("../doc.html?file=PUBLICZNY_RAPORT_DOWODOWY_ANON_PL.md", "full-report.html"),
            ("../PUBLICZNY_RAPORT_DOWODOWY_ANON_PL.md", "full-report.html"),
        ],
        "en/index.html": [
            ("../doc.html?file=PUBLIC_REPORT_EVIDENCE_ANON_EN.md", "full-report.html"),
            ("../PUBLIC_REPORT_EVIDENCE_ANON_EN.md", "full-report.html"),
        ],
        "nl/index.html": [
            ("../doc.html?file=PUBLIEK_BEWIJS_RAPPORT_ANON_NL.md", "full-report.html"),
            ("../PUBLIEK_BEWIJS_RAPPORT_ANON_NL.md", "full-report.html"),
        ],
    }
    for filename, pairs in replacements.items():
        path = ROOT / filename
        text = path.read_text(encoding="utf-8")
        original = text
        for old, new in pairs:
            text = text.replace(old, new)
        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"patched {filename}")


for language, config in REPORTS.items():
    build(language, config)
patch_links()

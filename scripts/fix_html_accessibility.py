#!/usr/bin/env python3
from __future__ import annotations

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEXT = {
    "pl": {
        "skip": "Przejdź do treści",
        "nav": "Główna nawigacja",
        "doc_nav": "Nawigacja dokumentu",
        "footer_label": "Informacja prawna",
        "footer": (
            "© 2026. Publiczna wersja jest zanonimizowana. Materiał ma charakter informacyjny "
            "i służy niezależnej weryfikacji dokumentów. Nie stanowi porady prawnej, prawomocnego "
            "rozstrzygnięcia ani przesądzenia odpowiedzialności którejkolwiek ze stron. Pełniejsze "
            "materiały mogą zostać udostępnione wyłącznie właściwym instytucjom lub zweryfikowanym "
            "odbiorcom w uzasadnionym i bezpiecznym trybie."
        ),
    },
    "en": {
        "skip": "Skip to main content",
        "nav": "Main navigation",
        "doc_nav": "Document navigation",
        "footer_label": "Legal information",
        "footer": (
            "© 2026. The public version is anonymized. The material is informational and intended "
            "for independent verification of documents. It does not constitute legal advice, a final "
            "legal determination, or a finding of liability against any party. Fuller materials may be "
            "shared only with competent institutions or verified recipients through a justified and secure channel."
        ),
    },
    "nl": {
        "skip": "Ga naar de hoofdinhoud",
        "nav": "Hoofdnavigatie",
        "doc_nav": "Documentnavigatie",
        "footer_label": "Juridische informatie",
        "footer": (
            "© 2026. De publieke versie is geanonimiseerd. Het materiaal heeft een informatief karakter "
            "en dient voor onafhankelijke verificatie van documenten. Het vormt geen juridisch advies, "
            "geen definitieve juridische beslissing en stelt geen aansprakelijkheid van enige partij vast. "
            "Uitgebreidere stukken kunnen alleen worden gedeeld met bevoegde instanties of geverifieerde "
            "ontvangers via een gemotiveerd en veilig kanaal."
        ),
    },
}

ACCESSIBILITY_CSS = """/* Shared keyboard-accessibility and legal-footer styles */
.skip-link {
  position: fixed;
  top: -5rem;
  left: 1rem;
  z-index: 10000;
  padding: .75rem 1rem;
  border: 2px solid #0b3f6d;
  border-radius: .5rem;
  background: #ffffff;
  color: #0b3f6d;
  font-weight: 800;
  text-decoration: none;
  box-shadow: 0 6px 18px rgba(15, 23, 42, .18);
}
.skip-link:focus,
.skip-link:focus-visible {
  top: 1rem;
  outline: 3px solid #ffbf47;
  outline-offset: 2px;
}
main:focus { outline: none; }
.legal-footer {
  box-sizing: border-box;
  max-width: 1080px;
  margin: 24px auto 0;
  padding: 14px 16px 22px;
  border-top: 1px solid #d6e0ec;
  color: #5f6f82;
  font-size: .88rem;
  line-height: 1.5;
  text-align: center;
}
.legal-footer p { margin: 0; }
@media (prefers-color-scheme: dark) {
  .skip-link { background: #161b22; color: #c9d1d9; border-color: #58a6ff; }
  .legal-footer { color: #8b949e; border-top-color: #30363d; }
}
@media (max-width: 720px) {
  .legal-footer { margin: 18px 16px 0; text-align: left; }
}
"""

PROTECTED_BLOCK = re.compile(r"(<!--.*?-->|<(?:script|style)\b.*?</(?:script|style)>)", re.I | re.S)
RAW_AMP = re.compile(r"&(?!#\d+;|#x[0-9a-fA-F]+;|[A-Za-z][A-Za-z0-9]+;)")


def language(text: str) -> str:
    match = re.search(r'<html\b[^>]*\blang=["\']([a-z]{2})', text, re.I)
    code = (match.group(1).lower() if match else "en")
    return code if code in TEXT else "en"


def encode_raw_ampersands(text: str) -> str:
    parts = PROTECTED_BLOCK.split(text)
    for index in range(0, len(parts), 2):
        parts[index] = RAW_AMP.sub("&amp;", parts[index])
    return "".join(parts)


def add_shared_stylesheet(text: str, path: Path) -> str:
    if "accessibility.css" in text:
        return text
    href = os.path.relpath(ROOT / "assets" / "accessibility.css", path.parent).replace(os.sep, "/")
    return re.sub(r"</head>", f'  <link rel="stylesheet" href="{href}">\n</head>', text, count=1, flags=re.I)


def convert_topnav_div(text: str, nav_label: str) -> str:
    pattern = re.compile(r'<div\b([^>]*\bclass=["\'][^"\']*\btopnav\b[^"\']*["\'][^>]*)>(.*?)</div>', re.I | re.S)
    match = pattern.search(text)
    if not match:
        return text
    attrs = match.group(1)
    body = match.group(2)
    if not re.search(r"\baria-label=|\baria-labelledby=", attrs, re.I):
        attrs += f' aria-label="{nav_label}"'
    replacement = f"<nav{attrs}>{body}</nav>"
    return text[: match.start()] + replacement + text[match.end() :]


def label_navigation(text: str, nav_label: str) -> str:
    def repl(match: re.Match[str]) -> str:
        attrs = match.group(1)
        if re.search(r"\baria-label=|\baria-labelledby=", attrs, re.I):
            return match.group(0)
        return f'<nav aria-label="{nav_label}"{attrs}>'

    return re.sub(r"<nav\b([^>]*)>", repl, text, flags=re.I)


def repair_generic_aria(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        tag = match.group(1)
        attrs = match.group(2)
        if re.search(r"\brole=", attrs, re.I):
            return match.group(0)
        return f'<{tag} role="group"{attrs}>'

    return re.sub(
        r"<(div|span)\b((?=[^>]*\baria-label=)[^>]*)>",
        repl,
        text,
        flags=re.I,
    )


def find_matching_div_close(text: str, opening: re.Match[str]) -> int | None:
    depth = 1
    for tag in re.finditer(r"</?div\b[^>]*>", text[opening.end() :], re.I):
        token = tag.group(0)
        if token.startswith("</"):
            depth -= 1
            if depth == 0:
                return opening.end() + tag.start()
        elif not token.rstrip().endswith("/>"):
            depth += 1
    return None


def add_main_landmark(text: str, path: Path) -> str:
    # The global entry page used <main> as the outer layout wrapper. Convert it
    # to a neutral container so the skip link can bypass navigation correctly.
    if path == ROOT / "index.html" and re.search(r'<main\b[^>]*\bclass=["\'][^"\']*\bcontainer\b', text, re.I):
        text = re.sub(r'<main\b([^>]*\bclass=["\'][^"\']*\bcontainer\b[^>]*)>', r'<div\1>', text, count=1, flags=re.I)
        text = re.sub(r"</main>", "</div>", text, count=1, flags=re.I)

    if re.search(r"<main\b", text, re.I):
        def main_repl(match: re.Match[str]) -> str:
            attrs = match.group(1)
            if not re.search(r"\bid=", attrs, re.I):
                attrs += ' id="main-content"'
            elif not re.search(r'\bid=["\']main-content["\']', attrs, re.I):
                attrs = re.sub(r'\bid=["\'][^"\']+["\']', 'id="main-content"', attrs, count=1, flags=re.I)
            if not re.search(r"\btabindex=", attrs, re.I):
                attrs += ' tabindex="-1"'
            return f"<main{attrs}>"

        return re.sub(r"<main\b([^>]*)>", main_repl, text, count=1, flags=re.I)

    body = re.search(r"<body\b[^>]*>", text, re.I)
    body_close = re.search(r"</body>", text, re.I)
    if not body or not body_close:
        raise RuntimeError(f"Cannot locate body in {path.relative_to(ROOT)}")

    wrapper = re.search(
        r'<div\b[^>]*\bclass=["\'][^"\']*\b(?:wrap|container)\b[^"\']*["\'][^>]*>',
        text[body.end() :],
        re.I,
    )
    if wrapper:
        wrapper = re.match(wrapper.re, text, re.I, wrapper.start() + body.end())
        assert wrapper is not None
        wrapper_close = find_matching_div_close(text, wrapper)
    else:
        wrapper_close = None

    search_start = wrapper.end() if wrapper else body.end()
    search_end = wrapper_close if wrapper_close is not None else body_close.start()
    nav = re.search(r"<nav\b[^>]*>.*?</nav>", text[search_start:search_end], re.I | re.S)
    main_start = search_start + nav.end() if nav else search_start
    main_end = wrapper_close if wrapper_close is not None else body_close.start()

    text = text[:main_end] + "\n    </main>\n" + text[main_end:]
    text = text[:main_start] + '\n    <main id="main-content" tabindex="-1">\n' + text[main_start:]
    return text


def add_skip_link(text: str, code: str) -> str:
    if 'class="skip-link"' in text:
        return text
    return re.sub(
        r"(<body\b[^>]*>)",
        rf'\1\n  <a class="skip-link" href="#main-content">{TEXT[code]["skip"]}</a>',
        text,
        count=1,
        flags=re.I,
    )


def add_footer(text: str, code: str) -> str:
    if re.search(r"<footer\b", text, re.I):
        return text
    footer = (
        f'  <footer class="legal-footer" aria-label="{TEXT[code]["footer_label"]}">\n'
        f'    <p>{TEXT[code]["footer"]}</p>\n'
        "  </footer>\n"
    )
    return re.sub(r"</body>", footer + "</body>", text, count=1, flags=re.I)


def fix_doc_viewer(text: str, code: str) -> str:
    text = re.sub(r'(<(?:meta|link)\b[^>]*?)\s*/>', r"\1>", text, flags=re.I)
    text = re.sub(
        r'<div\s+class="top">(.*?)</div>',
        rf'<nav class="top" aria-label="{TEXT[code]["doc_nav"]}">\1</nav>',
        text,
        count=1,
        flags=re.I | re.S,
    )
    text = re.sub(
        r'<article\b([^>]*\bid="content"[^>]*)>',
        r'<main\1 id="main-content" tabindex="-1">',
        text,
        count=1,
        flags=re.I,
    )
    # Avoid duplicate id attributes after the replacement above.
    text = re.sub(
        r'<main([^>]*)\bid="content"([^>]*)\bid="main-content"([^>]*)>',
        r'<main\1id="content"\2\3>',
        text,
        count=1,
        flags=re.I,
    )
    text = text.replace('id="content" id="main-content"', 'id="main-content"')
    text = re.sub(r"</article>", "</main>", text, count=1, flags=re.I)
    return text


def clean_generated_footer_css() -> None:
    path = ROOT / "assets" / "public-polish.css"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r"\n/\* Legal footer added automatically per language \*/.*?(?=\n@media \(max-width: 900px\))",
        "\n",
        text,
        flags=re.S,
    )
    text = re.sub(
        r"\n\s*html\[lang=\"pl\"\] body::after,\s*\n\s*html\[lang=\"en\"\] body::after,\s*\n\s*html\[lang=\"nl\"\] body::after \{.*?\n\s*\}",
        "",
        text,
        flags=re.S,
    )
    path.write_text(text, encoding="utf-8")


def process(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    code = language(text)

    if path == ROOT / "doc.html":
        text = fix_doc_viewer(text, code)

    text = convert_topnav_div(text, TEXT[code]["nav"])
    text = label_navigation(text, TEXT[code]["nav"])
    text = repair_generic_aria(text)
    text = add_main_landmark(text, path)
    text = add_skip_link(text, code)
    text = add_footer(text, code)
    text = add_shared_stylesheet(text, path)
    text = encode_raw_ampersands(text)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    html_files = sorted(p for p in ROOT.rglob("*.html") if ".git" not in p.parts)
    for path in html_files:
        process(path)

    (ROOT / "assets" / "accessibility.css").write_text(ACCESSIBILITY_CSS, encoding="utf-8")
    clean_generated_footer_css()
    print(f"Updated {len(html_files)} HTML files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def patch(path: str, replacements: list[tuple[str, str]]) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        target.write_text(text, encoding="utf-8")
        print(f"updated: {path}")


for path in ("pl/index.html", "pl/print.html"):
    patch(path, [('>Skip</a>', '>Przejdź do treści</a>')])

for path in ("en/index.html", "en/print.html"):
    patch(path, [('>Skip</a>', '>Skip to main content</a>'), ('<dt>Data</dt>', '<dt>Date</dt>')])

for path in ("nl/index.html", "nl/print.html"):
    patch(path, [('>Skip</a>', '>Ga naar de hoofdinhoud</a>'), ('<dt>Data</dt>', '<dt>Datum</dt>')])

patch("pl/contact.html", [("Copy the prepared text manually.", "Skopiuj przygotowany tekst ręcznie.")])
patch("nl/contact.html", [("Copy the prepared text manually.", "Kopieer de voorbereide tekst handmatig.")])

patch("pl/media.html", [
    ('<p><strong>Kontakt:</strong> <a href="https://www.linkedin.com/in/damian-nowak-3a50442b0"', '<p><strong>Kontakt:</strong> <a href="contact.html">formularz kontaktowy</a> lub <a href="https://www.linkedin.com/in/damian-nowak-3a50442b0"')
])
patch("en/media.html", [
    ('<p><strong>Contact:</strong> <a href="https://www.linkedin.com/in/damian-nowak-3a50442b0"', '<p><strong>Contact:</strong> <a href="contact.html">contact form</a> or <a href="https://www.linkedin.com/in/damian-nowak-3a50442b0"')
])
patch("nl/media.html", [
    ('<p><strong>Contact:</strong> <a href="https://www.linkedin.com/in/damian-nowak-3a50442b0"', '<p><strong>Contact:</strong> <a href="contact.html">contactformulier</a> of <a href="https://www.linkedin.com/in/damian-nowak-3a50442b0"')
])

# Keep the generator aligned with the corrected output.
gen = ROOT / "scripts/apply_site_information_architecture.py"
text = gen.read_text(encoding="utf-8")
text = text.replace('"menu_label": "Menu główne",', '"menu_label": "Menu główne",\n        "skip": "Przejdź do treści",\n        "copy_fallback": "Skopiuj przygotowany tekst ręcznie.",')
text = text.replace('"menu_label": "Main menu",', '"menu_label": "Main menu",\n        "skip": "Skip to main content",\n        "copy_fallback": "Copy the prepared text manually.",')
text = text.replace('"menu_label": "Hoofdmenu",', '"menu_label": "Hoofdmenu",\n        "skip": "Ga naar de hoofdinhoud",\n        "copy_fallback": "Kopieer de voorbereide tekst handmatig.",')
text = text.replace('<body><a class="skip-link" href="#main-content">Skip</a>', '<body><a class="skip-link" href="#main-content">{d[\'skip\']}</a>')
text = text.replace("<dl><dt>Data</dt><dd>{d['fact_dates'][i]}</dd>", "<dl><dt>{'Data' if lang=='pl' else ('Date' if lang=='en' else 'Datum')}</dt><dd>{d['fact_dates'][i]}</dd>")
text = text.replace("document.getElementById('copyStatus').textContent='Copy the prepared text manually.';", "document.getElementById('copyStatus').textContent='{d['copy_fallback']}';")
gen.write_text(text, encoding="utf-8")
print("updated: scripts/apply_site_information_architecture.py")

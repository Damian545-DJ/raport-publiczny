from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-07-14"

LANGS = {
    "pl": {
        "locale": "pl_PL",
        "title": "Spór pracowniczy Intrixo — publiczny raport dowodowy",
        "hero": "Publiczny raport dowodowy dotyczący sprawy Intrixo",
        "intro": "Pięć konkretnych punktów prowadzących bezpośrednio do dokumentów, wyliczeń i materiałów wymagających niezależnej weryfikacji.",
        "menu": ["Start", "Ustalenia", "Dowody", "Oś czasu", "Instytucje", "Media"],
        "paths": ["index.html", "najwazniejsze-ustalenia.html", "dowody.html", "timeline.html", "dla-instytucji.html", "media.html"],
        "menu_label": "Menu główne",
        "skip": "Przejdź do treści",
        "copy_fallback": "Skopiuj przygotowany tekst ręcznie.",
        "skip": "Przejdź do treści",
        "copy_fallback": "Skopiuj przygotowany tekst ręcznie.",
        "lang_label": "Wersja językowa",
        "facts_title": "Pięć faktów na pierwszą lekturę",
        "timeline_title": "Najważniejsze wydarzenia",
        "next_title": "Dalsza weryfikacja",
        "archive": "Archiwum źródeł",
        "print": "Druk / PDF",
        "contact": "Kontakt",
        "read": "Otwórz źródło",
        "labels": {"document": "dokument", "calculation": "wyliczenie", "verification": "weryfikacja", "private": "niepubliczne"},
        "status": ["Obowiązek zapisany w proces-verbaal", "Potwierdzony przelew; pełne dane bankowe pozostają prywatne", "Umowa źródłowa przechowywana prywatnie", "Robocza wersja wyliczenia; nie jest saldem końcowym", "Publiczny opis; pełna decyzja przechowywana prywatnie"],
        "fact_docs": ["Proces-verbaal Rechtbank Den Haag", "Potwierdzenie przelewu bankowego", "Umowa NBBU Fase 4", "Arkusz wyliczeń z 07.05.2026", "Decyzja Raad van Discipline 25-714/DH/DH"],
        "fact_dates": ["12.03.2024", "18.03.2024", "21.11.2022", "07.05.2026", "29.06.2026"],
        "fact_amounts": ["wynagrodzenie brutto od 06.05.2022", "5 000 EUR", "32 godziny tygodniowo", "7 741,03 EUR brutto", "nagana; zarzuty a i d zasadne"],
        "timeline": [
            ("06.05.2022", "Początek okresu objętego obowiązkiem wyliczenia brutto."),
            ("21.11.2022", "Umowa NBBU Fase 4 na czas nieokreślony i 32 godziny tygodniowo."),
            ("12.03.2024", "Proces-verbaal: zaliczka oraz wyliczenie brutto w ciągu dwóch tygodni."),
            ("18.03.2024", "Przelew zaliczki 5 000 EUR."),
            ("26.03.2024", "Upływ dwutygodniowego terminu na przekazanie wyliczenia."),
            ("01.04.2026", "Pierwsza wersja wyliczenia: około 3 503,05 EUR brutto."),
            ("07.05.2026", "Późniejsza wersja wyliczenia: 7 741,03 EUR brutto."),
            ("29.06.2026", "Decyzja Raad van Discipline, sygn. 25-714/DH/DH."),
        ],
        "archive_title": "Archiwum źródeł",
        "archive_intro": "Pełne pliki Markdown, dokumenty metodologiczne i techniczne zostały przeniesione z głównej strony do tego katalogu.",
        "print_title": "Wersja do druku i zapisu jako PDF",
        "print_intro": "Skrócona wersja dla instytucji i dziennikarzy. Użyj przycisku drukowania i wybierz „Zapisz jako PDF”.",
        "print_button": "Drukuj / zapisz jako PDF",
        "contact_title": "Formularz kontaktowy dla mediów i instytucji",
        "contact_intro": "Formularz nie wysyła danych na serwer. Przygotowuje uporządkowaną wiadomość, którą można skopiować i przesłać wybranym kanałem.",
        "fields": ["Imię i nazwisko", "Redakcja / instytucja", "Adres zwrotny", "Temat", "Wiadomość"],
        "copy": "Przygotuj i skopiuj wiadomość",
        "copied": "Wiadomość została skopiowana do schowka.",
        "linkedin": "Otwórz publiczny profil LinkedIn",
        "toc": "Spis treści",
    },
    "en": {
        "locale": "en_US",
        "title": "Intrixo employment dispute — public evidence report",
        "hero": "Public evidence report concerning the Intrixo matter",
        "intro": "Five concrete points leading directly to documents, calculations and materials requiring independent verification.",
        "menu": ["Start", "Findings", "Evidence", "Timeline", "Institutions", "Media"],
        "paths": ["index.html", "key-findings.html", "dowody.html", "timeline.html", "for-institutions.html", "media.html"],
        "menu_label": "Main menu",
        "skip": "Skip to main content",
        "copy_fallback": "Copy the prepared text manually.",
        "skip": "Skip to main content",
        "copy_fallback": "Copy the prepared text manually.",
        "lang_label": "Language version",
        "facts_title": "Five facts for a first reading",
        "timeline_title": "Key events",
        "next_title": "Further verification",
        "archive": "Source archive",
        "print": "Print / PDF",
        "contact": "Contact",
        "read": "Open source",
        "labels": {"document": "document", "calculation": "calculation", "verification": "verification", "private": "non-public"},
        "status": ["Obligation recorded in the proces-verbaal", "Transfer confirmed; full banking details remain private", "Source agreement held privately", "Working calculation; not the final balance", "Public description; complete decision held privately"],
        "fact_docs": ["District Court of The Hague proces-verbaal", "Bank transfer confirmation", "NBBU Fase 4 agreement", "Calculation spreadsheet dated 7 May 2026", "Raad van Discipline decision 25-714/DH/DH"],
        "fact_dates": ["12 March 2024", "18 March 2024", "21 November 2022", "7 May 2026", "29 June 2026"],
        "fact_amounts": ["gross wages from 6 May 2022", "EUR 5,000", "32 hours per week", "EUR 7,741.03 gross", "reprimand; parts a and d upheld"],
        "timeline": [
            ("6 May 2022", "Start of the period covered by the gross-wage calculation obligation."),
            ("21 Nov 2022", "NBBU Fase 4 indefinite-term agreement for 32 hours per week."),
            ("12 Mar 2024", "Proces-verbaal: advance payment and gross calculation within two weeks."),
            ("18 Mar 2024", "EUR 5,000 advance transferred."),
            ("26 Mar 2024", "Two-week deadline for providing the calculation expired."),
            ("1 Apr 2026", "First calculation version: approximately EUR 3,503.05 gross."),
            ("7 May 2026", "Later calculation version: EUR 7,741.03 gross."),
            ("29 Jun 2026", "Raad van Discipline decision, reference 25-714/DH/DH."),
        ],
        "archive_title": "Source archive",
        "archive_intro": "Full Markdown files, methodology documents and technical material have been moved from the home page to this catalogue.",
        "print_title": "Print and save-as-PDF version",
        "print_intro": "Concise version for institutions and journalists. Use the print button and select “Save as PDF”.",
        "print_button": "Print / save as PDF",
        "contact_title": "Contact form for media and institutions",
        "contact_intro": "The form does not transmit data to a server. It prepares a structured message that can be copied and sent through a chosen channel.",
        "fields": ["Name", "Newsroom / institution", "Reply address", "Subject", "Message"],
        "copy": "Prepare and copy message",
        "copied": "The message has been copied to the clipboard.",
        "linkedin": "Open the public LinkedIn profile",
        "toc": "Table of contents",
    },
    "nl": {
        "locale": "nl_NL",
        "title": "Arbeidsconflict Intrixo — publiek bewijsrapport",
        "hero": "Publiek bewijsrapport over de Intrixo-zaak",
        "intro": "Vijf concrete punten met directe links naar documenten, berekeningen en materiaal dat onafhankelijke verificatie vereist.",
        "menu": ["Start", "Bevindingen", "Bewijs", "Tijdlijn", "Instanties", "Media"],
        "paths": ["index.html", "belangrijkste-bevindingen.html", "dowody.html", "timeline.html", "voor-instanties.html", "media.html"],
        "menu_label": "Hoofdmenu",
        "skip": "Ga naar de hoofdinhoud",
        "copy_fallback": "Kopieer de voorbereide tekst handmatig.",
        "skip": "Ga naar de hoofdinhoud",
        "copy_fallback": "Kopieer de voorbereide tekst handmatig.",
        "lang_label": "Taalversie",
        "facts_title": "Vijf feiten voor een eerste lezing",
        "timeline_title": "Belangrijkste gebeurtenissen",
        "next_title": "Verdere verificatie",
        "archive": "Bronnenarchief",
        "print": "Afdrukken / PDF",
        "contact": "Contact",
        "read": "Bron openen",
        "labels": {"document": "document", "calculation": "berekening", "verification": "verificatie", "private": "niet-openbaar"},
        "status": ["Verplichting vastgelegd in het proces-verbaal", "Overschrijving bevestigd; volledige bankgegevens blijven privé", "Bronovereenkomst wordt privé bewaard", "Werkberekening; geen eindsaldo", "Publieke beschrijving; volledige beslissing wordt privé bewaard"],
        "fact_docs": ["Proces-verbaal Rechtbank Den Haag", "Bankoverschrijving", "NBBU Fase 4-overeenkomst", "Berekeningsbestand van 7 mei 2026", "Beslissing Raad van Discipline 25-714/DH/DH"],
        "fact_dates": ["12 maart 2024", "18 maart 2024", "21 november 2022", "7 mei 2026", "29 juni 2026"],
        "fact_amounts": ["brutoloon vanaf 6 mei 2022", "EUR 5.000", "32 uur per week", "EUR 7.741,03 bruto", "berisping; onderdelen a en d gegrond"],
        "timeline": [
            ("6 mei 2022", "Begin van de periode waarop de verplichting tot brutoloonberekening ziet."),
            ("21 nov 2022", "NBBU Fase 4-overeenkomst voor onbepaalde tijd en 32 uur per week."),
            ("12 mrt 2024", "Proces-verbaal: voorschot en brutoberekening binnen twee weken."),
            ("18 mrt 2024", "Voorschot van EUR 5.000 overgemaakt."),
            ("26 mrt 2024", "Einde van de termijn van twee weken voor de berekening."),
            ("1 apr 2026", "Eerste berekeningsversie: ongeveer EUR 3.503,05 bruto."),
            ("7 mei 2026", "Latere berekeningsversie: EUR 7.741,03 bruto."),
            ("29 jun 2026", "Beslissing Raad van Discipline, nummer 25-714/DH/DH."),
        ],
        "archive_title": "Bronnenarchief",
        "archive_intro": "Volledige Markdown-bestanden, methodologische documenten en technisch materiaal zijn van de startpagina naar deze catalogus verplaatst.",
        "print_title": "Versie voor afdrukken en opslaan als PDF",
        "print_intro": "Beknopte versie voor instanties en journalisten. Gebruik de afdrukknop en kies “Opslaan als PDF”.",
        "print_button": "Afdrukken / opslaan als PDF",
        "contact_title": "Contactformulier voor media en instanties",
        "contact_intro": "Het formulier verstuurt geen gegevens naar een server. Het maakt een geordend bericht dat kan worden gekopieerd en via een gekozen kanaal kan worden verzonden.",
        "fields": ["Naam", "Redactie / instantie", "Antwoordadres", "Onderwerp", "Bericht"],
        "copy": "Bericht maken en kopiëren",
        "copied": "Het bericht is naar het klembord gekopieerd.",
        "linkedin": "Open het openbare LinkedIn-profiel",
        "toc": "Inhoudsopgave",
    },
}

FACT_LINKS = {
    "pl": ["dowody.html#proces-verbaal", "../doc.html?file=PUBLICZNY_RAPORT_DOWODOWY_ANON_PL.md", "dowody.html#contract-32-hours", "../doc.html?file=PUBLICZNY_RAPORT_DOWODOWY_ANON_PL.md", "dowody.html#disciplinary-decision"],
    "en": ["dowody.html#proces-verbaal", "../doc.html?file=PUBLIC_REPORT_EVIDENCE_ANON_EN.md", "dowody.html#contract-32-hours", "../doc.html?file=PUBLIC_REPORT_EVIDENCE_ANON_EN.md", "dowody.html#disciplinary-decision"],
    "nl": ["dowody.html#proces-verbaal", "../doc.html?file=PUBLIEK_BEWIJS_RAPPORT_ANON_NL.md", "dowody.html#contract-32-hours", "../doc.html?file=PUBLIEK_BEWIJS_RAPPORT_ANON_NL.md", "dowody.html#disciplinary-decision"],
}

REPORT_FILES = {
    "pl": "PUBLICZNY_RAPORT_DOWODOWY_ANON_PL.md",
    "en": "PUBLIC_REPORT_EVIDENCE_ANON_EN.md",
    "nl": "PUBLIEK_BEWIJS_RAPPORT_ANON_NL.md",
}


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    old = target.read_text(encoding="utf-8") if target.exists() else None
    if old != content:
        target.write_text(content, encoding="utf-8")
        print(f"updated: {path}")


def shell_assets() -> None:
    css = r'''*{box-sizing:border-box}html{scroll-behavior:smooth}body{font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif!important;background:#f6f8fa;color:#1f2937}.wrap{max-width:1120px;margin:0 auto;padding:18px 16px 48px}.site-header{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;margin:0 0 18px}.desktop-nav{display:flex;gap:6px;flex-wrap:wrap}.desktop-nav a,.language-switch a,.mobile-menu a{display:inline-flex;align-items:center;min-height:38px;padding:7px 11px;border:1px solid #d0d7de;border-radius:999px;background:#fff;color:#174ea6;text-decoration:none;font-weight:700;font-size:.94rem}.desktop-nav a[aria-current="page"],.language-switch a[aria-current="true"]{background:#174ea6;color:#fff;border-color:#174ea6}.language-switch{display:flex;gap:4px;align-items:center;padding:4px;border:1px solid #d0d7de;border-radius:999px;background:#fff}.language-switch a{min-width:38px;justify-content:center;padding:5px 8px;border:0}.mobile-menu{display:none}.mobile-menu summary{cursor:pointer;list-style:none;border:1px solid #d0d7de;border-radius:999px;padding:8px 14px;background:#fff;color:#174ea6;font-weight:800}.mobile-menu summary::-webkit-details-marker{display:none}.mobile-menu .mobile-links{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;margin-top:8px;min-width:min(340px,90vw)}.mobile-menu a{justify-content:center;border-radius:10px}.hero-modern{background:linear-gradient(135deg,#fff 0%,#eef5ff 100%);border:1px solid #c7d8f5;border-radius:20px;padding:24px;margin:0 0 16px}.hero-modern h1{font-size:clamp(1.75rem,4vw,2.65rem);line-height:1.12;margin:0 0 10px;color:#123a73}.hero-modern p{max-width:780px;font-size:1.05rem}.fact-grid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px;margin:14px 0 22px}.fact-card{background:#fff;border:1px solid #d0d7de;border-radius:14px;padding:14px;min-width:0}.fact-card h2{font-size:1rem;margin:8px 0}.fact-card dl{margin:0}.fact-card dt{font-size:.75rem;text-transform:uppercase;letter-spacing:.04em;color:#667085;font-weight:800;margin-top:7px}.fact-card dd{margin:2px 0;overflow-wrap:anywhere}.fact-card a{font-weight:800}.claim-label{display:inline-flex;align-items:center;padding:3px 8px;border-radius:999px;font-size:.75rem;font-weight:800;letter-spacing:.02em}.claim-document{background:#e7f0ff;color:#174ea6}.claim-calculation{background:#e8f7ef;color:#146c43}.claim-verification{background:#fff4d6;color:#8a5a00}.claim-private{background:#f1e9f7;color:#6a3d82}.visual-timeline{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px;list-style:none;padding:0;margin:12px 0}.visual-timeline li{position:relative;background:#fff;border:1px solid #d0d7de;border-top:4px solid #5b7db1;border-radius:12px;padding:12px}.visual-timeline time{display:block;font-weight:900;color:#174ea6;margin-bottom:5px}.action-strip{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:10px}.action-strip a{display:block;background:#fff;border:1px solid #d0d7de;border-radius:12px;padding:14px;text-decoration:none;color:#1f2937;font-weight:800}.utility-links{display:flex;gap:10px;flex-wrap:wrap;margin-top:14px}.utility-links a{font-weight:750}.source-list{display:grid;gap:8px}.source-list a{display:block;background:#fff;border:1px solid #d0d7de;border-radius:10px;padding:10px;text-decoration:none}.contact-form{display:grid;gap:12px;max-width:760px}.contact-form label{font-weight:800}.contact-form input,.contact-form textarea{width:100%;padding:10px;border:1px solid #aeb7c2;border-radius:10px;font:inherit}.contact-form textarea{min-height:130px}.contact-output{white-space:pre-wrap;background:#fff;border:1px solid #d0d7de;border-radius:10px;padding:12px;min-height:80px}.print-actions{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}.toc-panel{background:#fff;border:1px solid #d0d7de;border-radius:12px;padding:12px;margin:0 0 16px}.toc-panel ol{columns:2;column-gap:30px}.toc-panel a{text-decoration:none}.legal-footer{font-size:.9rem}.legal-footer .footer-tools{margin-top:8px;display:flex;gap:10px;flex-wrap:wrap}@media(max-width:960px){.fact-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.visual-timeline{grid-template-columns:repeat(2,minmax(0,1fr))}.action-strip{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:720px){.desktop-nav{display:none}.mobile-menu{display:block}.site-header{align-items:flex-start}.language-switch{margin-left:auto}.fact-grid,.visual-timeline,.action-strip{grid-template-columns:1fr}.fact-card{padding:12px}.toc-panel ol{columns:1}.wrap{padding-top:12px}}@media print{.site-header,.print-actions,.language-switch,.mobile-menu,.desktop-nav,.footer-tools{display:none!important}body{background:#fff}.wrap{max-width:none;padding:0}.card,.fact-card,.hero-modern,.visual-timeline li{box-shadow:none;break-inside:avoid;border-color:#999}a{color:#000;text-decoration:none}a[href]::after{content:""}}'''
    js = r'''(()=>{const lang=(document.documentElement.lang||"en").slice(0,2);const cfg={pl:{menu:["Start","Ustalenia","Dowody","Oś czasu","Instytucje","Media"],paths:["index.html","najwazniejsze-ustalenia.html","dowody.html","timeline.html","dla-instytucji.html","media.html"],menuLabel:"Menu",langLabel:"Język",archive:"Archiwum źródeł",print:"Druk / PDF",contact:"Kontakt",labels:{document:"dokument",calculation:"wyliczenie",verification:"weryfikacja",private:"niepubliczne"}},en:{menu:["Start","Findings","Evidence","Timeline","Institutions","Media"],paths:["index.html","key-findings.html","dowody.html","timeline.html","for-institutions.html","media.html"],menuLabel:"Menu",langLabel:"Language",archive:"Source archive",print:"Print / PDF",contact:"Contact",labels:{document:"document",calculation:"calculation",verification:"verification",private:"non-public"}},nl:{menu:["Start","Bevindingen","Bewijs","Tijdlijn","Instanties","Media"],paths:["index.html","belangrijkste-bevindingen.html","dowody.html","timeline.html","voor-instanties.html","media.html"],menuLabel:"Menu",langLabel:"Taal",archive:"Bronnenarchief",print:"Afdrukken / PDF",contact:"Contact",labels:{document:"document",calculation:"berekening",verification:"verificatie",private:"niet-openbaar"}}}[lang]||null;if(!cfg)return;const page=location.pathname.split("/").pop()||"index.html";document.querySelectorAll("[data-site-nav]").forEach(nav=>{const links=cfg.menu.map((label,i)=>`<a href="${cfg.paths[i]}"${page===cfg.paths[i]?' aria-current="page"':''}>${label}</a>`).join("");nav.innerHTML=`<div class="desktop-nav">${links}</div><details class="mobile-menu"><summary>${cfg.menuLabel}</summary><div class="mobile-links">${links}</div></details>`;nav.setAttribute("aria-label",cfg.menuLabel)});const equivalents={"index.html":["index.html","index.html","index.html"],"najwazniejsze-ustalenia.html":["najwazniejsze-ustalenia.html","key-findings.html","belangrijkste-bevindingen.html"],"key-findings.html":["najwazniejsze-ustalenia.html","key-findings.html","belangrijkste-bevindingen.html"],"belangrijkste-bevindingen.html":["najwazniejsze-ustalenia.html","key-findings.html","belangrijkste-bevindingen.html"],"dowody.html":["dowody.html","dowody.html","dowody.html"],"timeline.html":["timeline.html","timeline.html","timeline.html"],"dla-instytucji.html":["dla-instytucji.html","for-institutions.html","voor-instanties.html"],"for-institutions.html":["dla-instytucji.html","for-institutions.html","voor-instanties.html"],"voor-instanties.html":["dla-instytucji.html","for-institutions.html","voor-instanties.html"],"media.html":["media.html","media.html","media.html"],"archive.html":["archive.html","archive.html","archive.html"],"print.html":["print.html","print.html","print.html"],"contact.html":["contact.html","contact.html","contact.html"],"home-of-people.html":["home-of-people.html","home-of-people.html","home-of-people.html"]};const eq=equivalents[page]||equivalents["index.html"];document.querySelectorAll("[data-language-switch]").forEach(el=>{el.className="language-switch";el.setAttribute("aria-label",cfg.langLabel);el.innerHTML=[["PL","pl",eq[0]],["EN","en",eq[1]],["NL","nl",eq[2]]].map(([label,code,file])=>`<a href="../${code}/${file}" hreflang="${code}" lang="${code}"${lang===code?' aria-current="true"':''}>${label}</a>`).join("")});const classify=t=>{t=t.toLowerCase();if(/private|prywat|niet-openbaar|non-public/.test(t))return"private";if(/calcul|wylicz|bereken|amount|kwot/.test(t))return"calculation";if(/decision|decyz|beslissing|contract|umow|overeenkomst|proces-verbaal/.test(t))return"document";return"verification"};document.querySelectorAll("main section.card h2,main article.card h2").forEach(h=>{if(h.querySelector('.claim-label'))return;const type=classify(h.textContent);const span=document.createElement('span');span.className=`claim-label claim-${type}`;span.textContent=cfg.labels[type];h.before(span)});document.querySelectorAll('.legal-footer').forEach(f=>{if(f.querySelector('.footer-tools'))return;const d=document.createElement('div');d.className='footer-tools';d.innerHTML=`<a href="archive.html">${cfg.archive}</a><a href="print.html">${cfg.print}</a><a href="contact.html">${cfg.contact}</a>`;f.appendChild(d)});})();'''
    write("assets/site-shell.css", css + "\n")
    write("assets/site-shell.js", js + "\n")


def head(lang: str, title: str, description: str, page: str) -> str:
    d = LANGS[lang]
    url = f"https://damian545-dj.github.io/raport-publiczny/{lang}/{page}"
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="pl" href="https://damian545-dj.github.io/raport-publiczny/pl/{page}">
<link rel="alternate" hreflang="en" href="https://damian545-dj.github.io/raport-publiczny/en/{page}">
<link rel="alternate" hreflang="nl" href="https://damian545-dj.github.io/raport-publiczny/nl/{page}">
<link rel="alternate" hreflang="x-default" href="https://damian545-dj.github.io/raport-publiczny/en/{page}">
<link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
<meta property="og:type" content="website">
<meta property="og:locale" content="{d['locale']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="https://damian545-dj.github.io/raport-publiczny/assets/og-image-neutral.png">
<link rel="stylesheet" href="../assets/accessibility.css">
<link rel="stylesheet" href="../assets/site-shell.css">
<script defer src="../assets/site-shell.js"></script>
<script type="application/ld+json">{json.dumps({'@context':'https://schema.org','@type':'Report','name':title,'url':url,'inLanguage':lang,'dateModified':DATE,'isAccessibleForFree':True}, ensure_ascii=False)}</script>
</head>'''


def nav(lang: str) -> str:
    return f'''<div class="site-header"><nav data-site-nav></nav><div data-language-switch></div></div>'''


def footer(lang: str) -> str:
    text = {
        "pl": "© 2026. Publiczna wersja jest zanonimizowana. Materiał służy niezależnej weryfikacji i nie stanowi porady prawnej ani prawomocnego rozstrzygnięcia.",
        "en": "© 2026. The public version is anonymized. The material is intended for independent verification and is not legal advice or a final legal determination.",
        "nl": "© 2026. De publieke versie is geanonimiseerd. Het materiaal is bedoeld voor onafhankelijke verificatie en vormt geen juridisch advies of definitieve juridische beslissing.",
    }[lang]
    return f'''<footer class="legal-footer"><p>{text}</p></footer>'''


def fact_cards(lang: str) -> str:
    d = LANGS[lang]
    types = ["document", "private", "document", "calculation", "private"]
    cards = []
    for i in range(5):
        cards.append(f'''<article class="fact-card"><span class="claim-label claim-{types[i]}">{d['labels'][types[i]]}</span><h2>{d['fact_docs'][i]}</h2><dl><dt>{'Data' if lang=='pl' else ('Date' if lang=='en' else 'Datum')}</dt><dd>{d['fact_dates'][i]}</dd><dt>{'Kwota / zakres' if lang=='pl' else ('Amount / scope' if lang=='en' else 'Bedrag / reikwijdte')}</dt><dd>{d['fact_amounts'][i]}</dd><dt>Status</dt><dd>{d['status'][i]}</dd></dl><p><a href="{FACT_LINKS[lang][i]}">{d['read']} →</a></p></article>''')
    return "".join(cards)


def home_page(lang: str) -> str:
    d = LANGS[lang]
    items = "".join(f'<li><time>{date}</time><span>{text}</span></li>' for date, text in d["timeline"])
    report = REPORT_FILES[lang]
    description = d["intro"]
    return head(lang, d["title"], description, "index.html") + f'''
<body><a class="skip-link" href="#main-content">{d['skip']}</a><div class="wrap">{nav(lang)}<main id="main-content" tabindex="-1">
<section class="hero-modern"><h1>{d['hero']}</h1><p>{d['intro']}</p><p><strong>{'Wersja' if lang=='pl' else ('Version' if lang=='en' else 'Versie')} 3.0</strong> · {DATE}</p></section>
<section aria-labelledby="facts-title"><h2 id="facts-title">{d['facts_title']}</h2><div class="fact-grid">{fact_cards(lang)}</div></section>
<section class="card"><h2>{d['timeline_title']}</h2><ol class="visual-timeline">{items}</ol><p><a href="timeline.html">{d['read']} →</a></p></section>
<section class="card"><h2>{d['next_title']}</h2><div class="action-strip"><a href="../doc.html?file={report}">{'Pełny raport' if lang=='pl' else ('Full report' if lang=='en' else 'Volledig rapport')}</a><a href="archive.html">{d['archive']}</a><a href="print.html">{d['print']}</a><a href="contact.html">{d['contact']}</a></div></section>
</main>{footer(lang)}</div></body></html>'''


def archive_page(lang: str) -> str:
    d = LANGS[lang]
    files = [
        (REPORT_FILES[lang], "Full evidence report"),
        (f"README.{lang}.md", "Overview / README"),
        (f"TIMELINE.{lang}.md", "Full timeline"),
        (f"EVIDENCE_INDEX.{lang}.md", "Evidence catalogue"),
        (f"ALLEGATIONS_AND_LAW.{lang}.md", "Legal verification map"),
        (f"ANONYMIZATION.{lang}.md", "Anonymization rules"),
        (f"DISCLAIMER.{lang}.md", "Legal disclaimer"),
        (f"home-of-people/README.{lang}.md", "Corporate context"),
        ("UPDATES.md", "Update log"),
    ]
    labels = {
        "pl": ["Pełny raport dowodowy", "Przegląd / README", "Pełna oś czasu", "Katalog dowodów", "Mapa prawna do weryfikacji", "Zasady anonimizacji", "Zastrzeżenia prawne", "Kontekst korporacyjny", "Rejestr aktualizacji"],
        "en": [x[1] for x in files],
        "nl": ["Volledig bewijsrapport", "Overzicht / README", "Volledige tijdlijn", "Bewijscatalogus", "Juridische verificatiekaart", "Anonimiseringsregels", "Juridische disclaimer", "Bedrijfscontext", "Wijzigingslogboek"],
    }[lang]
    links = "".join(f'<a href="../doc.html?file={path}"><strong>{labels[i]}</strong><br><code>{path}</code></a>' for i, (path, _) in enumerate(files))
    return head(lang, d["archive_title"], d["archive_intro"], "archive.html") + f'''<body><div class="wrap">{nav(lang)}<main id="main-content"><section class="hero-modern"><h1>{d['archive_title']}</h1><p>{d['archive_intro']}</p></section><section class="card"><div class="source-list">{links}</div></section></main>{footer(lang)}</div></body></html>'''


def print_page(lang: str) -> str:
    d = LANGS[lang]
    items = "".join(f'<li><time>{date}</time><span>{text}</span></li>' for date, text in d["timeline"])
    return head(lang, d["print_title"], d["print_intro"], "print.html") + f'''<body><div class="wrap">{nav(lang)}<main id="main-content"><section class="hero-modern"><h1>{d['print_title']}</h1><p>{d['print_intro']}</p><div class="print-actions"><button type="button" onclick="window.print()">{d['print_button']}</button><a href="../doc.html?file={REPORT_FILES[lang]}">{d['read']}</a></div></section><section><h2>{d['facts_title']}</h2><div class="fact-grid">{fact_cards(lang)}</div></section><section class="card"><h2>{d['timeline_title']}</h2><ol class="visual-timeline">{items}</ol></section><section class="card"><h2>{d['archive']}</h2><p><a href="archive.html">{d['archive']} →</a></p></section></main>{footer(lang)}</div></body></html>'''


def contact_page(lang: str) -> str:
    d = LANGS[lang]
    f = d["fields"]
    return head(lang, d["contact_title"], d["contact_intro"], "contact.html") + f'''<body><div class="wrap">{nav(lang)}<main id="main-content"><section class="hero-modern"><h1>{d['contact_title']}</h1><p>{d['contact_intro']}</p></section><section class="card"><form id="contactForm" class="contact-form"><label>{f[0]}<input name="name" required></label><label>{f[1]}<input name="org"></label><label>{f[2]}<input name="reply" type="email"></label><label>{f[3]}<input name="subject" required></label><label>{f[4]}<textarea name="message" required></textarea></label><button type="submit">{d['copy']}</button></form><p id="copyStatus" role="status"></p><pre id="contactOutput" class="contact-output"></pre><p><a href="https://www.linkedin.com/in/damian-nowak-3a50442b0" target="_blank" rel="noopener noreferrer">{d['linkedin']}</a></p></section></main>{footer(lang)}</div><script>document.getElementById('contactForm').addEventListener('submit',async e=>{{e.preventDefault();const x=Object.fromEntries(new FormData(e.target));const text=`{f[0]}: ${{x.name}}\n{f[1]}: ${{x.org||'-'}}\n{f[2]}: ${{x.reply||'-'}}\n{f[3]}: ${{x.subject}}\n\n${{x.message}}`;document.getElementById('contactOutput').textContent=text;try{{await navigator.clipboard.writeText(text);document.getElementById('copyStatus').textContent='{d['copied']}';}}catch(_e){{document.getElementById('copyStatus').textContent='{d['copy_fallback']}';}}}});</script></body></html>'''


def inject_shell() -> None:
    for lang in LANGS:
        for path in (ROOT / lang).glob("*.html"):
            if path.name in {"index.html", "archive.html", "print.html", "contact.html"}:
                continue
            text = path.read_text(encoding="utf-8")
            original = text
            if "../assets/site-shell.css" not in text:
                text = text.replace("</head>", '<link rel="stylesheet" href="../assets/site-shell.css">\n<script defer src="../assets/site-shell.js"></script>\n</head>')
            # Replace the first navigation block with the shared shell.
            text, n = re.subn(r'<nav\b[^>]*>.*?</nav>', nav(lang), text, count=1, flags=re.DOTALL | re.IGNORECASE)
            if not n and "<body" in text:
                text = re.sub(r'(<body[^>]*>)', r'\1\n<div class="wrap">' + nav(lang), text, count=1)
            text = text.replace("og-image-en.png", "og-image-neutral.png").replace("og-image-pl.png", "og-image-neutral.png").replace("og-image-nl.png", "og-image-neutral.png")
            if path.name == "media.html" and "contact.html" not in text:
                label = {"pl":"Formularz kontaktowy bez konta LinkedIn","en":"Contact form without a LinkedIn account","nl":"Contactformulier zonder LinkedIn-account"}[lang]
                block = f'<section class="card"><h2>{label}</h2><p><a class="btn" href="contact.html">{LANGS[lang]["contact"]}</a></p></section>'
                text = text.replace("</main>", block + "\n</main>")
            if text != original:
                path.write_text(text, encoding="utf-8")
                print(f"updated: {path.relative_to(ROOT)}")


def enhance_doc_viewer() -> None:
    path = ROOT / "doc.html"
    text = path.read_text(encoding="utf-8")
    original = text
    if "id=\"docToc\"" not in text:
        text = text.replace('<main class="markdown-body md" id="main-content"', '<aside id="docToc" class="toc-panel" hidden></aside>\n    <main class="markdown-body md" id="main-content"')
    if "function buildDocumentToc" not in text:
        function = r'''
    function buildDocumentToc(lang) {
      const headings = [...document.querySelectorAll("#main-content h2, #main-content h3")];
      const toc = document.getElementById("docToc");
      if (headings.length < 4) { toc.hidden = true; return; }
      const title = UI[lang].toc || (lang === "pl" ? "Spis treści" : lang === "nl" ? "Inhoudsopgave" : "Table of contents");
      const used = new Set();
      const items = headings.map((heading, index) => {
        let id = heading.id || heading.textContent.toLowerCase().normalize("NFKD").replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,"") || `section-${index+1}`;
        while (used.has(id)) id += `-${index+1}`;
        used.add(id); heading.id = id;
        return `<li class="toc-level-${heading.tagName.toLowerCase()}"><a href="#${id}">${heading.textContent}</a></li>`;
      }).join("");
      toc.innerHTML = `<strong>${title}</strong><ol>${items}</ol>`;
      toc.hidden = false;
    }
'''
        text = text.replace("    async function load() {", function + "\n    async function load() {")
        text = text.replace("        enhanceRenderedTables(lang);", "        enhanceRenderedTables(lang);\n        buildDocumentToc(lang);")
        text = text.replace('table: "Tabela w dokumencie — przewijaj poziomo klawiaturą, jeżeli jest to potrzebne"', 'table: "Tabela w dokumencie — przewijaj poziomo klawiaturą, jeżeli jest to potrzebne", toc: "Spis treści"')
        text = text.replace('table: "Document table — use the keyboard to scroll horizontally when necessary"', 'table: "Document table — use the keyboard to scroll horizontally when necessary", toc: "Table of contents"')
        text = text.replace('table: "Tabel in het document — gebruik het toetsenbord om indien nodig horizontaal te scrollen"', 'table: "Tabel in het document — gebruik het toetsenbord om indien nodig horizontaal te scrollen", toc: "Inhoudsopgave"')
    if "assets/site-shell.css" not in text:
        text = text.replace('<link rel="stylesheet" href="assets/accessibility.css">', '<link rel="stylesheet" href="assets/accessibility.css">\n<link rel="stylesheet" href="assets/site-shell.css">')
    if text != original:
        path.write_text(text, encoding="utf-8")
        print("updated: doc.html")


def main() -> None:
    shell_assets()
    for lang in LANGS:
        write(f"{lang}/index.html", home_page(lang))
        write(f"{lang}/archive.html", archive_page(lang))
        write(f"{lang}/print.html", print_page(lang))
        write(f"{lang}/contact.html", contact_page(lang))
    inject_shell()
    enhance_doc_viewer()


if __name__ == "__main__":
    main()

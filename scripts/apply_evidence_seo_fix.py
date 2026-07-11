#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://damian545-dj.github.io/raport-publiczny/"


def write(path: str, content: str) -> None:
    (ROOT / path).write_text(content.strip() + "\n", encoding="utf-8")


COMMON_STYLE = """
    :root { --bg:#f6f8fa; --text:#1f2328; --muted:#57606a; --line:#d0d7de; --card:#ffffff; --accent:#0550ae; --soft:#eef5ff; --warn:#fff8c5; }
    * { box-sizing:border-box; }
    body { margin:0; font-family:Arial,Helvetica,sans-serif; background:var(--bg); color:var(--text); line-height:1.62; }
    .wrap { max-width:1120px; margin:0 auto; padding:24px 16px 48px; }
    .card { background:var(--card); border:1px solid var(--line); border-radius:12px; padding:18px; margin:14px 0; }
    .note { background:var(--soft); }
    .warning { background:var(--warn); }
    h1 { margin:0 0 10px; color:var(--accent); font-size:1.9rem; }
    h2 { margin:0 0 10px; font-size:1.25rem; }
    h3 { margin:18px 0 8px; font-size:1.08rem; }
    p { margin:8px 0; }
    .muted,.meta { color:var(--muted); font-size:.95rem; }
    .btn,a.btn { display:inline-block; border:1px solid var(--line); border-radius:999px; padding:8px 12px; text-decoration:none; color:var(--accent); font-weight:700; background:#fff; margin:4px 6px 4px 0; }
    .topnav { display:flex; gap:8px; flex-wrap:wrap; margin-bottom:12px; }
    blockquote { margin:12px 0; padding:12px 16px; border-left:4px solid var(--accent); background:#f6f8fa; }
    code { padding:.15em .35em; border-radius:5px; background:#eef1f4; }
    .table-wrap { overflow-x:auto; }
    table { width:100%; border-collapse:collapse; margin:12px 0; background:#fff; }
    th,td { border:1px solid var(--line); padding:10px; text-align:left; vertical-align:top; }
    th { background:#eef5ff; }
    .source { margin-top:12px; padding-top:10px; border-top:1px dashed var(--line); }
    ul { margin:8px 0 8px 20px; }
    @media (max-width:720px) { th,td { min-width:170px; } }
"""


def page(lang: str, title: str, description: str, og_description: str, nav: str, body: str) -> str:
    return dedent(f"""
    <!DOCTYPE html>
    <html lang="{lang}">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>{title}</title>
      <meta name="description" content="{description}">
      <link rel="canonical" href="{BASE}{lang}/dowody.html">
      <link rel="icon" type="image/svg+xml" href="../assets/favicon.svg">
      <meta property="og:type" content="website">
      <meta property="og:title" content="{title}">
      <meta property="og:description" content="{og_description}">
      <meta property="og:url" content="{BASE}{lang}/dowody.html">
      <meta property="og:image" content="{BASE}assets/og-image-en.png">
      <style>{COMMON_STYLE}</style>
      <link rel="stylesheet" href="../assets/public-polish.css">
    </head>
    <body>
      <div class="wrap">
        <nav class="topnav" aria-label="Language and section navigation">{nav}</nav>
        <main id="main-content">
          {body}
        </main>
      </div>
    </body>
    </html>
    """)


pl_body = """
<section class="card">
  <h1>5 najmocniejszych dowodów — fragmenty do samodzielnej weryfikacji</h1>
  <p>Ta strona pokazuje zanonimizowane fragmenty treści dokumentów, a nie tylko ich opisy. Dane osobowe, podpisy, numery rachunków i wewnętrzne identyfikatory zostały pominięte.</p>
  <p class="meta">Fragment oznacza wierne przytoczenie istotnego pola lub sentencji. Nie zastępuje on pełnego dokumentu, który może zostać udostępniony właściwej instytucji lub zweryfikowanemu dziennikarzowi w bezpiecznym trybie.</p>
</section>
<section class="card note">
  <h2>1. Proces-verbaal z 12.03.2024</h2>
  <p><strong>Rodzaj dokumentu:</strong> protokół sądowy / proces-verbaal.</p>
  <blockquote lang="nl">een berekening van het sinds 6 mei 2022 verschuldigde bruto loon</blockquote>
  <p><strong>Co dokładnie potwierdza:</strong> Intrixo miało w ciągu dwóch tygodni przekazać pełnomocnikowi pracownicy wyliczenie należnego wynagrodzenia brutto od 6 maja 2022 r. Nie był to ogólny obowiązek obu stron.</p>
</section>
<section class="card">
  <h2>2. Umowa Fase 4 / Fase C — gwarancja 32 godzin</h2>
  <p><strong>Data rozpoczęcia wskazana w dokumentacji:</strong> 21.11.2022.</p>
  <blockquote lang="nl">arbeidsovereenkomst voor onbepaalde tijd · 32 uur per week · geen oproepovereenkomst</blockquote>
  <p><strong>Co dokładnie potwierdza:</strong> umowę na czas nieokreślony, wymiar 32 godzin tygodniowo i brak charakteru umowy na wezwanie. Fragment jest publicznym odpisem istotnych pól; dane stron i podpisy pozostają niepubliczne.</p>
</section>
<section class="card warning">
  <h2>3. Przykład pola z loonstrooka</h2>
  <blockquote lang="nl">Contracturen: 1:00 uur per week</blockquote>
  <p><strong>Co dokładnie potwierdza:</strong> na części pasków płacowych widnieje wymiar 1 godziny tygodniowo, mimo że dokumentacja umowy wskazuje 32 godziny. Sam zapis nie przesądza wysokości roszczenia, ale wymaga wyjaśnienia historii danych płacowych i korekt.</p>
</section>
<section class="card">
  <h2>4. Rejestr brakujących albo spóźnionych pasków i tygodni</h2>
  <p>Poniższa tabela przedstawia roboczy stan pakietu dokumentów. Określenie „brak” oznacza brak potwierdzonego kompletnego paska w analizowanym pakiecie, a nie twierdzenie, że dokument nigdy nie istniał.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Rok</th><th>Tygodnie wymagające uzupełnienia lub potwierdzenia</th><th>Status publiczny</th></tr></thead>
    <tbody>
      <tr><td>2022</td><td>W37, W38, W39, W48, W49</td><td>brak kompletnego, potwierdzonego zestawu w roboczym rejestrze</td></tr>
      <tr><td>2023</td><td>W13, W16, W31–W36, W38, W42–W46</td><td>brak albo niepełne ujęcie wymagające porównania z pełną loonadministratie</td></tr>
      <tr><td>2024</td><td>W02, W23</td><td>wymagają uzupełnienia lub jednoznacznego przypisania dokumentu</td></tr>
      <tr><td>2025</td><td>W32</td><td>dokument otrzymano później; nie jest już traktowany jako nieistniejący, lecz musi zostać włączony do pełnego rozrachunku</td></tr>
    </tbody>
  </table></div>
</section>
<section class="card note">
  <h2>5. Oficjalna decyzja Raad van Discipline</h2>
  <p><strong>Data i sygnatura:</strong> 29.06.2026, 25-714/DH/DH.</p>
  <blockquote lang="nl">het verzet gegrond · klachtonderdelen a) en d) gegrond · maatregel van berisping</blockquote>
  <p><strong>Co dokładnie potwierdza sentencja:</strong> sprzeciw został uwzględniony, wcześniejsza decyzja przewodniczącego została uchylona, zarzuty a) i d) uznano za zasadne, b) i c) za niezasadne, a wobec adwokata zastosowano karę nagany. Orzeczono również zwrot opłaty 50 EUR skarżącej oraz 1 250 EUR kosztów na rzecz Nederlandse Orde van Advocaten.</p>
  <p>Oficjalna decyzja znajduje się w posiadaniu autorów. W chwili tej aktualizacji nie odnaleziono jej bezpośredniego publicznego adresu w oficjalnej bazie; wyszukiwanie można prowadzić po sygnaturze w serwisie <a href="https://tuchtrecht.overheid.nl/" target="_blank" rel="noopener noreferrer">Tuchtrecht</a>. Zanonimizowana kopia może zostać udostępniona do niezależnej weryfikacji.</p>
</section>
<section class="card">
  <h2>Tabela kontrolna: twierdzenie — dokument — data — potwierdzenie</h2>
  <div class="table-wrap"><table>
    <thead><tr><th>Twierdzenie</th><th>Dokument</th><th>Data</th><th>Co dokładnie potwierdza</th></tr></thead>
    <tbody>
      <tr><td>Intrixo miało sporządzić pełne wyliczenie brutto od 06.05.2022</td><td>proces-verbaal</td><td>12.03.2024</td><td>konkretny obowiązek i początkową datę okresu rozliczeniowego</td></tr>
      <tr><td>Umowa przewidywała 32 godziny tygodniowo</td><td>umowa Fase 4 / Fase C</td><td>od 21.11.2022</td><td>czas nieokreślony, 32 h tygodniowo, brak umowy na wezwanie</td></tr>
      <tr><td>Na części pasków widnieje 1 godzina</td><td>loonstrooki</td><td>okres obowiązywania umowy</td><td>rozbieżność pola Contracturen względem danych umowy</td></tr>
      <tr><td>Pakiet dokumentów ma luki i dokumenty otrzymane po czasie</td><td>rejestr loonstrooków i korespondencja</td><td>2022–2025</td><td>tygodnie wymagające uzupełnienia, przypisania lub kontroli wersji</td></tr>
      <tr><td>Część skargi dyscyplinarnej była zasadna</td><td>decyzja Raad van Discipline</td><td>29.06.2026</td><td>uwzględnienie sprzeciwu, zasadność punktów a) i d) oraz naganę</td></tr>
    </tbody>
  </table></div>
  <p class="source"><a href="../EVIDENCE_INDEX.pl.md">Indeks dowodów w Markdown</a> · <a href="dla-instytucji.html">Bezpieczny dostęp dla instytucji</a></p>
</section>
"""

pl_nav = '<a class="btn" href="index.html">PL start</a><a class="btn" href="timeline.html">Oś czasu</a><a class="btn" href="najwazniejsze-ustalenia.html">Najważniejsze ustalenia</a><a class="btn" href="media.html">Media</a><a class="btn" href="../en/dowody.html">EN</a><a class="btn" href="../nl/dowody.html">NL</a>'


en_body = """
<section class="card">
  <h1>5 strongest evidence points — excerpts for independent verification</h1>
  <p>This page shows anonymised excerpts from document content, not only summaries. Personal data, signatures, account numbers and internal identifiers have been omitted.</p>
  <p class="meta">An excerpt is a faithful reproduction of a relevant field or operative part. It does not replace the full document, which can be shared securely with a competent institution or verified journalist.</p>
</section>
<section class="card note">
  <h2>1. Process-verbaal of 12 March 2024</h2>
  <p><strong>Document type:</strong> court record / process-verbaal.</p>
  <blockquote lang="nl">een berekening van het sinds 6 mei 2022 verschuldigde bruto loon</blockquote>
  <p><strong>What it specifically supports:</strong> Intrixo had to provide the worker's representative, within two weeks, with a calculation of gross wages due since 6 May 2022. This was not a general obligation imposed on both parties.</p>
</section>
<section class="card">
  <h2>2. Phase 4 / Phase C agreement — 32-hour guarantee</h2>
  <p><strong>Start date stated in the records:</strong> 21 November 2022.</p>
  <blockquote lang="nl">arbeidsovereenkomst voor onbepaalde tijd · 32 uur per week · geen oproepovereenkomst</blockquote>
  <p><strong>What it specifically supports:</strong> an indefinite-term agreement, 32 hours per week and no on-call contract. The excerpt reproduces relevant fields only; party details and signatures remain non-public.</p>
</section>
<section class="card warning">
  <h2>3. Example field from a payslip</h2>
  <blockquote lang="nl">Contracturen: 1:00 uur per week</blockquote>
  <p><strong>What it specifically supports:</strong> some payslips state one contractual hour per week although the agreement records 32 hours. The field alone does not determine the amount of a claim, but it requires an explanation of payroll-data and correction history.</p>
</section>
<section class="card">
  <h2>4. Register of missing or late payslips and weeks</h2>
  <p>The table reflects the working document inventory. “Missing” means that a confirmed complete payslip was not present in the analysed package; it does not assert that the document never existed.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Year</th><th>Weeks requiring completion or confirmation</th><th>Public status</th></tr></thead>
    <tbody>
      <tr><td>2022</td><td>W37, W38, W39, W48, W49</td><td>no complete confirmed set in the working register</td></tr>
      <tr><td>2023</td><td>W13, W16, W31–W36, W38, W42–W46</td><td>missing or incompletely represented; comparison with full payroll administration required</td></tr>
      <tr><td>2024</td><td>W02, W23</td><td>completion or unambiguous document allocation required</td></tr>
      <tr><td>2025</td><td>W32</td><td>received later; no longer treated as nonexistent, but it must be incorporated into the full account</td></tr>
    </tbody>
  </table></div>
</section>
<section class="card note">
  <h2>5. Official Raad van Discipline decision</h2>
  <p><strong>Date and reference:</strong> 29 June 2026, 25-714/DH/DH.</p>
  <blockquote lang="nl">het verzet gegrond · klachtonderdelen a) en d) gegrond · maatregel van berisping</blockquote>
  <p><strong>What the operative part specifically supports:</strong> the objection was upheld, the chair's earlier decision was set aside, complaint parts a) and d) were upheld, b) and c) were dismissed, and a reprimand was imposed. The decision also ordered reimbursement of the EUR 50 filing fee to the complainant and EUR 1,250 in costs to the Dutch Bar.</p>
  <p>The official decision is held by the authors. At the time of this update no direct public result URL was found in the official database; it can be searched by reference at <a href="https://tuchtrecht.overheid.nl/" target="_blank" rel="noopener noreferrer">Tuchtrecht</a>. An anonymised copy can be provided for independent verification.</p>
</section>
<section class="card">
  <h2>Control table: claim — document — date — exact support</h2>
  <div class="table-wrap"><table>
    <thead><tr><th>Claim</th><th>Document</th><th>Date</th><th>What it specifically supports</th></tr></thead>
    <tbody>
      <tr><td>Intrixo had to calculate gross wages from 6 May 2022</td><td>process-verbaal</td><td>12 March 2024</td><td>the specific obligation and starting date of the accounting period</td></tr>
      <tr><td>The agreement provided 32 hours per week</td><td>Phase 4 / Phase C agreement</td><td>from 21 November 2022</td><td>indefinite term, 32 weekly hours and no on-call agreement</td></tr>
      <tr><td>Some payslips state one hour</td><td>payslips</td><td>during the agreement</td><td>the Contracturen discrepancy against agreement data</td></tr>
      <tr><td>The document package has gaps and late documents</td><td>payslip register and correspondence</td><td>2022–2025</td><td>weeks requiring completion, allocation or version control</td></tr>
      <tr><td>Part of the disciplinary complaint was upheld</td><td>Raad van Discipline decision</td><td>29 June 2026</td><td>upheld objection, upheld parts a) and d), and reprimand</td></tr>
    </tbody>
  </table></div>
  <p class="source"><a href="../EVIDENCE_INDEX.en.md">Evidence index in Markdown</a> · <a href="for-institutions.html">Secure access for institutions</a></p>
</section>
"""

en_nav = '<a class="btn" href="index.html">EN start</a><a class="btn" href="timeline.html">Timeline</a><a class="btn" href="key-findings.html">Key findings</a><a class="btn" href="media.html">Media</a><a class="btn" href="../pl/dowody.html">PL</a><a class="btn" href="../nl/dowody.html">NL</a>'


nl_body = """
<section class="card">
  <h1>5 sterkste bewijspunten — fragmenten voor zelfstandige verificatie</h1>
  <p>Deze pagina toont geanonimiseerde fragmenten uit documenten en niet alleen samenvattingen. Persoonsgegevens, handtekeningen, rekeningnummers en interne kenmerken zijn weggelaten.</p>
  <p class="meta">Een fragment is een getrouwe weergave van een relevant veld of dictum. Het vervangt niet het volledige document, dat veilig aan een bevoegde instantie of geverifieerde journalist kan worden verstrekt.</p>
</section>
<section class="card note">
  <h2>1. Proces-verbaal van 12 maart 2024</h2>
  <p><strong>Documentsoort:</strong> proces-verbaal van de gerechtelijke fase.</p>
  <blockquote>een berekening van het sinds 6 mei 2022 verschuldigde bruto loon</blockquote>
  <p><strong>Wat dit precies bevestigt:</strong> Intrixo moest binnen twee weken aan de gemachtigde van de werkneemster een berekening verstrekken van het vanaf 6 mei 2022 verschuldigde brutoloon. Dit was geen algemene verplichting voor beide partijen.</p>
</section>
<section class="card">
  <h2>2. Fase 4 / Fase C-overeenkomst — garantie van 32 uur</h2>
  <p><strong>In de stukken vermelde ingangsdatum:</strong> 21 november 2022.</p>
  <blockquote>arbeidsovereenkomst voor onbepaalde tijd · 32 uur per week · geen oproepovereenkomst</blockquote>
  <p><strong>Wat dit precies bevestigt:</strong> een overeenkomst voor onbepaalde tijd, 32 uur per week en geen oproepovereenkomst. Alleen de relevante velden zijn weergegeven; partijgegevens en handtekeningen blijven niet-openbaar.</p>
</section>
<section class="card warning">
  <h2>3. Voorbeeldveld uit een loonstrook</h2>
  <blockquote>Contracturen: 1:00 uur per week</blockquote>
  <p><strong>Wat dit precies bevestigt:</strong> op een deel van de loonstroken staat één contractuur per week, terwijl de overeenkomst 32 uur vermeldt. Dit veld bepaalt op zichzelf niet de hoogte van een vordering, maar vereist uitleg over de loonadministratie en correctiegeschiedenis.</p>
</section>
<section class="card">
  <h2>4. Register van ontbrekende of later ontvangen loonstroken en weken</h2>
  <p>De tabel geeft de werkstatus van het documentenpakket weer. “Ontbrekend” betekent dat in het onderzochte pakket geen bevestigde volledige loonstrook aanwezig was; het betekent niet dat het document nooit heeft bestaan.</p>
  <div class="table-wrap"><table>
    <thead><tr><th>Jaar</th><th>Weken die aanvulling of bevestiging vereisen</th><th>Publieke status</th></tr></thead>
    <tbody>
      <tr><td>2022</td><td>W37, W38, W39, W48, W49</td><td>geen volledig bevestigd pakket in het werkregister</td></tr>
      <tr><td>2023</td><td>W13, W16, W31–W36, W38, W42–W46</td><td>ontbrekend of onvolledig opgenomen; vergelijking met de volledige loonadministratie vereist</td></tr>
      <tr><td>2024</td><td>W02, W23</td><td>aanvulling of eenduidige koppeling aan een document vereist</td></tr>
      <tr><td>2025</td><td>W32</td><td>later ontvangen; niet langer als niet-bestaand aangeduid, maar moet in de volledige afrekening worden verwerkt</td></tr>
    </tbody>
  </table></div>
</section>
<section class="card note">
  <h2>5. Officiële beslissing van de Raad van Discipline</h2>
  <p><strong>Datum en zaaknummer:</strong> 29 juni 2026, 25-714/DH/DH.</p>
  <blockquote>het verzet gegrond · klachtonderdelen a) en d) gegrond · maatregel van berisping</blockquote>
  <p><strong>Wat het dictum precies bevestigt:</strong> het verzet is gegrond verklaard, de eerdere voorzittersbeslissing is vernietigd, klachtonderdelen a) en d) zijn gegrond en b) en c) ongegrond verklaard, en een berisping is opgelegd. Ook is terugbetaling van EUR 50 griffierecht aan klaagster en EUR 1.250 proceskosten aan de Nederlandse Orde van Advocaten bepaald.</p>
  <p>De officiële beslissing is in bezit van de auteurs. Bij deze actualisering is geen directe openbare resultaat-URL in de officiële databank gevonden; zoeken kan op zaaknummer via <a href="https://tuchtrecht.overheid.nl/" target="_blank" rel="noopener noreferrer">Tuchtrecht</a>. Een geanonimiseerde kopie kan voor onafhankelijke verificatie worden verstrekt.</p>
</section>
<section class="card">
  <h2>Controletabel: stelling — document — datum — exacte bevestiging</h2>
  <div class="table-wrap"><table>
    <thead><tr><th>Stelling</th><th>Document</th><th>Datum</th><th>Wat dit precies bevestigt</th></tr></thead>
    <tbody>
      <tr><td>Intrixo moest het brutoloon vanaf 6 mei 2022 berekenen</td><td>proces-verbaal</td><td>12 maart 2024</td><td>de concrete verplichting en begindatum van de afrekenperiode</td></tr>
      <tr><td>De overeenkomst bepaalde 32 uur per week</td><td>Fase 4 / Fase C-overeenkomst</td><td>vanaf 21 november 2022</td><td>onbepaalde tijd, 32 uur en geen oproepovereenkomst</td></tr>
      <tr><td>Op een deel van de loonstroken staat één uur</td><td>loonstroken</td><td>tijdens de overeenkomst</td><td>de afwijking in Contracturen ten opzichte van de overeenkomst</td></tr>
      <tr><td>Het documentenpakket bevat hiaten en late stukken</td><td>loonstrookregister en correspondentie</td><td>2022–2025</td><td>weken die aanvulling, koppeling of versiecontrole vereisen</td></tr>
      <tr><td>Een deel van de tuchtklacht is gegrond verklaard</td><td>beslissing Raad van Discipline</td><td>29 juni 2026</td><td>gegrond verzet, gegronde onderdelen a) en d), en berisping</td></tr>
    </tbody>
  </table></div>
  <p class="source"><a href="../EVIDENCE_INDEX.nl.md">Bewijsindex in Markdown</a> · <a href="voor-instanties.html">Veilige toegang voor instanties</a></p>
</section>
"""

nl_nav = '<a class="btn" href="index.html">NL start</a><a class="btn" href="timeline.html">Tijdlijn</a><a class="btn" href="belangrijkste-bevindingen.html">Belangrijkste bevindingen</a><a class="btn" href="media.html">Media</a><a class="btn" href="../pl/dowody.html">PL</a><a class="btn" href="../en/dowody.html">EN</a>'

write("pl/dowody.html", page("pl", "5 najmocniejszych dowodów — zanonimizowane fragmenty dokumentów", "Zanonimizowane fragmenty proces-verbaal, umowy 32 godzin, loonstrooka, rejestru brakujących tygodni i decyzji Raad van Discipline.", "Dokumentowe fragmenty do niezależnej weryfikacji: proces-verbaal, umowa 32h, Contracturen 1:00, braki tygodni i decyzja dyscyplinarna.", pl_nav, pl_body))
write("en/dowody.html", page("en", "5 strongest evidence points — anonymised document excerpts", "Anonymised excerpts from the process-verbaal, 32-hour agreement, payslip, missing-week register and Raad van Discipline decision.", "Document excerpts for independent verification: process-verbaal, 32-hour agreement, Contracturen 1:00, missing weeks and disciplinary decision.", en_nav, en_body))
write("nl/dowody.html", page("nl", "5 sterkste bewijspunten — geanonimiseerde documentfragmenten", "Geanonimiseerde fragmenten uit het proces-verbaal, de 32-uurovereenkomst, loonstrook, ontbrekende-wekenregister en tuchtbeslissing.", "Documentfragmenten voor onafhankelijke verificatie: proces-verbaal, 32 uur, Contracturen 1:00, ontbrekende weken en tuchtbeslissing.", nl_nav, nl_body))

# Add hreflang to all corresponding PL/EN/NL pages.
groups = [
    ("pl/index.html", "en/index.html", "nl/index.html"),
    ("pl/najwazniejsze-ustalenia.html", "en/key-findings.html", "nl/belangrijkste-bevindingen.html"),
    ("pl/timeline.html", "en/timeline.html", "nl/timeline.html"),
    ("pl/dowody.html", "en/dowody.html", "nl/dowody.html"),
    ("pl/media.html", "en/media.html", "nl/media.html"),
    ("pl/dla-instytucji.html", "en/for-institutions.html", "nl/voor-instanties.html"),
    ("pl/home-of-people.html", "en/home-of-people.html", "nl/home-of-people.html"),
]
for group in groups:
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{code}" href="{BASE}{path}">'
        for code, path in zip(("pl", "en", "nl"), group)
    )
    for path in group:
        target = ROOT / path
        value = target.read_text(encoding="utf-8")
        value = re.sub(r'\s*<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+"\s*/?>', "", value, flags=re.I)
        canonical = re.search(r'(<link\s+rel="canonical"\s+href="[^"]+"\s*/?>)', value, flags=re.I)
        if not canonical:
            raise RuntimeError(f"No canonical link in {path}")
        value = value[:canonical.end()] + "\n" + alternates + value[canonical.end():]
        target.write_text(value, encoding="utf-8")

# Remove query-based document-viewer URLs from sitemap.
sitemap_path = ROOT / "sitemap.xml"
sitemap = sitemap_path.read_text(encoding="utf-8")
sitemap = "\n".join(line for line in sitemap.splitlines() if "doc.html?file=" not in line) + "\n"
sitemap_path.write_text(sitemap, encoding="utf-8")

# Mark the JS Markdown viewer noindex and give it one stable canonical URL.
doc_path = ROOT / "doc.html"
doc = doc_path.read_text(encoding="utf-8")ndoc_marker = '  <meta name="description" content="Podgląd źródeł Markdown dla publicznego briefingu sprawy Intrixo (wersja anonimizowana).">'
if ndoc_marker not in doc:
    raise RuntimeError("doc.html description marker not found")
doc = doc.replace(ndoc_marker, ndoc_marker + f'\n  <meta name="robots" content="noindex, nofollow">\n  <link rel="canonical" href="{BASE}doc.html">', 1)
doc = doc.replace('      document.title = formatDocTitle(file);', '      document.title = formatDocTitle(file);\n      document.documentElement.lang = file.endsWith(".en.md") ? "en" : (file.endsWith(".nl.md") ? "nl" : "pl");', 1)
doc_path.write_text(doc, encoding="utf-8")

# Update complete-site audit: no query URLs, doc noindex, and full hreflang groups.
audit_path = ROOT / "scripts/check_complete_site.py"
audit = audit_path.read_text(encoding="utf-8")
audit = audit.replace("from urllib.parse import parse_qs, urlparse", "from urllib.parse import urlparse")
audit = re.sub(r'\nDOC_FILES = \{.*?\nEXPECTED_DOC_URLS = \{BASE_URL \+ "doc\.html\?file=" \+ file for file in DOC_FILES\}\n', "\n", audit, flags=re.S)
audit = audit.replace("required = STATIC_PUBLIC_URLS | EXPECTED_DOC_URLS", "required = STATIC_PUBLIC_URLS")
old_query = '''        parsed = urlparse(url)\n        if parsed.query:\n            file_values = parse_qs(parsed.query).get("file", [])\n            if file_values:\n                file_path = file_values[0]\n                if not (ROOT / file_path).is_file():\n                    add(issues, "sitemap.xml", f"doc URL points to missing file: {file_path}")'''
new_query = '''        parsed = urlparse(url)\n        if parsed.query:\n            add(issues, "sitemap.xml", f"query-string URL must not be indexed: {url}")'''
if old_query not in audit:
    raise RuntimeError("Old sitemap query audit block not found")
audit = audit.replace(old_query, new_query)
audit = audit.replace('        elif path_rel != "doc.html":\n            add(issues, path_rel, "missing canonical URL")', '        else:\n            add(issues, path_rel, "missing canonical URL")')
needle = '        for tag in re.findall(r"<img\\b[^>]*>", text, flags=re.IGNORECASE):'
insert = '''        if path_rel == "doc.html" and not re.search(r'<meta\\s+name="robots"\\s+content="[^"]*noindex', text, flags=re.IGNORECASE):\n            add(issues, path_rel, "document viewer must be noindex")\n\n'''
if needle not in audit:
    raise RuntimeError("HTML audit insertion point not found")
audit = audit.replace(needle, insert + needle, 1)

hreflang_code = '''\n\nHREFLANG_GROUPS = [\n    ("pl/index.html", "en/index.html", "nl/index.html"),\n    ("pl/najwazniejsze-ustalenia.html", "en/key-findings.html", "nl/belangrijkste-bevindingen.html"),\n    ("pl/timeline.html", "en/timeline.html", "nl/timeline.html"),\n    ("pl/dowody.html", "en/dowody.html", "nl/dowody.html"),\n    ("pl/media.html", "en/media.html", "nl/media.html"),\n    ("pl/dla-instytucji.html", "en/for-institutions.html", "nl/voor-instanties.html"),\n    ("pl/home-of-people.html", "en/home-of-people.html", "nl/home-of-people.html"),\n]\n\ndef check_hreflang(issues: list[AuditIssue]) -> None:\n    for group in HREFLANG_GROUPS:\n        expected = {code: BASE_URL + path for code, path in zip(("pl", "en", "nl"), group)}\n        for path in group:\n            value = read_text(ROOT / path)\n            for code, href in expected.items():\n                pattern = rf'<link\\s+rel="alternate"\\s+hreflang="{code}"\\s+href="{re.escape(href)}"\\s*/?>'\n                if not re.search(pattern, value, flags=re.IGNORECASE):\n                    add(issues, path, f"missing hreflang {code} -> {href}")\n'''
if "HREFLANG_GROUPS = [" not in audit:
    audit = audit.replace("\ndef main() -> int:\n", hreflang_code + "\n\ndef main() -> int:\n", 1)
audit = audit.replace("    check_html_quality(issues)\n", "    check_html_quality(issues)\n    check_hreflang(issues)\n", 1)
audit_path.write_text(audit, encoding="utf-8")

# Update the language HTML/SEO audit to enforce hreflang on matching pages.
structure_path = ROOT / "scripts/check_html_structure.py"
structure = structure_path.read_text(encoding="utf-8")
structure_map = '''\nHREFLANG_GROUPS = [\n    ("pl/index.html", "en/index.html", "nl/index.html"),\n    ("pl/najwazniejsze-ustalenia.html", "en/key-findings.html", "nl/belangrijkste-bevindingen.html"),\n    ("pl/timeline.html", "en/timeline.html", "nl/timeline.html"),\n    ("pl/dowody.html", "en/dowody.html", "nl/dowody.html"),\n    ("pl/media.html", "en/media.html", "nl/media.html"),\n    ("pl/dla-instytucji.html", "en/for-institutions.html", "nl/voor-instanties.html"),\n    ("pl/home-of-people.html", "en/home-of-people.html", "nl/home-of-people.html"),\n]\nHREFLANG_LOOKUP = {path: group for group in HREFLANG_GROUPS for path in group}\n'''
if "HREFLANG_LOOKUP" not in structure:
    structure = structure.replace("\nREQUIRED_META = (", structure_map + "\nREQUIRED_META = (", 1)
anchor = '    if "href=\\\"#" in text:'
hreflang_check = '''    group = HREFLANG_LOOKUP.get(rel)\n    if group:\n        for code, target in zip(("pl", "en", "nl"), group):\n            expected = BASE_URL + target\n            pattern = rf'<link\\s+rel="alternate"\\s+hreflang="{code}"\\s+href="{re.escape(expected)}"\\s*/?>'\n            if not re.search(pattern, text, flags=re.IGNORECASE):\n                errors.append(HtmlError(path, f"missing hreflang {code} -> {expected}"))\n\n'''
if anchor not in structure:
    raise RuntimeError("Structure audit insertion point not found")
structure = structure.replace(anchor, hreflang_check + anchor, 1)
structure_path.write_text(structure, encoding="utf-8")

print("Applied evidence excerpts, evidence tables, sitemap no-query policy, doc noindex, and PL/EN/NL hreflang links.")

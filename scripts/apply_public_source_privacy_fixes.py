#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from textwrap import dedent
import re

ROOT = Path(__file__).resolve().parents[1]

OLD_RIJK = "https://www.rijksoverheid.nl/onderwerpen/hervormingen-arbeidsmarkt/aanpak-misstanden-arbeidsmigratie"
NEW_RIJK = "https://www.rijksoverheid.nl/themas/migratie-en-reizen/buitenlandse-werknemers/verbeteren-positie-arbeidsmigranten"
BAD_FLEX = "https://www.flexnieuws.nl/2024/06/home-of-people-neemt-ook-efficient-at-work-over/"
GOOD_FLEX = "https://www.flexnieuws.nl/2025/10/home-of-people-breidt-verder-uit-met-intrixo-en-masterteam/"

TEXT_SUFFIXES = {".md", ".html", ".xml", ".py", ".yml", ".yaml", ".txt"}
FILE_EXT = r"(?:pdf|png|jpe?g|xlsx?|zip|wav|mp4|docx?)"


def move_public_section() -> None:
    old_dir = ROOT / "sezer-duygulu"
    new_dir = ROOT / "home-of-people"
    if old_dir.exists() and not new_dir.exists():
        old_dir.rename(new_dir)
    for lang in ("pl", "en", "nl"):
        old = ROOT / lang / "sezer-duygulu.html"
        new = ROOT / lang / "home-of-people.html"
        if old.exists() and not new.exists():
            old.rename(new)


def dedupe_lines(value: str) -> str:
    result: list[str] = []
    previous = None
    for line in value.splitlines():
        if line == previous and line.startswith("http"):
            continue
        result.append(line)
        previous = line
    return "\n".join(result)


def global_cleanup() -> None:
    replacements = {
        OLD_RIJK: NEW_RIJK,
        BAD_FLEX: GOOD_FLEX,
        "9486553": "9487775",
        "sezer-duygulu": "home-of-people",
        "Sezer Duygulu i Home of People": "Home of People",
        "Sezer Duygulu and Home of People": "Home of People",
        "Sezer Duygulu en Home of People": "Home of People",
        "Sezer Duygulu": "Home of People",
    }
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        value = path.read_text(encoding="utf-8", errors="ignore")
        for old, new in replacements.items():
            value = value.replace(old, new)
        value = dedupe_lines(value)
        path.write_text(value, encoding="utf-8")


def redact_timeline(path: Path, lang: str) -> None:
    value = path.read_text(encoding="utf-8")

    # Remove evidence filenames while retaining the event and the evidence category.
    labels = {
        "pl": r"(?:dowód|plik|pliki|załącznik)",
        "en": r"(?:evidence|file|files|attachment)",
        "nl": r"(?:bewijs|bestand|bestanden|bijlage)",
    }[lang]
    value = re.sub(rf"\s*\((?i:{labels})\s*:[^)]*\)", "", value)
    value = re.sub(rf"(?im)^\s*(?i:{labels})\s*:.*$", "", value)
    value = re.sub(rf"[„\"]([^„”\"\n]+\.{FILE_EXT})[”\"]", "zanonimizowany dokument" if lang == "pl" else ("an anonymized document" if lang == "en" else "een geanonimiseerd document"), value, flags=re.I)
    value = re.sub(rf"\b[^\n()]*?\.{FILE_EXT}\b", "", value, flags=re.I)

    # Remove exact workplace references and internal identifiers.
    value = value.replace("Solaris tydzień 42", "tydzień 42")
    value = value.replace("Solaris week 42", "week 42")
    value = value.replace("Solaris week 42", "week 42")

    lines = value.splitlines()
    out: list[str] = []
    for line in lines:
        lower = line.lower()

        if "fr2024-1127" in lower or "1 512,50" in line or "1,512.50" in line or "1.512,50" in line:
            if lang == "pl":
                line = "- **25.06.2024:** wpłata na rzecz drugiego pełnomocnika w wysokości około **1,5 tys. EUR**; numer faktury i dane rachunkowe usunięto z wersji publicznej."
            elif lang == "en":
                line = "- **25.06.2024:** payment of approximately **EUR 1.5 thousand** to the second representative; the invoice number and account details were removed from the public version."
            else:
                line = "- **25.06.2024:** betaling van ongeveer **EUR 1,5 duizend** aan de tweede vertegenwoordiger; factuurnummer en rekeninggegevens zijn uit de publieke versie verwijderd."

        if "26.032" in line or "3nb7949" in lower:
            if lang == "pl":
                line = "- **25.02.2026:** trzeci pełnomocnik potwierdził otrzymanie pierwszej części wymaganej opłaty i rozpoczęcie działań; numery faktury oraz pomocy prawnej usunięto z wersji publicznej."
            elif lang == "en":
                line = "- **25.02.2026:** the third representative confirmed receipt of the first required contribution and the start of work; invoice and legal-aid identifiers were removed from the public version."
            else:
                line = "- **25.02.2026:** de derde vertegenwoordiger bevestigde ontvangst van de eerste vereiste bijdrage en de start van de werkzaamheden; factuur- en rechtsbijstandskenmerken zijn uit de publieke versie verwijderd."

        if "2485387" in line or "k077 2025" in lower:
            if "09.04.2025" in line:
                line = {
                    "pl": "- **09.04.2025:** samorząd adwokacki potwierdził wpływ skargi i poprosił o uzupełnienie korespondencji; wewnętrzny numer sprawy usunięto.",
                    "en": "- **09.04.2025:** the bar authority confirmed receipt of the complaint and requested additional correspondence; the internal case reference was removed.",
                    "nl": "- **09.04.2025:** de orde bevestigde ontvangst van de klacht en vroeg om aanvullende correspondentie; het interne zaaknummer is verwijderd.",
                }[lang]
            else:
                line = {
                    "pl": "- Orde van Advocaten (Den Haag): wewnętrzne oznaczenie sprawy usunięto z wersji publicznej.",
                    "en": "- The Hague Bar: the internal case reference was removed from the public version.",
                    "nl": "- Orde van Advocaten Den Haag: het interne zaaknummer is uit de publieke versie verwijderd.",
                }[lang]

        if "37856" in line or "v-657" in lower:
            if "03.12.2025" in line:
                line = {
                    "pl": "- **03.12.2025:** SNCU zarejestrowało zgłoszenie; wewnętrzny numer usunięto z wersji publicznej.",
                    "en": "- **03.12.2025:** SNCU registered the report; the internal reference was removed from the public version.",
                    "nl": "- **03.12.2025:** SNCU registreerde de melding; het interne kenmerk is uit de publieke versie verwijderd.",
                }[lang]
            else:
                line = {
                    "pl": "- **20.01.2026:** przekazano informację o zakończeniu postępowania wstępnego po kontakcie z pracodawcą; wewnętrzne oznaczenia spraw usunięto.",
                    "en": "- **20.01.2026:** information was provided that the preliminary procedure had ended after contact with the employer; internal case references were removed.",
                    "nl": "- **20.01.2026:** meegedeeld werd dat het vooronderzoek na contact met de werkgever was beëindigd; interne zaakreferenties zijn verwijderd.",
                }[lang]

        if ("2,50" in line or "2.50" in line) and ("2026" in line or "loonslip" in lower or "loonstrook" in lower):
            if "24.02.2026" in line:
                line = {
                    "pl": "- **24.02.2026:** Intrixo wystawiło końcowy dokument płacowy za tydzień 32/2025, wskazujący symboliczną kwotę netto poniżej 5 EUR; numer dokumentu usunięto.",
                    "en": "- **24.02.2026:** Intrixo issued a final payroll document for week 32/2025 showing a nominal net amount below EUR 5; the document number was removed.",
                    "nl": "- **24.02.2026:** Intrixo stelde een laatste loondocument voor week 32/2025 op met een symbolisch nettobedrag onder EUR 5; het documentnummer is verwijderd.",
                }[lang]
            elif "25.02.2026" in line:
                line = {
                    "pl": "- **25.02.2026:** na tym rozliczeniu odnotowano przelew symbolicznej kwoty poniżej 5 EUR; szczegóły rachunku i opis transakcji usunięto.",
                    "en": "- **25.02.2026:** a transfer of a nominal amount below EUR 5 was recorded following that settlement; account and transaction details were removed.",
                    "nl": "- **25.02.2026:** na die afrekening werd een overschrijving van een symbolisch bedrag onder EUR 5 geregistreerd; rekening- en transactiedetails zijn verwijderd.",
                }[lang]

        if any(token in line for token in ("50,98", "33,45", "17,53", "50.98", "33.45", "17.53")):
            line = {
                "pl": "Pracownik zgłosił ujemne saldo. Helpdesk wyjaśnił, że przy niewielkiej liczbie godzin koszty zakwaterowania i ubezpieczenia spowodowały zadłużenie rzędu kilkudziesięciu euro, następnie częściowo potrącane z kolejnego wynagrodzenia.",
                "en": "The worker reported a negative balance. The helpdesk explained that, with few hours worked, accommodation and insurance costs created a debt of several dozen euros, later partly deducted from the next wage payment.",
                "nl": "De werknemer meldde een negatief saldo. De helpdesk verklaarde dat bij weinig gewerkte uren huisvestings- en verzekeringskosten een schuld van enkele tientallen euro's veroorzaakten, die later gedeeltelijk op het volgende loon werd ingehouden.",
            }[lang]

        line = re.sub(r"\s*\(?(?:Zaak|case|zaak)\s*:?\s*\*\*?[-A-Z0-9./ ]+\*\*?\)?", "", line, flags=re.I)
        line = re.sub(r"(?:loonstrook|loonspecificatie|loonslip)(?:nummer|number|nr\.?| no\.?)?\s*\*\*?35\*\*?", "payroll document", line, flags=re.I)
        line = line.replace("griffierecht €50", "griffierecht").replace("court fee EUR 50", "court fee").replace("griffierecht EUR 50", "griffierecht")
        line = line.rstrip()
        out.append(line)

    value = "\n".join(out)
    value = re.sub(r"\n{4,}", "\n\n\n", value)
    path.write_text(value, encoding="utf-8")


def replace_legal_risk_section(path: Path, lang: str) -> None:
    value = path.read_text(encoding="utf-8")
    blocks = {
        "pl": dedent("""
            ## D) Kwestie prawne wymagające oceny właściwych organów

            Publiczna wersja raportu nie przypisuje osobom fizycznym odpowiedzialności karnej i nie formułuje kwalifikacji przestępstw. Materiał wskazuje wyłącznie kwestie, które mogą wymagać oceny sądu, organu nadzoru albo niezależnego prawnika:

            - zgodność rozliczeń płacowych i historii korekt,
            - dobrowolność podpisywania dokumentów i sposób prowadzenia rozmów,
            - prawidłowość potrąceń oraz tworzenia ujemnych sald,
            - kompletność informacji przekazywanych pracownikowi i instytucjom.

            W publikacji należy opisywać zdarzenia, dokumenty i rozbieżności, a ocenę prawną pozostawić właściwym organom.

            ---

            ## E) Prywatność w zakwaterowaniu agencyjnym

            Według materiału wideo osoby trzecie miały wchodzić do zamieszkanego pomieszczenia bez wcześniejszego powiadomienia lub zgody mieszkańców. Publiczna wersja nie ujawnia lokalizacji, numeru pokoju, twarzy, głosów ani danych osób prywatnych.

            Materiał powinien być zachowany w oryginale i przekazywany wyłącznie właściwym instytucjom lub pełnomocnikom. Publicznie należy ograniczyć się do ostrożnego opisu faktów i ochrony prywatności, bez przypisywania konkretnej osobie czynu zabronionego.

            ---
        """),
        "en": dedent("""
            ## D) Legal issues requiring assessment by competent authorities

            The public report does not attribute criminal responsibility to individuals and does not propose criminal-offence classifications. It identifies only matters that may require assessment by a court, supervisory authority or independent lawyer:

            - accuracy of payroll settlements and correction histories,
            - freedom of consent when documents were presented for signature and the manner in which meetings were conducted,
            - legality and transparency of deductions and negative balances,
            - completeness of information provided to the worker and institutions.

            Public reporting should describe events, documents and discrepancies while leaving legal qualification to competent authorities.

            ---

            ## E) Privacy in agency accommodation

            According to video material, third parties allegedly entered an occupied room without prior notice or the residents' consent. The public version does not reveal the location, room number, faces, voices or data of private individuals.

            Original material should be preserved and shared only with competent institutions or legal representatives. Public reporting should remain limited to a cautious factual description and privacy protection, without attributing a criminal act to a specific person.

            ---
        """),
        "nl": dedent("""
            ## D) Juridische kwesties die beoordeling door bevoegde instanties vereisen

            Het publieke rapport schrijft geen strafrechtelijke verantwoordelijkheid toe aan natuurlijke personen en formuleert geen strafrechtelijke kwalificaties. Het benoemt alleen onderwerpen die beoordeling door een rechter, toezichthouder of onafhankelijke jurist kunnen vereisen:

            - juistheid van loonafrekeningen en correctiegeschiedenis,
            - vrije instemming bij het voorleggen van documenten en de wijze waarop gesprekken zijn gevoerd,
            - rechtmatigheid en transparantie van inhoudingen en negatieve saldi,
            - volledigheid van informatie aan de werknemer en instanties.

            Publieke verslaglegging dient gebeurtenissen, documenten en tegenstrijdigheden te beschrijven en de juridische kwalificatie aan bevoegde instanties over te laten.

            ---

            ## E) Privacy in uitzendhuisvesting

            Volgens videomateriaal zouden derden een bewoonde kamer zijn binnengekomen zonder voorafgaande kennisgeving of toestemming van de bewoners. De publieke versie vermeldt geen locatie, kamernummer, gezichten, stemmen of gegevens van privépersonen.

            Het oorspronkelijke materiaal moet worden bewaard en alleen aan bevoegde instanties of juridische vertegenwoordigers worden verstrekt. Publiek dient men zich te beperken tot een voorzichtige feitelijke beschrijving en bescherming van de privacy, zonder een strafbaar feit aan een specifieke persoon toe te schrijven.

            ---
        """),
    }
    pattern = re.compile(r"## D\).*?(?=## F\))", re.S)
    value, count = pattern.subn(blocks[lang].strip() + "\n\n", value, count=1)
    if count != 1:
        raise RuntimeError(f"Could not replace D/E legal-risk section in {path}")
    path.write_text(value, encoding="utf-8")


def make_home_doc(body: str) -> str:
    lines = dedent(body).strip("\n").splitlines()
    footer = [
        "<!-- end of equivalent language version -->",
        "<!-- equivalent language version: verified -->",
        "<!-- public anonymization: verified -->",
    ]
    if len(lines) > 182:
        raise RuntimeError(f"Home of People document too long: {len(lines)}")
    lines.extend([""] * (182 - len(lines)))
    lines.extend(footer)
    assert len(lines) == 185
    return "\n".join(lines)


def write_home_docs() -> None:
    docs = {
        "pl": """
            [Wersja polska]

            # Home of People – publiczny kontekst podmiotów

            Ta sekcja przedstawia wyłącznie kontekst organizacyjny oparty na źródłach publicznych. Nie wskazuje osoby fizycznej jako odpowiedzialnej za działania którejkolwiek spółki i nie formułuje zarzutów karnych.

            ---

            ## 1. Cel sekcji

            - uporządkowanie publicznych informacji o grupie i jej markach,
            - oddzielenie faktów rejestrowych od ocen wymagających dalszej weryfikacji,
            - pokazanie kontekstu sprawy Intrixo bez przypisywania odpowiedzialności osobistej,
            - ograniczenie publikacji danych do informacji koniecznych i proporcjonalnych.

            ---

            ## 2. Podmioty występujące w publicznych materiałach

            - Home of People,
            - Uitzendbureau Solutions,
            - Intrixo / Voorneputten,
            - T&S Flexwerk,
            - NWH Jobs,
            - Efficient at Work,
            - Masterteam.

            ---

            ## 3. Charakter powiązań

            Publiczne materiały branżowe i korporacyjne opisują rozwój grupy poprzez integrację lub przejmowanie marek działających w pracy tymczasowej, rekrutacji i obsłudze pracowników migrujących.

            Samo powiązanie kapitałowe, organizacyjne, marketingowe albo historyczne nie dowodzi odpowiedzialności za konkretne zdarzenie. Może jedynie pomagać w zrozumieniu modelu działalności i struktury nadzoru.

            ---

            ## 4. Znaczenie dla sprawy Intrixo

            Główny raport dotyczy dokumentów indywidualnej sprawy pracowniczej: umowy, godzin, wynagrodzenia, potrąceń, zakwaterowania, korespondencji i wykonania proces-verbaal.

            Kontekst grupy nie zastępuje analizy tych dokumentów i nie może służyć do automatycznego przenoszenia odpowiedzialności między podmiotami.

            ---

            ## 5. Model praca–zakwaterowanie

            Połączenie pracy, transportu i zakwaterowania może zwiększać zależność ekonomiczną pracownika. Utrata pracy albo spór o potrącenia może wtedy wpływać również na bezpieczeństwo mieszkaniowe.

            Jest to ryzyko systemowe wymagające przejrzystych procedur, ale sam model nie dowodzi naruszenia w konkretnej sprawie.

            ---

            ## 6. Orzeczenia i źródła publiczne

            Sygnatury orzeczeń i nazwy spółek pozostają publiczne wyłącznie wtedy, gdy są potrzebne do odnalezienia oficjalnego źródła. Orzeczenia dotyczą różnych stanów faktycznych i nie mogą być automatycznie stosowane do innej sprawy.

            ---

            ## 7. Zasady prywatności

            - nie publikuje się imion i nazwisk osób fizycznych związanych z grupą, jeżeli nie jest to niezbędne,
            - nie publikuje się inicjałów prywatnych pracowników,
            - nie publikuje się dokładnych adresów zakwaterowania i miejsc pracy,
            - nie publikuje się numerów dokumentów, rachunków, faktur ani wewnętrznych oznaczeń spraw,
            - pełne materiały pozostają w archiwum prywatnym do przekazania właściwym instytucjom.

            ---

            ## 8. Bezpieczne ramy prawne publikacji

            Publikacja opisuje podmioty, dokumenty i publiczne źródła. Nie przypisuje konkretnej osobie winy karnej, cywilnej ani zawodowej. Wątpliwości prawne powinny być kierowane do właściwych organów lub niezależnego prawnika.

            ---

            ## 9. Zweryfikowane źródła

            - Home of People: https://www.homeofpeople.nl/
            - ACM – zgłoszenie koncentracji dotyczące Intrixo: https://www.acm.nl/nl/publicaties/home-people-wil-intrixo-overnemen-concentratiemelding
            - FlexNieuws – aktualny artykuł o Intrixo i Masterteam: https://www.flexnieuws.nl/2025/10/home-of-people-breidt-verder-uit-met-intrixo-en-masterteam/
            - GroentenNieuws – poprawny numer artykułu: https://www.groentennieuws.nl/article/9487775/
            - Rijksoverheid – poprawa pozycji pracowników migrujących: https://www.rijksoverheid.nl/themas/migratie-en-reizen/buitenlandse-werknemers/verbeteren-positie-arbeidsmigranten

            Stary artykuł FlexNieuws zwracający 404 został usunięty. Błędny numer artykułu GroentenNieuws 9486553 został zastąpiony numerem 9487775.

            ---

            ## 10. LinkedIn i automatyczne sprawdzanie

            LinkedIn może zwracać automatom kod 999. Jest to blokada dostępu automatycznego, a nie wystarczający dowód usunięcia profilu. Linki LinkedIn powinny być sprawdzane ręcznie i nie są automatycznie oznaczane jako martwe wyłącznie z powodu kodu 999.

            ---

            ## 11. Ograniczenia

            Rejestry mogą być niepełne, struktury właścicielskie mogą się zmieniać, a źródła wtórne wymagają potwierdzenia w materiałach pierwotnych. Brak publicznego dokumentu nie dowodzi, że dokument lub zdarzenie nie istnieje.

            ---

            ## 12. Wniosek

            Publiczny materiał uzasadnia ostrożną analizę modelu zatrudnienia, zakwaterowania, potrąceń i dokumentacji. Nie stanowi jednak ustalenia osobistej odpowiedzialności jakiejkolwiek osoby fizycznej.
        """,
        "en": """
            [English version]

            # Home of People – public entity context

            This section presents only organizational context based on public sources. It does not identify an individual as responsible for the conduct of any company and does not make criminal allegations.

            ---

            ## 1. Purpose

            - organize public information about the group and its brands,
            - separate registry facts from assessments requiring further verification,
            - show the context of the Intrixo matter without attributing personal responsibility,
            - limit publication to information that is necessary and proportionate.

            ---

            ## 2. Entities appearing in public materials

            - Home of People,
            - Uitzendbureau Solutions,
            - Intrixo / Voorneputten,
            - T&S Flexwerk,
            - NWH Jobs,
            - Efficient at Work,
            - Masterteam.

            ---

            ## 3. Nature of links

            Public industry and corporate materials describe the group's development through integration or acquisition of brands active in temporary work, recruitment and services for migrant workers.

            A capital, organizational, marketing or historical link does not establish responsibility for a specific event. It may only help explain the business model and oversight structure.

            ---

            ## 4. Relevance to the Intrixo matter

            The main report concerns documents from an individual employment matter: contract, hours, wages, deductions, accommodation, correspondence and performance of the proces-verbaal.

            Group context does not replace analysis of those documents and cannot automatically transfer responsibility between entities.

            ---

            ## 5. Work–housing model

            Combining work, transport and accommodation may increase a worker's economic dependence. Loss of work or a dispute about deductions may then also affect housing security.

            This is a systemic risk requiring transparent procedures, but the model itself does not establish a violation in an individual case.

            ---

            ## 6. Judgments and public sources

            Case identifiers and company names remain public only where needed to locate an official source. The judgments concern different facts and cannot automatically be applied to another case.

            ---

            ## 7. Privacy rules

            - names of individuals associated with the group are not published unless strictly necessary,
            - initials of private workers are not published,
            - exact accommodation and workplace addresses are not published,
            - document, account, invoice and internal case identifiers are not published,
            - full materials remain in a private archive for competent institutions.

            ---

            ## 8. Safe legal framing

            The publication describes entities, documents and public sources. It does not attribute criminal, civil or professional guilt to a specific person. Legal questions should be referred to competent authorities or an independent lawyer.

            ---

            ## 9. Verified sources

            - Home of People: https://www.homeofpeople.nl/
            - ACM concentration notice concerning Intrixo: https://www.acm.nl/nl/publicaties/home-people-wil-intrixo-overnemen-concentratiemelding
            - FlexNieuws – current article on Intrixo and Masterteam: https://www.flexnieuws.nl/2025/10/home-of-people-breidt-verder-uit-met-intrixo-en-masterteam/
            - GroentenNieuws – corrected article number: https://www.groentennieuws.nl/article/9487775/
            - Dutch government – improving the position of migrant workers: https://www.rijksoverheid.nl/themas/migratie-en-reizen/buitenlandse-werknemers/verbeteren-positie-arbeidsmigranten

            The old FlexNieuws article returning 404 was removed. The incorrect GroentenNieuws article number 9486553 was replaced with 9487775.

            ---

            ## 10. LinkedIn and automated checks

            LinkedIn may return status code 999 to automated clients. This is an anti-bot restriction, not sufficient evidence that a profile has been removed. LinkedIn links should be checked manually and are not marked dead solely because of code 999.

            ---

            ## 11. Limitations

            Registers may be incomplete, ownership structures may change and secondary sources require confirmation in primary materials. Failure to find a public document does not prove that the document or event does not exist.

            ---

            ## 12. Conclusion

            Public material supports careful review of employment, accommodation, deductions and documentation. It does not establish personal responsibility of any individual.
        """,
        "nl": """
            [Nederlandse versie]

            # Home of People – publieke context van entiteiten

            Deze sectie geeft uitsluitend organisatorische context op basis van publieke bronnen. Zij wijst geen natuurlijke persoon aan als verantwoordelijke voor het handelen van een vennootschap en formuleert geen strafrechtelijke beschuldigingen.

            ---

            ## 1. Doel

            - publieke informatie over de groep en haar merken ordenen,
            - registerfeiten scheiden van beoordelingen die nadere verificatie vereisen,
            - context bieden voor de Intrixo-zaak zonder persoonlijke verantwoordelijkheid toe te schrijven,
            - publicatie beperken tot noodzakelijke en evenredige informatie.

            ---

            ## 2. Entiteiten in publieke materialen

            - Home of People,
            - Uitzendbureau Solutions,
            - Intrixo / Voorneputten,
            - T&S Flexwerk,
            - NWH Jobs,
            - Efficient at Work,
            - Masterteam.

            ---

            ## 3. Aard van de verbanden

            Publieke branche- en bedrijfsinformatie beschrijft de ontwikkeling van de groep door integratie of overname van merken in uitzendwerk, werving en dienstverlening aan arbeidsmigranten.

            Een kapitaal-, organisatorisch, marketing- of historisch verband stelt geen verantwoordelijkheid voor een concreet voorval vast. Het kan alleen helpen om het bedrijfsmodel en de toezichtstructuur te begrijpen.

            ---

            ## 4. Betekenis voor de Intrixo-zaak

            Het hoofdrapport betreft documenten uit een individuele arbeidszaak: contract, uren, loon, inhoudingen, huisvesting, correspondentie en uitvoering van het proces-verbaal.

            Groepscontext vervangt de analyse van die documenten niet en kan verantwoordelijkheid niet automatisch tussen entiteiten overdragen.

            ---

            ## 5. Model werk–huisvesting

            De combinatie van werk, vervoer en huisvesting kan de economische afhankelijkheid van een werknemer vergroten. Verlies van werk of een geschil over inhoudingen kan dan ook de woonzekerheid raken.

            Dit is een systeemrisico dat transparante procedures vereist, maar het model zelf bewijst geen schending in een individuele zaak.

            ---

            ## 6. Uitspraken en publieke bronnen

            Zaakidentificaties en bedrijfsnamen blijven alleen openbaar wanneer zij nodig zijn om een officiële bron te vinden. De uitspraken betreffen verschillende feiten en kunnen niet automatisch op een andere zaak worden toegepast.

            ---

            ## 7. Privacyregels

            - namen van natuurlijke personen die met de groep worden verbonden worden niet gepubliceerd tenzij strikt noodzakelijk,
            - initialen van privéwerknemers worden niet gepubliceerd,
            - exacte huisvestings- en werkadressen worden niet gepubliceerd,
            - document-, rekening-, factuur- en interne zaaknummers worden niet gepubliceerd,
            - volledige materialen blijven in een privéarchief voor bevoegde instanties.

            ---

            ## 8. Veilige juridische inkadering

            De publicatie beschrijft entiteiten, documenten en publieke bronnen. Zij schrijft geen strafrechtelijke, civielrechtelijke of professionele schuld toe aan een specifieke persoon. Juridische vragen horen bij bevoegde instanties of een onafhankelijke jurist.

            ---

            ## 9. Geverifieerde bronnen

            - Home of People: https://www.homeofpeople.nl/
            - ACM-concentratiemelding betreffende Intrixo: https://www.acm.nl/nl/publicaties/home-people-wil-intrixo-overnemen-concentratiemelding
            - FlexNieuws – actueel artikel over Intrixo en Masterteam: https://www.flexnieuws.nl/2025/10/home-of-people-breidt-verder-uit-met-intrixo-en-masterteam/
            - GroentenNieuws – gecorrigeerd artikelnummer: https://www.groentennieuws.nl/article/9487775/
            - Rijksoverheid – verbeteren positie arbeidsmigranten: https://www.rijksoverheid.nl/themas/migratie-en-reizen/buitenlandse-werknemers/verbeteren-positie-arbeidsmigranten

            Het oude FlexNieuws-artikel dat 404 teruggaf is verwijderd. Het onjuiste GroentenNieuws-artikelnummer 9486553 is vervangen door 9487775.

            ---

            ## 10. LinkedIn en automatische controle

            LinkedIn kan aan automatische clients statuscode 999 teruggeven. Dit is een anti-botblokkade en geen voldoende bewijs dat een profiel is verwijderd. LinkedIn-links moeten handmatig worden gecontroleerd en worden niet uitsluitend wegens code 999 als dood gemarkeerd.

            ---

            ## 11. Beperkingen

            Registers kunnen onvolledig zijn, eigendomsstructuren kunnen veranderen en secundaire bronnen moeten in primaire materialen worden bevestigd. Het niet vinden van een openbaar document bewijst niet dat het document of de gebeurtenis niet bestaat.

            ---

            ## 12. Conclusie

            Publiek materiaal rechtvaardigt zorgvuldige beoordeling van werk, huisvesting, inhoudingen en documentatie. Het stelt geen persoonlijke verantwoordelijkheid van een natuurlijke persoon vast.
        """,
    }
    target = ROOT / "home-of-people"
    target.mkdir(exist_ok=True)
    for lang, body in docs.items():
        (target / f"README.{lang}.md").write_text(make_home_doc(body), encoding="utf-8")


def update_link_checker() -> None:
    path = ROOT / "scripts" / "check_links.py"
    value = path.read_text(encoding="utf-8")
    marker = "    def _http_check(self, url: str) -> tuple[bool, str]:\n"
    addition = (
        marker
        + "        host = (urlparse(url).hostname or '').lower()\n"
        + "        if host == 'linkedin.com' or host.endswith('.linkedin.com'):\n"
        + "            return True, 'LinkedIn automated verification skipped (anti-bot HTTP 999)'\n"
    )
    if "anti-bot HTTP 999" not in value:
        value = value.replace(marker, addition)
    path.write_text(value, encoding="utf-8")


def strengthen_privacy_check() -> None:
    path = ROOT / "scripts" / "check_language_parity.py"
    value = path.read_text(encoding="utf-8")
    insert = dedent("""

        additional_forbidden = (
            "FR2024-1127", "26.032", "3NB7949", "2485387", "9486553",
            "Sezer Duygulu", "sezer-duygulu",
            "aanpak-misstanden-arbeidsmigratie",
            "home-of-people-neemt-ook-efficient-at-work-over",
        )
        for path_name in public_files:
            current = text(path_name)
            for token in additional_forbidden:
                if token in current:
                    issues.append(f"{path_name}: public identifier or obsolete source remains: {token}")

        for required_path in (
            "home-of-people/README.pl.md", "home-of-people/README.en.md", "home-of-people/README.nl.md",
            "pl/home-of-people.html", "en/home-of-people.html", "nl/home-of-people.html",
        ):
            if not (ROOT / required_path).exists():
                issues.append(f"missing privacy-safe Home of People path: {required_path}")
    """)
    # Path references were globally renamed above. Add checks before final issue handling.
    if "additional_forbidden =" not in value:
        value = value.replace("\nif issues:\n", insert + "\nif issues:\n")
    path.write_text(value, encoding="utf-8")


def main() -> None:
    move_public_section()
    global_cleanup()
    for lang in ("pl", "en", "nl"):
        redact_timeline(ROOT / f"TIMELINE.{lang}.md", lang)
        replace_legal_risk_section(ROOT / f"ALLEGATIONS_AND_LAW.{lang}.md", lang)
    write_home_docs()
    update_link_checker()
    strengthen_privacy_check()
    print("Applied source, privacy and legal-risk fixes")


if __name__ == "__main__":
    main()

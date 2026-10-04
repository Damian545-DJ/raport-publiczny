const reportNavigationText = {
  "pl": {
    "brand": "Raport publiczny",
    "nav": "Główna nawigacja",
    "mobile": "Menu mobilne",
    "languages": "Wersje językowe",
    "items": [
      "Start",
      "Ustalenia",
      "Dowody",
      "Oś czasu",
      "Instytucje",
      "Media",
      "Pełny raport",
      "Tło instytucjonalne"
    ],
    "archive": "Archiwum źródeł",
    "privacy": "Zasady anonimizacji",
    "updates": "Historia aktualizacji"
  },
  "en": {
    "brand": "Public report",
    "nav": "Main navigation",
    "mobile": "Mobile menu",
    "languages": "Language versions",
    "items": [
      "Home",
      "Findings",
      "Evidence",
      "Timeline",
      "Institutions",
      "Media",
      "Full report",
      "Institutional context"
    ],
    "archive": "Source archive",
    "privacy": "Anonymization policy",
    "updates": "Update history"
  },
  "nl": {
    "brand": "Publiek rapport",
    "nav": "Hoofdnavigatie",
    "mobile": "Mobiel menu",
    "languages": "Taalversies",
    "items": [
      "Start",
      "Bevindingen",
      "Bewijs",
      "Tijdlijn",
      "Instanties",
      "Media",
      "Volledig rapport",
      "Institutionele context"
    ],
    "archive": "Bronnenarchief",
    "privacy": "Anonimiseringsbeleid",
    "updates": "Wijzigingenoverzicht"
  }
};
const reportNavigationGroups = [["index.html", "index.html", "index.html"], ["najwazniejsze-ustalenia.html", "key-findings.html", "belangrijkste-bevindingen.html"], ["dowody.html", "dowody.html", "dowody.html"], ["timeline.html", "timeline.html", "timeline.html"], ["dla-instytucji.html", "for-institutions.html", "voor-instanties.html"], ["media.html", "media.html", "media.html"], ["full-report.html", "full-report.html", "full-report.html"], ["home-of-people.html", "home-of-people.html", "home-of-people.html"]];
function updateReportNavigation(lang, file) {
  const codes = ['pl','en','nl'];
  const index = codes.indexOf(lang);
  const text = reportNavigationText[lang];
  const header = document.querySelector('.site-header');
  header.querySelector('.brand').textContent = text.brand;
  header.querySelector('.brand').href = `${lang}/index.html`;
  header.querySelector('.chrome-nav').setAttribute('aria-label', text.nav);
  header.querySelector('.mobile-menu nav').setAttribute('aria-label', text.mobile);
  header.querySelector('.lang-switch').setAttribute('aria-label', text.languages);
  document.querySelectorAll('[data-section]').forEach(a => {
    const section = Number(a.dataset.section);
    a.href = `${lang}/${reportNavigationGroups[section][index]}`;
    a.textContent = text.items[section];
  });
  const reports = ['PUBLICZNY_RAPORT_DOWODOWY_ANON_PL.md','PUBLIC_REPORT_EVIDENCE_ANON_EN.md','PUBLIEK_BEWIJS_RAPPORT_ANON_NL.md'];
  const families = ['README','TIMELINE','EVIDENCE_INDEX','ANONYMIZATION','DISCLAIMER','ALLEGATIONS_AND_LAW','CONTRIBUTING'];
  const family = families.find(name => file === `${name}.${lang}.md`);
  const hash = /^#worker-[12]-(?:timeline|index)$/.test(location.hash) ? location.hash : '';
  header.querySelectorAll('[data-language]').forEach(a => {
    const code = a.dataset.language;
    const target = reports.includes(file) ? reports[codes.indexOf(code)] : family ? `${family}.${code}.md` : null;
    a.href = target ? `doc.html?file=${encodeURIComponent(target)}${hash}` : `${code}/index.html`;
    if (code === lang) a.setAttribute('aria-current','page');
    else a.removeAttribute('aria-current');
  });
  const footer = document.getElementById('legalFooter');
  footer.querySelector('[data-privacy]').href = `doc.html?file=ANONYMIZATION.${lang}.md`;
  footer.querySelector('[data-privacy]').textContent = text.privacy;
  footer.querySelector('a[href="archive.html"]').textContent = text.archive;
  footer.querySelector('a[href="doc.html?file=UPDATES.md"]').textContent = text.updates;
}

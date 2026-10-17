# kizapro — afterBefore Promo Verifikacija i Analiza

Nezavisni javni repozitorijum za tehničku verifikaciju, analizu i reviziju koda stranice:  
🌐 **Live URL:** [https://afterbefore-promo.netlify.app/sr.html](https://afterbefore-promo.netlify.app/sr.html)

---

## 📋 Sadržaj Repozitorijuma

- [`ANALIZA_PROVERA_DOKAZI.md`](./ANALIZA_PROVERA_DOKAZI.md) — Glavni, detaljni izveštaj analize sa svim tehničkim nalazima, dokazima i preporukama.
- [`.agents/skills/website-verification/SKILL.md`](./.agents/skills/website-verification/SKILL.md) — Antigravity Skill za automatizovanu verifikaciju sajtova.
- [`scripts/verify_site.py`](./scripts/verify_site.py) — Skripta za testiranje linkova, HTML/CSS sintakse, SEO metapodataka i responzivnosti.
- [`verification_results.json`](./verification_results.json) — Automatizovani JSON log rezultata provere.
- [`sr.html`](./sr.html), [`styles.css`](./styles.css), [`app.js`](./app.js), [`assets/`](./assets/) — Kompletna lokalna kopija ispitivane stranice sa resursima.
- [`screenshot_desktop.png`](./screenshot_desktop.png) i [`screenshot_mobile.png`](./screenshot_mobile.png) — Vizuelni dokazi renderovanja na desktop i mobilnim rezolucijama.

---

## 🚀 Pokretanje Verifikacije

Da biste ponovili testiranje nad stranicom:

```bash
# Pokretanje automatske verifikacije
python3 scripts/verify_site.py sr.html

# Pokretanje lokalnog servera za pregled
python3 -m http.server 8080
# Otvorite http://localhost:8080/sr.html
```

---

## 🔍 Sažetak Ključnih Nalaza

1. **Status Linkova:** 100% ispravnost (svih 11 eksternih HTTPS linkova, Instagram objave partnera i svi interni anchor linkovi vraćaju HTTP 200).
2. **SEO i Social:** Canonical URL, OpenGraph poster i hreflang alternates (`sr` / `en`) su kompletno i ispravno konfigurisani.
3. **Pronađen Propust:** U `sr.html` meta tag za viewport nema `viewport-fit=cover`, što uzrokuje bele margine na iPhone uređajima (u engleskoj verziji je to prethodno korigovano). Detalji i rešenje su u izveštaju [`ANALIZA_PROVERA_DOKAZI.md`](./ANALIZA_PROVERA_DOKAZI.md).

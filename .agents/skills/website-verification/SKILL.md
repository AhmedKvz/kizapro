---
name: website-verification
description: Kompletna procedura i automatizovani alati za proveru, analizu i verifikaciju web sajtova (HTML/CSS validacija, responzivnost, linkovi, SEO/OpenGraph, performanse i pristupačnost).
---

# Skill: Verifikacija i Analiza Sajta (Website Verification)

Ovaj skill pruža standardizovanu metodologiju i automatizovane alate za dubinsku proveru, reviziju i verifikaciju web sajtova i odredišnih stranica (landing pages).

## Oblasti Provere (Verification Dimensions)

1. **Strukturalna i Sintaksna Validacija (HTML5 / DOM)**
   - W3C HTML5 usklađenost, zatvoreni tagovi, hijerarhija naslova (H1 -> H6).
   - Validnost `doctype`, `lang` atributa, `meta charset`.
   - ARIA atributi, pristupačnost (a11y), `role`, `aria-label`, `aria-hidden`.

2. **Responzivnost i CSS Arhitektura (Mobile / Desktop)**
   - Provera `viewport` meta taga i `viewport-fit=cover` za mobilne safe-area.
   - Ponašanje na standardnim breakpoint-ima (320px, 375px, 414px, 768px, 1024px, 1440px).
   - Odsustvo horizontalnog overflow-a (`overflow-x: hidden`).
   - Fontovi, kontrast boja, čitljivost teksta.

3. **Integritet Linkova i Navigacije (Link Integrity)**
   - Svi eksterni linkovi (`https://...`): HTTP status 200, ispravnost protokola.
   - Svi interni anchor linkovi (`#top`, `#pilot`, `#journey`, `#economy`, `#vision`): postojanje ciljnih elemenata sa odgovarajućim `id`.
   - Target attributi (`target="_blank"`) sa `rel="noopener"` ili `rel="noreferrer"` radi bezbednosti.

4. **SEO, OpenGraph i Društvene Mreže (Metadata & Social Sharing)**
   - Naslov (`<title>`) i meta opis (`<meta name="description">`).
   - Canonical URL (`<link rel="canonical">`) i višejezični hreflang tagovi (`<link rel="alternate" hreflang="...">`).
   - OpenGraph tagovi (`og:title`, `og:description`, `og:image`, `og:url`, `og:type`).
   - Twitter Card konfiguracija (`twitter:card`).
   - Favicon i Apple Touch Icon prisustvo i veličina.

5. **Interaktivnost i Skripte (JavaScript & Dynamic UI)**
   - Ponašanje tabova (tablist, role=tab, role=tabpanel).
   - Video plejer i kontrole (preview, modal, full screen, poster slika).
   - Eksterni embedovi (npr. Instagram blockquote embedovi).
   - Rukovanje greškama u konzoli (console.error, unhandled promise rejections).

6. **PWA i Distribucija (PWA / Web App Capabilities)**
   - Prečice za instalaciju aplikacije (Safari "Add to Home Screen", Android Chrome PWA).
   - Servisni fajlovi, offline ponašanje, keširanje.

7. **Jezička i Sadržajna Tačnost (Content Copy & Tone)**
   - Tačnost informacija o događajima (datumi, lokacije, satnice, partneri).
   - Doslednost terminologije (npr. TU SAM, IDEM, NightHub, Quests, Passport).

## Automatizovano Pokretanje

U repozitorijumu se nalazi skripta `scripts/verify_site.py` koja automatski vrši sve gorenavedene tehničke provere nad zadatim HTML/CSS/JS fajlovima i online endpoint-ima:

```bash
python3 scripts/verify_site.py --file sr.html --url https://afterbefore-promo.netlify.app/sr.html
```

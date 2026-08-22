# Tree India Foundation — Website

Multilingual (English / हिंदी / मराठी), SEO-ready static site for
**treeindiafoundation.org**. Positioning: **Education and Ecology**.

Each language is a separate, crawlable page so search engines can index all three:

| Language | URL                                  | File              |
|----------|--------------------------------------|-------------------|
| English  | https://treeindiafoundation.org/     | `index.html`      |
| हिंदी     | https://treeindiafoundation.org/hi/  | `hi/index.html`   |
| मराठी     | https://treeindiafoundation.org/mr/  | `mr/index.html`   |

---

## 1. Project structure

```
tif-website/
├── index.html            EN page  (generated — do not hand-edit)
├── hi/index.html         HI page  (generated — do not hand-edit)
├── mr/index.html         MR page  (generated — do not hand-edit)
├── content/
│   ├── en.json           ← EDIT TEXT HERE (English)
│   ├── hi.json           ← EDIT TEXT HERE (Hindi)
│   └── mr.json           ← EDIT TEXT HERE (Marathi)
├── build.py              regenerates the 3 pages from content/*.json
├── _map.svg              interactive Maharashtra map (used by build.py)
├── css/styles.css        all styling
├── js/
│   ├── config.js         ← paste the Google Apps Script URL here to switch forms on
│   ├── forms.js          form submit + validation
│   └── main.js           nav, reveal, map popups, modals, language switch
├── assets/               logo, favicon, Open Graph image
├── google-apps-script/   Code.gs + SETUP.md for the forms backend (Google Sheets)
├── robots.txt            references the sitemap
├── sitemap.xml           /, /hi/, /mr/ with hreflang
└── CNAME                 treeindiafoundation.org
```

> **The three `index.html` files are generated.** Never edit them by hand — your
> changes will be overwritten on the next build. Edit `content/*.json` and rebuild.

---

## 2. Editing the text (all three languages)

1. Open the language file you want to change: `content/en.json`, `content/hi.json`
   or `content/mr.json`. The keys are the same in every file, so the same field
   is easy to find across languages.
2. Change the text values only (keep the keys and the JSON structure).
3. Rebuild the pages:

   ```bash
   python3 build.py
   ```

   This rewrites `index.html`, `hi/index.html` and `mr/index.html`.
4. Preview locally (so the `/css`, `/js`, `/assets` paths resolve):

   ```bash
   python3 -m http.server 8000
   # then open http://localhost:8000/  ,  /hi/  ,  /mr/
   ```
5. Commit and push (see deploy section).

> GitHub Pages does not run Python, so **`build.py` must be run on your computer
> before you push.** You commit the generated HTML.

**Writing rule:** do not use em dashes ( — ) anywhere. Use commas, colons or periods.

---

## 3. Turning the forms on (Contact, Volunteer, Partner, Donate)

The four forms are built and validated but not yet connected. Until connected they
show: *"Form not connected yet. Please email treeindiafoundation1@gmail.com."*

To activate them:
1. Follow `google-apps-script/SETUP.md` to deploy `Code.gs` as a **Web App**
   (this creates a Google Sheet, emails an alert to treeindiafoundation1@gmail.com,
   and auto-replies to the submitter).
2. Copy the Web App URL and paste it into `js/config.js`:

   ```js
   window.TIF_CONFIG = { GAS_URL: "https://script.google.com/macros/s/XXXX/exec" };
   ```
3. Commit and push. No rebuild needed (config.js is shared by all pages).

Donations are currently **pledge-only** (they record intent to the sheet).
For live payments, integrate Razorpay / PayU / CCAvenue on the donate form later.

---

## 4. Deploying on GitHub Pages (custom domain)

1. Create a repo (e.g. `tree-india-foundation/website`) and push **the contents of
   this folder** to the `main` branch (including `index.html`, `hi/`, `mr/`,
   `CNAME`, `robots.txt`, `sitemap.xml`, `assets/`, `css/`, `js/`).
2. Repo **Settings → Pages**: Source = *Deploy from a branch*, Branch = `main`,
   Folder = `/ (root)`. Save.
3. **Custom domain**: it will read the `CNAME` file (`treeindiafoundation.org`).
   Tick **Enforce HTTPS** once the certificate is issued.
4. **DNS at GoDaddy** — point the domain at GitHub Pages:

   | Type  | Host | Value            |
   |-------|------|------------------|
   | A     | @    | 185.199.108.153  |
   | A     | @    | 185.199.109.153  |
   | A     | @    | 185.199.110.153  |
   | A     | @    | 185.199.111.153  |
   | CNAME | www  | `<your-user>.github.io` |

   DNS can take up to a few hours to propagate.
5. `/hi/` and `/mr/` work automatically because they are real folders with their
   own `index.html`. No extra routing config is needed.

To update the live site later: edit `content/*.json` → `python3 build.py` →
commit → push. GitHub Pages redeploys automatically.

---

## 5. Google Search Console (after the site is live on HTTPS)

1. Go to Google Search Console and add a property for **treeindiafoundation.org**
   (Domain property, verified with a DNS TXT record at GoDaddy, is recommended;
   URL-prefix with an HTML tag also works).
2. **Sitemaps →** submit: `sitemap.xml`
   (full URL: `https://treeindiafoundation.org/sitemap.xml`).
3. **URL Inspection →** test and *Request indexing* for each of:
   `https://treeindiafoundation.org/`, `/hi/`, `/mr/`.
4. Over the following days, review **Page indexing**, **HTTPS**, **Core Web Vitals**
   and **Enhancements** for any errors and fix as needed.

> Being technically indexable does **not** guarantee ranking or immediate indexing.
> Ranking also depends on content quality, links, authority and competition.

---

## 6. SEO features already built in

- Separate indexable URL per language with content rendered directly in the HTML.
- Unique `<title>` and meta description per language.
- One clear `<h1>` per page and a logical H2/H3 order.
- `rel="canonical"` per page and `hreflang` for en / hi / mr / x-default.
- Open Graph + Twitter tags with a branded share image (`assets/TIF_og.jpg`).
- JSON-LD structured data: NGO/Organization + WebSite + WebPage + ContactPoint,
  using only verified details (name, URL, logo, email, phone, Pune address).
- `robots.txt` (allows all, references the sitemap) and a valid `sitemap.xml`.
- Descriptive image `alt` text and semantic, keyboard-accessible markup.

---

## 7. Notes / open items

- **Address PIN:** the brief said "Pune - 48"; the full address is written as
  `... Katraj-Kondhwa Road, Pune - 411048` (48 read as the 411048 PIN).
  Change it in `content/*.json` if that is not correct.
- **Hindi / Marathi** are professional drafts; a quick native review before wide
  promotion is recommended (Marathi especially, as your native language).
- **Logo:** the tagline in the artwork now reads *Transforming Roots through
  Education & Ecology*. Original is backed up at
  `TIF_Logo_Transparent_ORIG_backup.png` (in the outputs folder, not the site).
- **Forms** go live only after the Apps Script URL is pasted into `js/config.js`.

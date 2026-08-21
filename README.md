# Tree India Foundation — website

Static, multilingual (English / मराठी / हिंदी) website for Tree India Foundation.
No build step, no framework. Just HTML, CSS, and vanilla JavaScript, so it runs on
GitHub Pages, any Apache/NGINX server, or an EC2 instance without changes.

## Folder structure
```
tif-website/
├── index.html            The whole page (structure only; text comes from lang/)
├── CNAME                 Custom domain for GitHub Pages (treeindiafoundation.org)
├── css/
│   └── styles.css        All styling. Colours + fonts are the :root variables at the top.
├── js/
│   ├── config.js         >>> Paste your Google Apps Script URL here <<<
│   ├── i18n.js           Language loading + switching
│   ├── forms.js          Sends form submissions to Google Sheets
│   └── main.js           Nav, map popups, modals, scroll effects
├── lang/
│   ├── en.json           English text  (source of truth)
│   ├── mr.json           Marathi text
│   └── hi.json           Hindi text
├── assets/               Logo + favicon (enhanced PNGs)
└── google-apps-script/
    ├── Code.gs           Backend that saves forms to your Sheet + emails
    └── SETUP.md          10-minute setup guide for the Sheet + Web App
```

## Editing content

- **Change any wording:** edit the matching key in `lang/en.json` (and `lang/mr.json`,
  `lang/hi.json` for the other languages). Each on-page text has a `data-i18n="key"`
  in `index.html`; the JSON files hold the actual words. Keep the same keys in all three
  files.
- **Change colours or fonts:** edit the `:root { --forest: ... }` variables at the top of
  `css/styles.css`. Everything on the site references those tokens.
- **Change the logo:** replace the files in `assets/` (keep the same filenames), or update
  the `src=` paths in `index.html`.
- **Fill in the blanks:** the Contact section has placeholders for your office address and
  phone number. Edit `con.officeVal` and `con.phoneVal` in the three `lang/*.json` files.

## Connect the forms (Contact, Volunteer, Partner, Donate)

Follow `google-apps-script/SETUP.md`. In short: create a Google Sheet, paste `Code.gs`
into Extensions → Apps Script, deploy it as a Web App, and paste the resulting URL into
`js/config.js`. Each form saves to its own tab, emails an alert to
treeindiafoundation1@gmail.com, and auto-replies to the visitor.
Until you add the URL, forms show a friendly "not connected yet" note.

---

## Deploy on GitHub Pages (recommended) with treeindiafoundation.org

1. Create a GitHub repository (e.g. `tif-website`) and upload **the contents of this
   folder** (so `index.html` sits at the repo root).
2. In the repo: **Settings → Pages**.
   - **Source:** Deploy from a branch
   - **Branch:** `main` (or `master`), folder `/ (root)` → **Save**.
3. **Custom domain:** the included `CNAME` file already contains
   `treeindiafoundation.org`. GitHub will pick it up. In Settings → Pages, confirm the
   custom domain shows `treeindiafoundation.org`, then tick **Enforce HTTPS** once it is
   available (can take a few minutes to an hour).
4. **Point the domain at GitHub (in GoDaddy DNS):**
   - Add four **A records** for `@` pointing to GitHub's IPs:
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - Add a **CNAME record** for `www` pointing to `YOUR-USERNAME.github.io`.
   - Remove any old parked/forwarding A records for `@` first.
   - DNS changes can take a little while to take effect.

That's it. To update the site later, edit files and push, GitHub Pages redeploys
automatically.

> Note: paths in the site are **relative** (e.g. `css/styles.css`, not `/css/styles.css`),
> so it also works from a project subpath like `username.github.io/tif-website/` if you
> ever skip the custom domain.

---

## Alternative: Apache or NGINX (EC2 or any server)

The site is plain static files, so just serve this folder.

**Apache**
1. Copy the folder contents into the web root, e.g. `/var/www/html/`.
2. Ensure the site is enabled and `index.html` is a directory index (default on Apache).
3. Restart: `sudo systemctl restart apache2`.

**NGINX**
```nginx
server {
    listen 80;
    server_name treeindiafoundation.org www.treeindiafoundation.org;
    root /var/www/tif-website;   # folder with index.html
    index index.html;
    location / { try_files $uri $uri/ =404; }
}
```
Then: `sudo nginx -t && sudo systemctl reload nginx`.
Add HTTPS with Let's Encrypt: `sudo certbot --nginx`.

On EC2, the `CNAME` file is harmless (it only matters to GitHub Pages) — you can leave it
or delete it. Point your domain's A record at the instance's Elastic IP instead.

---

## Notes
- The Marathi and Hindi text was drafted as a starting point. Have a native speaker
  proofread `lang/mr.json` and `lang/hi.json` before launch, especially programme terms.
- The impact numbers are five-year **targets**, labelled as such on the page.
- Form delivery uses a "fire and forget" request (the browser can't read Apps Script's
  cross-origin reply), so the site shows an optimistic success message. Your Sheet and the
  alert email are the real record that a submission arrived.

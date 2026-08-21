# Connecting the website forms to Google Sheets

This takes about 10 minutes. You do it once. After this, every form on the site
(Contact, Volunteer, Partner, Donate) saves to your Google Sheet, emails you an
alert, and sends the visitor an automatic thank-you reply.

## What you need
- A Google account with access to Google Sheets (you already have this).
- The file `Code.gs` from this folder.

## Step 1 — Create the Sheet
1. Go to https://sheets.google.com and create a **new blank spreadsheet**.
2. Name it something like **TIF Website Submissions**.
   (You do not need to add any tabs or headers. The script creates a tab for each
   form the first time that form is submitted: Contact, Volunteer, Partner, Donate.)

## Step 2 — Add the script
1. In that Sheet, click **Extensions → Apps Script**.
2. Delete any sample code in the editor.
3. Open `Code.gs` from this folder, copy everything, and paste it in.
4. (Optional) At the top of the file, check `OWNER_EMAIL` is
   `treeindiafoundation1@gmail.com`. Change it if you want alerts elsewhere.
5. Click the **save** icon.

## Step 3 — Deploy as a Web App
1. Click **Deploy → New deployment**.
2. Click the gear icon next to "Select type" and choose **Web app**.
3. Set:
   - **Description:** TIF forms (any text)
   - **Execute as:** **Me** (your account)
   - **Who has access:** **Anyone**
     (This is required so the website can post to it. It does not make your Sheet
     public — only this script can write to it, and only you can read the Sheet.)
4. Click **Deploy**.
5. Google will ask you to **authorize**. Approve the permissions
   (it needs to edit the Sheet and send email on your behalf).
   If you see "Google hasn't verified this app", click **Advanced → Go to (your project)**
   and continue. This warning is normal for your own scripts.
6. Copy the **Web app URL**. It looks like:
   `https://script.google.com/macros/s/AKfy...../exec`

## Step 4 — Put the URL in the website
1. Open `js/config.js` in the website files.
2. Paste your URL between the quotes:
   ```js
   GAS_URL: "https://script.google.com/macros/s/AKfy...../exec",
   ```
3. Save, and re-deploy the site (commit + push if using GitHub Pages).

## Step 5 — Test it
1. Open your live site, fill in the Contact form, and submit.
2. Check the Sheet: a **Contact** tab should appear with your row.
3. Check `treeindiafoundation1@gmail.com` for the alert email.
4. The email address you entered in the form should receive the auto-reply.

## Good to know
- **A tab per form:** Contact, Volunteer, Partner, and Donate each get their own tab,
  created automatically on first submission. Columns are added automatically to match
  the fields each form sends.
- **Editing the emails:** open the Apps Script editor and edit the text inside
  `sendAlert_` (team alert) or `sendAutoReply_` (visitor reply).
- **If you change `Code.gs` later:** click **Deploy → Manage deployments → (edit / pencil)
  → Version: New version → Deploy**. Keeping the same deployment keeps the same URL,
  so you don't have to update `config.js` again.
- **Email limits:** a normal Gmail account can send about 100 emails/day via Apps Script.
  That is plenty for typical NGO enquiry volumes.
- **Spam:** the forms include a hidden "honeypot" field that quietly blocks most bots.
  If spam ever becomes a problem, tell your developer and a free CAPTCHA can be added.

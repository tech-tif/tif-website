/*  Tree India Foundation — form handler for the website
 *  ---------------------------------------------------------------
 *  Receives submissions from index.html forms, writes each form type
 *  to its own tab, emails an alert to the team, and sends the visitor
 *  an auto-reply. Bound to your Google Sheet (Extensions > Apps Script).
 *  See SETUP.md for step-by-step deployment.
 * --------------------------------------------------------------- */

/* ============ CONFIG — edit these ============ */
var OWNER_EMAIL = "treeindiafoundation1@gmail.com";   // gets an alert on every submission
var ORG_NAME    = "Tree India Foundation";
var SEND_AUTOREPLY = true;                             // auto-reply to the submitter
var SEND_ALERT     = true;                             // alert email to OWNER_EMAIL

// Friendly tab + label per form type. Add a line here if you add a new form.
var FORMS = {
  contact:   { tab: "Contact",   label: "Contact enquiry" },
  volunteer: { tab: "Volunteer", label: "Volunteer sign-up" },
  partner:   { tab: "Partner",   label: "Partnership enquiry" },
  donate:    { tab: "Donate",    label: "Donation pledge" }
};
/* ============================================== */

function doPost(e) {
  try {
    var p = (e && e.parameter) ? e.parameter : {};
    var type = (p.formType || "contact").toLowerCase();
    var cfg = FORMS[type] || { tab: "Other", label: "Submission" };

    // Fields we don't want as their own columns
    var SKIP = { formType: 1, website: 1 };
    var fields = {};
    Object.keys(p).forEach(function (k) { if (!SKIP[k]) fields[k] = p[k]; });

    writeRow_(cfg.tab, fields);
    if (SEND_ALERT)     sendAlert_(cfg, fields);
    if (SEND_AUTOREPLY) sendAutoReply_(fields);

    return json_({ result: "success", tab: cfg.tab });
  } catch (err) {
    return json_({ result: "error", message: String(err) });
  }
}

// Simple browser check that the Web App is live
function doGet() {
  return json_({ result: "ok", service: ORG_NAME + " form handler" });
}

/* ---------- helpers ---------- */

function writeRow_(tabName, fields) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sh = ss.getSheetByName(tabName);
  if (!sh) {
    sh = ss.insertSheet(tabName);
    sh.appendRow(["Timestamp"]);
    sh.getRange(1, 1, 1, 1).setFontWeight("bold");
    sh.setFrozenRows(1);
  }
  // current headers
  var lastCol = Math.max(sh.getLastColumn(), 1);
  var headers = sh.getRange(1, 1, 1, lastCol).getValues()[0].filter(String);
  if (headers.length === 0) headers = ["Timestamp"];

  // add any new field as a new column
  Object.keys(fields).forEach(function (k) {
    if (headers.indexOf(k) === -1) {
      headers.push(k);
      sh.getRange(1, headers.length).setValue(k).setFontWeight("bold");
    }
  });

  // build row in header order
  var row = headers.map(function (h) {
    if (h === "Timestamp") return new Date();
    return fields[h] !== undefined ? fields[h] : "";
  });
  sh.appendRow(row);
}

function sendAlert_(cfg, fields) {
  var lines = Object.keys(fields).map(function (k) { return k + ": " + fields[k]; });
  var body = "New " + cfg.label + " from the website.\n\n" + lines.join("\n") +
             "\n\nSaved to the '" + cfg.tab + "' tab.";
  MailApp.sendEmail({
    to: OWNER_EMAIL,
    subject: "[" + ORG_NAME + "] " + cfg.label,
    body: body,
    replyTo: fields.email || OWNER_EMAIL
  });
}

function sendAutoReply_(fields) {
  var to = fields.email;
  if (!to || to.indexOf("@") === -1) return;   // no valid email, skip
  var name = fields.name || "there";
  var subject = "Thank you for reaching out to " + ORG_NAME;
  var body =
    "Namaste " + name + ",\n\n" +
    "Thank you for contacting " + ORG_NAME + ". We've received your message and " +
    "a member of our team will get back to you soon.\n\n" +
    "Together we're transforming roots through ecology and education.\n\n" +
    "Warm regards,\n" + ORG_NAME + "\n" + OWNER_EMAIL + "\nhttps://treeindiafoundation.org";
  MailApp.sendEmail(to, subject, body, { name: ORG_NAME });
}

function json_(obj) {
  return ContentService
    .createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

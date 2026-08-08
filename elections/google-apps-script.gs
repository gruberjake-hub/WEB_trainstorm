/* ===========================================================================
 * google-apps-script.gs  —  the bridge between the app and your Google Sheet
 * ---------------------------------------------------------------------------
 * You do NOT run this on your computer or on Render. You paste it into Google's
 * Apps Script editor, attached to a Google Sheet you create. It does two jobs:
 *
 *   WRITE (doPost): observers' "Submit to team" appends rows to the sheet.
 *   READ  (doGet):  drafters' "Load from team repo" pulls rows back out — but
 *                   ONLY when a matching secret token is supplied, so the data
 *                   isn't readable by anyone who finds the URL.
 *
 * SETUP (full steps in the README, "Central collection" and "Drafter read-back"):
 *   1. Create a Google Sheet.
 *   2. Extensions -> Apps Script.
 *   3. Delete the sample code, paste THIS in.
 *   4. Set READ_TOKEN below to a secret of your choice (any random string).
 *      Put the SAME value in Render as the env var SHEET_READ_TOKEN.
 *   5. Save.
 *   6. Deploy -> New deployment (or Manage deployments -> New version) ->
 *      Web app, Execute as: Me, Who has access: Anyone.
 *   7. Copy the /exec URL into Render as SHEET_WEBHOOK_URL (if not already set).
 * ========================================================================= */

// >>> REPLACE this with a random secret. The SAME value goes in Render as
//     SHEET_READ_TOKEN. Leave it blank to keep read-back disabled.
var READ_TOKEN = "REPLACE-WITH-A-SHARED-SECRET";

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];

    // Write the header row once, the first time anything is submitted.
    if (sheet.getLastRow() === 0 && data.header) {
      sheet.appendRow(data.header);
    }

    // Append one row per observation.
    var rows = data.rows || [];
    for (var i = 0; i < rows.length; i++) {
      sheet.appendRow(rows[i]);
    }

    return json({ ok: true, added: rows.length });
  } catch (err) {
    return json({ ok: false, error: String(err) });
  }
}

function doGet(e) {
  var params = (e && e.parameter) ? e.parameter : {};

  // Read-back mode: return the sheet as JSON, but only with the right token.
  if (params.action === "records") {
    if (!READ_TOKEN || params.token !== READ_TOKEN) {
      return json({ ok: false, error: "unauthorized" });
    }
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
    var values = sheet.getDataRange().getValues();
    if (values.length < 2) return json({ ok: true, records: [] });
    var header = values[0];
    var records = [];
    for (var r = 1; r < values.length; r++) {
      var obj = {};
      for (var c = 0; c < header.length; c++) {
        obj[header[c]] = values[r][c];
      }
      records.push(obj);
    }
    return json({ ok: true, records: records });
  }

  // Default: a simple liveness check you can open in a browser.
  return json({ ok: true, service: "observer-central-collection" });
}

function json(o) {
  return ContentService
    .createTextOutput(JSON.stringify(o))
    .setMimeType(ContentService.MimeType.JSON);
}

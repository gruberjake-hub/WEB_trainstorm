/* ===========================================================================
 * google-apps-script.gs  —  the tiny bridge that writes to your Google Sheet
 * ---------------------------------------------------------------------------
 * You do NOT run this file on your computer or on Render. You paste it into
 * Google's Apps Script editor, attached to a Google Sheet you create. Your
 * server then POSTs observations to the web-app URL Google gives you, and this
 * code appends them as rows.
 *
 * Full step-by-step is in the README under "Central collection". In short:
 *   1. Create a Google Sheet.
 *   2. Extensions -> Apps Script.
 *   3. Delete the sample code, paste THIS in, Save.
 *   4. Deploy -> New deployment -> type "Web app".
 *        - Execute as: Me
 *        - Who has access: Anyone
 *   5. Copy the Web app URL it gives you (ends in /exec).
 *   6. Put that URL in Render as the environment variable SHEET_WEBHOOK_URL.
 * ========================================================================= */

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

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true, added: rows.length }))
      .setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: String(err) }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Lets you open the web-app URL in a browser to confirm it's alive.
function doGet() {
  return ContentService
    .createTextOutput(JSON.stringify({ ok: true, service: "observer-central-collection" }))
    .setMimeType(ContentService.MimeType.JSON);
}

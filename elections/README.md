# Observer Field Log & Complaint Drafter — the harness

This is a small web app your fellow observers open on their phones in the field.
They log incidents as they happen; when they're ready, one tap sends the record
to a small server you run, which drafts a formal complaint using your Election
Complaint Filing Assistant system profile and the loaded Wisconsin ch. EL 4
rules.

You are reading the operator's guide. It has three parts:

1. **How the pieces fit together** (the mental model)
2. **Run it on your own computer** (5 minutes, to see it work)
3. **Put it on the internet** so your fellows can reach it from anywhere

There is no prior web-development knowledge assumed. Where a term might be new
(environment variable, endpoint, deploy), it's explained the first time it
appears.

---

## 1. How the pieces fit together

Think of it as three things talking to each other:

```
  PHONE (the observer)                 SERVER (you run this)            ANTHROPIC
  ────────────────────                 ─────────────────────           ─────────
  public/index.html         ──POST──►  server.js                ──►    Claude API
  - logs incidents                     - holds the secret key          - reads the
  - stores them on the                 - glues system-prompt.md          system profile
    phone (localStorage)                 + knowledge/*.md into a         - writes the
  - "Draft complaint" sends              system prompt                    complaint draft
    the record to the server           - forwards to Anthropic    ◄──   returns text
                            ◄─draft──   - returns the draft
```

The important idea: **the secret API key lives only on the server.** It is never
sent to the phones. That is the whole reason there is a server instead of just a
web page — a web page can't keep a secret. A server can.

The files, and what each one is for:

| File | What it is |
|---|---|
| `server.js` | The harness. One file, no external packages. Serves the app and does the drafting call. Heavily commented — read it top to bottom. |
| `public/index.html` | The app your fellows use. Self-contained (HTML + CSS + JavaScript in one file). |
| `system-prompt.md` | Your system profile. **Edit this to change how the drafter behaves** — no code changes needed. |
| `knowledge/project_context.md` | The loaded rule corpus (EL 4 statute + observer guidance). The source of truth for citations. |
| `.env` | Where your secret key lives on your own computer. Git-ignored, never shared. You create this from `.env.example`. |
| `.env.example` | A template showing which values to set. |
| `package.json` | Tells the host how to start the app (`node server.js`) and that it needs Node 18+. |

An **environment variable** (like `ANTHROPIC_API_KEY`) is just a named value the
computer hands to the program when it starts. On your own machine it comes from
the `.env` file. On a host, you type it into a settings box. Same idea, two
places.

---

## 2. Run it on your own computer

**You need:** Node.js version 18 or newer. Check by opening a terminal and
typing `node --version`. If it prints something below v18, or "command not
found", install the current LTS from <https://nodejs.org>.

**Step 1 — Get an Anthropic API key.**
Go to <https://console.anthropic.com>, sign in, add a payment method under
Billing (drafting costs money per use — see the cost note below), then
Settings → API Keys → Create Key. Copy the key; it starts with `sk-ant-`.
Treat it like a credit-card number.

**Step 2 — Create your `.env` file.**
In this folder, make a copy of `.env.example` and name the copy `.env`. Open it
and paste your key after `ANTHROPIC_API_KEY=`. Leave the other lines as they are
for now. Save.

**Step 3 — Start the server.**
In a terminal, move into this folder and run:

```
node server.js
```

You should see "Election Complaint Harness is running" and
"API key configured: yes". There are no packages to install — that's deliberate.

**Step 4 — Open it.**
In a browser on the same computer, go to <http://localhost:3000>.
Fill in the Setup tab, log a test incident, and tap **Draft complaint**. In a
few seconds you'll get a full draft with citation markers and a Dismissal Risk
Assessment.

To stop the server, press `Ctrl + C` in the terminal.

> Tip: the **Setup → Check server status** button confirms the server sees your
> key and which model it will use.

---

## 3. Put it on the internet (so your fellows can reach it)

Running it on your laptop only works while your laptop is on and only for you.
To give your fellows a link, put it on a host that runs it around the clock.

Any host that runs a Node app works (Render, Railway, Fly.io, a small VPS). The
walkthrough below uses **Render** because it has a free tier and a simple
dashboard. The same three ideas apply anywhere: give the host the code, tell it
the start command, and set the environment variables.

**Step 1 — Put the code on GitHub.**
Create a free account at <https://github.com>, make a new repository, and upload
this whole folder to it. (GitHub's web uploader works; the `.gitignore` here
makes sure your `.env` and its secret key are *not* uploaded.)

**Step 2 — Create the service on Render.**
Sign up at <https://render.com> → **New** → **Web Service** → connect your
GitHub repo. Set:

- **Runtime:** Node
- **Build command:** *(leave blank — there are no packages to install)*
- **Start command:** `node server.js`

**Step 3 — Add your environment variables.**
In the service's **Environment** section, add:

- `ANTHROPIC_API_KEY` = your `sk-ant-...` key
- `ACCESS_CODE` = a shared password of your choice (strongly recommended — see
  below)
- optionally `MODEL` = `claude-opus-5` for highest quality, or
  `claude-haiku-4-5-20251001` for lowest cost. Default is `claude-sonnet-5`.

Do **not** set `PORT` — Render provides it automatically, and the server reads
whatever the host gives it.

**Step 4 — Deploy.**
Click Create/Deploy. When it finishes, Render gives you a public URL like
`https://your-app.onrender.com`. That's the link you hand out. On a phone, open
it and use **Add to Home Screen** so it behaves like an app.

**Step 5 — Give your fellows the access code.**
If you set `ACCESS_CODE`, each fellow types it once under the app's **Setup**
tab. Without it, the server refuses to draft. This is what stops a stranger who
finds the URL from spending your API budget.

---

## Managing it once it's live

**Cost.** You pay Anthropic per draft, based on the model and the length of the
record + draft. With the default `claude-sonnet-5`, a typical single-incident
complaint is a fraction of a cent to a few cents of input plus output. `opus-5`
costs more per token; `haiku` costs less. Set a monthly spend limit in the
Anthropic console (Billing → Limits) so there are no surprises. The token counts
for each draft show under the generated complaint.

**Changing the drafter's behavior.** Edit `system-prompt.md` and redeploy (on
Render, push the change to GitHub and it redeploys, or click Manual Deploy). No
code changes required — the server rebuilds the system prompt from that file
every time it starts.

**Updating the rules.** Edit `knowledge/project_context.md` the same way. It is
the citation source of truth; keep it current with the statute.

**Changing the model.** Change the `MODEL` environment variable and redeploy.
Model IDs as of this build: `claude-opus-5`, `claude-sonnet-5`,
`claude-haiku-4-5-20251001`. If a model name is ever wrong, the app shows the
API's error (e.g. "model not found") right under the Draft button — swap the
value and redeploy.

---

## Security & responsibility notes

- The API key stays server-side and is never delivered to phones. Keep it that
  way — don't paste it into the front-end file.
- Use `ACCESS_CODE` for any public URL. It's a light gate, not a fortress; for
  anything more sensitive, put the app behind your host's password protection or
  a login.
- This tool **drafts**; it does not file, and it is not legal advice. Every
  draft carries citation-confidence markers (`[DIRECT CITATION]`, `[INFERRED]`,
  `[NOT FOUND]`) precisely so a human verifies each one against current statute
  text before filing. The Dismissal Risk Assessment is there to be read, not
  skipped.
- Observers' logged notes live on each observer's own device (localStorage) and
  in whatever JSON they export. Handle those exports the way you'd handle any
  contemporaneous field record.

---

## Troubleshooting

| Symptom | Likely cause / fix |
|---|---|
| Draft button says "no ANTHROPIC_API_KEY set" | The key env var isn't set (or, locally, `.env` is missing or misnamed). Set it and restart/redeploy. |
| "Anthropic API returned 401" | Wrong or revoked key. Create a fresh one. |
| "Anthropic API returned 404 ... model" | The `MODEL` value isn't a valid model ID. Use one from the list above. |
| "Anthropic API returned 400 ... credit balance" | Add a payment method / credit in the Anthropic console. |
| "Wrong or missing access code" | You set `ACCESS_CODE` on the server; enter the same code under the app's Setup tab. |
| Page loads but nothing saves | The browser is in private mode with storage blocked, or storage is full. Use a normal window. |
| Works on your laptop, not from a phone | `localhost` only works on the same machine — that's expected. Deploy (Part 3) to get a shareable URL. |

---

*Built from the Election Complaint Filing Assistant system profile, v2, and the
loaded ch. EL 4 corpus.*

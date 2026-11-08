<!-- Shared reference — one-time setup + quick "is everything connected?" check -->

# Setup & connection check

Run it **once after install** (when `python3 scripts/00_check.py show` says no assets source is chosen) and **again whenever a step fails** (Flow won't open, voice tools missing…). Keep it short and friendly: one line per step, a table at the end. You do the checking — the user only signs in / presses Connect when asked.

## Step 1 — Where do pictures and clips come from? (ask once)

Ask one question with two options (no jargon):

| Option | What it is | Needs | Best for |
|---|---|---|---|
| **A. Google API** (`api`) | Images from Google AI Studio by API key; videos (and fallback) via fal.ai | A free AI Studio key; fal key only if they want AI clips | Fast, stable, runs anywhere (phone/cloud too) |
| **B. My Google subscription** (`subscription`) | Claude drives **Google Flow in the user's Chrome** with their own Google plan | Chrome + the Claude extension + a Google account with Flow | No API bill, includes **video clips** (Veo); slower, computer only |

Recommend **B** if they have a Google AI plan and want clips without paying per clip; **A** if they want it simple and stable. Then save:

```bash
python3 scripts/00_check.py set-assets api            # or: subscription
```
They can switch any time ("use the API" / "use my subscription").

Free stock (`references/stock.md`) works in both modes.

## Step 2 — Run the checks (in this order)

```bash
python3 scripts/00_check.py show       # language, chosen source, tools (ffmpeg…), which keys exist
```
Missing `ffmpeg`/Whisper → `bash scripts/00_setup.sh --install` (ask first, as in start.md).

**A. ElevenLabs (voiceover)** — only if they want voiceovers.
Tools ending in `creative_list_voices` / `creative_generate_speech` present? ✅ Otherwise: `search_mcp_registry ["elevenlabs"]` → `suggest_connectors` with its uuid (shows the Connect button) → wait for "done" → re-check. Details: `references/voiceover.md`.

**B. If source = `subscription` → Chrome + Flow**
1. **Extension:** call `tabs_context_mcp` (load the Chrome tools with one ToolSearch first, see `google-flow.md`). Error / no browser → say: *"I can't reach Chrome. Open Chrome with the Claude extension enabled, then say 'done'."* If several browsers are listed, `list_connected_browsers` → `select_browser` the one that has the user's Google account.
2. **Flow access:** open a **new foreground tab** → `labs.google/fx/tools/flow` → `read_page` + screenshot. Judge by what you see:
   - Flow's workspace/project screen ✅ signed in and available.
   - A Google sign-in page, "Sign in" button, or a "not available / join waitlist / upgrade" message ❌.
3. **Not signed in → don't give up, and never type credentials.** Leave that tab **open and in front** (`tabs_select`) so the user sees it, say: *"Sign in to your Google account in this tab, then say 'done'."* Re-check once they answer. Account without Flow access? Tell them plainly and offer option A.
4. **Don't generate anything to test** — opening the page is enough (a test would spend credits).

**C. If source = `api` → key check**
```bash
python3 scripts/00_check.py gemini     # free read-only test of the AI Studio key (no generation)
```
No key → send them to aistudio.google.com → "Get API key" → paste into `.env` as `GEMINI_API_KEY=…` (never echo it back). For AI video clips they'd also need `FAL_KEY` (paid) — say so; otherwise switch to option B for clips.

## Step 3 — Report (one small table, then start working)

```
Language ........ English            ✅
Assets source ... Subscription (Flow) ✅  signed in as the open tab
Voiceover ....... ElevenLabs          ✅ connected
Stock ........... Pexels key          ✅ / — (optional)
Tools ........... ffmpeg · whisper    ✅
```
Anything ❌ → say the one fix in plain words and offer to continue without it. Then go on with the user's real request.

## When something fails later
- **Flow step fails, redirects to sign-in, or shows an account error** → **always bring Chrome forward**: `tabs_select` the Flow tab (or open `labs.google/fx/tools/flow` in a foreground tab), tell the user to sign in or pick the right Google account, wait for "done", then retry **once**. Still failing → one line to the user, fall back to option A / stock / motion graphics.
- **Voice tools gone** → repeat check A.
- **Key rejected** → repeat check C.

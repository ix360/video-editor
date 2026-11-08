<!-- Shared reference — Google Flow / AI Studio through the Chrome extension (EXPERIMENTAL) -->

# Google images & video without API cost

Order of preference for scene assets (cheapest first):
1. **Stock** — `references/stock.md`
2. **Gemini images by API key** — `GEMINI_API_KEY` from Google AI Studio; `17_gen_scenes.py` uses it automatically for images (free allowance if the account has one — check the quota in AI Studio).
3. **Google Flow in the browser** — this file. Images and **video clips** (Veo) with the user's own Google subscription, no API bill. ⚠️ Experimental.
4. **Paid fal.ai** — `references/gen-scenes.md`.

## When to use Flow
- The user wants a **video clip** (not just an image) and has a Google AI plan, and doesn't want to pay per clip.
- Never silently: say *"I'll generate this in your Google Flow with your subscription — it uses your daily credits and takes a few minutes. OK?"*

## ⛔ Honest limits (tell the user once)
- It is **UI automation of a consumer account**: it can break when Google changes the page, runs only on a computer with Chrome + the Claude extension (not phone/cloud), and clips take minutes each.
- Google's terms for automating a consumer account are unclear to me and I have not verified them. It is the user's account and risk — get a clear yes.
- Quotas and watermarks depend on the user's plan. After the first clip, check whether the result has a watermark; if it does, tell the user before using it.
- **Never** type a password or 2-step code. If Google asks to sign in, ask the user to sign in themselves in the tab, then continue.

## Procedure
Use the Chrome tools (`mcp__claude-in-chrome__*`; load them with ToolSearch in ONE call: `tabs_context_mcp, tabs_create_mcp, navigate, read_page, find, computer, javascript_tool`). Don't hard-code selectors — Google changes the UI. Find controls by reading the page (`read_page` / `find`) and verify with a screenshot.

1. `tabs_context_mcp`, open a **new tab**, navigate to **labs.google/fx/tools/flow** (images/video) — or **aistudio.google.com** for Gemini/Imagen prompts.
2. Signed in? If not → user signs in; wait.
3. Create/open a project named after the video. Choose: image or video, **9:16 vertical**, the model, and **one output** per prompt (each output spends credits).
4. Paste the prompt (English, from `gen.json`; keep the engine's rules: no readable text, no logos — see `references/gen-scenes.md`). Submit.
5. Wait with short `wait` calls (video: minutes). Screenshot to confirm it finished; **do not resubmit** while it's running.
6. Ask permission to download (it saves a file to the Downloads folder: say the file name). Then download via the page's download control.
7. Find the newest file: `ls -t ~/Downloads | head -3`; check with `ffprobe`; import:
   ```bash
   python3 scripts/17_gen_scenes.py <work> import <k> ~/Downloads/<file>.mp4
   ```
   (`import` turns a clip into frames, or a picture into the asset image.) Move on to the next asset.
8. Log what each clip cost (credits shown on the page) in your status line to the user.

## Setup, and sign-in failures
The one-time choice (Google API vs. subscription) and the connection check are in `references/setup-check.md`. Use this file only when the saved mode is `subscription` (`python3 scripts/00_check.py show`).
**If Flow shows a sign-in page, the wrong account, or won't open:** bring Chrome forward (`tabs_select`, or open Flow in a foreground tab), ask the user to sign in themselves, wait for "done", retry once.

## Failure → fall back
Page changed / generation blocked / quota hit → stop, say what happened in one line, and continue with the next option (stock → Gemini → fal.ai, or a motion-graphics scene instead of a photo). Don't loop.

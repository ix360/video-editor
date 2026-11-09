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

## What the Flow page looks like today (tested 9 Nov 2026)
Flow opens a project with a **chat agent** on the right ("What do you want to create?"). Don't hunt for old buttons — talk to the agent:
- **Settings first:** the sliders icon beside the send arrow → *Agent settings*: *Image generation default* → **9:16**, **x1** (one output per prompt); *Video generation default* → **9:16**, **x1**; keep *Confirm before generating: Always* if the user wants a safety net. Save.
- **Prompt as plain English:** "Generate one vertical 9:16 image: …" / "Generate one vertical 9:16 video of … (4 seconds, no text, no logos)". Submit with the send arrow. Images take about 30–50 s, video minutes. Do not resubmit while it runs; the card shows a percentage.
- **Download:** click the finished item → editor → the **download icon** (top right) → pick **1K original** (free). 2K/4K "upscaled" may cost credits or need an upgrade — don't pick them without asking. The file lands in `~/Downloads` (e.g. `Human_eye_macro_photograph_<hash>.jpg`). For video the same menu offers the video sizes: take the smallest that is ≥720p.
- Switch between the project's items with the little thumbnails at the top of the editor.
- Everything was done with the user's PRO account: no watermark was visible on the downloaded images. Check each video the same way.

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
   python3 scripts/17_gen_scenes.py <work> import <k> ~/Downloads/<file>.mp4 --project <motion-project>
   ```
   (`--project` is for motion films: it turns a clip into frames inside the project and registers `project.json → clips`, or a picture into `assets/` + `images`. Without it, `import` writes to `<work>/gen/` for the reel/podcast flow.) Move on to the next asset.
8. Log what each clip cost in your status line to the user. Flow's agent shows its own confirmation with the credit cost and the model before it generates (tested: **12 credits per 4-second clip**, model "Omni 1.2 Flash", about 2.5–3 minutes each); that dialog is Flow's, not a replacement for the user's one-time yes to the credits and the downloads. Downloaded video options: take **720p "Original size"**, not the upscales.

## Setup, and sign-in failures
The one-time choice (Google API vs. subscription) and the connection check are in `references/setup-check.md`. Use this file only when the saved mode is `subscription` (`python3 scripts/00_check.py show`).
**If Flow shows a sign-in page, the wrong account, or won't open:** bring Chrome forward (`tabs_select`, or open Flow in a foreground tab), ask the user to sign in themselves, wait for "done", retry once.

## Failure → fall back
Page changed / generation blocked / quota hit → stop, say what happened in one line, and continue with the next option (stock → Gemini → fal.ai, or a motion-graphics scene instead of a photo). Don't loop.

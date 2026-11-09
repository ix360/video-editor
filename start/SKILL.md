---
name: start
description: The one command that runs the whole video workflow end to end — setup check, a one-question brief, the script (hook, story, call to action), the voice (the user's own mp3, their ElevenLabs voice, or a ready-made one), photos and clips, then the edit and delivery. Use when the user types /video-editor:start, or says "start", "make a video", "make me a video about", "new video", "let's make a reel", "make an ad", "from idea to video", or "ابدأ"، "سو لي فيديو"، "ابي أسوي فيديو"، "فيديو جديد"، "commençons une vidéo"، "hagamos un video". It routes to video-editor, motion-video, podcast-video, montage-video, script-writer and voiceover-video — the user never has to pick a skill.
---

# Start — from idea to a finished video, one flow

You are the director. The user says what they want; you run the stages in order, skip what's already done, and never make them pick a skill or a mode.

Engine (all `scripts/`, `references/`, `motion/`): `${CLAUDE_SKILL_DIR}/../video-editor`

## 🌐 Language, tone
Work in the user's saved language (`python3 scripts/_lang.py`; ask once if none — `references/language.md`). You prepare things, they don't: never hand them commands, never ask "do you have X?" — check yourself. Say where you are in one line per stage. One question at a time.

## The map (6 stages)

```
 0 setup  →  1 brief  →  2 script  →  3 voice  →  4 look + assets  →  5 build  →  6 deliver
```

**Resume anywhere:** make (or find) the work folder, then run
`python3 scripts/42_start.py status <work>` — it prints which stages are done and the NEXT one. Continue from there. Save the brief with `python3 scripts/42_start.py set <work> topic="…" goal=… platform=… length=… format=… voice=…`.

---

### 0 · Setup (first time only — skip silently if done)
Do `references/start.md` steps **0.2 language** and **0.3 setup check** (assets source A/B, ElevenLabs, Chrome, Flow). Don't repeat them on later videos. Tell them in one line what's ready.

### 1 · The brief — ONE message
Ask only what you can't guess, in a single message:
1. **What is the video about** (a topic, an offer, a link, or "I have footage")?
2. **Goal and where it will be posted** (sell · leads · teach · followers — Reels/TikTok/Shorts/YouTube).
3. **Do you appear on camera, or is it voice only?**

**Detect the language of the script/footage** — if it differs from the chat language, run `python3 scripts/00_onboard.py lang video <code>` (and `lang video clear` for a video in the chat language) so voice, transcription and captions use it; say so in one line. Everything else (audience, length 30–45 s, the CTA) you infer and say back in one sentence. Then pick the **format** yourself — never ask "which mode?":

| What they have / want | Format | Skill that builds it |
|---|---|---|
| A video of them talking | **Talking reel** | `video-editor` |
| Two+ cameras, an episode, an interview | **Podcast** | `podcast-video` |
| Clips with no speech (café, product, travel) | **Montage** | `montage-video` |
| No footage — an idea, a text, a device, a website/app | **Motion film** (graphics, plus photos/clips for scenes that need them) | `motion-video` |
| Only a cover / thumbnail | **Cover** | `thumbnail-video` |

Save the brief (`42_start.py set …`).

### 2 · The script
Invoke the **`script-writer`** skill: three hooks → they pick → body → one CTA → shot list → checklist → `<work>/script.md`.
- They **already have a script** → don't rewrite; run its checklist and report only what fails.
- **Talking reel from their footage** → the words come from the footage; write only the hook and the CTA (`references/podcast-hook.md`, `22_hook.py`), and skip stage 3.

### 3 · The voice (voice-only films)
Ask once, as a list: **"Whose voice reads this?"**

1. **My own voice — I'll send an mp3** *(free, most natural)*. Tell them: **"Read the script above, record it on your phone (Voice Memos or any recorder), and attach the file here — mp3, m4a or wav."** When it arrives:
   `python3 scripts/39_voice_sample.py prepare <the-attached-file>` → use it as the narration `<work>/vo.mp3`. Under 5 s or very quiet → ask for another take, closer to the mic.
2. **My cloned ElevenLabs voice** → the `voiceover-video` skill (path A).
3. **A ready-made voice** → the `voiceover-video` skill (path C).
4. **Clone my voice from an mp3 sample** → they attach 1–3 minutes of themselves talking; `voiceover-video` path B.

Never generate before pricing it (`voiceover-video` rules). The audio becomes `<work>/vo.mp3`; Whisper then gives word timing.

### 4 · Look and assets
- **Theme:** `references/start.md` steps **0.5 and 1** (taste page, colors, caption style) — saved taste is **announced and offered for change, never skipped silently**, and the palette is the user's, never one you invent. Reuse an existing `theme.json`; never change it unasked.
- **The end card:** a reel/podcast uses `theme.json → outro` (its default wording follows the video language). A motion film has **no automatic end card**: its last scene *is* the call to action, drawn with the move bank.
- **The move palette (mandatory, every film):** `python3 scripts/35_moves.py plan --title "…" --family auto --cues number,contrast,emphasis,cta > <work>/moves_plan.json` (cues from the script's real moments) — the 3 core moves + accents the film revolves around (`references/moves.md`). Tell the user the palette in one line. Without `moves_plan.json`, `42_start.py status` will not let you reach the build. Replace the default end card with the CTA from the script (`theme.json → outro`).
- **Scene plan** (motion films): read `script.md`'s shot list and give every scene a type — `graphic` · `image` · `clip` · `screen`. Show it to the user as a short list before building. Default mix for a motion film: roughly **half graphics, half photos/clips**, because a film made only of graphics reads as a slideshow.
- **Default recipe for a motion film: motion graphics + at least one 3D scene + Flow video clips** (about a third each; at least 2 clips of 3–6 s). Flow clips beat photos, always — photos/stock only when the user declines the credits or Flow fails. Technical/medical facts stay graphics/3D; clips are for mood, place and action. Ask permission once for the Flow credits, then follow `references/google-flow.md`.
- Register each file straight into the project: `python3 scripts/17_gen_scenes.py <work> import <k> <file> --project <project>`; scenes play it with `ctx.drawClip(X, "<k>", lt, {...})` (`references/motion-mode.md`). Other sources, cheapest first, for the fallback: free stock (`references/stock.md`) → Gemini images (`references/gen-scenes.md`) → fal (paid, only if they agree).

### 5 · Build
**Zoom and motion are the point of this plugin, in every video:** a punch-in/camera move on the hook and on every key word, kinetic type, and a move from the plan on every scene — never a film of static cards. Photos are never still: push, parallax or ken-burns through `ctx.FX` (`pushIn`, `kenBurns`, `snapZoom`, `punchCut`…). Talking reels: `hookZoom`, `punchCut` and the compose moves.
For a motion film, **before rendering** run `python3 scripts/42_start.py audit <project>` — it fails if scenes don't use the move bank or have no camera/zoom moves; fix and re-run until it passes.
Hand over to the skill from the table in stage 1 and follow its steps (`motion-video` → `references/motion-mode.md`; `video-editor` → its SKILL.md). Rules that always apply: show a frame after each important step; no number or name on screen that isn't in the script or `facts.md`; Western digits; colors from `theme.json`.

### 6 · Deliver
Show the final frame sheet and the file path. Ask **one** question: "What do you want changed?" Apply, re-render only what changed. **Delivery is a file only — never post or schedule.**

---

## ⛔ Rules
- Don't skip the script for a no-footage film: a film without a written hook and CTA is the failure this flow exists to prevent.
- One decision per message; a stage already done (per `status`) is never asked again.
- If a connector or Flow fails mid-way, follow `references/setup-check.md` (bring Chrome forward so they can sign in) and resume — don't restart the flow.
- Cost: say what costs credits (ElevenLabs, paid generators) before spending, once.

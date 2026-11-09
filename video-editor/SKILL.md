---
name: video-editor
description: Edits a talking-head video into a 9:16 reel or ad — removes silences, adds word-timed captions (Arabic and 9 other languages) and motion graphics in the user's own colors. Use when the user says "edit this clip", "turn this video into a reel", "remove the silences", "add captions", "make an ad from this video", or sends a talking-head video; also "منتج هذا المقطع"، "حوّل الفيديو لريل"، "شيّل السكتات"، "ركّب كابشن عربي"، "سو من هذا الفيديو إعلان". Not for carousels or video covers.
---

# Reel from a talking video — no editing software

The whole edit is code:
- ffmpeg cuts.
- Whisper transcribes with word-level timing.
- A renderer draws captions and motion graphics over the video.

Output: one MP4, ready to post.

**Paths:** every `scripts/`, `references/` and `motion/` below lives in this skill's folder:
`${CLAUDE_SKILL_DIR}`

---

## Not a talking video? Go to the right mode

| Input | Mode | Read |
|---|---|---|
| A folder of clips with no speech (café, table, product) | Beat-synced montage | `references/montage.md` |
| Two or more cameras of the same session | Podcast → reels | `references/podcast.md` |
| A full episode "widescreen" or "for YouTube" | Podcast 16:9 | `references/podcast.md` (section "Full episode, widescreen") |
| A one-hour episode → several reels | Reels from an episode | `references/landscape.md` (section "Full episode") |
| Text or an idea, no person | Motion explainer | `references/motion-mode.md` |
| "Explain how X works" (a device, a machine) | The device as a machine that draws itself, then runs | `references/machine-explainer.md` |
| A website link or "explain the app" | Website / app explainer | `references/motion-mode.md` |

If a dedicated skill for that mode is installed (`motion-video`, `podcast-video`, `montage-video`), it takes priority.

⛔ **Never ask "which mode do you want?"** — tell the user in one sentence what you understood, and carry on.

**Renderer:** always the light one (`04_render_frames.js`), and never mention the word "renderer".
- User wants to edit by hand? Open the studio → `references/studio.md`
- A Remotion screen only if they ask for it by name → `references/remotion.md`

**🎞️ CapCut mode:** user says "make it in CapCut" or "I want to edit it myself in CapCut"? Instead of an MP4, produce an editable CapCut project (zoomed shots, CapCut captions and text, voice, effects, background audio, transparent motion) → `references/capcut.md` (one script, `scripts/40_capcut.py`).

---

## 🌐 Language

These instructions are for you; **the user picks their own language** (10 supported) — `references/language.md`. Ask once, the first time. After that, everything you say, the transcription language and the captions follow their choice (`scripts/_lang.py` prints the code). The example sentences below show meaning only — never copy them to a user who speaks another language.

## ⛔ How you treat the user

**You prepare things, not them.** Never hand them a list of commands to run.

- **Don't ask "do you have X?"** — check yourself.
  Something missing? "I need to set up two tools for you now, about two minutes — start?"
- **No jargon:** "a tool that draws the slides", not "puppeteer"; "video quality", not "codec".
- **Say where you are at every step** and estimate the time:
  "Silences removed — half the video is gone. Now transcribing your speech, about 3 minutes."
- **One thing at a time.**
- **Never deliver without showing them** a frame or a summary after each important stage.

## ✅ Where it runs — anywhere: phone · cloud · Mac · Windows · Linux · Codex

A local machine (Mac + Claude Code) is fastest and strongest, **but not required**. Never tell the user "this can't be done on your phone or in the cloud". If a tool doesn't work in the environment, drop to the fallback and mention in one line what you used instead.
**Read `references/any-environment.md`** — the ladder of fallbacks (transcription, person cut-out, motion drawing…) and the phone workflow. Tested recipes in detail (steady cut with no jitter, paper-cutout motion, assembly) are in `references/phone-cloud-playbook.md`.

- On a phone: the user attaches the video to the chat and it runs in the cloud environment; the phone can lock.
- Windows: `python`, not `python3` → `references/windows.md`.

---

## Steps 0, 0.5 and 1 — tools, taste and identity

Read `references/start.md` and do it — the same start for every mode.

---

## Step 2 — get the video

| Way | How |
|---|---|
| **A file on their computer** (best) | copy it to `<work>/src.mov` |
| **A Google Drive link** | sharing set to "anyone with the link", then the command below |
| **Google Drive connector** | if the file is private — use the connector's tools in the session |

Drive link (the ID sits between `/d/` and `/view`):

```bash
curl -sL "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t" -o <work>/src.mov
```

- 4K is best (zooming loses less quality). 1080p works too — **never reject it or ask for a re-shoot.**
- **A landscape video** (interview, podcast, TV episode)? Same steps.
  Step 6 crops lengthwise around the face for each shot instead of stretching → `references/landscape.md`
- **🪝 A reel from an episode or interview = a written hook is mandatory.** After `02_captions.py`:
  1. `python3 scripts/22_hook.py suggest <work>`
  2. Write 3 hooks from the strongest line (not the first sentence they said) → `check` → they choose → `apply`
  3. `preview` and read `hook_sheet.jpg` before the full render.
  - A reel built outside our engines (a finished mp4)? `22_hook.py overlay` → a transparent `hook.mov`.
  - Rules and formulas → `references/podcast-hook.md`

Check the duration:

```bash
ffprobe -v error -show_entries format=duration -of csv=p=0 <work>/src.mov
```

### 🎞️ Dropped frames?

A browser recording or a non-native camera app (an iPhone through a browser drops 13–54% of frames). Check for gaps before cutting:

```bash
ffprobe -v error -select_streams v -show_entries frame=pts_time -of csv=p=0 <work>/src.mov | python3 -c "import sys;t=[float(x) for x in sys.stdin if x.strip()];g=[(round(a,2),round(b-a,2)) for a,b in zip(t,t[1:]) if b-a>0.07];print(len(g),'gaps',g[:8])"
```

Gaps found? Repair before step 3:

```bash
ffmpeg -i src.mov -vf "minterpolate=fps=30:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" -c:a copy src_fixed.mov
```

Tell them: "The recording had dropped frames — I repaired it." And next time, advise recording with the camera app.

### 🔬 Light and color check (seconds, silent)

```bash
python3 scripts/25_scopes.py <work>
```

- "Fine" → don't mention it.
- A problem (dark, yellow cast, washed out) → one sentence: "The video is a bit dark with a yellow cast — fix it?"
  - Show before and after in one frame.
  - Yes → `theme.json` → `"grade":"auto"` (corrects exposure only).
  - No or silence → don't touch it (rule 4).

---

## Steps 3–11 — production

### 3) Cut plan

```bash
python3 scripts/01_cut_plan.py <work>
```

Tell them how much was removed: "Removed 52 seconds of silence — the video went from 98 to 46."

**3.5) Improve the audio (optional):** echo or noise, or they said "improve the audio"?
→ `references/audio-enhance.md`

```bash
bash scripts/02b_enhance_audio.sh <work> --local
```

### 4) Word-timed transcription

```bash
ffmpeg -v error -i <work>/src.mov -vn -ac 1 -ar 16000 -y <work>/a.wav
python3 -m whisper <work>/a.wav --language $(python3 scripts/_lang.py) --model medium --word_timestamps True \
  --output_format json --output_dir <work> --fp16 False --verbose False > <work>/whisper.log 2>&1
```

- Takes minutes — run it in the background and tell them what to expect.
- Failed? `tail -5 <work>/whisper.log`

**4.1) ⛔ Check the transcript before correcting it — mandatory** (6.1 — a "$1000 a day" reel: `medium` produced "subscribe to the channel" ×15 in the last 26 s instead of the real speech, and silently dropped 4 s in the middle):

```bash
python3 scripts/02a_whisper_check.py <work>          # 0 = clean · 3 = prints the suspicious windows
python3 scripts/02a_whisper_check.py <work> --fix    # re-transcribes only those windows and merges them into a.json (the original stays a_orig.json)
```

- Detects: the same sentence 3 times in a row · known hallucination phrases · a word ×4 · any gap with speech in the audio but no transcript.
- `--fix`: the window (with the sentence before and after — usually truncated) is split at silences into pieces ≤ 25 s and re-run **without context**
  (`condition_on_previous_text=False`): hallucinations feed on the previous text, and a lone piece resolves. It adds the piece's start to every timestamp and re-checks. About a minute.
- Manual, if needed: `ffmpeg -ss <from> -to <to> -i a.wav p.wav` → `python3 -m whisper p.wav … --condition_on_previous_text False`
  → add `<from>` to the sentence's `start`/`end` and its words → replace the window's sentences in `a.json`.
- Still something left after the fix? Correct it in step 5: one text instead of the list for the hallucinated sentence.

### 5) Corrections and captions

Read `a.json` and correct every sentence — Whisper makes mistakes, especially with dialects. Write `<work>/fixes.json`:

```json
{ "fix": [["every","thing","you","see"], ["the","caption","zoom"]], "hot": ["see","zoom"], "fx": {"done":"drop"} }
```

- `hot` = words that get a highlight pill while they are spoken.
- `fx` is optional → `references/word-fx.md`
- ⛔ **The word count of each sentence = Whisper's word count for the same sentence.** Otherwise the timings drift (the script stops you).

```bash
python3 scripts/02_captions.py <work>
```

### 5.5) Show them the text, and remove what they don't like → mandatory

Before designing any scene:

```bash
python3 scripts/10_script_edit.py <work> show
```

- Prints their speech numbered with timings, and writes `script.txt`.
- It also prints repeated sentences and a suggested deletion in the same run — don't run `dupes` afterwards.
- ⛔ **Print the whole script in the chat** and ask: "What do you want me to remove?" — don't just point to the file.

**A repeated sentence:** the first is a mistake, the second the correction.
"You said it twice — ‹we could solve the cause› then ‹we could identify the cause›. Remove the first?"

```bash
python3 scripts/10_script_edit.py <work> drop 6 8       # removes both sentences from the video and audio
python3 scripts/10_script_edit.py <work> keep 1 2 5 9   # keeps only these
python3 scripts/10_script_edit.py <work> undo
```

- Everything after shifts, and `cut.json`, `caps.json` and `sfx.json` update.
- **Do it here.** Deleting after the scenes are designed shifts all their timings.
- After any deletion: redo step 6, and render with `--force`.

### 6) Cut and zoom

```bash
python3 scripts/03_cut_zoom.py <work>
mkdir -p <work>/vfr && ffmpeg -v error -i <work>/cutz.mp4 -vf fps=30 -q:v 3 -y <work>/vfr/%05d.jpg
```

- **The zoom is locked per clip (6.0):** the first run writes `cut.json` → `"zooms": {"25.05": 1.06, …}` (the key is the clip start in source seconds).
  Removing, adding or splitting a clip? The other clips' zoom doesn't slide, so your drawing coordinates stay right. To change a clip's zoom, edit its number. `keep` order is free (a clip from the end of the speech may come before an earlier one).

**6.1) ⛔ Crop from above the head — mandatory in any video with a card** (screen text, `R_DOWN`, `R_LOWER`):

```bash
python3 scripts/23_headcrop.py <work> --from <start of the first card>
```

- Writes `studio.json` → `cardTop`.
- The crop is **fixed for the whole video** — no tracking, no camera following.
- It starts above the highest point the head reaches, with a small margin (1.5%).
- It never cuts the head and never leaves an empty ceiling — "too much space above the head" is just as wrong.
- The user has pointed this out more than once and was upset.
- Check with your own eyes on a frame where they lean toward the camera.
- Burned-in text under the body? Zoom in with `theme.json` → `cardZoom` (default 1).

### 7) Design the scenes → the most important step

**Before any scene, read:**
1. `references/motion-rules.md` — identity, the `facts.md` list, the prohibitions.
2. `references/scenes.md` — how to write a scene, the motion pack, ideas, b-roll.
3. `references/moves.md` — **the move bank:** `python3 scripts/35_moves.py plan --title "…" --cues …` → the video's palette (3 core moves it revolves around + accents). You choose consciously; the user doesn't need to.
   + `references/styles.md` — **the style bank (17):** the palette produces a `style` (knockout, paper cutout, documentary, news explainer…) = the look of the whole video (surface, texture, font, cards). A language, not a template: merge `a+b`, take a part, or invent one from the meaning of the sentence.

**🎯 The core from the first draft (6.0 — the Bobian reel that the bank adopted and went viral):** invest in performance and motion — rich, deep, surprising, not quiet things.
- Before drawing, plan **2–3 depth moments** and tell the user in one line: an element passing **behind their head** (`11_behind_text.js person` + `MV.person`),
  a **wave from their voice** (`37_env.py` → `MV.env`), a dot map behind their head, a **3D orbit**, a **shape from the client's identity** that becomes motion (the logo arc = a counter and a wipe), a **one-take entrance** (the camera dives into the logo and comes out in the next shot).
- These are the first things to reach for, not the only ones: cards, stamps and badges are **not forbidden** — use them when the topic deserves it.
- The sentence the motion writes out = `nocap` for it (so attention doesn't split between top and bottom). Writing above the head is best when there's room.
- **⛔ An element must not vanish with the last word (6.1):** it stays 0.3–0.6 s after it and leaves gently over 0.4 s, and the next one in the same place enters overlapping it — `e = last word + 0.45` (`references/motion-rules.md` §3).
- Recipes in code → `references/moves.md` §3f.

**⛔ Layout rule (approved by the user):**

| Moment | Rectangle | Look |
|---|---|---|
| Speech with no drawing | `R_FULL` | their face full screen, caption bottom at 1460 |
| Any drawing or motion | `R_DOWN` | the drawing on top (y 280–520) → caption → their face below at full width |
| B-roll or a big panel | `R_LOWER` | the big card on top → caption → a small face below |
| A full explanation (numbers, lists) | `R_OFF` | no face, their voice continues → `references/explainer-and-pace.md` |

- ⛔ **A caption is never written over the speaker's face.**
  In any mode with a video card, the whole caption sits above the card, with the progress bar.
- **Choosing the mode is your decision from the meaning** — is the face or the drawing more important? (Details in `scenes.md`.)

**⛔ Safe area** (Instagram buttons — `08_safe_check.js` checks it):

| Area | Put no text in |
|---|---|
| Top | y 0–150 |
| Bottom | y 1620–1920 (and a caution band 1500–1620) |
| Right | x 950–1080 between y 1100 and 1750 (like, comment, share) |

The engine is already set: caption bottom at 1460, progress bar at 1492 on full screen.
**And the first caption appears within the first half second.**

**Preview before drawing everything — one sheet of 6 frames:**

```bash
node scripts/04_render_frames.js <work> preview 1.2 4.6 12.3 27.6 31.0 48.4
bash scripts/07_contact_sheet.sh <work> <work>/sheet.jpg 1.2 4.6 12.3 27.6 31.0 48.4
```

- The sheet is 3 columns × 2 rows at 1080 wide, with each frame's time on it.
- **Read `sheet.jpg` alone** — not the frames one by one, and not many sheets.
- Show it to them before the full render.

### 7.x) Extras — each has its own reference; open it only when you need it

| Extra | Reference |
|---|---|
| A phone screen recording (inside a drawn phone frame) | `references/screen-recording.md` |
| Cut styles: speech behind the person, in front of the panel, head outside the rectangle (Mac) | `references/cut-styles.md` |
| "Layers" for the hook: one word above the head, two behind it, the rest in front (Mac) | `references/cut-styles.md` |
| Beat effects (cuts, zoom and shake on the beat) | `references/beat-fx.md` |
| Word effects, caption styles, the kashida | `references/word-fx.md` |
| A full explainer with no face + a calm pace | `references/explainer-and-pace.md` |
| Faded backdrop | `references/backdrop.md` |
| Collage (the screen is paper and they're a cut-out) | `references/collage.md` |
| An element that follows their hand — a logo rising from the palm (Mac) | below ↓ |
| Find a shot by meaning inside the b-roll | `references/find-shots.md` |
| 🆕 Setup check: assets source (API or Google Flow subscription) + ElevenLabs, Chrome and Flow connection | `references/setup-check.md` |
| 🆕 Free stock (video and photos) — Pexels · Pixabay · Unsplash | `references/stock.md` |
| AI-generated scenes: images with an AI Studio key (`GEMINI_API_KEY`) or fal (`FAL_KEY`) | `references/gen-scenes.md` |
| 🆕 Images and clips from Google Flow in the browser, no API cost (experimental) | `references/google-flow.md` |
| 🆕 Voiceover in their own voice or a ready-made one — ElevenLabs (skill `voiceover-video`) | `references/voiceover.md` |
| They are in another place and speak with their voice (avatar) | `references/talking-avatar.md` — ⛔ read "tried and failed" before spending anything |
| The studio — edit the timeline by hand | `references/studio.md` |

**Source order (cheapest first):** stock → Gemini images → Flow → paid fal. Spend only if the one before didn't suffice.

**"Layers" for the hook:**

```bash
node scripts/11_behind_text.js <work> stack 1
node scripts/04_render_frames.js <work> preview
```

Remove one of its sentences: `drop <number>`.

**An element that follows their hand:**

```bash
python3 scripts/29_handtrack.py <work> <from> <to>
```

- Produces `palm.js` (a smoothed palm path).
- Put it in `compose.html`: `<script src="palm.js"></script>`, and use `palmAt(t)` in your scene.
- Coordinates are on the full-screen video. The scene is a card (`R_DOWN`…)? Convert them with the card's scale.

### 8) Sound effects

```json
{ "outro": 5.2, "whoosh_up": [3.1,11.25], "whoosh_down": [7.85], "thud": [27.27,29.47], "tap": [23.08,24.06] }
```
- `outro` = the end card's duration. Missing = 0 (no card) — and `04_render_frames.js` stops with an error if the duration is not a number or is zero (before 6.0 it produced "0 frames" and silently succeeded).

```bash
python3 scripts/05_sfx.py <work>
```

### 9) Final render and assembly

```bash
node scripts/04_render_frames.js <work> all
bash scripts/06_encode.sh <work> <work>/ad-final.mp4
```

- The render resumes where it stopped — it doesn't redo finished frames.
- Edited a scene after rendering? Redo only its window, then assemble:
  `node scripts/04_render_frames.js <work> range 26.4 31.2`
- `--force` with `all` redoes everything. The script warns you if a frame is missing.
- **📦 Size (6.1):** a reel longer than a minute and a half usually comes out here above 30 MB (the $1000 reel: 124 s → 59 MB) — normal, this is the high-quality version.
  The cover (`28_cover.py --first`) produces the delivery file below it on its own (two-pass encoding at a computed bitrate).
  No cover? `FIT=1 bash scripts/06_encode.sh <work> <work>/ad-final.mp4` (target `MAXMB`, default 29). Don't do both — it would be compressed twice.

### 10) Loudness

```bash
bash scripts/06b_master.sh <work> <work>/ad-final.mp4 <work>/ad-master.mp4
```

- Raises the audio to -14 LUFS (the same level as the feed) and prints one line with the loudness and peak.
- A `<work>/bg-audio.mp3` exists? It is added and ducks automatically whenever they speak.
- The picture is copied without re-encoding.

### 11) Subtitle file

```bash
python3 scripts/09_srt.py <work> ad-master
```

- `.srt` for YouTube and LinkedIn.
- `.txt` = the full text of their speech, for the post caption.

---

## ⛔ Fixed rules

1. **A sound effect on a meaningful moment** (a number drops, something breaks, a scene changes) — not sprinkled on every word.
   15 events a minute at most, peak under -18 dBFS, and show them where you put them before export.
2. **Western digits always** (0-9).
3. **Colors from `theme.json` only** — no hard-coded color in code.
4. **Zero color grading on their picture:** no grade, tint, LUT or blur (`grade:false`) — unless explicitly asked.
   Colors are for cards and text only. The only exception: `"grade":"auto"` after they approve the light check.
5. **iPhone HDR → Apple's converter is mandatory.** `03_cut_zoom.py` detects it and builds `hdr2sdr.swift`.
   A naive conversion washes out the picture and they would call it "color grading".
6. **Correct the Whisper transcript** before the captions, and **never invent words they didn't say** — don't know? Generalize instead of guessing.
7. **No posting and no scheduling** — delivery is a file only.
8. **"Behind the person", "layers" and the cut styles once or twice per video** — more loses their effect. (Depth moments with `MV.person` are different — 2–3 per reel.)
   Every `build` or `stack` = the full list for its type (what you didn't mention is removed). And the front text is never written over the face.
9. **Call it "background audio", not "music".** The content is their decision, and you place it as `bg-audio.mp3` as it is.
10. **Invent new scenes every time.** The examples are a library of patterns, not a template.
11. **Any image, screen recording or logo keeps its original aspect ratio** — proportional scaling only. No squashing or cropping unless asked.
12. **Quran verbatim from the source — not one letter by hand:**
    - Copy it by machine from an API (`api.quran.com` → `text_imlaei`, or `api.alquran.cloud`).
    - Compare its letters against a second source before drawing.
    - The vocalized imlaei text reads more clearly than the Uthmani (the Uthmani `ٱلنَّبِيِّۦنَ` was read wrong). The Uthmani font: `Amiri Quran`.
    - Any text that is not a verse ("God Almighty said", the surah name) uses the normal theme font.
13. **Zoom-out = returning from a zoom-in, nothing else.** It never turns the frame into a card or goes smaller than the original.
14. **The hook has motion in the first second** — a quick gentle zoom-in, or icons rising from behind their back. A still first frame = a scroll.
15. **A pop-up word stays until its sentence ends** — not a half-second flash of text (at least 0.6 s, better: until the end of the sentence).
16. **Forbidden by default** — unless they ask for it by name:
    - Letter-by-letter typing (it breaks Arabic letters — animate word by word).
    - Glow, bounce, gradient on text, a purple → blue background.
    - Asked for a glow? On the full screen (`fillRect(0,0,W,H)`) — a limited rectangle shows edges.
    - Details → `references/motion-rules.md`
17. **A speaker whose slow style is deliberate** (Quran, a sermon, a reading): ask "Keep the pauses as they are?"
    Yes → `cut.json` → `"keep":[[0,duration]]`. Cutting here produces jumps.
18. **One element at a time, and show it.** A new scene or effect: build it alone, a frame sheet, then the next.
    A small request? Edit only that part, don't redo the skill from the start.

---

## ✅ Verify before delivery (mandatory)

**Before the full render** — a frame from **the middle of every scene** (not 6 random ones):

```bash
python3 scripts/32_midframes.py <work>
```

Look for: cut-off text, overlaps, a number not from `facts.md`, cut edges around the person, the order of "behind the person".
Fix, redo it, then render.

**0. Safe area and hook** — automatic, no eyes needed:

```bash
node scripts/08_safe_check.js <work> --shot
```

- Draws every moment twice in two colors in place of the video; whatever doesn't change is your drawing.
- Counts your texts inside the button zones and checks that the first caption comes within half a second.
- Exits with code 3 on a violation. `--shot` writes `safe.jpg` **only if it fails**.
- A frozen frame in transitions (`MV.frameAt`) counts as video, not text (6.0) — before that it gave a false alarm.
- The limits can be adjusted in `<work>/safe.json`.

**1. Sync** — transcribe the output and compare sentence starts with `caps.json`. The difference should be under 0.1 second:

```bash
ffmpeg -v error -i <work>/ad-final.mp4 -vn -ac 1 -ar 16000 -y <work>/fa.wav
python3 -m whisper <work>/fa.wav --language $(python3 scripts/_lang.py) --model small --output_format json --output_dir <work> --fp16 False --verbose False > <work>/whisper.log 2>&1
```

**2. Audio** — the last line of `06b_master.sh`: close to -14 LUFS, and the peak -1.5 dBTP or lower.

**3. Eyes** — one sheet of 6 frames from `ad-final.mp4`, actually looked at.
Beat effects? `beatfx-sheet.jpg` too (montage: `--sheet` · speech: `--check`).

**4. Size** — the delivery file under 30 MB. The cover handles it: longer than 90 s (or larger than `MAXMB`) → two passes at a computed bitrate
(the $1000 reel, 124 s: 1.72M → 27.9 MB with clear text).

---

## 💰 Saving tokens

Measured on 10 September: a 36-second video cost 3.1 million tokens.
41% was scattered terminal commands, and 8 preview images ate about 900,000 characters.

1. **One command per stage** — combine independent steps into one background command, and wait for its notification.
2. **One contact sheet per preview** (6 frames). Any other check by numbers, not by eye.
3. **Don't read a whole file:** `grep -n` for the function, `tail -5` for logs.
4. **References only when needed** — open `references/` only when the entry table sends you there.
5. **`theme.json` is saved per client** — the second video starts from it. Save `caps.json` and `cut.json` too.
6. **Short replies:** two lines and an image. ⛔ Show an image only for a visual question nothing else can answer.

---

## Delivery

Show the file with: the duration, how much silence was removed, the number of scenes, and the final loudness.
Deliver the `.srt` and `.txt` with it, and say you didn't post anything.

**🖼️ The cover = the first frame of every video — mandatory** (user's order, 3 October 2026):

```bash
python3 scripts/28_cover.py <work> "first line|*second line colored*" "small line" \
  [--photo me.png] [--x old.png] [--ok new.png] --first <work>/ad-master.mp4
```

- **The safe-square rule:** a reel is 9:16, but Instagram shows it on the profile at 4:5 (sometimes 1:1).
  Everything important — face, text, logos — sits inside a 1080×1080 square in the middle of the image (y 420–1500).
  The square is imaginary: no frame, no line.
- **The text is a short hook:** two lines, 5 words at most, about 9 characters per line — on the chest or a little below. `|` = new line, `*…*` = the accent color.
- **📏 Sizes that read on a phone:** the grid shrinks the cover to 12% → title ≥ 170 px, any text ≥ 110, logo ≥ 200, no handle. Details → `references/thumbnails.md`
- **The person's photo:** they have a cut-out photo (transparent background)? `--photo` — it's placed on a background in the video's own background color
  (or `--bg`), and the legs are cut as usual. Without it: a frame from the source.
- **🙂 The face (6.0):** without `--t` it picks a frame with **the speaker's face** biggest and clearest (the Mac face detector — not a b-roll shot with someone else).
  The text never covers the face: it detects the face and shrinks the cut-out (`--cut`/`--photo`) or raises the frame until the chin is 30 px above the top of the text.
  No Mac: it falls back to the clearest frame and prints a warning — check it's them, or set `--t`.
- **Two logos for a comparison story — not a rule:** only if the video is "from X to Y". `--x` = what they left (✕), `--ok` = the replacement (✓). They go in a row at the top of the square with the head below them.
- `--first` puts the cover in the video's first 0.1 s → `ad-master-cover.mp4` — this is the delivery file. (Longer than 90 s? It encodes in two passes under 29 MB on its own — 6.1)
- Show `cover_grid.jpg` (9:16 · 4:5 · 1:1 side by side) — make sure nothing is cut in the 1:1.
- Then `python3 scripts/34_phone_preview.py <work>/cover.jpg` — at its real size on a phone. Couldn't read it? Enlarge or shorten.
- Want a YouTube thumbnail too? → the `thumbnail-video` skill (or `scripts/33_thumb.py`).
- Instagram: choose the first frame as the cover. TikTok: the same.

Script and file map → `references/script-map.md`

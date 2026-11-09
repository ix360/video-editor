# 🎬 Video Editor — a video-editing plugin for Claude Code

**Talk to the camera… and get a vertical reel ready to post.**
It removes the silences, writes captions that follow your mouth, and draws motion graphics in your own colors — no editing software — from your phone or your computer.

Free · works from the **phone** and the computer · captions and transcription in **10 languages** (English, العربية, Français, Español, Português, Deutsch, Türkçe, اردو, فارسی, Bahasa Indonesia)

[**Start here — install in a minute ↓**](#start)

---

## 🌐 Pick your language

The first time, Claude asks which language you want and remembers it. Its replies, the voice **transcription** and the **captions** all follow your choice. To change it, say "change language". English is the default.
The taste page that opens in your browser also has a **language switcher at the top** (7 languages so far).
Details: [`language.md`](video-editor/references/language.md).

---

## 🆕 What's new

### Free stock · voiceover · images and video from Google
- **Free stock** (`38_stock.py`): search and download from Pexels, Pixabay and Unsplash, with the credit saved → [`stock.md`](video-editor/references/stock.md).
- **The `voiceover-video` skill:** checks that ElevenLabs is connected (and shows you the Connect button if not), lists your voices, and generates the voiceover — in your cloned voice, or from a sample you record in the browser → [`voiceover.md`](video-editor/references/voiceover.md).
- **Images from AI Studio** with a `GEMINI_API_KEY` (cheaper than fal) + **Google Flow in the browser** for video clips with no API cost (experimental) → [`google-flow.md`](video-editor/references/google-flow.md).
- **You choose once:** (A) the Google API (an AI Studio key) or (B) your own Google Flow subscription through Chrome. A **simple check** then verifies ElevenLabs, the Chrome extension and Flow access, and if Flow won't open it brings Chrome forward so you can sign in → [`setup-check.md`](video-editor/references/setup-check.md).
- Always cheapest first: stock → Gemini → Flow → fal.

### 6.3 — "Explain how X works": any device becomes a machine that draws itself and runs
<p align="center"><img src="_pkg/machine.gif" width="70%" alt="A hair dryer and a microwave drawn in ink, then running, with numbered steps underneath"></p>

Tell Claude one sentence: **"Explain how an air conditioner works."**
- It finds the facts from a **reliable source** first; every sentence on screen has a source.
- It draws the device **cut away** on a board, line by line in ink.
- Then it **runs it** in front of you: the fan spins, the wire glows red, the waves bounce…
- With **2–3 steps** underneath.

Great for teachers and any "how does … work?" — an AC, a fridge, a car, a heart…

<details><summary><b>Earlier in 6.2</b> — fixed frame · 3D slide wall · 3D logo on a talking reel · "chunk" captions</summary>

<p align="center"><img src="_pkg/stage-wall.jpg" width="100%" alt="A motion film with a fixed frame: a 3D slide wall"></p>

| New | Say |
|---|---|
| A motion film with a fixed title on top while the content changes below (it looks like one shot) | "make it with a fixed frame" |
| The camera flies over 3D cards and one card drops to become the first scene | "I want a slide wall" |
| A logo with thickness, shine and shadow on a talking reel | "make the logo 3D" |
| Captions in short chunks up to 4 words, with the spoken word colored | "chunk captions" |

These happen **only when you ask** — not in every video.
</details>

---

<a id="start"></a>

## 🚀 Start here — 3 steps

**① Install the plugin once from claude.ai · ② open a new chat (Opus 5.5 · Max) · ③ attach a video and write one sentence, e.g. "edit this clip".**

Copy the marketplace name (the copy button on the right of the box) and paste it into **Add marketplace**:

```
ix360/video-editor
```

### 1️⃣ Install the plugin — once only (a minute)

**The same for everyone** — phone, computer, the desktop app. No terminal and no file download. You install it once from **claude.ai** and it shows up on the web, desktop and phone, and updates itself.

**1.** Open **claude.ai** → click your name at the bottom → **Settings**

<p align="center"><img src="_pkg/step-1-settings.jpg" alt="Settings from the menu under your name" width="360"></p>

**2.** Under **Customize** → **Plugins** → **Add** → **Add marketplace**

<p align="center"><img src="_pkg/step-2-plugins.jpg" alt="Plugins under Customize" width="360"></p>

<p align="center"><img src="_pkg/step-3-add-marketplace.jpg" alt="Add, then Add marketplace" width="360"></p>

**3.** Paste this and add it:

```
ix360/video-editor
```

**4.** **video-editor** appears — add it.

**5.** Then **Add** → **Manage marketplaces** → **⋮** → turn on **Sync automatically** (so every update reaches you by itself).

<p align="center"><img src="_pkg/step-5-manage.jpg" alt="Add, then Manage marketplaces" width="360"></p>

<p align="center"><img src="_pkg/step-6-sync.jpg" alt="The three dots, then Sync automatically" width="360"></p>

> ✅ **Check it was added:** under **Plugins** you see **video-editor** in the list. Not there? Repeat step 3.

### 2️⃣ Open a new chat

From the model menu next to the send button → **Opus 5.5** → **Effort** → **Max** (strongest result).

### 3️⃣ Attach the video and write a sentence

For example: **"Edit this clip"** or **"Turn the video into a reel"**. The first time, Claude asks your language and shows a [taste page](#taste) (your colors, font and moves), then produces the reel. Want a change? Write it in the same chat.

### 📱 From the phone — no laptop

<p align="center"><img src="_pkg/mobile-banner.jpg" alt="Editing from the phone with no laptop: attach the video in the Claude app, lock the phone, and the reel waits in the same chat" width="100%"></p>

The same three steps from the **Claude phone app**: attach the video, write your request, and **lock the phone** — the edit runs in Claude's cloud and the reel waits in the same chat.

> ⏱️ The cloud is slower than a computer (cutting a person out of the background ≈ 18 minutes for a 40-second video), so let it run and come back. The attachment size limit depends on the app.

> 🧑‍💻 **Use the terminal, or want to download the file yourself?** [Other install methods below](#install).

---

## 🗣️ What you can do — everything with one sentence

No commands and no settings. Write Claude **the sentence under each item**, and it does the rest.

<table width="100%"><tr>
<td width="20%" align="center" valign="top"><img src="_pkg/talk.gif" width="100%"><br><b>🎙️ A reel from a talking video</b><br><sub>removes silences · captions follow your mouth · motion from the meaning of your speech</sub><br><b>"Edit this clip"</b></td>
<td width="20%" align="center" valign="top"><img src="_pkg/machine.gif" width="100%"><br><b>⚙️ Explain any device as a machine</b> 🆕<br><sub>drawn in ink, then running · facts from a source</sub><br><b>"Explain how an AC works"</b></td>
<td width="20%" align="center" valign="top"><img src="_pkg/motion.gif" width="100%"><br><b>✨ A motion film from text</b><br><sub>3D at 60 fps · no filming, no person</sub><br><b>"Make a motion video from this text"</b></td>
<td width="20%" align="center" valign="top"><img src="_pkg/add-marketplace.gif" width="100%"><br><b>🎥 One-take — a single shot, no cuts</b><br><sub>zoom in until the button swallows the screen… then zoom out to reveal</sub><br><b>"Make a one-take video about …"</b></td>
<td width="20%" align="center" valign="top"><img src="_pkg/montage.gif" width="100%"><br><b>🎞️ Montage of clips with no speech</b><br><sub>a folder of clips → a reel on the beat</sub><br><b>"Make a montage from these clips"</b></td>
</tr></table>

<table width="100%"><tr>
<td width="20%" align="center" valign="top"><img src="_pkg/f_web.png" width="100%"><br><b>📱 Explain a website or app</b><br><sub>real screenshots inside a 3D iPhone or MacBook</sub><br><b>"Explain this website in a video: link"</b></td>
<td width="20%" align="center" valign="top"><img src="_pkg/f_wide.png" width="100%"><br><b>🎧 Podcasts and interviews</b><br><sub>two cameras → reels with a written hook · the full 16:9 episode</sub><br><b>"Make reels from the episode"</b></td>
<td width="20%" align="center" valign="top"><img src="_pkg/cover_reel.jpg" width="100%"><br><b>🖼️ Covers and thumbnails that read on a phone</b><br><sub>the reel cover is the first frame · a YouTube thumbnail with three ideas</sub><br><b>"Make a cover" · "YouTube thumbnail"</b></td>
<td width="20%" align="center" valign="top"><img src="_pkg/timeline.jpg" width="100%"><br><b>🎚️ Edit by hand</b><br><sub>a timeline from the computer or phone · edits cost no tokens</sub><br><b>"Open the studio"</b></td>
<td width="20%" align="center" valign="top"><img src="_pkg/capcut-timeline.jpg" width="100%"><br><b>✂️ A CapCut project</b><br><sub>everything is a piece you can edit: captions, voice, effects, motion</sub><br><b>"Make it in CapCut"</b></td>
</tr></table>

<details><summary><b>CapCut — how it works</b></summary>

**How it works (3 steps):**
1. Open CapCut, create an **empty new project** and name it, then **quit CapCut completely** (Cmd+Q) — if it's open it overwrites the work.
2. Tell Claude **"make it in CapCut"** and give it the video. It shows you the motion shots before it continues.
3. It says "done" → open CapCut and enter the project; everything in it is editable.

> It works from **Claude on the computer** (the desktop app or Claude Code) because it writes the project files on your machine — not from the phone. And you need **CapCut Desktop** (Mac or Windows), not the phone app.

<sub>CapCut is a trademark of ByteDance — this plugin has no official relationship with it.</sub>
</details>

### More sentences that help

| You want | Say |
|---|---|
| Remove sentences from the video | "Remove 5 and 8" (after it prints your speech numbered) · "Bring them back" |
| A theme from images you like | Send the images + "I want a style like this" |
| See the moves and choose | "Show me the move bank" |
| Change your colors and font | "Change my settings" |
| Use a generation platform you have (fal · Higgsfield · ElevenLabs) | "Use fal for the b-roll" |
| A voiceover in your own voice | "Make a voiceover with my voice" |
| Free stock footage | "Find stock footage of coffee being poured" |

<a id="taste"></a>

## 🧭 It learns your taste — first time only
<p align="center"><img src="_pkg/onboarding.jpg" width="80%"></p>

A small page where you pick your colors, font, caption style, pace and voice — or write what you want and skip it. Every video after that follows your taste.

## 🎨 It doesn't repeat itself — 100 moves and 17 styles

<p align="center"><img src="_pkg/moves.gif" width="49%" alt="Moves from the bank"> <img src="_pkg/styles-17.gif" width="49%" alt="17 styles"></p>

Before each video it picks a **palette**: 3 core moves the video revolves around, and one style for the whole video (paper cutout, documentary, knockout, news explainer…). It keeps a log, so the next video comes out different. The bank is a base, not a limit — the strongest moments are invented from your sentence.

<details><summary><b>All 100</b> — each tile is the move's number in the bank; the new ones (62–100) have a frame and a black number</summary>
<p align="center"><img src="_pkg/moves-all-100.gif" width="100%" alt="The move bank: 100 numbered moves from 1 to 100"></p>
</details>

---

## 📚 Details (click to open)

<details><summary><b>🧰 Other install methods — for advanced users</b> (terminal · plugin file)</summary>

<a id="install"></a>

> Most people are fine with [Start here](#start). These are for the terminal, or if you want the plugin file by hand.

**The plugin = 6 skills in one package** (reel · motion · podcast · montage · cover and thumbnail · voiceover).

> ☝️ **Pick one method only** — installing it more than one way gives you duplicate copies of the same skills. Have more than one? Remove the extra copies from **Customize → Plugins**.

> 🏷️ **Two names not to mix up:** the marketplace `ix360/video-editor` (named `ix360-plugins`) · the plugin `video-editor`. The add command takes the **repository** name (`ix360/video-editor`), and the install command takes **plugin@marketplace** (`video-editor@ix360-plugins`).

### Download the file and upload it

1. [**Download the plugin**](https://github.com/ix360/video-editor/releases/latest/download/video-editor.plugin) (the file `video-editor.plugin`)
2. Open the **Claude** app → **Customize** → **Plugins** → **Upload plugin** → choose the file

> ⚠️ This method **doesn't update itself** — download and upload each new version again.

### From the terminal

**You need Claude Code installed.** Open the terminal — **Terminal** on Mac or **PowerShell** on Windows (not the Code tab in the desktop app) — and type `claude --version`. A version number? Continue. `command not found: claude`? You don't have Claude Code — **use [Start here](#start)**, you need nothing else.

Paste the commands **one at a time** (the command → Enter → wait):

```
claude plugin marketplace add ix360/video-editor
```

```
claude plugin marketplace list
```

```
claude plugin install video-editor@ix360-plugins
```

- **Check after the first command:** the second (`marketplace list`) **must show `ix360-plugins`**. It didn't? Run the first again (the connection may have dropped), then come back to the list.
- **Got `Failed to add marketplace … extraKnownMarketplaces`?** Don't assume "it was already added". Run `claude plugin marketplace list` — if `ix360-plugins` isn't there, the marketplace really is missing: run the first command again.
- **Restart `claude`** after installing, otherwise the skills don't appear in the session.

Then **turn on auto-update**: in a normal terminal type `claude` → Enter, then:

```
/plugin  →  Marketplaces  →  ix360-plugins  →  Enable auto-update
```

> ℹ️ The `/plugin` command is interactive and works **in a regular terminal only** — not inside the desktop app (the Code tab). And "Enable auto-update" only appears if `marketplace list` shows `ix360-plugins`.

<p align="center"><img src="_pkg/install.gif" alt="The steps inside Claude Code in the terminal" width="100%"></p>

> 🔁 **Want the latest version now?** In the terminal: `claude plugin update video-editor@ix360-plugins`
>
> 🧹 **Installed an older version as a skill (a `.skill` file)?** Remove it so it doesn't duplicate — the plugin has everything.
>
> 📦 **Want the reel skill alone?** [Download `video-editor.skill`](https://github.com/ix360/video-editor/releases/latest/download/video-editor.skill) → double-click → approve. (One skill with all the modes, but without the plugin's other skills.)
>
> 🤖 **Codex and any agent that runs commands:** it reads `SKILL.md` and the `references/` folder as instructions and runs the same scripts ([`any-environment.md`](video-editor/references/any-environment.md)) — *not yet tested on Codex itself.*

</details>

<details><summary><b>🔧 Requirements and privacy</b></summary>

**Requirements:** the plugin downloads these itself after your permission: **ffmpeg** (cutting and audio) · **Whisper** (word-timed transcription) · **Chrome** (drawing). Mac and Windows.

**Privacy:** on a computer everything stays on your machine — **your video isn't uploaded to any server.** From the phone, the video goes to Claude's cloud under your account (that's what edits it). The exceptions are optional and you switch them on (AI-generated scenes, ElevenLabs voiceover, Google Flow).

</details>

<details><summary><b>💬 A keyword at the end of the reel → a link by DM</b> (optional)</summary>

Episode reels end with "write [keyword] and the full episode reaches you". To make the reply automatic: [Zorcha](https://zorcha.com) — the automation is free, and controlling it from Claude (MCP) needs a subscription. Details: [`keyword-automation.md`](video-editor/references/keyword-automation.md).

</details>

<details><summary><b>📜 Release notes</b></summary>

### Newest — language, stock, voiceover, Google assets
- 10 languages, chosen once and saved (`00_onboard.py lang set <code>`); transcription, captions and Claude's replies follow it (`scripts/_lang.py`).
- Free stock search, a Gemini image backend, Google Flow in the browser, and the ElevenLabs `voiceover-video` skill.
- A one-time setup check (`00_check.py` + `setup-check.md`).
- The marketplace is now `ix360/video-editor`, and the plugin is named `video-editor`.

### 6.3 — "Explain how X works"
- **A new motion mode:** any device becomes a cut-away machine drawn in ink line by line, then it runs (rotation, glow, waves, steam) with 2–3 steps underneath.
- **Facts before drawing:** every sentence on screen has a source and a quote in `facts.md` — anything without a source appears in the drawing with no caption.
- **The user's sentence is typed in a bubble** above the machine (`ask`).
- A working example: `motion/examples/machine/` (hair dryer + microwave) · the guide: [`machine-explainer.md`](video-editor/references/machine-explainer.md).
- The isometric drawing tools come from the [Anatomy](https://github.com/wheresryan22/anatomy) project (MIT licence).

### 6.2.1 — lessons from a "$1000 a day" reel
- **`chunk` caption style:** pieces up to 4 words in a pill, the spoken word in the accent color with no jumping (and manual breaks with `CHUNK_BREAK`).
- **Numbers don't flip in Arabic:** "25–30" used to come out "30–25" — the engine now isolates them in captions and scenes.
- **A clean return** from "head outside the rectangle" (`tr` per scene) under a zoom that covers the screen, and `headbox` is always written (it used to fail silently).
- **Whisper hallucination check** and repair by cutting with no context (`02a_whisper_check.py`).
- **A long reel under 30 MB:** two-pass encoding at a computed bitrate.
- **An element doesn't vanish with the last word:** it stays a moment and leaves gently, and the caption stays after it.

### 6.2 — one-take motion and real 3D
- **A fixed frame** (`MOTION.stage`), a **3D slide wall** (`ctx.slideWall`), real **motion blur**, and a real **3D logo** on a talking reel (`41_logo3d.js` + `MV.overlay`) — only when you ask for them. Working example: `motion/examples/stage-wall/`.

### 6.1 — the style bank
- **17 styles** for the whole video (`references/styles.md`): knockout · UI glass · news explainer · paper cutout · documentary · magazine · Swiss · hand-drawn · terminal · risograph · newspaper · blueprint · VHS · brutalist · product studio · cartoon sticker · tool card.
- **The video's palette chooses the style** along with the moves (`35_moves.py plan` → `style`), and a third of videos come out as a **blend** of two styles. `--style paperCut` or `--style none` if you want.

### 6.0 — lessons from the Bobian reel
- **Deep motion from the first draft:** it plans 2–3 "depth moments" before drawing — an element passing behind your head, a wave moving with your real voice (`37_env.py`, `MV.env`), a dot map behind you, a 3D orbit, a shape from the client's identity, and a one-take entrance with the logo.
- **Smarter "layers":** choose how many words above the head and how many behind (`"stack":{"above":2,"behind":1}`).
- **The cover picks your face**, and the text never covers it. Zoom is locked per clip.

### Earlier
- **5.0** a 100-move bank (including Arabic-specific moves and a verse with calm reading in the Amiri Quran font) · **4.7** 61 moves · **4.5** the move bank + the "Moves" section of the intro page · **4.4** CapCut mode, one-take mode, and a library of examples from people · **4.2–4.1** cover and thumbnail skill · **4.0** four skills on one engine, with an automated test before every release.
- **3.9** theme from reference images, a full 16:9 podcast, website/app explainers, smart audio cleanup · **3.8** 3D motion explainers, the podcast hook, "layers", beat effects · **3.5** a full episode → reels · **3.4** the studio (a timeline by hand) · **3.2** generated scenes · **3.0** it updates itself · **2.9** screen recording in a phone frame · **2.8** Windows (thanks to [@thefhiter](https://github.com/thefhiter)) · **2.7** the podcast.

</details>

<details><summary><b>🛠️ For developers</b></summary>

A map of all the scripts and files: [`references/script-map.md`](video-editor/references/script-map.md) · instructions: [`SKILL.md`](video-editor/SKILL.md) · the other skills: [`motion-video`](motion-video/SKILL.md) · [`podcast-video`](podcast-video/SKILL.md) · [`montage-video`](montage-video/SKILL.md) · [`thumbnail-video`](thumbnail-video/SKILL.md) · [`voiceover-video`](voiceover-video/SKILL.md)

Build the release files: `bash tools/build-release.sh` (after committing) → `dist/video-editor.plugin` + `dist/video-editor.skill`.

**Note:** the skill entry files and the start/setup guides are in English; the deeper reference docs in `video-editor/references/` are still largely in Arabic (Gulf dialect), and the engine's example scenes show Arabic text. Claude reads them fine and answers the user in the language they chose.

</details>


## Licence
MIT — use it, change it and share it freely.

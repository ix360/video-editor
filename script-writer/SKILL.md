---
name: script-writer
description: Writes the script for a short video — a direct hook in the first seconds, a story that keeps people watching, and one clear call to action — with a shot list saying what the viewer sees on every line (person, graphic, photo, clip). Use when the user says "write a script", "write me a hook", "script for a reel", "script for an ad", "improve my script", "check my script", "storytelling script", "call to action", or "اكتب لي سكربت"، "سكربت ريل"، "هوك"، "سكربت إعلان"، "حسّن السكربت", "écris un script", "guion para un reel". Output is script.md that the video skills (video-editor, motion-video, voiceover-video) then use.
---

# Script writer — hook, story, call to action

The method lives in `${CLAUDE_SKILL_DIR}/../video-editor/references/script-writing.md`. **Read it and follow it.** All other scripts and references are in `${CLAUDE_SKILL_DIR}/../video-editor`.

## 🌐 Language
Talk to the user in their saved chat language (`python3 scripts/_lang.py`, see `references/language.md`; ask once if none is saved). Write the **script** in the video's language (`python3 scripts/_lang.py video`) — it can differ.

## Steps
0. **Pick the mode from their first words** — *rhythm* (default) or *yapping* (talk to camera, bullets, no manufactured hook) — see the reference's "Two modes" and §8.
1. **Brief, in one message** (§0 of the reference): topic · goal · audience · platform · length · on camera or voice only · the one action wanted at the end. Guess what they leave out and say your reading back in one sentence — don't interview them.
2. **Three hooks first**, each from a different formula (26 of them, §1) and built on one human need; also write the **screen hook** (≤ 6 words, shown in the first frame). They pick one. The first word must already carry the point — no greeting, no name, no "today".
3. **The body** with the skeleton that fits the goal (§1 Part 2) — in rhythm mode: lead past second 10, then exactly two body+loop cycles, then a bridge — and **one** call to action that serves the same need as the hook (Part 3).
4. **The shot list** (§3): next to every line, what the viewer sees — `person`, `graphic`, `image`, `clip`, `screen` — and an asset prompt for each `image`/`clip`.
5. **Run the checklist silently** (§5), fix what fails, then show the script in the chat — the whole of it, not a path.
6. Save `<work>/script.md` in the format of §4, and the call to action as the end-card text: `theme.json → outro` for a reel/podcast; for a motion film it is the last scene.

If the user already has a script: don't rewrite it — run the checklist and report only what fails (§6).

## ⛔ Rules
- One idea, one CTA, per video. Never both a list and a story in the hook.
- Never invent a number, a name or a result. Unsure → mark `[source?]` and ask.
- Spoken text is clean: no stage directions, no emoji, numbers written the way the voice should say them.
- This skill only writes. It doesn't render, post or schedule anything.

## Credit
The rhythm structure, the six-needs hook method, the 26 hook formulas and the yapping mode are adapted (translated and made dialect-neutral) from `reels-rhythm-script` in [majedphotos/majed-plugins](https://github.com/majedphotos/majed-plugins/tree/main/script), MIT-licensed, Copyright (c) 2026 Majed Alzaabi — see the repository `LICENSE`.

---
name: script-writer
description: Writes the script for a short video — a direct hook in the first seconds, a story that keeps people watching, and one clear call to action — with a shot list saying what the viewer sees on every line (person, graphic, photo, clip). Use when the user says "write a script", "write me a hook", "script for a reel", "script for an ad", "improve my script", "check my script", "storytelling script", "call to action", or "اكتب لي سكربت"، "سكربت ريل"، "هوك"، "سكربت إعلان"، "حسّن السكربت", "écris un script", "guion para un reel". Output is script.md that the video skills (video-editor, motion-video, voiceover-video) then use.
---

# Script writer — hook, story, call to action

The method lives in `${CLAUDE_SKILL_DIR}/../video-editor/references/script-writing.md`. **Read it and follow it.** All other scripts and references are in `${CLAUDE_SKILL_DIR}/../video-editor`.

## 🌐 Language
Write the script in the user's saved language (`python3 scripts/_lang.py`, see `references/language.md`); ask once if none is saved. Talk to them in it too.

## Steps
1. **Brief, in one message** (§0 of the reference): topic · goal · audience · platform · length · on camera or voice only · the one action wanted at the end. Guess what they leave out and say your reading back in one sentence — don't interview them.
2. **Three hooks first**, each from a different formula (§1), and let them pick. The first word must already carry the point — no greeting, no name, no "today".
3. **The body** with the skeleton that fits the goal (§1 Part 2) and **one** call to action (Part 3).
4. **The shot list** (§3): next to every line, what the viewer sees — `person`, `graphic`, `image`, `clip`, `screen` — and an asset prompt for each `image`/`clip`.
5. **Run the checklist silently** (§5), fix what fails, then show the script in the chat — the whole of it, not a path.
6. Save `<work>/script.md` in the format of §4, and the call to action as the end card text (`theme.json → outro`).

If the user already has a script: don't rewrite it — run the checklist and report only what fails (§6).

## ⛔ Rules
- One idea, one CTA, per video. Never both a list and a story in the hook.
- Never invent a number, a name or a result. Unsure → mark `[source?]` and ask.
- Spoken text is clean: no stage directions, no emoji, numbers written the way the voice should say them.
- This skill only writes. It doesn't render, post or schedule anything.

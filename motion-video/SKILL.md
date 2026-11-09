---
name: motion-video
description: A 3D motion-graphics film with no person and no filming — from a text, an idea or a script, with their own voice or a generated one, 60 fps. Also explains a website or app with real screenshots inside a 3D iPhone or MacBook, and explains any device as a cut-away machine that draws itself in ink and then runs ("explain how an air conditioner works"). Use when the user says "motion video", "make a video from this text", "explain this website in a video", "explain the app", "iPhone demo", "explain how X works", or "فيديو موشن"، "شرح بالموشن"، "سو فيديو من هالنص"، "اشرح لي شلون يشتغل"، "اشرح الجهاز كآلة". Not for editing a talking video (use video-editor).
---

# Motion explainer — a film from text, no filming

**The engine is shared** with the reel skill. All `scripts/`, `references/` and `motion/` are here:
`${CLAUDE_SKILL_DIR}/../video-editor`

## Steps

1. **Start:** read `references/start.md` and do it (tools, taste, identity).
2. **The mode:** read `references/motion-mode.md` and do it — all its rules are mandatory.
3. **Commands:** `motion/README.md`, and the scene-writer's guide `motion/ENGINE-API.md`.
4. **Explaining a website or app:** `references/web-app-explainer.md`
5. **One-take (the whole video is a single shot, no cuts):** `references/one-take.md` + the working example `motion/examples/one-take/`. For an app or tool ad, steps, or an idea with scenes inside scenes.
5b. **"Explain how X works" (any device as a machine that draws itself and runs):** `references/machine-explainer.md` + the working example `motion/examples/machine/` (a hair dryer + a microwave). Facts from a primary source first, then the drawing.
6. **Examples from people (inspiration, not copying):** `references/examples.md`
6b. **A fixed frame + a 3D slide wall — only when the user asks** (not the default): section "One shot with a fixed frame" in `references/motion-mode.md`, and the example `motion/examples/stage-wall/`. Motion blur (`motionBlur`) suits any film with fast movement.
7. **The move bank — a palette for every video (mandatory):** `references/moves.md`. Before the first scene: `python3 scripts/35_moves.py plan --title "…"` → 3 core moves the film revolves around + accents for special moments, called with `ctx.FX.<id>`.
8. **Footage or images for scenes:** free stock → `references/stock.md`; generated → `references/gen-scenes.md` / `references/google-flow.md`; a voiceover → the `voiceover-video` skill.

## 🌐 Language

The user picks their language once — `references/language.md` in the reel skill; the code comes from `python3 scripts/_lang.py`. Speak to them in it. On-screen text is in the film's language.

## ⛔ How you treat the user

- **You prepare things, not them.** Never hand them commands to run, and never ask "do you have X?" — check yourself.
- **No jargon,** and say where you are at every step and how long it takes.
- **One thing at a time,** and show a frame after each important stage.
- ⛔ Never ask "which mode do you want?" — say in one sentence what you understood and carry on.

## Fixed rules

- Western digits (1 2 3).
- Colors from `theme.json` only.
- No number or name on screen unless it is in `facts.md` → `references/motion-rules.md`
- No posting or scheduling — delivery is a file only.
- It runs on their machine through Claude Code. In the chat: only the script, the plan and the theme.

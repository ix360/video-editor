# Video Editor — instructions for any coding agent (Hermes, Codex, Cursor, Claude Code…)

This repository is a set of **Agent Skills** (`SKILL.md` folders) plus one shared engine. Start with `start/SKILL.md`: it is the orchestrator for the whole workflow (one-time setup → brief → script → voice → look → footage → build → deliver).

Layout (keep the skill folders as siblings under one parent):
- `start/`, `script-writer/`, `motion-video/`, `video-editor/`, `podcast-video/`, `montage-video/`, `thumbnail-video/`, `voiceover-video/` — each has a `SKILL.md`.
- `video-editor/` is also the engine: `scripts/`, `references/`, `motion/`. Every `scripts/…` path in the skills is relative to it.

First actions:
1. `python3 video-editor/scripts/42_start.py ready` — if `configured` is false, follow `start/SKILL.md` stage 0 (it sets up only what is missing, once).
2. Read `start/SKILL.md`, section "Running outside Claude Code" for the tool mapping (ElevenLabs via `39_voice_sample.py voices|speak`, Flow via any browser tool, plain-text questions).
3. Never skip stages: `node video-editor/motion/render.js <project> all` refuses to run until the move plan exists and `python3 video-editor/scripts/42_start.py audit <project>` passes.

Requirements: Python 3, Node, ffmpeg, Google Chrome (`bash video-editor/scripts/00_setup.sh --install` installs the rest). The workflow never posts or publishes anything: its output is a file.

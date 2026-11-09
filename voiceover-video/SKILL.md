---
name: voiceover-video
description: Voiceover for videos with ElevenLabs — lists the user's own voices (including their cloned voice), generates the narration from a script, or uses/clones the user's own voice from an mp3 they attach. Connects ElevenLabs if it is not connected yet. Use when the user says "voiceover", "narrate this", "read this script", "use my voice", "clone my voice", "use my own recording", "تعليق صوتي", "سو لي فويس أوفر", "بصوتي", "استنسخ صوتي", "بصوتي من ملف", "voix off", "locución". The output is an audio file that the video skills (video-editor, motion-video) then cut, caption and mix.
---

# Voiceover — your voice, via ElevenLabs

The engine is shared with the reel skill: all `scripts/` and `references/` live in
`${CLAUDE_SKILL_DIR}/../video-editor` (the `video-editor` folder that sits next to this skill's folder; if your agent runtime does not set `CLAUDE_SKILL_DIR`, use the folder that contains this SKILL.md).

## 🌐 Language
Work in the user's saved language (`python3 scripts/_lang.py`, see `references/language.md`). Ask once if none is saved.

## Steps
1. **Read `references/voiceover.md` and follow it.** It covers: checking the ElevenLabs connector (and showing the Connect button if it is missing), listing the user's voices, the two ways to get *their* voice (pick an existing clone, or attach an mp3 of themselves), estimating the cost, generating one take, downloading the audio and handing it to the video pipeline.
2. The audio file becomes `<work>/vo.mp3`; the normal steps (transcribe → captions → render) run on it. For a video with no person on screen use the "voice only" recipe in `references/onboarding.md` (generated voice section) or `motion-video`.

## ⛔ Rules
- **Never generate before pricing it:** call the generate tool with `estimate_only` first and tell the user the credits. One take by default (`generations_count: 1`); never call generate twice to "retry".
- **A `voice_id` only comes from the voice list or the user** — never from memory.
- **Never clone a voice that isn't the user's own** (or someone who clearly consented). An attached sample must be of the person at the keyboard.
- Never ask for, print or store the ElevenLabs API key in chat; if needed it goes in the user's `.env`.
- You do the setup, not the user: no command lists. Say where we are in one line each step.

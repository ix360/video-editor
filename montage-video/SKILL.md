---
name: montage-video
description: Beat-synced montage of clips with no speech — a folder of clips (café, table, product, place, event) becomes one 9:16 video that picks the best moment of each clip and cuts on the audio beats. Use when the user says "make a montage from these clips", "cut these clips to the music", "edit on the beat", or "مونتاج من هالمقاطع"، "ركّب المقاطع على الأغنية"، "مونتاج على الإيقاع", or sends a folder of clips without speech. Not for a talking video (use video-editor).
---

# Montage of clips with no speech

**The engine is shared** with the reel skill. All `scripts/` and `references/` are here:
`${CLAUDE_SKILL_DIR}/../video-editor` (the `video-editor` folder that sits next to this skill's folder; if your agent runtime does not set `CLAUDE_SKILL_DIR`, use the folder that contains this SKILL.md)

## Steps

1. **Tools:** only step 0 of `references/start.md`.
   ⛔ No color or logo questions — a montage has no text at all.
2. **The mode:** read `references/montage.md` and do it.
3. **Effects on the beat** (zoom, shake, flash, wipe) → `references/beat-fx.md`
4. **Find a shot by meaning** ("coffee being poured", "a close-up of the product") → `references/find-shots.md`
   Free stock to fill gaps → `references/stock.md`

## 🌐 Language

The user picks their language once — `references/language.md` in the reel skill; the code comes from `python3 scripts/_lang.py`. Speak to them in it.

## ⛔ How you treat the user

- You need one thing from them: **the folder of clips.**
- **You prepare things, not them.** No jargon, and say where you are and how long it takes.
- Show a numbered shot sheet before assembling.

## Fixed rules

- ⛔ No transcript, no captions, no drawn scenes.
- Call it "background audio", not "music" — the content is their decision.
- Zero color grading unless explicitly asked.
- No posting or scheduling — delivery is a file only.

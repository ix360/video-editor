---
name: podcast-video
description: Edits podcasts and interviews — two or more cameras of the same session into 9:16 reels with captions and a written hook, or the full 16:9 episode for YouTube, or a one-hour episode into several reels. Use when the user says "podcast", "interview", "two cameras", "full episode widescreen", "YouTube episode", "reels from the episode", or "بودكاست"، "كاميرتين"، "الحلقة كاملة بالعرض"، "ريلات من الحلقة"، or sends multi-camera files or a long episode. Not for a single talking video (use video-editor).
---

# Podcasts and interviews

**The engine is shared** with the reel skill. All `scripts/` and `references/` are here:
`${CLAUDE_SKILL_DIR}/../video-editor` (the `video-editor` folder that sits next to this skill's folder; if your agent runtime does not set `CLAUDE_SKILL_DIR`, use the folder that contains this SKILL.md)

## Steps

1. **Start:** read `references/start.md` and do it (tools, taste, identity).
2. **Pick the path from the input** — without asking:

| Input | Path | Read |
|---|---|---|
| Two or more cameras of the same session | Vertical reels (default) | `references/podcast.md` |
| They said "full episode", "YouTube" or "widescreen" | Full 16:9 episode | `references/podcast.md` (section "Full episode, widescreen") |
| A long episode (an hour) → several reels | Quick transcript → proposals → cut | `references/landscape.md` (section "Full episode") |

3. **🪝 Every reel from an episode or interview starts with a written hook — mandatory** → `references/podcast-hook.md`
   - In multi-camera mode, apply it **before** `15_podcast.py plan`.
4. **A reel from a single piece:** continue with steps 5–11 of the reel skill:
   `${CLAUDE_SKILL_DIR}/../video-editor/SKILL.md`
5. **Every seam between two pieces is checked** (`19_seam_check.py`) — mandatory.
6. Podcast extras → `references/podcast-upgrades.md`
7. **Closing keyword + the episode link by DM (automation):** change `theme.json → outro` to a card with the episode's keyword → `references/keyword-automation.md`
8. **How to work on each new episode:**
   - **The chat is for decisions:** transcribe the episode and give them a **numbered proposal sheet** (hook + start/end + why it works); they choose by number. Don't cut before they choose.
   - **After the edit — the review page (mandatory for 2+ items):** all reels and the carousel on one page with notes, approval and download → `references/review-page.md`. Later changes come from their notes on the page ("see the notes").
   - **One "setup" per episode:** a keyword + the episode link + an end card + one automation on "any post" — the same for all the episode's reels.
   - **The carousel from the episode:** the guest's or speaker's photo on the cover only, the rest of the slides from cut-out photos or elements — and show a preview grid before export.

## 🌐 Language

The user picks their language once — `references/language.md` in the reel skill; the code comes from `python3 scripts/_lang.py`. Speak to them in it.

## ⛔ How you treat the user

- **You prepare things, not them.** Never hand them commands to run.
- **No jargon,** and say where you are at each step and how long it takes.
- **One thing at a time,** and show a frame sheet after each important stage.

## Fixed rules

- A caption is never written over the speaker's face.
- Western digits, and colors from `theme.json` only.
- Zero color grading on the picture unless explicitly asked.
- Never invent words they didn't say, and no posting or scheduling — delivery is a file only.
- Mac only for faces and person cut-out (the Vision library).

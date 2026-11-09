---
name: thumbnail-video
description: Designs the reel cover (the first frame of the video, everything important inside a 1:1 square so it reads in the profile grid) and a 16:9 YouTube thumbnail with three ideas — at sizes that are readable on a phone screen. Use when the user says "make a cover", "reel cover", "thumbnail", "YouTube thumbnail", "the cover doesn't read", or "سو كفر"، "كفر الريل"، "ثمبنيل"، or after any finished video. Not for carousel covers.
---

# Cover and thumbnail — what reads on a phone

**The engine is shared** with the reel skill. All `scripts/` and `references/` are here:
`${CLAUDE_SKILL_DIR}/../video-editor`

**Read first:** `references/thumbnails.md` — the minimum sizes and their sources. The grid shrinks a cover to 12%, so anything under the limit doesn't read.

## Before you start — one question
**"Should I take your photo from the video, or do you have photos to give me?"**
- **From the video:** the script picks the clearest frame with their face large, and cuts them out onto a cream background (`--cut` for the cover · `--video` for the thumbnail — needs a Mac).
- **Their photos:** a cut-out photo with a transparent background (`--photo`) — best for a thumbnail: a clear expression (a big smile, surprise).
- No answer: from the video.

**Design from the video's topic every time — not a template:** the title comes from what they say, and logos/elements from what they talk about (a tool, a company, a number). The structure is fixed and the content changes.
**The background is cream like Claude** (`#F0EEE6`, or the theme's `bg` if it is light) — `--bg` changes it, and `--bg video` takes the video's background color.

## Reel cover (9:16) — also becomes the first frame

```bash
python3 scripts/28_cover.py <work> "line|*accent word*" [--photo me.png | --cut] [--x old.png --ok new.png] [--first ad-master.mp4]
python3 scripts/34_phone_preview.py <work>/cover.jpg
```

- Everything important sits inside the 1:1 square in the middle — imaginary, no frame.
- The title is 5 words at most, two lines, about 9 characters per line (the script warns you).
- ✕ and ✓ are **not a rule** — only if the video is "from X to Y". Logos go in a row above the head inside the square, and the text below on the chest.
- `--first` puts the cover on the first frame → `<name>-cover.mp4`.
- Show `cover_phone.jpg` (at its real phone size) — if you can't read it there, it won't read.

## YouTube thumbnail (16:9) — three ideas

```bash
python3 scripts/33_thumb.py <work> "line|*accent word*" [--photo me.png | --video src.mov] [--logo thing.png] [--x old.png --ok new.png]
python3 scripts/34_phone_preview.py <work>/thumb_A_1280.jpg --youtube
```

- Produces 3840×2160 (recommended) + 1280×720 (for phones, under 2 MB) for each idea, and a `thumbs_sheet.jpg` sheet — show it and let them choose.
- A large face with a clear expression · the bottom right empty (the video's duration badge) · 3–5 words.

## 🌐 Language

The user picks their language once — `references/language.md` in the reel skill; the code comes from `python3 scripts/_lang.py`. Speak to them in it. Cover text is in the video's spoken language.

## ⛔ Your style

- The title comes from the video's own content — a short hook; never invent words they didn't say.
- No text over the face. Fonts: Cairo (or their theme font) for Arabic script, Inter for Latin.
- Show the image before any upload or posting — no posting or scheduling.

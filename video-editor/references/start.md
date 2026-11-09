<!-- Shared reference for every mode of the skills — read at the start of every run -->

# Start — set up the tools, the taste and the identity

The same start for every mode: talking-head reel, podcast, montage and motion.
All paths here are from the main skill folder (`video-editor`).

---

## Before anything — a model and effort tip (once per session)
In your first message of the session, tell the user in two lines (and don't repeat it):
> "For the strongest result: **Opus 5.5** with effort **max**. It uses more of your limit, but the edit comes out much better."
- **In the chat (claude.ai / the app):** from the model menu next to the send button → Opus 5.5 → Effort → Max.
- **Claude Code (terminal, desktop, the Code tab on mobile):** type `/model opus` then `/effort max`.
- Already on Opus 5.5 (you know your own model)? Mention only the effort. Don't suggest "ultracode" for editing: it splits the work across agents, each drawing with its own taste, and the cost multiplies — one agent at max effort is better for one video.
- Don't quote cost figures or minutes — they weren't measured.

## Step 0.2 — Language (first time only)

Read `references/language.md` and do it: if `~/.video-ad-editor/lang.json` doesn't exist, ask **once** which language they want (a list of options) and save it with `python3 scripts/00_onboard.py lang set <code>`.
From then on **everything you say to them is in their language** — the Arabic example sentences in the instructions are meaning only, not text to copy. Transcription follows their language automatically.

## Step 0.3 — Setup check (first time only, and on any connection failure)

Run `python3 scripts/00_check.py show`. If "assets source" isn't set → read `references/setup-check.md` and do it: they choose (A) the Google API or (B) their own subscription through Google Flow in Chrome, and you verify ElevenLabs, the Chrome extension and Flow access with a small table. If Flow fails at any time, open Chrome in front of them so they can sign in (the steps are written there).

## Step 0 — Prepare silently

```bash
bash scripts/00_setup.sh
```

- It printed "everything is ready" → don't mention it.
- It printed "🆕 a newer version exists" → ask: "There's an update for the skill — update it now?"
  - Yes → run the line the script itself printed (it differs between the skill and the plugin).
- Something is missing → tell them in one sentence what will be downloaded, get their approval, then:

```bash
bash scripts/00_setup.sh --install
```

- Something failed → say the fix in one human sentence, without pasting the error.
- The "extras" line shows "—"? Those are optional (smart audio cleanup, search by meaning).
  - Offer them **once**, when you need them: "Shall I download the smart audio-cleanup tool? Two minutes."
  - Yes → `bash scripts/00_setup.sh --extras`
  - Each one falls back to the old way if missing.

Prepare a work folder, and copy `scripts/compose.REFERENCE.html` into it as `compose.html`.

### 💡 Tips from the Bobian reel (6.0)
- **Many iPhone clips (HLG/HDR) you want to merge into one video? Convert each clip to SDR first, then merge.**
  `03_cut_zoom.py` detects HDR in a single file only — merging with ffmpeg first loses the HLG tag, so the colors come out washed or orange with no warning.
  ```bash
  swiftc -O -o scripts/hdr2sdr scripts/hdr2sdr.swift          # once (Mac + Xcode tools)
  mkdir -p sdr; for f in IMG_*.MOV; do scripts/hdr2sdr "$f" "sdr/${f%.*}.mov"; done   # each clip on its own
  ```
  To know if it's HDR: `ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer -of csv=p=0 IMG_1.MOV` → `arib-std-b67` (HLG) or `smpte2084`.
- **Audio cleanup in Claude Code = DeepFilterNet on the machine** (`bash scripts/00_setup.sh --extras` then `02b_enhance_audio.sh <work> --local`).
  Adobe's `media_enhance_speech` tool starts the job, but Claude Code has no follow-up tool to fetch the cleaned file — don't rely on it here.

---

## Step 0.5 — The intro page (first time only)

```bash
python3 scripts/00_onboard.py show
```

The result `{}` = no saved choices.

**1. It printed choices** → don't open anything:

```bash
python3 scripts/00_onboard.py theme <work>
```

And say in one line: "Going with your settings: these colors, this caption style."
(Exit code 4 = a `theme.json` already exists — leave it.)

**2. It printed `{}` and they have an identity file** (`.auto-memory/creator-profile.md`) → don't open the page, go to step 1.

**3. It printed `{}` and they have no file** → run the page in the background:

```bash
python3 scripts/00_onboard.py --work <work>
```

- Tell them: "I opened a small page where you pick your taste — or write what you want and skip. I'll wait."
- Exited with code 0 → `python3 scripts/00_onboard.py theme <work>`
- It contains `skip:true` → work from `note`.

**Other cases:**
- They said "change my settings" → open it (it opens pre-filled), then `theme <work> --force` with their approval.
- A session with no browser → don't open it, go to step 1.
- Where each field goes, identity from a link, and the generated voice → `references/onboarding.md`.
- ⛔ A generated voice has no default: they choose (standard or dialect, man or woman).

---

## Step 1 — Their visual identity (there is no default color)

⛔ **Don't assume cream and clay** — that's Claude's theme, not theirs.
⛔ **Don't change an earlier theme.** They already have a `theme.json` from a previous video? Use it as it is.
Changing a main color only at their explicit request.

**0.** Was `theme.json` written in step 0.5? Skip this step.

**1.** Look for `.auto-memory/creator-profile.md`.
Found it? Take the colors, font and handle, and say: "I'll go with your colors: these — OK?"

**2.** Not there? **One question:**
"What are your account's colors? Give me the background color, the accent color and your logo.
Or your account link, or a few images whose style you like, and I'll extract the theme from them."

**Did they send reference images?** (even if they didn't say "reference" — style images + "I want it like this"):

```bash
python3 scripts/00_theme_refs.py <work> image1 image2 …
```

- It extracts colors with readable contrast, and writes `theme.json` and `refs_palette.jpg`.
- **Read the sheet with your own eyes.** Then the taste is your decision from the look of the images:
  - The font: `font`
  - The caption: soft → `shadow` or `underline` · bold → `card` or `big`
  - The pace: calm images → `"pace":"calm"`
- Tell them in one line: "From your images I took: this background, this accent, this caption style — OK?"
- The images have a shadow or a yellowish light? `--light` or `--dark` pins the direction.

**3.** Write `<work>/theme.json` and copy their logo as `logo.png`:

```json
{ "bg":"#101828", "ink":"#F5F7FA", "acc":"#F2B33D", "clay":"#C98B18", "mut":"#98A2B3",
  "font":"Tajawal", "handle":"@his_handle", "logo":"logo.png", "grade": false,
  "faceAnchor": 0.30, "badgeUntil": 0, "capStyle": "card" }
```

- All the drawing derives its colors from these values. Dark or light, both work.
- Wrote the colors by hand? Run this so white text doesn't land on a light accent:

```bash
python3 scripts/00_onboard.py onacc <work>
```

### Extra theme keys

| Key | What it does |
|---|---|
| `badgeUntil` | The account badge. Off (0) — the name is on the platform and on the end card. `3` = the first 3 seconds if they ask for it |
| `grade` | Always off — see the "zero color grading" rule |
| `capStyle` | The caption style → `references/word-fx.md` |
| `capStill` | `true` = a caption with no motion: the card enters and leaves by opacity only, and the word doesn't jump or pulse. Spoken-word coloring and the pill stay. Default is motion → `references/word-fx.md` |
| `bar` | `false` = no progress bar. Default shown. (Not `capStyle: "bar"` — that's a caption style) |
| `pace` | `"calm"` a calm pace → `references/explainer-and-pace.md` |
| `hookZoom` | A soft zoom on their face at the start of the hook (seconds = the hook's end). Off by default |
| `outro` | The end card `{l1,l2,chips,cta,word,sub}` |
| `hook` | A written hook line for podcast reels — written by `22_hook.py apply`, don't write it by hand |

**A calm premium ad** (17 October): `"capStill": true` + `"bar": false`, and any `FX.doorway` that opens on their face takes `zoomB: false` (no zoom on the face).

**`hookZoom` in detail:**
- After step 6 run `python3 scripts/22b_hook_center.py <work>` — it writes `hookCenter` onto their face.
- Without it, it takes the face from `behind.json`.
- And with it a very light whoosh in `sfx.json`:

```json
"soft": [[0, 0.035], [hook_end - 0.22, 0.06]]
```

**⚠️ `outro`:** the default is the skill's own ad ("comment with the word video").
Any video that isn't an ad for the skill (a podcast reel, for example) must change it.

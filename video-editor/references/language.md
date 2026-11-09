<!-- Shared reference — read at the very start of every run (Step 0.2 of start.md) -->

# Language — the user picks it once

The skill's entry files are in English (some deep reference docs are still Arabic, Gulf dialect), and **the user can work in any supported language**. The instructions are for you; what the user sees is in *their* language. English is the default until they choose.

## Supported languages

| code | language | code | language |
|---|---|---|---|
| `ar` | العربية | `pt` | Português |
| `en` | English (default) | `de` | Deutsch |
| `fr` | Français | `tr` | Türkçe |
| `es` | Español | `ur` | اردو |
| `id` | Bahasa Indonesia | `fa` | فارسی |

`python3 scripts/_lang.py list` prints the same table.

## Step 0.2 — pick the language (first run only)

```bash
python3 scripts/_lang.py          # prints the saved code (en if nothing is saved)
ls ~/.video-ad-editor/lang.json   # exists = the user already chose
```

- **`lang.json` exists** → use it silently. Do not ask again.
- **Missing** → ask **once**, in a short multi-option question (use the choice/question UI if the client has one, otherwise a numbered list), written in several languages at once because you don't know theirs yet:

  > Which language should I work in? · أي لغة تفضّل؟ · Quelle langue ? · ¿Qué idioma?
  > 1) العربية  2) English  3) Français  4) Español  5) Português  6) Deutsch  7) Türkçe  8) اردو  9) فارسی  10) Bahasa Indonesia

  Then save it:

  ```bash
  python3 scripts/00_onboard.py lang set <code>
  ```

- **If the user already wrote to you in a supported language**, don't ask: confirm in one line ("I'll work in English — say 'change language' any time.") and save it.
- **"Change language" / «غيّر اللغة» / "cambia el idioma"** at any time → ask again and save.
- Unsupported language? Pick the closest supported code for transcription and tell the user in one line.

## The taste page has a language switcher

The intro page that opens at `http://127.0.0.1:<port>/` has a language menu at the top. It shows the language saved in `lang.json` and switching it **saves the choice for the whole plugin** (Claude's replies, transcription, captions). Pages currently translated: العربية, English, Français, Español, Português, Deutsch, Türkçe — the other languages fall back to English on that page until their strings are added (`ROWS` in `onboarding/index.html`: `[ar, en, fr, es, pt, de, tr]`).

## What the language controls

| Part | Behaviour |
|---|---|
| **Everything you say to the user** (status lines, questions, summaries, errors) | Their language. Write natural, plain wording — no jargon. Example sentences in the instruction files are *meaning*, not text to copy. |
| **Transcription (Whisper)** | `--language <code>` — every script already reads it through `scripts/_lang.py`; in the manual commands use `$(python3 scripts/_lang.py)`. |
| **Captions on the video** | Written in the spoken language of the video. The renderer already switches direction per line (Arabic/Persian/Urdu → right-to-left, others → left-to-right, numbers isolated). |
| **Fonts** | Latin languages → `Inter` (in `motion/fonts/`). Arabic script → `Tajawal` / `Cairo` / `IBM Plex Sans Arabic` / `Noto Kufi`. Set `"font"` in `theme.json` accordingly. |
| **Generated voice (TTS)** | Pick a voice whose locale matches the language (e.g. `en-US-…Neural`, `fr-FR-…Neural`). The Arabic fusha/dialect question only applies to `ar`. |
| **Wake phrases** | The user may speak any language — treat the Arabic trigger phrases in each skill's description as *examples of intent* ("make this a reel", "remove the silences", "make a motion video from this text"). |

## ⛔ Known limits (be honest with the user if it matters)

- The transcript cleanup helpers (`02_captions.py` normalisation, `19_seam_check.py` text matching) were tuned on Arabic. For other languages check the transcript yourself in Step 5 and fix wording by hand.
- Whisper's "known hallucination phrases" list in `02a_whisper_check.py` is Arabic; repetition checks still work for every language.
- Built-in motion examples (`motion/examples/*`) have Arabic on-screen text. Treat them as layout examples and write the user's own text.

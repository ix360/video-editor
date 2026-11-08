<!-- Shared reference — ElevenLabs voiceover (used by the voiceover-video skill) -->

# Voiceover with ElevenLabs

Goal: an audio file `<work>/vo.mp3` with the user's script read in a voice the user chose — ideally **their own voice**.

## 0. Is ElevenLabs connected? (the full setup check is in `references/setup-check.md`)

Look for tools ending in `creative_list_voices` and `creative_generate_speech` (if they are deferred, load them with ToolSearch: `select:` those names).

- **Present →** continue to step 1.
- **Missing →** show the connect button, then stop and wait:
  1. `search_mcp_registry` with keywords `["elevenlabs"]` (the ElevenLabs entry has `directoryUuid` `f0709456-dc12-4718-87b1-e888d0bc5802`).
  2. `suggest_connectors` with that uuid. Tell the user in one line: *"Press Connect, sign in to ElevenLabs, then come back and say 'done'."*
  3. After "done", re-check the tools. Still missing? Say so plainly and offer the free fallback (`edge-tts`, see `references/onboarding.md`).
- The connector spends the user's ElevenLabs credits. Say so once.

## 1. Pick the voice — three paths

Ask one short question: **"Use one of your voices, record a new sample, or pick a ready-made voice?"**

### A. One of my voices (default when they ask for "my voice")
`creative_list_voices` (set `context`). The result includes the workspace voices — a cloned voice the user already made shows there. Show **names only** (max ~8) and let them choose; remember the `voice_id`.
No voice of theirs in the list? → path B.

### B. Record my voice now (instant clone)
1. Tell them: *"I'll open a small page. Read the text (1–3 min, quiet room), press Stop."*
2. ```bash
   python3 scripts/39_record_voice.py record --name my-voice
   ```
   It prints `URL: …` first — give it to the user if the browser doesn't open. It saves `~/.video-ad-editor/voice/my-voice.wav` and exits.
3. **Cloning needs an upload.** Either:
   - `ELEVENLABS_API_KEY` is in the user's `.env` → `python3 scripts/39_record_voice.py upload ~/.video-ad-editor/voice/my-voice.wav --name "My voice"` → prints `voice_id` (needs a plan with Instant Voice Cloning).
   - No key → tell them: *"Upload the file at elevenlabs.io → Voices → Add voice → Instant voice clone, then tell me when it's done."* Then re-run `creative_list_voices` to find it.
   (The connector tools can search and design voices but I could not confirm they can create a clone from a sample — don't promise it.)
4. Consent check, once: *"This sample is your own voice, right?"*

### C. Ready-made voice
`creative_list_voices` filtered by language (`languages`), `gender`, `use_cases` (e.g. `social_media`, `advertisement`) and the language from `scripts/_lang.py`. Play nothing — describe 3 options by name and traits; let them choose. Or `creative_design_voice` to make a new one from a text description (then `creative_save_designed_voice` to keep it).

## 2. Write the script

- The script is the user's text, or you write it from their idea. **Spoken words only** — no stage directions in brackets unless the model supports tags (`eleven_v4` does: `[softly]`, `[laughs]`).
- Keep one idea per sentence; numbers as words in the speaking language ("twenty-five", not "25") so the reading is right.
- Show the final text and get a "yes" before spending credits.

## 3. Price → generate → download

1. `creative_generate_speech` with `estimate_only: true`, `model_id: "eleven_v4"` (use `eleven_multilingual_v2` if the language sounds off), the `voice_id`, `prompt` = the script. Tell the user the credits.
2. On "go": the same call **without** `estimate_only` and `generations_count: 1`. It returns `flow_id` + `session_ids`.
3. Poll `creative_get_flow_run_status` (flow_id + session_ids) until `all_completed` or `has_failures`.
4. `creative_get_generations` → each has a signed `full_res_url`. Download:
   ```bash
   curl -sL "<full_res_url>" -o <work>/vo.mp3
   ffprobe -v error -show_entries format=duration -of csv=p=0 <work>/vo.mp3
   ```
5. Tell the user the duration and let them listen. **If they want another take, that's a new, charged generation — ask first.**

## 4. Hand over to the video

- **Talking-head video** exists → the voiceover replaces/accompanies it; run the normal reel steps on the final audio.
- **No person on screen** → treat `vo.mp3` as the narration: transcribe it (`--language $(python3 scripts/_lang.py)`), caption it, and build scenes (`motion-video`, stock via `references/stock.md`, generated images/clips via `references/gen-scenes.md` / `references/google-flow.md`). The voice-only recipe is in `references/onboarding.md` (generated voice section).
- Word timing comes from Whisper on the generated audio — no extra step.

## Known limits
- Cost and plan limits belong to the user's ElevenLabs account; cloning needs a plan that includes it.
- A cloned voice in another language keeps a slight accent of the sample language; check a 10-second test before the full script.
- Don't clone anyone else's voice.

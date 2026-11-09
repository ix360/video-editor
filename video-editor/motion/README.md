# Motion explainer — a complete motion film from a text

From a written script to a finished film: voice, 2D and 3D scenes, beat-synced effects, and a 60 fps MP4.

## Steps (from the `motion` folder)
```bash
python3 voice.py  <project>                  # a generated voice per line (the voice the user chose — there is no default) + word timing
python3 voice.py  <project> --own me.wav     # the person's OWN recording (or an ElevenLabs file): Whisper times the words and splits it into the script lines
python3 timeline.py <project>                # lays the lines on the beat and sets each scene's time
node render.js <project> preview 0.5 1.5 --safe   # preview stills + a contact sheet (look at them before anything else)
node render.js <project> all --scale 0.5     # fast draft
node render.js <project> all                 # final render (resumes where it stopped)
python3 audio.py <project>                   # background bed + effects + levelling → renders/final.mp4
python3 audio.py <project> --no-bed          # without the background bed → final-nobed.mp4
```
`audio.py` needs `scipy`; `bash scripts/00_setup.sh --install` puts it in a small venv (`~/.video-ad-editor/venv`) when the system Python blocks pip, and `audio.py` finds it by itself.
Transcription uses the **video language** (`python3 scripts/_lang.py video`), which can differ from the chat language.

## The project
- `project.json`: settings (colors, fonts, pace, scenes and each scene's lines, `images`)
- `script.json`: the script, line by line
- `sfx.json`: sound effects and their positions (scene, word, beat)
- `scenes/*.js`: one scene per file
- `assets/`: photos declared in `project.images` (from stock, Gemini or Flow)

A ready example is in `demo/`; the full guide for the scene writer is `ENGINE-API.md`.

## Rules
- No templates. Every film's motion is built from the meaning of its script.
- Western digits (1 2 3). The engine converts Arabic-Indic digits automatically.
- No text outside the safe zone — always check with `--safe`.
- Content rules are the owner's choice, not an engine default: only avoid what `theme.json → "avoid"` lists (e.g. `["no people"]`), and add those as negative constraints in every generated-image prompt.
- Edited a scene? Re-render with `all --fresh`, because resuming keeps the old frames as they were.

<!-- Reference for the video-editor skill — motion explainer mode (no person, no filming) -->

# Motion explainer — a film from text

Input: a text, an idea, or a script.
Path: voice (their own, or a generated one) → a 60 fps motion film, 2D and 3D, optionally mixed with photos.

Steps and commands → `motion/README.md`, then the scene writer's guide `motion/ENGINE-API.md`.

---

## ⛔ One agent builds the whole film

- One prompt. No team, no judges, no critics — unless the user asks to "polish it".
- Measured (28 Sept): one agent, 22 minutes → "excellent". A team of 13 builders plus critics → 6 hours.

## Quality bar

The user's own prompt, verbatim:

> Craft a high-energy motion graphics piece that flexes your top-tier animation skills
> like a killer portfolio reel. Pull out all the stops, like the creative work on Dribbble, fps 60

That means: 3D, line drawing, and kinetic type. The eye never rests.

## ⛔ Use the move bank — every film, every scene

The film's motion language comes from `references/moves.md`: `python3 scripts/35_moves.py plan …` gives the 3 core moves + accents, and the scenes call them as `ctx.FX.<id>(ctx, t, {...})` (`const { X, P, FX } = ctx`). Hand-drawn canvas code is for the *content* (a chart, a diagram); the **movement** (zooms, camera pushes, kinetic type, transitions, counters) comes from the bank.
- Every scene has a camera move or zoom (`pushIn`, `pullOut`, `kenBurns`, `snapZoom`, `punchCut`, `dollyZoom`, `handheld`, `parallax`), including photo scenes — a photo that doesn't move is a failure.
- A punch-in lands on the hook and on each key word (use `ctx.wordTime(...)` for the timing).
- The plan's core and accent moves all appear; never the same move twice in a row.
- Run `python3 scripts/42_start.py audit <project>` before rendering; it must pass.

## ⛔ Not graphics only — plan every scene before drawing

A film made only of graphics reads as a slideshow. Before writing any scene, give each scene a type (this is the `script.md` shot list from the `script-writer` skill):

| Type | Use it for | Source |
|---|---|---|
| `graphic` | numbers, comparisons, steps, diagrams, the key word | the engine |
| `clip` | **Flow video** — a real moving shot (a place, an action, a mood). **The default for anything that is not a diagram.** | Google Flow in Chrome (`references/google-flow.md`) |
| `image` | a still the code can't draw well — the fallback when a clip isn't worth the credits | stock → Gemini → Flow (`references/stock.md`, `references/gen-scenes.md`) |
| `3d` | a `stage3D` scene (objects, devices, text planes with bloom) | the engine |
| `screen` | a website or app | `references/web-app-explainer.md` |

- **The recipe for every motion film: motion graphics + at least one 3D scene + Flow video clips.** Default mix: about a third each. Flow clips are better than photos, always; 3D and kinetic graphics carry the facts.
- **Exception: technical or medical comparisons stay graphics/3D** (an AI video of an implant or an eye diagram can be wrong). Use clips for mood, place, action and people, never as evidence.
- **How many clips:** at least 2 per film, 3–6 s each, 9:16, muted. Reuse a clip across two scenes (different crop/zoom/speed) rather than ordering more. Tell the user once: "I'll generate N clips in your Flow — it uses your daily credits and takes a few minutes each."
- **Putting a clip in the film:** `python3 scripts/17_gen_scenes.py <work> import <k> <downloaded.mp4> --project <project>` turns it into frames inside the project and registers `project.json → clips`. In a scene: `ctx.drawClip(X, "<k>", lt, { zoom, ox, oy, speed, loop, pingpong, x, y, w, h, alpha })` (`lt` = seconds into the clip; it loops by default). Put the move-bank camera move around it (`FX.pushIn`, `snapZoom`…) and a dark gradient under any text.
- A photo scene = the image as a full-bleed background with a slow push (`ctx.img(name)`, `project.json → images`), used when a clip isn't worth the credits. Flow's free image download is 768×1376 (the 2K upscale may cost credits): keep photos behind overlays and motion.
- Clips are frame sequences at 720 px wide, 30 fps: fine as backgrounds and full-bleed shots under overlays.
- The owner's content rules (people, symbols, anything to avoid) live in `theme.json → "avoid"` — nothing is forbidden by default.
- **Latin-script films (French, English, Spanish…):** set `project.json → fonts` to Latin families (Inter, or fonts registered with `extraFonts`), pass explicit `text`/`labels` to every FX (their built-in defaults are Arabic), keep `keepBrand` on so the user's palette wins over a style, and skip Arabic-only moves (the planner already does). Text lays out left-to-right automatically.

## One-takes and examples

- A whole video in one shot, no cuts (interfaces, steps, ideas with scenes inside scenes): `references/one-take.md`.
- Examples and techniques from other people (inspiration, not copying): `references/examples.md`.

## A fixed frame with one changing slot — only when the user asks

⛔ **Not the default, and not for every film.** Use it when the user asks for it ("fixed frame", "a fixed title with the text changing under it", "slide wall", "3D"). Without a request, the film follows the usual approach: the idea comes from the meaning of the script.
When asked, the tools are:
- **Fixed frame** (`MOTION.stage`): a title on top that never moves, a slot underneath that changes and finishes the sentence (`ctx.text.slot`), and the content window in the middle. Scenes and transitions happen inside the window only.
- **One accent color** on a dark background, and the same card shape in every scene.
- **3D slide wall** (`ctx.slideWall`): the camera flies over it and ends on a card that becomes the first scene with no cut. The first frame shows the wall (not an empty screen) because it is the cover.
- **Motion blur** (`motionBlur`): the only one that suits any film with fast movement — not a look, it just makes motion smooth.
- All colors come from the theme (`project.palette`) — the example is light, and works dark or in any client's colors unchanged.
- The working example: `motion/examples/stage-wall/` — read it for the method, and take the idea itself from the meaning of your script.

## No template

- Brainstorm 3 ideas yourself, criticise them, and develop the strongest.
- Every sentence is shown at the moment it is said.

## Pace

- One sentence ≈ one scene.
- A hit or change every 0.5–1 s.
- But any word on screen stays at least 0.6 s so it can be read.
- Don't cut the gaps until it feels breathless.

## Sound — generated voice (Arabic only)

These tips are for Arabic edge-tts voices; skip them for other languages and for the user's own voice or an ElevenLabs voice.
- Fully vowelled Modern Standard Arabic — dialects come out broken in the free voices.
- A closing ta marbuta at the end of a sentence → "ه" in the voice text.
- No dagger alif.
- English names in Latin letters (Opus).
- Check every line by eye and with Whisper medium **before** drawing.
- Send them the audio to listen to.

## Sound — in the film

- Speech + sound effects only.
- ⛔ No background track by default — whoever wants a bed adds it themselves:

```bash
python3 motion/audio.py <project> --no-bed
```

## The user's own voice (attached mp3) or an ElevenLabs voice

Both enter the same way: `python3 motion/voice.py <project> --own <file>` aligns the real recording to the script lines with Whisper (in the **video language**: `python3 scripts/_lang.py video`), then `timing: {keepOriginal: true, snap: "none"}` in `project.json`. `audio.py` levels an own voice to −20 LUFS.

## Hand over a rough draft early

A contact sheet of frames, or the quality text — before the full render. Always check with `--safe` (the safe-zone overlay).

---

## Explaining a website or an app

They give a website link, or say "explain to people how to do X in the app".
Result: real screenshots inside a drawn phone or computer frame.

Capture the site (screens + scrolling + its texts and colors):

```bash
node scripts/27_web_capture.js <url>
```

An iPhone or MacBook demo in **real 3D** (metal, glass and shadow; it turns and zooms to the button):

```bash
node scripts/31_device3d.js
```

The flat, fast version: `scripts/30_demo.js`

All the details → `references/web-app-explainer.md`

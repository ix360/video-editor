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

## ⛔ Not graphics only — plan every scene before drawing

A film made only of graphics reads as a slideshow. Before writing any scene, give each scene a type (this is the `script.md` shot list from the `script-writer` skill):

| Type | Use it for | Source |
|---|---|---|
| `graphic` | numbers, comparisons, steps, diagrams, the key word | the engine |
| `image` | a concrete object, place or mood the code can't draw well | stock → Gemini → Flow (`references/stock.md`, `references/gen-scenes.md`, `references/google-flow.md`) |
| `screen` | a website or app | `references/web-app-explainer.md` |

- Default mix: roughly half graphics, half photos — but **technical or medical comparisons stay graphics** (an AI photo of an implant or an eye diagram can be wrong); use photos for mood, place and people.
- An image scene = the photo as a full-bleed background with a slow push (`ctx.img(name)`, declared in `project.json → images`, files in `<project>/assets/`), a dark gradient for legibility, and the engine drawing the words on top.
- **Video clips cannot be placed inside a motion film yet** — use a still frame from the clip, or build that film as a montage/reel.
- Generated images from Flow's free download are 768×1376 (the 2K upscale may cost credits). Keep photos behind overlays and motion; never show them tiny or pixel-peeped.
- The owner's content rules (people, symbols, anything to avoid) live in `theme.json → "avoid"` — nothing is forbidden by default.

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

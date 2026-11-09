# Move bank: every video gets a move board, and you choose with intent

## What is mandatory

1. Every video gets a move plan BEFORE the first scene: `python3 scripts/35_moves.py plan --title "..." --family auto --cues number,contrast,emphasis,cta > <work>/moves_plan.json` (cues = the real moments in the script). NEVER run `35_moves.py` with no arguments: it starts a gallery server and blocks.
2. The scenes must call the plan's core and accent moves as `ctx.FX.<id>`; every scene needs a camera move or zoom (pushIn, pullOut, kenBurns, snapZoom, punchCut, dollyZoom, handheld, parallax, tilt3D...), with a punch-in on the hook and on each key word.
3. `python3 scripts/42_start.py audit <project>` must pass before rendering.
4. Moves marked as Arabic-only (the "bonus" group in the gallery, e.g. letter-by-letter Arabic script moves) are for Arabic text only; the plan filters them out when the video language is not Arabic. For Latin-script films keep text direction left-to-right.

A numbered move bank that grows over time (`motion/moves/catalog.json`: 100 moves as of October 17). Each move is a ready function in `motion/moves.js` + a 4 s preview + its source.
**User decision (October 13):** "I want you rich in moves... and deliberate." The user does not pick move by move. You pick for each video.

| File | What it holds |
|---|---|
| `motion/moves/catalog.json` | number · `id` · name · `role` · `energy` 1–3 · `families` · `cues` · source · preview |
| `motion/moves.js` | the functions: `ctx.FX.<id>(ctx, t, o)`, every option is documented above each function |
| `motion/moves/index.html` | the gallery (opened by `scripts/35_moves.py`): for browsing, or if the user wants to block something |
| `motion/moves/CREDITS.md` | sources and licenses |

## 1) The video's board (mandatory before the first scene)

```bash
python3 scripts/35_moves.py plan --title "<video title>" --family auto --cues number,cta
```
This outputs the video's **board**:
- **Family** (`family`): the motion flavor for the whole video. `calm` quiet · `punch` energy · `onetake` continuous camera with no cuts · `editorial` editorial/explainer.
  `auto` = the family not used for the longest time. Choose yourself when the video is clear: calm advice = `calm`, hook and numbers = `punch`, one idea that evolves = `onetake`, explanation and steps = `editorial`.
- **3 core moves** (`core`): a word move + a transition + a camera or card move. **The whole video revolves around them**, like a one-take: the same visual language from start to end.
- **Accents** (`accents`, 2 at most): a special move for a special moment only. `--cues` = the moments in the script:
  `number` strong number · `list` bullet points · `price`/`cta` price or call to action · `contrast` comparison · `emphasis` key word · `reveal` reveal · `tech` tech · `hit` impact.
- **Rules** (`rules`): always follow them on timing (e.g. J-cut).
- **Style** (`style`): the look of the whole video: surface, texture, font and cards (17 styles, or a blend `a+b`). Details and code: `references/styles.md`. `moments` = a moment style (VHS/brutalist) for the hook or the CTA only.
- It is saved in the `moves-history.json` log, so the core moves change from video to video. Tell the user in one line: "Board for this video: punch - staggered rise + whip + notifications".

## 2) Rhythm inside the video

1. **Something happens every 2–4 s** (per `pace` in the profile). Not every sentence needs a move: ordinary sentences run on the caption alone.
2. **The core word move** goes on the important sentences. **The core transition** only when the scene or idea changes. **The core camera move** once per scene at most.
3. **The accent** only at its moment (the number, the price, the hit), and it does not repeat.
4. ⛔ Never the same move twice in a row. Do not bring a move from outside the board unless nothing on the board serves the sentence, and say so in one line.
5. **The move comes from the meaning of the sentence**: the board sets the language, the sentence sets where and when. Example: "from 0 to 1000" = the counter, not just any move. **And the bank does not limit you:** the strongest moments of the plugin owner were invented from the sentence: "copies" -> 3 copies of him, "ideas that already exist" -> a wall of cards behind him. If the sentence deserves something not in the bank, invent it.
6. `off` in the profile (if the user blocked something in the gallery) is banned completely. `on` puts it forward for selection. Both are optional: by default the user does not choose.

## 1b) The gallery (optional)
`python3 scripts/35_moves.py` opens the gallery for browsing or blocking. From the chat: `set "3 7" --off "5"` · `show` · `list`.

## 3) Using it in code

**In the motion engine** (`motion/`: the motion film, the one-take, any scene drawn by `render.js`): call the function directly.
```js
draw(t, lt, ctx) {
  const { X, P, FX } = ctx;
  X.fillStyle = P.bg; X.fillRect(0, 0, ctx.W, ctx.H);
  FX.riseUp(ctx, t, { text: 'الفكرة أهم من الأداة', s: ctx.wordTime('l2', 0).s, accent: [1] });    // 3 staggered rise
  FX.whip(ctx, t, { s: 4.2, A: Y => drawIntro(Y), B: Y => drawStats(Y) });                         // 11 whip
  const tau = FX.ramp(t, { hit: ctx.wordTime('l3', 2).s });                                          // 20 slow-down on the hit: use tau instead of t
}
```
- Colors come from `ctx.P` (the user's theme) automatically. Do not pass hard-coded colors.
- `o.s` must be the time of a real word (`ctx.wordTime`). `FX.caption` takes `line: 'l2'` and syncs with the audio word by word.
- Transitions (`crossZoom softWipe iris whip zoomWipe dotZoom dipFade slideOver clockWipe slices glitch flip lightLeak` and `compare`) take `A` and `B` as functions that draw the full frame. Put them inside one scene in place of the engine's transition.
  `glitch` and `flip` draw A/B onto the frame itself and take a snapshot of it, so any FX inside A/B (e.g. `MV.panel(Y, () => FX.ringStat(MV, t, …))`) renders correctly.
- Camera moves (`pushIn pullOut handheld kenBurns snapZoom shake`) wrap `draw`; `rackFocus` and `dollyZoom` take `back` and `front`; `parallax` takes `layers:[{draw, depth}]`. In the talking reel put them on the `'video'` layer.
- `lowerThird` sits bottom right inside the safe area (y ≤ 1500 and x ≤ 920). Do not move it into the buttons corner.
- `jcut` and `matchCut` are timing rules, not drawing: J-cut = the next shot's audio leads its picture by 4–12 frames. Match cut = the same shape in the same place and size on the cut frame.

**In the talking reel** (`compose.html`): the same functions, but the ctx is called `MV` (from `scripts/moves-compose.js`: text and timing tools, `theme.json` colors and its font, on top of the engine canvas).
`compose.REFERENCE.html` loads `moves.js` and `moves-compose.js` from the work folder, and `04_render_frames.js`/`08_safe_check.js` copy them in on their own if they are missing.
Your scenes go at the end of `compose.html` (after the loading line):
```js
MV.ready(() => {                                   // caps.json arrives at init: any wordTime/lineSpan outside drawing goes inside ready
  MV.hideCaption(MV.lineSpan(0).s, MV.lineSpan(2).e + 0.5);                 // FX.caption instead of the engine caption
  MV.scene('cap', t => { const n = [2,1,0].find(i => t >= MV.lineSpan(i).s);   // last sentence that started: the next one takes its place
    if (n !== undefined && t < MV.lineSpan(n).e + 0.5) FX.caption(MV, t, { line: n, y: 1280, out: MV.lineSpan(n).e }); });   // 1 · stays after its audio, then exits (6.1)
  const s = MV.wordTime(3, 0).s;
  MV.scene('push', t => { if (t >= s && t < MV.lineSpan(4).e)
    FX.pushIn(MV, t, { s, to: 1.18, focus: [540, 560], blur: false, draw: Y => MV.video(Y) }); }, 'video');   // 12 video layer
  const w = MV.wordTime(5, 0).s - 0.3;
  MV.scene('whip', t => { if (t >= w && t < MV.lineSpan(5).e)
    FX.whip(MV, t, { s: w, A: Y => MV.video(Y), B: Y => MV.panel(Y, () => FX.riseUp(MV, t, { text: 'الفكرة', s: w + 0.35 })) }); });   // 11
});
```
- The line = the sentence number in `caps.json` (`MV.wordTime(3, 0)` = the first word of sentence 3). `line: 0` works.
- `MV.video(Y, R?)` draws the current video frame (full screen by default): it is the A/B scene for transitions and the `draw` for camera moves.
- `MV.panel(Y, fn)` = theme background + your drawing: a full screen between two shots. The engine caption stays on top of it.
- `MV.scene(name, fn, 'video')` for a move that runs on the video itself (pushIn/pullOut), so the caption stays on top; with no layer = above the video and below the caption.
- ⛔ 6.1 **The element does not vanish on the last word:** `out` (start of the exit) = the last word, +0.3 if the move's exit is faster than 0.4 s (like `speechBubble`), and the scene window runs until `out + 0.7`. Do not cut the window at `lineSpan(n).e` (`motion-rules.md` §3).
- ⚠ `FX.caption` on a dark theme: the outline around the words automatically becomes the darker of `ink`/`bg`, and the current word is in `onAcc` on top of the pill.

## 3b) Cut-out speaker moves (51–61)

`orbit couchWall uiWorld frameBreak headlineWall doodleBoil coverStory glassType phoneMockup greenScreen paperCut`
- They take `person` (the cut-out speaker, full frame) and `video` (the full video). `glassType` takes `draw` instead of both, and `phoneMockup` takes `video` only.
- **The cut-out is Mac only** (`mask: required` and `mac: true` in the catalog). Prepare it for the range before drawing: `node scripts/11_behind_text.js <work> person 12.4-15.8`
  (cut-out only, no other effect). In the scene pass `person: MV.person` **as is**: FX asks `MV.person.ok()`.
- Without a cut-out (not a Mac, or the frame is outside the range) each move falls back to its own substitute: the video in a card (the orbit circles the card, the cover sits over the video, the green screen puts your face in a bubble). `uiWorld` and `doodleBoil` (`mask: optional`) look better with the cut-out and work without it.
- `o.out` = exit time (it returns to the video with the same move in reverse).
```js
MV.ready(() => { const s = MV.wordTime(4, 0).s;
  MV.scene('cover', t => { if (t >= s && t < s + 3) FX.coverStory(MV, t, { s, out: s + 2.5, person: MV.person, video: Y => MV.video(Y), title: 'مكينة' }); }); });
```

## 3c) Batch 62–73 (Arabic letters · sticker · connect · chapters)

`ijamDrop qalamWrite videoText joinSnap kufiGrid redact` (text) · `pageTurnRTL` (transition) · `tilt3D` (camera) · `stickerFreeze beamConnect lightRays dynamicIsland` (cards and layers).
- **Letter moves** (62 dots drop, 63 the pen, 66 letters join, 67 kufi): they break the fully drawn line into connected parts (joined letter/dot/mark), so the joins never break, and all of them end on the correct joined word. 66 is the only one that shows the letters separated (in their isolated form): that is the meaning of the move itself. ⛔ 62 and 66 are banned on Quran text.
- 63 uses Aref Ruqaa if it is loaded (motion engine), otherwise the theme font. 67 uses `kufi` (Noto Kufi in the engine, the theme font in the talking reel).
- `videoText` draws the full frame until `out`; after that return to `MV.video` yourself (match cut). `tilt3D`, `lightRays` and `stickerFreeze` draw the video themselves (pass `video`).
- `tilt3D` = the same move for every chapter in the video (rule): change only `title` and `num`.
- **`stickerFreeze` needs a frame from another time**: an engine addition (October 17) in `moves-compose.js`:
  `MV.frameAt(Y, t, R?)` the video frame at t (`vfr/`), and `MV.personAt(Y, t, R?)` the cut-out at t (`bt/person/`). The first request loads the image, and `04_render_frames.js` waits for `MV.settle()` and redraws the frame before the capture, so the result is deterministic.
  The cut-out must cover the freeze moment: `node scripts/11_behind_text.js <work> person <from-to>` with `s` inside the range. Without a cut-out it falls back to a polaroid of the full frame (`videoAt: MV.frameAt`).
```js
MV.ready(() => { const s = MV.wordTime(6, 0).s;
  MV.scene('freeze', t => { if (t >= s && t < s + 2.4) FX.stickerFreeze(MV, t, { s, out: s + 2, person: MV.person, personAt: MV.personAt, video: Y => MV.video(Y), videoAt: MV.frameAt, text: 'وقف!' }); }); });
```

## 3d) Batch 75–87 (copies · map · crane · terminal · glass · face)

`morphWord` (text) · `nuqtaCurtain glassLens scanLine` (transitions, they take `A` and `B`) · `craneUp punchCut` (camera) · `cloneTrio dotMap rimOutline terminalType lineChartDraw girihBloom speechBubble` (cards and layers).
- **Cut-out (Mac):** `cloneTrio` and `rimOutline` (`mask: required`): without it, 3 video cards / a beam on a card frame. `girihBloom` (`optional`) sits behind the person with the cut-out, and over the video without it.
  `cloneTrio` takes `personAt: MV.personAt` (the copies lag 0.2/0.4 s) and `videoAt: MV.frameAt` for the fallback: same cut-out condition as 3c.
- **Face (Mac, `face: optional` in the catalog)**, `speechBubble` and `punchCut`: an engine addition (October 17):
  `python3 scripts/36_facetrack.py <work> <from> <to>` outputs `face.js` (the same `facetrack.swift` as the podcast, smoothed σ=5 frames). Put it in compose.html: `<script src="face.js"></script>`, and pass `face: MV.faceAt`.
  `MV.faceAt(t)` = `{x,y,w,h,mx,my}` in canvas coordinates (same framing as `MV.video`) or `null`, and the move falls back to a default position.
  `punchCut` locks the face on the first frame of each shot (a real camera does not catch up), and the limit is ×2.
- `glassLens`: the lens carries the new scene with it (`carry`), so the B text stays whole inside it. Keep the B title to one or two words (widest ~400px) so no word gets clipped at its edge.
- `scanLine` takes `Aat: MV.frameAt` (the old frame frozen under the line). `craneUp` takes `A` (the video) and `B` (the next card): after `at + 0.5` draw `B` yourself. Cards are still images (`cards`).
- `dotMap` has its map built in (simplified land, from the Atlantic to Japan): cities outside that range do not show. `terminalType` command and output are in English (Menlo/monospace font), and the Arabic comment is on its own line.
```js
MV.ready(() => { const s = MV.wordTime(5, 0).s;
  MV.scene('bubble', t => { if (t >= s && t < MV.lineSpan(5).e + 1) FX.speechBubble(MV, t, { s, out: MV.lineSpan(5).e + 0.3, line: 5, face: MV.faceAt }); });   // stays after its audio (6.1)
  const p = MV.wordTime(7, 0).s;
  MV.scene('cam2', t => { if (t >= p && t < MV.lineSpan(7).e) FX.punchCut(MV, t, { s: p, out: MV.lineSpan(7).e, video: Y => MV.video(Y), face: MV.faceAt }); }, 'video'); });
```

## 3e) Batch C: 74 and 88–100 (ayah · post · receipt · search · door · echo)

`ayahCalm echoStack warpWave` (text) · `bentoCut doorway lumaMelt` (transitions, they take `A` and `B`) · `bodyFollow swishSettle motionEcho` (camera) · `postCard palmHold receiptPrint searchBar pointerCursor` (cards and layers).

**⛔ 74 Calm ayah (`ayahCalm`): Quran rules before the move:**
- **Text from a trusted source only**: Tarteel MCP (`search_ayahs_text`) or quran.com in Uthmani script, and pass it as `text` **exactly as received, letter for letter**. ⛔ Never write an ayah from memory, and never change a letter or a diacritic. The function does not change the text: it only splits it on spaces (and a pause mark like ۗ sticks to its word).
- ⛔ **62 "dots drop" is banned completely on Quran text** (it breaks apart the script and the dotting), and so are 66, kashida, glitch and any other text move. On an ayah: `ayahCalm` only (and behind the ayah `girihBloom` 84 is allowed: geometry with no living beings).
- `manual: true` in the catalog: the board (`plan`) never picks it. Use it only when the video contains an ayah.
- Font `Amiri Quran` (Uthmani, SIL OFL: `motion/fonts/AmiriQuran-Regular.ttf`): loaded in the engine; in the talking reel `04_render_frames.js`/`08_safe_check.js` copy it to the work folder when compose.html contains `ayahCalm`, and `MV.needFont` loads it (the frame waits for the font).
- Ayah number inside ۝: `digits: 'arabic'` (the default, ٢٨: drawn directly without the engine's western-digit conversion) or `'western'`. `surah` on top, and `ref` (e.g. `'13 : 28'`) below, optional.
- Background is the theme or `video` darkened 60%: no images of living beings over the ayah. Words appear calmly one by one (`stagger`, or `times` from the recitation timing).
```js
MV.ready(() => { const s = MV.lineSpan(4).s;   // text from search_ayahs_text as is
  MV.scene('ayah', t => { if (t >= s && t < s + 6) FX.ayahCalm(MV, t, { s, out: s + 5.3, text: AYAH_TEXT, surah: 'الرعد', ayah: 28, ref: '13 : 28' }); }); });
```
**The rest:**
- `bodyFollow` (89) needs the face (`face: MV.faceAt` from `36_facetrack.py`, Mac); without it, it falls back to `handheld` (31). On the `'video'` layer.
- `motionEcho` (100) needs a frame from another time: `videoAt: MV.frameAt`, and with the cut-out (`mask: optional`) `person: MV.person, personAt: MV.personAt` so the echo is on your body only. Without them it is skipped. Pair it with `FX.ramp` (20) on the same hit.
- `palmHold` (91) needs the palm (`hand: optional`): `python3 scripts/29_handtrack.py <work> <from> <to>` outputs `palm.js`. Put it in compose.html and pass `palm: MV.palmAt`. Without it the element stays fixed bottom left.
- `postCard` (88): ⚠ never make a fake post for a real person: either a real screenshot, or the account owner's own words. No platform logos.
- `receiptPrint` (93) prices in western digits, currency from `currency`. `searchBar` (94) and `pointerCursor` (98) use a mouse arrow in the theme ink; `pointerCursor` takes `steps` (several clicks) and `targets` (buttons it draws).
- `swishSettle` (95) is a scene opener (wraps `draw`), it scales up on its own until no frame edge shows. `doorway` (97) and `lumaMelt` (99) draw `A` on a side canvas.
```js
MV.ready(() => { const h = MV.wordTime(3, 2).s;
  MV.scene('echo', t => { if (t >= h - 0.1 && t < h + 0.7) FX.motionEcho(MV, t, { s: h, video: Y => MV.video(Y), videoAt: MV.frameAt, person: MV.person, personAt: MV.personAt }); }, 'video'); });
```

## 3f) Depth moments: the standard from the first draft (6.0, from the Boubyan reel)

The Boubyan reel (approved by the bank and widely shared) worked because the motion was **deep from the very first version**. The standard: put real effort into performance and motion, not quiet stuff.
Cards, stamps and badges are not banned; use them when the topic deserves it. But before you draw, **plan 2–3 depth moments** for the reel and state them in one line:
"Depth moments: your voice wave behind your head at (voice interview) · map of Kuwait at (first time) · an orbit circling you at (client/work/staff)".

| Tool | When | How |
|---|---|---|
| **Behind the person** | any element (wave, map, orbit) that passes behind the head | cut out the range: `node scripts/11_behind_text.js <work> person 5.8-7.7` · draw on the `'video'` layer then `MV.person(X)` on top |
| **His voice wave** | "voice", "talks", "interview", an AI that answers | `python3 scripts/37_env.py <work>` -> `env.js` · `<script src="env.js">` · height = `MV.env(t)` |
| **Dot map** | a place, "first time in Kuwait", spread | `FX.dotMap` with `cities:[]` and light colors, growing slowly behind the head |
| **3D orbit** | 3 things (client · work · staff) | elliptical ring: the text behind is drawn before `MV.person`, the text in front after it |
| **Shape from the client's identity** | number, transition | the arc of the logo draws itself = counter (`k` from 0 to 1), or a wipe that swallows the screen with the next shot inside it |
| **One-take entry** | shot change | the camera dives into the logo/tablet (zoom 1->10 + blur) and comes out in the next shot: `MV.frameAt` for the frozen frame |
| 🆕 6.1 **Client-color light behind the person** | client name, "they approved it", brand moment | the wall behind is tinted in the client's identity (`multiply` + a `screen` halo) then `MV.person(X)` on top: **his face gets no color change at all**. It switches on like a bulb (flickers in the first 0.3 s) |
| 🆕 6.1 **Spark transition** | every change of place/shot: the same language across the whole reel | the next shot is revealed **inside a shape from the client's identity** (icon/mark) that spins and grows until it covers the screen, with an accent-colored edge: `sparkReveal` below |

```js
/* his voice wave behind his head: video layer, and the person on top of it */
MV.scene('wave', t => { if (t < 5.86 || t > 7.62) return;
  const n = 43, cx = 540, cy = 790; X.save(); X.fillStyle = '#fff';
  for (let i = 0; i < n; i++) { const x = 40 + i * (1000 / (n - 1)), d = Math.abs(x - cx) / 500;
    const h = 18 + 420 * MV.env(t - d * 0.22) * (1 - d * 0.3); X.fillRect(x - 7, cy - h / 2, 14, h); }
  X.restore(); MV.person(X); }, 'video');

/* dot map behind his head: light colors, no cities */
const MAPC = Object.assign({}, MV, { P: Object.assign({}, MV.P, { mut: '#FFFFFF', bg: '#FFFFFF', ink: '#FFFFFF' }) });
MV.scene('map', t => { if (t < 11.8 || t > 14.4) return;
  FX.dotMap(MAPC, t, { s: 11.8, y: 140, cities: [], total: null, title: null }); MV.person(X); }, 'video');

/* orbit: the back part before the person, the front part after (orbitDraw is your function: front=false draws the back half of the ring) */
MV.scene('orbit', t => { if (t < 31 || t > 38) return; orbitDraw(t, false); MV.person(X); orbitDraw(t, true); }, 'video');

/* one-take entry at point (px,py) at cut tc */
function dive(t, tc, px, py) { if (t < tc - 0.38 || t > tc + 0.36) return;
  if (t < tc) { const k = Math.pow(2, 10 * ((t - tc + 0.38) / 0.38) - 10), s = 1 + 9 * k;
    X.save(); X.filter = `blur(${(k * 14).toFixed(1)}px)`; X.translate(px, py); X.scale(s, s); X.translate(-px, -py); MV.video(X); X.restore(); }
  else { const k = 1 - Math.pow(2, -10 * ((t - tc) / 0.36)), s = 1.45 - 0.45 * k;
    X.save(); X.filter = `blur(${((1 - k) * 12).toFixed(1)}px)`; X.translate(540, 900); X.scale(s, s); X.translate(-540, -900); MV.video(X); X.restore(); } }
```

**🆕 6.1 from the "$1000 in a day" reel (Majed: "reached another level"): the two recipes that got praised:**
```js
/* client-color light behind the person: the wall gets tinted and the face is untouched. Cut out the range first (Mac):
   node scripts/11_behind_text.js <work> person 32.3-36.3   <- covers on-0.05 until off+0.45
   colors = the client's official identity from facts.md (Boubyan: #C8102E · #961428): the client's identity moment, not the reel theme */
MV.ready(() => { const RL = { on: MV.wordTime(19, 4).s - 0.06, off: MV.lineSpan(20).e + 0.05 };   // "...Boubyan" -> end of sentence 20
MV.scene('brandLight', t => {
  if (t < RL.on - 0.05 || t > RL.off + 0.45 || !MV.person.ok()) return;            // ⛔ no cut-out for this frame = do not tint, it would tint his face
  const fl = t < RL.on + 0.32 ? [1, 0.25, 0.95, 0.4, 1][Math.min(4, Math.floor((t - RL.on) / 0.065))] : 1;   // switches on like a bulb
  const a = pr(t, RL.on, RL.on + 0.05) * fl * (1 - eio(pr(t, RL.off, RL.off + 0.45))); if (a <= 0) return;
  X.save(); X.globalAlpha = a; X.globalCompositeOperation = 'multiply';              // the light wall takes the color (dark areas barely show it)
  const g = X.createRadialGradient(560, 820, 60, 560, 900, 1250); g.addColorStop(0, '#FF4D5E'); g.addColorStop(0.45, '#C8102E'); g.addColorStop(1, '#961428');
  X.fillStyle = g; X.fillRect(0, 0, 1080, 1920); X.restore();
  X.save(); X.globalAlpha = a * 0.55; X.globalCompositeOperation = 'screen';         // soft halo behind the head
  const g2 = X.createRadialGradient(560, 760, 20, 560, 760, 620); g2.addColorStop(0, 'rgba(255,90,100,.85)'); g2.addColorStop(1, 'rgba(255,90,100,0)');
  X.fillStyle = g2; X.fillRect(0, 0, 1080, 1920); X.restore();
  MV.person(X);                                                                      // he sits on top of the tint as is: zero color change on his image
}, 'video'); });

/* spark transition: tc = first frame of the next shot · shape(Y,x,y,size,rot,col) draws the identity shape filled with col.
   before the cut: A = the live video and B = the first frame of the next shot, frozen · after it: A = the last frame, frozen, and B = live */
let SPARK_CV = null;   // ⚠️ do not name your constants AR or MARK: the engine already defines them ("already declared" error kills your whole scenes script)
function sparkReveal(Y, t, tc, shape, o = {}) {
  const d0 = o.d0 || 0.34, d1 = o.d1 || 0.42; if (t < tc - d0 || t > tc + d1) return false;
  const FR = 1 / 30, A = Z => (t < tc ? MV.video(Z) : MV.frameAt(Z, tc - FR)), B = Z => (t >= tc ? MV.video(Z) : MV.frameAt(Z, tc + FR));
  const xi = u => u <= 0 ? 0 : Math.pow(2, 10 * u - 10), xo = u => u >= 1 ? 1 : 1 - Math.pow(2, -10 * u), k = pr(t, tc - d0, tc + d1);
  const g = k < 0.5 ? 0.5 * xi(k * 2) * 0.85 + 0.5 * (k * 2) * 0.15 : 0.5 + 0.5 * xo((k - 0.5) * 2);   // slows -> launches at the cut -> settles
  const S = lerp(10, 12500, g), rot = -0.9 + 1.6 * eio(k), cx = o.cx || 540, cy = o.cy || 900;
  if (!SPARK_CV) { SPARK_CV = document.createElement('canvas'); SPARK_CV.width = 1080; SPARK_CV.height = 1920; }
  const G = SPARK_CV.getContext('2d');
  A(Y);
  Y.save(); Y.globalAlpha = 1 - pr(k, 0.75, 1); shape(Y, cx, cy, S * 1.045, rot, o.edge || MV.P.acc); Y.restore();   // accent edge behind the mask
  G.setTransform(1, 0, 0, 1, 0, 0); G.globalCompositeOperation = 'source-over'; G.clearRect(0, 0, 1080, 1920); B(G);
  G.globalCompositeOperation = 'destination-in'; shape(G, cx, cy, S, rot, '#000'); G.globalCompositeOperation = 'source-over';
  Y.drawImage(SPARK_CV, 0, 0); return true;
}
/* identity shape as Path2D (sharp at any size, no loading): the path from his logo SVG with viewBox 0 0 100 100 */
const BRAND_PATH = new Path2D('M50 0 L61 39 L100 50 L61 61 L50 100 L39 61 L0 50 L39 39 Z');   // example: a star, put in the path of his mark
const brandMark = (Y, x, y, s, r, col) => { Y.save(); Y.translate(x, y); Y.rotate(r); Y.scale(s / 100, s / 100); Y.translate(-50, -50); Y.fillStyle = col; Y.fill(BRAND_PATH); Y.restore(); };
MV.scene('sparks', t => { for (const [tc, cx, cy] of [[262 / 30, 760, 905], [1639 / 30, 540, 440]]) sparkReveal(X, t, tc, brandMark, { cx, cy }); }, 'video');
```
- **Shape center** = something in the shot that deserves it (the logo in the background, the phone, the head): in the $1000 reel once on the phone (760, 905) and twice above the head (540, 440).
- Is the shape an image (PNG icon)? Color it with `source-in` on a side canvas, and let the image load before drawing (`MV.settle` must wait for it). Path2D is simpler and sharper.
- The cut `tc` comes from the cuts in `cut.json` (first frame of the new shot), and `MV.frameAt` needs `vfr/` (present since step 6). `08_safe_check.js` counts the frozen frame as video.
- Both run full screen (`R_FULL`): `MV.video` and `MV.person` draw the full frame; in card mode they break the layout.
- The same transition on every change of place (3 times in the two-minute reel): a consistent language is part of the level. And "client light" is one depth moment out of the 2–3, not on every sentence.
- These are ideas, not templates: every reel invents its moments from its own words and its client's identity (Boubyan: the logo arc as a 90-second counter, an "among the first" race, a red stepped card).
- Any sentence whose words are written in motion = `nocap` for that sentence (`references/scenes.md`).
- Text that must show in front of the person (`cutout` mode) = the `'afterPerson'` layer or `window.AFTER_PERSON`.
- `08_safe_check.js` counts the frozen frame (`MV.frameAt`) as video, not text: transitions do not raise a false alarm (6.0).

## 4) Adding a new move (the bank reached 100: any addition gets a new number at the end)

0. Give it `role`, `energy`, `families` and `cues` in the catalog. **Weak families first**: run `plan --dry` for each family and see where the options are few.
1. A new function in `moves.js` with the same shape `FX.<id>(ctx, t, o)`, colors from `ctx.P`.
2. A catalog line **with a new number at the end**. ⛔ Never renumber the old ones: people have memorized the numbers.
3. A 4 s preview at half resolution: `previews/NN.mp4`, drawn from the function itself, not from other code.
4. The source in `CREDITS.md`, a link you opened yourself.

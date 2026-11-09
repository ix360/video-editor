<!-- Shared reference — writing the script (used by the script-writer skill and the /start orchestrator) -->

# Writing the script — hook first, story in the middle, one clear call to action

A short video is won or lost in the first 2 seconds and remembered by its last line. This file is the method. The output is `<work>/script.md`.

## 0. What you need to know (ask once, in one message — guess the rest)

| Need | Default if they don't say |
|---|---|
| **Topic / offer** | — (the only thing you must have) |
| **Goal** — sell · get leads · teach · grow followers · announce | grow followers |
| **Audience** — who, and what they already feel | infer from the topic, say it back in one line |
| **Platform** — Reels / TikTok / Shorts / YouTube / LinkedIn | vertical 9:16 short |
| **Length** | 30–45 s |
| **On camera, or voice only?** | voice only |
| **The action** they want at the end (follow, comment a word, DM, link, buy) | follow + comment a word |

Say your reading of it back in one sentence ("A 40-second vertical video that teaches freelancers one pricing mistake, ending with 'comment PRICE'") and go. Don't interview them.

## 1. The three parts

### Part 1 — The hook (first 1–3 seconds, ≤ 12 words)

**Rules**
- **Start in the middle.** No greeting, no "today I'm going to…", no name, no "in this video". The first word already carries the point.
- **One promise or one tension** — never both a list and a story.
- Spoken in the same words the viewer would say to themselves.
- If it still works with the first sentence deleted, delete the first sentence.

**Pick a formula (write 3 hooks, each from a different formula, let the user choose):**

| Formula | Pattern | Example |
|---|---|---|
| **Bold claim** | A true thing most people believe the opposite of | "Your editing isn't why nobody watches." |
| **Stop doing** | Names the mistake and the cost | "Stop starting videos with your name." |
| **Number + result** | A specific, believable number | "Three seconds decide if they stay." |
| **Open question** | A question the viewer can't answer yet | "Why do the best videos start in the middle?" |
| **Before → after** | Shows the jump, hides the how | "Zero views to 40,000 — one change." |
| **Secret / insider** | What the pros do and don't say | "Editors never tell you this about captions." |
| **Direct address** | Calls out the exact person | "If you sell online and post daily, listen." |
| **Pattern break** | Odd, concrete, visual | "This is a $0 camera." |

Never promise what the video doesn't deliver (it kills retention in the second half and the account's trust).

### Part 2 — The story (the body)

Use one of these skeletons. **One idea per video.** One sentence = one idea = one breath (6–14 words).

| Skeleton | Beats | Use for |
|---|---|---|
| **PAS** | Problem → Agitate (what it costs) → Solution | Ads, offers |
| **Mistake → Fix → Proof** | The mistake · why it hurts · the fix in 1–3 steps · a result | Teaching, authority |
| **Story arc** | Normal → Trouble → Turn → Result → Lesson | Personal, trust |
| **Myth → Truth** | The myth · why it's wrong · the truth · what to do | Contrarian, shares |
| **List with a twist** | 3 items, the third is the surprise | Saves, quick tips |
| **Demo** | Result first → how in 3 steps → result again | Products, apps |

**Retention tools**
- **Open a loop** in the hook and close it only at the end ("…and the third one surprised me").
- **Re-hook every 8–10 s:** a turn, a number, a "but", a question. A flat 15-second stretch loses people.
- **Concrete over abstract:** a name, a number, a place, an object beats a concept.
- **Show, don't explain:** every line should be able to have a picture (see §3).
- Cut every sentence that doesn't move the viewer one step closer to the promise.

### Part 3 — The call to action (last 2–4 seconds)

- **One action only.** Two asks = no ask.
- **Direct and specific:** "Comment PRICE and I'll send it", "Follow for one tip a day", "Link in my bio" — never "if you liked it, maybe…".
- **Give a reason** for the action ("so you don't miss part 2").
- **Match the goal:** sell → link/DM · leads → comment a word · grow → follow · teach → save/share.
- Optional **micro-CTA** at ~60% ("save this for later") only if the video is 45 s+. Never in the first 5 s.
- The CTA is also the **end card** text. Replace the engine's default end card (it is an ad for this skill) with the user's own: set `theme.json → outro`.

## 2. Length and pace

| Language | Words per second (natural speech) | 30 s | 45 s | 60 s |
|---|---|---|---|---|
| English | 2.5 | ~75 | ~110 | ~150 |
| Arabic / French / Spanish / Portuguese | 2.2–2.4 | ~68 | ~100 | ~135 |

Count the words, don't guess. Over budget → cut, don't speed up the voice.

## 3. Write for the eye too (the shot list)

Next to every line, decide what the viewer **sees**. This is what makes the film hybrid instead of all-graphics:

| Visual | When | Source |
|---|---|---|
| `person` | The speaker on camera (hook and CTA are best on camera) | their footage |
| `graphic` | A number, a comparison, a step, a diagram, a word being emphasised | the motion engine |
| `image` | A concrete object / place / person / mood | stock → Gemini → Flow (`references/stock.md`, `references/gen-scenes.md`) |
| `clip` | A real action or a place that moves | stock clip → Flow |
| `screen` | A website or app | `references/web-app-explainer.md` |

Rule of thumb: **never more than ~4 seconds of the same visual type in a row**; the hook line and the CTA line each get their own visual.

## 4. The output format (`<work>/script.md`)

```markdown
# <working title>
Goal: … · Audience: … · Platform: … · Length: ~40 s · Voice: voice-only | on camera | their mp3

## Hook options (the chosen one is marked ✅)
1. ✅ "…"   (formula: stop-doing)
2. "…"
3. "…"

## Script
| # | Time | Spoken line | Visual | Visual note / asset prompt |
|---|------|-------------|--------|----------------------------|
| 1 | 0–3 | "…" | person | hook, direct to camera |
| 2 | 3–8 | "…" | graphic | the big number, counts up |
| 3 | 8–13 | "…" | image | "a freelancer at a desk at night, laptop glow, cinematic" |
| … |
| N | 38–42 | "…CTA…" | person | end card: <the CTA word> |

## Spoken text only (what the voice reads, no notes)
…
Words: 112 · est. 44 s
```

## 5. Checklist before showing it (run it silently, fix, then show)

- [ ] The first word is not a greeting, a name or "today".
- [ ] The hook makes a promise the body keeps.
- [ ] One idea. One CTA. The CTA is the last spoken thing.
- [ ] Every sentence ≤ 14 words and can be said in one breath.
- [ ] Numbers and names are real — nothing invented. If a fact needs a source, mark it `[source?]` and ask.
- [ ] Word count fits the length.
- [ ] Spoken text has no stage directions, no emoji, no parentheses (numbers written as the voice should say them).
- [ ] No two same-type visuals in a row for more than ~4 s.

Then show: **the 3 hooks first (let them pick), then the full script.** One round of edits is normal; apply them and re-check the checklist.

## 6. If they bring their own script
Don't rewrite it. Run the checklist and report only what fails ("Your first line is a greeting — here are 3 stronger openings. The CTA asks for two things — keep 'comment PRICE'"). Apply only what they approve.

## 7. Adding another writing method
If the user installs another script-writing skill they like (a storytelling framework, a hook library), use it for Parts 1–3 and still finish with §3–§5 here, so the script always leaves with a shot list and the checklist done.

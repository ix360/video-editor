#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Where is this video project? — the memory of the /start orchestrator.

  python3 42_start.py set <work> key=value [key=value ...]     saves the brief into <work>/brief.json
        keys: topic goal audience platform length format voice cta language   (any key is allowed)
  python3 42_start.py status <work>                            prints the stages done / missing and the NEXT step (JSON with --json)

Stages (in order): brief → script → voice → theme → assets → build.  `assets` is optional (graphic-only films skip it).
The files it looks for:  brief.json · script.md · vo.mp3 (or a talking video: a.wav / input.*) · theme.json · gen.json or stock/credits.json · final.mp4 (or out.mp4 / output*.mp4) at the top level.
Python standard library only."""
import sys, os, json, glob

STAGES = ["brief", "script", "voice", "theme", "assets", "build"]
HINT = {
    "brief": "ask the one-question brief (topic, goal, platform, length, on camera or not) and save it with `set`",
    "script": "write the script with the script-writer skill (hook → story → CTA) and save it as script.md",
    "voice": "get the voice: an attached mp3 of the user, their ElevenLabs voice, or the footage's own audio",
    "theme": "run the taste page / theme step (references/start.md, step 0.5 and 1)",
    "assets": "fill the scenes that need photos or clips (stock → Gemini → Flow); skip if the film is graphics only",
    "build": "build the film with the chosen skill, show frames, deliver the file",
}


def _has(work, *pats):
    return any(glob.glob(os.path.join(work, p)) for p in pats)


def stages(work):
    brief = {}
    p = os.path.join(work, "brief.json")
    if os.path.isfile(p):
        try: brief = json.load(open(p, encoding="utf-8"))
        except Exception: brief = {}
    done = {
        "brief": bool(brief),
        "script": _has(work, "script.md") and os.path.getsize(os.path.join(work, "script.md")) > 20,
        "voice": _has(work, "vo.mp3", "vo.wav", "a.wav", "input.*"),
        "theme": _has(work, "theme.json"),
        "assets": _has(work, "gen.json", "stock/credits.json", "gen/*"),
        "build": _has(work, "final*.mp4", "*_final.mp4", "out.mp4", "output*.mp4"),
    }
    optional = {"assets"} if brief.get("format") in ("graphics", "motion-graphics") else set()
    return brief, done, optional


def status(work, as_json):
    if not os.path.isdir(work): sys.exit("❌ not a folder: %s" % work)
    brief, done, optional = stages(work)
    nxt = next((s for s in STAGES if not done[s] and s not in optional), None)
    if as_json:
        print(json.dumps({"done": done, "next": nxt, "hint": HINT.get(nxt, "all done — deliver the file"), "brief": brief}, ensure_ascii=False)); return
    for s in STAGES:
        mark = "✅" if done[s] else ("➖" if s in optional else "⬜")
        print("%s %s" % (mark, s))
    print("NEXT:", ("%s — %s" % (nxt, HINT[nxt])) if nxt else "all done — deliver the file")


def set_(work, kv):
    os.makedirs(work, exist_ok=True)
    p = os.path.join(work, "brief.json")
    brief = json.load(open(p, encoding="utf-8")) if os.path.isfile(p) else {}
    for item in kv:
        if "=" not in item: sys.exit("❌ expected key=value, got: %s" % item)
        k, v = item.split("=", 1); brief[k.strip()] = v.strip()
    json.dump(brief, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("✅ saved", p)


def main():
    a = sys.argv[1:]
    if len(a) < 2: sys.exit(__doc__)
    if a[0] == "status": return status(a[1], "--json" in a)
    if a[0] == "set": return set_(a[1], a[2:])
    sys.exit(__doc__)


if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    main()

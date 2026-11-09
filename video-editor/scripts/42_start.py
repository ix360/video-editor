#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Where is this video project? — the memory of the /start orchestrator.

  python3 42_start.py set <work> key=value [key=value ...]     saves the brief into <work>/brief.json
        keys: topic goal audience platform length format voice cta language   (any key is allowed)
  python3 42_start.py status <work>                            prints the stages done / missing and the NEXT step (JSON with --json)
  python3 42_start.py audit <project>                          motion film only: checks the scenes really use the move bank (FX.*), camera moves/zooms and the saved plan. Exit 0 = pass, 3 = fix it before rendering

Stages (in order): brief → script → voice → theme → assets → build.  `assets` is optional (graphic-only films skip it).
The files it looks for:  brief.json · script.md · vo.mp3 (or a talking video: a.wav / input.*) · theme.json · gen.json or stock/credits.json · final.mp4 (or out.mp4 / output*.mp4) at the top level.
Python standard library only."""
import sys, os, json, glob

STAGES = ["brief", "script", "voice", "theme", "moves", "assets", "build"]
HINT = {
    "brief": "ask the one-question brief (topic, goal, platform, length, on camera or not) and save it with `set`",
    "script": "write the script with the script-writer skill (hook → story → CTA) and save it as script.md",
    "voice": "get the voice: an attached mp3 of the user, their ElevenLabs voice, or the footage's own audio",
    "theme": "run the taste page / theme step (references/start.md, step 0.5 and 1)",
    "moves": "make the film's move palette: python3 scripts/35_moves.py plan --title \"…\" --cues … > <work>/moves_plan.json (mandatory — references/moves.md)",
    "assets": "fill the scenes that need photos or clips (stock → Gemini → Flow); skip if the film is graphics only",
    "build": "build the film with the chosen skill, show frames, deliver the file",
}


def _has(work, *pats):
    return any(glob.glob(os.path.join(work, p)) for p in pats)


def _built(work):
    """A finished film: final*.mp4 / *-final.mp4 / out.mp4 / output*.mp4, or any top-level mp4 that isn't a source clip, or <project>/renders/final*.mp4."""
    import fnmatch
    src = ("input", "src", "raw", "img_", "clip", "source")
    for f in glob.glob(os.path.join(work, "*.mp4")):
        n = os.path.basename(f).lower()
        if not n.startswith(src): return True
    return _has(work, "*/renders/final*.mp4", "renders/final*.mp4")


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
        "moves": _has(work, "moves_plan.json"),
        "assets": _has(work, "gen.json", "stock/credits.json", "gen/*", "*/assets/clips/*", "*/assets/*.jpg", "assets/clips/*"),
        "build": _built(work),
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


CAMERA = {"pushIn", "pullOut", "handheld", "kenBurns", "snapZoom", "punchCut", "dollyZoom", "rackFocus", "parallax", "shake", "crossZoom", "zoomWipe", "dotZoom", "tilt3D", "orbit", "craneUp"}


def _camera_ids():
    """The camera moves = the catalog's cat=="camera" ids (plus the static list)."""
    try:
        cat = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "motion", "moves", "catalog.json"), encoding="utf-8"))
        return CAMERA | {m["id"] for m in cat["moves"] if m.get("cat") == "camera"}
    except Exception:
        return CAMERA


def audit(proj):
    """A motion film must be built WITH the move bank (zooms, camera moves, kinetic type) — not hand-drawn graphics only."""
    import re
    sc = sorted(glob.glob(os.path.join(proj, "scenes", "*.js")))
    sc = [f for f in sc if os.path.basename(f) != "stage.js"]
    if not sc: sys.exit("❌ no scenes/*.js in %s" % proj)
    problems, used_all, cam_scenes = [], set(), 0
    for f in sc:
        src = open(f, encoding="utf-8").read()
        ids = set(re.findall(r"\bFX\.(\w+)\s*\(", src)); used_all |= ids   # real calls only, not a mention in a comment
        cam = ids & _camera_ids()
        if not ids: problems.append("%s uses no FX.* move at all" % os.path.basename(f))
        if cam: cam_scenes += 1
    if cam_scenes < max(1, int(len(sc) * 0.7 + 0.5)):
        problems.append("only %d of %d scenes have a camera move/zoom (%s) — aim for at least 70%%, with a punch-in on the hook and on key words" % (cam_scenes, len(sc), ", ".join(sorted(CAMERA)[:6]) + "…"))
    if len(used_all) < 4: problems.append("only %d different moves used (%s) — the plan's 3 core moves + accents should all appear" % (len(used_all), ", ".join(sorted(used_all)) or "none"))
    plan_p = os.path.join(os.path.dirname(os.path.abspath(proj)), "moves_plan.json")
    plan_ids = set()
    try:
        raw = open(plan_p, encoding="utf-8").read(); raw = raw[raw.index("{"):]
        pl = json.loads(raw); plan_ids = set(pl.get("core", [])) | set(pl.get("accents", []))
    except Exception:
        problems.append("no readable moves_plan.json next to the project (run 35_moves.py plan … > moves_plan.json)")
    if plan_ids:
        miss = sorted(plan_ids - used_all)
        if miss: problems.append("planned moves never used: %s" % ", ".join(miss))
    # Arabic literals in a film whose script isn't Arabic = a leftover default/sample text
    try:
        sj = open(os.path.join(proj, "script.json"), encoding="utf-8").read()
        if not re.search(r"[\u0600-\u06FF]", sj):
            for f in sc:
                if re.search(r"[\u0600-\u06FF]", re.sub(r"//.*|/\*[\s\S]*?\*/", "", open(f, encoding="utf-8").read())):
                    problems.append("%s contains Arabic text but the script is not Arabic — replace it" % os.path.basename(f))
    except Exception:
        pass
    print("Scenes: %d · camera/zoom scenes: %d · distinct moves: %s" % (len(sc), cam_scenes, ", ".join(sorted(used_all)) or "none"))
    if problems:
        print("❌ AUDIT FAILED — fix before rendering:"); [print("  -", p) for p in problems]; sys.exit(3)
    print("✅ audit passed")


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
    if a[0] == "audit": return audit(a[1])
    if a[0] == "set": return set_(a[1], a[2:])
    sys.exit(__doc__)


if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    main()

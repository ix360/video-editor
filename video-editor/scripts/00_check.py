#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Setup check — verifies what can be checked from the machine; Claude does the rest (references/setup-check.md).

  python3 00_check.py show                 summary: language, assets mode, which keys exist (values never printed), tools
  python3 00_check.py set-assets api|subscription     saves the user's choice of image/clip source
  python3 00_check.py gemini               tests the AI Studio key with a free read-only call (no generation, no spend)
Exit: 0 all good · 3 something missing (see the report) · 1 usage error
Python standard library only."""
import sys, os, json, shutil, subprocess, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _lang, _setup


def env(name):
    if os.environ.get(name): return os.environ[name]
    for d in (os.getcwd(), os.path.expanduser("~")):
        p = os.path.join(d, ".env")
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                if line.startswith(name + "="): return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def ok(b): return "✅" if b else "—"


def gemini():
    k = env("GEMINI_API_KEY") or env("GOOGLE_API_KEY")
    if not k: print("— no GEMINI_API_KEY (free key: aistudio.google.com → Get API key)"); return False
    r = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models?pageSize=1", headers={"x-goog-api-key": k})
    try:
        urllib.request.urlopen(r, timeout=20); print("✅ AI Studio key works"); return True
    except urllib.error.HTTPError as e:
        print("❌ AI Studio key rejected (%s) — check it was copied in full and is enabled" % e.code); return False
    except Exception as e:
        print("⚠️ Could not reach Google (%s) — check the connection" % str(e)[:80]); return False


def show():
    mode = _setup.assets_mode(); lang_saved = os.path.exists(os.path.join(os.path.dirname(str(_setup._path())), "lang.json"))
    miss = 0
    print("Language:      %s %s" % (_lang.get(), "" if lang_saved else "(default — not chosen yet)"))
    print("Assets source: %s" % (mode or "— not chosen yet"))
    if not mode: miss += 1
    print("\nMachine tools:")
    for t in ("ffmpeg", "ffprobe", "python3", "node"):
        f = shutil.which(t); print("  %s %s" % (ok(f), t)); miss += 0 if f else (1 if t in ("ffmpeg", "ffprobe") else 0)
    try: import whisper; w = True
    except Exception: w = False
    print("  %s whisper (transcription — 00_setup.sh --install gets it)" % ok(w))
    print("\nKeys (free or optional):")
    for n, why in (("GEMINI_API_KEY", "AI Studio images"), ("FAL_KEY", "paid clips/images"), ("PEXELS_API_KEY", "stock"), ("PIXABAY_API_KEY", "stock"), ("UNSPLASH_ACCESS_KEY", "stock photos"), ("ELEVENLABS_API_KEY", "upload a voice-clone sample")):
        print("  %s %-20s %s" % (ok(env(n)), n, why))
    if mode == "api" and not (env("GEMINI_API_KEY") or env("GOOGLE_API_KEY")):
        print("\n⚠️ You chose api but there is no GEMINI_API_KEY."); miss += 1
    print("\nClaude checks by itself: ElevenLabs connected · Chrome extension · Google Flow sign-in (references/setup-check.md)")
    return 0 if not miss else 3


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == "show": sys.exit(show())
    if a[0] == "gemini": sys.exit(0 if gemini() else 3)
    if a[0] == "set-assets" and len(a) > 1 and a[1] in _setup.MODES:
        _setup.save(assets=a[1]); print(a[1]); return
    sys.exit(__doc__)


if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    main()

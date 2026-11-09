#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The user's own voice from a file THEY attach (mp3 / m4a / wav / voice note) — no recorder page.

  python3 39_voice_sample.py prepare <file> [--out DIR] [--name my-voice]
        checks the file (duration, loudness, silence) and writes a clean 44.1k mono wav to DIR (default ~/.video-ad-editor/voice).
        Prints one JSON line: {ok, path, seconds, advice}.  Exit: 0 usable · 2 too short / empty · 1 error
  python3 39_voice_sample.py upload <file> [--name "My voice"]
        uploads the sample to ElevenLabs (instant clone) and prints the voice_id.  Needs ELEVENLABS_API_KEY (env or .env) and a plan with cloning.
  python3 39_voice_sample.py voices
        lists the ElevenLabs voices of the account (name · voice_id · category) through the REST API — for runtimes WITHOUT the ElevenLabs connector.  Needs ELEVENLABS_API_KEY.
  python3 39_voice_sample.py speak --voice <voice_id> (--text-file <f> | --text "...") [--out vo.mp3] [--model eleven_multilingual_v2] [--yes]
        text-to-speech through the REST API. Without --yes it only prints the character count (nothing is sent or billed); run it with --yes after the user agrees.
  python3 39_voice_sample.py script
        prints a short reading text to give the user if they have nothing to read (covers varied sounds and tones)

Two ways to use the attached file:
  1. AS the narration — they read the finished script; the file becomes <work>/vo.mp3 (no cloning, no credits).
  2. AS a clone sample — 1–3 minutes of anything, then `upload` (or they upload it at elevenlabs.io themselves).

Python standard library + ffmpeg only."""
import sys, os, json, subprocess, urllib.request, urllib.error, uuid, re
from pathlib import Path

HOME = Path(os.environ.get("VAE_HOME") or (Path.home() / ".video-ad-editor"))

READING = {
    "ar": "السلام عليكم ورحمة الله. اليوم بحكي لكم عن شي استفدت منه بحياتي. أول شي، لازم تبدأ بخطوة صغيرة. ثاني شي، لا تقارن نفسك بغيرك. وثالث شي، خلّ عندك صبر. تعالوا نبدأ، وشوفوا النتيجة بعد أسبوع واحد بس!",
    "en": "Hi everyone. Today I want to share something that changed how I work. First, start small. Second, don't compare yourself to anyone else. Third, be patient. Let's begin, and check back in just one week. Are you ready? Let's go!",
}


def env(name):
    if os.environ.get(name): return os.environ[name]
    for d in (os.getcwd(), os.path.expanduser("~")):
        p = os.path.join(d, ".env")
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                if line.startswith(name + "="): return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def arg(a, n, d=None):
    return a[a.index(n) + 1] if n in a and a.index(n) + 1 < len(a) else d


def _run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def prepare(a):
    if not a: sys.exit("usage: 39_voice_sample.py prepare <file> [--out DIR] [--name N]")
    src = a[0]
    if not os.path.isfile(src): sys.exit("❌ file not found: %s" % src)
    out = Path(arg(a, "--out", str(HOME / "voice"))).expanduser(); out.mkdir(parents=True, exist_ok=True)
    name = re.sub(r"[^A-Za-z0-9_.-]", "_", arg(a, "--name", "my-voice"))
    dst = out / (name + ".wav")
    r = _run(["ffmpeg", "-y", "-v", "error", "-i", src, "-vn", "-ac", "1", "-ar", "44100", "-c:a", "pcm_s16le", str(dst)])
    if r.returncode != 0 or not dst.exists():
        print(json.dumps({"ok": False, "error": "ffmpeg could not read this file", "detail": r.stderr[-200:]})); sys.exit(1)
    d = _run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(dst)])
    try: secs = float(d.stdout.strip())
    except ValueError: secs = 0.0
    # loudness: mean volume (dB) — very quiet = far from the mic
    v = _run(["ffmpeg", "-v", "info", "-i", str(dst), "-af", "volumedetect", "-f", "null", "-"])
    m = re.search(r"mean_volume:\s*(-?[\d.]+) dB", v.stderr)
    mean = float(m.group(1)) if m else None
    advice = []
    if secs < 5: advice.append("empty or too short")
    elif secs < 60: advice.append("fine as the narration; for a clone sample 1–3 minutes works much better")
    if mean is not None and mean < -35: advice.append("very quiet — mic too far or low input level; ask for a re-record closer to the mic")
    ok = secs >= 5
    print(json.dumps({"ok": ok, "path": str(dst), "seconds": round(secs, 1), "mean_db": mean, "advice": "; ".join(advice) or "good"}, ensure_ascii=False))
    sys.exit(0 if ok else 2)


def upload(a):
    if not a: sys.exit("usage: 39_voice_sample.py upload <file> [--name N]")
    f = a[0]; name = arg(a, "--name", "My voice"); key = env("ELEVENLABS_API_KEY")
    if not key: sys.exit("❌ No ELEVENLABS_API_KEY (env or .env). Alternative: upload the file yourself at elevenlabs.io → Voices → Add voice → Instant voice clone.")
    b = uuid.uuid4().hex; data = open(f, "rb").read(); parts = []
    for k, v in (("name", name), ("remove_background_noise", "true")):
        parts.append(('--%s\r\nContent-Disposition: form-data; name="%s"\r\n\r\n%s\r\n' % (b, k, v)).encode())
    parts.append(('--%s\r\nContent-Disposition: form-data; name="files"; filename="%s"\r\nContent-Type: application/octet-stream\r\n\r\n' % (b, os.path.basename(f))).encode() + data + b"\r\n")
    parts.append(("--%s--\r\n" % b).encode())
    r = urllib.request.Request("https://api.elevenlabs.io/v1/voices/add", data=b"".join(parts), headers={"xi-api-key": key, "Content-Type": "multipart/form-data; boundary=" + b})
    try: res = json.load(urllib.request.urlopen(r, timeout=180))
    except urllib.error.HTTPError as e: sys.exit("❌ %s %s\n   (usually: the plan has no instant cloning, or the sample is too short / not clean)" % (e.code, e.read()[:300].decode("utf-8", "ignore")))
    print("✅ voice_id:", res.get("voice_id"))


def _api(path, key, body=None, accept="application/json"):
    r = urllib.request.Request("https://api.elevenlabs.io" + path, data=(json.dumps(body).encode() if body is not None else None),
                               headers={"xi-api-key": key, "Content-Type": "application/json", "Accept": accept})
    return urllib.request.urlopen(r, timeout=300)


def voices(a):
    key = env("ELEVENLABS_API_KEY")
    if not key: sys.exit("❌ No ELEVENLABS_API_KEY (env or .env). Create one at elevenlabs.io → Developers → API keys; never paste it into the chat.")
    try: res = json.load(_api("/v1/voices", key))
    except urllib.error.HTTPError as e: sys.exit("❌ %s %s" % (e.code, e.read()[:200].decode("utf-8", "ignore")))
    for v in res.get("voices", []): print("%-34s %s  %s" % (v.get("name", "?"), v.get("voice_id"), v.get("category", "")))


def speak(a):
    vid = arg(a, "--voice"); out = arg(a, "--out", "vo.mp3"); model = arg(a, "--model", "eleven_multilingual_v2")
    tf = arg(a, "--text-file"); text = open(tf, encoding="utf-8").read() if tf else arg(a, "--text")
    if not vid or not text: sys.exit("usage: 39_voice_sample.py speak --voice <voice_id> (--text-file <f> | --text \"...\") [--out vo.mp3] [--yes]")
    n = len(text.strip())
    if "--yes" not in a:
        print(json.dumps({"characters": n, "voice": vid, "model": model, "sent": False, "note": "ElevenLabs bills per character (see the user's plan). Tell the user, then re-run with --yes."})); return
    key = env("ELEVENLABS_API_KEY")
    if not key: sys.exit("❌ No ELEVENLABS_API_KEY (env or .env).")
    try: data = _api("/v1/text-to-speech/%s?output_format=mp3_44100_128" % vid, key, {"text": text.strip(), "model_id": model}, "audio/mpeg").read()
    except urllib.error.HTTPError as e: sys.exit("❌ %s %s" % (e.code, e.read()[:300].decode("utf-8", "ignore")))
    open(out, "wb").write(data); print("✅ %s (%d characters, %.0f KB) — one take; another take is a new charge" % (out, n, len(data) / 1024))


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == "prepare": return prepare(a[1:])
    if a[0] == "upload": return upload(a[1:])
    if a[0] == "voices": return voices(a[1:])
    if a[0] == "speak": return speak(a[1:])
    if a[0] == "script":
        try: import _lang; print(READING.get(_lang.get(), READING["en"]))
        except Exception: print(READING["en"])
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    main()

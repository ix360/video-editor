#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Record your voice in the browser (a clone sample) — a local page; audio leaves your machine only if you run --upload.

  python3 39_record_voice.py record [--name my-voice] [--out DIR] [--no-open] [--timeout 600]
        opens a page with "Record / Stop" and saves <DIR>/<name>.wav (44.1k mono).  Default DIR=~/.video-ad-editor/voice
        The line "URL: …" is printed first — give it to the user if the browser didn't open.   Exit: 0 saved · 2 timed out · 1 error
  python3 39_record_voice.py upload <file.wav|mp3> [--name my-voice]
        uploads the sample to ElevenLabs (instant clone) and prints the voice_id.  Needs ELEVENLABS_API_KEY (env or .env) and a plan with cloning.
  python3 39_record_voice.py script            prints a suggested reading text (covers varied sounds and tones)

Sample tip: one to three minutes, a quiet room, the mic close, a natural tone, no music. Longer and cleaner = closer to the original.
No external libraries — Python standard library + ffmpeg."""
import sys, os, json, time, threading, subprocess, urllib.request, urllib.error, uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HOME = Path(os.environ.get("VAE_HOME") or (Path.home() / ".video-ad-editor"))

READING = {
    "ar": "السلام عليكم ورحمة الله. اليوم بحكي لكم عن شي استفدت منه بحياتي. أول شي، لازم تبدأ بخطوة صغيرة. ثاني شي، لا تقارن نفسك بغيرك. وثالث شي، خلّ عندك صبر. تعالوا نبدأ، وشوفوا النتيجة بعد أسبوع واحد بس!",
    "en": "Hi everyone. Today I want to share something that changed how I work. First, start small. Second, don't compare yourself to anyone else. Third, be patient. Let's begin, and check back in just one week. Are you ready? Let's go!",
}

PAGE = """<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Record your voice</title>
<style>body{font:17px/1.6 system-ui,sans-serif;max-width:640px;margin:40px auto;padding:0 20px;background:#101828;color:#f5f7fa}
button{font:600 18px system-ui;padding:14px 28px;border:0;border-radius:12px;background:#f2b33d;color:#101828;cursor:pointer;margin:6px 6px 6px 0}
button:disabled{opacity:.4}.box{background:#1d2939;padding:16px 20px;border-radius:12px;margin:16px 0}#t{font:700 28px ui-monospace,monospace}</style>
<h2>🎙️ Record your voice sample</h2>
<div class="box"><b>Tips:</b> quiet room · mic close · natural tone · 1–3 minutes. Read the text below or speak freely.</div>
<div class="box" id="txt" style="white-space:pre-wrap">__TEXT__</div>
<div id="t">00:00</div>
<button id="go">● Record</button><button id="stop" disabled>■ Stop &amp; save</button>
<p id="msg"></p>
<script>
let rec,chunks=[],t0,tm;const $=id=>document.getElementById(id);
$('go').onclick=async()=>{try{const s=await navigator.mediaDevices.getUserMedia({audio:{echoCancellation:false,noiseSuppression:true,autoGainControl:false}});
rec=new MediaRecorder(s);chunks=[];rec.ondataavailable=e=>chunks.push(e.data);
rec.onstop=async()=>{s.getTracks().forEach(x=>x.stop());clearInterval(tm);$('msg').textContent='Saving…';
const r=await fetch('/save',{method:'POST',body:new Blob(chunks,{type:rec.mimeType})});$('msg').textContent=r.ok?'✅ Saved — you can close this tab.':'❌ '+await r.text();};
rec.start();t0=Date.now();tm=setInterval(()=>{const s=Math.floor((Date.now()-t0)/1000);$('t').textContent=String(Math.floor(s/60)).padStart(2,'0')+':'+String(s%60).padStart(2,'0')},250);
$('go').disabled=true;$('stop').disabled=false;}catch(e){$('msg').textContent='❌ Mic blocked: '+e.message}};
$('stop').onclick=()=>{rec.stop();$('stop').disabled=true};
</script></html>"""


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


def record(a):
    name = arg(a, "--name", "my-voice"); out = Path(arg(a, "--out", str(HOME / "voice"))); out.mkdir(parents=True, exist_ok=True)
    timeout = int(arg(a, "--timeout", 600)); done = threading.Event(); result = {}
    try:
        import _lang; text = READING.get(_lang.get(), READING["en"])
    except Exception:
        text = READING["en"]
    page = PAGE.replace("__TEXT__", text).encode("utf-8")

    class H(BaseHTTPRequestHandler):
        def log_message(self, *x): pass
        def do_GET(self):
            self.send_response(200); self.send_header("Content-Type", "text/html; charset=utf-8"); self.end_headers(); self.wfile.write(page)
        def do_POST(self):
            if self.path != "/save": self.send_error(404); return
            raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            tmp = out / (name + ".webm"); tmp.write_bytes(raw); wav = out / (name + ".wav")
            r = subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-ac", "1", "-ar", "44100", str(wav)], capture_output=True, text=True)
            ok = r.returncode == 0 and wav.exists() and wav.stat().st_size > 1000
            if ok: tmp.unlink(missing_ok=True); result["path"] = str(wav)
            self.send_response(200 if ok else 500); self.end_headers(); self.wfile.write(b"ok" if ok else (r.stderr or "empty recording").encode()[:300])
            if ok: done.set()

    srv = ThreadingHTTPServer(("127.0.0.1", 0), H); url = "http://127.0.0.1:%d/" % srv.server_address[1]
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    print("URL:", url, flush=True)
    if "--no-open" not in a:
        try:
            import webbrowser; webbrowser.open(url)
        except Exception: pass
    if not done.wait(timeout): print("⏱️ Timed out with no recording", file=sys.stderr); return 2
    dur = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", result["path"]], capture_output=True, text=True).stdout.strip()
    print("✅ %s (%.0f s)" % (result["path"], float(dur or 0)))
    return 0


def upload(a):
    if not a: sys.exit("usage: 39_record_voice.py upload <file> [--name N]")
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


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == "record": sys.exit(record(a[1:]))
    if a[0] == "upload": return upload(a[1:])
    if a[0] == "script":
        try: import _lang; print(READING.get(_lang.get(), READING["en"]))
        except Exception: print(READING["en"])
        return
    sys.exit(__doc__)


if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    main()

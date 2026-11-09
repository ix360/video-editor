#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🖼️ 17_gen_scenes.py — مشاهد مولّدة (v3.2): صور ومقاطع قصيرة يولّدها الذكاء الاصطناعي وتدخل الفيديو كمشاهد، والمحرّك يرسم فوقها.

الاستخدام:
  python3 scripts/17_gen_scenes.py <work> cost      # كم بتكلّف الأصول المطلوبة (بلا توليد)
  python3 scripts/17_gen_scenes.py <work> fetch     # يولّد الناقص فقط → <work>/gen/ ويكتب genFrames بـstudio.json
  python3 scripts/17_gen_scenes.py <work> status    # شنو جاهز وشنو ناقص

الملف: <work>/gen.json
{
  "assets": [
    {"k":"desk",  "kind":"video", "prompt":"...", "dur":5, "ar":"9:16"},
    {"k":"paper", "kind":"image", "prompt":"...", "ar":"3:4"}
  ],
  "scenes": [ {"s":"w:منو","e":"w:الجواب+","k":"paper","mode":"card","draw":[{"op":"vs","at":"w:ولا","l":"ورقة","r":"الجوال"}]} ]
}
Providers (cheapest first):
  • images: Google AI Studio (Gemini) if GEMINI_API_KEY exists (uses the free allowance if available), otherwise fal.ai (FAL_KEY).
  • clips: fal.ai (FAL_KEY) — or Google Flow in the browser (references/google-flow.md) then `import` below.
  • GEN_BACKEND=auto|gemini|fal|flow forces the choice (default auto). The saved assets mode (00_check.py set-assets) decides otherwise.
Keys come from the environment or a .env file (work folder, project or home).
  python3 17_gen_scenes.py <work> import <k> <file.mp4|jpg|png>   registers a ready file (e.g. from Flow or stock) as asset <k> -> frames/image in gen/
الموديلات: صورة = fal-ai/nano-banana (≈0.04$) · مقطع = fal-ai/wan-25-preview/text-to-video 720p (≈0.05$/ث).
⛔ يولّد فقط اللي ما هو موجود بمجلد gen/ (ما يعيد ولا يدفع مرتين). لو فشل طلب مرة، يوقف ويقول السبب — ما يكرّر.
"""
import sys, os, json, time, subprocess, urllib.request, urllib.error
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _setup

IMG_MODEL = "fal-ai/nano-banana"
VID_MODEL = "fal-ai/wan-25-preview/text-to-video"
IMG_COST, VID_COST_PER_S = 0.04, 0.05
NEG = "no readable text, no logos, no watermark"   # engine default only. Content rules (e.g. "no people", "no women") are the OWNER'S choice: theme.json -> "avoid": ["no people", ...]

def _neg(work):
    try: av = json.load(open(os.path.join(work, "theme.json"), encoding="utf-8")).get("avoid") or []
    except Exception: av = []
    return ", ".join([NEG] + [str(x) for x in av])

def _env(work, *names):
    """أول قيمة لأحد الأسماء من البيئة ثم .env (مجلد الشغل ← الحالي ← البيت)"""
    for n in names:
        if os.environ.get(n): return os.environ[n]
    for d in (work, os.getcwd(), os.path.expanduser("~")):
        p = os.path.join(d, ".env")
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                for n in names:
                    if line.startswith(n + "="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None

def _key(work): return _env(work, "FAL_KEY")
def _gkey(work): return _env(work, "GEMINI_API_KEY", "GOOGLE_API_KEY")

GEMINI_IMG = "gemini-2.5-flash-image"
GEMINI_AR = {"1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"}

def _backend(work):
    b = (os.environ.get("GEN_BACKEND") or "").lower()
    if not b and _setup.assets_mode() == "subscription": return "flow"     # they chose their subscription: Google Flow in the browser, no API
    b = b or "auto"
    if b == "flow": return "flow"
    if b == "fal": return "fal"
    if b == "gemini": return "gemini" if _gkey(work) else None
    return "gemini" if _gkey(work) else "fal"      # auto: Google first (free/cheaper), otherwise fal

def _gemini_image(key, prompt, ar, out_jpg):
    """AI Studio: gemini-2.5-flash-image -> an image at out_jpg (ffmpeg converts PNG to JPEG)"""
    import base64, tempfile
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseModalities": ["IMAGE"], **({"imageConfig": {"aspectRatio": ar}} if ar in GEMINI_AR else {})}}
    r = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent" % GEMINI_IMG,
                               data=json.dumps(body).encode(), headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    res = json.load(urllib.request.urlopen(r, timeout=180))
    parts = ((res.get("candidates") or [{}])[0].get("content") or {}).get("parts") or []
    data = next((p.get("inlineData") or p.get("inline_data") for p in parts if p.get("inlineData") or p.get("inline_data")), None)
    if not data: raise RuntimeError("Google returned no image (was the prompt refused?): " + json.dumps(res)[:200])
    tmp = tempfile.mktemp(suffix=".img")
    open(tmp, "wb").write(base64.b64decode(data["data"]))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-q:v", "2", out_jpg], check=True); os.remove(tmp)

def import_asset(work, k, src):
    """A ready file (clip/image from Flow or elsewhere) -> asset <k> in gen/"""
    if not os.path.exists(src): sys.exit("❌ File not found: " + src)
    g = os.path.join(work, "gen"); os.makedirs(g, exist_ok=True)
    if src.lower().endswith((".mp4", ".mov", ".webm", ".mkv")):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", "fps=30", "-q:v", "3", os.path.join(g, k + "_%04d.jpg")], check=True)
        print("✅ %s <- clip -> %d frames" % (k, frames_of(work, k)))
    else:
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-q:v", "2", os.path.join(g, k + ".jpg")], check=True)
        print("✅ %s <- image" % k)

def _post(url, key, body, timeout=120):
    r = urllib.request.Request(url, data=json.dumps(body).encode(), headers={"Authorization": "Key " + key, "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(r, timeout=timeout))

def _get(url, key, timeout=60):
    r = urllib.request.Request(url, headers={"Authorization": "Key " + key})
    return json.load(urllib.request.urlopen(r, timeout=timeout))

def _dl(url, path):
    urllib.request.urlretrieve(url, path)

def load(work):
    p = os.path.join(work, "gen.json")
    if not os.path.exists(p):
        sys.exit("❌ No gen.json in the work folder — write it first (format at the top of this file)")
    return json.load(open(p, encoding="utf-8"))

def have(work, a):
    g = os.path.join(work, "gen")
    if a.get("kind") == "video":
        return os.path.exists(os.path.join(g, a["k"] + "_0001.jpg"))
    return os.path.exists(os.path.join(g, a["k"] + ".jpg"))

def cost(assets, img_cost=IMG_COST):
    return sum((VID_COST_PER_S * float(a.get("dur", 5))) if a.get("kind") == "video" else img_cost for a in assets)

def frames_of(work, k):
    g = os.path.join(work, "gen"); n = 0
    while os.path.exists(os.path.join(g, "%s_%04d.jpg" % (k, n + 1))): n += 1
    return n

def write_studio(work, cfg):
    """يكتب scenes/genFrames بـstudio.json (يدمج بلا ما يمسح باقي الإعدادات)"""
    sp = os.path.join(work, "studio.json")
    st = json.load(open(sp, encoding="utf-8")) if os.path.exists(sp) else {}
    st["gen"] = cfg.get("scenes", [])
    st["genFrames"] = {a["k"]: frames_of(work, a["k"]) for a in cfg.get("assets", []) if a.get("kind") == "video"}
    json.dump(st, open(sp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return st

def main():
    if len(sys.argv) < 3: sys.exit(__doc__)
    work, cmd = sys.argv[1], sys.argv[2]
    if cmd == "import":
        if len(sys.argv) < 5: sys.exit("usage: 17_gen_scenes.py <work> import <k> <file>")
        import_asset(work, sys.argv[3], sys.argv[4])
        if os.path.exists(os.path.join(work, "gen.json")):   # reel/podcast flow: wire the asset into studio.json
            write_studio(work, load(work))
        else:   # motion film (no gen.json): the file is ready in gen/ — copy it to <project>/assets/ and declare it in project.json "images"
            print("ℹ️  No gen.json here (a motion film does not need one): the asset is ready in %s" % os.path.join(work, "gen"))
        return
    cfg = load(work); assets = cfg.get("assets", [])
    missing = [a for a in assets if not have(work, a)]
    be = _backend(work); gimg = 0.0 if be in ("gemini", "flow") else IMG_COST     # جوجل: حصة مجانية (تحقق من حدّك) — نحسبها صفر
    if cmd == "cost" and be == "flow":
        print("Assets: %d (missing %d) — subscription mode: Google Flow in the browser, no API cost (uses your daily Flow credits)" % (len(assets), len(missing)))
        for a in missing: print("  •", a["k"], a.get("kind", "image"))
        return
    if cmd == "cost":
        print("Assets: %d (missing %d) — estimated cost of the missing ones ≈ $%.2f (images via: %s)" % (len(assets), len(missing), cost(missing, gimg), be or "—"))
        for a in missing: print("  •", a["k"], a.get("kind", "image"), ("%ss" % a.get("dur", 5)) if a.get("kind") == "video" else "", "≈ %.2f$" % (VID_COST_PER_S * float(a.get("dur", 5)) if a.get("kind") == "video" else gimg))
        return
    if cmd == "status":
        for a in assets: print(("✅" if have(work, a) else "⏳"), a["k"], a.get("kind", "image"), (("%d frames" % frames_of(work, a["k"])) if a.get("kind") == "video" and have(work, a) else ""))
        write_studio(work, cfg); print("studio.json ← gen:", len(cfg.get("scenes", [])), "scenes"); return
    if cmd != "fetch": sys.exit(__doc__)
    if be == "flow":
        print("ℹ️ Your assets source = subscription (Google Flow). Not generating by API — generate the missing ones in the browser per references/google-flow.md, then for each asset:")
        for a in missing: print("   python3 scripts/17_gen_scenes.py %s import %s <downloaded file>   # %s" % (work, a["k"], a.get("kind", "image")))
        print("   (Want the API instead? python3 scripts/00_check.py set-assets api)")
        sys.exit(0)
    key, gkey = _key(work), _gkey(work)
    need_fal = any(a.get("kind") == "video" or be != "gemini" for a in missing)
    if need_fal and not key:
        sys.exit("❌ No FAL_KEY — needed for clips (and images if there is no GEMINI_API_KEY). Free alternatives: images -> an AI Studio key (GEMINI_API_KEY), clips -> Flow in the browser (references/google-flow.md) then `import`.")
    g = os.path.join(work, "gen"); os.makedirs(g, exist_ok=True)
    print("🎨 Generating %d assets (≈ $%.2f) — images via %s" % (len(missing), cost(missing, gimg), be))
    for a in missing:
        k, kind, prompt = a["k"], a.get("kind", "image"), a["prompt"].strip() + ", " + _neg(work)
        t0 = time.time()
        try:
            if kind == "video":
                dur = str(int(float(a.get("dur", 5))))
                q = _post("https://queue.fal.run/" + VID_MODEL, key, {"prompt": prompt, "aspect_ratio": a.get("ar", "9:16"), "duration": dur, "resolution": a.get("res", "720p"), "enable_prompt_expansion": False}, 60)
                su, ru = q["status_url"], q["response_url"]
                for _ in range(120):
                    st = _get(su, key).get("status")
                    if st == "COMPLETED": break
                    if st == "FAILED": raise RuntimeError("Clip generation failed: " + k)
                    time.sleep(5)
                res = _get(ru, key); url = res["video"]["url"]
                mp4 = os.path.join(g, k + ".mp4"); _dl(url, mp4)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mp4, "-vf", "fps=30", "-q:v", "3", os.path.join(g, k + "_%04d.jpg")], check=True)
                print("  ✅ %s clip %s s → %d frames (%.0f s)" % (k, dur, frames_of(work, k), time.time() - t0))
            elif be == "gemini":
                _gemini_image(gkey, prompt, a.get("ar", "3:4"), os.path.join(g, k + ".jpg"))
                print("  ✅ %s image (Google, %.0f s)" % (k, time.time() - t0))
            else:
                res = _post("https://fal.run/" + IMG_MODEL, key, {"prompt": prompt, "num_images": 1, "aspect_ratio": a.get("ar", "3:4"), "output_format": "jpeg"}, 120)
                _dl(res["images"][0]["url"], os.path.join(g, k + ".jpg"))
                print("  ✅ %s image (%.0f s)" % (k, time.time() - t0))
        except urllib.error.HTTPError as e:
            body = e.read()[:300].decode("utf-8", "ignore")
            sys.exit("❌ fal rejected \"%s\": %s %s\n   (not retried — diagnose: the key? the credit? the content?)" % (k, e.code, body))
        except Exception as e:
            sys.exit("❌ Stopped at \"%s\": %s" % (k, str(e)[:200]))
    st = write_studio(work, cfg)
    print("📝 studio.json ← gen: %d scenes · genFrames: %s" % (len(st["gen"]), st["genFrames"]))

if __name__ == "__main__":
    main()

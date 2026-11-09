#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Move gallery: the user browses the numbered moves (motion/moves) and picks "Yes" or "No" (references/moves.md).

  python3 scripts/35_moves.py serve [--port N] [--no-open] [--timeout SEC]
      Opens the gallery page and waits for "Save"; writes the choice into ~/.video-ad-editor/profile.json under "moves"
      (touching nothing else) and prints it. The line "URL: ..." is printed first: give it to the user if the browser did not open.
      Exit codes: 0 = saved · 2 = timed out without saving · 1 = error.   ⚠ blocks until saved: never run it without arguments in a script.
  python3 scripts/35_moves.py show             prints the choice: {"on": [...], "off": [...]} by id + number
  python3 scripts/35_moves.py set "3 7 12" [--off "5"]
      saves a choice straight from the chat (gallery numbers), for when the user answers "I want 3 and 7, not 5" instead of using the page.
  python3 scripts/35_moves.py list             prints the catalog (number · id · name · state)
  python3 scripts/35_moves.py plan --title "<video title>" [--family calm|punch|onetake|editorial|auto] [--cues number,list,price,cta,contrast,emphasis,reveal,tech,hit] [--style auto|none|<id>] [--dry]
      The video's move board: 3 core moves (words + transition + camera/card) from ONE family that the whole video revolves around,
      + accents for special moments (from --cues), + the rules that always apply. It avoids the cores of the last 3 videos and anything the user turned "off".
      For a non-Arabic video (python3 scripts/_lang.py video) the Arabic-script moves are skipped. Saved to moves-history.json (unless --dry)
      so the next video comes out different. Save the output as <work>/moves_plan.json.

  VAE_HOME=<folder> changes where things are saved (for testing) instead of ~/.video-ad-editor. Python standard library only.
"""
import json, os, re, sys, threading, webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, unquote

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

SKILL = Path(__file__).resolve().parent.parent
MOVES = SKILL / "motion" / "moves"
CATALOG = MOVES / "catalog.json"
HOME = Path(os.environ.get("VAE_HOME") or (Path.home() / ".video-ad-editor"))
PROFILE = HOME / "profile.json"
TYPES = {".html": "text/html; charset=utf-8", ".json": "application/json; charset=utf-8", ".mp4": "video/mp4", ".png": "image/png"}


def ensure_previews(moves_dir):
    """ملف البلقن (رفع تطبيق كلود، حد 200 ملف) يحمل المعاينات zip واحد — نفكّه أول مرة."""
    import zipfile
    d, z = moves_dir / "previews", moves_dir / "previews.zip"
    if z.exists():                                        # يفك الناقص بس (تحديث البنك يضيف معاينات جديدة لمجلد مفكوك من قبل)
        d.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(z) as f:
            for n in f.namelist():
                if n.endswith(".mp4") and "/" not in n.strip("/").replace("previews/", "", 1) and not (d / Path(n).name).exists():
                    (d / Path(n).name).write_bytes(f.read(n))


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def catalog():
    return json.loads(CATALOG.read_text(encoding="utf-8"))["moves"]


def load_profile():
    try:
        return json.loads(PROFILE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_moves(on, off):
    """يدمج "moves" بالبروفايل بلا ما يلمس باقي المفاتيح."""
    ids = {m["id"] for m in catalog()}
    on = [i for i in dict.fromkeys(on) if i in ids]
    off = [i for i in dict.fromkeys(off) if i in ids and i not in on]
    p = load_profile()
    p["moves"] = {"on": on, "off": off}
    PROFILE.parent.mkdir(parents=True, exist_ok=True)
    tmp = PROFILE.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, PROFILE)
    return p["moves"]


def described(mv):
    by = {m["id"]: m for m in catalog()}
    f = lambda xs: [{"n": by[i]["n"], "id": i, "name": by[i]["name"]} for i in xs if i in by]
    return {"on": f(mv.get("on", [])), "off": f(mv.get("off", []))}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        if not isinstance(body, (bytes, bytearray)):
            body = json.dumps(body, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        u = unquote(urlparse(self.path).path)
        if u in ("/", "/index.html"):
            return self._send(200, (MOVES / "index.html").read_bytes(), TYPES[".html"])
        if u == "/api/state":
            p = load_profile()
            cols = ((p.get("identity") or {}).get("colors")) or {}
            try:
                sys.path.insert(0, str(Path(__file__).resolve().parent)); import _lang; lg = _lang.get()
            except Exception:
                lg = "en"
            return self._send(200, {"moves": p.get("moves") or {"on": [], "off": []}, "colors": cols, "lang": lg})
        f = (MOVES / u.lstrip("/")).resolve()
        if MOVES.resolve() in f.parents and f.is_file() and f.suffix in TYPES:
            return self._send(200, f.read_bytes(), TYPES[f.suffix])
        return self._send(404, {"ok": False})

    def do_POST(self):
        if urlparse(self.path).path != "/api/save":
            return self._send(404, {"ok": False})
        ctype = (self.headers.get("Content-Type") or "").split(";")[0].strip().lower()
        origin, host = self.headers.get("Origin"), self.headers.get("Host") or ""
        if ctype != "application/json" or (origin and origin != "http://" + host):
            return self._send(403, {"ok": False, "error": "forbidden"})
        try:
            n = int(self.headers.get("Content-Length") or 0)
            obj = json.loads(self.rfile.read(min(n, 65536)).decode("utf-8"))
            mv = save_moves(obj.get("on") or [], obj.get("off") or [])
        except Exception as e:
            return self._send(400, {"ok": False, "error": str(e)})
        self._send(200, {"ok": True})
        self.server.result = mv
        threading.Thread(target=self.server.shutdown, daemon=True).start()


def serve(args):
    ensure_previews(MOVES)
    port, do_open, timeout, i = 0, True, 1800, 0
    while i < len(args):
        a = args[i]
        if a == "--port":
            port = int(args[i + 1]); i += 1
        elif a == "--no-open":
            do_open = False
        elif a == "--timeout":
            timeout = int(args[i + 1]); i += 1
        i += 1
    srv = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    srv.result = None
    url = "http://127.0.0.1:%d/" % srv.server_address[1]
    print("URL: " + url, flush=True)
    if do_open:
        try:
            webbrowser.open(url)
        except Exception:
            pass
    timer = threading.Timer(timeout, srv.shutdown); timer.daemon = True; timer.start()
    try:
        srv.serve_forever(poll_interval=0.3)
    except KeyboardInterrupt:
        pass
    timer.cancel(); srv.server_close()
    if not srv.result:
        log("⏱️ خلص الوقت وما انحفظ شي.")
        return 2
    log("✅ انحفظ بـ" + str(PROFILE))
    print(json.dumps(described(srv.result), ensure_ascii=False, indent=2), flush=True)
    return 0


HISTORY = HOME / "moves-history.json"
STYLES = Path(__file__).resolve().parent.parent / "motion" / "styles" / "catalog.json"


def styles_catalog():
    try:
        return json.loads(STYLES.read_text(encoding="utf-8")).get("styles", [])
    except Exception:
        return []


def pick_style(title, family, cues, hist, want="auto"):
    """🎨 ستايل الفيديو (motion/styles.js): يناسب العائلة واللحظات، وما يتكرر ورا بعض. يرجّع (style, moments, why).
    want: auto · none · <id> · <a>+<b> (دمج). اللحظات (vhs/brutal) ما تصير ستايل الفيديو كله — تنقترح للهوك/الطلب بس."""
    cat = styles_catalog()
    if not cat or want == "none":
        return None, [], []
    ids = {c["id"]: c for c in cat}
    moments = [c["id"] for c in cat if c.get("moment") and set(c.get("cues", [])) & set(cues or [])]
    if want != "auto":
        bad = [x for x in want.split("+") if x not in ids]
        if bad:
            raise SystemExit("ستايل مو معروف: %s — الموجود: %s" % (" ".join(bad), " ".join(ids)))
        return want, moments, ["ستايل (اختيارك): " + " × ".join(ids[x]["name"] for x in want.split("+"))]
    recent = [h.get("style", "").split("+")[0] for h in hist[-4:]]
    def score(c):                                          # الأقل = الأحسن
        s = recent.count(c["id"]) * 10 - 2 * len(set(c.get("cues", [])) & set(cues or [])) + _h(title, "style", c["id"])
        if family not in c.get("families", []):
            s += 6
        if c.get("needsCut") and sys.platform != "darwin":   # السطح يحتاج قصّ الشخص (ماك) — برّاه يرجع لمعالجة الفيديو
            s += 3
        return s
    pool = sorted([c for c in cat if not c.get("moment")], key=score)
    a = pool[0]
    style, why = a["id"], ["style: %s — %s" % (a["name"], a["desc"])]
    mates = [b for b in a.get("blend", []) if b in ids and not ids[b].get("moment") and b not in recent]
    if mates and _h(title, "blend") < 0.35:                 # ثلث الفيديوهات تطلع دمج: سطح الأول + خط وحركة الثاني
        style += "+" + mates[0]
        why = ["style: blend %s × %s (surface from the first, font and motion from the second)" % (a["name"], ids[mates[0]]["name"])]
    if moments:
        why.append("moments: " + " · ".join(ids[m]["name"] for m in moments) + " (hook or call to action only, 1–3 s)")
    return style, moments, why
SLOTS = [("text", ("text",)), ("transition", ("transition",)), ("camera", ("camera", "card"))]


def history():
    try:
        return json.loads(HISTORY.read_text(encoding="utf-8"))
    except Exception:
        return []


def _h(*a):
    import hashlib
    return int(hashlib.sha1("|".join(map(str, a)).encode("utf-8")).hexdigest()[:8], 16) / 0xFFFFFFFF


ARABIC_ONLY = {"kashida", "ijamDrop", "qalamWrite", "joinSnap", "kufiGrid", "ayahCalm"}   # move arabic-script letters: never planned for Latin-script films


def _en(m):
    return ((m.get("i18n") or {}).get("en") or {}).get("name") or m["name"]


def plan(title, family="auto", cues=(), dry=False, style="auto"):
    cat = catalog()
    off = set((load_profile().get("moves") or {}).get("off", []))
    if sys.platform != "darwin":                           # حركات القصّ (mac: true) تحتاج Vision بالماك — برّاه ما تنختار
        off |= {m["id"] for m in cat if m.get("mac")}
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent)); import _lang; vlang = _lang.video()
    except Exception:
        vlang = "en"
    if vlang != "ar":                                      # the video is not Arabic: skip the Arabic-script moves
        off |= ARABIC_ONLY | {m["id"] for m in cat if m.get("bonus")}
    pref = set((load_profile().get("moves") or {}).get("on", []))
    hist = history()
    fams = list(json.loads(CATALOG.read_text(encoding="utf-8")).get("families", {}))
    if family == "auto":                                   # العائلة اللي ما انستخدمت من زمان (قرعة ثابتة بالعنوان عند التعادل)
        last = {h.get("family"): i for i, h in enumerate(hist)}
        family = min(fams, key=lambda f: (last.get(f, -1), _h(title, f)))
    recent = [i for h in hist[-3:] for i in h.get("core", [])]
    used = [i for h in hist for i in h.get("core", []) + h.get("accents", [])]
    def score(m):                                          # الأقل = الأحسن
        return (recent.count(m["id"]) * 10 + used.count(m["id"]) - (3 if m["id"] in pref else 0) + _h(title, m["id"]))
    pool = [m for m in cat if family in m.get("families", []) and m["id"] not in off and not m.get("manual")]   # manual (74 الآية) ما تنختار أبداً
    core, why = [], []
    for slot, roles in SLOTS:
        cands = sorted([m for m in pool if m["role"] in roles], key=score)
        if cands:
            core.append(cands[0]["id"]); why.append("%s: %d %s" % (slot, cands[0]["n"], _en(cands[0])))
    accents = []
    for cue in cues:                                       # لهجة لكل لحظة خاصة — من أي عائلة، بلا تكرار الأساسيات
        cands = sorted([m for m in cat if cue in m.get("cues", []) and m["id"] not in off and not m.get("manual") and m["id"] not in core + accents], key=score)
        if cands:
            accents.append(cands[0]["id"]); why.append("accent %s: %d %s" % (cue, cands[0]["n"], _en(cands[0])))
    rules = [m["id"] for m in cat if m["role"] == "rule" and family in m.get("families", []) and m["id"] not in off and m["id"] not in accents]
    caption = [m["id"] for m in cat if m["role"] == "caption" and m["id"] not in off]
    st, moments, swhy = pick_style(title, family, cues, hist, style)
    out = {"title": title, "family": family, "style": st, "moments": moments, "core": core, "accents": accents[:2], "rules": rules, "caption": caption, "why": swhy + why}
    if not dry:
        import datetime
        hist.append({"date": datetime.date.today().isoformat(), "title": title, "family": family, "style": st or "", "core": core, "accents": accents[:2]})
        HISTORY.parent.mkdir(parents=True, exist_ok=True)
        HISTORY.write_text(json.dumps(hist[-50:], ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def nums(s):
    by = {m["n"]: m["id"] for m in catalog()}
    return [by[int(x)] for x in re.findall(r"\d+", s or "") if int(x) in by]


def main(argv):
    if any(a in ("-h", "--help", "help") for a in argv[:1]):
        print(__doc__); return 0
    cmd = argv[0] if argv and not argv[0].startswith("--") else "serve"
    rest = argv[1:] if argv and not argv[0].startswith("--") else argv
    if cmd not in ("serve", "show", "set", "list", "plan"):
        print("unknown command: %s\n" % cmd); print(__doc__); return 1
    if cmd == "serve":
        return serve(rest)
    if cmd == "show":
        print(json.dumps(described(load_profile().get("moves") or {}), ensure_ascii=False, indent=2))
        return 0
    if cmd == "set":
        on = nums(rest[0] if rest else "")
        off = nums(rest[rest.index("--off") + 1]) if "--off" in rest else []
        print(json.dumps(described(save_moves(on, off)), ensure_ascii=False, indent=2))
        return 0
    if cmd == "list":
        mv = load_profile().get("moves") or {}
        for m in catalog():
            st = "✓" if m["id"] in mv.get("on", []) else "✗" if m["id"] in mv.get("off", []) else "·"
            print("%s %2d  %-11s %s" % (st, m["n"], m["id"], m["name"]))
        return 0
    if cmd == "plan":
        opt = lambda k, d=None: rest[rest.index(k) + 1] if k in rest else d
        cues = [c.strip() for c in (opt("--cues", "") or "").split(",") if c.strip()]
        print(json.dumps(plan(opt("--title", "Untitled"), opt("--family", "auto"), cues, "--dry" in rest, opt("--style", "auto")), ensure_ascii=False, indent=2))
        return 0
    log(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

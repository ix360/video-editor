#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""بحث وتنزيل ستوك مجاني (فيديو وصور) — Pexels · Pixabay · Unsplash (صور).

  python3 38_stock.py keys                                    أي مفاتيح موجودة (بلا طباعتها)
  python3 38_stock.py search <work> "coffee pouring" [--kind video|image] [--n 8] [--provider pexels|pixabay|unsplash]
                                                               [--orient portrait|landscape|square] [--minsec 3]
        ← يطبع قائمة مرقّمة ويحفظ <work>/stock/results.json
  python3 38_stock.py get <work> <رقم_من_القائمة> --k <اسم_الأصل>
        ← ينزّل النسخة المناسبة لـ<work>/stock/ ويسجّل المصدر بـstock/credits.json
        ← ويطبع سطر الاستيراد: 17_gen_scenes.py <work> import <k> <الملف> (يدخل الأصل بنفس نظام المشاهد المولّدة)
  python3 38_stock.py credits <work>                           سطور الإسناد (اسم المصور + الرابط) للوصف/الكابشن

المفاتيح (مجانية، من موقع كل مزوّد) من البيئة أو ملف .env:
  PEXELS_API_KEY · PIXABAY_API_KEY · UNSPLASH_ACCESS_KEY
⛔ الرخص: Pexels وPixabay وUnsplash تسمح بالاستخدام التجاري بلا إسناد إلزامي، بس لا تعيد بيعها كما هي ولا تظهر ناس بسياق مسيء.
   سجّل المصدر دايماً (credits.json). Unsplash تطلب إشعار «تنزيل» وهذا السكربت يرسله."""
import sys, os, json, urllib.request, urllib.parse, urllib.error, subprocess

UA = {"User-Agent": "video-studio-plugin/1.0"}
KEYS = {"pexels": "PEXELS_API_KEY", "pixabay": "PIXABAY_API_KEY", "unsplash": "UNSPLASH_ACCESS_KEY"}


def env(work, name):
    if os.environ.get(name): return os.environ[name]
    for d in (work, os.getcwd(), os.path.expanduser("~")):
        p = os.path.join(d or ".", ".env")
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                if line.startswith(name + "="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def getj(url, headers=None):
    r = urllib.request.Request(url, headers={**UA, **(headers or {})})
    return json.load(urllib.request.urlopen(r, timeout=30))


def item(provider, kind, id_, page, user, user_url, dur, w, h, url, thumb):
    return dict(provider=provider, kind=kind, id=str(id_), page=page, user=user, user_url=user_url,
                duration=dur, w=w, h=h, url=url, thumb=thumb)


def pick_video(files, want_portrait):
    """أنسب ملف: عرض ≤ 1080 (أو الأقرب)، ويفضّل نفس الاتجاه"""
    files = [f for f in files if f.get("link") or f.get("url")]
    def score(f):
        w, h = f.get("width") or 0, f.get("height") or 0
        return (0 if (h >= w) == want_portrait else 1, abs(min(w, h) - 1080))
    f = sorted(files, key=score)[0]
    return f.get("link") or f.get("url"), f.get("width"), f.get("height")


def search_pexels(key, q, kind, n, orient):
    h = {"Authorization": key}
    o = "&orientation=" + orient if orient else ""
    out = []
    if kind == "video":
        d = getj("https://api.pexels.com/videos/search?query=%s&per_page=%d%s" % (urllib.parse.quote(q), n, o), h)
        for v in d.get("videos", []):
            url, w, hh = pick_video(v.get("video_files", []), orient != "landscape")
            out.append(item("pexels", "video", v["id"], v.get("url"), (v.get("user") or {}).get("name"), (v.get("user") or {}).get("url"),
                            v.get("duration"), w, hh, url, v.get("image")))
    else:
        d = getj("https://api.pexels.com/v1/search?query=%s&per_page=%d%s" % (urllib.parse.quote(q), n, o), h)
        for p in d.get("photos", []):
            s = p.get("src", {})
            out.append(item("pexels", "image", p["id"], p.get("url"), p.get("photographer"), p.get("photographer_url"), None,
                            p.get("width"), p.get("height"), s.get("large2x") or s.get("original"), s.get("medium")))
    return out


def search_pixabay(key, q, kind, n, orient):
    out = []
    n = max(3, min(n, 200))
    if kind == "video":
        d = getj("https://pixabay.com/api/videos/?key=%s&q=%s&per_page=%d" % (key, urllib.parse.quote(q), n))
        for v in d.get("hits", []):
            vs = v.get("videos", {})
            files = [dict(link=x.get("url"), width=x.get("width"), height=x.get("height")) for x in vs.values() if x.get("url")]
            if not files: continue
            url, w, hh = pick_video(files, orient != "landscape")
            out.append(item("pixabay", "video", v["id"], v.get("pageURL"), v.get("user"), "https://pixabay.com/users/%s-%s/" % (v.get("user"), v.get("user_id")),
                            v.get("duration"), w, hh, url, (vs.get("tiny") or {}).get("thumbnail")))
    else:
        o = {"portrait": "vertical", "landscape": "horizontal"}.get(orient or "", "all")
        d = getj("https://pixabay.com/api/?key=%s&q=%s&image_type=photo&orientation=%s&per_page=%d" % (key, urllib.parse.quote(q), o, n))
        for p in d.get("hits", []):
            out.append(item("pixabay", "image", p["id"], p.get("pageURL"), p.get("user"), "https://pixabay.com/users/%s-%s/" % (p.get("user"), p.get("user_id")), None,
                            p.get("imageWidth"), p.get("imageHeight"), p.get("largeImageURL"), p.get("previewURL")))
    return out


def search_unsplash(key, q, kind, n, orient):
    if kind == "video": return []
    o = "&orientation=" + {"portrait": "portrait", "landscape": "landscape", "square": "squarish"}.get(orient or "", "") if orient else ""
    d = getj("https://api.unsplash.com/search/photos?query=%s&per_page=%d%s" % (urllib.parse.quote(q), min(n, 30), o), {"Authorization": "Client-ID " + key})
    out = []
    for p in d.get("results", []):
        u = p.get("user", {}); urls = p.get("urls", {})
        it = item("unsplash", "image", p["id"], (p.get("links") or {}).get("html"), u.get("name"), (u.get("links") or {}).get("html"), None,
                  p.get("width"), p.get("height"), urls.get("regular"), urls.get("small"))
        it["download_location"] = (p.get("links") or {}).get("download_location")
        out.append(it)
    return out


SEARCH = {"pexels": search_pexels, "pixabay": search_pixabay, "unsplash": search_unsplash}


def arg(a, name, default=None):
    return a[a.index(name) + 1] if name in a and a.index(name) + 1 < len(a) else default


def cmd_search(a):
    work, q = a[0], a[1]
    kind = arg(a, "--kind", "video"); n = int(arg(a, "--n", 8)); orient = arg(a, "--orient", "portrait")
    minsec = float(arg(a, "--minsec", 0)); only = arg(a, "--provider")
    provs = [only] if only else list(SEARCH)
    res, skipped = [], []
    for p in provs:
        key = env(work, KEYS[p])
        if not key: skipped.append(p); continue
        try: res += SEARCH[p](key, q, kind, n, orient)
        except urllib.error.HTTPError as e: print("⚠️ %s رفض الطلب (%s) — المفتاح؟ الحد؟" % (p, e.code), file=sys.stderr)
        except Exception as e: print("⚠️ %s: %s" % (p, str(e)[:120]), file=sys.stderr)
    if minsec: res = [r for r in res if not r.get("duration") or r["duration"] >= minsec]
    if not res:
        miss = ("ما فيه مفاتيح لـ: " + ", ".join(KEYS[p] for p in skipped) + " — كلها مجانية (سجّل بموقع المزوّد وانسخ المفتاح).") if len(skipped) == len(provs) else "ما لقيت نتائج — جرّب وصف إنقليزي أبسط."
        sys.exit("❌ " + miss)
    os.makedirs(os.path.join(work, "stock"), exist_ok=True)
    json.dump(res, open(os.path.join(work, "stock", "results.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for i, r in enumerate(res, 1):
        print("%2d. [%s %s] %sx%s %s — %s · %s" % (i, r["provider"], r["kind"], r["w"], r["h"], ("%ss" % r["duration"]) if r["duration"] else "", r["user"], r["page"]))
    if skipped: print("(ما دوّرت بـ: %s — ما فيه مفتاح)" % ", ".join(skipped))


def cmd_get(a):
    work, idx = a[0], int(a[1]); k = arg(a, "--k")
    if not k: sys.exit("❌ --k <اسم_الأصل> مطلوب")
    res = json.load(open(os.path.join(work, "stock", "results.json"), encoding="utf-8"))
    if not 1 <= idx <= len(res): sys.exit("❌ الرقم خارج القائمة (1..%d)" % len(res))
    r = res[idx - 1]
    ext = ".mp4" if r["kind"] == "video" else ".jpg"
    path = os.path.join(work, "stock", "%s_%s%s" % (r["provider"], r["id"], ext))
    if r["provider"] == "unsplash" and r.get("download_location"):
        key = env(work, KEYS["unsplash"])
        try: getj(r["download_location"], {"Authorization": "Client-ID " + key})   # إشعار تنزيل مطلوب من شروط Unsplash
        except Exception: pass
    req = urllib.request.Request(r["url"], headers=UA)
    with urllib.request.urlopen(req, timeout=120) as f, open(path, "wb") as o:
        while True:
            b = f.read(1 << 20)
            if not b: break
            o.write(b)
    cp = os.path.join(work, "stock", "credits.json")
    cr = json.load(open(cp, encoding="utf-8")) if os.path.exists(cp) else []
    cr = [c for c in cr if c["k"] != k] + [dict(k=k, file=path, provider=r["provider"], id=r["id"], user=r["user"], user_url=r["user_url"], page=r["page"])]
    json.dump(cr, open(cp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("✅ %s (%.1f MB) ← %s" % (path, os.path.getsize(path) / 1e6, r["page"]))
    print("استورده كأصل:  python3 scripts/17_gen_scenes.py %s import %s %s" % (work, k, path))


def cmd_credits(a):
    cp = os.path.join(a[0], "stock", "credits.json")
    if not os.path.exists(cp): sys.exit("ما فيه ستوك منزّل")
    for c in json.load(open(cp, encoding="utf-8")):
        print("%s — %s (%s) %s" % (c["k"], c["user"], c["provider"], c["page"]))


def main():
    a = sys.argv[1:]
    if not a: sys.exit(__doc__)
    if a[0] == "keys":
        for p, n in KEYS.items(): print("%-9s %s  %s" % (p, n, "✅" if env(".", n) else "—"))
        return
    {"search": cmd_search, "get": cmd_get, "credits": cmd_credits}.get(a[0], lambda _: sys.exit(__doc__))(a[1:])


if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    main()

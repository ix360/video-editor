#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""فحص الإعداد — يتأكد من اللي ينفحص من الجهاز نفسه، وكلود يكمّل الباقي (references/setup-check.md).

  python3 00_check.py show                 ملخص: اللغة، وضع الأصول، المفاتيح الموجودة (بلا طباعة قيمها)، الأدوات
  python3 00_check.py set-assets api|subscription     يحفظ اختيار المستخدم لمصدر الصور والمقاطع
  python3 00_check.py gemini               يجرّب مفتاح AI Studio بطلب قراءة مجاني (بلا توليد وبلا صرف)
الرمز: 0 كل شي تمام · 3 فيه ناقص (مكتوب بالتقرير) · 1 خطأ استخدام
بايثون القياسية بس."""
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
    if not k: print("— ما فيه GEMINI_API_KEY (مفتاح مجاني من aistudio.google.com ← Get API key)"); return False
    r = urllib.request.Request("https://generativelanguage.googleapis.com/v1beta/models?pageSize=1", headers={"x-goog-api-key": k})
    try:
        urllib.request.urlopen(r, timeout=20); print("✅ مفتاح AI Studio يشتغل"); return True
    except urllib.error.HTTPError as e:
        print("❌ مفتاح AI Studio مرفوض (%s) — تأكد إنه منسوخ كامل ومفعّل" % e.code); return False
    except Exception as e:
        print("⚠️ ما قدرت أوصل لجوجل (%s) — تأكد من النت" % str(e)[:80]); return False


def show():
    mode = _setup.assets_mode(); lang_saved = os.path.exists(os.path.join(os.path.dirname(str(_setup._path())), "lang.json"))
    miss = 0
    print("اللغة:        %s %s" % (_lang.get(), "" if lang_saved else "(افتراضي — ما اختار بعد)"))
    print("مصدر الأصول:  %s" % (mode or "— ما اختار بعد"))
    if not mode: miss += 1
    print("\nأدوات الجهاز:")
    for t in ("ffmpeg", "ffprobe", "python3", "node"):
        f = shutil.which(t); print("  %s %s" % (ok(f), t)); miss += 0 if f else (1 if t in ("ffmpeg", "ffprobe") else 0)
    try: import whisper; w = True
    except Exception: w = False
    print("  %s whisper (التفريغ — الخطوة 0 بـ00_setup.sh تنزّله)" % ok(w))
    print("\nمفاتيح (مجانية أو اختيارية):")
    for n, why in (("GEMINI_API_KEY", "صور AI Studio"), ("FAL_KEY", "مقاطع/صور مدفوعة"), ("PEXELS_API_KEY", "ستوك"), ("PIXABAY_API_KEY", "ستوك"), ("UNSPLASH_ACCESS_KEY", "صور ستوك"), ("ELEVENLABS_API_KEY", "رفع عينة الاستنساخ")):
        print("  %s %-20s %s" % (ok(env(n)), n, why))
    if mode == "api" and not (env("GEMINI_API_KEY") or env("GOOGLE_API_KEY")):
        print("\n⚠️ اخترت «api» بس ما فيه GEMINI_API_KEY."); miss += 1
    print("\nكلود يفحص بنفسه: موصّل ElevenLabs · إضافة كروم · دخول جوجل فلو (references/setup-check.md)")
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

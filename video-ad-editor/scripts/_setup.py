# -*- coding: utf-8 -*-
"""إعدادات الإعداد المحفوظة (~/.video-ad-editor/setup.json) — مصدر واحد للسكربتات.
  assets: "api"          ← صور بمفتاح AI Studio (GEMINI_API_KEY) والمقاطع/الاحتياط عبر fal (FAL_KEY)
          "subscription" ← جوجل فلو من متصفح كروم باشتراك المستخدم (references/google-flow.md) — بلا مفاتيح
          None           ← ما اختار بعد (يسأله كلود مرة وحدة)"""
import json, os
from pathlib import Path

MODES = ("api", "subscription")


def _path():
    return Path(os.environ.get("VAE_HOME") or (Path.home() / ".video-ad-editor")) / "setup.json"


def load():
    try: return json.loads(_path().read_text(encoding="utf-8"))
    except Exception: return {}


def save(**kw):
    d = load(); d.update(kw)
    p = _path(); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    return d


def assets_mode():
    m = (os.environ.get("VAE_ASSETS") or load().get("assets") or "").lower()
    return m if m in MODES else None

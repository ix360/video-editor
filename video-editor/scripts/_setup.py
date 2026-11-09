# -*- coding: utf-8 -*-
"""Saved setup choices (~/.video-ad-editor/setup.json) — one source for the scripts.
  assets: "api"          -> images by AI Studio key (GEMINI_API_KEY); videos/fallback via fal (FAL_KEY)
          "subscription" -> Google Flow in the user's Chrome with their own Google plan (references/google-flow.md) — no keys
          None           -> not chosen yet (Claude asks once)"""
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

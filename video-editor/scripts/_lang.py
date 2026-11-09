# -*- coding: utf-8 -*-
"""The user's language — one source of truth for every script.
Order: env var VAE_LANG -> ~/.video-ad-editor/lang.json -> "en" (default).
  python3 _lang.py            prints the current code (e.g. en)
  python3 _lang.py list       prints the supported languages
Used for the Whisper language, captions and Claude's replies."""
import json, os, sys
from pathlib import Path

# code: (native name, Whisper code, right-to-left?)
LANGS = {
    "ar": ("العربية", "ar", True),
    "en": ("English", "en", False),
    "fr": ("Français", "fr", False),
    "es": ("Español", "es", False),
    "pt": ("Português", "pt", False),
    "de": ("Deutsch", "de", False),
    "tr": ("Türkçe", "tr", False),
    "ur": ("اردو", "ur", True),
    "fa": ("فارسی", "fa", True),
    "id": ("Bahasa Indonesia", "id", False),
}
DEFAULT = "en"


def _profile():
    home = Path(os.environ.get("VAE_HOME") or (Path.home() / ".video-ad-editor"))
    try:
        return json.loads((home / "lang.json").read_text(encoding="utf-8"))
    except Exception:
        return {}


def get():
    """The chosen language code (default en)."""
    c = (os.environ.get("VAE_LANG") or _profile().get("lang") or DEFAULT).strip().lower()
    return c if c in LANGS else DEFAULT


def whisper():
    return LANGS[get()][1]


def rtl():
    return LANGS[get()][2]


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        for k, (n, _, r) in LANGS.items():
            print(f"{k}\t{n}\t{'rtl' if r else 'ltr'}")
    else:
        print(get())

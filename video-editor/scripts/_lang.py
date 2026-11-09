# -*- coding: utf-8 -*-
"""The user's language — one source of truth for every script.
Two settings, because they differ in real life (a user chats in English and makes a French video):
  get()    the CHAT language — what Claude speaks to the user.   VAE_LANG  > lang.json "lang"  > "en"
  video()  the VIDEO language — the voice, the Whisper language and the captions.   VAE_VIDEO_LANG > lang.json "video" > get()
  python3 _lang.py            prints the chat language (e.g. en)
  python3 _lang.py video      prints the video language
  python3 _lang.py list       prints the supported languages"""
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


def video():
    """The language of the VIDEO (voice, transcription, captions). Falls back to the chat language."""
    c = (os.environ.get("VAE_VIDEO_LANG") or _profile().get("video") or get()).strip().lower()
    return c if c in LANGS else get()


def whisper():
    return LANGS[video()][1]


def rtl():
    return LANGS[video()][2]


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) > 1 and sys.argv[1] == "list":
        for k, (n, _, r) in LANGS.items():
            print(f"{k}\t{n}\t{'rtl' if r else 'ltr'}")
    elif len(sys.argv) > 1 and sys.argv[1] == "video":
        print(video())
    else:
        print(get())

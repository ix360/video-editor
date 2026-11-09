#!/bin/bash
# فحص وتجهيز الأدوات.  ./00_setup.sh          → يفحص ويقول وش ناقص
#                      ./00_setup.sh --install → ينزّل الناقص (بعد إذن المستخدم)
#                      ./00_setup.sh --extras  → الإضافات الاختيارية: تنظيف صوت ذكي · نبض · بحث بالمعنى
# ✏️ معدّل ليشتغل على ويندوز وماك ولينكس. الأصل الماكي محفوظ بـ00_setup.sh.mac-orig
. "$(dirname "$0")/_compat.sh"
INSTALL=0; [ "$1" = "--install" ] && INSTALL=1
MISS=(); OK=(); NOTE=()
have(){ command -v "$1" >/dev/null 2>&1; }
line(){ printf '%s\n' "$1"; }

case "$(uname -s)" in
  MINGW*|MSYS*|CYGWIN*) OS=win ;;
  Darwin) OS=mac ;;
  *) OS=linux ;;
esac
SKILL="$(abspath "$(dirname "$0")/..")"
# ☁️ بيئة سحابية / جوال (6 أكتوبر 2026 — قرار ماجد: ما فيه «ما يصير»): بدل ما نوقف، ننبّه ونكمّل بالمسار البديل.
#    هنا تنزيل موديل وِسبر الأصلي قد يكون محجوب وما فيه واجهة، فنستخدم السلّم بـreferences/any-environment.md
#    (faster-whisper · MODNet · كروم بلا واجهة + ffmpeg). الجلسة الأولى على الجوال أثبتت إنه يشتغل.
if [ "$OS" = linux ] && { [ -n "$CLAUDE_SANDBOX" ] || [ ! -d /Applications ]; } && ! curl -sI -m 8 https://openaipublic.azureedge.net >/dev/null 2>&1; then
  echo "☁️ Cloud/phone environment: the original Whisper download is blocked here — continuing with the fallbacks: faster-whisper for transcription, MODNet for person cut-out, headless Chrome for drawing."
  echo "   Read references/any-environment.md. Don't stop, and never tell the user \"it can't be done\"."
  CLOUD=1
fi

# 🔄 تحديث تلقائي (v2.9): نقارن VERSION المحلي بآخر إصدار على قت هب بصمت (5 ثوانٍ كحد أقصى).
#    لو فيه أحدث: نطبع سطراً واحداً — وكلود يسأل المستخدم ثم يشغّل: bash scripts/00_setup.sh --update
SKROOT="$(cd "$(dirname "$0")/.." && pwd)"; LOCALV="$(cat "$SKROOT/VERSION" 2>/dev/null || echo 0)"
# v4: لو السكل منصّب كـplugin (video-editor) التحديث يكون من مدير الإضافات — مو بالاستبدال اليدوي
case "$SKROOT" in */.claude/plugins/*) PLUGIN=1 ;; *) PLUGIN=0 ;; esac
PLUG_UPD="claude plugin marketplace update ix360-plugins && claude plugin update video-editor@ix360-plugins"
if [ "$1" = "--update" ] && [ "$PLUGIN" = 1 ]; then
  echo "ℹ️ Installed as a plugin — run: $PLUG_UPD  (then open a new session)"; exit 0
fi
if [ "$1" = "--update" ]; then
  TMP="$(mktemp -d)"; echo "⬇️ Downloading the latest version…"
  if curl -sL -m 120 -o "$TMP/skill.zip" https://github.com/ix360/video-editor/releases/latest/download/video-editor.skill \
     && unzip -q -o "$TMP/skill.zip" -d "$TMP/x" && [ -f "$TMP/x/video-editor/SKILL.md" ]; then
    rsync -a --delete --exclude=bin --exclude=hdr2sdr --exclude=personmask --exclude=facetrack --exclude=node_modules "$TMP/x/video-editor/" "$SKROOT/" \
      && echo "✅ Updated to v$(cat "$SKROOT/VERSION" 2>/dev/null) — carry on as usual" || echo "⚠️ Could not replace the files"
  else echo "⚠️ Could not download the update — try again later"; fi
  rm -rf "$TMP"; exit 0
fi
LATEST="$(curl -sL -m 5 https://api.github.com/repos/ix360/video-editor/releases/latest 2>/dev/null | sed -n 's/.*"tag_name": *"v\([0-9.]*\)".*/\1/p' | head -1)"
if [ -n "$LATEST" ] && [ "$LATEST" != "$LOCALV" ] && [ "$(printf '%s\n%s' "$LOCALV" "$LATEST" | sort -V | tail -1)" = "$LATEST" ]; then
  if [ "$PLUGIN" = 1 ]; then
    echo "🆕 A newer version exists: v$LATEST (you have v$LOCALV) — ask the user, and if they agree run: $PLUG_UPD  (then a new session)"
  else
    echo "🆕 A newer version exists: v$LATEST (you have v$LOCALV) — ask the user, and if they agree run: bash scripts/00_setup.sh --update"
  fi
fi

# ➕ الإضافات (v3.9، أفكار Palmier) — اختيارية، السكل يشتغل بدونها وكل وحدة ترجع للطريق القديم لو ناقصة:
#    ‹deep-filter› تنظيف صوت ذكي (02c) · ‹transformers› البحث بالمعنى (26)
# 🆕 6.0: pip القديم (قبل 23) ما يعرف --break-system-packages — كان يطلّع «no such option» ويفشل التنصيب.
#    نجرّب عادي ← لو pip يعرف الخيار نجرّبه ← وإلا --user (يشتغل بكل نسخ pip وبلا صلاحيات مدير).
pip_in(){ "$PY" -m pip install --quiet "$@" 2>/dev/null && return 0
  if "$PY" -m pip install --help 2>/dev/null | grep -q -- '--break-system-packages'; then
    "$PY" -m pip install --quiet --break-system-packages "$@" && return 0
  fi
  "$PY" -m pip install --quiet --user "$@"; }
extras_status(){
  local e=()
  { [ -x "$SKILL/bin/deep-filter" ] || [ -x "$SKILL/bin/deep-filter.exe" ] || have deep-filter; } && e+=("audio-cleanup✅") || e+=("audio-cleanup—")
  "$PY" -c "import transformers,PIL" 2>/dev/null && e+=("search-by-meaning✅") || e+=("search-by-meaning—")
  echo "${e[*]}"
}
if [ "$1" = "--extras" ]; then
  pipx2(){ pip_in "$@"; }
  mkdir -p "$SKILL/bin"
  DFV=0.5.6
  case "$OS-$(uname -m)" in
    mac-arm64)          T=aarch64-apple-darwin ;;
    mac-x86_64)         T=x86_64-apple-darwin ;;
    win-*)              T=x86_64-pc-windows-msvc.exe ;;
    linux-x86_64)       T=x86_64-unknown-linux-musl ;;
    *)                  T="" ;;
  esac
  DF="$SKILL/bin/deep-filter"; [ "$OS" = win ] && DF="$DF.exe"
  if [ -n "$T" ] && [ ! -x "$DF" ]; then
    line "⏬ Smart audio cleanup (DeepFilterNet3, ~20 MB)…"
    if curl -sfL -m 180 -o "$DF" "https://github.com/Rikorose/DeepFilterNet/releases/download/v$DFV/deep-filter-$DFV-$T" \
       && [ "$(wc -c < "$DF")" -gt 1000000 ]; then
      chmod +x "$DF"; [ "$OS" = mac ] && xattr -d com.apple.quarantine "$DF" 2>/dev/null
      "$DF" --help >/dev/null 2>&1 && line "   ✅ ready" || { rm -f "$DF"; line "   ⚠️ downloaded but did not run — the normal ffmpeg filter stays"; }
    else rm -f "$DF"; line "   ⚠️ could not download it — the normal ffmpeg filter stays"; fi
  fi
  "$PY" -c "import torch" 2>/dev/null || { line "⏬ torch (base for the models)…"; pipx2 torch; }
  "$PY" -c "import transformers,PIL" 2>/dev/null || { line "⏬ Search by meaning (transformers — the ~1.5 GB model downloads on first search)…"; pipx2 "transformers>=4.49" pillow sentencepiece protobuf || line "   ⚠️ failed"; }
  line "Extras: $(extras_status)"
  exit 0
fi

have ffmpeg  && OK+=("ffmpeg")  || MISS+=("ffmpeg")
have ffprobe && OK+=("ffprobe") || MISS+=("ffprobe")
"$PY" -c "import whisper" 2>/dev/null && OK+=("whisper") || MISS+=("whisper")
"$PY" -c "import numpy"   2>/dev/null && OK+=("numpy")   || MISS+=("numpy")

# كروم: نفس ترتيب البحث اللي بالسكربتات
find_chrome(){
  [ -n "$CHROME_PATH" ] && [ -f "$CHROME_PATH" ] && { echo "$CHROME_PATH"; return 0; }
  local c
  for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
           "${ProgramFiles:-C:/Program Files}/Google/Chrome/Application/chrome.exe" \
           "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" \
           "${LOCALAPPDATA:-}/Google/Chrome/Application/chrome.exe" \
           "${ProgramFiles:-C:/Program Files}/Microsoft/Edge/Application/msedge.exe" \
           /usr/bin/google-chrome /usr/bin/chromium /usr/bin/chromium-browser; do
    [ -f "$c" ] && { echo "$c"; return 0; }
  done; return 1
}
CHROME="$(find_chrome)" && OK+=("chrome") || MISS+=("chrome")

# puppeteer-core: يُبحث عنه من مجلد السكل نفسه (هناك ينزّل)
( cd "$SKILL" && node -e "require.resolve('puppeteer-core')" ) 2>/dev/null \
  && OK+=("puppeteer-core") || MISS+=("puppeteer-core")

# scipy: the audio mixer (motion/audio.py) needs it. Systems that block system-wide pip (PEP 668) get a small venv in ~/.video-ad-editor/venv.
VAE_H="${VAE_HOME:-$HOME/.video-ad-editor}"; VPY="$VAE_H/venv/bin/python"; [ "$OS" = win ] && VPY="$VAE_H/venv/Scripts/python.exe"
if "$PY" -c "import scipy" 2>/dev/null || { [ -x "$VPY" ] && "$VPY" -c "import scipy" 2>/dev/null; }; then OK+=("scipy"); else MISS+=("scipy"); fi

line "System: $OS · Python: $PY"
[ -n "$CHROME" ] && line "Chrome: $CHROME"
line "Ready: ${OK[*]:-nothing}"
line "Extras (optional — 00_setup.sh --extras): $(extras_status)"
if have npm; then line "Second engine (Remotion): available on request — 04b_remotion.sh setup downloads it (~500 MB)"
else line "Second engine (Remotion): needs npm — not available, the light one is enough"; fi
[ "$OS" = mac ] || NOTE+=("The \"text behind the person\" effect (11_behind_text.js) works on Mac only — everything else works as usual")

if [ ${#MISS[@]} -eq 0 ]; then
  line "✅ Everything is ready — we can start."
  [ ${#NOTE[@]} -gt 0 ] && printf 'ℹ️  %s\n' "${NOTE[@]}"
  exit 0
fi
line "Missing: ${MISS[*]}"
if [ $INSTALL -eq 0 ]; then line "Run: $0 --install"; exit 10; fi

pipi(){ pip_in "$@"; }
for m in "${MISS[@]}"; do
  case "$m" in
    ffmpeg|ffprobe)
      [ "$m" = ffprobe ] && continue
      line "⏬ ffmpeg…"
      if   [ "$OS" = win ] && have winget; then winget install --id Gyan.FFmpeg -e --accept-package-agreements --accept-source-agreements || NOTE+=("ffmpeg failed — download it from ffmpeg.org and add it to PATH")
      elif have brew;  then brew install ffmpeg || NOTE+=("ffmpeg failed")
      elif have apt;   then sudo apt install -y ffmpeg || NOTE+=("ffmpeg failed")
      else NOTE+=("Download ffmpeg manually from ffmpeg.org and add it to PATH"); fi ;;
    whisper) line "⏬ openai-whisper… (the model downloads on first run, 1.4 GB)"
      pipi openai-whisper || NOTE+=("whisper failed") ;;
    scipy)   line "⏬ scipy (audio mixer, ~35 MB, into $VAE_H/venv)…"
      { "$PY" -m venv --system-site-packages "$VAE_H/venv" && "$VPY" -m pip install --quiet scipy; } || NOTE+=("scipy failed — try: $PY -m venv --system-site-packages $VAE_H/venv && $VPY -m pip install scipy") ;;
    numpy)   pipi numpy || NOTE+=("numpy failed") ;;
    puppeteer-core) line "⏬ puppeteer-core…"
      ( cd "$SKILL" && npm i --silent puppeteer-core ) || NOTE+=("puppeteer-core failed") ;;
    chrome) NOTE+=("Chrome is not installed — get it from google.com/chrome or set CHROME_PATH") ;;
  esac
done

FAIL=0
have ffmpeg || FAIL=1
"$PY" -c "import whisper,numpy" 2>/dev/null || FAIL=1
find_chrome >/dev/null || FAIL=1
{ "$PY" -c "import scipy" 2>/dev/null || { [ -x "$VPY" ] && "$VPY" -c "import scipy" 2>/dev/null; }; } || FAIL=1
( cd "$SKILL" && node -e "require.resolve('puppeteer-core')" ) 2>/dev/null || FAIL=1
[ ${#NOTE[@]} -gt 0 ] && printf '⚠️  %s\n' "${NOTE[@]}"
[ $FAIL -eq 0 ] && line "✅ Everything is ready now." || { line "❌ Still missing something — see the notes above."; exit 11; }

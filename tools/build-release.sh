#!/bin/bash
# يبني ملفات الإصدار من آخر كوميت بهالمستودع (بلا نسخ من أي مجلد ثاني):
#   bash tools/build-release.sh   →   dist/video-studio.plugin + dist/video-ad-editor.skill
# لا ينشر شي. النشر (push + gh release) خطوة منفصلة بموافقتك.
set -euo pipefail
REPO="$(cd "$(dirname "$0")/.." && pwd)"; cd "$REPO"
[ -z "$(git status --porcelain -- .claude-plugin video-ad-editor motion-video podcast-video montage-video thumbnail-video voiceover-video)" ] || { echo "❌ فيه تعديلات مو مكومتة — كوميت أول"; exit 1; }
T="$(mktemp -d)"; trap 'rm -rf "$T"' EXIT
git archive HEAD .claude-plugin video-ad-editor motion-video podcast-video montage-video thumbnail-video voiceover-video | tar -x -C "$T"
P="$T/video-ad-editor"
# مو للتشغيل: صور الشرح وملفات npm وملفات جيت الداخلية (نفس 4.4.4)
rm -rf "$P/img" "$P/package.json" "$P/package-lock.json" "$P/motion/.gitignore"
# حد 200 ملف لرفع تطبيق كلود: معاينات بنك الحركات ← zip واحد (35_moves.py / 00_onboard.py يفكّونه أول مرة)
( cd "$P/motion/moves" && zip -qr previews.zip previews && rm -rf previews )
# ونفس الشي لمكتبة three.js (25 ملف ← 1) — motion/vendor.js يفكها أول مرة
( cd "$P/motion" && zip -qr vendor.zip vendor && rm -rf vendor )
# marketplace.json يبقى بالمستودع (هو المتجر نفسه) وما له شغل داخل ملف البلقن
rm -f "$T/.claude-plugin/marketplace.json"
mkdir -p dist; rm -f dist/video-studio.plugin dist/video-ad-editor.skill
( cd "$T" && zip -qr "$REPO/dist/video-studio.plugin" .claude-plugin video-ad-editor motion-video podcast-video montage-video thumbnail-video voiceover-video -x '*/.DS_Store' )
# ملف .skill القديم: سكل واحد بوصف يغطي كل الأوضاع (دبل كليك + التحديث الذاتي للنسخ القديمة)
S="$(mktemp -d)"; cp -R "$P" "$S/"
python3 - "$S/video-ad-editor/SKILL.md" <<'PY'
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
full = ('description: يمنتج فيديو كلام للكاميرا إلى ريل/إعلان 9:16: يشيل السكتات، كابشن عربي بتوقيت الكلمة، وموشن قرافيكس بألوانه. '
        'وفيه مونتاج مقاطع بلا كلام وبودكاست بكاميرتين. Use when user says "منتج هذا المقطع"، "سو من هذا الفيديو إعلان"، "شيّل السكتات"، '
        '"حوّل الفيديو لريل"، "ركّب كابشن عربي"، "اقص الصمت"، "مونتاج من هالمقاطع"، "بودكاست"، "كاميرتين"، or sends a talking video/clip folder. '
        'Also a no-person 3D motion-graphics explainer from text: "فيديو موشن"، "شرح بالموشن"، "سو فيديو من هالنص"، "موشن قرافيكس"، '
        '"اشرح هالموقع/التطبيق بفيديو"، "اشرح لي شلون يشتغل [جهاز]" (cutaway machine drawn in ink, then runs). Also a full 16:9 YouTube podcast edit from raw multi-camera files ("الحلقة كاملة بالعرض"). '
        'Not for carousels or video covers.')
lines = s.split("\n"); i = next(k for k, l in enumerate(lines) if l.startswith("description:"))
lines[i] = full; open(p, "w", encoding="utf-8").write("\n".join(lines))
PY
( cd "$S" && zip -qr "$REPO/dist/video-ad-editor.skill" video-ad-editor -x '*/.DS_Store' ); rm -rf "$S"
# فحوص
for z in video-ad-editor.skill video-studio.plugin; do N="$(unzip -Z1 "dist/$z" | grep -vc '/$')"; [ "$N" -le 200 ] || { echo "❌ $z فيه $N ملف (الحد 200)"; exit 1; }; echo "  $z: $N ملف"; done
V="$(cat "$P/VERSION")"; PV="$(python3 -c "import json;print(json.load(open('$T/.claude-plugin/plugin.json'))['version'])")"
[ "$V" = "$PV" ] || { echo "❌ VERSION ($V) ≠ plugin.json ($PV)"; exit 1; }
! grep -rIl "/Users/" "$P" | grep -q . || { echo "❌ فيه مسار شخصي:"; grep -rIl "/Users/" "$P"; exit 1; }
( cd "$T" && claude plugin validate . >/dev/null && claude plugin validate .claude-plugin/plugin.json >/dev/null ) || { echo "❌ فحص الـplugin فشل"; exit 1; }
echo "✅ v$V جاهز بـdist/ — .plugin $(du -h dist/video-studio.plugin | cut -f1) · .skill $(du -h dist/video-ad-editor.skill | cut -f1)"

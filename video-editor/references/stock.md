<!-- Shared reference — free stock footage and photos -->

# Stock footage and photos (free) — `38_stock.py`

Cheapest source of b-roll: **try stock first**, then free Gemini images, then Google Flow, and only then paid generation.

Sources: **Pexels** (video + photos) · **Pixabay** (video + photos) · **Unsplash** (photos). Keys are free:
`PEXELS_API_KEY`, `PIXABAY_API_KEY`, `UNSPLASH_ACCESS_KEY` (environment or `.env`). Check: `python3 scripts/38_stock.py keys`.
No key yet? Say in one line which sign-up pages are needed (pexels.com/api · pixabay.com/api/docs · unsplash.com/developers) and ask the user to paste the key into `.env` — never into chat history you re-print.

```bash
python3 scripts/38_stock.py search <work> "coffee being poured, close up" --kind video --orient portrait --minsec 3
python3 scripts/38_stock.py get <work> 4 --k coffee           # item 4 from the list → stock/…mp4, credit saved
python3 scripts/17_gen_scenes.py <work> import coffee <path printed above>   # becomes an asset like any generated clip
python3 scripts/38_stock.py credits <work>                    # who to credit
```

## Rules
1. **Write the query in English as a short caption** ("a person typing on a laptop at night"). Translate from the user's language yourself.
2. Show the **thumbnails/titles** (3–6 candidates) and let the user pick, or pick by the script's meaning and say why. Look at the file (`ffmpeg` one frame) before using it.
3. Vertical first (`--orient portrait`); a landscape clip is fine as a background with the engine's crop.
4. **Local alternative** for the user's own footage: `references/find-shots.md` (semantic search).
5. Licences allow commercial use without mandatory credit, but always keep `stock/credits.json`; offer to add a credit line to the caption. No people in sensitive contexts; no logos/brands as the subject unless the user wants them.
6. Rate limits are modest — search once per scene, not per word.

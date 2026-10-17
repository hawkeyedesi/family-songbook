"""Build the static family songbook. Run: python3 build.py"""
from pathlib import Path
import json
from html import escape

ROOT = Path(__file__).resolve().parent
songs = json.loads((ROOT / "data/songs.json").read_text())
assert len({s["slug"] for s in songs}) == len(songs), "Duplicate song slug"

KANNADA_STACK = '"Kannada Sangam MN","Noto Sans Kannada","Noto Serif Kannada","Kedage",system-ui,sans-serif'


def scans_for(song):
    items = song.get("scans") or []
    if song.get("scan"):
        items = [song["scan"], *[s for s in items if s != song["scan"]]]
    assert items, f"No scans for {song['slug']}"
    for name in items:
        assert (ROOT / "assets" / name).is_file(), f"Missing scan {name}"
    return items


def shell(title, description, body, prefix="", lang="en"):
    return f"""<!doctype html>
<html lang="{escape(lang)}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · ಭಕ್ತಿ</title><meta name="description" content="{escape(description, quote=True)}">
<meta name="theme-color" content="#f7f3eb"><meta property="og:title" content="{escape(title, quote=True)} · ಭಕ್ತಿ">
<meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:type" content="website">
<link rel="stylesheet" href="{prefix}assets/style.css"><script defer src="{prefix}assets/site.js"></script></head>
<body><header><a class="brand" href="{prefix or "./"}" aria-label="Bhakti home"><span class="symbol" aria-hidden="true">✺</span> ಭಕ್ತಿ</a><span class="header-note">ಕುಟುಂಬದ ಭಕ್ತಿ ಸಂಗ್ರಹ</span></header>
<main>{body}</main><footer>ನಮ್ಮ ಸಂಗ್ರಹ. ನಮ್ಮ ಸಂಪ್ರದಾಯ.<br><span>ಶ್ಲೋಕಗಳು ಮತ್ತು ಭಜನೆಗಳು — ಓದಿ, ಪಠಿಸಿ, ಹಂಚಿಕೊಳ್ಳಿ.</span></footer></body></html>"""


cards = "".join(
    f"""<a class="song-card" href="songs/{escape(s["slug"])}/"><span class="eyebrow">{escape(s["category"])}</span><h2>{escape(s["title"])}</h2><p>{escape(s["description"])}</p><span class="card-bottom">{escape(s["language"])}<span aria-hidden="true">↗</span></span></a>"""
    for s in songs
)
home = f"""<section class="intro"><span class="eyebrow">ನಮ್ಮ ಸಂಗ್ರಹ</span><h1>ನಿತ್ಯಪಾರಾಯಣದ ಸಂಗಾತಿ.</h1><p>ಶ್ಲೋಕಗಳು ಮತ್ತು ಭಜನೆಗಳು — ನಿತ್ಯಪಾರಾಯಣಕ್ಕೆ,<br class="desktop"> ಕುಟುಂಬದೊಂದಿಗೆ ಹಾಡಲು.</p></section>
<section aria-label="Song collection"><div class="collection-heading"><h2>ಭಕ್ತಿ ಸಂಗ್ರಹ</h2><span>{len(songs)} ಪಠ್ಯಗಳು</span></div><label class="search-label" for="search">ಶ್ಲೋಕ ಅಥವಾ ಭಜನೆ ಹುಡುಕಿ</label><input id="search" type="search" placeholder="ಸಂಗ್ರಹದಲ್ಲಿ ಹುಡುಕಿ…" autocomplete="off"><div class="cards">{cards}</div><p id="empty" hidden>ಪಠ್ಯ ಸಿಗಲಿಲ್ಲ. ಬೇರೊಂದು ಹೆಸರು ಹುಡುಕಿ.</p></section>
<aside class="collection-note">ಇದು ಬೆಳೆಯುವ ಸಂಗ್ರಹ. ಪ್ರತಿಯೊಂದಕ್ಕೂ ತನ್ನದೇ ಲಿಂಕ್ ಇದೆ — ಬುಕ್‌ಮಾರ್ಕ್ ಮಾಡಿ, ಕುಟುಂಬದೊಂದಿಗೆ ಹಂಚಿ.</aside>"""
(ROOT / "index.html").write_text(
    shell(
        "ಕುಟುಂಬದ ಭಕ್ತಿ ಸಂಗ್ರಹ",
        "ಶ್ಲೋಕ ಮತ್ತು ಭಜನೆಗಳ ಕುಟುಂಬ ಸಂಗ್ರಹ. ಕನ್ನಡ ಲಿಪಿಯಲ್ಲಿ, ಮೂಲ ಪುಟಗಳೊಂದಿಗೆ.",
        home,
        lang="kn",
    )
)

for song in songs:
    slug = song["slug"]
    assert slug and all(c in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in slug), "Invalid slug"
    images = scans_for(song)
    p = ROOT / "songs" / slug
    p.mkdir(parents=True, exist_ok=True)
    kn = song.get("script") == "kannada"
    chorus_lines = song.get("chorus") or []
    chorus_html = ""
    if chorus_lines:
        chorus = "<br>".join(escape(x) for x in chorus_lines)
        chorus_html = f'<section class="chorus"><span class="eyebrow">ಪಲ್ಲವಿ</span><p>{chorus}</p></section>'
    verses = "".join(
        f'<section class="verse"><span class="verse-number">{i:02}</span><p>{"<br>".join(escape(x) for x in lines)}</p></section>'
        for i, lines in enumerate(song.get("verses") or [], 1)
    )
    scan_blocks = []
    for i, name in enumerate(images, 1):
        label = f"ಮೂಲ ಪುಟ {i}" if len(images) > 1 else "ಮೂಲ ಪುಟ"
        scan_blocks.append(
            f"""<details{" open" if i == 1 else ""}><summary>{escape(label)}</summary>
<a href="../../assets/{escape(name)}" target="_blank" rel="noopener"><img src="../../assets/{escape(name)}" alt="{escape(song["title"])} — original page {i}" loading="lazy"></a>
<p>ಪೂರ್ಣ ಗಾತ್ರಕ್ಕೆ ಚಿತ್ರವನ್ನು ತಟ್ಟಿ.</p></details>
<a class="download" href="../../assets/{escape(name)}" download>ಈ ಪುಟವನ್ನು ಇಳಿಸಿ ↓</a>"""
        )
    references = song.get("references", [])
    ref_html = "" if not references else '<h3>ಪಠ್ಯ ಪರಿಶೀಲನೆಗೆ ಆಧಾರಗಳು</h3><ul>' + ''.join(f'<li><a href="{escape(r["url"], quote=True)}" target="_blank" rel="noopener">{escape(r["label"])}</a></li>' for r in references) + '</ul>'
    kn_class = " kn" if kn else ""
    body = f"""<nav class="back"><a href="../../">← ಸಂಗ್ರಹಕ್ಕೆ ಹಿಂತಿರುಗಿ</a></nav><section class="song-heading"><span class="eyebrow">{escape(song["category"])} / {escape(song["language"])}</span><h1>{escape(song["title"])}</h1><p>{escape(song["description"])}</p></section>
<div class="toolbar" aria-label="Reading tools"><div class="font-controls"><button id="smaller" aria-label="Smaller text">ಅ−</button><button id="larger" aria-label="Larger text">ಅ+</button></div><button id="print">ಮುದ್ರಿಸಿ / ಉಳಿಸಿ</button><button id="share">ಹಂಚಿಕೊಳ್ಳಿ ↗</button></div><p id="share-status" role="status" aria-live="polite"></p>
<article class="lyrics{kn_class}" aria-label="Lyrics">{chorus_html}{verses}</article>
<section class="source"><h2>ಮೂಲ ಪುಟ</h2><p>{escape(song["note"])}</p>{ref_html}{"".join(scan_blocks)}</section>"""
    (p / "index.html").write_text(
        shell(song["title"], song["description"], body, "../../", "kn" if kn else "en")
    )

print(f"Built collection + {len(songs)} song page(s).")

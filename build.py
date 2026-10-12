"""Build the static family songbook. Run: python3 build.py"""
from pathlib import Path
import json
from html import escape

ROOT = Path(__file__).resolve().parent
songs = json.loads((ROOT / 'data/songs.json').read_text())
assert len({s['slug'] for s in songs}) == len(songs), 'Duplicate song slug'

def shell(title, description, body, prefix=''):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · Bhakti</title><meta name="description" content="{escape(description, quote=True)}">
<meta name="theme-color" content="#f7f3eb"><meta property="og:title" content="{escape(title, quote=True)} · Bhakti">
<meta property="og:description" content="{escape(description, quote=True)}"><meta property="og:type" content="website">
<link rel="stylesheet" href="{prefix}assets/style.css"><script defer src="{prefix}assets/site.js"></script></head>
<body><header><a class="brand" href="{prefix or './'}" aria-label="Bhakti home"><span class="symbol" aria-hidden="true">✺</span> Bhakti</a><span class="header-note">A family songbook</span></header>
<main>{body}</main><footer>A little collection. A lasting tradition.<br><span>Shlokas &amp; bhajans, kept close and shared with love.</span></footer></body></html>'''

cards = ''.join(f'''<a class="song-card" href="songs/{escape(s['slug'])}/"><span class="eyebrow">{escape(s['category'])}</span><h2>{escape(s['title'])}</h2><p>{escape(s['description'])}</p><span class="card-bottom">{escape(s['language'])}<span aria-hidden="true">↗</span></span></a>''' for s in songs)
body = f'''<section class="intro"><span class="eyebrow">OUR COLLECTION</span><h1>Words to return to.</h1><p>Shlokas and bhajans for quiet moments, daily prayer,<br class="desktop"> and singing together.</p></section>
<section aria-label="Song collection"><div class="collection-heading"><h2>The songbook</h2><span>{len(songs)} {'entry' if len(songs)==1 else 'entries'}</span></div><label class="search-label" for="search">Find a shloka or bhajan</label><input id="search" type="search" placeholder="Search the collection…" autocomplete="off"><div class="cards">{cards}</div><p id="empty" hidden>No matches. Try another title or language.</p></section>
<aside class="collection-note">This is a growing collection. Each entry has its own link, ready to bookmark or share with family.</aside>'''
(ROOT / 'index.html').write_text(shell('A family songbook', 'A growing family collection of shlokas and bhajans, with readable lyrics and original scans.', body))

for song in songs:
    slug = song['slug']
    assert slug and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in slug), 'Invalid slug'
    assert (ROOT / 'assets' / song['scan']).is_file(), 'Missing scan'
    p = ROOT / 'songs' / slug
    p.mkdir(parents=True, exist_ok=True)
    chorus = '<br>'.join(escape(x) for x in song.get('chorus', []))
    verses = ''.join(f'<section class="verse"><span class="verse-number">{i:02}</span><p>{"<br>".join(escape(x) for x in lines)}</p></section>' for i, lines in enumerate(song['verses'], 1))
    body = f'''<nav class="back"><a href="../../">← All shlokas &amp; bhajans</a></nav><section class="song-heading"><span class="eyebrow">{escape(song['category'])} / {escape(song['language'])}</span><h1>{escape(song['title'])}</h1><p>{escape(song['description'])}</p></section>
<div class="toolbar" aria-label="Reading tools"><div class="font-controls"><button id="smaller" aria-label="Smaller text">A−</button><button id="larger" aria-label="Larger text">A+</button></div><button id="print">Print / Save PDF</button><button id="share">Share link ↗</button></div><p id="share-status" role="status" aria-live="polite"></p>
<article class="lyrics" aria-label="Lyrics"><section class="chorus"><span class="eyebrow">CHORUS</span><p>{chorus}</p></section>{verses}</article>
<section class="source"><h2>The original page</h2><p>{escape(song['note'])}</p><details><summary>View the original scan</summary><a href="../../assets/{escape(song['scan'])}" target="_blank" rel="noopener"><img src="../../assets/{escape(song['scan'])}" alt="Original printed page of {escape(song['title'])}" loading="lazy" width="900" height="1200"></a><p>Tap the image to open it at full size.</p></details><a class="download" href="../../assets/{escape(song['scan'])}" download>Download original photo ↓</a></section>'''
    (p / 'index.html').write_text(shell(song['title'], song['description'], body, '../../'))
print(f'Built collection + {len(songs)} song page(s).')

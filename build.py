"""Build Bhakti's static pages. Run: python3 build.py (stdlib only)."""
from pathlib import Path
import json,re
from html import escape as e
ROOT=Path(__file__).resolve().parent
songs=json.loads((ROOT/'data/songs.json').read_text())
assert len({s['slug'] for s in songs})==len(songs),'Duplicate slug'
UI={
'kn':dict(brand='ಭಕ್ತಿ',family='ಕುಟುಂಬದ ಭಕ್ತಿ ಸಂಗ್ರಹ',footer='ನಮ್ಮ ಸಂಗ್ರಹ. ನಮ್ಮ ಸಂಪ್ರದಾಯ.',footer_note='ಶ್ಲೋಕಗಳು ಮತ್ತು ಭಜನೆಗಳು — ಓದಿ, ಪಠಿಸಿ, ಹಂಚಿಕೊಳ್ಳಿ.',back='← ಸಂಗ್ರಹಕ್ಕೆ ಹಿಂತಿರುಗಿ',smaller='ಅ−',larger='ಅ+',print='ಮುದ್ರಿಸಿ / ಉಳಿಸಿ',share='ಹಂಚಿಕೊಳ್ಳಿ ↗',source='ಮೂಲ ಮತ್ತು ಪರಿಶೀಲನೆ',scan='ಮೂಲ ಪುಟ',fullsize='ಪೂರ್ಣ ಗಾತ್ರಕ್ಕೆ ಚಿತ್ರವನ್ನು ತಟ್ಟಿ.',download='ಈ ಪುಟವನ್ನು ಇಳಿಸಿ ↓',references='ಪಠ್ಯ ಪರಿಶೀಲನೆಗೆ ಆಧಾರಗಳು',choose='ಲಿಪಿ ಆಯ್ಕೆ / Choose script',sections='ಭಾಗಕ್ಕೆ ಹೋಗಿ',count='ಪಠ್ಯಗಳು'),
'en':dict(brand='Bhakti',family='A family songbook',footer='A little collection. A lasting tradition.',footer_note='Shlokas & bhajans — read, chant, and share.',back='← Back to the collection',smaller='A−',larger='A+',print='Print / Save PDF',share='Share link ↗',source='Sources & text notes',scan='Original page',fullsize='Tap the image to open it at full size.',download='Download this page ↓',references='Text comparison sources',choose='Choose script / ಲಿಪಿ ಆಯ್ಕೆ',sections='Jump to a section',count='entries')}

def localized(s,key,ui):return s.get(key+'_en',s[key]) if ui=='en' else s[key]
def shell(title,description,body,prefix='',lang='kn',ui='kn'):
 u=UI[ui];home=prefix+('en/' if ui=='en' else '')
 return f'''<!doctype html>
<html lang="{lang}" data-ui="{ui}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · {u['brand']}</title><meta name="description" content="{e(description,quote=True)}">
<meta name="theme-color" content="#f7f3eb"><meta property="og:title" content="{e(title,quote=True)} · {u['brand']}"><meta property="og:description" content="{e(description,quote=True)}"><meta property="og:type" content="website">
<link rel="stylesheet" href="{prefix}assets/style.css"><script defer src="{prefix}assets/site.js"></script></head>
<body><header><a class="brand" href="{home or './'}"><span class="symbol" aria-hidden="true">✺</span> {u['brand']}</a><span class="header-note">{u['family']}</span></header>
<main>{body}</main><footer>{u['footer']}<br><span>{u['footer_note']}</span></footer></body></html>'''

def home(ui):
 en=ui=='en';prefix='../' if en else '';u=UI[ui]
 cards=[]
 for s in songs:
  multi='versions_file' in s
  target=prefix+'songs/'+s['slug']+'/'+('roman/' if en and multi else '')
  aliases=' '.join([s['title'],s.get('title_en',''),s['category'],s.get('category_en','')])
  cards.append(f'''<a class="song-card" href="{target}" data-work="{s['slug']}" data-multiscript="{str(multi).lower()}" data-base="{prefix}songs/{s['slug']}/" data-search="{e(aliases,quote=True)}"><span class="eyebrow">{e(localized(s,'category',ui))}</span><h2>{e(localized(s,'title',ui))}</h2><p>{e(localized(s,'description',ui))}</p><span class="card-bottom">{e(localized(s,'language',ui))}<span aria-hidden="true">↗</span></span></a>''')
 toggle=f'''<nav class="language-switch" aria-label="Landing page language"><a href="{prefix or './'}" {'aria-current="page"' if not en else ''}>ಕನ್ನಡ</a><a href="{prefix}en/" {'aria-current="page"' if en else ''}>English (Roman)</a></nav>'''
 title='Words to return to.' if en else 'ನಿತ್ಯಪಾರಾಯಣದ ಸಂಗಾತಿ.'
 intro='Shlokas and bhajans for daily prayer,<br class="desktop"> quiet moments, and chanting together.' if en else 'ಶ್ಲೋಕಗಳು ಮತ್ತು ಭಜನೆಗಳು — ನಿತ್ಯಪಾರಾಯಣಕ್ಕೆ,<br class="desktop"> ಕುಟುಂಬದೊಂದಿಗೆ ಹಾಡಲು.'
 body=f'''{toggle}<section class="intro"><span class="eyebrow">{'OUR COLLECTION' if en else 'ನಮ್ಮ ಸಂಗ್ರಹ'}</span><h1>{title}</h1><p>{intro}</p></section>
<section aria-label="Song collection"><div class="collection-heading"><h2>{'The songbook' if en else 'ಭಕ್ತಿ ಸಂಗ್ರಹ'}</h2><span>{len(songs)} {u['count']}</span></div><label class="search-label" for="search">{'Find a shloka or bhajan' if en else 'ಶ್ಲೋಕ ಅಥವಾ ಭಜನೆ ಹುಡುಕಿ'}</label><input id="search" type="search" placeholder="{'Search by Kannada or Roman title…' if en else 'ಕನ್ನಡ ಅಥವಾ ರೋಮನ್ ಹೆಸರಿನಿಂದ ಹುಡುಕಿ…'}" autocomplete="off"><div class="cards">{''.join(cards)}</div><p id="empty" hidden>{'No matches. Try another title.' if en else 'ಪಠ್ಯ ಸಿಗಲಿಲ್ಲ. ಬೇರೊಂದು ಹೆಸರು ಹುಡುಕಿ.'}</p></section>
<aside class="collection-note">{'A growing collection. Each entry has its own link to bookmark or share. Choose a script on the new multilingual entries.' if en else 'ಇದು ಬೆಳೆಯುವ ಸಂಗ್ರಹ. ಪ್ರತಿಯೊಂದಕ್ಕೂ ತನ್ನದೇ ಲಿಂಕ್ ಇದೆ. ಬಹುಲಿಪಿಯ ಪಠ್ಯಗಳಲ್ಲಿ ನಿಮಗೆ ಬೇಕಾದ ಲಿಪಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.'}</aside>'''
 p=ROOT/'en/index.html' if en else ROOT/'index.html';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(shell('A family songbook' if en else 'ಕುಟುಂಬದ ಭಕ್ತಿ ಸಂಗ್ರಹ','Shlokas and bhajans in one growing family collection.' if en else 'ಶ್ಲೋಕ ಮತ್ತು ಭಜನೆಗಳ ಕುಟುಂಬ ಸಂಗ್ರಹ.',body,prefix,'en' if en else 'kn',ui))

def scans(s):
 images=s.get('scans',[])
 if s.get('scan'):images=[s['scan']]+[n for n in images if n!=s['scan']]
 for n in images:assert (ROOT/'assets'/n).is_file(),n
 return images

def refs_html(refs,ui):
 if not refs:return ''
 return '<h3>'+UI[ui]['references']+'</h3><ul>'+''.join(f'<li><a href="{e(r["url"],quote=True)}" target="_blank" rel="noopener">{e(r["label"])}</a></li>' for r in refs)+'</ul>'

def toolbar(ui):
 u=UI[ui]
 return f'''<div class="toolbar" aria-label="Reading tools"><div class="font-controls"><button id="smaller" aria-label="Smaller text">{u['smaller']}</button><button id="larger" aria-label="Larger text">{u['larger']}</button></div><button id="print">{u['print']}</button><button id="share">{u['share']}</button></div><p id="share-status" role="status" aria-live="polite"></p>'''

def scan_html(s,ui,prefix):
 u=UI[ui];parts=[]
 for i,name in enumerate(scans(s),1):
  parts.append(f'''<details{' open' if i==1 else ''}><summary>{u['scan']} {i}</summary><a href="{prefix}assets/{e(name)}" target="_blank" rel="noopener"><img src="{prefix}assets/{e(name)}" alt="{e(s['title'],quote=True)} — original page {i}" loading="lazy"></a><p>{u['fullsize']}</p></details><a class="download" href="{prefix}assets/{e(name)}" download>{u['download']} ↓</a>''')
 return ''.join(parts)

def render_legacy(s):
 kn=s.get('script')=='kannada';slug=s['slug'];prefix='../../';u=UI['kn'];chorus=''
 if s.get('chorus'):chorus='<section class="chorus"><span class="eyebrow">ಪಲ್ಲವಿ</span><p>'+'<br>'.join(e(x) for x in s['chorus'])+'</p></section>'
 verses=''.join(f'<section class="verse" id="verse-{i}"><span class="verse-number">{i:02}</span><p>{"<br>".join(e(x) for x in lines)}</p></section>' for i,lines in enumerate(s['verses'],1))
 body=f'''<nav class="back"><a href="../../">{u['back']}</a></nav><section class="song-heading"><span class="eyebrow">{e(s['category'])} / {e(s['language'])}</span><h1>{e(s['title'])}</h1><p>{e(s['description'])}</p></section>{toolbar('kn')}<article class="lyrics{' kn' if kn else ''}" aria-label="Lyrics">{chorus}{verses}</article><section class="source"><h2>{u['source']}</h2><p>{e(s['note'])}</p>{refs_html(s.get('references',[]),'kn')}{scan_html(s,'kn',prefix)}</section>'''
 p=ROOT/'songs'/slug/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(shell(s['title'],s['description'],body,prefix,'kn' if kn else 'en'))

# Keep each source paragraph intact. Numbered verse markers define stable anchors.
HEADINGS=re.compile(r'^(?:ಕರನ್ಯಾಸಃ|ಅಂಗನ್ಯಾಸಃ|ಧ್ಯಾನಂ|ಹರಿಃ ಓಂ|ಪೂರ್ವ ಪೀಠಿಕಾ|ಉತ್ತರ ಪೀಠಿಕಾ|ಫಲಶ್ರುತಿಃ|ಸ್ತೋತ್ರಂ|करन्यासः|अंगन्यासः|ध्यानं|हरिः ॐ|पूर्व पीठिका|उत्तर पीठिका|फलश्रुतिः|स्तोत्रं|karanyāsaḥ|aṅganyāsaḥ|dhyānaṃ|hariḥ ōṃ|pūrva pīṭhikā|uttara pīṭhikā|phalaśrutiḥ|stōtraṃ)$')
def render_chapter(c):
 out=[f'<section class="text-chapter" id="{c["id"]}"><h2>{e(c["title"])}</h2>'];pending=[];occ={}
 def flush(number=None):
  if not pending:return
  if number is not None:
   occ[number]=occ.get(number,0)+1;anchor=f'{c["id"]}-verse-{number}-{occ[number]}'
   out.append(f'<div class="source-verse" id="{anchor}" data-verse="{number}">')
  else:out.append('<div class="source-verse unnumbered">')
  out.append('<p>'+'<br>'.join(e(x) for x in pending)+'</p></div>');pending.clear()
 for p in c['paragraphs']:
  if HEADINGS.fullmatch(p):flush();out.append('<h3>'+e(p)+'</h3>');continue
  pending.append(p)
  m=re.search(r'[।॥]\s*(\d+)\s*॥',p)
  if m:flush(int(m[1]))
  elif p.rstrip().endswith('॥'):flush()
 flush();out.append('</section>');return ''.join(out)

def render_multiscript(s):
 bundle=json.loads((ROOT/'data'/s['versions_file']).read_text());versions=bundle['versions']
 assert [v['id'] for v in versions]==['kannada','devanagari','roman']
 sequences=[[int(x) for c in v['chapters'] for p in c['paragraphs'] for x in re.findall(r'[।॥]\s*(\d+)\s*॥',p)] for v in versions]
 assert sequences[0]==sequences[1]==sequences[2],s['slug']
 for v in versions:
  vid=v['id'];ui='kn' if vid=='kannada' else 'en';u=UI[ui];deep=vid!='kannada';prefix='../../../' if deep else '../../';base='../' if deep else './'
  nav='<nav class="script-switch" aria-label="Choose reading script">'+''.join(f'<a href="{base}{"" if w["id"]=="kannada" else w["id"]+"/"}" data-script="{w["id"]}" {"aria-current=\"page\"" if vid==w["id"] else ""}>{e(w["label"])}</a>' for w in versions)+'</nav>'
  toc='<nav class="chapter-nav" aria-label="Sections"><span>'+u['sections']+':</span>'+''.join(f'<a href="#{c["id"]}">{e(c["title"])}</a>' for c in v['chapters'])+'</nav>'
  body=f'''<nav class="back"><a href="{prefix}{'en/' if ui=='en' else ''}">{u['back']}</a></nav><section class="song-heading"><span class="eyebrow">{e(localized(s,'category',ui))} / {e(v['label'])}</span><h1>{e(v['title'])}</h1><p>{e(localized(s,'description',ui))}</p></section><div class="script-label">{u['choose']}</div>{nav}{toc}{toolbar(ui)}<article class="lyrics multilingual {vid}" lang="{v['lang']}" aria-label="Prayer text">{''.join(render_chapter(c) for c in v['chapters'])}</article><section class="source"><h2>{u['source']}</h2><p>{e(localized(s,'note',ui))}</p>{refs_html(v['references']+s.get('references',[]),ui)}</section>'''
  p=ROOT/'songs'/s['slug']/('' if not deep else vid)/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(shell(v['title'],localized(s,'description',ui),body,prefix,v['lang'],ui))

home('kn');home('en')
for s in songs:
 assert s['slug'] and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in s['slug'])
 if 'versions_file' in s:render_multiscript(s)
 else:render_legacy(s)
print(f'Built 2 landing pages, {len(songs)} entries and {sum(3 if "versions_file" in s else 1 for s in songs)} reading pages.')

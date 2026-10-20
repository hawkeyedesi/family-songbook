"""Build Bhakti's static pages. Run: python3 build.py (stdlib only)."""
from pathlib import Path
import json,re
from html import escape as e
ROOT=Path(__file__).resolve().parent
songs=json.loads((ROOT/'data/songs.json').read_text())
assert len({s['slug'] for s in songs})==len(songs),'Duplicate slug'
from source_audit import badge as audit_badge, render as render_audit, validate as validate_audit
validate_audit(songs)
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

COLLECTIONS={'daily':('ದಿನನಿತ್ಯ','Daily'),'weekly':('ವಾರದ ಪಠ್ಯಗಳು','Weekly'),'friday':('ಶುಕ್ರವಾರ','Friday'),'paduka-puja-bhajans':('ಪಾದುಕಾ ಪೂಜಾ ಭಜನೆಗಳು','Paduka Puja Bhajans')}
TAGS={'navaratri':('ನವರಾತ್ರಿ','Navaratri')}
FILTERS={**COLLECTIONS,**TAGS}
def memberships(s):return s.get('collections',[s.get('collection','daily')])+s.get('tags',[])
def work_tags(s,ui,prefix):
 return '<nav class="work-tags" aria-label="Tags">'+''.join(f'<a href="{prefix}{"en/" if ui=="en" else ""}{tag}/">{e(TAGS[tag][1 if ui=="en" else 0])}</a>' for tag in s.get('tags',[]) if tag in TAGS)+'</nav>' if s.get('tags') else ''
def home(ui,collection=None):
 en=ui=='en';prefix='../'*((1 if en else 0)+(1 if collection else 0));u=UI[ui]
 selected=[s for s in songs if collection is None or collection in memberships(s)]
 if collection:selected.sort(key=lambda s:s.get('collection_order',{}).get(collection,999))
 collection_labels=FILTERS
 group_base=prefix+('en/' if en else '')
 category_links='<nav class="collection-nav" aria-label="Collection categories">'
 for key in [None,*FILTERS]:
  label=('All' if en else 'ಎಲ್ಲವೂ') if key is None else collection_labels[key][1 if en else 0]
  count=len(songs) if key is None else sum(key in memberships(x) for x in songs)
  target=group_base+(key+'/' if key else '')
  category_links+=f'<a href="{target or './'}" data-collection="{key or 'all'}" '+('aria-current="page"' if key==collection else '')+f'>{label} <span>{count}</span></a>'
 category_links+=f'<a href="{group_base}kamalamma-ajji/" data-collection="kamalamma-ajji">'+('Kamalamma Ajji' if en else 'ಕಮಲಮ್ಮ ಅಜ್ಜಿ')+'</a></nav>'
 cards=[]
 for s in selected:
  multi='versions_file' in s
  target=prefix+'songs/'+s['slug']+'/'+('roman/' if en and multi else '')
  aliases=' '.join([s['title'],s.get('title_en',''),s['category'],s.get('category_en','')]+s.get('search_aliases',[])+(['Navaratri Navarathri ನವರಾತ್ರಿ नवरात्रि'] if 'navaratri' in s.get('tags',[]) else []))
  cards.append(f'''<a class="song-card" href="{target}" data-work="{s['slug']}" data-multiscript="{str(multi).lower()}" data-base="{prefix}songs/{s['slug']}/" data-search="{e(aliases,quote=True)}"><span class="eyebrow">{e(localized(s,'category',ui))}</span><h2>{e(localized(s,'title',ui))}</h2><p>{e(localized(s,'description',ui))}</p><span class="card-bottom">{e(localized(s,'language',ui))}<span aria-hidden="true">↗</span></span></a>''')
 category_path=collection+'/' if collection else ''
 toggle=f'''<nav class="language-switch" aria-label="Landing page language"><a href="{prefix+category_path or './'}" {'aria-current="page"' if not en else ''}>ಕನ್ನಡ</a><a href="{prefix}en/{category_path}" {'aria-current="page"' if en else ''}>English (Roman)</a></nav>'''
 title=('Navaratri prayers' if en else 'ನವರಾತ್ರಿ ಪಾರಾಯಣ') if collection in TAGS else ('Words to return to.' if en else 'ನಿತ್ಯಪಾರಾಯಣದ ಸಂಗಾತಿ.')
 intro='Shlokas and bhajans for daily prayer,<br class="desktop"> quiet moments, and chanting together.' if en else 'ಶ್ಲೋಕಗಳು ಮತ್ತು ಭಜನೆಗಳು — ನಿತ್ಯಪಾರಾಯಣಕ್ಕೆ,<br class="desktop"> ಕುಟುಂಬದೊಂದಿಗೆ ಹಾಡಲು.'
 recording=''
 if collection=='navaratri':
  from navaratri import render as render_recording
  recording=render_recording(ui,prefix,songs,render_chapter)+'<p class="chant-link"><a href="'+prefix+('en/' if en else '')+'durga-saptashloki/">'+('▶ Durga Saptashloki — Guruji chant-along' if en else '▶ ದುರ್ಗಾ ಸಪ್ತಶ್ಲೋಕಿ — ಗುರುಗಳ ಪಠಣ')+'</a></p>'
 body=f'''{toggle}{category_links}<section class="intro"><span class="eyebrow">{'OUR COLLECTION' if en else 'ನಮ್ಮ ಸಂಗ್ರಹ'}</span><h1>{title}</h1><p>{intro}</p></section>{recording}
<section aria-label="Song collection"><div class="collection-heading"><h2>{'The songbook' if en else 'ಭಕ್ತಿ ಸಂಗ್ರಹ'}</h2><span>{len(selected)} {u['count']}</span></div><label class="search-label" for="search">{'Find a shloka or bhajan' if en else 'ಶ್ಲೋಕ ಅಥವಾ ಭಜನೆ ಹುಡುಕಿ'}</label><input id="search" type="search" placeholder="{'Search by Kannada or Roman title…' if en else 'ಕನ್ನಡ ಅಥವಾ ರೋಮನ್ ಹೆಸರಿನಿಂದ ಹುಡುಕಿ…'}" autocomplete="off"><div class="cards">{''.join(cards)}</div>{('<p class="category-empty">'+('No entries in this category yet.' if en else 'ಈ ವಿಭಾಗದಲ್ಲಿ ಇನ್ನೂ ಪಠ್ಯಗಳಿಲ್ಲ.')+'</p>') if not selected else ''}<p id="empty" hidden>{'No matches. Try another title.' if en else 'ಪಠ್ಯ ಸಿಗಲಿಲ್ಲ. ಬೇರೊಂದು ಹೆಸರು ಹುಡುಕಿ.'}</p></section>
<p class="source-check"><a href="{prefix}{'en/' if en else ''}source-checks/">{'Sringeri source checks — results & differences' if en else 'ಶೃಂಗೇರಿ ಮೂಲಪಾಠ ಪರಿಶೀಲನೆಯ ಫಲಿತಾಂಶಗಳು'} ↗</a></p><aside class="collection-note">{'A growing collection. Each entry has its own link to bookmark or share. Choose a script on the new multilingual entries.' if en else 'ಇದು ಬೆಳೆಯುವ ಸಂಗ್ರಹ. ಪ್ರತಿಯೊಂದಕ್ಕೂ ತನ್ನದೇ ಲಿಂಕ್ ಇದೆ. ಬಹುಲಿಪಿಯ ಪಠ್ಯಗಳಲ್ಲಿ ನಿಮಗೆ ಬೇಕಾದ ಲಿಪಿಯನ್ನು ಆಯ್ಕೆಮಾಡಿ.'}</aside>'''
 p=ROOT/('en' if en else '')/(collection or '')/'index.html';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(shell('A family songbook' if en else 'ಕುಟುಂಬದ ಭಕ್ತಿ ಸಂಗ್ರಹ','Shlokas and bhajans in one growing family collection.' if en else 'ಶ್ಲೋಕ ಮತ್ತು ಭಜನೆಗಳ ಕುಟುಂಬ ಸಂಗ್ರಹ.',body,prefix,'en' if en else 'kn',ui))

def scans(s):
 images=s.get('scans',[])
 if s.get('scan'):images=[s['scan']]+[n for n in images if n!=s['scan']]
 for n in images:assert (ROOT/'assets'/n).is_file(),n
 return images

def refs_html(refs,ui):
 if not refs:return ''
 refs=list({r['url']:r for r in reversed(refs)}.values())[::-1]
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
 body=f'''<nav class="back"><a href="../../">{u['back']}</a></nav>{work_tags(s,'kn',prefix)}<section class="song-heading"><span class="eyebrow">{e(s['category'])} / {e(s['language'])}</span><h1>{e(s['title'])}</h1><p>{e(s['description'])}</p></section>{toolbar('kn')}<article class="lyrics{' kn' if kn else ''}" aria-label="Lyrics">{chorus}{verses}</article><section class="source"><h2>{u['source']}</h2><p>{e(s['note'])}</p>{refs_html(s.get('references',[]),'kn')}{scan_html(s,'kn',prefix)}</section>'''
 p=ROOT/'songs'/slug/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(shell(s['title'],s['description'],body,prefix,'kn' if kn else 'en'))

# Keep each source paragraph intact. Numbered verse markers define stable anchors.
HEADINGS=re.compile(r'^(?:ಕರನ್ಯಾಸಃ|ಅಂಗನ್ಯಾಸಃ|ಧ್ಯಾನಂ|ಹರಿಃ ಓಂ|ಪೂರ್ವ ಪೀಠಿಕಾ|ಉತ್ತರ ಪೀಠಿಕಾ|ಫಲಶ್ರುತಿಃ|ಸ್ತೋತ್ರಂ|करन्यासः|अंगन्यासः|ध्यानं|हरिः ॐ|पूर्व पीठिका|उत्तर पीठिका|फलश्रुतिः|स्तोत्रं|karanyāsaḥ|aṅganyāsaḥ|dhyānaṃ|hariḥ ōṃ|pūrva pīṭhikā|uttara pīṭhikā|phalaśrutiḥ|stōtraṃ)$')
def render_chapter(c):
 out=[f'<section class="text-chapter" id="{c["id"]}"><h2>{e(c["title"])}</h2>'];pending=[];occ={}
 if c.get('layout')=='verses':
  for i,p in enumerate(c['paragraphs'],c.get('number_start',1)):
   out.append(f'<section class="verse" id="verse-{i}" data-verse="{i}"><span class="verse-number">{i:02}</span><p>{"<br>".join(e(line) for line in p.splitlines())}</p></section>')
  return ''.join(out)+'</section>'
 if c.get('layout')=='names':
  for i,p in enumerate(c['paragraphs'],1):
   display=re.sub(r'([।|])\s*[0-9೦-೯०-९]+\s*$',r'\1',p)
   out.append(f'<div class="source-name" id="names-name-{i}" data-name="{i}"><span class="verse-number">{i:02}</span><p>{e(display)}</p></div>')
  return ''.join(out)+'</section>'

 def flush(number=None):
  if not pending:return
  if number is not None:
   occ[number]=occ.get(number,0)+1;anchor=f'{c["id"]}-verse-{number}-{occ[number]}'
   out.append(f'<div class="source-verse" id="{anchor}" data-verse="{number}">')
  else:out.append('<div class="source-verse unnumbered">')
  out.append('<p>'+'<br>'.join(e(line) for paragraph in pending for line in paragraph.splitlines())+'</p></div>');pending.clear()
 for p in c['paragraphs']:
  if HEADINGS.fullmatch(p):flush();out.append('<h3>'+e(p)+'</h3>');continue
  pending.append(p)
  m=re.search(r'[।॥]\s*(\d+)\s*॥',p)
  if m:flush(int(m[1]))
  elif p.rstrip().endswith('॥'):flush()
 flush();out.append('</section>');return ''.join(out)

def svara_html(s,v,prefix):
 if not s.get('vedic'):return ''
 kn=v['id']=='kannada'
 if s['svara_status']=='scan-only':
  url=prefix+'assets/'+scans(s)[0]
  title='ಸ್ವರಪಠಣಕ್ಕೆ ಮೂಲ ಚಿತ್ರವನ್ನು ಬಳಸಿ' if kn else 'For svara chanting, use the original marked page'
  note='ಈ ಡಿಜಿಟಲ್ ಪಾಠದಲ್ಲಿ ಸ್ವರಗುರುತುಗಳು ಇನ್ನೂ ಪರಿಶೀಲಿತವಾಗಿಲ್ಲ. ಮೂಲ ಚಿತ್ರದ ಗುರುತುಗಳನ್ನು ಸರಳ ಪಾಠದಿಂದ ಬದಲಿಸಬೇಡಿ.' if kn else 'The digital text below is not yet accent-verified. The original photographed page preserves the svara marks; do not use the plain transcription as a pitch guide.'
  link='ಸ್ವರಗುರುತುಗಳಿರುವ ಮೂಲ ಪುಟವನ್ನು ತೆರೆಯಿರಿ ↗' if kn else 'Open the original accent-marked page ↗'
  notice=f'<aside class="svara-notice scan-only" role="note"><strong>{title}</strong><p>{note}</p><a class="marked-scan-link" href="{e(url)}" target="_blank" rel="noopener">{link}</a></aside>'
 else:
  title='ವೈದಿಕ ಸ್ವರಗುರುತುಗಳನ್ನು ಉಳಿಸಲಾಗಿದೆ' if kn else 'Vedic svara marks retained from the published source'
  notice=f'<aside class="svara-notice" role="note"><strong>{title}</strong></aside>'
 title='ಸ್ವರ ಮತ್ತು ಉಚ್ಚಾರಣೆಯ ಗುರುತುಗಳು' if kn else 'Svara & pronunciation key'
 labels=(['ಅನುದಾತ್ತ — ಕಡಿಮೆ ಸ್ವರ','ಸ್ವರಿತ — ಇಳಿಯುವ ಸ್ವರ','ದೀರ್ಘ/ದ್ವಿಸ್ವರಿತ — ಮೂಲ ಸಂಪ್ರದಾಯದಂತೆ ಉಚ್ಚರಿಸಿ'] if kn else ['Anudātta — low pitch','Svarita — falling pitch','Long/double svarita — follow the source tradition’s timing'])
 examples={'kannada':['ಅ॒','ಅ॑','ಅ᳚'],'devanagari':['अ॒','अ॑','अ᳚'],'roman':['a̠ / a̱','a̍','a̎']}[v['id']]
 rows=''.join(f'<li><span class="svara-example {v["id"]}">{ex}</span><span>{label}</span></li>' for ex,label in zip(examples,labels))
 note=('ಇವು ಸ್ವರಗುರುತುಗಳು, ಒತ್ತಿಹೇಳುವ ಗುರುತುಗಳಲ್ಲ. ಗುರುತು ಇಲ್ಲದ ಪ್ರತಿಯೊಂದು ಅಕ್ಷರವೂ ಉದಾತ್ತವಲ್ಲ. ā, ī, ū ದೀರ್ಘಸ್ವರಗಳು; ಇವು ಸ್ವರಿತದ ಗುರುತುಗಳಲ್ಲ. ś, ṣ, s ಬೇರೆ ವರ್ಣಗಳು; ṭ, ḍ, ṇ ಮೂರ್ಧನ್ಯ ವರ್ಣಗಳು. ṃ/ṁ ಅನುಸ್ವಾರ; ḥ (ಕೆಲವು ಮೂಲಗಳಲ್ಲಿ :) ವಿಸರ್ಗ. ಮೂಲದ ಸಂಧಿ ಮತ್ತು ನಾಸಿಕ್ಯ ಗುರುತುಗಳನ್ನು ಉಳಿಸಲಾಗಿದೆ.' if kn else 'These are pitch marks, not stress accents. Unmarked syllables are not automatically all udātta: the notation also leaves pracaya unmarked. ā, ī, ū mark long vowels, not pitch; e/o are long Sanskrit vowels even when a source prints them without a macron. ś/ṣ/s are distinct; ṭ/ḍ/ṇ are retroflex. ṃ/ṁ marks anusvāra; ḥ (sometimes : in the source) marks visarga. Keep the source’s nasal and sandhi notation; exact recitation follows the taught śākhā.')
 return notice+f'<details class="svara-key"><summary>{title}</summary><ul>{rows}</ul><p>{note}</p></details>'

def paduka_sequence(s,ui,prefix,vid):
 if 'paduka-puja-bhajans' not in s.get('collections',[]):return ''
 ordered=sorted([w for w in songs if 'paduka-puja-bhajans' in w.get('collections',[])],key=lambda w:w.get('collection_order',{}).get('paduka-puja-bhajans',999))
 at=next(i for i,w in enumerate(ordered) if w['slug']==s['slug'])
 def link(w,direction):
  suffix='' if vid=='kannada' else vid+'/'
  title=w.get('title_en',w['title']) if ui=='en' else w['title']
  return f'<a rel="{direction}" href="{prefix}songs/{w["slug"]}/{suffix}">{"← " if direction=="prev" else ""}{e(title)}{" →" if direction=="next" else ""}</a>'
 collection=prefix+('en/' if ui=='en' else '')+'paduka-puja-bhajans/'
 middle=f'<a href="{collection}">{"Paduka Puja Bhajans" if ui=="en" else "ಪಾದುಕಾ ಪೂಜಾ ಭಜನೆಗಳು"} · {at+1}/{len(ordered)}</a>'
 return '<nav class="paduka-sequence" aria-label="Paduka Puja reading order">'+(link(ordered[at-1],'prev') if at else '')+middle+(link(ordered[at+1],'next') if at+1<len(ordered) else '')+'</nav>'

def render_multiscript(s):
 bundle=json.loads((ROOT/'data'/s['versions_file']).read_text());versions=bundle['versions']
 assert [v['id'] for v in versions]==['kannada','devanagari','roman']
 sequences=[[int(x) for c in v['chapters'] for p in c['paragraphs'] for x in re.findall(r'[।॥]\s*(\d+)\s*॥',p)] for v in versions]
 assert sequences[0]==sequences[1]==sequences[2],s['slug']
 for v in versions:
  vid=v['id'];ui='kn' if vid=='kannada' else 'en';u=UI[ui];deep=vid!='kannada';prefix='../../../' if deep else '../../';base='../' if deep else './'
  nav='<nav class="script-switch" aria-label="Choose reading script">'+''.join(f'<a href="{base}{"" if w["id"]=="kannada" else w["id"]+"/"}" data-script="{w["id"]}" {"aria-current=\"page\"" if vid==w["id"] else ""}>{e(w["label"])}</a>' for w in versions)+'</nav>'
  toc='<nav class="chapter-nav" aria-label="Sections"><span>'+u['sections']+':</span>'+''.join(f'<a href="#{c["id"]}">{e(c["title"])}</a>' for c in v['chapters'])+'</nav>'
  notation=svara_html(s,v,prefix)
  sequence=paduka_sequence(s,ui,prefix,vid)
  reading_notice=('<aside class="reading-notice" role="note">'+e(v['reading_notice'])+'</aside>') if v.get('reading_notice') else ''
  source_check=audit_badge(s,ui,prefix)
  chant_link=('<p class="chant-link"><a href="'+prefix+('en/' if ui=='en' else '')+'durga-saptashloki/">'+('▶ Chant along with Guruji — synchronized reading' if ui=='en' else '▶ ಗುರುಗಳ ಪಠಣದೊಂದಿಗೆ ಶ್ಲೋಕಗಳನ್ನು ಅನುಸರಿಸಿ')+'</a></p>') if s['slug']=='durga-saptashloki' else ''
  original=''
  if s.get('preserve_original_transcription'):
   original='<details class="original-transcription"><summary>'+('ಕುಟುಂಬದ ಮೂಲ ಕನ್ನಡ ಪಾಠ' if ui=='kn' else 'Original family-book Kannada transcription')+'</summary><div class="lyrics kn" lang="kn">'+''.join(f'<div class="source-name"><span class="verse-number">{i:02}</span><p>{"<br>".join(e(x) for x in lines)}</p></div>' for i,lines in enumerate(s['verses'],1))+'</div></details>'
  if v.get('family_archive'):
   archived=json.loads((ROOT/v['family_archive']).read_text())
   previous=next(w for w in archived['versions'] if w['id']==vid)
   archive_html=''.join(render_chapter(c) for c in previous['chapters'])
   archive_html=re.sub(r'id="([^"]+)"',r'id="family-\1"',archive_html)
   original+='<details class="previous-edition"><summary>'+('ಹಿಂದಿನ ಕುಟುಂಬದ / ಪ್ರಕಟಿತ ಪಾಠ — ಪ್ರತ್ಯೇಕವಾಗಿ ಉಳಿಸಲಾಗಿದೆ' if ui=='kn' else 'Previous family / published edition — preserved separately')+'</summary><p>'+('ಮುಖ್ಯ ಪಾರಾಯಣ ಪಾಠವು ಶೃಂಗೇರಿ ಪಾಠವಾಗಿದೆ.' if ui=='kn' else 'The main chanting text above follows Sringeri. This is the previous edition, not merged into that text.')+'</p><div class="lyrics multilingual '+vid+'" lang="'+v['lang']+'">'+archive_html+'</div></details>'
  body=f'''<nav class="back"><a href="{prefix}{'en/' if ui=='en' else ''}">{u['back']}</a></nav>{work_tags(s,ui,prefix)}<section class="song-heading"><span class="eyebrow">{e(localized(s,'category',ui))} / {e(v['label'])}</span><h1>{e(v['title'])}</h1><p>{e(localized(s,'description',ui))}</p></section><div class="script-label">{u['choose']}</div>{nav}{source_check}{chant_link}{reading_notice}{notation}{toc}{toolbar(ui)}<article class="lyrics multilingual {vid}" lang="{v['lang']}" aria-label="Prayer text">{''.join(render_chapter(c) for c in v['chapters'])}</article>{sequence}<section class="source"><h2>{u['source']}</h2><p>{e(localized(s,'note',ui))}</p>{refs_html(v['references']+s.get('references',[]),ui)}{original}{scan_html(s,ui,prefix)}</section>'''
  p=ROOT/'songs'/s['slug']/('' if not deep else vid)/'index.html';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(shell(v['title'],localized(s,'description',ui),body,prefix,v['lang'],ui))

for ui in ['kn','en']:
 prefix='../../' if ui=='en' else '../'
 title,body=render_audit(ui,prefix)
 p=ROOT/('en' if ui=='en' else '')/'source-checks'/'index.html';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(shell(title,title,body,prefix,ui,ui))
 from navaratri import render as render_recording
 r=json.loads((ROOT/'data/durga-recording.json').read_text())
 body='<nav class="back"><a href="'+prefix+('en/' if ui=='en' else '')+'navaratri/">← Navaratri</a></nav>'+render_recording(ui,prefix,songs,render_chapter,recording=r)
 p=ROOT/('en' if ui=='en' else '')/'durga-saptashloki'/'index.html';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(shell(r['heading_en'] if ui=='en' else r['heading'],'Durga Saptashloki — official Sringeri recording with synchronized reading.',body,prefix,ui,ui))
from kamalamma import render as render_ajji, render_texts as render_ajji_texts
for ui in ['kn','en']:
 prefix='../../' if ui=='en' else '../'
 title,body=render_ajji(ui,prefix)
 p=ROOT/('en' if ui=='en' else '')/'kamalamma-ajji'/'index.html';p.parent.mkdir(parents=True,exist_ok=True)
 p.write_text(shell(title,'Kamalamma Ajji — original family recordings and bhajan readings.',body,prefix,ui,ui))
render_ajji_texts(shell,render_chapter)
home('kn');home('en')
for collection in FILTERS:
 home('kn',collection);home('en',collection)
for s in songs:
 assert s['slug'] and all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-' for c in s['slug'])
 if 'versions_file' in s:render_multiscript(s)
 else:render_legacy(s)
print(f'Built {2*(1+len(FILTERS))} landing/category/tag pages, {len(songs)} entries and {sum(3 if "versions_file" in s else 1 for s in songs)} reading pages.')

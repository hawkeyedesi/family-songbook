"""Publish Sringeri's displayed readings as primary, keeping every previous edition.
Explicit family decision (2026-10-19): keep family scans, prefer Sringeri.
Source website renders its IAST field through its language engine; use that actual
reading rather than contradictory hidden Sanskrit fields. Never use ASR for text.
"""
from pathlib import Path
import json,hashlib,re
from importlib.metadata import version
assert version('indic-transliteration')=='2.3.82','Use requirements-import.txt pinned environment'
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate as tr
ROOT=Path(__file__).resolve().parents[1]
MAPPING={'durga-saptashloki':('devistotrani','durgasaptashloki'),'soundarya-lahari':('devistotrani','saundaryalahari'),'lakshmi-ashtottara-shatanamavali':('devistotrani','shrilakshmi-ashtottarashatanamavalih'),'guru-bhakti-gurvashtakam':('gurustotrani','gurvashtakam'),'sharada-bhujanga-ashtakam':('sharadastotrani','sharada-bhujanga-prayatashtakam'),'kalabhairava-ashtakam':('bhairavastotrani','kalabhairavashtakam'),'krishna-ashtakam':('vishnustotrani','krishnashtakam'),'lakshmi-nrisimha-karavalamba':('narasimha-stotrani','lakshminrisimha-karunarasa-stotram')}
def digest(cs):return hashlib.sha256('\n\n'.join('\n\n'.join(c['paragraphs']) for c in cs).encode()).hexdigest()
def clean(t):
 if re.search('[\u0904-\u0939]',t):t=tr(t,sanscript.DEVANAGARI,sanscript.IAST)
 return re.sub(r'\.\s*(\d+)\s*\.',r'॥ \1 ॥',t.replace(';','।').replace('’',"'")).strip()
songs=json.loads((ROOT/'data/songs.json').read_text());by={s['slug']:s for s in songs}
for slug,(deity,st) in MAPPING.items():
 p=ROOT/'data/texts'/f'{slug}.json';old=json.loads(p.read_text());archive=ROOT/'data/sringeri'/f'before-{slug}.json'
 if not archive.exists():archive.write_text(json.dumps(old,ensure_ascii=False,indent=2)+'\n')
 d=json.loads((ROOT/'data/sringeri/sources'/f'{st}.json').read_text());items=[];colophons=[];intro=[]
 for x in sorted(d['shlokas'],key=lambda x:x.get('orderId',0)):
  text=next((v['value'] for v in x['title'] if v['lang']=='en'),'')
  if not text:continue
  if x.get('orderId',0)==0:intro.append(clean(text));continue
  if 'sampūrṇ' in text or 'samāpt' in text:colophons.append(clean(text));continue
  items.append(clean(text))
 chapters=[]
 if slug=='lakshmi-ashtottara-shatanamavali':chapters=[dict(id='names',title='108 names',layout='names',paragraphs=items[:108]),dict(id='closing',title='Closing invocation',paragraphs=items[108:]+colophons)]
 elif slug=='soundarya-lahari':chapters=[dict(id='ananda',title='Ānanda Lahari · 1–41',paragraphs=items[:41]),dict(id='soundarya',title='Soundarya Lahari · 42–100',paragraphs=items[41:]),dict(id='colophon',title='Conclusion',paragraphs=colophons)]
 elif slug=='kalabhairava-ashtakam':chapters=[dict(id='main',title='Kālabhairavāṣṭakam',paragraphs=items[:8]),dict(id='closing',title='Phalaśruti',paragraphs=items[8:]+colophons)]
 else:chapters=[dict(id='main',title=next(v['value'] for v in d['stotra']['title'] if v['lang']=='en'),paragraphs=items)]
 # The optional sankalpa in Sringeri's page is distinct from the seven verses and
 # from the official standalone clip. Keep it as a separate reading section.
 if intro:chapters.append(dict(id='sankalpa',title='Optional saṅkalpa (not in the seven-verse clip)',paragraphs=intro))
 if colophons and slug not in ['lakshmi-ashtottara-shatanamavali','soundarya-lahari','kalabhairava-ashtakam']:chapters.append(dict(id='colophon',title='Conclusion',paragraphs=colophons))
 # English chapter labels describe the UI; scripture paragraphs alone are transliterated.
 vs=[]
 for previous in old['versions']:
  vid=previous['id'];scheme={'kannada':sanscript.KANNADA,'devanagari':sanscript.DEVANAGARI,'roman':sanscript.IAST}[vid]
  cs=[{**c,'title':{'names':{'kannada':'೧೦೮ ನಾಮಗಳು','devanagari':'अष्टोत्तरशतनामावलिः','roman':'108 names'}}.get(c['id'],{}).get(vid,c['title']),'paragraphs':[tr(t,sanscript.IAST,scheme) if vid!='roman' else t for t in c['paragraphs']]} for c in chapters]
  for c in cs:
   c['title']=({'main':{'kannada':previous['title'],'devanagari':previous['title'],'roman':previous['title']},'closing':{'kannada':'ಸಮಾಪನ','devanagari':'समापनम्','roman':'Closing'},'colophon':{'kannada':'ಸಮಾಪನ','devanagari':'समापनम्','roman':'Conclusion'},'sankalpa':{'kannada':'ಐಚ್ಛಿಕ ಸಂಕಲ್ಪ — ಧ್ವನಿಮುದ್ರಿಕೆಯಲ್ಲಿಲ್ಲ','devanagari':'ऐच्छिकसङ्कल्पः — ध्वनिमुद्रणात् पृथक्','roman':'Optional sankalpa — separate from the recording'},'ananda':{'kannada':'ಆನಂದಲಹರೀ · ೧–೪೧','devanagari':'आनन्दलहरी · १–४१','roman':'Ananda Lahari · 1–41'},'soundarya':{'kannada':'ಸೌಂದರ್ಯಲಹರೀ · ೪೨–೧೦೦','devanagari':'सौन्दर्यलहरी · ४२–१००','roman':'Soundarya Lahari · 42–100'}}.get(c['id'],{}).get(vid,c['title']))
  v={k:previous[k] for k in ['id','lang','label','title']};v.update(chapters=cs,references=[dict(label='Sringeri Sharada Peetham — primary chanting edition',url=d['url'])],source_sha256=digest(cs),family_archive=f'data/sringeri/before-{slug}.json',primary_edition='sringeri',derivation=dict(tool='indic-transliteration',version='2.3.82',from_script='IAST',from_sha256=digest(chapters),note='IAST text actually displayed by Sringeri; no lexical corrections, family variants or ASR inserted.'))
  if slug in ['kalabhairava-ashtakam','sharada-bhujanga-ashtakam']:v['reading_notice']='Primary reading follows Sringeri as requested, including its printed spellings. Apparent source transcription issues and the previous family/published reading are documented under Sources; nothing has been silently corrected.'
  vs.append(v)
 p.write_text(json.dumps(dict(versions=vs),ensure_ascii=False,indent=2)+'\n')
 s=by[slug];s['published_edition']=True;s['note_en']='Primary chanting text follows the reading displayed by Sringeri Sharada Peetham, the family’s chosen authority. Kannada, Devanagari and Roman show the same source edition; the previous reading and family scans are retained below. Source-page inconsistencies are documented in the source check.';s['note']='ಮುಖ್ಯ ಪಾರಾಯಣ ಪಾಠವು ಶೃಂಗೇರಿ ಶಾರದಾಪೀಠದ ಪ್ರಕಟಿತ ಪಾಠವನ್ನು ಅನುಸರಿಸುತ್ತದೆ. ಕುಟುಂಬದ ಹಿಂದಿನ ಪಾಠ ಮತ್ತು ಮೂಲ ಚಿತ್ರಗಳನ್ನು ಪ್ರತ್ಯೇಕವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'
(ROOT/'data/songs.json').write_text(json.dumps(songs,ensure_ascii=False,indent=2)+'\n')
print('Published8Sringerieditions;previous8bundlesandallscansretained')

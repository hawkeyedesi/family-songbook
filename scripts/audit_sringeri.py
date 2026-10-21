"""Compare fetched Sringeri readings, preserving variants instead of claiming blanket verification.
Run with the project transliteration venv: python scripts/audit_sringeri.py.
Fetched public source snapshots are pinned under data/sringeri/sources; no network at build time.
"""
from pathlib import Path
import json,re,unicodedata,hashlib,difflib
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate as tr
ROOT=Path(__file__).resolve().parents[1]
MAPPING={'durga-saptashloki':('devistotrani','durgasaptashloki'),'soundarya-lahari':('devistotrani','saundaryalahari'),'lakshmi-ashtottara-shatanamavali':('devistotrani','shrilakshmi-ashtottarashatanamavalih'),'guru-bhakti-gurvashtakam':('gurustotrani','gurvashtakam'),'sharada-bhujanga-ashtakam':('sharadastotrani','sharada-bhujanga-prayatashtakam'),'kalabhairava-ashtakam':('bhairavastotrani','kalabhairavashtakam'),'krishna-ashtakam':('vishnustotrani','krishnashtakam'),'lakshmi-nrisimha-karavalamba':('narasimha-stotrani','lakshminrisimha-karunarasa-stotram')}
def norm(t):
 t=unicodedata.normalize('NFC',t).replace('’','ऽ').replace("'",'ऽ')
 return ''.join(c for c in t if c.isalpha() or unicodedata.category(c).startswith('M'))
def units(slug,v):
 out=[]
 for c in v['chapters']:
  if c.get('layout')=='names':return c['paragraphs']
  if slug in ['krishna-ashtakam','lakshmi-nrisimha-karavalamba','durga-saptashloki']:out.extend(c['paragraphs']);continue
  pending=[]
  for p in c['paragraphs']:
   if p.startswith(('प्रथम भागः','द्वितीय भागः')):continue
   pending.append(p)
   if re.search(r'[।॥]\s*\d+\s*॥',p):out.append('\n'.join(pending));pending=[]
 if slug=='soundarya-lahari':out[0]=out[0][out[0].index('शिवः शक्त्या'):]
 return out
notes={
'durga-saptashloki':'All seven verses agree with the IAST text actually displayed by Sringeri after removing punctuation, spaces and verse numerals. Hidden Sanskrit field has dāridraya instead of dāridrya in verse 2 and an unsandhied hi āśrayatām in verse 6; the website renders from its IAST field, which agrees with our reading. No guessed Vedic accents added.',
'krishna-ashtakam':'Same composition and all eight stanzas checked. Verse 8 opening corrected from yathā to yadā in all three scripts against both official Sanskrit and IAST. Remaining differences include anusvara vs homorganic nasals and the missing avagraha in hantā’bja. Original family-book transcription retained separately.',
'kalabhairava-ashtakam':'Eight verses and phalashruti compared. Corrected bhavabdhi to bhavābdhi in verse 2 in all three scripts. Other differences are edition readings, including aṣṭaśūla versus astaśūnya in verse 2 and extra words in verses 4–6. Sringeri itself prints bherava (not bhairava) in the phalashruti; the primary edition now retains that source spelling exactly, with this note. Previous edition remains available.',
'lakshmi-ashtottara-shatanamavali':'108-name sequence compared by position; Sringeri also appends śrīmahālakṣmyai namaḥ as item 109 and a colophon. Differences include kṣamā vs kāmākṣī at 28, split/combined names at 29, and buddhi/siddhi case endings. The primary page now uses Sringeri’s first108names and puts its109thinvocation separately under Closing; the earlier108-name reading is archived.',
'guru-bhakti-gurvashtakam':'Eight core stanzas compared. Sringeri puts manaścenna lagnaṃ before guroraṅghripadme; the family sings the reverse order. Family stanza 9 (Anarghyāṇi) and closing verse are outside Sringeri’s eight-stanza edition and are preserved, not claimed Sringeri-verified.',
'sharada-bhujanga-ashtakam':'All eight stanzas compared. Differences in 3, 5 and 7, including lasadgānalolām vs official lasadnānalolām and kare vs dṛgante. Some look like source transcription issues; both readings are documented. Sringeri’s displayed spelling is now primary, as requested; earlier reading is archived.',
'soundarya-lahari':'All 100 core verses compared; readings differ in spelling, sandhi and some words. Existing source also prints alternatives within verses, which the comparison retains. Introductory verse and appendix 101–103 are not in the official 100-verse edition; not certified by that comparison.',
'lakshmi-nrisimha-karavalamba':'Same incipit, but editions differ: current published reading has 25 stanzas, Sringeri has 17 plus a colophon, and original family scan has 17. The first 17 are compared positionally; do not assume equal numbering means identical verse content. Original family transcription remains available.'}
rows=[]
for s in json.loads((ROOT/'data/songs.json').read_text()):
 slug=s['slug'];vs=json.loads((ROOT/'data'/s['versions_file']).read_text())['versions'];v=next(x for x in vs if x['id']=='devanagari')
 row=dict(slug=slug,title=s['title_en'],checked='2026-10-19',script_scope='Sanskrit/Devanagari text compared; Kannada and Roman are script renderings, not separate independent editions.',current_text_hashes={x['id']:x['source_sha256'] for x in vs})
 if slug=='visarjana-mantra':
  row.pop('checked')
  row.update(status='not-checked',added='2026-10-21',note='Added after the 2026-10-19 catalog audit. Family ritual sequence with Rigveda-sourced accents for the two Vedic passages; no Sringeri comparison claimed.',source_url='https://www.sringeri.net/stotras')
  rows.append(row)
  continue
 if slug not in MAPPING:
  row.update(status='not-located',note='No corresponding full text located in Sringeri’s 17-category Stotras catalog in this check. Existing family/published source retained; NOT Sringeri-verified. This is not a claim that no Sringeri publication exists elsewhere.',source_url='https://www.sringeri.net/stotras')
  if s.get('vedic'):row['note']+=' Existing Vedic accent checks remain against the cited marked sources, not against Sringeri.'
 else:
  deity,st=MAPPING[slug];source=ROOT/'data/sringeri/sources'/f'{st}.json';d=json.loads(source.read_text());off=[]
  for x in sorted(d['shlokas'],key=lambda x:x.get('orderId',0)):
   text=next((a['value'] for a in x['title'] if a['lang']=='en'),'')
   if x.get('orderId',0)==0 or 'sampūrṇ' in text or 'samāpt' in text:continue
   off.append(tr(text.replace(';','।').replace('.','॥').replace('’',"'"),sanscript.IAST,sanscript.DEVANAGARI))
  previous=json.loads((ROOT/'data/sringeri'/f'before-{slug}.json').read_text())
  previous_v=next(x for x in previous['versions'] if x['id']=='devanagari')
  ours=units(slug,previous_v)
  if slug=='lakshmi-ashtottara-shatanamavali':ours=[re.sub('^ओं\\s*','',p) for p in ours]
  differences=[];equal=0
  for i,(a,b) in enumerate(zip(ours,off),1):
   if norm(a)==norm(b):equal+=1
   else:differences.append(dict(unit=i,collection=a,sringeri_display=b))
  row.update(status='sringeri-edition',primary_source_faithful=True,previous_comparison_status='match' if slug=='durga-saptashloki' else 'differences',note='Primary text now follows Sringeri in all three scripts. Previous edition comparison: '+notes[slug],source_url=f'https://www.sringeri.net/stotras/{deity}/{st}',source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),source_snapshot=f'data/sringeri/sources/{st}.json',units_compared=min(len(ours),len(off)),units_matching_normalized=equal,collection_units=len(ours),sringeri_units=len(off),differences=differences)
 rows.append(row)
report=dict(checked='2026-10-19',catalog_url='https://www.sringeri.net/api/stotras',catalog_scope='17 deity groups; full catalog enumerated, matching compositions checked by incipit, not title alone.',normalization='NFC; remove spaces, punctuation and decimal numerals; equate ASCII/curly avagraha with Devanagari avagraha. Do NOT erase vowel length, consonants or pitch marks.',summary={k:sum(r['status']==k for r in rows) for k in ['sringeri-edition','not-located']},works=rows)
(ROOT/'data/sringeri-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(report['summary'])

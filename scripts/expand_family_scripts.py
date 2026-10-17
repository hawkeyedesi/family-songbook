"""Render remaining verified family readings into Devanagari/IAST.
Import-only dependency: indic-transliteration==2.3.82. The build/runtime stay stdlib/static.
No external edition is substituted for the family Kannada text.
"""
from pathlib import Path
import hashlib,json,re
from importlib.metadata import version
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
ROOT=Path(__file__).resolve().parents[1]
items=json.loads((ROOT/'data/songs.json').read_text())
config={
'aditya-hridayam':('आदित्यहृदयम्','https://vignanam.org/devanagari/aditya-hrudayam.html'),
'lakshmi-nrisimha-karavalamba':('श्रीलक्ष्मीनृसिंहकरावलम्बस्तोत्रम्','https://vignanam.org/devanagari/lakshmi-nrusimha-karavalamba-stotram.html'),
'durga-suktam':('दुर्गासूक्तम्','https://vignanam.org/devanagari/durga-suktam.html'),
'sri-suktam':('श्रीसूक्तम्','https://vignanam.org/devanagari/sri-suktam.html'),
'krishna-ashtakam':('श्रीकृष्णाष्टकम्','https://stotranidhi.com/hi/krishnashtakam-2-in-sanskrit/'),
'surya-kavacham':('सूर्यकवचस्तोत्रम्','https://stotranidhi.com/hi/sri-surya-kavacham-in-sanskrit/'),
'daily-puja-mantras':('नित्यपूजामन्त्राः','https://vignanam.org/devanagari/mantra-pushpam.html')}
labels=['ಕನ್ನಡ','संस्कृतम्','English (Roman)'];vids=['kannada','devanagari','roman'];langs=['kn','sa','en']
schemes=[None,sanscript.DEVANAGARI,sanscript.IAST]
normalize=lambda t:re.sub(r'\s+',' ',t.replace('|','।')).strip()
assert version('indic-transliteration')=='2.3.82'
for s in items:
 slug=s['slug']
 if slug not in config or s.get('published_edition'):continue
 title_sa,url=config[slug];original=['\n'.join(lines) for lines in s['verses']]
 # Kannada regional lateral spellings correspond to classical Sanskrit la here.
 # Verified in the Devanagari comparison edition for Aditya and Karavalamba.
 canonical=[p.replace('ಳ','ಲ') for p in original]
 vs=[]
 for i,scheme in enumerate(schemes):
  ps=original if scheme is None else [transliterate(p,sanscript.KANNADA,scheme) for p in canonical]
  if scheme is not None:
   for before,after in zip(canonical,ps):
    assert normalize(transliterate(after,scheme,sanscript.KANNADA))==normalize(before),(slug,i,before)
  if slug=='daily-puja-mantras':
   names=['ಯೋ ವೇದಾದೌ','ಗೌರೀರ್ಮಿಮಾಯ','ಗಣಾನಾಂ ತ್ವಾ','ತದ್ವಿಷ್ಣೋಃ','ಆ ಕೃಷ್ಣೇನ','ರಾಜಾಧಿರಾಜಾಯ','ಪರ್ಯಾಪ್ತ್ಯಾ']
   chapters=[dict(id=f'mantra-{j}',title=names[j-1] if scheme is None else transliterate(names[j-1],sanscript.KANNADA,scheme),paragraphs=[p],layout='verses',number_start=j) for j,p in enumerate(ps,1)]
  else:chapters=[dict(id='main',title=['ಕುಟುಂಬದ ಪಾಠ','पारिवारिकपाठः','Family reading'][i],paragraphs=ps,layout='verses')]
  text='\n\n'.join(ps)
  v=dict(id=vids[i],label=labels[i],lang=langs[i],title=[s['title'],title_sa,s['title_en']][i],chapters=chapters,references=s.get('references',[])+[dict(label='Published Sanskrit comparison text',url=url)],source_sha256=hashlib.sha256(text.encode()).hexdigest())
  if scheme is not None:v['derivation']=dict(from_script='kannada',from_sha256=hashlib.sha256('\n\n'.join(original).encode()).hexdigest(),tool='indic-transliteration',version='2.3.82',roundtrip_verified=True,normalization='Kannada regional ಳ -> classical Sanskrit ल/l where present; original Kannada unchanged')
  vs.append(v)
 (ROOT/'data/texts'/f'{slug}.json').write_text(json.dumps(dict(versions=vs),ensure_ascii=False,indent=2)+'\n')
 s.update(versions_file=f'texts/{slug}.json',language='ಕನ್ನಡ · संस्कृतम् · Roman',language_en='Kannada · Sanskrit · Roman')
 s.setdefault('family_note_original',s['note']);s.setdefault('family_note_original_en',s.get('note_en',''))
 s['note']=s['family_note_original']+' ಕನ್ನಡದ ಕುಟುಂಬದ ಪಾಠವನ್ನು ಬದಲಿಸಿಲ್ಲ. ಅದೇ ಪಾಠವನ್ನು ದೇವನಾಗರಿ ಮತ್ತು ರೋಮನ್ ಲಿಪಿಗಳಲ್ಲೂ ನೀಡಲಾಗಿದೆ; ಇವು ಅರ್ಥಾನುವಾದಗಳಲ್ಲ. ಹೊಸ ಲಿಪಿಗಳಲ್ಲಿ ಶಾಸ್ತ್ರೀಯ ಸಂಸ್ಕೃತ ವರ್ಣರೂಪಗಳನ್ನು ಬಳಸಲಾಗಿದೆ.'
 s['note_en']='The family Kannada reading is preserved exactly. Devanagari and Roman are script renderings of that same reading, not translations or substituted editions. Standard Sanskrit letter forms are used where regional Kannada spelling differs. Original scans and comparison sources remain below.'
 if slug=='daily-puja-mantras':s['note_en']+=' These are the same seven selected mantra passages from the family page, not an expanded daily-puja manual. Vedic accent marks remain in the scan rather than being reconstructed.'
 print('Upgraded',slug,len(ps),'units; source and transliteration round trips verified')
(ROOT/'data/songs.json').write_text(json.dumps(items,ensure_ascii=False,indent=2)+'\n')

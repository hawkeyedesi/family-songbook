"""Import the next four reviewed, complete source extracts. Stdlib only."""
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1];src=Path(sys.argv[1]);songs=json.loads((ROOT/'data/songs.json').read_text())
scripts=[('kannada','kn','ಕನ್ನಡ'),('devanagari','sa','संस्कृतम्'),('roman','en','English (Roman)')]
configs=[
('lakshmi-ashtottara-shatanamavali',None,'ಶ್ರೀ ಲಕ್ಷ್ಮೀ ಅಷ್ಟೋತ್ತರ ಶತನಾಮಾವಳಿ','श्रीलक्ष्म्यष्टोत्तरशतनामावलिः','Lakshmi Ashtottara Shatanamavali','ಶ್ರೀ ಲಕ್ಷ್ಮೀದೇವಿಯ ನೂರ ಎಂಟು ಹೆಸರುಗಳು — ಮೂರು ಲಿಪಿಗಳಲ್ಲಿ.','The 108 names of Lakshmi, in three scripts.'),
('kalabhairava-ashtakam','kalabhairava-ashtakam','ಕಾಲಭೈರವ ಅಷ್ಟಕಮ್','कालभैरवाष्टकम्','Kalabhairava Ashtakam','ಕಾಲಭೈರವನ ಎಂಟು ಶ್ಲೋಕಗಳು ಮತ್ತು ಫಲಶ್ರುತಿ.','The eight verses to Kalabhairava, with phalashruti.'),
('hanuman-chalisa','hanuman-chalisa','ಹನುಮಾನ್ ಚಾಲೀಸಾ','हनुमान चालीसा','Hanuman Chalisa','ತುಲಸೀದಾಸರ ಚಾಲೀಸಾ — ನಲವತ್ತು ಚೌಪಾಯಿಗಳು, ಆರಂಭ ಮತ್ತು ಸಮಾಪನ ದೋಹಾಗಳೊಂದಿಗೆ.','Tulsidas’s forty chaupais, with opening and closing dohas.'),
('mahalakshmi-ashtakam','maha-lakshmi-ashtakam','ಮಹಾಲಕ್ಷ್ಮಿ ಅಷ್ಟಕಮ್ — ನಮಸ್ತೇಽಸ್ತು ಮಹಾಮಾಯೇ','महालक्ष्म्यष्टकम्','Mahalakshmi Ashtakam — Namaste Astu Mahamaye','“ನಮಸ್ತೇಽಸ್ತು ಮಹಾಮಾಯೇ” ಎಂದು ಆರಂಭವಾಗುವ ಎಂಟು ಶ್ಲೋಕಗಳು ಮತ್ತು ಫಲಶ್ರುತಿ.','The hymn beginning “Namaste Astu Mahamaye”, with eight verses and phalashruti.')]
num=lambda t:[int(x) for x in re.findall(r'[।॥]\s*(\d+)\s*॥',t)]
norm=lambda t:re.sub(r'\s+',' ',t).strip()
def ch(cid,titles,i,t):return dict(id=cid,title=titles[i],paragraphs=t.strip().split('\n\n'))
def after_eight(t):
 m=next(m for m in re.finditer(r'[।॥]\s*(\d+)\s*॥',t) if int(m[1])==8);end=t.find('\n\n',m.end());assert end>0
 return t[:end].strip(),t[end:].strip()
for slug,source,kn,sa,en,desc,desc_en in configs:
 versions=[];sequences=[]
 for i,(vid,lang,label) in enumerate(scripts):
  script='english' if vid=='roman' else vid
  if source:
   t=(src/f'{slug}-{script}.txt').read_text().strip();url=f'https://vignanam.org/{script}/{source}.html'
   assert '<<<' not in t and '[Showing truncated' not in t
   if slug=='hanuman-chalisa':
    dh=['ಧ್ಯಾನಂ','ध्यानम्','dhyānam'][i];cp=['ಚೌಪಾಈ','चौपाई','chaupāī'][i];doha=['ದೋಹಾ','दोहा','dōhā'][i]
    a=t.index(dh);b=t.index(cp);c=t.rfind(doha)
    chapters=[ch('opening',['ಆರಂಭದ ದೋಹಾಗಳು','प्रारम्भिक दोहे','Opening dohas'],i,t[:a]),ch('dhyana',['ಪ್ರಕಟಿತ ಮೂಲದ ಧ್ಯಾನ ಶ್ಲೋಕಗಳು','स्रोतमें दिये गये ध्यानश्लोक','Additional dhyana prayers'],i,t[a:b]),ch('chalisa',['ಚಾಲೀಸಾ — ೪೦ ಚೌಪಾಯಿಗಳು','चालीसा — ४० चौपाइयाँ','Chalisa — 40 chaupais'],i,t[b:c]),ch('closing',['ಸಮಾಪನ ದೋಹಾ','समापन दोहा','Closing doha'],i,t[c:])]
    assert num(t)==list(range(1,41));lang='awa' if vid=='devanagari' else lang
   else:
    main,closing=after_eight(t);chapters=[ch('main',['ಅಷ್ಟಕ — ಎಂಟು ಶ್ಲೋಕಗಳು','अष्टकम् — अष्टश्लोकाः','Ashtakam — eight verses'],i,main),ch('closing',['ಫಲಶ್ರುತಿ ಮತ್ತು ಸಮಾಪ್ತಿ','फलश्रुतिः समाप्तिश्च','Phalashruti & closing'],i,closing)]
    assert num(main)==list(range(1,9)) and closing
   assert norm('\n\n'.join('\n\n'.join(c['paragraphs']) for c in chapters))==norm(t)
   seq=num(t)
  else:
   whole=(src/f'lakshmi-check-{script}.txt').read_text();start={'kannada':'ಓಂ ಪ್ರಕೃತ್ಯೈ','devanagari':'ओं प्रकृत्यै','english':'ōṁ prakr̥tyai'}[script]
   t=whole[whole.index(start):];prefix={'kannada':'ಓಂ ','devanagari':'ओं ','english':'ōṁ '}[script]
   ps=[p for p in t.split('\n\n') if p.startswith(prefix)][:108];assert len(ps)==108
   assert all({'kannada':'ನಮಃ','devanagari':'नमः','english':'namaḥ'}[script] in p for p in ps)
   t='\n\n'.join(ps);chapters=[dict(id='names',title=['ನೂರ ಎಂಟು ಹೆಸರುಗಳು','अष्टोत्तरशतनामावलिः','The 108 names'][i],paragraphs=ps,layout='names')];seq=list(range(1,109))
   url=['https://stotranidhi.com/kn/sri-lakshmi-ashtottara-shatanamavali-in-kannada/','https://stotranidhi.com/hi/sri-lakshmi-ashtottara-shatanamavali-in-sanskrit/','https://stotranidhi.com/en/sri-lakshmi-ashtottara-shatanamavali-in-english/'][i]
  versions.append(dict(id=vid,lang=lang,label='देवनागरी' if slug=='hanuman-chalisa' and vid=='devanagari' else label,title=[kn,sa,en][i],chapters=chapters,references=[dict(label=('Vaidika Vignanam' if source else 'Stotra Nidhi')+' — '+label,url=url)],source_sha256=hashlib.sha256(t.encode()).hexdigest()))
  sequences.append(seq)
 assert sequences[0]==sequences[1]==sequences[2]
 (ROOT/'data/texts'/f'{slug}.json').write_text(json.dumps(dict(versions=versions),ensure_ascii=False,indent=2)+'\n')
 old=next((s for s in songs if s['slug']==slug),None)
 s=old if old else dict(slug=slug)
 s.update(title=kn,title_en=en,category='ನಾಮಾವಳಿ' if not source else 'ಸ್ತೋತ್ರ',category_en='Namavali' if not source else 'Stotra',language='ಕನ್ನಡ · देवनागरी · Roman' if slug=='hanuman-chalisa' else 'ಕನ್ನಡ · संस्कृतम् · Roman',language_en='Kannada · Devanagari · Roman' if slug=='hanuman-chalisa' else 'Kannada · Sanskrit · Roman',script='kannada',description=desc,description_en=desc_en,versions_file=f'texts/{slug}.json')
 if old:
  s['note']='ಮೂರು ಲಿಪಿಗಳಲ್ಲಿ ಒಂದೇ ಪ್ರಕಟಿತ ೧೦೮ ನಾಮಗಳ ಪಾಠವನ್ನು ನೀಡಲಾಗಿದೆ. ಪುಸ್ತಕದ ಕೆಲವು ಹೆಸರುಗಳಿಗೆ ಪಾಠಭೇದಗಳಿವೆ. ಕುಟುಂಬದ ಮೂಲ ಕನ್ನಡ ಪಾಠ ಮತ್ತು ಎರಡೂ ಚಿತ್ರಗಳನ್ನು ಕೆಳಗೆ ಉಳಿಸಲಾಗಿದೆ.'
  s['note_en']='The three scripts use one matched published 108-name edition. A few names differ from the family book. Its original Kannada transcription and both scans are preserved below.'
  s['preserve_original_transcription']=True
 else:
  s['note']='ಒಂದೇ ಮೂಲದ ಪಠ್ಯವನ್ನು ಮೂರು ಲಿಪಿಗಳಲ್ಲಿ ನೀಡಲಾಗಿದೆ. ರೋಮನ್ ಲಿಪಿಯು ಪಠಣಕ್ಕಾಗಿ; ಅರ್ಥಾನುವಾದವಲ್ಲ. ಮೂಲದ ಪಾಠಭೇದಗಳನ್ನು ಉಳಿಸಲಾಗಿದೆ.'
  s['note_en']='The same published text in three scripts. Roman text is pronunciation transliteration, not translated meaning. Source variants are retained.'
  s['references']=[dict(label='Stotra Nidhi — comparison edition (Kannada)',url='https://stotranidhi.com/kn/'+{'kalabhairava-ashtakam':'kalabhairava-ashtakam','hanuman-chalisa':'hanuman-chalisa','mahalakshmi-ashtakam':'mahalakshmi-ashtakam'}[slug]+'-in-kannada/')]
  songs.append(s)
 if slug=='hanuman-chalisa':
  s['note']+=' ಚಾಲೀಸಾದ ಮೂಲಭಾಷೆ ಅವಧಿ; ದೇವನಾಗರಿ ಆಯ್ಕೆಯು ಅದೇ ಮೂಲ ಪದಗಳನ್ನು ತೋರಿಸುತ್ತದೆ, ಸಂಸ್ಕೃತ ಅನುವಾದವಲ್ಲ. ಧ್ಯಾನ ಶ್ಲೋಕಗಳನ್ನು ಪ್ರತ್ಯೇಕ ಭಾಗವಾಗಿ ನೀಡಲಾಗಿದೆ.'
  s['note_en']+=' The Chalisa is originally Awadhi: the Devanagari option preserves its words, not a Sanskrit translation. The source’s additional dhyana prayers are a separate section.'
 print(slug,len(sequences[0]),'matched units per script')
assert len(songs)==17
(ROOT/'data/songs.json').write_text(json.dumps(songs,ensure_ascii=False,indent=2)+'\n')

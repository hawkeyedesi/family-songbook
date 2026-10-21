from pathlib import Path
import json,re,hashlib
from indic_transliteration import sanscript as S
R=Path(__file__).resolve().parents[1]
texts=[]
def write(p,d):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def src(n):
 d=json.loads((R/f'data/kamalamma-sources/{n}.json').read_text());return d,d['text'].split('---\n',1)[1].split('<<<END')[0].strip()
def add(id,title,en,pars,source,refs,note,layout='verses'):
 versions=[]
 for vid,scheme,lang,label in [('kannada',S.KANNADA,'kn','ಕನ್ನಡ'),('devanagari',S.DEVANAGARI,'sa' if source!=S.KANNADA else 'kn-Deva','देवनागरी'),('roman',S.IAST,'sa-Latn' if source!=S.KANNADA else 'kn-Latn','English (Roman)')]:
  pp=[S.transliterate(p,source,scheme) for p in pars]
  versions.append(dict(id=vid,title=title if vid=='kannada' else en,label=label,lang=lang,chapters=[dict(id='reading',title=title if vid=='kannada' else en,layout=layout,paragraphs=pp)],references=refs,source_sha256=hashlib.sha256('\n'.join(pp).encode()).hexdigest()))
 path=f'kamalamma-texts/{id}.json';write(R/'data'/path,dict(versions=versions))
 texts.append(dict(id=id,title=title,title_en=en,path=f'kamalamma-ajji/texts/{id}/',versions_file=path,note_en=note))
def ref(d,label):return [dict(url=d['url'],label=label)]
d,t=src('lingashtakam');t=t.split('लिङ्गाष्टकमिदं')[0];t=t.replace(' [विनाशन]','').replace(' (परमपदं)','')
pars=re.split(r'॥\s*\d+\s*॥',t);pars=['\n'.join(p.strip().split('\n\n')) for p in pars if p.strip()];assert len(pars)==8
add('lingashtakam','ಲಿಂಗಾಷ್ಟಕಮ್','Lingashtakam',pars,S.DEVANAGARI,ref(d,'Vaidika Vignanam — eight-verse text'),'Eight verses, as in the recording; the printed phalashruti is not sung here. Published wording is a reading reference, not a claim that every sung syllable is identical.')
d,t=src('shani-names');pars=re.findall(r'^ओं[^\n]*नमः[^\n]*',t,re.M);assert len(pars)==108,len(pars)
add('shani-ashtottara','ಶನಿ ಅಷ್ಟೋತ್ತರ ಶತನಾಮಾವಳಿ','Shani Ashtottara Shatanamavali',pars,S.DEVANAGARI,ref(d,'Stotra Nidhi — 108 names'),'Published 108-name version matching the opening and sequence. Section-level timing only; individual names have not been assigned timestamps.','names')
d,t=src('eesha');t=t[t.index('ಈಶ ನಿನ್ನ'):].split('............')[0];lines=[x.strip() for x in t.splitlines() if x.strip()];pars=[];pending=[]
for line in lines:
 pending.append(line)
 if line.endswith('|') or line.endswith('ಈಶ ನಿನ್ನ||'):
  pars.append('\n'.join(pending));pending=[]
assert not pending and len(pars)==26,(pending,len(pars))
add('eesha-ninna','ಈಶ ನಿನ್ನ ಚರಣ ಭಜನೆ','Eesha Ninna Charana Bhajane',pars,S.KANNADA,ref(d,'Kannada Savigana — Kannada text'),'Kannada composition shown in three scripts, not translated into Sanskrit. Published version; Ajji’s repetitions and small oral variants follow her recording.')
d,t=src('narasimha');t=t[t.index('ನಾರಸಿಂಹನೆಂಬೊ'):].split('So, attached')[0];blocks=re.split(r'।\s*PA\s*।|।।\s*\d+\s*।।?',t);pars=['\n'.join(p.strip().split('\n\n')) for p in blocks if p.strip()];assert len(pars)==15,len(pars)
add('narasimhanembo','ನಾರಸಿಂಹನೆಂಬೊ ದೇವನು','Narasimhanembo Devanu',pars,S.KANNADA,ref(d,'Kalpavriksha Kamadhenu — full Kannada text'),'Published full version (pallavi and 14 verses). Ajji sings a shorter selection beginning with verse 7, followed by verses 9–13; local oral wording differs. This is a comparison reading, not a verbatim transcription.')
d,t=src('nama-ramayanam');pars=[x.strip() for x in t.split('\n\n') if x.strip()]
add('nama-ramayanam','ನಾಮ ರಾಮಾಯಣಮ್','Nama Ramayanam',pars,S.DEVANAGARI,ref(d,'Vaidika Vignanam — complete Nama Ramayanam'),'Full published text for reference. Recording 4 opens at “Sheshatalpa Sukhanidrita Rama” (name 3) and reaches the end of Yuddha Kanda; Uttara Kanda is not sung in this recording. Some sung forms vary from this edition.')
d=json.loads((R/'data/kamalamma-sources/ganesha-pancharatnam.json').read_text());pars=[next(t['value'] for t in x['title'] if t['lang']=='en') for x in sorted(d['shlokas'],key=lambda x:x['orderId'])];assert len(pars)==6
add('ganesha-pancharatnam','ಗಣೇಶ ಪಂಚರತ್ನಮ್','Ganesha Pancharatnam',pars,S.IAST,ref(d,'Sringeri Sharada Peetham — official text'),'Official Sringeri text, including the concluding sixth verse. Reading follows Ajji’s bhajan; minor sung diction is not silently rewritten into the recording.')
# Preserve Sringeri's own script-specific witnesses rather than re-transliterating them.
ganeshabundle=R/'data/kamalamma-texts/ganesha-pancharatnam.json'
g=json.loads(ganeshabundle.read_text())
for v in g['versions']:
 lang={'kannada':'kn','devanagari':'sa','roman':'en'}[v['id']]
 pp=[next(t['value'] for t in x['title'] if t['lang']==lang) for x in sorted(d['shlokas'],key=lambda x:x['orderId'])]
 v['chapters'][0]['paragraphs']=pp
 v['source_sha256']=hashlib.sha256('\n'.join(pp).encode()).hexdigest()
write(ganeshabundle,g)
# Short invocations have been checked against the audible recording. These are
# explicit family transcriptions, not falsely labelled Sringeri-verified editions.
family=[dict(url='../../../assets/audio/kamalamma-ajji/amma-01.mp3',label='Kamalamma Ajji — original recording 1')]
# Use root-independent public recording URL for source citations on deep routes.
family=[dict(url='https://hawkeyedesi.github.io/family-songbook/assets/audio/kamalamma-ajji/amma-01.mp3',label='Kamalamma Ajji — original recording 1')]
add('opening-prayers','ಆರಂಭದ ಪ್ರಾರ್ಥನೆಗಳು','Opening prayers',[
'शुक्लाम्बरधरं विष्णुं शशिवर्णं चतुर्भुजम् ।\nप्रसन्नवदनं ध्यायेत् सर्वविघ्नोपशान्तये ॥',
'गुरुर्ब्रह्मा गुरुर्विष्णुर्गुरुर्देवो महेश्वरः ।\nगुरुः साक्षात् परं ब्रह्म तस्मै श्रीगुरवे नमः ॥',
'या कुन्देन्दुतुषारहारधवला या शुभ्रवस्त्रावृता\nया वीणावरदण्डमण्डितकरा या श्वेतपद्मासना ।\nया ब्रह्माच्युतशङ्करप्रभृतिभिर्देवैः सदा पूजिता\nसा मां पातु सरस्वती भगवती निःशेषजाड्यापहा ॥',
'मृत्युञ्जयाय रुद्राय नीलकण्ठाय शम्भवे ।\nअमृतेशाय शर्वाय महादेवाय ते नमः ॥',
'नमः सूर्याय चन्द्राय मङ्गलाय बुधाय च ।\nगुरुशुक्रशनिभ्यश्च राहवे केतवे नमः ॥'],S.DEVANAGARI,family,'Family reading of the five opening invocations, checked against recording 1. Not certified against a Sringeri edition. Sanskrit in Kannada, Devanagari and Roman scripts; these are not Vedic accented passages.')
add('rama-invocations','ರಾಮ ಭಜನೆಗಳು ಮತ್ತು ಮಂತ್ರ','Rama bhajans and mantra',[
'रघुपति राघव राजा राम ।\nपतित पावन सीता राम ॥\nईश्वर अल्लाह तेरे नाम ।\nसबको सन्मति दे भगवान् ॥',
'हरे राम हरे राम राम राम हरे हरे ।\nहरे कृष्ण हरे कृष्ण कृष्ण कृष्ण हरे हरे ॥',
'रामाय रामभद्राय रामचन्द्राय वेधसे ।\nरघुनाथाय नाथाय सीतायाः पतये नमः ॥\nश्री राम जय राम जय जय राम ॥'],S.DEVANAGARI,family,'Short bhajans in Ajji’s opening sequence. Family reading checked against the recording; not a Sringeri-verified edition. Repetitions follow the audio.')
add('pujyaya-raghavendraya','ಪೂಜ್ಯಾಯ ರಾಘವೇಂದ್ರಾಯ','Pujyaya Raghavendraya',['पूज्याय राघवेन्द्राय सत्यधर्मरताय च ।\nभजतां कल्पवृक्षाय नमतां कामधेनवे ॥'],S.DEVANAGARI,family,'Family reading of the short Raghavendra invocation in recording 1, not a Sringeri-verified edition.')
# User-approved provisional reading: gaps and tentative words stay visible.
shiva=json.loads((R/'data/kamalamma-sources/shiva-family-transcription.json').read_text())
add('shiva-aksharamala-family','ಶಿವ ಅಕ್ಷರಮಾಲೆ — ಅಜ್ಜಿಯ ಪಾಠ','Shiva Aksharamala — Ajji’s version',
 [line['reading'] for line in shiva['lines']],S.DEVANAGARI,family,
 'PROVISIONAL FAMILY TRANSCRIPTION — working title, not an identified canonical edition or Sringeri-verified text. [?] marks tentative words; [… ?] marks unrecovered syllables. Unmarked lines are still provisional, not independently certified. Based on the family-supplied phonetic transcript and recording 1 (01:14–03:04). No invented words fill the gaps. Section-level following, not word-by-word alignment.')
texts[-1]['note']='ತಾತ್ಕಾಲಿಕ ಕುಟುಂಬ ಪಾಠ — ಇದು ಖಚಿತ ಶೀರ್ಷಿಕೆ ಅಥವಾ ಶೃಂಗೇರಿ-ಪರಿಶೀಲಿತ ಪಾಠವಲ್ಲ. [?] ಇರುವ ಪದಗಳು ಇನ್ನೂ ಖಚಿತವಾಗಿಲ್ಲ; [… ?] ಇರುವಲ್ಲಿ ಪದಗಳನ್ನು ತುಂಬಿಲ್ಲ. ಗುರುತಿಲ್ಲದ ಸಾಲುಗಳೂ ತಾತ್ಕಾಲಿಕವೇ. ಅಜ್ಜಿಯ ಮೊದಲ ಧ್ವನಿಮುದ್ರಿಕೆ (01:14–03:04) ಮತ್ತು ಕುಟುಂಬ ನೀಡಿದ ಪಾಠ ಆಧಾರ.'
texts[-1]['status']='provisional-family-transcription'
for id,title,en,slug,note in [
('mahalakshmi','ಮಹಾಲಕ್ಷ್ಮೀ ಅಷ್ಟಕಮ್','Mahalakshmi Ashtakam','mahalakshmi-ashtakam','Published reading of the eight verses and phalashruti; small sung diction may differ.'),
('lalitha-ashtottara','ಲಲಿತಾ ಅಷ್ಟೋತ್ತರ ಶತನಾಮಾವಳಿ','Lalitha Ashtottara — Rajatachala','lalitha-ashtottara-shatanamavali','Rajatachala family version, spanning recordings 2 and 3. The start of recording 3 continues at name 99; it is not a new hymn.'),
('kalabhairava','ಕಾಲಭೈರವಾಷ್ಟಕಮ್ — ಕುಟುಂಬದ ಪಾಠ','Kalabhairava Ashtakam — family reading','kalabhairava-ashtakam','Family/comparison edition corresponding to Ajji’s sung “akshashula” variant. The main songbook retains Sringeri’s canonical text separately.')]:
 entry=dict(id=id,title=title,title_en=en,path=f'songs/{slug}/',note_en=note)
 if id=='kalabhairava':entry.update(path='kamalamma-ajji/texts/kalabhairava/',versions_file='sringeri/before-kalabhairava-ashtakam.json')
 texts.append(entry)
tracks=json.loads((R/'data/kamalamma-ajji.json').read_text())['recordings']
# Boundaries are section-level estimates derived from listening and timestamped
# transcripts. Never manufacture per-word alignment or timestamps for names.
rows=[
[(0,'opening-prayers',None),(44.1,'rama-invocations',None),(74,'shiva-aksharamala-family',None),(184,'lingashtakam',None),(250,None,'Om Shiva Om Shiva Paratpara Shiva'),(259,None,'Jai Jai Vittala Panduranga'),(269.2,'pujyaya-raghavendraya',None),(276.8,None,'Vande Raghava — verse variant awaiting text'),(291.2,None,'Rama Rama Raghu Rama Paratpara'),(334.4,None,'Dattatreya Stotram — family variant'),(425,'eesha-ninna',None),(561,None,'Kangettu Bandenai Narayana Krishna'),(640,None,'Keshava Madhava — continues in recording 2')],
[(0,None,'Keshava Madhava — continued'),(62,'narasimhanembo',None),(180,'mahalakshmi',None),(255.1,'shani-ashtottara',None),(382,'lalitha-ashtottara',None)],
[(0,'lalitha-ashtottara',None),(32.4,None,'Palisennamma Muddu Sharade — family variant'),(114.8,None,'Mangalam Guru Sri Chandramouleshwarage'),(279.6,None,'Om Mangalam — Namah Shivaya Mangalam'),(344,None,'End of recording / pause')],
[(0,'nama-ramayanam',None),(299,None,'Atri Tanaya Guru Dattatreya'),(425.3,None,'Taraka Brahma Tanmayada Puje — family variant'),(623.5,None,'Kaliyugadali Harinamava — continues in recording 5')],
[(0,None,'Kaliyugadali Harinamava — continued'),(162.7,None,'Badatanada Pujeyanu Bidade Swikarisai'),(382,None,'Jai Guruve Sadguruve'),(463.3,'ganesha-pancharatnam',None),(590.4,'kalabhairava',None)],
[(0,'kalabhairava',None),(78,None,'Hanuman Chalisa — Kannada translation, source awaiting confirmation')]]
for tr,rs in zip(tracks,rows):
 tr.pop('tags',None);tr['cues']=[]
 for i,(start,tid,title) in enumerate(rs):
  c=dict(id=f'{tr["id"]}-{i+1}',start=start,end=rs[i+1][0] if i+1<len(rs) else tr['duration'])
  if tid:c['text']=tid
  else:c.update(title_en=title,title=title)
  if tr['id']=='amma-03' and i==0:c['anchor']='names-name-99'
  if tr['id']=='amma-06' and i==0:c['anchor']='main-verse-5-1'
  if tr['id']=='amma-04' and i==0:c['anchor']='verse-4'
  tr['cues'].append(c)
write(R/'data/kamalamma-ajji.json',dict(title='Kamalamma Ajji',timing_precision='Approximate section starts, not word-level alignment',recordings=tracks,texts=texts))
print(len(texts),'reading sets',sum(len(t['cues']) for t in tracks),'sections')

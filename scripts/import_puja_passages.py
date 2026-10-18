"""Import bounded published ritual excerpts; never transcribe guesses from audio."""
from pathlib import Path
import json,re,hashlib,unicodedata,sys
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
ROOT=Path(__file__).resolve().parents[1];src=Path(sys.argv[1]);slug='navaratri-puja-passages'
marks='\u0951\u0952\u1cda\u030d\u030e\u0320\u0331'
def norm(t):return ''.join(c for c in unicodedata.normalize('NFD',t.lower()) if c.isalpha())
rows=[
 ('opening','purvanga','शुक्लाम्बरधरं','अगजानन','ಆರಂಭದ ಪ್ರಾರ್ಥನೆ','Opening prayer'),
 ('bell','purvanga','आगमार्थं','इति घण्टानादं','ಘಂಟಾನಾದ','Bell prayer'),
 ('bhuta','purvanga','उत्तिष्ठन्तु','प्राणायामम्','ಭೂತೋಚ್ಚಾಟನ','Bhuta-ucchatana'),
 ('waters','purvanga','गङ्गे च यमुने','कावेरी तुङ्गभद्रा','ಕಲಶ — ನದಿ ಪ್ರಾರ್ಥನೆ','Kalasha — river invocation'),
 ('gananam','haridra','ओं गणानां','ओं महागणपतये','ಗಣಾನಾಂ ತ್ವಾ','Gananam tva'),
 ('ganesha-names','haridra','ओं सुमुखाय','ओं महागणपतये','ಗಣಪತಿ ನಾಮಪೂಜೆ','Ganapathy nama puja'),
 ('naivedya','haridra','ओं भूर्भुवस्सुव','ओं महागणपतये','ನೈವೇದ್ಯ ಮಂತ್ರಗಳು','Naivedya mantras'),
 ('ganesha-pradakshina','haridra','यानिकानि','ओं महागणपतये','ಗಣಪತಿ ಪ್ರದಕ್ಷಿಣೆ','Ganapathy pradakshina'),
 ('vakratunda','haridra','ओं वक्रतुण्ड महाकाय','अनया ध्यान','ವಕ್ರತುಂಡ ಮಹಾಕಾಯ','Vakratunda mahakaya'),
 ('abhisheka-milk','abhisheka','आ प्यायस्व','श्री','ಪಂಚಾಮೃತ — ಹಾಲು','Panchamrita — milk'),
 ('abhisheka-curd','abhisheka','दधिक्राव्ण्णो','श्री','ಪಂಚಾಮೃತ — ಮೊಸರು','Panchamrita — curd'),
 ('abhisheka-ghee','abhisheka','शुक्रमसि','श्री','ಪಂಚಾಮೃತ — ತುಪ್ಪ','Panchamrita — ghee'),
 ('abhisheka-honey','abhisheka','मधु वाता','श्री','ಪಂಚಾಮೃತ — ಜೇನು','Panchamrita — honey'),
 ('abhisheka-sugar','abhisheka','स्वादुः पवस्व','श्री','ಪಂಚಾಮೃತ — ಸಕ್ಕರೆ','Panchamrita — sugar'),
 ('abhisheka-fruit','abhisheka','याः फलिनी','श्री','ಫಲೋದಕ','Fruit water'),
 ('abhisheka-water','abhisheka','आपो हिष्ठा','श्री','ಶುದ್ಧೋದಕ ಸ್ನಾನ','Pure-water bathing'),
 ('gandha','haridra','गन्धद्वारां','ओं महागणपतये','ಗಂಧದ್ವಾರಾಂ','Gandhadvāram'),
 ('devi-pradakshina','lalitha','यानि कानि','ओं श्री ललिता देव्यै नमः प्रदक्षिण','ದೇವೀ ಪ್ರದಕ್ಷಿಣೆ','Devi pradakshina'),
 ('royal-offerings','lalitha','ओं श्री ललिता देव्यै नमः छत्रं','नमस्कारान्','ರಾಜೋಪಚಾರಗಳು','Royal offerings'),
]
deva_titles=['प्रार्थना','घण्टानादः','भूतोच्चाटनम्','कलशोदकप्रार्थना','गणपतिमन्त्रः','गणपतिनामपूजा','नैवेद्यमन्त्राः','गणपतिप्रदक्षिणम्','वक्रतुण्डप्रार्थना','क्षीराभिषेकः','दध्यभिषेकः','आज्याभिषेकः','मध्वभिषेकः','शर्कराभिषेकः','फलोदकाभिषेकः','शुद्धोदकस्नानम्','गन्धसमर्पणम्','देवीप्रदक्षिणप्रार्थना','राजोपचाराः']
versions=[]
for i,(vid,lang,scheme,sc) in enumerate([('kannada','kn',sanscript.KANNADA,'kn'),('devanagari','sa',sanscript.DEVANAGARI,'hi'),('roman','en',sanscript.IAST,'en')]):
 chapters=[];refs={}
 for cid,book,start,end,kn,en in rows:
  raw=(src/f'{book}-{sc}.txt').read_text();lines=raw.splitlines()
  def marker(t):return norm(transliterate(t,sanscript.DEVANAGARI,scheme) if vid!='devanagari' else t)
  def find(m,after=0):
   for j in range(after,len(lines)):
    if norm(lines[j]).startswith(marker(m)):return j
   raise ValueError((vid,cid,m))
  first=find(start);last=find(end,first+1);ps=['\n'.join(lines[first:last]).strip()]
  assert ps[0] and not any(z in ps[0] for z in ['<<<','http'])
  title=kn if i==0 else (deva_titles[len(chapters)] if i==1 else en)
  chapters.append(dict(id=cid,title=title,paragraphs=ps))
  base={'purvanga':'puja-vidhanam-poorvangam','haridra':'sri-haridra-ganapati-puja','lalitha':'sri-lalitha-shodasopachara-puja-vidhanam','abhisheka':'panchamrutha-abhishekam-mantras'}[book]
  refs[book]=dict(label='Stotra Nidhi — '+book,url=f'https://stotranidhi.com/{sc}/{base}-in-'+['kannada','sanskrit','english'][i]+'/')
 text='\n\n'.join('\n\n'.join(c['paragraphs']) for c in chapters);ms=''.join(c for c in text if c in marks)
 versions.append(dict(id=vid,lang=lang,label=['ಕನ್ನಡ','संस्कृतम्','English (Roman)'][i],title=['ನವರಾತ್ರಿ ಪೂಜೆಯ ಆಯ್ದ ಮಂತ್ರಗಳು','नवरात्रिपूजायाः चयनितमन्त्राः','Navaratri puja — sourced passages'][i],chapters=chapters,references=list(refs.values()),source_sha256=hashlib.sha256(text.encode()).hexdigest(),svara_profile=dict(counts={f'U+{ord(c):04X}':ms.count(c) for c in sorted(set(ms))},sequence_sha256=hashlib.sha256(ms.encode()).hexdigest())))
 print(vid,len(chapters),len(ms))
(ROOT/'data/texts'/f'{slug}.json').write_text(json.dumps(dict(versions=versions),ensure_ascii=False,indent=2)+'\n')
songs=json.loads((ROOT/'data/songs.json').read_text());old=next((s for s in songs if s['slug']==slug),None);s=old or dict(slug=slug,collections=[],tags=['navaratri'])
s.update(title=versions[0]['title'],title_en=versions[2]['title'],category='ಪೂಜಾ ಮಂತ್ರಗಳು',category_en='Puja passages',language='ಕನ್ನಡ · संस्कृतम् · Roman',language_en='Kannada · Sanskrit · Roman',script='kannada',versions_file=f'texts/{slug}.json',vedic=True,svara_status='marked',description='ಧ್ವನಿಮುದ್ರಿಕೆಗಳಲ್ಲಿನ ಆಯ್ದ ಪೂಜಾ ಭಾಗಗಳಿಗೆ ಪ್ರಕಟಿತ ಮೂಲದ ಪಠ್ಯ.',description_en='Published-source excerpts for matched passages in the two family recordings.',note='ಪ್ರಕಟಿತ ಮೂಲದ ಆಯ್ದ ಭಾಗಗಳು ಮಾತ್ರ; ಧ್ವನಿಮುದ್ರಿಕೆಯ ಸಂಪೂರ್ಣ ಪದಶಃ ಲಿಪ್ಯಂತರವಲ್ಲ. ಕುಟುಂಬದ ಪಠಣದಲ್ಲಿ ಪದ ಅಥವಾ ಕ್ರಮಭೇದಗಳಿರಬಹುದು. ಮೂಲದ ಸ್ವರಗುರುತುಗಳನ್ನು ಉಳಿಸಲಾಗಿದೆ; ಗುರುತುಗಳನ್ನು ಊಹಿಸಿ ಸೇರಿಸಿಲ್ಲ.',note_en='Selected published passages, not a complete verbatim transcript of the family ritual. The recording can differ in wording, deity invocations, extra names and order. The 16-name sequence includes the source’s additional Sarvasiddhiprada closing name. Source Vedic marks are retained exactly, not reconstructed. Unmatched ritual passages remain explicitly labelled in the player.')
if not old:songs.append(s)
(ROOT/'data/songs.json').write_text(json.dumps(songs,ensure_ascii=False,indent=2)+'\n')

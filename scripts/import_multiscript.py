"""Import reviewed Vaidika Vignanam text extracts; no runtime dependencies.
Usage: python3 scripts/import_multiscript.py /tmp/bhakti-multiscript
The input directory must contain complete <source-id>-<script>.txt extracts.
"""
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1]
INPUT=Path(sys.argv[1])
SCRIPTS=[('kannada','kannada','kn','ಕನ್ನಡ'),('devanagari','devanagari','sa','संस्कृतम्'),('roman','english','en','English (Roman)')]
CONFIG=[
 ('lalitha-sahasranama','sree-lalitha-sahasra-nama-stotram','ಶ್ರೀ ಲಲಿತಾ ಸಹಸ್ರನಾಮ ಸ್ತೋತ್ರಮ್','श्रीललितासहस्रनामस्तोत्रम्','Lalitha Sahasranama','ನ್ಯಾಸ ಮತ್ತು ಧ್ಯಾನ ಸಹಿತ ಲಲಿತಾದೇವಿಯ ಸಹಸ್ರನಾಮ ಸ್ತೋತ್ರ.','Lalitha’s thousand names, with nyasa and dhyana.'),
 ('vishnu-sahasranama','sree-vishnu-sahasra-nama-stotram','ಶ್ರೀ ವಿಷ್ಣು ಸಹಸ್ರನಾಮ ಸ್ತೋತ್ರಮ್','श्रीविष्णुसहस्रनामस्तोत्रम्','Vishnu Sahasranama','ಪೂರ್ವಪೀಠಿಕಾ, ಸಹಸ್ರನಾಮ ಮತ್ತು ಫಲಶ್ರುತಿ ಸಹಿತ ವಿಷ್ಣು ಸ್ತೋತ್ರ.','Vishnu’s thousand names, with opening prayers and phalashruti.'),
 ('rudra-namakam-chamakam',None,'ಶ್ರೀ ರುದ್ರಮ್ — ನಮಕಮ್ ಮತ್ತು ಚಮಕಮ್','श्रीरुद्रम् — नमकम् च चमकम्','Sri Rudram — Namakam & Chamakam','ನಮಕದ ಹನ್ನೊಂದು ಮತ್ತು ಚಮಕದ ಹನ್ನೊಂದು ಅನುವಾಕಗಳು, ಸಮಾಪನ ಮಂತ್ರಗಳೊಂದಿಗೆ.','All eleven anuvakas of Namakam and eleven of Chamakam, with closing prayers.'),
 ('ganesha-atharvashirsham','ganapati-atharva-sheersham','ಶ್ರೀ ಗಣಪತಿ ಅಥರ್ವಶೀರ್ಷಮ್','श्रीगणपत्यथर्वशीर्षम्','Ganesha Atharvashirsham','ಶಾಂತಿಮಂತ್ರ ಮತ್ತು ಫಲಶ್ರುತಿ ಸಹಿತ ಗಣಪತ್ಯಥರ್ವಶೀರ್ಷ ಉಪನಿಷತ್.','The Ganapati Atharvashirsha Upanishad, with peace prayers and phalashruti.'),
 ('soundarya-lahari','soundarya-lahari','ಸೌಂದರ್ಯ ಲಹರೀ','सौन्दर्यलहरी','Soundarya Lahari','ಆನಂದಲಹರೀ ಮತ್ತು ಸೌಂದರ್ಯಲಹರಿಯ ನೂರು ಮುಖ್ಯ ಶ್ಲೋಕಗಳು; ಅನುಬಂಧ ಪ್ರತ್ಯೇಕವಾಗಿ.','The 100 principal verses, with Ananda Lahari and clearly separated supplementary verses.')]

def read(name,script):
 t=(INPUT/f'{name}-{script}.txt').read_text().strip()
 assert t and '<<<' not in t and '[Showing truncated' not in t,name
 return t

def nums(t):return [int(x) for x in re.findall(r'[।॥]\s*(\d+)\s*॥',t)]
def norm(t):return re.sub(r'\s+',' ',t).strip()
def split_number(t,n):
 matches=list(re.finditer(r'[।॥]\s*(\d+)\s*॥',t))
 m=next(m for m in matches if int(m[1])==n)
 # Keep optional textual variants immediately following a verse with that verse.
 end=t.find('\n\n',m.end())
 if end<0:end=len(t)
 return t[:end].strip(),t[end:].strip()

def chapter(cid,title,text):return {'id':cid,'title':title,'paragraphs':text.split('\n\n')}

def chapters(slug,t,idx):
 if slug=='lalitha-sahasranama':
  marker=['ಶ್ರೀಮಾತಾ,','श्रीमाता,','śrīmātā,'][idx];pos=t.index(marker)
  out=[chapter('opening',['ನ್ಯಾಸ ಮತ್ತು ಧ್ಯಾನ','न्यासः ध्यानं च','Nyasa & Dhyana'][idx],t[:pos].strip()),chapter('main',['ಸಹಸ್ರನಾಮ ಸ್ತೋತ್ರ','सहस्रनामस्तोत्रम्','Sahasranama hymn'][idx],t[pos:].strip())]
 elif slug=='vishnu-sahasranama':
  # This occurrence has the complete first verse, not the earlier karanyasa quotation.
  marker=['ವಿಶ್ವಂ ವಿಷ್ಣುರ್ವಷಟ್ಕಾರೋ','विश्वं विष्णुर्वषट्कारो','viśvaṃ viṣṇurvaṣaṭkārō'][idx]
  pos=t.index(marker)
  tailmarker=['ಉತ್ತರ ಪೀಠಿಕಾ','उत्तर पीठिका','uttara pīṭhikā'][idx]
  end=t.index(tailmarker,pos)
  out=[chapter('opening',['ಪೂರ್ವಪೀಠಿಕಾ ಮತ್ತು ಧ್ಯಾನ','पूर्वपीठिका ध्यानं च','Opening prayers & Dhyana'][idx],t[:pos].strip()),chapter('main',['ಸಹಸ್ರನಾಮ ಸ್ತೋತ್ರ','सहस्रनामस्तोत्रम्','Sahasranama hymn'][idx],t[pos:end].strip()),chapter('closing',['ಉತ್ತರಪೀಠಿಕಾ ಮತ್ತು ಫಲಶ್ರುತಿ','उत्तरपीठिका फलश्रुतिश्च','Uttara Peethika & Phalashruti'][idx],t[end:].strip())]
 elif slug=='soundarya-lahari':
  one,rest=split_number(t,41);two,three=split_number(rest,100)
  out=[chapter('ananda',['ಆನಂದಲಹರೀ — ೧–೪೧','आनन्दलहरी — १–४१','Ananda Lahari — 1–41'][idx],one),chapter('soundarya',['ಸೌಂದರ್ಯಲಹರೀ — ೪೨–೧೦೦','सौन्दर्यलहरी — ४२–१००','Soundarya Lahari — 42–100'][idx],two),chapter('appendix',['ಸಮಾಪ್ತಿ ಮತ್ತು ಅನುಬಂಧ — ೧೦೧–೧೦೩','समाप्तिः परिशिष्टं च — १०१–१०३','Closing & supplementary verses — 101–103'][idx],three)]
 else:out=[chapter('text',['ಪೂರ್ಣ ಪಠ್ಯ','सम्पूर्णपाठः','Complete text'][idx],t)]
 assert norm('\n\n'.join('\n\n'.join(c['paragraphs']) for c in out))==norm(t),'Lost text '+slug
 return out

songs=json.loads((ROOT/'data/songs.json').read_text())
existing_collections={s['slug']:s.get('collection','daily') for s in songs}
songs=[s for s in songs if s['slug'] not in {c[0] for c in CONFIG}]
for slug,source,kn,sa,en,description,description_en in CONFIG:
 versions=[];sequences=[]
 for idx,(vid,script,lang,label) in enumerate(SCRIPTS):
  refs=[]
  if source:
   t=read(slug,script);cs=chapters(slug,t,idx);seq=nums(t)
   refs=[{'label':f'Vaidika Vignanam — {label}','url':f'https://vignanam.org/{script}/{source}.html'}]
  else:
   nt=read('rudram-namakam',script);ct=read('rudram-chamakam',script)
   assert nums(nt)==list(range(1,12)) and nums(ct)==list(range(1,12))
   cs=[chapter('namakam',['ನಮಕಮ್','नमकम्','Namakam'][idx],nt),chapter('chamakam',['ಚಮಕಮ್','चमकम्','Chamakam'][idx],ct)]
   seq=nums(nt)+nums(ct);t=nt+'\n\n'+ct
   refs=[{'label':f'Vaidika Vignanam — {part.title()} ({label})','url':f'https://vignanam.org/{script}/sri-rudram-{part}.html'} for part in ['namakam','chamakam']]
  versions.append(dict(id=vid,label=label,lang=lang,title=[kn,sa,en][idx],chapters=cs,references=refs,source_sha256=hashlib.sha256(t.encode()).hexdigest()))
  sequences.append(seq)
 assert sequences[0]==sequences[1]==sequences[2],slug+' mismatched verse numbers'
 expected={'lalitha-sahasranama':187,'vishnu-sahasranama':171,'rudra-namakam-chamakam':22,'ganesha-atharvashirsham':14,'soundarya-lahari':103}[slug]
 assert len(sequences[0])==expected,(slug,len(sequences[0]))
 (ROOT/'data/texts'/f'{slug}.json').write_text(json.dumps({'versions':versions},ensure_ascii=False,indent=2)+'\n')
 comparison_urls={
 'lalitha-sahasranama':'https://stotranidhi.com/kn/sri-lalitha-sahasranama-stotram-in-kannada/',
 'vishnu-sahasranama':'https://stotranidhi.com/kn/sri-vishnu-sahasranama-stotram-in-kannada/',
 'rudra-namakam-chamakam':'https://stotranidhi.com/kn/sri-rudram-namakam-in-kannada/',
 'ganesha-atharvashirsham':'https://stotranidhi.com/kn/sri-ganapati-atharvashirsha-upanishat-in-kannada/',
 'soundarya-lahari':'https://stotranidhi.com/kn/saundaryalahari-in-kannada/'}
 songs.append(dict(collection=existing_collections.get(slug,'daily'),references=[{'label':'Stotra Nidhi — comparison edition (Kannada)','url':comparison_urls[slug]}],slug=slug,title=kn,title_en=en,category='ಸ್ತೋತ್ರ' if source else 'ವೇದಮಂತ್ರ',category_en='Stotra' if source else 'Vedic hymn',language='ಕನ್ನಡ · संस्कृतम् · Roman',language_en='Kannada · Sanskrit · Roman',script='kannada',description=description,description_en=description_en,versions_file=f'texts/{slug}.json',note='ಒಂದೇ ಸಂಸ್ಕೃತ ಪಠ್ಯದ ಮೂರು ಲಿಪಿಗಳು. ರೋಮನ್ ಪಠ್ಯವು ಉಚ್ಚಾರಣೆಗಾಗಿ; ಇಂಗ್ಲಿಷ್ ಅರ್ಥಾನುವಾದವಲ್ಲ. ಪ್ರಕಟಿತ ಮೂಲದಲ್ಲಿರುವ ಪಾಠಭೇದಗಳು ಮತ್ತು ವೇದಸ್ವರ ಗುರುತುಗಳನ್ನು ಉಳಿಸಲಾಗಿದೆ.',note_en='Three scripts of the same Sanskrit text. Roman text is for pronunciation, not an English translation. Published variants and Vedic accent marks are retained.'))
 print(slug,expected,'numbered passages per script; all 3 matched')
(ROOT/'data/songs.json').write_text(json.dumps(songs,ensure_ascii=False,indent=2)+'\n')

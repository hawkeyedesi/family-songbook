"""Restore published svara-marked readings without guessing accents.
Usage: python3 scripts/import_vedic.py /tmp/bhakti-vedic
Retains exact source codepoints; no Unicode normalization or accent reconstruction.
"""
from pathlib import Path
import json,hashlib,re,sys
ROOT=Path(__file__).resolve().parents[1];src=Path(sys.argv[1])
songs=json.loads((ROOT/'data/songs.json').read_text());by={s['slug']:s for s in songs}
MARKS='\u0951\u0952\u1cda\u030d\u030e\u0320\u0331'
def profile(text):
 marks=''.join(c for c in text if c in MARKS)
 return dict(counts={f'U+{ord(c):04X}':marks.count(c) for c in sorted(set(marks))},sequence_sha256=hashlib.sha256(marks.encode()).hexdigest())
for slug in ['sri-suktam','durga-suktam']:
 s=by[slug];versions=[]
 for i,sc in enumerate(['kannada','devanagari','english']):
  whole=(src/f'nidhi-{slug}-{sc}.txt').read_text().strip()
  marker=({'sri-suktam':['ಹಿರ॑','हिर॑','hira̍'],'durga-suktam':['ಓಂ ಜಾ॒','ओं जा॒','oṃ jā̱']}[slug])[i]
  raw=whole[whole.index(marker):].split(['\n\nಇನ್ನಷ್ಟು','\n\nटिप्पणि:','\n\nNote:'][i])[0].strip()
  assert len([c for c in raw if c in MARKS])>150
  raw=raw.replace('||','॥').replace('|','।') # Equivalent punctuation, not accent normalization.
  ps=raw.split('\n\n')
  def chapter(cid,titles,items,**kw):return dict(id=cid,title=titles[i],paragraphs=items,**kw)
  if slug=='sri-suktam':
   core=ps[:30];closing=ps[-3:]
   assert [int(n) for n in re.findall(r'॥\s*(\d+)\s*॥','\n\n'.join(core))]==list(range(1,16))
   chapters=[chapter('main',['ಶ್ರೀಸೂಕ್ತ — ೧೫ ಋಕ್ಕುಗಳು','श्रीसूक्तम् — पञ्चदशर्चः','Sri Sukta — 15 principal richas'],core),chapter('gayatri',['ಲಕ್ಷ್ಮೀ ಗಾಯತ್ರೀ','लक्ष्मीगायत्री','Lakshmi Gayatri'],closing[:2]),chapter('shanti',['ಶಾಂತಿಮಂತ್ರ','शान्तिमन्त्रः','Peace prayer'],closing[2:])]
   text='\n\n'.join(core+closing);selected_source='\n\n'.join(core+closing)
  else:
   assert len(ps)==16
   verses=['\n'.join(ps[n:n+2]) for n in range(0,14,2)]
   chapters=[chapter('main',['ದುರ್ಗಾಸೂಕ್ತ — ಏಳು ಮಂತ್ರಗಳು','दुर्गासूक्तम् — सप्तमन्त्राः','Durga Sukta — seven mantras'],verses,layout='verses'),chapter('gayatri',['ದುರ್ಗಾ ಗಾಯತ್ರೀ','दुर्गागायत्री','Durga Gayatri'],[ps[14]]),chapter('shanti',['ಶಾಂತಿಮಂತ್ರ','शान्तिमन्त्रः','Peace prayer'],[ps[15]])]
   text='\n\n'.join('\n\n'.join(c['paragraphs']) for c in chapters)
   selected_source=raw
  original_marks=''.join(c for c in selected_source if c in MARKS);assert ''.join(c for c in text if c in MARKS)==original_marks
  vid='roman' if sc=='english' else sc
  v=dict(id=vid,label=['ಕನ್ನಡ','संस्कृतम्','English (Roman)'][i],lang=['kn','sa','en'][i],title=[s['title'],{'sri-suktam':'श्रीसूक्तम्','durga-suktam':'दुर्गासूक्तम्'}[slug],s['title_en']][i],chapters=chapters,references=[dict(label='Stotra Nidhi — accent-marked '+sc,url=f'https://stotranidhi.com/{["kn","hi","en"][i]}/{slug}-in-{["kannada","sanskrit","english"][i]}/')],source_sha256=hashlib.sha256(text.encode()).hexdigest(),svara_profile=profile(text))
  versions.append(v)
 (ROOT/'data/texts'/f'{slug}.json').write_text(json.dumps(dict(versions=versions),ensure_ascii=False,indent=2)+'\n')
 s.update(published_edition='stotra-nidhi-svara',preserve_original_transcription=True,vedic=True,svara_status='marked')
 s['note']='ವೈದಿಕ ಸ್ವರಗುರುತುಗಳಿರುವ ಪ್ರಕಟಿತ ಮೂಲದ ಪಠ್ಯವನ್ನು ಮೂರು ಲಿಪಿಗಳಲ್ಲೂ ಉಳಿಸಲಾಗಿದೆ. ಕುಟುಂಬದ ಮೂಲ ಕನ್ನಡ ಪಾಠ ಮತ್ತು ಚಿತ್ರಗಳನ್ನು ಕೆಳಗೆ ಪ್ರತ್ಯೇಕವಾಗಿ ಉಳಿಸಲಾಗಿದೆ. ಸ್ವರಗುರುತುಗಳನ್ನು ಊಹಿಸಿ ಸೇರಿಸಿಲ್ಲ.'
 s['note_en']='The published svara-marked reading is preserved in all three scripts, including vowel-length, nasal and visarga notation. Dad’s original Kannada book transcription and scans are retained separately below. Accents have not been guessed or reconstructed.'
 if slug=='sri-suktam':
  s['note_en']+=' The 15 principal richas are followed by separately labelled Lakshmi Gayatri and peace prayer. The source’s additional poetic stotras are not mixed into the Vedic reading. Dad’s book-specific closing prayer remains in the original transcription below. Equivalent pipe punctuation is displayed as danda marks.'
  s['description_en']='The 15 principal richas with Vedic accents, followed by Lakshmi Gayatri and a peace prayer.'
for slug in ['ganesha-atharvashirsham','rudra-namakam-chamakam','mantra-pushpam']:
 s=by[slug];p=ROOT/'data'/s['versions_file'];d=json.loads(p.read_text())
 for v in d['versions']:
  t='\n\n'.join('\n\n'.join(c['paragraphs']) for c in v['chapters']);v['svara_profile']=profile(t)
  assert sum(v['svara_profile']['counts'].values())>300
 p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');s.update(vedic=True,svara_status='marked')
# A marked scan is authoritative here; plain digital text must not masquerade as a svara edition.
s=by['daily-puja-mantras'];s.update(vedic=True,svara_status='scan-only')
s['note_en']='The seven selected passages are preserved from Dad’s book. The original photographed page contains Vedic accents, but this digital transcription has not yet been verified with all those marks. Use the original accent-marked page linked above for svara chanting; the plain digital text is a reading reference, not an accent-verified chant edition.'
s['note']='ಕುಟುಂಬದ ಪುಸ್ತಕದ ಏಳು ಆಯ್ದ ಮಂತ್ರಗಳನ್ನು ಉಳಿಸಲಾಗಿದೆ. ಮೂಲ ಚಿತ್ರದಲ್ಲಿ ವೈದಿಕ ಸ್ವರಗುರುತುಗಳಿವೆ; ಡಿಜಿಟಲ್ ಪಾಠದಲ್ಲಿ ಅವೆಲ್ಲವೂ ಇನ್ನೂ ಪರಿಶೀಲಿತವಾಗಿಲ್ಲ. ಸ್ವರಪಠಣಕ್ಕೆ ಮೇಲೆ ನೀಡಿರುವ ಮೂಲ ಚಿತ್ರವನ್ನು ಬಳಸಿ; ಈ ಸರಳ ಡಿಜಿಟಲ್ ಪಾಠವು ಸ್ವರಪರಿಶೀಲಿತ ಪಾಠವಲ್ಲ.'
(ROOT/'data/songs.json').write_text(json.dumps(songs,ensure_ascii=False,indent=2)+'\n')
print('Published svara source marks preserved; five marked works audited; daily-mantra scan explicitly distinguished.')

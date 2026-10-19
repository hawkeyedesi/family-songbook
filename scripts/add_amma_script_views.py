"""Family Kannada bhajan in three scripts. Roman original is preserved verbatim."""
from pathlib import Path
import json,hashlib,unicodedata
from importlib.metadata import version
assert version('indic-transliteration')=='2.3.82'
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate as tr
ROOT=Path(__file__).resolve().parents[1];songs=json.loads((ROOT/'data/songs.json').read_text());s=next(s for s in songs if s['slug']=='amma-baaramma')
chorus='ಅಮ್ಮ ಬಾರಮ್ಮ ನಮ್ಮ ತಾಯಿ ಬಾರಮ್ಮ ।\nತಾಯಿ ಬಾರಮ್ಮ ನಮ್ಮ ದೇವಿಯೇ ಬಾರಮ್ಮ ॥'
ps=[
'ಮೂನು ಲೋಕದೊಡೆಯ ಶಿವನ ರಾಣಿಯೇ ಬಾರಮ್ಮ ।\nನಿನ್ನಯ ಗೆಜ್ಜೆಯ ನಾದ ಗಲುಗಲು ಎನ್ನುತ ತಾಯಿ ಬಾರಮ್ಮ ॥',
'ಗಜಮುಖ ಜನನಿಯೇ ಧೀರ ಗಂಭೀರಳೆ ಗಾಯತ್ರಿ ದೇವಿಯೇ ಬಾರಮ್ಮ ।\nಅಂಬಾ ಭವಾನಿಯೇ ಗಂಗಾ ಭವಾನಿಯೇ ತುಳಸಿಯ ಭವಾನಿಯೇ ಬಾರಮ್ಮ ॥',
'ಶಂಕರ ಸ್ಥಾಪಿತೆ ಶ್ರೀಚಕ್ರ ಪೂಜಿತೆ ಶಾರದಾ ದೇವಿಯೇ ಬಾರಮ್ಮ ।\nಶೃಂಗೇರಿಯಲ್ಲಿ ನಗುನಗುತಿರುವ ಭಾರತಿ ದೇವಿಯೇ ಬಾರಮ್ಮ ॥',
'ಖಡ್ಗಧಾರಿಣಿ ತ್ರಿಶೂಲಪಾಣಿ ಚಾಮುಂಡೇಶ್ವರಿ ಬಾರಮ್ಮ ।\nರಾಜಾಧಿರಾಜರಿಂದ ಪೂಜಿಸಲ್ಪಡುವಂಥ ರಾಜರಾಜೇಶ್ವರಿ ಬಾರಮ್ಮ ॥',
'ಜಪವನ ಅರಿಯೆನು ತಪವನ ಅರಿಯೆನು ಮೂದಲ ಕರುಣಿಸು ಬಾರಮ್ಮ ।\nಮೂಜಗ ವಂದಿತೆ ಮುರಹರನೊಲ್ಲಭೆ ಮೂಕಾಂಬಿಕೆ ಮಾತೆ ಬಾರಮ್ಮ ॥',
'ಕಾಂಚಿ ಕಾಮಾಕ್ಷಿ ಮಧುರೈ ಮೀನಾಕ್ಷಿ ಕಾಶಿ ವಿಶಾಲಾಕ್ಷಿ ಬಾರಮ್ಮ ।\nಕಾಮಿತ ಫಲಗತ ನೀಡುವಂಥ ಕರುಣಾಸಾಗರಿ ಬಾರಮ್ಮ ॥',
'ಶ್ರೀ ಜಯಲಕ್ಷ್ಮಿ ಜಯಜಯ ಲಕ್ಷ್ಮಿ ಪ್ರಸನ್ನ ಲಕ್ಷ್ಮಿಯೇ ಬಾರಮ್ಮ ।\nಶ್ರಾವಣ ಮಾಸದಿ ಪೂಜಿಸಲ್ಪಡುವಂಥ ವರಮಹಾಲಕ್ಷ್ಮಿಯೇ ಬಾರಮ್ಮ ॥',
'ಶ್ರೀ ಜಯಗೌರಿ ಸಿರಿವರ ಗೌರಿ ಮಂಗಳ ಗೌರಿಯೇ ಬಾರಮ್ಮ ।\nಭಾದ್ರಪದ ಮಾಸದಿ ಪೂಜಿಸಲ್ಪಡುವಂಥ ಸ್ವರ್ಣಗೌರಿಯೇ ಬಾರಮ್ಮ ॥',
'ನವರಾತ್ರಿ ದೇವಿ ಮೂಲ ಸರಸ್ವತಿ ಅಷ್ಟಮಿ ದುರ್ಗಿಯೇ ಬಾರಮ್ಮ ।\nದಶಮಿಯ ದಿನದೊಳು ವಿಜಯಂಗೈಯಲು ವಿಜಯಲಕ್ಷ್ಮಿಯೇ ಬಾರಮ್ಮ ॥',
'ಆದಿಶಕ್ತಿ ಅಖಿಲಾಂಡೇಶ್ವರಿ ಅನ್ನಪೂರ್ಣೇಶ್ವರಿ ಬಾರಮ್ಮ ।\nಆಶ್ರಿತ ಜನರಿಗೆ ಅಭಯ ನೀಡಲು ಸಂತೋಷಿ ಮಾತೆಯೇ ಬಾರಮ್ಮ ॥']
versions=[]
for vid,lang,label in [('kannada','kn','ಕನ್ನಡ'),('devanagari','kn-Deva','देवनागरी'),('roman','kn-Latn','English (Roman)')]:
 if vid=='roman':c='\n'.join(s['chorus']);vp=['\n'.join(v) for v in s['verses']]
 elif vid=='kannada':c=chorus;vp=ps
 else:
  c=tr(chorus,sanscript.KANNADA,sanscript.DEVANAGARI);vp=[tr(p,sanscript.KANNADA,sanscript.DEVANAGARI) for p in ps]
  for x,y in zip([chorus]+ps,[c]+vp):assert unicodedata.normalize('NFD',tr(y,sanscript.DEVANAGARI,sanscript.KANNADA))==unicodedata.normalize('NFD',x)
 chapters=[dict(id='chorus',title={'kannada':'ಪಲ್ಲವಿ','devanagari':'पल्लवि','roman':'Chorus'}[vid],paragraphs=[c]),dict(id='main',title={'kannada':'ಚರಣಗಳು','devanagari':'चरणाः','roman':'Verses'}[vid],paragraphs=vp,layout='verses')]
 text='\n\n'.join('\n\n'.join(ch['paragraphs']) for ch in chapters)
 versions.append(dict(id=vid,lang=lang,label=label,title={'kannada':'ಅಮ್ಮ ಬಾರಮ್ಮ','devanagari':'अम्म बारम्म','roman':'Amma Baaramma'}[vid],chapters=chapters,source_sha256=hashlib.sha256(text.encode()).hexdigest(),references=[dict(label='Family book — original Roman-script Kannada song',url='https://hawkeyedesi.github.io/family-songbook/assets/paduka-family-06.jpg')]))
versions[0]['reading_notice']='ಇದು ಕುಟುಂಬದ ಮೂಲ ರೋಮನ್ ಪಾಠದ ಕನ್ನಡ ಲಿಪಿರೂಪ. ಕೆಲವು ಅಸ್ಪಷ್ಟ ಪದಗಳಿಗೆ ಕುಟುಂಬದ ಪರಿಶೀಲನೆ ಬಾಕಿ. ಮೂಲ ಪಾಠವನ್ನು Roman ಆಯ್ಕೆಯಲ್ಲಿ ಓದಬಹುದು.'
versions[1]['reading_notice']='This is a script rendering of the Kannada song, not a Sanskrit translation. A few ambiguous Roman spellings still need family confirmation; the original Roman text is unchanged.'
(ROOT/'data/texts/amma-baaramma.json').write_text(json.dumps(dict(versions=versions),ensure_ascii=False,indent=2)+'\n')
s.update(versions_file='texts/amma-baaramma.json',language='ಕನ್ನಡ ಭಜನೆ · ಮೂರು ಲಿಪಿಗಳು',language_en='Kannada bhajan · three scripts',note='ಮೂಲ ರೋಮನ್ ಪಾಠ ಮತ್ತು ಚಿತ್ರವನ್ನು ಉಳಿಸಲಾಗಿದೆ. ಹೊಸ ಕನ್ನಡ ಮತ್ತು ದೇವನಾಗರಿ ಪಾಠಗಳು ಅದೇ ಕನ್ನಡ ಹಾಡಿನ ಲಿಪಿರೂಪಗಳು; ಸಂಸ್ಕೃತ ಅನುವಾದವಲ್ಲ. ಮೂಲದ “Moonu”, “Moodala”, “phalagata” ಮೊದಲಾದ ಅಸ್ಪಷ್ಟ ರೋಮನ್ ಪದಗಳ ಕನ್ನಡ ರೂಪಗಳಿಗೆ ಇನ್ನೂ ಕುಟುಂಬದ ಪರಿಶೀಲನೆ ಬೇಕಿದೆ.',note_en='The original Roman text is preserved verbatim. Kannada and Devanagari are phonetic script renderings of the same Kannada song, not Sanskrit translations. Ambiguous book spellings such as Moonu, Moodala and phalagata are retained phonetically, not silently corrected; their Kannada readings still need family confirmation. The source photo remains available.')
(ROOT/'data/songs.json').write_text(json.dumps(songs,ensure_ascii=False,indent=2)+'\n')
print('Amma: original Roman chorus/10verses unchanged; Kannada and Devanagari script views with explicit ambiguous-word note.')

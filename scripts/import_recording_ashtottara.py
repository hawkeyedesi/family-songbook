"""Import the Bhurupa 108-name version matched to the family recording.
Import-only dependency: indic-transliteration==2.3.82. Never use ASR as prayer text.
"""
from pathlib import Path
import json,re,hashlib,sys
from importlib.metadata import version
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
ROOT=Path(__file__).resolve().parents[1];raw=Path(sys.argv[1]).read_text();slug='lalitha-ashtottara-bhurupa'
assert version('indic-transliteration')=='2.3.82'
start=raw.index('ॐ भूरूपसकलाधारायै');stop=raw.index('इति श्रीललिताष्टोत्तरशतनामावलिः समाप्ता')
body=raw[start:stop].strip();names=[re.sub(r'-\n\s*','',p.strip()) for p in re.split(r'(?m)(?=^ॐ )',body) if p.strip()]
assert len(names)==108
for n,p in enumerate(names,1):
 assert p.startswith('ॐ ') and 'नमः' in p
 marker=re.search(r'(\d+)\s*$',p)
 if marker:assert int(marker[1])==n
assert names[15].startswith('ॐ घ्राणरूपायै') and names[17].startswith('ॐ गन्धग्रहणकारिण्यै')
opening=raw[raw.index('सिन्दूरारुणविग्रहां'):start].strip().split('\n\n');assert len(opening)==3
base=[dict(id='dhyana',title='ध्यानम्',paragraphs=opening),dict(id='names',title='अष्टोत्तरशतनामावलिः',paragraphs=names,layout='names'),dict(id='closing',title='समाप्तिः',paragraphs=['इति श्रीललिताष्टोत्तरशतनामावलिः समाप्ता ।'])]
versions=[];original='\n\n'.join('\n\n'.join(c['paragraphs']) for c in base)
for i,(vid,lang,label,scheme,title) in enumerate([
 ('kannada','kn','ಕನ್ನಡ',sanscript.KANNADA,'ಲಲಿತಾ ಅಷ್ಟೋತ್ತರ — ಭೂರೂಪ ಪಾಠ'),
 ('devanagari','sa','संस्कृतम्',sanscript.DEVANAGARI,'ललिताष्टोत्तरशतनामावलिः — भूरूपपाठः'),
 ('roman','en','English (Roman)',sanscript.IAST,'Lalitha Ashtottara — Bhurupa recording version')]):
 chapters=[]
 for c in base:
  ps=[transliterate(p,sanscript.DEVANAGARI,scheme) if vid!='devanagari' else p for p in c['paragraphs']]
  if vid!='devanagari':
   for before,after in zip(c['paragraphs'],ps):
    roundtrip=transliterate(after,scheme,sanscript.DEVANAGARI)
    assert roundtrip==before,(vid,before,roundtrip)
  chapters.append({**c,'title':transliterate(c['title'],sanscript.DEVANAGARI,scheme),'paragraphs':ps})
 text='\n\n'.join('\n\n'.join(c['paragraphs']) for c in chapters)
 v=dict(id=vid,label=label,lang=lang,title=title,chapters=chapters,references=[dict(label='Sanskrit Documents — Lalitha Ashtottara 2 (Bhurupa)',url='https://sanskritdocuments.org/doc_devii/lalitAShTottarashatanAmAvalI2.html')],source_sha256=hashlib.sha256(text.encode()).hexdigest())
 if vid!='devanagari':v['derivation']=dict(from_script='devanagari',from_sha256=hashlib.sha256(original.encode()).hexdigest(),tool='indic-transliteration',version='2.3.82',roundtrip_verified=True)
 versions.append(v)
(ROOT/'data/texts'/f'{slug}.json').write_text(json.dumps(dict(versions=versions,source_raw_sha256=hashlib.sha256(raw.encode()).hexdigest(),source_normalization='Joined discretionary hyphen/newline compounds; retained source wording and printed count markers.'),ensure_ascii=False,indent=2)+'\n')
songs=json.loads((ROOT/'data/songs.json').read_text());old=next((s for s in songs if s['slug']==slug),None);s=old or dict(slug=slug,collections=[],tags=['navaratri'])
s.update(title=versions[0]['title'],title_en=versions[2]['title'],category='ನಾಮಾವಳಿ',category_en='Namavali',language='ಕನ್ನಡ · संस्कृतम् · Roman',language_en='Kannada · Sanskrit · Roman',script='kannada',versions_file=f'texts/{slug}.json',description='“ಭೂರೂಪಸಕಲಾಧಾರಾಯೈ” ಎಂದು ಆರಂಭವಾಗುವ ೧೦೮ ನಾಮಗಳು — ಕುಟುಂಬದ ಧ್ವನಿಮುದ್ರಿಕೆಯಲ್ಲಿ ಪಠಿಸಿದ ಪಾಠ.',description_en='The 108 names beginning “Bhurupa-sakaladharāyai”, matched to the family recording.',note='ಪ್ರಕಟಿತ ಸಂಸ್ಕೃತ ಮೂಲದ ೧೦೮ ನಾಮಗಳನ್ನು ಉಳಿಸಲಾಗಿದೆ. ಕನ್ನಡ ಮತ್ತು ರೋಮನ್ ಲಿಪ್ಯಂತರಗಳನ್ನು ಹಿಮ್ಮುಖ ಲಿಪ್ಯಂತರದಿಂದ ಪರಿಶೀಲಿಸಲಾಗಿದೆ. ರಜತಾಚಲ ಪಾಠವು ಪ್ರತ್ಯೇಕವಾಗಿದೆ; ಇಲ್ಲಿ ಧ್ವನಿಮುದ್ರಿಕೆಯ ಪಾಠದ ಬದಲಿಗೆ ಬಳಸಿಲ್ಲ.',note_en='The published Sanskrit Bhurupa version matches the recording’s distinctive name sequence, including ghranarūpa, gandharūpa and gandhagrahanakarinī. All 108 names, the source’s three dhyana verses and closing are included. Kannada and Roman are deterministic, round-trip-checked script renderings, not translations or ASR guesses. Discretionary line-break hyphens are joined. The separately supplied Rajatachala version remains a separate entry.')
if not old:songs.append(s)
(ROOT/'data/songs.json').write_text(json.dumps(songs,ensure_ascii=False,indent=2)+'\n')
print('Imported recording-matched Bhurupa version:108 names and three dhyana verses; script round trips passed.')

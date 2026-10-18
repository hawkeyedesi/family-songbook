"""Import the separately supplied Rajatachala 108-name edition in three scripts."""
from pathlib import Path
import json,re,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];src=Path(sys.argv[1]);slug='lalitha-ashtottara-shatanamavali'
titles=['ಲಲಿತಾ ಅಷ್ಟೋತ್ತರ ಶತನಾಮಾವಳಿ — ರಜತಾಚಲ ಪಾಠ','ललिताष्टोत्तरशतनामावलिः — रजताचलपाठः','Lalitha Ashtottara — Rajatachala version']
versions=[]
for i,(sc,vid,lang,label,ending) in enumerate([('kn','kannada','kn','ಕನ್ನಡ','ನಮೋ ನಮಃ'),('hi','devanagari','sa','संस्कृतम्','नमो नमः'),('en','roman','en','English (Roman)','namō namaḥ')]):
 t=(src/f'lalitha108-{sc}.txt').read_text().strip();ps=t.split('\n\n');names=[p for p in ps if ending in p]
 assert len(names)==108 and all(len(p)<220 for p in names)
 for n,p in enumerate(names,1):
  m=re.search(r'(\d+)\s*$',p)
  if m:assert int(m[1])==n,(sc,n,p)
 seed=next(p for p in ps if p.startswith(['ಓಂ ಐಂ','ओं ऐं','ōṁ aiṁ'][i]))
 close=next(p for p in ps if p.startswith(['ಇತಿ ಶ್ರೀಲಲಿತಾ','इति श्रीललिता','iti śrīlalitā'][i]))
 chapters=[dict(id='invocation',title=['ಆರಂಭ','आरम्भः','Invocation'][i],paragraphs=[seed]),dict(id='names',title=['ನೂರ ಎಂಟು ಹೆಸರುಗಳು','अष्टोत्तरशतनामावलिः','The 108 names'][i],paragraphs=names,layout='names'),dict(id='closing',title=['ಸಮಾಪ್ತಿ','समाप्तिः','Closing'][i],paragraphs=[close])]
 text='\n\n'.join('\n\n'.join(c['paragraphs']) for c in chapters)
 url=f'https://stotranidhi.com/{sc}/sri-lalitha-ashtottara-{"shatanamavali" if sc=="kn" else "satanamavali"}-in-{["kannada","sanskrit","english"][i]}/'
 versions.append(dict(id=vid,label=label,lang=lang,title=titles[i],chapters=chapters,references=[dict(label='Stotra Nidhi — '+label,url=url)],source_sha256=hashlib.sha256(text.encode()).hexdigest()))
(ROOT/'data/texts'/f'{slug}.json').write_text(json.dumps(dict(versions=versions),ensure_ascii=False,indent=2)+'\n')
songs=json.loads((ROOT/'data/songs.json').read_text());old=next((s for s in songs if s['slug']==slug),None)
s=old or dict(slug=slug,collections=[],tags=['navaratri'])
s.update(title=titles[0],title_en=titles[2],category='ನಾಮಾವಳಿ',category_en='Namavali',language='ಕನ್ನಡ · संस्कृतम् · Roman',language_en='Kannada · Sanskrit · Roman',script='kannada',versions_file=f'texts/{slug}.json',description='“ರಜತಾಚಲಶೃಂಗಾಗ್ರ” ಎಂದು ಆರಂಭವಾಗುವ ಪ್ರತ್ಯೇಕ ೧೦೮ ನಾಮಗಳ ಪಾಠ.',description_en='The separate 108-name text beginning “Rajatachala-shringagra”.',note='ಹಂಚಿದ ಸ್ತೋತ್ರನಿಧಿಯ ಪ್ರತ್ಯೇಕ ಪಾಠವನ್ನು ಮೂರು ಲಿಪಿಗಳಲ್ಲಿ ನೀಡಲಾಗಿದೆ. ಕುಟುಂಬದ ಧ್ವನಿಮುದ್ರಿಕೆಯ ನಾಮಾವಳಿಗೆ ಬದಲಿಯಾಗಿ ಇದನ್ನು ಬಳಸಿಲ್ಲ. ರೋಮನ್ ಪಾಠವು ಉಚ್ಚಾರಣೆಗಾಗಿ; ಅರ್ಥಾನುವಾದವಲ್ಲ.',note_en='The separately supplied Stotra Nidhi edition, preserved in its three published scripts. It is not substituted for the family recording’s different namavali. Roman is pronunciation text, not an English translation.')
if not old:songs.append(s)
(ROOT/'data/songs.json').write_text(json.dumps(songs,ensure_ascii=False,indent=2)+'\n')
print('Imported the separate Lalitha Ashtottara:108 names per script, printed count markers checked.')

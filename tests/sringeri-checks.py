"""Guard meaningful source scope, preserved variants, corrections and exact cue targets."""
from pathlib import Path
import json,sys,re
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from source_audit import validate
from collections import Counter
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate as tr
import unicodedata
def normalized(t):return ''.join(c for c in unicodedata.normalize('NFC',t).replace('’',"'").replace('ऽ',"'") if c.isalpha() or unicodedata.category(c).startswith('M'))
songs=json.loads((ROOT/'data/songs.json').read_text());validate(songs)
by={s['slug']:s for s in songs}
for slug in ['rudra-namakam-chamakam','ganesha-atharvashirsham','vishnu-sahasranama','lalitha-sahasranama','soundarya-lahari']:assert 'weekly' in by[slug]['collections']
a=json.loads((ROOT/'data/sringeri-audit.json').read_text());assert a['summary']=={'sringeri-edition':8,'not-located':25}
for r in a['works']:
 for suffix in ['', 'devanagari','roman']:
  html=(ROOT/'songs'/r['slug']/suffix/'index.html').read_text()
  assert f'source-check {r["status"]}' in html and f'source-checks/#{r["slug"]}' in html
 if r['status']=='sringeri-edition':
  source=json.loads((ROOT/r['source_snapshot']).read_text());expected=[]
  for x in source['shlokas']:
   raw=next(v['value'] for v in x['title'] if v['lang']=='en')
   if re.search('[\u0904-\u0939]',raw):raw=tr(raw,sanscript.DEVANAGARI,sanscript.IAST)
   expected.append(normalized(raw))
  bundle=json.loads((ROOT/'data/texts'/f'{r["slug"]}.json').read_text())
  for v in bundle['versions']:
   scheme={'kannada':sanscript.KANNADA,'devanagari':sanscript.DEVANAGARI,'roman':sanscript.IAST}[v['id']]
   actual=[normalized(tr(p,scheme,sanscript.IAST) if v['id']!='roman' else p) for c in v['chapters'] for p in c['paragraphs']]
   assert Counter(actual)==Counter(expected),(r['slug'],v['id'],'source divergence')
   assert 'previous-edition' in (ROOT/'songs'/r['slug']/('' if v['id']=='kannada' else v['id'])/'index.html').read_text()
 if r['status']=='not-located':assert 'NOT Sringeri-verified' in r['note']
r=json.loads((ROOT/'data/durga-recording.json').read_text());assert r['videoId']=='_DP9lHAvGBU' and r['duration']==118.42
assert len(r['cues'])==8 and not r['cues'][0].get('work')
for i,c in enumerate(r['cues']):
 if i:assert r['cues'][i-1]['end']==c['start'] and c['anchor']==f'main-verse-{i}-1'
 for suffix in ['', 'devanagari','roman']:
  if c.get('anchor'):assert f'id="{c["anchor"]}"' in (ROOT/'songs/durga-saptashloki'/suffix/'index.html').read_text()
assert r['cues'][-1]['end']==r['duration']
for slug,readings in {'krishna-ashtakam':['ಯದಾ ಧರ್ಮಗ್ಲಾನಿರ್ಭವತಿ','यदा धर्मग्लानिर्भवति','yadā dharmaglānirbhavati'],'kalabhairava-ashtakam':['ಭವಾಬ್ಧಿತಾರಕಂ','भवाब्धितारकं','bhavābdhitārakaṃ']}.items():
 vs=json.loads((ROOT/'data/texts'/f'{slug}.json').read_text())['versions']
 for v,want in zip(vs,readings):assert want in '\n'.join(p for c in v['chapters'] for p in c['paragraphs'])
 assert (ROOT/'data/sringeri'/f'before-{slug}.json').is_file()
print('PASS all33 honest statuses,99 visible badges,8 immutable witnesses,two3-scriptcorrections,Durga7cueanchors,Daily/Navaratri preserved')

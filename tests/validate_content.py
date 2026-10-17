"""Meaningful completeness/edition checks; run before publishing."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
a=json.loads((ROOT/'data/songs.json').read_text());by_slug={s['slug']:s for s in a}
assert len(a)==17 and len(by_slug)==17
assert all('versions_file' in s for s in a if s['slug']!='amma-baaramma'),'Incomplete script coverage'
old=json.loads(subprocess.check_output(['git','show','e4e65c9:data/songs.json'],cwd=ROOT))
for s in old:
 assert by_slug[s['slug']]['verses']==s['verses'],f'Changed existing prayer: {s["slug"]}'
 assert by_slug[s['slug']].get('chorus')==s.get('chorus')
for s in a:
 if 'versions_file' not in s:continue
 versions=json.loads((ROOT/'data'/s['versions_file']).read_text())['versions']
 assert [v['id'] for v in versions]==['kannada','devanagari','roman']
 seqs=[]
 for v in versions:
  text='\n\n'.join('\n\n'.join(c['paragraphs']) for c in v['chapters'])
  assert hashlib.sha256(text.encode()).hexdigest()==v['source_sha256'],s['slug']+' source text changed'
  assert '<<<' not in text and '[Showing truncated' not in text and '\ufffd' not in text
  if v['id']=='kannada':assert not re.search('[A-Za-z\u0904-\u0939]',text)
  if v['id']=='devanagari':assert not re.search('[A-Za-z\u0c80-\u0cff]',text)
  if v['id']=='roman':assert not re.search('[\u0904-\u0939\u0c80-\u0cff]',text)
  seqs.append([int(n) for n in re.findall(r'[।॥]\s*(\d+)\s*॥',text)])
  if s['slug'] in {'aditya-hridayam','lakshmi-nrisimha-karavalamba','durga-suktam','sri-suktam','krishna-ashtakam','surya-kavacham','daily-puja-mantras'}:
   ps=[p for c in v['chapters'] for p in c['paragraphs']]
   assert len(ps)==len(s['verses'])
   if v['id']=='kannada':assert ps==['\n'.join(lines) for lines in s['verses']]
   else:
    assert v['derivation']['from_sha256']==hashlib.sha256('\n\n'.join('\n'.join(lines) for lines in s['verses']).encode()).hexdigest()
    assert v['derivation']['roundtrip_verified'] is True
  chapter={c['id']:'\n\n'.join(c['paragraphs']) for c in v['chapters']}
  numbers=lambda t:[int(n) for n in re.findall(r'[।॥]\s*(\d+)\s*॥',t)]
  if s['slug']=='lalitha-sahasranama':assert numbers(chapter['main'])==list(range(1,184))
  if s['slug']=='vishnu-sahasranama':assert numbers(chapter['main'])==list(range(1,109))
  if s['slug']=='rudra-namakam-chamakam':
   assert numbers(chapter['namakam'])==list(range(1,12));assert numbers(chapter['chamakam'])==list(range(1,12))
  if s['slug']=='ganesha-atharvashirsham':assert numbers(text)==list(range(1,15))
  if s['slug']=='soundarya-lahari':
   assert numbers(chapter['ananda'])==list(range(1,42));assert numbers(chapter['soundarya'])==list(range(42,101));assert numbers(chapter['appendix'])==[101,102,103]
  if s['slug']=='lakshmi-ashtottara-shatanamavali':
   assert len(v['chapters'])==1 and len(v['chapters'][0]['paragraphs'])==108
   assert v['chapters'][0]['layout']=='names'
  if s['slug']=='hanuman-chalisa':
   assert numbers(chapter['chalisa'])==list(range(1,41));assert chapter['opening'] and chapter['closing'] and chapter['dhyana']
  if s['slug'] in ['kalabhairava-ashtakam','mahalakshmi-ashtakam']:
   assert numbers(chapter['main'])==list(range(1,9));assert chapter['closing']
 assert seqs[0]==seqs[1]==seqs[2]
 print('PASS',s['slug'],'complete source text + matching verse sequence in three scripts')
print('PASS: all nine original transcriptions preserved; 17 entries total.')

"""Meaningful completeness/edition checks; run before publishing."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
a=json.loads((ROOT/'data/songs.json').read_text());by_slug={s['slug']:s for s in a}
assert len(a)==14 and len(by_slug)==14
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
  chapter={c['id']:'\n\n'.join(c['paragraphs']) for c in v['chapters']}
  numbers=lambda t:[int(n) for n in re.findall(r'[।॥]\s*(\d+)\s*॥',t)]
  if s['slug']=='lalitha-sahasranama':assert numbers(chapter['main'])==list(range(1,184))
  if s['slug']=='vishnu-sahasranama':assert numbers(chapter['main'])==list(range(1,109))
  if s['slug']=='rudra-namakam-chamakam':
   assert numbers(chapter['namakam'])==list(range(1,12));assert numbers(chapter['chamakam'])==list(range(1,12))
  if s['slug']=='ganesha-atharvashirsham':assert numbers(text)==list(range(1,15))
  if s['slug']=='soundarya-lahari':
   assert numbers(chapter['ananda'])==list(range(1,42));assert numbers(chapter['soundarya'])==list(range(42,101));assert numbers(chapter['appendix'])==[101,102,103]
 assert seqs[0]==seqs[1]==seqs[2]
 print('PASS',s['slug'],'complete source text + matching verse sequence in three scripts')
print('PASS: all nine existing prayers unchanged; 14 entries total.')

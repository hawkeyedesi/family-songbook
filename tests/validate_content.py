"""Meaningful completeness/edition checks; run before publishing."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
a=json.loads((ROOT/'data/songs.json').read_text());by_slug={s['slug']:s for s in a}
assert len(a)==23 and len(by_slug)==23
groups={g:[s['slug'] for s in a if g in s.get('collections',[s.get('collection','daily')])] for g in ['daily','weekly','friday','paduka-puja-bhajans']}
assert {g:len(ls) for g,ls in groups.items()}=={'daily':7,'weekly':4,'friday':12,'paduka-puja-bhajans':1}
assert all(s.get('collections') and set(s['collections']) <= set(groups) for s in a)
assert groups['paduka-puja-bhajans']==['amma-baaramma']
assert 'amma-baaramma' not in groups['daily']
assert 'lakshmi-nrisimha-karavalamba' in groups['weekly'] and 'lakshmi-nrisimha-karavalamba' in groups['friday']
expected_friday=['lakshmi-nrisimha-karavalamba','lakshmi-ashtottara-shatanamavali','durga-suktam','sri-suktam','ya-devi-sarva-bhuteshu','sharada-bhujanga-ashtakam','mahishasura-mardini','bhagyada-lakshmi-baramma','mantra-pushpam','hanuman-chalisa','mahalakshmi-ashtakam','kalabhairava-ashtakam']
assert sorted(groups['friday'],key=lambda slug:by_slug[slug]['collection_order']['friday'])==expected_friday
assert all('versions_file' in s for s in a if s['slug']!='amma-baaramma'),'Incomplete script coverage'
old=json.loads(subprocess.check_output(['git','show','e4e65c9:data/songs.json'],cwd=ROOT))
vedic_totals={'sri-suktam':[279]*3,'durga-suktam':[156]*3,'ganesha-atharvashirsham':[391]*3,'rudra-namakam-chamakam':[2317,2318,2318],'mantra-pushpam':[403]*3}
assert {s['slug'] for s in a if s.get('vedic')}=={*vedic_totals,'daily-puja-mantras'}
assert by_slug['daily-puja-mantras']['svara_status']=='scan-only'
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
  if s['slug'] in {'aditya-hridayam','durga-suktam','sri-suktam','krishna-ashtakam','surya-kavacham','daily-puja-mantras'} and not s.get('published_edition'):
   ps=[p for c in v['chapters'] for p in c['paragraphs']]
   assert len(ps)==len(s['verses'])
   if v['id']=='kannada':assert ps==['\n'.join(lines) for lines in s['verses']]
   else:
    assert v['derivation']['from_sha256']==hashlib.sha256('\n\n'.join('\n'.join(lines) for lines in s['verses']).encode()).hexdigest()
    assert v['derivation']['roundtrip_verified'] is True
  chapter={c['id']:'\n\n'.join(c['paragraphs']) for c in v['chapters']}
  if s.get('vedic') and s['svara_status']=='marked':
   marks=''.join(c for c in text if c in '\u0951\u0952\u1cda\u030d\u030e\u0320\u0331')
   assert len(marks)>150
   assert v['svara_profile']['sequence_sha256']==hashlib.sha256(marks.encode()).hexdigest(),'Lost/reordered Vedic marks'
   assert v['svara_profile']['counts']=={f'U+{ord(c):04X}':marks.count(c) for c in set(marks)}
   suffix='' if v['id']=='kannada' else v['id']
   rendered=(ROOT/'songs'/s['slug']/suffix/'index.html').read_text()
   article=rendered.split('aria-label="Prayer text">',1)[1].split('</article>',1)[0]
   assert ''.join(c for c in article if c in '\u0951\u0952\u1cda\u030d\u030e\u0320\u0331')==marks,'Renderer lost/reordered svara'
   assert 'svara-key' in rendered and 'svara-notice' in rendered
  if s['slug']=='sri-suktam':assert [int(n) for n in re.findall(r'॥\s*(\d+)\s*॥',chapter['main'])]==list(range(1,16)) and chapter['gayatri'] and chapter['shanti']
  if s['slug']=='durga-suktam':
   assert len(v['chapters'][0]['paragraphs'])==7 and chapter['gayatri'] and chapter['shanti']
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
  if s['slug']=='lalitha-sahasra-namavali':
   ns=next(c for c in v['chapters'] if c['id']=='names');assert len(ns['paragraphs'])==1000 and ns['layout']=='names'
   for n,p in enumerate(ns['paragraphs'],1):
    marker=re.search(r'(\d+)\s*$',p)
    if marker:assert int(marker[1])==n
  if s['slug'] in ['ya-devi-sarva-bhuteshu','sharada-bhujanga-ashtakam','mahishasura-mardini']:
   assert numbers(text)==list(range(1,{'ya-devi-sarva-bhuteshu':28,'sharada-bhujanga-ashtakam':8,'mahishasura-mardini':21}[s['slug']]+1))
  if s['slug']=='bhagyada-lakshmi-baramma':
   assert [c['id'] for c in v['chapters']]==['pallavi',*[f'charanam-{n}' for n in range(1,6)]]
   assert len(v['source_corrections'])==3
   for fix in v['source_corrections']:assert fix['reading'] in text and fix['original'] not in text
  if s['slug']=='mantra-pushpam':
   assert [c['id'] for c in v['chapters']]==['opening','main','closing']
   assert all(c['paragraphs'] for c in v['chapters'])
  if s['slug']=='lakshmi-nrisimha-karavalamba':
   ps=v['chapters'][0]['paragraphs'];assert len(ps)==25
   assert [int(re.search(r'(?:॥|\|\|)\s*(\d+)\s*(?:॥|\|\|)',p)[1]) for p in ps]==list(range(1,26))
   assert s['preserve_original_transcription'] and len(s['verses'])==17
  if s['slug']=='hanuman-chalisa':
   assert numbers(chapter['chalisa'])==list(range(1,41));assert chapter['opening'] and chapter['closing'] and chapter['dhyana']
  if s['slug'] in ['kalabhairava-ashtakam','mahalakshmi-ashtakam']:
   assert numbers(chapter['main'])==list(range(1,9));assert chapter['closing']
 assert seqs[0]==seqs[1]==seqs[2]
 if s['slug'] in vedic_totals:
  totals=[sum(v['svara_profile']['counts'].values()) for v in versions];assert totals==vedic_totals[s['slug']],(s['slug'],totals)
  mapping={'\u0951':'S','\u0952':'A','\u1cda':'D','\u030d':'S','\u030e':'D','\u0320':'A','\u0331':'A'}
  accents=[''.join(mapping[c] for c in '\n\n'.join('\n\n'.join(ch['paragraphs']) for ch in v['chapters']) if c in mapping) for v in versions]
  if s['slug']=='rudra-namakam-chamakam':
   # Published namakam 9 has gṃ vs g-m nasal expansion; retain each source, don't invent a repair.
   assert accents[1]==accents[2]
   assert accents[1][1061]=='A' and accents[1][:1061]+accents[1][1062:]==accents[0]
  else:assert accents[0]==accents[1]==accents[2],'Cross-script svara mismatch'
 if s['slug']=='daily-puja-mantras':
  for suffix in ['', 'devanagari','roman']:
   html=(ROOT/'songs'/s['slug']/suffix/'index.html').read_text();assert 'svara-notice scan-only' in html and 'marked-scan-link' in html and 'daily-mantras-p65.jpg' in html
 print('PASS',s['slug'],'complete source text + matching verse sequence in three scripts')
print('PASS: all nine original transcriptions preserved; 23 entries; Friday order and overlapping schedules verified.')
for ui in ['', 'en']:
 for group in [None,*groups]:
  path=ROOT/ui/(group or '')/'index.html';html=path.read_text()
  want=a if group is None else sorted([s for s in a if s['slug'] in groups[group]],key=lambda s:s.get('collection_order',{}).get(group,999))
  assert re.findall(r'data-work="([a-z0-9-]+)"',html)==[s['slug'] for s in want],str(path)
  assert len(re.findall('data-collection=',html))==5
  for href in re.findall(r'<a href="([^"]+)"',html):
   if href.startswith(('http','#')):continue
   target=(path.parent/href).resolve()
   assert target.is_file() or (target/'index.html').is_file(),(path,href)
print('PASS: all ten generated landing pages, list order, category links and static destinations.')

"""Meaningful completeness/edition checks; run before publishing."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parents[1]
a=json.loads((ROOT/'data/songs.json').read_text());by_slug={s['slug']:s for s in a}
assert len(a)==33 and len(by_slug)==33
groups={g:[s['slug'] for s in a if g in s.get('collections',[s.get('collection','daily')])] for g in ['daily','weekly','friday','paduka-puja-bhajans']}
assert {g:len(ls) for g,ls in groups.items()}=={'daily':7,'weekly':4,'friday':12,'paduka-puja-bhajans':10}
assert all((s.get('collections') or s.get('tags')) and set(s['collections']) <= set(groups) for s in a)
expected_paduka=['durga-saptashloki','om-jai-jagdish-hare','hanuman-chalisa','mahalakshmi-ashtakam','amma-baaramma','sharade-sharade','dehi-dehi-sharada','guru-bhakti-gurvashtakam','jagadguru-pancharatnamala','shankara-guru']
assert sorted(groups['paduka-puja-bhajans'],key=lambda slug:by_slug[slug]['collection_order']['paduka-puja-bhajans'])==expected_paduka
assert 'amma-baaramma' not in groups['daily']
assert 'lakshmi-nrisimha-karavalamba' in groups['weekly'] and 'lakshmi-nrisimha-karavalamba' in groups['friday']
expected_friday=['lakshmi-nrisimha-karavalamba','lakshmi-ashtottara-shatanamavali','durga-suktam','sri-suktam','ya-devi-sarva-bhuteshu','sharada-bhujanga-ashtakam','mahishasura-mardini','bhagyada-lakshmi-baramma','mantra-pushpam','hanuman-chalisa','mahalakshmi-ashtakam','kalabhairava-ashtakam']
assert sorted(groups['friday'],key=lambda slug:by_slug[slug]['collection_order']['friday'])==expected_friday
assert all('versions_file' in s for s in a if s['slug']!='amma-baaramma'),'Incomplete script coverage'
old=json.loads(subprocess.check_output(['git','show','e4e65c9:data/songs.json'],cwd=ROOT))
vedic_totals={'sri-suktam':[279]*3,'durga-suktam':[156]*3,'ganesha-atharvashirsham':[391]*3,'rudra-namakam-chamakam':[2317,2318,2318],'mantra-pushpam':[403]*3}
assert {s['slug'] for s in a if s.get('vedic')}=={*vedic_totals,'daily-puja-mantras','navaratri-puja-passages'}
assert by_slug['daily-puja-mantras']['svara_status']=='scan-only'
assert [s['slug'] for s in a if 'navaratri' in s.get('tags',[])]==['lalitha-sahasra-namavali','lalitha-ashtottara-shatanamavali','lalitha-ashtottara-bhurupa','navaratri-puja-passages']
assert 'weekly' in by_slug['lalitha-sahasra-namavali']['collections'],'Tagging must not replace schedule'
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
   assert len(marks)>=(227 if s['slug']=='navaratri-puja-passages' else 150)
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
  if s['slug'] in ['lalitha-ashtottara-bhurupa','lalitha-ashtottara-shatanamavali']:
   ns=next(c for c in v['chapters'] if c['id']=='names');assert len(ns['paragraphs'])==108 and ns['layout']=='names'
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
print('PASS: all nine original transcriptions preserved; 33 entries; Friday order and overlapping schedules verified.')
for ui in ['', 'en']:
 for group in [None,*groups,'navaratri']:
  path=ROOT/ui/(group or '')/'index.html';html=path.read_text()
  want=a if group is None else sorted([s for s in a if (group in s.get('tags',[]) if group=='navaratri' else s['slug'] in groups[group])],key=lambda s:s.get('collection_order',{}).get(group,999))
  assert re.findall(r'data-work="([a-z0-9-]+)"',html)==[s['slug'] for s in want],str(path)
  assert len(re.findall('data-collection=',html))==6
  for href in re.findall(r'<a href="([^"]+)"',html):
   if href.startswith(('http','#')):continue
   target=(path.parent/href).resolve()
   assert target.is_file() or (target/'index.html').is_file(),(path,href)
print('PASS: all twelve generated landing/tag pages, list order, category links and static destinations.')

recording=json.loads((ROOT/'data/navaratri-recording.json').read_text())
assert recording['videoId']=='Cjd9t7t7MAA' and recording['duration']==2475
assert recording['reciter']=='Devenhalli Nagaraj Shastrigalu' and 'Narayana' in recording['recorder']
cues=recording['cues'];assert cues and cues[0]['start']==0 and cues[-1]['end']==2475
assert len({c['id'] for c in cues})==len(cues)
for i,c in enumerate(cues):
 assert 0<=c['start']<c['end']<=2475
 if i:assert cues[i-1]['end']==c['start'],'Timeline gaps must be explicitly labelled'
 if c.get('work'):
  assert c['work'] in by_slug and c['evidence']
  for v in json.loads((ROOT/'data'/by_slug[c['work']]['versions_file']).read_text())['versions']:
   anchor=c.get('anchor');chapters=v['chapters']
   if anchor and anchor.startswith('names-name-'):
    count=int(anchor.removeprefix('names-name-'));assert 0<count<=len(next(ch for ch in chapters if ch['id']=='names')['paragraphs'])
   elif anchor:assert anchor in [ch['id'] for ch in chapters]
print('PASS recording credits, complete explicit timeline and valid sourced reading anchors')

extra=json.loads((ROOT/'data/texts/navaratri-puja-passages.json').read_text())['versions']
code={'\u0951':'S','\u0952':'A','\u1cda':'D','\u030d':'S','\u030e':'D','\u0320':'A','\u0331':'A'}
pitches=[''.join(code[c] for ch in v['chapters'] for p in ch['paragraphs'] for c in p if c in code) for v in extra]
assert pitches[0]==pitches[1]==pitches[2] and len(pitches[0])==227
prelude=recording['preludes'][0];assert prelude['videoId']=='tw9uOA5d7-A' and prelude['start']==2106 and prelude['duration']==2749
assert prelude['cues'][0]['start']==2106 and prelude['cues'][-1]['end']==2749
for i,c in enumerate(prelude['cues']):
 assert c['start']<c['end']
 if i:assert prelude['cues'][i-1]['end']==c['start']
 if c.get('work'):
  assert c['work']=='navaratri-puja-passages' and c['evidence']
  assert all(c['anchor'] in [ch['id'] for ch in v['chapters']] for v in extra)
print('PASS Ganapathy offset/timeline and227exact cross-script Vedic marks in sourced ritual excerpts')

counts={'durga-saptashloki':[7],'om-jai-jagdish-hare':[10],'sharade-sharade':[3,1],'dehi-dehi-sharada':[4,1],'guru-bhakti-gurvashtakam':[8,1,1],'jagadguru-pancharatnamala':[6],'shankara-guru':[3],'amma-baaramma':[1,10]}
for slug,want in counts.items():
 vs=json.loads((ROOT/'data'/by_slug[slug]['versions_file']).read_text())['versions']
 assert all([len(c['paragraphs']) for c in v['chapters']]==want for v in vs),slug
 if slug=='amma-baaramma':
  assert vs[2]['chapters'][0]['paragraphs']==['\n'.join(by_slug[slug]['chorus'])]
  assert vs[2]['chapters'][1]['paragraphs']==['\n'.join(v) for v in by_slug[slug]['verses']]
 if slug=='guru-bhakti-gurvashtakam':
  assert 'अनर्घ्याणि' in vs[1]['chapters'][1]['paragraphs'][0]
  assert 'गुरोरुक्तवाक्ये' in vs[1]['chapters'][2]['paragraphs'][0]
assert by_slug['hanuman-chalisa']['scans']==['paduka-family-04.jpg','paduka-family-03.jpg']
assert by_slug['shankara-guru']['scans']==[],'Contact-bearing scan must stay private'
assert len(list((ROOT/'assets').glob('paduka-family-*.jpg')))==10
assert all('daily' not in by_slug[slug]['collections'] for slug in expected_paduka)
print('PASS Paduka10works,33total,all3scripts,split-pagecompleteness,unchangedAmmaRoman,private-scanexclusion')

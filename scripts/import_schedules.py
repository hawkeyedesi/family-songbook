"""Import reviewed Weekly/Friday extracts, then apply the family reading lists.
Usage: python3 scripts/import_schedules.py /tmp/bhakti-schedules
Input files are complete Vaidika Vignanam extracts, except lalitha-nidhi-*.
"""
from pathlib import Path
import hashlib,json,re,sys
ROOT=Path(__file__).resolve().parents[1];src=Path(sys.argv[1])
songs=json.loads((ROOT/'data/songs.json').read_text());by={s['slug']:s for s in songs}
scripts=[('kannada','kn','ಕನ್ನಡ'),('devanagari','sa','संस्कृतम्'),('english','en','English (Roman)')]
configs=[
 ('ya-devi-sarva-bhuteshu','devi-aparajita-stotram','ಯಾ ದೇವೀ ಸರ್ವಭೂತೇಷು — ಅಪರಾಜಿತಾ ಸ್ತೋತ್ರಮ್','या देवी सर्वभूतेषु — अपराजितास्तोत्रम्','Ya Devi Sarva Bhuteshu — Aparajita Stotram',28),
 ('sharada-bhujanga-ashtakam','sharada-bhujanga-prayata-ashtakam','ಶಾರದಾ ಭುಜಂಗ ಪ್ರಯಾತ ಅಷ್ಟಕಮ್','शारदाभुजङ्गप्रयाताष्टकम्','Sharada Bhujanga Prayata Ashtakam',8),
 ('mahishasura-mardini','sri-mahishasura-mardini-stotram-ayigiri-nandini','ಮಹಿಷಾಸುರಮರ್ದಿನೀ ಸ್ತೋತ್ರಮ್ — ಅಯಿಗಿರಿ ನಂದಿನಿ','महिषासुरमर्दिनीस्तोत्रम् — अयि गिरिनन्दिनि','Mahishasura Mardini Stotram — Aigiri Nandini',21),
 ('bhagyada-lakshmi-baramma','bhagyada-lakshmi-baramma','ಭಾಗ್ಯದ ಲಕ್ಷ್ಮೀ ಬಾರಮ್ಮ','भाग्यद लक्ष्मी बारम्म','Bhagyada Lakshmi Baramma',5),
 ('mantra-pushpam','mantra-pushpam','ಮಂತ್ರಪುಷ್ಪಮ್','मन्त्रपुष्पम्','Mantra Pushpam',0),
 ('lalitha-sahasra-namavali','lalitha-nidhi','ಶ್ರೀ ಲಲಿತಾ ಸಹಸ್ರನಾಮಾವಳಿ','श्रीललितासहस्रनामावलिः','Lalitha Sahasra Namavali',1000),
]
def ch(cid,title,ps,**kw):return dict(id=cid,title=title,paragraphs=ps,**kw)
for slug,source,kn,sa,en,count in configs:
 versions=[];seqs=[]
 for i,(sc,lang,label) in enumerate(scripts):
  whole=(src/f'{source}-{sc}.txt').read_text().strip();assert whole and '<<<' not in whole
  ps=whole.split('\n\n');chapters=[]
  if source=='lalitha-nidhi':
   prefix=['ಓಂ ','ओं ','ōṁ '][i];end=['ನಮಃ','नमः','namaḥ'][i]
   names=[p for p in ps if p.startswith(prefix) and end in p]
   assert len(names)==1000
   # Every published decade marker must agree with its actual list position.
   for n,p in enumerate(names,1):
    marker=re.search(r'(\d+)\s*$',p)
    if marker:assert int(marker[1])==n,(sc,n,p)
   invocation=next(p for p in ps if p.startswith(prefix) and end not in p)
   chapters=[ch('invocation',['ಆರಂಭ','आरम्भः','Invocation'][i],[invocation]),ch('names',['ಸಾವಿರ ನಾಮಗಳು','सहस्रनामावलिः','The 1,000 names'][i],names,layout='names')]
   url=f'https://stotranidhi.com/{["kn","hi","en"][i]}/sri-lalitha-sahasranamavali-in-{["kannada","sanskrit","english"][i]}/';publisher='Stotra Nidhi'
  else:
   url=f'https://vignanam.org/{sc}/{source}.html';publisher='Vaidika Vignanam'
   if slug=='bhagyada-lakshmi-baramma':
    # Music metadata uses different solfege alphabets; keep the song itself intact.
    t=whole[whole.index(['ಪಲ್ಲವಿ','पल्लवि','pallavi'][i]):];ps=t.split('\n\n')
    pattern=['ಚರಣಂ ','चरणं ','charaṇaṃ '][i]
    indices=[j for j,p in enumerate(ps) if p.startswith(pattern)];assert len(indices)==5
    chapters=[ch('pallavi',['ಪಲ್ಲವಿ','पल्लवि','Pallavi'][i],ps[:indices[0]])]
    for n,j in enumerate(indices):
     end=indices[n+1] if n<4 else len(ps)
     chapters.append(ch('charanam-'+str(n+1),[f'ಚರಣ {n+1}',f'चरण {n+1}',f'Charanam {n+1}'][i],ps[j:end]))
    lang='kn' if sc=='devanagari' else lang;label='देवनागरी' if sc=='devanagari' else label
   elif slug=='mantra-pushpam':
    plain=lambda p:re.sub('[\u0951\u0952\u1cda\u1cdd\u030d\u030e\u0320]','',p)
    start=next(j for j,p in enumerate(ps) if plain(p).startswith(['ಯೋ','यो','yō'][i]));close=next(j for j,p in enumerate(ps) if ['ರಾಜಾಧಿ','राजाधि','rājādhi'][i] in plain(p))
    chapters=[ch('opening',['ಶಾಂತಿಮಂತ್ರ','शान्तिमन्त्रः','Opening peace prayer'][i],ps[:start]),ch('main',['ಮಂತ್ರಪುಷ್ಪಮ್','मन्त्रपुष्पम्','Mantra Pushpam'][i],ps[start:close]),ch('closing',['ಸಮಾಪನ ಮಂತ್ರಗಳು','समापनमन्त्राः','Closing prayers'][i],ps[close:])]
   else:
    nums=[int(n) for n in re.findall(r'[।॥]\s*(\d+)\s*॥',whole)];assert nums==list(range(1,count+1)),(slug,sc,nums)
    chapters=[ch('main',['ಸ್ತೋತ್ರಮ್','स्तोत्रम्','Hymn'][i],ps)]
  t='\n\n'.join('\n\n'.join(c['paragraphs']) for c in chapters)
  versions.append(dict(id='roman' if sc=='english' else sc,lang=lang,label=label,title=[kn,sa,en][i],chapters=chapters,references=[dict(label=publisher+' — '+label,url=url)],source_sha256=hashlib.sha256(t.encode()).hexdigest()))
  seqs.append([int(n) for n in re.findall(r'[।॥]\s*(\d+)\s*॥',t)])
 assert seqs[0]==seqs[1]==seqs[2],slug
 (ROOT/'data/texts'/f'{slug}.json').write_text(json.dumps(dict(versions=versions),ensure_ascii=False,indent=2)+'\n')
 bhajan=slug=='bhagyada-lakshmi-baramma'
 s=by.get(slug,dict(slug=slug))
 s.update(title=kn,title_en=en,category='ಭಜನೆ' if bhajan else ('ನಾಮಾವಳಿ' if count==1000 else 'ಸ್ತೋತ್ರ'),category_en='Bhajan' if bhajan else ('Namavali' if count==1000 else 'Stotra'),language='ಕನ್ನಡ · देवनागरी · Roman' if bhajan else 'ಕನ್ನಡ · संस्कृतम् · Roman',language_en='Kannada · Devanagari · Roman' if bhajan else 'Kannada · Sanskrit · Roman',script='kannada',description=kn+' — ಮೂರು ಲಿಪಿಗಳಲ್ಲಿ.',description_en=en+' — in three scripts.',versions_file=f'texts/{slug}.json',note='ಪ್ರಕಟಿತ ಮೂಲದ ಪಠ್ಯವನ್ನು ಮೂರು ಲಿಪಿಗಳಲ್ಲಿ ಉಳಿಸಲಾಗಿದೆ. ರೋಮನ್ ಲಿಪಿಯು ಪಠಣಕ್ಕಾಗಿ; ಅರ್ಥಾನುವಾದವಲ್ಲ.',note_en='One published edition in three scripts. Roman text is for pronunciation, not an English translation. Textual variants are retained.')
 if bhajan:
  s['note']+=' ಪುರಂದರದಾಸರ ಕನ್ನಡ ಕೀರ್ತನೆ; ದೇವನಾಗರಿಯಲ್ಲಿಯೂ ಅದೇ ಕನ್ನಡ ಪದಗಳು, ಸಂಸ್ಕೃತ ಅನುವಾದವಲ್ಲ.'
  s['note_en']+=' Purandara Dasa’s Kannada composition: Devanagari also preserves the Kannada words, not a Sanskrit translation. Pallavi and all five charanams are included. This is distinct from Amma Baaramma.'
  s['references']=[dict(label='Bhakti Nidhi — comparison Kannada edition',url='https://bhaktinidhi.com/kn/bhagyada-lakshmi-baramma-lyrics-in-kannada/')]
 if slug=='ya-devi-sarva-bhuteshu':s['references']=[dict(label='Stotra Nidhi — comparison edition',url='https://stotranidhi.com/hi/aparajitha-stotram-in-sanskrit/')]
 if slug=='sharada-bhujanga-ashtakam':
  s['references']=[dict(label='Sanskrit Documents — comparison edition',url='https://sanskritdocuments.org/doc_devii/shaaradaabhuja.html')]
  s['note_en']+=' The comparison edition has variants in verses 3 and 5; the reading follows Vaidika Vignanam consistently.'
 if slug=='mantra-pushpam':
  s['category']='ವೇದಮಂತ್ರ';s['category_en']='Vedic hymn'
  s['note_en']+=' Includes the source’s opening peace prayer and closing mantras. Other puja compilations may add Narayana Suktam and additional Gayatris; these are not silently blended into this edition.'
  s['references']=[dict(label='Stotra Nidhi — expanded puja compilation for comparison',url='https://stotranidhi.com/kn/mantra-pushpam-in-kannada/')]
 if count==1000:
  s['note_en']+=' A separate 1,000-name offering list, not the metrical Sahasranama stotram. The family’s temple PDF is linked as a comparison; the reading uses one matched Stotra Nidhi edition.'
  s['references']=[dict(label='Family-shared temple PDF — Devanagari namavali',url='https://www.temple.org/templates/jd_boston/downloads/sree_lalitha_sahasra_namavali_Hindi.pdf')]
 if slug not in by:songs.append(s);by[slug]=s
 print(slug,'three scripts checked')
friday=['lakshmi-nrisimha-karavalamba','lakshmi-ashtottara-shatanamavali','durga-suktam','sri-suktam','ya-devi-sarva-bhuteshu','sharada-bhujanga-ashtakam','mahishasura-mardini','bhagyada-lakshmi-baramma','mantra-pushpam','hanuman-chalisa','mahalakshmi-ashtakam','kalabhairava-ashtakam']
weekly=['lakshmi-nrisimha-karavalamba','soundarya-lahari','lalitha-sahasranama','lalitha-sahasra-namavali']
for s in songs:
 groups=[g for g,ls in [('weekly',weekly),('friday',friday)] if s['slug'] in ls]
 s['collections']=groups or s.get('collections',['daily'])
 s.pop('collection',None)
 s['collection_order']={g:ls.index(s['slug']) for g,ls in [('weekly',weekly),('friday',friday)] if s['slug'] in ls}
for slug,url in [('soundarya-lahari','https://sanskritdocuments.org/doc_devii/saundaryalahari.pdf'),('lalitha-sahasranama','https://sanskritdocuments.org/doc_devii/lalita.pdf'),('lakshmi-nrisimha-karavalamba','https://stotranidhi.com/hi/lakshmi-narasimha-karavalamba-stotram-in-sanskrit/')]:
 refs=by[slug].setdefault('references',[])
 if not any(r['url']==url for r in refs):refs.append(dict(label='Family-shared comparison edition',url=url))
# The shared Karavalamba source is a longer edition than the 17-verse family scan.
s=by['lakshmi-nrisimha-karavalamba'];versions=[]
for i,(sc,lang,label) in enumerate(scripts):
 whole=(src/f'karavalamba-{sc}.txt').read_text().strip()
 start=whole.index(['ಶ್ರೀಮತ್ಪಯೋನಿಧಿ','श्रीमत्पयोनिधि','śrīmatpayōnidhi'][i])
 t=whole[start:].replace('||','॥').replace('|','।');matches=list(re.finditer(r'॥\s*(\d+)\s*॥',t));assert [int(m[1]) for m in matches[:25]]==list(range(1,26))
 ps=[];pos=0
 for m in matches[:25]:ps.append(t[pos:m.end()].strip());pos=m.end()
 text='\n\n'.join(ps)
 url=f'https://stotranidhi.com/{["kn","hi","en"][i]}/lakshmi-narasimha-karavalamba-stotram-in-{["kannada","sanskrit","english"][i]}/'
 versions.append(dict(id='roman' if sc=='english' else sc,lang=lang,label=label,title=[s['title'],'श्रीलक्ष्मीनृसिंहकरावलम्बस्तोत्रम्',s['title_en']][i],chapters=[ch('main',['ಪ್ರಕಟಿತ ಪೂರ್ಣ ಪಾಠ — ೨೫ ಶ್ಲೋಕಗಳು','प्रकाशितपाठः — २५ श्लोकाः','Shared edition — 25 verses'][i],ps,layout='verses')],references=[dict(label='Stotra Nidhi — shared 25-verse edition',url=url)],source_sha256=hashlib.sha256(text.encode()).hexdigest()))
(ROOT/'data/texts'/f'{s["slug"]}.json').write_text(json.dumps(dict(versions=versions),ensure_ascii=False,indent=2)+'\n')
s['published_edition']='stotra-nidhi-25';s['preserve_original_transcription']=True
s['note']='ಹಂಚಿದ ಸ್ತೋತ್ರನಿಧಿ ಮೂಲದ ೨೫ ಶ್ಲೋಕಗಳ ಪೂರ್ಣ ಪಾಠವನ್ನು ಮೂರು ಲಿಪಿಗಳಲ್ಲಿ ನೀಡಲಾಗಿದೆ. ಕುಟುಂಬದ ಪುಸ್ತಕದ ೧೭ ಶ್ಲೋಕಗಳ ಕನ್ನಡ ಪಾಠ ಮತ್ತು ಮೂಲ ಚಿತ್ರಗಳನ್ನು ಕೆಳಗೆ ಪ್ರತ್ಯೇಕವಾಗಿ ಉಳಿಸಲಾಗಿದೆ.'
s['note_en']='The shared Stotra Nidhi link has a 25-verse edition, provided here in all three scripts. Dad’s original 17-verse Kannada book reading and scans are preserved separately below; the editions are not silently blended. Source pipe punctuation is displayed as danda marks.'
(ROOT/'data/songs.json').write_text(json.dumps(songs,ensure_ascii=False,indent=2)+'\n')

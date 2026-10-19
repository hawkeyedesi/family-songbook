"""Visible, conservative source-check results, pinned to the actual reading hashes."""
from pathlib import Path
from html import escape as e
import json,hashlib
ROOT=Path(__file__).resolve().parent
AUDIT=json.loads((ROOT/'data/sringeri-audit.json').read_text())
BY={x['slug']:x for x in AUDIT['works']}
LABELS={'sringeri-edition':('ಶೃಂಗೇರಿ ಮುಖ್ಯ ಪಾಠ','Sringeri primary edition'),'differences':('ಮೂಲ ಪಾಠದಲ್ಲಿ ವ್ಯತ್ಯಾಸಗಳಿವೆ','Compared — readings differ'),'not-located':('ಶೃಂಗೇರಿ ಪಾಠ ಇನ್ನೂ ಸಿಕ್ಕಿಲ್ಲ','Not yet Sringeri-verified')}
def validate(songs):
 assert set(BY)=={s['slug'] for s in songs}
 for s in songs:
  r=BY[s['slug']];vs=json.loads((ROOT/'data'/s['versions_file']).read_text())['versions']
  assert r['current_text_hashes']=={v['id']:v['source_sha256'] for v in vs},'Stale source audit: rerun scripts/audit_sringeri.py'
  if r.get('source_snapshot'):assert hashlib.sha256((ROOT/r['source_snapshot']).read_bytes()).hexdigest()==r['source_sha256']
 assert BY['durga-saptashloki']['differences']==[] and BY['durga-saptashloki']['units_compared']==7

def badge(s,ui,prefix):
 r=BY[s['slug']];label=LABELS[r['status']][ui=='en'];target=prefix+('en/' if ui=='en' else '')+'source-checks/#'+s['slug']
 return f'<aside class="source-check {r["status"]}"><a href="{target}">{e(label)} ↗</a><span> · 2026-10-19 · Sringeri</span></aside>'

def render(ui,prefix):
 en=ui=='en';parts=[]
 for r in AUDIT['works']:
  detail=''
  if r.get('differences'):
   detail='<details><summary>'+('Compare previous edition with Sringeri (Devanagari)' if en else 'ಹೋಲಿಸಿದ ಪಾಠಗಳು (ದೇವನಾಗರಿ)')+'</summary>'
   for d in r['differences']:
    detail+=f'<section class="audit-difference"><h4>{"Verse / name" if en else "ಶ್ಲೋಕ / ನಾಮ"} {d["unit"]}</h4><p><b>Previous edition:</b><br>{"<br>".join(e(x) for x in d["collection"].splitlines())}</p><p><b>Sringeri displayed text:</b><br>{"<br>".join(e(x) for x in d["sringeri_display"].splitlines())}</p></section>'
   detail+='</details>'
  suffix='roman/' if en else ''
  counts=(f'<p>{r["units_compared"]} previous-edition units compared; {r["units_matching_normalized"]} agree under the stated normalization.</p>' if 'units_compared' in r else '')
  parts.append(f'<section class="audit-work" id="{r["slug"]}"><h2><a href="{prefix}songs/{r["slug"]}/{suffix}">{e(r["title"])}</a></h2><strong>{LABELS[r["status"]][en]}</strong><p>{e(r["note"])}</p>{counts}<p><a href="{e(r["source_url"])}" target="_blank" rel="noopener">Sringeri source ↗</a></p>{detail}</section>')
 title='Sringeri source checks' if en else 'ಶೃಂಗೇರಿ ಮೂಲಪಾಠ ಪರಿಶೀಲನೆ'
 return title, f'''<h1>{title}</h1><p>2026-10-19 · 33 works checked against the complete 17-category official Stotras catalog. Eight corresponding texts now use Sringeri’s displayed reading as the primary edition in all three scripts, by explicit family choice. Previous readings and scans are retained separately. Twenty-five full texts were not located in that catalog and remain clearly unverified against Sringeri.</p><p>The checked Sanskrit/IAST reading is the textual witness. Kannada and Roman renderings are not independent authorities. Vedic accent checks remain tied to each cited marked source; absence from Sringeri is not accent verification.</p><p>Differences include valid traditional variants, family additions, punctuation and apparent website transcription issues. Sringeri is the chosen primary authority; its spellings are retained faithfully, even where the site appears internally inconsistent. Previous family editions remain separately accessible, not merged into the chanting text. Original family scans and nine transcriptions remain unchanged. Among the differences resolved by using Sringeri’s edition are Krishna verse 8 <span lang="sa">यथा → यदा</span>, and Kalabhairava verse 2 <span lang="sa">भवब्धि → भवाब्धि</span>.</p><p>Comparison normalization: Unicode NFC; ignore punctuation, whitespace and verse numerals; normalize avagraha punctuation. Vowel lengths, consonants and pitch marks are not discarded. Alternatives printed inside a verse are retained and may produce a comparison difference. Karavalamba’s differing-length editions are compared positionally, not asserted to be one-to-one.</p><p><a href="{prefix}data/sringeri-audit.json">Download exact checks and source hashes</a> · <a href="{prefix}data/sringeri/before-krishna-ashtakam.json">Previous Krishna reading</a> · <a href="{prefix}data/sringeri/before-kalabhairava-ashtakam.json">Previous Kalabhairava reading</a></p>{''.join(parts)}'''

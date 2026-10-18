"""Static, progressively enhanced family recording page; no service/runtime dependency."""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parent

def render(ui,prefix,songs,render_chapter):
 en=ui=='en';r=json.loads((ROOT/'data/navaratri-recording.json').read_text())
 by={s['slug']:s for s in songs};s=by[r['defaultWork']]
 vs=json.loads((ROOT/'data'/s['versions_file']).read_text())['versions'];v=vs[2 if en else 0]
 def url(slug,script):return prefix+'songs/'+slug+'/'+('' if script=='kannada' else script+'/')
 def label(c):return c.get('label_en',c['label']) if en else c['label']
 sections=[]
 for cue in r['cues']:
  m,sec=divmod(int(cue['start']),60)
  sections.append(f'<li><button type="button" data-cue="{e(cue["id"])}"><span class="cue-time">{m:02}:{sec:02}</span><span>{e(label(cue))}</span></button></li>')
 parts=[*r.get('preludes',[]),{k:v for k,v in r.items() if k!='preludes'}]
 sources=list(dict.fromkeys([r['defaultWork']]+[c['work'] for part in parts for c in part['cues'] if c.get('work')]+[s['slug'] for s in songs if 'navaratri' in s.get('tags',[])]))
 options=''.join(f'<option value="{slug}">{e(by[slug].get("title_en",by[slug]["title"]) if en else by[slug]["title"])}</option>' for slug in sources)
 links=''.join(f'<a data-reader-script="{w["id"]}" href="{url(s["slug"],w["id"])}" {"aria-current=page" if v["id"]==w["id"] else ""}>{e(w["label"])}</a>' for w in vs)
 config={**r,'parts':parts,'base':prefix,'ui':ui,'script':v['id'],'labels':{
  'loading':'Loading the recording…' if en else 'ಧ್ವನಿಮುದ್ರಿಕೆಯನ್ನು ತೆರೆಯಲಾಗುತ್ತಿದೆ…',
  'ready':'Recording ready. Press Play to begin.' if en else 'ಧ್ವನಿಮುದ್ರಿಕೆ ಸಿದ್ಧವಾಗಿದೆ. ಆರಂಭಿಸಲು Play ಒತ್ತಿ.',
  'error':'The embedded player could not play here. Open the recording on YouTube; the texts still work below.' if en else 'ಇಲ್ಲಿ ಪ್ಲೇಯರ್ ತೆರೆಯಲಿಲ್ಲ. ಧ್ವನಿಮುದ್ರಿಕೆಯನ್ನು YouTubeನಲ್ಲಿ ತೆರೆಯಿರಿ; ಪಠ್ಯಗಳನ್ನು ಕೆಳಗೆ ಓದಬಹುದು.',
  'textLoading':'Loading text…' if en else 'ಪಠ್ಯವನ್ನು ತೆರೆಯಲಾಗುತ್ತಿದೆ…',
  'textError':'Text could not load. Use the full-text link below.' if en else 'ಪಠ್ಯ ತೆರೆಯಲಿಲ್ಲ. ಕೆಳಗಿನ ಪೂರ್ಣ ಪಾಠದ ಲಿಂಕ್ ಬಳಸಿ.',
  'unmapped':'This passage is not text-matched yet. Keep listening, or choose a text manually.' if en else 'ಈ ಭಾಗಕ್ಕೆ ಪಠ್ಯವನ್ನು ಇನ್ನೂ ಜೋಡಿಸಿಲ್ಲ. ಆಲಿಸಿ ಅಥವಾ ಪಠ್ಯವನ್ನು ಆಯ್ಕೆಮಾಡಿ.',
  'manual':'Manual reading — turn Follow recording on to rejoin.' if en else 'ಆಯ್ದ ಪಠ್ಯ — ಮತ್ತೆ ಅನುಸರಿಸಲು ಧ್ವನಿಮುದ್ರಿಕೆ ಅನುಸರಿಸಿ ಆಯ್ಕೆಮಾಡಿ.',
 }}
 part_buttons=''.join(f'<button type="button" data-recording-part="{i}" '+('aria-current="true"' if part['videoId']==r['videoId'] else '')+f'>{i+1}. {e(part.get("label_en","Lalitha puja") if en else part.get("label","ಲಲಿತಾ ಪೂಜೆ"))}</button>' for i,part in enumerate(parts))
 part_sources=''.join(f'<li><a href="{e(part["sourceUrl"])}" target="_blank" rel="noopener">{e(part.get("label_en","Lalitha puja") if en else part.get("label","ಲಲಿತಾ ಪೂಜೆ"))} ↗</a></li>' for part in parts)
 encoded=json.dumps(config,ensure_ascii=False).replace('<','\\u003c')
 title='Grandpa’s Navaratri recording' if en else 'ತಾತನ ನವರಾತ್ರಿ ಧ್ವನಿಮುದ್ರಿಕೆ'
 credit=(f'Lalitha recording: chanted by {r["reciter"]}. Recorded by {r["recorder"]} in {r["year"]}, {r["location"]}.' if en else 'ಲಲಿತಾ ಧ್ವನಿಮುದ್ರಿಕೆ: ದೇವನಹಳ್ಳಿ ನಾಗರಾಜ ಶಾಸ್ತ್ರಿಗಳ ಪಠಣ. ದಿವಂಗತ ಎಚ್. ಜಿ. ನಾರಾಯಣ ಅವರ ಧ್ವನಿಮುದ್ರಿಕೆ — ೧೯೮೩, ಜಯನಗರ, ಬೆಂಗಳೂರು.')
 intro=('A family tradition, kept in its original voice. Play the recording and read along in your preferred script.' if en else 'ಕುಟುಂಬದ ಸಂಪ್ರದಾಯ, ಮೂಲ ಧ್ವನಿಯಲ್ಲೇ. ಧ್ವನಿಮುದ್ರಿಕೆಯನ್ನು ಆಲಿಸುತ್ತಾ ನಿಮಗೆ ಬೇಕಾದ ಲಿಪಿಯಲ್ಲಿ ಓದಿ.')
 return f'''<section class="recording" id="navaratri-recording"><div class="recording-heading"><span class="eyebrow">1983 · {'FAMILY ARCHIVE' if en else 'ಕುಟುಂಬದ ಸಂಗ್ರಹ'}</span><h2>{title}</h2><p>{intro}</p><p class="recording-credit">{e(credit)}</p></div>
<nav class="recording-parts" aria-label="Puja recording order">{part_buttons}</nav><details class="recording-originals"><summary>{"Original recordings, in puja order" if en else "ಪೂಜೆಯ ಕ್ರಮದಲ್ಲಿ ಮೂಲ ಧ್ವನಿಮುದ್ರಿಕೆಗಳು"}</summary><ol>{part_sources}</ol></details><div class="recording-layout"><div class="recording-listen"><div class="recording-player" id="nav-player"><button type="button" id="load-recording">▶ {'Start puja: Ganapathy → Lalitha' if en else 'ಪೂಜೆ ಆರಂಭಿಸಿ: ಗಣಪತಿ → ಲಲಿತಾ'}</button><p>{'The YouTube player loads only when you press this button.' if en else 'ಈ ಗುಂಡಿ ಒತ್ತಿದಾಗ ಮಾತ್ರ YouTube ಪ್ಲೇಯರ್ ತೆರೆಯುತ್ತದೆ.'}</p></div><p id="player-status" role="status" aria-live="polite"></p><a class="recording-external" href="{r['sourceUrl']}" target="_blank" rel="noopener">{'Open original on YouTube ↗' if en else 'ಮೂಲ ಧ್ವನಿಮುದ್ರಿಕೆಯನ್ನು YouTubeನಲ್ಲಿ ತೆರೆಯಿರಿ ↗'}</a>
<label class="follow-toggle"><input type="checkbox" id="follow-recording" checked> {'Follow the recording' if en else 'ಧ್ವನಿಮುದ್ರಿಕೆಯನ್ನು ಅನುಸರಿಸಿ'}</label><p class="timing-note">{'Text changes at the matched section boundaries. Timings are approximate section starts, not syllable-by-syllable karaoke.' if en else 'ಜೋಡಿಸಿದ ಭಾಗಗಳ ಆರಂಭದಲ್ಲಿ ಪಠ್ಯ ಬದಲಾಗುತ್ತದೆ; ಇದು ಅಕ್ಷರಕ್ಕಕ್ಷರ ಜೋಡಣೆಯಲ್ಲ.'}</p><details class="recording-jump"><summary>{'Jump to a recording section' if en else 'ಧ್ವನಿಮುದ್ರಿಕೆಯ ಭಾಗಕ್ಕೆ ಹೋಗಿ'}</summary><ol class="recording-sequence" id="recording-sequence">{''.join(sections)}</ol></details><noscript><p>{'Playing and reading the full texts works without JavaScript; automatic following needs JavaScript.' if en else 'ಪೂರ್ಣ ಪಠ್ಯಗಳನ್ನು ಲಿಂಕ್‌ಗಳಿಂದ ಓದಬಹುದು. ಸ್ವಯಂಚಾಲಿತ ಜೋಡಣೆಗೆ JavaScript ಬೇಕು.'}</p></noscript></div>
<div class="recording-reading"><label for="recording-work">{'Choose a text' if en else 'ಪಠ್ಯ ಆಯ್ಕೆಮಾಡಿ'}</label><select id="recording-work">{options}</select><nav class="script-switch" aria-label="Recording reading script">{links}</nav><p id="reading-status" role="status" aria-live="polite"></p><div class="recording-text-tools"><button type="button" id="nav-text-smaller" aria-label="Smaller reading text">A−</button><button type="button" id="nav-text-larger" aria-label="Larger reading text">A+</button><span id="current-recording-time">00:00 / 41:15</span></div><h3 id="recording-text-title">{e(v['title'])}</h3><p class="recording-cue-label" id="active-recording-cue"></p><div class="recording-scroll" id="recording-scroll"><article class="lyrics multilingual {v['id']}" lang="{v['lang']}" id="recording-text">{''.join(render_chapter(c) for c in v['chapters'])}</article></div><a id="recording-full-text" href="{url(s['slug'],v['id'])}">{'Open full text & sources ↗' if en else 'ಪೂರ್ಣ ಪಾಠ ಮತ್ತು ಮೂಲಗಳು ↗'}</a></div></div>
<script type="application/json" id="recording-config">{encoded}</script><script defer src="{prefix}assets/navaratri.js"></script></section>'''

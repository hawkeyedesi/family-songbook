"""Family-owned native-audio archive: no third-party player or Drive dependency."""
from pathlib import Path
from html import escape as e
import json
ROOT=Path(__file__).resolve().parent

def clock(seconds):
 m,s=divmod(int(seconds),60);return f'{m:02}:{s:02}'
def load():return json.loads((ROOT/'data/kamalamma-ajji.json').read_text())
def text_url(text,script,prefix):return prefix+text['path']+('' if script=='kannada' else script+'/')
def render(ui,prefix):
 r=load();en=ui=='en';script='roman' if en else 'kannada';texts={t['id']:t for t in r['texts']};cards=[]
 for i,track in enumerate(r['recordings']):
  cues=[]
  for cue in track['cues']:
   text=texts.get(cue.get('text'));title=cue.get('title_en') if en else cue.get('title')
   title=title or (text['title_en'] if en else text['title']) if text else (title or ('Unmatched passage' if en else 'ಪಾಠವನ್ನು ಇನ್ನೂ ಜೋಡಿಸಿಲ್ಲ'))
   dest=text_url(text,script,prefix) if text else prefix+track['path']+f'#t={cue["start"]}'
   link=f'<a href="{dest}" data-cue-track="{i}" data-cue-id="{cue["id"]}">{clock(cue["start"])} · {e(title)}</a>'
   cues.append('<li>'+link+'</li>')
  src=prefix+track['path']
  cards.append(f'''<section class="ajji-track" id="{track['id']}"><div class="ajji-track-heading"><h3><a data-ajji-track="{i}" href="{src}">{'Recording' if en else 'ಧ್ವನಿಮುದ್ರಿಕೆ'} {i+1} · {clock(track['duration'])}</a></h3><a href="{src}" download="{e(track['filename'])}">{'Download original MP3' if en else 'ಮೂಲ MP3 ಇಳಿಸಿ'} ↓</a></div><p>{e(track['filename'])} · {track['bytes']/1_000_000:.1f} MB</p><ol class="ajji-cues">{''.join(cues)}</ol></section>''')
 config={**r,'base':prefix,'script':script,'ui':ui}
 encoded=json.dumps(config,ensure_ascii=False).replace('<','\\u003c')
 labels=[('kannada','ಕನ್ನಡ'),('devanagari','देवनागरी'),('roman','English (Roman)')]
 # A complete native audio player is usable before JS. All six original file links
 # and source-text pages remain ordinary links when JS or a fetch fails.
 switch='<nav class="script-switch" aria-label="Recording reading script">'+''.join(f'<button type="button" data-ajji-script="{sid}" '+('aria-pressed="true"' if sid==script else 'aria-pressed="false"')+f'>{label}</button>' for sid,label in labels)+'</nav>'
 home=prefix+('en/' if en else '')
 toggle='<nav class="language-switch"><a href="'+prefix+'kamalamma-ajji/">ಕನ್ನಡ</a><a href="'+prefix+'en/kamalamma-ajji/">English (Roman)</a></nav>'
 title='Kamalamma Ajji' if en else 'ಕಮಲಮ್ಮ ಅಜ್ಜಿ'
 return title,f'''<nav class="back"><a href="{home}">← {'The songbook' if en else 'ಭಕ್ತಿ ಸಂಗ್ರಹ'}</a></nav>{toggle}<section class="intro ajji-intro"><span class="eyebrow">{'FAMILY VOICES' if en else 'ಕುಟುಂಬದ ಧ್ವನಿಗಳು'}</span><h1>{title}</h1><p>{'Her voice. Our family’s bhajans.' if en else 'ಅಜ್ಜಿಯ ಧ್ವನಿ. ನಮ್ಮ ಕುಟುಂಬದ ಭಜನೆಗಳು.'}</p><p class="ajji-description">{'Six original recordings, preserved here for the family. Listen in sequence or jump to a bhajan and read in your preferred script.' if en else 'ಕುಟುಂಬಕ್ಕಾಗಿ ಇಲ್ಲಿ ಉಳಿಸಿರುವ ಆರು ಮೂಲ ಧ್ವನಿಮುದ್ರಿಕೆಗಳು. ಕ್ರಮವಾಗಿ ಆಲಿಸಿ ಅಥವಾ ಭಜನೆಯ ಭಾಗಕ್ಕೆ ಹೋಗಿ ನಿಮ್ಮ ಲಿಪಿಯಲ್ಲಿ ಓದಿ.'}</p><p>{len(r['recordings'])} {'recordings' if en else 'ಧ್ವನಿಮುದ್ರಿಕೆಗಳು'} · {clock(sum(t['duration'] for t in r['recordings']))} · {'Original MP3s hosted with this website, not streamed from Google Drive.' if en else 'ಮೂಲ MP3ಗಳು ಈ ತಾಣದಲ್ಲೇ ಇವೆ; Google Drive ಅವಲಂಬನೆ ಇಲ್ಲ.'}</p></section>
<div class="ajji-layout"><section class="ajji-listen"><h2>{'Listen to Ajji' if en else 'ಅಜ್ಜಿಯ ಪಠಣ ಆಲಿಸಿ'}</h2><p id="ajji-track-title">{'Recording 1' if en else 'ಧ್ವನಿಮುದ್ರಿಕೆ ೧'}</p><audio id="ajji-player" controls preload="none" src="{prefix}{r['recordings'][0]['path']}"><a href="{prefix}{r['recordings'][0]['path']}">MP3</a></audio><div class="ajji-controls"><button type="button" id="ajji-prev">← {'Previous' if en else 'ಹಿಂದಿನದು'}</button><button type="button" id="ajji-next">{'Next' if en else 'ಮುಂದಿನದು'} →</button></div><label class="follow-toggle"><input type="checkbox" id="ajji-autonext" checked> {'Continue to the next recording' if en else 'ಮುಂದಿನ ಧ್ವನಿಮುದ್ರಿಕೆಯನ್ನು ಆಲಿಸಿ'}</label><p id="ajji-play-status" role="status" aria-live="polite"></p><noscript><p>{'The player above plays recording 1. Open any original MP3 or reading below; synchronized following needs JavaScript.' if en else 'ಮೇಲಿನ ಪ್ಲೇಯರ್ ಮೊದಲ ಧ್ವನಿಮುದ್ರಿಕೆಗೆ. ಕೆಳಗಿನ MP3 ಮತ್ತು ಪಾಠದ ಲಿಂಕ್‌ಗಳು JavaScript ಇಲ್ಲದೆ ಕೆಲಸ ಮಾಡುತ್ತವೆ.'}</p></noscript><details class="ajji-recordings"><summary>{'Choose a recording or bhajan' if en else 'ಧ್ವನಿಮುದ್ರಿಕೆ ಅಥವಾ ಭಜನೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ'}</summary>{''.join(cards)}</details></section>
<section class="ajji-reading" aria-label="Read along"><h2>{'Read along' if en else 'ಜೊತೆಯಲ್ಲಿ ಓದಿ'}</h2>{switch}<label class="follow-toggle"><input type="checkbox" id="ajji-follow" checked> {'Follow the recording' if en else 'ಧ್ವನಿಮುದ್ರಿಕೆಯನ್ನು ಅನುಸರಿಸಿ'}</label><p id="ajji-reading-status" role="status" aria-live="polite">{'Choose a bhajan below or start the recording. Texts follow matched sections; uncertain passages are labelled, never guessed.' if en else 'ಭಜನೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ ಅಥವಾ ಧ್ವನಿಮುದ್ರಿಕೆಯನ್ನು ಆಲಿಸಿ. ಖಚಿತವಾಗಿ ಜೋಡಿಸಿದ ಭಾಗಗಳ ಪಾಠ ಮಾತ್ರ ತೋರಿಸಲಾಗುತ್ತದೆ.'}</p><h3 id="ajji-text-title"></h3><p id="ajji-text-note"></p><div class="recording-scroll" id="ajji-scroll"><article class="lyrics multilingual" id="ajji-text" hidden></article></div><p><a id="ajji-full-text" hidden>{'Full text and sources ↗' if en else 'ಪೂರ್ಣ ಪಾಠ ಮತ್ತು ಮೂಲಗಳು ↗'}</a></p><p class="timing-note">{'Section starts are approximate, not word-by-word karaoke. Kannada songs remain Kannada in each script; Devanagari is not a Sanskrit translation. The recording is the authority for Ajji’s sung order and repetitions.' if en else 'ಭಾಗಗಳ ಸಮಯ ಅಂದಾಜು; ಅಕ್ಷರಕ್ಕಕ್ಷರ ಜೋಡಣೆಯಲ್ಲ. ಕನ್ನಡ ಭಜನೆಗಳ ದೇವನಾಗರಿ ಲಿಪಿ ಸಂಸ್ಕೃತ ಅನುವಾದವಲ್ಲ. ಹಾಡಿನ ಕ್ರಮ ಮತ್ತು ಪುನರಾವರ್ತನೆಗೆ ಅಜ್ಜಿಯ ಧ್ವನಿಯೇ ಆಧಾರ.'}</p></section></div>
<details class="archive-notes"><summary>{'Preservation and text notes' if en else 'ಸಂಗ್ರಹ ಮತ್ತು ಪಾಠದ ವಿವರಗಳು'}</summary><p>{'Original filenames and all audio bytes are retained. Upload and file-modification dates are not treated as recording dates. Source links and any uncertain readings appear with each text. Five forwarded WhatsApp files were byte-for-byte identical to the Drive originals and were not duplicated. No phone number is published.' if en else 'ಮೂಲ ಕಡತಗಳ ಹೆಸರು ಮತ್ತು ಎಲ್ಲ ಧ್ವನಿಯನ್ನು ಉಳಿಸಲಾಗಿದೆ. ಕಡತಗಳ ದಿನಾಂಕವನ್ನು ಧ್ವನಿಮುದ್ರಿಕೆಯ ದಿನಾಂಕವೆಂದು ಪರಿಗಣಿಸಿಲ್ಲ. ಮೂಲ ಮತ್ತು ಅನಿಶ್ಚಿತ ಪಾಠಗಳನ್ನು ಪ್ರತ್ಯೇಕವಾಗಿ ಸೂಚಿಸಲಾಗಿದೆ.'}</p><a href="{prefix}data/kamalamma-ajji.json">{'Audio manifest and checksums' if en else 'ಧ್ವನಿಮುದ್ರಿಕೆಗಳ ಪಟ್ಟಿ ಮತ್ತು ಪರಿಶೀಲನಾ ಗುರುತುಗಳು'}</a></details><script type="application/json" id="ajji-config">{encoded}</script><script defer src="{prefix}assets/kamalamma.js"></script>'''

def render_texts(shell,render_chapter):
 r=load()
 for t in r['texts']:
  if not t.get('versions_file'):continue
  bundle=json.loads((ROOT/'data'/t['versions_file']).read_text())
  for v in bundle['versions']:
   vid=v['id'];en=vid!='kannada';prefix='../../../../' if en else '../../../';ui='en' if en else 'kn';base='../' if en else './'
   switch='<nav class="script-switch" aria-label="Choose reading script">'+''.join(f'<a href="{base}{"" if w["id"]=="kannada" else w["id"]+"/"}" data-script="{w["id"]}" '+('aria-current="page"' if w['id']==vid else '')+f'>{e(w["label"])}</a>' for w in bundle['versions'])+'</nav>'
   refs='<ul>'+''.join(f'<li><a href="{e(x["url"])}" target="_blank" rel="noopener">{e(x["label"])}</a></li>' for x in v['references'])+'</ul>'
   body=f'<nav class="back"><a href="{prefix}{"en/" if en else ""}kamalamma-ajji/">← Kamalamma Ajji</a></nav><h1>{e(v["title"])}</h1>{switch}<aside class="reading-notice">{e(t.get("note_en", "Published text matched to the identified bhajan; repetitions follow the recording."))}</aside><article class="lyrics multilingual {vid}" lang="{v["lang"]}" aria-label="Prayer text">'+''.join(render_chapter(c) for c in v['chapters'])+'</article><section class="source"><h2>Sources</h2>'+refs+'</section>'
   target=ROOT/t['path']/('' if vid=='kannada' else vid)/'index.html';target.parent.mkdir(parents=True,exist_ok=True);target.write_text(shell(v['title'],'Kamalamma Ajji — bhajan reading',body,prefix,v['lang'],ui))

/* Native MP3s are the source clock. Text requests never restart the recording. */
(() => {
 const configNode=document.querySelector('#ajji-config');if(!configNode)return;
 const config=JSON.parse(configNode.textContent),audio=document.querySelector('#ajji-player');
 const records=config.recordings,texts=new Map(config.texts.map(t=>[t.id,t]));
 const title=document.querySelector('#ajji-track-title'),playStatus=document.querySelector('#ajji-play-status');
 const status=document.querySelector('#ajji-reading-status'),text=document.querySelector('#ajji-text');
 const scroll=document.querySelector('#ajji-scroll'),full=document.querySelector('#ajji-full-text');
 const heading=document.querySelector('#ajji-text-title'),note=document.querySelector('#ajji-text-note');
 const follow=document.querySelector('#ajji-follow'),autonext=document.querySelector('#ajji-autonext');
 const scripts=[...document.querySelectorAll('[data-ajji-script]')],cache=new Map();
 let index=0,script=config.script,currentCue=null,currentText=null,request=0,pendingSeek=null,started=false;
 const url=(path)=>new URL(config.base+path,location.href).href;
 const textURL=(t,s)=>url(t.path+(s==='kannada'?'':s+'/'));
 const label=(t)=>config.ui==='en'?t.title_en:t.title;
 const findCue=(track,time)=>track.cues.find(c=>time>=c.start&&time<c.end)||null;
 function preferred(){try{return localStorage.getItem('bhakti-script')}catch{return null}}
 if(['kannada','devanagari','roman'].includes(preferred()))script=preferred();
 function scriptState(){for(const b of scripts)b.setAttribute('aria-pressed',String(b.dataset.ajjiScript===script))}
 function highlight(anchor){
  for(const el of text.querySelectorAll('.recording-current-line'))el.classList.remove('recording-current-line');
  if(!anchor)return;
  const el=text.querySelector('#'+CSS.escape(anchor));if(!el)return;
  el.classList.add('recording-current-line');scroll.scrollTop+=el.getBoundingClientRect().top-scroll.getBoundingClientRect().top-18;
 }
 function visibleAnchor(){return [...text.querySelectorAll('[data-verse], [data-name], .text-chapter')].find(el=>el.getBoundingClientRect().bottom>scroll.getBoundingClientRect().top+18)?.id}
 async function read(id,anchor=null){
  const entry=texts.get(id);if(!entry)return;
  const token=++request;currentText=id;text.hidden=true;full.hidden=false;full.href=textURL(entry,script);
  heading.textContent=label(entry);note.textContent=config.ui==='en'?(entry.note_en||''):(entry.note||entry.note_en||'');
  status.textContent=config.ui==='en'?'Loading reading…':'ಪಾಠ ತೆರೆಯಲಾಗುತ್ತಿದೆ…';
  try{
   const dest=textURL(entry,script);
   if(!cache.has(dest)){
    const response=await fetch(dest);if(!response.ok)throw Error('Reading unavailable');
    const doc=new DOMParser().parseFromString(await response.text(),'text/html'),article=doc.querySelector('article.lyrics');
    if(!article)throw Error('Reading missing');
    cache.set(dest,{article,notices:[...doc.querySelectorAll('.reading-notice,.svara-notice,.svara-key')]});
   }
   if(token!==request)return;
   const content=cache.get(dest);text.replaceChildren(...content.notices.map(n=>n.cloneNode(true)),...[...content.article.childNodes].map(n=>n.cloneNode(true)));
   text.className=content.article.className;text.lang=content.article.lang;text.hidden=false;status.textContent='';highlight(anchor);
  }catch{if(token===request){text.hidden=true;status.textContent=config.ui==='en'?'Reading could not load. Open the full-text link below; audio continues.':'ಪಾಠ ತೆರೆಯಲಿಲ್ಲ. ಪೂರ್ಣ ಪಾಠದ ಲಿಂಕ್ ಬಳಸಿ; ಧ್ವನಿ ಮುಂದುವರಿಯುತ್ತದೆ.'}}
 }
 function unmatched(cue){
  ++request;text.hidden=true;full.hidden=true;currentText=null;
  heading.textContent=cue?label(cue)||'':'';note.textContent='';
  status.textContent=config.ui==='en'?'This passage is preserved in the audio but has no securely matched text yet. We have not guessed its words.':'ಈ ಭಾಗದ ಧ್ವನಿ ಉಳಿಸಲಾಗಿದೆ; ಖಚಿತ ಪಾಠ ಇನ್ನೂ ಜೋಡಿಸಿಲ್ಲ. ಊಹಿಸಿ ಪದಗಳನ್ನು ಸೇರಿಸಿಲ್ಲ.';
 }
 function sync(force=false){
  if(!started||!follow.checked)return;
  const cue=findCue(records[index],audio.currentTime);
  if(!force&&cue?.id===currentCue?.id)return;
  currentCue=cue;
  for(const a of document.querySelectorAll('[data-cue-id]'))a.setAttribute('aria-current',String(Number(a.dataset.cueTrack)===index&&a.dataset.cueId===cue?.id));
  if(!cue?.text){unmatched(cue);return}
  if(currentText!==cue.text||text.hidden||force)read(cue.text,cue.anchor);
  else highlight(cue.anchor);
 }
 function applySeek(){
  if(pendingSeek===null)return;
  if(pendingSeek>0&&!Array.from({length:audio.seekable.length},(_,i)=>[audio.seekable.start(i),audio.seekable.end(i)]).some(([a,b])=>pendingSeek>=a&&pendingSeek<=b))return;
  try{const target=pendingSeek;audio.currentTime=target;if(Math.abs(audio.currentTime-target)<.5)pendingSeek=null;sync(true)}catch{}
 }
 function selectTrack(n,start=0,play=true){
  if(n<0||n>=records.length)return;
  const changed=index!==n||audio.src!==url(records[n].path);index=n;started=true;currentCue=null;pendingSeek=start;follow.checked=true;
  title.textContent=`${config.ui==='en'?'Recording':'ಧ್ವನಿಮುದ್ರಿಕೆ'} ${index+1} · ${records[index].filename}`;
  document.querySelector('#ajji-prev').disabled=index===0;document.querySelector('#ajji-next').disabled=index===records.length-1;
  for(const a of document.querySelectorAll('[data-ajji-track]'))a.setAttribute('aria-current',String(Number(a.dataset.ajjiTrack)===index));
  if(changed){audio.src=url(records[index].path);audio.load()}
  if(audio.readyState>=1)applySeek();
  else{
   const cue=findCue(records[index],start);if(cue?.text)read(cue.text,cue.anchor);else unmatched(cue);
  }
  if(play)audio.play().catch(()=>{playStatus.textContent=config.ui==='en'?'Press Play to continue.':'ಮುಂದುವರಿಯಲು Play ಒತ್ತಿ.'});
 }
 for(const a of document.querySelectorAll('[data-ajji-track]'))a.addEventListener('click',e=>{e.preventDefault();selectTrack(Number(a.dataset.ajjiTrack))});
 for(const a of document.querySelectorAll('[data-cue-id]'))a.addEventListener('click',e=>{
  e.preventDefault();const n=Number(a.dataset.cueTrack),cue=records[n].cues.find(c=>c.id===a.dataset.cueId);selectTrack(n,cue.start);
 });
 for(const b of scripts)b.addEventListener('click',()=>{
  const anchor=visibleAnchor();script=b.dataset.ajjiScript;scriptState();try{localStorage.setItem('bhakti-script',script)}catch{}
  if(currentText)read(currentText,anchor||currentCue?.anchor);
  for(const a of document.querySelectorAll('[data-cue-id]')){
   const cue=records[Number(a.dataset.cueTrack)].cues.find(c=>c.id===a.dataset.cueId);if(cue?.text)a.href=textURL(texts.get(cue.text),script);
  }
 });
 audio.addEventListener('loadedmetadata',applySeek);audio.addEventListener('progress',applySeek);audio.addEventListener('canplay',applySeek);audio.addEventListener('timeupdate',()=>sync());audio.addEventListener('seeked',()=>sync(true));
 audio.addEventListener('play',()=>{started=true;playStatus.textContent='';sync(true)});
 audio.addEventListener('ended',()=>{if(autonext.checked&&index<records.length-1)selectTrack(index+1);else{currentCue=null;unmatched(null);status.textContent=config.ui==='en'?'Recording finished.':'ಧ್ವನಿಮುದ್ರಿಕೆ ಮುಗಿದಿದೆ.'}});
 audio.addEventListener('error',()=>{playStatus.textContent=config.ui==='en'?'Audio could not load. Use the original MP3 link below.':'ಧ್ವನಿ ತೆರೆಯಲಿಲ್ಲ. ಕೆಳಗಿನ ಮೂಲ MP3 ಲಿಂಕ್ ಬಳಸಿ.'});
 follow.addEventListener('change',()=>{if(follow.checked)sync(true);else status.textContent=config.ui==='en'?'Manual reading — turn Follow on to rejoin.':'ಆಯ್ದ ಪಾಠ — ಮತ್ತೆ ಅನುಸರಿಸಲು ಆಯ್ಕೆಮಾಡಿ.'});
 document.querySelector('#ajji-prev').addEventListener('click',()=>selectTrack(index-1));document.querySelector('#ajji-next').addEventListener('click',()=>selectTrack(index+1));document.querySelector('#ajji-prev').disabled=true;
 scriptState();window.KamalammaArchive={config,findCue,sync,selectTrack};
})();

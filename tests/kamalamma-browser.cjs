const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'/Users/kashy/.npm-cache/_npx/420ff84f11983ee5/node_modules/playwright');
const assert=require('node:assert/strict'),fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=path.resolve(__dirname,'..'),base=process.env.BHAKTI_TEST_URL||'http://127.0.0.1:8769/';
(async()=>{
 const cfg=JSON.parse(fs.readFileSync(path.join(root,'data/kamalamma-ajji.json')));
 assert.equal(cfg.recordings.length,6);assert.equal(cfg.texts.length,12);
 for(const t of cfg.recordings){
  const b=fs.readFileSync(path.join(root,t.path));assert.equal(b.length,t.bytes);assert.equal(crypto.createHash('sha256').update(b).digest('hex'),t.sha256);
  assert.equal(t.cues[0].start,0);assert.equal(t.cues.at(-1).end,t.duration);
  t.cues.forEach((c,i)=>{assert(c.end>c.start);if(i)assert.equal(c.start,t.cues[i-1].end);if(c.text)assert(cfg.texts.some(t=>t.id===c.text));});
 }
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const page=await browser.newPage();const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 await page.goto(base+'en/kamalamma-ajji/');await page.waitForFunction(()=>window.KamalammaArchive);
 for(const t of cfg.texts)for(const s of ['','devanagari/','roman/']){
  const p=await browser.newPage();await p.goto(base+t.path+s);assert(await p.locator('article.lyrics').count(),t.id+s);if(t.versions_file)assert(await p.locator('article.lyrics').innerText());await p.close();
 }
 await page.evaluate(()=>{document.querySelector('audio').muted=true;window.KamalammaArchive.selectTrack(0,185,true)});
 await page.waitForFunction(()=>document.querySelector('audio').currentTime>185.3&&!document.querySelector('audio').paused);
 await page.waitForFunction(()=>document.querySelector('#ajji-text-title').textContent==='Lingashtakam'&&!document.querySelector('#ajji-text').hidden);
 const before=await page.locator('audio').evaluate(a=>a.currentTime);
 await page.locator('[data-ajji-script="devanagari"]').click();await page.waitForFunction(()=>document.querySelector('#ajji-text').textContent.includes('ब्रह्ममुरारि'));
 const after=await page.locator('audio').evaluate(a=>a.currentTime);assert(after>=before&&after-before<4,'Script switch restarted/seeks audio');
 await page.evaluate(()=>{const a=document.querySelector('audio');a.pause();a.currentTime=85;window.KamalammaArchive.sync(true)});
 await page.waitForFunction(()=>document.querySelector('#ajji-text').hidden&&document.querySelector('#ajji-reading-status').textContent.includes('no securely matched text'));
 // Native source clock and half-open boundaries, including cross-file continuation.
 await page.evaluate(()=>window.KamalammaArchive.selectTrack(2,0,false));
 await page.waitForFunction(()=>document.querySelector('#ajji-text-title').textContent.includes('Lalitha')&&!document.querySelector('#ajji-text').hidden);
 assert(await page.locator('#ajji-text #names-name-99').count());
 await page.evaluate(()=>window.KamalammaArchive.selectTrack(4,464,false));
 await page.waitForFunction(()=>document.querySelector('#ajji-text-title').textContent==='Ganesha Pancharatnam'&&!document.querySelector('#ajji-text').hidden);
 assert.equal(await page.locator('#ajji-text [data-verse]').count(),6);
 // Automatic continuation is triggered by native ended, not by reading changes.
 await page.evaluate(()=>document.querySelector('audio').dispatchEvent(new Event('ended')));
 await page.waitForFunction(()=>document.querySelector('audio').src.endsWith('amma-06.mp3'));await page.locator('audio').evaluate(a=>a.pause());
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'/tmp/kamalamma-mobile.png',fullPage:true});
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Mobile overflow');
 const nojs=await browser.newContext({javaScriptEnabled:false});const staticPage=await nojs.newPage();await staticPage.goto(base+'en/kamalamma-ajji/');assert.equal(await staticPage.locator('a[download]').count(),6);assert(await staticPage.locator('audio[controls]').count());await nojs.close();
 // A failed reading request must not remove audio access or display stale text.
 const bad=await browser.newPage();await bad.route('**/songs/**',r=>r.abort());await bad.goto(base+'en/kamalamma-ajji/');await bad.evaluate(()=>window.KamalammaArchive.selectTrack(2,0,false));await bad.waitForFunction(()=>document.querySelector('#ajji-reading-status').textContent.includes('could not load'));assert(await bad.locator('#ajji-full-text:visible').count());await bad.close();
 assert.deepEqual(errors,[]);await browser.close();console.log('PASS six original checksums, 34 continuous sections, 36 reading routes, real MP3 playback, no-restart script switch, unknown-text clearing, cross-file continuation, fetch failure, mobile and no-JS');
})().catch(e=>{console.error(e);process.exit(1)});

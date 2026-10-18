/* Integration test: run a local server on 8769; PLAYWRIGHT_MODULE may point to a local installation. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'});
 const page=await browser.newPage();
 await page.addInitScript(()=>{
  window.mockTime=0;window.seeks=[];window.loads=[];
  window.YT={Player:class{
   constructor(id,opts){this.o=opts;window.mockPlayer=this;setTimeout(()=>opts.events.onReady(),500)}
   getCurrentTime(){return window.mockTime}
   seekTo(t){window.mockTime=t;window.seeks.push(t)}
   loadVideoById(o){window.loads.push(o);this.seekTo(o.startSeconds);this.playVideo()}
   playVideo(){this.o.events.onStateChange({data:1})}
  }};
 });
 await page.goto('http://localhost:8769/en/navaratri/');
 await page.waitForFunction(()=>window.BhaktiRecording);
 for(const width of [320,390,1280]){
  await page.setViewportSize({width,height:900});
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow ${width}`);
 }
 await page.locator('.recording-jump summary').click();
 const cues=await page.evaluate(()=>BhaktiRecording.config.cues);
 assert(cues.length>1,'Need matched recording cues');
 for(const c of cues){
  assert.equal(await page.evaluate(t=>BhaktiRecording.findCue(BhaktiRecording.config.cues,t)?.id,c.start),c.id);
  assert.notEqual(await page.evaluate(t=>BhaktiRecording.findCue(BhaktiRecording.config.cues,t)?.id,c.end),c.id);
 }
 const matched=cues.filter(c=>c.work);
 await page.locator(`[data-cue="${matched[0].id}"]`).click();
 await page.locator(`[data-cue="${matched.at(-1).id}"]`).click();
 await page.waitForTimeout(650);
 assert.equal(await page.evaluate(()=>seeks.at(-1)),matched.at(-1).start,'latest pending seek wins');
 await page.waitForFunction(()=>!document.querySelector('#recording-text').hidden);
 const before=await page.evaluate(()=>seeks.length);
 await page.locator('[data-reader-script="devanagari"]').click();
 await page.waitForFunction(()=>document.querySelector('#recording-text').lang==='sa');
 assert.equal(await page.evaluate(()=>seeks.length),before,'Script switch must not seek');
 await page.locator('#recording-work').selectOption('lalitha-ashtottara-shatanamavali');
 assert.equal(await page.locator('#follow-recording').isChecked(),false);
 await page.waitForFunction(()=>document.querySelector('#recording-text-title').textContent.includes('रजताचल'));
 await page.locator('#follow-recording').check();
 await page.waitForFunction(w=>document.querySelector('#recording-work').value===w,matched.at(-1).work);
 const gap=cues.find(c=>!c.work);
 if(gap){await page.evaluate(t=>{mockTime=t;BhaktiRecording.sync(true)},gap.start);await page.waitForFunction(()=>document.querySelector('#recording-text').hidden)}
 await page.evaluate(t=>{mockTime=t;BhaktiRecording.sync(true)},matched[0].start);
 await page.waitForFunction(()=>!document.querySelector('#recording-text').hidden);
 await page.evaluate(()=>{mockTime=2475;BhaktiRecording.sync(true)});
 assert(await page.locator('#recording-text').isHidden(),'End must not retain wrong source');
 // Both recordings use one player; prepended part starts at the user-specified offset.
 await page.locator('[data-recording-part="0"]').click();
 assert.equal(await page.evaluate(()=>seeks.at(-1)),2106);
 const gana=await page.evaluate(()=>BhaktiRecording.config.cues.find(c=>c.id==='ganapathy-invocation'));
 await page.locator(`[data-cue="${gana.id}"]`).click();
 await page.waitForFunction(()=>!document.querySelector('#recording-text').hidden);
 assert.equal(await page.locator('#recording-text .svara-key').count(),1,'Vedic key must accompany cloned text');
 // Changing script in an unmatched interval must not expose unrelated text.
 await page.evaluate(()=>{mockTime=2106;BhaktiRecording.sync(true)});
 await page.locator('[data-reader-script="roman"]').click();
 assert(await page.locator('#recording-text').isHidden());
 // Simulate end of prelude: continue to Lalitha rather than replaying the beginning of the first video.
 await page.evaluate(()=>{mockTime=2749;mockPlayer.o.events.onStateChange({data:0})});
 assert.equal(await page.evaluate(()=>BhaktiRecording.config.videoId),'Cjd9t7t7MAA');
 assert.equal(await page.evaluate(()=>seeks.at(-1)),0);
 // A delayed fetch from an earlier intent cannot overwrite the final chosen script/work.
 await page.route('**/songs/lalitha-ashtottara-shatanamavali/roman/',async route=>{
  await new Promise(resolve=>setTimeout(resolve,300));await route.continue();
 });
 await page.locator('#recording-work').selectOption('lalitha-ashtottara-shatanamavali');
 await page.locator('[data-reader-script="kannada"]').click();
 await page.waitForFunction(()=>document.querySelector('#recording-text').lang==='kn'&&!document.querySelector('#recording-text').hidden);
 await page.waitForTimeout(400);assert.equal(await page.locator('#recording-text').getAttribute('lang'),'kn');
 // Failed fetch exposes a real fallback link and never stale prayer content.
 await page.route('**/songs/lalitha-ashtottara-bhurupa/roman/',route=>route.fulfill({status:503,body:'unavailable'}));
 await page.locator('#recording-work').selectOption('lalitha-ashtottara-bhurupa');
 await page.locator('[data-reader-script="roman"]').click();
 await page.waitForFunction(()=>document.querySelector('#reading-status').textContent.includes('could not load'));
 assert(await page.locator('#recording-text').isHidden());
 assert((await page.locator('#recording-full-text').getAttribute('href')).endsWith('lalitha-ashtottara-bhurupa/roman/'));
 const nojs=await browser.newPage({javaScriptEnabled:false});
 await nojs.goto('http://localhost:8769/en/navaratri/');
 assert(await nojs.locator('#recording-text [data-name]').count()===1000);
 assert(await nojs.locator('.recording-external').getAttribute('href'));
 await browser.close();console.log('PASS mobile layout, cue boundaries, pending seek, script switching without seek, manual/follow, gaps/end, no-JS full text');
})().catch(e=>{console.error(e);process.exit(1)});

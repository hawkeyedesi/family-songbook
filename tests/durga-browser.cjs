const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'chrome'});const page=await browser.newPage();
 await page.addInitScript(()=>{window.mockTime=0;window.seeks=[];window.YT={Player:class{constructor(id,o){this.o=o;window.player=this;setTimeout(()=>o.events.onReady(),50)}getCurrentTime(){return window.mockTime}seekTo(t){mockTime=t;seeks.push(t)}loadVideoById(o){this.seekTo(o.startSeconds);this.playVideo()}playVideo(){this.o.events.onStateChange({data:1})}}}});
 await page.goto('http://localhost:8769/en/durga-saptashloki/');await page.waitForFunction(()=>window.BhaktiRecording);
 for(const width of [320,390,1280]){await page.setViewportSize({width,height:900});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth))}
 assert.equal(await page.locator('h2').first().textContent(),'Durga Saptashloki — chant along with Guruji');
 assert.equal(await page.locator('.recording-credit').count(),1);
 assert(!((await page.locator('body').innerText()).includes('1983')),'Never misattribute official chant to family archive');
 await page.locator('#load-recording').click();await page.waitForFunction(()=>window.player&&seeks.length>0);
 const cues=await page.evaluate(()=>BhaktiRecording.config.cues);
 for(const c of cues){
  await page.evaluate(t=>{mockTime=t;BhaktiRecording.sync(true)},c.start);
  if(!c.work){assert(await page.locator('#recording-text').isHidden());continue}
  await page.waitForFunction(anchor=>!document.querySelector('#recording-text').hidden&&document.querySelector('#recording-text .recording-current-line')?.id===anchor,c.anchor);
  assert.equal(await page.evaluate(t=>BhaktiRecording.findCue(BhaktiRecording.config.cues,t)?.id,c.end),c===cues.at(-1)?undefined:cues[cues.indexOf(c)+1].id);
 }
 const before=await page.evaluate(()=>seeks.length);
 for(const script of ['devanagari','kannada','roman']){await page.locator(`[data-reader-script="${script}"]`).click();await page.waitForFunction(s=>document.querySelector('#recording-text').classList.contains(s),script)}
 assert.equal(await page.evaluate(()=>seeks.length),before);
 await page.locator('.recording-jump summary').click();await page.locator('[data-cue="verse-3"]').click();assert.equal(await page.evaluate(()=>seeks.at(-1)),43.45);
 await page.evaluate(()=>{mockTime=118.42;BhaktiRecording.sync(true)});assert(await page.locator('#recording-text').isHidden());
 const nojs=await browser.newContext({javaScriptEnabled:false});const p=await nojs.newPage();await p.goto('http://localhost:8769/en/durga-saptashloki/');assert.equal(await p.locator('#recording-text [data-verse]').count(),7);assert((await p.locator('.recording-external').getAttribute('href')).includes('_DP9lHAvGBU'));
 await browser.close();console.log('PASS Durga official credit,7verse sync,opening/end gaps,seek,3scripts without playback reset,mobile,noJS');
})().catch(e=>{console.error(e);process.exit(1)});

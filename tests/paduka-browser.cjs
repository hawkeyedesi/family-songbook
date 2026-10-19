/* Static reading, scripture integrity and ordered links; local server defaults to8769. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),base=process.env.BHAKTI_TEST_URL||'http://127.0.0.1:8769/';
const songs=JSON.parse(fs.readFileSync(path.join(root,'data/songs.json'))).filter(s=>s.collections.includes('paduka-puja-bhajans')).sort((a,b)=>a.collection_order['paduka-puja-bhajans']-b.collection_order['paduka-puja-bhajans']);
(async()=>{const b=await chromium.launch({headless:true,channel:'chrome'}),p=await b.newPage({viewport:{width:320,height:900}});
for(const prefix of['','en/']){await p.goto(base+prefix+'paduka-puja-bhajans/');assert.deepEqual(await p.locator('[data-work]').evaluateAll(es=>es.map(e=>e.dataset.work)),songs.map(s=>s.slug));}
let checked=0;
for(const [index,s]of songs.entries())for(const script of['kannada','devanagari','roman']){
 const suffix=script==='kannada'?'':script+'/';const r=await p.goto(base+'songs/'+s.slug+'/'+suffix);assert.equal(r.status(),200);await p.evaluate(()=>document.fonts.ready);
 assert.equal(await p.locator('article.lyrics').count(),1);assert.equal(await p.locator('.script-switch [data-script]').count(),3);
 assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow ${s.slug}/${script}`);
 const seq=p.locator('.paduka-sequence');assert.equal(await seq.count(),1);
 assert((await seq.innerText()).includes(`${index+1}/10`));
 for(const [direction,offset]of[['prev',-1],['next',1]]){const a=seq.locator(`[rel="${direction}"]`),target=songs[index+offset];assert.equal(await a.count(),target?1:0);if(target)assert((await a.getAttribute('href')).endsWith(`songs/${target.slug}/${suffix}`));}
 const bundle=JSON.parse(fs.readFileSync(path.join(root,'data',s.versions_file))),v=bundle.versions.find(v=>v.id===script);
 assert.equal(await p.locator('.text-chapter').count(),v.chapters.length);
 for(const c of v.chapters){const display=await p.locator('article.lyrics #'+c.id).innerText();assert(display.length>c.title.length);const expectedBreaks=c.paragraphs.reduce((n,t)=>n+(t.match(/\n/g)||[]).length,0);assert((await p.locator('article.lyrics #'+c.id+' br').count())>=expectedBreaks,'Lost printed line breaks');}
 checked++;
}
for(const width of[390,1280]){await p.setViewportSize({width,height:900});await p.goto(base+'en/paduka-puja-bhajans/');assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}
await p.goto(base+'songs/jagadguru-pancharatnamala/roman/');await p.screenshot({path:'/tmp/bhakti-paduka-final.png',fullPage:true});
const nojs=await b.newPage({javaScriptEnabled:false});await nojs.goto(base+'songs/durga-saptashloki/roman/');await nojs.locator('.paduka-sequence [rel="next"]').click();assert(nojs.url().endsWith('/om-jai-jagdish-hare/roman/'));
await b.close();console.log(`PASS ${checked}readingviews at320px,3script links,allprevious/nextlinks,categoryorder,390/1280landinglayouts,noJSnavigation`);
})().catch(e=>{console.error(e);process.exit(1)});

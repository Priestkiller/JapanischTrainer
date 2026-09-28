import {createRequire} from 'node:module';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import assert from 'node:assert/strict';
import {Store,Course,PHASES} from '../web/core.mjs';
import {previewServer} from '../tools/preview-server.mjs';
const require=createRequire(import.meta.url),{chromium}=require(process.env.JT_NODE_MODULES+'/playwright');
const read=p=>JSON.parse(readFileSync(new URL('../../'+p,import.meta.url),'utf8'));
const course=new Course(read('data/course.json'),read('data/catalog.json'),read('data/deep_lessons.json'),new Store());
const data=read('data/exercises.json'),cards=[...new Map([...course.cards].sort((a,b)=>(b.jp+b.romaji+b.de).length-(a.jp+a.romaji+a.de).length).slice(0,8).concat(course.cards[0],course.cards.find(c=>c.jp==='ありがとう')).filter(Boolean).map(c=>[c.key,c])).values()];
const output=new URL('../test-results/stage/',import.meta.url);mkdirSync(output,{recursive:true});
const report={passed:false,coreViews:0,extraViews:0,viewportChecks:[],realDevice:false};
const server=await previewServer(),browser=await chromium.launch({headless:true,channel:process.env.JT_BROWSER_CHANNEL??'msedge'});let page;
try{
 for(const [width,height] of [[412,915],[393,800],[320,640],[844,390],[768,1024]]){
  const context=await browser.newContext({viewport:{width,height},isMobile:true,hasTouch:true});
  await context.addInitScript(()=>{window.AndroidTrainer={getProfile:()=>{const seed=localStorage.getItem('stage-seed');if(seed){localStorage.removeItem('stage-seed');localStorage.setItem('stage-profile',seed);return seed;}return localStorage.getItem('stage-profile')??'{}';},saveProfile:s=>{localStorage.setItem('stage-profile',s);return true;},getCapabilities:()=>'{"native":true,"models":true}',stopAudio:()=>{},stopRecording:()=>{}};});
  page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto(`http://127.0.0.1:${server.address().port}`);await page.waitForSelector('html[data-ready=true]');
  async function open(card,phase,extraIndex=null){
   const key=card.lesson_key,index=card.card_index,profile={xp:320,streak:7,teacher_id:'sakura',completed:[],course_revision:11,legacy_unlocked:[key],last_lesson:{key,card:index},lesson_sessions:{[key]:{flow_revision:2,index,phase,passed:PHASES.slice(0,PHASES.indexOf(phase)),mode:'learn'}}};
   if(extraIndex!==null){const pack=data.packs.find(p=>p.lesson===key);profile.lesson_sessions['exercises:'+key]={revision:1,queue:pack.tasks,index:extraIndex,stage:'main',review:[],review_index:0,reviewed:[],outcomes:[],task:{}};}
   await page.evaluate(p=>localStorage.setItem('stage-seed',JSON.stringify(p)),profile);await page.reload();await page.waitForSelector('html[data-ready=true]');await page.locator('#hero-resume').click();
   if(await page.locator('.focus-sheet:not([hidden])').count())await page.locator('.focus-sheet-close').click();
   assert.equal(await page.locator('.focus-lesson-title h1').innerText(),course.byKey.get(key).title);assert.match(await page.locator('#step-count').textContent(),new RegExp('Schritt '+(PHASES.indexOf(phase)+1)+'/6'));
   if(extraIndex!==null){await page.getByRole('button',{name:'◇ Mehr üben',exact:true}).click();await page.locator('#exercise-round').click();}
   await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
  }
  async function bounded(label){
   const r=await page.evaluate(()=>{const w=document.querySelector('.focus-workspace'),v=document.querySelector('.focus-task-viewport'),d=document.querySelector('.focus-dock').getBoundingClientRect(),teacher=document.querySelector('.focus-teacher')?.getBoundingClientRect();return {outer:document.documentElement.scrollHeight-innerHeight,horizontal:document.documentElement.scrollWidth-innerWidth,workspace:w.scrollHeight-w.clientHeight,task:v.scrollHeight-v.clientHeight,dockBottom:d.bottom,dockTop:d.top,teacherTop:teacher?.top,teacherWidth:teacher?.width,speaking:document.querySelector('.focus-session').classList.contains('is-speaking')};});
   assert.ok(r.outer<=1&&r.horizontal<=1&&r.dockBottom<=height+1&&r.dockTop>=0,label+JSON.stringify(r));
   assert.equal(await page.locator('.focus-teacher').count(),r.speaking?1:0,label+' teacher only during speech');assert.equal(await page.locator('.focus-kiko').count(),0);
   if(r.speaking)assert.ok(r.teacherTop>=0&&r.teacherWidth>=25,label+' companion is visible');
   for(const selector of ['.focus-fixed-record','.focus-fixed-audio']){const n=page.locator(selector);if(await n.count()){await n.scrollIntoViewIfNeeded();const r=await n.boundingBox();assert.ok(r.x>=0&&r.x+r.width<=width+1&&r.y>=0&&r.y+r.height<=height-35,label+' recording/listening remains reachable in same view');}}
   const bubble=page.locator('.focus-coach-copy'),kiko=page.locator('.focus-kiko');if(await bubble.isVisible()&&await kiko.isVisible()){const a=await bubble.boundingBox(),b=await kiko.boundingBox();assert.ok(a.y+a.height<=b.y+1,label+' readable companion bubbles do not overlap');}
   const pager=page.locator('.focus-page-nav');if(await pager.isVisible()){
    for(let i=0;i<25&&!await pager.locator('button').last().isDisabled();i++)await pager.locator('button').last().click();
    assert.equal(await pager.locator('button').last().isDisabled(),true,label+' bounded page count');
    while(!await pager.locator('button').first().isDisabled())await pager.locator('button').first().click();
   }
  }
  for(const card of cards)for(const phase of PHASES){await open(card,phase);await bounded(`${width}:${card.key}:${phase}`);if(height>=740&&card.jp==='あ'&&phase==='speak')assert.equal(await page.locator('.focus-page-nav').isVisible(),false,'A short kana stays together with pronunciation and recording');report.coreViews++;if(width===412&&card.jp==='ありがとう'&&phase==='speak')await page.screenshot({path:new URL('speaking-412.png',output).pathname.replace(/^\/([A-Z]:)/,'$1')});}
  if(width===412)for(const pack of data.packs)for(let i=0;i<pack.tasks.length;i++){
   await open(course.cards.find(c=>c.lesson_key===pack.lesson),'speak',i);await bounded(pack.tasks[i]);report.extraViews++;
   const t=data.tasks.find(t=>t.id===pack.tasks[i]);if(['translate','read','echo'].includes(t.family)&&pack.lesson==='5:0')await page.screenshot({path:new URL(t.family+'-412.png',output).pathname.replace(/^\/([A-Z]:)/,'$1')});
  }
  assert.deepEqual(errors,[]);report.viewportChecks.push({width,height,speechCueTogether:true,longContentScrollFallback:true,explicitAnswerPages:true});await context.close();
 }
 report.passed=true;
}catch(e){if(page)await page.screenshot({path:new URL('failure.png',output).pathname.replace(/^\/([A-Z]:)/,'$1')});throw e;}finally{writeFileSync(new URL('report.json',output),JSON.stringify(report,null,2));await browser.close();server.close();}
console.log(report);


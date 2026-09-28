import {createRequire} from 'node:module';
import {mkdirSync,writeFileSync,readFileSync} from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {previewServer} from '../tools/preview-server.mjs';
const require=createRequire(import.meta.url),{chromium}=require(path.join(process.env.JT_NODE_MODULES,'playwright'));
const data=JSON.parse(readFileSync(new URL('../../data/exercises.json',import.meta.url),'utf8')),tasks=new Map(data.tasks.map(t=>[t.id,t]));
const out=new URL('../test-results/exercises/',import.meta.url);mkdirSync(out,{recursive:true});
const server=await previewServer(),browser=await chromium.launch({headless:true,channel:process.env.JT_BROWSER_CHANNEL??'msedge'});
const report={passed:false,viewports:[],entries:0,task_checks:0,simulated_audio:true,real_microphone:false};let lastPage;
try{
 for(const [width,height] of [[320,640],[412,915],[844,390],[768,1024]]){
  const context=await browser.newContext({viewport:{width,height},isMobile:true,hasTouch:true});
  await context.addInitScript(()=>{
   window.testRequests=[];window.AndroidTrainer={getProfile:()=>{const seed=localStorage.getItem('ex-seed');if(seed){localStorage.removeItem('ex-seed');localStorage.setItem('ex-profile',seed);return seed;}return localStorage.getItem('ex-profile')??'{}';},saveProfile:v=>{localStorage.setItem('ex-profile',v);return true;},getCapabilities:()=>JSON.stringify({native:true,models:true}),stopAudio:()=>{},stopRecording:()=>{},
    speak:(text,speaker,speed,id)=>{window.testRequests.push({text,speaker,speed,id});if(!window.holdAudio)setTimeout(()=>{window.JTNative('audioStarted',{request:id});window.JTNative('audioDone',{request:id});},5);},
    record:id=>{window.lastRecord=id;setTimeout(()=>window.JTNative('recording',{request:id}),5);},playRecording:(old,id)=>setTimeout(()=>window.JTNative('audioDone',{request:id}),5)};
  });
  const page=await context.newPage(),errors=[];lastPage=page;page.on('pageerror',e=>errors.push(e.message));await page.goto(`http://127.0.0.1:${server.address().port}`);await page.waitForSelector('html[data-ready=true]');
  async function open(key,taskIndex=null){
   const profile={xp:321,completed:['0:0'],teacher_id:'ren',course_revision:11,motion_enabled:false,legacy_unlocked:[key],last_lesson:{key,card:0},lesson_sessions:{[key]:{flow_revision:2,index:0,phase:'speak',passed:[],mode:'learn'}}};
   if(taskIndex!==null){const pack=data.packs.find(p=>p.lesson===key);profile.lesson_sessions['exercises:'+key]={revision:1,queue:pack.tasks,index:taskIndex,stage:'main',review:[],review_index:0,reviewed:[],outcomes:[],task:{}};}
   await page.evaluate(p=>localStorage.setItem('ex-seed',JSON.stringify(p)),profile);await page.reload();await page.waitForSelector('html[data-ready=true]');await page.locator('#hero-resume').click();await page.locator('#exercise-round').click();await page.locator('#ex-next').waitFor({state:'attached'});
  }
  async function state(key){return page.evaluate(key=>JSON.parse(localStorage.getItem('ex-profile')).lesson_sessions['exercises:'+key],key);}
  async function bounded(){assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth)<=width+1,'horizontal overflow');}
  for(const pack of data.packs){await open(pack.lesson);assert.match(await page.locator('#exercise-content').innerText(),/Erst verstehen/);await bounded();await page.locator('#ex-next').click();assert.equal((await state(pack.lesson)).stage,'main');report.entries++;}
  // Complete a real mixed round through UI controls, including audio request correlation.
  const key='5:0',pack=data.packs.find(p=>p.lesson===key);await open(key);await page.locator('#ex-next').click();
  for(const tid of pack.tasks){const t=tasks.get(tid);assert.equal((await state(key)).queue[(await state(key)).index],tid);await bounded();
   assert.ok(await page.locator('#ex-next').isDisabled());
   if(t.family==='hear_gap'){
    assert.equal(await page.locator('#exercise-content').getByText(t.answers[0],{exact:true}).count(),0);
    await page.locator('#ex-input').fill('mi');await page.locator('#ex-help').click();assert.equal(await page.locator('#ex-input').inputValue(),'mi');await page.locator('#ex-help').click();
    await page.locator('#ex-input').dispatchEvent('compositionstart');await page.locator('#ex-input').press('Enter');assert.equal((await state(key)).task.checks,0);await page.locator('#ex-input').dispatchEvent('compositionend');
    await page.locator('#ex-audio').click();await page.waitForFunction(()=>!document.querySelector('#ex-audio-status').textContent);await page.locator('#ex-input').fill(t.answers[0]);
   }else if(t.family==='pairs'){
    for(const p of t.pairs){await page.locator(`[data-ex-left="${p.id}"]`).click();await page.locator(`[data-ex-right="${p.id}"]`).click();}
    if(t.mode==='audio')await page.waitForFunction(key=>JSON.parse(localStorage.getItem('ex-profile')).lesson_sessions['exercises:'+key].task.heard.length===3,key);
   }else if(['echo','recall'].includes(t.family)){
    if(t.family==='echo'){assert.ok((await page.locator('#exercise-content').innerText()).includes(t.audio));await page.locator('#ex-audio').click();await page.waitForFunction(()=>!document.querySelector('#ex-audio-status').textContent);}
    else{assert.ok(!(await page.locator('#exercise-content').innerText()).includes(t.audio));await page.locator('#ex-help').click();assert.ok(!(await page.locator('#exercise-content').innerText()).includes(t.audio));await page.locator('#ex-help').click();}
    await page.locator('#ex-record').click();await page.waitForFunction(()=>!!window.lastRecord);await page.evaluate(text=>window.JTNative('speechResult',{request:window.lastRecord,text}),t.accepted_speech[0]);
   }else if(['choice_gap','read'].includes(t.family))await page.locator(`[data-ex-choice="${t.answers[0]}"]`).click();
   else{
    const pool=[...t.tokens];for(let i=0;i<t.solutions[0].length;i++){const at=pool.findIndex(x=>x.text===t.solutions[0][i]),token=pool.splice(at,1)[0];if(t.family==='multi_gap')await page.locator(`[data-ex-slot="${i}"]`).click();await page.locator(`.tokens [data-ex-token="${token.id}"]`).click();}
   }
   if(!['echo','recall'].includes(t.family))await page.locator('#ex-check').click();assert.equal((await state(key)).task.success,true,t.id);
   await page.locator('#ex-help').click();assert.equal((await state(key)).task.success,true);await page.locator('#ex-help').click();await bounded();
   if(width===412)await page.screenshot({path:path.join(out.pathname.replace(/^\//,''),t.family+(t.mode??'')+'.png'),fullPage:true});
   await page.locator('#ex-next').click();report.task_checks++;
  }
  assert.equal((await state(key)).stage,'complete');
  // Delayed audio from a paused task and cancelled/denied speech cannot pass.
  await open(key,0);await page.evaluate(()=>window.holdAudio=true);await page.locator('#ex-audio').click();
  const stale=await page.evaluate(()=>testRequests.at(-1).id);await page.locator('#ex-pause').click();await page.evaluate(id=>window.JTNative('audioDone',{request:id}),stale);
  await page.locator('#exercise-round').click();assert.equal((await state(key)).task.heard.length,0);
  await page.evaluate(()=>window.holdAudio=false);await page.locator('#ex-slow').click();await page.waitForFunction(()=>!document.querySelector('#ex-audio-status').textContent);
  const requests=await page.evaluate(()=>testRequests.slice(-2));assert.ok(requests[1].speed<requests[0].speed);assert.equal(requests[0].text,requests[1].text);
  await page.locator('#ex-record').click();await page.waitForFunction(()=>!!window.lastRecord);
  await page.evaluate(()=>window.JTNative('speechError',{request:lastRecord,message:'Mikrofonberechtigung verweigert · Testsignal'}));assert.equal((await state(key)).task.success,false);assert.equal((await state(key)).outcomes.at(-1).result,'technical');
  await page.locator('#ex-record').click();const oldRecording=await page.evaluate(()=>lastRecord);await page.locator('#ex-pause').click();
  await page.evaluate(({request,text})=>window.JTNative('speechResult',{request,text}),{request:oldRecording,text:tasks.get(pack.tasks[0]).accepted_speech[0]});
  await page.locator('#exercise-round').click();assert.equal((await state(key)).task.success,false);
  // Reading has visible original text; translation only after explicit help.
  const readingPack=data.packs.find(p=>p.lesson==='v11:read-plan'),ri=readingPack.tasks.findIndex(k=>tasks.get(k).family==='read'),rt=tasks.get(readingPack.tasks[ri]);await open(readingPack.lesson,ri);
  assert.ok((await page.locator('.exercise-reading').innerText()).includes(rt.text));await page.locator('[data-ex-choice="w0"]').click();assert.equal((await state(readingPack.lesson)).task.checks,0);await page.locator('#ex-check').click();assert.equal((await state(readingPack.lesson)).task.success,false);assert.ok(await page.locator('mark').count());
  await page.locator('#ex-help').click();await page.locator('#ex-solution').click();assert.equal((await state(readingPack.lesson)).task.help,2);assert.equal((await state(readingPack.lesson)).task.success,false);await bounded();
  if(width===412)await page.screenshot({path:path.join(out.pathname.replace(/^\//,''),'read-help.png'),fullPage:true});
  const final=await page.evaluate(()=>JSON.parse(localStorage.getItem('ex-profile')));assert.equal(final.xp,321);assert.deepEqual(final.completed,['0:0']);assert.deepEqual(errors,[]);
  report.viewports.push({width,height});await context.close();
 }
 report.passed=true;writeFileSync(new URL('report.json',out),JSON.stringify(report,null,2));console.log(report);
}catch(e){if(lastPage){await lastPage.screenshot({path:path.join(out.pathname.replace(/^\//,''),'failure.png')});console.log(await lastPage.evaluate(()=>({viewport:{w:innerWidth,h:innerHeight,y:scrollY,visual:visualViewport?.offsetTop,scale:visualViewport?.scale},button:document.querySelector('#ex-next')?.getBoundingClientRect().toJSON(),html:document.querySelector('#exercise-content')?.outerHTML.slice(-2000)})));}throw e;}finally{await browser.close();server.close();}

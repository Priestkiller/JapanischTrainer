import {createRequire} from 'node:module';
import {mkdirSync,writeFileSync,readFileSync} from 'node:fs';
import assert from 'node:assert/strict';
import {fileURLToPath} from 'node:url';
import {previewServer} from '../tools/preview-server.mjs';
const require=createRequire(import.meta.url),{chromium}=require(process.env.JT_NODE_MODULES+'/playwright');
const out=new URL('../../validation/characters-1114/',import.meta.url);mkdirSync(out,{recursive:true});
const server=await previewServer(),browser=await chromium.launch({headless:true,channel:'msedge'});
const teachers=JSON.parse(readFileSync(new URL('../../data/catalog.json',import.meta.url))).TEACHERS;
const lesson=JSON.parse(readFileSync(new URL('../../data/course.json',import.meta.url))).units[0].lessons[1];
const report={passed:false,simulatedNative:true,humanMicrophone:false,views:0,teachers:[],formats:6};let page;
const formats=[[412,915,1,false],[393,851,1,false],[320,640,1,false],[844,390,1,false],[412,915,1.6,false],[412,915,1,true]];
async function open(seed,format){
 const [width,height,scale,reduced]=format,ctx=await browser.newContext({viewport:{width,height},hasTouch:true,reducedMotion:reduced?'reduce':'no-preference'});page=await ctx.newPage();
 await page.addInitScript(({seed,scale})=>{
  window.profile=seed;window.AndroidTrainer={getProfile:()=>JSON.stringify(profile),getCapabilities:()=>JSON.stringify({native:true,models:true}),saveProfile:s=>(profile=JSON.parse(s),true),stopAudio(){},stopRecording(){},speak(t,s,v,id){window.audioRequest=id;},record(id){window.speechRequest=id;},recordKana(id){window.speechRequest=id;},recordComparison(id){window.speechRequest=id;}};
  window.addEventListener('DOMContentLoaded',()=>{document.documentElement.style.fontSize=`${scale*16}px`;});
 },{seed,scale});await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.waitForFunction(()=>document.documentElement.dataset.ready==='true');
 await page.evaluate(()=>JTNative('capabilities',{native:true,models:true}));return ctx;
}
async function capture(name){await page.screenshot({path:fileURLToPath(new URL(name+'.png',out))});report.views++;}
async function visible(selector){assert.ok(await page.locator(selector).evaluate(n=>{const r=n.getBoundingClientRect();return r.width>0&&r.height>0&&r.left>=-1&&r.right<=innerWidth+1&&r.top>=0&&r.bottom<=innerHeight+1;}),selector+' fits the usable screen');}
try{
 for(const teacher of teachers){
  for(let f=0;f<formats.length;f++){
   const ctx=await open({xp:77,teacher_id:teacher.id,course_revision:11,motion_enabled:true},formats[f]);const errors=[];page.on('pageerror',e=>errors.push(e.message));
   await page.locator('#hero-resume').click();await page.waitForSelector('.focus-sheet:not([hidden])');await page.evaluate(()=>JTBack());
   await page.waitForFunction(()=>document.querySelector('#teacher-canvas')?.dataset.frame);
   if(!formats[f][3])await page.waitForFunction(()=>document.querySelector('#teacher-canvas').dataset.playing==='true');
   assert.equal(await page.locator('.focus-coach-copy strong').textContent(),teacher.name);await visible('#teacher-canvas');await visible('#record');await visible('#hear-normal');
   assert.ok(await page.locator('#teacher-canvas').evaluate(n=>n.getBoundingClientRect().height)>= (formats[f][1]<550?68:formats[f][2]>1?82:100));
   assert.equal(await page.locator('#record').isDisabled(),true);await page.locator('#hear-normal').click();assert.equal(await page.locator('body').getAttribute('data-coach-state'),'preparing');
   await page.evaluate(()=>JTNative('audioStarted',{request:audioRequest}));assert.equal(await page.locator('body').getAttribute('data-coach-state'),'speaking');await visible('#record');await capture(`${teacher.id}-${f}-speaking`);
   await page.evaluate(()=>JTNative('audioDone',{request:audioRequest}));await page.locator('#record').click();await page.evaluate(()=>JTNative('recording',{request:speechRequest}));assert.equal(await page.locator('body').getAttribute('data-coach-state'),'listening');
   await page.evaluate(()=>JTNative('recognizing',{request:speechRequest}));assert.equal(await page.locator('body').getAttribute('data-coach-state'),'thinking');await visible('#record');
   await page.evaluate(()=>JTNative('speechResult',{request:speechRequest,text:'あ',shortKana:true,audioQualified:true}));assert.equal(await page.locator('body').getAttribute('data-coach-state'),'happy');assert.equal(await page.evaluate(()=>profile.xp),77);await visible('#advance');
   await page.locator('#advance').click();assert.equal(await page.locator('#teacher-canvas').count(),0);assert.deepEqual(errors,[]);await ctx.close();
  }report.teachers.push(teacher.id);
 }
 for(let f=0;f<formats.length;f++)for(const repeat of [false,true]){
  const count=lesson.cards.length,ctx=await open({xp:repeat?45:20,completed:repeat?['0:0','0:1']:['0:0'],motion_enabled:true,course_revision:11,last_lesson:{key:'0:1',card:count-1},lesson_sessions:{'0:1':{flow_revision:2,passed:[],index:count-1,phase:'meaning',mode:'recap',recap:[count-1],recap_total:count,recap_passed:count-1}}},formats[f]);
  await page.locator('[data-page=course]').click();await page.locator('[data-lesson="0:1"]').click();await page.locator('[data-choice]').filter({hasText:lesson.cards.at(-1).de}).click();await page.locator('#advance').click();
  await page.waitForFunction(()=>document.querySelector('.kiko-actor')?.dataset.frame);await visible('#complete-next');await visible('.completion-actions [data-nav=course]');
  assert.equal(await page.evaluate(()=>profile.xp),45);assert.equal(await page.locator('.completion-xp').textContent(),repeat?'Wiederholung geschafft':'+25 XP');
  if(!formats[f][3]){const pixels=await page.locator('.reward-confetti').evaluate(n=>n.toDataURL());await page.waitForTimeout(100);assert.notEqual(await page.locator('.reward-confetti').evaluate(n=>n.toDataURL()),pixels);}
  else assert.equal(await page.locator('.reward-stage').getAttribute('data-celebration'),'finished');
  await capture(`complete-${f}-${repeat?'repeat':'first'}`);
  if(f===0&&repeat){await page.waitForFunction(()=>document.querySelector('.reward-stage').dataset.celebration==='finished');assert.equal(await page.locator('#complete-next').isEnabled(),true);assert.equal(await page.evaluate(()=>profile.xp),45);}
  await page.locator('#complete-next').click();assert.equal(await page.locator('.reward-stage').count(),0);await ctx.close();
 }
 const talkCtx=await open({xp:77,teacher_id:'haruto',course_revision:11},formats[0]);
 await page.locator('[data-page=more]').click();await page.locator('[data-nav="speech-lab"]').click();await page.waitForFunction(()=>document.querySelector('#teacher-canvas')?.dataset.frame);assert.equal(await page.locator('.voice-bubble strong').textContent(),'Haruto');await capture('speech-lab');
 await page.locator('#lab-record').click();await page.evaluate(()=>JTNative('recording',{request:speechRequest}));assert.equal(await page.locator('body').getAttribute('data-coach-state'),'listening');await capture('speech-lab-listening');
 await page.evaluate(()=>JTNative('speechResult',{request:speechRequest,results:[{model:'sensevoice',text:'あ',decodeMs:10,loadMs:5}]}));assert.equal(await page.evaluate(()=>profile.xp),77);
 await page.locator('[data-page=more]').click();await page.locator('[data-nav=talk]').click();await page.locator('[data-talk-scene]').first().click();
 for(let i=0;i<10&&await page.locator('#talk-prep-next').count();i++)await page.locator('#talk-prep-next').click();
 await page.waitForFunction(()=>document.querySelector('#teacher-canvas')?.dataset.frame);assert.equal(await page.locator('.voice-bubble strong').textContent(),'Haruto');await page.locator('#talk-replay').click();await page.evaluate(()=>JTNative('audioStarted',{request:audioRequest}));assert.equal(await page.locator('body').getAttribute('data-coach-state'),'speaking');await capture('conversation');await page.locator('#talk-stop').click();assert.equal(await page.locator('body').getAttribute('data-coach-state'),'ready');assert.equal(await page.evaluate(()=>profile.xp),77);await talkCtx.close();
 const ctx=await open({xp:77,teacher_id:'sakura',course_revision:11,motion_enabled:false},formats[0]);await page.locator('#hero-resume').click();await page.waitForSelector('.focus-sheet:not([hidden])');await page.evaluate(()=>JTBack());await page.waitForFunction(()=>document.querySelector('#teacher-canvas')?.dataset.frame);
 const still=await page.locator('#teacher-canvas').evaluate(n=>n.toDataURL());await page.waitForTimeout(300);assert.equal(await page.locator('#teacher-canvas').evaluate(n=>n.toDataURL()),still);await ctx.close();
 report.passed=true;
}catch(e){if(page)await page.screenshot({path:fileURLToPath(new URL('failure.png',out))});throw e;}
finally{writeFileSync(new URL('report.json',out),JSON.stringify(report,null,2));await browser.close();server.close();}
console.log(JSON.stringify(report));

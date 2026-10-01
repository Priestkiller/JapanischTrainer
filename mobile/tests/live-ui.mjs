import {createRequire} from 'node:module';
import {mkdirSync,writeFileSync,readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
import {previewServer} from '../tools/preview-server.mjs';
const require=createRequire(import.meta.url),{chromium}=require(process.env.JT_NODE_MODULES+'/playwright');
const out=new URL('../../validation/live-1113/',import.meta.url);mkdirSync(out,{recursive:true});
const server=await previewServer(),browser=await chromium.launch({headless:true,channel:'msedge'});
const raw=JSON.parse(readFileSync(new URL('../../data/course.json',import.meta.url))),lesson=raw.units[0].lessons[1],answer=lesson.cards.at(-1).de;
const report={passed:false,simulatedNative:true,humanMicrophone:false,formats:[],views:0};let page;
try{
 for(const [width,height,scale,reduced] of [[412,915,1,false],[393,851,1,false],[320,640,1,false],[844,390,1,false],[412,915,1.6,false],[412,915,1,true]]){
  const ctx=await browser.newContext({viewport:{width,height},hasTouch:true,reducedMotion:reduced?'reduce':'no-preference'});page=await ctx.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.addInitScript(({scale})=>{
   const now=new Date(),yesterday=new Date();yesterday.setDate(now.getDate()-1);const day=d=>`${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
   window.profile={xp:321,completed:['0:0'],streak:7,last_active:day(yesterday),teacher_id:'yuki',course_revision:11};
   window.AndroidTrainer={getProfile:()=>JSON.stringify(profile),saveProfile:s=>{profile=JSON.parse(s);return true;},getCapabilities:()=>'{"native":true,"models":true}',stopAudio:()=>{},stopRecording:()=>{}};
   document.addEventListener('DOMContentLoaded',()=>document.documentElement.style.fontSize=16*scale+'px');
  },{scale});
  await page.goto(`http://127.0.0.1:${server.address().port}`);await page.waitForSelector('html[data-ready=true]');
  async function capture(name){assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true,name+' no horizontal clipping');report.views++;await page.screenshot({path:fileURLToPath(new URL(`${name}-${width}-${height}-${scale}-${reduced}.png`,out))});}
  assert.ok(await page.locator('.home-stats').evaluate(n=>n.getBoundingClientRect().bottom<document.querySelector('.hero').getBoundingClientRect().top&&n.getBoundingClientRect().top>=0));await capture('home');
  await page.locator('[data-nav=calendar]').click();await page.waitForSelector('.calendar-grid');
  assert.equal(await page.evaluate(()=>profile.xp===321&&profile.streak===7&&profile.teacher_id==='yuki'&&profile.learning_days.length===1),true);
  await capture('calendar');const current=await page.locator('#calendar-month').textContent();
  assert.equal(await page.locator('#calendar-next').isDisabled(),true);await page.locator('#calendar-prev').click();assert.notEqual(await page.locator('#calendar-month').textContent(),current);await page.locator('#calendar-next').click();assert.equal(await page.locator('#calendar-month').textContent(),current);
  await page.locator('[data-page=home]').click();await page.locator('.kiko-greeting').scrollIntoViewIfNeeded();await page.waitForFunction(()=>document.querySelector('.kiko-actor').dataset.frame!==undefined);
  await page.locator('.kiko-greeting').click();
  if(!reduced){await page.waitForFunction(()=>Number(document.querySelector('.kiko-actor').dataset.frame)>=8);const pixels=await page.locator('.kiko-actor').evaluate(n=>n.toDataURL());await page.waitForTimeout(180);assert.notEqual(await page.locator('.kiko-actor').evaluate(n=>n.toDataURL()),pixels);}
  else assert.equal(await page.locator('.kiko-actor').getAttribute('data-playing'),'false');
  await capture('kiko');
  await page.locator('#settings-shortcut').click();await page.locator('#motion').uncheck();await page.locator('[data-page=home]').click();await page.locator('.kiko-greeting').scrollIntoViewIfNeeded();await page.waitForFunction(()=>document.querySelector('.kiko-actor').dataset.frame!==undefined);const still=await page.locator('.kiko-actor').evaluate(n=>n.toDataURL());await page.waitForTimeout(180);assert.equal(await page.locator('.kiko-actor').evaluate(n=>n.toDataURL()),still);
  for(const repeat of [false,true]){
   await page.evaluate(({repeat,count})=>JTNative('profileImported',{xp:repeat?45:20,completed:repeat?['0:0','0:1']:['0:0'],course_revision:11,last_lesson:{key:'0:1',card:count-1},lesson_sessions:{'0:1':{flow_revision:2,passed:[],index:count-1,phase:'meaning',mode:'recap',recap:[count-1],recap_total:count,recap_passed:count-1}}}),{repeat,count:lesson.cards.length});
   await page.locator('[data-page=course]').click();await page.locator('[data-lesson="0:1"]').click();await page.waitForSelector('[data-choice]');
   await page.locator('[data-choice]').filter({hasText:answer}).click();await page.locator('#advance').click();await page.waitForSelector('.completion');
   assert.equal(await page.locator('.completion-xp').textContent(),repeat?'Wiederholung geschafft':'+25 XP');assert.equal(await page.evaluate(()=>profile.xp),45);
   assert.equal(await page.locator('#complete-next').isEnabled(),true);assert.equal(await page.locator('img.completion-kiko').count(),0);await page.waitForFunction(()=>document.querySelector('.kiko-actor').dataset.frame!==undefined);
   assert.equal(await page.locator('.completion').evaluate(n=>{const s=getComputedStyle(n);return s.color==='rgb(245, 248, 255)'&&!s.backgroundColor.startsWith('rgb(255');}),true);
   await capture(repeat?'complete-repeat':'complete-first');await page.locator('#complete-next').click();await page.waitForSelector('#record');assert.equal(await page.locator('.kiko-actor').count(),0);
  }
  assert.deepEqual(errors,[]);report.formats.push({width,height,scale,reduced,oldProgressPreserved:true,actualSpritePixelsChanged:!reduced,repeatXp:0});await ctx.close();
 }report.passed=true;
}catch(e){if(page)await page.screenshot({path:fileURLToPath(new URL('failure.png',out))});throw e;}
finally{writeFileSync(new URL('report.json',out),JSON.stringify(report,null,2));await browser.close();server.close();}
console.log(JSON.stringify({passed:report.passed,views:report.views,formats:report.formats.length}));

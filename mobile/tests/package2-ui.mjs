import {createRequire} from 'node:module';
import {mkdirSync,writeFileSync,readFileSync} from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {previewServer} from '../tools/preview-server.mjs';
const require=createRequire(import.meta.url);
const {chromium}=require(path.join(process.env.JT_NODE_MODULES,'playwright'));
const pack=Number(process.env.JT_CONTENT_PACKAGE??2);
const raw=JSON.parse(readFileSync(new URL('../../data/course.json',import.meta.url),'utf8'));
const lessons=raw.units.flatMap((u,ui)=>u.lessons.map((l,li)=>({...l,id:l.id??`${ui}:${li}`}))).filter(l=>l.study_guide?.package===pack);
const output=new URL(`../test-results/package${pack}/`,import.meta.url);mkdirSync(output,{recursive:true});
const server=await previewServer(),url=`http://127.0.0.1:${server.address().port}`;
const browser=await chromium.launch({headless:true,channel:process.env.JT_BROWSER_CHANNEL??'msedge'});
const report={passed:false,simulated_audio:true,real_microphone:false,viewports:[],checks:0};
try {
 for(const [width,height] of [[320,640],[412,915],[844,390]]) {
  const context=await browser.newContext({viewport:{width,height},isMobile:true,hasTouch:true});
  await context.addInitScript(()=>{window.AndroidTrainer={getProfile:()=>{const seed=localStorage.getItem('jt-p2-seed');if(seed){localStorage.removeItem('jt-p2-seed');localStorage.setItem('jt-p2',seed);return seed;}return localStorage.getItem('jt-p2')??'{}';},saveProfile:v=>{localStorage.setItem('jt-p2',v);return true;},getCapabilities:()=>JSON.stringify({native:true,models:true}),stopAudio:()=>{},stopRecording:()=>{},speak:()=>{},record:()=>{}};});
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));await page.goto(url);await page.waitForSelector('html[data-ready=true]');
  async function resume(l,phase='speak') {
   const phases=['speak','meaning','listen','build','write','apply'];
   const p={course_revision:11,teacher_id:'ren',xp:321,completed:['0:0'],motion_enabled:false,legacy_unlocked:[l.id],last_lesson:{key:l.id,card:0},review:{'0:0:1':{box:2,due:9999999999}},lesson_sessions:{[l.id]:{flow_revision:2,index:0,phase,passed:phases.slice(0,phases.indexOf(phase)),mode:'learn',recap:[],recap_total:0,recap_passed:0}}};
   await page.evaluate(p=>localStorage.setItem('jt-p2-seed',JSON.stringify(p)),p);await page.reload();await page.waitForSelector('html[data-ready=true]');await page.locator('#hero-resume').click();await page.locator('#advance').waitFor();
  }
  async function bounded(){assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));}
  for(const l of lessons) {
   await resume(l);assert.ok((await page.locator('.lesson-goal').textContent()).includes(l.goal),l.id+': '+await page.locator('.lesson-goal').textContent());
   assert.equal(await page.locator('.lesson-guide[open]').count(),1);assert.ok((await page.locator('.lesson-guide').textContent()).includes(l.study_guide.points[1]));await bounded();
   assert.equal(await page.locator('#advance').isDisabled(),true);
   await resume(l,'apply');const task=page.locator('#task');assert.equal(await task.locator('.romaji').count(),0);assert.equal(await task.locator('.exercise-hint').count(),0);
   const scenario=l.cards[0].detail.scenario,wrong=scenario.wrong[0];
   await page.getByRole('button',{name:wrong,exact:true}).click();assert.ok((await page.locator('#task-feedback').innerText()).includes(scenario.feedback[wrong]));
   assert.equal(await page.locator('#advance').isDisabled(),true);await bounded();
   await page.locator('#show-hint').click();assert.equal(await page.locator('.exercise-hint').count(),1);assert.equal(await page.locator('#advance').isDisabled(),true);
   const saved=await page.evaluate(()=>JSON.parse(AndroidTrainer.getProfile()));assert.equal(saved.xp,321);assert.deepEqual(saved.completed,['0:0']);assert.equal(saved.teacher_id,'ren');assert.equal(saved.study_cards[l.id+':0'].hints,1);assert.equal(saved.review['0:0:1'].box,2);
   await page.locator('#show-hint').click();assert.equal(await page.locator('.exercise-hint').count(),0);
   await page.getByRole('button',{name:scenario.correct,exact:true}).click();assert.equal(await page.locator('#advance').isDisabled(),false);
   if(['15:0','v11:dialog-directions','v11:read-profile','6:0','v11:checkout','v11:dialog-cafe','v11:clock-hours','v11:dialog-weekend','v11:read-plan'].includes(l.id))await page.screenshot({path:new URL(`${l.id.replaceAll(':','-')}-${width}.png`,output).pathname.replace(/^\/([A-Za-z]:)/,'$1'),fullPage:true});
   await page.locator('#advance').click();assert.equal(await page.locator('#step-count').textContent(),'Schritt 1/6');assert.equal(await page.locator('.exercise-hint').count(),0);report.checks++;
  }
  assert.deepEqual(errors,[]);report.viewports.push({width,height,lessons:lessons.length});await context.close();
 }
 report.passed=true;
} finally {writeFileSync(new URL('report.json',output),JSON.stringify(report,null,2));await browser.close();await new Promise(resolve=>server.close(resolve));}
console.log(JSON.stringify(report));

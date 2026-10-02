import {createRequire} from 'node:module';
import {readFileSync,writeFileSync,mkdirSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
import {previewServer} from '../tools/preview-server.mjs';
const require=createRequire(import.meta.url),{chromium}=require(process.env.JT_NODE_MODULES+'/playwright');
const data=JSON.parse(readFileSync(new URL('../../data/exercises.json',import.meta.url),'utf8')),
 pack=data.packs.find(p=>p.lesson==='5:0'),out=new URL('../../validation/keyboard-regression-1115/',import.meta.url);
mkdirSync(out,{recursive:true});
const server=await previewServer(),browser=await chromium.launch({headless:true,channel:'msedge'}),report={passed:false,views:0,simulatedKeyboardResize:true,actualAndroidKeyboard:false,cases:[]};
try{for(const [width,height,scale] of [[393,780,1],[393,744,1],[320,640,1],[393,780,1.2],[412,915,1.6],[844,390,1]])for(const extra of [false,true]){
 const ctx=await browser.newContext({viewport:{width,height},hasTouch:true}),page=await ctx.newPage(),key=extra?'5:0':'0:0',id=extra?'ex-input':'romaji-input',errors=[];
 page.on('pageerror',e=>errors.push(e.message));
 const seed={xp:321,completed:[],teacher_id:'ren',course_revision:11,legacy_unlocked:[key],last_lesson:{key,card:0},lesson_sessions:{[key]:{flow_revision:2,index:0,phase:extra?'speak':'write',passed:extra?[]:['speak','meaning','listen','build'],mode:'learn'}}};
 if(extra)seed.lesson_sessions['exercises:5:0']={revision:1,queue:pack.tasks,index:5,stage:'main',review:[],review_index:0,reviewed:[],outcomes:[],task:{}};
 await page.addInitScript(({seed,scale})=>{window.AndroidTrainer={getProfile:()=>localStorage.getItem('p')??JSON.stringify(seed),saveProfile:s=>(localStorage.setItem('p',s),true),getCapabilities:()=>'{"native":true,"models":true}',stopAudio(){},stopRecording(){}};document.addEventListener('DOMContentLoaded',()=>document.documentElement.style.fontSize=16*scale+'px');},{seed,scale});
 async function open(){await page.waitForSelector('html[data-ready=true]');await page.locator('#hero-resume').click();if(await page.locator('.focus-sheet:not([hidden])').count())await page.locator('.focus-sheet-close').click();if(extra){await page.getByRole('button',{name:'◇ Mehr üben',exact:true}).click();await page.locator('#exercise-round').click();}await page.waitForTimeout(150);}
 const hit=()=>page.locator('#'+id).evaluate(n=>{const r=n.getBoundingClientRect();return r.width>0&&r.height>0&&document.elementFromPoint(r.left+r.width/2,r.top+r.height/2)===n;});
 async function find(){for(let i=0;i<20;i++){if(await hit())return;assert.equal(await page.locator('.focus-page-nav button').last().isEnabled(),true);await page.locator('.focus-page-nav button').last().click();await page.waitForTimeout(80);}throw Error('Input unreachable');}
 await page.goto(`http://127.0.0.1:${server.address().port}`);await open();await find();await page.locator('#'+id).fill('mi');await page.locator('#'+id).press('ArrowLeft');await page.waitForTimeout(180);
 assert.equal(await page.evaluate(()=>document.activeElement.id),id,'Focus must survive an ordinary layout pass');
 assert.equal(await page.locator('#'+id).evaluate(n=>n.selectionStart),1);
 await page.setViewportSize({width,height:Math.max(260,Math.round(height*.65))});await page.waitForTimeout(250);
 assert.equal(await page.evaluate(()=>document.activeElement.id),id,'Keyboard resize must not detach the active field');
 assert.equal(await page.locator('#'+id).evaluate(n=>n.selectionStart),1,'Cursor remains where the learner put it');assert.equal(await hit(),true,'Active field remains touchable');
 const profile=await page.evaluate(()=>JSON.parse(localStorage.getItem('p')));assert.equal(profile.xp,321);assert.deepEqual(profile.completed,[]);assert.equal(profile.teacher_id,'ren');assert.equal(await page.locator(extra?'#ex-next':'#advance').isEnabled(),false);
 await page.screenshot({path:fileURLToPath(new URL(`${extra?'extra':'main'}-${width}-${height}-${scale}.png`,out))});report.views++;
 await page.setViewportSize({width,height});await page.reload();await open();await find();assert.equal(await page.locator('#'+id).inputValue(),'mi');assert.equal((await page.evaluate(()=>JSON.parse(localStorage.getItem('p')))).xp,321);assert.deepEqual(errors,[]);
 report.cases.push({width,height,scale,extra,focusPreserved:true,cursorPreserved:true,draftAfterRestart:true,noUnlock:true});await ctx.close();
}report.passed=true;}finally{writeFileSync(new URL('report.json',out),JSON.stringify(report,null,2));await browser.close();server.close();}
console.log(JSON.stringify(report));

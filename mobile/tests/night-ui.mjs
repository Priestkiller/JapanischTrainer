import {createRequire} from 'node:module';
import {mkdirSync,writeFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
import {previewServer} from '../tools/preview-server.mjs';
const require=createRequire(import.meta.url),{chromium}=require(process.env.JT_NODE_MODULES+'/playwright');
const out=new URL('../../validation/night-1112/',import.meta.url);mkdirSync(out,{recursive:true});
const server=await previewServer(),browser=await chromium.launch({headless:true,channel:'msedge'});
const report={passed:false,realDevice:false,simulatedAudio:true,formats:[],views:0};let page;
try{
 for(const [width,height,scale] of [[412,915,1],[393,851,1],[320,640,1],[844,390,1],[412,915,1.6]]){
  const ctx=await browser.newContext({viewport:{width,height},hasTouch:true});page=await ctx.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.addInitScript(scale=>{window.calls=[];window.AndroidTrainer={getProfile:()=>localStorage.getItem('night-profile')??'{}',saveProfile:s=>{localStorage.setItem('night-profile',s);return true;},getCapabilities:()=>'{"native":true,"models":true}',stopAudio:()=>{},stopRecording:()=>{},speak:(text,teacher,speed,id)=>calls.push({kind:'audio',id}),recordKana:id=>calls.push({kind:'record',id}),record:id=>calls.push({kind:'record',id})};document.addEventListener('DOMContentLoaded',()=>document.documentElement.style.fontSize=16*scale+'px');},scale);
  await page.goto(`http://127.0.0.1:${server.address().port}`);await page.waitForSelector('html[data-ready=true]');
  async function capture(name){assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).colorScheme),'dark');assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true,name+' no horizontal clipping');report.views++;await page.screenshot({path:fileURLToPath(new URL(`${name}-${width}-${height}-${scale}.png`,out))});}
  for(const route of ['home','course','review','teachers','more']){await page.locator(`[data-page=${route}]`).click();await capture(route);}
  for(const route of ['library','grammar','progress','settings','daily','practice-lab','talk','speech-lab']){await page.locator('[data-page=more]').click();await page.locator(`[data-nav=${route}]`).click();await capture(route);}
  await page.locator('[data-page=home]').click();await page.locator('#hero-resume').click();if(await page.locator('.focus-sheet:not([hidden])').count())await page.locator('.focus-sheet-close').click();
  await page.waitForTimeout(150);await capture('speaking');
  const geometry=await page.evaluate(()=>{const t=document.querySelector('.focus-teacher').getBoundingClientRect(),p=document.querySelector('.focus-speaking-paper').getBoundingClientRect(),d=document.querySelector('.focus-dock').getBoundingClientRect(),tools=document.querySelector('.focus-tools').getBoundingClientRect();return {scene:document.querySelector('.focus-session').classList.contains('focus-coach-scene'),teacher:t.toJSON(),paper:p.toJSON(),dock:d.toJSON(),tools:tools.toJSON(),outer:document.documentElement.scrollHeight-innerHeight};});
  assert.ok(geometry.outer<=1&&geometry.dock.bottom<=height+1);
  assert.ok(geometry.teacher.top>=0&&geometry.teacher.bottom<=geometry.dock.top+1);
  if(geometry.scene){assert.ok(geometry.teacher.width>=120);assert.ok(geometry.teacher.top>=geometry.tools.bottom-1);}
  else assert.ok(geometry.teacher.bottom<=geometry.paper.top+1);
  assert.equal(await page.locator('.focus-kiko').count(),0);
  await page.locator('#hear-normal').click();await page.evaluate(()=>JTNative('audioDone',{request:calls.at(-1).id}));await page.locator('#record').click();await page.evaluate(()=>JTNative('speechResult',{request:calls.at(-1).id,text:'あ',audioQualified:true,shortKana:true}));await page.locator('#advance').click();
  assert.equal(await page.locator('.focus-teacher').count(),0);await capture('meaning');assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('night-profile')).xp),0);
  assert.deepEqual(errors,[]);report.formats.push({width,height,scale,geometry});await ctx.close();
 }report.passed=true;
}catch(e){if(page)await page.screenshot({path:fileURLToPath(new URL('failure.png',out))});throw e;}
finally{writeFileSync(new URL('report.json',out),JSON.stringify(report,null,2));await browser.close();server.close();}
console.log(JSON.stringify({passed:report.passed,views:report.views,formats:report.formats.length}));

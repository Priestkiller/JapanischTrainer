import {createRequire} from 'node:module';
import {mkdirSync,writeFileSync} from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {previewServer} from '../tools/preview-server.mjs';
const require=createRequire(import.meta.url),{chromium}=require(path.join(process.env.JT_NODE_MODULES,'playwright'));
const output=new URL('../test-results/focus/',import.meta.url);mkdirSync(output,{recursive:true});
const server=await previewServer(),browser=await chromium.launch({headless:true,channel:process.env.JT_BROWSER_CHANNEL});
const report={passed:false,simulatedNativeEvents:true,humanMicrophone:false,viewports:[]};
try{
 for(const [width,height] of [[320,640],[412,915],[844,390],[768,1024]]){
  const context=await browser.newContext({viewport:{width,height},isMobile:true,hasTouch:true});
  await context.addInitScript(()=>{window.calls=[];window.AndroidTrainer={
   getProfile:()=>localStorage.getItem('focus-profile')??'{}',saveProfile:s=>{localStorage.setItem('focus-profile',s);return true;},getCapabilities:()=>JSON.stringify({native:true,models:true}),
   speak:(text,sid,speed,id)=>calls.push({kind:'audio',id}),recordKana:id=>calls.push({kind:'kana',id}),record:id=>calls.push({kind:'word',id}),
   playRecording:(original,id)=>calls.push({kind:'own',original,id}),stopAudio:()=>{},stopRecording:cancel=>calls.push({kind:'stop',cancel})};});
  const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}`);await page.waitForSelector('html[data-ready=true]');await page.locator('#hero-resume').click();
  async function dock(){const d=await page.locator('.focus-dock').boundingBox();assert.ok(d.y>=0&&d.y+d.height<=height+1);assert.equal(await page.locator('.focus-primary:visible').count(),1);assert.equal(await page.locator('.bottom-nav').isVisible(),false);assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));}
  async function listen(){await page.locator('#hear-normal').click();await page.evaluate(()=>JTNative('audioDone',{request:calls.filter(c=>c.kind==='audio').at(-1).id}));}
  async function start(){await page.locator('#record').click();const c=await page.evaluate(()=>calls.at(-1));assert.equal(c.kind,'kana');await page.evaluate(id=>JTNative('recording',{request:id}),c.id);return c.id;}
  await dock();await listen();let id=await start();
  await page.evaluate(id=>JTNative('speechLevel',{request:id,level:.4,seconds:1.2}),id);
  assert.equal(await page.locator('#mic-level').evaluate(e=>e.value),.4);assert.equal(await page.locator('#mic-time').innerText(),'0:01');
  await page.screenshot({path:path.join(output.pathname.replace(/^\/([A-Z]:)/,'$1'),`record-${width}.png`)});
  await page.locator('#lesson-cancel').click();
  await page.evaluate(id=>JTNative('speechResult',{request:id,text:'あ',audioQualified:true,shortKana:true}),id);
  assert.equal(await page.locator('#advance').isDisabled(),true);assert.equal(await page.locator('#confirm-short-speech').count(),0);
  await listen();id=await start();await page.evaluate(id=>JTNative('speechError',{request:id,message:'Keine sichere Stimme erkannt.'}),id);
  assert.equal(await page.locator('#confirm-short-speech').count(),0);
  id=await start();await page.evaluate(id=>{JTNative('recognizing',{request:id});JTNative('speechResult',{request:id,text:'',audioQualified:true,shortKana:true});},id);
  await dock();assert.equal(await page.locator('#advance').isDisabled(),true);
  const profile=await page.evaluate(()=>JSON.parse(localStorage.getItem('focus-profile')));assert.equal(profile.study_cards['0:0:0'].mistakes,0);assert.equal(profile.xp,0);
  await page.locator('#lesson-own').click();assert.equal(await page.evaluate(()=>calls.at(-1).original),id);
  await page.evaluate(()=>JTNative('audioDone',{request:calls.at(-1).id}));
  await page.locator('#confirm-short-speech').click();await dock();
  await page.screenshot({path:path.join(output.pathname.replace(/^\/([A-Z]:)/,'$1'),`self-check-${width}.png`)});
  await page.locator('#advance').click();assert.equal(await page.locator('#lesson-own').count(),0);
  assert.equal(await page.locator('.focus-progress-row>span').innerText(),'2 / 6');
  await page.locator('#show-hint').click();assert.equal(await page.locator('#advance').isDisabled(),true);
  assert.equal(errors.length,0,errors.join('\n'));report.viewports.push({width,height,dockReachable:true,qualifiedSelfCheck:true,cancelAndStaleIgnored:true,ownRecordingExplicit:true});await context.close();
 }
 report.passed=true;
}finally{writeFileSync(new URL('report.json',output),JSON.stringify(report,null,2));await browser.close();server.close();}
console.log(JSON.stringify(report,null,2));

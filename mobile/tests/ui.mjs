import {createRequire} from 'node:module';
import {mkdirSync,writeFileSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import assert from 'node:assert/strict';
import {previewServer} from '../tools/preview-server.mjs';
const require=createRequire(import.meta.url);
const {chromium}=require(process.env.JT_NODE_MODULES?path.join(process.env.JT_NODE_MODULES,'playwright'):'playwright');
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const output=path.join(root,'test-results');mkdirSync(output,{recursive:true});
const server=await previewServer();const url=`http://127.0.0.1:${server.address().port}`;
const browser=await chromium.launch({headless:true,channel:process.env.JT_BROWSER_CHANNEL||undefined});
const report={passed:false,kind:'Browser viewport and sequential-flow tests; simulated native events, real model tests are separate',viewports:[],checks:[]};
try {
 for(const [width,height] of [[320,640],[360,800],[390,844],[412,892],[412,915],[844,390],[768,1024]]) {
  const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1,isMobile:true,hasTouch:true});
  await context.addInitScript(()=>{
   window.testCalls=[];
   window.AndroidTrainer={
    getProfile:()=>localStorage.getItem('jt-test-profile')??'{}',
    saveProfile:json=>{localStorage.setItem('jt-test-profile',json);return true;},
    getCapabilities:()=>JSON.stringify({native:true,models:true,version:'UI-Test'}),
    speak:(text,sid,speed,request)=>window.testCalls.push({type:'audio',request,text}),
    record:request=>window.testCalls.push({type:'speech',request}),
    stopAudio:()=>{},stopRecording:()=>{}
   };
  });
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(url);await page.waitForSelector('html[data-ready=true]');await page.locator('#teacher-canvas').waitFor();
  await page.screenshot({path:path.join(output,`home-${width}x${height}.png`),fullPage:true});
  if(width===412&&height===892) await page.screenshot({path:path.join(output,'s24-ultra-layout-preview.png')});
  async function noOverflow(label) {
   const dimensions=await page.evaluate(()=>({screen:innerWidth,body:document.documentElement.scrollWidth}));
   assert.ok(dimensions.body<=dimensions.screen+1,`${label}: horizontal overflow at ${width}×${height}: ${JSON.stringify(dimensions)}`);
   const tiny=await page.locator('button:visible').evaluateAll(buttons=>buttons.filter(b=>{const r=b.getBoundingClientRect();return r.height<43||r.width<35}).map(b=>b.textContent));
   assert.deepEqual(tiny,[],`${label}: touch targets too small`);
  }
  await noOverflow('home');
  await page.locator('#hero-resume').click();await page.locator('#record').waitFor();await noOverflow('lesson');
  assert.equal(await page.locator('#step-count').textContent(),'Schritt 1/6');
  assert.equal(await page.locator('#advance').isDisabled(),true);assert.equal(await page.locator('#record').isDisabled(),true);
  assert.ok((await page.locator('.pronunciation').innerText()).includes('wie a in Mann'));
  await page.screenshot({path:path.join(output,`lesson-${width}x${height}.png`),fullPage:true});
  async function audioDone(selector) {
   await page.locator(selector).click();
   await page.evaluate(()=>{const call=window.testCalls.filter(c=>c.type==='audio').at(-1);window.JTNative('audioDone',{request:call.request});});
  }
  async function recognize(text) {
   await page.locator('#record').click();
   await page.evaluate(text=>{const call=window.testCalls.filter(c=>c.type==='speech').at(-1);window.JTNative('recording',{request:call.request});window.JTNative('recognizing',{request:call.request});window.JTNative('speechResult',{request:call.request,text});},text);
  }
  await page.locator('#hear-normal').click();
  await page.evaluate(()=>{const call=window.testCalls.at(-1);window.JTNative('audioError',{request:call.request,message:'Test: Kein Audio'});});
  assert.equal(await page.locator('#record').isDisabled(),true);
  assert.equal(await page.locator('#confirm-short-speech').count(),0);
  await audioDone('#hear-normal');await recognize('falsch');assert.equal(await page.locator('#advance').isDisabled(),true);
  assert.equal(await page.locator('#confirm-short-speech').count(),1);
  await recognize('あ');assert.equal(await page.locator('#advance').isDisabled(),false);
  await page.locator('#advance').click();assert.ok(await page.locator('[data-choice]').count());
  assert.equal(await page.locator('#step-count').textContent(),'Schritt 2/6');
  for(const selector of ['#record','#hear-normal','.romaji','.translation','details'])assert.equal(await page.locator(selector).count(),0,selector);
  await page.evaluate(()=>{const old=window.testCalls.filter(c=>c.type==='speech').at(-1);window.JTNative('speechResult',{request:old.request,text:'あ'});});
  assert.equal(await page.locator('#advance').isDisabled(),true,'Late speech result cannot solve the next exercise');
  await page.screenshot({path:path.join(output,`meaning-${width}x${height}.png`),fullPage:true});
  await page.reload();await page.waitForSelector('html[data-ready=true]');await page.locator('#hero-resume').click();await page.locator('[data-choice]').first().waitFor();
  await page.getByRole('button',{name:'Laut i',exact:true}).click();assert.equal(await page.locator('#advance').isDisabled(),true);
  await page.getByRole('button',{name:'Laut a',exact:true}).click();await page.locator('#advance').click();
  assert.equal(await page.locator('#step-count').textContent(),'Schritt 3/6');
  assert.equal(await page.locator('[data-choice]').first().isDisabled(),true);
  for(const selector of ['#record','#without-audio','.exercise-prompt','.romaji'])assert.equal(await page.locator(selector).count(),0);
  await audioDone('#hear-task');await page.getByRole('button',{name:'Laut a',exact:true}).click();await page.locator('#advance').click();
  assert.equal(await page.locator('#step-count').textContent(),'Schritt 4/6');
  await page.getByRole('button',{name:'a',exact:true}).click();await page.locator('#advance').click();
  assert.equal(await page.locator('#step-count').textContent(),'Schritt 5/6');
  for(const selector of ['#record','.romaji','details'])assert.equal(await page.locator(selector).count(),0);
  await page.locator('#romaji-input').fill('wrong');await page.locator('#write-form button').click();assert.equal(await page.locator('#advance').isDisabled(),true);
  await page.locator('#romaji-input').fill('a');await page.locator('#write-form button').click();assert.equal(await page.locator('#advance').isDisabled(),false);
  await page.locator('#advance').click();assert.equal(await page.locator('#step-count').textContent(),'Schritt 6/6');
  await page.getByRole('button',{name:'Ein Zeichen für den Laut a.',exact:true}).click();await page.locator('#advance').click();
  assert.equal(await page.locator('#step-count').textContent(),'Schritt 1/6');assert.equal(await page.locator('.romaji').first().innerText(),'i');assert.equal(await page.locator('#advance').isDisabled(),true);
  assert.equal(await page.locator('#confirm-short-speech').count(),0);await audioDone('#hear-normal');await recognize('いい？');
  assert.equal(await page.locator('#advance').isDisabled(),true);await page.locator('#confirm-short-speech').click();assert.equal(await page.locator('#advance').isDisabled(),false);
  assert.ok((await page.locator('#task-feedback').innerText()).includes('Selbstprüfung'));
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('jt-test-profile')).speech_scores['い'].last),0);
  await page.locator('#settings-shortcut').click();await noOverflow('settings');
  await page.screenshot({path:path.join(output,`settings-${width}x${height}.png`),fullPage:true});
  await page.locator('[data-page=teachers]').click();await page.locator('[data-teacher=yuki]').click();await page.locator('#select-teacher').click();
  assert.equal(await page.locator('#select-teacher').innerText(),'✓ Ausgewählt');await noOverflow('teachers');
  await page.locator('[data-page=course]').click();await page.locator('#course-search').fill('ありがとう');assert.ok(await page.locator('[data-lesson]').count());await noOverflow('search');
  await page.locator('#settings-shortcut').click();await page.locator('#licenses').click();await page.locator('.licenses').waitFor();await noOverflow('licenses');
  assert.equal(errors.length,0,errors.join('\n'));
  report.viewports.push({width,height,horizontalOverflow:false,touchTargets:true,resume:true,allSixSequentialSteps:true,speakingRequired:true,noAnswerCardInLaterSteps:true,staleSpeechIgnored:true,writeValidation:true,teacherSelection:true,search:true});
  await context.close();
 }
 report.passed=true;console.log(JSON.stringify(report,null,2));
} finally {writeFileSync(path.join(output,'ui-report.json'),JSON.stringify(report,null,2));await browser.close();server.close();}

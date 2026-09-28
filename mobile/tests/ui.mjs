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
    speak:(text,sid,speed,request)=>window.testCalls.push({type:'audio',request,text,sid,speed}),
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
  assert.ok((await page.locator('.lesson-goal').innerText()).includes('Vokale'));
  assert.equal(await page.locator('.lesson-guide[open]').count(),1);
  await noOverflow('foundation-guide');
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
  await page.locator('#show-hint').click();assert.equal(await page.locator('.exercise-hint').count(),1);
  assert.equal(await page.locator('#advance').isDisabled(),true,'Opening a hint does not solve the task');
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('jt-test-profile')).study_cards['0:0:0'].hints),1);
  await noOverflow('exercise-hint');await page.locator('#show-hint').click();
  assert.equal(await page.locator('.exercise-hint').count(),0);
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
  await page.locator('#romaji-input').fill('wrong');await page.locator('#check-write').click();assert.equal(await page.locator('#advance').isDisabled(),true);
  await page.locator('#romaji-input').fill('a');await page.locator('#check-write').click();assert.equal(await page.locator('#advance').isDisabled(),false);
  await page.locator('#advance').click();assert.equal(await page.locator('#step-count').textContent(),'Schritt 6/6');
  await page.getByRole('button',{name:'Ein Zeichen für den Laut a.',exact:true}).click();await page.locator('#advance').click();
  assert.equal(await page.locator('#step-count').textContent(),'Schritt 1/6');assert.equal(await page.locator('.romaji').first().innerText(),'i');assert.equal(await page.locator('#advance').isDisabled(),true);
  assert.equal(await page.locator('#confirm-short-speech').count(),0);await audioDone('#hear-normal');await recognize('いい？');
  assert.equal(await page.locator('#advance').isDisabled(),true);await page.locator('#confirm-short-speech').click();assert.equal(await page.locator('#advance').isDisabled(),false);
  assert.ok((await page.locator('#task-feedback').innerText()).includes('Selbstprüfung'));
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('jt-test-profile')).speech_scores['い'].last),0);
  await page.getByRole('button',{name:'Übung pausieren und zurück',exact:true}).click();await page.locator('#settings-shortcut').click();await noOverflow('settings');
  await page.screenshot({path:path.join(output,`settings-${width}x${height}.png`),fullPage:true});
  await page.locator('[data-page=teachers]').click();await page.locator('[data-teacher=yuki]').click();await page.locator('#select-teacher').click();
  assert.equal(await page.locator('#select-teacher').innerText(),'✓ Ausgewählt');await noOverflow('teachers');
  await page.locator('[data-page=course]').click();await page.locator('#course-search').fill('ありがとう');assert.ok(await page.locator('[data-lesson]').count());await noOverflow('search');
  await page.locator('#settings-shortcut').click();await page.locator('#licenses').click();await page.locator('.licenses').waitFor();await noOverflow('licenses');
  await page.locator('[data-page=review]').click();await page.getByRole('button',{name:'Gespräche üben →',exact:true}).click();await noOverflow('talk-hub');
  assert.equal(await page.locator('[data-talk-scene]').count(),5);
  await page.screenshot({path:path.join(output,`talk-hub-${width}x${height}.png`),fullPage:true});
  await page.locator('[data-talk-scene=cafe]').click();await noOverflow('conversation');
  assert.equal(await page.locator('.chat-translation').count(),0);assert.equal(await page.locator('#talk-send').isDisabled(),true);
  assert.equal(await page.evaluate(()=>window.testCalls.filter(c=>c.type==='audio').at(-1).sid),4,'Uses selected Yuki voice');
  await page.locator('#talk-record').click();
  await page.evaluate(()=>{const call=window.testCalls.filter(c=>c.type==='speech').at(-1);window.JTNative('speechError',{request:call.request,message:'Mikrofonzugriff nicht erlaubt.'});});
  assert.equal(await page.locator('#talk-send').isDisabled(),true);assert.equal(await page.locator('#talk-record').isDisabled(),false);
  async function talkRecognize(text) {
   await page.locator('#talk-record').click();
   await page.evaluate(text=>{const call=window.testCalls.filter(c=>c.type==='speech').at(-1);window.JTNative('recording',{request:call.request});window.JTNative('recognizing',{request:call.request});window.JTNative('speechResult',{request:call.request,text});},text);
  }
  async function talkSend(text) {await page.locator('#talk-draft').fill(text);await page.locator('#talk-send').click();}
  await talkRecognize('お茶をください。');assert.equal(await page.locator('#talk-draft').inputValue(),'お茶をください。');assert.equal(await page.locator('.from-user').count(),0,'Recognition alone does not submit a wrong transcript');
  await talkSend('コーヒーをお願いします。');assert.ok((await page.locator('.from-teacher').last().innerText()).includes('コーヒー'));
  assert.ok((await page.locator('.from-user').last().innerText()).includes('Text'));
  await page.locator('#talk-translation').click();await page.locator('#talk-reading').click();assert.ok(await page.locator('.chat-translation').count());assert.ok(await page.locator('.chat-reading').count());
  await page.screenshot({path:path.join(output,`talk-cafe-${width}x${height}.png`),fullPage:true});
  await talkSend('コーヒーはいりません。');assert.ok((await page.locator('.talk-composer').innerText()).includes('Offline-Szene'));
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('jt-test-profile')).talk.sessions.cafe.node),'temperature');
  await talkRecognize('冷たいものをお願いします。');
  await page.reload();await page.waitForSelector('html[data-ready=true]');await page.locator('[data-nav=talk]').click();await page.locator('[data-talk-scene=cafe]').click();
  assert.equal(await page.locator('#talk-draft').inputValue(),'冷たいものをお願いします。');assert.ok((await page.locator('.talk-partner').innerText()).includes('Yuki'));
  await page.locator('#talk-record').click();const stale=await page.evaluate(()=>window.testCalls.filter(c=>c.type==='speech').at(-1).request);
  await page.locator('[data-nav=talk]').click();await page.locator('[data-talk-scene=weekend]').click();
  await page.evaluate(request=>window.JTNative('speechResult',{request,text:'映画を見たいです。'}),stale);
  assert.equal(await page.locator('#talk-draft').inputValue(),'');assert.equal(await page.locator('.from-user').count(),0,'Old recording cannot answer another scene');
  await page.locator('[data-nav=talk]').click();await page.locator('[data-talk-scene=cafe]').click();await page.locator('#talk-send').click();
  await talkSend('小さいサイズでお願いします。');await talkSend('持ち帰りでお願いします。');await talkSend('カードでお願いします。');
  await page.locator('.talk-complete').waitFor();assert.equal(await page.locator('#talk-record').count(),0);await noOverflow('talk-completed');
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('jt-test-profile')).talk.completed.cafe),1);
  assert.equal(await page.evaluate(()=>JSON.parse(localStorage.getItem('jt-test-profile')).xp),0,'Conversation does not bypass lesson XP');
  assert.equal(errors.length,0,errors.join('\n'));
  report.viewports.push({width,height,horizontalOverflow:false,touchTargets:true,resume:true,allSixSequentialSteps:true,speakingRequired:true,noAnswerCardInLaterSteps:true,staleSpeechIgnored:true,writeValidation:true,teacherSelection:true,search:true,conversationBranching:true,editableTranscript:true,talkResume:true,microphoneErrorRecoverable:true,staleTalkResultsIgnored:true});
  await context.close();
 }
 report.passed=true;console.log(JSON.stringify(report,null,2));
} finally {writeFileSync(path.join(output,'ui-report.json'),JSON.stringify(report,null,2));await browser.close();server.close();}

import {createRequire} from 'node:module';
import {mkdirSync,writeFileSync} from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import {previewServer} from '../tools/preview-server.mjs';
const require=createRequire(import.meta.url);
const {chromium}=require(path.join(process.env.JT_NODE_MODULES,'playwright'));
const out=new URL('../test-results/update-channels/',import.meta.url);mkdirSync(out,{recursive:true});
const server=await previewServer();const browser=await chromium.launch({headless:true,channel:'msedge'});
const report={passed:false,bridge:'simulated',viewports:[]};
try {
 for(const [width,height] of [[320,640],[412,915],[844,390]]) {
  const context=await browser.newContext({viewport:{width,height},isMobile:true,hasTouch:true});
  await context.addInitScript(()=>{
   window.updateCalls=[];
   window.AndroidTrainer={getProfile:()=>'{"xp":321,"teacher_id":"ren"}',saveProfile:()=>true,
    getCapabilities:()=>JSON.stringify({native:true,models:true,version:'11.0.4-android.1'}),stopAudio:()=>{},stopRecording:()=>{},
    checkUpdates:()=>{updateCalls.push('stable');JTNative('updateChecking',{test:false});},
    checkTestUpdates:()=>{updateCalls.push('test');JTNative('updateChecking',{test:true});},
    installUpdate:()=>{updateCalls.push('install');JTNative('updateProgress',{done:1,total:10});}};
  });
  const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
  await page.goto(`http://127.0.0.1:${server.address().port}`);await page.waitForSelector('html[data-ready=true]');
  await page.locator('#settings-shortcut').click();assert.equal((await page.evaluate(()=>updateCalls)).length,0);
  await page.locator('#check-test-updates').click();assert.equal(await page.locator('#check-updates').isDisabled(),true);
  await page.evaluate(()=>JTNative('updateAvailable',{test:true,name:'11.0.5-android.1-test',notes:'Testangebot'}));
  assert.equal(await page.locator('#install-update').innerText(),'Testversion herunterladen');
  await page.locator('#install-update').click();assert.equal(await page.locator('#check-test-updates').isDisabled(),true);
  await page.evaluate(()=>JTNative('updateReady'));
  await page.locator('#check-updates').click();assert.equal(await page.locator('#install-update').count(),0);
  await page.evaluate(()=>JTNative('updateError',{message:'Offline-Test'}));
  assert.equal(await page.locator('#install-update').count(),0);assert.ok((await page.locator('#updates-box').innerText()).includes('Offline-Test'));
  await page.locator('#check-test-updates').click();await page.evaluate(()=>JTNative('updateCurrent',{test:true}));
  assert.ok((await page.locator('#updates-box').innerText()).includes('Keine neuere Testversion verfügbar.'));
  assert.deepEqual(await page.evaluate(()=>updateCalls),['test','install','stable','test']);
  assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));assert.deepEqual(errors,[]);
  await page.locator('#updates-box').scrollIntoViewIfNeeded();await page.screenshot({path:new URL(`${width}.png`,out).pathname.replace(/^\/(\w:)/,'$1')});
  report.viewports.push({width,height,passed:true});await context.close();
 }
 report.passed=true;
} finally {writeFileSync(new URL('report.json',out),JSON.stringify(report,null,2));await browser.close();await new Promise(r=>server.close(r));}
console.log(JSON.stringify(report));

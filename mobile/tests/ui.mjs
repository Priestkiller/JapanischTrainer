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
const report={passed:false,kind:'Browser viewport tests; native Android tests are separate',viewports:[],checks:[]};
try {
 for(const [width,height] of [[320,640],[360,800],[390,844],[412,892],[412,915],[844,390],[768,1024]]) {
  const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1,isMobile:true,hasTouch:true});
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
  assert.ok((await page.locator('.pronunciation').innerText()).includes('wie a in Mann'));
  await page.screenshot({path:path.join(output,`lesson-${width}x${height}.png`),fullPage:true});
  await page.locator('#advance').click();assert.ok(await page.locator('[data-choice]').count());
  await page.reload();await page.waitForSelector('html[data-ready=true]');await page.locator('#hero-resume').click();await page.locator('[data-choice]').first().waitFor();
  await page.getByRole('button',{name:'Laut a',exact:true}).click();await page.locator('#advance').click();
  await page.locator('#without-audio').click();await page.getByRole('button',{name:'Laut a',exact:true}).click();await page.locator('#advance').click();
  await page.getByRole('button',{name:'a',exact:true}).click();await page.locator('#advance').click();
  await page.locator('#romaji-input').fill('wrong');await page.locator('#write-form button').click();assert.equal(await page.locator('#advance').isDisabled(),true);
  await page.locator('#romaji-input').fill('a');await page.locator('#write-form button').click();assert.equal(await page.locator('#advance').isDisabled(),false);
  await page.locator('#settings-shortcut').click();await noOverflow('settings');
  await page.screenshot({path:path.join(output,`settings-${width}x${height}.png`),fullPage:true});
  await page.locator('[data-page=teachers]').click();await page.locator('[data-teacher=yuki]').click();await page.locator('#select-teacher').click();
  assert.equal(await page.locator('#select-teacher').innerText(),'✓ Ausgewählt');await noOverflow('teachers');
  await page.locator('[data-page=course]').click();await page.locator('#course-search').fill('ありがとう');assert.ok(await page.locator('[data-lesson]').count());await noOverflow('search');
  await page.locator('#settings-shortcut').click();await page.locator('#licenses').click();await page.locator('.licenses').waitFor();await noOverflow('licenses');
  assert.equal(errors.length,0,errors.join('\n'));
  report.viewports.push({width,height,horizontalOverflow:false,touchTargets:true,resume:true,writeValidation:true,teacherSelection:true,search:true});
  await context.close();
 }
 report.passed=true;console.log(JSON.stringify(report,null,2));
} finally {writeFileSync(path.join(output,'ui-report.json'),JSON.stringify(report,null,2));await browser.close();server.close();}

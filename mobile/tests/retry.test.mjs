import test from 'node:test';import assert from 'node:assert/strict';import {readFileSync} from 'node:fs';
import {Course,Store,Session,PHASES} from '../web/core.mjs';
const read=n=>JSON.parse(readFileSync(new URL('../../data/'+n,import.meta.url),'utf8'));
const setup=(p={})=>new Course(read('course.json'),read('catalog.json'),read('deep_lessons.json'),new Store(p));
function pass(s){if(s.mode==='recap')s.choose(s.answers().correct);else if(s.phase==='speak'){s.audio_seen=true;s.checkSpeech(s.card.jp);}else if(s.phase==='write')s.checkWrite(s.card.romaji);else if(s.phase==='build'&&s.course.blocks(s.card,s.lesson).length){s.tokens=s.course.blocks(s.card,s.lesson).map((_,i)=>i);s.checkBuild();}else{s.audio_seen=true;s.choose(s.answers().correct);}}
function fail(s){if(s.phase==='write')s.checkWrite('nichtpassend');else if(s.phase==='build'&&s.course.blocks(s.card,s.lesson).length){s.tokens=[];s.checkBuild();}else{s.audio_seen=true;s.choose(s.answers().options.find(o=>o!==s.answers().correct));}}
test('Each actual non-speech mistake queues the original task once, without passing it',()=>{
 const c=setup(),l=c.byKey.get('v11:long-vowels');
 for(const phase of PHASES.slice(1)){const s=new Session(l,c,false);s.index=4;s.phase=phase;s.passed=PHASES.slice(0,PHASES.indexOf(phase));s.reset();fail(s);assert.equal(s.success,false);assert.equal(s.advance(),'blocked');assert.equal(s.canDefer,true);assert.equal(s.retryTasks.length,1);assert.equal(s.retryTasks[0].phase,phase);const heard=s.listenCard;fail(s);assert.equal(s.retryTasks.length,1);if(phase==='listen')assert.equal(s.lesson.cards[s.retryTasks[0].listen_index],heard);assert.equal(s.defer(),'next');assert.equal(c.store.data.xp,0);assert.equal(c.store.data.completed.length,0);}
});
test('Failed tasks repeat at the end in their own phase and rotate until solved; XP only after recap',()=>{
 const c=setup(),s=new Session(c.byKey.get('v11:long-vowels'),c,false);const seen=[];
 while(s.mode==='learn'){if(s.index===4&&['meaning','listen','build','write','apply'].includes(s.phase)){fail(s);seen.push({...s.retryTasks.at(-1)});s.defer();}else{pass(s);s.advance();}}
 assert.equal(s.mode,'retry');assert.equal(s.retryTasks.length,5);assert.equal(s.retry_total,5);assert.equal(s.store.data.xp,0);
 const initial=s.retryTasks[0];fail(s);assert.equal(s.defer(),'next');assert.deepEqual(s.retryTasks.at(-1),initial);assert.equal(s.retry_passed,0);assert.equal(s.retryTasks.length,5);
 let restored=new Session(s.lesson,setup(JSON.parse(JSON.stringify(s.store.data))));assert.equal(restored.mode,'retry');assert.deepEqual(restored.retryTasks,s.retryTasks);assert.equal(restored.index,s.index);assert.equal(restored.phase,s.phase);
 const attempts=[];while(restored.mode==='retry'){attempts.push(restored.phase);assert.equal(restored.advance(),'blocked');pass(restored);assert.equal(restored.success,true);restored.advance();}
 assert.equal(attempts.length,5);assert.equal(restored.retry_passed,5);assert.equal(restored.mode,'recap');assert.equal(restored.store.data.xp,0);let ended=false;for(let i=0;i<20;i++){pass(restored);if(restored.advance()==='complete'){ended=true;break;}}
 assert.equal(ended,true);assert.equal(restored.store.data.xp,s.lesson.xp??20);restored.store.complete(s.lesson);assert.equal(restored.store.data.xp,s.lesson.xp??20);
});
test('Old profiles keep their passed step; a forged defer without its real queue does not bypass gates',()=>{
 const c=setup({xp:45,teacher_id:'ren',completed:['0:0'],course_revision:11,lesson_sessions:{'0:1':{flow_revision:2,index:2,phase:'apply',passed:PHASES.slice(0,5),mode:'learn'}}});const s=new Session(c.byKey.get('0:1'),c);assert.equal(s.phase,'apply');assert.equal(c.store.data.xp,45);assert.equal(c.teacher().id,'ren');assert.equal(s.defer(),'blocked');
 const bad=setup({lesson_sessions:{'0:0':{flow_revision:2,index:0,phase:'apply',passed:['speak'],deferred:['meaning','listen','build','write'],retry_tasks:[{index:999,phase:'write'},{index:0,phase:'speak'}],mode:'retry'}}});const b=new Session(bad.lessons[0],bad);assert.deepEqual(b.retryTasks,[]);assert.equal(b.phase,'meaning');assert.equal(b.advance(),'blocked');assert.equal(b.defer(),'blocked');
});
test('Only real wrong answers add retries; hints, missing audio and technical speech failures do not',()=>{
 const c=setup(),s=new Session(c.lessons[0],c);s.hintOpen=true;assert.equal(s.defer(),'blocked');for(let i=0;i<3;i++){s.support.begin('t'+i);s.support.finish('t'+i,'technical');}assert.equal(s.support.unlocked,true);assert.deepEqual(s.retryTasks,[]);assert.equal(s.canDefer,false);
 pass(s);s.advance();pass(s);s.advance();s.choose(s.answers().correct);assert.deepEqual(s.retryTasks,[]);assert.equal(s.canDefer,false);assert.equal(s.success,false);
});

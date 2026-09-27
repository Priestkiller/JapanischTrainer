import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {Course,Store,Session,PHASES,FLOW_REVISION} from '../web/core.mjs';
import {TalkSession} from '../web/talk.mjs';
const read=n=>JSON.parse(readFileSync(new URL('../../data/'+n,import.meta.url),'utf8'));
const raw=read('course.json'),catalog=read('catalog.json'),deep=read('deep_lessons.json');
const setup=(p={})=>new Course(raw,catalog,deep,new Store(p));
test('Package 03: all 119 cards have usable solutions and explanatory wrong answers without unlocks',()=>{
 const c=setup(),lessons=c.lessons.filter(l=>l.study_guide?.package===3);
 assert.equal(lessons.length,25);assert.equal(lessons.reduce((n,l)=>n+l.cards.length,0),119);
 for(const l of lessons)for(let i=0;i<l.cards.length;i++) {
  const q=l.cards[i].detail.scenario;
  for(const [wrong,why] of Object.entries(q.feedback)) {
   const s=new Session(l,c,false);s.index=i;s.phase='apply';s.passed=PHASES.slice(0,5);s.reset();
   if(!s.answers().options.includes(wrong))continue;
   s.choose(wrong);assert.equal(s.success,false);assert.ok(s.feedback.includes(why));assert.equal(s.advance(),'blocked');
  }
  const s=new Session(l,c,false);s.index=i;s.phase='apply';s.passed=PHASES.slice(0,5);s.reset();s.choose(q.correct);assert.equal(s.success,true,`${l.key}:${i}`);
 }
 assert.equal(c.store.data.xp,0);assert.deepEqual(c.store.data.completed,[]);
});
test('All 25 old lesson sessions keep their earned step, completion, review and conversations',()=>{
 for(const l of setup().lessons.filter(l=>l.study_guide?.package===3)) {
  const key=l.key,p={course_revision:11,xp:456,teacher_id:'ren',completed:['0:0','14:0'],legacy_unlocked:[key],
   review:{'14:0:2':{box:3,due:9999999999}},last_lesson:{key,card:1},talk:{completed:{shopping:2},sessions:{}},
   lesson_sessions:{[key]:{flow_revision:FLOW_REVISION,index:1,phase:'write',passed:PHASES.slice(0,4),mode:'learn',recap:[],recap_total:0,recap_passed:0}}};
  const c=setup(p),s=new Session(c.byKey.get(key),c,true);
  for(const f of ['xp','teacher_id','completed','review','last_lesson','talk'])assert.deepEqual(c.store.data[f],p[f]);
  assert.equal(s.phase,'write');assert.equal(s.index,1);assert.equal(s.advance(),'blocked');
  s.hintOpen=true;assert.equal(s.advance(),'blocked');
 }
});
test('Taught cafe and shopping replies traverse two different paths each without changing conversation code',()=>{
 const paths=[['cafe',['みずをください。','ここでおねがいします。','げんきんではらいます。']],
  ['cafe',['コーヒーをください。','アイスをおねがいします。','エルサイズでおねがいします。','もちかえりでおねがいします。','カードでおねがいします。']],
  ['shopping',['これはいくらですか。','これをください。','くろをおねがいします。','カードでおねがいします。']],
  ['shopping',['これはいくらですか。','やめておきます。']]];
 for(const [scene,replies] of paths) {
  const s=new TalkSession(new Store({}),scene,'sakura');
  for(const text of replies){s.setDraft(text,'typed');assert.equal(s.respond().accepted,true,`${scene}/${s.node}: ${text}`);}
  assert.equal(s.done,true);assert.equal(s.store.data.xp,0);assert.deepEqual(s.store.data.completed,[]);
 }
});

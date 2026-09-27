import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {Course,Store,Session,PHASES,FLOW_REVISION} from '../web/core.mjs';
const read=n=>JSON.parse(readFileSync(new URL('../../data/'+n,import.meta.url),'utf8'));
const raw=read('course.json'),catalog=read('catalog.json'),details=read('deep_lessons.json');
const setup=(p={})=>new Course(raw,catalog,details,new Store(p));
test('Package 02: every authored wrong answer explains itself without giving progress',()=>{
 const c=setup(),lessons=c.lessons.filter(l=>l.study_guide?.package===2);
 assert.equal(lessons.length,25);assert.equal(lessons.reduce((n,l)=>n+l.cards.length,0),121);
 for(const l of lessons)for(let index=0;index<l.cards.length;index++)for(const [wrong,why] of Object.entries(l.cards[index].detail.scenario.feedback)) {
   const s=new Session(l,c,false);s.index=index;s.phase='apply';s.passed=PHASES.slice(0,5);s.reset();
   if(!s.answers().options.includes(wrong))continue;
   s.choose(wrong);assert.ok(s.feedback.includes(why));assert.equal(s.success,false);assert.equal(s.advance(),'blocked');
   assert.deepEqual(s.passed,PHASES.slice(0,5));assert.equal(c.store.data.review[s.key].box,0);
 }
 assert.equal(c.store.data.xp,0);assert.deepEqual(c.store.data.completed,[]);
});
test('An existing 11.0.2 profile resumes at its earned step with review and conversations preserved',()=>{
 const profile={course_revision:11,completed:['0:0','1:0','14:0'],xp:321,teacher_id:'ren',legacy_unlocked:['v11:positions'],
   review:{'14:0:2':{box:3,due:9999999999}},last_lesson:{key:'v11:positions',card:2},
   talk:{completed:{meeting:2},sessions:{}},
   lesson_sessions:{'v11:positions':{flow_revision:FLOW_REVISION,index:2,phase:'write',passed:PHASES.slice(0,4),mode:'learn',recap:[],recap_total:0,recap_passed:0}}};
 const c=setup(profile),s=new Session(c.byKey.get('v11:positions'),c,true);
 for(const key of ['xp','teacher_id','completed','legacy_unlocked','last_lesson','review','talk'])assert.deepEqual(c.store.data[key],profile[key]);
 assert.equal(s.phase,'write');assert.equal(s.index,2);assert.deepEqual(s.passed,PHASES.slice(0,4));assert.equal(s.advance(),'blocked');
 s.hintOpen=true;assert.equal(s.advance(),'blocked');assert.equal(c.store.data.xp,321);
});
test('Listening options use only introduced cards and feedback follows the heard target',()=>{
 const c=setup(),l=c.byKey.get('v11:polite-past');
 for(let index=0;index<l.cards.length;index++) {
   const s=new Session(l,c,false);s.index=index;s.phase='listen';s.reset();
   assert.ok(s.answers().options.every(v=>l.cards.slice(0,index+1).some(x=>x.de===v)));
 }
 const s=new Session(l,c,false);s.index=4;s.phase='listen';s.reset();s.listenCard=l.cards[2];s.audio_seen=true;s.choose(l.cards[1].de);
 if(s.answers().options.includes(l.cards[1].de)){assert.ok(s.feedback.includes('Vergangenheit'));assert.equal(s.success,false);}
});
test('Both single readings on the nani/nan overview are accepted, unrelated words stay blocked',()=>{
 const c=setup(),l=c.byKey.get('13:0');
 for(const reading of ['nani','nan']){const s=new Session(l,c,false);s.phase='write';s.passed=PHASES.slice(0,4);s.checkWrite(reading);assert.equal(s.success,true);}
 for(const spoken of ['なに','なん','何']){const s=new Session(l,c,false);s.audio_seen=true;s.checkSpeech(spoken);assert.equal(s.success,true);}
 const s=new Session(l,c,false);s.audio_seen=true;s.checkSpeech('どこ');assert.equal(s.success,false);assert.equal(s.confirmShortSpeech(),false);assert.equal(s.advance(),'blocked');
});
test('Targeted writing and ordering explanations never mark a step passed',()=>{
 const c=setup(),s=new Session(c.byKey.get('v11:location-action'),c,false);
 s.phase='build';s.passed=PHASES.slice(0,3);s.checkBuild();assert.match(s.feedback,/Partikel/);assert.equal(s.advance(),'blocked');
 s.phase='write';s.passed=PHASES.slice(0,4);s.reset();s.checkWrite('wrong');assert.match(s.feedback,/Bewegungsziel/);assert.equal(s.advance(),'blocked');
 assert.equal(c.store.data.xp,0);
});

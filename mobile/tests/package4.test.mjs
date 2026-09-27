import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {Course,Store,Session,PHASES,FLOW_REVISION} from '../web/core.mjs';
import {TalkSession} from '../web/talk.mjs';
const read=n=>JSON.parse(readFileSync(new URL('../../data/'+n,import.meta.url),'utf8'));
const raw=read('course.json'),catalog=read('catalog.json'),deep=read('deep_lessons.json');
const setup=(p={})=>new Course(raw,catalog,deep,new Store(p));
const selected=c=>c.lessons.filter(l=>l.study_guide?.package===4);

test('Package 04: 123 cards, all six phases reject empty/wrong answers and help grants no credit',()=>{
 const c=setup();assert.equal(selected(c).length,25);assert.equal(selected(c).reduce((n,l)=>n+l.cards.length,0),123);
 for(const l of selected(c))for(let i=0;i<l.cards.length;i++)for(const phase of PHASES) {
  const s=new Session(l,c,false);s.index=i;s.phase=phase;s.passed=PHASES.slice(0,PHASES.indexOf(phase));s.reset();
  s.hintOpen=true;assert.equal(s.advance(),'blocked');s.choose('');assert.equal(s.success,false);
  if(phase==='speak') {
   s.checkSpeech(s.card.jp);assert.equal(s.success,false);s.audio_seen=true;
   s.checkSpeech('');assert.equal(s.success,false);s.checkSpeech('無関係');assert.equal(s.success,false);
   s.checkSpeech(c.speechTarget(s.card,l).target);
  } else if(phase==='write') {
   s.checkWrite('');assert.equal(s.success,false);s.checkWrite('unrelated');assert.equal(s.success,false);s.checkWrite(s.card.romaji);
  } else if(phase==='build'&&c.blocks(s.card,l).length) {
   s.tokens=[];s.checkBuild();assert.equal(s.success,false);assert.equal(s.advance(),'blocked');
   s.tokens=c.blocks(s.card,l).map((_,j)=>j);s.checkBuild();
  } else {
   if(phase==='listen'){s.choose(s.answers().correct);assert.equal(s.success,false);s.audio_seen=true;}
   for(const wrong of s.answers().options.filter(x=>x!==s.answers().correct)) {
    s.choose(wrong);assert.equal(s.success,false);assert.equal(s.advance(),'blocked');
    if(phase==='apply')assert.ok(s.feedback.includes(s.card.detail.scenario.feedback[wrong]));
   }
   s.choose(s.answers().correct);
  }
  assert.equal(s.success,true,`${l.key}:${i}/${phase}`);
 }
 assert.equal(c.store.data.xp,0);assert.deepEqual(c.store.data.completed,[]);
});

test('Package 04: all 25 old sessions and the corrected numbers card preserve earned progress',()=>{
 for(const key of [...selected(setup()).map(l=>l.key),'12:0']) {
  const index=key==='12:0'?4:1,p={course_revision:11,xp:456,teacher_id:'ren',tts_speed:.85,completed:['0:0','14:0'],legacy_unlocked:[key],
   review:{'14:0:2':{box:3,due:9999999999}},last_lesson:{key,card:index},talk:{completed:{cafe:2},sessions:{}},
   lesson_sessions:{[key]:{flow_revision:FLOW_REVISION,index,phase:'write',passed:PHASES.slice(0,4),mode:'learn',recap:[],recap_total:0,recap_passed:0}}};
  const c=setup(p),s=new Session(c.byKey.get(key),c,true);
  for(const f of ['xp','teacher_id','tts_speed','completed','review','last_lesson','talk'])assert.deepEqual(c.store.data[f],p[f]);
  assert.equal(s.phase,'write');assert.equal(s.index,index);assert.equal(s.migrated,false);assert.equal(s.advance(),'blocked');
  s.hintOpen=true;assert.equal(s.advance(),'blocked');
 }
});

test('Numbers pairs prepare the full task without speech/write/self-check bypass',()=>{
 const c=setup(),l=c.byKey.get('12:0'),s=new Session(l,c,false);s.index=4;s.reset();
 assert.equal(s.card.detail.parts.length,3);assert.equal(s.card.detail.extra.length,3);
 s.hintOpen=true;s.audio_seen=true;s.checkSpeech('ごろく');assert.equal(s.success,false);assert.equal(s.confirmShortSpeech(),false);assert.equal(s.advance(),'blocked');
 s.checkSpeech(c.speechTarget(s.card,l).target);assert.equal(s.success,true);
 s.phase='write';s.passed=PHASES.slice(0,4);s.reset();s.checkWrite('go roku');assert.equal(s.success,false);s.checkWrite(s.card.romaji);assert.equal(s.success,true);
 assert.equal(c.store.data.xp,0);
});

test('Taught weekend answers cover three activities, both days, all three times and both places',()=>{
 const routes=[['えいがをみたいです。','どようびがいいです。','ごぜんじゅうじはどうですか。','はい、いいですね。'],
  ['こうえんにいきたいです。','にちようびにしましょう。','ごごにじがいいです。','カフェのまえはどうですか。'],
  ['カフェにいきたいです。','どようびがいいです。','ごごさんじにしましょう。','はい、いいですね。']];
 const lesson=setup().byKey.get('v11:dialog-weekend');assert.ok(lesson.study_guide.points.join(' ').includes('10 Uhr'));
 for(const replies of routes) {
  const s=new TalkSession(new Store({}), 'weekend','sakura');
  for(const text of replies){s.setDraft(text,'typed');assert.equal(s.respond().accepted,true,`${s.node}/${text}`);}
  assert.equal(s.done,true);assert.ok(s.history.at(-1).jp.includes(s.slots.time));assert.ok(s.history.at(-1).jp.includes(s.slots.place));
  assert.equal(s.store.data.xp,0);assert.deepEqual(s.store.data.completed,[]);
 }
});

test('Cafe quantities and M remain unsupported routes, never diagnosed as bad pronunciation',()=>{
 const c=setup(),guide=c.byKey.get('v11:dialog-cafe').study_guide.points.join(' ');
 assert.ok(guide.includes('ohne Mengenwort'));assert.ok(guide.includes('M und Stückzahlen bleiben zusätzliche Kursübungen'));
 const s=new TalkSession(new Store({}), 'cafe','sakura');
 s.setDraft('コーヒーをひとつください。','spoken');assert.equal(s.respond().accepted,false);assert.equal(s.node,'order');
 assert.ok(s.feedback.includes('vorbereiteten Wegen'));assert.ok(!s.feedback.match(/Aussprache|Phonetik|Tonhöhe/));
 for(const text of ['コーヒーをください。','アイスをおねがいします。']){s.setDraft(text,'typed');assert.equal(s.respond().accepted,true);}
 s.setDraft('エムサイズでおねがいします。','spoken');assert.equal(s.respond().accepted,false);assert.equal(s.node,'size');
 assert.ok(s.feedback.includes('vorbereiteten Wegen'));assert.ok(!s.feedback.match(/Aussprache|Phonetik|Tonhöhe/));
 for(const text of ['エルサイズでおねがいします。','ここでおねがいします。','カードでおねがいします。']){s.setDraft(text,'typed');assert.equal(s.respond().accepted,true);}
 assert.equal(s.done,true);assert.equal(s.store.data.xp,0);
});

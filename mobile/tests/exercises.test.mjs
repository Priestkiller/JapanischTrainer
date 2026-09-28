import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {Store,Course,Session,cleanProfile} from '../web/core.mjs';
import {ExerciseBook,ExerciseRound,matches,order} from '../web/exercises.mjs';
const read=n=>JSON.parse(readFileSync(new URL('../../data/'+n,import.meta.url),'utf8'));
const book=new ExerciseBook(read('exercises.json'));
const setup=()=>{const store=new Store({xp:321,completed:['0:0'],teacher_id:'ren'});const course=new Course(read('course.json'),read('catalog.json'),read('deep_lessons.json'),store);return {store,course};};
function solve(r){const t=r.task,k=t.family;if(['echo','recall'].includes(k)){r.heard();return r.check(t.accepted_speech[0]);}
 if(k==='pairs'){for(const p of t.pairs)r.heard(p.id);r.set('pairs',Object.fromEntries(t.pairs.map(p=>[p.id,p.id])));}
 else if(['choice_gap','read'].includes(k))r.set('choice',t.answers[0]);
 else if(k==='hear_gap'){r.heard();r.set('text',t.answers[0]);}
 else{const pool=[...t.tokens],ids=t.solutions[0].map(word=>{const i=pool.findIndex(x=>x.text===word);return pool.splice(i,1)[0].id;});r.set(k==='translate'?'tokens':'slots',k==='translate'?ids:Object.fromEntries(ids.map((v,i)=>[i,v])));}
 return r.check();}
test('all 156 tasks can be solved, explanations do not pass and repetitions are bounded',()=>{
 const {store,course}=setup(),seen=new Set();const old={flow_revision:2,index:2,phase:'write',passed:['speak','meaning','listen','build']};store.data.lesson_sessions['5:0']=old;
 for(const pack of book.packs.values()){
  const r=new ExerciseRound(book,course.byKey.get(pack.lesson),store);assert.equal(r.state.stage,'intro');assert.equal(r.check('anything'),false);r.start();
  let count=0;while(r.state.stage!=='complete'&&count++<40){const t=r.task;seen.add(t.id);assert.equal(r.advance(),false);r.help(1);assert.equal(r.answer.success,false);
   if(['echo','recall'].includes(t.family)){r.heard();assert.equal(r.check(''),false);assert.equal(r.check('別の文'),false);}
   else{r.heard();for(const p of t.pairs??[])r.heard(p.id);assert.equal(r.check(),false);}
   r.help(2);assert.equal(solve(r),true,t.id);const n=r.state.outcomes.length;solve(r);assert.equal(r.state.outcomes.length,n);assert.equal(r.state.outcomes.at(-1).result,'solution');r.advance();
  }
  assert.equal(r.state.stage,'complete');assert.ok(r.state.review.length<=6);
 }
 assert.equal(seen.size,156);assert.equal(store.data.xp,321);assert.deepEqual(store.data.completed,['0:0']);assert.deepEqual(store.data.lesson_sessions['5:0'],old);assert.equal(store.data.teacher_id,'ren');
});
test('restore and export/import retain inputs, selected pairs, hint and task identity',()=>{
 const {store,course}=setup(),r=new ExerciseRound(book,course.byKey.get('5:0'),store);r.start();r.state.index=5;r.set('text','mi');r.help(1);
 const before=JSON.stringify(r.state);store.data=cleanProfile(JSON.parse(JSON.stringify(store.data)),true);assert.equal(JSON.stringify(new ExerciseRound(book,r.lesson,store).state),before);
});
test('safe comparison preserves small kana, negation and vowel length',()=>{
 assert.ok(matches('コーヒー',['こーひー'],'speech'));assert.ok(matches('koohii',['kōhī'],'romaji'));assert.ok(matches('学生です',['がくせいです','学生です'],'speech'));
 for(const [a,b] of [['のみません','のみます'],['きて','きって'],['おばさん','おばあさん'],['しや','しゃ'],['こんにちわ','こんにちは']])assert.equal(matches(a,[b],'speech'),false);
 assert.equal(matches('kohi',['kōhī'],'romaji'),false);assert.equal(matches('kani',["kan'i"],'romaji'),false);
});
test('partial gaps cannot complete the round and correct positions stay visible',()=>{
 const {store,course}=setup(),r=new ExerciseRound(book,course.byKey.get('5:0'),store);r.start();r.state.index=r.state.queue.findIndex(k=>book.tasks.get(k).family==='multi_gap');
 const t=r.task;r.set('slots',{'0':t.tokens.find(v=>v.text===t.solutions[0][0]).id});assert.equal(r.check(),false);assert.deepEqual(r.answer.per_slot,[true,false]);assert.equal(r.advance(),false);assert.ok(solve(r));
});
test('reading audio is recorded as assistance and no extra listening pass',()=>{
 const {store,course}=setup(),r=new ExerciseRound(book,course.byKey.get('v11:read-plan'),store);r.start();r.state.index=r.state.queue.findIndex(k=>book.tasks.get(k).family==='read');r.heard('target',true);assert.ok(solve(r));assert.equal(r.state.outcomes.at(-1).result,'hint');assert.equal(store.data.study_cards[r.task.card],undefined);
});
test('audio gate, stale repeat revision and technical pause cannot release a lesson',()=>{
 const {store,course}=setup(),r=new ExerciseRound(book,course.byKey.get('5:0'),store);r.start();assert.equal(r.check(r.task.audio),false);r.technical('No microphone',true);assert.equal(r.advance(),false);assert.equal(store.data.review[r.task.card],undefined);
 r.state.revision=0;r.save();assert.equal(new ExerciseRound(book,r.lesson,store).state.stage,'intro');assert.equal(store.data.xp,321);
});
test('shuffle is stable and independent for both sides',()=>{
 assert.deepEqual(order([0,1,2,3,4,5,6,7,8],'left'),[...order([0,1,2,3,4,5,6,7,8],'left')]);assert.notDeepEqual(order([0,1,2,3,4,5,6,7,8],'left'),order([0,1,2,3,4,5,6,7,8],'right'));
});
test('base task input, tokens and hint survive reload and import without advancing',()=>{
 const {store,course}=setup(),l=course.byKey.get('5:0');
 store.data.lesson_sessions[l.key]={flow_revision:2,index:3,phase:'write',passed:['speak','meaning','listen','build'],mode:'learn'};
 let s=new Session(l,course,true);s.input_text='mizu o';s.tokens=[1,0];s.hintOpen=true;s.snapshot();
 store.data=cleanProfile(JSON.parse(JSON.stringify(store.data)),true);s=new Session(l,course,true);
 assert.equal(s.input_text,'mizu o');assert.deepEqual(s.tokens,[1,0]);assert.equal(s.hintOpen,true);assert.equal(s.advance(),'blocked');assert.equal(store.data.xp,321);
});

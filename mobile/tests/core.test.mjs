import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {Course,Store,Session,PHASES,FLOW_REVISION,isShortKana,cleanProfile,matchesRomaji,speechMatch,reviewCard} from '../web/core.mjs';
const read=name=>JSON.parse(readFileSync(new URL('../../data/'+name,import.meta.url),'utf8'));
const raw=read('course.json'),catalog=read('catalog.json'),details=read('deep_lessons.json');
const setup=(profile={})=>new Course(raw,catalog,details,new Store(profile));
function pass(s) {
 if(s.mode==='recap')s.choose(s.answers().correct);
 else if(s.phase==='speak'){s.audio_seen=true;s.checkSpeech(s.course.speechTarget(s.card,s.lesson).target);}
 else if(['meaning','listen','apply'].includes(s.phase)){s.audio_seen=true;s.choose(s.answers().correct);}
 else if(s.phase==='build'){const parts=s.course.blocks(s.card,s.lesson);if(parts.length){s.tokens=parts.map((_,i)=>i);s.checkBuild();}else s.choose(s.answers().correct);}
 else s.checkWrite(s.card.romaji);
}

test('The full original course and stable IDs are available on Android',()=>{
 const c=setup();assert.equal(c.lessons.length,150);assert.equal(c.cards.length,680);
 assert.deepEqual(c.lessons.map(l=>l.key),raw.learning_order);assert.equal(c.catalog.TEACHERS.length,8);
 for(const l of c.lessons)for(const card of l.cards){assert.ok(c.profile(card,l).scenario.correct);assert.ok(c.example(card).jp);}
});
test('Legacy progress keeps XP, teacher and card; the unfinished card starts the new speaking sequence',()=>{
 const profile={completed:['0:0'],xp:275,streak:3,teacher_id:'yuki',tts_speed:.85,last_lesson:{key:'1:1',card:1},lesson_sessions:{'1:1':{index:1,phase:'write',mode:'learn'}},course_revision:11};
 const c=setup(profile),s=new Session(c.byKey.get('1:1'),c);
 assert.equal(c.store.data.xp,275);assert.equal(c.teacher().id,'yuki');assert.equal(c.store.data.tts_speed,.85);
 assert.equal(s.index,1);assert.equal(s.phase,'speak');assert.equal(s.migrated,true);assert.deepEqual(s.passed,[]);assert.deepEqual(c.store.data.completed,['0:0']);
});
test('An entire six-phase lesson plus recap is required before XP is awarded, only once',()=>{
 const c=setup(),l=c.lessons[0],s=new Session(l,c);let steps=0;
 assert.equal(s.advance(),'blocked');assert.equal(c.store.data.xp,0);
 while(steps++<200) {
  assert.equal(s.advance(),'blocked');pass(s);
  assert.equal(s.success,true);if(s.advance()==='complete')break;
 }
 assert.ok(steps>=l.cards.length*7);assert.deepEqual(c.store.data.completed,[l.key]);assert.equal(c.store.data.xp,l.xp??20);
 c.store.complete(l);assert.equal(c.store.data.xp,l.xp??20);assert.equal(c.unlocked(c.lessons[1].key),true);
});
test('Wrong answers and missing listening audio keep the step locked; skipping cannot pass',()=>{
 const c=setup(),s=new Session(c.lessons[0],c);pass(s);s.advance();
 const wrong=s.answers().options.find(o=>o!==s.answers().correct);s.choose(wrong);
 assert.equal(s.success,false);assert.equal(s.advance(),'blocked');assert.equal(s.metrics().mistakes,1);
 pass(s);s.advance();assert.equal(s.phase,'listen');s.choose(s.answers().correct);assert.equal(s.success,false);
 s.audio_skipped=true;s.choose(s.answers().correct);assert.equal(s.success,false);assert.equal(s.advance(),'blocked');
 assert.equal(s.metrics().phases.includes('listen'),false);assert.equal(c.store.data.xp,0);
 s.audio_seen=true;s.choose(s.answers().correct);assert.equal(s.success,true);assert.equal(s.advance(),'next');
});
test('Speaking must follow completed playback and match the target before step two unlocks',()=>{
 const c=setup(),s=new Session(c.lessons[0],c);
 assert.equal(s.phase,'speak');s.checkSpeech('あ');assert.equal(s.success,false);
 s.audio_seen=true;
 for(const heard of ['', 'こんにちは']){s.checkSpeech(heard);assert.equal(s.success,false);assert.equal(s.advance(),'blocked');}
 s.checkSpeech('ア。');assert.equal(s.success,true);assert.deepEqual(s.passed,['speak']);assert.equal(s.advance(),'next');assert.equal(s.phase,'meaning');
 assert.equal(s.checkSpeech('あ'),false);assert.equal(s.success,false);
});
test('Successful steps and the current exercise persist without reopening later steps',()=>{
 const c=setup(),lesson=c.lessons[0];let s=new Session(lesson,c);pass(s);
 s=new Session(lesson,setup(JSON.parse(JSON.stringify(c.store.data))));assert.equal(s.success,true);assert.equal(s.phase,'speak');s.advance();
 pass(s);s.advance();assert.equal(s.phase,'listen');
 const restored=new Session(lesson,setup(JSON.parse(JSON.stringify(s.store.data))));assert.equal(restored.phase,'listen');assert.deepEqual(restored.passed,['speak','meaning']);assert.equal(restored.advance(),'blocked');
 for(const phase of ['listen','build','write','apply']){assert.equal(restored.phase,phase);pass(restored);restored.advance();}
 assert.equal(restored.index,1);assert.equal(restored.phase,'speak');assert.deepEqual(restored.passed,[]);assert.equal(restored.advance(),'blocked');
});
test('Short kana self-check needs a real nonempty speech result and never forges an ASR match',()=>{
 const c=setup(),s=new Session(c.lessons[0],c);assert.equal(s.confirmShortSpeech(),false);
 s.audio_seen=true;assert.equal(s.confirmShortSpeech(),false);s.checkSpeech('');assert.equal(s.confirmShortSpeech(),false);
 s.checkSpeech('いい？');assert.equal(s.success,false);assert.equal(s.shortSpeechReady,true);assert.equal(s.confirmShortSpeech(),true);
 assert.equal(s.metrics().speech_self_checks,1);assert.equal(c.store.data.speech_scores['あ'].last,0);assert.equal(c.store.data.speech_scores['あ'].best,0);
 assert.equal(s.advance(),'next');assert.equal(s.phase,'meaning');assert.equal(s.confirmShortSpeech(),false);
});
test('Words never allow self-check, and a short-kana self-check is not carried across restart',()=>{
 const c=setup(),s=new Session(c.lessons[0],c);s.audio_seen=true;s.checkSpeech('いい');
 const resumed=new Session(s.lesson,setup(JSON.parse(JSON.stringify(c.store.data))));assert.equal(resumed.confirmShortSpeech(),false);
 for(const word of ['はい','こんにちは','いえ','ありがとうございます'])assert.equal(isShortKana(word),false);
 for(const kana of ['い','カ','きゃ'])assert.equal(isShortKana(kana),true);
 const lesson=c.lessons.find(l=>l.cards.some(card=>card.jp==='こんにちは'));const word=new Session(lesson,c,false);word.index=lesson.cards.findIndex(card=>card.jp==='こんにちは');word.reset();word.audio_seen=true;word.checkSpeech('違います');assert.equal(word.confirmShortSpeech(),false);assert.equal(word.advance(),'blocked');
});
test('Out-of-order saved steps and a success flag alone cannot bypass prerequisites',()=>{
 const c=setup({lesson_sessions:{'0:0':{flow_revision:FLOW_REVISION,index:0,phase:'write',passed:['meaning'],mode:'learn'}}});
 const s=new Session(c.lessons[0],c);assert.equal(s.phase,'speak');assert.equal(s.advance(),'blocked');
 s.phase='write';s.success=true;assert.equal(s.advance(),'blocked');assert.deepEqual(PHASES,['speak','meaning','listen','build','write','apply']);
});
test('Romaji requires vowel length and permits the documented spellings',()=>{
 for(const value of ['arigatō','arigatou','arigatoo'])assert.equal(matchesRomaji(value,'arigatō'),true);
 assert.equal(matchesRomaji('arigato','arigatō'),false);assert.equal(matchesRomaji('toukyou','tōkyō'),true);
 assert.equal(matchesRomaji('wrong','arigatō'),false);
});
test('Empty or wrong recognition never awards a successful text match',()=>{
 assert.equal(speechMatch('', ['ありがとう']),false);assert.equal(speechMatch('',''),false);
 assert.equal(speechMatch('こんにちは',['ありがとう']),false);
 assert.equal(speechMatch('アリガトウ。',['ありがとう']),true);assert.equal(speechMatch('ありがとうございます。',['ありがとうございます']),true);
});
test('Exports round trip, malformed imports are rejected, and course search handles Japanese',()=>{
 const c=setup({completed:['0:0'],xp:42,teacher_id:'ren'});
 assert.deepEqual(cleanProfile(JSON.parse(JSON.stringify(c.store.data)),true),c.store.data);
 for(const bad of [null,[],{completed:[],xp:-1},{completed:'all',xp:99}])assert.throws(()=>cleanProfile(bad,true));
 assert.ok(c.search('こんにちは').some(l=>l.cards.some(c=>c.jp==='こんにちは')));
 assert.equal(c.search('not-a-real-japanese-word').length,0);assert.ok(c.available().every(card=>card.lesson_key==='0:0'));
});
test('Reviews schedule weak cards earlier and do not grant lesson completion',()=>{
 const c=setup(),card=c.available()[0];reviewCard(c,false,card,1000);assert.equal(c.store.data.review[card.key].due,1060);
 reviewCard(c,true,card,1000);assert.equal(c.store.data.review[card.key].due,1600);assert.equal(c.store.data.xp,0);
});
test('Streak crosses month boundaries in local time and saves atomically through the bridge',()=>{
 const store=new Store({last_active:'2026-01-31',streak:2});store.touch(new Date(2026,1,1,12));assert.equal(store.data.streak,3);
 store.touch(new Date(2026,1,1,17));assert.equal(store.data.streak,3);
 assert.throws(()=>new Store({},()=>false).save(),/gespeichert/);
});

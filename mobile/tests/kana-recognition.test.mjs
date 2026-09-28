import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {Course,Store,Session} from '../web/core.mjs';
import {applyKanaRecognition} from '../web/kana-recognition.mjs';
const read=n=>JSON.parse(readFileSync(new URL('../../data/'+n,import.meta.url),'utf8'));
const create=()=>{const c=new Course(read('course.json'),read('catalog.json'),read('deep_lessons.json'),new Store({}));return new Session(c.lessons[0],c,false);};
test('Qualified uncertain kana creates no mistake, score, XP or automatic pass',()=>{
 for(const text of ['', 'いい', '違う']){const s=create();s.audio_seen=true;
  assert.equal(applyKanaRecognition(s,text,true),true);assert.equal(s.shortSpeechReady,true);
  assert.equal(s.metrics().mistakes,0);assert.equal(s.metrics().speech_attempts,1);
  assert.equal(s.success,false);assert.equal(s.advance(),'blocked');assert.equal(s.store.data.xp,0);
  assert.deepEqual(s.store.data.speech_scores,{});assert.deepEqual(s.store.data.review,{});
  assert.equal(s.confirmShortSpeech(),true);assert.ok(s.feedback.includes('Selbstprüfung'));
  assert.equal(s.metrics().speech_self_checks,1);assert.equal(s.advance(),'next');assert.equal(s.phase,'meaning');
 }
});
test('No qualification, no listening, other phase, recap or word cannot use kana fallback',()=>{
 const cases=[s=>{},s=>{s.audio_seen=false},s=>{s.phase='write'},s=>{s.mode='recap'},s=>{s.index=1;s.lesson={...s.lesson,cards:[s.card,{...s.card,jp:'こんにちは'}]}}];
 cases.forEach((change,i)=>{const s=create();s.audio_seen=true;change(s);assert.equal(applyKanaRecognition(s,'いい',i!==0),false);assert.equal(s.shortSpeechReady,false);assert.equal(s.success,false);});
});
test('Exact qualified kana uses the existing match and cannot score twice',()=>{
 const s=create();s.audio_seen=true;assert.equal(applyKanaRecognition(s,'あ',true),true);
 assert.equal(s.success,true);assert.equal(s.shortSpeechReady,false);assert.equal(s.metrics().speech_attempts,1);
 assert.equal(applyKanaRecognition(s,'あ',true),false);assert.equal(s.metrics().speech_attempts,1);
});
test('Restart does not restore a self-check authorization after the RAM recording is gone',()=>{
 const s=create();s.audio_seen=true;applyKanaRecognition(s,'いい',true);
 const restored=new Session(s.lesson,s.course);assert.equal(restored.shortSpeechReady,false);assert.equal(restored.confirmShortSpeech(),false);
});

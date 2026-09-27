import test from 'node:test';
import assert from 'node:assert/strict';
import {Store} from '../web/core.mjs';
import {SCENES,TalkSession,cleanTalk} from '../web/talk.mjs';
const setup=(id='cafe',data={})=>new TalkSession(new Store(data),id,'sakura');
function answer(s,text,source='typed'){s.setDraft(text,source);return s.respond();}
function follow(s,lines){for(const text of lines)assert.equal(answer(s,text).accepted,true,`${s.scene.id}/${s.node}: ${text}`);return s;}

test('All scenes, all authored hint answers and all routes lead to a valid reachable conversation',()=>{
 let checked=0;
 for(const scene of SCENES) {
  const visited=new Set();const queue=[setup(scene.id)];
  while(queue.length){const s=queue.shift();if(visited.has(s.node))continue;visited.add(s.node);
   assert.ok(s.prompt.jp&&s.prompt.romaji&&s.prompt.de);assert.ok(!s.prompt.jp.includes('undefined'));
   if(s.done)continue;
   const covered=new Set();
   for(const hint of s.current.hints){const copy=new TalkSession(new Store(JSON.parse(JSON.stringify(s.store.data))),scene.id);const result=answer(copy,hint.jp);assert.ok(result.accepted||result.repeated,`${scene.id}/${s.node}: ${hint.jp}`);if(result.accepted){covered.add(result.route);queue.push(copy);}checked++;}
   for(const route of s.current.routes)assert.ok(covered.has(route.id),`Route needs a usable example: ${scene.id}/${s.node}/${route.id}`);
  }
  assert.deepEqual([...visited].sort(),Object.keys(scene.nodes).sort(),scene.id);
 }
 assert.ok(checked>=45);
});
test('Café choices change the path and survive a restart without replaying an answer',()=>{
 const s=follow(setup(),['コーヒーをお願いします。','冷たいものをお願いします。']);
 const restored=new TalkSession(new Store(JSON.parse(JSON.stringify(s.store.data))),'cafe','ren');
 assert.equal(restored.node,'size');assert.equal(restored.teacherId,'sakura');assert.equal(restored.slots.temperature,'冷たい');assert.equal(restored.replies.length,2);
 follow(restored,['小さいサイズでお願いします。','持ち帰りでお願いします。','カードでお願いします。']);assert.equal(restored.done,true);assert.equal(restored.slots.payment,'カード');assert.match(restored.prompt.jp,/コーヒー/);
 const water=follow(setup(),['水をください。']);assert.equal(water.node,'where');assert.equal(water.replies.length,1);
});
test('Weekend closing remembers the chosen day, time and alternate meeting place',()=>{
 const s=follow(setup('weekend'),['公園に行きたいです。','日曜日にしましょう。','午後三時にしましょう。','カフェの前はどうですか。']);
 assert.equal(s.done,true);assert.match(s.prompt.jp,/日曜日の午後三時に、カフェの前/);assert.equal(s.slots.activity,'公園');
});
test('Declining a purchase is a valid conversation, not a wrong answer',()=>{
 const s=follow(setup('shopping'),['このバッグはいくらですか。','すみません、やめておきます。']);assert.equal(s.node,'declined');assert.equal(s.done,true);assert.equal(s.store.data.talk.completed.shopping,1);
});
test('Unsupported, empty or negative drink replies do not make up an order',()=>{
 const s=setup();for(const text of ['', '!!!','今日は天気がいいです。','コーヒーはいりません。','コーヒーじゃないです。']){assert.equal(answer(s,text).accepted,false);assert.equal(s.node,'order');}
 assert.equal(s.replies.length,0);assert.equal(s.store.data.xp,0);assert.match(s.feedback,/Offline/);
});
test('A spoken request to repeat stays at the same question and does not count as a completed answer',()=>{
 const s=setup('directions');const result=answer(s,'もう一度お願いします。','spoken');assert.equal(result.repeated,true);assert.equal(s.node,'destination');assert.equal(s.replies.length,0);assert.equal(s.history[1].source,'spoken');
});
test('Recognized drafts and typed corrections persist with their actual source',()=>{
 const s=setup();s.setDraft('コーヒーをお願いします。','spoken');s.save();const copy=new TalkSession(new Store(JSON.parse(JSON.stringify(s.store.data))),'cafe');
 assert.equal(copy.source,'spoken');assert.equal(copy.draft,'コーヒーをお願いします。');copy.setDraft('水をください。','typed');copy.respond();assert.equal(copy.history.at(-2).source,'typed');assert.equal(copy.slots.drink,'お水');
});
test('Finishing and restoring does not duplicate completion or unlock course lessons',()=>{
 const s=follow(setup(),['水をください。','ここで飲みます。','現金で払います。']);assert.equal(s.done,true);assert.equal(s.store.data.talk.completed.cafe,1);
 answer(s,'ありがとうございます。');const copy=new TalkSession(new Store(JSON.parse(JSON.stringify(s.store.data))),'cafe');assert.equal(copy.done,true);assert.equal(copy.store.data.talk.completed.cafe,1);assert.equal(copy.store.data.xp,0);assert.deepEqual(copy.store.data.completed,[]);
});
test('Different scenes retain separate unfinished conversations',()=>{
 const s=follow(setup(),['コーヒーをお願いします。']);const other=new TalkSession(s.store,'weekend','ren');answer(other,'映画を見たいです。');
 assert.equal(new TalkSession(s.store,'cafe').node,'temperature');assert.equal(new TalkSession(s.store,'weekend').node,'day');
});
test('Imported conversations cannot inject slot values or jump to unearned later nodes',()=>{
 const s=follow(setup(),['コーヒーをお願いします。']);const data=JSON.parse(JSON.stringify(s.store.data.talk));data.sessions.cafe.slots.drink='Injected text';data.sessions.cafe.history.at(-1).jp='Injected prompt';
 const clean=cleanTalk(data);assert.equal(clean.sessions.cafe.slots.drink,'コーヒー');assert.match(clean.sessions.cafe.history.at(-1).jp,/コーヒー/);
 data.sessions.cafe.node='done';assert.equal(cleanTalk(data).sessions.cafe,undefined);assert.deepEqual(cleanTalk(null),{sessions:{},completed:{}});
});
test('Retry history and drafts are bounded while a fresh old profile still works',()=>{
 const s=setup();for(let i=0;i<55;i++)answer(s,'まだわかりません。');assert.ok(s.history.length<=40);s.setDraft('あ'.repeat(1000));assert.equal(s.draft.length,300);assert.deepEqual(new Store({completed:[],xp:0}).data.talk,{sessions:{},completed:{}});
});

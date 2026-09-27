import {SCENES,TalkSession} from './talk.mjs';

export function createTalkUI({state,store,course,native,play,stopMedia,navigate,render,toast,esc,nextRequest}) {
 const $=selector=>document.querySelector(selector),$$=selector=>[...document.querySelectorAll(selector)];
 let session=null,showTranslation=false,showReading=false;
 const teacher=()=>course.catalog.TEACHERS.find(t=>t.id===session?.teacherId)??course.teacher();
 const safely=action=>{try{return action();}catch(e){toast(e.message);return null;}};
 function hub() {
  const t=course.teacher();
  return `<div class="page-heading"><p class="eyebrow">Miteinander sprechen</p><h1>Dein Gesprächsraum</h1><p class="sub">Höre zu, antworte und frage nach. ${esc(t.name)} begleitet dich durch kleine Alltagssituationen.</p></div>
   <div class="coach talk-coach"><img src="assets/teachers/${t.id}/avatar.png" alt=""><div class="coach-copy"><strong>${esc(t.name)}</strong><p class="sub">${esc(t.style)}</p></div><span class="pill">Offline</span></div>
   <p class="sub">Geführte Gespräche mit verschiedenen Antwortwegen. Freie Themen sind in diesem Bereich noch nicht möglich.</p>
   <div class="talk-scenes">${SCENES.map(scene=>{const saved=store.data.talk.sessions[scene.id],resume=saved&&!scene.nodes[saved.node].done,count=store.data.talk.completed[scene.id]??0;return `<button class="card talk-scene" data-talk-scene="${scene.id}"><span class="talk-scene-icon" aria-hidden="true">${scene.icon}</span><span><strong>${esc(scene.title)}</strong><span class="sub">${esc(scene.goal)}</span><span class="talk-scene-action">${resume?'Gespräch fortsetzen →':count?'Noch einmal sprechen →':'Gespräch beginnen →'}</span>${count?`<span class="sub">${count}× abgeschlossen</span>`:''}</span></button>`;}).join('')}</div>
   <div class="info"><strong>In deinem Tempo.</strong><p>Dein Lehrer spricht mit der gewählten Stimme. Prüfe kurz den erkannten Text und sende deine Antwort. Übersetzung und Antwortideen helfen bei Bedarf. Aufnahmen werden nicht gespeichert oder hochgeladen.</p>${state.caps.models?'':'<p>Für Hören und Mikrofon brauchst du das vorhandene Sprachpaket. Tippen funktioniert auch ohne.</p><button class="small ghost" data-nav="settings">Sprachpaket einrichten</button>'}</div>`;
 }
 function open(sceneId,restart=false) {
  stopMedia();const next=safely(()=>new TalkSession(store,sceneId,course.teacher().id,!restart));if(!next)return;
  session=next;if(session.done){session=safely(()=>new TalkSession(store,sceneId,course.teacher().id,false));if(!session)return;}
  navigate('conversation');if(state.caps.native&&state.caps.models)playReply();
 }
 function conversation() {
  if(!session)return hub();const t=teacher();
  return `<div class="talk-layout"><div class="lesson-header"><button class="back-button" data-nav="talk" aria-label="Zurück zu den Gesprächen">‹</button><div><h1>${esc(session.scene.title)}</h1><span class="sub">Geführtes Offline-Gespräch</span></div></div>
   <div class="talk-partner"><img src="assets/teachers/${t.id}/avatar.png" alt=""><div><strong>${esc(t.name)}</strong><p class="sub">${esc(session.scene.role)}</p></div><span class="pill">${session.done?'Geschafft':'Du & '+esc(t.name)}</span></div>
   <div class="talk-aids"><button class="small ghost" id="talk-translation" aria-pressed="${showTranslation}">Übersetzung ${showTranslation?'aus':'an'}</button><button class="small ghost" id="talk-reading" aria-pressed="${showReading}">Lesung ${showReading?'aus':'an'}</button></div>
   <div class="chat-history" role="log" aria-label="Gesprächsverlauf" aria-live="polite">${session.history.map(m=>`<div class="chat-bubble ${m.role==='user'?'from-user':'from-teacher'}"><span class="chat-speaker">${m.role==='user'?'Du'+(m.source==='spoken'?' · gesprochen':' · Text'):esc(t.name)}</span><p class="chat-jp" lang="ja">${esc(m.jp)}</p>${m.role==='teacher'&&showReading&&m.romaji?`<p class="chat-reading">${esc(m.romaji)}</p>`:''}${m.role==='teacher'&&showTranslation&&m.de?`<p class="chat-translation">${esc(m.de)}</p>`:''}</div>`).join('')}</div>
   <div class="talk-audio"><button class="small ghost" id="talk-replay">▷ Noch einmal</button><button class="small ghost" id="talk-slow">▷ Langsam</button><button class="small ghost" id="talk-stop" aria-label="Stimme stoppen">■ Stopp</button></div><p id="talk-audio-status" class="speech-message" role="status"></p>
   ${session.done?`<section class="card talk-complete"><span class="pill success">Gespräch abgeschlossen</span><h2>Ihr habt euch verständigt.</h2><p class="sub">${session.replies.length} passende Antworten. Probiere beim nächsten Mal einen anderen Gesprächsweg.</p><button class="primary wide" id="talk-again">Dieses Gespräch wiederholen</button><button class="ghost wide" data-nav="talk">Andere Situation wählen</button></section>`:`
   <section class="card talk-composer"><p class="eyebrow">Du bist dran</p><p class="talk-cue">${esc(session.current.cue)}</p>
   ${session.feedback?`<div class="info" role="status">${esc(session.feedback)}</div>`:''}
   <button class="record-button wide" id="talk-record">◉ Antwort aufnehmen</button><p id="talk-speech-status" class="speech-message" role="status">${esc(state.speechMessage)}</p>
   <form id="talk-form"><label class="field"><span>${session.source==='spoken'?'Erkannter Text · bei Bedarf berichtigen':'Deine Antwort · Japanisch tippen oder aufnehmen'}</span><input id="talk-draft" type="text" lang="ja" maxlength="300" autocomplete="off" autocapitalize="none" spellcheck="false" enterkeyhint="send" value="${esc(session.draft)}" placeholder="ここに入力 …"></label><button class="primary wide" id="talk-send">Antwort senden →</button></form>
   <details id="talk-help"><summary>Mir fehlen die Worte · Antwortideen ＋</summary><p class="sub">Du kannst diese Beispiele verändern, soweit es zur Situation passt. Die Offline-Szene kennt die beschriebenen Antwortwege.</p>${session.current.hints.map((h,i)=>`<div class="talk-hint"><p lang="ja">${esc(h.jp)}</p><p class="chat-reading">${esc(h.romaji)}</p><p class="sub">${esc(h.de)}</p><button class="small ghost" data-talk-hint="${i}">Als Text einsetzen</button></div>`).join('')}<p class="sub">Auch möglich: もう一度お願いします。– Noch einmal, bitte.</p></details></section>`}
   <p class="sub talk-privacy">Nur auf deinem Handy: Der Textverlauf wird zum Fortsetzen gespeichert und ist in deiner Lernstandsicherung enthalten. Es gibt keine Aussprache-Note.</p></div>`;
 }
 function playReply(slow=false) {if(session)play(session.prompt.jp,false,slow,teacher());}
 function bind() {
  $$('[data-talk-scene]').forEach(b=>b.onclick=()=>{const saved=store.data.talk.sessions[b.dataset.talkScene];open(b.dataset.talkScene,!!saved&&!!SCENES.find(s=>s.id===b.dataset.talkScene).nodes[saved.node].done);});
  if(state.page!=='conversation'||!session)return;
  $('#talk-translation').onclick=()=>{showTranslation=!showTranslation;render();};
  $('#talk-reading').onclick=()=>{showReading=!showReading;render();};
  $('#talk-replay').onclick=()=>playReply();$('#talk-slow').onclick=()=>playReply(true);
  $('#talk-stop').onclick=()=>{native('stopAudio');state.audio=null;refresh();};
  if($('#talk-again'))$('#talk-again').onclick=()=>open(session.scene.id,true);
  if($('#talk-record'))$('#talk-record').onclick=record;
  if($('#talk-form')) {
   $('#talk-draft').oninput=e=>{session.setDraft(e.target.value,'typed');refresh();};
   $('#talk-form').onsubmit=e=>{e.preventDefault();if(state.recording!=='idle')return;native('stopAudio');state.audio=null;const result=safely(()=>session.respond());state.speechMessage='';render();if(result?.reply&&state.caps.models)playReply(result.repeated);};
   $$('[data-talk-hint]').forEach(b=>b.onclick=()=>{if(state.recording!=='idle')return;session.setDraft(session.current.hints[Number(b.dataset.talkHint)].jp);safely(()=>session.save());render();$('#talk-draft')?.focus();});
  }
  const history=$('.chat-history');if(history)history.scrollTop=history.scrollHeight;refresh();
 }
 function record() {
  if(!session||session.done||state.page!=='conversation')return;
  if(state.recording==='recording'){state.recording='recognizing';native('stopRecording',false);refresh();return;}
  if(state.recording!=='idle')return;
  if(!state.caps.native){toast('Das Mikrofon ist in der installierten Android-App verfügbar. Du kannst hier tippen.');return;}
  if(!state.caps.models){toast('Lade zuerst unter Einstellungen das Sprachpaket. Du kannst auch tippen.');return;}
  native('stopAudio');state.audio=null;const id=nextRequest();state.speech={id,kind:'talk',context:session.context};
  state.recording='requesting';state.speechMessage='Mikrofon wird vorbereitet …';native('record',id);refresh();
 }
 function recognized(value,context) {
  if(state.page!=='conversation'||!session||context!==session.context||session.done)return;
  session.setDraft(value,'spoken');session.feedback='';safely(()=>session.save());state.speechMessage='Prüfe den erkannten Text und sende deine Antwort.';render();
 }
 function refresh() {
  if(state.page!=='conversation'||!session)return;
  const busy=state.recording!=='idle',record=$('#talk-record');
  if(record){record.textContent={idle:'◉ Antwort aufnehmen',requesting:'Mikrofon wird vorbereitet …',recording:'■ Aufnahme beenden',recognizing:'Sprache wird erkannt …'}[state.recording];record.disabled=!['idle','recording'].includes(state.recording);record.classList.toggle('recording',state.recording==='recording');}
  if($('#talk-send'))$('#talk-send').disabled=busy||!session.draft.trim();if($('#talk-draft'))$('#talk-draft').disabled=busy;
  for(const selector of ['#talk-replay','#talk-slow'])if($(selector))$(selector).disabled=busy||!state.caps.models;
  if($('#talk-stop'))$('#talk-stop').disabled=!state.audio;
  $$('[data-talk-hint]').forEach(b=>b.disabled=busy);
  if($('#talk-speech-status'))$('#talk-speech-status').textContent=state.speechMessage;
  if($('#talk-audio-status'))$('#talk-audio-status').textContent=state.audio?.message??(state.caps.models?'':'Ohne Sprachpaket kannst du Antworten tippen. Stimmen und Mikrofon lassen sich unter Einstellungen einrichten.');
 }
 return {hub,conversation,bind,refresh,recognized,save:()=>{if(session)safely(()=>session.save());},reset:()=>{session=null;},open};
}

import {createSpeechLab} from './speech-lab.mjs';
import {createPracticeUI} from './practice-ui.mjs';
import {createDailyUI} from './daily-ui.mjs';
import {Store,Course,Session,PHASES,LABELS,cleanProfile,compact,shuffle,reviewCard,isShortKana} from './core.mjs';
import {createTalkUI} from './talk-ui.mjs';
import {createExerciseUI} from './exercise-ui.mjs';
import {focusLesson,closeFocusSheet} from './focus-ui.mjs';
import {applyKanaRecognition} from './kana-recognition.mjs';
import {supportView,bindSupport} from './speech-support-ui.mjs';
import {calendarView,currentStreak,dayKey,shiftMonth} from './calendar.mjs';
import {mascotMarkup,animateMascots} from './mascot.mjs';
import {animateTeacher as runTeacher,syncCoach,coachMarkup} from './characters.mjs';
import {rewardMarkup,animateReward} from './reward.mjs';

const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const bridge=window.AndroidTrainer;
const state={page:'home',session:null,query:'',stage:'Alle',libraryQuery:'',review:null,revealed:false,teacherDetail:null,
  caps:{native:!!bridge,models:false,modelBytes:0,version:'11.0.15-android.1-test'},audio:null,speech:null,speechMessage:'',recording:'idle',calendarMonth:dayKey().slice(0,7),completeXP:0,
  modelStatus:'',modelPercent:0,modelBusy:false,updateStatus:'',updateAvailable:false,updateBusy:false,updateTest:false,licenseText:'',completeLesson:null};
let speechLab,practiceUI,dailyUI,course,store,catalog,talkUI,exerciseUI,blinkIndex,expressions,animationStop=()=>{},mascotStop=()=>{},rewardStop=()=>{},toastTimer,requestCounter=0,saveError='';
const native=(name,...args)=> { if(bridge&&typeof bridge[name]==='function')return bridge[name](...args);return undefined; };
function toast(text) { $('#toast').textContent=text;$('#toast').classList.add('visible');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').classList.remove('visible'),4800); }
function persist(text) {
  try {if(bridge) {if(!native('saveProfile',text))throw Error('Speichern fehlgeschlagen.');} else localStorage.setItem('jt-mobile-profile',text);saveError='';return true;}
  catch(e) {saveError='Lernstand konnte nicht gespeichert werden. Bitte Speicherplatz prüfen und die App geöffnet lassen.';showSaveError();return false;}
}
function showSaveError() {let el=$('#save-error');if(!el){el=document.createElement('div');el.id='save-error';el.className='storage-error';el.role='alert';document.body.prepend(el);}el.textContent=saveError;}
function save() {try{store.save();}catch(e){toast(e.message);}}
function stopMedia() {speechLab?.cancel();state.speech?.support?.cancel();native('stopAudio');native('stopRecording',true);state.audio=null;state.speech=null;state.ownSpeech=null;if(state.session)state.session.shortSpeechReady=false;state.recording='idle';talkUI?.refresh();}
function navigate(page) {
  if(state.page==='exercises'&&page!==state.page)exerciseUI?.cancel();
  if(state.session&&state.page==='lesson')state.session.snapshot();
  if(state.page==='conversation')talkUI?.save();
  stopMedia();animationStop();state.page=page;document.body.dataset.teacherMood='idle';state.speechMessage='';render();window.scrollTo(0,0);$('#app').focus({preventScroll:true});
}
function heading(eyebrow,title,description='') {return `<div class="page-heading"><p class="eyebrow">${esc(eyebrow)}</p><h1>${esc(title)}</h1>${description?`<p class="sub">${esc(description)}</p>`:''}</div>`;}
function teacherStrip() {const t=course.teacher();return `<div class="coach"><img src="assets/teachers/${t.id}/avatar.png" alt=""><div class="coach-copy"><strong>${esc(t.name)} begleitet dich</strong><p class="sub">${esc(t.style)}</p></div><span class="pill">Schritt für Schritt</span></div>`;}
function home() {
  const t=course.teacher(),next=course.next(),done=course.lessons.filter(l=>store.data.completed.includes(l.key)).length,streak=currentStreak(store.data);
  return `<div class="stats home-stats" aria-label="Dein Lernfortschritt"><button class="stat accent" data-nav="calendar" aria-label="Lernserie: ${streak} ${streak===1?'Tag':'Tage'}. Kalender öffnen"><strong>${streak} ${streak===1?'Tag':'Tage'}</strong><span>Lernserie · Kalender ›</span></button><div class="stat"><strong>${store.data.xp} XP</strong><span>Level ${Math.floor(store.data.xp/250)+1}</span></div><div class="stat"><strong>${done} / ${course.lessons.length}</strong><span>Lektionen</span></div></div>
  <p class="eyebrow">Dein kleiner Schritt nach Japan</p><section class="hero" aria-label="Willkommen"><div class="hero-copy"><span class="pill">${state.caps.models?'● Alles bereit · offline':`${course.lessons.length} Lektionen · offline lernen`}</span><h1 style="margin-top:16px">Ein bisschen<br>Japanisch.<br>Jeden Tag.</h1><p class="sub">${esc(t.name)} begleitet dich auf deinem Lernweg.</p><button class="primary" id="hero-resume">Weiterlernen →</button><p class="hero-quote">„${esc(t.de)}“</p></div><canvas id="teacher-canvas" width="512" height="768" role="img" aria-label="${esc(t.name)}"></canvas></section>
  ${dailyUI.summary()}
  <section class="section"><div class="section-title"><h2>Dein nächster Schritt</h2><button class="text-link" data-nav="course">Lernweg ansehen</button></div><article class="card next-card"><span class="pill">${esc(next.level)}</span><p class="lesson-title">${esc(next.title)}</p><p class="sub">${esc(next.goal??next.unit)}</p><div class="progress" aria-label="${done} von ${course.lessons.length} Lektionen"><span style="width:${done/course.lessons.length*100}%"></span></div><div class="row"><span class="sub">${next.cards.length} Lernkarten · ${next.xp??20} XP</span><button class="small primary" id="next-resume">${store.data.last_lesson.key===next.key?'Fortsetzen':'Loslegen'} →</button></div></article></section>
  <section class="card talk-home"><span class="pill">Neu · Gespräche offline</span><h2>Einfach mal miteinander reden.</h2><p class="sub">Mit ${esc(t.name)} im Café bestellen, jemanden kennenlernen oder das Wochenende planen.</p><button class="primary wide" data-nav="talk">Gespräche üben →</button></section>
  ${!state.caps.models?`<aside class="info"><strong>Deine Lehrer bekommen eine Stimme.</strong><p style="margin:5px 0 7px">Lade einmal das Sprachpaket für Stimmen und Sprechen. Danach funktioniert auch das offline.</p><button class="small ghost" data-nav="settings">Sprachpaket einrichten</button></aside>`:''}
  ${store.data.show_kiko?`<div class="kiko-note"><button class="kiko-greeting" aria-label="Kiko begrüßen">${mascotMarkup()}</button><span>Lieber fünf Minuten mit Freude als gar nicht anfangen.<small>Tippe auf Kiko, um Hallo zu sagen.</small></span></div>`:''}`;
}
function courseList() {return heading('Dein Lernweg','Schritt für Schritt',`${course.lessons.length} Lektionen. Vom ersten Laut bis zum zusammenhängenden Text.`)+
  `<div class="filters"><label class="field"><span>Lektion oder Wort suchen</span><input id="course-search" type="search" placeholder="Zum Beispiel: Hiragana, Reisen …" value="${esc(state.query)}"></label><label class="field"><span>Abschnitt</span><select id="stage"><option>Alle</option>${course.stages.map(s=>`<option ${s===state.stage?'selected':''}>${esc(s)}</option>`).join('')}</select></label></div><div id="course-results">${courseRows()}</div>`;}
function courseRows() {
  const list=course.search(state.query,state.stage);let previous='';
  if(!list.length)return '<div class="empty">Keine passende Lektion gefunden.</div>';
  return `<p class="sub">${list.length} Lektionen</p>`+list.map(l=> {
    const group=l.level!==previous?`<h2 class="course-group">${esc(l.level)}</h2>`:'';previous=l.level;
    const done=store.data.completed.includes(l.key),unlocked=course.unlocked(l.key);
    return group+`<button class="lesson-row ${done?'done':''} ${unlocked?'':'locked'}" data-lesson="${esc(l.key)}" aria-label="${esc(l.title)}${unlocked?'':' · noch gesperrt'}"><span class="lesson-number">${done?'✓':unlocked?course.positions.get(l.key)+1:'⌑'}</span><span class="lesson-text"><strong>${esc(l.title)}</strong><small>${l.cards.length} Karten · ${l.xp??20} XP${done?' · abgeschlossen':''}</small></span><span class="chevron">›</span></button>`;
  }).join('');
}
function openLesson(key) {
  if(!course.unlocked(key)) {toast('Schließe zuerst die vorherige Lektion ab. Dein Lernweg führt dich der Reihe nach weiter.');return;}
  state.session=new Session(course.byKey.get(key),course);navigate('lesson');
  if(state.session.migrated)toast('Neuer Übungsablauf: Deine angefangene Karte startet mit Hören & Sprechen. Abgeschlossene Lektionen und XP bleiben erhalten.');
}
function pronunciation(card) {return card.approx??card.pron_de??card.pron??card.pronunciation??card.hint??'';}
function cardView(card) {
  return `<div class="speaking-card"><p class="sub" id="speak-instruction">Höre die Vorlage an und sprich sie danach nach.</p><p class="jp" lang="ja">${esc(card.jp)}</p><p class="romaji">${esc(card.romaji)}</p><p class="translation">${esc(card.de)}</p>${pronunciation(card)?`<p class="pronunciation">Aussprachehilfe: ${esc(pronunciation(card))}</p>`:''}<div class="audio-actions"><button id="hear-normal">▷ Anhören</button><button id="hear-slow">▷ Langsam</button></div><p id="audio-status" class="speech-message" role="status"></p>
  <div class="speech-panel"><button id="record" class="record-button" disabled>Erst die Vorlage anhören</button><div class="microphone-live" hidden><meter id="mic-level" min="0" max="1" value="0" aria-label="Mikrofonpegel"></meter><span id="mic-time">0:00</span></div><p id="speech-status" class="speech-message" aria-live="polite">${esc(state.speechMessage)}</p><p class="speech-caption">${isShortKana(card.jp)?'Einmal normal aussprechen. Nach einer kurzen Pause endet die Aufnahme automatisch.':'Sprich die Vorlage nach und tippe dann auf Aufnahme beenden.'} Lokale Erkennung, keine Aussprache-Note.</p><button id="lesson-own" hidden>▷ Meine Aufnahme</button><button id="lesson-cancel" hidden>Aufnahme abbrechen</button></div>${!state.caps.models?'<div class="info"><p>Für diesen Schritt brauchst du das lokale Sprachpaket.</p><button class="small ghost" data-nav="settings">Sprachpaket einrichten</button></div>':''}</div>`;
}
function explanation(card,lesson) {
  const p=course.profile(card,lesson),ex=course.example(card);
  return `<div class="explain"><h3>${esc(p.kind)}</h3><p>${esc(p.usage)}</p><h3>So funktioniert es</h3><p>${esc(p.explain)}</p>${p.parts?.length?`<ul>${p.parts.map(part=>`<li><strong lang="ja">${esc(part[0])}</strong> – ${esc(part[1])}</li>`).join('')}</ul>`:''}<h3>Ein Beispiel</h3><div class="example"><p class="jp" lang="ja">${esc(ex.jp)}</p><p class="romaji">${esc(ex.romaji)}</p><p>${esc(ex.de)}</p><button class="small ghost" id="hear-example">▷ Beispiel hören</button></div>${p.register?`<h3>Wann passt das?</h3><p>${esc(p.register)}</p>`:''}<h3>Achte darauf</h3><p>${esc(p.pitfall)}</p>${p.extra?.length?`<ul>${p.extra.map(x=>`<li>${esc(Array.isArray(x)?x.join(' · '):x)}</li>`).join('')}</ul>`:''}</div>`;
}
function lessonGuide(lesson,open=false) {
  const g=lesson.study_guide;
  const points=g?.points??(lesson.intro?[lesson.intro]:[]);
  if(!points.length)return '';
  const before=(g?.prerequisites??[]).map(key=>course.byKey.get(key)?.title).filter(Boolean);
  return `<details class="lesson-guide" ${open?'open':''}><summary>Vorwissen & Lernhilfe</summary><div class="explain">${before.length?`<p class="sub"><strong>Das greifst du wieder auf:</strong> ${esc(before.join(' · '))}</p>`:''}${points.map(p=>`<p>${esc(p)}</p>`).join('')}${g?.recall?`<div class="info"><strong>Zum selbst Ausprobieren</strong><p>${esc(g.recall)}</p></div>`:''}</div></details>`;
}
function lesson() {
  const s=state.session;if(!s)return '';
  const phase=PHASES.indexOf(s.phase);
  return `<div class="lesson-layout"><div class="lesson-header"><button class="back-button" data-nav="course" aria-label="Zurück zum Lernweg">‹</button><div><h1>${esc(s.lesson.title)}</h1><span class="sub">${esc(s.lesson.level)} · Karte ${s.index+1} von ${s.lesson.cards.length}</span></div></div>
  ${s.mode==='learn'&&s.phase==='speak'&&s.lesson.goal?`<p class="lesson-goal"><strong>Dein Lernziel:</strong> ${esc(s.lesson.goal)}</p>`:''}
  ${s.mode==='retry'?`<div class="info">Noch ${s.retryTasks.length} Aufgaben aus dieser Runde. Du wiederholst dieselbe Aufgabe; falsche Antworten kommen erneut ans Ende.</div>`:s.mode==='recap'?`<div class="info">Noch ${s.recap.length} Zuordnungen in der Abschlussrunde. Schwierige Karten kommen noch einmal dran.</div>`:`<div class="phase-track" aria-label="Schritt ${phase+1} von 6">${PHASES.map((p,i)=>`<span class="${i===phase?'current':i<phase?'past':''}"></span>`).join('')}</div>`}
  <section class="card exercise-card" data-step="${s.mode==='recap'?'recap':s.phase}"><div class="task-header"><div><p class="eyebrow" id="step-count">${s.mode==='retry'?`Fehlerwiederholung · ${s.retry_passed+1}/${s.retry_total}`:s.mode==='recap'?`Abschlussrunde · ${s.recap_passed+1}/${s.recap_total}`:`Schritt ${phase+1}/6`}</p><h2>${s.mode==='recap'?'Zum Abschluss':LABELS[s.phase]}</h2></div></div><div id="task">${task()}</div></section>${exerciseUI?.has(s.lesson.key)?'<button id="exercise-round" class="ghost wide">Abwechslungsreich üben</button>':''}</div>`;
}
function task() {
  const s=state.session;let html='';
  if(s.mode==='recap')html=`<p>Welche Bedeutung passt?</p><p class="jp exercise-prompt" lang="ja">${esc(s.card.jp)}</p>`+options(s);
  else if(s.phase==='speak')html=cardView(s.card)+(s.success?'':supportView(s.support,s.supportDeck(),esc))+lessonGuide(s.lesson,s.index===0);
  else if(s.phase==='meaning')html=`<p>Was bedeutet die japanische Form?</p><p class="jp exercise-prompt" lang="ja">${esc(s.card.jp)}</p>`+options(s);
  else if(s.phase==='listen')html=`<p>Höre eine bereits geübte Form. Welche Bedeutung passt?</p><button class="primary wide" id="hear-task">▷ Hörbeispiel abspielen</button><p id="audio-status" class="speech-message" role="status"></p>${options(s)}`;
  else if(s.phase==='build') {
    const parts=course.blocks(s.card,s.lesson);
    html=parts.length?`<p>Setze die Bausteine in die richtige Reihenfolge.</p><p class="build-meaning">${esc(s.card.de)}</p><div class="token-board" id="token-board">${s.tokens.length?s.tokens.map((v,i)=>`<button data-remove-token="${i}">${esc(parts[v])}</button>`).join(''):'<span class="sub">Tippe die Bausteine unten an.</span>'}</div><div class="tokens">${shuffle(parts.map((p,i)=>i),s.key).map(i=>`<button data-token="${i}" ${s.tokens.includes(i)||s.success?'disabled':''}>${esc(parts[i])}</button>`).join('')}</div><button class="ghost wide" id="check-build" ${s.success?'disabled':''}>Reihenfolge prüfen</button>`:`<p>Diese kurze Form hat keine getrennten Bausteine. Wähle ihre Lesung.</p><p class="jp exercise-prompt" lang="ja">${esc(s.card.jp)}</p>`+options(s);
  } else if(s.phase==='write')html=`<p>Schreibe die Lesung aus dem Gedächtnis in Romaji.</p><p class="jp exercise-prompt" lang="ja">${esc(s.card.jp)}</p><form id="write-form"><label class="field"><span>Deine Lesung</span><input id="romaji-input" value="${esc(s.input_text??'')}" type="text" autocomplete="off" autocapitalize="none" spellcheck="false" enterkeyhint="done" placeholder="Romaji eingeben" ${s.success?'disabled':''}></label><button id="check-write" class="ghost wide" ${s.success?'disabled':''}>Lesung prüfen</button></form>`;
  else if(s.phase==='apply') {
    const p=course.profile(s.card,s.lesson),q=p.scenario.question;
    html=`${p.kind==='Leseverständnis'?`<p class="jp exercise-prompt" lang="ja">${esc(s.card.jp)}</p>`:''}<p>${esc(q)}</p>${/dieser (Lern)?Karte/i.test(q)?`<p lang="ja">${esc(s.card.jp)} (${esc(s.card.romaji)})</p>`:''}${options(s)}`;
  }
  if(s.mode==='recap'||s.phase!=='speak')html+=`<button id="show-hint" class="ghost wide">${s.hintOpen?'Hilfe schließen':'Ich brauche einen Hinweis'}</button>${s.hintOpen?`<aside class="exercise-hint"><p class="sub">Nachgeschaut · Hilfe gibt den nächsten Schritt nicht frei.</p><p class="jp" lang="ja">${esc(s.card.jp)}</p><p class="romaji">${esc(s.card.romaji)}</p><p>${esc(s.card.de)}</p>${lessonGuide(s.lesson)}${explanation(s.card,s.lesson)}</aside>`:''}`;
  html+=`<div id="task-feedback" aria-live="polite">${feedback(s)}</div>`;
  if(s.mode==='learn'&&s.phase==='speak'&&s.shortSpeechReady&&!s.success)html+='<div class="info"><strong>Einzellaut selbst prüfen</strong><p>Bei kurzen Kana kann die Erkennung abweichen. Vergleiche mit der Vorlage: Hast du den Laut nachgesprochen?</p><button id="confirm-short-speech" class="ghost wide">Ja, selbst geprüft</button><p class="sub" style="margin-top:8px">Als Selbstprüfung gespeichert, nicht als automatisch erkannte Übereinstimmung.</p></div>';
  html+=`<div class="task-footer"><button id="advance" class="primary" ${s.success?'':'disabled'}>${s.mode==='retry'?(s.retryTasks.length===1?'Zur Abschlussrunde →':'Nächste Wiederholung →'):s.mode==='recap'?(s.recap.length===1?'Lektion abschließen':'Weiter →'):PHASES.indexOf(s.phase)<5?`Weiter zu ${PHASES.indexOf(s.phase)+2}/6 →`:s.index<s.lesson.cards.length-1?'Nächste Karte →':s.retryTasks.length?'Fehler wiederholen →':'Zur Abschlussrunde →'}</button>${s.canDefer?'<button id="defer-task" class="primary">Weiter · am Ende wiederholen →</button>':''}</div>`;
  if(s.mode!=='recap')html+=`<details><summary>Erklärung und Beispiel ansehen ＋</summary>${explanation(s.card,s.lesson)}</details>`;
  return html;
}
function options(s) {const choices=s.answers().options;return `<p class="answer-count">Wähle eine von ${choices.length} Antworten.</p><div class="options">${choices.map((o,i)=>`<button class="option ${s.chosen===o?(s.success?'correct':'wrong'):''}" data-choice="${i}" ${s.success?'disabled':''}>${esc(o)}</button>`).join('')}</div>`;}
function feedback(s) {return s.feedback?`<div class="feedback ${s.success?'correct':'wrong'}">${s.success?'✓ ':''}${esc(s.feedback)}</div>`:'';}
function decorateLesson(){focusLesson({page:state.page,session:state.session,teacher:course.teacher(),store,esc});}
function refreshTask() {$('#app').innerHTML=lesson();decorateLesson();bindTask();bindNavigation();refreshAudio();}
function bindTask() {
  const s=state.session;
  if(s.phase==='speak')bindSupport(s.support,refreshTask,()=>{if(state.recording==='idle')s.acceptSupport();});
  if($('#show-hint'))$('#show-hint').onclick=()=>{s.hintOpen=!s.hintOpen;if(s.hintOpen){const m=s.metrics();m.hints=(Number.isInteger(m.hints)?m.hints:0)+1;}s.snapshot();refreshTask();};
  $$('[data-choice]').forEach(b=>b.onclick=()=>{s.choose(s.answers().options[Number(b.dataset.choice)]);refreshTask();});
  $$('[data-token]').forEach(b=>b.onclick=()=>{s.tokens.push(Number(b.dataset.token));s.snapshot();refreshTask();});
  $$('[data-remove-token]').forEach(b=>b.onclick=()=>{if(!s.success){s.tokens.splice(Number(b.dataset.removeToken),1);s.snapshot();refreshTask();}});
  if($('#check-build'))$('#check-build').onclick=()=>{s.checkBuild();refreshTask();};
  if($('#write-form')) {
    const input=$('#romaji-input');let composing=false;input.oninput=()=>{s.input_text=input.value;s.snapshot();};input.oncompositionstart=()=>{composing=true;};input.oncompositionend=()=>{composing=false;s.input_text=input.value;s.snapshot();};
    input.onkeydown=e=>{if(e.key==='Enter'&&(composing||e.isComposing||e.keyCode===229))e.preventDefault();};
    $('#write-form').onsubmit=e=>{e.preventDefault();if(composing)return;s.input_text=input.value;s.checkWrite(input.value);refreshTask();};
  }
  if($('#hear-normal'))$('#hear-normal').onclick=()=>play(s.card.jp,true);
  if($('#hear-slow'))$('#hear-slow').onclick=()=>play(s.card.jp,true,true);
  if($('#record'))$('#record').onclick=record;
  if($('#lesson-cancel'))$('#lesson-cancel').onclick=()=>{stopMedia();state.speechMessage='Aufnahme abgebrochen. Du kannst erneut versuchen.';refreshTask();};
  if($('#lesson-own'))$('#lesson-own').onclick=()=>{if(!state.ownSpeech||state.recording!=='idle')return;native('stopAudio');const id=`own-${++requestCounter}`;state.audio={id,forListen:false,message:'Deine Aufnahme …'};native('playRecording',state.ownSpeech,id);refreshAudio();};
  if($('#confirm-short-speech'))$('#confirm-short-speech').onclick=()=>{if(state.recording==='idle'&&s.confirmShortSpeech()){s.support.data.open=false;s.support.save();refreshTask();}};
  if($('#hear-task'))$('#hear-task').onclick=()=>play(s.listenCard.jp,true);
  if($('#hear-example'))$('#hear-example').onclick=()=>play(course.example(s.card).jp);
  const continueLesson=defer=>{
    const beforeXP=store.data.xp,result=defer?s.defer():s.advance();if(result==='blocked')return;
    stopMedia();state.speechMessage='';
    if(result==='complete'){state.completeLesson=s.lesson;state.completeXP=store.data.xp-beforeXP;navigate('complete');}
    else {render();window.scrollTo({top:0,behavior:'instant'});}
  };
  $('#advance').onclick=()=>continueLesson(false);
  if($('#defer-task'))$('#defer-task').onclick=()=>continueLesson(true);
}
function complete() {const l=state.completeLesson;return `<div class="completion-scene"><section class="card completion"><p class="eyebrow">Lektion abgeschlossen</p><h1>Gut gemacht!</h1><p>Du hast „${esc(l.title)}“ abgeschlossen.</p><p class="completion-xp">${state.completeXP?`+${state.completeXP} XP`:'Wiederholung geschafft'}</p><p class="sub">${state.completeXP?'Für deinen ersten Abschluss.':'Die XP für diese Lektion hast du bereits erhalten.'}</p>${rewardMarkup(store.data.show_kiko)}<p>Kleine Schritte, große Fortschritte!</p></section><div class="completion-actions"><button class="primary wide" id="complete-next">Weiterlernen →</button><button class="ghost wide" data-nav="course">Zum Lernpfad</button></div></div>`;}
function teachers() {
  const selected=course.teacher();const detail=catalog.TEACHERS.find(t=>t.id===state.teacherDetail)??selected;
  return heading('Deine Begleitung','Mit wem lernst du?','Acht Persönlichkeiten. Wähle die Begleitung, mit der du dich wohlfühlst.')+
  `<section class="card"><div class="teacher-detail"><img src="assets/teachers/${detail.id}/avatar.png" alt=""><div><h2>${esc(detail.name)}</h2><p class="sub">${esc(detail.style)}</p><p class="sub">${esc(detail.voice)}</p></div></div><p class="sub">${esc(detail.detail)}</p><p class="sub"><strong>Schwerpunkt:</strong> ${esc(detail.focus)}</p><div class="toolbar"><button id="select-teacher" class="primary" ${detail.id===selected.id?'disabled':''}>${detail.id===selected.id?'✓ Ausgewählt':'Mit '+esc(detail.name)+' lernen'}</button><button id="teacher-voice" class="ghost">▷ Stimmprobe</button></div></section>
  <div class="teacher-grid">${catalog.TEACHERS.map(t=>`<button class="teacher-tile ${t.id===selected.id?'selected':''}" data-teacher="${t.id}" aria-label="${esc(t.name)} ansehen"><img src="assets/teachers/${t.id}/card.png" alt="" loading="lazy">${t.id===selected.id?'<span class="selected-check">✓</span>':''}<div class="tile-copy"><strong>${esc(t.name)}</strong><p class="sub">${esc(t.style)}</p></div></button>`).join('')}</div>`;
}
function nextReview() {const available=course.available();const due=available.filter(c=>(store.data.review[c.key]?.due??0)<=Date.now()/1000);const pool=due.length?due:available;const old=state.review?.key;state.review=pool.find(c=>c.key!==old)??pool[0];state.revealed=false;}
function review() {
  if(!state.review)nextReview();const c=state.review;
  const speechReviews=Object.entries(store.data.speech_reviews??{}).filter(([,v])=>v.status==='pending').map(([key,v])=>{const card=course.cards.find(c=>c.key===v.card);if(v.kind==='talk')return `<button class="ghost wide" data-talk-review="${esc(v.scene)}">Gespräch erneut üben · freiwillig</button>`;return card?`<button class="ghost wide" data-speech-review="${esc(key)}">${esc(card.jp)} · ${esc(card.de)}<small>${v.due>Date.now()/1000?'Für morgen vorgemerkt · schon jetzt freiwillig üben':'Jetzt freiwillig sprechen üben'}</small></button>`:'';}).join('');
  return heading('In deinem Tempo','Üben & miteinander sprechen','Wiederhole gelernte Karten oder probiere ein geführtes Gespräch.')+
  (speechReviews?`<section class="card"><h2>Sprechen später üben</h2><p>Nach der Auswahlhilfe vorgemerkt. Dein Lektionsfortschritt bleibt erhalten.</p>${speechReviews}</section>`:'')+
  `<section class="card talk-home"><h2>Dein Gesprächsraum</h2><p class="sub">Du sprichst, dein Lehrer reagiert. Fünf Alltagssituationen mit verschiedenen Gesprächswegen.</p><button class="primary wide" data-nav="talk">Gespräche üben →</button></section>`+
  `<article class="card review-card"><span class="pill">${esc(c.lesson)}</span><p class="jp" lang="ja">${esc(c.jp)}</p><button id="review-audio" class="ghost small">▷ Anhören</button>${state.revealed?`<div style="margin-top:20px"><p class="romaji">${esc(c.romaji)}</p><p>${esc(c.de)}</p><div class="toolbar"><button id="review-again" class="ghost">Noch einmal</button><button id="review-known" class="primary">Gewusst ✓</button></div></div>`:`<button class="primary wide" id="reveal" style="margin-top:25px">Lesung & Bedeutung zeigen</button>`}</article><p class="sub">Ehrlich einschätzen hilft mehr als Raten. „Noch einmal“ legt die Karte früher wieder vor.</p><button class="ghost wide" data-nav="library">Alle gelernten Wörter ansehen</button>`;
}
function library() {return heading('Dein Nachschlagewerk','Wörter & Sätze','Lerne im Kurs weiter und fülle nach und nach deine persönliche Bibliothek.')+
  `<label class="field"><span>Japanisch, Romaji oder Deutsch</span><input id="library-search" type="search" placeholder="Wort oder Satz suchen" value="${esc(state.libraryQuery)}"></label><label class="setting-row"><span>Auch noch nicht gelernte Karten anzeigen</span><input id="library-all" type="checkbox" ${store.data.library_all?'checked':''}></label><div id="library-results">${libraryRows()}</div>`;}
function libraryRows() {const query=state.libraryQuery.normalize('NFKC').toLowerCase();const cards=course.available(store.data.library_all).filter(c=>[c.jp,c.de,c.romaji].join(' ').normalize('NFKC').toLowerCase().includes(query));return `<p class="sub">${cards.length} Karten${cards.length>60?' · zeige die ersten 60; grenze die Suche ein':''}</p>`+cards.slice(0,60).map(c=>`<article class="card library-card"><span class="sub">${esc(c.lesson)}</span><p class="jp" lang="ja">${esc(c.jp)}</p><p class="romaji">${esc(c.romaji)}</p><p>${esc(c.de)}</p><button class="small ghost" data-library-audio="${esc(c.key)}">▷ Anhören</button></article>`).join('');}
function grammar() {return heading('Zum Nachlesen','Grammatik im Überblick','Kleine Erklärungen, die du jederzeit wieder aufschlagen kannst.')+catalog.GRAMMAR_TOPICS.map(([title,jp,romaji,text])=>`<article class="card library-card"><h2>${esc(title)}</h2><p class="jp" lang="ja">${esc(jp)}</p><p class="romaji">${esc(romaji)}</p><p class="sub">${esc(text)}</p></article>`).join('');}
function progress() {const done=course.lessons.filter(l=>store.data.completed.includes(l.key));return heading('Dein Fortschritt','Jeder kleine Schritt zählt.')+
  `<div class="stats"><div class="stat"><strong>${done.length}/150</strong><span>Lektionen</span></div><div class="stat accent"><strong>${store.data.xp} XP</strong><span>Erfahrung</span></div><button class="stat" data-nav="calendar"><strong>${currentStreak(store.data)}</strong><span>Lernserie · Kalender ›</span></button></div><section class="section">${course.stages.map(stage=>{const lessons=course.lessons.filter(l=>l.level===stage),count=lessons.filter(l=>store.data.completed.includes(l.key)).length;return `<article class="card"><div class="row"><h3>${esc(stage)}</h3><span class="sub">${count} / ${lessons.length}</span></div><div class="progress"><span style="width:${count/lessons.length*100}%"></span></div></article>`;}).join('')}</section><div class="info">Der Kurs ist ein Lernweg und keine JLPT- oder GER-Zertifizierung.</div>`;}
function more() {return heading('Alles an einem Ort','Mehr für deinen Lernweg')+`<div class="list-menu">${[['speech-lab','Sprachvergleich','Freiwillige lokale Testrunde und Testmodelle'],['practice-lab','Hörsituationen & Zeichen','Bekanntes anwenden und Formen nachzeichnen'],['daily','Heute für dich','Deine persönliche kurze Übungsrunde'],['talk','Gespräche','Mit deinem Lehrer Alltagssituationen üben'],['library','Wörter & Sätze','Deine persönliche Bibliothek'],['grammar','Grammatik','Erklärungen zum Nachschlagen'],['progress','Fortschritt','Lektionen, XP und deine Lernserie'],['settings','Einstellungen','Stimmen, Updates und Lernstand sichern']].map(([page,title,desc])=>`<button class="menu-button" data-nav="${page}"><div>${title}<span>${desc}</span></div><b>›</b></button>`).join('')}</div>`;}
function settings() {return heading('So passt es zu dir','Einstellungen')+
  `<section class="card"><h2>Offline-Stimmen & Sprechen</h2><p class="sub">Die acht Lehrer-Stimmen und japanische Erkennung arbeiten mit dem Sprachpaket direkt auf deinem Handy. Aufnahmen werden nicht hochgeladen.</p><div id="models-box">${modelBox()}</div></section>
  <section class="card"><h2>Lernen & Darstellung</h2><label class="field"><span>Sprechtempo · zusätzlich zum Lehrerprofil</span><select id="speed">${[.65,.8,.85,1,1.15].map(v=>`<option value="${v}" ${Math.abs(store.data.tts_speed-v)<.001?'selected':''}>${v.toLocaleString('de-DE')}× ${v===1?'· normal':''}</option>`).join('')}</select></label><label class="setting-row"><span>Sanfte Figurenbewegung</span><input id="motion" type="checkbox" ${store.data.motion_enabled?'checked':''}></label><label class="setting-row"><span>Kiko auf der Startseite</span><input id="kiko" type="checkbox" ${store.data.show_kiko?'checked':''}></label><p class="sub">Schriftgröße und Bildschirmzoom folgen zusätzlich deinen Android-Einstellungen.</p></section>
  <section class="card"><h2>Lernstand sichern</h2><p class="sub">Eine JSON-Sicherung enthält XP, Lehrerauswahl, Lernschritte und den letzten Textverlauf je Gesprächsszene. Du kannst auch einen Export der Windows-Version übernehmen. Es gibt keine automatische Synchronisierung.</p><div class="toolbar"><button id="export" class="ghost">Exportieren</button><button id="import" class="ghost">Importieren</button></div><p class="sub">Bei Deinstallation löscht Android die App-Daten. Exportiere deinen Lernstand vorher. Bei einem App-Update bleiben sie erhalten.</p></section>
  <section class="card"><h2>App-Updates</h2><p class="sub">Installiert: ${esc(state.caps.version)}</p><p class="sub">Updates werden erst auf deinen Wunsch geladen. Android bittet anschließend um deine Installationsbestätigung.</p><div id="updates-box">${updateBox()}</div></section>
  <section class="card"><h2>Über den Trainer</h2><p class="sub">Kurs ${esc(course.raw.content_version)} · ${course.lessons.length} Lektionen · ${course.cards.length} Lernkarten</p><p class="sub">Programmquellcode: GPL-3.0-or-later.<br>Sprachmodelle haben eigene Lizenzbedingungen.</p><button id="licenses" class="ghost wide">Lizenzen & Modellbedingungen</button></section>`;}
function modelBox() {return state.caps.models?'<p class="info success">✓ Sprachpaket bereit. Stimmen und Erkennung sind offline verfügbar.</p>':
  `<p class="download-status">${esc(state.modelStatus||`Einmaliger Download: ca. ${Math.round(state.caps.modelBytes/1e6)} MB. Für spätere App-Updates wird das Paket weiterverwendet.`)}</p>${state.modelBusy?`<div class="progress"><span style="width:${state.modelPercent}%"></span></div><button class="ghost wide" id="cancel-models">Download abbrechen</button>`:`<button class="primary wide" id="download-models">Sprachpaket laden</button>`}`;}
function updateBox() {return `<p class="download-status" role="status">${esc(state.updateStatus)}</p><button class="ghost wide" id="check-updates" ${state.updateBusy?'disabled':''}>Nach Updates suchen</button><button style="margin-top:10px" class="ghost wide" id="check-test-updates" ${state.updateBusy?'disabled':''}>Testversion suchen</button><p class="muted">Testversionen enthalten neue Funktionen zum Ausprobieren. Dein Lernstand und das Sprachpaket bleiben erhalten.</p>${state.updateAvailable?`<button style="margin-top:10px" class="primary wide" id="install-update" ${state.updateBusy?'disabled':''}>${state.updateTest?'Testversion herunterladen':'Update installieren'}</button>`:''}`;}
function render() {
  document.body.classList.toggle('focus-mode',['lesson','exercises'].includes(state.page));
  document.body.classList.toggle('completion-mode',state.page==='complete');
  animationStop();mascotStop();rewardStop();document.body.classList.toggle('motion-off',!store.data.motion_enabled||store.data.motion_preset==='off');
  const pages={home,calendar:()=>calendarView(store.data,state.calendarMonth,esc),'speech-lab':()=>speechLab.view(),daily:()=>dailyUI.view(),'practice-lab':()=>practiceUI.view(),course:courseList,lesson,complete,teachers,review,library,grammar,progress,more,settings,exercises:()=>exerciseUI.view(),talk:()=>talkUI.hub(),conversation:()=>talkUI.conversation(),
    licenses:()=>heading('Informationen','Lizenzen & Modellbedingungen')+`<button class="ghost" data-nav="settings">‹ Einstellungen</button><pre class="licenses">${esc(state.licenseText)}</pre>`};
  $('#app').innerHTML=(pages[state.page]??home)();
  if(state.page==='lesson')decorateLesson();
  if(state.page==='speech-lab')document.querySelector('.daily-card')?.insertAdjacentHTML('afterbegin',coachMarkup(course.teacher(),esc));
  const active=state.page==='calendar'?'home':['home','course','review','teachers'].includes(state.page)?state.page:['lesson','complete','exercises'].includes(state.page)?'course':['talk','conversation'].includes(state.page)?'review':'more';
  $$('.bottom-nav button').forEach(b=>b.setAttribute('aria-current',b.dataset.page===active?'page':'false'));
  bindNavigation();bindPage();syncCoach(state);animateTeacher();rewardStop=animateReward(()=>store.data.motion_enabled&&store.data.motion_preset!=='off');mascotStop=animateMascots(()=>store.data.motion_enabled&&store.data.motion_preset!=='off');if(saveError)showSaveError();
}
function bindNavigation() {$$('[data-nav]').forEach(b=>b.onclick=()=>navigate(b.dataset.nav));$$('[data-lesson]').forEach(b=>b.onclick=()=>openLesson(b.dataset.lesson));}
function bindPage() {
  dailyUI?.bind();practiceUI?.bind();speechLab?.bind();
  talkUI?.bind();
  exerciseUI?.bind();
  if($('#exercise-round'))$('#exercise-round').onclick=()=>exerciseUI.open(state.session.lesson.key);
  if(state.page==='home') {$('#hero-resume').onclick=$('#next-resume').onclick=()=>openLesson(course.next().key);animateTeacher();}
  if(state.page==='complete')$('#complete-next').onclick=()=>openLesson(course.next().key);
  if(state.page==='calendar')for(const [id,offset] of [['calendar-prev',-1],['calendar-next',1]])$('#'+id).onclick=()=>{state.calendarMonth=shiftMonth(state.calendarMonth,offset);render();};
  if(state.page==='course') {const update=()=>{$('#course-results').innerHTML=courseRows();bindNavigation();};$('#course-search').oninput=e=>{state.query=e.target.value;update();};$('#stage').onchange=e=>{state.stage=e.target.value;update();};}
  if(state.page==='lesson') {bindTask();refreshAudio();}
  if(state.page==='teachers') {
    $$('[data-teacher]').forEach(b=>b.onclick=()=>{stopMedia();state.teacherDetail=b.dataset.teacher;render();window.scrollTo(0,0);});
    const t=catalog.TEACHERS.find(t=>t.id===state.teacherDetail)??course.teacher();
    $('#select-teacher').onclick=()=>{store.data.teacher_id=t.id;store.data.speaker_id=t.speaker_id;save();render();toast(`${t.name} begleitet dich ab jetzt.`);};
    $('#teacher-voice').onclick=()=>play(t.jp,false,false,t);
  }
  if(state.page==='review') {
    $$('[data-talk-review]').forEach(b=>b.onclick=()=>talkUI.open(b.dataset.talkReview,true));
    $$('[data-speech-review]').forEach(b=>b.onclick=()=>exerciseUI.reviewSpeech(b.dataset.speechReview));
    $('#review-audio').onclick=()=>play(state.review.jp);
    if($('#reveal'))$('#reveal').onclick=()=>{state.revealed=true;render();};
    for(const [id,known] of [['review-again',false],['review-known',true]])if($('#'+id))$('#'+id).onclick=()=>{reviewCard(course,known,state.review);nextReview();render();};
  }
  if(state.page==='library') {
    const update=()=>{$('#library-results').innerHTML=libraryRows();bindLibraryAudio();};
    $('#library-search').oninput=e=>{state.libraryQuery=e.target.value;update();};
    $('#library-all').onchange=e=>{store.data.library_all=e.target.checked;save();update();};bindLibraryAudio();
  }
  if(state.page==='settings') {
    $('#speed').onchange=e=>{store.data.tts_speed=Number(e.target.value);save();};
    $('#motion').onchange=e=>{store.data.motion_enabled=e.target.checked;save();document.body.classList.toggle('motion-off',!e.target.checked);animationStop();mascotStop();if(e.target.checked){animateTeacher();mascotStop=animateMascots(()=>store.data.motion_enabled&&store.data.motion_preset!=='off');}};
    $('#kiko').onchange=e=>{store.data.show_kiko=e.target.checked;save();};
    $('#export').onclick=()=>{save();if(bridge)native('exportProfile',JSON.stringify(store.data,null,2));else toast('Datei-Export ist in der installierten Android-App verfügbar.');};
    $('#import').onclick=()=>{if(bridge)native('importProfile');else toast('Datei-Import ist in der installierten Android-App verfügbar.');};
    $('#licenses').onclick=async()=>{const paths=['ANDROID_NOTICES.txt','MODEL_LICENSES.txt','MODEL_ATTRIBUTION.txt','LICENSE.txt','licenses/android/sherpa-onnx-APACHE-2.0.txt','licenses/android/onnxruntime-MIT.txt','licenses/android/silero-vad-MIT.txt','licenses/android/piper-phonemize-LICENSE.txt','licenses/android/espeak-ng-GPL-3.0.txt'];const texts=await Promise.all(paths.map(p=>fetch(p).then(r=>{if(!r.ok)throw Error('Lizenzdatei fehlt.');return r.text();})));state.licenseText=texts.join('\n\n');navigate('licenses');};
    bindSettingsBoxes();
  }
}
function bindSettingsBoxes() {
  if($('#download-models'))$('#download-models').onclick=()=>bridge?native('downloadModels'):toast('Das Sprachpaket wird in der installierten Android-App geladen.');
  if($('#cancel-models'))$('#cancel-models').onclick=()=>native('cancelDownload');
  if($('#check-updates'))$('#check-updates').onclick=()=>bridge?native('checkUpdates'):toast('Die Update-Prüfung ist in der Android-App verfügbar.');
  if($('#check-test-updates'))$('#check-test-updates').onclick=()=>bridge?native('checkTestUpdates'):toast('Die Prüfung auf Testversionen ist in der Android-App verfügbar.');
  if($('#install-update'))$('#install-update').onclick=()=>{save();native('installUpdate');};
}
function refreshSettingsBoxes() {if($('#models-box'))$('#models-box').innerHTML=modelBox();if($('#updates-box'))$('#updates-box').innerHTML=updateBox();bindSettingsBoxes();}
function bindLibraryAudio() {$$('[data-library-audio]').forEach(b=>b.onclick=()=>play(course.cards.find(c=>c.key===b.dataset.libraryAudio).jp));}
function play(text,forListen=false,slow=false,teacher=course.teacher()) {
  if(!bridge){toast('Die lokale Stimme läuft in der installierten Android-App.');return;}
  if(!state.caps.models){toast('Bitte zuerst unter Einstellungen das Sprachpaket laden.');return;}
  if(state.recording!=='idle'){toast('Bitte zuerst die Aufnahme beenden.');return;}
  const id=`audio-${++requestCounter}`;state.audio={id,forListen,context:state.session?`${state.session.key}:${state.session.phase}`:'',message:'Stimme wird vorbereitet …'};
  native('speak',text,teacher.speaker_id,Math.min(1.4,Math.max(.5,teacher.speed*store.data.tts_speed*(slow?.72:1))),id);refreshAudio();
  if(!['lesson','conversation'].includes(state.page))toast('Stimme wird vorbereitet …');
}
function record() {
  const s=state.session;
  if(state.page!=='lesson'||!s||s.mode!=='learn'||s.phase!=='speak'||s.success)return;
  if(state.recording==='recording'){state.recording='recognizing';native('stopRecording',false);refreshAudio();return;}
  if(state.recording!=='idle')return;
  if(!bridge){toast('Das Mikrofon ist in der installierten Android-App verfügbar.');return;}
  if(state.caps.models&&!s.audio_seen){toast('Höre die Vorlage zuerst vollständig an.');return;}
  native('stopAudio');state.audio=null;
  s.shortSpeechReady=false;
  state.ownSpeech=null;state.micLevel=0;state.micSeconds=0;
  const id=`speech-${++requestCounter}`;
  if(!s.support.begin(id))return;
  if(!state.caps.models){s.support.finish(id,'technical');state.speechMessage='Das Sprachpaket fehlt. Richte es unter Einstellungen ein oder nutze nach drei Versuchen die Auswahlhilfe.';refreshTask();return;}
  state.speech={id,context:`${s.key}:${s.phase}`,target:course.speechTarget(s.card,s.lesson),support:s.support};
  state.recording='requesting';state.speechMessage='Mikrofon wird vorbereitet …';native(isShortKana(s.card.jp)&&bridge?.recordKana?'recordKana':'record',id);refreshAudio();
}
function refreshAudio() {
  talkUI?.refresh();
  exerciseUI?.refresh();
  document.body.dataset.recording=state.recording;
  const s=state.session,button=$('#record');if(button) {button.textContent=s.success?(s.support.data.assisted?'✓ Mit Auswahlhilfe geschafft':s.metrics().last_speech_outcome==='self_check'?'✓ Selbst geprüft':'✓ Text passt'):!state.caps.models?'◉ Aufnahme versuchen':!s.audio_seen?'Erst die Vorlage anhören':{idle:'◉ Jetzt nachsprechen',requesting:'Mikrofon wird vorbereitet …',recording:'■ Aufnahme beenden',recognizing:'Sprache wird erkannt …'}[state.recording];button.disabled=s.success||(state.caps.models&&!s.audio_seen)||!['idle','recording'].includes(state.recording);button.classList.toggle('recording',state.recording==='recording');}
  if($('#speak-instruction'))$('#speak-instruction').textContent=s.success?'Geschafft! Weiter geht’s mit der Bedeutung.':s.audio_seen?'Jetzt bist du dran: Sprich die Vorlage nach.':'Höre die Vorlage an und sprich sie danach nach.';
  if(s?.phase==='listen')$$('[data-choice]').forEach(b=>b.disabled=s.success||!s.audio_seen);
  if($('#confirm-short-speech'))$('#confirm-short-speech').disabled=state.recording!=='idle'||!s.shortSpeechReady;
  if($('#speech-status'))$('#speech-status').textContent=state.speechMessage||(s?.phase==='speak'&&s.support.data.transcript?`Zuletzt erkannt: „${s.support.data.transcript}“`:'');
  $$('[data-support-choice],#speech-confirm,#speech-alternative,#speech-prepare,#hear-normal,#hear-slow').forEach(b=>b.disabled=state.recording!=='idle');
  if($('#lesson-own')){$('#lesson-own').hidden=!state.ownSpeech;$('#lesson-own').disabled=state.recording!=='idle';}
  if($('#lesson-cancel'))$('#lesson-cancel').hidden=state.recording==='idle';
  if($('.microphone-live'))$('.microphone-live').hidden=state.recording!=='recording';
  if($('#mic-level'))$('#mic-level').value=state.micLevel??0;
  if($('#mic-time'))$('#mic-time').textContent=`0:${String(Math.floor(state.micSeconds??0)).padStart(2,'0')}`;
  if($('#audio-status'))$('#audio-status').textContent=state.audio?.message??'';
  syncCoach(state);
}
window.JTNative=(type,data={})=> {
  if(!course)return;
  if(speechLab?.event(type,data))return;
  practiceUI?.event(type,data);
  if(dailyUI?.event(type,data))return;
  if(exerciseUI?.handle(type,data))return;
  if(type==='capabilities'){state.caps={...state.caps,...data};refreshSettingsBoxes();refreshAudio();}
  else if(type==='message')toast(data.message);
  else if(type==='modelProgress'){state.modelBusy=true;state.modelPercent=data.done/data.total*100;state.modelStatus=`${Math.round(data.done/1e6)} / ${Math.round(data.total/1e6)} MB · ${Math.floor(state.modelPercent)} %`;refreshSettingsBoxes();}
  else if(type==='modelsReady'){state.modelBusy=false;state.caps={...state.caps,...data};refreshSettingsBoxes();toast('Sprachpaket bereit. Du kannst jetzt offline hören und sprechen.');}
  else if(type==='modelError'){state.modelBusy=false;state.modelStatus=data.message;refreshSettingsBoxes();toast(data.message);}
  else if(type.startsWith('update')) {
    if(type==='updateChecking'){state.updateBusy=true;state.updateAvailable=false;state.updateTest=!!data.test;state.updateStatus=state.updateTest?'Suche nach Testversionen …':'Suche nach regulären Updates …';}
    if(type==='updateCurrent'){state.updateBusy=false;state.updateAvailable=false;state.updateStatus=data.test?'Keine neuere Testversion verfügbar.':'Keine neuere reguläre Android-Version verfügbar.';}
    if(type==='updateAvailable'){state.updateBusy=false;state.updateAvailable=true;state.updateTest=!!data.test;state.updateStatus=`${state.updateTest?'Testversion':'Version'} ${data.name} ist verfügbar. ${data.notes??''}`;}
    if(type==='updateProgress'){state.updateBusy=true;state.updateStatus=`Update wird geladen: ${Math.floor(data.done/data.total*100)} %`;}
    if(type==='updateReady'){state.updateBusy=false;state.updateAvailable=true;state.updateStatus='Download und Herausgeber geprüft. Android fragt nach deiner Bestätigung.';}
    if(type==='updateError'){state.updateBusy=false;state.updateStatus=data.message;}
    refreshSettingsBoxes();
  } else if(type==='profileCandidate') {
    try {const profile=cleanProfile(JSON.parse(data.json),true);native('confirmImport',JSON.stringify(profile));}catch(e){toast(e.message);}
  } else if(type==='profileImported') {practiceUI?.reset();dailyUI?.reset();exerciseUI?.reset();store.data=cleanProfile(data,true);state.session=null;state.review=null;talkUI?.reset();navigate('home');toast('Lernstand übernommen.');}
  else if(type==='audioCancelled'){state.speech?.support?.cancel();state.audio=null;state.speech=null;state.ownSpeech=null;if(state.session)state.session.shortSpeechReady=false;state.recording='idle';state.speechMessage='';refreshAudio();}
  else if(type.startsWith('audio')&&data.request===state.audio?.id) {
    if(type==='audioLoading')state.audio.message='Stimme wird vorbereitet …';
    if(type==='audioStarted'){state.audio.message='Wiedergabe läuft …';state.audio.started=true;}
    if(type==='audioDone') {if(state.audio.forListen&&state.session&&state.audio.context===`${state.session.key}:${state.session.phase}`)state.session.audio_seen=true;state.audio=null;}
    if(type==='audioError'){toast(data.message);state.audio=null;}
    refreshAudio();
  } else if(data.request===state.speech?.id) {
    if(type==='speechLevel'){state.micLevel=data.level;state.micSeconds=data.seconds;}
    if(type==='recording'){state.recording='recording';state.speechMessage='Sprich jetzt. Nach spätestens 15 Sekunden endet die Aufnahme.';}
    if(type==='recognizing'){state.recording='recognizing';state.speechMessage='Dein Handy wertet die Aufnahme lokal aus …';}
    if(type==='speechError'){state.recording='idle';state.speechMessage=data.message;state.speech.support?.finish(data.request,'technical');state.speech=null;if(state.page==='lesson'){state.session.feedback=state.session.support.data.feedback;state.session.snapshot();refreshTask();}else if(state.page==='conversation')render();}
    if(type==='speechResult') {
      state.recording='idle';const s=state.session;
      if(state.speech.kind==='talk')talkUI?.recognized(data.text,state.speech.context);
      else if(state.page==='lesson'&&s&&s.mode==='learn'&&s.phase==='speak'&&state.speech.context===`${s.key}:${s.phase}`) {
        if(state.speech.support.active!==data.request)return;
        state.ownSpeech=state.speech.id;
        const heard=data.text??'';
        if(!applyKanaRecognition(s,heard,data.audioQualified===true&&data.shortKana===true)&&heard.trim()&&!(data.shortKana===true&&data.audioQualified!==true))s.checkSpeech(heard);
        state.speech.support?.finish(data.request,s.success?'accepted':!heard.trim()||data.shortKana&&!data.audioQualified?'unreliable':'mismatch');
        if(!s.success&&s.support.data.reason==='unreliable'){s.feedback=s.support.data.feedback;s.snapshot();}
        s.support.data.transcript=heard;s.support.save();
        state.speechMessage=data.text?`Erkannt: „${data.text}“`:'Die Aufnahme konnte nicht sicher verschriftlicht werden.';
        refreshTask();
      }
      state.speech=null;
    }
    refreshAudio();
  }
};
window.JTBack=()=> {if(closeFocusSheet())return;if(state.page==='home')native('closeApp');else navigate(state.page==='exercises'?exerciseUI.backPage():state.page==='lesson'?'course':state.page==='conversation'?'talk':state.page==='talk'?'review':state.page==='licenses'?'settings':'home');};
function animateTeacher() {
  animationStop();const canvas=$('#teacher-canvas');if(!canvas)return;
  const teacher=catalog.TEACHERS.find(t=>t.id===canvas.dataset.teacher)??course.teacher();
  animationStop=runTeacher({teacher,blinkIndex,expressions,enabled:()=>store.data.motion_enabled&&store.data.motion_preset!=='off'});
}
// Even handlers that consume comparison/exercise events update the visible coach.
const handleNative=window.JTNative;
window.JTNative=(type,data)=>{try{return handleNative(type,data);}finally{syncCoach(state);}};
async function start() {
  const files=['data/course.json','data/catalog.json','data/deep_lessons.json','assets/animation/blink_index.json','assets/animation/expressions.json','data/exercises.json','data/practice_content.json','data/speech_trial.json'];
  const [raw,c,d,b,e,exerciseData,practiceData,trialData]=await Promise.all(files.map(p=>fetch(p).then(r=>{if(!r.ok)throw Error('Kursdatei fehlt: '+p);return r.json();})));
  catalog=c;blinkIndex=b;expressions=e;
  document.addEventListener('jt-actors',()=>animateTeacher());
  document.addEventListener('visibilitychange',()=>{document.body.dataset.actorsPaused=String(document.hidden);animationStop();mascotStop();if(document.hidden)stopMedia();else {syncCoach(state);animateTeacher();mascotStop=animateMascots(()=>store.data.motion_enabled&&store.data.motion_preset!=='off');}});
  let profile={};try{profile=JSON.parse(bridge?native('getProfile'):localStorage.getItem('jt-mobile-profile')??'{}');}catch(error){toast('Lernstand ist nicht lesbar. Bitte eine Sicherung importieren.');}
  store=new Store(profile,persist);course=new Course(raw,c,d,store);
  exerciseUI=createExerciseUI({data:exerciseData,state,store,course,native,navigate,render,stopMedia,toast,esc,nextRequest:()=>`exercise-${++requestCounter}`,explanation,lessonGuide,focusLesson});
  practiceUI=createPracticeUI({data:practiceData,state,store,course,play,stopMedia,navigate,render,esc,toast});
  dailyUI=createDailyUI({state,store,course,native,play,stopMedia,navigate,render,toast,esc,nextRequest:()=>`daily-${++requestCounter}`});
  speechLab=createSpeechLab({data:trialData,state,native,play,stopMedia,render,esc,toast,nextRequest:()=>`speech-lab-${++requestCounter}`});
  talkUI=createTalkUI({state,store,course,native,play,stopMedia,navigate,render,toast,esc,nextRequest:()=>`talk-speech-${++requestCounter}`});
  if(bridge)state.caps={...state.caps,...JSON.parse(native('getCapabilities'))};
  else {const pack=await fetch('model-pack.json').then(r=>r.json());state.caps.modelBytes=pack.bytes;}
  $$('.bottom-nav button').forEach(button=>button.onclick=()=>navigate(button.dataset.page));
  $('#settings-shortcut').onclick=()=>navigate('settings');$('.brand').onclick=e=>{e.preventDefault();navigate('home');};
  document.addEventListener('visibilitychange',()=>{if(document.hidden){if(state.page==='conversation')talkUI?.save();stopMedia();save();}});
  document.addEventListener('focusin',e=>{if(e.target.matches('input[type=text],input[type=search]'))document.body.classList.add('keyboard');});
  document.addEventListener('focusout',()=>{setTimeout(()=>{if(!document.activeElement.matches('input[type=text],input[type=search]'))document.body.classList.remove('keyboard');},100);});
  render();document.documentElement.dataset.ready='true';if(state.caps.profileWarning)toast(state.caps.profileWarning);
}
start().catch(error=>{$('#app').innerHTML=`<div class="info error"><h1>Start nicht möglich</h1><p>${esc(error.message)}</p><p>Bitte starte die App erneut. Deine Lernstand-Datei wird nicht absichtlich gelöscht.</p></div>`;console.error(error);});

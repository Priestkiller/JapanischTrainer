import {dailyPlan,finishDaily,SKILL_LABELS} from './adaptive.mjs';
import {shuffle,matchesRomaji,speechMatch,isShortKana} from './core.mjs';

export function createDailyUI({state,store,course,native,play,stopMedia,navigate,render,toast,esc,nextRequest}){
 const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
 let task=null,heard=false,help=false,helpUsed=false,success=false,feedback='',draft='',request=null,audioId=null;
 function plan(){
  const lesson=course.next(),cursor=store.data.last_lesson;
  const start=cursor.key===lesson.key?Math.max(0,cursor.card??0):0;
  const upcoming=store.data.completed.includes(lesson.key)?[]:course.cards.filter(c=>c.lesson_key===lesson.key).slice(start,start+2);
  const p=dailyPlan(store.data,course.cards,course.available(),upcoming);store.save();return p;
 }
 const card=()=>course.cards.find(c=>c.key===task?.card);
 function open(){task=null;pick();navigate('daily');}
 function pick(){const p=plan();task=p.tasks.find(t=>!p.done.includes(t.id))??null;heard=false;help=false;helpUsed=false;success=false;feedback='';draft='';request=null;audioId=null;}
 function summary(){const p=plan();return `<section class="card daily-summary"><span class="pill">Deine persönliche Runde</span><h2>Heute für dich</h2><p>${p.done.length} / ${p.tasks.length} kleine Aufgaben · bekannte Wörter gezielt wiederholen und bis zu zwei Karten kennenlernen.</p><button class="primary wide" data-nav="daily">${p.tasks.length&&p.done.length===p.tasks.length?'Heutige Runde ansehen':'Meine Runde starten'} →</button><p class="sub">Kursfortschritt und XP bleiben getrennt. Freiwilliges Sprechen lässt sich später wiederholen.</p></section>`;}
 function options(){const c=card(),lesson=course.byKey.get(c.lesson_key);
  const correct=task.skill==='use'?course.profile(c,lesson).scenario.correct:c.de;
  const pool=task.skill==='use'?course.profile(c,lesson).scenario.wrong:course.cards.filter(x=>x.lesson_key===c.lesson_key||store.data.adaptive.introduced.includes(x.key)).map(x=>x.de);
  return {correct,values:shuffle([correct,...shuffle([...new Set(pool)].filter(v=>v!==correct),task.id).slice(0,3)],task.id+'options')};
 }
 function view(){
  const p=plan();if(!task||!p.tasks.some(t=>t.id===task.id))pick();
  if(!task)return `<section class="card daily-card"><span class="pill success">${p.tasks.length?'Deine Runde ist geschafft':'Heute ist nichts fällig'}</span><h1>Ein guter Schritt für heute.</h1><p>Du hast ${p.done.length} Aufgaben bearbeitet. Dein regulärer Lernweg bleibt an seiner bisherigen Stelle.</p><button class="primary wide" data-nav="course">Im Kurs weiterlernen →</button><button class="ghost wide" data-nav="practice-lab">Hörsituationen & Zeichen</button><button class="ghost wide" data-nav="talk">Gespräche üben</button></section>`;
  const c=card(),lesson=course.byKey.get(c.lesson_key),profile=course.profile(c,lesson),intro=task.skill==='intro',speaking=task.skill==='speak';
  const cue={intro:'Lerne Bedeutung und Verwendung kennen.',read:'Welche Bedeutung passt?',listen:'Höre zu. Welche Bedeutung passt?',write:'Schreibe die japanische Lesung in Romaji.',speak:'Höre die Vorlage und sprich sie nach.',use:profile.scenario.question}[task.skill];
  const target=intro||speaking?`<p class="jp" lang="ja">${esc(c.jp)}</p><p class="romaji">${esc(c.romaji)}</p><p>${esc(c.de)}</p><p class="sub">Aussprachehilfe (Annäherung): ${esc(c.approx??c.pron_de??c.pron??'Höre auf die Vorlage.')}</p>`:task.skill==='read'?`<p class="jp" lang="ja">${esc(c.jp)}</p>`:task.skill==='write'?`<p>${esc(c.de)}</p>`:'';
  return `<div class="daily-layout"><div class="lesson-header"><button class="back-button" data-nav="home" aria-label="Runde verlassen">×</button><div><h1>${esc(SKILL_LABELS[task.skill])}</h1><p class="sub">${p.done.length+1} / ${p.tasks.length} · Heute für dich</p></div></div>
  <section class="card daily-card"><h2>${esc(cue)}</h2>${target}
  ${['intro','listen','speak'].includes(task.skill)?'<div class="row"><button class="primary" id="daily-audio">▷ Anhören</button><button class="ghost" id="daily-slow">▷ Langsam</button></div>':''}
  ${intro?`<p>${esc(profile.usage)}</p><p class="sub">${esc(profile.explain)}</p><p class="sub">Kennenlernen schließt noch keine Kurslektion ab.</p>`:speaking?'<button class="record-button wide" id="daily-record">◉ Nachsprechen</button>':task.skill==='write'?`<label class="field"><span>Deine Lesung</span><input id="daily-input" maxlength="200" autocomplete="off" spellcheck="false" value="${esc(draft)}"></label>`:`<div class="options">${options().values.map((v,i)=>`<button class="option" data-daily-choice="${i}" ${success?'disabled':''}>${esc(v)}</button>`).join('')}</div>`}
  ${!intro?`<button class="ghost small" id="daily-help" aria-expanded="${help}">Hinweis & Erklärung</button>${help?`<div class="info"><p lang="ja">${esc(c.jp)} · ${esc(c.romaji)}</p><p>${esc(c.de)}</p><p>${esc(profile.explain)}</p><p class="sub">Mit geöffneter Hilfe wird die Antwort als unterstützt gespeichert.</p></div>`:''}`:''}
  <p id="daily-status" class="feedback" role="status">${esc(feedback)}</p></section>
  <div class="daily-footer">${success?'<button class="primary wide" id="daily-next">Weiter →</button>':intro?'<button class="primary wide" id="daily-intro">Karte kennengelernt →</button>':task.skill==='write'?'<button class="primary wide" id="daily-check">Überprüfen →</button>':''}
  ${speaking&&!success?'<button class="ghost wide" id="daily-defer">Sprechen später üben</button>':''}</div></div>`;
 }
 function mark(ok,message,assisted=helpUsed){if(success)return;success=finishDaily(store.data,task,ok,assisted);feedback=message;if(!ok)helpUsed=true;store.touch();store.save();render();}
 function feedbackFor(value){const c=card(),other=course.cards.find(x=>x.de===value);return `${other?`Deine Auswahl bedeutet „${other.jp}“ (${other.romaji}). `:''}${course.profile(c,course.byKey.get(c.lesson_key)).explain} Versuche es noch einmal.`;}
 function listen(slow=false){play(card().jp,false,slow);audioId=state.audio?.id??null;feedback='Höre die Vorlage vollständig an.';const el=$('#daily-status');if(el)el.textContent=feedback;}
 function bind(){
  if(state.page!=='daily')return;
  if($('#daily-next'))$('#daily-next').onclick=()=>{stopMedia();pick();render();};
  if($('#daily-audio'))$('#daily-audio').onclick=()=>listen();if($('#daily-slow'))$('#daily-slow').onclick=()=>listen(true);
  if($('#daily-help'))$('#daily-help').onclick=()=>{help=!help;helpUsed||=help;render();};
  $$('[data-daily-choice]').forEach(b=>b.onclick=()=>{if(task.skill==='listen'&&!heard){feedback='Höre das Beispiel zuerst vollständig an.';render();return;}const o=options(),value=o.values[+b.dataset.dailyChoice];mark(value===o.correct,value===o.correct?'Richtig. Diese Fähigkeit wird später gezielt wiederholt.':feedbackFor(value));});
  if($('#daily-input'))$('#daily-input').oninput=e=>{draft=e.target.value;};
  if($('#daily-check'))$('#daily-check').onclick=()=>{const c=card(),ok=[c.romaji,...(c.romaji_aliases??[])].some(x=>matchesRomaji(draft,x));mark(ok,ok?'Die Lesung passt.':course.profile(c,course.byKey.get(c.lesson_key)).pitfall+' Prüfe die Lesung und die Vokallänge.');};
  if($('#daily-intro'))$('#daily-intro').onclick=()=>mark(true,'Kennengelernt. Du wirst diese Karte später wiederholen.');
  if($('#daily-defer'))$('#daily-defer').onclick=()=>mark(true,'Für später vorgemerkt. Das ist keine bestandene Sprechprüfung.',true);
  if($('#daily-record'))$('#daily-record').onclick=()=>{
   if(state.recording==='recording'){native('stopRecording',false);return;}
   if(state.recording!=='idle'||success)return;
   if(!heard){feedback='Höre die Vorlage zuerst vollständig an.';render();return;}
   if(!state.caps.native||!state.caps.models){toast('Für Sprechen brauchst du die installierte App und das Sprachpaket. Du kannst die Aufgabe für später vormerken.');return;}
   request=nextRequest();state.recording='requesting';state.speech={id:request,kind:'daily'};native(isShortKana(card().jp)?'recordKana':'record',request);
  };
 }
 function event(type,data){
  if(state.page!=='daily')return false;
  if(type==='audioDone'&&data.request===audioId){heard=true;feedback='Vorlage gehört. Du bist dran.';$('#daily-status').textContent=feedback;}
  if(!request||data.request!==request)return false;
  if(type==='recording'){$('#daily-record').textContent='■ Aufnahme beenden';state.recording='recording';}
  if(type==='recognizing'){$('#daily-record').textContent='Erkennung läuft …';state.recording='recognizing';}
  if(type==='speechResult'||type==='speechError'){
   request=null;state.recording='idle';state.speech=null;
   if(type==='speechError'){feedback=data.message;render();return true;}
   const c=card(),target=course.speechTarget(c,course.byKey.get(c.lesson_key)),ok=speechMatch(data.text,[target.target,...(target.accept??[])]);
   mark(ok,ok?'Der erkannte Text passt.':`Erkannt: „${data.text??''}“. Die Erkennung ist möglicherweise unsicher. Höre erneut oder merke Sprechen für später vor.`);
  }
  return true;
 }
 return {view,bind,summary,open,event,reset:()=>{task=null;request=null;}};
}

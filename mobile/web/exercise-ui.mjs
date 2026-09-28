import {ExerciseBook,ExerciseRound,FAMILIES,order} from './exercises.mjs';

export function createExerciseUI({data,state,store,course,native,navigate,render,stopMedia,toast,esc,nextRequest,explanation,lessonGuide,focusLesson}) {
 const book=new ExerciseBook(data),$=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
 let round=null,epoch=0,composing=false,ownRequest=null;
 const card=key=>{const at=key.lastIndexOf(':');return course.byKey.get(key.slice(0,at)).cards[Number(key.slice(at+1))];};
 const context=()=>round?`${round.task.id}:${round.state.stage}:${epoch}:${course.teacher().id}`:'';
 const audioReady=()=>{if(!state.caps.native){toast('Die lokale Stimme ist in der installierten Android-App verfügbar.');return false;}if(!state.caps.models){round.technical('Das lokale Sprachpaket fehlt. Lade es unter Einstellungen oder pausiere.');refresh();return false;}return true;};
 function open(key){composing=false;if(!course.unlocked(key)||!book.packs.has(key))return;round=new ExerciseRound(book,course.byKey.get(key),store);epoch++;ownRequest=null;navigate('exercises');}
 function cancel(){composing=false;epoch++;ownRequest=null;if(round)round.save();}
 function reset(){composing=false;epoch++;ownRequest=null;round=null;}
 function source(key){const c=card(key),l=course.byKey.get(key.slice(0,key.lastIndexOf(':')));return `<div class="exercise-source"><p class="jp" lang="ja">${esc(c.jp)}</p><p class="romaji">${esc(c.romaji)}</p><p class="translation">${esc(c.de)}</p><p class="pronunciation">Aussprachehilfe · deutsche Näherung: ${esc(c.approx??'')} ${esc(c.note??'')}</p><div class="audio-actions"><button data-ex-teach="${esc(key)}">▷ Normal</button><button data-ex-teach="${esc(key)}" data-slow="true">▷ Langsam</button></div>${explanation(c,l).replace(/<button[^>]*id="hear-example"[^>]*>[\s\S]*?<\/button>/g,'')}</div>`;}
 const button=(id,label,disabled=false,extra='')=>`<button id="${id}" class="ghost wide" ${disabled?'disabled':''} ${extra}>${label}</button>`;
 function view(){if(!round)return '';const r=round,s=r.state,d=r.answer,t=r.task,teacher=course.teacher();
  const count=s.stage==='intro'?'Einführung · ohne Bewertung':s.stage==='complete'?'Zusatzrunde beendet':s.stage==='review'?`Das üben wir noch einmal · ${s.review_index+1}/${s.review.length}`:`Aufgabe ${s.index+1}/${s.queue.length} · Zusatztraining`;
  let content='';
  if(s.stage==='intro')content=`<h2>Erst verstehen, dann ausprobieren</h2><p>Hier werden alle benötigten Ausdrücke mit Bedeutung und Lesung eingeführt. Die Zusatzrunde ersetzt keine Pflichtschritte und vergibt keine zusätzlichen XP.</p>${lessonGuide(r.lesson,true)}${r.pack.introduced.map(source).join('')}`;
  else if(s.stage==='complete'){
   const labels={independent:'selbstständig im ersten Versuch',hint:'mit Hinweis',solution:'nach angezeigter Erklärung',corrected:'nach Korrektur',wrong:'noch nicht passend',technical:'technischer Hinweis',unverified:'nicht sicher prüfbar',paused:'pausiert'},counts={};for(const e of s.outcomes)counts[e.result]=(counts[e.result]??0)+1;
   content=`<h2>Deine Übungsrunde</h2><ul>${Object.entries(counts).map(([k,v])=>`<li>${esc(labels[k]??k)}: ${v}</li>`).join('')}</ul><p>Fehler sind in der vorhandenen Wiederholungsplanung vorgemerkt. Pflichtschritte und XP wurden nicht verändert.</p>`;
  }else{
   content=`<h2>${FAMILIES[t.family]}</h2><p id="ex-prompt">${esc(t.prompt)}</p>`;
   if(t.family==='echo'){
    const c=card(t.card);content+=`<div class="speaking-card"><p class="jp" lang="ja">${esc(c.jp)}</p><p class="romaji">${esc(c.romaji)}</p><p>${esc(c.de)}</p><p class="pronunciation">Aussprachehilfe · Näherung: ${esc(c.approx??'')} ${esc(c.note??'')}</p></div>`;
   }
   if(t.family==='read'){
    const text=esc(t.text),evidence=esc(t.evidence);content+=`<p class="jp exercise-reading" lang="ja">${d.checks?text.replace(evidence,`<mark>${evidence}</mark>`):text}</p>`;
   }
   if(['choice_gap','hear_gap'].includes(t.family))content+=`<p class="jp exercise-frame" lang="ja">${esc(t.frame)}</p>`;
   if(['echo','hear_gap','read'].includes(t.family)||(t.family==='recall'&&d.help===2))content+=`<div class="audio-actions">${button('ex-audio','▷ Normal'+(t.family==='read'?' · Lesehilfe':''),state.recording!=='idle')}${button('ex-slow','▷ Langsam',state.recording!=='idle')}</div>`;
   if(t.family==='pairs'){
    const left=order(t.pairs,t.id+':left'),right=order(t.pairs,t.id+':right');content+='<div class="exercise-pairs">';
    for(let i=0;i<left.length;i++){const a=left[i],b=right[i],linked=t.pairs.find(p=>p.id===d.pairs[a.id]);
     content+=`<button data-ex-left="${a.id}" aria-pressed="${d.left===a.id}" ${d.success?'disabled':''}>${t.mode==='audio'?`▷ Ton ${i+1}`:esc(a.jp)}<small>${d.left===a.id?'Ausgewählt · ':''}${linked?'→ '+esc(linked.de):'Noch offen'}${d.checks&&d.pairs[a.id]===a.id?' · ✓ passend':''}</small></button><button data-ex-right="${b.id}" ${d.success?'disabled':''}>${esc(b.de)}</button>`;
    }content+='</div>';
   }else if(['choice_gap','read'].includes(t.family))content+=`<div class="options">${order(t.choices,t.id).map(c=>`<button data-ex-choice="${c.id}" aria-pressed="${d.choice===c.id}" ${d.success?'disabled':''}>${d.choice===c.id?'● ':'○ '}${esc(c.text)}</button>`).join('')}</div>`;
   else if(t.family==='hear_gap')content+=`<label class="field"><span>Nur die fehlende Einheit · Eingabe in Romaji</span><input id="ex-input" value="${esc(d.text)}" type="text" autocomplete="off" autocapitalize="none" spellcheck="false" enterkeyhint="done" ${d.success?'disabled':''}></label>`;
   else if(['translate','multi_gap'].includes(t.family)){
    const by=Object.fromEntries(t.tokens.map(x=>[x.id,x.text]));
    if(t.family==='translate')content+=`<div class="token-board">${d.tokens.length?d.tokens.map(i=>`<button data-ex-token="${i}" ${d.success?'disabled':''}>${esc(by[i])} ×</button>`).join(''):'Tippe die Bausteine in der gewünschten Reihenfolge an.'}</div>`;
    else content+=`<p class="jp exercise-frame">${t.frame.map(v=>v.startsWith('□')?`<button data-ex-slot="${Number(v.slice(1))-1}" aria-pressed="${d.active===Number(v.slice(1))-1}">Lücke ${v.slice(1)}${d.active===Number(v.slice(1))-1?' · aktiv':''}: ${esc(by[d.slots[Number(v.slice(1))-1]]??'leer')}</button>`:esc(v)).join(' ')}</p>`;
    content+=`<div class="tokens">${order(t.tokens,t.id).map(token=>`<button data-ex-token="${token.id}" ${d.success?'disabled':''}>${esc(token.text)}${d.tokens.includes(token.id)||Object.values(d.slots).includes(token.id)?' ✓':''}</button>`).join('')}</div>${button('ex-reset','Zurücksetzen',d.success)}`;
   }
   if(['echo','recall'].includes(t.family))content+=`${button('ex-record',state.recording==='recording'?'■ Aufnahme beenden':'◉ Jetzt sprechen',d.success||!['idle','recording'].includes(state.recording))}${ownRequest?button('ex-own','▷ Eigene Aufnahme',state.recording!=='idle'):''}<p class="sub">Lokaler Textvergleich, keine Aussprache- oder Tonhöhennote. Kurze Wörter können unsicher erkannt werden.</p>${d.transcript?`<p>Erkannt: ${esc(d.transcript)}</p>`:''}`;
   else content+=button('ex-check','Prüfen',d.success);
   content+=`<p id="ex-audio-status" class="speech-message" role="status"></p>${button('ex-help',d.help_open?'Hilfe schließen':'Erklären / Warum?')}`;
   if(d.help_open){content+=`<aside class="exercise-hint"><h3>Hinweis ohne vollständige Lösung</h3><p>${esc(t.hint)}</p>`;
    if(d.help<2)content+=button('ex-solution','Vollständig erklären · Lösung zeigen');
    else content+=`<p class="sub">Nachgeschaut · dieser Versuch bleibt als unterstützt erkennbar.</p><p>${esc(t.solution)}</p>${['pairs','read'].includes(t.family)?t.prerequisites.map(source).join(''):source(t.card)}`;
    content+='</aside>';
   }
   if(t.family==='echo')content+=`<details><summary>Ausführliche Bedeutung und Verwendung</summary>${explanation(card(t.card),r.lesson).replace(/<button[^>]*id="hear-example"[^>]*>[\s\S]*?<\/button>/g,'')}</details>`;
   if(d.feedback)content+=`<div class="feedback ${d.success?'correct':''}" role="status">${esc(d.feedback)}</div>`;
  }
  const nextLabel=s.stage==='intro'?'Einführung gelesen · jetzt üben':s.stage==='complete'?'Neue Runde':'Weiter →';
  return `<div class="lesson-layout exercise-variety"><div class="lesson-header"><button id="ex-back" class="back-button" aria-label="Pause und zurück zur Lektion">‹</button><div><h1>${esc(r.lesson.title)}</h1><p class="sub">${esc(count)}</p></div></div><div class="coach"><img src="assets/teachers/${teacher.id}/avatar.png" alt=""><div><strong>${esc(teacher.name)} begleitet dich</strong><p class="sub">Fragen und Nachschauen sind erlaubt.</p></div></div><section class="card" id="exercise-content" data-family="${t.family}">${content}<div class="task-footer">${button('ex-next',nextLabel,!['intro','complete'].includes(s.stage)&&!d.success)}</div>${button('ex-pause','Kann gerade nicht hören / sprechen · Pause')}</section></div>`;
 }
 function refresh(){if(state.page==='exercises'){const focused=document.activeElement?.id,selection=focused==='ex-input'?[$('#ex-input').selectionStart,$('#ex-input').selectionEnd]:null,scroll=window.scrollY;$('#app').innerHTML=view();bind();window.scrollTo(0,scroll);if(selection&&$('#ex-input')){$('#ex-input').focus({preventScroll:true});$('#ex-input').setSelectionRange(...selection);}audioStatus();}}
 function audioStatus(){if($('#ex-audio-status'))$('#ex-audio-status').textContent=state.recording==='idle'?(state.audio?.message??''):state.speechMessage;const b=$('#ex-record');if(b){b.textContent=state.recording==='recording'?'■ Aufnahme beenden':state.recording==='recognizing'?'Wird lokal erkannt …':'◉ Jetzt sprechen';b.disabled=round.answer.success||!['idle','recording'].includes(state.recording);}}
 function play(identity='target',slow=false,own=false,sourceKey=null){if(!round||state.recording!=='idle'||!audioReady())return;const t=round.task,teacher=course.teacher(),id=nextRequest();
  if(t.family==='recall'&&!own)round.help(2);
  const text=sourceKey?card(sourceKey).jp:t.family==='pairs'?t.pairs.find(p=>p.id===identity).jp:(t.text??t.audio);
  state.audio={id,kind:'exercise',context:context(),identity,own,sourceKey,message:'Stimme wird vorbereitet …'};
  if(own)native('playRecording',ownRequest,id);else native('speak',text,teacher.speaker_id,Math.min(1.4,Math.max(.5,teacher.speed*store.data.tts_speed*(slow?.72:1))),id);
  audioStatus();
 }
 function record(){if(!round)return;const r=round;
  if(state.recording==='recording'){state.recording='recognizing';native('stopRecording',false);audioStatus();return;}
  if(state.recording!=='idle'||r.answer.success||!audioReady())return;
  if(r.task.family==='echo'&&!r.answer.heard.includes('target')){r.technical('Höre die Vorlage zuerst vollständig an.');refresh();return;}
  native('stopAudio');state.audio=null;ownRequest=null;const id=nextRequest();state.speech={id,kind:'exercise',context:context()};state.recording='requesting';state.speechMessage='Mikrofon wird vorbereitet …';native('record',id);audioStatus();
 }
 function handle(type,data){
  if(type==='audioCancelled'){ownRequest=null;epoch++;return false;}
  if(state.audio?.kind==='exercise'&&data.request===state.audio.id){const a=state.audio;if(state.page!=='exercises'||a.context!==context()){state.audio=null;return true;}
   if(type==='audioLoading')a.message='Stimme wird vorbereitet …';if(type==='audioStarted')a.message='Wiedergabe läuft …';
   if(type==='audioDone'){if(!a.own&&!a.sourceKey)round.heard(a.identity,round.task.family==='read');state.audio=null;}
   if(type==='audioError'){round.technical(data.message??'Audio nicht verfügbar. Du kannst erneut versuchen oder pausieren.');state.audio=null;refresh();}
   audioStatus();return true;
  }
  if(state.speech?.kind==='exercise'&&data.request===state.speech.id){const request=state.speech;
   if(state.page!=='exercises'||request.context!==context()){state.speech=null;state.recording='idle';return true;}
   if(type==='recording'){state.recording='recording';state.speechMessage='Sprich jetzt. Die Vorlage bleibt beim Nachsprechen sichtbar.';}
   if(type==='recognizing'){state.recording='recognizing';state.speechMessage='Dein Handy erkennt die Aufnahme lokal …';}
   if(type==='speechError'){state.recording='idle';round.technical(data.message??'Keine sichere Erkennung.');state.speech=null;refresh();}
   if(type==='speechResult'){state.recording='idle';ownRequest=request.id;round.check(data.text??'');state.speech=null;refresh();}
   audioStatus();return true;
  }return false;
 }
 function bind(){if(state.page!=='exercises'||!round)return;focusLesson({page:state.page,round,teacher:course.teacher(),store,esc});const r=round,d=r.answer,t=r.task;
  const on=(id,fn)=>{if($('#'+id))$('#'+id).onclick=fn;};
  const back=()=>{r.technical('Freiwillig pausiert. Die Aufgabe und deine Eingabe bleiben erhalten.',true);stopMedia();navigate('lesson');};
  on('ex-back',back);on('ex-pause',back);
  on('ex-next',()=>{if(state.recording!=='idle')return;stopMedia();ownRequest=null;epoch++;if(r.state.stage==='intro')r.start();else if(r.state.stage==='complete')r.restart();else r.advance();refresh();window.scrollTo(0,0);});
  on('ex-help',()=>{if(d.help)r.set('help_open',!d.help_open);else r.help(1);refresh();});on('ex-solution',()=>{r.help(2);refresh();});
  on('ex-check',()=>{if(composing)return;r.check();refresh();});on('ex-audio',()=>play());on('ex-slow',()=>play('target',true));on('ex-own',()=>play('target',false,true));on('ex-record',record);
  $$('[data-ex-choice]').forEach(b=>b.onclick=()=>{r.set('choice',b.dataset.exChoice);refresh();});
  $$('[data-ex-left]').forEach(b=>b.onclick=()=>{r.set('left',b.dataset.exLeft);refresh();if(t.mode==='audio')play(b.dataset.exLeft);});
  $$('[data-ex-right]').forEach(b=>b.onclick=()=>{if(!d.left||d.success)return;const pairs=Object.fromEntries(Object.entries(d.pairs).filter(([,v])=>v!==b.dataset.exRight));pairs[d.left]=b.dataset.exRight;r.set('pairs',pairs);refresh();});
  $$('[data-ex-slot]').forEach(b=>b.onclick=()=>{r.set('active',Number(b.dataset.exSlot));refresh();});
  $$('[data-ex-token]').forEach(b=>b.onclick=()=>{if(d.success)return;const id=b.dataset.exToken;
   if(t.family==='multi_gap'){const slots=Object.fromEntries(Object.entries(d.slots).filter(([,v])=>v!==id));if(d.slots[d.active]!==id)slots[d.active]=id;r.set('slots',slots);}
   else r.set('tokens',d.tokens.includes(id)?d.tokens.filter(i=>i!==id):[...d.tokens,id]);refresh();});
  on('ex-reset',()=>{r.set(t.family==='translate'?'tokens':'slots',t.family==='translate'?[]:{});refresh();});
  const input=$('#ex-input');if(input){input.oninput=()=>r.set('text',input.value);input.oncompositionstart=()=>{composing=true;};input.oncompositionend=()=>{composing=false;r.set('text',input.value);};input.onkeydown=e=>{if(e.key==='Enter'){e.preventDefault();if(!composing&&!e.isComposing&&e.keyCode!==229){r.set('text',input.value);r.check();refresh();}}};}
  $$('[data-ex-teach]').forEach(b=>b.onclick=()=>play('teaching',b.dataset.slow==='true',false,b.dataset.exTeach));
 }
 return {book,open,view,bind,handle,cancel,reset,refresh:audioStatus,has:key=>book.packs.has(key)};
}

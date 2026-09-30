import {speechMatch} from './core.mjs';
const NAMES={sensevoice:'SenseVoice (Standard)',reazonspeech:'ReazonSpeech (experimentell)',qwen3:'Qwen3 ASR (experimentell)'};
const KEY='jt-speech-trial-v1';
export function createSpeechLab({data,state,native,play,stopMedia,render,esc,toast,nextRequest}){
 const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
 let rows=[];try{const old=JSON.parse(localStorage.getItem(KEY)||'[]');if(Array.isArray(old))rows=old.slice(-200).filter(x=>x&&typeof x.id==='string');}catch{}
 let index=0,request=null,last=null,status='',busy=false,download='',own=null;
 const prompt=()=>data.prompts[index];
 function save(){try{localStorage.setItem(KEY,JSON.stringify(rows.slice(-200)));}catch{toast('Testergebnisse konnten nicht gespeichert werden. Bitte exportieren.');}}
 function view(){const p=prompt(),caps=state.caps;
 return `<h1>Lokaler Sprachvergleich</h1><section class="card"><p>${esc(data.notice)}</p><p class="sub">Die Modelle bekommen nur die Aufnahme, niemals den erwarteten Text. Ein Textvergleich bewertet keine Aussprache. Größere Modelle sind nicht automatisch besser.</p><details><summary>Optionale Erkennungsmodelle</summary><p>Das Grundpaket bleibt erhalten. Zusatzmodelle werden nur auf deinen Wunsch geladen und geprüft. ReazonSpeech: etwa 127 MB; Qwen3: etwa 845 MB Download und deutlich mehr Arbeitsspeicher.</p>${['reazonspeech','qwen3'].map(k=>`<p>${esc(NAMES[k])} <button class="ghost small" data-lab-download="${k}" ${caps.testModels?.[k]?.ready||download?'disabled':''}>${caps.testModels?.[k]?.ready?'Installiert':'Testmodell laden'}</button> <button class="ghost small" data-lab-import="${k}" ${caps.testModels?.[k]?.ready||download?'disabled':''}>ZIP vom Gerät wählen</button></p>`).join('')}${download?'<button class="ghost" id="lab-cancel-download">Download abbrechen</button>':''}<label class="field">Erkennung für normale Übungen<select id="lab-model" ${busy?'disabled':''}>${Object.entries(NAMES).filter(([k])=>k==='sensevoice'||caps.testModels?.[k]?.ready).map(([k,n])=>`<option value="${k}" ${caps.recognizer===k?'selected':''}>${esc(n)}</option>`).join('')}</select></label></details></section>
 <section class="card daily-card"><span class="pill">Testrunde ${index+1} / ${data.prompts.length}</span><h2 lang="ja">${esc(p.jp||'Still bleiben')}</h2><p class="romaji">${esc(p.romaji)}</p><p>${esc(p.de)}</p>${!p.negative?'<button class="ghost" id="lab-audio">▷ Vorlage anhören</button>':''}<button class="record-button wide" id="lab-record" ${busy&&state.recording!=='recording'?'disabled':''}>${state.recording==='recording'?'■ Aufnahme beenden':busy?'Vergleich läuft …':'◉ Für Vergleich aufnehmen'}</button>${own&&!busy?'<button class="ghost" id="lab-replay">▷ Meine Aufnahme</button>':''}<p id="lab-status" role="status">${esc(status)}</p>
 ${last?`<div class="practice-list">${(last.results??[]).map(r=>`<div class="info"><strong>${esc(NAMES[r.model]??r.model)}</strong><p>${esc(r.error||r.text||'Kein Text erkannt')}</p><span class="sub">${r.error?'Modellprüfung fehlgeschlagen':`${r.match?'Text passt zur Vorgabe':'Text weicht ab'} · Erkennen ${r.decodeMs} ms · Laden ${r.loadMs} ms`}</span></div>`).join('')}</div><label class="field">Für einen brauchbaren Vergleich: Hast du die Vorgabe tatsächlich gesprochen?<select id="lab-quality"><option value="unconfirmed">Noch nicht bestätigt</option><option value="as_requested">${p.negative?'Ja, ich bin still geblieben':'Ja, ich habe die Vorgabe gesprochen'}</option><option value="invalid_take">Nein / versprochen / Störung</option></select></label>`:''}
 <div class="row"><button class="ghost" id="lab-prev" ${index===0||busy?'disabled':''}>← Zurück</button><button class="primary" id="lab-next" ${index===data.prompts.length-1||busy?'disabled':''}>Nächstes Beispiel →</button></div></section>
 <section class="card"><p>${rows.length} Versuche lokal gespeichert. Keine Audiodateien im Bericht. Vor einem Teilen kannst du die Datei prüfen.</p><button class="primary" id="lab-export">Bericht als Datei speichern</button><button class="ghost" id="lab-clear">Testergebnisse löschen</button></section>`;
 }
 function move(delta){stopMedia();index+=delta;last=null;status='';own=null;render();}
 function bind(){if(state.page!=='speech-lab')return;
  $$('[data-lab-download]').forEach(b=>b.onclick=()=>native('downloadTestModel',b.dataset.labDownload));
  $$('[data-lab-import]').forEach(b=>b.onclick=()=>native('importTestModel',b.dataset.labImport));
  if($('#lab-cancel-download'))$('#lab-cancel-download').onclick=()=>native('cancelTestModel');
  $('#lab-model').onchange=e=>native('selectRecognizer',e.target.value);
  if($('#lab-audio'))$('#lab-audio').onclick=()=>{if(!busy)play(prompt().jp,false,false);};
  $('#lab-record').onclick=()=>{if(state.recording==='recording'){native('stopRecording',false);return;}if(busy)return;if(!state.caps.models||!state.caps.native){toast('Installierte App und Grundsprachpaket erforderlich.');return;}stopMedia();request=nextRequest();busy=true;last=null;own=null;status='Mikrofon wird vorbereitet …';state.recording='requesting';state.speech={id:request,kind:'speech-lab'};native('recordComparison',request,!!prompt().short);render();};
  if($('#lab-replay'))$('#lab-replay').onclick=()=>native('playRecording',own,nextRequest());
  $('#lab-prev').onclick=()=>move(-1);$('#lab-next').onclick=()=>move(1);
  if($('#lab-quality')){$('#lab-quality').value=last.confirmation;$('#lab-quality').onchange=e=>{last.confirmation=e.target.value;save();};}
  $('#lab-export').onclick=()=>native('exportSpeechReport',JSON.stringify({schema:1,source:'voluntary_device_recording',device:state.caps.device??'unknown',app:state.caps.version,automatic_upload:false,audio_included:false,pronunciation_assessed:false,attempts:rows},null,2));
  $('#lab-clear').onclick=()=>{if(busy)return;if(confirm('Nur die lokalen Sprachtest-Ergebnisse löschen? Der Lernstand bleibt erhalten.')){rows=[];last=null;own=null;save();render();}};
 }
 function cancel(){request=null;busy=false;own=null;status='Aufnahme abgebrochen. Kein Fehlversuch im Kurs.';}
 function event(type,d){
  if(type==='capabilities'){state.caps={...state.caps,...d};if(state.page==='speech-lab')render();return false;}
  if(type.startsWith('testModel')){download=type==='testModelProgress'?d.kind:'';if(type==='testModelReady')state.caps={...state.caps,...d};status=type==='testModelProgress'?`Sprachpaket: ${Math.floor(d.done/d.total*100)} %`:d.message||'Testmodell bereit.';if(state.page==='speech-lab')render();return true;}
  if(type==='audioCancelled'&&busy){cancel();if(state.page==='speech-lab')render();return false;}
  if(state.page!=='speech-lab'||!request||d.request!==request)return false;
  if(type==='recording'){state.recording='recording';status=prompt().negative?'Bleibe drei Sekunden still, dann beende die Aufnahme.':'Sprich die Vorlage. Beende die Aufnahme danach.';render();}
  if(type==='speechLevel'){const el=$('#lab-status');if(el)el.textContent=`${status} (${Math.floor(d.seconds)} s)`;}
  if(type==='recognizing'){state.recording='recognizing';status='Dieselbe Aufnahme wird nacheinander mit allen installierten Modellen erkannt …';render();}
  if(type==='speechResult'||type==='speechError'){
   const p=prompt();last={id:request,prompt:p.id,expected:p.jp,at:new Date().toISOString(),confirmation:'unconfirmed',negative:!!p.negative,audioQualified:d.audioQualified===true,status:type==='speechResult'?'decoded':d.reason==='no_voice'?'no_voice':'technical_error',message:d.message??'',results:(d.results??[]).map(r=>({...r,match:!p.negative&&!r.error&&speechMatch(r.text,[p.jp,...(p.accept??[])])}))};
   rows.push(last);rows=rows.slice(-200);save();own=type==='speechResult'?request:null;request=null;busy=false;state.recording='idle';state.speech=null;status=type==='speechResult'?'Vergleich fertig. Bitte die Aufnahmequalität bestätigen.':d.message;render();
  }
  return true;
 }
 return {view,bind,event,cancel};
}

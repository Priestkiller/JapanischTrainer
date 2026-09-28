/* Presentation only: original controls and grading remain the source of truth. */
const seenGuides=new Set();
let presentation={key:'',page:0,sheet:'',sheetPage:0},layoutObserver=null,flowObserver=null,resizeTimer;
const el=(tag,cls,html='')=>{const n=document.createElement(tag);n.className=cls;n.innerHTML=html;return n;};
const button=(label,fn,cls='')=>{const b=el('button',cls);b.type='button';b.textContent=label;b.onclick=fn;return b;};
const icons={book:'▤',speak:'♩',meaning:'文',listen:'♫',build:'▦',write:'✎',apply:'◇'};
export function closeFocusSheet(){const close=document.querySelector('.focus-sheet:not([hidden]) .focus-sheet-close');if(!close)return false;close.click();return true;}
export function focusLesson({page,session,round,teacher,store,esc}) {
 const active=['lesson','exercises'].includes(page);document.body.classList.toggle('focus-mode',active);
 layoutObserver?.disconnect();flowObserver?.disconnect();clearTimeout(resizeTimer);if(!active)return;
 const root=document.querySelector('.lesson-layout');if(!root)return;
 const extra=page==='exercises',stage=extra?round.state.stage:session.phase,success=extra?round.answer.success:session.success;
 const recap=!extra&&session.mode==='recap',family=extra?round.task.family:recap?'recap':stage;
 const key=extra?`${round.task.id}:${stage}:${round.state.review_index}`:`${session.key}:${stage}:${session.mode}`;
 if(presentation.key!==key)presentation={key,page:0,sheet:'',sheetPage:0};
 const helpOpen=extra?round.answer.help_open:session.hintOpen;
 if(helpOpen)presentation.sheet='help';else if(presentation.sheet==='help')presentation.sheet='';
 root.className+=' focus-session';root.dataset.family=family;
 const oldHeader=root.querySelector('.lesson-header'),back=oldHeader.querySelector('button'),title=oldHeader.querySelector('h1').textContent;
 const total=extra?(stage==='review'?round.state.review.length:round.state.queue.length):recap?session.recap_total:6;
 const current=extra?(stage==='review'?round.state.review_index:round.state.index)+1:recap?session.recap_passed+1:['speak','meaning','listen','build','write','apply'].indexOf(stage)+1;
 const header=el('header','focus-header');
 header.innerHTML=`<div class="focus-brand"><span class="focus-logo" aria-hidden="true"><svg viewBox="0 0 48 48"><path d="M3 5q21 7 42 0l-2 7H5z" fill="#ff4c70"/><path d="M7 18h34v5H7zM12 10h5l-2 35H9zm20 0h5l2 35h-6z" fill="#eb3e5d"/><path d="M6 4q18 5 36 0" fill="none" stroke="#72c9e8" stroke-width="3"/></svg></span><div><strong>Japanisch<span>Trainer</span></strong><small>Dein Weg nach Japan <span aria-hidden="true">🌸</span></small></div><div class="focus-stats"><span><b>🔥 ${store.data.streak} Tage</b><small>Lernserie</small></span><span><b>🌸 ${store.data.xp} XP</b><small>Gesammelt</small></span></div></div>`;
 const progress=el('div','focus-progress-row');back.textContent='×';back.setAttribute('aria-label','Übung pausieren und zurück');progress.append(back);
 progress.insertAdjacentHTML('beforeend',`<progress max="${total}" value="${stage==='complete'?total:stage==='intro'?0:current}" aria-label="${extra?'Zusatzaufgabe':'Lernschritt'} ${current} von ${total}"></progress><span>${stage==='intro'?'Start':`${current} / ${total}`}</span>`);header.append(progress);
 header.insertAdjacentHTML('beforeend',`<div class="focus-lesson-title"><div><h1>${esc(title)}</h1><small class="focus-card-count">${extra?(stage==='intro'?'Erst kennenlernen':stage==='review'?'Vorherige Fehler üben':'Abwechslungsreich üben'):`Karte ${session.index+1} von ${session.lesson.cards.length}${recap?' · Abschlussrunde':' · Schritt für Schritt'}`}</small></div><span class="focus-course-badge">▤ <span>Japanisch<small>Schritt für Schritt 🌸</small></span></span></div>`);
 const workspace=el('div','focus-workspace');workspace.setAttribute('aria-label','Aktuelle Aufgabe');
 const paper=root.querySelector(extra?'#exercise-content':'.exercise-card');
 const flow=extra?el('div','focus-flow'):root.querySelector('#task');flow.classList.add('focus-flow');
 if(extra){for(const n of [...paper.childNodes])flow.append(n);paper.append(flow);}
 const caption=extra?flow.querySelector('h2'):paper.querySelector('.task-header');
 if(extra)paper.prepend(caption);
 caption.classList.add('focus-task-title');caption.insertAdjacentHTML('afterbegin',`<span class="focus-task-icon" aria-hidden="true">${icons[family]??icons.book}</span>`);
 const viewport=el('div','focus-task-viewport');flow.before(viewport);viewport.append(flow);
 const tools=el('div','focus-tools'),dock=el('footer','focus-dock');dock.setAttribute('aria-label','Aktionen zur Aufgabe');
 const controls=el('div','focus-controls');dock.append(controls);
 const query=s=>root.querySelector(s),sheets=new Map();
 const next=query(extra?'#ex-next':'#advance'),record=query(extra?'#ex-record':'#record'),check=query(extra?'#ex-check':'#check-build, #check-write');
 for(const b of [next,check].filter(Boolean)){if(b.closest('form'))b.setAttribute('form',b.closest('form').id);controls.append(b);b.hidden=b===next?!(success||['intro','complete'].includes(stage)):success;b.classList.toggle('focus-primary',!b.hidden);}
 if(check)check.textContent='Überprüfen →';
 if(record){record.classList.toggle('focus-primary',!success);record.hidden=success;record.classList.add('focus-microphone');}
 if(!controls.querySelector('button:not([hidden])')){const tip=el('p','focus-tap-tip');tip.textContent=record?'Anhören → nachsprechen → weiter':'Tippe auf die passende Antwort.';controls.append(tip);}
 const feedback=query(extra?'#exercise-content .feedback':'#task-feedback'),feedbackText=feedback?.textContent.trim()??'';
 const freshFeedback=feedbackText!==presentation.feedback;presentation.feedback=feedbackText;let revealResult=freshFeedback&&!!feedbackText;
 if(feedback){feedback.classList.add('focus-feedback');if(!feedbackText)feedback.hidden=true;}
 const storeSheet=(id,label,nodes)=>{const body=el('div','focus-sheet-content');for(const n of nodes.filter(Boolean))body.append(n);sheets.set(id,{label,body});};
 for(const d of [...flow.querySelectorAll(':scope > details')]){const id=d.classList.contains('lesson-guide')?'guide':'explain';d.open=true;storeSheet(id,id==='guide'?'Vorwissen & Lernhilfe':'Warum? · Erklärung und Beispiel',[d]);}
 const help=flow.querySelector('.exercise-hint');if(help)storeSheet('help','Hinweis & Erklärung',[help]);
 const hint=query(extra?'#ex-help':'#show-hint');if(hint){hint.textContent='💡 Hinweis';tools.append(hint);}
 const lessonGoal=query('.lesson-goal');if(lessonGoal){const body=sheets.get('guide')?.body;if(body)body.prepend(lessonGoal);else storeSheet('guide','Dein Lernziel',[lessonGoal]);}
 for(const [id,label] of [['guide','▤ Vorwissen'],['explain','ⓘ Warum?']])if(sheets.has(id))tools.append(button(label,()=>openSheet(id)));
 const extraEntry=query('#exercise-round');if(extraEntry){storeSheet('variety','Zusätzliche Übungen',[el('p','','Du kannst mit weiteren Aufgaben zu dieser Lektion üben. Dein Pflichtfortschritt bleibt erhalten.'),extraEntry]);tools.append(button('◇ Mehr üben',()=>openSheet('variety')));}
 const reset=query('#ex-reset');if(reset){reset.textContent='↺ Neu';reset.setAttribute('aria-label','Bausteine zurücksetzen');tools.append(reset);}
 const pause=query('#ex-pause');if(pause){pause.textContent='Pause';tools.append(pause);}
 if(extra&&stage==='intro'){
  const nodes=[...flow.children].filter(n=>!n.classList.contains('task-footer'));
  storeSheet('intro','Vorwissen und neue Ausdrücke',nodes);
  flow.append(el('p','','Lerne die benötigten Ausdrücke mit Bedeutung, Aussprache und Beispielen kennen.'));
  const intro=button('▤ Einführung öffnen',()=>openSheet('intro'));intro.id='focus-intro';flow.append(intro);
 }
 let recordingPanel=null,fixedAudio=null;
 const speaking=flow.querySelector('.speaking-card');
 if(speaking){
  const model=el('div','focus-model'),words=el('div','focus-word'),pron=speaking.querySelector('.pronunciation');
  for(const n of [...speaking.children])if(n.matches('.jp,.romaji,.translation')||(extra&&n.tagName==='P'&&!n.className))words.append(n);
  model.append(words);if(pron){pron.textContent=pron.textContent.replace(/^Aussprachehilfe(?: · Näherung)?[: ·]*/,'');pron.insertAdjacentHTML('afterbegin','<strong>Aussprachehilfe</strong>');model.append(pron);}speaking.prepend(model);speaking.querySelector('#speak-instruction')?.remove();
 }
 if(record){
  let panel=record.closest('.speech-panel');if(!panel){panel=el('div','speech-panel');record.before(panel);panel.append(record);}
  recordingPanel=panel;panel.classList.add('focus-fixed-record');paper.classList.add('focus-speaking-paper');fixedAudio=flow.querySelector('.audio-actions');if(fixedAudio){fixedAudio.classList.add('focus-fixed-audio');paper.append(fixedAudio);}paper.append(panel);const own=query('#ex-own');if(own)panel.append(own);
  panel.prepend(el('div','focus-record-label','<span>● Jetzt aufnehmen</span><small>Deine Stimme bleibt auf dem Gerät</small>'));
  const caption=panel.querySelector('.speech-caption')??[...flow.querySelectorAll(':scope > p.sub')].find(p=>p.textContent.startsWith('Lokaler Textvergleich'));if(caption){storeSheet('microphone','Sprechen und Erkennen',[family==='echo'?flow.querySelector('#ex-prompt'):null,caption]);tools.append(button('ⓘ Aufnahme',()=>openSheet('microphone')));}
 }
 const companions=el('div','focus-companions');companions.setAttribute('aria-label',`${teacher.name} begleitet dich`);
 const encouragement=success?'Gut gemacht! Weiter zum nächsten Schritt.':family==='speak'||family==='echo'?'Sprich in Ruhe nach. Die Vorlage bleibt sichtbar.':family==='build'||family==='translate'?'Baue den Satz in Ruhe. Du kannst jederzeit nachschauen.':'Schritt für Schritt. Du kannst dir Zeit lassen.';
 companions.innerHTML=`<img class="focus-teacher" src="assets/teachers/${teacher.id}/full.png" alt="${esc(teacher.name)}"><p class="focus-coach-copy"><strong>🌸 ${esc(teacher.name)}</strong><span>${esc(encouragement)}</span></p>${store.data.show_kiko?'<div class="focus-kiko"><img src="assets/mascot/kiko_study.png" alt="Kiko"><p><strong>Kiko 🌱</strong><span>Kleine Schritte,<br>große Träume! 🌸</span></p></div>':''}`;
 const pager=el('nav','focus-page-nav');pager.setAttribute('aria-label','Seiten der aktuellen Aufgabe');
 const prev=button('← Zurück',()=>setTaskPage(presentation.page-1)),count=el('span',''),forward=button('Weiterlesen →',()=>setTaskPage(presentation.page+1));pager.append(prev,count,forward);pager.hidden=true;
 workspace.append(paper,tools,pager,companions);root.replaceChildren(header,workspace,dock);
 const sheet=el('section','focus-sheet');sheet.setAttribute('role','dialog');sheet.setAttribute('aria-modal','true');sheet.setAttribute('aria-labelledby','focus-sheet-title');sheet.hidden=true;root.append(sheet);
 const storage=el('div','focus-sheet-storage');storage.hidden=true;root.append(storage);
 let restoreFocus=null,taskPages=1,stride=0;
 function setTaskPage(p){presentation.page=Math.max(0,Math.min(taskPages-1,p));viewport.scrollLeft=presentation.page*stride;count.textContent=`Ansicht ${presentation.page+1} / ${taskPages}`;prev.disabled=presentation.page===0;forward.disabled=presentation.page===taskPages-1;}
 function layout(){
  if(!root.isConnected)return;
  flow.classList.remove('focus-pagination');flow.style.height='';flow.style.columnWidth='';flow.style.columnGap='';flow.style.columnFill='';viewport.style.height='';viewport.scrollLeft=0;pager.hidden=true;
  const reserve=document.body.classList.contains('keyboard')?0:innerHeight>700?(record?140:190):innerHeight>550?(record?55:120):0;
  const available=Math.max(110,workspace.clientHeight-tools.offsetHeight-caption.offsetHeight-48-reserve-(recordingPanel?.offsetHeight??0)-(fixedAudio?.offsetHeight??0));
  if(flow.scrollHeight>available+2){
   flow.classList.add('focus-pagination');const height=Math.max(record?88:100,available-50),width=viewport.clientWidth;
   flow.style.height=`${height}px`;flow.style.columnWidth=`${width}px`;flow.style.columnGap='24px';flow.style.columnFill='auto';viewport.style.height=`${height}px`;stride=width+24;
   taskPages=Math.max(1,Math.ceil((flow.scrollWidth+24)/stride));pager.hidden=taskPages===1;
  }else taskPages=1;
  setTaskPage(presentation.page);
  const target=document.activeElement?.matches('input,textarea')?document.activeElement:revealResult?(flow.querySelector('#confirm-short-speech')?.closest('.info')??feedback):null;
  if(target&&taskPages>1){const r=target.getBoundingClientRect(),v=viewport.getBoundingClientRect();setTaskPage(Math.floor((r.left-v.left+viewport.scrollLeft+1)/stride));}revealResult=false;
  root.classList.toggle('focus-short',innerHeight<550);companions.classList.toggle('focus-companions-compact',companions.clientHeight<240);companions.classList.toggle('focus-companions-minimal',companions.clientHeight<155);
 }
 function closeSheet(){
  if(presentation.sheet==='help'&&helpOpen){document.getElementById(extra?'ex-help':'show-hint')?.click();return;}
  presentation.sheet='';sheet.hidden=true;header.inert=false;workspace.inert=false;dock.inert=false;restoreFocus?.focus({preventScroll:true});
 }
 function openSheet(id){
  const content=sheets.get(id);if(!content)return;
  if(presentation.sheet!==id)presentation.sheetPage=0;presentation.sheet=id;restoreFocus=document.activeElement;
  for(const entry of sheets.values())storage.append(entry.body);sheet.replaceChildren();
  const top=el('div','focus-sheet-top',`<h2 id="focus-sheet-title">${esc(content.label)}</h2>`);top.append(button('×',closeSheet,'focus-sheet-close'));top.lastChild.setAttribute('aria-label','Zurück zur Aufgabe');
  const reading=el('div','focus-sheet-reading');reading.append(content.body);
  const bottom=el('div','focus-sheet-actions');const earlier=button('← Zurück',()=>move(-1)),pageNumber=el('span',''),later=button('Weiterlesen →',()=>move(1));bottom.append(earlier,pageNumber,later);
  sheet.append(top,reading,bottom);sheet.hidden=false;header.inert=true;workspace.inert=true;dock.inert=true;
  let pages=1,step=0;
  function paginate(){if(sheet.hidden)return;const w=reading.clientWidth,h=reading.clientHeight;content.body.style.height=`${h}px`;content.body.style.columnWidth=`${w}px`;content.body.style.columnGap='28px';content.body.style.columnFill='auto';step=w+28;pages=Math.max(1,Math.ceil((content.body.scrollWidth+28)/step));move(0);}
  function move(delta){presentation.sheetPage=Math.max(0,Math.min(pages-1,presentation.sheetPage+delta));reading.scrollLeft=presentation.sheetPage*step;pageNumber.textContent=`${presentation.sheetPage+1} / ${pages}`;earlier.disabled=presentation.sheetPage===0;later.disabled=presentation.sheetPage===pages-1;}
  sheet.onkeydown=e=>{if(e.key==='Escape'){e.preventDefault();closeSheet();}if(e.key==='Tab'){const visible=[...sheet.querySelectorAll('button,summary,input')].filter(b=>!b.disabled&&b.getBoundingClientRect().width&&b.getBoundingClientRect().left>=sheet.getBoundingClientRect().left&&b.getBoundingClientRect().right<=sheet.getBoundingClientRect().right);const first=visible[0],last=visible.at(-1);e.preventDefault();if(visible.length){const at=visible.indexOf(document.activeElement),next=(at+(e.shiftKey?-1:1)+visible.length)%visible.length;visible[next].focus({preventScroll:true});}}};
  requestAnimationFrame(()=>{paginate();top.lastChild.focus({preventScroll:true});});sheet._paginate=paginate;
 }
 for(const entry of sheets.values())storage.append(entry.body);
 const relayout=()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{layout();sheet._paginate?.();},40);};
 layoutObserver=new ResizeObserver(relayout);layoutObserver.observe(workspace);flowObserver=new MutationObserver(relayout);flowObserver.observe(flow,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['hidden']});if(recordingPanel)flowObserver.observe(recordingPanel,{childList:true,subtree:true,characterData:true,attributes:true,attributeFilter:['hidden']});
 if(!extra&&session.mode==='learn'&&stage==='speak'&&session.index===0&&sheets.has('guide')&&!seenGuides.has(session.lesson.key)){seenGuides.add(session.lesson.key);presentation.sheet='guide';}if(extra&&stage==='intro'&&!seenGuides.has('extra:'+round.lesson.key)){seenGuides.add('extra:'+round.lesson.key);presentation.sheet='intro';}if(presentation.sheet)openSheet(presentation.sheet);requestAnimationFrame(layout);
 viewport.addEventListener('focusin',e=>{if(taskPages>1){const r=e.target.getBoundingClientRect(),v=viewport.getBoundingClientRect();setTaskPage(Math.floor((r.left-v.left+viewport.scrollLeft+1)/stride));}});
}

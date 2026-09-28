/* Presentation only. Existing task buttons, events, session and grading stay in use. */
let resizeTimer;
function revealInput(){
 clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{
  const input=document.activeElement;
  if(document.body.classList.contains('focus-mode')&&input?.matches('input,textarea'))input.scrollIntoView({block:'center',behavior:'instant'});
 },180);
}
window.addEventListener('resize',revealInput);
window.visualViewport?.addEventListener('resize',revealInput);
document.addEventListener('focusin',revealInput);
export function focusLesson({page,session,round,teacher,store,esc}) {
 const active=['lesson','exercises'].includes(page);
 document.body.classList.toggle('focus-mode',active);
 if(!active)return;
 const root=document.querySelector('.lesson-layout');if(!root)return;
 const isExtra=page==='exercises',success=isExtra?round.answer.success:session.success;
 const stage=isExtra?round.state.stage:session.phase;
 const recap=!isExtra&&session.mode==='recap';
 const total=isExtra?(stage==='review'?round.state.review.length:round.state.queue.length):recap?session.recap_total:6;
 const current=isExtra?(stage==='review'?round.state.review_index:round.state.index)+1:
   recap?session.recap_passed+1:Math.max(1,['speak','meaning','listen','build','write','apply'].indexOf(session.phase)+1);
 root.querySelector('.focus-dock')?.remove();
 if(!root.classList.contains('focus-session')) {
  root.classList.add('focus-session');
  const header=root.querySelector('.lesson-header'),back=header.querySelector('button');
  const title=header.querySelector('h1').textContent;
  header.className='focus-header';header.replaceChildren();
  const brand=document.createElement('div');brand.className='focus-brand';
  brand.innerHTML=`<span><b>日本</b> Japanisch<span>Trainer</span></span><small>${store.data.streak} Tage · ${store.data.xp} XP</small>`;
  header.append(brand);
  const bar=document.createElement('div');bar.className='focus-progress-row';
  back.textContent='×';back.setAttribute('aria-label','Übung pausieren und zurück');
  bar.append(back);bar.insertAdjacentHTML('beforeend',`<progress max="${total}" value="${stage==='complete'?total:stage==='intro'?0:current}" aria-label="${isExtra?'Zusatzaufgabe':'Lernschritt'} ${current} von ${total}"></progress><span>${stage==='intro'?'Start':`${current} / ${total}`}</span>`);header.append(bar);
  const context=document.createElement('div');context.className='focus-lesson-title';
  context.innerHTML=`<span>${esc(title)}</span><span class="focus-partner"><img src="assets/teachers/${teacher.id}/avatar.png" alt=""><span>${esc(teacher.name)}<small>begleitet dich</small></span></span>`;header.append(context);
  const workspace=document.createElement('div');workspace.className='focus-workspace';workspace.setAttribute('aria-label','Aktuelle Aufgabe');
  for(const node of [...root.children])if(node!==header)workspace.append(node);
  root.append(workspace);
  workspace.querySelector('.coach')?.remove();
  workspace.querySelector('.phase-track')?.setAttribute('hidden','');
  const guide=document.createElement('div');guide.className='focus-companions';
  guide.innerHTML=`<div class="focus-coach-copy">${store.data.show_kiko?'<img src="assets/mascot/kiko_study.png" alt="Kiko">':''}<p><strong>${esc(teacher.name)}</strong><span>In deinem Tempo. Du kannst jederzeit nachschauen.</span></p></div><img class="focus-teacher" src="assets/teachers/${teacher.id}/full.png" alt="${esc(teacher.name)}">`;
  workspace.append(guide);
 }
 const dock=document.createElement('div');dock.className='focus-dock';dock.setAttribute('aria-label','Aktionen zur Aufgabe');
 const query=s=>root.querySelector(s);
 const feedback=query(isExtra?'#exercise-content > .feedback':'#task-feedback');
 if(feedback?.textContent.trim()){feedback.classList.add('focus-feedback');dock.append(feedback);}
 const controls=document.createElement('div');controls.className='focus-controls';
 const next=query(isExtra?'#ex-next':'#advance');
 const record=query(isExtra?'#ex-record':'#record');
 const check=query(isExtra?'#ex-check':'#check-build, #check-write');
 const primary=success||['intro','complete'].includes(stage)?next:record??check;
 for(const b of [next,record,check].filter(Boolean)) {
  if(b.closest('form'))b.setAttribute('form',b.closest('form').id);
  b.classList.toggle('focus-primary',b===primary);b.hidden=b!==primary;controls.append(b);
 }
 if(!primary){const tip=document.createElement('p');tip.className='focus-tap-tip';tip.textContent='Tippe auf die passende Antwort.';controls.append(tip);}
 dock.append(controls);
 const secondary=document.createElement('div');secondary.className='focus-secondary';
 for(const selector of isExtra?['#ex-help','#ex-own','#ex-pause']:['#show-hint','#lesson-own','#lesson-cancel']) {
  const b=query(selector);if(b)secondary.append(b);
 }
 if(!isExtra&&!query('#show-hint')) {
  const details=query('#task > details:last-child');
  if(details){if(!details.id)details.id='focus-explanation';const b=document.createElement('button');b.className='focus-explain-button';b.textContent=details.open?'Erklärung schließen':'Erklären / Warum?';b.onclick=()=>{details.open=!details.open;b.textContent=details.open?'Erklärung schließen':'Erklären / Warum?';if(details.open)details.scrollIntoView({block:'start',behavior:'smooth'});};secondary.append(b);}
 }
 if(secondary.children.length)dock.append(secondary);
 root.append(dock);
 // Hints remain inside the scrollable task; no modal or duplicate answer nodes.
 const help=query(isExtra?'.exercise-hint':'#task > .exercise-hint');
 if(help)requestAnimationFrame(()=>help.scrollIntoView({block:'nearest',behavior:'smooth'}));
}

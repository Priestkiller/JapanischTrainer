/* GPL-3.0-or-later. Reuse the selected teacher and local expression assets. */
export function coachState({recording='idle',audio=null,mood='idle'}={}) {
  if(recording==='recording')return ['listening','Ich höre dir zu. Sprich in deinem Tempo.'];
  if(recording==='requesting')return ['preparing','Das Mikrofon wird vorbereitet.'];
  if(recording==='recognizing')return ['thinking','Deine Aufnahme wird auf dem Gerät erkannt.'];
  if(audio?.started)return ['speaking','Hör mir zu. Danach bist du dran.'];
  if(audio)return ['preparing','Meine Stimme wird vorbereitet.'];
  if(mood==='praise')return ['happy','Geschafft! Wir machen Schritt für Schritt weiter.'];
  return ['ready','Sprich in Ruhe nach. Du kannst es erneut versuchen.'];
}
export function coachMarkup(teacher,esc) {
  return `<div class="voice-companion" aria-label="${esc(teacher.name)} begleitet dich"><canvas id="teacher-canvas" data-teacher="${esc(teacher.id)}" width="512" height="768" role="img" aria-label="${esc(teacher.name)}, dein Sprachbegleiter"></canvas><p class="voice-bubble"><strong>${esc(teacher.name)}</strong><span data-coach-message></span><small>Dein Sprachbegleiter</small></p></div>`;
}
export function syncCoach(state) {
  const [mode,text]=coachState({...state,mood:document.body.dataset.teacherMood});
  if(document.body.dataset.coachState!==mode)document.body.dataset.coachState=mode;
  document.querySelectorAll('[data-coach-message]').forEach(n=>{if(n.textContent!==text)n.textContent=text;});
}
const images=new Map();
const load=src=>{if(!images.has(src))images.set(src,new Promise(resolve=>{const img=new Image();img.onload=()=>resolve(img);img.onerror=()=>resolve(null);img.src=src;}));return images.get(src);};
export function animateTeacher({teacher,blinkIndex,expressions,enabled}) {
  const canvas=document.querySelector('#teacher-canvas');if(!canvas)return ()=>{};
  const ctx=canvas.getContext('2d'),media=matchMedia('(prefers-reduced-motion: reduce)');
  let alive=true,timer=0,visible=true,step=0,last='',assets;
  const stop=()=>{alive=false;clearTimeout(timer);observer.disconnect();changes.disconnect();media.removeEventListener('change',draw);document.removeEventListener('visibilitychange',draw);};
  const observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;draw();});observer.observe(canvas);
  const changes=new MutationObserver(()=>{last='';draw();});changes.observe(document.body,{attributes:true,attributeFilter:['data-coach-state','class']});changes.observe(document.querySelector('#app'),{attributes:true,subtree:true,attributeFilter:['inert']});
  const patch=(image,box)=>{if(image&&box)ctx.drawImage(image,box[0]/2,box[1]/2,(box[2]-box[0])/2,(box[3]-box[1])/2);};
  function draw(){
    clearTimeout(timer);if(!alive||!assets||!canvas.isConnected)return;
    const moving=enabled()&&!media.matches&&!document.hidden&&visible&&!canvas.closest('[inert]');
    const mode=canvas.classList.contains('voice-actor')||canvas.closest('.voice-companion')?document.body.dataset.coachState:'ready';
    const blink=moving&&step%27<5?step%27:-1;
    const mouth=mode==='happy'?'praise':mode==='speaking'&&moving&&step%2?'encourage':'idle';
    const key=blink+':'+mouth;
    if(key!==last){ctx.clearRect(0,0,512,768);ctx.drawImage(assets.base,0,0,512,768);patch(assets[mouth],assets.expression[mouth]?.bbox);if(blink>=0)patch(assets.frames[blink],assets.blink?.bbox);last=key;canvas.dataset.frame=key;}
    canvas.style.animationPlayState=moving?'running':'paused';canvas.dataset.mode=mode;canvas.dataset.playing=String(moving);if(moving){step++;timer=setTimeout(draw,blink>=0?65:180);}
  }
  media.addEventListener('change',draw);document.addEventListener('visibilitychange',draw);
  (async()=>{
    const expression=expressions.expressions[teacher.id],blink=blinkIndex[teacher.id];
    const base=await load(`assets/teachers/${teacher.id}/full.png`);
    const [idle,praise,encourage,...frames]=await Promise.all(['idle','praise','encourage'].map(k=>load(`assets/animation/${teacher.id}/${expression[k].file}`)).concat((blink?.frames??[]).map(f=>load(`assets/animation/${teacher.id}/${f}`))));
    if(!alive)return;if(!base){canvas.dataset.error='true';return;}assets={base,idle,praise,encourage,frames,expression,blink};draw();
  })();return stop;
}

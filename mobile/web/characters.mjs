/* GPL-3.0-or-later. Full-body poses follow actual local audio/recording events. */
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
const load=src=>{if(!images.has(src)){images.set(src,new Promise(resolve=>{const img=new Image();img.onload=()=>resolve(img);img.onerror=()=>resolve(null);img.src=src;}));if(images.size>2)images.delete(images.keys().next().value);}return images.get(src);};
export function teacherPose(mode,step=0,moving=true) {
  const row=mode==='happy'?3:mode==='listening'||mode==='thinking'?2:mode==='speaking'?1:0;
  const sequence=row===0?[0,0,0,1,2,3,2,1]:[0,1,2,3,2,1];
  return row*4+(moving?sequence[step%sequence.length]:0);
}
export function animateTeacher({teacher,enabled}) {
  const canvas=document.querySelector('#teacher-canvas');if(!canvas)return ()=>{};
  const ctx=canvas.getContext('2d'),media=matchMedia('(prefers-reduced-motion: reduce)');
  let alive=true,timer=0,visible=true,step=0,last=-1,previousMode='',atlas,geometry;
  const stop=()=>{alive=false;clearTimeout(timer);observer.disconnect();changes.disconnect();media.removeEventListener('change',draw);document.removeEventListener('visibilitychange',draw);};
  const observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;draw();});observer.observe(canvas);
  const changes=new MutationObserver(draw);changes.observe(document.body,{attributes:true,attributeFilter:['data-coach-state','class']});changes.observe(document.querySelector('#app'),{attributes:true,subtree:true,attributeFilter:['inert']});
  function draw(){
    clearTimeout(timer);if(!alive||!atlas||!canvas.isConnected)return;
    const moving=enabled()&&!media.matches&&!document.hidden&&visible&&!canvas.closest('[inert]');
    const mode=canvas.classList.contains('voice-actor')||canvas.closest('.voice-companion')?document.body.dataset.coachState:'ready';
    if(mode!==previousMode){step=0;previousMode=mode;}
    const frame=teacherPose(mode,step,moving),[x,y,w,h,center]=geometry.frames[frame],s=geometry.scale;
    if(frame!==last){ctx.clearRect(0,0,canvas.width,canvas.height);ctx.drawImage(atlas,x,y,w,h,canvas.width/2+(x-center)*s,canvas.height-20-h*s,w*s,h*s);last=frame;canvas.dataset.frame=String(frame);}
    canvas.style.animationPlayState=moving?'running':'paused';canvas.dataset.mode=mode;canvas.dataset.playing=String(moving);canvas.dataset.fullBody='true';if(moving){step++;timer=setTimeout(draw,mode==='ready'?420:200);}
  }
  media.addEventListener('change',draw);document.addEventListener('visibilitychange',draw);
  (async()=>{
    try{
      const metadata=await fetch('artwork/teacher-bodies-1114.json').then(r=>{if(!r.ok)throw Error('Teacher geometry missing');return r.json();});
      geometry=metadata[teacher.id];const image=await load(`artwork/${geometry.file}`);
      if(!alive)return;if(!image||geometry.frames.length!==16){canvas.dataset.error='true';return;}atlas=image;draw();
    }catch{if(alive)canvas.dataset.error='true';}
  })();return stop;
}

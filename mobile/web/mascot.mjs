/* GPL-3.0-or-later. Local hand-drawn frame sequences, no remote media or audio. */
let atlasPromise;
const atlas=()=>atlasPromise??=new Promise(resolve=>{const img=new Image();img.onload=()=>resolve(img);img.onerror=()=>resolve(null);img.src='artwork/kiko-motion.png';});
export function mascotMarkup(mood='idle') {
  return `<canvas class="kiko-actor" data-mood="${mood==='cheer'?'cheer':'idle'}" width="320" height="320" role="img" aria-label="${mood==='cheer'?'Kiko freut sich mit dir':'Kiko, dein kleiner Lernbegleiter'}"></canvas>`;
}
export function animateMascots(enabled) {
  const canvases=[...document.querySelectorAll('.kiko-actor')];let alive=true;const cleanup=[];
  const media=matchMedia('(prefers-reduced-motion: reduce)');
  const stop=()=>{alive=false;cleanup.splice(0).forEach(fn=>fn());};
  atlas().then(img=>{
    if(!alive)return;
    for(const canvas of canvases){
      if(!img){canvas.dataset.error='true';canvas.setAttribute('aria-label','Kiko-Grafik konnte nicht geladen werden');continue;}
      const ctx=canvas.getContext('2d'),cheer=canvas.dataset.mood==='cheer';let step=0,started=performance.now(),greetingUntil=0,timer=0;
      const box=canvas.getBoundingClientRect();let visible=box.bottom>0&&box.top<innerHeight;
      const draw=()=>{
        clearTimeout(timer);if(!alive||!canvas.isConnected)return;
        const moving=enabled()&&!media.matches&&!document.hidden&&visible;
        const greeting=performance.now()<greetingUntil,celebrating=cheer||greeting;
        const playing=moving&&(!cheer||performance.now()-started<2650);
        const index=(celebrating?8:0)+(playing?step%8:0),x=index%4,y=Math.floor(index/4);
        const sx=Math.round(x*img.width/4),sy=Math.round(y*img.height/4),sw=Math.round((x+1)*img.width/4)-sx,sh=Math.round((y+1)*img.height/4)-sy;
        ctx.clearRect(0,0,320,320);ctx.drawImage(img,sx,sy,sw,sh,0,0,320,320);canvas.dataset.frame=String(index);canvas.dataset.playing=String(playing);
        if(playing){const delay=celebrating?140:[1000,550,500,110,130,500,550,850][step%8];step++;timer=setTimeout(draw,delay);}
      };
      const greet=()=>{if(!alive||cheer||!enabled()||media.matches)return;step=0;greetingUntil=performance.now()+2300;draw();};
      const button=canvas.closest('.kiko-greeting');button?.addEventListener('click',greet);
      const observer=new IntersectionObserver(entries=>{if(!alive)return;visible=entries[0].isIntersecting;draw();});observer.observe(canvas);
      media.addEventListener('change',draw);
      cleanup.push(()=>{clearTimeout(timer);observer.disconnect();button?.removeEventListener('click',greet);media.removeEventListener('change',draw);});
      draw();
    }
  });
  return stop;
}

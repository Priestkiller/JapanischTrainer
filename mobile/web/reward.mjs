/* GPL-3.0-or-later. A finite, skippable local celebration; never grants XP. */
import {mascotMarkup} from './mascot.mjs';
export const CELEBRATION_MS=3200;
export function rewardMarkup(showKiko=true) {
  return `<div class="reward-stage" data-celebration="waiting"><div class="reward-halo" aria-hidden="true"></div><canvas class="reward-confetti" width="580" height="360" aria-hidden="true"></canvas>${showKiko?mascotMarkup('cheer'):'<span class="reward-check" aria-hidden="true">✓</span>'}<span class="reward-star star-one" aria-hidden="true">✦</span><span class="reward-star star-two" aria-hidden="true">✦</span><span class="reward-star star-three" aria-hidden="true">✦</span></div>`;
}
export function animateReward(enabled) {
  const stage=document.querySelector('.reward-stage');if(!stage)return ()=>{};
  const canvas=stage.querySelector('.reward-confetti'),ctx=canvas.getContext('2d'),media=matchMedia('(prefers-reduced-motion: reduce)');
  let alive=true,raf=0,visible=true,started=performance.now();
  const particles=Array.from({length:36},(_,i)=>({x:290,y:250,vx:Math.cos(i*2.399)*(.8+i%6)*28,vy:-100-i%7*36,color:['#ffc95c','#78edc7','#ff7bad','#77d8ff'][i%4],spin:i*.9,size:4+i%3}));
  const draw=now=>{
    cancelAnimationFrame(raf);if(!alive||!stage.isConnected)return;
    const moving=enabled()&&!media.matches&&!document.hidden&&visible;
    const elapsed=now-started,playing=moving&&elapsed<CELEBRATION_MS;
    stage.dataset.celebration=playing?'playing':'finished';ctx.clearRect(0,0,580,360);
    if(playing){const t=elapsed/1000;for(const p of particles){const x=p.x+p.vx*t,y=p.y+p.vy*t+85*t*t;ctx.save();ctx.globalAlpha=Math.max(0,1-t/3.2);ctx.translate(x,y);ctx.rotate(p.spin+t*3);ctx.fillStyle=p.color;ctx.fillRect(-p.size,-p.size/2,p.size*2,p.size);ctx.restore();}raf=requestAnimationFrame(draw);}
  };
  const update=()=>draw(performance.now()),observer=new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;update();});observer.observe(stage);
  const changes=new MutationObserver(update);changes.observe(document.body,{attributes:true,attributeFilter:['class']});
  media.addEventListener('change',update);document.addEventListener('visibilitychange',update);update();
  return ()=>{alive=false;cancelAnimationFrame(raf);observer.disconnect();changes.disconnect();media.removeEventListener('change',update);document.removeEventListener('visibilitychange',update);};
}

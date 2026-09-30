/* GPL-3.0-or-later. Same stable data contract as adaptive.py. No course unlocks or XP. */
export const SKILLS=['read','listen','write','speak','use'];
export const SKILL_LABELS={read:'Lesen',listen:'Hören',write:'Schreiben',speak:'Sprechen',use:'Anwenden',intro:'Neu kennenlernen'};
export const PHASE_SKILL={meaning:'read',listen:'listen',write:'write',build:'write',apply:'use',speak:'speak'};
const object=x=>x!==null&&typeof x==='object'&&!Array.isArray(x);
export function cleanAdaptive(value){
 const out={skills:{},introduced:[],daily:{},milestones:{}};if(!object(value))return out;
 for(const [key,skills] of Object.entries(object(value.skills)?value.skills:{}).slice(0,2000)){
  if(key.length>150||['__proto__','constructor','prototype'].includes(key)||!object(skills))continue;out.skills[key]={};
  for(const skill of SKILLS){const raw=skills[skill];if(!object(raw))continue;
   out.skills[key][skill]=Object.fromEntries(['attempts','right','streak','due','last','assisted'].map(k=>[k,typeof raw[k]==='number'&&Number.isFinite(raw[k])?Math.max(0,Math.min(1e12,raw[k])):0]));}
 }
 out.introduced=[...new Set((Array.isArray(value.introduced)?value.introduced:[]).filter(x=>typeof x==='string'&&x.length<150))].slice(0,2000);
 const raw=value.daily;
 if(object(raw)&&typeof raw.date==='string'){
  const tasks=(Array.isArray(raw.tasks)?raw.tasks:[]).slice(0,10).filter(x=>object(x)&&['id','card','skill'].every(k=>typeof x[k]==='string')&&[...SKILLS,'intro'].includes(x.skill)&&x.card.length<150).map(({id,card,skill})=>({id,card,skill}));
  out.daily={date:raw.date.slice(0,10),tasks,done:[...new Set((Array.isArray(raw.done)?raw.done:[]).filter(id=>tasks.some(t=>t.id===id)))]};
 }
 if(object(value.milestones))out.milestones=Object.fromEntries(Object.entries(value.milestones).slice(0,100).filter(([k,v])=>object(v)));
 return out;
}
export function recordAttempt(data,key,skill,ok,assisted=false,now=Date.now()/1000){
 if(!SKILLS.includes(skill))return;
 const a=data.adaptive??=cleanAdaptive(),m=(a.skills[key]??={})[skill]??={attempts:0,right:0,streak:0,due:0,last:0,assisted:0};
 m.attempts++;m.last=now;if(assisted)m.assisted++;
 if(ok&&!assisted){m.right++;m.streak=Math.min(6,m.streak+1);m.due=now+[1,2,4,7,14,30][m.streak-1]*86400;}
 else {m.streak=0;m.due=now+(ok?86400:0);}
}
const localDay=()=>{const d=new Date();return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;};
export function dailyPlan(data,cards,available,upcoming,today=localDay(),now=Date.now()/1000){
 const a=data.adaptive??=cleanAdaptive(),byKey=new Map(cards.map(c=>[c.key,c])),old=a.daily;
 if(old?.date===today&&old.tasks?.length&&old.tasks.every(t=>byKey.has(t.card)))return old;
 const known=[...new Set([...available.filter(c=>data.completed?.includes(c.lesson_key)||(data.study_cards?.[c.key]?.attempts??0)>0||Object.hasOwn(data.review??{},c.key)).map(c=>c.key),...a.introduced.filter(k=>byKey.has(k))])],candidates=[];
 for(const key of known)SKILLS.forEach((skill,rank)=>{const m=a.skills[key]?.[skill]??{};if((m.due??0)<=now)candidates.push({priority:-Math.min(20,(m.attempts??0)-(m.right??0)),last:m.last??0,rank,key,skill});});
 candidates.sort((a,b)=>a.priority-b.priority||a.last-b.last||a.rank-b.rank||(a.key<b.key?-1:a.key>b.key?1:0));
 const tasks=[],chosen=new Set();
 for(const {key,skill} of candidates){if(chosen.has(key)||tasks.length>=5)continue;chosen.add(key);tasks.push({id:`${today}:${key}:${skill}`,card:key,skill});}
 for(const card of upcoming.slice(0,2))if(!a.introduced.includes(card.key)&&tasks.length<7)tasks.push({id:`${today}:${card.key}:intro`,card:card.key,skill:'intro'});
 return a.daily={date:today,tasks,done:[]};
}
export function finishDaily(data,task,ok,assisted=false,now=Date.now()/1000){
 const a=data.adaptive??=cleanAdaptive(),p=a.daily;
 if(!p.tasks?.some(t=>t.id===task.id&&t.card===task.card&&t.skill===task.skill)||p.done.includes(task.id))return false;
 if(task.skill==='intro'){if(ok&&!a.introduced.includes(task.card))a.introduced.push(task.card);}
 else recordAttempt(data,task.card,task.skill,ok,assisted,now);
 if(ok)p.done.push(task.id);return !!ok;
}

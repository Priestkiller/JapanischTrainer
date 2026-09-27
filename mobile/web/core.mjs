/* GPL-3.0-or-later. Mobile port of learning.py and study.py; stable desktop IDs. */
export const PHASES=['understand','meaning','listen','build','write','apply'];
export const LABELS={understand:'Verstehen',meaning:'Bedeutung',listen:'Hören',build:'Bausteine',write:'Schreiben',apply:'Anwenden'};
export const compact=s=>String(s??'').normalize('NFKC').toLowerCase().replace(/[\s\-・、。！？!?.,:;~〜～/…「」“”"'()]/gu,'');
export function romajiForms(text) {
  const forms=new Set([compact(text)]);
  for(const [long,replacements] of Object.entries({'ā':['aa'],'ī':['ii'],'ū':['uu'],'ē':['ee'],'ō':['ou','oo']}))
    for(const old of [...forms]) for(const replacement of replacements) forms.add(old.replaceAll(long,replacement));
  return forms;
}
export const matchesRomaji=(given,expected)=>romajiForms(expected).has(compact(given));
export function shuffle(values,seed='') {
  const result=[...values]; let h=2166136261;
  for(const c of seed)h=Math.imul(h^c.charCodeAt(0),16777619)>>>0;
  for(let i=result.length-1;i>0;i--) { h=(Math.imul(h,1664525)+1013904223)>>>0; const j=h%(i+1); [result[i],result[j]]=[result[j],result[i]]; }
  return result;
}
const record=v=>v!==null&&typeof v==='object'&&!Array.isArray(v);
const number=(v,low,high,fallback)=>Number.isFinite(Number(v))?Math.max(low,Math.min(high,Number(v))):fallback;
export function cleanProfile(input={},strict=false) {
  if(!record(input)||(strict&&(!Array.isArray(input.completed)||!Number.isInteger(input.xp)||input.xp<0)))throw Error('Keine gültige Lernstand-Datei. Bitte einen JSON-Export des Trainers wählen.');
  const out={completed:[],xp:0,streak:0,last_active:null,teacher_id:'sakura',speaker_id:2,tts_speed:1,
    ui_scale:1,motion_enabled:true,motion_preset:'natural',show_kiko:true,library_all:false,
    review:{},last_lesson:{},speech_scores:{},study_cards:{},lesson_sessions:{},legacy_unlocked:[],course_revision:0};
  for(const key of ['review','last_lesson','speech_scores','study_cards','lesson_sessions'])
    if(record(input[key]))out[key]=JSON.parse(JSON.stringify(input[key]));
  for(const key of ['completed','legacy_unlocked'])
    if(Array.isArray(input[key]))out[key]=[...new Set(input[key].filter(v=>typeof v==='string'&&v.length<150))];
  for(const key of ['xp','streak','speaker_id','course_revision'])out[key]=Math.floor(number(input[key],0,10_000_000,0));
  for(const key of ['motion_enabled','show_kiko','library_all'])if(typeof input[key]==='boolean')out[key]=input[key];
  if(typeof input.teacher_id==='string'&&/^[a-z]{2,15}$/.test(input.teacher_id))out.teacher_id=input.teacher_id;
  if(['natural','gentle','lively','subtle','off'].includes(input.motion_preset))out.motion_preset=input.motion_preset;
  if(/^\d{4}-\d{2}-\d{2}$/.test(input.last_active))out.last_active=input.last_active;
  out.tts_speed=number(input.tts_speed,.5,1.4,1);out.ui_scale=number(input.ui_scale,.8,1.2,1);
  return out;
}
export function localDate(date=new Date()) { return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`; }
export class Store {
  constructor(data={},persist=()=>true) { this.data=cleanProfile(data);this.persist=persist; }
  save() { if(this.persist(JSON.stringify(this.data))===false)throw Error('Lernstand konnte nicht gespeichert werden. Bitte Speicherplatz prüfen.'); }
  touch(date=new Date()) {
    const today=localDate(date);if(this.data.last_active===today)return;
    const yesterday=new Date(date);yesterday.setDate(date.getDate()-1);
    this.data.streak=this.data.last_active===localDate(yesterday)?this.data.streak+1:1;this.data.last_active=today;
  }
  complete(lesson) { if(!this.data.completed.includes(lesson.key)) { this.data.completed.push(lesson.key);this.data.xp+=lesson.xp??20; }this.touch();this.save(); }
}
export class Course {
  constructor(course,catalog,details,store) {
    this.raw=course;this.catalog=catalog;this.details=details;this.store=store;
    const all=course.units.flatMap((unit,ui)=>unit.lessons.map((lesson,li)=>({...lesson,key:lesson.id??`${ui}:${li}`,unit:unit.title.replace(/^\d+\.\s*/,''),level:lesson.stage??unit.level})));
    this.byKey=new Map(all.map(l=>[l.key,l]));
    const order=course.learning_order??all.map(l=>l.key);
    if(this.byKey.size!==all.length||new Set(order).size!==all.length||order.some(k=>!this.byKey.has(k)))throw Error('Kurskennungen sind ungültig.');
    this.lessons=order.map(k=>this.byKey.get(k));this.positions=new Map(order.map((k,i)=>[k,i]));
    this.cards=this.lessons.flatMap(l=>l.cards.map((c,i)=>({...c,key:`${l.key}:${i}`,lesson_key:l.key,lesson:l.title,card_index:i})));
    this.stages=[...new Set(this.lessons.map(l=>l.level))];
    if(store.data.course_revision!==course.revision) {
      const allowed=new Set(store.data.legacy_unlocked);const done=new Set(store.data.completed);
      (course.legacy_order??[]).forEach((k,i,keys)=>{if(!i||done.has(k)||done.has(keys[i-1]))allowed.add(k);});
      if(this.byKey.has(store.data.last_lesson.key))allowed.add(store.data.last_lesson.key);
      store.data.legacy_unlocked=[...allowed];store.data.course_revision=course.revision;store.save();
    }
  }
  teacher() { return this.catalog.TEACHERS.find(t=>t.id===this.store.data.teacher_id)??this.catalog.TEACHERS[0]; }
  unlocked(key) { const frontier=Math.max(-1,...this.store.data.completed.map(k=>this.positions.get(k)??-1));return this.byKey.has(key)&&(this.positions.get(key)<=frontier+1||this.store.data.legacy_unlocked.includes(key)); }
  next() { const cursor=this.store.data.last_lesson.key;if(this.unlocked(cursor)&&!this.store.data.completed.includes(cursor))return this.byKey.get(cursor);return this.lessons.find(l=>!this.store.data.completed.includes(l.key))??this.lessons.at(-1); }
  available(all=false) { if(all)return this.cards;const done=new Set(this.store.data.completed),cursor=this.store.data.last_lesson;const cards=this.cards.filter(c=>done.has(c.lesson_key)||(c.lesson_key===cursor.key&&c.card_index<=(cursor.card??0)));return cards.length?cards:[this.cards[0]]; }
  search(query='',stage='Alle') { const terms=query.normalize('NFKC').toLowerCase().split(/\s+/).filter(Boolean);return this.lessons.filter(l=>(stage==='Alle'||l.level===stage)&&terms.every(t=>[l.title,l.unit,l.goal??'',...l.cards.flatMap(c=>[c.jp,c.de,c.romaji])].join(' ').normalize('NFKC').toLowerCase().includes(t))); }
  profile(card,lesson) {
    return card.detail??this.details.profiles[card.jp]??{kind:'Lernwort / Satzmuster',usage:`In dieser Karte lernst du: ${card.de}.`,
      explain:card.note||'Vergleiche die japanische Schreibweise mit der Lesung und lerne zuerst diese konkrete Form.',
      pitfall:'Die deutsche Aussprachehilfe ist eine Annäherung. Höre auf die Vokallängen.',parts:[],extra:[],register:'',
      scenario:{question:'Welche Beschreibung gehört zu dieser Lernkarte?',correct:card.de,wrong:lesson.cards.filter(c=>c.de!==card.de).map(c=>c.de).slice(0,3)}};
  }
  example(card) { if(record(card.example)&&['jp','romaji','de'].every(k=>card.example[k]))return card.example;const x=this.catalog.EXAMPLES[card.jp];return Array.isArray(x)?{jp:x[0],romaji:x[1],de:x[2]}:card; }
  blocks(card,lesson) {
    const roman=card.romaji.trim().split(/\s+/);if(roman.length>=2&&roman.length<=10)return roman;
    const jp=card.jp.replace(/[。！？!?]+$/,'');const parts=this.profile(card,lesson).parts??[];
    if(parts.length>=2&&parts.length<=10&&compact(parts.map(p=>p[0]).join(''))===compact(jp))return parts.map(p=>p[0]);
    const chars=[];for(const c of jp) { if('ゃゅょャュョぁぃぅぇぉァィゥェォ'.includes(c)&&chars.length)chars[chars.length-1]+=c;else if(c.trim())chars.push(c); }
    return chars.length>=2&&chars.length<=10?chars:[];
  }
  speechTarget(card,lesson) { return lesson.speech?.find(t=>t.target.replace(/[。！？!?]+$/,'')===card.jp.replace(/[。！？!?]+$/,''))??{target:card.jp,accept:[card.jp],meaning:card.de,romaji:card.romaji}; }
}
export class Session {
  constructor(lesson,course,restore=true) {
    this.lesson=lesson;this.course=course;this.store=course.store;this.index=0;this.phase='understand';this.mode='learn';this.recap=[];this.recap_total=0;this.recap_passed=0;
    const saved=this.store.data.lesson_sessions[lesson.key];
    if(restore&&record(saved)) {
      this.index=Math.floor(number(saved.index,0,lesson.cards.length-1,0));this.phase=PHASES.includes(saved.phase)?saved.phase:'understand';
      if(saved.mode==='recap'&&Array.isArray(saved.recap)) {
        this.recap=saved.recap.filter(i=>Number.isInteger(i)&&i>=0&&i<lesson.cards.length);
        if(this.recap.length) { this.mode='recap';this.index=this.recap[0]; }
        this.recap_total=Math.floor(number(saved.recap_total,this.recap.length,lesson.cards.length*2,lesson.cards.length));
        this.recap_passed=Math.floor(number(saved.recap_passed,0,this.recap_total,0));
      }
    }
    this.reset();this.snapshot();
  }
  get card() {return this.lesson.cards[this.index];}
  get key() {return `${this.lesson.key}:${this.index}`;}
  reset() { this.success=false;this.feedback='';this.tokens=[];this.audio_seen=false;this.audio_skipped=false;this.skipped=false;this.chosen=null;this.listenCard=shuffle(this.lesson.cards.slice(0,this.index+1),`${this.key}:${this.phase}`)[0]; }
  snapshot() {this.store.data.lesson_sessions[this.lesson.key]={index:this.index,phase:this.phase,mode:this.mode,recap:[...this.recap],recap_total:this.recap_total,recap_passed:this.recap_passed};this.store.data.last_lesson={key:this.lesson.key,card:this.index};this.store.save();}
  metrics() { const existing=this.store.data.study_cards[this.key];const m=record(existing)?existing:{};this.store.data.study_cards[this.key]=m;for(const key of ['attempts','mistakes','speech_attempts','speech_skips'])if(!Number.isInteger(m[key]))m[key]=0;if(!Array.isArray(m.phases))m.phases=[];return m; }
  mark(ok,feedback,skipped=false) {
    if(this.success)return;this.success=!!ok;this.feedback=feedback;this.skipped=skipped;
    const m=this.metrics();m.attempts++;if(!ok) {m.mistakes++;this.store.data.review[this.key]={box:0,due:Date.now()/1000};}
    else if(!skipped&&!m.phases.includes(this.phase))m.phases.push(this.phase);
    if(skipped) {if(!Array.isArray(m.skipped_phases))m.skipped_phases=[];m.skipped_phases.push(this.phase);}
    this.store.touch();this.snapshot();
  }
  answers() {
    let correct,pool;
    if(this.mode==='recap'||this.phase==='meaning') {correct=this.card.de;pool=this.lesson.cards.map(c=>c.de);}
    else if(this.phase==='listen') {correct=this.listenCard.de;pool=this.lesson.cards.slice(0,this.index+1).map(c=>c.de);}
    else if(this.phase==='apply') {const p=this.course.profile(this.card,this.lesson).scenario;correct=p.correct;pool=p.wrong;}
    else {correct=this.card.romaji;pool=this.lesson.cards.slice(0,this.index+1).map(c=>c.romaji);}
    const options=shuffle([...new Set(pool)].filter(p=>p!==correct),this.key).slice(0,3);options.push(correct);
    return {correct,options:shuffle(options,`${this.key}:${this.phase}:options`)};
  }
  choose(value) {
    const {correct,options}=this.answers();if(!options.includes(value))return;
    if(this.phase==='listen'&&this.mode!=='recap'&&!this.audio_seen&&!this.audio_skipped) {this.feedback='Bitte zuerst anhören oder „Ohne Ton üben“ wählen.';return;}
    this.chosen=value;const ok=value===correct;this.mark(ok,ok?'Richtig. '+(this.phase==='apply'?this.course.profile(this.card,this.lesson).explain:`Die passende Zuordnung ist: ${correct}`):'Noch nicht. Vergleiche die Erklärung und versuche es erneut.',this.phase==='listen'&&this.audio_skipped);
  }
  checkWrite(text) {const ok=[this.card.romaji,...(this.card.romaji_aliases??[])].some(r=>matchesRomaji(text,r));this.mark(ok,ok?'Richtig geschrieben. Auch die Vokallängen stimmen.':'Noch nicht passend. Für ō kannst du ou oder oo schreiben; die Länge darf nicht fehlen.');}
  checkBuild() {const parts=this.course.blocks(this.card,this.lesson);if(!parts.length)return;const ok=this.tokens.length===parts.length&&this.tokens.map(i=>parts[i]).every((v,i)=>v===parts[i]);this.mark(ok,ok?'Richtig zusammengesetzt.':'Die Reihenfolge stimmt noch nicht. Vergleiche die Lernkarte und versuche es erneut.');}
  advance() {
    if(!this.success)return 'blocked';
    if(this.mode==='recap') {this.recap.shift();this.recap_passed++;if(!this.recap.length){this.store.complete(this.lesson);delete this.store.data.lesson_sessions[this.lesson.key];this.store.save();return 'complete';}this.index=this.recap[0];}
    else {const index=PHASES.indexOf(this.phase);
      if(index<PHASES.length-1)this.phase=PHASES[index+1];
      else if(this.index<this.lesson.cards.length-1){this.index++;this.phase='understand';}
      else {this.mode='recap';this.phase='meaning';this.recap=shuffle(this.lesson.cards.map((_,i)=>i),this.lesson.key);this.recap.push(...this.recap.filter(i=>(this.store.data.study_cards[`${this.lesson.key}:${i}`]?.mistakes??0)>0));this.recap_total=this.recap.length;this.index=this.recap[0];}
    }
    this.reset();this.snapshot();return 'next';
  }
}
export function speechMatch(heard,accepted) {
  const normalize=s=>compact(s.replace(/<\|.*?\|>/g,'')).replace(/[ァ-ヶ]/g,c=>String.fromCharCode(c.charCodeAt(0)-0x60));
  const text=normalize(heard);if(!text)return false;
  return accepted.some(a=>text===normalize(a));
}
export function reviewCard(course,known,card,now=Date.now()/1000) {
  const old=course.store.data.review[card.key];const box=known?Math.min(5,Math.max(0,Number(old?.box)||0)+1):0;
  course.store.data.review[card.key]={box,due:now+[60,600,86400,259200,604800,2592000][box]};course.store.touch();course.store.save();
}

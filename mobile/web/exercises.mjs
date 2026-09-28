/* Additional rounds on the existing course and profile. No XP or completion writes. */
import {SpeechSupport} from './speech-support.mjs';
export const FAMILIES={pairs:'Paare zuordnen',echo:'Nachsprechen',recall:'Sag das auf Japanisch',hear_gap:'Hörlücke',choice_gap:'Lücke auswählen',multi_gap:'Mehrfachlücken',translate:'Übersetzen mit Bausteinen',read:'Lesen und antworten'};
export const INSTRUCTIONS={pairs:'Wähle links eine Form oder ein Audiofeld und rechts ihre Bedeutung. Ordne alle Paare zu und bestätige mit Überprüfen.',echo:'Höre zuerst normal oder langsam zu. Sprich danach die sichtbare Vorlage nach.',recall:'Sprich die deutsche Vorgabe auf Japanisch. Die gesuchte Antwort bleibt zunächst verborgen.',hear_gap:'Höre zu und schreibe nur die fehlende Einheit in Romaji. Normal und Langsam wiederholen die Vorlage.',choice_gap:'Wähle eine passende Ergänzung für die Lücke und bestätige mit Überprüfen.',multi_gap:'Wähle zuerst eine Lücke, dann ihren Baustein. Ergänze alle Lücken und bestätige mit Überprüfen.',translate:'Übersetze die deutsche Vorgabe mit den japanischen Bausteinen. Tippe sie in der Satzreihenfolge an und bestätige mit Überprüfen.',read:'Lies den japanischen Text. Wähle eine Antwort auf die Frage und bestätige mit Überprüfen.'};
const clone=x=>JSON.parse(JSON.stringify(x));
export const normalize=s=>String(s).normalize('NFKC').toLowerCase().replace(/[\s。！？!?.,、·「」“”]/gu,'');
export function matches(value,answers,mode='exact') {
  const speech=s=>normalize(s.replace(/<\|.*?\|>/g,'')).replace(/[ァ-ヶ]/g,c=>String.fromCharCode(c.charCodeAt(0)-0x60));
  if(mode==='speech')return !!speech(value)&&answers.some(a=>speech(a)===speech(value));
  const forms=new Set();
  for(const a of answers) {const f=new Set([normalize(a)]);
    if(mode==='romaji')for(const [mark,alts] of Object.entries({'ā':['aa'],'ī':['ii'],'ū':['uu'],'ē':['ee'],'ō':['ou','oo']}))for(const old of [...f])for(const alt of alts)f.add(old.replaceAll(mark,alt));
    for(const v of f)forms.add(v);
  }
  return !!normalize(value)&&forms.has(normalize(value));
}
export function order(values,seed) {
  const out=[...values];let h=2166136261;
  for(const c of seed)h=Math.imul(h^c.codePointAt(0),16777619)>>>0;
  for(let i=out.length-1;i>0;i--){h=(Math.imul(h,1664525)+1013904223)>>>0;const j=h%(i+1);[out[i],out[j]]=[out[j],out[i]];}
  return out;
}
export class ExerciseBook {
  constructor(data){this.data=data;this.packs=new Map(data.packs.map(p=>[p.lesson,p]));this.tasks=new Map(data.tasks.map(t=>[t.id,t]));}
}
export class ExerciseRound {
  constructor(book,lesson,store){this.book=book;this.lesson=lesson;this.store=store;this.pack=book.packs.get(lesson.key);this.key=`exercises:${lesson.key}`;
    const saved=store.data.lesson_sessions[this.key];this.state=saved&&saved.revision===book.data.revision&&JSON.stringify(saved.queue)===JSON.stringify(this.pack.tasks)?clone(saved):this.fresh();this.sanitize();this.save();}
  fresh(){return {revision:this.book.data.revision,queue:[...this.pack.tasks],index:0,stage:'intro',review:[],review_index:0,reviewed:[],outcomes:[],task:{}};}
  sanitize(){const s=this.state;if(!['intro','main','review','complete'].includes(s.stage))s.stage='intro';
    for(const [field,max] of [['index',s.queue.length-1],['review_index',5]])s[field]=Number.isInteger(s[field])?Math.min(max,Math.max(0,s[field])):0;
    for(const field of ['review','reviewed'])s[field]=Array.isArray(s[field])?s[field].filter(v=>this.pack.tasks.includes(v)).slice(0,field==='review'?6:20):[];
    if(s.stage==='review'&&s.review_index>=s.review.length)s.stage='complete';s.outcomes=Array.isArray(s.outcomes)?s.outcomes.slice(-200):[];
    if(!s.task||typeof s.task!=='object'||Array.isArray(s.task))s.task={};
    const defaults={choice:null,text:'',tokens:[],slots:{},pairs:{},active:0,left:null,heard:[],help:0,help_open:false,success:false,feedback:'',checks:0,per_slot:[],transcript:'',audio_help:false};
    for(const [key,value] of Object.entries(defaults))if(!(key in s.task)||(value!==null&&(typeof s.task[key]!==typeof value||Array.isArray(s.task[key])!==Array.isArray(value)||s.task[key]===null)))s.task[key]=clone(value);
    const d=s.task;for(const k of ['choice','left'])if(d[k]!==null&&typeof d[k]!=='string')d[k]=null;
    for(const k of ['text','feedback','transcript'])d[k]=d[k].slice(0,4000);
    for(const [k,max] of [['help',2],['checks',1000],['active',9]])d[k]=Number.isInteger(d[k])?Math.min(max,Math.max(0,d[k])):0;
    for(const k of ['tokens','heard'])d[k]=d[k].filter(v=>typeof v==='string').slice(0,20);
    for(const k of ['slots','pairs'])d[k]=Object.fromEntries(Object.entries(d[k]).filter(([,v])=>typeof v==='string').slice(0,20));
  }
  get task(){const s=this.state,ids=s.stage==='review'?s.review:s.queue,i=s.stage==='review'?s.review_index:s.index;return this.book.tasks.get(ids[Math.min(i,ids.length-1)]);}
  get answer(){return this.state.task;}
  get support(){const key=this.supportKey??`exercise:${this.task.id}:${this.state.stage}`;if(this._support?.key!==key)this._support=new SpeechSupport(this.store,key,{card:this.task.card,lesson:this.task.card.slice(0,this.task.card.lastIndexOf(':')),kind:'exercise',task:this.task.id});return this._support;}
  acceptSupport(deck){if(!['main','review'].includes(this.state.stage)||!['echo','recall'].includes(this.task.family)||this.answer.success||!this.support.confirm(deck))return false;
    this.answer.success=true;this.answer.feedback=this.support.data.feedback;this.answer.supported_speech=true;this.log('selection');
    if(this.state.stage==='main')this.state.review=this.state.review.filter(id=>id!==this.task.id&&id!==this.task.repeat);this.save();return true;}
  save(){this.store.data.lesson_sessions[this.key]=clone(this.state);this.store.save();}
  start(){if(this.state.stage==='intro'){this.state.stage='main';this.save();}}
  restart(){for(const id of this.pack.tasks)for(const phase of ['main','review'])delete this.store.data.speech_support?.[`exercise:${id}:${phase}`];this._support=null;this.state=this.fresh();this.sanitize();this.save();}
  help(level){this.answer.help=Math.max(level,this.answer.help);this.answer.help_open=true;this.save();}
  set(key,value){if(['help_open','active','left'].includes(key)||!this.answer.success){this.answer[key]=value;this.save();}}
  heard(identity='target',readingHelp=false){if(!this.answer.heard.includes(identity))this.answer.heard.push(identity);if(readingHelp)this.answer.audio_help=true;this.save();}
  technical(message,paused=false){this.answer.feedback=message;this.log(paused?'paused':'technical');this.save();}
  log(status){this.state.outcomes.push({task:this.task.id,result:status,help:this.answer.help,audio_help:this.answer.audio_help});this.state.outcomes=this.state.outcomes.slice(-200);}
  schedule(){const t=this.task;this.store.data.review[t.card]={box:0,due:Date.now()/1000+60};const target=t.repeat??t.id;if(this.state.stage==='main'&&!this.state.review.includes(target)&&this.state.review.length<6)this.state.review.push(target);}
  check(speech=null){const d=this.answer,t=this.task,k=t.family;if(!['main','review'].includes(this.state.stage)||d.success)return false;
    if(['hear_gap','echo'].includes(k)&&!d.heard.includes('target')){d.feedback='Höre die Vorlage zuerst vollständig an. Du kannst auch pausieren.';this.save();return false;}
    if(k==='pairs'&&t.mode==='audio'&&!t.pairs.every(p=>d.heard.includes(p.id))){d.feedback='Höre zuerst alle Audiofelder vollständig an.';this.save();return false;}
    let ok=false,feedback=t.why;d.per_slot=[];
    if(['echo','recall'].includes(k)){
      if(speech===null)return false;if(!speech.trim()){this.technical('Keine sichere Erkennung. Prüfe das Mikrofon oder pausiere.');return false;}d.transcript=speech;ok=matches(speech,t.accepted_speech,'speech');
      if(!ok){d.checks++;this.log('unverified');this.schedule();d.feedback='Der erkannte Text ist nicht unter den geprüften Antworten. Eine andere zulässige Form oder ein Erkennungsfehler ist möglich. Keine Aussprachebewertung. Öffne die Erklärung oder versuche es erneut.';this.save();return false;}
    }else if(k==='pairs'){
      ok=t.pairs.every(p=>d.pairs[p.id]===p.id);const wrong=t.pairs.find(p=>d.pairs[p.id]!==p.id);if(wrong)feedback=`Noch offen: ${wrong.jp} bedeutet hier „${wrong.de}“. Wähle das linke Feld erneut, um nur dieses Paar zu korrigieren.`;
    }else if(['choice_gap','read'].includes(k)){ok=t.answers.includes(d.choice);feedback=t.choices.find(c=>c.id===d.choice)?.feedback??'Wähle zuerst eine Antwort aus.';
    }else if(k==='hear_gap'){ok=matches(d.text,t.answers,t.input_mode);feedback=t.hint+' Vergleiche die gehörte Einheit und behalte die Vokallänge bei.';
    }else if(['translate','multi_gap'].includes(k)){
      const by=Object.fromEntries(t.tokens.map(v=>[v.id,v.text])),ids=k==='translate'?d.tokens:t.solutions[0].map((_,i)=>d.slots[String(i)]),words=ids.map(v=>by[v]??'');
      ok=ids.length===new Set(ids).size&&t.solutions.some(v=>JSON.stringify(v)===JSON.stringify(words));feedback=t.hint+' Prüfe Bedeutung und Reihenfolge; die Aufgabe benötigt eine vollständige passende Lösung.';
      if(k==='multi_gap'){d.per_slot=words.map((word,i)=>t.solutions.some(v=>word===v[i]));feedback=d.per_slot.map((good,i)=>`Lücke ${i+1}: `+(good?'passt an dieser Stelle.':t.slot_feedback[i])).join(' ');}
    }
    d.checks++;d.success=ok;
    if(ok){const supported=d.help>0||d.audio_help;this.log(d.help===2?'solution':supported?'hint':d.checks===1?'independent':'corrected');d.feedback=(supported?'Mit Unterstützung gelöst. ':'Passend gelöst. ')+feedback;}
    else{this.log('wrong');this.schedule();d.feedback=feedback;if(d.checks>=3)d.feedback+=' Du darfst die vollständige Erklärung öffnen oder eine Pause machen. Die Aufgabe bleibt offen.';}
    this.save();return ok;
  }
  advance(){if(!this.answer.success)return false;const s=this.state;
    if(s.stage==='main'){s.index++;if(s.index>=s.queue.length){s.index=s.queue.length-1;s.stage=s.review.length?'review':'complete';}}
    else if(s.stage==='review'){s.review_index++;if(s.review_index>=s.review.length)s.stage='complete';}
    s.task={};this.sanitize();this.save();return true;
  }
}

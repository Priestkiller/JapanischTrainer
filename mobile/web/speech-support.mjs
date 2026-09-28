/* Speech assistance is a separate outcome, never a pronunciation score or XP. */
export const SUPPORT_MESSAGE='Die Erkennung klappt gerade nicht zuverlässig. Du kannst die passende Antwort auswählen und später weiter sprechen üben.';
export const REASONS={mismatch:'Der erkannte Text passt noch nicht zur Vorgabe. Das kann auch an der Erkennung liegen.',unreliable:'Es wurde keine verlässliche Sprache erkannt. Daraus folgt kein Aussprachefehler.',technical:'Die Aufnahme oder Auswertung ist technisch fehlgeschlagen. Das ist kein Aussprachefehler.'};
const object=x=>x&&typeof x==='object'&&!Array.isArray(x);
export class SpeechSupport {
 constructor(store,key,source={}){this.store=store;this.key=key;this.source=source;this.active=null;const all=store.data.speech_support??={};const old=all[key];
  this.data=object(old)?old:{};const d=this.data;
  d.failures=Number.isInteger(d.failures)?Math.max(0,Math.min(1000,d.failures)):0;
  d.reason=Object.hasOwn(REASONS,d.reason)?d.reason:'';
  for(const k of ['open','prepared','assisted'])d[k]=d[k]===true;
  d.choice=typeof d.choice==='string'?d.choice:null;d.feedback=typeof d.feedback==='string'?d.feedback.slice(0,4000):'';
  d.transcript=typeof d.transcript==='string'?d.transcript.slice(0,4000):'';
  all[key]=d;store.data.speech_reviews??={};
 }
 save(){this.store.data.speech_support[this.key]=this.data;this.store.save();}
 get unlocked(){return this.data.failures>=3;}
 begin(id){if(!id||this.active||this.data.assisted)return false;this.active=id;return true;}
 cancel(){this.active=null;}
 finish(id,reason){if(!id||id!==this.active)return false;this.active=null;
  if(reason==='accepted'){delete this.store.data.speech_reviews[this.key];this.data.feedback='Der erkannte Text passt zur Vorgabe.';this.save();return true;}
  if(!Object.hasOwn(REASONS,reason))return false;
  this.data.failures++;this.data.reason=reason;this.data.feedback=REASONS[reason];this.save();return true;
 }
 open(){if(!this.unlocked)return false;this.data.open=true;this.save();return true;}
 select(id){if(!this.unlocked||this.data.assisted)return;this.data.choice=id;this.save();}
 prepare(){if(!this.unlocked)return;this.data.prepared=true;this.save();}
 confirm(deck){if(this.active||!this.unlocked||!this.data.open||this.data.assisted||deck.options.length<2||deck.needsPreparation&&!this.data.prepared)return false;
  const picked=deck.options.find(c=>c.id===this.data.choice);if(!picked){this.data.feedback='Wähle eine Antwort und bestätige sie.';this.save();return false;}
  if(picked.id!==deck.correct){this.data.feedback=`Noch nicht. ${picked.jp} (${picked.romaji}) bedeutet hier „${picked.de}“. Vergleiche die Vorgabe und versuche es erneut.`;this.save();return false;}
  this.data.assisted=true;this.data.feedback='Mit Auswahlhilfe geschafft. Sprechen übst du später weiter.';
  this.store.data.speech_reviews[this.key]={...this.source,due:Date.now()/1000+86400,status:'pending'};this.save();return true;
 }
 newRound(){this.cancel();this.data={failures:0,reason:'',open:false,prepared:false,assisted:false,choice:null,feedback:''};this.save();}
}
const norm=x=>String(x??'').normalize('NFKC').toLowerCase().replace(/[\s。！？!?.,、]/g,'');
export function speechDeck(target,known,available=[],mode='meaning'){
 const candidates=[target],usedJP=new Set([norm(target.jp)]),usedDE=new Set([norm(target.de)]);
 function add(c){if(!c||!c.jp||!c.de||usedJP.has(norm(c.jp))||usedDE.has(norm(c.de)))return;usedJP.add(norm(c.jp));usedDE.add(norm(c.de));candidates.push(c);}
 [...known].reverse().forEach(add);const needsPreparation=candidates.length<2;
 if(needsPreparation)for(const c of available){add(c);if(candidates.length>=2)break;}
 const options=candidates.slice(0,4).map(c=>({...c,id:c.key,label:mode==='japanese'?`${c.jp} · ${c.romaji}`:c.de}));
 // Stable rotation; never consistently put the correct answer first.
 const shift=[...target.key].reduce((n,c)=>n+c.codePointAt(0),0)%Math.max(1,options.length);
 options.push(...options.splice(0,shift));
 return {correct:target.key,options,needsPreparation,prepare:candidates.slice(0,2),mode};
}

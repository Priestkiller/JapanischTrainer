import {SUPPORT_MESSAGE} from './speech-support.mjs';
export function supportView(support,deck,esc){const d=support.data;
 let html=d.failures?`<p class="support-count" role="status">${d.failures} erfolglose Versuche · ${esc(d.feedback)}</p>`:'';
 if(!support.unlocked||d.assisted)return html;
 html+=`<button id="speech-alternative" class="ghost wide">${d.open?'Auswahlhilfe schließen':'Antwort stattdessen auswählen'}</button>`;
 if(!d.open)return html;
 html+=`<section class="speech-alternative" role="dialog" aria-modal="true" aria-labelledby="support-title"><div class="support-top"><h3 id="support-title">Mit Auswahlhilfe weiterlernen</h3><button id="speech-close" aria-label="Zurück zur Sprechaufgabe">×</button></div><p>${SUPPORT_MESSAGE}</p>${d.feedback?`<p class="support-feedback" role="status">${esc(d.feedback)}</p>`:''}`;
 if(deck.needsPreparation&&!d.prepared){html+='<p>Für diese erste Auswahl lernst du den Vergleich vorher kennen:</p>'+deck.prepare.map(c=>`<p><strong lang="ja">${esc(c.jp)}</strong> · ${esc(c.romaji)} · ${esc(c.de)}</p>`).join('')+'<button id="speech-prepare">Verglichen · jetzt auswählen</button>';}
 else{const target=deck.options.find(c=>c.id===deck.correct);html+=`<p class="support-prompt">${deck.mode==='japanese'?'Wähle die passende japanische Form für: '+esc(target.de):'Welche Bedeutung gehört zu '+esc(target.jp)+' ('+esc(target.romaji)+')?'}</p><div class="options">${deck.options.map(c=>`<button data-support-choice="${esc(c.id)}" aria-pressed="${d.choice===c.id}">${esc(c.label)}</button>`).join('')}</div><button id="speech-confirm" class="primary wide">Auswahl bestätigen</button>`;}
 return html+'</section>';
}
export function bindSupport(support,refresh,accept){if(support.active)return;const q=s=>document.querySelector(s);
 const panel=q('.speech-alternative'),root=q('.focus-session')??q('.talk-layout');
 if(panel&&root){root.append(panel);for(const e of root.children)if(e!==panel)e.inert=true;panel.onkeydown=e=>{if(e.key==='Escape'){e.preventDefault();q('#speech-close').click();}if(e.key==='Tab'){const buttons=[...panel.querySelectorAll('button:not(:disabled)')];e.preventDefault();buttons[(buttons.indexOf(document.activeElement)+(e.shiftKey?-1:1)+buttons.length)%buttons.length]?.focus();}};q('#speech-close').onclick=()=>{support.data.open=false;support.save();refresh();};}
 if(q('#speech-alternative'))q('#speech-alternative').onclick=()=>{if(!support.data.open)support.open();else{support.data.open=false;support.save();}refresh();};
 if(q('#speech-prepare'))q('#speech-prepare').onclick=()=>{support.prepare();refresh();};
 document.querySelectorAll('[data-support-choice]').forEach(b=>b.onclick=()=>{support.select(b.dataset.supportChoice);document.querySelectorAll('[data-support-choice]').forEach(n=>n.setAttribute('aria-pressed',n===b));});
 if(q('#speech-confirm'))q('#speech-confirm').onclick=()=>{accept();refresh();};
}

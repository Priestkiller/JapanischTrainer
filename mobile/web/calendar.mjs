/* GPL-3.0-or-later. Civil dates, no UTC/local-midnight or DST drift. */
export function validDay(value) {
  if(typeof value!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(value))return false;
  const [y,m,d]=value.split('-').map(Number);
  return y>=2000&&m>=1&&m<=12&&d>=1&&d<=new Date(Date.UTC(y,m,0)).getUTCDate();
}
export function dayKey(date=new Date()) {return `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;}
export function dayOffset(day,offset) {
  if(!validDay(day))return null;
  const [y,m,d]=day.split('-').map(Number),date=new Date(Date.UTC(y,m-1,d+offset));
  return date.toISOString().slice(0,10);
}
export function cleanDays(days) {return [...new Set((Array.isArray(days)?days:[]).filter(validDay))].sort().slice(-20_000);}
export function currentStreak(data,today=dayKey()) {
  return [today,dayOffset(today,-1)].includes(data.last_active)?data.streak:0;
}
export function monthDays(month,today=dayKey(),known=[]) {
  if(!/^\d{4}-\d{2}$/.test(month)||!validDay(month+'-01'))throw Error('Ungültiger Kalendermonat.');
  const [y,m]=month.split('-').map(Number),start=new Date(Date.UTC(y,m-1,1));
  const leading=(start.getUTCDay()+6)%7,days=start.getUTCMonth()===11?31:new Date(Date.UTC(y,m,0)).getUTCDate(),set=new Set(known);
  const cells=Array.from({length:leading},()=>null);
  for(let d=1;d<=days;d++){const key=`${month}-${String(d).padStart(2,'0')}`;cells.push({key,day:d,learned:set.has(key),today:key===today,future:key>today});}
  while(cells.length%7)cells.push(null);
  return cells;
}
export function shiftMonth(month,offset) {
  const [y,m]=month.split('-').map(Number),d=new Date(Date.UTC(y,m-1+offset,1));
  return d.toISOString().slice(0,7);
}
export function calendarView(data,month,esc,today=dayKey()) {
  const streak=currentStreak(data,today),cells=monthDays(month,today,data.learning_days);
  const label=new Intl.DateTimeFormat('de-DE',{month:'long',year:'numeric',timeZone:'UTC'}).format(new Date(month+'-01T12:00:00Z'));
  const since=data.learning_calendar_since,partial=data.learning_calendar_partial;
  return `<div class="page-heading"><p class="eyebrow">Deine Lerntage</p><h1>Deine Lernserie</h1><p>${streak} ${streak===1?'Tag':'Tage'} in Folge${data.last_active===today?' · Heute schon gelernt':streak?' · Lerne heute weiter':' · Jeder neue Tag zählt'}.</p></div>
  <button class="ghost" data-nav="home">‹ Zur Startseite</button><section class="card streak-calendar"><div class="calendar-heading"><button id="calendar-prev" aria-label="Vorheriger Monat" ${month==='2000-01'?'disabled':''}>‹</button><h2 id="calendar-month">${esc(label)}</h2><button id="calendar-next" aria-label="Nächster Monat" ${month>=today.slice(0,7)?'disabled':''}>›</button></div>
  <table class="calendar-grid" aria-labelledby="calendar-month"><thead><tr>${['Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag','Sonntag'].map(d=>`<th scope="col"><abbr title="${d}">${d.slice(0,2)}</abbr></th>`).join('')}</tr></thead><tbody>${Array.from({length:cells.length/7},(_,row)=>`<tr>${cells.slice(row*7,row*7+7).map(c=>c?`<td class="${c.learned?'learned ':''}${c.today?'today ':''}${c.future?'future':''}"><time datetime="${c.key}" aria-label="${c.day}. ${esc(label)}${c.learned?', gelernt':''}${c.today?', heute':''}">${c.day}${c.learned?'<span aria-hidden="true">✓</span>':''}</time></td>`:'<td></td>').join('')}</tr>`).join('')}</tbody></table>
  <p class="calendar-legend"><span>✓ Gelernt</span><span>Umrandung: Heute</span></p><p class="sub">Eine bearbeitete Lernaufgabe zählt. Die App nur zu öffnen, erhöht deine Serie nicht.</p></section>
  ${partial?`<p class="info">Deine bisherige Serie bleibt erhalten. Ältere einzelne Lerntage wurden noch nicht gespeichert; der Kalender zeigt nur bekannte Tage${since?` und neue Lerntage ab ${esc(new Intl.DateTimeFormat('de-DE').format(new Date(since+'T12:00:00')))}`:''}.</p>`:''}`;
}

"""Native Tk/Pillow exercise adapter; reuses the lesson layout and audio engine."""
import time
from exercises import ExerciseBook, ExerciseRound, FAMILIES, order
from ui_renderer import WHITE, MUTED, INK

class ExerciseMixin:
    def init_exercises(self):
        self.exercise_book=ExerciseBook(self.learning.root);self.exercise_round=None;self.exercise_epoch=0
    def open_exercises(self):
        if self.job or self.recording:self.notify('Beende zuerst die laufende Aufnahme oder Wiedergabe.');return
        if self.lesson['key'] not in self.exercise_book.packs:return
        self.flow.snapshot();self.exercise_round=ExerciseRound(self.exercise_book,self.lesson,self.store)
        self.navigate('exercises')
    def exercise_return(self):
        if self.exercise_round.state['stage'] in ('main','review'):self.exercise_round.technical('Freiwillig pausiert. Die Aufgabe und deine Eingabe bleiben erhalten.',True)
        self.cancel_exercise();self.navigate('lesson')
    def cancel_exercise(self):
        self.exercise_epoch+=1
        try:
            import sounddevice as sd
            sd.stop()
        except Exception:pass
        if self.recording:self.exercise_stop(False)
        self.last_audio=None
        if self.exercise_round:self.exercise_round.save()
    def exercise_refresh(self):self.request_draw()
    def exercise_help(self,level=None):
        r=self.exercise_round
        if level is None:r.set('help_open',not r.answer['help_open']) if r.answer['help'] else r.help(1)
        else:r.help(level)
        self.request_draw()
    def exercise_input_changed(self,*_):
        if self.entry and self.entry_mode=='exercise':self.exercise_round.set('text',self.entry.get())
    def exercise_set(self,key,value):self.exercise_round.set(key,value);self.request_draw()
    def exercise_token(self,identity):
        r=self.exercise_round;d=r.answer
        if d['success']:return
        if r.task['family']=='multi_gap':
            slots=dict(d['slots']);active=str(d['active'])
            for k,v in list(slots.items()):
                if v==identity:del slots[k]
            if d['slots'].get(active)!=identity:slots[active]=identity
            r.set('slots',slots)
        else:
            tokens=list(d['tokens'])
            if identity in tokens:tokens.remove(identity)
            else:tokens.append(identity)
            r.set('tokens',tokens)
        self.request_draw()
    def exercise_pair(self,side,identity):
        r=self.exercise_round;d=r.answer
        if d['success']:return
        if side=='left':
            r.set('left',identity)
            if r.task['mode']=='audio':self.exercise_audio(identity)
        elif d['left']:
            pairs={k:v for k,v in d['pairs'].items() if v!=identity};pairs[d['left']]=identity;r.set('pairs',pairs)
        self.request_draw()
    def exercise_check(self):
        r=self.exercise_round
        if self.entry and self.entry_mode=='exercise':r.set('text',self.entry.get())
        if r.task['family'] in ('echo','recall'):self.exercise_record();return
        ok=r.check();self.react('praise' if ok else 'encourage','exercise-answer');self.request_draw()
    def exercise_next(self):
        if self.job or self.recording:return
        self.hide_entry();r=self.exercise_round
        if r.state['stage']=='intro':r.start()
        elif r.state['stage']=='complete':r.restart()
        else:r.advance()
        self.exercise_epoch+=1;self.last_audio=None;self.scroll=0;self.clear_reaction();self.request_draw()
    def exercise_audio(self,identity='target',slow=False,source_key=None,example_text=None):
        if self.recording or self.job:return
        r=self.exercise_round;t=r.task;teacher=self.learning.teacher();epoch=self.exercise_epoch
        if example_text:text=example_text
        elif source_key:text=self.exercise_card(source_key)['jp']
        elif t['family']=='pairs':text=next(p['jp'] for p in t['pairs'] if p['id']==identity)
        else:text=t.get('text',t['audio'])
        if t['family']=='recall':r.help(2)
        def done(_):
            if self.view=='exercises' and self.exercise_round is r and self.exercise_epoch==epoch and teacher['id']==self.learning.teacher()['id']:
                if not source_key and not example_text:r.heard(identity,t['family']=='read')
                self.request_draw()
        cancelled=lambda:self.closed or self.view!='exercises' or self.exercise_epoch!=epoch or teacher['id']!=self.learning.teacher()['id']
        done.on_error=lambda error:None if cancelled() else r.technical(error)
        self.run_worker('Hörbeispiel',lambda:self.engine.speak(text,float(self.store.data.get('tts_speed',1))*teacher['speed']*(.72 if slow else 1),int(teacher['speaker_id']),cancelled=cancelled),done)
    def exercise_record(self):
        r=self.exercise_round
        if self.recording:self.exercise_stop(True);return
        if self.job or r.answer['success']:return
        if r.task['family']=='echo' and 'target' not in r.answer['heard']:
            r.technical('Höre die sichtbare Vorlage zuerst vollständig an.');self.request_draw();return
        try:
            self.exercise_epoch+=1;self.engine.start_recording(self.store.data.get('mic_device'))
            self.recording=True;self.record_started=time.monotonic();self.last_audio=None;self.speech_error=''
        except Exception as exc:r.technical('Mikrofon nicht verfügbar. Du kannst pausieren oder es erneut versuchen. '+str(exc))
        self.request_draw()
    def exercise_stop(self,grade=True):
        if not self.recording:return
        self.recording=False;r=self.exercise_round;epoch=self.exercise_epoch;task_id=r.task['id'];teacher=self.learning.teacher()['id']
        try:
            self.last_audio=self.engine.stop_recording();self.last_rate=self.engine.sample_rate
            if grade:
                a=self.last_audio.copy();sr=self.last_rate;accepted=list(r.task['accepted_speech'])
                def done(result):
                    if self.view!='exercises' or self.exercise_round is not r or self.exercise_epoch!=epoch or r.task['id']!=task_id or self.learning.teacher()['id']!=teacher:return
                    if not result.reliable or result.quality and result.quality.status=='bad':r.technical('Diese Aufnahme ist nicht sicher auswertbar. Kein Aussprachefehler daraus abgeleitet.')
                    else:
                        ok=r.check(result.heard)
                        if ok:self.react('praise','exercise-speech')
                    self.request_draw()
                done.on_error=lambda error:None if self.view!='exercises' or self.exercise_epoch!=epoch or self.exercise_round is not r else r.technical(error)
                self.run_worker('Spracherkennung',lambda:self.engine.recognize_for_target(a,accepted,sr),done)
            else:r.technical('Aufnahme abgebrochen. Die Sprechaufgabe bleibt offen.',True)
        except Exception as exc:r.technical('Audio konnte nicht ausgewertet werden. '+str(exc))
        self.request_draw()
    def exercise_card(self,key):
        lesson,index=key.rsplit(':',1);return self.learning.by_key[lesson]['cards'][int(index)]
    def exercise_explain_card(self,p,o,w,key):
        c=self.exercise_card(key);lesson=self.learning.by_key[key.rsplit(':',1)[0]];d=self.book.profile(c,lesson)
        o=self.text_block(p,o,w,'Bedeutung hier',c['jp']+'\n'+c['romaji']+'\n'+c['de'])
        o=self.text_block(p,o,w,'Aussprachehilfe · deutsche Näherung',c.get('approx','')+' '+c.get('note',''))
        o=self.exercise_button(p,o,w,'ex-teach-'+key,'Normal anhören',lambda key=key:self.exercise_audio(source_key=key),enabled=not self.job and not self.recording)
        o=self.exercise_button(p,o,w,'ex-teach-slow-'+key,'Langsam anhören',lambda key=key:self.exercise_audio(source_key=key,slow=True),enabled=not self.job and not self.recording)
        for title,text in [('Wann benutzt man das?',d['usage']),('Warum diese Form?',d['explain']),('Wort für Wort / Bausteine','; '.join(a+' – '+b for a,b in d['parts'])),('Höflichkeit',d['register']),('Häufige Verwechslung',d['pitfall'])]:o=self.text_block(p,o,w,title,text)
        for j,example in enumerate(d['extra']):o=self.example_block(p,o,w,example,j)
        return o
    def exercise_button(self,p,o,w,identity,label,action,kind='secondary',enabled=True):
        h=max(44,18+20*len(p.wrap(label,w-70,14,True)))
        p.button(identity,(18,o,w-44,h),'',action,kind,size=14,enabled=enabled)
        p.paragraph(29,o+9,label,w-67,14,WHITE,True,lineheight=20)
        return o+h+10
    def draw_exercises(self,s):
        r=self.exercise_round
        if not r:self.draw_lesson(s);return
        stage=r.state['stage'];d=r.answer;t=r.task
        subtitle='Einführung · ohne Bewertung' if stage=='intro' else 'Runde beendet · Pflichtschritte bleiben unverändert' if stage=='complete' else f'Das üben wir noch einmal · {r.state["review_index"]+1}/{len(r.state["review"])}' if stage=='review' else f'Zusatzrunde · Aufgabe {r.state["index"]+1}/{len(r.state["queue"])}'
        self.heading(s,'Abwechslungsreich üben',self.lesson['title']+' · '+subtitle)
        x=294;y=191;w=min(720,(self.W-x-38)*.69);rx=x+w+18;vh=self.H-y-83
        p=self.make_pane(w,16000);o=-self.scroll
        if stage=='intro':
            o=self.text_block(p,o,w,'Erst verstehen, dann ausprobieren','Hier lernst du die benötigten Ausdrücke und Unterschiede vor den neuen Aufgaben. Du kannst anschließend jederzeit Erklären öffnen. Diese Zusatzrunde setzt keine Pflichtschritte auf bestanden.')
            o=self.text_block(p,o,w,'Dein Lernziel',self.lesson.get('goal',''))
            for point in self.lesson.get('study_guide',{}).get('points',[]):o=self.text_block(p,o,w,'Vorwissen und Erklärung',point)
            for key in r.pack['introduced']:o=self.exercise_explain_card(p,o,w,key)
        elif stage=='complete':
            counts={}
            for event in r.state['outcomes']:counts[event['result']]=counts.get(event['result'],0)+1
            labels={'independent':'selbstständig im ersten Versuch','hint':'mit Hinweis','solution':'nach angezeigter Erklärung','corrected':'nach Korrektur','wrong':'noch nicht passend','technical':'technischer Hinweis','unverified':'nicht sicher prüfbar','paused':'pausiert'}
            o=self.text_block(p,o,w,'Deine Übungsrunde','\n'.join(f'{labels.get(k,k)}: {v}' for k,v in counts.items()) or 'Keine bewerteten Versuche.')
            o=self.text_block(p,o,w,'In deinem Tempo','Fehler sind in der vorhandenen Wiederholungsplanung vorgemerkt. Es wurden keine zusätzlichen XP vergeben und keine Pflichtschritte ersetzt.')
        else:
            o=self.text_block(p,o,w,FAMILIES[t['family']],t['prompt'])
            if t['family']=='echo':
                c=self.exercise_card(t['card'])
                h=110+len(p.wrap(c['jp'],w-70,26,True,True))*35+len(p.wrap(c['de'],w-70,15))*22+len(p.wrap(c.get('approx',''),w-70,14))*20
                p.panel((2,o+2,w-12,h),'dark',16);q=o+18
                q+=p.paragraph(23,q,c['jp'],w-60,26,WHITE,True,lineheight=35,jp=True)+8
                q+=p.paragraph(23,q,c['romaji'],w-60,16,MUTED,lineheight=24)+8
                q+=p.paragraph(23,q,c['de'],w-60,15,WHITE,lineheight=22)+10
                p.paragraph(23,q,'Aussprachehilfe · Näherung: '+c.get('approx',''),w-60,14,MUTED,lineheight=20);o+=h+14
            if t['family']=='read':o=self.text_block(p,o,w,'Japanischer Ausgangstext',t['text'])
            if t['family'] in ('hear_gap','choice_gap'):o=self.text_block(p,o,w,'Satz mit Lücke',t['frame'])
            if t['family'] in ('echo','hear_gap','read') or (t['family']=='recall' and d['help']==2):
                o=self.exercise_button(p,o,w,'ex-audio','Normal anhören'+(' · Lesehilfe' if t['family']=='read' else ''),self.exercise_audio,enabled=not self.job and not self.recording)
                o=self.exercise_button(p,o,w,'ex-slow','Langsam anhören',lambda:self.exercise_audio(slow=True),enabled=not self.job and not self.recording)
            if t['family']=='pairs':
                left=order(t['pairs'],t['id']+':left');right=order(t['pairs'],t['id']+':right');cw=(w-54)/2
                for j,(a,b) in enumerate(zip(left,right)):
                    selected=d['left']==a['id'];linked=d['pairs'].get(a['id']);target=next((v['de'] for v in right if v['id']==linked),'noch offen')
                    label=('Anhören · Ton '+str(j+1) if t['mode']=='audio' else a['jp'])+(' · ausgewählt' if selected else '')+'\n→ '+target
                    h=max(72,18+20*max(len(p.wrap(label,cw-24,13)),len(p.wrap(b['de'],cw-24,13))))
                    for side,item,text,xx in [('left',a,label,18),('right',b,b['de'],28+cw)]:
                        p.button('ex-pair-'+side+'-'+item['id'],(xx,o,cw,h),'',lambda side=side,i=item['id']:self.exercise_pair(side,i),'selected' if side=='left' and selected else 'secondary',enabled=not d['success'])
                        p.paragraph(xx+12,o+9,text,cw-24,13,WHITE,lineheight=20)
                    o+=h+10
            elif t['family'] in ('choice_gap','read'):
                for c in order(t['choices'],t['id']):o=self.exercise_button(p,o,w,'ex-choice-'+c['id'],('● ' if d['choice']==c['id'] else '○ ')+c['text'],lambda i=c['id']:self.exercise_set('choice',i),enabled=not d['success'])
                if t['family']=='read' and d['checks']:o=self.text_block(p,o,w,'Belegstelle im Text',t['evidence'])
            elif t['family']=='hear_gap':
                o=self.text_block(p,o,w,'Eingabe in Romaji','Schreibe nur die fehlende Einheit. Lange Vokale bleiben wichtig. Während der Zeichenkomposition wird nicht geprüft.')
                p.panel((18,o,w-44,50),'white');self.entry_target=('exercise-local',(30,o+8,w-70,32));o+=68
            elif t['family'] in ('translate','multi_gap'):
                by={v['id']:v['text'] for v in t['tokens']}
                if t['family']=='multi_gap':
                    frame=' '.join(t['frame']);o=self.text_block(p,o,w,'Satz mit nummerierten Lücken',frame)
                    for j in range(len(t['solutions'][0])):o=self.exercise_button(p,o,w,f'ex-slot-{j}',f'Lücke {j+1}'+(' · aktiv' if d['active']==j else '')+': '+by.get(d['slots'].get(str(j)),'leer'),lambda j=j:self.exercise_set('active',j),'selected' if d['active']==j else 'secondary')
                else:o=self.text_block(p,o,w,'Deine Reihenfolge',' · '.join(by.get(i,'') for i in d['tokens']) or 'Tippe Bausteine an. Erneutes Antippen entfernt sie.')
                for token in order(t['tokens'],t['id']):o=self.exercise_button(p,o,w,'ex-token-'+token['id'],token['text'],lambda i=token['id']:self.exercise_token(i),enabled=not d['success'])
                o=self.exercise_button(p,o,w,'ex-reset','Zurücksetzen',lambda:self.exercise_set('tokens' if t['family']=='translate' else 'slots',[] if t['family']=='translate' else {}),enabled=not d['success'])
            if t['family'] in ('echo','recall'):
                o=self.exercise_button(p,o,w,'ex-record','■ Aufnahme beenden' if self.recording else 'Jetzt sprechen',self.exercise_record,'red',not self.job and not d['success'])
                if self.last_audio is not None:o=self.exercise_button(p,o,w,'ex-own','Eigene Aufnahme anhören',self.play_recording,enabled=not self.job and not self.recording)
                o=self.text_block(p,o,w,'Lokale Aufnahme',self.job or ('Aufnahme läuft · maximal 15 Sekunden' if self.recording else 'Textvergleich, keine Aussprache- oder Tonhöhennote. Kurze Wörter können unsicher erkannt werden.'))
                if d['transcript']:o=self.text_block(p,o,w,'Erkannter Text',d['transcript'])
            else:o=self.exercise_button(p,o,w,'ex-check','Prüfen',self.exercise_check,'blue',not d['success'] and not self.job)
            if d['help_open']:
                o=self.text_block(p,o,w,'Hinweis ohne vollständige Lösung',t['hint'])
                if d['help']<2:o=self.exercise_button(p,o,w,'ex-solution','Vollständig erklären · Lösung zeigen',lambda:self.exercise_help(2))
                else:
                    o=self.text_block(p,o,w,'Nachgeschaut · unterstützter Versuch',t['solution'])
                    if t['family'] in ('pairs','read'):
                        for key in t['prerequisites']:o=self.exercise_explain_card(p,o,w,key)
                    else:o=self.exercise_explain_card(p,o,w,t['card'])
            if d['feedback']:o=self.text_block(p,o,w,'Rückmeldung',d['feedback'])
            if self.speech_error:o=self.text_block(p,o,w,'Technischer Audiohinweis',self.speech_error)
        self.scroll_pane(s,p,x,y,vh,o+self.scroll+12)
        if self.entry_target and self.entry_target[0]=='exercise-local':
            _,(ex,ey,ew,eh)=self.entry_target
            self.entry_target=('exercise',(x+ex,y+ey,ew,eh)) if 0<=ey and ey+eh<=vh else None
        fy=self.H-66
        s.button('ex-back',(x,fy,125,43),'Pause / Zurück',self.exercise_return,size=12)
        if stage in ('main','review'):s.button('ex-help',(x+135,fy,125,43),'Hilfe schließen' if d['help_open'] else 'Erklären / Warum?',self.exercise_help,size=12)
        s.button('ex-next',(x+270,fy,w-283,43),'Einführung gelesen · üben' if stage=='intro' else 'Neue Runde' if stage=='complete' else 'Weiter →',self.exercise_next,'green',size=12,enabled=not self.job and not self.recording and (stage in ('intro','complete') or d['success']))
        self.teacher_stage(s,(rx,179,self.W-rx-17,self.H-196),'Du darfst fragen und nachschauen. Deine Eingabe bleibt dabei erhalten.')

"""V8 lesson UI: pinned pronunciation card, inline recording and guided practice."""
from __future__ import annotations
import math,time
from pathlib import Path
from actors import ActorLayer,ActorSpec
from reactions import ReactionController
from motion import PRESETS,preset_name,preset_strength
from study import PracticeBook,StudySession,PHASES,LABELS,matches_romaji
from ui_renderer import WHITE,MUTED,INK,BLUE,PINK

class LessonMixin:
    def init_v8(self):
        self.book=PracticeBook(self.learning.root,self.learning)
        self.flow=StudySession(self.lesson,self.store,self.book,self.card_index)
        self.inline_speech=False;self.detail_open=False;self.speech_epoch=0
        self.reactions=ReactionController();self.reaction_until=0.;self.reaction='idle';self.actor_specs=[]
        self.pinned_rect=None;self.inline_rect=None;self.exercise_rect=None
        self.actors=ActorLayer(self.root,self.canvas,lambda:self.store.data.get('motion_enabled',True),self.actor_mood,self.actor_feedback,lambda:preset_strength(self.store.data.get('motion_preset')))
    def new_flow(self,index=0,restore=False):
        self.clear_reaction()
        self.flow=StudySession(self.lesson,self.store,self.book,index,restore)
        self.card_index=self.flow.index;self.inline_speech=False;self.detail_open=False
        self.speech_epoch+=1;self.result=None;self.speech_error='';self.last_audio=None
        self.answer=None;self.answer_correct=False;self.scroll=0;self.hide_entry()
        self.flow.snapshot()
    def next_card(self):
        if self.recording or self.job:
            self.notify('Beende zuerst die Aufnahme oder warte auf die Audioauswertung.');return
        if self.flow.phase=='understand' and self.flow.mode=='learn' and not self.flow.success:
            self.flow.mark(True,'Erklärung gelesen.')
        state=self.flow.advance()
        if state=='blocked':self.notify('Löse zuerst diesen Übungsschritt. Hilfe bleibt erlaubt.');return
        if state=='complete':
            self.store.mark_complete(self.lesson['key'],self.lesson.get('xp',20))
            self.store.data.setdefault('lesson_sessions',{}).pop(self.lesson['key'],None)
            self.store.save();self.navigate('complete');self.react('praise','lesson-complete');return
        self.clear_reaction()
        changed=self.card_index!=self.flow.index
        self.card_index=self.flow.index;self.answer=None;self.answer_correct=False
        self.inline_speech=False;self.detail_open=False;self.scroll=0;self.hide_entry()
        if changed:
            self.speech_epoch+=1;self.result=None;self.speech_error='';self.last_audio=None;self.speech_item=None
        self.remember_card();self.request_draw()
    def previous_step(self):
        if self.recording or self.job:return
        self.clear_reaction()
        if self.flow.mode=='recap':self.detail_open=True;self.scroll=0;self.request_draw();return
        i=PHASES.index(self.flow.phase)
        if i>0:self.flow.phase=PHASES[i-1];self.flow.reset_task()
        elif self.flow.index>0:self.flow.index-=1;self.flow.phase='understand';self.flow.reset_task();self.card_index=self.flow.index
        self.inline_speech=False;self.detail_open=False;self.scroll=0;self.hide_entry();self.flow.snapshot();self.request_draw()
    def _react_to_step(self,before_attempts,source):
        # Repeated clicks, hints, unread-audio gates and skipped tasks aren't successes.
        if self.flow.metrics()['attempts']<=before_attempts:return
        if self.flow.skipped:
            self.clear_reaction();return
        self.react('praise' if self.flow.success else 'encourage',source)
    def check_answer(self,value):
        if self.flow.success or (self.flow.phase=='understand' and self.flow.mode=='learn'):return
        before=self.flow.metrics()['attempts']
        self.flow.choose(value);self.answer=value;self.answer_correct=self.flow.success
        self._react_to_step(before,'answer');self.request_draw()
    def react(self,mood,source='answer'):
        if self.reactions.trigger(mood,self.learning.teacher()['id'],source):
            self.reaction=mood;self.reaction_until=self.reactions.started+self.reactions.DURATION
            self.request_draw()
    def clear_reaction(self):
        self.reactions.clear();self.reaction='idle';self.reaction_until=0.
    def actor_feedback(self):
        return self.reactions.sample(self.teacher()['id'],self.recording,self.job)
    def actor_mood(self):return self.actor_feedback().mood
    def add_actor(self,s,path,b,role='teacher',id='teacher'):
        x,y,w,h=b
        if w<10 or h<10 or not Path(path).is_file():return
        self.actor_specs.append(ActorSpec(id,str(path),tuple(s.px(v) for v in b),role,self.actor_mood()))
    def toggle_motion(self):
        self.store.data['motion_enabled']=not self.store.data.get('motion_enabled',True)
        self.store.save();self.request_draw()
    def cycle_motion_preset(self):
        values=list(PRESETS);old=preset_name(self.store.data.get('motion_preset'))
        self.store.data['motion_preset']=values[(values.index(old)+1)%len(values)]
        self.store.save();self.request_draw()
    def speak_card(self,c,lesson=None):
        if self.view=='lesson':
            if self.inline_speech:
                if self.recording:self.stop_capture(False)
                self.inline_speech=False
            else:
                item=self.learning.speech_target(c,lesson or self.lesson)
                if (self.speech_item or {}).get('target')!=item['target']:
                    self.speech_epoch+=1;self.result=None;self.last_audio=None;self.speech_error=''
                self.speech_item=item;self.inline_speech=True
            self.scroll=0;self.hide_entry();self.request_draw();return
        self.speech_epoch+=1;self.speech_item=self.learning.speech_target(c,lesson or self.lesson)
        self.speech_item['approx']=c.get('approx','');self.speech_item['note']=c.get('note','')
        self.speech_return=self.view;self.result=None;self.speech_error='';self.last_audio=None;self.navigate('speaking')
    def skip_speaking(self):
        self.clear_reaction()
        if self.recording:self.stop_capture(False)
        self.flow.metrics()['speech_skips']+=1;self.flow.snapshot()
        self.inline_speech=False;self.scroll=0;self.notify('Sprechübung ausgelassen. Kein Fehler und kein vorgetäuschter Erfolg.');self.request_draw()
    def listen_exercise(self):
        if self.recording:return
        flow=self.flow;card=flow.listen_card;t=self.learning.teacher()
        speed=float(self.store.data.get('tts_speed',1))*t['speed']
        def finished(_):
            if self.flow is flow and flow.phase=='listen':flow.audio_seen=True;flow.feedback='Hörbeispiel abgespielt. Jetzt kannst du zuordnen.'
        self.run_worker('Hörbeispiel',lambda:self.engine.speak(card['jp'],speed,int(t['speaker_id'])),finished)
    def skip_listening(self):
        self.flow.audio_skipped=True;self.flow.feedback='Ohne Ton: Diese Aufgabe zählt als Leseübung, nicht als bestandener Hörtest.';self.request_draw()
    def learn_text_changed(self,e=None):
        if self.entry and self.entry_mode=='study':self.flow.input_text=self.entry.get()
    def check_learn_text(self):
        if not self.entry or self.entry_mode!='study' or self.flow.success:return
        before=self.flow.metrics()['attempts'];text=self.entry.get()
        if self.flow.phase=='listen':
            if not(self.flow.audio_seen or self.flow.audio_skipped):self.flow.feedback='Zuerst anhören oder bewusst „Ohne Ton“ wählen.'
            else:self.flow.mark(matches_romaji(text,self.flow.listen_card['romaji']),
                    'Passende Lesung.' if matches_romaji(text,self.flow.listen_card['romaji']) else 'Vergleiche die Lesung noch einmal.',skipped=self.flow.audio_skipped)
        else:self.flow.check_write(text)
        self._react_to_step(before,'write');self.request_draw()
    def pick_block(self,index):
        if self.flow.success:return
        if index not in self.flow.tokens:self.flow.tokens.append(index);self.request_draw()
    def clear_blocks(self):
        if not self.flow.success:self.flow.tokens=[];self.flow.feedback='';self.request_draw()
    def check_blocks(self):
        if self.flow.success:return
        before=self.flow.metrics()['attempts'];self.flow.check_build()
        self._react_to_step(before,'build');self.request_draw()
    def show_explanation(self):
        self.detail_open=not self.detail_open;self.flow.hint_used=True;self.scroll=0;self.request_draw()
    def pinned_text_layout(self,s,w,c):
        """Measure full lesson text; never cut a new sentence to an ellipsis."""
        left_w=w-max(221,w*.365)-74;right_w=max(221,w*.365)-30
        def measured(text,width,start,minimum,max_lines,bold=False,jp=False):
            size=start
            while size>minimum and len(s.wrap(text,width,size,bold,jp))>max_lines:size-=1
            lines=s.wrap(text,width,size,bold,jp)
            return size,len(lines)*(size*1.25),len(lines)
        j=measured(c['jp'],left_w,37,21,2,True,True)
        r=measured(c['romaji'],left_w,18,15,2)
        d=measured('Bedeutung: '+c['de'],left_w,14.5,13,3,True)
        a=measured(c.get('approx') or c['romaji'],right_w,15,12,3,True)
        # Keep pronunciation and meaning fully visible even with the recorder open.
        white=max(164,17+j[1]+8+r[1]+12+d[1]+16,52+a[1]+14+33+16)
        return {'jp':j,'romaji':r,'de':d,'approx':a,'white_h':white}
    def draw_pinned_word(self,s,x,y,w,h,c):
        self.pinned_rect=(x,y,w-10,h)
        s.panel((x,y,w-10,h));s.icon('book',x+21,y+16,26);s.text(x+61,y+19,'Neues Wort' if self.flow.mode=='learn' else 'Dein Wiederholungswort',19,WHITE,True)
        white_h=h-108;top=y+50;ix=x+w-max(221,w*.365)-26;iw=x+w-29-ix
        s.panel((x+16,top,w-42,white_h),'white',16,False);s.panel((ix,top+11,iw,white_h-22),'info',12,False)
        layout=self.pinned_text_layout(s,w,c);yy=top+17
        size=layout['jp'][0]
        yy+=s.paragraph(x+35,yy,c['jp'],ix-x-48,size,INK,True,lineheight=size*1.25,jp=True)+8
        size=layout['romaji'][0]
        yy+=s.paragraph(x+35,yy,c['romaji'],ix-x-48,size,'#56749a',lineheight=size*1.25)+12
        size=layout['de'][0]
        s.paragraph(x+35,yy,'Bedeutung: '+c['de'],ix-x-48,size,INK,True,lineheight=size*1.25)
        s.text(ix+14,top+24,'Aussprachehilfe',12,INK,True)
        size=layout['approx'][0]
        ah=s.paragraph(ix+14,top+52,c.get('approx') or c['romaji'],iw-27,size,'#20579d',True,lineheight=size*1.25)
        ny=top+52+ah+14
        s.icon('info',ix+14,ny,17,'#168cf2')
        s.paragraph(ix+40,ny,c.get('note') or 'Hör zu und sprich danach nach.',iw-54,11,'#3c5c80',max_lines=max(2,int((top+white_h-ny-13)/15)),lineheight=15)
        bw=(w-60)/3;by=y+h-48
        s.button('listen',(x+16,by,bw,36),'Normal anhören',lambda:self.speak(c['jp']),'blue','speaker',12,enabled=not self.recording and not self.job)
        s.button('slow',(x+24+bw,by,bw,36),'Langsam anhören',lambda:self.speak(c['jp'],True),'secondary','turtle',12,enabled=not self.recording and not self.job)
        s.button('speak',(x+32+2*bw,by,bw,36),'Sprechfeld zu' if self.inline_speech else 'Jetzt sprechen',lambda:self.speak_card(c),'red','mic',12,enabled=not self.job)
    def draw_inline_recording(self,s,x,y,w,h):
        self.inline_rect=(x,y,w-10,h)
        s.panel((x,y,w-10,h));s.icon('mic',x+18,y+13,22,'#ff99bb');s.text(x+53,y+17,'Hier sprechen · Lernkarte bleibt sichtbar',16,WHITE,True,width=w-90)
        s.icon('close',x+w-43,y+15,18,MUTED);s.register('inline-close',(x+w-48,y+10,29,29),lambda:self.speak_card(self.current_card()))
        bw=(w-55)*.59
        s.button('record',(x+16,y+45,bw,40),'Stoppen & auswerten' if self.recording else 'Aufnahme starten',self.toggle_recording,'red','pause' if self.recording else 'mic',13,enabled=not self.job)
        s.button('play-own',(x+25+bw,y+45,w-51-bw,40),'Deine Aufnahme',self.play_recording,'secondary','headphones',12,enabled=self.last_audio is not None and not self.recording and not self.job)
        label=f'Aufnahme: {int(time.monotonic()-self.record_started)} / 15 s · Leertaste stoppt' if self.recording else self.job+' …' if self.job else 'Lokal auf deinem Computer · Leertaste startet und stoppt'
        s.text(x+19,y+96,label,11.5,MUTED,width=w-46);s.progress((x+18,y+117,w-48,4),self.record_level if self.recording else 0)
        feedback='Noch keine Aufnahme. Du kannst so oft üben, wie du möchtest.'
        color=INK
        if self.speech_error:feedback='Audio-Hinweis: '+self.speech_error
        elif self.result:
            r=self.result;reliable=r.reliable and (not r.quality or r.quality.status!='bad')
            feedback=('Erkannt: '+(r.heard or 'kein Text')+' · '+str(r.score)+' % Textabgleich') if reliable else 'Aufnahme nicht sicher auswertbar. Kein Aussprachefehler daraus abgeleitet.'
        box_h=max(33,h-164);s.panel((x+16,y+130,w-42,box_h),'white',10,False)
        s.paragraph(x+28,y+139,feedback,w-66,12.5,color,max_lines=2,lineheight=17)
        s.text(x+18,y+h-23,'Textabgleich, keine Laut-/Akzentnote.',10.5,MUTED,width=w-207)
        s.text(x+w-28,y+h-23,'Ohne Mikrofon weiter',11,'#95cffa',True,align='right')
        s.register('speech-skip',(x+w-202,y+h-31,180,24),self.skip_speaking)
    def draw_lesson(self,s):
        if self.flow.lesson['key']!=self.lesson['key']:self.new_flow(self.card_index)
        f=self.flow;c=self.current_card();step=PHASES.index(f.phase)+1
        sub=(f'Wiederholung {f.recap_passed+1} / {f.recap_total} · Bekannte Wörter, neu gemischt' if f.mode=='recap' else
             f'Karte {self.card_index+1} / {len(self.lesson["cards"])} · Schritt {step} / 6: {LABELS[f.phase]} · Kein Zeitdruck')
        self.heading(s,'Lektion – '+self.lesson['title'],sub,True)
        x=294;y=193;lw=min(682,(self.W-x-36)*.615);rx=x+lw+22
        value=(f.recap_passed/max(1,f.recap_total)) if f.mode=='recap' else (self.card_index+(step-1)/6)/len(self.lesson['cards'])
        s.progress((x,175,lw-12,7),value)
        word_h=max(304 if self.H>=960 else 280,108+self.pinned_text_layout(s,lw,c)['white_h'])
        self.draw_pinned_word(s,x,y,lw,word_h,c);by=y+word_h+12;self.inline_rect=None
        if self.inline_speech:
            ih=209 if self.H>=930 else 197
            self.draw_inline_recording(s,x,by,lw,ih);by+=ih+12
        fy=self.H-64
        # Fixed card & recorder stay above a separate scrolling practice area.
        tabs_y=by;cw=(lw-18)/6
        if fy-by>100:
            for i,phase in enumerate(PHASES):
                col='#0e8fda' if phase==f.phase and f.mode=='learn' else '#18344f'
                s.fill((x+i*cw,tabs_y,cw-5,28),col,8)
                s.text(x+i*cw+(cw-5)/2,tabs_y+8,LABELS[phase],10.5,WHITE if phase==f.phase else MUTED,phase==f.phase,align='center')
            by+=40
        vh=max(0,fy-by-12);self.exercise_rect=(x,by,lw,vh)
        if vh>=72:
            p=self.make_pane(lw,max(vh,1800));o=-self.scroll
            total=self.draw_study_content(p,o,lw)
            self.scroll_pane(s,p,x,by,vh,total+self.scroll+14)
            if self.entry_target and self.entry_target[0]=='study-local':
                _,(ex,ey,ew,eh)=self.entry_target
                if 0<=ey and ey+eh<=vh:self.entry_target=('study',(x+ex,by+ey,ew,eh))
                else:self.entry_target=None
        else:
            self.max_scroll=0
            if fy-by>25:s.text(x+9,by+4,'Schließe das Sprechfeld, um die Übungen wieder zu sehen.',12,MUTED,width=lw-25)
        ready=f.success or f.phase=='understand' and f.mode=='learn'
        label='Weiter  →'
        if f.mode=='recap':label='Lektion abschließen  →' if len(f.recap)==1 else 'Nächste Wiederholung  →'
        elif f.phase=='apply' and self.card_index==len(self.lesson['cards'])-1:label='Zur Wiederholungsrunde  →'
        elif f.phase=='understand':label='Verstanden · jetzt üben  →'
        s.button('step-back',(x,fy,88,43),'‹ Zurück',self.previous_step,size=12,enabled=not self.recording and not self.job)
        s.button('learn-help',(x+98,fy,109,43),'Erklärung',self.show_explanation,size=12,enabled=not self.recording)
        s.button('next',(x+217,fy,lw-230,43),label,self.next_card,'green',size=14,enabled=ready and not self.recording and not self.job)
        message=('Ich höre zu. Aussprachehilfe und Wort bleiben direkt neben dir.' if self.recording else
                 'Du darfst nachschauen. Kleine Wiederholungen sind Teil des Lernens.' if f.mode=='recap' else
                 'Erst verstehen. Dann in kleinen Schritten üben – ganz in deinem Tempo.')
        self.teacher_stage(s,(rx,166,self.W-rx-17,self.H-182),message)
    def text_block(self,p,o,w,title,text,kind='white'):
        if not text:return o
        lines=p.wrap(text,w-66,15);height=61+len(lines)*22
        p.panel((2,o+2,w-12,height),'dark',16);p.text(23,o+19,title,18,WHITE,True,width=w-50)
        p.paragraph(23,o+53,text,w-56,15,MUTED,lineheight=22)
        return o+height+14
    def example_block(self,p,o,w,example,index=0):
        # Measure first; long Japanese sentences are wrapped, never silently cut.
        jp,roma,de=example;lines=p.wrap(jp,w-95,24,True,True);rl=p.wrap(roma,w-79,14);dl=p.wrap(de,w-61,14,True)
        inner=18+len(lines)*31+len(rl)*20+len(dl)*20+12;h=inner+61
        p.panel((2,o+2,w-12,h));p.icon('chat',23,o+18,23);p.text(60,o+21,'Beispielsatz',18,WHITE,True)
        p.panel((17,o+53,w-42,inner),'white',14,False);q=o+64
        q+=p.paragraph(32,q,jp,w-95,24,INK,True,lineheight=31,jp=True)
        q+=p.paragraph(32,q+3,roma,w-79,14,'#557399',lineheight=20)+6
        p.paragraph(32,q,de,w-70,14,INK,True,lineheight=20)
        p.icon('speaker',w-64,o+65,24,'#1089ef');p.register('example:'+str(index),(w-75,o+56,42,42),lambda jp=jp:self.speak(jp))
        return o+h+15
    def draw_explanation(self,p,o,w):
        f=self.flow;c=f.card;profile=self.book.profile(c,self.lesson)
        if f.index==0:o=self.text_block(p,o,w,'Ziel dieser Lektion',self.book.intro(self.lesson))
        o=self.text_block(p,o,w,'Wann benutzt du das? · '+profile['kind'],profile['usage'])
        o=self.text_block(p,o,w,'So funktioniert es',profile['explain'])
        if profile['register']:o=self.text_block(p,o,w,'Höflichkeit & Situation',profile['register'])
        if profile['parts']:
            h=56+len(profile['parts'])*45;p.panel((2,o+2,w-12,h));p.text(23,o+21,'Wort für Wort / Schreibbausteine',18,WHITE,True)
            q=o+53
            for jp,de in profile['parts']:
                p.panel((17,q,w-42,38),'white',9,False);p.text(29,q+9,jp,18,INK,True,width=min(164,w*.29));p.text(36+min(164,w*.29),q+11,de,13,INK,width=w-91-min(164,w*.29));q+=45
            o+=h+15
        o=self.text_block(p,o,w,'Darauf solltest du achten',profile['pitfall'])
        examples=profile['extra'] or [[v for v in self.learning.examples(c).values()]]
        for i,ex in enumerate(examples):o=self.example_block(p,o,w,ex,i)
        return o
    def draw_options(self,p,o,w,labels):
        opts,_=self.flow.answers();colw=(w-50)/2
        for row in range(math.ceil(len(opts)/2)):
            values=opts[row*2:row*2+2];texts=[self.book.option_label(v) if labels else v for v in values]
            h=max(48,max(len(p.wrap(text,colw-24,13,True))*18+15 for text in texts))
            for j,(v,text) in enumerate(zip(values,texts)):
                i=row*2+j;kind='selected' if self.flow.chosen==v and self.flow.success else 'wrong' if self.flow.chosen==v else 'answer'
                # Surface.button supports two lines; use an independently measured label
                # for Japanese choice + reading + meaning so no unknown choice is hidden.
                p.button('answer:'+str(i),(18+j*(colw+8),o,colw,h),'',lambda v=v:self.check_answer(v),kind,size=13,enabled=not self.flow.success)
                p.paragraph(29+j*(colw+8),o+8,text,colw-23,13,WHITE,True,lineheight=18)
            o+=h+10
        return o
    def study_input(self,p,o,w,label):
        p.text(22,o,label,15,MUTED,True);o+=29;p.panel((17,o,w-42,49),'white',12,False)
        self.entry_target=('study-local',(30,o+9,w-70,32));o+=62
        p.button('study-check',(18,o,w-44,41),'Antwort prüfen',self.check_learn_text,'blue',size=14,enabled=not self.flow.success)
        return o+58
    def _draw_study_content(self,p,o,w):
        f=self.flow;c=f.card;profile=self.book.profile(c,self.lesson)
        if f.phase=='understand' and f.mode=='learn':return self.draw_explanation(p,o,w)
        if self.detail_open:
            o=self.draw_explanation(p,o,w)
        title='Abschlussrunde · Welche Bedeutung passt?' if f.mode=='recap' else {
            'meaning':'Übung · Welche Bedeutung passt?', 'listen':'Hörübung · Hören und zuordnen',
            'build':'Übung · Bausteine zusammensetzen','write':'Übung · Die Lesung schreiben',
            'apply':'Lesen · Den Inhalt verstehen' if profile.get('kind')=='Leseverständnis' else 'Anwenden · Die passende Situation'}[f.phase]
        p.panel((2,o+2,w-12,55));p.icon('chat',23,o+17,24);p.text(59,o+20,title,17,WHITE,True,width=w-85);o+=70
        if f.mode=='recap' or f.phase=='meaning':
            o=self.draw_options(p,o,w,False)
            if f.mode!='recap':
                ex=self.learning.examples(c);o=self.example_block(p,o+7,w,[ex['jp'],ex['romaji'],ex['de']])
        elif f.phase=='listen':
            text='Höre eines der bisher eingeführten Wörter aus dieser Lektion. Die Lernhilfe oben darf sichtbar bleiben. Das Hörwort kann ein früheres Wort sein.'
            o+=p.paragraph(23,o,text,w-54,14,MUTED,lineheight=21)+15
            bw=(w-52)*.65;p.button('exercise-audio',(18,o,bw,43),'Hörbeispiel abspielen',self.listen_exercise,'blue','speaker',13,enabled=not self.job and not self.recording)
            p.button('exercise-skip',(28+bw,o,w-53-bw,43),'Ohne Ton',self.skip_listening,size=12,enabled=not self.job);o+=60
            opts,_=f.answers()
            if len(opts)==1:o=self.study_input(p,o,w,'Welchen Laut / welche Lesung hast du gehört?')
            else:o=self.draw_options(p,o,w,False)
        elif f.phase=='build':
            parts,kind=self.book.blocks(c,self.lesson)
            if parts:
                o+=p.paragraph(23,o,'Klicke die Bausteine in der richtigen Reihenfolge an. Die Lernkarte oben zeigt dir die Vorlage. Das ist eine Schreibübung, keine Lautanalyse.',w-57,14,MUTED,lineheight=21)+16
                chosen='  ·  '.join(parts[i] for i in f.tokens) or 'Deine Reihenfolge …'
                sh=max(59,len(p.wrap(chosen,w-72,20,True))*29+23);p.panel((17,o,w-42,sh),'white',12,False);p.paragraph(29,o+13,chosen,w-71,20,INK,True,lineheight=29);o+=sh+14
                import random
                order=list(range(len(parts)));random.Random(f.card_key+':blocks').shuffle(order)
                if order==list(range(len(parts))):order=order[1:]+order[:1]
                cols=min(4,len(parts));cw=(w-44-(cols-1)*8)/cols
                for n,i in enumerate(order):
                    p.button('block:'+str(i),(18+(n%cols)*(cw+8),o+(n//cols)*51,cw,43),parts[i],lambda i=i:self.pick_block(i),'secondary',size=17,enabled=i not in f.tokens and not f.success)
                o+=math.ceil(len(parts)/cols)*51+4
                p.button('build-check',(18,o,(w-52)*.64,42),'Reihenfolge prüfen',self.check_blocks,'blue',size=14,enabled=not f.success)
                p.button('build-reset',(28+(w-52)*.64,o,(w-52)*.36,42),'Zurücksetzen',self.clear_blocks,size=12,enabled=not f.success);o+=59
            else:
                o+=p.paragraph(23,o,'Dieses Zeichen / Muster braucht keine künstliche Zerlegung. Wähle stattdessen seine Lesung.',w-53,14,MUTED,lineheight=21)+14
                o=self.draw_options(p,o,w,False)
        elif f.phase=='write':
            o+=p.paragraph(23,o,'Schreibe die Romaji-Lesung mit deiner normalen Tastatur. Anfangs darfst du oben ablesen; später kannst du es aus dem Gedächtnis versuchen.',w-56,14,MUTED,lineheight=21)+13
            o=self.study_input(p,o,w,'Deine Romaji-Antwort')
            o+=p.paragraph(23,o,'Tastaturhilfe: ō = ou oder oo, ū = uu, ā = aa. Leerzeichen, Bindestriche und Satzzeichen sind nicht entscheidend. Vokallänge bleibt wichtig.',w-56,12,MUTED,lineheight=19)+18
        elif f.phase=='apply':
            o+=p.paragraph(23,o,profile['scenario']['question'],w-58,17,WHITE,True,lineheight=25)+19
            o=self.draw_options(p,o,w,True)
        if f.feedback:
            col='#96edbd' if f.success else '#ffd6a3';o=self.text_block(p,o+5,w,'Gut gemacht' if f.success and not f.skipped else 'Hinweis',f.feedback)
        if f.success:
            p.text(23,o,'Weiter geht es unten mit dem grünen Button.',13,'#9ae0bd',True,width=w-56);o+=34
        return o

    def draw_study_content(self,p,o,w):
        if self.flow.phase=='understand' and self.flow.mode=='learn':
            return self._draw_study_content(p,o,w)
        # A dark opaque practice surface stays behind every instruction and field.
        # Draw it after measuring content, then composite the real controls above it.
        content=self.make_pane(p.width,p.height)
        end=self._draw_study_content(content,o,w)
        p.panel((2,o+2,w-12,max(330,end-o+16)),'solid',18)
        p.compose(content,0,0,(p.width,p.height))
        return max(end,o+330)+10

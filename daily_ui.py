"""Native daily-practice view; leaves six-step course sessions untouched."""
from adaptive import daily_plan, finish_daily, LABELS
from study import matches_romaji
from ui_renderer import WHITE, MUTED, BLUE
import random


class DailyMixin:
    def daily_plan(self):
        lesson=self.learning.next_lesson();cursor=self.store.data.get('last_lesson',{})
        start=cursor.get('card',0) if cursor.get('key')==lesson['key'] else 0
        upcoming=[] if lesson['key'] in self.store.data['completed'] else [c for c in self.learning.cards if c['lesson_key']==lesson['key']][start:start+2]
        p=daily_plan(self.store.data,self.learning.cards,self.learning.available_cards(),upcoming)
        self.store.save();return p

    def daily_pick(self):
        p=self.daily_plan()
        self.daily_task=next((t for t in p['tasks'] if t['id'] not in p['done']),None)
        self.daily_feedback='';self.daily_success=False;self.daily_help=False;self.daily_help_used=False;self.daily_heard=False;self.daily_input=''
        self.scroll=0;self.hide_entry()

    def daily_card(self):
        return next(c for c in self.learning.cards if c['key']==self.daily_task['card'])

    def daily_options(self):
        c=self.daily_card();lesson=self.learning.by_key[c['lesson_key']]
        profile=self.book.profile(c,lesson)
        correct=profile['scenario']['correct'] if self.daily_task['skill']=='use' else c['de']
        pool=profile['scenario']['wrong'] if self.daily_task['skill']=='use' else [x['de'] for x in lesson['cards']]
        pool=list(dict.fromkeys(v for v in pool if v!=correct));r=random.Random(self.daily_task['id']);r.shuffle(pool)
        options=[correct]+pool[:3];r.shuffle(options);return options,correct

    def daily_mark(self,ok,message,assisted=False):
        if self.daily_success:return
        self.daily_success=finish_daily(self.store.data,self.daily_task,ok,assisted or self.daily_help_used)
        if not ok:self.daily_help_used=True
        self.daily_feedback=message;self.store.touch_day();self.store.save();self.request_draw()

    def daily_choose(self,value):
        skill=self.daily_task['skill'];c=self.daily_card();lesson=self.learning.by_key[c['lesson_key']]
        if skill=='listen' and not self.daily_heard:self.daily_feedback='Höre das Beispiel zuerst vollständig an.';self.request_draw();return
        options,correct=self.daily_options()
        if value not in options:return
        other=next((x for x in lesson['cards'] if x['de']==value),None)
        reason=(f'Deine Auswahl gehört zu {other["jp"]} ({other["romaji"]}). ' if other else '')+self.book.profile(c,lesson)['explain']
        self.daily_mark(value==correct,'Richtig. Diese Fähigkeit wird später gezielt wiederholt.' if value==correct else reason+' Versuche es noch einmal.')

    def daily_write(self):
        if self.entry:self.daily_input=self.entry.get()
        c=self.daily_card();ok=any(matches_romaji(self.daily_input,x) for x in [c['romaji']]+c.get('romaji_aliases',[]))
        self.daily_mark(ok,'Die Lesung passt.' if ok else self.book.profile(c,self.learning.by_key[c['lesson_key']])['pitfall'])

    def daily_listen(self,slow=False):
        if self.recording or self.job:return
        t=self.learning.teacher();speed=self.store.data['tts_speed']*t['speed']*(.72 if slow else 1);identity=self.daily_task['id']
        def done(_):
            if self.view=='daily' and self.daily_task and self.daily_task['id']==identity:
                self.daily_heard=True;self.daily_feedback='Vorlage gehört. Du bist dran.';self.request_draw()
        self.run_worker('Vorlesen',lambda:self.engine.speak(self.daily_card()['jp'],speed,int(t['speaker_id'])),done)

    def daily_toggle_help(self):
        if self.entry:self.daily_input=self.entry.get()
        self.daily_help=not self.daily_help;self.daily_help_used|=self.daily_help;self.request_draw()

    def draw_daily(self,s):
        p=self.daily_plan()
        if not hasattr(self,'daily_task') or self.daily_task and self.daily_task not in p['tasks']:self.daily_pick()
        task=self.daily_task;x=294;y=181;w=self.W-x-25
        self.heading(s,'Heute für dich',f"{len(p['done'])} / {len(p['tasks'])} kleine Aufgaben · Lesen, Hören und Sprechen getrennt üben")
        if not task:
            s.panel((x,y,w,260));s.text(x+24,y+25,'Deine Runde ist geschafft.' if p['tasks'] else 'Heute ist nichts fällig.',25,WHITE,True)
            s.paragraph(x+24,y+75,'Der Kurs bleibt an seiner bisherigen Stelle. Du kannst weiterlernen oder eine Hörsituation üben.',w-48,18)
            s.button('daily-course',(x+24,y+160,w-48,48),'Im Kurs weiterlernen →',self.resume,'green')
            s.button('daily-practice',(x+24,y+216,w-48,40),'Hörsituationen und Zeichen',lambda:self.navigate('practice_lab'))
            return
        c=self.daily_card();skill=task['skill'];profile=self.book.profile(c,self.learning.by_key[c['lesson_key']]);vh=self.H-y-85
        s.panel((x,y,w,vh),'solid',16)
        panel=self.make_pane(w,3000);o=-self.scroll+16
        cue={'intro':'Lerne Bedeutung und Verwendung kennen.','read':'Welche Bedeutung passt?','listen':'Höre zu. Welche Bedeutung passt?','write':'Schreibe die Lesung in Romaji.','speak':'Höre die Vorlage und sprich sie nach.','use':profile['scenario']['question']}[skill]
        o+=panel.paragraph(18,o,LABELS[skill]+' · '+cue,w-36,22,WHITE,True)+15
        if skill in ('intro','speak','read'):
            o+=panel.paragraph(18,o,c['jp'],w-36,32,WHITE,True,jp=True)+10
        if skill in ('intro','speak'):
            o+=panel.paragraph(18,o,c['romaji']+'\n'+c['de'],w-36,19)+15
        if skill=='write':o+=panel.paragraph(18,o,c['de'],w-36,21)+15
        if skill in ('intro','speak','listen'):
            panel.button('daily-audio',(18,o,(w-48)/2,44),'Anhören',self.daily_listen,'blue',enabled=not self.job)
            panel.button('daily-slow',(30+(w-48)/2,o,(w-48)/2,44),'Langsam',lambda:self.daily_listen(True),enabled=not self.job);o+=58
        if skill=='intro':
            o+=panel.paragraph(18,o,profile['usage']+'\n'+profile['explain'],w-36,18,lineheight=25)+16
        elif skill=='speak':
            panel.button('daily-speak',(18,o,w-36,46),'Freiwillig nachsprechen',lambda:self.speak_card(c,self.learning.by_key[c['lesson_key']]),'red');o+=58
            panel.button('daily-defer',(18,o,w-36,44),'Sprechen später üben',lambda:self.daily_mark(True,'Für später vorgemerkt. Keine bestandene Sprechprüfung.',True));o+=58
        elif skill=='write':
            if o>=0 and o+46<=vh:self.entry_target=('daily',(x+18,y+o,w-36,46))
            panel.panel((18,o,w-36,46),'white');o+=60
        else:
            for i,value in enumerate(self.daily_options()[0]):
                height=max(48,20+panel.paragraph(18,2800,value,w-58,17,lineheight=23))
                panel.button('daily-choice:'+str(i),(18,o,w-36,height),value,lambda v=value:self.daily_choose(v),size=16,enabled=not self.daily_success);o+=height+10
        if skill!='intro':
            panel.button('daily-help',(18,o,w-36,42),'Hinweis und Erklärung',self.daily_toggle_help);o+=54
        if self.daily_help:
            o+=panel.paragraph(18,o,f"{c['jp']} · {c['romaji']}\n{c['de']}\n{profile['explain']}\nAntworten nach dieser Hilfe werden als unterstützt gespeichert.",w-36,17,MUTED,lineheight=24)+15
        if self.daily_feedback:o+=panel.paragraph(18,o,self.daily_feedback,w-36,17,BLUE,lineheight=24)+20
        self.scroll_pane(s,panel,x,y,vh,o+self.scroll)
        if self.daily_success:s.button('daily-next',(x,self.H-65,w,46),'Weiter →',lambda:(self.daily_pick(),self.request_draw()),'green')
        elif skill=='intro':s.button('daily-intro',(x,self.H-65,w,46),'Karte kennengelernt →',lambda:self.daily_mark(True,'Kennengelernt. Keine Kurslektion übersprungen.'),'green')
        elif skill=='write':s.button('daily-check',(x,self.H-65,w,46),'Überprüfen →',self.daily_write,'green')

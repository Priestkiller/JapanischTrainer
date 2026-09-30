"""Authored listening situations and manual shape practice; no stroke grading."""
import json
from datetime import datetime,timezone
from adaptive import record_attempt
from ui_renderer import WHITE,MUTED,BLUE


class PracticeMixin:
    def practice_data(self):
        if not hasattr(self,'practice_content'):
            self.practice_content=json.loads((self.learning.root/'data/practice_content.json').read_text('utf8'))
        return self.practice_content

    def practice_known(self,key):
        return key in self.store.data['completed'] or all(f'{key}:{i}' in self.store.data['adaptive']['introduced'] for i in range(len(self.learning.by_key[key]['cards'])))

    def practice_open(self,story):
        if not self.practice_known(story['lesson']):return
        self.practice_story=story;self.practice_index=0;self.practice_heard=False;self.practice_help=False;self.practice_help_used=False;self.practice_success=False;self.practice_feedback='';self.scroll=0;self.request_draw()

    def practice_listen(self,slow=False):
        if self.job or self.recording:return
        story=self.practice_story;t=self.learning.teacher();speed=self.store.data['tts_speed']*t['speed']*(.72 if slow else 1)
        text=' '.join(c['jp'].rstrip('。')+'。' for c in self.learning.by_key[story['lesson']]['cards'])
        def done(_):
            if self.view=='practice_lab' and self.practice_story==story:self.practice_heard=True;self.practice_feedback='Dialog gehört. Du bist dran.';self.request_draw()
        self.run_worker('Vorlesen',lambda:self.engine.speak(text,speed,int(t['speaker_id'])),done)

    def practice_choose(self,value):
        if self.practice_success:return
        if not self.practice_heard and not self.practice_help:self.practice_feedback='Höre den Dialog vollständig oder öffne bewusst die Lesehilfe.';self.request_draw();return
        story=self.practice_story;q=story['questions'][self.practice_index];c=self.learning.by_key[story['lesson']]['cards'][q['evidence']]
        if value not in q['options']:return
        ok=value==q['correct'];record_attempt(self.store.data,f"{story['lesson']}:{q['evidence']}",'listen' if self.practice_heard and not self.practice_help_used else 'read',ok,self.practice_help_used)
        self.practice_success=ok;self.practice_feedback='Richtig.' if ok else f'Achte auf {c["jp"]} ({c["romaji"]}): {c["de"]}.'
        if not ok:self.practice_help_used=True
        self.store.save();self.request_draw()

    def practice_next(self):
        if not self.practice_success:return
        self.practice_index+=1;self.practice_success=False;self.practice_feedback='';self.scroll=0
        if self.practice_index==len(self.practice_story['questions']):
            old=self.store.data['adaptive']['milestones'].get(self.practice_story['id'],{})
            self.store.data['adaptive']['milestones'][self.practice_story['id']]={'mode':'listening' if old.get('mode')=='listening' or not self.practice_help_used else 'supported','completedAt':datetime.now(timezone.utc).isoformat()};self.store.touch_day();self.store.save()
        self.request_draw()

    def practice_toggle(self):
        self.practice_help=not self.practice_help;self.practice_help_used|=self.practice_help;self.request_draw()

    def practice_back(self):
        self.practice_story=None;self.trace_card=None;self.scroll=0;self.request_draw()

    def trace_open(self,card):
        self.trace_card=card;self.trace_strokes=[];self.trace_guide=True;self.request_draw()

    def trace_event(self,event,start=False):
        if self.view!='practice_lab' or not getattr(self,'trace_card',None):return False
        x,y,w,h=self.trace_box;px=event.x/self.render_scale;py=event.y/self.render_scale
        if not(x<=px<=x+w and y<=py<=y+h):return False
        if start:self.trace_strokes.append([])
        if not self.trace_strokes:return False
        self.trace_strokes[-1].append(((px-x)/w,(py-y)/h));self.request_draw();return True

    def draw_practice_lab(self,s):
        self.heading(s,'Hörsituationen und Zeichen','Bekannten Wortschatz anwenden · Formen selbst vergleichen')
        x=294;y=183;w=self.W-x-25;story=getattr(self,'practice_story',None);trace=getattr(self,'trace_card',None)
        s.panel((x,y,w,self.H-y-85),'solid',16)
        if trace:
            side=min(330,self.H-300);self.trace_box=(x+24,y+45,side,side);s.text(x+24,y,trace['jp']+' · '+trace['romaji'],26,WHITE,True)
            s.panel(self.trace_box,'white');bx,by,bw,bh=self.trace_box
            if self.trace_guide:s.text(bx+bw/2,by+25,trace['jp'],side*.7,'#c1d2e0',width=bw,align='center',jp=True)
            for stroke in self.trace_strokes:
                if len(stroke)>1:s.draw.line([(s.px(bx+px*bw),s.px(by+py*bh)) for px,py in stroke],fill='#1677b1',width=max(2,s.px(4)),joint='curve')
            rx=x+side+45;rw=w-side-62
            s.paragraph(rx,y+45,self.practice_data()['trace_note'],rw,18,lineheight=26)
            s.button('trace-guide',(rx,y+185,rw,44),'Vorlage aus / ein',lambda:(setattr(self,'trace_guide',not self.trace_guide),self.request_draw()))
            s.button('trace-clear',(rx,y+243,rw,44),'Neu zeichnen',lambda:(setattr(self,'trace_strokes',[]),self.request_draw()))
            s.button('practice-back',(x,self.H-65,w,44),'Zurück',self.practice_back);return
        p=self.make_pane(w,4000);o=-self.scroll+14
        if not story:
            for item in self.practice_data()['stories']:
                known=self.practice_known(item['lesson']);old=self.store.data['adaptive']['milestones'].get(item['id'],{})
                suffix=' · Durch Hörfragen belegt' if old.get('mode')=='listening' else ''
                p.button(item['id'],(16,o,w-32,48),item['title']+suffix,lambda it=item:self.practice_open(it),enabled=known);o+=58
                if not known:o+=p.paragraph(16,o,'Zuerst: '+self.learning.by_key[item['lesson']]['title'],w-32,14,MUTED)+15
            o+=p.paragraph(16,o,'Zeichen nachzeichnen · '+self.practice_data()['trace_note'],w-32,17)+18
            kana=[c for c in self.learning.available_cards() if len(c['jp'])==1 and '\u3041'<=c['jp']<='\u30fe'][:80]
            columns=max(1,int((w-32)//75))
            for i,c in enumerate(kana):
                col=i%columns;row=i//columns;p.button('trace:'+c['key'],(16+75*col,o+65*row,64,54),c['jp'],lambda card=c:self.trace_open(card),size=25)
            o+=((len(kana)+columns-1)//columns)*65
        elif self.practice_index>=len(story['questions']):
            o+=p.paragraph(16,o,story['title']+' · Situation geübt',w-32,26,WHITE,True)+24
            o+=p.paragraph(16,o,'Mit Lesehilfe bearbeitet.' if self.practice_help_used else 'Beide Hörfragen mit bekanntem Wortschatz gelöst.',w-32,20)+24
            p.button('practice-back',(16,o,w-32,46),'Andere Situation',self.practice_back);o+=60
        else:
            q=story['questions'][self.practice_index];o+=p.paragraph(16,o,f"{story['title']} · Frage {self.practice_index+1} / {len(story['questions'])}",w-32,22,WHITE,True)+18
            p.button('story-play',(16,o,(w-44)/2,44),'Dialog anhören',self.practice_listen,'blue',enabled=not self.job);p.button('story-slow',(28+(w-44)/2,o,(w-44)/2,44),'Langsam',lambda:self.practice_listen(True),enabled=not self.job);o+=56
            p.button('story-help',(16,o,w-32,42),'Lesung und Bedeutung',self.practice_toggle);o+=54
            if self.practice_help:
                for c in self.learning.by_key[story['lesson']]['cards']:o+=p.paragraph(16,o,c['jp']+'\n'+c['romaji']+' · '+c['de'],w-32,17,MUTED,lineheight=24)+15
            o+=p.paragraph(16,o,q['prompt'],w-32,20,WHITE,True)+15
            for i,value in enumerate(q['options']):p.button('story-choice:'+str(i),(16,o,w-32,50),value,lambda v=value:self.practice_choose(v),enabled=not self.practice_success);o+=62
            o+=p.paragraph(16,o,self.practice_feedback,w-32,17,BLUE,lineheight=24)+16
        self.scroll_pane(s,p,x,y,self.H-y-85,o+self.scroll)
        if story and self.practice_index<len(story['questions']):s.button('story-next',(x,self.H-65,w,44),'Weiter →' if self.practice_success else 'Zurück',self.practice_next if self.practice_success else self.practice_back,'green')

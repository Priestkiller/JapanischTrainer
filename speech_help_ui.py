"""Windows speech-help adapter; speaking remains optional in the lesson flow."""
from speech_support import SpeechSupport,speech_deck,SUPPORT_MESSAGE
from ui_renderer import WHITE,MUTED,INK

class SpeechHelpMixin:
    def current_speech_support(self):
        if self.view=='exercises':return self.exercise_round.support
        c=self.support_card();key=getattr(self,'speech_review_key',None) if self.view=='speaking' else None
        key=key or 'lesson:'+c['key']
        if getattr(self,'_speech_support',None) is None or self._speech_support.key!=key:self._speech_support=SpeechSupport(self.store,key,{'card':c['key'],'lesson':c['lesson_key'],'kind':'lesson'})
        return self._speech_support
    def support_card(self):
        if self.view=='exercises':return next(c for c in self.learning.cards if c['key']==self.exercise_round.task['card'])
        target=(self.speech_item or {}).get('target')
        explicit=(self.speech_item or {}).get('card_key')
        if explicit:return next(c for c in self.learning.cards if c['key']==explicit)
        current=next(c for c in self.learning.cards if c['key']==f'{self.lesson["key"]}:{self.card_index}')
        if current['jp']==target:return current
        return next((c for c in self.learning.cards if c['jp']==target),next(c for c in self.learning.cards if c['key']==f'{self.lesson["key"]}:{self.card_index}'))
    def speech_help_deck(self):
        c=self.support_card()
        if self.view=='exercises':
            r=self.exercise_round;known=[x for x in self.learning.cards if x['key'] in r.pack['introduced']];mode='japanese' if r.task['family']=='recall' else 'meaning'
        else:known=self.learning.cards[:self.learning.cards.index(c)+1];mode='meaning'
        return speech_deck(c,known,self.learning.cards,mode)
    def toggle_speech_help(self):
        if self.recording or self.job:return
        support=self.current_speech_support()
        if support.data['open']:support.data['open']=False;support.save()
        else:support.open()
        self.request_draw()
    def choose_speech_help(self,identity):self.current_speech_support().select(identity);self.request_draw()
    def prepare_speech_help(self):self.current_speech_support().prepare();self.request_draw()
    def confirm_speech_help(self):
        if self.recording or self.job:return
        support=self.current_speech_support();deck=self.speech_help_deck()
        ok=self.exercise_round.accept_support(deck) if self.view=='exercises' else support.confirm(deck)
        if ok:
            if self.view=='lesson':
                metrics=self.flow.metrics();metrics['speech_supported']=metrics.get('speech_supported',0)+1;metrics['last_speech_outcome']='selection';self.flow.snapshot()
            self.react('praise','speech-assisted')
        self.request_draw()
    def draw_speech_help(self,s,b):
        # Independent, explicit paging keeps the lesson and recording cue fixed.
        x,y,w,h=b;offset=getattr(self,'speech_help_offset',0);p=self.make_pane(w,6000)
        old=self.entry_target
        self._draw_speech_help_content(p,(0,0,w,6000))
        total=getattr(self,'speech_help_height',600);vh=max(90,h-50);maximum=max(0,total-vh)
        offset=min(offset,maximum);self.speech_help_offset=offset
        # Surface.compose clips a translated surface; use its image and matching hits.
        cropped=self.make_pane(w,vh);cropped.compose(p,0,-offset,(w,6000))
        s.compose(cropped,x,y,(w,vh));self.entry_target=old
        if maximum:
            def move(delta):self.speech_help_offset=max(0,min(maximum,offset+delta));self.request_draw()
            s.button('support-up',(x,y+h-43,(w-8)/2,38),'↑ Zurück',lambda:move(-vh*.7),size=12,enabled=offset>0)
            s.button('support-down',(x+(w+8)/2,y+h-43,(w-8)/2,38),'Weiterlesen ↓',lambda:move(vh*.7),size=12,enabled=offset<maximum)
        return True
    def _draw_speech_help_content(self,s,b):
        support=self.current_speech_support();d=support.data;x,y,w,h=b
        if not d['open']:
            if d['failures']:
                s.paragraph(x+12,y+12,f'{d["failures"]} erfolglose Versuche. '+d['feedback'],w-24,13,MUTED,lineheight=18)
            return False
        deck=self.speech_help_deck();s.panel(b,'dark',16);q=y+14
        q+=s.paragraph(x+14,q,'Mit Auswahlhilfe weiterlernen',w-28,18,WHITE,True,lineheight=24)+10
        q+=s.paragraph(x+14,q,SUPPORT_MESSAGE,w-28,13,MUTED,lineheight=18)+12
        if deck['needsPreparation'] and not d['prepared']:
            q+=s.paragraph(x+14,q,'Lerne den Vergleich zuerst kennen:',w-28,14,WHITE,lineheight=19)+8
            for c in deck['prepare']:q+=s.paragraph(x+14,q,c['jp']+' · '+c['romaji']+' · '+c['de'],w-28,14,WHITE,lineheight=20,jp=True)+10
            s.button('support-prepare',(x+12,q,w-24,44),'Verglichen · jetzt auswählen',self.prepare_speech_help,'blue',size=12)
        else:
            c=next(c for c in deck['options'] if c['id']==deck['correct'])
            prompt=('Wähle die japanische Form für: '+c['de']) if deck['mode']=='japanese' else 'Welche Bedeutung gehört zu '+c['jp']+' ('+c['romaji']+')?'
            q+=s.paragraph(x+14,q,prompt,w-28,15,WHITE,True,lineheight=21,jp=True)+12
            for c in deck['options']:
                bh=max(44,16+18*len(s.wrap(c['label'],w-50,13)))
                s.button('support-choice:'+c['id'],(x+12,q,w-24,bh),'',lambda key=c['id']:self.choose_speech_help(key),'selected' if d['choice']==c['id'] else 'secondary',enabled=not d['assisted'])
                s.paragraph(x+24,q+8,c['label'],w-48,13,WHITE,lineheight=18,jp=True);q+=bh+8
            s.button('support-confirm',(x+12,q,w-24,44),'Auswahl bestätigen',self.confirm_speech_help,'green',size=13,enabled=not d['assisted']);q+=54
        if deck['needsPreparation'] and not d['prepared']:q+=54
        if d['feedback']:q+=s.paragraph(x+14,q,d['feedback'],w-28,13,MUTED,lineheight=18)
        self.speech_help_height=q+16
        return True
    def start_speech_review(self,key):
        entry=self.store.data.get('speech_reviews',{}).get(key);c=next((c for c in self.learning.cards if entry and c['key']==entry.get('card')),None)
        if not c:return
        self.speech_review_key=key;self.speech_item=self.learning.speech_target(c,self.learning.by_key[c['lesson_key']]);self.speech_item['approx']=c.get('approx','');self.speech_item['note']=c.get('note','');self.speech_item['card_key']=c['key']
        self.navigate('speaking');support=self.current_speech_support()
        if support.data['assisted']:support.new_round()
        self.result=None;self.last_audio=None;self.speech_error='';self.request_draw()

"""Persisted, task-scoped speech assistance. No XP, completion or score writes."""
import time, unicodedata, re

SUPPORT_MESSAGE='Die Erkennung klappt gerade nicht zuverlässig. Du kannst die passende Antwort auswählen und später weiter sprechen üben.'
REASONS={'mismatch':'Der erkannte Text passt noch nicht zur Vorgabe. Das kann auch an der Erkennung liegen.',
         'unreliable':'Es wurde keine verlässliche Sprache erkannt. Daraus folgt kein Aussprachefehler.',
         'technical':'Die Aufnahme oder Auswertung ist technisch fehlgeschlagen. Das ist kein Aussprachefehler.'}

class SpeechSupport:
    def __init__(self,store,key,source=None):
        self.store=store;self.key=key;self.source=source or {};self.active=None
        all=store.data.setdefault('speech_support',{});old=all.get(key)
        self.data=old if isinstance(old,dict) else {};d=self.data
        d['failures']=max(0,min(1000,d.get('failures',0))) if type(d.get('failures')) is int else 0
        d['reason']=d.get('reason') if d.get('reason') in REASONS else ''
        for k in ('open','prepared','assisted'):d[k]=d.get(k) is True
        d['choice']=d.get('choice') if isinstance(d.get('choice'),str) else None
        d['feedback']=d.get('feedback','')[:4000] if isinstance(d.get('feedback',''),str) else ''
        all[key]=d;store.data.setdefault('speech_reviews',{})
    def save(self):self.store.data['speech_support'][self.key]=self.data;self.store.save()
    @property
    def unlocked(self):return self.data['failures']>=3
    def begin(self,identity):
        if not identity or self.active or self.data['assisted']:return False
        self.active=identity;return True
    def cancel(self):self.active=None
    def finish(self,identity,reason):
        if not identity or identity!=self.active:return False
        self.active=None
        if reason=='accepted':
            self.store.data['speech_reviews'].pop(self.key,None);self.data['feedback']='Der erkannte Text passt zur Vorgabe.';self.save();return True
        if reason not in REASONS:return False
        self.data['failures']+=1;self.data['reason']=reason;self.data['feedback']=REASONS[reason];self.save();return True
    def open(self):
        if not self.unlocked:return False
        self.data['open']=True;self.save();return True
    def select(self,identity):
        if not self.unlocked or self.data['assisted']:return
        self.data['choice']=identity;self.save()
    def prepare(self):
        if self.unlocked:self.data['prepared']=True;self.save()
    def confirm(self,deck):
        d=self.data
        if self.active or not self.unlocked or not d['open'] or d['assisted'] or len(deck['options'])<2 or deck['needsPreparation'] and not d['prepared']:return False
        picked=next((c for c in deck['options'] if c['id']==d['choice']),None)
        if not picked:d['feedback']='Wähle eine Antwort und bestätige sie.';self.save();return False
        if picked['id']!=deck['correct']:
            d['feedback']=f'Noch nicht. {picked["jp"]} ({picked["romaji"]}) bedeutet hier „{picked["de"]}“. Vergleiche die Vorgabe und versuche es erneut.';self.save();return False
        d['assisted']=True;d['feedback']='Mit Auswahlhilfe geschafft. Sprechen übst du später weiter.'
        self.store.data['speech_reviews'][self.key]={**self.source,'due':time.time()+86400,'status':'pending'};self.save();return True
    def new_round(self):
        self.cancel();self.data={'failures':0,'reason':'','open':False,'prepared':False,'assisted':False,'choice':None,'feedback':''};self.save()

def speech_deck(target,known,available=(),mode='meaning'):
    norm=lambda s:re.sub(r'[\s。！？!?.,、]','',unicodedata.normalize('NFKC',str(s)).lower())
    candidates=[target];used_jp={norm(target['jp'])};used_de={norm(target['de'])}
    def add(c):
        if not c or not c.get('jp') or not c.get('de') or norm(c['jp']) in used_jp or norm(c['de']) in used_de:return
        used_jp.add(norm(c['jp']));used_de.add(norm(c['de']));candidates.append(c)
    for c in reversed(known):add(c)
    needs=len(candidates)<2
    if needs:
        for c in available:
            add(c)
            if len(candidates)>=2:break
    options=[{**c,'id':c['key'],'label':c['jp']+' · '+c['romaji'] if mode=='japanese' else c['de']} for c in candidates[:4]]
    shift=sum(ord(c) for c in target['key'])%max(1,len(options));options=options[shift:]+options[:shift]
    return {'correct':target['key'],'options':options,'needsPreparation':needs,'prepare':candidates[:2],'mode':mode}

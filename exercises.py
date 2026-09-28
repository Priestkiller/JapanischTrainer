"""Bounded additional rounds on the existing course, profile and review schedule.

No lesson completion or XP writes. Stable task IDs are independent of display order.
The JSON description is shared with the Android adapter in exercises.mjs.
"""
from __future__ import annotations
import copy, json, re, time, unicodedata
from pathlib import Path
from speech_support import SpeechSupport

FAMILIES={'pairs':'Paare zuordnen','echo':'Nachsprechen','recall':'Sag das auf Japanisch',
          'hear_gap':'Hörlücke','choice_gap':'Lücke auswählen','multi_gap':'Mehrfachlücken',
          'translate':'Übersetzen mit Bausteinen','read':'Lesen und antworten'}
INSTRUCTIONS={'pairs':'Wähle links eine Form oder ein Audiofeld und rechts ihre Bedeutung. Ordne alle Paare zu und bestätige mit Prüfen.',
 'echo':'Höre zuerst normal oder langsam zu. Sprich danach die sichtbare Vorlage nach.',
 'recall':'Sprich die deutsche Vorgabe auf Japanisch. Die gesuchte Antwort bleibt zunächst verborgen.',
 'hear_gap':'Höre zu und schreibe nur die fehlende Einheit in Romaji. Normal und Langsam wiederholen die Vorlage.',
 'choice_gap':'Wähle eine passende Ergänzung für die Lücke und bestätige mit Prüfen.',
 'multi_gap':'Wähle zuerst eine Lücke, dann ihren Baustein. Ergänze alle Lücken und bestätige mit Prüfen.',
 'translate':'Übersetze die deutsche Vorgabe mit den japanischen Bausteinen. Tippe sie in der Satzreihenfolge an und bestätige mit Prüfen.',
 'read':'Lies den japanischen Text. Wähle eine Antwort auf die Frage und bestätige mit Prüfen.'}

def normalize(value):
    return re.sub(r'[\s。！？!?.,、·「」“”]', '', unicodedata.normalize('NFKC',str(value)).lower())

def matches(value,answers,mode='exact'):
    def speech(s):
        s=normalize(re.sub(r'<\|.*?\|>','',s))
        return ''.join(chr(ord(c)-0x60) if 'ァ'<=c<='ヶ' else c for c in s)
    if mode=='speech':return bool(speech(value)) and any(speech(value)==speech(a) for a in answers)
    forms=set()
    for a in answers:
        f={normalize(a)}
        if mode=='romaji':
            for mark,alts in {'ā':['aa'],'ī':['ii'],'ū':['uu'],'ē':['ee'],'ō':['ou','oo']}.items():
                for old in list(f):
                    for alt in alts:f.add(old.replace(mark,alt))
        forms.update(f)
    return bool(normalize(value)) and normalize(value) in forms

def order(values,seed):
    """Identical deterministic shuffle in both adapters, independent left/right seeds."""
    values=list(values);h=2166136261
    for c in seed:h=((h ^ ord(c))*16777619)&0xffffffff
    for i in range(len(values)-1,0,-1):
        h=(h*1664525+1013904223)&0xffffffff;j=h%(i+1)
        values[i],values[j]=values[j],values[i]
    return values

class ExerciseBook:
    def __init__(self,root):
        self.data=json.loads((Path(root)/'data/exercises.json').read_text(encoding='utf8'))
        self.packs={p['lesson']:p for p in self.data['packs']}
        self.tasks={t['id']:t for t in self.data['tasks']}

class ExerciseRound:
    def __init__(self,book,lesson,store):
        self.book=book;self.lesson=lesson;self.store=store;self.pack=book.packs[lesson['key']]
        self.key='exercises:'+lesson['key'];saved=store.data.setdefault('lesson_sessions',{}).get(self.key)
        valid=isinstance(saved,dict) and saved.get('revision')==book.data['revision'] and saved.get('queue')==self.pack['tasks']
        # Preserve completed rounds until the user explicitly starts another round.
        self.state=copy.deepcopy(saved) if valid else self.fresh()
        self.sanitize();self.save()
    def fresh(self):return {'revision':self.book.data['revision'],'queue':list(self.pack['tasks']),'index':0,'stage':'intro','review':[],'review_index':0,'reviewed':[],'outcomes':[],'task':{}}
    def sanitize(self):
        s=self.state
        if s.get('stage') not in ('intro','main','review','complete'):s['stage']='intro'
        for field,maximum in [('index',len(s['queue'])-1),('review_index',5)]:
            v=s.get(field);s[field]=min(maximum,max(0,v)) if isinstance(v,int) else 0
        s['review']=[v for v in (s.get('review',[]) if isinstance(s.get('review'),list) else []) if v in self.pack['tasks']][:6]
        s['reviewed']=[v for v in (s.get('reviewed',[]) if isinstance(s.get('reviewed'),list) else []) if v in self.pack['tasks']][:20]
        if s['stage']=='review' and s['review_index']>=len(s['review']):s['stage']='complete'
        if not isinstance(s.get('outcomes'),list):s['outcomes']=[]
        s['outcomes']=s['outcomes'][-200:]
        if not isinstance(s.get('task'),dict):s['task']={}
        d=s['task']
        defaults={'choice':None,'text':'','tokens':[],'slots':{},'pairs':{},'active':0,'left':None,'heard':[],
                  'help':0,'help_open':False,'success':False,'feedback':'','checks':0,'per_slot':[],'transcript':'','audio_help':False}
        for key,value in defaults.items():
            if key not in d or value is not None and type(d[key]) is not type(value):d[key]=copy.deepcopy(value)
        for key in ('choice','left'):
            if d[key] is not None and not isinstance(d[key],str):d[key]=None
        for key in ('text','feedback','transcript'):d[key]=d[key][:4000]
        d['help']=min(2,max(0,d['help']));d['checks']=min(1000,max(0,d['checks']));d['active']=min(9,max(0,d['active']))
        d['tokens']=[v for v in d['tokens'] if isinstance(v,str)][:20]
        d['heard']=[v for v in d['heard'] if isinstance(v,str)][:20]
        for key in ('slots','pairs'):d[key]={str(k):v for k,v in list(d[key].items())[:20] if isinstance(v,str)}
    @property
    def task(self):
        s=self.state;ids=s['review'] if s['stage']=='review' else s['queue']
        i=s['review_index'] if s['stage']=='review' else s['index']
        return self.book.tasks[ids[min(i,len(ids)-1)]]
    @property
    def answer(self):return self.state['task']
    @property
    def support(self):
        key=f'exercise:{self.task["id"]}:{self.state["stage"]}'
        if getattr(self,'_support',None) is None or self._support.key!=key:self._support=SpeechSupport(self.store,key,{'card':self.task['card'],'lesson':self.lesson['key'],'kind':'exercise','task':self.task['id']})
        return self._support
    def accept_support(self,deck):
        if self.state['stage'] not in ('main','review') or self.task['family'] not in ('echo','recall') or self.answer['success'] or not self.support.confirm(deck):return False
        self.answer['success']=True;self.answer['feedback']=self.support.data['feedback'];self.answer['supported_speech']=True;self.log('selection')
        if self.state['stage']=='main':self.state['review']=[v for v in self.state['review'] if v not in (self.task['id'],self.task.get('repeat'))]
        self.save();return True
    def save(self):self.store.data['lesson_sessions'][self.key]=copy.deepcopy(self.state);self.store.save()
    def start(self):
        if self.state['stage']=='intro':self.state['stage']='main';self.save()
    def restart(self):
        for identity in self.pack['tasks']:
            for stage in ('main','review'):self.store.data.get('speech_support',{}).pop(f'exercise:{identity}:{stage}',None)
        self._support=None;self.state=self.fresh();self.sanitize();self.save()
    def help(self,level):
        d=self.answer;d['help']=max(d['help'],level);d['help_open']=True;self.save()
    def set(self,key,value):
        if key in ('help_open','active','left') or not self.answer['success']:
            self.answer[key]=value;self.save()
    def heard(self,identity='target',reading_help=False):
        if identity not in self.answer['heard']:self.answer['heard'].append(identity)
        if reading_help:self.answer['audio_help']=True
        self.save()
    def technical(self,message,paused=False):
        self.answer['feedback']=message
        self.log('paused' if paused else 'technical');self.save()
    def log(self,status):
        self.state['outcomes'].append({'task':self.task['id'],'result':status,'help':self.answer['help'],'audio_help':self.answer['audio_help']})
        self.state['outcomes']=self.state['outcomes'][-200:]
    def schedule(self):
        t=self.task;self.store.data.setdefault('review',{})[t['card']]={'box':0,'due':time.time()+60}
        target=t.get('repeat') or t['id']
        if self.state['stage']=='main' and target not in self.state['review'] and len(self.state['review'])<6:self.state['review'].append(target)
    def check(self,speech=None):
        d=self.answer;t=self.task;k=t['family']
        if self.state['stage'] not in ('main','review') or d['success']:return False
        if (k=='hear_gap' or k=='echo') and 'target' not in d['heard']:
            d['feedback']='Höre die Vorlage zuerst vollständig an. Du kannst auch pausieren.';self.save();return False
        if k=='pairs' and t['mode']=='audio' and not all(p['id'] in d['heard'] for p in t['pairs']):
            d['feedback']='Höre zuerst alle Audiofelder vollständig an.';self.save();return False
        ok=False;feedback=t['why'];d['per_slot']=[]
        if k in ('echo','recall'):
            if speech is None:return False
            if not speech.strip():self.technical('Keine sichere Erkennung. Prüfe das Mikrofon oder pausiere.');return False
            d['transcript']=speech
            ok=matches(speech,t['accepted_speech'],'speech')
            if not ok:
                d['checks']+=1;self.log('unverified');self.schedule();d['feedback']='Der erkannte Text ist nicht unter den geprüften Antworten. Eine andere zulässige Form oder ein Erkennungsfehler ist möglich. Keine Aussprachebewertung. Öffne die Erklärung oder versuche es erneut.';self.save();return False
        elif k=='pairs':
            ok=all(d['pairs'].get(p['id'])==p['id'] for p in t['pairs'])
            wrong=next((p for p in t['pairs'] if d['pairs'].get(p['id'])!=p['id']),None)
            if wrong:feedback=f'Noch offen: {wrong["jp"]} bedeutet hier „{wrong["de"]}“. Wähle das linke Feld erneut, um nur dieses Paar zu korrigieren.'
        elif k in ('choice_gap','read'):
            ok=d['choice'] in t['answers']
            chosen=next((c for c in t['choices'] if c['id']==d['choice']),None)
            feedback=chosen['feedback'] if chosen else 'Wähle zuerst eine Antwort aus.'
        elif k=='hear_gap':
            ok=matches(d['text'],t['answers'],t['input_mode']);feedback=t['hint']+' Vergleiche die gehörte Einheit und behalte die Vokallänge bei.'
        elif k in ('translate','multi_gap'):
            by={v['id']:v['text'] for v in t['tokens']}
            ids=d['tokens'] if k=='translate' else [d['slots'].get(str(i)) for i in range(len(t['solutions'][0]))]
            words=[by.get(v,'') for v in ids]
            unique=len(ids)==len(set(ids))
            ok=unique and words in t['solutions']
            feedback=t['hint']+' Prüfe Bedeutung und Reihenfolge; die Aufgabe benötigt eine vollständige passende Lösung.'
            if k=='multi_gap':
                d['per_slot']=[any(i<len(v) and word==v[i] for v in t['solutions']) for i,word in enumerate(words)]
                feedback=' '.join(f'Lücke {i+1}: '+('passt an dieser Stelle.' if good else t['slot_feedback'][i]) for i,good in enumerate(d['per_slot']))
        d['checks']+=1;d['success']=ok
        if ok:
            supported=d['help']>0 or d['audio_help']
            status='solution' if d['help']==2 else 'hint' if supported else 'independent' if d['checks']==1 else 'corrected'
            self.log(status)
            d['feedback']=('Mit Unterstützung gelöst. ' if supported else 'Passend gelöst. ')+feedback
        else:
            self.log('wrong');self.schedule();d['feedback']=feedback
            if d['checks']>=3:d['feedback']+=' Du darfst die vollständige Erklärung öffnen oder eine Pause machen. Die Aufgabe bleibt offen.'
        self.save();return ok
    def advance(self):
        if not self.answer['success']:return False
        s=self.state
        if s['stage']=='main':
            s['index']+=1
            if s['index']>=len(s['queue']):
                s['index']=len(s['queue'])-1;s['stage']='review' if s['review'] else 'complete'
        elif s['stage']=='review':
            s['review_index']+=1
            if s['review_index']>=len(s['review']):s['stage']='complete'
        s['task']={};self.sanitize();self.save();return True

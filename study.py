"""Deterministic guided practice; no audio recognition result gates course progress.

The six phases teach first, then retrieve the same material in different ways.
Legacy identifiers remain the V6/V7 keys; additions have explicit v11:slug keys. Display order never becomes a progress identifier.
"""
from __future__ import annotations
import json, random, re, time, unicodedata
from pathlib import Path
from adaptive import record_attempt, PHASE_SKILL

PHASES = ('understand','meaning','listen','build','write','apply')
LABELS = {'understand':'Verstehen','meaning':'Bedeutung','listen':'Hören',
          'build':'Bausteine','write':'Schreiben','apply':'Anwenden'}

def compact(text: str) -> str:
    text = unicodedata.normalize('NFKC', str(text)).lower()
    return re.sub(r'[\s\-・、。！？!?.,:;~〜～/…「」“”"\'()]', '', text)

def romaji_forms(text: str) -> set[str]:
    """Keep vowel length: arigatō accepts arigatou/arigatoo, NOT arigato."""
    forms={compact(text)}
    for long,alternatives in {'ā':('aa',),'ī':('ii',),'ū':('uu',),'ē':('ee',),'ō':('ou','oo')}.items():
        for old in list(forms):
            if long in old:
                for replacement in alternatives: forms.add(old.replace(long,replacement))
    return forms

def matches_romaji(given: str, expected: str) -> bool:
    # Apostrophe disambiguation after n is optional here; vowel length is not.
    return compact(given) in romaji_forms(expected)

class PracticeBook:
    def __init__(self, root: Path, learning):
        self.learning=learning
        self.data=json.loads((root/'data/deep_lessons.json').read_text(encoding='utf8'))
    def profile(self,card,lesson):
        supplied=card.get('detail') or self.data['profiles'].get(card['jp'])
        if supplied: return supplied
        note=card.get('note','').strip()
        is_row=' ' in card['jp'] and not any(k in card['jp'] for k in ('です','ます','。'))
        return {'kind':'Zeichenreihe' if is_row else 'Lernwort / Satzmuster',
                'usage':'In dieser Karte lernst du: '+card['de']+'.',
                'explain':note or 'Vergleiche die japanische Schreibweise mit der Lesung. Lerne zuerst diese konkrete Form; du musst noch keine weiteren Formen selbst herleiten.',
                'pitfall':'Die deutsche Aussprachehilfe ist nur eine Annäherung. Höre die Vorlage und halte lange Vokale bewusst länger. Du darfst beim Üben jederzeit nachschauen.',
                'parts':[], 'extra':[], 'register':'',
                'scenario':{'question':'Welche Beschreibung gehört zu dieser Lernkarte?',
                            'correct':card['de'],
                            'wrong':[c['de'] for c in lesson['cards'] if c['de']!=card['de']][:3]}}
    def intro(self,lesson):
        return lesson.get('intro') or self.data['lesson_notes'].get(lesson['key'],
            f"In „{lesson['title']}“ übst du jede Karte in sechs Schritten. Lies zuerst Erklärung und Beispiel. "
            'Dann ordnest du die Bedeutung zu, hörst zu, setzt Bausteine zusammen, tippst die Lesung und prüfst die Anwendung. '
            'Die abschließende Wiederholungsrunde enthält nur Material aus dieser Lektion. Fehler kosten keine Leben.')
    def option_label(self,value):
        # Make Japanese choices self-contained: never hide an unknown option's reading.
        card=next((c for c in self.learning.cards if compact(c['jp'])==compact(value)),None)
        return f"{value} · {card['romaji']}\n{card['de']}" if card and re.search('[ぁ-龯]',value) else value
    def blocks(self,card,lesson):
        roman=card['romaji'].strip().split()
        if 2<=len(roman)<=10:return roman, 'Romaji-Wörter'
        jp=card['jp'].strip().rstrip('。！？!?')
        supplied=self.profile(card,lesson)['parts']
        if 2<=len(supplied)<=10 and compact(''.join(p[0] for p in supplied))==compact(jp):
            return [p[0] for p in supplied], 'Schreibbausteine'
        chars=[]
        for char in jp:
            if char in 'ゃゅょャュョぁぃぅぇぉァィゥェォ' and chars:chars[-1]+=char
            elif not char.isspace():chars.append(char)
        if 2<=len(chars)<=10:return chars, 'Schreibbausteine'
        return [], 'Lesung'

class StudySession:
    def __init__(self, lesson, store, book, index=0, restore=False):
        self.lesson=lesson;self.store=store;self.book=book
        self.index=max(0,min(int(index),len(lesson['cards'])-1))
        self.phase='understand';self.mode='learn';self.recap=[];self.recap_total=0;self.recap_passed=0
        saved=store.data.setdefault('lesson_sessions',{}).get(lesson['key'],{})
        if restore and isinstance(saved,dict):
            self.index=max(0,min(int(saved.get('index',self.index)),len(lesson['cards'])-1))
            self.phase=saved.get('phase') if saved.get('phase') in PHASES else 'understand'
            if saved.get('mode')=='recap':
                self.recap=[int(i) for i in saved.get('recap',[]) if isinstance(i,int) and 0<=i<len(lesson['cards'])]
                if self.recap:self.mode='recap';self.index=self.recap[0]
                self.recap_total=int(saved.get('recap_total',len(lesson['cards'])))
                self.recap_passed=int(saved.get('recap_passed',0))
        self.reset_task()
        task=saved.get('task') if restore and isinstance(saved,dict) else None
        if isinstance(task,dict) and task.get('identity')==self.card_key+':'+self.phase+':'+self.mode:
            for name in ('input_text','feedback'):
                if isinstance(task.get(name),str):setattr(self,name,task[name][:4000])
            for name in ('success','audio_seen','audio_skipped','hint_used','skipped'):
                if isinstance(task.get(name),bool):setattr(self,name,task[name])
            if isinstance(task.get('chosen'),str):self.chosen=task['chosen']
            self.tokens=[v for v in task.get('tokens',[]) if isinstance(v,int) and 0<=v<len(self.book.blocks(self.card,self.lesson)[0])][:10] if isinstance(task.get('tokens'),list) else []
    @property
    def card(self):return self.lesson['cards'][self.index]
    @property
    def card_key(self):return self.lesson['key']+':'+str(self.index)
    def reset_task(self):
        self.success=False;self.feedback='';self.chosen=None;self.tokens=[];self.audio_seen=False
        self.audio_skipped=False;self.skipped=False;self.hint_used=False;self.input_text=''
        rng=random.Random(self.card_key+':'+self.phase)
        self.listen_index=rng.randrange(self.index+1)
        self.listen_card=self.lesson['cards'][self.listen_index]
    def snapshot(self):
        self.store.data.setdefault('lesson_sessions',{})[self.lesson['key']]={
            'index':self.index,'phase':self.phase,'mode':self.mode,'recap':self.recap,
            'recap_total':self.recap_total,'recap_passed':self.recap_passed,
            'task':{'identity':self.card_key+':'+self.phase+':'+self.mode,**{k:getattr(self,k) for k in ('input_text','feedback','success','audio_seen','audio_skipped','hint_used','skipped','chosen','tokens')}}}
        self.store.data['last_lesson']={'key':self.lesson['key'],'card':self.index}
        self.store.save()
    def metrics(self):
        v=self.store.data.setdefault('study_cards',{}).setdefault(self.card_key,{})
        for key in ('attempts','mistakes','speech_attempts','speech_skips'):
            if not isinstance(v.get(key),int):v[key]=0
        if not isinstance(v.get('phases'),list):v['phases']=[]
        return v
    def mark(self,ok,feedback,skipped=False):
        if self.success:return
        self.success=bool(ok);self.feedback=feedback;self.skipped=skipped
        m=self.metrics();m['attempts']+=1
        if not ok:
            m['mistakes']+=1
            self.store.data.setdefault('review',{})[self.card_key]={'box':0,'due':time.time()}
        elif not skipped and self.phase not in m['phases']:m['phases'].append(self.phase)
        if skipped:m.setdefault('skipped_phases',[]).append(self.phase)
        skill=PHASE_SKILL.get(self.phase)
        if skill:
            index=self.listen_index if self.phase=='listen' and self.mode!='recap' else self.index
            record_attempt(self.store.data, self.lesson['key']+':'+str(index), skill, ok, skipped or self.hint_used)
        self.store.touch_day();self.snapshot()
    def answers(self):
        if self.mode=='recap' or self.phase=='meaning':
            correct=self.card['de'];pool=[c['de'] for c in self.lesson['cards']]
        elif self.phase=='listen':
            correct=self.listen_card['de'];pool=[c['de'] for c in self.lesson['cards'][:self.index+1]]
        elif self.phase=='apply':
            scenario=self.book.profile(self.card,self.lesson)['scenario'];correct=scenario['correct'];pool=scenario['wrong']
        else:
            correct=self.card['romaji'];pool=[c['romaji'] for c in self.lesson['cards'][:self.index+1]]
        pool=list(dict.fromkeys(p for p in pool if p!=correct))
        rng=random.Random(self.card_key+':'+self.phase+':options');rng.shuffle(pool)
        opts=[correct]+pool[:3];rng.shuffle(opts)
        return opts,correct
    def choose(self,value):
        opts,correct=self.answers()
        if value not in opts:return
        if self.phase=='listen' and self.mode!='recap' and not(self.audio_seen or self.audio_skipped):
            self.feedback='Bitte zuerst das Hörbeispiel anhören oder „Ohne Ton“ wählen.';return
        self.chosen=value;ok=value==correct
        why=self.book.profile(self.card,self.lesson)
        feedback=('Richtig. '+(why['scenario'].get('explanation',why['explain']) if self.phase=='apply' and self.mode!='recap' else 'Die passende Zuordnung ist: '+str(correct))) if ok else self.wrong_choice(value)
        self.mark(ok,feedback,skipped=self.phase=='listen' and self.audio_skipped)
    def wrong_choice(self,value):
        if self.phase=='apply' and self.mode!='recap':
            profile=self.book.profile(self.card,self.lesson)
            reason=profile['scenario'].get('feedback',{}).get(value) or profile['explain']
        elif self.phase=='build' and self.mode!='recap':
            profile=self.book.profile(self.card,self.lesson)
            reason=profile.get('feedback',{}).get('write',profile['pitfall'])
        else:
            target=self.listen_card if self.phase=='listen' and self.mode!='recap' else self.card
            other=next((c for c in self.lesson['cards'] if c['de']==value),None)
            prefix=f'Deine Auswahl gehört zu {other["jp"]} ({other["romaji"]}). ' if other else ''
            reason=prefix+self.book.profile(target,self.lesson)['explain']
        return 'Noch nicht. '+reason+' Die Aufgabe bleibt offen.'
    def check_build(self):
        parts,_=self.book.blocks(self.card,self.lesson)
        if not parts:return
        right=self.tokens==list(range(len(parts))) or [parts[i] for i in self.tokens]==parts
        hint=self.book.profile(self.card,self.lesson).get('feedback',{}).get('build','Die Bausteine müssen vollständig sein. '+self.book.profile(self.card,self.lesson)['explain'])
        self.mark(right,'Richtig zusammengesetzt.' if right else 'Die Reihenfolge stimmt noch nicht. '+hint)
    def check_write(self,text):
        self.input_text=text;ok=any(matches_romaji(text,reading) for reading in [self.card['romaji']]+self.card.get('romaji_aliases',[]))
        hint=self.book.profile(self.card,self.lesson).get('feedback',{}).get('write',self.book.profile(self.card,self.lesson)['pitfall'])
        self.mark(ok,'Richtig geschrieben. Lange Vokale sind erhalten.' if ok else
                  'Noch nicht passend. '+hint+' Für ō sind ou oder oo möglich; fehlende Vokallänge bleibt ein Fehler.')
    def advance(self):
        """Returns complete only after every task and a full recap, never after one MC."""
        if not self.success:return 'blocked'
        if self.mode=='recap':
            self.recap.pop(0);self.recap_passed+=1
            if not self.recap:return 'complete'
            self.index=self.recap[0]
        else:
            pi=PHASES.index(self.phase)
            if pi+1<len(PHASES):self.phase=PHASES[pi+1]
            elif self.index+1<len(self.lesson['cards']):self.index+=1;self.phase='understand'
            else:
                self.mode='recap';self.phase='meaning';self.recap=list(range(len(self.lesson['cards'])))
                random.Random(self.lesson['key']+':recap').shuffle(self.recap)
                # Harder cards reappear a second time after intervening cards.
                weak=[i for i in self.recap if self.store.data.get('study_cards',{}).get(self.lesson['key']+':'+str(i),{}).get('mistakes',0)>0]
                self.recap+=weak;self.recap_total=len(self.recap);self.recap_passed=0;self.index=self.recap[0]
        self.reset_task();self.snapshot();return 'next'

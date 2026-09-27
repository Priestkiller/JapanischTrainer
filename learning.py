"""Course adapter with stable progress keys and a separate pedagogical order.

The physical position of old units/cards is retained. Display order and search
are independent of those IDs, so expanding the course cannot erase old results.
"""
from __future__ import annotations
import json, random, re, shutil, unicodedata
from copy import deepcopy

class Learning:
    def __init__(self,root,store):
        self.root=root;self.store=store
        self.course=json.loads((root/'data/course.json').read_text(encoding='utf8'))
        self.catalog=json.loads((root/'data/catalog.json').read_text(encoding='utf8'))
        self.teachers=self.catalog['TEACHERS'];self.by_teacher={x['id']:x for x in self.teachers}
        physical=[]
        for ui,u in enumerate(self.course['units']):
            for li,l in enumerate(u['lessons']):
                physical.append(dict(l,key=l.get('id',f'{ui}:{li}'),
                    unit=re.sub(r'^\d+\.\s*','',u['title']),
                    level=l.get('stage',u['level']),ui=ui,li=li))
        by_key={l['key']:l for l in physical}
        if len(by_key)!=len(physical):raise ValueError('Doppelte Lektionskennung im Kurs.')
        order=self.course.get('learning_order',[l['key'] for l in physical])
        if len(order)!=len(set(order)) or set(order)!=set(by_key):
            raise ValueError('Die Kursreihenfolge enthält fehlende oder doppelte Kennungen.')
        self.lessons=[by_key[k] for k in order];self.by_key=by_key
        self.positions={key:i for i,key in enumerate(order)}
        self.stages=list(dict.fromkeys(l['level'] for l in self.lessons))
        self.cards=[]
        for l in self.lessons:
            for i,c in enumerate(l['cards']):
                self.cards.append(dict(c,key=f"{l['key']}:{i}",lesson_key=l['key'],
                    lesson=l['title'],card_index=i))
        self.migrate_course_progress()

    def migrate_course_progress(self):
        """Backup first; retain completions, XP, current phase and old access.

        New foundational units may be placed before an existing completion.
        They are available as optional catch-up, never a forced reset.
        """
        data=self.store.data;revision=int(self.course.get('revision',1))
        if data.get('course_revision')==revision:return
        path=self.store.path
        if path.exists():
            backup=path.with_name(f'progress.before-course-v{revision}.json')
            if not backup.exists():shutil.copy2(path,backup)
        legacy=self.course.get('legacy_order',[])
        done=set(data.get('completed',[]))
        allowed=set(data.get('legacy_unlocked',[]) or [])
        for i,key in enumerate(legacy):
            if i==0 or key in done or legacy[i-1] in done:allowed.add(key)
        cursor=data.get('last_lesson',{}).get('key')
        if cursor in self.by_key:allowed.add(cursor)
        allowed.update(k for k in data.get('lesson_sessions',{}) if k in legacy)
        data['legacy_unlocked']=[k for k in self.by_key if k in allowed]
        data['course_revision']=revision
        self.store.save()

    def teacher(self,id=None):return self.by_teacher.get(id or self.store.data.get('teacher_id'),self.teachers[0])
    def asset(self,t=None,kind='full'):return self.root/'assets/teachers'/(t or self.teacher())['id']/(kind+'.png')
    def unlocked(self,key):
        if key not in self.positions:return False
        done=set(self.store.data['completed'])
        frontier=max((self.positions[k] for k in done if k in self.positions),default=-1)
        return (self.positions[key]<=frontier+1 or key in self.store.data.get('legacy_unlocked',[]))
    def next_lesson(self):
        done=set(self.store.data['completed']);cursor=self.store.data.get('last_lesson',{}).get('key')
        if cursor in self.by_key and cursor not in done and self.unlocked(cursor):return self.by_key[cursor]
        return next((l for l in self.lessons if l['key'] not in done),self.lessons[-1])
    def available_cards(self,all_=False):
        if all_:return self.cards
        done=set(self.store.data['completed']);cursor=self.store.data.get('last_lesson',{})
        cards=[c for c in self.cards if c['lesson_key'] in done or (c['lesson_key']==cursor.get('key') and c['card_index']<=cursor.get('card',0))]
        return cards or [self.cards[0]]
    def filtered_lessons(self,query='',stage='Alle',new_only=False):
        terms=unicodedata.normalize('NFKC',query).casefold().split()
        def matches(lesson):
            if stage!='Alle' and lesson['level']!=stage:return False
            if new_only and lesson.get('origin')!='v11':return False
            text=' '.join([lesson['title'],lesson['unit'],lesson.get('goal','')]+[
                c[k] for c in lesson['cards'] for k in ('jp','de','romaji')])
            folded=unicodedata.normalize('NFKC',text).casefold()
            return all(t in folded for t in terms)
        return [l for l in self.lessons if matches(l)]
    def examples(self,card):
        x=card.get('example')
        if isinstance(x,dict) and all(x.get(k) for k in ('jp','romaji','de')):return deepcopy(x)
        x=self.catalog['EXAMPLES'].get(card['jp'])
        return dict(jp=x[0],romaji=x[1],de=x[2]) if x else dict(jp=card['jp'],romaji=card['romaji'],de=card['de'])
    def answers(self,card,lesson):
        # German-only alternatives in the same topic; no unknown Japanese answer.
        pool=list(dict.fromkeys(c['de'] for c in lesson['cards'] if c['de']!=card['de']))
        rng=random.Random(card['jp']+'v7');rng.shuffle(pool);opts=[card['de']]+pool[:3];rng.shuffle(opts);return opts
    def speech_target(self,card,lesson):
        match=next((x for x in lesson.get('speech',[]) if x['target'].rstrip('。！？!?')==card['jp'].rstrip('。！？!?')),None)
        return deepcopy(match) if match else dict(target=card['jp'],romaji=card['romaji'],meaning=card['de'],accept=[card['jp']])
    @staticmethod
    def normalize_answer(s):return unicodedata.normalize('NFKC',str(s)).strip().lower().replace(' ','').rstrip('。.!?！？')

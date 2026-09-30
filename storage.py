"""V6-compatible local progress storage with atomic writes and migration backups."""
from __future__ import annotations
import json, math, os, shutil
from datetime import date, timedelta, datetime
from pathlib import Path
from motion import preset_name
from adaptive import clean_adaptive


def data_dir():
    if os.environ.get('JAPANISCHTRAINER_DATA_DIR'):
        p=Path(os.environ['JAPANISCHTRAINER_DATA_DIR'])
    elif os.environ.get('APPDATA'):
        p=Path(os.environ['APPDATA'])/'JapanischTrainer'
    else:
        p=Path.home()/'.japanisch_trainer'
    p.mkdir(parents=True,exist_ok=True)
    return p


class ProgressStore:
    def __init__(self):
        self.path=data_dir()/'progress.json'
        self.warning=''
        self.data={'completed':[],'xp':0,'speech_scores':{},'speaker_id':0,
                   'teacher_id':'sakura','tts_speed':1.,'mic_device':None,'streak':0,
                   'last_active':None,'review':{},'last_lesson':{},'ui_scale':1.,
                   'show_kiko':True,'library_all':False,'motion_enabled':True,
                   'study_cards':{},'lesson_sessions':{},'speech_support':{},'speech_reviews':{},'motion_preset':'natural'}
        self.load()
        self.data['adaptive']=clean_adaptive(self.data.get('adaptive'))

    def load(self):
        if not self.path.exists():return
        try:
            incoming=json.loads(self.path.read_text(encoding='utf8'))
            if not isinstance(incoming,dict) or not isinstance(incoming.get('completed',[]),list):
                raise ValueError('Invalid progress')
            merged=dict(self.data)
            merged.update(incoming)
            for key in ('xp','streak'):
                merged[key]=max(0,int(merged.get(key,0)))
            for key in ('review','last_lesson','speech_scores','study_cards','lesson_sessions','speech_support','speech_reviews'):
                if not isinstance(merged.get(key),dict):merged[key]={}
            merged['completed']=list(dict.fromkeys(str(k) for k in merged['completed']))
            for key,lower,upper in [('ui_scale',.8,1.2),('tts_speed',.5,1.4)]:
                try:
                    value=float(merged.get(key,1.))
                    merged[key]=min(upper,max(lower,value)) if math.isfinite(value) else 1.
                except (TypeError,ValueError):merged[key]=1.
            merged['motion_enabled']=merged.get('motion_enabled',True) if isinstance(merged.get('motion_enabled',True),bool) else True
            merged['motion_preset']=preset_name(merged.get('motion_preset'))
            device=merged.get('mic_device')
            if device is not None and (not isinstance(device,int) or device<0):merged['mic_device']=None
            cursor=merged['last_lesson']
            if cursor:
                try:
                    merged['last_lesson']={'key':str(cursor.get('key','')),'card':max(0,int(cursor.get('card',0)))}
                except (TypeError,ValueError):merged['last_lesson']={}
            backup=self.path.with_name('progress.before-v8.json')
            if not backup.exists():shutil.copy2(self.path,backup)
            self.data=merged
        except Exception:
            self.warning='Die Fortschrittsdatei war nicht lesbar. Die Originaldatei wurde gesichert.'
            target=self.path.with_name('progress.invalid-'+datetime.now().strftime('%Y%m%d-%H%M%S')+'.json')
            shutil.copy2(self.path,target)

    def save(self):
        tmp=self.path.with_suffix('.tmp')
        tmp.write_text(json.dumps(self.data,ensure_ascii=False,indent=2),encoding='utf8')
        tmp.replace(self.path)

    def touch_day(self):
        today=date.today();raw=self.data.get('last_active')
        if raw==today.isoformat():return
        try:previous=date.fromisoformat(raw) if raw else None
        except (ValueError,TypeError):previous=None
        self.data['streak']=self.data['streak']+1 if previous==today-timedelta(days=1) else 1
        self.data['last_active']=today.isoformat()
        self.save()

    def mark_complete(self,key,xp):
        if key not in self.data['completed']:
            self.data['completed'].append(key)
            self.data['xp']+=int(xp)
        self.touch_day();self.save()

    def set_speech_score(self,target,score,heard):
        old=self.data['speech_scores'].get(target,{})
        self.data['speech_scores'][target]={'best':max(int(old.get('best',0)),int(score)),
                                           'last':int(score),'heard':heard}
        self.save()

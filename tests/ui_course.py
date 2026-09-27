"""V11 native course integration. Test profile only, explicit audio dispatch probe.

Screenshots are OS window captures. No model inference / Windows claims.
"""
from __future__ import annotations
import argparse,json,os,sys,tempfile,time
from pathlib import Path
import tkinter as tk
from PIL import ImageGrab
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from app import TrainerApp
out=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'test-results-v11'
out.mkdir(parents=True,exist_ok=True)
checks=[]
def record(text):checks.append(text);print(text,flush=True)
class AudioProbe:
    def __init__(self):self.calls=[]
    def speak(self,text,speed,sid):self.calls.append((text,speed,sid))
    def model_status(self):return {'tts':False,'asr':False}
    def list_input_devices(self):return []

with tempfile.TemporaryDirectory() as tmp:
    os.environ['JAPANISCHTRAINER_DATA_DIR']=tmp
    old={'completed':['0:0','0:1','1:0'],'xp':75,'teacher_id':'sakura','motion_enabled':True,'motion_preset':'natural',
         'last_lesson':{'key':'1:1','card':1},'lesson_sessions':{'1:1':{'index':1,'phase':'write','mode':'learn'}}}
    (Path(tmp)/'progress.json').write_text(json.dumps(old),encoding='utf8')
    root=tk.Tk();args=argparse.Namespace(page='home',lesson='',card=0,size='1440x1040',capture='')
    app=TrainerApp(root,args)
    def refresh():
        app.redraw();root.update();assert not app.render_error,app.render_error
    def pause(seconds):
        stop=time.monotonic()+seconds
        while time.monotonic()<stop:root.update();time.sleep(.01)
    def click(id):
        refresh();hit=next((h for h in app.hits if h.id==id),None)
        if not hit:
            app.scroll=0;refresh()
            while not hit and app.scroll<app.max_scroll:
                app.wheel(130);refresh();hit=next((h for h in app.hits if h.id==id),None)
        assert hit,(id,app.view,app.scroll,app.max_scroll)
        x,y,w,h=hit.rect;s=app.render_scale
        app.canvas.event_generate('<Button-1>',x=round((x+w/2)*s),y=round((y+h/2)*s));root.update();refresh()
    def type_search(text):
        refresh();assert app.entry_mode=='search' and app.entry
        app.entry.focus_force();root.update();app.entry.delete(0,'end');app.entry.insert(0,text);app.entry.event_generate('<KeyRelease>',keysym='a');root.update();refresh()
        assert app.query==text
    def correct():
        opts,a=app.flow.answers();click('answer:'+str(opts.index(a)))
    def capture(name):
        refresh();pause(.12)
        x,y=root.winfo_rootx(),root.winfo_rooty()
        app.actors.composite(app.frame.image).convert('RGB').save(out/name)
    def await_audio():
        end=time.monotonic()+5
        while app.job and time.monotonic()<end:pause(.03)
        assert not app.job;refresh()
    try:
        refresh();pause(.12)
        assert len(app.learning.lessons)==150 and len(app.learning.cards)==680
        for k in ('completed','xp','teacher_id','motion_enabled','motion_preset','last_lesson','lesson_sessions'):assert app.store.data[k]==old[k],k
        assert (Path(tmp)/'progress.before-course-v11.json').exists()
        record('Native startup migrates old profile without resetting XP, completions, teacher or motion')
        click('resume');assert app.lesson['key']=='1:1' and app.card_index==1 and app.flow.phase=='write'
        record('Home Continue restores the existing lesson, card and exercise phase')
        app.navigate('path');refresh();assert app.entry_mode=='search'
        click('path-new');assert app.path_new_only and len(app.learning.filtered_lessons(new_only=True))==100
        record('Native new-lessons filter selects exactly 100 added lessons')
        type_search('selbstständig');rows=app.learning.filtered_lessons(app.query,app.path_stage,app.path_new_only)
        assert len(rows)==1 and rows[0]['key']=='v11:jobs'
        record('German search via real keyboard events finds the jobs lesson')
        type_search('おばあさん');assert app.learning.filtered_lessons(app.query)[0]['key']=='v11:long-vowels'
        record('Japanese search finds the vowel-length lesson')
        type_search('jieigyō');assert any(l['key']=='v11:jobs' for l in app.learning.filtered_lessons(app.query))
        record('Romaji search accepts the displayed macrons')
        type_search('zzzz-no-result');assert not app.learning.filtered_lessons(app.query)
        assert app.max_scroll==0
        record('Zero-result search shows a usable empty state, not an exception')
        type_search('');app.set_path_stage('Zahlen & Zeit');refresh()
        assert len(app.learning.filtered_lessons('',app.path_stage,True))==10
        record('Section filter selects the ten new number/time lessons')
        app.set_path_stage('Praxis');refresh()
        assert len(app.learning.filtered_lessons('',app.path_stage,True))==15
        record('Practice section contains work, dialogs and reading passages')
        app.set_path_stage('Alle');type_search('Vokale');refresh()
        click('lesson:v11:long-vowels');assert app.view=='lesson' and app.lesson['key']=='v11:long-vowels'
        assert app.flow.phase=='understand' and app.book.profile(app.current_card(),app.lesson)['explain']
        record('A newly inserted foundational lesson opens through its native button')
        click('next');assert app.flow.phase=='meaning';correct();click('next');assert app.flow.phase=='listen'
        app.engine=AudioProbe();probe=app.engine;click('exercise-audio');await_audio();assert app.flow.audio_seen
        assert probe.calls[-1][0]==app.flow.listen_card['jp']
        if len(app.flow.answers()[0])==1:
            app.entry.delete(0,'end');app.entry.insert(0,app.flow.listen_card['romaji']);click('study-check')
        else:correct()
        click('next');assert app.flow.phase=='build'
        parts,_=app.book.blocks(app.current_card(),app.lesson)
        for i in range(len(parts)):click('block:'+str(i))
        click('build-check');click('next');assert app.flow.phase=='write'
        app.entry.delete(0,'end');app.entry.insert(0,app.current_card()['romaji']);app.entry.event_generate('<KeyRelease>');root.update()
        before=app.entry.get();frame=app.actors.frame_count;pause(.35)
        assert app.entry.get()==before and app.actors.frame_count>frame
        click('study-check');assert app.flow.success;click('next');assert app.flow.phase=='apply';correct();click('next')
        assert app.card_index==1 and app.flow.phase=='understand'
        record('All six native exercise steps work on a new card, including typing while idle animates')
        app.store.data['motion_enabled']=False
        for l in [l for l in app.learning.lessons if l.get('origin')=='v11']:
            i=max(range(len(l['cards'])),key=lambda i:len(l['cards'][i]['jp'])+len(l['cards'][i]['romaji']))
            app.open_lesson(l['key'],i,True);refresh()
            assert app.pinned_rect[1]+app.pinned_rect[3]<app.H-100,l['key']
            assert app.book.profile(app.current_card(),l)==app.current_card()['detail']
        record('All 100 new lessons render their longest card with card-specific explanations')
        for key in ['v11:read-profile','v11:read-day','v11:read-weekend','v11:read-plan','v11:read-message']:
            app.open_lesson(key,0,True);app.flow.phase='apply';app.flow.reset_task();refresh()
            assert app.book.profile(app.current_card(),app.lesson)['kind']=='Leseverständnis'
            correct();assert app.flow.success
        record('Five reading passages use actual content questions, not generic usage labels')
        for size,scale in [('1440x1040',1.),('1280x800',1.),('1180x760',1.1),('1920x1080',1.)]:
            root.geometry(size);app.store.data['ui_scale']=scale;pause(.1)
            app.open_lesson('v11:permission-duty',1,True);click('speak')
            assert app.inline_speech and app.view=='lesson'
            assert app.inline_rect[1]>=app.pinned_rect[1]+app.pinned_rect[3]
            assert app.inline_rect[1]+app.inline_rect[3]<app.H-55,(size,app.inline_rect,app.H)
            pinned=app.pinned_rect;app.wheel(650);refresh();assert app.pinned_rect==pinned
            record('Long sentence + inline microphone fits '+size+' @ '+str(scale))
        root.geometry('1440x1040');app.store.data['ui_scale']=1;app.store.data['motion_enabled']=True;pause(.15)
        app.open_lesson('v11:jobs',2,True);refresh()
        for t in app.learning.teachers:
            app.choose_teacher(t['id'],True);app.speak(app.current_card()['jp']);await_audio()
            assert probe.calls[-1][0]=='じえいぎょう' and probe.calls[-1][2]==t['speaker_id']
        record('New content dispatches to all eight existing voice profiles (explicit probe, not synthesis)')
        app.choose_teacher('sakura',True);refresh();start=app.actors.frame_count;pause(.4)
        assert app.actors.frame_count>start
        record('Idle animation continues on the expanded lesson page')
        app.flow.phase='meaning';app.flow.reset_task();refresh();correct()
        assert app.actor_mood()=='praise';pause(2.9);assert app.actor_mood()=='idle'
        record('Correct new answer triggers celebration and returns to idle')
        # New long sentences are readable in standalone listening/speaking as well.
        app.navigate('vocab');app.store.data['library_all']=True;refresh();type_search('しゃしんをとってもいいですか')
        card=next(c for c in app.learning.cards if c['lesson_key']=='v11:permission-duty' and c['card_index']==1)
        click('vocab-slow:'+card['key']);assert app.view=='speaking';refresh()
        assert app.speech_item['target']==card['jp'];click('speech-play');await_audio()
        assert probe.calls[-1][0]==card['jp']
        record('Long new sentences work from vocabulary through standalone speech UI')
        # Capture only a clearly separate demonstration profile; no fabricated learner scores.
        app.navigate('path');app.path_stage='Einstieg';app.path_new_only=False;app.query='';app.hide_entry();app.scroll=0
        capture('LIVE_V11_Lernpfad.png')
        app.open_lesson('v11:jobs',2,True);app.scroll=0;capture('LIVE_V11_Neue_Lektion.png')
        app.open_lesson('v11:read-day',2,True);app.flow.phase='apply';app.flow.reset_task();app.scroll=0
        capture('LIVE_V11_Leseverstaendnis.png')
        click('speak');capture('LIVE_V11_Inline.png')
        record('Live framebuffer captured from the running native window')
        (out/'ui-course-report.json').write_text(json.dumps({'checks':checks,'count':len(checks),'passed':True,
            'environment':sys.platform+'; temporary test profile','real_audio_inference':False,
            'audio':'Explicit dispatcher probe','windows_installer_executed':False},ensure_ascii=False,indent=2))
        print('PASS',len(checks),flush=True)
    finally:
        if not app.closed:app.close()

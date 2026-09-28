"""Native V10 window tests with real pointer dispatch; explicit ASR callback probes.
All data is isolated. No microphone/model inference and no Windows binary are run.
"""
from __future__ import annotations
import os,sys,json,time,tempfile,argparse
from pathlib import Path
import tkinter as tk
import numpy as np
from PIL import Image,ImageGrab
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from app import TrainerApp
from reactions import PROFILES
from speech_engine import PronunciationResult,AudioQuality
out=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'reaction-test-results';out.mkdir(parents=True,exist_ok=True)
checks=[]
def log(name):
    checks.append(name);print(time.strftime('%H:%M:%S'),name,flush=True)
with tempfile.TemporaryDirectory() as temp:
    os.environ['JAPANISCHTRAINER_DATA_DIR']=temp
    root=tk.Tk();app=TrainerApp(root,argparse.Namespace(page='lesson',lesson='1:0',card=1,size='1440x1040',capture=''))
    def pump(secs=.05):
        end=time.monotonic()+secs
        while time.monotonic()<end:root.update();time.sleep(.007)
    def refresh():app.redraw();root.update();assert not app.render_error,app.render_error
    def click(id):
        refresh();h=next(h for h in app.hits if h.id==id);x,y,w,h0=h.rect
        app.canvas.event_generate('<Button-1>',x=round((x+w*.5)*app.render_scale),y=round((y+h0*.5)*app.render_scale))
        root.update();refresh()
    def prepare(name):
        app.choose_teacher(name,True);app.open_lesson('1:0',1,True)
        app.flow.phase='meaning';app.flow.reset_task();app.detail_open=True;app.message='';app.hover='';app.focus='';app.clear_reaction();refresh();pump(.04)
    def correct():
        opts,c=app.flow.answers();click('answer:'+str(opts.index(c)))
    def capture(name):
        refresh();root.update_idletasks();x=root.winfo_rootx();y=root.winfo_rooty()
        app.actors.composite(app.frame.image).convert('RGB').save(out/name)
    try:
        pump(.2)
        for name in PROFILES:
            prepare(name);assert app.actor_mood()=='idle'
            assert app.actors.rigs['teacher'].capabilities['closed_idle']
            capture(name+'_idle.png')
            correct();pump(.20);assert app.actor_mood()=='praise',name
            assert app.actor_feedback().teacher_id==name
            assert 'praise' in app.actors.rigs['teacher'].capabilities['expressions']
            assert 'kiko' not in app.actors.specs
            capture(name+'_richtig.png')
            log('Closed idle and real correct-answer teacher joy during an explicit explanation; no Kiko: '+name)
            seq=app.reactions.sequence;app.check_answer(app.flow.answers()[1]);assert app.reactions.sequence==seq
            app.flow.reset_task();app.clear_reaction();opts,c=app.flow.answers()
            wrong=next(i for i,v in enumerate(opts) if v!=c);click('answer:'+str(wrong));pump(.05)
            assert not app.flow.success and app.actor_mood()=='encourage',name
            log('Friendly encouragement and duplicate-answer guard: '+name)
        prepare('sakura');correct();app.choose_teacher('ren',True)
        assert app.actor_mood()=='idle';log('Teacher change resets a previous celebration')
        app.navigate('home');assert app.actor_mood()=='idle';log('Navigation cannot carry a previous reaction onto another page')
        prepare('emiri');correct();pump(2.9);assert app.actor_mood()=='idle' and not app.actor_feedback().message
        log('Joy expires automatically and dialog returns to idle')
        prepare('yuki');app.job='Vorlesen';assert app.actor_mood()=='speaking' and app.actor_feedback().amount==0
        app.recording=True;assert app.actor_mood()=='listening' and app.actor_feedback().amount==0
        app.recording=False;app.job='Spracherkennung';assert app.actor_mood()=='thinking'
        app.job='';log('Playback, recording and processing never open a talking-mouth loop')
        for name in PROFILES:
            prepare(name);app.speech_item=app.learning.speech_target(app.current_card(),app.lesson)
            q=AudioQuality('bad','TEST: bad recording, no real microphone',1,0,0,0,0,1)
            r=PronunciationResult(99,'ありがとう','ありがとう','','','TEST PROBE',quality=q,reliable=True)
            app.received_speech(r,app.speech_item['target'],app.speech_epoch)
            assert app.actor_mood()=='encourage';assert app.actor_feedback().source=='speech-uncertain'
            assert 'keine falsche Antwort' in app.actor_feedback().message
            app.clear_reaction();q=AudioQuality('ok','TEST PROBE only',1,1,.04,.04,0,1)
            r=PronunciationResult(90,'ありがとう','ありがとう','','','TEST PROBE',quality=q,reliable=True)
            app.received_speech(r,app.speech_item['target'],app.speech_epoch)
            assert app.actor_mood()=='praise';assert app.actor_feedback().source=='speech-match'
            app.clear_reaction();app.received_speech(r,app.speech_item['target'],app.speech_epoch-1)
            assert app.actor_mood()=='idle'
            log('Speech callbacks: quality gate, reliable match, stale result guard (probe): '+name)
        prepare('satoshi');app.store.data['motion_enabled']=False;refresh();pump(.2)
        correct();pump(.1);first=np.asarray(app.actors.images['teacher']).copy();count=app.actors.frame_count
        pump(.4);np.testing.assert_array_equal(first,np.asarray(app.actors.images['teacher']))
        assert app.actors.frame_count==count;log('Reduced motion changes expression once but does not animate it')
        app.store.data['motion_enabled']=True;prepare('haruto')
        app.flow.phase='listen';app.flow.reset_task();_,c=app.flow.answers();app.check_answer(c)
        assert app.actor_mood()=='idle'
        app.skip_listening();app.check_answer(c);assert app.flow.success and app.actor_mood()=='idle'
        log('Unread and explicitly skipped audio are not celebrated')
        prepare('sakura');app.flow.phase='write';app.flow.reset_task();refresh()
        assert app.entry is not None;app.entry.insert(0,'arigatoo');app.entry.event_generate('<KeyRelease>');root.update()
        app.check_learn_text();assert app.actor_mood()=='praise';entry=app.entry;value=entry.get()
        pump(.4);assert app.entry is entry and entry.get()==value
        log('Correct writing triggers joy without recreating the entry or losing typed text')
        app.navigate('writing');refresh();app.entry.delete(0,'end');app.entry.insert(0,app.write_card['romaji'])
        app.check_writing();assert app.actor_mood()=='praise';log('Standalone writing uses the same reaction logic')
        app.navigate('review');app.reveal_review();app.rate_review(True)
        assert app.actor_mood()=='praise' and app.actor_feedback().source=='review-known'
        log('Self-rated review acknowledges memory without a fabricated pronunciation score')
        prepare('sakura');click('speak');assert app.view=='lesson' and app.inline_speech
        pinned=app.pinned_rect;app.wheel(500);refresh();assert app.pinned_rect==pinned
        log('Inline speaking and pronunciation assistance stay on the lesson page')
        # UI-only figures screen captures have no simulated ASR results on screen.
        assert not app.actors.render_errors,app.actors.render_errors
        log('No actor rendering errors during the native-window session')
    finally:app.close()
report={'passed':checks,'count':len(checks),'platform':sys.platform,
        'audio':'Callback probes only. No microphone/model inference.',
        'windows':'Not executed. Installer builds the Windows executable on the target PC.',
        'captures':'Live native app framebuffer with a temporary test profile; no desktop capture.'}
(out/'reaction-ui-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('PASS',len(checks),flush=True)

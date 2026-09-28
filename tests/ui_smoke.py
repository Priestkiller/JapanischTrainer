"""V8 native-window integration tests; an explicit audio probe replaces hardware.
No microphone, model inference, Windows installer or Windows EXE is tested here.
Every test uses a temporary learner profile. Screenshots use OS window capture.
"""
import os,sys,time,tempfile,json,argparse
from pathlib import Path
import tkinter as tk
from PIL import ImageGrab,ImageChops,Image
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from app import TrainerApp
from speech_engine import PronunciationResult,AudioQuality
from study import PHASES
out=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'test-results';out.mkdir(parents=True,exist_ok=True)
class CheckLog(list):
    def append(self,item):
        super().append(item);print(time.strftime('%H:%M:%S'),item,flush=True)
checks=CheckLog()
class AudioProbe:
    def __init__(self):self.sample_rate=48000;self.calls=[];self._chunks=[];self.rec=False
    def speak(self,text,speed,sid):self.calls.append(('speak',text,speed,sid))
    def start_recording(self,device):
        self.calls.append(('record',device));self.rec=True;self._chunks=[np.full(4800,.04,dtype=np.float32)]
    def stop_recording(self):
        self.calls.append(('stop',));self.rec=False;return np.full(48000,.04,dtype=np.float32)
    def recognize_for_target(self,a,accepted,sr):
        self.calls.append(('recognize',sr,list(accepted)))
        return PronunciationResult(90,accepted[0],accepted[0],'test','test','TEST PROBE',
            quality=AudioQuality('ok','Simulierter Audiopfad, keine Sprachprüfung.',1.,1.,.04,.04,0.,1.))
    def play_recording(self,a,sr):self.calls.append(('own',sr))
    def model_status(self):return {'tts':False,'asr':False}
    def list_input_devices(self):return []
with tempfile.TemporaryDirectory() as temp:
    os.environ['JAPANISCHTRAINER_DATA_DIR']=temp
    root=tk.Tk();args=argparse.Namespace(page='home',lesson='',card=0,size='1440x1040',capture='')
    app=TrainerApp(root,args);root.update();app.redraw();root.update()
    real_engine=app.engine;probe=AudioProbe()
    def refresh():
        app.redraw();root.update();assert not app.render_error,app.render_error
    def pause(seconds):
        end=time.monotonic()+seconds
        while time.monotonic()<end:root.update();time.sleep(.012)
    def click(id,scroll=True):
        refresh()
        hit=next((h for h in app.hits if h.id==id),None)
        if not hit and scroll:
            app.scroll=0;refresh()
            while not hit and app.scroll<app.max_scroll:
                app.wheel(150);refresh();hit=next((h for h in app.hits if h.id==id),None)
        assert hit,('Missing interactive control',id,app.view,app.flow.phase,app.scroll,app.max_scroll)
        x,y,w,h=hit.rect;sc=app.render_scale
        app.canvas.event_generate('<Button-1>',x=round((x+w/2)*sc),y=round((y+h/2)*sc));root.update();refresh()
    def wait_audio():
        end=time.time()+4
        while app.job and time.time()<end:pause(.025)
        assert not app.job,'Audio callback did not finish';refresh()
    def capture(name):
        refresh();pause(.09);x=root.winfo_rootx();y=root.winfo_rooty()
        im=app.actors.composite(app.frame.image).convert('RGB')
        im.save(out/name);return im
    def correct_option():
        opts,correct=app.flow.answers();click('answer:'+str(opts.index(correct)))
    try:
        for page in ['home','path','lesson','speaking','teachers','listening','vocab','writing','grammar','kanji','review','progress','settings','complete']:
            app.navigate(page);refresh();assert len(app.hits)>10,page
            checks.append('Live page renders: '+page)
        app.navigate('teachers');click('teacher:aiko');assert app.preview_teacher=='aiko' and app.store.data['teacher_id']=='sakura'
        click('teacher-select');assert app.store.data['teacher_id']=='aiko';checks.append('Teacher preview & committed choice preserved')
        app.engine=probe;app.speak('ありがとう',teacher_id='aiko');wait_audio();assert probe.calls[-1][3]==0
        checks.append('Existing voice profile dispatch (probe, not actual TTS)')
        app.open_lesson('1:0',1,True);refresh();pinned=app.pinned_rect;phase=app.flow.phase;click('speak')
        assert app.view=='lesson' and app.inline_speech and app.pinned_rect[:2]==pinned[:2] and app.flow.phase==phase
        pinned=app.pinned_rect # The speaking teacher takes an explicit column; the task alone uses full width.
        checks.append('Jetzt sprechen expands inline without page or lesson-phase change')
        for delta in (600,-200,1600,-3000):
            app.wheel(delta);refresh();assert app.pinned_rect==pinned;assert app.inline_rect[1]>pinned[1]+pinned[3]
        checks.append('Word, Romaji, meaning and pronunciation aid stay pinned while lower panel scrolls')
        def denied(device):raise RuntimeError('Test: Mikrofonzugriff verweigert')
        original_start=probe.start_recording;probe.start_recording=denied;click('record')
        assert not app.recording and app.speech_error and app.view=='lesson';assert not app.store.data['speech_scores']
        probe.start_recording=original_start;checks.append('Denied microphone remains inline; no success awarded')
        click('record');assert app.recording and app.view=='lesson';assert app.flow.phase==phase
        click('record');wait_audio();assert app.result and app.view=='lesson';assert app.flow.phase==phase
        assert probe.calls[-1][0]=='recognize';assert app.flow.metrics()['speech_attempts']==1
        checks.append('Start, stop, result and progress retention via explicit recording probe')
        click('play-own');wait_audio();assert probe.calls[-1][0]=='own';checks.append('Own recording replay dispatch')
        prior=len(probe.calls);click('record');app.canvas.event_generate('<KeyPress-Escape>');root.update();refresh()
        assert not app.recording;assert not any(c[0]=='recognize' for c in probe.calls[prior:]);checks.append('Escape cancels recording without recognition')
        old=app.result;epoch=app.speech_epoch;app.speech_epoch+=1
        fake=PronunciationResult(0,'STALE','ありがとう','','','PROBE',reliable=False)
        app.received_speech(fake,'ありがとう',epoch);assert app.result is old;checks.append('Late recognition callback cannot overwrite a newer speech context')
        click('speech-skip');assert not app.inline_speech;assert app.flow.metrics()['speech_skips']==1;checks.append('Explicit speech skip is separate from success')
        # Run all six steps of the Danke card with actual mouse and keyboard events.
        app.open_lesson('1:0',1,True);click('next');assert app.flow.phase=='meaning'
        opts,correct=app.flow.answers();wrong=next(i for i,v in enumerate(opts) if v!=correct);click('answer:'+str(wrong));assert not app.flow.success
        assert not any(h.id=='next' for h in app.hits);correct_option();click('next');assert app.flow.phase=='listen'
        click('exercise-audio');wait_audio();assert app.flow.audio_seen;correct_option();click('next');assert app.flow.phase=='build'
        parts,_=app.book.blocks(app.current_card(),app.lesson)
        for i in range(len(parts)):click('block:'+str(i))
        click('build-check');assert app.flow.success;click('next');assert app.flow.phase=='write'
        refresh();assert app.entry and app.entry_mode=='study'
        app.entry.delete(0,'end');app.entry.insert(0,'arigatoo');app.entry.event_generate('<KeyRelease>');root.update()
        app.entry.focus_set();pause(.3);before=app.entry.get();count=app.actors.frame_count;pause(.35)
        assert app.entry.get()==before and app.actors.frame_count==count and not app.actor_specs
        app.entry.event_generate('<KeyPress-Return>');root.update();refresh();assert app.flow.success
        click('next');assert app.flow.phase=='apply';correct_option();click('next');assert app.card_index==2 and app.flow.phase=='understand'
        checks.append('All six guided steps work through real pointer and keyboard input')
        checks.append('Character animation does not destroy typed text, caret or exercise state')
        app.open_lesson('0:1',force=True)
        for _ in range(90):
            if app.view=='complete':break
            f=app.flow
            if f.phase=='understand' and f.mode!='recap':click('next');continue
            if f.phase=='write' and f.mode!='recap':f.check_write(f.card['romaji'])
            elif f.phase=='build' and f.mode!='recap' and app.book.blocks(f.card,f.lesson)[0]:
                f.tokens=list(range(len(app.book.blocks(f.card,f.lesson)[0])));f.check_build()
            else:f.audio_seen=True;_,v=f.answers();f.choose(v)
            refresh();click('next')
        assert app.view=='complete' and '0:1' in app.store.data['completed'];checks.append('Full lesson completes only after all cards plus recap; XP saved once')
        before_xp=app.store.data['xp'];app.store.mark_complete('0:1',25);assert app.store.data['xp']==before_xp
        app.navigate('settings');refresh();app.store.data['motion_enabled']=False;app.request_draw();refresh();pause(.4);count=app.actors.frame_count;pause(.4);assert app.actors.frame_count==count
        app.store.data['motion_enabled']=True;refresh();checks.append('Reduced-motion setting freezes sprites without changing UI')
        app.engine=real_engine;app.choose_teacher('sakura',True);app.message=''
        for size,scale in [('1440x1040',1.),('1280x800',1.),('1180x760',1.),('1920x1080',1.),('1180x760',1.1)]:
            app.store.data['ui_scale']=scale;root.geometry(size);root.update();app.open_lesson('1:0',1,True);click('speak');refresh()
            x,y,w,h=app.pinned_rect;ix,iy,iw,ih=app.inline_rect
            assert y+h<iy and iy+ih<app.H-50,(size,scale,app.pinned_rect,app.inline_rect,app.H)
            old=app.pinned_rect;app.wheel(1000);refresh();assert old==app.pinned_rect
            for hit in app.hits:
                x0,y0,w0,h0=hit.rect
                assert y0+h0<=app.H+1,(size,hit.id,hit.rect,app.H)
            checks.append('Pinned inline layout fits '+size+' @ '+str(scale))
        # JT_SKIP_MEDIA leaves the interaction suite intact; use record_idle.py
        # for an independent real-time operating-system capture.
        if os.environ.get('JT_SKIP_MEDIA') != '1':
            # Show real screenshots of the new controls without fabricated recognition output.
            app.store.data['ui_scale']=1.;app.store.data['motion_enabled']=True;root.geometry('1440x1040');root.update()
            app.open_lesson('1:0',1,True);app.message='';app.hover='';app.focus='';capture('LIVE_V8_EXPLANATION.png')
            click('speak');app.speech_error='';app.result=None;app.last_audio=None;app.hover='';app.focus='';capture('LIVE_V8_INLINE.png')
            app.inline_speech=False;app.flow.phase='build';app.flow.reset_task();app.scroll=0;capture('LIVE_V8_BLOCKS.png')
            app.flow.phase='write';app.flow.reset_task();app.scroll=0;capture('LIVE_V8_WRITING.png')
            app.navigate('teachers');app.message='';capture('LIVE_V8_TEACHERS.png')
            app.open_lesson('1:0',1,True);app.inline_speech=True;app.speech_item=app.learning.speech_target(app.current_card(),app.lesson);app.message='';refresh()
            # Recorded native application frames, not a generated mockup or invented poses.
            frames=[]
            for i in range(32):
                pause(.14);im=app.actors.composite(app.frame.image).convert('RGB')
                im.thumbnail((1000,730),Image.Resampling.LANCZOS);frames.append(im.convert('P',palette=Image.Palette.ADAPTIVE,colors=128))
            frames[0].save(out/'LIVE_V8_IDLE.gif',save_all=True,append_images=frames[1:],duration=145,loop=0,optimize=False)
            checks.append('Live application framebuffer and idle animation captured from the running native app')
    finally:app.close()
report={'passed':checks,'count':len(checks),'environment':sys.platform,
        'audio_inference':'NOT EXECUTED: AudioProbe checks dispatch/callbacks/errors only.',
        'windows_exe':'NOT EXECUTED: source and installation package only.',
        'screenshots': 'Skipped in this run; recorded separately.' if os.environ.get('JT_SKIP_MEDIA')=='1' else 'Live application framebuffer with isolated test profile; no desktop capture or generated mockups.'}
(out/'ui-test-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('\n'.join(checks));print('PASS:',len(checks),'checks')

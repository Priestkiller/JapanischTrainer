"""Real native-window regression test: idle -> correct click -> idle, no audio.
Run in short groups using --teachers; profiles never touch the user's progress.
"""
from __future__ import annotations
import argparse, json, os, sys, tempfile, time
from pathlib import Path
import tkinter as tk
import numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from app import TrainerApp
from reactions import PROFILES
from storage import ProgressStore

parser=argparse.ArgumentParser()
parser.add_argument('output');parser.add_argument('--teachers',default=','.join(PROFILES))
args=parser.parse_args();out=Path(args.output);out.parent.mkdir(parents=True,exist_ok=True)
names=args.teachers.split(',');checks=[];metrics=[]
def log(text):checks.append(text);print(text,flush=True)
with tempfile.TemporaryDirectory() as temp:
    os.environ['JAPANISCHTRAINER_DATA_DIR']=temp
    root=tk.Tk();app=TrainerApp(root,argparse.Namespace(page='lesson',lesson='1:0',card=1,size='1440x1040',capture=''))
    def pump(seconds):
        end=time.monotonic()+seconds
        while time.monotonic()<end:root.update();time.sleep(.009)
    def refresh():app.redraw();root.update();assert not app.render_error,app.render_error
    def click(id):
        refresh();h=next(h for h in app.hits if h.id==id)
        x,y,w,h0=h.rect;s=app.render_scale
        app.canvas.event_generate('<Button-1>',x=round((x+w/2)*s),y=round((y+h0/2)*s));root.update()
    try:
        pump(.18)
        for name in names:
            assert name in PROFILES
            app.choose_teacher(name,True);app.open_lesson('1:0',1,True)
            app.flow.phase='meaning';app.flow.reset_task();app.message='';app.hover='';app.focus='';refresh()
            assert app.actor_mood()=='idle' and app.actors.rigs['teacher'].capabilities['closed_idle']
            before=np.asarray(app.actors.images['teacher']).copy();tick=app.actors.clock.time;pump(.50)
            after=np.asarray(app.actors.images['teacher']).copy()
            changed=int(np.count_nonzero(np.any(before!=after,axis=2)))
            assert changed>30,(name,changed)
            assert app.actors.clock.time>tick
            log(name+': visible idle continues with closed-mouth base')
            opts,target=app.flow.answers();click('answer:'+str(opts.index(target)));pump(.24)
            assert app.flow.success and app.actor_mood()=='praise'
            tick=app.actors.clock.time;pump(.23)
            assert app.actors.clock.time>tick
            log(name+': real correct-answer click adds joy without stopping idle time')
            pump(2.42);assert app.actor_mood()=='idle'
            before=np.asarray(app.actors.images['teacher']).copy();tick=app.actors.clock.time;pump(.46)
            assert app.actors.clock.time>tick
            assert np.any(before!=np.asarray(app.actors.images['teacher']))
            assert app.actors.rigs['teacher'].capabilities['closed_idle']
            log(name+': reaction ends; animated closed-mouth idle keeps running')
            metrics.append({'teacher':name,'idle_pixels_changed_in_half_second':changed,
                            'mean_actor_render_ms':round(float(np.mean(app.actors.render_ms)),2)})
        # Test preference via actual pointer event, then return to the lesson.
        app.navigate('settings');app.message='';refresh()
        old=app.store.data.get('motion_preset');click('setting:4')
        assert app.store.data['motion_preset']!=old
        assert ProgressStore().data['motion_preset']==app.store.data['motion_preset']
        app.store.data['motion_preset']='natural';app.store.save();app.navigate('lesson');refresh()
        log('Motion-preset button changes and saves the real preference')
        tick=app.actors.clock.time;root.withdraw();pump(.30);paused=app.actors.clock.time
        pump(.30);assert app.actors.clock.time==paused
        root.deiconify();pump(.06);assert app.actors.clock.time-paused<.15
        log('Hidden window pauses visual time; restoring it does not skip the idle loop')
        app.store.data['motion_enabled']=False;refresh();pump(.36)
        frames=app.actors.frame_count;before=np.asarray(app.actors.images['teacher']).copy();pump(.36)
        assert app.actors.frame_count==frames
        np.testing.assert_array_equal(before,np.asarray(app.actors.images['teacher']))
        app.store.data['motion_enabled']=True;refresh();pump(.22)
        assert app.actors.frame_count>frames
        log('Motion off is static; motion on resumes without changing the mouth state')
        assert not app.actors.render_errors,app.actors.render_errors
        log('No actor-render or UI-render exceptions')
    finally:app.close()
report={'passed':checks,'count':len(checks),'metrics':metrics,'environment':sys.platform,
        'window':'Native Tk/Pillow application; temporary isolated profile',
        'audio':'NOT EXECUTED: no TTS, microphone or ASR inference',
        'windows_exe':'NOT EXECUTED: Windows build/install not tested here'}
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print('PASS:',len(checks),'checks',flush=True)

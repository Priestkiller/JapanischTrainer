"""Real Windows widgets with isolated profiles; deliberately simulated capture errors."""
import argparse,json,os,sys,tempfile,time,tkinter as tk
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from PIL import ImageGrab
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from app import TrainerApp
from speech_support import SpeechSupport
out=ROOT/'validation/speech-ui-windows';out.mkdir(parents=True,exist_ok=True)
report={'passed':False,'nativeWindows':True,'simulatedCaptureErrors':True,'humanMicrophone':False,'sizes':[]}
with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':tmp}):
 root=tk.Tk();app=TrainerApp(root,argparse.Namespace(page='home',lesson='',card=0,size='1440x1040',capture=''))
 def render():app.redraw();root.update();assert not app.render_error,app.render_error
 def capture(name):root.lift();root.update();ImageGrab.grab(window=root.winfo_id()).save(out/(name+'.png'))
 def hit(identity):
  render();h=next((h for h in app.hits if h.id==identity),None)
  if not h and identity.startswith('support-'):
   for _ in range(30):
    h=next((h for h in app.hits if h.id==identity),None)
    if h:break
    down=next((h for h in app.hits if h.id=='support-down'),None)
    if not down:break
    down.action();render()
  assert h,identity
  x,y,w,hg=h.rect;assert x>=0 and y>=0 and x+w<=app.W+1 and y+hg<=app.H+1,(identity,h.rect,app.W,app.H)
  h.action();render()
 try:
  app.store.data['motion_enabled']=False
  for size in ['1440x1040','1080x700','1280x800']:
   root.geometry(size);root.update();app.open_lesson('0:0',0,True);render();app.current_speech_support().new_round();hit('speak');support=app.current_speech_support()
   with patch.object(app.engine,'start_recording',side_effect=RuntimeError('Simulierter technischer Mikrofonfehler')):
    for i in range(3):hit('record');assert support.data['failures']==i+1;assert support.unlocked==(i==2)
   assert app.flow.phase=='understand' and not app.flow.success;assert app.store.data['xp']==0 and not app.store.data['speech_scores']
   assert SpeechSupport(app.store,support.key).data['failures']==3
   capture('third-'+size);hit('speech-help');hit('support-prepare');app.speech_help_offset=0;render();deck=app.speech_help_deck();wrong=next(c for c in deck['options'] if c['id']!=deck['correct']);hit('support-choice:'+wrong['id']);hit('support-confirm');assert not support.data['assisted'];assert 'Noch nicht' in support.data['feedback']
   app.speech_help_offset=0;render();hit('support-choice:'+deck['correct']);capture('selection-'+size);hit('support-confirm');assert support.data['assisted'];assert app.flow.metrics()['last_speech_outcome']=='selection';assert not app.store.data['speech_scores'];assert app.actor_feedback().source=='speech-assisted'
   # The next step is comprehension, even without any accepted spoken result.
   app.next_card();render();assert app.flow.phase=='meaning';assert not app.actor_specs
   capture('meaning-'+size);report['sizes'].append(size)
  app.open_lesson('0:0',0,True);f=app.flow;f.mode='recap';f.phase='meaning';f.recap=[0];f.recap_total=5;f.recap_passed=4;f.success=True;app.next_card();render();assert app.view=='complete';xp=app.store.data['xp'];assert xp>0
  assert any(a.role=='mascot' for a in app.actor_specs);assert not app.figures_moving();capture('kiko-complete');render();assert app.store.data['xp']==xp;assert next(h for h in app.hits if h.id=='complete-next');hit('complete-path');assert app.store.data['xp']==xp
  report['passed']=True;print('PASS Windows speech assistance',report['sizes'])
 finally:app.close();(out/'report.json').write_text(json.dumps(report,indent=2),'utf8')

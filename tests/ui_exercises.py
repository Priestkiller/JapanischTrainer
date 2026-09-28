"""Real native Tk rendering/actions. Synthetic audio events, no microphone claim."""
import argparse,json,os,sys,tempfile,tkinter as tk
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
from PIL import ImageGrab
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from app import TrainerApp
from tests.test_exercises import solve
out=ROOT/'validation/exercises-ui';out.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':tmp,'JT_SKIP_MEDIA':'1'}):
 root=tk.Tk();app=TrainerApp(root,argparse.Namespace(page='home',lesson='',card=0,size='1440x1040',capture=''))
 app.store.data['motion_enabled']=False;checks=[]
 def render():app.redraw();root.update();assert not app.render_error,app.render_error
 def capture(name):
  root.lift();root.update();ImageGrab.grab(window=root.winfo_id()).save(out/(name+'.png'))
 def click(identity):
  for scroll in range(0,int(app.max_scroll)+600,250):
   app.scroll=min(scroll,app.max_scroll);render();hit=next((h for h in app.hits if h.id==identity),None)
   if hit:
    x,y,w,h=hit.rect;app.on_click(SimpleNamespace(x=(x+w/2)*app.render_scale,y=(y+h/2)*app.render_scale));render();return
  raise AssertionError('Unreachable: '+identity)
 try:
  for key in app.exercise_book.packs:
   app.open_lesson(key,0,True);render();click('exercise-round');assert app.view=='exercises';assert app.exercise_round.state['stage']=='intro';click('ex-next');r=app.exercise_round
   assert r.state['stage']=='main';checks.append(key)
   if key in ('5:0','v11:read-plan'):
    for tid in r.state['queue']:
     assert r.task['id']==tid
     family=r.task['family'];render()
     if family=='hear_gap':
      for scroll in range(0,int(app.max_scroll)+500,180):
       app.scroll=min(scroll,app.max_scroll);render()
       if app.entry:break
      assert app.entry;app.entry.insert(0,'mi');root.update();app.exercise_help();render();assert r.answer['text']=='mi';app.exercise_help();render()
     else:click('ex-help');assert r.answer['help']>=1;assert not r.answer['success'];click('ex-help')
     if family!='hear_gap':app.scroll=0
     render();capture(family)
     t=r.task
     if family in ('echo','recall'):assert solve(r) # explicit synthetic speech result
     else:
      if family=='pairs':
       # Replay completion is synthetic; selections/checking are actual UI actions.
       for pair in t['pairs']:
        r.heard(pair['id'])
        with patch.object(app,'exercise_audio'):click('ex-pair-left-'+pair['id'])
        click('ex-pair-right-'+pair['id'])
      elif family in ('read','choice_gap'):click('ex-choice-'+t['answers'][0])
      elif family=='hear_gap':
       r.heard();app.scroll=0;render()
       while not app.entry:app.wheel(120);render()
       app.focus='';app.on_key(SimpleNamespace(widget=app.canvas,keysym='Tab',state=0,char=''));root.update();assert app.focus=='native-input'
       app.entry.delete(0,'end');app.entry.insert(0,t['answers'][0]);root.update()
      else:
       pool=list(t['tokens'])
       for j,word in enumerate(t['solutions'][0]):
        token=next(v for v in pool if v['text']==word);pool.remove(token)
        if family=='multi_gap':click('ex-slot-'+str(j))
        click('ex-token-'+token['id'])
      click('ex-check');assert r.answer['success'],t['id']
     render();click('ex-next')
    assert r.state['stage']=='complete'
   app.exercise_return();render();assert app.view=='lesson';assert app.flow.phase=='understand'
  app.open_lesson('v11:read-plan',0,True);app.open_exercises();r=app.exercise_round;r.restart();r.start();r.state['index']=next(i for i,k in enumerate(r.state['queue']) if r.book.tasks[k]['family']=='read');r.state['task']={};r.sanitize();app.scroll=0;render();capture('read')
  for size in ['1080x700','1280x800','1920x1080']:
   root.geometry(size);root.update();render();click('ex-help');render();capture('window-'+size);click('ex-help')
  assert app.store.data['xp']==0 and app.store.data['completed']==[]
  (out/'report.json').write_text(json.dumps({'passed':True,'lesson_entry_points':checks,'full_rounds':['5:0','v11:read-plan'],'native_window':True,'microphone':False,'simulated_audio_results':True,'native_task_controls':True,'keyboard_focus':True},ensure_ascii=False,indent=2),'utf8')
  print('PASS native Windows:',len(checks),'entry points, full round, help and preserved input')
 finally:app.close()

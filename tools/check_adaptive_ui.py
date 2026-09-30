"""Real Tk/Pillow controls, isolated profiles; audio callbacks simulated."""
import json,os,sys,tempfile,tkinter as tk
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R))
from app import TrainerApp
out=R/'validation/native-1111';out.mkdir(parents=True,exist_ok=True)
report={'passed':False,'microphone':False,'sizes':[]}
for size in ['1440x1040','1080x700']:
 with tempfile.TemporaryDirectory() as profile,patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':profile}):
  root=tk.Tk();app=TrainerApp(root,SimpleNamespace(page='home',lesson='',card=0,size=size,capture=''))
  def draw(name):
   root.update();app.redraw();root.update_idletasks();assert not app.render_error,(name,app.render_error)
   app.frame.image.save(out/f'{name}-{size}.png')
  def click(name):
   h=next(h for h in app.hits if h.id==name);h.action();draw(name)
  try:
   app.navigate('daily');draw('daily');click('daily-intro');click('daily-next');click('daily-intro');click('daily-next');assert app.store.data['xp']==0 and not app.store.data['completed']
   app.navigate('practice_lab');draw('practice');card=app.learning.cards[0];app.trace_open(card);draw('trace')
   x,y,w,h=app.trace_box;app.trace_event(SimpleNamespace(x=(x+20)*app.render_scale,y=(y+20)*app.render_scale),True);app.trace_event(SimpleNamespace(x=(x+70)*app.render_scale,y=(y+100)*app.render_scale));draw('trace-drawn');assert len(app.trace_strokes[0])==2
   app.practice_back();app.store.data['completed'].append('v11:dialog-cafe');app.store.data['xp']=777;story=app.practice_data()['stories'][0];app.practice_open(story);draw('story');app.practice_choose('Ein Kaffee');assert not app.practice_success
   app.practice_heard=True;app.practice_choose('Ein Tee');assert app.practice_help_used;app.practice_choose('Ein Kaffee');app.practice_next();app.practice_choose(story['questions'][1]['correct']);app.practice_next();draw('story-done');assert app.store.data['adaptive']['milestones'][story['id']]['mode']=='supported';assert app.store.data['xp']==777
   app.navigate('daily');p=app.daily_plan();key=card['key'];p['tasks']=[dict(id='ui-write',card=key,skill='write')];p['done']=[];app.daily_pick();draw('write');assert app.entry
   app.entry.insert(0,card['romaji']);app.daily_write();draw('write-done');assert app.daily_success
   app.navigate('speech_lab');draw('speech-lab');app.lab_result={'results':[dict(model='sensevoice',text='あ',match=True,loadMs=10,decodeMs=20)],'confirmation':'unconfirmed'};app.lab_rows.append(app.lab_result);app.lab_confirm('as_requested');draw('speech-result');assert app.store.data['xp']==777
   app.store.save();report['sizes'].append(dict(size=size,passed=True,progressPreserved=True))
  finally:
   for task in root.tk.call('after','info'):root.after_cancel(task)
   app.close()
report['passed']=True;(out/'report.json').write_text(json.dumps(report,indent=2),'utf8');print(report)

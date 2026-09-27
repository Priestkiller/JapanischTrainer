"""Native Tk course/help/error checks, isolated profile, no microphone claim."""
import argparse,json,os,sys,tempfile
from pathlib import Path
from unittest.mock import patch
import tkinter as tk
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from app import TrainerApp
from ui_renderer import Surface
PACKAGE=int(os.environ.get('JT_CONTENT_PACKAGE','2'))
if PACKAGE==4:
 from tools.upgrade_package4 import GUIDES
elif PACKAGE==3:
 from tools.upgrade_package3 import GUIDES
else:
 from tools.upgrade_package2 import GUIDES
out=ROOT/f'validation/package{PACKAGE}-ui';out.mkdir(parents=True,exist_ok=True)
checks=[];text=[]
old_text=Surface.text;old_para=Surface.paragraph
def text_probe(self,x,y,value,*a,**kw):text.append(str(value));return old_text(self,x,y,value,*a,**kw)
def para_probe(self,x,y,value,*a,**kw):text.append(str(value));return old_para(self,x,y,value,*a,**kw)
with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':tmp,'JT_SKIP_MEDIA':'1'}):
 root=tk.Tk();app=TrainerApp(root,argparse.Namespace(page='home',lesson='',card=0,size='1440x1040',capture=''))
 app.store.data['motion_enabled']=False
 def render():text.clear();app.redraw();root.update();assert not app.render_error,app.render_error
 try:
  with patch.object(Surface,'text',text_probe),patch.object(Surface,'paragraph',para_probe):
   for key in GUIDES:
    app.open_lesson(key,0,True);render();assert app.pinned_rect and app.lesson['goal'] in text,key
    assert app.lesson['study_guide']['points'][1] in text,key
    for phase in ['meaning','listen','build','write','apply']:
     app.flow.phase=phase;app.flow.reset_task();app.scroll=0;render();assert app.pinned_rect is None,(key,phase)
     assert not any(v.startswith('Bedeutung: ') for v in text),(key,phase)
     if phase=='write':assert app.flow.card['romaji'] not in text,key
    q=app.flow.card['detail']['scenario'];app.flow.choose(q['wrong'][0]);render()
    assert q['feedback'][q['wrong'][0]] in app.flow.feedback;assert app.flow.feedback in text,key
    assert not app.flow.success and app.flow.advance()=='blocked';before=app.flow.metrics().get('hints',0)
    app.show_explanation();render();assert app.pinned_rect;assert app.flow.metrics()['hints']==before+1
    assert not app.flow.success and app.flow.advance()=='blocked'
    app.show_explanation();render();assert app.pinned_rect is None
    if key in ['15:0','v11:positions','v11:dialog-directions','v11:read-profile','6:0','v11:checkout','v11:dialog-cafe','v11:clock-hours','v11:dialog-weekend','v11:read-plan']:
     app.actors.composite(app.frame.image).convert('RGB').save(out/(key.replace(':','-')+'.png'))
    checks.append(key)
   if PACKAGE==4:
    app.open_lesson('12:0',4,True);render()
    assert any('drei Paaren' in v for v in text)
    assert any('Miniübung 1' in v for v in text)
    app.flow.phase='write';app.flow.reset_task();render();assert app.pinned_rect is None
    app.flow.check_write('go roku');render();assert not app.flow.success and app.flow.advance()=='blocked'
    app.show_explanation();render();assert app.pinned_rect and not app.flow.success
    app.actors.composite(app.frame.image).convert('RGB').save(out/'numbers-preparation.png')
   app.open_lesson('13:0',0,True);app.flow.phase='listen';app.flow.reset_task();app.flow.audio_seen=True;render()
   assert app.entry;app.entry.delete(0,'end');app.entry.insert(0,'nan');app.check_learn_text();render();assert app.flow.success
   assert app.store.data['xp']==0 and app.store.data['completed']==[]
  (out/'report.json').write_text(json.dumps({'passed':True,'lessons':checks,'checks':['teaching','five retrieval phases hide template','wrong answer explanation','help does not advance','nani/nan listening alias'],'real_audio':False},ensure_ascii=False,indent=2),'utf8')
  print('PASS:',len(checks),'lessons, five retrieval phases, feedback, help and alias; no XP awarded')
 finally:app.close()

"""Native teaching/answer-leak checks with an isolated profile, no audio inference."""
import argparse,json,os,sys,tempfile
from pathlib import Path
from unittest.mock import patch
import tkinter as tk
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from app import TrainerApp
from ui_renderer import Surface

out=ROOT/'validation/foundations-ui';out.mkdir(parents=True,exist_ok=True)
checks=[];text=[]
original_text=Surface.text;original_paragraph=Surface.paragraph
def track_text(self,x,y,value,*args,**kwargs):
    text.append(str(value));return original_text(self,x,y,value,*args,**kwargs)
def track_paragraph(self,x,y,value,*args,**kwargs):
    text.append(str(value));return original_paragraph(self,x,y,value,*args,**kwargs)

with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'JAPANISCHTRAINER_DATA_DIR':tmp}):
    root=tk.Tk();app=TrainerApp(root,argparse.Namespace(page='home',lesson='',card=0,size='1440x1040',capture=''))
    app.store.data['motion_enabled']=False
    def render():
        text.clear();app.redraw();root.update();assert not app.render_error,app.render_error
    def capture(name):app.actors.composite(app.frame.image).convert('RGB').save(out/name)
    try:
        with patch.object(Surface,'text',track_text),patch.object(Surface,'paragraph',track_paragraph):
            app.open_lesson('v11:long-vowels',0,True);render()
            assert app.pinned_rect and 'Dein Lernziel' in text and 'Lernhilfe 1' in text
            capture('windows-lesson-guide.png');checks.append('New lesson guide and full target appear in the teaching step')
            for phase in ['meaning','listen','build','write','apply']:
                app.flow.phase=phase;app.flow.reset_task();app.scroll=0;render()
                assert app.pinned_rect is None,phase
                assert not any(h.id in ('speak','listen','slow') for h in app.hits),phase
                assert not any(v.startswith('Bedeutung: ') for v in text),phase
                if phase=='write':assert app.flow.card['romaji'] not in text
                if phase=='meaning':assert 'Beispielsatz' not in text
                capture('windows-'+phase+'.png')
            checks.append('Five retrieval steps hide full target, transliteration and premature example answers')
            app.flow.phase='write';app.flow.reset_task();app.show_explanation();render()
            assert app.pinned_rect and app.flow.metrics()['hints']==1 and not app.flow.success
            assert app.flow.advance()=='blocked';capture('windows-explicit-help.png')
            app.show_explanation();render();assert app.pinned_rect is None
            checks.append('Explicit help is counted and cannot solve or advance a task')
            app.open_lesson('v11:read-day',0,True);app.flow.phase='apply';app.flow.reset_task();render()
            assert app.flow.card['jp'] in text
            assert not any(v.startswith('Bedeutung: ') for v in text)
            capture('windows-reading.png');checks.append('Reading comprehension retains the Japanese passage without its translation')
            app.flow.mode='recap';app.flow.phase='meaning';app.flow.reset_task();render()
            assert app.pinned_rect is None;checks.append('Recap also hides the answer template')
        (out/'report.json').write_text(json.dumps({'passed':True,'checks':checks,'real_audio':False},ensure_ascii=False,indent=2),'utf-8')
        print('PASS',len(checks),*checks,sep='\n')
    finally:app.close()

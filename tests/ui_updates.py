"""Real native settings button and update dialog; controlled offline response."""
import argparse,json,os,sys,tempfile,time
from pathlib import Path
from unittest.mock import patch
import tkinter as tk
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from app import TrainerApp
out=ROOT/'validation/ui-updates';out.mkdir(parents=True,exist_ok=True)
with tempfile.TemporaryDirectory() as tmp,patch('updater.open_url',side_effect=OSError('offline test')):
    os.environ['JAPANISCHTRAINER_DATA_DIR']=tmp
    root=tk.Tk();app=TrainerApp(root,argparse.Namespace(page='settings',lesson='',card=0,size='1280x860',capture=''))
    try:
        root.update();app.redraw();root.update();app.scroll=app.max_scroll;app.redraw();root.update()
        hit=next(h for h in app.hits if h.id=='setting:9')
        x,y,w,h=hit.rect;s=app.render_scale
        app.canvas.event_generate('<Button-1>',x=round((x+w/2)*s),y=round((y+h/2)*s));root.update()
        assert app.update_window.winfo_exists()
        end=time.monotonic()+1.5
        while time.monotonic()<end:root.update();time.sleep(.02)
        labels=[child.cget('text') for child in app.update_window.winfo_children() if isinstance(child,tk.Label)]
        assert any('nicht erreichbar' in text for text in labels),labels
        assert not any('ist aktuell' in text for text in labels)
        app.actors.composite(app.frame.image).convert('RGB').save(out/'settings-update-button.png')
        (out/'report.json').write_text(json.dumps({'passed':True,'button_click':True,'offline_error_visible':True,'profile':'temporary'}),encoding='utf8')
    finally:app.close()
print('PASS: native Update-Schaltfläche und sichtbare Offline-Fehlermeldung')

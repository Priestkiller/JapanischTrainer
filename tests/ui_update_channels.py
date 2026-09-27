"""Native Tk update controls with isolated storage and controlled network results."""
import json, os, sys, tempfile, time, tkinter as tk
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import update_ui
from PIL import ImageGrab

out = ROOT/'validation/ui-update-channels'; out.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory() as profile:
    os.environ['JAPANISCHTRAINER_DATA_DIR'] = profile
    root = tk.Tk(); root.geometry('200x100'); root.update()
    app = SimpleNamespace(root=root, closed=False, recording=False, job=None)
    calls=[]
    def check(folder, current, channel='stable'):
        calls.append(channel)
        return (b'test-signature', {'version':'11.0.5', 'notes':'Kontrollierte Testversion'}) if channel=='test' else None
    def buttons(parent):
        return [c for child in parent.winfo_children() for c in ([child] if isinstance(child, tk.Button) else buttons(child))]
    def button(text):return next(b for b in buttons(app.update_window) if b.cget('text')==text)
    def spin():
        end=time.monotonic()+.35
        while time.monotonic()<end:root.update();time.sleep(.01)
    with patch('update_ui.check_update',side_effect=check), patch('update_ui.download_update',return_value=Path(profile)/'update.zip') as download:
        update_ui.show_updates(app,ROOT,'11.0.4');spin()
        assert calls==['stable']
        button('Testversion suchen').invoke()
        assert str(button('Nach Updates suchen')['state'])=='disabled'
        spin();assert calls==['stable','test']
        button('Testversion herunterladen').invoke();spin()
        download.assert_called_once();assert download.call_args.args[1]==b'test-signature'
        assert button('Update einspielen und neu starten').winfo_ismapped()
        button('Nach Updates suchen').invoke();spin()
        assert not button('Update einspielen und neu starten').winfo_ismapped()
        assert calls==['stable','test','stable']
        button('Testversion suchen').invoke();spin()
        w=app.update_window
        import ctypes
        hwnd=ctypes.windll.user32.GetParent(w.winfo_id())
        ImageGrab.grab(window=hwnd).save(out/'test-channel.png')
        app.closed=True;w.destroy();root.destroy()
    assert not list(Path(profile).glob('progress*.json'))
(out/'report.json').write_text(json.dumps({'passed':True,'native_ui':True,'network':'controlled','separate_test_profile':True,'check_download_switch_clears_install':True}),encoding='utf8')
print('PASS native test update selection, download and channel reset')

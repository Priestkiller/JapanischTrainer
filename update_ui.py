"""Native update dialog; UI stays responsive during network and disk work."""
import queue
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import uuid
from updater import check_update, download_update, launch_worker
from storage import data_dir


def show_updates(app, root_path, current):
    existing = getattr(app, 'update_window', None)
    if existing is not None and existing.winfo_exists():
        existing.lift()
        return
    win = tk.Toplevel(app.root)
    app.update_window = win
    win.title('JapanischTrainer – Updates')
    win.geometry('640x410')
    win.minsize(520, 340)
    win.transient(app.root)
    win.configure(bg='#10243e')
    status = tk.StringVar(value='Installierte Version: '+current)
    tk.Label(win, text='Programm aktualisieren', bg='#10243e', fg='white', font=('Segoe UI',17,'bold')).pack(padx=22,pady=(22,12),anchor='w')
    tk.Label(win, textvariable=status, bg='#10243e', fg='#dceaff', wraplength=580, justify='left', font=('Segoe UI',11)).pack(padx=22,anchor='w')
    notes = tk.Text(win, height=8, wrap='word', bg='#eef5ff', fg='#142942', font=('Segoe UI',11), relief='flat', padx=12,pady=10)
    notes.pack(padx=22,pady=14,fill='both',expand=True)
    notes.insert('1.0','Du kannst während der Update-Prüfung weiterlernen. Dein Fortschritt bleibt erhalten.')
    notes.configure(state='disabled')
    bar = ttk.Progressbar(win, maximum=100)
    bar.pack(padx=22,fill='x')
    events = queue.Queue()
    cancelled = threading.Event()
    state = {'busy':False, 'release':None, 'ready':False, 'closed':False, 'cache':None}

    def close():
        cancelled.set()
        state['closed'] = True
        win.destroy()

    def worker(action):
        state['busy'] = True
        button.configure(state='disabled')
        def run():
            try: events.put(('done',action()))
            except Exception as exc: events.put(('error',str(exc)))
        threading.Thread(target=run, daemon=True).start()

    def check():
        status.set('Suche nach Updates …')
        worker(lambda: ('checked', check_update(root_path,current)))

    def download():
        state['cache'] = data_dir()/'updates'/uuid.uuid4().hex
        status.set('Update wird heruntergeladen …')
        worker(lambda: ('downloaded', download_update(root_path,state['release'][0],state['cache'],
            lambda a,b:events.put(('progress',(a,b))), cancelled.is_set)))

    def install():
        if app.recording or app.job:
            status.set('Bitte zuerst die Aufnahme oder Sprachausgabe beenden.')
            return
        if not messagebox.askyesno('Update einspielen','Jetzt speichern, das Update einspielen und JapanischTrainer neu starten?',parent=win):
            return
        try:
            app.store.save()
            launch_worker(root_path,state['cache'],data_dir())
        except Exception as exc:
            status.set('Update konnte nicht gestartet werden: '+str(exc))
            return
        state['closed'] = True
        app.close()

    button = tk.Button(win,text='Nach Updates suchen',command=check,bg='#008bed',fg='white',relief='flat',padx=18,pady=9)
    button.pack(pady=16)
    win.protocol('WM_DELETE_WINDOW',close)

    def poll():
        if state['closed'] or app.closed or not win.winfo_exists():return
        try:
            while True:
                kind,value=events.get_nowait()
                if kind=='progress':
                    a,b=value;bar['value']=a/b*100
                    status.set(f'Update wird geladen: {a/1048576:.1f} / {b/1048576:.1f} MB')
                    continue
                state['busy']=False;button.configure(state='normal')
                if kind=='error':
                    status.set(value);button.configure(text='Erneut prüfen',command=check)
                elif value[0]=='checked':
                    state['release']=value[1]
                    if value[1] is None:
                        status.set('Version '+current+' ist aktuell.')
                        button.configure(text='Erneut prüfen',command=check)
                    else:
                        info=value[1][1]
                        status.set('Installiert: '+current+' · Verfügbar: '+info['version'])
                        notes.configure(state='normal');notes.delete('1.0','end');notes.insert('1.0',info.get('notes','Neue Programmversion.'));notes.configure(state='disabled')
                        button.configure(text='Update herunterladen',command=download)
                else:
                    status.set('Download und Signatur geprüft. Dein Lernstand bleibt erhalten.')
                    button.configure(text='Update einspielen und neu starten',command=install)
        except queue.Empty:pass
        win.after(100,poll)
    poll()
    check()

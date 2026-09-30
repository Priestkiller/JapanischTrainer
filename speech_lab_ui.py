"""Explicitly voluntary local microphone trial. No course metrics are changed."""
import json,platform,time
from datetime import datetime,timezone
from tkinter import filedialog,messagebox
from ui_renderer import WHITE,MUTED
from storage import data_dir
from speech_engine import app_root
import re,unicodedata
import modelpacks
from speech_trial import compare

def normalize_japanese(text):
    text=unicodedata.normalize('NFKC',str(text))
    return ''.join(chr(ord(c)-96) if 'ァ'<=c<='ヶ' else c for c in re.sub(r'[\s。、！？!?.,]','',text)).lower()

class SpeechLabMixin:
    def lab_open(self):
        self.lab_data=json.loads((app_root()/'data/speech_trial.json').read_text('utf8'));self.lab_index=0;self.lab_result=None;self.lab_status='';self.lab_cancelled=False
        self.lab_rows=[]
        try:
            rows=json.loads((data_dir()/'speech-trial.json').read_text('utf8'))
            if isinstance(rows,list):self.lab_rows=rows[-200:]
        except (OSError,ValueError):pass
    def lab_save(self):
        p=data_dir()/'speech-trial.json';tmp=p.with_suffix('.tmp');tmp.write_text(json.dumps(self.lab_rows[-200:],ensure_ascii=False,indent=2),'utf8');tmp.replace(p)
    def lab_record(self):
        if self.recording:self.lab_stop(True);return
        if self.job:return
        self.lab_cancelled=False;self.lab_result=None;self.lab_status='Sprich jetzt die Vorlage. Bei Stille: drei Sekunden warten, dann stoppen.'
        try:
            self.engine.start_recording(self.store.data.get('mic_device'));self.recording=True;self.record_started=time.monotonic()
        except Exception as e:self.lab_status=str(e)
        self.request_draw()
    def lab_stop(self,grade):
        self.recording=False;audio=self.engine.stop_recording();rate=self.engine.sample_rate
        if not grade:self.lab_cancelled=True;return
        p=dict(self.lab_data['prompts'][self.lab_index]);epoch=self.speech_epoch
        self.last_audio=audio;self.last_rate=rate;self.lab_status='Vergleiche dieselbe Aufnahme …'
        self.engine._tts=None;self.engine._sense=None;self.engine._parakeet=None
        # The target is retained only for reporting, outside the recognizer worker.
        def done(result):
            if self.view!='speech_lab' or epoch!=self.speech_epoch:return
            result.update(id=str(time.time_ns()),prompt=p['id'],expected=p['jp'],at=datetime.now(timezone.utc).isoformat(),negative=bool(p.get('negative')),confirmation='unconfirmed')
            for row in result['results']:row['match']=bool(not p.get('negative') and not row.get('error') and normalize_japanese(row['text']) in [normalize_japanese(x) for x in [p['jp']]+p.get('accept',[])])
            self.lab_result=result;self.lab_rows.append(result);self.lab_save();self.lab_status=result.get('message','Vergleich fertig. Bitte bestätige, ob du die Vorgabe gesprochen hast.');self.request_draw()
        done.on_error=lambda e:self.lab_error(e)
        self.run_worker('Lokaler Sprachvergleich',lambda:compare(audio,rate,bool(p.get('short')),lambda:self.lab_cancelled),done)
        self.request_draw()
    def lab_error(self,error):self.lab_status=str(error);self.request_draw()
    def lab_move(self,delta):
        if self.job or self.recording:return
        self.lab_index=max(0,min(len(self.lab_data['prompts'])-1,self.lab_index+delta));self.lab_result=None;self.lab_status='';self.last_audio=None;self.scroll=0;self.request_draw()
    def lab_confirm(self,value):
        if self.lab_result:self.lab_result['confirmation']=value;self.lab_save();self.lab_status='Deine Bestätigung wurde im lokalen Bericht gespeichert.';self.request_draw()
    def lab_export(self):
        path=filedialog.asksaveasfilename(parent=self.root,title='Sprachtestbericht speichern',defaultextension='.json',initialfile='JapanischTrainer-Sprachvergleich.json',filetypes=[('JSON','*.json')])
        if path:
            from pathlib import Path
            Path(path).write_text(json.dumps(dict(schema=1,source='voluntary_device_recording',device=platform.platform(),automatic_upload=False,audio_included=False,pronunciation_assessed=False,attempts=self.lab_rows),ensure_ascii=False,indent=2),'utf8');self.notify('Bericht gespeichert. Er wurde nicht hochgeladen.')
    def lab_clear(self):
        if messagebox.askyesno('Testergebnisse löschen','Nur Sprachtest-Ergebnisse löschen? Dein Lernstand bleibt erhalten.',parent=self.root):self.lab_rows=[];self.lab_result=None;self.lab_save();self.request_draw()
    def lab_download(self,kind):
        if self.job or self.recording:return
        m=modelpacks.manifest(kind)
        if not messagebox.askyesno('Freiwilliges Testmodell',f"{modelpacks.NAMES[kind]}: {m['bytes']/1e6:.0f} MB Download, {m['unpacked_bytes']/1e6:.0f} MB installiert. Qualität und Geschwindigkeit auf deinem Gerät sind noch offen. Die Standarderkennung bleibt erhalten. Jetzt laden?",parent=self.root):return
        self.lab_cancelled=False
        self.run_worker('Testmodell laden',lambda:modelpacks.install(kind,lambda:self.lab_cancelled),lambda _:self.notify('Testmodell geprüft und bereit.'))
    def lab_import(self,kind):
        if self.job or self.recording:return
        path=filedialog.askopenfilename(parent=self.root,title=modelpacks.NAMES[kind]+' Paket wählen',filetypes=[('Geprüftes Modellpaket','*.zip')])
        if not path:return
        self.lab_cancelled=False
        self.run_worker('Modellpaket prüfen',lambda:modelpacks.install_local(kind,path,lambda:self.lab_cancelled),lambda _:self.notify('Testmodell geprüft und bereit.'))
    def draw_speech_lab(self,s):
        self.heading(s,'Lokaler Sprachvergleich','Freiwilliger Test mit denselben Aufnahmen · keine Kurswertung')
        x=294;y=183;w=self.W-x-24;vh=self.H-y-82;s.panel((x,y,w,vh),'solid',16);p=self.make_pane(w,2400);o=12-self.scroll;item=self.lab_data['prompts'][self.lab_index]
        o+=p.paragraph(18,o,self.lab_data['notice'],w-40,15,MUTED,lineheight=23)+18
        p.text(18,o,f"Beispiel {self.lab_index+1} / {len(self.lab_data['prompts'])}",16,MUTED,True);o+=35
        o+=p.paragraph(18,o,item['jp'] or 'Still bleiben',w-40,32,WHITE,True,lineheight=44)+8
        o+=p.paragraph(18,o,item['romaji']+' · '+item['de'],w-40,18,WHITE,lineheight=26)+12
        if not item.get('negative'):p.button('lab-audio',(18,o,220,44),'Vorlage anhören',lambda:self.speak(item['jp']),'blue')
        p.button('lab-record',(252,o,min(w-270,330),44),'Aufnahme beenden' if self.recording else 'Für Vergleich aufnehmen',self.lab_record,'red');o+=58
        o+=p.paragraph(18,o,self.lab_status,w-40,15,MUTED,lineheight=23)+15
        if self.lab_result:
            for row in self.lab_result['results']:
                p.text(18,o,row['model'],16,WHITE,True);o+=26
                o+=p.paragraph(18,o,row.get('error') or row.get('text') or 'Kein Text erkannt',w-40,20,WHITE,lineheight=29)+5
                text='Modellfehler' if row.get('error') else f"{'Text passt' if row['match'] else 'Text weicht ab'} · Erkennen {row['decodeMs']} ms · Laden {row['loadMs']} ms"
                o+=p.paragraph(18,o,text,w-40,14,MUTED,lineheight=21)+12
            p.button('lab-good',(18,o,270,44),'Vorgabe ausgeführt',lambda:self.lab_confirm('as_requested'),'green');p.button('lab-bad',(304,o,240,44),'Versprochen / Störung',lambda:self.lab_confirm('invalid_take'));o+=58
            p.button('lab-own',(18,o,250,44),'Meine Aufnahme',self.play_recording);o+=62
        p.text(18,o,'Optionale Testmodelle',19,WHITE,True);o+=32
        o+=p.paragraph(18,o,'Die Erkennung bekommt niemals die erwartete Antwort. Im Vergleich laufen alle installierten Modelle nacheinander. Größer bedeutet nicht automatisch besser; die normale Erkennung bleibt voreingestellt.',w-40,15,MUTED,lineheight=23)+15
        for kind,name in modelpacks.NAMES.items():
            present=modelpacks.ready(kind);p.button('lab-model:'+kind,(18,o,(w-52)/2,44),name+(' · installiert' if present else ' laden'),(lambda:self.notify('Für den Vergleich bereit.')) if present else lambda k=kind:self.lab_download(k))
            p.button('lab-import:'+kind,(34+(w-52)/2,o,(w-52)/2,44),'ZIP vom Computer wählen',lambda k=kind:self.lab_import(k),enabled=not present);o+=56
        if self.job:p.button('lab-cancel',(18,o,250,44),'Vorgang abbrechen',lambda:setattr(self,'lab_cancelled',True));o+=56
        p.text(18,o,f'{len(self.lab_rows)} lokale Versuche · keine Aussprache-Note',15,MUTED);o+=35
        p.button('lab-export',(18,o,260,44),'Bericht speichern',self.lab_export,'blue');p.button('lab-clear',(294,o,220,44),'Testergebnisse löschen',self.lab_clear);o+=60
        self.scroll_pane(s,p,x,y,vh,o+self.scroll+15)
        s.button('lab-prev',(x,self.H-65,180,44),'← Zurück',lambda:self.lab_move(-1));s.button('lab-next',(self.W-300,self.H-65,270,44),'Nächstes Beispiel →',lambda:self.lab_move(1),'green')

"""JapanischTrainer V11: native, explicitly rendered desktop UI.

The previous V6 speech backend and course identifiers are preserved. Rendering is
implemented in native Tk/Pillow components, not in QML or an embedded browser.
The real window can be captured for repeatable visual/integration tests.
"""
from __future__ import annotations
import argparse,json,logging,math,os,queue,random,shutil,threading,time,tkinter as tk
from tkinter import filedialog,messagebox
from pathlib import Path
import numpy as np
from PIL import Image,ImageTk
from ui_renderer import Surface,WHITE,MUTED,INK,BLUE,PINK,scaled_image
from speech_engine import LocalSpeechEngine,app_root
from storage import ProgressStore,data_dir
from learning import Learning
from lesson_ui import LessonMixin
from study import matches_romaji
from motion import PRESETS,preset_name
ROOT=app_root();VERSION='11.0.1'
NAV=[('home','home','Startseite'),('path','book','Lernen'),('speaking','mic','Sprechen'),('listening','headphones','Hören'),('writing','pencil','Schreiben'),('vocab','cards','Vokabeln'),('grammar','layers','Grammatik'),('kanji','kanji','Kanji'),('review','repeat','Wiederholen'),('progress','chart','Fortschritt'),('teachers','teachers','Lehrer'),('settings','settings','Einstellungen')]

class TrainerApp(LessonMixin):
    def __init__(self,root,args):
        self.root=root;self.args=args;self.store=ProgressStore();self.learning=Learning(ROOT,self.store);self.engine=LocalSpeechEngine()
        self.audio_status=self.engine.model_status();self.view=args.page or 'home';self.previous='home';self.scroll=0.;self.max_scroll=0.;self.hover='';self.focus='';self.hits=[]
        self.frame=None;self.photo=None;self.pending_draw=None;self.bg_cache={};self.events=queue.Queue();self.job='';self.task_token=0;self.closed=False
        self.last_audio=None;self.last_rate=48000;self.recording=False;self.record_started=0.;self.record_level=0.;self.result=None;self.speech_error=''
        self.preview_teacher=self.learning.teacher()['id'];self.lesson=self.learning.by_key.get(args.lesson,self.learning.next_lesson());self.card_index=min(max(0,args.card),len(self.lesson['cards'])-1)
        self.answer=None;self.answer_correct=False;self.speech_item=None;self.speech_return='speaking';self.message='';self.message_until=0.
        self.query='';self.path_stage='Alle';self.path_new_only=False;self.entry=None;self.entry_mode='';self.entry_target=None;self.write_mode='Romaji';self.write_card=self.learning.cards[0];self.write_feedback=''
        self.review_card=None;self.review_revealed=False;self.devices=[(None,'Windows-Standardmikrofon')];self.render_error='';self.kana_mode='Hiragana'
        root.title('JapanischTrainer – Dein Weg nach Japan · V11');root.configure(bg='#061426');root.minsize(1080,700)
        if os.name=='nt':
            try:root.iconbitmap(str(ROOT/'assets/icon.ico'))
            except tk.TclError:pass
        w,h=map(int,args.size.split('x'))
        if not args.capture:w=min(w,root.winfo_screenwidth()-40);h=min(h,root.winfo_screenheight()-80)
        root.geometry(f'{w}x{h}+20+20')
        self.canvas=tk.Canvas(root,bg='#061426',highlightthickness=0,borderwidth=0,takefocus=1);self.canvas.pack(fill='both',expand=True)
        self.init_v8()
        self.canvas.bind('<Configure>',self.on_resize);self.canvas.bind('<Motion>',self.on_motion);self.canvas.bind('<Leave>',self.on_leave);self.canvas.bind('<Button-1>',self.on_click)
        self.canvas.bind('<MouseWheel>',lambda e:self.wheel(-e.delta/120*65));self.canvas.bind('<Button-4>',lambda e:self.wheel(-70));self.canvas.bind('<Button-5>',lambda e:self.wheel(70))
        root.bind('<Key>',self.on_key);root.protocol('WM_DELETE_WINDOW',self.close);self.canvas.focus_set()
        root.after(50,self.pump);root.after(120,self.redraw)
        if self.store.warning:self.notify(self.store.warning,12)
        if args.capture:root.after(800,self.capture_and_exit)
    def current_card(self):return self.lesson['cards'][self.card_index]
    def teacher(self):return self.learning.teacher(self.preview_teacher if self.view=='teachers' else None)
    def notify(self,text,seconds=7):self.message=str(text);self.message_until=time.monotonic()+seconds;self.request_draw()
    def request_draw(self):
        if not self.closed and self.pending_draw is None:self.pending_draw=self.root.after(12,self.redraw)
    def on_resize(self,e):self.bg_cache.clear();self.request_draw()
    def hit_at(self,x,y):return next((h for h in reversed(self.hits) if h.rect[0]<=x<h.rect[0]+h.rect[2] and h.rect[1]<=y<h.rect[1]+h.rect[3]),None)
    def on_motion(self,e):
        if not hasattr(self,'render_scale'):return
        h=self.hit_at(e.x/self.render_scale,e.y/self.render_scale);id=h.id if h else ''
        if id!=self.hover:self.hover=id;self.canvas.configure(cursor='hand2' if h else '');self.request_draw()
    def on_leave(self,e):self.hover='';self.request_draw()
    def on_click(self,e):
        self.canvas.focus_set();h=self.hit_at(e.x/self.render_scale,e.y/self.render_scale)
        if h:
            self.focus=h.id
            try:h.action()
            except Exception as exc:logging.exception('UI action failed');self.notify(exc)
            self.request_draw()
    def wheel(self,n):
        new=min(self.max_scroll,max(0,self.scroll+n))
        if new!=self.scroll:self.scroll=new;self.request_draw()
    def on_key(self,e):
        if e.widget is self.entry:
            if e.keysym=='Return' and self.entry_mode=='writing':self.check_writing()
            elif e.keysym=='Return' and self.entry_mode=='study':self.check_learn_text()
            return
        if e.keysym=='Tab':
            ids=[h.id for h in self.hits]
            if ids:
                i=ids.index(self.focus) if self.focus in ids else -1;self.focus=ids[(i+(-1 if e.state&1 else 1))%len(ids)];self.request_draw()
            return 'break'
        if e.keysym=='Return':
            h=next((h for h in self.hits if h.id==self.focus),None)
            if h:h.action();self.request_draw()
        if e.keysym=='Escape':
            if self.recording:self.stop_capture(False)
            elif self.view=='lesson' and self.inline_speech:self.speak_card(self.current_card())
            elif self.view in ('lesson','speaking','complete'):self.navigate('path')
        if e.keysym=='space':
            if self.view=='speaking':self.toggle_recording()
            elif self.view=='lesson':
                if self.inline_speech:self.toggle_recording()
                else:self.speak(self.current_card()['jp'])
            return 'break'
        if self.view=='lesson' and e.char in ('1','2','3','4'):
            opts,_=self.flow.answers();i=int(e.char)-1
            if i<len(opts):self.check_answer(opts[i])
        if e.keysym in ('Next','Down'):self.wheel(120)
        if e.keysym in ('Prior','Up'):self.wheel(-120)
    def navigate(self,page):
        if self.recording:self.stop_capture(False)
        if self.view=='lesson':self.flow.snapshot()
        if page!=self.view:self.speech_epoch+=1;self.inline_speech=False
        if page!=self.view:self.clear_reaction()
        self.previous=self.view;self.view=page;self.scroll=0;self.hover='';self.focus='';self.query='';self.hide_entry()
        if page=='teachers':self.preview_teacher=self.learning.teacher()['id']
        if page=='writing':self.new_writing()
        if page=='review':self.next_review()
        if page=='settings':self.audio_status=self.engine.model_status();self.devices=[(None,'Windows-Standardmikrofon')]+self.engine.list_input_devices()
        self.request_draw()
    def resume(self):
        c=self.store.data.get('last_lesson',{});key=c.get('key')
        if key in self.learning.by_key and (key not in self.store.data['completed'] or key in self.store.data.get('lesson_sessions',{})):self.open_lesson(key,c.get('card',0),restore=True)
        else:self.open_lesson(self.learning.next_lesson()['key'])
    def open_lesson(self,key,index=0,force=False,restore=False):
        if not force and not self.learning.unlocked(key):self.notify('Zuerst die vorherige Lektion abschließen.');return
        self.lesson=self.learning.by_key[key];self.card_index=min(max(0,int(index)),len(self.lesson['cards'])-1);self.answer=None;self.answer_correct=False
        self.navigate('lesson');self.new_flow(self.card_index,restore);self.remember_card()
    def remember_card(self):self.store.data['last_lesson']={'key':self.lesson['key'],'card':self.card_index};self.store.save()
    def choose_teacher(self,id,commit=False):
        if id!=self.preview_teacher or (commit and id!=self.learning.teacher()['id']):self.clear_reaction()
        self.preview_teacher=id
        if commit:self.store.data['teacher_id']=id;self.store.save();self.notify(self.learning.teacher(id)['name']+' ist jetzt deine Lehrkraft.')
        self.request_draw()
    def run_worker(self,name,fn,callback):
        if self.job:self.notify('Der Audioprozess läuft noch. Bitte kurz warten.');return False
        self.job=name;self.task_token+=1;token=self.task_token
        def work():
            try:self.events.put((token,callback,fn(),None))
            except Exception as exc:logging.exception('Audio task failed');self.events.put((token,callback,None,str(exc)))
        threading.Thread(target=work,daemon=True,name='JapanischTrainer-'+name).start();self.request_draw();return True
    def speak(self,text,slow=False,teacher_id=None):
        if self.recording:self.notify('Bitte zuerst die Aufnahme beenden.');return
        t=self.learning.teacher(teacher_id);speed=float(self.store.data.get('tts_speed',1))*t['speed']*(.72 if slow else 1.)
        self.run_worker('Vorlesen',lambda:self.engine.speak(text,speed,int(t['speaker_id'])),lambda _:None)
    def toggle_recording(self):
        if self.recording:self.stop_capture(True);return
        if self.job:self.notify('Bitte auf das Ende der Sprachausgabe warten.');return
        try:
            if self.view=='lesson':self.speech_item=self.learning.speech_target(self.current_card(),self.lesson)
            self.speech_epoch+=1
            self.engine.start_recording(self.store.data.get('mic_device'))
            if self.view=='lesson':self.flow.metrics()['speech_attempts']+=1;self.flow.snapshot()
            self.recording=True;self.record_started=time.monotonic();self.result=None;self.speech_error='';self.record_level=0.
        except Exception as exc:
            self.speech_error='Mikrofon nicht verfügbar: '+str(exc)
            try:self.engine.stop_recording()
            except Exception:pass
        self.request_draw()
    def stop_capture(self,grade=True):
        if not self.recording:return
        self.recording=False
        try:
            self.last_audio=self.engine.stop_recording();self.last_rate=self.engine.sample_rate
            if grade:
                item=self.speech_item or self.learning.speech_target(self.current_card(),self.lesson);self.speech_item=item
                a=self.last_audio.copy();sr=self.last_rate;accepted=list(item['accept'])
                self.run_worker('Spracherkennung',lambda:self.engine.recognize_for_target(a,accepted,sr),lambda result,target=item['target'],epoch=self.speech_epoch:self.received_speech(result,target,epoch))
        except Exception as exc:self.speech_error=str(exc)
        self.request_draw()
    def received_speech(self,r,target=None,epoch=None):
        # Preserve the recorded target if the learner navigated while ASR was busy.
        target=target or (self.speech_item or {}).get('target','')
        if target==(self.speech_item or {}).get('target') and (epoch is None or epoch==self.speech_epoch):
            self.result=r
            reliable=r.reliable and (not r.quality or r.quality.status!='bad')
            self.react('praise' if reliable and r.score>=80 else 'encourage',
                       'speech-match' if reliable else 'speech-uncertain')
        if target and r.reliable and (not r.quality or r.quality.status!='bad'):
            self.store.set_speech_score(target,r.score,r.heard);self.store.touch_day()
        self.request_draw()
    def play_recording(self):
        if self.last_audio is not None:
            audio=self.last_audio.copy();rate=self.last_rate
            self.run_worker('Deine Aufnahme',lambda:self.engine.play_recording(audio,rate),lambda _:None)
    def pump(self):
        if self.closed:return
        try:
            while True:
                token,cb,value,error=self.events.get_nowait()
                if token!=self.task_token:continue
                self.job=''
                if error:
                    self.speech_error=error
                    if self.view!='speaking' and not (self.view=='lesson' and self.inline_speech):self.notify(error,10)
                else:cb(value)
                self.request_draw()
        except queue.Empty:pass
        if self.recording:
            if time.monotonic()-self.record_started>=15:self.stop_capture(True)
            else:
                chunks=getattr(self.engine,'_chunks',[])
                if chunks:self.record_level=min(1.,float(np.sqrt(np.mean(chunks[-1]**2)+1e-10))*8)
                self.request_draw()
        if self.reaction!='idle' and time.monotonic()>self.reaction_until:self.clear_reaction();self.request_draw()
        if self.message and time.monotonic()>self.message_until:self.message='';self.request_draw()
        self.root.after(140 if self.recording else 70,self.pump)
    def background(self,w,h,sc):
        key=(round(w*sc),round(h*sc))
        if key not in self.bg_cache:
            im=scaled_image(str(ROOT/'assets/backgrounds/main.jpg'),*key,'cover',.5).copy();im.alpha_composite(Image.new('RGBA',im.size,(5,16,36,64)));self.bg_cache={key:im}
        return self.bg_cache[key].copy()
    def redraw(self):
        self.pending_draw=None
        if self.closed:return
        aw=max(1080,self.canvas.winfo_width());ah=max(650,self.canvas.winfo_height());self.render_scale=max(.78,min(1.3,aw/1440))*float(self.store.data.get('ui_scale',1))
        self.W=aw/self.render_scale;self.H=ah/self.render_scale
        s=Surface(self.W,self.H,self.render_scale,self.background(self.W,self.H,self.render_scale),self.hover,self.focus)
        self.actor_specs=[];self.entry_target=None;self.max_scroll=0;self.render_error='';self.draw_sidebar(s);self.draw_topbar(s)
        try:getattr(self,'draw_'+self.view,self.draw_home)(s)
        except Exception as exc:
            self.render_error=str(exc);logging.exception('Render failed');s.panel((294,140,self.W-320,170),'solid');s.paragraph(318,167,str(exc),self.W-368,17)
        if self.message:
            y=self.H-63;s.panel((286,y,self.W-311,48),'solid',12);s.icon('info',302,y+12,22,BLUE);s.text(337,y+15,self.message,14,WHITE,width=self.W-372)
        if self.job:s.panel((self.W-311,96,290,36),'solid',11);s.text(self.W-292,106,self.job+' …',14,'#91d7ff',True)
        self.frame=s;self.hits=s.hits;self.photo=ImageTk.PhotoImage(s.image.convert('RGB'),master=self.root)
        self.canvas.delete('frame');self.canvas.create_image(0,0,anchor='nw',image=self.photo,tags='frame');self.canvas.tag_lower('frame');self.actors.sync(self.actor_specs);self.place_entry()
    def draw_sidebar(self,s):
        s.fill((0,0,264,self.H),(5,20,39,249));s.fill((263,0,1,self.H),'#325173');s.icon('torii',20,28,36,'#ff585e')
        s.fitted(69,27,'JapanischTrainer',183,21,16,WHITE,True,False);s.text(69,57,'Dein Weg nach Japan',12,MUTED,width=184)
        y=116;active='path' if self.view in ('lesson','complete') else self.view
        for page,icon,label in NAV:
            id='nav:'+page;sel=active==page
            if sel:s.button(id,(8,y-8,248,42),'',lambda p=page:self.navigate(p),'blue')
            elif self.hover==id:s.fill((8,y-8,248,42),'#1c344f',10)
            s.icon(icon,26,y,25);s.text(66,y+4,label,16,WHITE,sel);s.register(id,(8,y-8,248,42),lambda p=page:self.navigate(p),label);y+=44
        if self.H>910 and self.store.data.get('show_kiko',True):
            y=max(y+30,self.H-250);s.panel((14,y,234,199));s.text(133,y+20,'Kiko',21,WHITE,True);s.text(133,y+47,'Maskottchen',11,MUTED)
            self.add_actor(s,ROOT/'assets/mascot/kiko_idle.png',(16,y+49,118,144),'mascot','kiko');s.panel((129,y+74,108,87),'bubble',16,False);s.paragraph(140,y+86,'Juhu!\nGut gemacht!' if self.actor_mood()=='praise' else 'Noch einmal.\nWir üben!' if self.actor_mood()=='encourage' else 'Gemeinsam\nschaffen\nwir das!',87,12,INK)
        else:
            s.panel((16,self.H-124,232,74),'soft',13,False);t=self.learning.teacher();s.image_at(self.learning.asset(t,'avatar'),(26,self.H-115,52,54),radius=10);s.text(90,self.H-106,t['name'],17,WHITE,True);s.text(90,self.H-80,'Deine Lehrkraft',12,MUTED)
        s.text(24,self.H-32,'V'+VERSION+' · Offline-Lerntrainer',11,'#8ba6c1')
    def draw_topbar(self,s):
        s.panel((280,14,self.W-294,72),'dark',20,False);s.text(302,40,'日本語',20,WHITE,True,jp=True);s.text(379,43,'·  Schritt für Schritt',15,WHITE,True,width=max(130,self.W-840))
        x=self.W-350
        for ic,main,sub,col in [('flame',str(self.store.data['streak'])+(' Tag' if self.store.data['streak']==1 else ' Tage'),'Lernserie','#ffb43f'),('flower',str(self.store.data['xp'])+' XP','Level '+str(self.store.data['xp']//250+1),'#ffafd8')]:
            s.icon(ic,x,32,34,col);s.text(x+47,34,main,17,col,True);s.text(x+47,58,sub,11,MUTED);x+=139
        s.fill((self.W-69,26,49,49),'#1b324d',25);s.icon('user',self.W-55,38,23);s.register('profile',(self.W-69,26,49,49),lambda:self.navigate('progress'))
    def heading(self,s,title,sub='',back=False):
        x=294;y=111
        if back:s.button('back',(x,y,94,36),'‹  Zurück',lambda:self.navigate('path'),size=13);x+=116
        s.text(x,y+1,title,27,WHITE,True,width=self.W-x-25)
        if sub:s.text(x,y+41,sub,14,MUTED,width=self.W-x-30)
    def teacher_stage(self,s,b,message=None):
        t=self.teacher();x,y,w,h=b;bh=122
        feedback=self.actor_feedback()
        if feedback.message:message=feedback.message
        if message:
            s.panel((x+10,y,w-20,bh),'bubble',23);s.icon('flower',x+27,y+17,21,PINK);s.text(x+58,y+19,t['name'],16,INK,True);s.paragraph(x+27,y+49,message,w-55,15,INK,max_lines=3,lineheight=21)
        top=y+(bh+12 if message else 0);art_h=max(210,h-(bh+92 if message else 82))
        self.add_actor(s,self.learning.asset(t),(x-3,top,w+6,art_h));by=y+h-72;s.panel((x+24,by,w-48,65))
        s.icon('flower',x+42,by+20,23,PINK);s.text(x+78,by+13,t['name'],20,WHITE,True);s.text(x+78,by+40,t['style'],12,MUTED,width=w-115);s.register('teacher-stage',(x+24,by,w-48,65),lambda:self.navigate('teachers'))
    def make_pane(self,w,h):return Surface(w,h,self.render_scale,hover=self.hover,focus=self.focus)
    def scroll_pane(self,s,p,x,y,vh,total):
        self.max_scroll=max(0,total-vh)
        if self.scroll>self.max_scroll:self.scroll=self.max_scroll;self.request_draw()
        s.compose(p,x,y,(p.width,vh))
        if self.max_scroll>0:
            th=max(36,vh*vh/(vh+self.max_scroll));sy=y+(vh-th)*self.scroll/self.max_scroll;s.fill((x+p.width-4,y,3,vh),'#263e5a',2);s.fill((x+p.width-4,sy,3,th),'#6da9d4',2)
    def draw_home(self,s):
        self.heading(s,'Willkommen zurück','Deine nächste kleine Etappe auf dem Weg nach Japan.');x=294;y=187;w=self.W-x-22;s.panel((x,y,w,116));s.text(x+18,y+15,'Deine Lehrkräfte',13,MUTED,True)
        for i,t in enumerate(self.learning.teachers):
            xx=x+19+i*min(126,(w-42)/8);sel=t['id']==self.learning.teacher()['id'];s.panel((xx,y+39,105,63),'soft',12,False,stroke=PINK if sel else '#376083');s.image_at(self.learning.asset(t,'avatar'),(xx+5,y+44,47,53),radius=10)
            s.text(xx+55,y+65,t['name'],10,WHITE,True,width=45);s.register('quick:'+t['id'],(xx,y+39,105,63),lambda id=t['id']:self.choose_teacher(id,True))
        lw=min(649,w*.61);rx=x+lw+22;y=328;l=self.learning.next_lesson();done=len([k for k in self.store.data['completed'] if k in self.learning.by_key])
        s.panel((x,y,lw,274));s.icon('book',x+25,y+25,28);s.text(x+69,y+27,'Dein nächster Schritt',24,WHITE,True);s.panel((x+20,y+79,lw-40,112),'white',16,False)
        s.text(x+39,y+96,l['title'],22,INK,True,width=lw-80);s.text(x+39,y+135,l['unit'],14,'#597494',width=lw-80);s.text(x+39,y+161,l['level']+' · '+str(l.get('xp',20))+' XP',12,'#597494');s.button('resume',(x+20,y+207,lw-40,48),'Weiterlernen  →',self.resume,'blue',size=18)
        y+=294;gap=14;sw=(lw-2*gap)/3
        for i,(v,label) in enumerate([(str(done)+' / '+str(len(self.learning.lessons)),'Lektionen'),(str(self.store.data['xp']),'Erfahrungspunkte'),(str(len(self.store.data['speech_scores'])),'Sprechziele geübt')]):
            xx=x+i*(sw+gap);s.panel((xx,y,sw,114));s.text(xx+18,y+23,v,26,WHITE,True,width=sw-30);s.text(xx+18,y+70,label,12,MUTED,width=sw-26)
        y+=136
        if y+150<self.H:
            s.panel((x,y,lw,145));s.text(x+24,y+21,'Lernen, ohne zu raten.',20,WHITE,True);s.paragraph(x+24,y+58,'Jedes neue Wort mit Bedeutung und Aussprachehilfe. Danach hörst du zu, übst und sprichst selbst.',lw-48,16,MUTED,max_lines=3)
        self.teacher_stage(s,(rx,331,self.W-rx-15,self.H-343),self.learning.teacher()['de'])
    def draw_path(self,s):
        self.heading(s,'Dein Lernpfad · '+str(len(self.learning.lessons))+' Lektionen',
            'Erst verstehen, dann üben. Neue Grundlagen, Alltagssituationen und kurze Texte.')
        x=294;y=184;w=self.W-x-25
        s.panel((x,y,w-8,92),'dark',16)
        s.text(x+18,y+14,'Suche: Thema, Wort, Lesung oder Bedeutung',11,MUTED)
        s.panel((x+15,y+35,w-445,39),'white',10,False)
        self.entry_target=('search',(x+23,y+40,w-461,28))
        s.button('path-stage',(x+w-413,y+33,210,43),self.path_stage+'  ›',self.show_path_stages,'secondary',size=13)
        s.button('path-new',(x+w-191,y+33,160,43),'Nur neue: '+('An' if self.path_new_only else 'Aus'),
            self.toggle_new_lessons,'blue' if self.path_new_only else 'secondary',size=13)
        rows=self.learning.filtered_lessons(self.query,self.path_stage,self.path_new_only)
        s.text(x+4,y+106,f'{len(rows)} passende Lektionen · 100 zusätzliche Einheiten in V11',12,MUTED,width=w-15)
        y+=137;vh=self.H-y-24;p=self.make_pane(w,max(vh,850));o=-self.scroll
        for l in rows:
            if o>vh+145:break
            unlocked=self.learning.unlocked(l['key']);done=l['key'] in self.store.data['completed']
            if o+131>=0:
                p.panel((2,o+2,w-12,126),'dark',16)
                p.icon('check' if done else 'book' if unlocked else 'lock',24,o+40,29,'#63dfa4' if done else WHITE if unlocked else '#7b93b2')
                no=self.learning.positions[l['key']]+1
                p.text(76,o+16,f'{no:03d} · '+l['title'],18,WHITE if unlocked else '#a6b7cb',True,width=w-275)
                p.text(76,o+46,l['level']+' · '+l['unit'],11.5,MUTED,width=w-275)
                goal=l.get('goal') or 'Bekannte Einheit: Erklären, hören, zusammensetzen, schreiben und wiederholen.'
                p.paragraph(76,o+67,goal,w-279,11.5,'#a8c2dc',max_lines=2,lineheight=16)
                p.text(76,o+106,str(len(l['cards']))+' Karten · 6 Schritte je Karte + Abschlussrunde',10.5,MUTED,width=w-280)
                if l.get('origin')=='v11':
                    p.fill((w-164,o+14,115,23),'#173d4c',9);p.text(w-106,o+19,'NEU IN V11',10,'#82e4bd',True,align='center')
                p.button('lesson:'+l['key'],(w-181,o+56,148,43),'Wiederholen' if done else 'Starten',
                    lambda key=l['key']:self.open_lesson(key),'blue' if unlocked else 'secondary',size=14,enabled=unlocked)
            o+=141
        if not rows:
            p.panel((2,2,w-12,140),'dark',16)
            p.text(25,27,'Keine passende Lektion gefunden.',20,WHITE,True,width=w-70)
            p.paragraph(25,68,'Versuche einen anderen Suchbegriff oder stelle den Abschnitt auf „Alle“.',w-62,14,MUTED,max_lines=2)
        self.scroll_pane(s,p,x,y,vh,len(rows)*141 if rows else 148)
    def show_path_stages(self):
        menu=tk.Menu(self.root,tearoff=False,bg='#10263f',fg='#eef5ff',activebackground='#067cc9')
        for stage in ['Alle']+self.learning.stages:
            menu.add_command(label=('✓ ' if stage==self.path_stage else '   ')+stage,
                command=lambda value=stage:self.set_path_stage(value))
        try:menu.tk_popup(self.root.winfo_pointerx(),self.root.winfo_pointery())
        finally:menu.grab_release()
    def set_path_stage(self,stage):
        if stage not in ['Alle']+self.learning.stages:return
        self.path_stage=stage;self.scroll=0;self.request_draw()
    def toggle_new_lessons(self):
        self.path_new_only=not self.path_new_only;self.scroll=0;self.request_draw()
    def draw_teachers(self,s):
        self.heading(s,'Lehrer auswählen','Wähle deine Begleitung. Die Auswahl ändert Bild, Sprecherprofil und Sprechtempo.');x=294;y=194;w=self.W-x-22;gw=min(660,w*.61);gap=12;cw=(gw-3*gap)/4;vh=self.H-y-22;ch=min(325,max(242,(vh-20)/2));p=self.make_pane(gw,max(vh,ch*2+16));off=-self.scroll
        for i,t in enumerate(self.learning.teachers):
            xx=(i%4)*(cw+gap)+2;yy=(i//4)*(ch+15)+off;selected=t['id']==self.preview_teacher;committed=t['id']==self.learning.teacher()['id']
            if selected:p.fill((xx-3,yy-3,cw+6,ch+6),'#167bae',17);p.fill((xx-1,yy-1,cw+2,ch+2),'#1c9ee4',16)
            p.panel((xx,yy,cw,ch),'solid',15,True,stroke='#73d9ff' if selected else '#387cac');p.image_at(self.learning.asset(t,'card'),(xx+3,yy+3,cw-6,ch-88),'cover',.05,radius=12);p.fill((xx+1,yy+ch-96,cw-2,94),'#10253f',13)
            p.text(xx+13,yy+ch-82,t['name'],19,WHITE,True,width=cw-25);p.paragraph(xx+13,yy+ch-47,t['style'],cw-23,12,MUTED,max_lines=2,lineheight=17)
            if committed:p.fill((xx+cw-33,yy+10,24,24),'#019cff',12);p.icon('check',xx+cw-30,yy+13,18)
            p.register('teacher:'+t['id'],(xx,yy,cw,ch),lambda id=t['id']:self.choose_teacher(id))
        self.scroll_pane(s,p,x,y,vh,ch*2+18);rx=x+gw+20;rw=self.W-rx-18;t=self.learning.teacher(self.preview_teacher)
        s.panel((rx,y-7,rw,self.H-y-12),'dark',23);s.text(rx+22,y+13,t['name'],31,WHITE,True);s.icon('flower',rx+rw-59,y+19,29,PINK)
        foot=268;at=y+61;ah=max(130,self.H-25-foot-at);self.add_actor(s,self.learning.asset(t),(rx+6,at,rw-12,ah));by=self.H-25-foot;s.panel((rx+13,by,rw-26,foot-12),'solid',17)
        s.icon('speaker',rx+28,by+15,22,'#91d3ff');s.text(rx+62,by+17,'Stimme',13,MUTED,True);s.text(rx+28,by+43,t['voice'],15,WHITE,width=rw-58)
        s.button('voice-preview',(rx+26,by+74,rw-52,44),'Stimmprobe anhören',lambda:self.speak(t['jp'],False,t['id']),'secondary','play',14);s.text(rx+29,by+134,'Schwerpunkt',12,'#8ac9fb',True);s.paragraph(rx+29,by+157,t['focus'],rw-58,14,WHITE,max_lines=2,lineheight=19)
        s.button('teacher-select',(rx+26,by+201,rw-52,45),'Ausgewählt ✓' if t['id']==self.learning.teacher()['id'] else 'Diese Lehrkraft wählen  →',lambda:self.choose_teacher(t['id'],True),'blue',size=15)
    def draw_speaking(self,s):
        self.heading(s,'Sprechen mit '+self.learning.teacher()['name'],'Vorhören → aufnehmen → erkannte Wörter vergleichen. Leertaste startet und stoppt.')
        item=self.speech_item or self.learning.speech_target(self.current_card(),self.lesson);x=294;y=189;lw=min(666,(self.W-x-38)*.61);rx=x+lw+25;vh=self.H-y-24;p=self.make_pane(lw,max(vh,860));o=-self.scroll
        th=len(p.wrap(item['target'],lw-80,30,True,True))*38
        rh=len(p.wrap(item.get('romaji',''),lw-80,16))*22
        dh=len(p.wrap(item.get('meaning',''),lw-80,14,True))*21
        inner=max(116,th+rh+dh+30);head=inner+137
        p.panel((2,o+2,lw-10,head));p.icon('chat',22,o+21,25);p.text(62,o+23,'Dein Sprechziel',20,WHITE,True)
        p.panel((18,o+64,lw-43,inner),'white',16,False);yy=o+78
        yy+=p.paragraph(36,yy,item['target'],lw-80,30,INK,True,lineheight=38,jp=True)
        yy+=p.paragraph(37,yy+4,item.get('romaji',''),lw-80,16,'#56739a',lineheight=22)+7
        p.paragraph(37,yy,item.get('meaning',''),lw-80,14,INK,True,lineheight=21);bw=(lw-54)/2
        by=o+head-58
        p.button('speech-play',(18,by,bw,44),'Normal anhören',lambda:self.speak(item['target']),'blue','speaker',14);p.button('speech-slow',(27+bw,by,bw,44),'Langsam anhören',lambda:self.speak(item['target'],True),'secondary','turtle',14)
        head_advance=head+19;o+=head_advance;p.panel((2,o,lw-10,177));p.icon('mic',22,o+19,25,'#ff94b4');p.text(62,o+23,'Jetzt bist du dran',19,WHITE,True)
        p.button('record',(18,o+62,(lw-55)*.59,50),'Aufnahme stoppen' if self.recording else 'Aufnahme starten',self.toggle_recording,'red','pause' if self.recording else 'mic',15,enabled=not self.job)
        p.button('play-own',(29+(lw-55)*.59,o+62,(lw-55)*.41,50),'Deine Aufnahme',self.play_recording,'secondary','headphones',12,enabled=self.last_audio is not None and not self.recording and not self.job)
        status=f'Aufnahme läuft · {int(time.monotonic()-self.record_started)} / 15 s' if self.recording else self.job+' …' if self.job else 'Die Aufnahme bleibt auf deinem Computer.';p.text(22,o+130,status,13,MUTED,width=lw-40);p.progress((22,o+153,lw-48,6),self.record_level if self.recording else 0)
        o+=195;p.panel((2,o,lw-10,286));p.text(23,o+20,'Was wurde verstanden?',20,WHITE,True)
        if self.speech_error:
            p.panel((18,o+61,lw-43,123),'white',15,False);p.paragraph(35,o+77,self.speech_error,lw-80,15,INK,max_lines=5);p.button('speech-settings',(18,o+207,lw-43,47),'Mikrofon und Modelle prüfen',lambda:self.navigate('settings'),size=15)
        elif self.result:
            r=self.result;reliable=r.reliable and (not r.quality or r.quality.status!='bad');p.panel((18,o+61,lw-43,87),'white',15,False);p.paragraph(35,o+78,r.heard or 'Kein Text erkannt.',lw-80,23,INK,True,max_lines=2,lineheight=31)
            p.text(24,o+163,'Textübereinstimmung' if reliable else 'Aufnahme nicht zuverlässig auswertbar',14,MUTED,True,width=lw-70)
            if reliable:p.progress((24,o+195,lw-122,10),r.score/100);p.text(lw-79,o+184,str(r.score)+' %',20,'#79ecc1',True)
            p.paragraph(24,o+217,(r.quality.message if r.quality else '')+' · '+r.engine,lw-55,12,MUTED,max_lines=3,lineheight=17)
        else:
            p.panel((18,o+61,lw-43,95),'white',15,False);p.paragraph(35,o+78,'Noch keine Aufnahme ausgewertet. Hör dir das Wort an und sprich es danach selbst.',lw-80,17,INK,max_lines=3)
            p.paragraph(24,o+180,'Keine erfundene Aussprache-Note: Die Erkennung vergleicht Text, nicht einzelne Laute oder japanischen Tonhöhenakzent.',lw-55,14,MUTED,max_lines=4,lineheight=20)
        o+=304;p.button('speech-back',(18,o,lw-43,46),'Zurück zur Lernkarte  →',lambda:self.navigate('lesson'),'green',size=16);self.scroll_pane(s,p,x,y,vh,head_advance+562)
        self.teacher_stage(s,(rx,171,self.W-rx-16,self.H-181),'Ich höre zu. Sprich in deinem Tempo.' if self.recording else 'Hör erst zu. Danach probieren wir es gemeinsam.')
    def draw_listening(self,s):self.draw_library(s,True)
    def draw_vocab(self,s):self.draw_library(s,False)
    def draw_library(self,s,listening):
        self.heading(s,'Hören & nachsprechen' if listening else 'Deine Vokabeln','Japanisch, Lesung und Bedeutung – mit der Stimme deiner ausgewählten Lehrkraft.');x=294;w=self.W-x-25
        s.panel((x,184,w,62),'dark',14);s.icon('search',x+17,202,23,'#9abfe1');self.entry_target=('search',(x+54,197,w-328,34));all_=self.store.data.get('library_all',False)
        s.button('library-filter',(self.W-267,197,220,36),'Ganzer Kurs' if all_ else 'Bisher eingeführt',self.toggle_library,size=13);y=266;vh=self.H-y-24;cards=self.learning.available_cards(all_);q=self.query.lower().strip()
        if q:cards=[c for c in cards if q in (c['jp']+' '+c['romaji']+' '+c['de']).lower()]
        seen=set();unique=[]
        for c in cards:
            k=(c['jp'],c['de'])
            if k not in seen:seen.add(k);unique.append(c)
        p=self.make_pane(w,max(vh,950));o=-self.scroll;total=0
        left_w=(w-200)*.47;right_w=(w-200)*.45
        for c in unique:
            jl=p.wrap(c['jp'],left_w,25,True,True);rl=p.wrap(c['romaji'],left_w,14)
            dl=p.wrap(c['de'],right_w,16,True)
            inner=max(92,16+len(jl)*32+6+len(rl)*20+13,len(dl)*23+28);height=inner+43
            if o<vh+200 and o+height>0:
                p.panel((2,o+2,w-12,height-10),'dark',15);p.panel((16,o+15,w-188,inner),'white',13,False)
                q=o+27;q+=p.paragraph(32,q,c['jp'],left_w,25,INK,True,lineheight=32,jp=True)+6
                p.paragraph(33,q,c['romaji'],left_w,14,'#607da0',lineheight=20)
                dx=28+(w-200)*.51;p.paragraph(dx,o+29,c['de'],right_w,16,INK,True,lineheight=23)
                p.button('vocab-audio:'+c['key'],(w-154,o+15,124,38),'Hören',lambda c=c:self.speak(c['jp']),'blue','speaker',13)
                p.button('vocab-slow:'+c['key'],(w-154,o+65,124,38),'Langsam' if listening else 'Sprechen',lambda c=c:self.speak(c['jp'],True) if listening else self.speak_card(c,self.learning.by_key[c['lesson_key']]),'secondary','turtle' if listening else 'mic',12)
            o+=height;total+=height
        if not unique:p.paragraph(20,18,'Keine passenden Wörter gefunden.',w-50,18)
        self.scroll_pane(s,p,x,y,vh,max(110,total))
    def toggle_library(self):self.store.data['library_all']=not self.store.data.get('library_all',False);self.store.save();self.scroll=0;self.request_draw()
    def draw_grammar(self,s):
        self.heading(s,'Grammatik verstehen','Zum Nachschlagen: kurze Erklärungen und hörbare Beispielsätze.');x=294;y=192;w=self.W-x-26;vh=self.H-y-24;p=self.make_pane(w,max(vh,1000));o=-self.scroll;total=0
        for i,(title,jp,roma,explain) in enumerate(self.learning.catalog['GRAMMAR_TOPICS']):
            h=218
            if o<vh and o+h>0:
                p.panel((2,o+2,w-12,h-14),'dark',17);p.icon('layers',23,o+20,24);p.text(63,o+23,title,20,WHITE,True,width=w-120);p.panel((20,o+63,w-51,72),'white',13,False)
                p.fitted(36,o+77,jp,w-143,26,18,INK,True,True);p.text(36,o+111,roma,14,'#5a749b',width=w-170);p.icon('speaker',w-74,o+85,24,'#1d98ef');p.register('grammar-say:'+str(i),(w-92,o+67,55,64),lambda t=jp:self.speak(t))
                p.paragraph(24,o+151,explain,w-59,15,MUTED,max_lines=2,lineheight=21)
            total+=h;o+=h
        self.scroll_pane(s,p,x,y,vh,total)
    def draw_kanji(self,s):
        mode=self.kana_mode;self.heading(s,'Schriftzeichen','Kleine Gruppen statt Ratespiel. Klicke auf ein Zeichen, um es anzuhören.');x=294;y=186;w=self.W-x-25
        for i,label in enumerate(['Hiragana','Katakana','Kanji']):s.button('kana-tab:'+label,(x+i*170,y,157,43),label,lambda v=label:self.set_kana_mode(v),'blue' if mode==label else 'secondary',size=15)
        y+=68;vh=self.H-y-24;data=self.learning.catalog['KANJI'] if mode=='Kanji' else self.learning.catalog['KANA'];cols=5 if mode=='Kanji' else 8;gap=13;cw=(w-gap*(cols-1)-9)/cols;ch=176 if mode=='Kanji' else 125;p=self.make_pane(w,max(vh,1000));off=-self.scroll
        for i,row in enumerate(data):
            xx=i%cols*(cw+gap)+2;yy=i//cols*(ch+gap)+off
            if yy>vh+ch:break
            if yy+ch<=0:continue
            char=row[0]
            if mode=='Katakana':char=''.join(chr(ord(c)+96) if 0x3041<=ord(c)<=0x3096 else c for c in char)
            p.panel((xx,yy,cw,ch),'dark',14);p.text(xx+cw/2,yy+15,char,40,WHITE,True,align='center',jp=True);p.paragraph(xx+12,yy+70,row[1],cw-24,13,'#8ed0ff',max_lines=2,lineheight=18)
            if mode=='Kanji':p.paragraph(xx+12,yy+115,row[2],cw-24,12,MUTED,max_lines=3,lineheight=17)
            p.register('kana:'+str(i),(xx,yy,cw,ch),lambda c=char:self.speak(c),char)
        self.scroll_pane(s,p,x,y,vh,math.ceil(len(data)/cols)*(ch+gap))
    def set_kana_mode(self,mode):self.kana_mode=mode;self.scroll=0;self.request_draw()
    def new_writing(self):
        self.clear_reaction();self._last_write_check=None
        self.write_card=random.choice(self.learning.available_cards());self.write_feedback=''
        if self.entry and self.entry_mode=='writing':self.entry.delete(0,'end')
        self.request_draw()
    def set_write_mode(self,mode):self.write_mode=mode;self.new_writing()
    def check_writing(self):
        if not self.entry:return
        target=self.write_card['romaji'] if self.write_mode=='Romaji' else self.write_card['jp'];ok=any(matches_romaji(self.entry.get(),reading) for reading in [target]+self.write_card.get('romaji_aliases',[])) if self.write_mode=='Romaji' else Learning.normalize_answer(self.entry.get())==Learning.normalize_answer(target)
        self.write_feedback='Richtig – gut gelesen!' if ok else 'Noch nicht. Die Lösung ist: '+target
        if ok:self.store.touch_day()
        if getattr(self,'_last_write_check',None)!=(self.write_card['key'],self.write_mode,self.entry.get()):
            self.react('praise' if ok else 'encourage','write')
            self._last_write_check=(self.write_card['key'],self.write_mode,self.entry.get())
        self.request_draw()
    def draw_writing(self,s):
        self.heading(s,'Lesen & schreiben','Schreibe die Lesung oder das japanische Wort. Die Lösung wird vorher erklärt.');x=294;y=196;w=min(676,(self.W-x-42)*.62);rx=x+w+24;s.panel((x,y,w,480))
        for i,l in enumerate(['Romaji','Japanisch']):s.button('write-mode:'+l,(x+20+i*171,y+20,155,42),l,lambda v=l:self.set_write_mode(v),'blue' if self.write_mode==l else 'secondary',size=14)
        c=self.write_card;s.panel((x+20,y+83,w-40,131),'white',16,False);s.text(x+39,y+104,c['jp'] if self.write_mode=='Romaji' else c['de'],32,INK,True,width=w-83);s.text(x+39,y+157,'Bedeutung: '+c['de'] if self.write_mode=='Romaji' else 'Schreibe die japanische Form.',15,'#5b7599',width=w-83)
        s.text(x+23,y+242,'Deine Antwort',15,MUTED,True);s.panel((x+20,y+274,w-40,58),'white',14,False);self.entry_target=('writing',(x+36,y+284,w-74,38))
        s.button('write-check',(x+20,y+350,(w-51)/2,47),'Antwort prüfen',self.check_writing,'blue',size=15);s.button('write-new',(x+31+(w-51)/2,y+350,(w-51)/2,47),'Nächstes Wort',self.new_writing,size=15)
        if self.write_feedback:s.paragraph(x+25,y+421,self.write_feedback,w-50,15,'#95e8c1' if self.write_feedback.startswith('Richtig') else '#ffd1db',max_lines=2)
        s.panel((x,y+503,w,133));s.icon('info',x+23,y+526,23,BLUE);s.paragraph(x+64,y+522,'Im Modus „Japanisch“ kannst du die japanische Windows-Tastatur verwenden. Romaji schreibst du mit deiner normalen deutschen Tastatur.',w-88,15,MUTED,max_lines=4,lineheight=22)
        self.teacher_stage(s,(rx,186,self.W-rx-16,self.H-199),'Du darfst die Lesung in der Lernkarte jederzeit nachschauen.')
    def next_review(self):
        cards=self.learning.available_cards();review=self.store.data.setdefault('review',{});now=time.time();due=[c for c in cards if review.get(c['key'],{}).get('due',0)<=now]
        self.review_card=random.choice(due or cards);self.review_revealed=False;self.request_draw()
    def reveal_review(self):self.review_revealed=True;self.request_draw()
    def rate_review(self,known):
        if not self.review_revealed:return
        c=self.review_card;r=self.store.data.setdefault('review',{});old=r.get(c['key'],{});box=min(5,int(old.get('box',0))+1) if known else 0
        r[c['key']]={'box':box,'due':time.time()+[60,600,86400,259200,604800,2592000][box]};self.store.touch_day();self.store.save();self.next_review();self.react('praise' if known else 'encourage','review-known' if known else 'review-again')
    def draw_review(self,s):
        if self.review_card is None:self.review_card=self.learning.available_cards()[0]
        self.heading(s,'Wiederholen','Nur bereits eingeführte Wörter. Schwierige Wörter kommen früher wieder.');x=294;y=194;w=min(676,(self.W-x-40)*.62);rx=x+w+24;c=self.review_card;s.panel((x,y,w,470));s.icon('repeat',x+23,y+22,25);s.text(x+62,y+24,'Erinnerst du dich?',20,WHITE,True)
        s.panel((x+20,y+82,w-40,230),'white',16,False);s.fitted(x+40,y+106,c['jp'],w-80,47,25,INK,True,True);s.button('review-listen',(x+40,y+182,w-80,44),'Anhören',lambda:self.speak(c['jp']),'blue','speaker',15)
        if self.review_revealed:s.text(x+40,y+247,c['romaji'],20,'#567aa3',width=w-80);s.text(x+40,y+279,c['de'],16,INK,True,width=w-80)
        else:s.text(x+40,y+253,'Erst überlegen, dann aufdecken.',16,'#6d809a',width=w-80)
        s.button('review-reveal',(x+20,y+333,w-40,44),'Antwort aufdecken',self.reveal_review,size=15,enabled=not self.review_revealed)
        s.button('review-again',(x+20,y+396,(w-50)/2,48),'Noch üben',lambda:self.rate_review(False),size=15,enabled=self.review_revealed);s.button('review-known',(x+30+(w-50)/2,y+396,(w-50)/2,48),'Gewusst',lambda:self.rate_review(True),'green',size=15,enabled=self.review_revealed)
        self.teacher_stage(s,(rx,181,self.W-rx-16,self.H-194),'Wiederholung zählt. Es ist normal, etwas noch einmal zu brauchen.')
    def draw_progress(self,s):
        self.heading(s,'Dein Fortschritt','Gespeicherte Lernergebnisse – keine Beispielzahlen.');x=294;y=189;w=self.W-x-24;done=[k for k in self.store.data['completed'] if k in self.learning.by_key];gap=16;cw=(w-gap*2)/3
        for i,(a,b) in enumerate([(f'{len(done)} / {len(self.learning.lessons)}','Lektionen abgeschlossen'),(str(self.store.data['xp']),'Erfahrungspunkte'),(str(self.store.data['streak']),'Lerntage in Folge')]):
            xx=x+i*(cw+gap);s.panel((xx,y,cw,119));s.text(xx+25,y+23,a,30,WHITE,True);s.text(xx+25,y+78,b,14,MUTED,width=cw-42)
        y+=146;s.progress((x+1,y,w-3,11),len(done)/len(self.learning.lessons));y+=36;vh=self.H-y-25;p=self.make_pane(w,max(vh,800));o=-self.scroll;rows=[l for l in self.learning.lessons if l['key'] in done]
        if not rows:p.panel((2,o+2,w-10,160));p.text(25,o+24,'Deine erste Etappe wartet.',22,WHITE,True);p.button('progress-start',(25,o+79,240,46),'Erste Lektion starten',self.resume,'blue',size=15)
        for l in rows:
            if o>vh+85:break
            if o+79>0:p.panel((2,o+2,w-10,69),'dark',12);p.icon('check',23,o+23,25,'#70e5af');p.text(66,o+21,l['title'],18,WHITE,True,width=w-160)
            o+=83
        self.scroll_pane(s,p,x,y,vh,max(175,len(rows)*83))
    def draw_settings(self,s):
        self.heading(s,'Einstellungen','Stimmen, Mikrofon und Fortschritt bleiben lokal auf deinem Computer.');x=294;y=188;w=self.W-x-24;vh=self.H-y-24;p=self.make_pane(w,max(vh,1040));o=-self.scroll
        blocks=[('Sprechgeschwindigkeit',f"Aktuell: {float(self.store.data.get('tts_speed',1)):.2f}× · kombiniert mit dem Lehrerprofil.",'Tempo ändern',self.cycle_speed),('Mikrofon',next((n for i,n in self.devices if i==self.store.data.get('mic_device')),'Windows-Standardmikrofon'),'Mikrofon wählen',self.select_mic),('Oberflächengröße',f"Skalierung: {round(float(self.store.data.get('ui_scale',1))*100)} %",'Größe ändern',self.cycle_scale),('Figurenanimation','Dauerhafte Idle-Bewegung mit geschlossenem Mund. Lobreaktionen kommen zusätzlich dazu. Keine Lippensynchronisation.','Bewegung aus' if self.store.data.get('motion_enabled',True) else 'Bewegung an',self.toggle_motion),('Idle-Stärke',f"Aktuell: {PRESETS[preset_name(self.store.data.get('motion_preset'))][0]}. Atmen, Kopf, Haare und Kleidung; Kiko mit Ohren und Schwanz.",'Stärke: '+PRESETS[preset_name(self.store.data.get('motion_preset'))][0],self.cycle_motion_preset),('Kiko in der Seitenleiste','Ein Maskottchen, ein fester Platz. Keine doppelten Figuren.','Ausblenden' if self.store.data.get('show_kiko',True) else 'Einblenden',self.toggle_kiko),('Fortschritt sichern','Exportiert die Lerndaten. Sprachaufnahmen sind nicht enthalten.','Exportieren',self.export_progress),('Fortschritt wiederherstellen','Importiert eine vorher exportierte JSON-Sicherung.','Importieren',self.import_progress),('Offline-Modelle',('Stimmen vorhanden' if self.audio_status['tts'] else 'Stimmen fehlen')+' · '+('Erkennung vorhanden' if self.audio_status['asr'] else 'Erkennung fehlt'),'Modellordner öffnen',self.open_model_folder)]
        blocks.append(('Programm-Updates','Installierte Version: '+VERSION+' · Lernstand und Einstellungen bleiben erhalten.','Nach Updates suchen',self.open_updates))
        for i,(title,desc,label,action) in enumerate(blocks):
            if o+116>0 and o<vh:
                p.panel((2,o+2,w-10,104),'dark',16);p.text(24,o+21,title,18,WHITE,True,width=w-260);p.paragraph(24,o+54,desc,w-279,13,MUTED,max_lines=2,lineheight=19);p.button('setting:'+str(i),(w-235,o+33,206,43),label,action,size=13)
            o+=122
        p.panel((2,o+2,w-10,153));p.text(24,o+21,'Was die Sprachauswertung tatsächlich misst',19,WHITE,True,width=w-55);p.paragraph(24,o+60,'Der Prozentwert vergleicht die erkannte Aussage mit dem Zieltext. Er bewertet weder einzelne Laute noch den Tonhöhenakzent. Bei schlechter Aufnahmequalität wird keine Note vergeben.',w-57,15,MUTED,max_lines=4,lineheight=23)
        self.scroll_pane(s,p,x,y,vh,len(blocks)*122+165)
    def open_updates(self):
        from update_ui import show_updates
        show_updates(self,ROOT,VERSION)
    def cycle_speed(self):
        vals=[.75,.85,1.,1.1];old=float(self.store.data.get('tts_speed',1));self.store.data['tts_speed']=vals[(vals.index(old)+1)%len(vals)] if old in vals else 1.;self.store.save();self.request_draw()
    def cycle_scale(self):
        vals=[.9,1.,1.1];old=float(self.store.data.get('ui_scale',1));self.store.data['ui_scale']=vals[(vals.index(old)+1)%len(vals)] if old in vals else 1.;self.store.save();self.bg_cache.clear();self.scroll=0;self.request_draw()
    def toggle_kiko(self):self.store.data['show_kiko']=not self.store.data.get('show_kiko',True);self.store.save();self.request_draw()
    def select_mic(self):
        self.devices=[(None,'Windows-Standardmikrofon')]+self.engine.list_input_devices();win=tk.Toplevel(self.root);win.title('Mikrofon auswählen');win.configure(bg='#10243e');win.geometry('620x340');win.transient(self.root)
        tk.Label(win,text='Mikrofon für die Aufnahme auswählen',bg='#10243e',fg='white',font=('Segoe UI',13,'bold')).pack(padx=18,pady=17,anchor='w')
        lb=tk.Listbox(win,bg='#eef5ff',fg='#142942',selectbackground='#087fce',selectforeground='white',font=('Segoe UI',11),highlightthickness=0);lb.pack(padx=18,fill='both',expand=True)
        for id,name in self.devices:lb.insert('end',name)
        lb.selection_set(next((i for i,(id,n) in enumerate(self.devices) if id==self.store.data.get('mic_device')),0))
        def accept():
            ix=lb.curselection()
            if ix:self.store.data['mic_device']=self.devices[ix[0]][0];self.store.save()
            win.destroy();self.request_draw()
        tk.Button(win,text='Übernehmen',command=accept,bg='#008bed',fg='white',relief='flat',padx=20,pady=8).pack(pady=16);lb.bind('<Double-Button-1>',lambda e:accept());win.grab_set()
    def export_progress(self):
        path=filedialog.asksaveasfilename(parent=self.root,title='Fortschritt exportieren',defaultextension='.json',initialfile='JapanischTrainer_Fortschritt.json',filetypes=[('JSON-Datei','*.json')])
        if path:Path(path).write_text(json.dumps(self.store.data,ensure_ascii=False,indent=2),encoding='utf8');self.notify('Fortschritt exportiert.')
    def import_progress(self):
        path=filedialog.askopenfilename(parent=self.root,title='Fortschritt importieren',filetypes=[('JSON-Datei','*.json')])
        if not path:return
        try:
            d=json.loads(Path(path).read_text(encoding='utf8'))
            if not isinstance(d,dict) or not isinstance(d.get('completed'),list) or not isinstance(d.get('xp'),int):raise ValueError('Kein gültiger Fortschrittsexport.')
            if any(not isinstance(k,str) for k in d['completed']):raise ValueError('Ungültige Lektionskennungen.')
            if not messagebox.askyesno('Importieren','Fortschritt ersetzen? Die jetzigen Daten werden vorher gesichert.',parent=self.root):return
            self.store.save();shutil.copy2(self.store.path,self.store.path.with_name('progress.before-import.json'));self.store.data.update(d);self.store.save();self.store.load();self.notify('Fortschritt importiert.')
        except Exception as exc:messagebox.showerror('Import fehlgeschlagen',str(exc),parent=self.root)
        self.request_draw()
    def open_model_folder(self):
        if os.name=='nt':os.startfile(str(ROOT/'models'))
        else:self.notify('Modellordner: '+str(ROOT/'models'),9)
    def draw_complete(self,s):
        self.heading(s,'Lektion geschafft!','Dein Fortschritt. Kein Zeitdruck, keine verlorenen Leben.');x=294;y=196;w=min(674,(self.W-x-40)*.62);rx=x+w+25
        s.panel((x,y,w,430));s.icon('star',x+25,y+26,41,'#ffd375');s.text(x+84,y+28,'Gut gemacht!',31,WHITE,True);s.text(x+27,y+99,self.lesson['title'],23,WHITE,True,width=w-50);s.progress((x+27,y+152,w-54,13),1)
        s.panel((x+23,y+200,w-46,97),'white',16,False);s.text(x+43,y+222,str(len(self.lesson['cards']))+' Wörter / Lernkarten geübt',21,INK,True,width=w-83);s.text(x+43,y+263,'Fortschritt auf deinem Gerät gespeichert.',13,'#527396',width=w-83)
        s.button('complete-next',(x+24,y+327,w-48,57),'Zur nächsten Etappe  →',lambda:self.open_lesson(self.learning.next_lesson()['key']),'green',size=18);self.teacher_stage(s,(rx,189,self.W-rx-16,self.H-202),'Schritt für Schritt. Das hast du gut gemacht!')
    def hide_entry(self):
        if self.entry:
            if self.entry_mode=='study' and hasattr(self,'flow'):self.flow.input_text=self.entry.get()
            self.entry.destroy();self.entry=None;self.entry_mode=''
    def place_entry(self):
        if self.entry_target is None:self.hide_entry();return
        mode,b=self.entry_target
        if self.entry is None or self.entry_mode!=mode:
            self.hide_entry();self.entry_mode=mode;self.entry=tk.Entry(self.root,relief='flat',bd=0,highlightthickness=0,insertbackground='#4b8bbe',bg='#f3f8ff' if mode in ('writing','study') else '#112840',fg='#163559' if mode in ('writing','study') else '#f3f7ff')
            if mode=='search':self.entry.insert(0,self.query);self.entry.bind('<KeyRelease>',self.search_changed)
            elif mode=='study':self.entry.insert(0,self.flow.input_text);self.entry.bind('<KeyRelease>',self.learn_text_changed)
        x,y,w,h=b;sc=self.render_scale;family='Yu Gothic UI' if os.name=='nt' and mode=='writing' and self.write_mode=='Japanisch' else 'Segoe UI' if os.name=='nt' else 'DejaVu Sans'
        light=mode in ('writing','study') or (mode=='search' and self.view=='path')
        self.entry.configure(font=(family,max(11,round(16*sc))),bg='#f3f8ff' if light else '#112840',fg='#163559' if light else '#f3f7ff');self.entry.place(x=round(x*sc),y=round(y*sc),width=round(w*sc),height=round(h*sc))
    def search_changed(self,e):
        if self.entry and self.entry_mode=='search':self.query=self.entry.get();self.scroll=0;self.request_draw()
    def capture_and_exit(self):
        if self.render_error:raise RuntimeError('Starttest fehlgeschlagen: '+self.render_error)
        self.redraw();self.root.update_idletasks();out=Path(self.args.capture);out.parent.mkdir(parents=True,exist_ok=True);self.actors.composite(self.frame.image).convert('RGB').save(out);print('Live UI framebuffer:',out,flush=True);self.close()
    def close(self):
        if self.closed:return
        self.closed=True
        self.actors.close()
        if self.recording:
            try:self.engine.stop_recording()
            except Exception:pass
        try:
            import sounddevice as sd
            sd.stop()
        except Exception:pass
        try:self.store.save()
        except Exception:logging.exception('Could not save on close')
        self.root.destroy()

def enable_dpi():
    if os.name=='nt':
        try:
            import ctypes
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except Exception:pass

def main():
    import sys
    if len(sys.argv)==3 and sys.argv[1]=='--diagnostics':
        from diagnostics import run
        run(sys.argv[2]);return
    p=argparse.ArgumentParser(description='JapanischTrainer V11 - native Desktop-App');p.add_argument('--page',default='home',choices=[x[0] for x in NAV]+['lesson','complete']);p.add_argument('--lesson',default='');p.add_argument('--card',type=int,default=0);p.add_argument('--size',default='1440x1040');p.add_argument('--capture',default='');args=p.parse_args()
    enable_dpi();logging.basicConfig(filename=str(data_dir()/'application-v11.log'),level=logging.INFO,encoding='utf8',format='%(asctime)s %(levelname)s %(message)s');root=tk.Tk()
    def error(exc,val,tb):logging.error('Tk callback failed',exc_info=(exc,val,tb));messagebox.showerror('JapanischTrainer',str(val),parent=root)
    root.report_callback_exception=error;TrainerApp(root,args);root.mainloop()
if __name__=='__main__':main()

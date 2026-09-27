"""Native, state-driven UI components, not a mockup used as a background.

All panels, buttons, text and figures are independently drawn. Explicit alpha
composition prevents inherited themes from making a white learning card invisible.
The Tk window owns input/keyboard handling; this module owns high-quality painting.
Fonts come from the installed operating system. No font files are distributed.
"""
from __future__ import annotations
import math,os,re
from pathlib import Path
from functools import lru_cache
from dataclasses import dataclass
from typing import Callable
from PIL import Image,ImageDraw,ImageFont,ImageColor,ImageChops
WHITE='#f3f7ff';MUTED='#b5c6de';INK='#11253f';BLUE='#00a9ff';PINK='#ff99ca'

def rgba(c):
    if isinstance(c,tuple):return c if len(c)==4 else (*c,255)
    return ImageColor.getcolor(c,'RGBA')

def japanese(s):return bool(re.search('[\u3000-\u30ff\u3400-\u9fff]',str(s)))

@lru_cache(maxsize=256)
def font(size,bold=False,jp=False):
    paths=[]
    if os.name=='nt':
        win=Path(os.environ.get('WINDIR','C:/Windows'))/'Fonts'
        names=(['YuGothB.ttc','meiryob.ttc','YuGothM.ttc','meiryo.ttc'] if bold else ['YuGothM.ttc','meiryo.ttc','msgothic.ttc']) if jp else (['seguisb.ttf','segoeuib.ttf','arialbd.ttf'] if bold else ['segoeui.ttf','arial.ttf'])
        paths.extend(str(win/n) for n in names)
    if jp:paths.append('/usr/share/fonts/opentype/noto/NotoSansCJK-'+('Bold' if bold else 'Regular')+'.ttc')
    paths.extend(['/usr/share/fonts/opentype/inter/Inter-'+('SemiBold' if bold else 'Regular')+'.otf','/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf','/System/Library/Fonts/Helvetica.ttc'])
    p=next((p for p in paths if Path(p).is_file()),None)
    return ImageFont.truetype(p,max(8,int(size))) if p else ImageFont.load_default(size=max(8,int(size)))

@lru_cache(maxsize=180)
def panel_texture(w,h,r,top,bottom,border,thick=1):
    w=max(1,int(w));h=max(1,int(h));ss=2
    im=Image.new('RGBA',(w*ss,h*ss));d=ImageDraw.Draw(im);a,b=rgba(top),rgba(bottom)
    for y in range(h*ss):
        k=y/max(1,h*ss-1);d.line((0,y,w*ss,y),fill=tuple(round(a[i]*(1-k)+b[i]*k) for i in range(4)))
    mask=Image.new('L',im.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,w*ss-1,h*ss-1),radius=r*ss,fill=255)
    im.putalpha(ImageChops.multiply(im.getchannel('A'),mask))
    if border:ImageDraw.Draw(im).rounded_rectangle((1,1,w*ss-2,h*ss-2),radius=r*ss,outline=rgba(border),width=max(1,round(thick*ss)))
    return im.resize((w,h),Image.Resampling.LANCZOS)

@lru_cache(maxsize=80)
def load_image(path):
    with Image.open(path) as im:return im.convert('RGBA')

@lru_cache(maxsize=140)
def scaled_image(path,w,h,mode='contain',ay=0.):
    im=load_image(path);w=max(1,int(w));h=max(1,int(h))
    k=max(w/im.width,h/im.height) if mode=='cover' else min(w/im.width,h/im.height)
    out=im.resize((max(1,round(im.width*k)),max(1,round(im.height*k))),Image.Resampling.LANCZOS)
    if mode=='cover':
        x=(out.width-w)//2;y=round((out.height-h)*ay);out=out.crop((x,y,x+w,y+h))
    return out

@lru_cache(maxsize=250)
def icon_bitmap(name,size,color):
    # Consistent original geometric symbols; no platform-dependent emoji widgets.
    k=4;n=24*k;im=Image.new('RGBA',(n,n));d=ImageDraw.Draw(im);c=rgba(color)
    def coords(a):return [(x*k,y*k) for x,y in a]
    def ln(a,w=1.8):d.line(coords(a),fill=c,width=max(1,round(w*k)),joint='curve')
    def poly(a):d.polygon(coords(a),fill=c)
    def box(a,fill=False,r=2):d.rounded_rectangle(tuple(v*k for v in a),radius=r*k,fill=c if fill else None,outline=c,width=2*k)
    def el(a,fill=False):d.ellipse(tuple(v*k for v in a),fill=c if fill else None,outline=c,width=2*k)
    if name=='home':poly([(2,11),(12,2),(22,11),(19,11),(19,21),(14,21),(14,14),(10,14),(10,21),(5,21),(5,11)])
    elif name=='book':
        ln([(12,5),(8,3),(2,3),(2,20),(8,20),(12,22),(16,20),(22,20),(22,3),(16,3),(12,5),(12,22)])
        for y in (7,11):ln([(5,y),(9,y)]);ln([(15,y),(19,y)])
    elif name=='mic':
        box((8,2,16,16),r=4);d.arc((4*k,7*k,20*k,21*k),0,180,fill=c,width=2*k);ln([(12,21),(12,23)]);ln([(7,23),(17,23)])
    elif name=='headphones':d.arc((3*k,2*k,21*k,21*k),180,360,fill=c,width=2*k);box((2,11,6,21),True);box((18,11,22,21),True)
    elif name=='pencil':poly([(4,15),(16,3),(21,8),(9,20),(3,22)])
    elif name=='cards':box((3,3,16,19));box((9,6,22,22),True)
    elif name=='layers':poly([(2,7),(12,2),(22,7),(12,12)]);ln([(2,12),(12,17),(22,12)]);ln([(2,17),(12,22),(22,17)])
    elif name=='kanji':d.text((n/2,n/2),'漢',font=font(n-5,True,True),fill=c,anchor='mm')
    elif name=='repeat':
        d.arc((3*k,4*k,21*k,22*k),30,195,fill=c,width=2*k);d.arc((3*k,2*k,21*k,20*k),205,355,fill=c,width=2*k);poly([(1,10),(7,10),(2,4)]);poly([(23,14),(17,14),(22,20)])
    elif name=='chart':
        for x,y in [(2,13),(10,8),(18,2)]:box((x,y,x+4,22),True,1)
    elif name=='teachers':
        for b in [(8,1,16,9),(0,4,7,11),(17,4,24,11)]:el(b,True)
        box((7,12,17,23),True,4);box((0,13,5,22),True);box((19,13,24,22),True)
    elif name=='settings':
        poly([(12+math.sin(i*math.pi/16)*(11 if i%4<2 else 8),12+math.cos(i*math.pi/16)*(11 if i%4<2 else 8)) for i in range(32)])
        d.ellipse((8*k,8*k,16*k,16*k),fill=(8,24,43,255))
    elif name in ('back','left'):ln([(14,5),(7,12),(14,19)],2);ln([(7,12),(22,12)],2)
    elif name in ('right','arrow'):ln([(14,5),(21,12),(14,19)],2);ln([(2,12),(21,12)],2)
    elif name=='check':ln([(4,12),(9,18),(21,5)],2.5)
    elif name=='close':ln([(5,5),(19,19)],2);ln([(19,5),(5,19)],2)
    elif name=='play':poly([(6,2),(21,12),(6,22)])
    elif name=='pause':box((5,3,9,21),True,1);box((15,3,19,21),True,1)
    elif name=='speaker':
        poly([(2,9),(7,9),(13,4),(13,20),(7,15),(2,15)]);d.arc((9*k,6*k,20*k,18*k),285,75,fill=c,width=2*k);d.arc((10*k,2*k,26*k,22*k),292,68,fill=c,width=2*k)
    elif name=='turtle':d.pieslice((4*k,6*k,20*k,22*k),180,360,fill=c);el((18,10,24,16),True);ln([(7,17),(5,21)]);ln([(16,17),(18,21)])
    elif name=='flower':
        for i in range(5):
            a=i*2*math.pi/5-math.pi/2;x,y=12+5*math.cos(a),12+5*math.sin(a);el((x-5,y-5,x+5,y+5),True)
        d.ellipse((10*k,10*k,14*k,14*k),fill=(255,232,174,255))
    elif name=='flame':poly([(13,0),(16,7),(19,5),(22,13),(20,21),(12,24),(5,21),(2,15),(6,5),(8,11)]);d.polygon(coords([(12,10),(16,17),(14,21),(9,21),(7,18)]),fill=(255,230,150,255))
    elif name=='star':poly([(12+math.cos(i*math.pi/5-math.pi/2)*(11 if i%2==0 else 5),12+math.sin(i*math.pi/5-math.pi/2)*(11 if i%2==0 else 5)) for i in range(10)])
    elif name=='user':el((8,2,16,10),True);box((4,13,20,23),True,6)
    elif name=='info':
        el((1,1,23,23),True);d.ellipse((11*k,5*k,13*k,7*k),fill='white');d.rectangle((11*k,10*k,13*k,18*k),fill='white')
    elif name=='chat':
        box((1,3,23,19),True,7);poly([(6,17),(6,24),(13,18)])
        for x in (6,12,18):d.ellipse(((x-1)*k,10*k,(x+1)*k,12*k),fill=(13,31,52,255))
    elif name=='torii':poly([(0,2),(12,4),(24,2),(24,5),(12,7),(0,5)]);box((2,10,22,12),True,0);poly([(5,6),(8,6),(7,24),(4,24)]);poly([(16,6),(19,6),(20,24),(17,24)])
    elif name=='search':el((2,2,17,17));ln([(15,15),(23,23)],2.5)
    elif name=='lock':box((5,10,19,23),True,3);d.arc((7*k,1*k,17*k,16*k),180,360,fill=c,width=2*k)
    else:el((4,4,20,20))
    return im.resize((size,size),Image.Resampling.LANCZOS)

@dataclass
class Hit:
    id:str
    rect:tuple
    action:Callable
    label:str=''

class Surface:
    def __init__(self,w,h,scale=1.,image=None,hover='',focus=''):
        self.width=w;self.height=h;self.scale=scale;self.hover=hover;self.focus=focus;self.hits=[]
        self.image=image if image is not None else Image.new('RGBA',(round(w*scale),round(h*scale)),(0,0,0,0))
        self.draw=ImageDraw.Draw(self.image)
    def px(self,x):return round(x*self.scale)
    def bounds(self,b):return tuple(self.px(v) for v in b)
    def fill(self,b,color,radius=0):
        x,y,w,h=b
        if w>0 and h>0:self.draw.rounded_rectangle(self.bounds((x,y,x+w,y+h)),radius=self.px(radius),fill=rgba(color))
    def panel(self,b,kind='dark',radius=18,shadow=True,stroke=None):
        colors={'dark':('#10263fee','#0a192df5','#4380ad'),'solid':('#13283f','#091b30','#3d759d'),'soft':('#182e48ed','#102239f5','#345a7d'),'white':('#fbfdff','#f0f6ff','#dce8f5'),'info':('#e7f2ff','#d9eafb','#d6e8f8'),'bubble':('#fffcfd','#f9f8fb','#e9e7f0')}
        a,z,border=colors[kind];x,y,w,h=b
        if w<1 or h<1:return
        if shadow:self.fill((x+2,y+5,w,h),(0,4,15,80),radius)
        self.image.alpha_composite(panel_texture(self.px(w),self.px(h),self.px(radius),a,z,stroke or border),(self.px(x),self.px(y)))
    def text(self,x,y,text,size=16,color=WHITE,bold=False,width=None,align='left',jp=None):
        text=str(text);f=font(self.px(size),bold,japanese(text) if jp is None else jp)
        if width is not None:
            while len(text)>1 and f.getlength(text)>self.px(width):text=text[:-2].rstrip()+'…'
        self.draw.text((self.px(x),self.px(y)),text,font=f,fill=rgba(color),anchor={'left':'lt','right':'rt','center':'mt'}[align])
        return f.getlength(text)/self.scale
    def wrap(self,text,width,size=16,bold=False,jp=None):
        jp=japanese(text) if jp is None else jp;f=font(self.px(size),bold,jp);lines=[]
        for para in str(text).split('\n'):
            sep='' if jp and ' ' not in para else ' ';words=list(para) if not sep else para.split(' ');line=''
            for word in words:
                candidate=line+sep+word if line else word
                if line and f.getlength(candidate)>self.px(width):lines.append(line);line=word
                else:line=candidate
                while len(line)>1 and f.getlength(line)>self.px(width):
                    n=len(line)-1
                    while n>1 and f.getlength(line[:n])>self.px(width):n-=1
                    lines.append(line[:n]);line=line[n:]
            lines.append(line)
        return lines
    def paragraph(self,x,y,text,width,size=16,color=WHITE,bold=False,max_lines=None,lineheight=None,jp=None):
        jp=japanese(text) if jp is None else jp;lines=self.wrap(text,width,size,bold,jp);lh=lineheight or size*1.45
        if max_lines and len(lines)>max_lines:lines=lines[:max_lines];lines[-1]=lines[-1].rstrip(' .')+'…'
        for i,line in enumerate(lines):self.text(x,y+i*lh,line,size,color,bold,width,jp=jp)
        return len(lines)*lh
    def fitted(self,x,y,text,width,size=42,min_size=22,color=INK,bold=True,jp=None):
        while size>min_size and font(self.px(size),bold,japanese(text) if jp is None else jp).getlength(str(text))>self.px(width):size-=1
        return self.text(x,y,text,size,color,bold,width,jp=jp)
    def icon(self,name,x,y,size=24,color=WHITE):self.image.alpha_composite(icon_bitmap(name,max(1,self.px(size)),color),(self.px(x),self.px(y)))
    def image_at(self,path,b,mode='contain',ay=0.,align='center',radius=0):
        x,y,w,h=b;path=str(path)
        if w<=0 or h<=0 or not Path(path).is_file():return
        im=scaled_image(path,self.px(w),self.px(h),mode,ay)
        if radius:
            im=im.copy();mask=Image.new('L',im.size);ImageDraw.Draw(mask).rounded_rectangle((0,0,im.width-1,im.height-1),radius=self.px(radius),fill=255);im.putalpha(ImageChops.multiply(im.getchannel('A'),mask))
        dx=0 if align=='left' else self.px(w)-im.width if align=='right' else (self.px(w)-im.width)//2;dy=(self.px(h)-im.height)//2
        self.image.alpha_composite(im,(self.px(x)+dx,self.px(y)+dy))
    def register(self,id,b,action,label='',enabled=True):
        if enabled:self.hits.append(Hit(id,b,action,label))
    def button(self,id,b,label,action,kind='secondary',icon=None,size=15,enabled=True):
        x,y,w,h=b
        styles={'blue':('#149cff','#0071ea','#60d5ff'),'green':('#17bc6a','#07883e','#42e687'),'red':('#ff4266','#ed1545','#ff9bae'),'secondary':('#2a415f','#162a45','#647b96'),'answer':('#243a57','#142540','#c8d8ef'),'selected':('#2d905e','#0d7545','#62edb1'),'wrong':('#873747','#5c2433','#ff8598')}
        a,z,line=styles[kind]
        if self.hover==id and enabled:a,z=z,a
        if not enabled and kind not in ('selected','wrong'):a,z,line='#26394c','#1a293d','#34485e'
        self.image.alpha_composite(panel_texture(self.px(w),self.px(h),self.px(13),a,z,line,1.1),(self.px(x),self.px(y)))
        if self.focus==id:self.draw.rounded_rectangle(self.bounds((x-2,y-2,x+w+2,y+h+2)),radius=self.px(15),outline='#ffe4a0',width=max(1,self.px(2)))
        color=WHITE if enabled or kind in ('selected','wrong') else '#91a3b8'
        if icon:self.icon(icon,x+14,y+(h-22)/2,22,color);self.text(x+43,y+(h-size)/2-1,label,size,color,True,width=w-51)
        else:
            lines=self.wrap(label,w-18,size,True)[:2]
            for i,t in enumerate(lines):self.text(x+w/2,y+(h-len(lines)*(size+3))/2+i*(size+3),t,size,color,True,w-16,'center')
        self.register(id,b,action,label,enabled)
    def progress(self,b,value):
        x,y,w,h=b;self.fill(b,'#3e516e',h/2)
        if value>0:self.image.alpha_composite(panel_texture(self.px(max(h,w*min(1,value))),self.px(h),self.px(h/2),'#0ccc7b','#06b7c9',None),(self.px(x),self.px(y)))
    def compose(self,other,x,y,clip):
        cw,ch=clip;self.image.alpha_composite(other.image.crop((0,0,self.px(cw),self.px(ch))),(self.px(x),self.px(y)))
        for hit in other.hits:
            hx,hy,hw,hh=hit.rect
            if hy+hh<=0 or hy>=ch or hx+hw<=0 or hx>=cw:continue
            l,t=max(0,hx),max(0,hy);r,b=min(cw,hx+hw),min(ch,hy+hh)
            self.hits.append(Hit(hit.id,(x+l,y+t,r-l,b-t),hit.action,hit.label))

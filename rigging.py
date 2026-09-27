"""V10.1 bounded local 2D rig, with independently timed eyelids and secondary motion.

This is not Live2D, 3D, face tracking or phoneme lip-sync. It uses local mesh
influence regions and pre-authored eyelid/mouth patches over the supplied PNG artwork.
No whole-image rotation, zoom, vertical bouncing or automatic facial inference.
No webcam or extra speech model. Optional OpenCV acceleration; Pillow fallback.
"""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
import hashlib,json,math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
try:
    import cv2
    cv2.setNumThreads(1)
except (ImportError, OSError):
    cv2=None  # Native Pillow fallback, slower but functional.

from reactions import PROFILES, nod_envelope

TAU=math.tau

@dataclass(frozen=True)
class Pose:
    blink: float=0.
    breath: float=0.
    head: float=0.
    hair_left: float=0.
    hair_right: float=0.
    cloth: float=0.
    pendant: float=0.
    ear_left: float=0.
    ear_right: float=0.
    tail: float=0.
    nod: float=0.
    posture: float=0.
    head_lift: float=0.


def ease(x: float)->float:
    x=min(1.,max(0.,x));return x*x*(3-2*x)


def blink_envelope(age: float)->float:
    """Fast closure, brief hold, slower reopening. 270 ms total."""
    if age<0 or age>=.27:return 0.
    if age<.075:return ease(age/.075)
    if age<.12:return 1.
    return 1-ease((age-.12)/.15)


@lru_cache(maxsize=32)
def blink_schedule(seed: int)->tuple[float,...]:
    # Not a repeating sine wave; reproducible for QA, different for each actor.
    rng=np.random.default_rng(seed)
    points=[];at=1.8+float(rng.uniform(0,1.4))
    while at<83.:
        points.append(at)
        if len(points)%5==0:points.append(at+.38)
        at+=float(rng.uniform(3.4,6.4))
    return tuple(points)


def pose_at(t: float,seed: int,mood: str='idle',strength: float=1.,profile: dict|None=None)->Pose:
    """Continuous idle channels plus a small attentive attitude.

    Unlike a whole-sprite sway, the head, breathing, hair tips and fabric receive
    separate bounded rig fields. Hair lags the head; it does not reset on praise.
    The animation strength never changes blinking or expression visibility.
    """
    t=max(0.,float(t));strength=max(0.,min(1.5,float(strength)))
    p=profile or {};speed=float(p.get('tempo',1.));q=t*speed
    phase=(seed%59)/59*TAU;local=t%90.
    blink=max((blink_envelope(local-onset) for onset in blink_schedule(seed)),default=0.)
    breath=math.sin(q*TAU/4.9+phase)+.09*math.sin(q*TAU/2.45+phase*2-.2)
    def head_at(at):
        return .66*math.sin(at*TAU/10.4+phase)+.20*math.sin(at*TAU/17.3+phase*.3)
    h=head_at(q)
    if mood=='listening':h+=.30
    elif mood=='thinking':h-=.25
    elif mood=='speaking':h+=.10*math.sin(q*TAU/3.2)
    left=.72*math.sin(q*TAU/6.7+phase)+.23*head_at(q-.50)
    right=.66*math.sin(q*TAU/7.9+phase+.8)+.24*head_at(q-.72)
    cloth=.78*math.sin(q*TAU/9.6+phase-.45)+.14*math.sin(q*TAU/4.9+phase-.5)
    pendant=.70*math.sin(q*TAU/4.1+phase+.65)+.26*(head_at(q)-head_at(q-.4))
    age=(q+seed*.043)%11.4
    twitch=math.sin(age*TAU/.55)*math.sin(math.pi*age/.8) if age<.8 else 0.
    age2=(q+seed*.021+4.2)%13.9
    twitch2=math.sin(age2*TAU/.6)*math.sin(math.pi*age2/.9) if age2<.9 else 0.
    # Legacy direct renders may still request praise; the application always
    # calls this with idle for event reactions and adds the one-shot separately.
    tail_period=2.4 if mood=='praise' else 3.8
    tail=.85*math.sin(q*TAU/tail_period+phase)+.12*math.sin(q*TAU/8.1+phase)
    return Pose(blink=blink,breath=breath*strength*float(p.get('breath',1.)),
        head=h*strength*float(p.get('head',1.)),
        hair_left=left*strength*float(p.get('hair',1.)),
        hair_right=right*strength*float(p.get('hair',1.)),
        cloth=cloth*strength*float(p.get('cloth',1.)),
        pendant=pendant*strength,ear_left=twitch*strength,ear_right=twitch2*strength,
        tail=tail*strength,posture=.54*math.sin(q*TAU/14.1+phase-.3)*strength,
        head_lift=math.sin(q*TAU/4.9+phase-.10)*strength*float(p.get('breath',1.)))


@lru_cache(maxsize=8)
def rig_document(directory: str)->dict:
    file=Path(directory)/'rigs.json'
    try:
        data=json.loads(file.read_text(encoding='utf8'))
        return data.get('rigs',{}) if data.get('version')==1 else {}
    except (OSError,ValueError,TypeError):return {}


def locate_rig(path: str):
    file=Path(path)
    for parent in file.parents:
        if parent.name=='assets':
            folder=parent/'animation';identity=file.parent.name if file.parent.parent.name=='teachers' else file.stem
            return folder,identity,rig_document(str(folder)).get(identity,{})
    return file.parent,'',{}


@lru_cache(maxsize=8)
def expression_document(directory: str)->dict:
    try:
        data=json.loads((Path(directory)/'expressions.json').read_text(encoding='utf8'))
        return data.get('expressions',{}) if data.get('version')==1 else {}
    except (OSError,ValueError,TypeError):return {}


class CharacterRig:
    """Prepared sprite with shared-vertex mesh. Memory bounded to one actor size."""
    def __init__(self,path: str,w: int,h: int):
        self.path=str(path);self.size=(max(10,int(w)),max(10,int(h)))
        folder,self.identity,self.config=locate_rig(self.path)
        self.seed=int(self.config.get('seed',int.from_bytes(hashlib.md5(path.encode()).digest()[:2],'little')))
        with Image.open(path) as raw:original=raw.convert('RGBA')
        self.original_size=original.size
        pad=max(5,round(min(self.size)*.026))
        ratio=min((self.size[0]-pad*2)/original.width,(self.size[1]-pad*2)/original.height)
        sw=max(1,round(original.width*ratio));sh=max(1,round(original.height*ratio))
        self.scale=(sw/original.width,sh/original.height)
        self.offset=((self.size[0]-sw)//2,self.size[1]-pad-sh)
        fitted=original.resize((sw,sh),Image.Resampling.LANCZOS)
        self.base=Image.new('RGBA',self.size);self.base.alpha_composite(fitted,self.offset)
        self.expression_config=expression_document(str(folder)).get(self.identity,{})
        self.expression_patches={}
        for kind in ('idle','praise','encourage','cheeks','praise_face'):
            info=self.expression_config.get(kind)
            if not info:continue
            x0,y0,x1,y1=info['bbox'];sx,sy=self.scale;ox,oy=self.offset
            px0=round(x0*sx)+ox;py0=round(y0*sy)+oy
            size=(max(1,round(x1*sx)+ox-px0),max(1,round(y1*sy)+oy-py0))
            with Image.open(folder/self.identity/info['file']) as patch:
                self.expression_patches[kind]=(patch.convert('RGBA').resize(size,Image.Resampling.LANCZOS),(px0,py0))
        if 'idle' in self.expression_patches:
            patch,pos=self.expression_patches['idle'];self.base.alpha_composite(patch,pos)
        self._expression_cache_key=None;self._expression_cache=None
        self.eye_frames=[];self.eye_amounts=[0.];self.eye_pos=(0,0)
        blink=self.config.get('blink')
        if blink:
            x0,y0,x1,y1=blink['bbox'];sx,sy=self.scale;ox,oy=self.offset
            px0=round(x0*sx)+ox;py0=round(y0*sy)+oy
            bw=max(1,round(x1*sx)+ox-px0);bh=max(1,round(y1*sy)+oy-py0)
            self.eye_pos=(px0,py0);self.eye_frames=[Image.new('RGBA',(bw,bh))]
            for filename in blink['frames']:
                with Image.open(folder/self.identity/filename) as frame:
                    self.eye_frames.append(frame.convert('RGBA').resize((bw,bh),Image.Resampling.LANCZOS))
            self.eye_amounts=[0.]+list(blink['amounts'])
        self._last_eye_key=None;self._last_eye_patch=None
        self._prepare_mesh()

    def _prepare_mesh(self):
        w,h=self.size
        # Equal shared vertices avoid cracks between deformed tiles.
        gx=np.unique(np.round(np.linspace(0,w,max(9,min(25,w//18))+1))).astype(int)
        gy=np.unique(np.round(np.linspace(0,h,max(13,min(43,h//18))+1))).astype(int)
        X,Y=np.meshgrid(gx,gy);self.grid=np.stack([X,Y],axis=-1).astype(np.float64)
        self.boxes=[(int(gx[i]),int(gy[j]),int(gx[i+1]),int(gy[j+1])) for j in range(len(gy)-1) for i in range(len(gx)-1)]
        sx,sy=self.scale;ox,oy=self.offset;x=(X-ox)/sx;y=(Y-oy)/sy
        self.fields=[]
        if cv2 is not None:
            # Exact interpolation in the same shared-vertex mesh as the fallback.
            ix=np.interp(np.arange(w),gx,np.arange(len(gx))).astype(np.float32)
            iy=np.interp(np.arange(h),gy,np.arange(len(gy))).astype(np.float32)
            self.dense_ix,self.dense_iy=np.meshgrid(ix,iy)
            yy,xx=np.mgrid[0:h,0:w]
            self.pixel_grid=np.stack([xx,yy],axis=-1).astype(np.float32)
        # Outer gutter and source boundary are fixed, not cropped by a rotation.
        edge=np.minimum.reduce([np.clip(x/34,0,1),np.clip((self.original_size[0]-x)/34,0,1),np.clip(y/30,0,1),np.clip((self.original_size[1]-y)/34,0,1)])
        for spec in self.config.get('fields',[]):
            cx,cy=spec['center'];rx,ry=spec['radii'];q=((x-cx)/rx)**2+((y-cy)/ry)**2
            amount=np.clip((1-q)/.68,0,1);weight=amount*amount*(3-2*amount)*edge
            dx=np.zeros_like(x);dy=np.zeros_like(y)
            if 'pivot' in spec:
                px,py=spec['pivot'];angle=math.radians(spec['angle']);dx=-(y-py)*angle;dy=(x-px)*angle
            if 'move' in spec:dx+=spec['move'][0];dy+=spec['move'][1]
            self.fields.append((spec['channel'],np.stack([dx*sx*weight,dy*sy*weight],axis=-1)))

    def idle_pose(self,t: float,mood: str='idle',strength: float=1.)->Pose:
        # Praise/encouragement overlay the same ongoing idle. Neither changes
        # phase, frequency nor animation clock of breathing/hair/tail.
        base_mood='idle' if mood in ('praise','encourage') else mood
        return pose_at(t,self.seed,base_mood,strength,self.config.get('idle_profile'))

    def displacement(self,pose: Pose)->np.ndarray:
        delta=np.zeros_like(self.grid)
        for name,field in self.fields:
            value=getattr(pose,name,0.)
            limit=self.config.get('channel_limits',{}).get(name)
            if limit:
                # Smooth saturation keeps Kiko's narrow tail-root mesh from
                # compressing sharply when lively idle and a cheer overlap.
                value=float(limit)*math.tanh(value/float(limit))
            delta+=value*field
        return delta

    def _eyelids(self,amount: float,source=None):
        source=self.base if source is None else source
        if not self.eye_frames or amount<=.001:return source
        # Five local source patches, interpolate between adjacent closure stages.
        amount=min(1.,max(0.,amount));step=int(np.searchsorted(self.eye_amounts,amount,side='right'))
        step=min(step,len(self.eye_frames)-1);prev=max(0,step-1)
        span=self.eye_amounts[step]-self.eye_amounts[prev]
        mix=(amount-self.eye_amounts[prev])/span if span else 1.
        key=(prev,step,round(mix,2))
        if key!=self._last_eye_key:
            self._last_eye_patch=Image.blend(self.eye_frames[prev],self.eye_frames[step],key[2]);self._last_eye_key=key
        source=source.copy();source.alpha_composite(self._last_eye_patch,self.eye_pos)
        return source

    def _face(self,mood: str,amount: float):
        if mood not in ('praise','encourage') or amount<=.001:return self.base
        amount=round(min(1.,max(0.,amount)),2);key=(mood,amount)
        if key==self._expression_cache_key:return self._expression_cache
        source=self.base.copy()
        kinds=['praise','cheeks','praise_face'] if mood=='praise' else ['encourage']
        for kind in kinds:
            if kind not in self.expression_patches:continue
            patch,pos=self.expression_patches[kind]
            if amount<.999:
                patch=patch.copy();patch.putalpha(patch.getchannel('A').point(lambda a:round(a*amount)))
            source.alpha_composite(patch,pos)
        # Expressions may change facial colour, never cutout coverage.
        source.putalpha(self.base.getchannel('A'))
        self._expression_cache_key=key;self._expression_cache=source
        return source

    def _sparkles(self,image,age,amount):
        if amount<=.02:return image
        # Three small one-shot sparkles inside this actor's own transparent canvas.
        # No effects are drawn on words, answers, buttons or other actors.
        mascot=self.identity=='kiko_idle'
        joy=PROFILES.get(self.identity,{}).get('joy',1.0)
        center=self.expression_config.get('head',[515,270]);sx,sy=self.scale;ox,oy=self.offset
        offsets=[(-112,-139),(105,-131),(-143,-53)] if mascot else [(-177,-127),(176,-97),(-146,-211)]
        d=ImageDraw.Draw(image)
        for i,(dx,dy) in enumerate(offsets):
            u=max(0.,min(1.,(age-i*.09)/1.55));visible=amount*math.sin(math.pi*min(1.,u+.10))
            if visible<=.02:continue
            x=ox+(center[0]+dx)*sx;y=oy+(center[1]+dy)*sy-u*(6 if mascot else 12)
            radius=(2.8+1.5*joy)*(1+.12*math.sin(age*9+i))
            x=min(image.width-radius-3,max(radius+3,x));y=min(image.height-radius-3,max(radius+3,y))
            rgba=(255,217,138,round(190*visible))
            d.polygon([(x,y-radius),(x+radius*.3,y-radius*.27),(x+radius,y),
                       (x+radius*.3,y+radius*.27),(x,y+radius),(x-radius*.3,y+radius*.27),
                       (x-radius,y),(x-radius*.3,y-radius*.27)],fill=rgba)
        return image

    def render(self,t: float,mood: str='idle',strength: float=1.,enabled: bool=True,pose: Pose|None=None,
               reaction_strength: float|None=None,reaction_age: float=0.)->Image.Image:
        # Legacy/static renders never start a reaction just because a word was read.
        amount=0. if reaction_strength is None else min(1.,max(0.,reaction_strength))
        if not enabled or not self.config:
            return self._face(mood,amount).copy()
        pose=pose or self.idle_pose(t,mood,strength)
        source=self._face(mood,amount)
        if not (self.identity=='kiko_idle' and mood=='praise' and amount>.5):
            source=self._eyelids(pose.blink,source)
        displacement=self.displacement(pose)
        if cv2 is not None:
            dense=cv2.remap(displacement.astype(np.float32),self.dense_ix,self.dense_iy,
                            cv2.INTER_LINEAR,borderMode=cv2.BORDER_REPLICATE)
            inverse=self.pixel_grid-dense
            # Interpolate premultiplied alpha to prevent dark outlines on hair/fur.
            premult=np.asarray(source.convert('RGBa'))
            result=cv2.remap(premult,inverse,None,cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_CONSTANT,borderValue=(0,0,0,0))
            result=Image.fromarray(result,'RGBa').convert('RGBA')
            return self._sparkles(result,reaction_age,amount) if mood=='praise' else result
        v=self.grid-displacement
        # Pillow QUAD ordering: upper left, lower left, lower right, upper right.
        a=v[:-1,:-1];b=v[1:,:-1];c=v[1:,1:];d=v[:-1,1:]
        quads=np.stack([a,b,c,d],axis=2).reshape(-1,8)
        mesh=list(zip(self.boxes,map(tuple,quads)))
        result=source.transform(self.size,Image.Transform.MESH,mesh,Image.Resampling.BILINEAR)
        return self._sparkles(result,reaction_age,amount) if mood=='praise' else result

    @property
    def capabilities(self):
        return {'rig':bool(self.config),'blink':bool(self.eye_frames),'channels':sorted({n for n,_ in self.fields}),
                'closed_idle':bool(self.expression_config.get('closed_idle')),
                'expressions':sorted(self.expression_patches)}

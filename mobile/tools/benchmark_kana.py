"""Controlled synthetic-audio comparison; not a human pronunciation/microphone test.

Uses the installed, unchanged Supertonic/SenseVoice models. Output stays under
ignored validation/. The Kotlin input algorithm is mirrored for host comparison;
native tests separately execute SpeechInput and the bundled VAD.
"""
from pathlib import Path
import json, re, sys
import numpy as np
import sherpa_onnx as so
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT))
from speech_engine import LocalSpeechEngine
OUT=ROOT/'validation/asr-1108';OUT.mkdir(parents=True,exist_ok=True)
def normalize(s):
    return ''.join(chr(ord(c)-96) if 'ァ'<=c<='ヶ' else c for c in re.sub(r'[\s。、！？!?.,]','',s))
def prepare(x,short):
    if not len(x) or len(x)>256000 or not np.isfinite(x).all() or np.mean(np.abs(x)>=.985)>=.08:return None
    x=x.astype(np.float32)-float(np.mean(x));peak=float(np.max(np.abs(x)))
    energy=np.array([np.sqrt(np.mean(x[i:i+320]**2)) for i in range(0,len(x),320)])
    active=np.where(energy>=max(.0006,float(energy.max())*.08))[0]
    if peak<.001 or len(active)<(4 if short else 8):return None
    y=x[max(0,active[0]*320-2400):min(len(x),(active[-1]+1)*320+3200)]
    gain=max(1.,min(10.,.08/max(.0001,np.sqrt(np.mean(y*y))),.9/peak))
    return (y*gain).astype(np.float32)
def vad(x,short):
    cfg=so.VadModelConfig();cfg.silero_vad.model=str(ROOT/'mobile/app/src/main/assets/speech/silero_vad.onnx')
    cfg.silero_vad.threshold=.5;cfg.silero_vad.min_speech_duration=.064 if short else .128
    cfg.silero_vad.min_silence_duration=.3;cfg.sample_rate=16000
    v=so.VoiceActivityDetector(cfg,buffer_size_in_seconds=20)
    for offset in range(0,len(x),512):v.accept_waveform(np.pad(x[offset:offset+512],(0,max(0,offset+512-len(x)))))
    v.flush();return not v.empty()
def old_gate(x):
    return len(x)>=6400 and np.max(np.abs(x))>.012 and np.sqrt(np.mean(x*x))>.002 and np.sum(np.abs(x)>.015)>600
def main():
    targets=['あ','い','う','え','お','か','し','つ','ん','きゃ','ねこ','みずをのみます。']
    aliases={'ねこ':['ねこ','猫'],'みずをのみます。':['みずをのみます','水を飲みます']}
    engine=LocalSpeechEngine();tts=engine._ensure_tts();cases=[]
    for speaker in [2,0,6,9]:
        for target in targets:
            cache=OUT/f'voice-{speaker}-{target.rstrip("。").replace("。","")}.npy'
            if cache.exists():x=np.load(cache)
            else:
                gen=so.GenerationConfig();gen.sid=speaker;gen.speed=.95;gen.num_steps=8;gen.extra={'lang':'ja'}
                a=tts.generate(target,gen)
                x=np.interp(np.arange(int(len(a.samples)*16000/a.sample_rate))*a.sample_rate/16000,np.arange(len(a.samples)),a.samples).astype(np.float32)
                np.save(cache,x)
            for label,scale,pad in [('clean',1,0),('quiet',.025,0),('delayed',.025,16000)]:
                cases.append((speaker,target,label,np.pad(x*scale,(pad,pad)).astype(np.float32)))
    del tts;engine._tts=None
    records={itn:so.OfflineRecognizer.from_sense_voice(model=str(ROOT/'models/sensevoice/model.int8.onnx'),tokens=str(ROOT/'models/sensevoice/tokens.txt'),language='ja',use_itn=itn,num_threads=4) for itn in (True,False)}
    report={'synthetic':True,'human_microphone':False,'held_out_speakers':[6,9],'cases':[]}
    for speaker,target,label,x in cases:
        short=target not in aliases;p=prepare(x,short);qualified=p is not None and vad(p,short)
        old=engine._decode(records[True],x,16000) if old_gate(x) else '<audio-rejected>'
        new=engine._decode(records[not short],np.pad(p,(1600,4800)),16000) if qualified else '<audio-rejected>'
        accepted=[normalize(t) for t in aliases.get(target,[target])]
        report['cases'].append(dict(speaker=speaker,target=target,variant=label,short=short,qualified=bool(qualified),old=old,new=new,old_match=normalize(old) in accepted,new_match=normalize(new) in accepted))
        print(f'{speaker} {target} {label}: {old} -> {new}',flush=True)
    negatives={'silence':np.zeros(32000),'click':np.r_[np.zeros(8000),.5,np.zeros(8000)],'hum':.02*np.sin(2*np.pi*100*np.arange(32000)/16000),'clipping':np.tile([1.,-1.],16000)}
    for seed in [1,77,123]:
        for level in [.001,.01,.08]:negatives[f'noise-{seed}-{level}']=np.random.default_rng(seed).normal(0,level,32000)
    report['negative']={}
    for name,x in negatives.items():
        p=prepare(x,True);report['negative'][name]=bool(p is not None and vad(p,True))
    report['summary']={}
    for label in ['clean','quiet','delayed']:
        rows=[c for c in report['cases'] if c['short'] and c['variant']==label]
        report['summary'][label]={'cases':len(rows),'old_match':sum(c['old_match'] for c in rows),'new_match':sum(c['new_match'] for c in rows),'qualified':sum(c['qualified'] for c in rows),'regressions':sum(c['old_match'] and not c['new_match'] for c in rows)}
    (OUT/'final-comparison.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf8')
    print(json.dumps({'summary':report['summary'],'negative':report['negative']},indent=2))
    assert not any(report['negative'].values()),'Noise-only fixture was qualified'
if __name__=='__main__':main()

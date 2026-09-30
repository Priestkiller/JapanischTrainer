"""Target-blind optional-model comparison, with the same signal gate as Android."""
import gc,time
import numpy as np
from speech_engine import app_root,SENSEVOICE_DIR,PARAKEET_DIR
import modelpacks

class NoVoice(ValueError):pass
def prepare(raw,rate,short):
    raw=np.asarray(raw,dtype=np.float32)
    if not len(raw) or len(raw)>rate*16 or not np.isfinite(raw).all():raise ValueError('Keine gültige Aufnahme')
    if np.mean(np.abs(raw)>=.985)>=.08:raise ValueError('Aufnahme übersteuert')
    x=np.interp(np.arange(int(len(raw)*16000/rate))*rate/16000,np.arange(len(raw)),raw).astype(np.float32)
    x-=float(np.mean(x));peak=float(np.max(np.abs(x)))
    energy=np.array([np.sqrt(np.mean(x[i:i+320]**2)) for i in range(0,len(x),320)])
    active=np.where(energy>=max(.0006,float(energy.max())*.08))[0]
    if peak<.001 or len(active)<(4 if short else 8):raise NoVoice('Keine ausreichend hörbare Stimme. Bei der Stilleprobe ist das erwartbar.')
    segment=x[max(0,active[0]*320-2400):min(len(x),(active[-1]+1)*320+3200)]
    gain=max(1.,min(10.,.08/max(.0001,np.sqrt(np.mean(segment*segment))),.9/peak))
    return (segment*gain).astype(np.float32)
def compare(raw,rate,short,cancel=lambda:False):
    import sherpa_onnx as so
    try:audio=prepare(raw,rate,short)
    except NoVoice as e:return dict(status='no_voice',message=str(e),results=[])
    cfg=so.VadModelConfig();cfg.silero_vad.model=str(app_root()/'data/speech/silero_vad.onnx');cfg.silero_vad.threshold=.5;cfg.silero_vad.min_speech_duration=.064 if short else .128;cfg.silero_vad.min_silence_duration=.3;cfg.sample_rate=16000
    vad=so.VoiceActivityDetector(cfg,buffer_size_in_seconds=20)
    for offset in range(0,len(audio),512):vad.accept_waveform(np.pad(audio[offset:offset+512],(0,max(0,offset+512-len(audio)))))
    vad.flush()
    if vad.empty():return dict(status='no_voice',message='Keine sichere Stimme erkannt.',results=[])
    del vad
    audio=np.pad(audio,(1600,4800));rows=[]
    kinds=['sensevoice','parakeet']+[k for k in modelpacks.NAMES if modelpacks.ready(k)]
    for kind in kinds:
        if cancel():raise RuntimeError('Vergleich abgebrochen')
        start=time.perf_counter();rec=None
        try:
            if kind=='sensevoice':rec=so.OfflineRecognizer.from_sense_voice(model=str(SENSEVOICE_DIR/'model.int8.onnx'),tokens=str(SENSEVOICE_DIR/'tokens.txt'),language='ja',use_itn=not short,num_threads=2)
            elif kind=='parakeet':rec=so.OfflineRecognizer.from_nemo_ctc(model=str(PARAKEET_DIR/'model.int8.onnx'),tokens=str(PARAKEET_DIR/'tokens.txt'),num_threads=2)
            else:rec=modelpacks.recognizer(kind)
            loaded=time.perf_counter();stream=rec.create_stream()
            if kind=='qwen3':stream.set_option('language','Japanese')
            stream.accept_waveform(16000,audio);rec.decode_stream(stream);text=stream.result.text;del stream
            rows.append(dict(model=kind,text=text,loadMs=round((loaded-start)*1000),decodeMs=round((time.perf_counter()-loaded)*1000)))
        except Exception as e:rows.append(dict(model=kind,error=str(e),text=''))
        finally:del rec;gc.collect()
    return dict(status='decoded',audioQualified=True,results=rows)

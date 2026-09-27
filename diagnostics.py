"""Real offline model inference. No microphone, cloud service, or speaker playback."""
import json
import socket
import time
from pathlib import Path
import wave
import numpy as np
import speech_engine


def run(output):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    started=time.monotonic()
    report={'passed':False,'microphone':False,'speaker_playback':False,'network_connections_allowed':False,'teachers':[]}
    original_connect=socket.socket.connect
    original_audio=speech_engine.sd
    class CaptureSink:
        samples=None
        @staticmethod
        def stop():pass
        @classmethod
        def play(cls,samples,sample_rate,blocking=True):cls.samples=np.asarray(samples).copy();cls.sample_rate=sample_rate
    def offline(*args,**kwargs):raise RuntimeError('Network access forbidden during offline test')
    socket.socket.connect=offline
    speech_engine.sd=CaptureSink
    try:
        engine=speech_engine.LocalSpeechEngine()
        catalog=json.loads((speech_engine.ROOT/'data/catalog.json').read_text(encoding='utf8'))
        for teacher in catalog['TEACHERS']:
            durations=[]
            for slow in (False,True):
                engine.speak('ありがとうございます。',teacher['speed']*(.72 if slow else 1.),teacher['speaker_id'])
                samples=CaptureSink.samples;rate=CaptureSink.sample_rate
                if samples is None or len(samples)<rate*.2 or not np.isfinite(samples).all() or np.max(np.abs(samples))<.01:
                    raise RuntimeError('Keine brauchbare Sprachausgabe: '+teacher['id'])
                durations.append(round(len(samples)/rate,3))
                if not slow:
                    with wave.open(str(output/(teacher['id']+'.wav')),'wb') as file:
                        file.setparams((1,2,rate,0,'NONE','not compressed'));file.writeframes((np.clip(samples,-1,1)*32767).astype('<i2').tobytes())
                    if teacher['id']=='sakura':reference=samples.copy();reference_rate=rate
            report['teachers'].append({'teacher':teacher['id'],'speaker_id':teacher['speaker_id'],'normal_seconds':durations[0],'slow_seconds':durations[1]})
            (output/'progress.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
        parakeet=engine._ensure_parakeet();sense=engine._ensure_sensevoice()
        report['parakeet']=engine._decode(parakeet,reference,reference_rate)
        report['sensevoice']=engine._decode(sense,reference,reference_rate)
        if not report['parakeet'] or not report['sensevoice']:raise RuntimeError('Spracherkennung ergab keinen Text.')
        result=engine.recognize_for_target(reference,['ありがとうございます'],reference_rate)
        report['target_result']={'heard':result.heard,'score':result.score,'reliable':result.reliable}
        silent=engine.recognize_for_target(np.zeros(48000,dtype=np.float32),['ありがとうございます'],48000)
        if silent.reliable:raise RuntimeError('Stille darf keinen zuverlässigen Treffer ergeben.')
        report['silence_rejected']=True
        report['passed']=True
    except Exception as exc:
        report['error']=str(exc)
        raise
    finally:
        socket.socket.connect=original_connect;speech_engine.sd=original_audio
        report['seconds']=round(time.monotonic()-started,2)
        (output/'audio-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')


if __name__=='__main__':
    import sys
    run(sys.argv[1])

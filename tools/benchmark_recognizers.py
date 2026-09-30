"""Compare identical waveforms. Synthetic/public fixtures are NOT S24 microphone tests.

No expected phrase is passed into either recognizer. Keeps raw results in ignored
validation/. Human exports can be evaluated separately using the same contract.
"""
import argparse,json,time,sys,gc
from pathlib import Path
import numpy as np
import sherpa_onnx as so
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from mobile.tools.benchmark_kana import prepare,vad,normalize


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--model-dir',type=Path,default=ROOT/'validation/asr-1111/reazonspeech')
    parser.add_argument('--output',type=Path,default=ROOT/'validation/asr-1111/comparison.json');args=parser.parse_args()
    fixtures=[]
    for sid in (2,6):
        for target in ('あ','い','う','え','お','か','し','つ','ん','きゃ','ねこ','みずをのみます'):
            path=ROOT/f'validation/asr-1108/voice-{sid}-{target}.npy'
            if path.is_file():fixtures.append(dict(id=f'synthetic-{sid}-{target}',expected=target,kind='synthetic',audio=np.load(path,allow_pickle=False),short=len(target)<=2 and target!='ねこ'))
    for name,audio in {'silence':np.zeros(32000),'noise':np.random.default_rng(2026).normal(0,.01,32000),'click':np.r_[np.zeros(8000),.5,np.zeros(8000)]}.items():
        fixtures.append(dict(id=name,expected='',kind='negative',audio=audio,short=True))
    assert len(fixtures)>3,'Synthetic fixture cache is missing; run benchmark_kana.py first.'
    prepared=[]
    for f in fixtures:
        x=prepare(f['audio'],f['short']);qualified=x is not None and vad(x,f['short'])
        prepared.append({**f,'qualified':qualified,'prepared':np.pad(x,(1600,4800)) if qualified else None})
    results={};cold={}
    for backend in ('sensevoice','reazonspeech','qwen3'):
        start=time.perf_counter()
        if backend=='sensevoice':rec=so.OfflineRecognizer.from_sense_voice(model=str(ROOT/'models/sensevoice/model.int8.onnx'),tokens=str(ROOT/'models/sensevoice/tokens.txt'),language='ja',use_itn=False,num_threads=2)
        elif backend=='qwen3':
            q=ROOT/'validation/asr-1111/qwen3';rec=so.OfflineRecognizer.from_qwen3_asr(conv_frontend=str(q/'conv_frontend.onnx'),encoder=str(q/'encoder.int8.onnx'),decoder=str(q/'decoder.int8.onnx'),tokenizer=str(q/'tokenizer'),num_threads=2,max_new_tokens=80)
        else:rec=so.OfflineRecognizer.from_transducer(encoder=str(args.model_dir/'encoder-epoch-99-avg-1.int8.onnx'),decoder=str(args.model_dir/'decoder-epoch-99-avg-1.int8.onnx'),joiner=str(args.model_dir/'joiner-epoch-99-avg-1.int8.onnx'),tokens=str(args.model_dir/'tokens.txt'),num_threads=2,decoding_method='greedy_search')
        cold[backend]=time.perf_counter()-start;rows=[]
        for f in prepared:
            heard='';start=time.perf_counter()
            if f['qualified']:
                stream=rec.create_stream()
                if backend=='qwen3':stream.set_option('language','Japanese')
                stream.accept_waveform(16000,f['prepared']);rec.decode_stream(stream);heard=stream.result.text;del stream
            aliases={'ねこ':['猫'],'みずをのみます':['水を飲みます']}.get(f['expected'],[])
            match=f['qualified'] and normalize(heard) in [normalize(x) for x in [f['expected'],*aliases]]
            rows.append(dict(id=f['id'],kind=f['kind'],expected=f['expected'],short=f['short'],qualified=bool(f['qualified']),heard=heard,match=bool(match),seconds=round(time.perf_counter()-start,4)))
        results[backend]=rows;del rec;gc.collect();print(backend, 'matches',sum(x['match'] for x in rows),'/',sum(x['kind']=='synthetic' for x in rows),flush=True)
    report={'human_microphone':False,'s24_measurement':False,'expected_text_given_to_recognizer':False,'language':'Japanese explicitly selected for SenseVoice and Qwen3; ReazonSpeech is Japanese-only','cold_start_seconds':cold,'cases':results}
    report['summary']={b:{'synthetic_matches':sum(x['match'] for x in rows),'synthetic_count':sum(x['kind']=='synthetic' for x in rows),'negative_qualified':sum(x['qualified'] for x in rows if x['kind']=='negative'),'p95_decode_seconds':float(np.percentile([x['seconds'] for x in rows if x['qualified']],95))} for b,rows in results.items()}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf8');print(json.dumps(report['summary'],indent=2))
    assert all(v['negative_qualified']==0 for v in report['summary'].values())

if __name__=='__main__':main()

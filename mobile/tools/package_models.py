"""Publish only the existing mobile-compatible models, never learner profiles."""
import argparse, hashlib, json, zipfile
from pathlib import Path

parser=argparse.ArgumentParser(); parser.add_argument('models'); args=parser.parse_args()
source=Path(args.models).resolve(); mobile=Path(__file__).resolve().parents[1]
target=mobile/'release'; target.mkdir(parents=True,exist_ok=True)
names=['supertonic/'+n for n in ('duration_predictor.int8.onnx','text_encoder.int8.onnx',
    'vector_estimator.int8.onnx','vocoder.int8.onnx','tts.json','unicode_indexer.bin','voice.bin')]
names += ['sensevoice/model.int8.onnx','sensevoice/tokens.txt']
def sha(path):
    with path.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
records=[dict(path=n,size=(source/n).stat().st_size,sha256=sha(source/n)) for n in names]
archive=target/'JapanischTrainer-Android-Sprachpaket-1.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for n in names:z.write(source/n,n)
manifest=dict(version=1,url='https://github.com/Priestkiller/JapanischTrainer/releases/download/android-models-v1/'+archive.name,
    bytes=archive.stat().st_size,sha256=sha(archive),unpacked_bytes=sum(x['size'] for x in records),files=records)
(mobile/'model-pack.json').write_text(json.dumps(manifest,indent=2),encoding='utf8')
print(json.dumps({k:v for k,v in manifest.items() if k!='files'},indent=2))

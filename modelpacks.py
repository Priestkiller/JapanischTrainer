"""Optional, pinned ASR weights. No remote manifests or executable plugins."""
import hashlib,json,os,shutil,urllib.request,urllib.parse,zipfile
from pathlib import Path
from speech_engine import app_root
from storage import data_dir

NAMES={'reazonspeech':'ReazonSpeech','qwen3':'Qwen3 ASR'}
def manifest(kind):
    if kind not in NAMES:raise ValueError('Unbekanntes Modell')
    return json.loads((app_root()/'data/modelpacks'/f'{kind}.json').read_text('utf8'))
def folder(kind):
    m=manifest(kind);return data_dir()/'test-models'/f"models-{m['version']}"
def digest(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def ready(kind):
    m=manifest(kind);root=folder(kind)
    try:return (root/'verified.sha256').read_text()==m['sha256'] and all((root/f['path']).stat().st_size==f['size'] for f in m['files'])
    except OSError:return False
class SecureRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        check_url(newurl);return super().redirect_request(req,fp,code,msg,headers,newurl)
def check_url(url):
    parsed=urllib.parse.urlsplit(url)
    if parsed.scheme!='https' or not parsed.hostname or parsed.username or parsed.password:raise ValueError('Unsichere Modelladresse')
def unpack(archive,stage,m,cancel=lambda:False):
    stage=Path(stage).resolve();stage.mkdir(parents=True,exist_ok=True)
    if Path(archive).stat().st_size!=m['bytes'] or digest(archive)!=m['sha256']:raise ValueError('Paket-Prüfsumme stimmt nicht')
    with zipfile.ZipFile(archive) as bundle:
        if sorted(bundle.namelist())!=sorted(f['path'] for f in m['files']):raise ValueError('Unerwarteter Paketinhalt')
        for f in m['files']:
            if cancel():raise RuntimeError('Abgebrochen')
            path=(stage/f['path']).resolve()
            if not path.is_relative_to(stage) or path==stage:raise ValueError('Ungültiger Paketpfad')
            entry=bundle.getinfo(f['path'])
            if entry.is_dir() or entry.file_size!=f['size'] or (entry.external_attr>>16)&0o170000==0o120000:raise ValueError('Ungültige Modelldatei')
            path.parent.mkdir(parents=True,exist_ok=True)
            with bundle.open(entry) as src,path.open('wb') as dst:
                count=0
                while chunk:=src.read(65536):
                    if cancel():raise RuntimeError('Abgebrochen')
                    count+=len(chunk)
                    if count>f['size']:raise ValueError('Modelldatei zu groß')
                    dst.write(chunk)
            if count!=f['size'] or digest(path)!=f['sha256']:raise ValueError('Dateiprüfung fehlgeschlagen')
    (stage/'verified.sha256').write_text(m['sha256'])
def install(kind,cancel=lambda:False):
    m=manifest(kind);target=folder(kind);parent=target.parent;parent.mkdir(parents=True,exist_ok=True)
    if ready(kind):return
    if shutil.disk_usage(parent).free<m['bytes']+m['unpacked_bytes']+100_000_000:raise RuntimeError('Zu wenig freier Speicher')
    stage=parent/f'.staging-{m["version"]}';archive=parent/f'.download-{m["version"]}.zip'
    # Both paths are fixed, private children of the selected app-data directory.
    check_url(m['url'])
    try:
        opener=urllib.request.build_opener(SecureRedirect())
        with opener.open(urllib.request.Request(m['url'],headers={'User-Agent':'JapanischTrainer'}),timeout=30) as response,archive.open('wb') as output:
            total=0
            while chunk:=response.read(65536):
                if cancel():raise RuntimeError('Download abgebrochen')
                total+=len(chunk)
                if total>m['bytes']:raise ValueError('Download größer als erwartet')
                output.write(chunk)
        unpack(archive,stage,m,cancel)
        if target.exists():shutil.rmtree(target)
        os.replace(stage,target)
    finally:
        archive.unlink(missing_ok=True)
        if stage.exists():shutil.rmtree(stage)
def install_local(kind,archive,cancel=lambda:False):
    m=manifest(kind);target=folder(kind);stage=target.parent/f'.staging-{m["version"]}'
    target.parent.mkdir(parents=True,exist_ok=True)
    if shutil.disk_usage(target.parent).free<m['unpacked_bytes']+100_000_000:raise RuntimeError('Zu wenig freier Speicher')
    try:
        unpack(archive,stage,m,cancel)
        if target.exists():shutil.rmtree(target)
        os.replace(stage,target)
    finally:
        if stage.exists():shutil.rmtree(stage)
def recognizer(kind):
    import sherpa_onnx as so
    if not ready(kind):raise RuntimeError('Testmodell zuerst vollständig laden')
    p=folder(kind)
    if kind=='qwen3':return so.OfflineRecognizer.from_qwen3_asr(conv_frontend=str(p/'conv_frontend.onnx'),encoder=str(p/'encoder.int8.onnx'),decoder=str(p/'decoder.int8.onnx'),tokenizer=str(p/'tokenizer'),num_threads=2,max_new_tokens=80)
    return so.OfflineRecognizer.from_transducer(encoder=str(p/'encoder-epoch-99-avg-1.int8.onnx'),decoder=str(p/'decoder-epoch-99-avg-1.int8.onnx'),joiner=str(p/'joiner-epoch-99-avg-1.int8.onnx'),tokens=str(p/'tokens.txt'),num_threads=2,decoding_method='greedy_search')

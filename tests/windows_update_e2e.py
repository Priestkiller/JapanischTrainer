"""Real TLS download, signed release, frozen updater, and two built app versions."""
import base64
import argparse
from datetime import datetime, timedelta, timezone
import functools
import http.server
import json
import os
from pathlib import Path
import shutil
import ssl
import subprocess
import sys
import threading
import urllib.request
from unittest.mock import patch
import uuid

ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from cryptography.x509.oid import NameOID
import updater

work=ROOT/'validation'/('update-e2e-'+uuid.uuid4().hex)
work.mkdir(parents=True)
installed=work/'installed';profile=work/'profile';profile.mkdir()
p=argparse.ArgumentParser()
p.add_argument('--installed-source',type=Path,default=ROOT/'dist/JapanischTrainer')
p.add_argument('--new-release',type=Path,default=ROOT/'build-release/11.0.1/dist/JapanischTrainer')
p.add_argument('--archive',type=Path,default=ROOT/'release/JapanischTrainer-11.0.1-Update-x64.zip')
args=p.parse_args()
shutil.copytree(args.installed_source,installed)
archive=args.archive;release=args.new_release
old_version=updater.current_version(installed);new_version=updater.current_version(release)
signing=ed25519.Ed25519PrivateKey.generate()
public=base64.b64encode(signing.public_key().public_bytes_raw()).decode()
tls_key=rsa.generate_private_key(public_exponent=65537,key_size=2048)
subject=x509.Name([x509.NameAttribute(NameOID.COMMON_NAME,'localhost')])
cert=(x509.CertificateBuilder().subject_name(subject).issuer_name(subject).public_key(tls_key.public_key())
    .serial_number(x509.random_serial_number()).not_valid_before(datetime.now(timezone.utc)-timedelta(minutes=1))
    .not_valid_after(datetime.now(timezone.utc)+timedelta(days=1))
    .add_extension(x509.SubjectAlternativeName([x509.DNSName('localhost')]),critical=False)
    .sign(tls_key,hashes.SHA256()))
(work/'tls-cert.pem').write_bytes(cert.public_bytes(serialization.Encoding.PEM))
(work/'tls-key.pem').write_bytes(tls_key.private_bytes(serialization.Encoding.PEM,serialization.PrivateFormat.PKCS8,serialization.NoEncryption()))
manifest=b''
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self,*args):pass
    def do_GET(self):
        if self.path=='/update.json':
            self.send_response(200);self.send_header('Content-Length',str(len(manifest)));self.end_headers();self.wfile.write(manifest)
        elif self.path=='/update.zip':
            self.send_response(200);self.send_header('Content-Length',str(archive.stat().st_size));self.end_headers()
            with archive.open('rb') as stream:shutil.copyfileobj(stream,self.wfile)
        else:self.send_error(404)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
context=ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER);context.load_cert_chain(work/'tls-cert.pem',work/'tls-key.pem')
server.socket=context.wrap_socket(server.socket,server_side=True)
base=f'https://localhost:{server.server_port}'
payload=json.dumps({'format':1,'app':updater.APP,'version':new_version,'minimum_version':old_version,
    'url':base+'/update.zip','sha256':updater.sha256(archive),'size':archive.stat().st_size,'notes':'Lokaler Integrationstest'}).encode()
manifest=json.dumps({'payload':base64.b64encode(payload).decode(),'signature':base64.b64encode(signing.sign(payload)).decode()}).encode()
(installed/'update-source.json').write_text(json.dumps({'manifest_url':base+'/update.json','public_key':public}),encoding='utf8')
state={'completed':['0:0'],'xp':275,'streak':3,'teacher_id':'yuki','tts_speed':.85,
       'last_lesson':{'key':'1:1','card':1},'course_revision':11,
       'lesson_sessions':{'1:1':{'index':1,'phase':'write','mode':'learn'}}}
updater.write_json(profile/'progress.json',state)
before={p.relative_to(installed).as_posix():(updater.sha256(p),p.stat().st_mtime_ns) for p in (installed/'models').rglob('*') if p.is_file()}
threading.Thread(target=server.serve_forever,daemon=True).start()
client_context=ssl.create_default_context(cafile=str(work/'tls-cert.pem'))
def local_transport(url):
    updater.secure_url(url)
    return urllib.request.urlopen(url,context=client_context,timeout=20)
report={'passed':False,'work':str(work),'from':old_version,'to':new_version,'tls':True,'frozen_worker':True}
try:
    with patch('updater.open_url',local_transport):
        raw,info=updater.check_update(installed,old_version)
        downloaded=updater.download_update(installed,raw,work/'download')
    worker=work/'download/JapanischTrainerUpdater.exe';shutil.copy2(release/worker.name,worker)
    result=subprocess.run([str(worker),'--target',str(installed),'--archive',str(downloaded),
        '--manifest',str(downloaded.parent/'update.json'),'--profile',str(profile),'--no-restart'],timeout=180,cwd=work)
    outcome=json.loads((downloaded.parent/'result.json').read_text(encoding='utf8'))
    if result.returncode or not outcome['success']:raise RuntimeError(outcome)
    assert updater.current_version(installed)==new_version
    capture=work/'after-update.png'
    env=os.environ.copy();env['JAPANISCHTRAINER_DATA_DIR']=str(profile)
    result=subprocess.run([str(installed/'JapanischTrainer.exe'),'--capture',str(capture),'--size','1280x860'],cwd=work,env=env,timeout=90)
    assert result.returncode==0 and capture.stat().st_size>5000
    after=json.loads((profile/'progress.json').read_text(encoding='utf8'))
    for name in state:assert after[name]==state[name],name
    for name,expected in before.items():
        path=installed/name;assert (updater.sha256(path),path.stat().st_mtime_ns)==expected,name
    report.update(passed=True,model_files_reused=len(before),profile_preserved=True,download_bytes=downloaded.stat().st_size,
                  native_start_test=True,explicit_restart_with_profile=True,backup=outcome['backup'])
finally:
    server.shutdown();server.server_close()
    updater.write_json(ROOT/'validation/update-e2e-report.json',report)
print(json.dumps(report,ensure_ascii=False,indent=2))

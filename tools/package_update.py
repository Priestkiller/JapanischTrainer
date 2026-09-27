"""Create a model-free update and Ed25519 envelope. Private keys never enter ZIPs."""
import argparse
import base64
import json
from pathlib import Path
import sys
import zipfile
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from updater import APP, ROOT_FILES, ROOT_DIRS, current_version, safe_relative, sha256, write_json


def create_package(source, output, private_key, url, notes, minimum='11.0.0'):
    source,output=Path(source),Path(output)
    output.mkdir(parents=True,exist_ok=True)
    current=current_version(source)
    files=[]
    for path in sorted(source.rglob('*')):
        if not path.is_file():continue
        relative=path.relative_to(source).as_posix()
        if relative not in ROOT_FILES and relative.split('/')[0] not in ROOT_DIRS:continue
        safe_relative(relative)
        files.append({'path':relative,'size':path.stat().st_size,'sha256':sha256(path)})
    models=[]
    for path in sorted((source/'models').rglob('*')):
        if path.is_file() and path.suffix in ('.onnx','.bin','.json') or (path.is_file() and path.name=='tokens.txt'):
            models.append({'path':path.relative_to(source).as_posix(),'size':path.stat().st_size,'sha256':sha256(path)})
    package={'app':APP,'version':current,'files':files,'models':models}
    archive=output/(APP+'-'+current+'-Update-x64.zip')
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as bundle:
        bundle.writestr('update-package.json',json.dumps(package,ensure_ascii=False))
        for record in files:bundle.write(source/record['path'],record['path'])
    payload=json.dumps({'format':1,'app':APP,'version':current,'minimum_version':minimum,'url':url,
        'size':archive.stat().st_size,'sha256':sha256(archive),'notes':notes},ensure_ascii=False,separators=(',',':')).encode('utf8')
    key=Ed25519PrivateKey.from_private_bytes(Path(private_key).read_bytes())
    write_json(output/'update.json',{'payload':base64.b64encode(payload).decode(),
        'signature':base64.b64encode(key.sign(payload)).decode()})
    return archive


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--output',required=True)
    p.add_argument('--key',required=True);p.add_argument('--url',required=True);p.add_argument('--notes',required=True)
    a=p.parse_args();print(create_package(a.source,a.output,a.key,a.url,Path(a.notes).read_text(encoding='utf8')))

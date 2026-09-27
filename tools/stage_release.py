"""Copy only reviewed program resources; never include profiles, keys or test audio."""
import argparse
import importlib.metadata as metadata
import json
from pathlib import Path
import shutil
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from updater import sha256

p=argparse.ArgumentParser();p.add_argument('destination');a=p.parse_args()
target=Path(a.destination).resolve();target.mkdir(parents=True,exist_ok=True)
if not target.is_relative_to(ROOT) or target==ROOT:raise RuntimeError('Ausgabe muss innerhalb des Projektordners liegen.')
for name in ('assets','data','licenses'):
    shutil.copytree(ROOT/name,target/name,dirs_exist_ok=True)
for name in ('release.json','update-source.json','README.txt','KURSUEBERSICHT_V11.txt','RELEASE_NOTES_V11.txt','MODEL_ATTRIBUTION.txt','THIRD_PARTY_NOTICES.txt','MODEL_LICENSES.txt'):
    shutil.copy2(ROOT/name,target/name)
config=json.loads((ROOT/'installer_tools/installer/config.json').read_text(encoding='utf-8-sig'))
for name,files in config['model_files'].items():
    dest=target/'models'/name;dest.mkdir(parents=True,exist_ok=True)
    for filename in files:shutil.copy2(ROOT/'models'/name/filename,dest/filename)
    for filename in ('LICENSE','README.md'):
        source=ROOT/'models'/name/filename
        if source.is_file():shutil.copy2(source,dest/filename)
records=[]
for dist in metadata.distributions():
    for item in dist.files or []:
        if any('license' in part.lower() or 'copying' in part.lower() or 'notice' in part.lower() for part in item.parts):
            source=Path(dist.locate_file(item))
            if source.is_file() and source.suffix not in ('.pyc','.py'):
                dest=target/'licenses'/'python-packages'/dist.metadata['Name']/str(item)
                dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
for path in sorted(target.rglob('*')):
    if path.is_file():records.append({'path':path.relative_to(target).as_posix(),'bytes':path.stat().st_size,'sha256':sha256(path)})
(target/'INSTALLATION_MANIFEST.json').write_text(json.dumps({'personal_data_included':False,'files':records},indent=2),encoding='utf8')
print('Release-Dateien:',len(records))

"""Explicit source allowlist. No build caches, credentials, learner profiles or recordings."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('destination');a=p.parse_args()
target=Path(a.destination).resolve();target.mkdir(parents=True,exist_ok=True)
files=list(ROOT.glob('*.py'))
names=['.gitignore','README.md','README.txt','LICENSE.txt','BUILD_ANLEITUNG.md','TESTBERICHT.md',
       'requirements.txt','requirements-lock.txt','release.json','update-source.json','version_info.txt',
       'Build-Release.ps1','download_models.ps1','MODEL_ATTRIBUTION.txt','MODEL_LICENSES.txt',
       'THIRD_PARTY_NOTICES.txt','KURSUEBERSICHT_V11.txt','RELEASE_NOTES_V11.txt','RELEASE_NOTES_11.0.1.md',
       'models/README.txt','docs/LEGACY_COURSE_V101.json','docs/DEVELOPMENT.txt','docs/SOURCES.txt',
       'installer_tools/SETUP_ERSTELLEN.bat']
files += [ROOT/name for name in names]
for name in ('assets','data','licenses','tests','vendor-sources','installer_tools/installer','installer_tools/tests'):
    files += [f for f in (ROOT/name).rglob('*') if f.is_file() and '__pycache__' not in f.parts]
for name in ('package_update.py','init_update_key.py','stage_release.py','prepare_public_source.py','write_release_report.py'):
    files.append(ROOT/'tools'/name)
records=[]
for source in sorted(set(files)):
    if source.is_symlink() or source.suffix in ('.key','.pem','.pfx','.p12','.wav','.log','.exe'):
        raise RuntimeError('Nicht freigegebene Datei: '+str(source))
    relative=source.relative_to(ROOT);destination=target/relative
    destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,destination)
    records.append({'path':relative.as_posix(),'sha256':hashlib.sha256(source.read_bytes()).hexdigest()})
(target/'SOURCE_MANIFEST.json').write_text(json.dumps(records,indent=2),encoding='utf8')
version=json.loads((ROOT/'release.json').read_text())['version']
archive=ROOT/'release'/('JapanischTrainer-'+version+'-Source.zip')
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as bundle:
    for record in records:bundle.write(target/record['path'],'JapanischTrainer/'+record['path'])
    bundle.write(target/'SOURCE_MANIFEST.json','JapanischTrainer/SOURCE_MANIFEST.json')
print(json.dumps({'files':len(records),'archive':str(archive),'bytes':archive.stat().st_size}))

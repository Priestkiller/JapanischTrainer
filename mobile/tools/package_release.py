"""Package the signed APK and Git-tracked source, never local profiles or keys."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[2]
MOBILE = ROOT / 'mobile'
parser = argparse.ArgumentParser()
parser.add_argument('--apk', type=Path, required=True)
parser.add_argument('--commit', required=True, help='Exact source commit for this release')
args = parser.parse_args()
version = json.loads((MOBILE / 'android-version.json').read_text(encoding='utf-8'))
out = MOBILE / 'release'
out.mkdir(exist_ok=True)
commit = subprocess.check_output(['git', 'rev-parse', '--verify', args.commit + '^{commit}'], cwd=ROOT, text=True).strip()
tracked = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', commit], cwd=ROOT, text=True).splitlines()
for name in tracked:
    parts = {p.lower() for p in Path(name).parts}
    if parts & {'.keys', '.release-keys', 'toolchain', 'generated', 'recordings', 'node_modules', '.venv'}:
        raise ValueError(f'Private/generated path in source tree: {name}')
    if name.lower().endswith(('.p12', '.jks', '.keystore')) or 'signing-password' in name.lower():
        raise ValueError(f'Signing material in source tree: {name}')

apk = out / f'JapanischTrainer-{version["course"]}-Android.apk'
if args.apk.resolve() != apk.resolve():
    shutil.copy2(args.apk, apk)
source = out / f'JapanischTrainer-{version["course"]}-Android-Quellcode.zip'
subprocess.run(['git', 'archive', '--format=zip', '--prefix=JapanischTrainer/', '-o', str(source), commit], cwd=ROOT, check=True)
for name in ('INSTALLIEREN_ANDROID.md', 'TESTBERICHT_ANDROID.md'):
    shutil.copy2(MOBILE / name, out / name)

def sha(file):
    with file.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

feed = {'package': version['package'], 'code': version['code'], 'name': version['name'],
        'url': version['releasePage'].replace('/tag/', '/download/') + '/' + apk.name,
        'bytes': apk.stat().st_size, 'sha256': sha(apk),
        'notes': 'Erste Android-Version: Handy-Layout, 150 Lektionen, acht Offline-Stimmen, Lernstand-Import und Update-Button.',
        'sourceCommit': commit}
(out / 'android-update.json').write_text(json.dumps(feed, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
files = [apk, source, out / 'android-update.json', out / 'INSTALLIEREN_ANDROID.md', out / 'TESTBERICHT_ANDROID.md']
(out / 'SHA256SUMS-Android.txt').write_text(''.join(f'{sha(file)}  {file.name}\n' for file in files), encoding='utf-8')
print(json.dumps({'sourceCommit': commit, 'apkBytes': apk.stat().st_size, 'apkSha256': sha(apk), 'files': [p.name for p in files]}, indent=2))

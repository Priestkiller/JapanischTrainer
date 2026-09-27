"""Reuse course/art without changing Windows assets; build a private-data-free APK tree."""
import argparse, hashlib, json, shutil, urllib.request
from pathlib import Path

MOBILE = Path(__file__).resolve().parents[1]
ROOT = MOBILE.parent
parser = argparse.ArgumentParser()
parser.add_argument('--download-library', action='store_true')
args = parser.parse_args()
out = MOBILE/'generated/assets'
out.mkdir(parents=True, exist_ok=True)
for name in ('data', 'assets', 'licenses'):
    shutil.copytree(ROOT/name, out/name, dirs_exist_ok=True)
shutil.copytree(MOBILE/'licenses',out/'licenses/android',dirs_exist_ok=True)
for license_name in ('sherpa-onnx-APACHE-2.0.txt', 'onnxruntime-MIT.txt', 'piper-phonemize-LICENSE.txt', 'espeak-ng-GPL-3.0.txt'):
    if not (MOBILE/'licenses'/license_name).is_file():
        raise FileNotFoundError(f'Android license missing: {license_name}')
shutil.copy2(MOBILE/'ANDROID_NOTICES.txt',out/'ANDROID_NOTICES.txt')
for name in ('LICENSE.txt', 'MODEL_LICENSES.txt', 'MODEL_ATTRIBUTION.txt', 'THIRD_PARTY_NOTICES.txt'):
    shutil.copy2(ROOT/name, out/name)
shutil.copy2(MOBILE/'model-pack.json', out/'model-pack.json')
shutil.copy2(MOBILE/'android-version.json', out/'android-version.json')
# Android launcher artwork is the existing icon; no image regeneration.
from PIL import Image
icon = MOBILE/'app/src/main/res/mipmap-xxxhdpi/ic_launcher.png'
icon.parent.mkdir(parents=True, exist_ok=True)
with Image.open(ROOT/'assets/icon.ico') as image:
    image.convert('RGBA').resize((192, 192)).save(icon)
aar = MOBILE/'vendor/sherpa-onnx-1.13.8.aar'
expected = '633c24321e06b1fe79feafa03ea16cbc0f8a286641e2da3559bac91bdb13bd96'
if not aar.exists() and args.download_library:
    aar.parent.mkdir(exist_ok=True)
    urllib.request.urlretrieve('https://github.com/k2-fsa/sherpa-onnx/releases/download/v1.13.8/'+aar.name, aar)
if not aar.exists() or hashlib.sha256(aar.read_bytes()).hexdigest() != expected:
    raise RuntimeError('The official sherpa-onnx Android library is missing or corrupt.')
print('Course, artwork, licenses and verified speech library are ready.')

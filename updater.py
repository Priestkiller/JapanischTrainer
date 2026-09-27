"""Signed updates. Network access occurs only after an explicit UI action."""
from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import subprocess
import time
import urllib.request
import uuid
import zipfile

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

APP = 'JapanischTrainer'
MAX_PACKAGE = 900 * 1024 * 1024
MAX_UNPACKED = 1800 * 1024 * 1024
ROOT_FILES = {APP+'.exe', 'JapanischTrainerUpdater.exe', 'release.json',
              'update-source.json', 'README.txt', 'KURSUEBERSICHT_V11.txt',
              'RELEASE_NOTES_V11.txt', 'MODEL_ATTRIBUTION.txt', 'THIRD_PARTY_NOTICES.txt',
              'MODEL_LICENSES.txt', 'INSTALLATION_HINWEISE.txt'}
ROOT_DIRS = {'_internal', 'assets', 'data', 'licenses'}


class UpdateError(RuntimeError):
    pass


class Cancelled(UpdateError):
    pass


def version(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{1,4}\.\d{1,4}\.\d{1,4}', value):
        raise UpdateError('Ungültige Versionsnummer.')
    return tuple(map(int, value.split('.')))


def sha256(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_json(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix+'.tmp')
    with temporary.open('w', encoding='utf8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.flush()
        os.fsync(stream.fileno())
    temporary.replace(path)


def load_source(root):
    path = Path(root)/'update-source.json'
    if not path.is_file():
        return {'manifest_url': '', 'public_key': ''}
    result = json.loads(path.read_text(encoding='utf8'))
    if not isinstance(result, dict):
        raise UpdateError('Update-Quelle ist ungültig.')
    return result


def secure_url(value):
    from urllib.parse import urlsplit
    parts = urlsplit(value)
    if parts.scheme != 'https' or not parts.hostname or parts.username or parts.password or parts.fragment:
        raise UpdateError('Updates benötigen eine HTTPS-Adresse ohne Zugangsdaten.')
    return value


class HTTPSRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        secure_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def open_url(url):
    secure_url(url)
    req = urllib.request.Request(url, headers={'User-Agent': 'JapanischTrainer-Update/1'})
    return urllib.request.build_opener(HTTPSRedirect()).open(req, timeout=25)


def verify_envelope(raw, public_key):
    try:
        envelope = json.loads(raw)
        payload = base64.b64decode(envelope['payload'], validate=True)
        signature = base64.b64decode(envelope['signature'], validate=True)
        key = Ed25519PublicKey.from_public_bytes(base64.b64decode(public_key, validate=True))
        key.verify(signature, payload)
        info = json.loads(payload)
        if info['app'] != APP or info['format'] != 1:
            raise ValueError('app/format')
        version(info['version'])
        version(info['minimum_version'])
        secure_url(info['url'])
        if not re.fullmatch('[a-f0-9]{64}', info['sha256']):
            raise ValueError('hash')
        if type(info['size']) is not int or not 0 < info['size'] <= MAX_PACKAGE:
            raise ValueError('size')
        if not isinstance(info.get('notes', ''), str) or len(info.get('notes', '')) > 12000:
            raise ValueError('notes')
        return info
    except Exception as exc:
        raise UpdateError('Die Update-Signatur oder die Versionsinformationen sind ungültig.') from exc


def check_update(root, current):
    source = load_source(root)
    if not source.get('manifest_url') or not source.get('public_key'):
        raise UpdateError('Update-Quelle noch nicht eingerichtet.')
    try:
        with open_url(source['manifest_url']) as response:
            raw = response.read(65537)
        if len(raw) > 65536:
            raise UpdateError('Die Update-Informationen sind zu groß.')
        info = verify_envelope(raw, source['public_key'])
    except UpdateError:
        raise
    except Exception as exc:
        raise UpdateError('Updates derzeit nicht erreichbar. Bitte Internetverbindung prüfen und später erneut versuchen.') from exc
    if version(info['version']) <= version(current):
        return None
    if version(current) < version(info['minimum_version']):
        raise UpdateError('Diese Version benötigt einmalig das vollständige neue Setup aus dem Download-Bereich.')
    return raw, info


def download_update(root, raw, destination, progress=lambda a,b: None, cancelled=lambda: False):
    info = verify_envelope(raw, load_source(root)['public_key'])
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    partial = destination/'update.zip.part'
    final = destination/'update.zip'
    try:
        count = 0
        digest = hashlib.sha256()
        with open_url(info['url']) as response, partial.open('wb') as output:
            while True:
                if cancelled():
                    raise Cancelled('Download abgebrochen. Die vorhandene Version bleibt erhalten.')
                chunk = response.read(256*1024)
                if not chunk:
                    break
                count += len(chunk)
                if count > info['size']:
                    raise UpdateError('Das Update hat eine unerwartete Größe.')
                output.write(chunk)
                digest.update(chunk)
                progress(count, info['size'])
        if count != info['size'] or digest.hexdigest() != info['sha256']:
            raise UpdateError('Das Update ist unvollständig oder beschädigt. Bitte erneut laden.')
        partial.replace(final)
        (destination/'update.json').write_bytes(raw)
        return final
    except Exception:
        partial.unlink(missing_ok=True)
        raise


def safe_relative(name, model=False):
    if not isinstance(name, str) or len(name) > 220 or '\\' in name:
        raise UpdateError('Ungültiger Dateipfad im Update.')
    path = PurePosixPath(name)
    if path.is_absolute() or name != path.as_posix():
        raise UpdateError('Ungültiger Dateipfad im Update.')
    for part in path.parts:
        if part in ('.', '..') or part.endswith((' ', '.')) or re.search(r'[<>:"|?*\x00-\x1f]', part):
            raise UpdateError('Ungültiger Windows-Dateiname im Update.')
        if re.fullmatch(r'(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\..*)?', part, re.I):
            raise UpdateError('Reservierter Windows-Dateiname im Update.')
    if model:
        allowed = len(path.parts) >= 3 and path.parts[0] == 'models'
    else:
        allowed = name in ROOT_FILES or (len(path.parts) >= 2 and path.parts[0] in ROOT_DIRS)
    if not allowed:
        raise UpdateError('Das Update enthält Dateien außerhalb der Programmdateien.')
    return path


def assert_plain_tree(root):
    for path in [Path(root), *Path(root).rglob('*')]:
        if path.is_symlink() or (hasattr(path, 'is_junction') and path.is_junction()):
            raise UpdateError('Verknüpfungen im Update-Pfad werden nicht unterstützt.')


def current_version(root):
    root = Path(root)
    path = root/'release.json'
    if path.exists():
        return json.loads(path.read_text(encoding='utf8'))['version']
    return json.loads((root/'data/course.json').read_text(encoding='utf8'))['content_version']


def extract_verified(root, archive, envelope, stage):
    root, stage, archive = Path(root), Path(stage), Path(archive)
    info = verify_envelope(Path(envelope).read_bytes(), load_source(root)['public_key'])
    old = current_version(root)
    if version(info['version']) <= version(old) or version(old) < version(info['minimum_version']):
        raise UpdateError('Das Update passt nicht zur installierten Version.')
    if archive.stat().st_size != info['size'] or sha256(archive) != info['sha256']:
        raise UpdateError('Die Update-Datei stimmt nicht mit der Signatur überein.')
    with zipfile.ZipFile(archive) as bundle:
        entries = bundle.infolist()
        names = [entry.filename for entry in entries]
        if len(names) > 12000 or len({n.casefold() for n in names}) != len(names):
            raise UpdateError('Doppelte oder zu viele Dateien im Update.')
        if sum(entry.file_size for entry in entries) > MAX_UNPACKED:
            raise UpdateError('Das entpackte Update ist zu groß.')
        metadata = bundle.getinfo('update-package.json')
        if metadata.file_size > 4*1024*1024:
            raise UpdateError('Ungültiges Paketverzeichnis.')
        package = json.loads(bundle.read(metadata))
        if package['app'] != APP or package['version'] != info['version']:
            raise UpdateError('Paketversion stimmt nicht überein.')
        expected = {record['path']: record for record in package['files']}
        if len(expected) != len(package['files']) or set(names) != set(expected) | {'update-package.json'}:
            raise UpdateError('Das Paketverzeichnis ist unvollständig.')
        for name in expected:
            safe_relative(name)
        for record in package['models']:
            safe_relative(record['path'], model=True)
            path = root/record['path']
            if not path.is_file() or path.stat().st_size != record['size'] or sha256(path) != record['sha256']:
                raise UpdateError('Die vorhandenen Sprachmodelle passen nicht. Bitte das vollständige Setup verwenden.')
        if not {APP+'.exe', 'JapanischTrainerUpdater.exe', 'release.json', 'update-source.json', 'data/course.json'} <= set(expected):
            raise UpdateError('Im Update fehlen notwendige Programmdateien.')
        for entry in entries:
            if entry.filename == 'update-package.json':
                continue
            if entry.is_dir() or stat.S_ISLNK(entry.external_attr >> 16):
                raise UpdateError('Verknüpfungen sind in Updates nicht erlaubt.')
            record = expected[entry.filename]
            if entry.file_size != record['size']:
                raise UpdateError('Dateigröße stimmt nicht.')
            target = stage/entry.filename
            target.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(entry) as src, target.open('wb') as dst:
                shutil.copyfileobj(src, dst, 256*1024)
            if sha256(target) != record['sha256']:
                raise UpdateError('Dateiprüfsumme stimmt nicht.')
        if current_version(stage) != info['version']:
            raise UpdateError('Die Programmversion im Update stimmt nicht.')
    return info


def restore_transaction(root, work, journal):
    root, work = Path(root), Path(work)
    for name in reversed(journal['planned']):
        if name not in ROOT_DIRS | ROOT_FILES:
            raise UpdateError('Ungültiges Wiederherstellungsprotokoll.')
        old, target = work/'old'/name, root/name
        if old.exists():
            if target.exists():
                failed = work/'failed'/name
                failed.parent.mkdir(parents=True, exist_ok=True)
                target.replace(failed)
            old.replace(target)
        elif not journal['existed'][name] and target.exists():
            failed = work/'failed'/name
            failed.parent.mkdir(parents=True, exist_ok=True)
            target.replace(failed)
    journal['status'] = 'rolled_back'
    write_json(work/'journal.json', journal)


def apply_update(root, archive, envelope, health_check, profile=None):
    """Replace only allowlisted program components; retain models and personal data."""
    root = Path(root).resolve(strict=True)
    assert_plain_tree(root)
    # An exclusive Windows file lock also blocks a second updater process.
    import msvcrt
    lock = (root/'.update.lock').open('a+b')
    try:
        lock.seek(0); lock.write(b'0'); lock.flush(); lock.seek(0)
        msvcrt.locking(lock.fileno(), msvcrt.LK_NBLCK, 1)
        for pending in root.glob('.update-*/journal.json'):
            previous = json.loads(pending.read_text(encoding='utf8'))
            if previous['status'] == 'applying':
                restore_transaction(root, pending.parent, previous)
        if not (root/(APP+'.exe')).is_file():
            raise UpdateError('Kein installierter JapanischTrainer im Zielordner.')
        work = root/('.update-'+uuid.uuid4().hex)
        stage = work/'new'
        stage.mkdir(parents=True)
        info = extract_verified(root, archive, envelope, stage)
        if shutil.disk_usage(root).free < sum(p.stat().st_size for p in stage.rglob('*') if p.is_file()) + 128*1024*1024:
            raise UpdateError('Zu wenig freier Speicher für das Update.')
        names = sorted(p.name for p in stage.iterdir())
        journal = {'status':'applying', 'version':info['version'], 'planned':[],
                   'existed':{n:(root/n).exists() for n in names}}
        (work/'old').mkdir()
        if profile and (Path(profile)/'progress.json').exists():
            backup = Path(profile)/'Backups'
            backup.mkdir(exist_ok=True)
            shutil.copy2(Path(profile)/'progress.json', backup/('progress.before-update-'+uuid.uuid4().hex+'.json'))
        try:
            for name in names:
                journal['planned'].append(name)
                write_json(work/'journal.json', journal)
                if (root/name).exists():
                    (root/name).replace(work/'old'/name)
                (stage/name).replace(root/name)
            health_check(root, work)
            journal['status'] = 'complete'
            write_json(work/'journal.json', journal)
            return work
        except Exception as exc:
            restore_transaction(root, work, journal)
            raise UpdateError('Update fehlgeschlagen. Die bisherige Programmversion wurde wiederhergestellt: '+str(exc)) from exc
    finally:
        lock.close()


def run_health_check(root, work):
    profile = work/'probe-profile'
    profile.mkdir()
    capture = work/'starttest.png'
    env = os.environ.copy()
    env['JAPANISCHTRAINER_DATA_DIR'] = str(profile)
    completed = subprocess.run([str(root/(APP+'.exe')), '--capture', str(capture), '--size', '1280x860'],
                               cwd=work, env=env, timeout=90)
    if completed.returncode or not capture.is_file() or capture.stat().st_size < 5000:
        raise UpdateError('Die neue Version hat den Starttest nicht bestanden.')


def wait_for_parent(pid):
    if not pid:
        return
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.WaitForSingleObject.argtypes = [wintypes.HANDLE, wintypes.DWORD]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.OpenProcess(0x00100000, False, pid)
    if not handle:
        if ctypes.get_last_error() == 87:  # already exited
            return
        raise UpdateError('Die laufende Anwendung konnte nicht geprüft werden.')
    try:
        if kernel.WaitForSingleObject(handle, 60000) != 0:
            raise UpdateError('JapanischTrainer ist noch geöffnet. Bitte schließen und erneut versuchen.')
    finally:
        kernel.CloseHandle(handle)


def launch_worker(root, cache, profile):
    worker = Path(cache)/'JapanischTrainerUpdater.exe'
    shutil.copy2(Path(root)/worker.name, worker)
    return subprocess.Popen([str(worker), '--target', str(root), '--archive', str(Path(cache)/'update.zip'),
                             '--manifest', str(Path(cache)/'update.json'), '--parent', str(os.getpid()),
                             '--profile', str(profile)], cwd=cache)

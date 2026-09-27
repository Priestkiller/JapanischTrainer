import base64
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import updater
from tools.package_update import create_package


class UpdateTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.base=Path(self.temp.name)
        self.old=self.base/'installed';self.new=self.base/'next'
        self.key=Ed25519PrivateKey.generate()
        self.keyfile=self.base/'private.key';self.keyfile.write_bytes(self.key.private_bytes_raw())
        self.public=base64.b64encode(self.key.public_key().public_bytes_raw()).decode()
        for folder,v in [(self.old,'11.0.0'),(self.new,'11.0.1')]:
            folder.mkdir()
            for name in ('_internal','assets','data','models'):(folder/name).mkdir()
            (folder/'JapanischTrainer.exe').write_bytes(v.encode())
            (folder/'JapanischTrainerUpdater.exe').write_bytes(b'worker')
            (folder/'assets/image.png').write_bytes(v.encode())
            (folder/'_internal/runtime.dll').write_bytes(v.encode())
            (folder/'data/course.json').write_text(json.dumps({'content_version':v}))
            (folder/'release.json').write_text(json.dumps({'version':v}))
            (folder/'update-source.json').write_text(json.dumps({'public_key':self.public,'manifest_url':'https://example.test/update.json'}))
        self.profile=self.base/'profile';self.profile.mkdir()
        (self.profile/'progress.json').write_text('{"xp":123,"teacher_id":"yuki"}')
        self.archive=create_package(self.new,self.base/'download',self.keyfile,'https://example.test/update.zip','Test')
        self.envelope=self.archive.parent/'update.json'

    def tearDown(self):self.temp.cleanup()

    def test_signed_manifest_roundtrip(self):
        self.assertEqual(updater.verify_envelope(self.envelope.read_bytes(),self.public)['version'],'11.0.1')

    def test_unknown_key_rejected(self):
        key=base64.b64encode(Ed25519PrivateKey.generate().public_key().public_bytes_raw()).decode()
        with self.assertRaises(updater.UpdateError):updater.verify_envelope(self.envelope.read_bytes(),key)

    def test_tampered_manifest_rejected(self):
        env=json.loads(self.envelope.read_bytes());env['payload']=base64.b64encode(b'{}').decode()
        with self.assertRaises(updater.UpdateError):updater.verify_envelope(json.dumps(env),self.public)

    def test_apply_preserves_profile_and_models(self):
        (self.old/'models/keep.bin').write_bytes(b'existing-model')
        backup=updater.apply_update(self.old,self.archive,self.envelope,lambda a,b:None,self.profile)
        self.assertEqual(updater.current_version(self.old),'11.0.1')
        self.assertEqual((self.old/'models/keep.bin').read_bytes(),b'existing-model')
        self.assertEqual(json.loads((self.profile/'progress.json').read_text())['xp'],123)
        self.assertEqual((backup/'old/JapanischTrainer.exe').read_bytes(),b'11.0.0')
        self.assertTrue(list((self.profile/'Backups').glob('*.json')))

    def test_failed_start_restores_previous_files(self):
        def fail(a,b):raise RuntimeError('simulierter Startfehler')
        with self.assertRaisesRegex(updater.UpdateError,'wiederhergestellt'):
            updater.apply_update(self.old,self.archive,self.envelope,fail,self.profile)
        self.assertEqual(updater.current_version(self.old),'11.0.0')
        self.assertEqual((self.old/'_internal/runtime.dll').read_bytes(),b'11.0.0')

    def test_same_version_does_not_replace(self):
        updater.apply_update(self.old,self.archive,self.envelope,lambda a,b:None)
        with self.assertRaises(updater.UpdateError):updater.apply_update(self.old,self.archive,self.envelope,lambda a,b:None)

    def test_interrupted_executable_replacement_is_recovered_before_retry(self):
        pending=self.old/'.update-interrupted';(pending/'old').mkdir(parents=True)
        (self.old/'JapanischTrainer.exe').replace(pending/'old/JapanischTrainer.exe')
        updater.write_json(pending/'journal.json',{'status':'applying','version':'11.0.1',
            'planned':['JapanischTrainer.exe'],'existed':{'JapanischTrainer.exe':True}})
        updater.apply_update(self.old,self.archive,self.envelope,lambda a,b:None)
        self.assertEqual(updater.current_version(self.old),'11.0.1')
        self.assertEqual(json.loads((pending/'journal.json').read_text())['status'],'rolled_back')

    def test_damaged_archive_leaves_existing_app(self):
        with self.archive.open('ab') as stream:stream.write(b'broken')
        with self.assertRaises(updater.UpdateError):updater.apply_update(self.old,self.archive,self.envelope,lambda a,b:None)
        self.assertEqual(updater.current_version(self.old),'11.0.0')

    def test_windows_traversal_and_protected_paths(self):
        for path in ('../bad.exe','/bad.exe','C:/bad.exe','data/../bad.exe','data/CON','assets/a:stream','data/x.','models/x.onnx','progress.json','data\\x','data//x'):
            with self.subTest(path=path),self.assertRaises(updater.UpdateError):updater.safe_relative(path)

    def test_https_only_including_redirect(self):
        for url in ('http://example.test/a','https://user:secret@example.test/a','file:///a'):
            with self.assertRaises(updater.UpdateError):updater.secure_url(url)
        with self.assertRaises(updater.UpdateError):updater.HTTPSRedirect().redirect_request(None,None,302,'',{},'http://example.test/a')

    def test_offline_is_not_reported_as_current(self):
        with patch('updater.open_url',side_effect=OSError('offline')):
            with self.assertRaisesRegex(updater.UpdateError,'nicht erreichbar'):updater.check_update(self.old,'11.0.0')

    def test_unconfigured_source_is_explicit(self):
        (self.old/'update-source.json').unlink()
        with self.assertRaisesRegex(updater.UpdateError,'noch nicht eingerichtet'):updater.check_update(self.old,'11.0.0')

    def test_cancel_removes_partial_download(self):
        with patch('updater.open_url',return_value=io.BytesIO(self.archive.read_bytes())):
            with self.assertRaises(updater.Cancelled):
                updater.download_update(self.old,self.envelope.read_bytes(),self.base/'cancel',cancelled=lambda:True)
        self.assertFalse((self.base/'cancel/update.zip.part').exists())
        self.assertFalse((self.base/'cancel/update.zip').exists())

    def test_truncated_download_not_accepted(self):
        with patch('updater.open_url',return_value=io.BytesIO(b'partial')):
            with self.assertRaises(updater.UpdateError):updater.download_update(self.old,self.envelope.read_bytes(),self.base/'truncated')
        self.assertFalse((self.base/'truncated/update.zip').exists())

    def test_completed_download_checks_digest(self):
        with patch('updater.open_url',return_value=io.BytesIO(self.archive.read_bytes())):
            path=updater.download_update(self.old,self.envelope.read_bytes(),self.base/'complete')
        self.assertEqual(updater.sha256(path),updater.sha256(self.archive))

    def test_signature_verified_before_network(self):
        with patch('updater.open_url') as network:
            with self.assertRaises(updater.UpdateError):updater.download_update(self.old,b'{}',self.base/'invalid')
            network.assert_not_called()

    def test_package_excludes_model_weights_and_private_files(self):
        with zipfile.ZipFile(self.archive) as archive:
            self.assertFalse(any(n.startswith('models/') or 'private.key' in n for n in archive.namelist()))


if __name__=='__main__':unittest.main(verbosity=2)

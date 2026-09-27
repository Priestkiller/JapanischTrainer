"""Signed release selection: stable and opt-in test channels never cross."""
import base64
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
import updater


class UpdateChannelTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.key = Ed25519PrivateKey.generate()
        self.source = {'manifest_url': 'https://example.test/stable.json',
                       'test_releases_url': 'https://api.github.com/repos/Priestkiller/JapanischTrainer/releases?per_page=30',
                       'public_key': base64.b64encode(self.key.public_key().public_bytes_raw()).decode()}
        (self.root/'update-source.json').write_text(json.dumps(self.source), encoding='utf8')
        self.releases = []
        self.files = {}

    def tearDown(self):
        self.temp.cleanup()

    def envelope(self, number, url):
        payload = json.dumps({'app': updater.APP, 'format': 1, 'version': number,
            'minimum_version': '11.0.0', 'url': url, 'size': 100, 'sha256': 'a'*64}).encode()
        return json.dumps({'payload': base64.b64encode(payload).decode(),
                          'signature': base64.b64encode(self.key.sign(payload)).decode()}).encode()

    def add(self, number, prefix='windows-test-v', draft=False, prerelease=True):
        tag = prefix+number
        url = 'https://github.com/Priestkiller/JapanischTrainer/releases/download/'+tag+'/update.json'
        self.files[url] = self.envelope(number, url.replace('update.json', 'update.zip'))
        self.releases.append({'tag_name': tag, 'draft': draft, 'prerelease': prerelease,
                              'assets': [{'name': 'update.json', 'browser_download_url': url}]})
        return url

    def fetch(self, url):
        if url == self.source['test_releases_url']:
            return io.BytesIO(json.dumps(self.releases).encode())
        return io.BytesIO(self.files[url])

    def test_regular_check_does_not_read_test_list(self):
        raw = self.envelope('11.0.4', 'https://example.test/stable.zip')
        with patch('updater.open_url', return_value=io.BytesIO(raw)) as request:
            self.assertEqual(updater.check_update(self.root, '11.0.2')[1]['version'], '11.0.4')
        request.assert_called_once_with(self.source['manifest_url'])

    def test_newest_signed_test_selected_not_draft_regular_or_android(self):
        self.add('11.0.5'); self.add('11.0.7'); self.add('11.0.6')
        self.add('11.0.9', draft=True); self.add('12.0.0', prefix='v')
        self.add('13.0.0', prefix='android-test-v'); self.add('11.0.8', prerelease=False)
        with patch('updater.open_url', side_effect=self.fetch):
            self.assertEqual(updater.check_update(self.root, '11.0.4', 'test')[1]['version'], '11.0.7')

    def test_empty_or_older_test_channel_never_downgrades(self):
        with patch('updater.open_url', side_effect=self.fetch):
            self.assertIsNone(updater.check_update(self.root, '11.0.4', 'test'))
            self.add('11.0.3')
            self.assertIsNone(updater.check_update(self.root, '11.0.4', 'test'))
            self.add('11.0.4')
            self.assertIsNone(updater.check_update(self.root, '11.0.4', 'test'))

    def test_bad_test_signature_is_not_offered(self):
        url = self.add('11.0.5'); self.files[url] = b'{}'
        with patch('updater.open_url', side_effect=self.fetch):
            with self.assertRaisesRegex(updater.UpdateError, 'Signatur'):
                updater.check_update(self.root, '11.0.4', 'test')

    def test_test_package_cannot_point_to_other_release(self):
        url = self.add('11.0.5'); self.files[url] = self.envelope('11.0.5', 'https://example.test/other.zip')
        with patch('updater.open_url', side_effect=self.fetch):
            with self.assertRaisesRegex(updater.UpdateError, 'gehört nicht'):
                updater.check_update(self.root, '11.0.4', 'test')

    def test_offline_test_channel_is_not_reported_as_current(self):
        with patch('updater.open_url', side_effect=OSError('offline')):
            with self.assertRaisesRegex(updater.UpdateError, 'nicht erreichbar'):
                updater.check_update(self.root, '11.0.4', 'test')

    def test_oversized_listing_and_unknown_channel_rejected(self):
        with patch('updater.open_url', return_value=io.BytesIO(b' '*2_000_001)):
            with self.assertRaisesRegex(updater.UpdateError, 'zu groß'):
                updater.check_update(self.root, '11.0.4', 'test')
        with self.assertRaisesRegex(updater.UpdateError, 'Unbekannter'):
            updater.check_update(self.root, '11.0.4', 'other')


if __name__ == '__main__':
    unittest.main()

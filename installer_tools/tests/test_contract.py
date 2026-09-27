"""Static package checks only. These do NOT execute PowerShell, ISCC or Windows.
Run from this package with: python -m unittest discover -s tests -v
"""
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
CONFIG = json.loads((ROOT / 'installer/config.json').read_text(encoding='utf-8-sig'))
PS = (ROOT / 'installer/Build-Installer.ps1').read_text(encoding='utf-8-sig')
ISS = (ROOT / 'installer/JapanischTrainer.iss').read_text(encoding='utf-8-sig')
BAT = (ROOT / 'SETUP_ERSTELLEN.bat').read_bytes()

class PackageContract(unittest.TestCase):
    def test_expected_directories(self):
        self.assertEqual(CONFIG['allowed_directories'], ['_internal','assets','data','models','licenses'])
    def test_models_declared(self):
        self.assertEqual(set(CONFIG['model_files']), {'supertonic','parakeet-ja','sensevoice'})
        self.assertEqual(sum(map(len,CONFIG['model_files'].values())), 11)
    def test_all_teachers(self):
        self.assertEqual(len(CONFIG['teachers']), 8)
        self.assertEqual(len(set(CONFIG['teachers'])), 8)
    def test_runtime_and_course_not_exe_only(self):
        for p in ['JapanischTrainer.exe','data/course.json','data/catalog.json','data/deep_lessons.json']:
            self.assertIn(p,CONFIG['required_files'])
        self.assertIn("'python3*.dll'",PS)
        self.assertIn("'_tkinter.pyd'",PS)
    def test_pinned_official_download(self):
        self.assertEqual(CONFIG['compiler']['url'],'https://github.com/jrsoftware/issrc/releases/download/is-6_7_3/innosetup-6.7.3.exe')
        self.assertEqual(CONFIG['compiler']['sha256'],'9c73c3bae7ed48d44112a0f48e66742c00090bdb5bef71d9d3c056c66e97b732')
        self.assertIn('Get-AuthenticodeSignature', PS)
        self.assertIn('$hash -ne $Config.compiler.sha256',PS)
    def test_default_confirmation_no(self):
        self.assertIn('MessageBoxDefaultButton]::Button2',PS)
    def test_no_pip_pyinstaller_winget_execution(self):
        executable_lines='\n'.join(l for l in PS.splitlines() if not l.strip().startswith('#'))
        self.assertNotRegex(executable_lines,r'(?im)^\s*(?:&\s+)?(?:pip|winget|pyinstaller|python)\b')
    def test_user_state_never_a_payload_root(self):
        self.assertNotIn('progress.json',CONFIG['allowed_root_files'])
        self.assertIn("$name -like 'progress*.json'",PS)
        self.assertIn("'recordings'",PS)
        self.assertIn('personal_data_included=$false',PS)
    def test_launch_test_isolated_profile(self):
        self.assertIn('$env:JAPANISCHTRAINER_DATA_DIR = $profile',PS)
        self.assertIn("SetEnvironmentVariable('JAPANISCHTRAINER_DATA_DIR', $old, 'Process')",PS)
        self.assertIn("@('--page','home','--size','1280x860','--capture',$capture)",PS)
    def test_no_skip_launch_parameter(self):
        self.assertNotIn('[switch]$SkipLaunchTest',PS)
    def test_non_elevated_install(self):
        self.assertIn('PrivilegesRequired=lowest',ISS)
        self.assertIn('DefaultDirName={localappdata}\\Programs\\JapanischTrainer',ISS)
    def test_os_arch_explicit(self):
        self.assertIn('ArchitecturesAllowed=x64os',ISS)
        self.assertIn('MinVersion=10.0.17763',ISS)
    def test_installer_has_no_network_steps(self):
        self.assertNotRegex(ISS,r'https?://')
        run=ISS.split('[Run]',1)[1].split('[Code]',1)[0]
        self.assertNotRegex(run.lower(),r'powershell|python|winget|curl|pip')
        self.assertIn('{app}\\JapanischTrainer.exe',run)
    def test_progress_preservation(self):
        self.assertIn("FileCopy(ProgressFile, BackupFile, True)",ISS)
        cleanup=ISS.split('[UninstallDelete]',1)[1].split('[Code]',1)[0]
        self.assertNotIn('{userappdata}',cleanup)
        self.assertNotIn('progress',cleanup.lower())
        self.assertNotRegex(ISS,r'(?im)^\[InstallDelete\]')
        self.assertIn('ssPostInstall',ISS)
    def test_old_app_migration_gated_by_location(self):
        self.assertIn("SamePath(LegacyDir, ExpandConstant('{app}'))",ISS)
        self.assertIn('(CurStep = ssPostInstall) and LegacySameLocation',ISS)
    def test_downgrade_protection(self):
        self.assertIn('(CurrentMS > NewVersionMS)',ISS)
        self.assertIn('(CurrentLS > NewVersionLS)',ISS)
    def test_powershell5_encoding_and_batch_no_control_chars(self):
        self.assertIn('#requires -Version 5.1',PS)
        self.assertNotIn(b'\x0b',BAT)
        self.assertNotIn(b'\x00',BAT)
        self.assertIn(b'\\WindowsPowerShell\\v1.0\\powershell.exe',BAT)
        for p in ROOT.rglob('*'):
            if p.is_file(): self.assertNotIn(p.suffix.lower(),{'.ttf','.otf','.ttc','.woff','.woff2'})
    def test_no_fabricated_binary(self):
        self.assertFalse(any(ROOT.rglob('*.exe')))
    def test_compile_and_copy_hash_gated(self):
        self.assertIn('if ($LASTEXITCODE -ne 0)',PS)
        self.assertIn('if ($targetHash -ne $sourceHash)',PS)
        self.assertIn("Get-FileHash -LiteralPath $final -Algorithm SHA256",PS)
    def test_reports_limits(self):
        self.assertIn("installed_end_to_end_test='not performed by this packaging step'",PS)
        self.assertIn('code_signed=$false',PS)
        self.assertIn("microphone_and_model_inference='not tested by this packaging step'",PS)

if __name__=='__main__': unittest.main()

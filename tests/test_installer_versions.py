import os,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
@unittest.skipUnless(os.name=='nt','Actual PowerShell installer validation needs Windows')
class InstallerVersionTests(unittest.TestCase):
 def test_explicit_mapping_rejects_mixed_exe_metadata_and_course(self):
  text=(ROOT/'installer_tools/installer/Build-Installer.ps1').read_text('utf-8-sig')
  function=text[text.index('function Assert-VersionMapping'):text.index('function Validate-App')]
  cases="""
$ErrorActionPreference='Stop'
Assert-VersionMapping '11.0.10.0' '11.0.7' ([pscustomobject]@{app='JapanischTrainer';version='11.0.10';course_version='11.0.7'})
Assert-VersionMapping '11.0.4.0' '11.0.4' $null
$failed=0
foreach($case in @(
 @('11.0.10','11.0.6',@{app='JapanischTrainer';version='11.0.10';course_version='11.0.7'}),
 @('11.0.10','11.0.7',@{app='JapanischTrainer';version='11.0.9';course_version='11.0.7'}),
 @('11.0.10','11.0.7',@{app='WrongApp';version='11.0.10';course_version='11.0.7'}),
 @('11.0.10','11.0.7',@{app='JapanischTrainer';version='11.0.10'}),
 @('11.0.10','11.0.11',@{app='JapanischTrainer';version='11.0.10';course_version='11.0.11'})
)) {try { Assert-VersionMapping $case[0] $case[1] ([pscustomobject]$case[2]) } catch {$failed++}}
if($failed -ne 5){throw "Only $failed mixed packages were rejected"}
Write-Output 'PASS 2 valid, 5 invalid mappings'
"""
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'check.ps1';p.write_text(function+cases,'utf8');result=subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(p)],capture_output=True,text=True)
   self.assertEqual(result.returncode,0,result.stdout+result.stderr);self.assertIn('PASS 2 valid, 5 invalid mappings',result.stdout)

#requires -Version 5.1
[CmdletBinding()]
param([string]$Python = '', [string]$IsccPath = 'C:\Program Files\Inno Setup 7\ISCC.exe')
$ErrorActionPreference = 'Stop'
$releaseRoot = $PSScriptRoot
Set-Location -LiteralPath $releaseRoot
if (-not $Python) { $Python = Join-Path $releaseRoot '.venv\Scripts\python.exe' }
function Run-Checked([string]$Exe, [string[]]$Values) {
    & $Exe @Values
    if ($LASTEXITCODE -ne 0) { throw "Build fehlgeschlagen: $Exe ($LASTEXITCODE)" }
}
$version = (Get-Content -LiteralPath 'release.json' -Raw | ConvertFrom-Json).version
$work = Join-Path $releaseRoot ('build-release\' + $version)
$dist = Join-Path $work 'dist'
$app = Join-Path $dist 'JapanischTrainer'
$release = Join-Path $releaseRoot 'release'
New-Item -ItemType Directory -Path $work,$release -Force | Out-Null
Run-Checked $Python @('-c','import sys;assert sys.platform=="win32" and sys.maxsize>2**32')
Run-Checked $Python @('-m','PyInstaller','--noconfirm','--windowed','--onedir','--noupx','--name','JapanischTrainer',
    '--distpath',$dist,'--workpath',(Join-Path $work 'pyinstaller'),'--specpath',$work,
    '--icon',(Join-Path $releaseRoot 'assets\icon.ico'),'--version-file',(Join-Path $releaseRoot 'version_info.txt'),
    '--collect-all','cv2','--collect-all','sherpa_onnx','--collect-all','pykakasi','--collect-all','sounddevice',
    '--hidden-import','PIL.ImageTk','--hidden-import','_tkinter',(Join-Path $releaseRoot 'app.py'))
Run-Checked $Python @('-m','PyInstaller','--noconfirm','--windowed','--onefile','--noupx','--name','JapanischTrainerUpdater',
    '--distpath',$app,'--workpath',(Join-Path $work 'updater'),'--specpath',$work,
    '--icon',(Join-Path $releaseRoot 'assets\icon.ico'),(Join-Path $releaseRoot 'update_worker.py'))
Run-Checked $Python @((Join-Path $releaseRoot 'tools\stage_release.py'),$app)
Run-Checked 'powershell.exe' @('-NoProfile','-ExecutionPolicy','Bypass','-File',
    (Join-Path $releaseRoot 'installer_tools\installer\Build-Installer.ps1'),
    '-AppDir',$app,'-Destination',$release,'-IsccPath',$IsccPath,'-NonInteractive',
    '-WorkRoot',(Join-Path $work 'installer'))
Write-Host ('Fertig: '+$release)

#requires -Version 5.1
param([string]$SetupPath='')
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
$validationRoot=Join-Path $projectRoot 'validation'
$runRoot=Join-Path $validationRoot ('installation-'+[guid]::NewGuid().ToString('N'))
$target=Join-Path $runRoot 'app'
$profile=Join-Path $runRoot 'profile'
if(-not ([IO.Path]::GetFullPath($target).StartsWith([IO.Path]::GetFullPath($validationRoot)+'\',[StringComparison]::OrdinalIgnoreCase))){throw 'Invalid test path'}
New-Item -ItemType Directory -Path $runRoot,$profile -Force | Out-Null
$env:JAPANISCHTRAINER_DATA_DIR=$profile
$profileState=@{completed=@('0:0');xp=275;streak=3;teacher_id='yuki';tts_speed=0.85;course_revision=11;last_lesson=@{key='1:1';card=1}}
# Match the application's UTF-8 writer on both Windows PowerShell 5.1 and PowerShell 7.
[IO.File]::WriteAllText((Join-Path $profile 'progress.json'),($profileState | ConvertTo-Json -Depth 5),(New-Object System.Text.UTF8Encoding($false)))
$setup=if($SetupPath){[IO.Path]::GetFullPath($SetupPath)}else{Join-Path $validationRoot 'installer\JapanischTrainer-Validation-Setup.exe'}
function Invoke-TestProcess([string]$File,[string[]]$Arguments,[int]$Timeout=180000){
    $process=Start-Process -FilePath $File -ArgumentList $Arguments -WorkingDirectory $runRoot -WindowStyle Hidden -PassThru
    if(-not $process.WaitForExit($Timeout)){[void]$process.CloseMainWindow();throw ('Test timed out: '+$File)}
    if($process.ExitCode -ne 0){throw ('Test process failed: '+$File+' / '+$process.ExitCode)}
}
$report=[ordered]@{passed=$false;isolated_validation_build=$true;production_appid_tested=$false;work=$runRoot;setup=$setup;setup_sha256=(Get-FileHash -LiteralPath $setup -Algorithm SHA256).Hash.ToLowerInvariant()}
try{
    Invoke-TestProcess $setup @('/SP-','/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART',('/DIR="'+$target+'"'),('/LOG="'+(Join-Path $runRoot 'install.log')+'"'))
    $exe=Join-Path $target 'JapanischTrainer.exe'
    if(-not(Test-Path -LiteralPath $exe)){throw 'Installed executable missing'}
    $shortcut=Join-Path $target 'JapanischTrainer Test.lnk'
    $shell=New-Object -ComObject WScript.Shell
    $link=$shell.CreateShortcut($shortcut)
    if($link.TargetPath -ne $exe -or $link.WorkingDirectory -ne $target){throw 'Invalid shortcut'}
    $capture=Join-Path $runRoot 'shortcut-start.png'
    Invoke-TestProcess $shortcut @('--capture',('"'+$capture+'"'),'--size','1280x860') 90000
    if(-not(Test-Path -LiteralPath $capture)){throw 'Shortcut launch did not create app framebuffer'}
    $before=Get-Content -LiteralPath (Join-Path $profile 'progress.json') -Raw | ConvertFrom-Json
    if($before.xp -ne 275 -or $before.teacher_id -ne 'yuki'){throw 'Profile changed on first install/start'}
    Invoke-TestProcess $setup @('/SP-','/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART',('/DIR="'+$target+'"'),('/LOG="'+(Join-Path $runRoot 'reinstall-update.log')+'"'))
    $after=Get-Content -LiteralPath (Join-Path $profile 'progress.json') -Raw | ConvertFrom-Json
    if($after.xp -ne $before.xp -or $after.teacher_id -ne $before.teacher_id){throw 'Update modified profile'}
    $backupCount=@(Get-ChildItem -LiteralPath (Join-Path $profile 'Backups') -Filter '*.json').Count
    if($backupCount -lt 2){throw 'Setup backups missing'}
    Invoke-TestProcess (Join-Path $target 'unins000.exe') @('/VERYSILENT','/SUPPRESSMSGBOXES','/NORESTART',('/LOG="'+(Join-Path $runRoot 'uninstall.log')+'"'))
    if(Test-Path -LiteralPath $exe){throw 'Uninstaller left executable'}
    if(-not(Test-Path -LiteralPath (Join-Path $profile 'progress.json'))){throw 'Uninstaller removed learning profile'}
    $final=Get-Content -LiteralPath (Join-Path $profile 'progress.json') -Raw | ConvertFrom-Json
    if($final.xp -ne 275 -or $final.teacher_id -ne 'yuki'){throw 'Uninstaller changed profile'}
    $report.passed=$true
    $report.install=$true;$report.shortcut_start=$true;$report.reinstall_preserves_profile=$true
    $report.uninstall=$true;$report.profile_retained=$true;$report.backups=$backupCount
}finally{
    $report | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $validationRoot 'installer-test-report.json') -Encoding UTF8
}
$report | ConvertTo-Json -Depth 5

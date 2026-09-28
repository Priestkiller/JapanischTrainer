#requires -Version 5.1
<#
One-time packager for an ALREADY BUILT JapanischTrainer V11 installation.
It never builds Python code or modifies the source installation. The result is
an Inno Setup offline installer, not a script wrapper or a download bootstrapper.
Windows execution / ISCC compilation must still be performed by the operator.
#>
[CmdletBinding()]
param(
    [string]$AppDir = '',
    [string]$Destination = '',
    [string]$IsccPath = '',
    [switch]$KeepStaging,
    [switch]$NonInteractive,
    [string]$WorkRoot = ''
)
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
$PackageRoot = Split-Path -Parent $PSScriptRoot
$Config = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'config.json') -Raw -Encoding UTF8 | ConvertFrom-Json
$script:Work = $null
$script:TranscriptStarted = $false
$script:Success = $false
$script:ReadyExe = $null
$script:ExitCode = 1
$script:CompilerDescription = ''
$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$LogDir = Join-Path $PackageRoot 'Protokolle'

function Message([string]$Text, [string]$Title = 'JapanischTrainer - Installer erstellen', [bool]$Question = $false) {
    Add-Type -AssemblyName System.Windows.Forms
    if ($NonInteractive) {
        Write-Host ($Title + ': ' + $Text)
        if ($Question) { return [System.Windows.Forms.DialogResult]::No }
        return
    }
    if ($Question) {
        return [System.Windows.Forms.MessageBox]::Show($Text, $Title,
            [System.Windows.Forms.MessageBoxButtons]::YesNo,
            [System.Windows.Forms.MessageBoxIcon]::Question,
            [System.Windows.Forms.MessageBoxDefaultButton]::Button2)
    }
    [void][System.Windows.Forms.MessageBox]::Show($Text, $Title,
        [System.Windows.Forms.MessageBoxButtons]::OK,
        [System.Windows.Forms.MessageBoxIcon]::Information)
}

function Full-Path([string]$Value) {
    return [IO.Path]::GetFullPath([Environment]::ExpandEnvironmentVariables($Value))
}

function Is-Within([string]$Child, [string]$Parent) {
    $a = (Full-Path $Child).TrimEnd('\')
    $b = (Full-Path $Parent).TrimEnd('\')
    return $a.Equals($b, [StringComparison]::OrdinalIgnoreCase) -or
        $a.StartsWith($b + '\', [StringComparison]::OrdinalIgnoreCase)
}

function Need-File([string]$Path, [long]$MinimumSize = 1) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        throw "Erforderliche Datei fehlt: $Path"
    }
    if ((Get-Item -LiteralPath $Path).Length -lt $MinimumSize) {
        throw "Datei ist leer oder unvollstaendig: $Path"
    }
}

function Test-PE([string]$Path, [bool]$RequireX64 = $true) {
    Need-File $Path 1024
    $stream = [IO.File]::OpenRead($Path)
    $reader = New-Object IO.BinaryReader($stream)
    try {
        if ($reader.ReadUInt16() -ne 0x5a4d) { throw "Keine Windows-EXE: $Path" }
        $stream.Position = 0x3c
        $peOffset = $reader.ReadInt32()
        if ($peOffset -lt 64 -or $peOffset -gt ($stream.Length - 26)) {
            throw "Ungueltiger EXE-Kopf: $Path"
        }
        $stream.Position = $peOffset
        if ($reader.ReadUInt32() -ne 0x00004550) { throw "Ungueltige PE-Signatur: $Path" }
        $machine = $reader.ReadUInt16()
        if ($RequireX64 -and $machine -ne 0x8664) {
            throw 'Diese Vorlage braucht den vorhandenen 64-Bit-Build (x64), keine 32-Bit- oder ARM-Datei.'
        }
    } finally { $reader.Dispose(); $stream.Dispose() }
}

function Resolve-AppFolder([string]$Requested) {
    if ($Requested) {
        $path = Full-Path $Requested
        if (Test-Path -LiteralPath $path -PathType Leaf) { $path = Split-Path -Parent $path }
        return $path
    }
    # Only known application locations; never search the user's entire disk.
    $candidates = New-Object 'System.Collections.Generic.List[string]'
    foreach ($key in @(
        'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\JapanischTrainer_is1',
        'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\JapanischTrainer'
    )) {
        $item = Get-ItemProperty -LiteralPath $key -Name InstallLocation -ErrorAction SilentlyContinue
        if ($item -and $item.InstallLocation) { $candidates.Add([string]$item.InstallLocation) }
    }
    $candidates.Add((Join-Path $env:LOCALAPPDATA 'Programs\JapanischTrainer'))
    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath (Join-Path $candidate 'JapanischTrainer.exe') -PathType Leaf) {
            return (Full-Path $candidate)
        }
    }
    Message 'Keine fertig gebaute Installation am Standardort gefunden. Bitte im naechsten Fenster die bereits lauffaehige JapanischTrainer.exe aus V11 auswaehlen. Eine Quellcode-ZIP oder app.py reicht nicht.'
    Add-Type -AssemblyName System.Windows.Forms
    $dialog = New-Object System.Windows.Forms.OpenFileDialog
    $dialog.Title = 'Vorhandene, fertig gebaute JapanischTrainer.exe auswaehlen'
    $dialog.Filter = 'JapanischTrainer.exe|JapanischTrainer.exe'
    $dialog.CheckFileExists = $true
    try {
        if ($dialog.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) {
            throw 'Abgebrochen: keine Programmdatei ausgewaehlt.'
        }
        return (Split-Path -Parent $dialog.FileName)
    } finally { $dialog.Dispose() }
}

function Is-PrivatePath([string]$Relative) {
    $p = $Relative.Replace('\','/').ToLowerInvariant()
    $parts = $p.Split('/')
    foreach ($segment in $parts) {
        if ($segment -in @('.git','.venv','venv','recordings','aufnahmen','logs','cache','__pycache__','test-profile')) {
            return $true
        }
    }
    $name = $parts[$parts.Length - 1]
    return ($name -like 'progress*.json' -or $name -like '*.log' -or
        $name -match '\.(wav|mp3|flac|ogg|m4a|pfx|p12)$' -or
        $name -eq '.env' -or $name -eq 'uninstall.ps1' -or $name -like 'unins*.exe' -or $name -like 'unins*.dat')
}

function Assert-VersionMapping([Version]$AppVersion, [Version]$CourseVersion, $Metadata) {
    $appText = '{0}.{1}.{2}' -f $AppVersion.Major,$AppVersion.Minor,$AppVersion.Build
    $expected = $AppVersion
    if ($null -ne $Metadata) {
        $declared = [Version]$Metadata.version
        $declaredText = '{0}.{1}.{2}' -f $declared.Major,$declared.Minor,$declared.Build
        if ($Metadata.app -ne 'JapanischTrainer' -or $declaredText -ne $appText) { throw 'EXE und release.json passen nicht zusammen.' }
        if ($Metadata.PSObject.Properties.Name -contains 'course_version') { $expected = [Version]$Metadata.course_version }
    }
    if ($CourseVersion.Major -ne $expected.Major -or $CourseVersion.Minor -ne $expected.Minor -or $CourseVersion.Build -ne $expected.Build -or $CourseVersion -gt $AppVersion) {
        throw 'Kursdateien stimmen nicht mit der ausdruecklichen Versionszuordnung ueberein. Keine gemischte Installation verpacken.'
    }
}
function Validate-App([string]$Source) {
    foreach ($relative in $Config.required_files) {
        Need-File (Join-Path $Source $relative)
    }
    Test-PE (Join-Path $Source 'JapanischTrainer.exe')
    foreach ($dir in $Config.allowed_directories) {
        $folder = Join-Path $Source $dir
        if (-not (Test-Path -LiteralPath $folder -PathType Container)) { throw "Programmordner fehlt: $folder" }
        if (((Get-Item -LiteralPath $folder).Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            throw "Verknuepfte Ordner werden aus Sicherheitsgruenden nicht verpackt: $folder"
        }
        foreach ($item in (Get-ChildItem -LiteralPath $folder -Recurse -Force)) {
            if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
                throw "Verknuepfung im Programmordner gefunden: $($item.FullName). Bitte einen vollstaendigen lokalen Programmordner verwenden."
            }
        }
    }
    $internal = Join-Path $Source '_internal'
    $pythonDll = @(Get-ChildItem -LiteralPath $internal -File -Filter 'python3*.dll')
    if ($pythonDll.Count -eq 0) { throw 'Die mitgelieferte Python-Laufzeit fehlt im Ordner _internal. Das ist kein vollstaendiger PyInstaller-Ordner.' }
    if (@(Get-ChildItem -LiteralPath $internal -Recurse -File -Filter '_tkinter.pyd').Count -eq 0) {
        throw 'Das Tkinter-Laufzeitmodul fehlt. Bitte den vollstaendigen dist\JapanischTrainer-Ordner verwenden.'
    }
    foreach ($name in $Config.teachers) {
        foreach ($file in @('full.png','card.png','avatar.png')) {
            Need-File (Join-Path $Source ("assets\teachers\$name\$file"))
        }
    }
    foreach ($model in $Config.model_files.PSObject.Properties) {
        foreach ($file in $model.Value) {
            $min = 1
            if ($file.EndsWith('.onnx')) { $min = 4096 }
            Need-File (Join-Path $Source ("models\$($model.Name)\$file")) $min
        }
    }
    $course = Get-Content -LiteralPath (Join-Path $Source 'data\course.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    $catalog = Get-Content -LiteralPath (Join-Path $Source 'data\catalog.json') -Raw -Encoding UTF8 | ConvertFrom-Json
    $versionInfo = [Diagnostics.FileVersionInfo]::GetVersionInfo((Join-Path $Source 'JapanischTrainer.exe'))
    if ($versionInfo.ProductName -notlike 'JapanischTrainer*') { throw 'Die EXE gehoert laut Versionsinformationen nicht zum JapanischTrainer.' }
    $versionMatch = [regex]::Match([string]$versionInfo.ProductVersion, '^\d+\.\d+\.\d+(?:\.\d+)?')
    if (-not $versionMatch.Success) { throw 'Keine gueltige Programmversion in der EXE gefunden.' }
    $version = [Version]$versionMatch.Value
    if ($version -lt [Version]$Config.minimum_version) {
        throw "Hier ist noch Version $version installiert. Fuer den V11-Installer zuerst die V11 fertig bauen/installieren oder deren dist\JapanischTrainer-Ordner mit -AppDir angeben. Die alte Version wurde nicht veraendert."
    }
    $metadata = $null
    $metadataPath = Join-Path $Source 'release.json'
    if (Test-Path -LiteralPath $metadataPath -PathType Leaf) { $metadata = Get-Content -LiteralPath $metadataPath -Raw -Encoding UTF8 | ConvertFrom-Json }
    Assert-VersionMapping $version $course.content_version $metadata
    $lessons = @($course.units | ForEach-Object { $_.lessons })
    $cards = @($lessons | ForEach-Object { $_.cards })
    if ($lessons.Count -lt $Config.minimum_lessons -or $cards.Count -lt $Config.minimum_cards) {
        throw "Kurs unvollstaendig: $($lessons.Count) Lektionen / $($cards.Count) Karten. Erwartet wird mindestens V11."
    }
    foreach ($name in $Config.teachers) {
        if (@($catalog.TEACHERS | Where-Object { $_.id -eq $name }).Count -ne 1) { throw "Lehrerprofil fehlt oder ist doppelt: $name" }
    }
    return [PSCustomObject]@{
        Version = ('{0}.{1}.{2}' -f $version.Major,$version.Minor,$version.Build)
        Version4 = ('{0}.{1}.{2}.{3}' -f $version.Major,$version.Minor,$version.Build,[Math]::Max(0,$version.Revision))
        VersionMS = (([long]$version.Major -shl 16) -bor $version.Minor)
        VersionLS = (([long]$version.Build -shl 16) -bor [Math]::Max(0,$version.Revision))
        Lessons = $lessons.Count
        Cards = $cards.Count
    }
}

function Get-PayloadFiles([string]$Source) {
    $files = New-Object 'System.Collections.Generic.List[object]'
    foreach ($name in $Config.allowed_root_files) {
        $path = Join-Path $Source $name
        if (Test-Path -LiteralPath $path -PathType Leaf) { $files.Add((Get-Item -LiteralPath $path)) }
    }
    foreach ($dir in $Config.allowed_directories) {
        foreach ($file in (Get-ChildItem -LiteralPath (Join-Path $Source $dir) -Recurse -File -Force)) {
            $rel = $file.FullName.Substring($Source.TrimEnd('\').Length + 1)
            if (-not (Is-PrivatePath $rel)) { $files.Add($file) }
        }
    }
    return @($files | Sort-Object FullName)
}

function Snapshot-Payload([string]$Source, [string]$Stage, [object[]]$Files) {
    New-Item -ItemType Directory -Path $Stage -Force | Out-Null
    $records = New-Object 'System.Collections.Generic.List[object]'
    $index = 0
    foreach ($file in $Files) {
        $index++
        $rel = $file.FullName.Substring($Source.TrimEnd('\').Length + 1)
        $target = Join-Path $Stage $rel
        Write-Progress -Activity 'Programm und Offline-Modelle verpacken' -Status $rel -PercentComplete ([int](100*$index/$Files.Count))
        New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force | Out-Null
        $sourceHash = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        Copy-Item -LiteralPath $file.FullName -Destination $target
        $targetHash = (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($targetHash -ne $sourceHash) { throw "Datei hat sich beim Kopieren veraendert: $rel. JapanischTrainer schliessen und erneut versuchen." }
        $records.Add([PSCustomObject]@{path=$rel.Replace('\','/'); bytes=(Get-Item -LiteralPath $target).Length; sha256=$targetHash})
    }
    Write-Progress -Activity 'Programm und Offline-Modelle verpacken' -Completed
    $manifest = [ordered]@{
        format=1; generated_utc=[DateTime]::UtcNow.ToString('o'); personal_data_included=$false;
        description='Snapshot der Programmdateien. Kein Lernprofil und keine Mikrofonaufnahmen.';
        files=@($records.ToArray())
    }
    [IO.File]::WriteAllText((Join-Path $Stage 'INSTALLATION_MANIFEST.json'),
        ($manifest | ConvertTo-Json -Depth 8), (New-Object Text.UTF8Encoding($false)))
}

function Quote-Native([string]$Value) {
    # Our file arguments cannot contain quotes or newlines. Escape terminal slashes
    # for the Windows CommandLineToArgvW convention; do NOT concatenate shell code.
    if ($Value -match '["\r\n]') { throw 'Ungueltiges Zeichen in einem Programmargument.' }
    return '"' + [regex]::Replace($Value, '(\\+)$', '$1$1') + '"'
}

function Invoke-Process([string]$Exe, [string[]]$Values, [int]$TimeoutSeconds = 0) {
    $line = ($Values | ForEach-Object { Quote-Native $_ }) -join ' '
    $info = New-Object Diagnostics.ProcessStartInfo
    $info.FileName = $Exe
    $info.Arguments = $line
    $info.WorkingDirectory = Split-Path -Parent $Exe
    $info.UseShellExecute = $false
    $p = New-Object Diagnostics.Process
    $p.StartInfo = $info
    try {
        if (-not $p.Start()) { throw "Prozess konnte nicht gestartet werden: $Exe" }
        if ($TimeoutSeconds -gt 0) {
            if (-not $p.WaitForExit($TimeoutSeconds * 1000)) {
                try { $p.Kill(); $p.WaitForExit(5000) | Out-Null } catch {}
                throw "Zeitlimit beim Start von $([IO.Path]::GetFileName($Exe)). Details im Protokoll."
            }
        } else { $p.WaitForExit() }
        if ($p.ExitCode -ne 0) { throw "Programm fehlgeschlagen, Exit-Code $($p.ExitCode): $Exe" }
    } finally { $p.Dispose() }
}

function Test-StagedLaunch([string]$Stage, [string]$Work) {
    Write-Host '[3/6] Vorhandene EXE mit getrenntem Testprofil starten ...' -ForegroundColor Cyan
    $old = [Environment]::GetEnvironmentVariable('JAPANISCHTRAINER_DATA_DIR', 'Process')
    $profile = Join-Path $Work 'test-profile'
    $capture = Join-Path $Work 'Starttest.png'
    try {
        $env:JAPANISCHTRAINER_DATA_DIR = $profile
        Invoke-Process (Join-Path $Stage 'JapanischTrainer.exe') @('--page','home','--size','1280x860','--capture',$capture) 90
        Need-File $capture 5000
        $bytes = [IO.File]::ReadAllBytes($capture)
        if ([BitConverter]::ToString($bytes[0..7]) -ne '89-50-4E-47-0D-0A-1A-0A') {
            throw 'Der Starttest hat keine gueltige PNG-Aufnahme erzeugt.'
        }
    } finally {
        [Environment]::SetEnvironmentVariable('JAPANISCHTRAINER_DATA_DIR', $old, 'Process')
    }
    return $capture
}

function Compiler-Accepted([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { return $false }
    $info = [Diagnostics.FileVersionInfo]::GetVersionInfo($Path)
    # Dark-mode wizard directives require Inno Setup 6.6 or newer.
    if (($info.FileMajorPart -eq 6 -and $info.FileMinorPart -ge 6) -or $info.FileMajorPart -eq 7) { return $true }
    # Some official Inno 7 binaries expose 0.0.0.0 in the PE version resource.
    $startInfo = New-Object Diagnostics.ProcessStartInfo
    $startInfo.FileName = $Path
    $startInfo.Arguments = '/?'
    $startInfo.UseShellExecute = $false
    $startInfo.CreateNoWindow = $true
    $startInfo.RedirectStandardOutput = $true
    $startInfo.RedirectStandardError = $true
    $compilerProbe = [Diagnostics.Process]::Start($startInfo)
    try {
        $helpText = $compilerProbe.StandardOutput.ReadToEnd() + $compilerProbe.StandardError.ReadToEnd()
        $compilerProbe.WaitForExit()
        return ($helpText -match '(?m)^Inno Setup 7 Command-Line Compiler')
    } finally { $compilerProbe.Dispose() }
}

function Find-Compiler([string]$Explicit) {
    if ($Explicit) {
        $p = Full-Path $Explicit
        if (-not (Compiler-Accepted $p)) { throw 'Bitte ISCC.exe von Inno Setup 6.6+ oder 7 angeben.' }
        return $p
    }
    $paths = New-Object 'System.Collections.Generic.List[string]'
    $cmd = Get-Command ISCC.exe -ErrorAction SilentlyContinue
    if ($cmd) { $paths.Add($cmd.Source) }
    foreach ($base in @(${env:ProgramFiles(x86)},$env:ProgramFiles,(Join-Path $env:LOCALAPPDATA 'Programs'))) {
        if (-not $base) { continue }
        foreach ($dir in @('Inno Setup 7','Inno Setup 6')) { $paths.Add((Join-Path $base ($dir+'\ISCC.exe'))) }
    }
    foreach ($p in $paths) { if (Compiler-Accepted $p) { return $p } }
    return $null
}

function Ensure-Compiler([string]$Explicit, [string]$Work) {
    $found = Find-Compiler $Explicit
    if ($found) { return $found }
    $text = "Zum einmaligen Erstellen der Setup.exe wird Inno Setup $($Config.compiler.version) gebraucht. Es ist ein separates Installer-Werkzeug, nicht Python und kein Sprachmodell.`r`n`r`nSoll der offizielle, signierte Installer heruntergeladen und fuer dein Benutzerkonto installiert werden?`r`n`r`nDer Download wird vor dem Start mit fest hinterlegter SHA-256-Pruefsumme und Windows-Signatur geprueft. Hinweise des Herstellers zur privaten/gewerblichen Nutzung stehen in der Anleitung."
    $answer = Message $text 'Inno Setup als Verpackungswerkzeug' $true
    if ($answer -ne [System.Windows.Forms.DialogResult]::Yes) {
        throw 'Kein Compiler installiert. Du kannst Inno Setup selbst von jrsoftware.org installieren und dann SETUP_ERSTELLEN.bat erneut starten.'
    }
    [Net.ServicePointManager]::SecurityProtocol = [Net.ServicePointManager]::SecurityProtocol -bor [Net.SecurityProtocolType]::Tls12
    $download = Join-Path $Work ('innosetup-'+$Config.compiler.version+'.exe')
    Write-Host 'Offizielles Inno Setup herunterladen ...' -ForegroundColor Cyan
    Invoke-WebRequest -Uri $Config.compiler.url -OutFile $download -UseBasicParsing -TimeoutSec 240
    $hash = (Get-FileHash -LiteralPath $download -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($hash -ne $Config.compiler.sha256) { throw 'Die Compiler-Pruefsumme stimmt nicht. Der Download wird NICHT ausgefuehrt.' }
    $signature = Get-AuthenticodeSignature -LiteralPath $download
    if ($signature.Status -ne [System.Management.Automation.SignatureStatus]::Valid -or
        -not $signature.SignerCertificate -or $signature.SignerCertificate.Subject -notmatch 'Pyrsys B\.V\.') {
        throw 'Die Windows-Signatur des Compiler-Installers konnte nicht bestaetigt werden. Es wird nichts ausgefuehrt. Bitte Datum, Internetzugang und offizielle Signatur pruefen; Sicherheitsfunktionen nicht abschalten.'
    }
    # This is the explicitly accepted tool installation. The produced application
    # installer has no compiler, PowerShell, pip, winget or network dependency.
    $toolDir = Join-Path $env:LOCALAPPDATA 'Programs\Inno Setup 6'
    Invoke-Process $download @('/CURRENTUSER','/SP-','/SILENT','/SUPPRESSMSGBOXES','/NORESTART','/TASKS=',('/DIR='+$toolDir)) 600
    $found = Find-Compiler ''
    if (-not $found) { throw 'Inno Setup wurde nicht gefunden. Bitte die Installation des Werkzeugs pruefen.' }
    return $found
}

try {
    if ($env:OS -ne 'Windows_NT') { throw 'Dieses Verpackungswerkzeug muss unter Windows ausgefuehrt werden.' }
    if (-not [Environment]::Is64BitOperatingSystem) { throw 'Windows 10/11 in 64 Bit wird benoetigt.' }
    New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
    Start-Transcript -Path (Join-Path $LogDir ('Installer-'+$stamp+'.log')) | Out-Null
    $script:TranscriptStarted = $true
    Write-Host '[1/6] Vorhandenes Programm pruefen ...' -ForegroundColor Cyan
    $Source = (Resolve-AppFolder $AppDir).TrimEnd('\')
    if (Get-Process -Name JapanischTrainer -ErrorAction SilentlyContinue) {
        throw 'JapanischTrainer ist noch geoeffnet. Bitte normal schliessen und danach SETUP_ERSTELLEN.bat erneut starten.'
    }
    $meta = Validate-App $Source
    Write-Host ("V{0}: {1} Lektionen, {2} Lernkarten, acht Lehrer und alle drei Offline-Modelle gefunden." -f $meta.Version,$meta.Lessons,$meta.Cards) -ForegroundColor Green
    if (-not $Destination) { $Destination = Join-Path $PackageRoot 'Fertiger_Installer' }
    $Destination = Full-Path $Destination
    if (Is-Within $Destination $Source) { throw 'Der Ausgabeordner darf nicht innerhalb der installierten Anwendung liegen.' }
    $workBase = if ($WorkRoot) { Full-Path $WorkRoot } else { Join-Path $PackageRoot 'build-work' }
    New-Item -ItemType Directory -Path $workBase -Force | Out-Null
    $script:Work = Join-Path $workBase ([Guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $script:Work | Out-Null
    if (Is-Within $script:Work $Source) { throw 'Arbeitsordner und Programmquelle duerfen sich nicht ueberschneiden.' }
    $files = @(Get-PayloadFiles $Source)
    $sourceBytes = ($files | Measure-Object Length -Sum).Sum
    if ($sourceBytes -gt 1850MB) {
        throw 'Die Programmkopie ist groesser als die Sicherheitsgrenze fuer den einzelnen Setup-EXE-Container dieser Vorlage (1850 MiB). Es wurde kein unvollstaendiger Installer erzeugt. Dafuer ist ein mehrteiliges Installationspaket noetig.'
    }
    # Reserve space for the snapshot, compressed installer, and safety margin.
    $needed = [long](2*$sourceBytes + 768MB)
    $workDrive = New-Object IO.DriveInfo([IO.Path]::GetPathRoot($script:Work))
    if ($workDrive.AvailableFreeSpace -lt $needed) { throw ('Zu wenig freier Speicher fuer die Erstellung. Benoetigt etwa {0:N1} GB.' -f ($needed/1GB)) }
    New-Item -ItemType Directory -Path $Destination -Force | Out-Null
    $destDrive = New-Object IO.DriveInfo([IO.Path]::GetPathRoot($Destination))
    if ($destDrive.AvailableFreeSpace -lt ($sourceBytes+256MB)) { throw 'Auf dem Ausgabelaufwerk ist zu wenig freier Speicher.' }
    Write-Host '[2/6] Unveraenderte Programmkopie mit Pruefsummen anlegen ...' -ForegroundColor Cyan
    $stage = Join-Path $script:Work 'payload'
    Snapshot-Payload $Source $stage $files
    # Revalidate the snapshot after privacy filtering and verified copying.
    [void](Validate-App $stage)
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'Installation_Hinweise.txt') -Destination (Join-Path $stage 'INSTALLATION_HINWEISE.txt')
    $capture = Test-StagedLaunch $stage $script:Work
    Write-Host '[4/6] Installer-Compiler bereitstellen ...' -ForegroundColor Cyan
    $compiler = Ensure-Compiler $IsccPath $script:Work
    $script:CompilerDescription = [Diagnostics.FileVersionInfo]::GetVersionInfo($compiler).FileVersion
    Write-Host '[5/6] Echte Setup.exe inklusive Offline-Modellen erstellen ...' -ForegroundColor Cyan
    $outBase = ('JapanischTrainer-'+$meta.Version+'-Setup-x64')
    # Compile to a unique intermediate directory. An interrupted build cannot be
    # mistaken for an older installer already present in Fertiger_Installer.
    $buildOut = Join-Path $script:Work 'compiled'
    New-Item -ItemType Directory -Path $buildOut | Out-Null
    $arguments = @(
        ('/DAppSource='+$stage),('/DAppVersion='+$meta.Version),('/DAppVersion4='+$meta.Version4),
        ('/DAppVersionMS='+$meta.VersionMS),('/DAppVersionLS='+$meta.VersionLS),
        ('/O'+$buildOut),('/F'+$outBase),(Join-Path $PSScriptRoot 'JapanischTrainer.iss')
    )
    # Use direct invocation here so the compiler's own progress/error messages
    # are visible and captured by the transcript. Every argument is separate.
    & $compiler @arguments
    if ($LASTEXITCODE -ne 0) { throw "Inno Setup meldet einen Fehler ($LASTEXITCODE). Kein fertiges Paket freigegeben." }
    $built = Join-Path $buildOut ($outBase+'.exe')
    Need-File $built 1048576
    Test-PE $built $false
    $hash = (Get-FileHash -LiteralPath $built -Algorithm SHA256).Hash.ToLowerInvariant()
    $final = Join-Path $Destination ($outBase+'.exe')
    # Never silently discard a previously built setup.
    if (Test-Path -LiteralPath $final) {
        $answer = Message "Im Ausgabeordner existiert bereits $outBase.exe.`r`n`r`nSoll sie durch den gerade erfolgreich erstellten Installer ersetzt werden?" 'Vorhandenen Installer ersetzen?' $true
        if ($answer -ne [System.Windows.Forms.DialogResult]::Yes) {
            $final = Join-Path $Destination ($outBase+'-'+$stamp+'.exe')
        }
    }
    Copy-Item -LiteralPath $built -Destination $final -Force
    if ((Get-FileHash -LiteralPath $final -Algorithm SHA256).Hash.ToLowerInvariant() -ne $hash) {
        throw 'Pruefsumme der ausgegebenen Setup.exe ist ungueltig. Datei nicht verwenden.'
    }
    $script:ReadyExe = $final
    $leaf = [IO.Path]::GetFileName($final)
    [IO.File]::WriteAllText(($final+'.sha256'), ($hash+'  '+$leaf+"`r`n"), [Text.Encoding]::ASCII)
    $checkDir = Join-Path $Destination 'Pruefung'
    New-Item -ItemType Directory -Path $checkDir -Force | Out-Null
    Copy-Item -LiteralPath $capture -Destination (Join-Path $checkDir ('Starttest-'+$stamp+'.png'))
    $report = [ordered]@{
        app_version=$meta.Version; created_utc=[DateTime]::UtcNow.ToString('o');
        installer=$leaf; sha256=$hash; installer_bytes=(Get-Item -LiteralPath $final).Length;
        input_files=$files.Count; input_bytes=$sourceBytes; lessons=$meta.Lessons; learning_cards=$meta.Cards;
        all_model_files_present=$true; all_teachers_present=$true; staged_exe_launch_test='passed';
        staged_exe_test_profile='separate temporary profile; no personal progress copied';
        installed_end_to_end_test='not performed by this packaging step';
        microphone_and_model_inference='not tested by this packaging step';
        compiler_version=$script:CompilerDescription; code_signed=$false
    }
    [IO.File]::WriteAllText((Join-Path $checkDir ('Buildbericht-'+$stamp+'.json')),
        ($report | ConvertTo-Json -Depth 6),(New-Object Text.UTF8Encoding($false)))
    Write-Host '[6/6] Fertig. Setup.exe und SHA-256-Pruefsumme liegen im Ausgabeordner.' -ForegroundColor Green
    Write-Host $final -ForegroundColor Green
    Write-Host 'Der Installer ist nicht digital signiert. Virenschutz/SmartScreen nicht abschalten.'
    Write-Host 'Die vorhandene Lern-App und dein Lernprofil wurden nicht veraendert.'
    $script:Success = $true
    $script:ExitCode = 0
    try { Message ("Installer erstellt:`r`n$final`r`n`r`nDiese Setup.exe enthaelt das vorhandene Programm, Laufzeit, Figuren, Kurs und Sprachmodelle. Fuer eine Installation wird kein Python oder Compiler benoetigt.`r`n`r`nBitte die Setup.exe vor Weitergabe auf einem zweiten Windows-Benutzerkonto testen. Sie ist nicht digital signiert.") 'JapanischTrainer - Setup.exe erstellt'
    if (-not $NonInteractive) { Start-Process -FilePath 'explorer.exe' -ArgumentList ('/select,'+(Quote-Native $final)) }
    } catch { Write-Warning ('Installer wurde erstellt, aber die Abschlussanzeige konnte nicht geoeffnet werden: '+$_.Exception.Message) }
} catch {
    $script:ExitCode = 1
    Write-Host ''
    Write-Host ('ABBRUCH: '+$_.Exception.Message) -ForegroundColor Red
    Write-Host $_.ScriptStackTrace
    try { Message ($_.Exception.Message+"`r`n`r`nEs wurde kein neuer, freigegebener Installer gemeldet. Deine vorhandene Installation bleibt unveraendert.`r`n`r`nDetails im Ordner Protokolle neben SETUP_ERSTELLEN.bat.") 'Installer noch nicht erstellt' } catch {}
} finally {
    if ($script:TranscriptStarted) { try { Stop-Transcript | Out-Null } catch {} }
    # Only delete our own GUID staging directory, never source or output files.
    if ($script:Work -and (Test-Path -LiteralPath $script:Work)) {
        if ($KeepStaging) { Write-Host ('Arbeitsordner behalten: '+$script:Work) }
        elseif ((Split-Path -Leaf $script:Work) -match '^[0-9a-f]{32}$' -and (Is-Within $script:Work $workBase)) {
            try { Remove-Item -LiteralPath $script:Work -Recurse -Force } catch { Write-Warning "Arbeitsordner bitte spaeter entfernen: $script:Work" }
        }
    }
}
exit $script:ExitCode

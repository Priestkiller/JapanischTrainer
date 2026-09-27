$ErrorActionPreference='Stop'
$Root=Split-Path -Parent $MyInvocation.MyCommand.Path
$Models=Join-Path $Root 'models'
New-Item -ItemType Directory -Force -Path $Models | Out-Null
function Has-Files([string]$Folder,[string[]]$Files) {
    foreach ($f in $Files) {
        $p=Join-Path $Folder $f
        if (-not (Test-Path $p -PathType Leaf)) { return $false }
        if ((Get-Item $p).Length -eq 0) { return $false }
    }
    return $true
}
function Ensure-Model([string]$Name,[string]$Url,[string]$Extracted,[string]$TargetName,[string[]]$Files) {
    $Target=Join-Path $Models $TargetName
    if (Has-Files $Target $Files) { Write-Host "[OK] $Name vorhanden, kein Download." -ForegroundColor Green;return }
    $Tmp=Join-Path $env:TEMP ('JapanischTrainerV7-'+[guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Force -Path $Tmp | Out-Null
    try {
        $Archive=Join-Path $Tmp 'model.tar.bz2'
        Write-Host "[DOWNLOAD] $Name" -ForegroundColor Cyan
        if (Get-Command curl.exe -ErrorAction SilentlyContinue) {
            & curl.exe -L --fail --retry 4 --retry-delay 3 --output $Archive $Url
            if ($LASTEXITCODE -ne 0) { throw "Modell-Download fehlgeschlagen: $Name" }
        } else { Invoke-WebRequest -Uri $Url -OutFile $Archive -UseBasicParsing }
        & tar.exe -xjf $Archive -C $Tmp
        if ($LASTEXITCODE -ne 0) { throw "Entpacken fehlgeschlagen: $Name" }
        $Source=Join-Path $Tmp $Extracted
        if (-not (Has-Files $Source $Files)) { throw "Modell unvollstaendig: $Name" }
        if (Test-Path $Target) { Remove-Item $Target -Recurse -Force }
        Move-Item $Source $Target
    } finally { if (Test-Path $Tmp) { Remove-Item $Tmp -Recurse -Force } }
}
# Same release artifacts as the supplied V6 audio backend.
Ensure-Model 'Supertonic 3 - japanische Stimmen' `
 'https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/sherpa-onnx-supertonic-3-tts-int8-2026-05-11.tar.bz2' `
 'sherpa-onnx-supertonic-3-tts-int8-2026-05-11' 'supertonic' `
 @('duration_predictor.int8.onnx','text_encoder.int8.onnx','vector_estimator.int8.onnx','vocoder.int8.onnx','tts.json','unicode_indexer.bin','voice.bin')
Ensure-Model 'Parakeet JA - japanische Erkennung' `
 'https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-nemo-parakeet-tdt_ctc-0.6b-ja-35000-int8.tar.bz2' `
 'sherpa-onnx-nemo-parakeet-tdt_ctc-0.6b-ja-35000-int8' 'parakeet-ja' @('model.int8.onnx','tokens.txt')
Ensure-Model 'SenseVoice - zweite Erkennung' `
 'https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17.tar.bz2' `
 'sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17' 'sensevoice' @('model.int8.onnx','tokens.txt')

#requires -Version 7.0
[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$Apk,[string]$Output='',
      [string]$JavaDirectory='', [string]$BuildToolsDirectory='', [switch]$InitializeKey)
$ErrorActionPreference='Stop'
$mobileRoot=Split-Path -Parent $PSScriptRoot
$keyDirectory=Join-Path $mobileRoot '.keys'
if(-not $JavaDirectory){$JavaDirectory=(Get-ChildItem -LiteralPath (Join-Path $mobileRoot 'toolchain\jdk') -Directory | Select-Object -First 1).FullName}
if(-not $BuildToolsDirectory){$BuildToolsDirectory=Join-Path $mobileRoot 'toolchain\build-tools\android-15'}
$java=Join-Path $JavaDirectory 'bin\java.exe'
$keytool=Join-Path $JavaDirectory 'bin\keytool.exe'
$signer=Join-Path $BuildToolsDirectory 'lib\apksigner.jar'
foreach($file in @($Apk,$java,$keytool,$signer)){if(-not(Test-Path -LiteralPath $file)){throw ('Datei fehlt: '+$file)}}
$key=Join-Path $keyDirectory 'android-release.p12'
$passwordFile=Join-Path $keyDirectory 'android-signing-password.txt'
if(-not(Test-Path -LiteralPath $key)){
    if(-not $InitializeKey){throw 'Herausgeberschlüssel fehlt. Keinen neuen Schlüssel für ein bestehendes Release erzeugen.'}
    if(Test-Path -LiteralPath $passwordFile){throw 'Unvollständige Schlüsselanlage: vorhandene Datei zuerst prüfen.'}
    New-Item -ItemType Directory -Path $keyDirectory -Force | Out-Null
    $acl=Get-Acl -LiteralPath $keyDirectory
    $acl.SetAccessRuleProtection($true,$false)
    $sid=[Security.Principal.WindowsIdentity]::GetCurrent().User
    $rule=New-Object Security.AccessControl.FileSystemAccessRule($sid,'FullControl','ContainerInherit,ObjectInherit','None','Allow')
    $acl.AddAccessRule($rule)
    Set-Acl -LiteralPath $keyDirectory -AclObject $acl
    $password=[Convert]::ToBase64String([Security.Cryptography.RandomNumberGenerator]::GetBytes(48))
    [IO.File]::WriteAllText($passwordFile,$password,(New-Object System.Text.UTF8Encoding($false)))
    $password=$null
    & $keytool -genkeypair -noprompt -alias trainer -keyalg RSA -keysize 3072 -sigalg SHA256withRSA -validity 10000 -storetype PKCS12 -keystore $key '-storepass:file' $passwordFile '-keypass:file' $passwordFile -dname 'CN=Priestkiller, OU=JapanischTrainer, O=Priestkiller'
    if($LASTEXITCODE -ne 0){throw 'Android-Schlüssel konnte nicht erzeugt werden.'}
}
if(-not $Output){$Output=Join-Path $mobileRoot 'release\JapanischTrainer-11.0.1-Android.apk'}
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Output) | Out-Null
& $java -jar $signer sign --ks $key --ks-key-alias trainer --ks-pass ('file:'+$passwordFile) --v4-signing-enabled false --min-sdk-version 28 --out $Output $Apk
if($LASTEXITCODE -ne 0){throw 'APK-Signierung fehlgeschlagen.'}
& $java -jar $signer verify --verbose --print-certs $Output
if($LASTEXITCODE -ne 0){throw 'APK-Signaturprüfung fehlgeschlagen.'}
& (Join-Path $BuildToolsDirectory 'zipalign.exe') -c -P 16 4 $Output
if($LASTEXITCODE -ne 0){throw 'APK-Alignment fehlgeschlagen.'}
Get-FileHash -LiteralPath $Output -Algorithm SHA256

; JapanischTrainer - real offline setup, packaging an already built x64 app.
; Compile with Inno Setup >= 6.6. Build-Installer.ps1 supplies all defines.
; No Python, PowerShell, compiler or model downloads run on the recipient's PC.
#ifndef AppSource
  #error AppSource fehlt. Bitte SETUP_ERSTELLEN.bat verwenden.
#endif
#ifndef AppVersion
  #error AppVersion fehlt.
#endif
#ifndef AppVersion4
  #error AppVersion4 fehlt.
#endif
#ifndef AppVersionMS
  #error AppVersionMS fehlt.
#endif
#ifndef AppVersionLS
  #error AppVersionLS fehlt.
#endif

[Setup]
#ifdef ValidationBuild
AppId=JapanischTrainerValidation
CreateUninstallRegKey=no
UsePreviousAppDir=no
#else
AppId=JapanischTrainer
UsePreviousAppDir=yes
#endif
AppName=JapanischTrainer
AppVersion={#AppVersion}
AppVerName=JapanischTrainer {#AppVersion}
AppPublisher=JapanischTrainer
VersionInfoVersion={#AppVersion4}
VersionInfoProductName=JapanischTrainer
VersionInfoDescription=JapanischTrainer Offline-Installation
DefaultDirName={localappdata}\Programs\JapanischTrainer
DefaultGroupName=JapanischTrainer
DisableProgramGroupPage=yes
AllowNoIcons=yes
PrivilegesRequired=lowest
ArchitecturesAllowed=x64os
ArchitecturesInstallIn64BitMode=x64os
MinVersion=10.0.17763
UninstallDisplayName=JapanischTrainer
UninstallDisplayIcon={app}\JapanischTrainer.exe
OutputBaseFilename=JapanischTrainer-{#AppVersion}-Setup-x64
SetupIconFile={#AppSource}\assets\icon.ico
WizardStyle=modern dark
WizardSizePercent=110
DisableWelcomePage=no
DisableReadyPage=no
DisableFinishedPage=no
InfoBeforeFile=Installation_Hinweise.txt
LicenseFile={#AppSource}\MODEL_LICENSES.txt
Compression=lzma2/normal
SolidCompression=yes
LZMANumBlockThreads=2
DiskSpanning=no
CloseApplications=yes
CloseApplicationsFilter=*.exe,*.dll,*.pyd
RestartApplications=no
UsePreviousGroup=yes
UsePreviousTasks=yes
SetupLogging=yes
Uninstallable=yes
SignedUninstaller=no

[Languages]
Name: "german"; MessagesFile: "compiler:Languages\German.isl"

[Messages]
WelcomeLabel1=Willkommen bei JapanischTrainer
WelcomeLabel2=Dieser Assistent installiert JapanischTrainer {#AppVersion} mit Kurs, Figuren, Laufzeit und Offline-Sprachmodellen.%n%nBitte schließe JapanischTrainer vor einem Update.%n%nFür die Installation werden weder Python noch ein Compiler benötigt. Dein vorhandener Lernfortschritt bleibt separat gespeichert.
FinishedHeadingLabel=JapanischTrainer wurde installiert
FinishedLabel=Du kannst JapanischTrainer jetzt über das Startmenü starten.%n%nStimmen und Spracherkennung sind lokal enthalten. Mikrofonberechtigungen und ein geeignetes Audio-Gerät werden weiterhin benötigt.

[Tasks]
Name: "desktopicon"; Description: "Verknüpfung auf dem Desktop erstellen"; GroupDescription: "Verknüpfungen:"

[Files]
; AppSource is a verified snapshot containing ONLY allowlisted program files.
; Never use the user's whole installation/profile directory directly here.
Source: "{#AppSource}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
#ifdef ValidationBuild
Name: "{app}\JapanischTrainer Test"; Filename: "{app}\JapanischTrainer.exe"; WorkingDir: "{app}"; IconFilename: "{app}\assets\icon.ico"
#else
Name: "{group}\JapanischTrainer"; Filename: "{app}\JapanischTrainer.exe"; WorkingDir: "{app}"; IconFilename: "{app}\assets\icon.ico"
Name: "{group}\JapanischTrainer deinstallieren"; Filename: "{uninstallexe}"
Name: "{userdesktop}\JapanischTrainer"; Filename: "{app}\JapanischTrainer.exe"; WorkingDir: "{app}"; IconFilename: "{app}\assets\icon.ico"; Tasks: desktopicon
#endif

[Run]
Filename: "{app}\JapanischTrainer.exe"; WorkingDir: "{app}"; Description: "JapanischTrainer starten"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Remove app-owned files added by later updates. Never target APPDATA.
Type: filesandordirs; Name: "{app}\_internal"
Type: filesandordirs; Name: "{app}\assets"
Type: filesandordirs; Name: "{app}\data"
Type: filesandordirs; Name: "{app}\licenses"
Type: filesandordirs; Name: "{app}\.update-*"
Type: files; Name: "{app}\.update.lock"

[Code]
const
  LegacyKey = 'Software\Microsoft\Windows\CurrentVersion\Uninstall\JapanischTrainer';
  NewVersionMS = {#AppVersionMS};
  NewVersionLS = {#AppVersionLS};
var
  ProgressBackedUp: Boolean;
  LegacySameLocation: Boolean;

function SamePath(const Left, Right: String): Boolean;
begin
  Result := CompareText(AddBackslash(Left), AddBackslash(Right)) = 0;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
var
  CurrentMS, CurrentLS: Cardinal;
  ProgressFile, BackupDir, BackupFile, BaseName, LegacyDir: String;
  Suffix: Integer;
begin
  Result := '';
  { Do not silently downgrade an existing newer app. }
  if GetVersionNumbers(ExpandConstant('{app}\JapanischTrainer.exe'), CurrentMS, CurrentLS) then
  begin
    if (CurrentMS > NewVersionMS) or ((CurrentMS = NewVersionMS) and (CurrentLS > NewVersionLS)) then
    begin
      Result := 'Im gewählten Ordner ist bereits eine neuere Version installiert. Bitte einen passenden neueren Installer verwenden. Es wurden noch keine Programmdateien ersetzt.';
      Exit;
    end;
  end;

  LegacySameLocation := False;
#ifndef ValidationBuild
  if RegQueryStringValue(HKCU, LegacyKey, 'InstallLocation', LegacyDir) then
    LegacySameLocation := SamePath(LegacyDir, ExpandConstant('{app}'));
#endif

  if ProgressBackedUp then Exit;
#ifdef ValidationBuild
  ProgressFile := GetEnv('JAPANISCHTRAINER_DATA_DIR') + '\progress.json';
#else
  ProgressFile := ExpandConstant('{userappdata}\JapanischTrainer\progress.json');
#endif
  if FileExists(ProgressFile) then
  begin
    BackupDir := ExtractFileDir(ProgressFile) + '\Backups';
    if not ForceDirectories(BackupDir) then
    begin
      Result := 'Der vorhandene Lernfortschritt konnte nicht gesichert werden. Bitte die Schreibrechte im Benutzerprofil prüfen. Das Update wird nicht gestartet.';
      Exit;
    end;
    BaseName := BackupDir + '\progress.before-setup-' + GetDateTimeString('yyyymmdd-hhnnss', '-', ':');
    BackupFile := BaseName + '.json';
    Suffix := 1;
    while FileExists(BackupFile) do
    begin
      BackupFile := BaseName + '-' + IntToStr(Suffix) + '.json';
      Suffix := Suffix + 1;
    end;
    if not FileCopy(ProgressFile, BackupFile, True) then
    begin
      Result := 'Die Fortschrittssicherung ist fehlgeschlagen. Bitte JapanischTrainer schließen und das Update erneut starten. Es werden keine Programmdateien ersetzt.';
      Exit;
    end;
    Log('Lernfortschritt gesichert: ' + BackupFile);
  end;
  ProgressBackedUp := True;
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  if (CurStep = ssPostInstall) and LegacySameLocation then
  begin
    { The old batch-based installer used a different uninstall key. Remove
      only that exact entry AFTER a successful install at the same path. }
    if not RegDeleteKeyIncludingSubkeys(HKCU, LegacyKey) then
      Log('Alter Deinstallations-Eintrag konnte nicht entfernt werden.');
    { Remove only the old, specifically named launcher files. Never remove
      *.previous, a source project, models or anything in APPDATA. }
    DeleteFile(ExpandConstant('{app}\uninstall.ps1'));
    DeleteFile(ExpandConstant('{userprograms}\JapanischTrainer.lnk'));
    DeleteFile(ExpandConstant('{userprograms}\JapanischTrainer deinstallieren.lnk'));
  end;
end;

{ Learner progress and its backups are retained outside the program directory. }

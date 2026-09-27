# Windows-Build und Updates

Stand: JapanischTrainer 11.0.1, 27.09.2026.

## Verwendete Umgebung

- Windows x64, Build 10.0.26200.0; PowerShell 7.6.5 und Windows PowerShell 5.1.
- Python 3.12.10 x64 mit Tk, PyInstaller 6.22.3, Hooks 2026.7.
- Inno Setup 7 (`ISCC /?` bestätigt die Hauptversion; diese Installation meldet
  im PE-Versionsfeld 0.0.0.0). Kein Compiler-Download für diesen Build nötig.
- Vollständige Paketversionen: `requirements-lock.txt`. Keine pauschalen Updates.

## Reproduzieren

In PowerShell im Projektordner:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
# Vorhandene vollständige Modelle unter models/ bereitstellen.
# Alternativ download_models.ps1 nach Prüfung der offiziellen Quellen verwenden.
.\.venv\Scripts\python.exe selftest.py
.\Build-Release.ps1 -IsccPath 'C:\Program Files\Inno Setup 7\ISCC.exe'
```

`Build-Release.ps1` baut App und Update-Helfer in `build-release/<Version>/`,
kopiert nur Programmressourcen und kompiliert das Setup unter `release/`.
Es installiert die App nicht in das persönliche Benutzerkonto. Das historische
`INSTALLIEREN.bat` und `build_windows.ps1` sind kein isolierter Release-Build.

Die Build-Umgebung benötigt einmalig installierte Pakete und Modelle. Auf dem
Zielrechner benötigt der fertige Installer kein Python, pip oder Modell-Download.
Bitidentische Reproduzierbarkeit wird wegen Build-Zeitstempeln nicht behauptet.

## Signierte Updates veröffentlichen

Die Update-Adresse ist
`https://github.com/Priestkiller/JapanischTrainer/releases/latest/download/update.json`.
Nur eine ausdrückliche Nutzeraktion startet die Prüfung oder den Download.

1. App-Version in `app.py`, `release.json`, `version_info.txt` und den passenden
   Release-/Kursmetadaten konsistent aktualisieren; Kurskennungen nicht ändern.
2. Tests ausführen und den neuen Installer bauen.
3. Update-Paket erstellen:

```powershell
.\.venv\Scripts\python.exe tools\package_update.py `
  --source build-release\11.0.1\dist\JapanischTrainer --output release `
  --key .release-keys\update-ed25519.key `
  --url https://github.com/Priestkiller/JapanischTrainer/releases/download/v11.0.1/JapanischTrainer-11.0.1-Update-x64.zip `
  --notes RELEASE_NOTES_11.0.1.md
```

4. Zuerst als Entwurf auf GitHub bereitstellen: Setup, Update-ZIP, `update.json`,
   Prüfsummen, passender Quellcode und Berichte. Nach Prüfung veröffentlichen.
   Vor dem nächsten Release alle Versionsnummern und Downloadnamen anpassen.

**Privater Update-Schlüssel:** `.release-keys/update-ed25519.key` bleibt ausschließlich
lokal und muss separat sicher gesichert werden. Niemals in Git, ZIPs, Installer,
Logs oder GitHub-Releases aufnehmen. `update-source.json` enthält nur den öffentlichen
Prüfschlüssel. `tools/init_update_key.py` dient der einmaligen Einrichtung eines
eigenen Herausgebers; den offiziellen Schlüssel nicht unabsichtlich ersetzen.
Der Ed25519-Schlüssel ist kein Windows-Code-Signing-Zertifikat.

Das Update-ZIP enthält Programm, Ressourcen und Bibliotheken, jedoch keine
unveränderten Modellgewichte. Es prüft die bereits vorhandenen Modelle gegen den
Paketvertrag. Bei Änderungen an den Modellgewichten ist in dieser Version das
vollständige neue Setup erforderlich; ein separater Modell-Updater ist nicht enthalten.

Vor dem Austausch werden Dateien und Signaturen geprüft. Der Helfer wartet auf
das Beenden der App und legt ein Transaktionsprotokoll sowie vorherige Programmdateien
unter `.update-<Kennung>/` im Installationsordner ab. Bei einem Startfehler stellt
er die alte Version wieder her. Ein unterbrochener Austausch wird beim erneuten
Aufruf desselben Helfers mit denselben Argumenten vor dem nächsten Versuch repariert.
Lerndatensicherungen liegen im persönlichen Profil unter `Backups`.

## Prüfkommandos

```powershell
.\.venv\Scripts\python.exe selftest.py
.\.venv\Scripts\python.exe -m unittest discover -s installer_tools\tests -v
.\.venv\Scripts\python.exe tests\ui_smoke.py validation\ui-smoke
.\.venv\Scripts\python.exe tests\ui_course.py validation\ui-course
.\.venv\Scripts\python.exe tests\ui_idle.py validation\idle-report.json
.\.venv\Scripts\python.exe tests\ui_reactions.py validation\reactions
.\.venv\Scripts\python.exe tests\ui_updates.py
```

`tests/windows_update_e2e.py` benötigt den erhaltenen 11.0.0-Build unter
`dist/JapanischTrainer`, den neuen Build und das fertige Update-ZIP. Er verwendet
eine Projektkopie und einen lokalen HTTPS-Server mit eigener Test-Zertifizierungsstelle.

Der Installer-Test verwendet dieselbe Inno-Vorlage mit `/DValidationBuild`, einer
separaten App-ID, keiner Uninstall-Registrierung und einer Verknüpfung im Testordner.
So werden Installation, erneutes Einspielen, Verknüpfungsstart und Deinstallation
geprüft, ohne eine persönliche Installation zu verändern. Er ersetzt keinen Test
der unveränderten Produktions-Setup.exe auf einem sauberen Windows-System.

Die ursprünglichen UI-Prüfungen verwenden für Bedienabläufe Audio-Testadapter.
Die echten Modelle werden zusätzlich durch `diagnostics.py` und durch die gebaute
App mit `--diagnostics <Ausgabeordner>` geprüft. Dabei werden japanische Testdateien
erzeugt, aber kein Mikrofon und keine Lautsprecher verwendet.

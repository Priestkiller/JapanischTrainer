"""Summarize actual recorded checks and hash the delivered artifacts."""
import hashlib,json,re,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
release=ROOT/'release'
def digest(path):
    with path.open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()
def report(path):return json.loads((ROOT/path).read_text(encoding='utf-8-sig'))
installer=release/'JapanischTrainer-11.0.1-Setup-x64.exe'
update=release/'JapanischTrainer-11.0.1-Update-x64.zip'
assert report('validation/update-e2e-report.json')['passed']
assert report('validation/installer-test-report.json')['passed']
assert report('validation/frozen-audio/audio-report.json')['passed']
core=(ROOT/'validation/final-core-tests.log').read_text(encoding='utf8')
assert re.search(r'Ran 140 tests',core) and core.rstrip().endswith('OK')
content=f'''# Testbericht – JapanischTrainer 11.0.1

Prüfdatum: 27.09.2026. Ergebnisse wurden unter Windows lokal ausgeführt.
Historische Linux-Berichte aus dem ursprünglichen Archiv sind keine Grundlage
für die folgenden Erfolgsmeldungen.

## Tatsächlich erzeugte Dateien

| Datei | Bytes | SHA-256 |
| --- | ---: | --- |
| {installer.name} | {installer.stat().st_size} | `{digest(installer)}` |
| {update.name} | {update.stat().st_size} | `{digest(update)}` |

Der Windows-Installer ist **nicht Authenticode-signiert**. Es wurde kein
Windows-Signierzertifikat bereitgestellt oder gekauft. Das Update-Manifest
`update.json` besitzt davon unabhängig eine Ed25519-Signatur; der öffentliche
Prüfschlüssel liegt in der App. Private Schlüssel wurden nicht verpackt.

## Umgebung und Ergebnis

Windows x64 10.0.26200.0, Python 3.12.10 x64, Tk/Pillow, PyInstaller 6.22.3,
PowerShell 7.6.5 und Windows PowerShell 5.1, Inno Setup 7. Paketversionen siehe
`requirements-lock.txt`. Kursdaten direkt gezählt: 150 Lektionen, 680 Lernkarten,
564 Sprechziele und acht Lehrer. Vorhandene Kurskennungen bleiben erhalten.

| Prüfung | Tatsächliches Ergebnis |
| --- | --- |
| Unveränderter Ausgangsstand | 123 automatisierte Tests bestanden |
| Endgültiger Quellstand | 140 automatisierte Tests bestanden, davon 17 Update-Tests |
| Installer-Vertragsprüfungen | 20 Prüfungen bestanden |
| Native Oberfläche / Lernablauf | 34 Prüfungen bestanden, mit explizitem Audio-Testadapter |
| Erweiterter Kurs | 22 Prüfungen bestanden; alle 100 neuen Lektionen gerendert |
| Idle / Rückkehr nach Lob | 28 Prüfungen bestanden, alle acht Lehrer |
| Reaktionen / Fehler / Inline-Sprechen | 35 Prüfungen bestanden, alle acht Lehrer |
| Update-Button | Echter Klick in der nativen Oberfläche; Offline-Fehler sichtbar, keine falsche „aktuell“-Meldung |
| Gebaute EXE | Start mit getrenntem Profil aus fremdem Arbeitsverzeichnis; echte App-Renderbilder erzeugt |
| Lokale Sprachmodelle | Echte Inferenz aus Quellcode und gebündelter Windows-EXE erfolgreich |
| Vollständiges Update | Lokaler HTTPS-Download, Signaturprüfung, echter gefrorener Helfer, 11.0.0 → 11.0.1, Starttest und expliziter Neustart erfolgreich |
| Datenerhalt beim Update | XP, Streak, Lehrer, Tempo, Lektionsposition und angefangene Übung erhalten; alle 25 vorhandenen Modelldateien unverändert |
| Fehlerfälle | Fremder Schlüssel, manipulierte Metadaten, beschädigtes ZIP, abgebrochener/unvollständiger Download, falsche Pfade, Offline-Zustand, Downgrade und Fehler beim Start geprüft |
| Wiederherstellung | Simulierter Startfehler stellt alte Dateien wieder her; unterbrochener EXE-Austausch wird vor erneutem Versuch repariert |
| Installer in Testfassung | Installation, Start über erzeugte Verknüpfung, erneutes Einspielen, zwei Sicherungen und Deinstallation erfolgreich; Lernprofil erhalten |
| Paketinhalt | Ressourcen, lokale Modelle, Python/Tk, OpenCV, sherpa-onnx und PortAudio enthalten; persönliche Profile, Aufnahmen und Schlüssel ausgeschlossen |

## Sprachtest: Umfang und Grenzen

Für jeden der acht Lehrer wurde „ありがとうございます。“ mit dem zugeordneten
Sprecherprofil in normalem und langsamem Tempo synthetisiert: 16 echte Ausgaben.
Parakeet erkannte „ありがとうございます“, SenseVoice „ありがとうございます。“.
Eine stille Aufnahme wurde als unzuverlässig abgewiesen. Dieser Test belegt die
lokale Verarbeitung, nicht die allgemeine Erkennungsqualität für Menschen oder
eine korrekte Laut-/Tonhöhenbewertung. Der angezeigte Vergleich bleibt ein Textvergleich.

Im Test waren Python-Socketverbindungen gesperrt; es wurden keine Modelle
nachgeladen. Globale Netzwerk-, Firewall- oder Sicherheitseinstellungen wurden
nicht verändert. Die normalen UI-Audiotests benutzen Testadapter und werden
ausdrücklich nicht als echte Inferenz ausgegeben.

## Installationstest und offene Punkte

Der Installationstest nutzt **dieselbe Inno-Vorlage und dieselben Programmdateien**
mit `ValidationBuild`: eigene App-ID, keine Uninstall-Registrierung, Verknüpfung
im Projekt-Testordner und ein separates Lernprofil. Der Standard-Startmenüpfad,
Desktop-Verknüpfung und produktive Registry-Eintrag wurden dadurch nicht auf dem
persönlichen System installiert. Die unveränderte Produktions-Setup.exe wurde
kompiliert und gehasht, aber nicht in eine vorhandene persönliche Installation eingespielt.

Ein Zwischenlauf mit Windows PowerShell 5.1 erzeugte das künstliche Testprofil
mit UTF-8-BOM; die App behandelte diese Datei als ungültig und sicherte sie.
Der Testschreiber wurde auf das BOM-freie UTF-8-Format der App korrigiert und
der vollständige Installationstest erneut ausgeführt. Die App-Dateien wurden
wegen dieses Testaufbaufehlers nicht geändert.

Ein frisches Windows-System ohne vorhandenes Python war nicht verfügbar;
Windows Sandbox ist hier nicht installiert. Ein Saubersystemtest bleibt offen.
Automatisiert geprüft wurden Fenstergrößen bis 1920×1080 und appinterne Skalierung
bis 110 %. Separate Windows-DPI-Einstellungen wurden nicht systemweit umgestellt.

Mikrofonaufnahmen und manuelles Abhören wurden **nicht ausgeführt**. Für die
Abnahme am eigenen Gerät:

1. Setup öffnen, App starten, Lehrer wählen und normale/langsame Stimmprobe hören.
2. Eine Lernkarte öffnen, „Jetzt sprechen“ wählen und bewusst Mikrofonzugriff erlauben.
3. Wort sprechen, Aufnahme beenden; Textvergleich und Fehlerhinweise prüfen.
4. Bei leerer/schlechter Aufnahme darf kein fiktiver Lernerfolg entstehen.

Die ursprünglichen Desktop-Screenshots konnten durch andere Fenster verdeckt
sein und werden nicht als Beleg oder öffentliches Material verwendet. Die neuen
Renderbilder stammen direkt aus der tatsächlich laufenden App mit Testprofil.

## Modelle und Lizenzen

Die vorhandenen Modellgewichte wurden wiederverwendet. Die Modelle konnten
erfolgreich geladen werden; Prüfsummen der ausgelieferten Dateien sind im
Installationsmanifest erfasst. Ein bitweiser Vergleich sämtlicher lokaler Gewichte
mit frisch heruntergeladenen Originalarchiven wurde nicht zusätzlich durchgeführt.

- [Supertonic 3](https://huggingface.co/Supertone/supertonic-3/blob/main/LICENSE):
  BigScience Open RAIL-M für Modellgewichte; Originaltext und Nutzungsbedingungen beigelegt.
- [Parakeet JA](https://huggingface.co/nvidia/parakeet-tdt_ctc-0.6b-ja): CC BY 4.0,
  NVIDIA-Attribution und Konvertierungshinweis beigelegt.
- [SenseVoiceSmall / FunASR](https://github.com/modelscope/FunASR/blob/main/MODEL_LICENSE):
  Modelllizenz und Attribution beigelegt.
- Programmquellcode unter GPL-3.0-or-later mit Zustimmung des Nutzers;
  Originalquellcode von pykakasi 2.3.0 und dessen Lizenz im Quellpaket.

## Updates und Nachweise

Öffentliches Projekt: https://github.com/Priestkiller/JapanischTrainer
Der vorhandene Discord-Dienst wurde nicht geändert. Für 11.0.0 ohne Update-Button
ist einmalig das neue Setup erforderlich; weitere Programmupdates laufen über
den Button. Bei geänderten Modellgewichten benötigt diese Version das volle Setup.

Lokale Rohprotokolle und Testprofile liegen unter `validation/`, Build-Protokolle
zusätzlich unter `installer_tools/Protokolle/`. Diese Verzeichnisse werden nicht
veröffentlicht. Der isolierte Installer-Test und der lokale HTTPS-Test protokollieren
ihre Ergebnisse als JSON. Private Lernstände wurden weder gelesen noch verpackt.
'''
(ROOT/'TESTBERICHT.md').write_text(content,encoding='utf8')
(release/'TESTBERICHT.md').write_text(content,encoding='utf8')
shutil.copy2(ROOT/'BUILD_ANLEITUNG.md',release/'BUILD_ANLEITUNG.md')
print('Berichte mit tatsächlichen Dateigrößen und SHA-256 erstellt.')

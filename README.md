> Aktuell: [Windows 11.0.2](https://github.com/Priestkiller/JapanischTrainer/releases/tag/v11.0.2) und [Android 11.0.2-android.1](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-v11.0.2-1). 30 Einstiegslektionen vertieft; [Änderungen](RELEASE_NOTES_11.0.2.md), [Prüfungen](TESTBERICHT_11.0.2.md).

# JapanischTrainer

Deutschsprachiger Offline-Lerntrainer für Windows 10/11 x64 und Android,
mit acht Lehrern, 150 Lektionen, 680 Lernkarten und lokalen Sprachmodellen.

## Download

[Aktuelle Windows-Version und Setup herunterladen](https://github.com/Priestkiller/JapanischTrainer/releases/latest).
Für die erste Installation die **Setup-x64.exe** verwenden. Sie enthält die Laufzeit
und Sprachmodelle; Python oder Entwicklungswerkzeuge sind nicht erforderlich.

Ab 11.0.1: **Einstellungen → Programm-Updates → Nach Updates suchen**.
Die App lädt signierte Updates, speichert den Lernstand und startet nach dem
Einspielen neu. Unveränderte Sprachmodelle bleiben auf dem Rechner.
Der Windows-Installer hat kein Authenticode-Zertifikat; die Update-Metadaten
werden separat mit Ed25519 signiert und in der App geprüft.

### Android

[Android-APK und Installationshilfe](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-v11.0.1-3)
für Android 9+ mit ARM64, darunter das Samsung Galaxy S24 Ultra. Die erste
Android-Version wird als Vorschau veröffentlicht. Sie hat eine eigene
Handy-Oberfläche mit Navigation am unteren Rand, großen Bedienelementen,
Hoch-/Querformat und denselben Kursdaten wie Windows.

Jede Karte startet mit Hören und Sprechen (1/6). Danach folgen fünf weitere
Übungen, jeweils erst nach erfolgreichem Abschluss des vorherigen Schritts.
Die vollständige Lösungskarte erscheint nur im ersten Schritt.

APK installieren und einmalig in den Einstellungen das Sprachpaket laden
(ca. 284 MB). Danach sind Lehrer-Stimmen und Spracherkennung offline verfügbar.
Der Update-Button erhält Lernstände und Sprachpaket. Details:
[Android-Anleitung](mobile/INSTALLIEREN_ANDROID.md) und
[Android-Technik und Build](mobile/README.md).

## Lernen und Datenschutz

Lernen, Sprachausgabe und Erkennung arbeiten lokal. Die manuelle Update-Prüfung
verbindet sich mit GitHub; Mikrofonaufnahmen werden dabei nicht übertragen.
Unter Windows liegen Lernstand und Einstellungen unter `%APPDATA%\JapanischTrainer` und bleiben
bei Updates und Deinstallation erhalten.
Android speichert sie im privaten App-Speicher; vor einer Android-Deinstallation
den Lernstand exportieren. Windows-JSON-Exporte lassen sich am Handy importieren.

Die Sprachauswertung vergleicht den erkannten Text mit der Zielaussage. Sie ist
keine Bewertung einzelner Laute oder des Tonhöhenakzents. Der Kurs ist keine
JLPT-/GER-Zertifizierung und kein vollständiger N1-Kurs.

## Entwicklung

Siehe [BUILD_ANLEITUNG.md](BUILD_ANLEITUNG.md) und [TESTBERICHT.md](TESTBERICHT.md).
Mitgeliefert werden Quellcode, Grafiken, Kursdaten, Tests, Build-Skripte und
festgehaltene Abhängigkeiten. Die großen Modellgewichte sind in der Setup-Datei,
nicht im Git-Repository. Downloadquellen stehen in `download_models.ps1`.

Programmquellcode: **GPL-3.0-or-later**, siehe [LICENSE.txt](LICENSE.txt).
Sprachmodelle sind separat lizenziert; deren Originaltexte und Attributionen
stehen in `MODEL_LICENSES.txt`, `MODEL_ATTRIBUTION.txt` und `licenses/`.
Das Paket `vendor-sources/` enthält den Originalquellcode von pykakasi 2.3.0.

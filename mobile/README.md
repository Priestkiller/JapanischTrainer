# JapanischTrainer für Android

Android 9 oder neuer auf einem Gerät mit ARM64-Prozessor. Der Android-Port nutzt
die gleichen 150 Lektionen, 680 Karten, acht Lehrerbilder und stabilen Kurskennungen
wie die Windows-Version. Die Oberfläche passt sich Hochformat, Querformat und
Tablets an. Der Lernablauf umfasst sechs Schritte pro Karte und eine Abschlussrunde.

## Installation und Offline-Sprache

Die signierte APK wird separat unter `android-v11.0.1-1` veröffentlicht; Windows
behält seinen bestehenden Update-Kanal. Android fragt beim ersten APK-Download
nach der Freigabe zur Installation aus der jeweiligen Download-App.

Unter **Einstellungen → Offline-Stimmen & Sprechen** lässt sich das einmalige
Sprachpaket laden (284.336.522 Bytes). Danach laufen die originalen Supertonic-
Lehrer-Stimmen und SenseVoice-Erkennung lokal. Für die Handyversion wird die
kleinere, bereits in Windows enthaltene SenseVoice-Engine verwendet; das große
Parakeet-Modell wird nicht zusätzlich benötigt. Mikrofonaufnahmen bleiben im
Arbeitsspeicher und werden nicht hochgeladen oder als Audiodateien gespeichert.
Das Paket wird über HTTPS geladen und mit den in der APK festgelegten SHA-256-
Prüfsummen kontrolliert. Modellbedingungen sind vor dem Download in der App lesbar.

Die textbasierte Lernfunktion funktioniert auch vor dem Sprachpaket-Download.
„Ohne Ton üben“ wird nicht als bestandene Hörübung gewertet. Der Sprachvergleich
bewertet erkannten Text, keine Einzellaute oder Tonhöhen. Kurze Kana können von
Spracherkennung unzuverlässig erkannt werden. Stimmen und Erkennung werden
abwechselnd geladen, damit nicht beide Modelle gleichzeitig RAM belegen.

## Lernstände und Updates

Ein App-Update erhält den lokalen Lernstand und das bereits geladene Sprachpaket.
Die Update-Prüfung filtert ausschließlich Android-Releases. Vor Installation
werden Paketname, höhere Versionsnummer, SHA-256 und die Übereinstimmung des
Android-Signierzertifikats geprüft. Android verlangt eine bewusste Bestätigung.

**Eine Deinstallation löscht Android-App-Daten.** Vorher über Einstellungen
exportieren. Windows-JSON-Exporte lassen sich importieren; eine vorhandene
Handy-Datei wird vor dem Ersetzen intern gesichert. Es gibt keinen Cloud-Sync.

## Entwicklung

Der lokale Inhalt liegt in `web/`, die Android-Schicht in `app/`. WebView lädt
ausschließlich gebündelte App-Inhalte über `WebViewAssetLoader`; externe Seiten,
Frames und Dateizugriffe werden gesperrt. Der Lernstand wird nativ mit `AtomicFile`
geschrieben. Die Android-Schicht verwaltet Mikrofon, lokale Modelle, Datei-Dialoge
und den Android-Paketinstaller.

Benötigt: JDK 17, Gradle 8.11.1, Android SDK 35, Python mit Pillow 12.3.0, Node 22+.
Im Repository-Stamm:

```sh
python mobile/tools/prepare_assets.py --download-library
node --test mobile/tests/core.test.mjs
cd mobile
gradle :app:assembleRelease :app:lintRelease
gradle :app:connectedDebugAndroidTest
```

Der CI-Workflow `.github/workflows/android.yml` baut die APK und führt echte
Android-Instrumentierung in einem Emulator aus. Die Sprachdiagnose verwendet
synthetische japanische Sprache, kein Mikrofon und keine Lautsprecher.
Der Build erzeugt zunächst eine **unsignierte** Release-APK. Der private
Herausgeberschlüssel bleibt ausschließlich lokal und wird nicht in CI hochgeladen.
Ein Signierschlüssel muss für künftige Updates dauerhaft erhalten bleiben.

Zum Signieren unter Windows dient `tools/Sign-Android.ps1` mit JDK 17 und den
Android Build-Tools 35. Der lokal erzeugte Schlüssel und seine Passwortdatei liegen
im ignorierten Verzeichnis `mobile/.keys/`. Beide müssen gemeinsam sicher gesichert
werden. Nicht veröffentlichen, nicht in CI hochladen und für Updates nicht ersetzen.
Der öffentliche SHA-256-Zertifikatsfingerabdruck dieser Android-Ausgabe lautet
`3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9`.

`tools/package_release.py --apk <signierte-APK> --commit <Quellcommit>` erzeugt
APK-Paket, Git-Quellarchiv, Anleitung, Prüfbericht, Update-Metadaten und Prüfsummen
unter `mobile/release/`. Für eine neue Version müssen Android-`versionCode`,
`versionName`, `android-version.json` und die Release-Adresse gemeinsam erhöht
werden. Android-Releases heißen `android-v…`, bleiben außerhalb von GitHubs
Windows-`latest` und enthalten `android-update.json`. Das Sprachpaket liegt
unabhängig davon unter `android-models-v1` und wird bei App-Updates weiterverwendet.

Die Animation nutzt vorhandene geschlossene Mund- und Blinkbilder mit sanfter
Bewegung. Die aufwendige Windows-Verformung mit OpenCV wird nicht auf dem Handy
ausgeführt. Android-Schriftgröße, geringe Bewegungspräferenz und Bildschirmausschnitte
werden berücksichtigt. Ein echter Gerätetest bleibt zusätzlich zum Emulator nötig.

## Quellen

- [Android: lokaler WebView-Inhalt](https://developer.android.com/develop/ui/views/layout/webapps/load-local-content)
- [Android: App signieren](https://developer.android.com/studio/publish/app-signing)
- [sherpa-onnx 1.13.8](https://github.com/k2-fsa/sherpa-onnx/releases/tag/v1.13.8), Android-AAR SHA-256 `633c24321e06b1fe79feafa03ea16cbc0f8a286641e2da3559bac91bdb13bd96`
- [Supertonic-API](https://k2-fsa.github.io/sherpa/onnx/tts/supertonic.html)

Programmquellcode GPL-3.0-or-later. Modellbedingungen und Drittanbieter-Lizenzen
stehen im Hauptprojekt und sind in der Android-App enthalten.

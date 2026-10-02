# JapanischTrainer für Android

Android 9 oder neuer auf einem Gerät mit ARM64-Prozessor. Der Android-Port nutzt
die gleichen 150 Lektionen, 680 Karten, acht Lehrerbilder und stabilen Kurskennungen
wie die Windows-Version. Die Oberfläche passt sich Hochformat, Querformat und
Tablets an. Der Lernablauf umfasst sechs Schritte pro Karte und eine Abschlussrunde.

## Installation und Offline-Sprache

Die signierte APK wird separat unter `android-v11.0.1-3` veröffentlicht; Windows
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

Der Lektionsablauf beginnt mit **1/6 Hören & Sprechen**. Nach einer vollständig
abgespielten Vorlage und erfolgreicher Sprechübung wird **2/6 Bedeutung** frei.
Normalerweise erfordert das einen passenden erkannten Text; für kurze Kana gilt
die unten beschriebene Selbstprüfung. Danach folgen **3/6 Hörverstehen**, **4/6 Bausteine**, **5/6 Schreiben** und
**6/6 Anwenden**. Die vollständige Vorlage und das Mikrofon erscheinen nur im
ersten Schritt. Spätere Aufgaben zeigen nur die nötige Frage; Erklärungen mit
Lösungen bleiben in bewusst aufrufbaren Hilfen verborgen; Hilfe allein gibt nichts frei.

Für diesen Ablauf ist das Sprachpaket erforderlich. Fehlende Wiedergabe,
fehlgeschlagene Aufnahmen und bloßes Überspringen geben keinen Folgeschritt frei.
Nach einer echten falschen Antwort kannst du erneut antworten oder die Aufgabe
mit „Weiter · am Ende wiederholen“ vormerken. Am Ende folgt dieselbe Aufgabe
in einer Fehlerwiederholung. Erst nach deren Lösung und der Abschlussrunde
wird die Lektion abgeschlossen. Nach drei erfolglosen Sprechversuchen bleibt
„Antwort stattdessen auswählen“ fest unten erreichbar; die Auswahl erfordert
eine passende Antwort und ausdrückliche Bestätigung. Freiwilliges Sprechen
wird dabei separat für später gespeichert. Kursübersicht und Nachschlagewerk bleiben ohne Modelle nutzbar.
Erfolge und Voraussetzungen werden je Karte gespeichert und beim Fortsetzen
geprüft. Bei älteren Lernständen beginnt nur die noch angefangene Karte mit dem
neuen ersten Schritt; abgeschlossene Lektionen, XP und Abschlussrunden bleiben
erhalten. Der Sprachvergleich
bewertet erkannten Text, keine Einzellaute oder Tonhöhen. Kurze Kana können von
Spracherkennung unzuverlässig erkannt werden. Nur bei einzelnen Kana (einschließlich
Kombinationen wie きゃ) kann deshalb nach einer Aufnahme mit erkanntem Sprachinhalt
eine ausdrücklich gekennzeichnete Selbstprüfung den Sprechschritt abschließen.
Sie wird separat gespeichert und verbessert nicht den automatischen Textvergleich.
Wörter und Sätze werden weiterhin automatisch geprüft. Stille, Aufnahmefehler und
fehlende Mikrofonfreigabe öffnen diese Möglichkeit nicht. Stimmen und Erkennung werden
abwechselnd geladen, damit nicht beide Modelle gleichzeitig RAM belegen.

## Lernstände und Updates

Unter **Üben → Gespräche üben** stehen fünf geführte Offline-Gespräche bereit:
Kennenlernen, Café, Einkaufen, Wegfragen und Wochenendpläne. Der gewählte Lehrer
spricht die japanischen Beiträge mit seiner vorhandenen Stimme. Antworten können
aufgenommen oder getippt werden. Erkannter Text wird vor dem Senden angezeigt
und kann berichtigt werden. Je nach Antwort folgt ein anderer vorbereiteter
Gesprächsweg; offene Themen und frei erzeugte KI-Antworten werden nicht angeboten.
Übersetzung, Lesung, langsame Wiederholung und Antwortideen sind zuschaltbar.

Die Szenen laufen mit dem vorhandenen Sprachpaket ohne Anbieterzugang oder
zusätzliche Modelle. Textverläufe (höchstens 40 Beiträge je Szene), Entwürfe und
Gesprächspositionen bleiben lokal im Lernstand und werden mit einer JSON-Sicherung
exportiert. Audiodaten bleiben im Arbeitsspeicher. Gespräche haben eigene
Abschlusszähler und überspringen keine Kurslektionen oder XP-Voraussetzungen.

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
node --test mobile/tests/core.test.mjs mobile/tests/talk.test.mjs
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

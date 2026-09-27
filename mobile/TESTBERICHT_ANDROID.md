# Android-Prüfbericht – JapanischTrainer 11.0.1-android.2

Datum: 27.09.2026. Paket `de.priestkiller.japanischtrainer`, VersionCode 11000102.
Zielgerät des Nutzers: Samsung Galaxy S24 Ultra. Die Vorgängerversion wurde vom
Nutzer dort installiert; diese Aktualisierung wurde nicht auf seinem Gerät getestet.

## Build und Nachweis

- APK-Quellcommit: `929b78b39af693957fa0981fa0d15a6f951200b6`.
- [Android-Build und Emulatorlauf](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36322474243).
- Release-/Debug-APK, Android-Lint, 14 Verhaltenstests und beide Android-
  Instrumentierungstests erfolgreich; der oben verlinkte Build ist grün.
- JDK 17, Gradle 8.11.1, Android Gradle Plugin 8.9.3, Kotlin 2.1.20,
  compile/target SDK 35; Minimum Android 9/API 28.
- ARM64- und x86_64-Bibliotheken; ARM64-Bibliotheken mit 16-KB-ELF-Segmentausrichtung.
- Die finale APK wird lokal mit dem bestehenden Schlüssel signiert und mit
  `apksigner verify --verbose --print-certs` und `zipalign -c -P 16 4` geprüft.
- Zertifikat SHA-256:
  `3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9`.
- Exakte Größe, SHA-256 und Quellarchiv-Commit stehen in `android-update.json`.
  `SHA256SUMS-Android.txt` erfasst APK, Quellen, Anleitung und Testnachweise.

## Lernlogik – 14 bestandene Verhaltenstests

Der Ablauf ist Hören & Sprechen (1/6), Bedeutung erkennen (2/6), Hörverstehen
(3/6), Bausteine ordnen (4/6), selbst Schreiben (5/6), Anwenden (6/6).

- Alle 150 Lektionen und 680 Karten bleiben unter ihren bisherigen Kennungen
  erhalten. XP werden erst nach allen Karten und der Abschlussrunde vergeben,
  für dieselbe Lektion nur einmal.
- Vor dem Sprechversuch muss die Vorlage vollständig abgespielt worden sein.
  Falsche Antworten, fehlendes Audio und Überspringen öffnen keinen Folgeschritt.
- Erfolgreiche Schritte bleiben über einen Neustart erhalten. Gespeicherte
  Voraussetzungen müssen eine vollständige Folge bilden; eine manipulierte
  spätere Phase allein umgeht den Ablauf nicht.
- Alte Lernstände behalten XP, Lehrer, abgeschlossene Lektionen und Kartenposition.
  Nur eine noch offene Karte beginnt einmalig mit dem neuen Sprechschritt.
- Die Selbstprüfung ist auf kurze Kana begrenzt und setzt ein nicht leeres
  Erkennungsergebnis voraus. Sie zählt separat; ein fehlgeschlagener automatischer
  Textvergleich bleibt bei 0. Wörter und Sätze erlauben diese Bestätigung nicht.
  Eine noch unbestätigte Selbstprüfung wird nach einem Neustart nicht angeboten,
  ohne erneut aufzunehmen.
- Romaji-Längen, zulässige Schreibweisen, leere/falsche Erkennung, Export/Import,
  japanische Suche, Wiederholungsplanung, Lernserie und Speicherfehler sind geprüft.

## Oberfläche – sieben bestandene Größenprüfungen

Isolierter Edge-Browser mit Playwright, Touch-Viewports:
320×640, 360×800, 390×844, 412×892, 412×915, 844×390 und 768×1024 CSS-Pixel.
412×892 prüft ein passendes Handyformat; Android-Zoom und Systemleisten können
die tatsächlich nutzbare Größe auf dem S24 Ultra verändern.

In jeder Größe wird die vollständige Sechs-Schritte-Folge durchlaufen und die
nächste Karte bei 1/6 geprüft. Falsche Antworten bleiben gesperrt, Hörfragen
erfordern vorheriges Audio, spätere Aufgaben zeigen weder Lösungskarte noch
Mikrofon. Auch ein verspätetes Sprachergebnis löst keine spätere Aufgabe.
Fortsetzen nach Neuladen, Kana-Selbstprüfung, Schreibprüfung, Lehrerwahl,
japanische Suche, Lizenzdialog, Touch-Flächen und horizontale Überbreite sind geprüft.

Diese Browserprüfungen verwenden ausdrücklich simulierte native Audioereignisse.
Sie prüfen die Bedienlogik, keine echte Aufnahme oder Sprachausgabe.

## Echter Android-Emulator – zwei Instrumentierungstests

Android 15/API 35, Google APIs, Pixel-5-Profil, x86_64, 4 GB RAM.

- Die native Activity lädt die gebündelte WebView. Schritt 1 ist zunächst
  gesperrt. Eine ausdrücklich gesetzte Test-Lernstanddatei mit bestandenem
  Sprechschritt bleibt nach Activity-Neustart bei 2/6; dort fehlen Mikrofon und
  vorgegebene Lesung. Das ist ein Persistenztest, keine simulierte Mikrofonprüfung.
  Einstellungen, 150 % WebView-Textgröße und Querformat sind ebenfalls geprüft.
- Das öffentliche Sprachpaket wird geladen und gegen festgelegte Prüfsummen
  geprüft. Die echten nativen Modelle erzeugen für acht Lehrer je normale und
  langsame Sprache (16 Ausgaben). Die langsamen Ausgaben sind länger. SenseVoice
  erkennt aus synthetischer japanischer Sprache den erwarteten „ありがとう“-Text.
  Mikrofon und Lautsprecher werden hierfür nicht verwendet.

Fünf Screenshots sichern Startseite, Sprechschritt, Bedeutungsfrage, große Schrift
und Querformat. Sie warten auf den WebView-Zeichenabschluss bzw. den tatsächlichen
Orientierungswechsel und werden vor dem Aufräumen der Testinstallation gesichert.

## Zusätzliche Prüfung kurzer Kana mit echten Modellen

Unter Windows wurden die vorhandenen Supertonic-/SenseVoice-Modelle direkt mit
synthetischer Sprache geprüft, ohne Mikrofon oder Lautsprecher. Dabei wurde etwa
„い“ als „いい？“ und „う“ als „うん。“ erkannt; „こんにちは“ und
„ありがとうございます“ wurden passend verschriftlicht. Das ist kein Nachweis
für alle Stimmen oder reale Sprecher. Es erklärt die ausdrücklich freigegebene
Selbstprüfung für kurze Kana nach einer Aufnahme mit erkanntem Sprachinhalt.
Der automatische Vergleich wird dadurch nicht künstlich als bestanden gewertet.

## Update und Grenzen der Prüfung

- Paketname und Herausgeberschlüssel bleiben gleich; VersionCode steigt von
  11000101 auf 11000102. Android-Lernstand und vorhandenes Sprachpaket bleiben
  bei einer normalen Aktualisierung erhalten. Vorher nicht deinstallieren.
- Die Instrumentierung verwendet den Debug-Build mit denselben App-Quellen und
  Assets. Die finale signierte APK wird zusätzlich als Paket und kryptografisch
  geprüft. Der Android-Paketinstaller auf dem physischen S24 Ultra ist nicht
  automatisiert durchlaufen worden.
- Keine echte Mikrofonaufnahme, manuelle Hörbewertung oder Bluetooth-Prüfung;
  keine phonetische Aussprachebewertung. Aufnahme, Hörbarkeit, Samsung One UI und
  ein zusätzlicher Test im Flugmodus bleiben dem echten Gerätetest vorbehalten.
- Android 9 bis 14 wurden nicht zusätzlich auf Geräten geprüft. Der Emulator
  prüft Android 15; die Bibliotheken unterstützen ARM64 und x86_64.
- Android verwendet einen eigenen Update-Kanal. Windows `v11.0.1` bleibt „Latest“.

Die verbleibenden kurzen Geräteprüfungen stehen in `INSTALLIEREN_ANDROID.md`.

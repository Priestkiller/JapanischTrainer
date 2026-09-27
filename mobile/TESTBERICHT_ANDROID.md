# Android-Prüfbericht – JapanischTrainer 11.0.1-android.3

Datum: 27.09.2026. Paket `de.priestkiller.japanischtrainer`, VersionCode 11000103.
Zielgerät des Nutzers: Samsung Galaxy S24 Ultra. Diese Aktualisierung wurde
nicht auf seinem physischen Gerät getestet.

## Build und Paketprüfung

- APK-Build-Quellcommit: `d1e990b2569934eabd01abf486be464dc159df19`.
- [Erfolgreicher Build und Android-Emulatorlauf](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36324820475).
- Release-/Debug-APK, Android-Lint, 25 Verhaltenstests und alle drei Android-
  Instrumentierungstests erfolgreich.
- Finale Nachweise stammen aus Versuch 2 desselben Builds. Im ersten Versuch
  verdeckte ein Pixel-Launcher-Fehler des Emulators die Screenshots. Der frische
  Wiederholungslauf zeigt die App ohne diesen Dialog; die APK beider Läufe ist
  bytegleich. Die verdeckten Bilder werden nicht als Release-Nachweise verwendet.

- JDK 17, Gradle 8.11.1, Android Gradle Plugin 8.9.3, Kotlin 2.1.20,
  compile/target SDK 35; Minimum Android 9/API 28.
- ARM64- und x86_64-Bibliotheken; ARM64 mit 16-KB-ELF-Segmentausrichtung.
- Signierung mit demselben lokalen Herausgeberschlüssel wie die Vorgänger;
  Kontrolle mit `apksigner verify --verbose --print-certs` und `zipalign -c -P 16 4`.
- Zertifikat SHA-256:
  `3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9`.
- Größe, SHA-256 und exakter Quellarchiv-Commit stehen in `android-update.json`.
  `SHA256SUMS-Android.txt` erfasst APK, GPL-Quellen, Anleitung und Testnachweise.

## Lernlogik und Gespräche – 25 bestandene Verhaltenstests

Die 14 bisherigen Tests prüfen weiterhin Kursdaten, alle sechs Lernschritte,
Freischaltung nach Erfolg, Kana-Selbstprüfung, Vokallängen, Fortsetzen, alte
Lernstände, Export/Import, Suche, Wiederholungen, Lernserie und Speicherfehler.
Alle 150 Lektionen und 680 Karten behalten ihre Kennungen; Gespräche ändern
weder XP noch Freischaltungen der Kurslektionen.

Elf zusätzliche Tests prüfen:

1. Alle fünf Szenen, alle Knoten, Antwortwege und eingeblendeten Antwortideen
   sind erreichbar und führen zu einer gültigen vorbereiteten Reaktion.
2. Die Getränkeauswahl verändert den Café-Verlauf; Wasser überspringt die Frage
   nach Temperatur und Größe. Auswahl und ursprünglicher Lehrer bleiben gespeichert.
3. Wochenendpläne übernehmen Tag, Zeit und den alternativ gewählten Treffpunkt
   in die abschließende japanische Antwort.
4. Eine höfliche Kaufabsage schließt den entsprechenden Gesprächsweg erfolgreich ab.
5. Leere, unbekannte und negative Bestellantworten erzeugen keine erfundene Bestellung.
6. Eine Bitte um Wiederholung bleibt bei derselben Frage und zählt nicht als
   erfolgreicher Abschluss einer Antwort.
7. Erkannte Entwürfe bleiben erhalten. Eine getippte Korrektur wird als Text
   gespeichert; sie wird nicht als unverändert gesprochene Antwort dargestellt.
8. Erneutes Laden oder Senden nach Abschluss vergibt keinen zweiten Abschluss.
9. Jede Szene behält ihren eigenen angefangenen Verlauf.
10. Importierte Zustände werden anhand der akzeptierten Antworten rekonstruiert;
    gefälschte Auswahlwerte oder ein Sprung zu einem späteren Knoten reichen nicht.
11. Verlauf und Eingabe sind begrenzt; ältere Profile ohne Gesprächsdaten funktionieren.

## Oberfläche – sieben bestandene Größenprüfungen

Isolierter Edge-Browser mit Playwright, Touch-Viewports:
320×640, 360×800, 390×844, 412×892, 412×915, 844×390 und 768×1024 CSS-Pixel.
Die effektive S24-Ultra-Größe hängt zusätzlich von Android-Zoom und Systemleisten ab.

In allen Größen: vollständiger Sechs-Schritte-Lernablauf, Lehrerwechsel, Suche,
Lizenzdialog, Gesprächsauswahl, Café-Verzweigung, Übersetzung, Lesung und Abschluss.
Geprüft sind außerdem abgelehnte Mikrofonfreigabe, Textkorrektur vor dem Senden,
Speichern eines erkannten Entwurfs, Neustart, Szenenwechsel während einer Aufnahme
und das Ignorieren ihres verspäteten Ergebnisses. Die gewählte Stimme wird verwendet.
Keine horizontale Überbreite, keine JavaScript-Seitenfehler; Touch-Flächen erfüllen
die festgelegten Mindestmaße. Der Gesprächsverlauf besitzt einen eigenen Scrollbereich.

Die Browser-Audiotests verwenden ausdrücklich simulierte native Ereignisse.
Sie prüfen die Bedienlogik, keine echte Aufnahme, Aussprache oder Hörbarkeit.

## Android-Emulator – drei Instrumentierungstests

Android 15/API 35, Google APIs, Pixel-5-Profil, x86_64, 4 GB RAM.

- Native WebView, zunächst gesperrter Sprechschritt und Fortsetzen bei 2/6 anhand
  einer ausdrücklich gespeicherten Test-Voraussetzung. Einstellungen, 150 %
  WebView-Textgröße und Querformat werden geprüft.
- Neuer Gesprächsbereich: Café-Bestellung per Texteingabe, passende Rückfrage,
  Übersetzung und Lesung sowie Erhalt von Getränk und Antwortentwurf nach
  Activity-Neustart. Dies ist ein nativer UI-/Persistenztest, kein Mikrofontest.
- Das echte öffentliche Sprachpaket wird gegen seine Prüfsummen geprüft.
  Supertonic erzeugt für acht Lehrer je normale und langsame Sprache (16 Ausgaben).
  Die langsamen Ausgaben sind länger. SenseVoice erkennt den erwarteten
  „ありがとう“-Text aus der synthetischen Ausgabe, ohne Mikrofon oder Lautsprecher.

Sieben Emulator-Screenshots zeigen Startseite, Lernschritte 1 und 2,
Gesprächsauswahl, Café, große Schrift und Querformat. Die Bildaufnahme wartet
auf den WebView-Zeichenabschluss bzw. den tatsächlichen Orientierungswechsel.

## Zusätzlicher Sprachmodelltest mit Gesprächsantworten

Unter Windows wurden 18 typische Antworten aus allen fünf Szenen mit den
vorhandenen Supertonic-/SenseVoice-Modellen geprüft. Sakura-Stimme, synthetische
Sprache, kein Mikrofon/Lautsprecher. 16 Antworten wurden so erkannt, dass sie
unverändert zum vorbereiteten Antwortweg passten. Bei zwei Antworten gingen
Wörter verloren: „すみません、やめておきます。“ wurde zu „すみません やめ てます。“,
„歩いて何分ですか。“ zu „歩いて何分です。“. Beide benötigen eine Textkorrektur;
sie werden nicht künstlich als korrekt eingestuft. Ergebnisse liegen den
Testnachweisen bei. Dies beweist keine Erkennungsquote für reale Sprecher.

## Update, Datenschutz und Grenzen

- VersionCode steigt auf 11000103; Paketname, Schlüssel und Sprachpaket bleiben
  gleich. Eine normale Aktualisierung erhält Lernstand und Modelle. Nicht deinstallieren.
- Die Android-Instrumentierung verwendet den Debug-Build mit denselben Quellen
  und Assets. Die signierte Release-APK wird zusätzlich als Paket und kryptografisch
  geprüft. Der Installer auf einem physischen S24 Ultra wurde nicht automatisiert bedient.
- Mikrofonaufnahmen bleiben im Arbeitsspeicher. Der letzte Textverlauf je Szene,
  Entwürfe und Gesprächspositionen bleiben lokal und sind in Lernstand-Exporten enthalten.
- Die Dialoge sind vorbereitete Offline-Szenen mit verschiedenen Antwortwegen.
  Es gibt keine Online-KI, keine frei generierten Antworten, keinen Anbieterzugang
  und keinen weiteren Modelldownload. Passende Formulierungen außerhalb der
  erfassten Varianten können trotzdem eine Korrektur oder Antwortidee erfordern.
- Keine echte Mikrofon-, manuelle Hör- oder Bluetooth-Prüfung dieser Version;
  keine phonetische Aussprachebewertung. Samsung One UI und echter Flugmodus
  bleiben ergänzende Gerätetests. Android 9 bis 14 wurden nicht separat geprüft.
- Android hat einen eigenen Update-Kanal. Windows `v11.0.1` bleibt „Latest“.

Bedienung und verbleibende Geräteprüfungen stehen in `INSTALLIEREN_ANDROID.md`.

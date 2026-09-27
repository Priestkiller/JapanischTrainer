# Android-Prüfbericht – JapanischTrainer 11.0.1-android.1

Datum: 27.09.2026. Paket `de.priestkiller.japanischtrainer`, VersionCode 11000101.
Gewünschtes Zielgerät: Samsung Galaxy S24 Ultra. Kein physisches S24 Ultra war
für diese Prüfung verbunden. Diese erste Android-Ausgabe ist eine Vorschau.

## Build und Nachweis

- APK-Build aus Commit `b5225e580c3bf61e179248819c9529e3c6db80f0`.
- [GitHub-Build mit Android-Instrumentierung und Screenshots](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36319598975).
- JDK 17, Gradle 8.11.1, Android Gradle Plugin 8.9.3, Kotlin 2.1.20,
  compile/target SDK 35; Minimum Android 9/API 28.
- ARM64- und x86_64-Bibliotheken. Die enthaltenen ARM64-Bibliotheken besitzen
  16-KB-ELF-Segmentausrichtung. Die fertige APK wird zusätzlich mit
  `zipalign -c -P 16 4` geprüft.
- Release- und Debug-APK kompiliert, `lintRelease` erfolgreich.
- Lokal signierte Release-APK, APK Signature Scheme v3. `apksigner verify
  --verbose --print-certs` prüft den fertigen Download.
- Zertifikat SHA-256:
  `3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9`.
- APK-Prüfsumme und exakte Dateigröße stehen in `android-update.json`;
  `SHA256SUMS-Android.txt` erfasst auch das passende Git-Quellarchiv.

## Lernlogik – neun bestandene Verhaltenstests

1. Vollständiger Originalkurs: 150 Lektionen, 680 Karten, stabile Kennungen.
2. Windows-Profil übernimmt XP, Lehrer und die angefangene Schreibaufgabe.
3. Alle sechs Lernschritte und die Abschlussrunde sind für den Abschluss nötig;
   XP werden für dieselbe Lektion nur einmal vergeben.
4. Falsche Antworten lassen die Aufgabe offen; übersprungene Hörübungen werden
   nicht als erfolgreiche Hörleistung gespeichert.
5. Romaji berücksichtigt Vokallänge und erlaubte Schreibweisen.
6. Leeres oder falsches Erkennungsergebnis erzeugt keinen erfolgreichen Vergleich.
7. Profil-Export/Import erhält Daten; ungültige Importe werden abgelehnt;
   japanische Kurssuche funktioniert.
8. Schwache Wiederholungskarten werden früher vorgelegt; Wiederholung ist kein
   neuer Lektionsabschluss.
9. Lernserie über Monatsgrenzen und Fehlerweitergabe beim nativen Speichern.

## Oberfläche – sieben bestandene Größenprüfungen

Isolierter Chromium/Edge-Browser, Playwright 1.62.1, Touch-Viewport:
320×640, 360×800, 390×844, 412×892, 412×915, 844×390 und 768×1024 CSS-Pixel.
412×892 dient als Handy-Layoutprüfung für das gewünschte S24-Ultra-Format;
die tatsächlich nutzbare Größe hängt von Android-Bildschirmzoom und Systemleisten ab.

Geprüft: Startseite, Lernkarte, Einstellungen, Lehrerauswahl, japanische Suche,
vollständiger Lizenzdialog, Neuladen und Fortsetzen, falsche/richtige Schreibantwort.
Keine horizontale Überbreite, keine JavaScript-Seitenfehler in diesen Abläufen;
sichtbare Buttons erfüllen die im Test festgelegten Mindestmaße.
Die Browserprüfung simuliert keine native Sprachausgabe und keinen Mikrofonzugriff.

## Echter Android-Emulator – zwei Instrumentierungstests

Android 15/API 35, Google APIs, Pixel-5-Profil, x86_64, 4 GB RAM.

- Native Activity startet die gebündelte WebView-Oberfläche; eine angefangene
  Aufgabe wird nach Neuerstellung der Activity fortgesetzt. Einstellungen,
  Aussprachehilfe, 150 % WebView-Textgröße und Querformat sind geprüft.
- Das echte öffentliche Sprachpaket wird geladen, ausgepackt und anhand seiner
  festgelegten Prüfsummen geprüft. Supertonic erzeugt für alle acht Lehrer je
  eine normale und eine langsame Ausgabe (16 Ausgaben). Die langsamen Ausgaben
  sind länger. SenseVoice erkennt aus dem erzeugten japanischen Audiosignal
  „ありがとう“. Dies verwendet echte native Modelle, keine Attrappen.

Screenshots stammen aus Browser bzw. laufendem Android-Emulator. Die Bildaufnahme
wartet auf den WebView-Zeichenabschluss und einen tatsächlichen Querformatwechsel.
Die Gradle-Testausgabesammlung sichert sie vor dem Aufräumen der Testinstallation.
Bei der Prüfung wurden außerdem eine fehlende Lizenzdatei und schlecht lesbare
Android-Systemleisten nach einem Bildschirmwechsel korrigiert.

## Grenzen und noch offene Gerätetests

- Die Instrumentierung verwendet den Debug-Build mit derselben App-Logik und
  denselben Assets. Die signierte Release-APK wurde kryptografisch und als Paket
  geprüft; ihre Installation auf einem physischen ARM64-Handy ist noch offen.
- Keine echte Mikrofonaufnahme, keine manuelle Hörbewertung, kein Test mit
  Bluetooth-Kopfhörern. Die TTS/ASR-Diagnose arbeitet ohne Mikrofon/Lautsprecher.
- Android 9 bis 14 und Samsung One UI wurden nicht auf echten Geräten geprüft.
- Ein vollständiges Update von einer älteren veröffentlichten Android-Version
  über den Android-Paketinstaller ist noch nicht möglich: Dies ist die erste
  Ausgabe. Paketname, höhere Versionsnummer, SHA-256 und passendes Signierzertifikat
  werden im Update-Code geprüft. Der Release-Feed ist für Folgeversionen eingerichtet.
- Die Sprachmodelle werden lokal verarbeitet. Der Emulator lud sie vor dem
  Test herunter; ein zusätzlicher echter Gerätetest im Flugmodus steht aus.
- Die Handy-Animation verwendet die vorhandenen Bilder, geschlossene Münder,
  Blinzeln und sanfte Bewegung. Sie bildet die aufwendige Windows-OpenCV-
  Verformung nicht vollständig nach.

Die kurze Anleitung in `INSTALLIEREN_ANDROID.md` beschreibt die verbleibende
Hör-, Mikrofon-, Querformat- und Neustartprüfung auf dem S24 Ultra.

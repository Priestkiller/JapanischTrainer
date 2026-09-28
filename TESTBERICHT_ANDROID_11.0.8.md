# Android 11.0.8 Testversion

Stand: 28. September 2026. Version 11.0.8-android.1-test, Code 11000801,
Paket de.priestkiller.japanischtrainer. Umsetzung der Handy-Bildreferenzen und
Verbesserungen für einzelne Kana und kurze, leise Aufnahmen. Windows bleibt
11.0.7 im Testkanal; stabil bleibt auf beiden Plattformen 11.0.4.

## Umsetzung und Bestand

Die sechs Pflichtschritte und die Zusatzübungen verwenden jetzt eine dunkle
Lernansicht mit vorhandenem Japan-Hintergrund, blau abgegrenzten Karten,
kompaktem Fortschritt und gewähltem Lehrer. Hören ist blau, Aufnehmen rosa,
Prüfen beziehungsweise Weiter grün. Eine feste Aktionsleiste und ein eigener
Scrollbereich halten die Hauptaktion erreichbar. Große Schrift, Querformat und
Tastatur werden berücksichtigt. Lehrer und Kiko stehen unter der Aufgabe;
ein kleines Lehrerporträt bleibt im Kopfbereich sichtbar. Keine fremden
Referenzbilder, Systemleisten oder vorgetäuschten XP wurden eingebaut.

Die Startseite und allgemeinen Bereiche behalten ihre bisherige Gestaltung.
Die aufgabenbezogene Darstellung ist HTML/CSS und bedienbar, kein Bild der
Vorlage. Lange Hilfen sind aufrufbar und scrollen; sie schalten nichts frei.
Die sechs Schritte, Kursdaten, bestehenden IDs, Lehrer, Stimmen, Animationen,
Fortschrittsspeicherung und Update-Sicherheit bleiben erhalten. Der Kurs bleibt
bei 150 Lektionen, 680 Karten und 156 Zusatzaufgaben; Revision 11 und
Inhaltsversion 11.0.7 ändern sich nicht. releaseVersion trennt die neue
Android-Programmausgabe von der unveränderten Inhaltsversion bei der Paketierung.

## Aufnahme und Erkennung

Ein sichtbarer Pegel und eine Laufzeit zeigen den tatsächlichen Mikrofoneingang.
Kurze Kana enden nach einem hörbaren Eingangsblock und einer Sekunde Pause;
manuelles Beenden bleibt möglich, maximal 15 Sekunden. Abbruch, Hintergrundwechsel
und eine neue Aufgabe entwerten alte Antworten und die Wiedergabeidentität.
Die letzte Aufnahme kann bewusst aus dem Arbeitsspeicher angehört werden.

Die Aufbereitung entfernt Gleichanteile, erhält Randbereiche vor und nach der
Stimme und hebt leise Signale begrenzt an. Kurze Signale werden nicht mehr
pauschal an einer Mindestdauer von 400 ms verworfen. Ein zusätzliches kleines
Silero-VAD-Modell prüft Sprachaktivität vor der Auffüllung mit Stille; es ist
keine Sprecher- oder Ausspracheprüfung. Für kurze Kana ist die automatische
Umformung zu Zahlen/Schreibformaten deaktiviert. Japanisch bleibt explizit gesetzt.
Die bisherigen SenseVoice- und Supertonic-Gewichte und das separat geladene
Sprachpaket sind unverändert. VAD benötigt 643854 zusätzliche Bytes in der APK.

Eine qualifizierte Aufnahme mit unsicherem oder leerem Kana-Transkript erhält
keinen automatischen Erfolg, keine Fehlerwertung und keine Aussprachepunktzahl.
Erst die bewusste, ausdrücklich gekennzeichnete Selbstprüfung kann weiterführen.
Stille, Klicks, Übersteuerung oder ein technischer Aufnahmefehler geben sie nicht
frei. Wörter, Vokallängen und kleine Kana werden nicht pauschal gleichgesetzt.
Es gibt keine Antwortvorgabe an das Modell und keinen Upload von Sprache.

## Tatsächlich ausgeführte Softwareprüfungen

- 180 Python-Tests bestanden. Alte Kurs-/Fortschrittsregeln und Windows-Code
  bleiben geschützt. Der bisherige komplette Android-Sprachdatei-Hash musste
  wegen des ausdrücklich beauftragten ASR-Umbaus angepasst werden; historischer
  Hash, TTS-Funktion und bisherige Modell-Diagnose bleiben separat geschützt.
- 51 JavaScript-Tests bestanden, darunter neue Grenzfälle für Kana-Selbstprüfung,
  leeres Transkript, fehlende Audioqualifikation, falsche Phase, Neustart,
  Doppelwertung und erhaltene Kursvoraussetzungen.
- Vollständiger bisheriger Lernablauf in sieben Browserformaten bestanden:
  320×640, 360×800, 390×844, 412×892, 412×915, 844×390, 768×1024.
- Zusatzübungen in vier Formaten: 100 Lektions-Einstiege, 36 Aufgabeninteraktionen.
  Separate vier Formate prüfen Aktionsleiste, Pegel, Abbruch, verspätete Antworten,
  eigene Aufnahme, Selbstprüfung und Hintergrundabbruch.
- Browser-Audioereignisse sind simuliert; das ist kein Mikrofontest.
- Lokaler Release-/Debug-/Test-APK-Build und Android Lint bestanden.
- Finaler Android-15-Lauf [36413812852](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36413812852):
  zwölf native Tests bestanden, null Fehler/übersprungene Tests. Alte Profile,
  Kurspakete, Gespräche, Updatefilter, Aufnahmeidentität, echte lokale TTS-/ASR-
  und VAD-Inferenz, Drehung, 140 Prozent Schrift und tatsächlich geöffnete
  Tastatur geprüft. Eingabefeld vollständig sichtbar; Emulatorbilder kontrolliert.
- Lint: null Fehler, zehn Hinweise zu Ziel-SDK/Abhängigkeitsständen, notwendigem
  WebView-JavaScript, Backup-Regeln, Launcherform und KTX-Schreibweise. Keine
  ungefragten SDK-/Bibliotheksmigrationen in dieser UI-/ASR-Änderung.
- Produktions-APK aus diesem Prüflauf mit bisherigem Zertifikat signiert.
  APK-Signatur v3 und 16-KB-Zipalignment bestanden. Öffentliche Nachkontrolle
  erfolgt nach Upload und steht getrennt im Veröffentlichungsbericht.

Aufgetretene und korrigierte Prüfprobleme: Ein alter UI-Test erwartete den nun
bewusst versteckten Weiter-Button als sichtbar. Ein verlegter Formularbutton
bekam eine stabile Kennung; die Formularzuordnung bleibt erhalten. Die Vorschau
brauchte erneut erzeugte Lizenzressourcen. Ein Pegel-Test benutzte zunächst die
Input-API für ein meter-Element. Der alte vollständige Sprachdatei-Hash meldete
den beauftragten Umbau erwartungsgemäß. Finale lokale Läufe nach den Korrekturen
bestanden. Vorbereitende Benchmark-Skripte wurden an die tatsächlich vorhandene
Python-API angepasst. Diese Fehlversuche sind keine bestandenen Produkttests.
Die erste native Sichtprüfung zeigte bei 140 Prozent Schrift und offener
Bildschirmtastatur einen teilweise verdeckten Eingabefeldrand. Eine Reaktion auf
Fokus- und Größenwechsel scrollt das Eingabefeld vollständig in den Aufgabenbereich;
eine zusätzliche native Prüfung kontrolliert beide Feldränder.

## Kontrollierter Modellvergleich

`mobile/tools/benchmark_kana.py` verwendet identische synthetische Signale vor
und nach der Änderung: zehn Kana, vier Stimmen, jeweils normal, auf 2,5 Prozent
Amplitude reduziert und zusätzlich mit je einer Sekunde Stille davor/dahinter.
Zwei Stimmen wurden erst im abschließenden Vergleich verwendet. 120 Kana-Fälle
plus 24 Wort-/Satzkontrollen; keine menschlichen Aufnahmen. Gewertet wird der
normalisierte erkannte Text, nicht die phonetische Qualität. Der Host bildet die
Kotlin-Aufbereitung nach; native VAD-/Modellprüfungen sind separat auszuweisen.

| Kana-Signal | Fälle | Passender Text vorher | Passender Text nachher |
| --- | --- | --- | --- |
| Normale Lautstärke | 40 | 26 | 29 |
| Sehr leise | 40 | 0 | 25 |
| Leise mit Stille davor und danach | 40 | 0 | 23 |

Von den normalen Signalen regressieren drei zuvor passende Ergebnisse:
Stimme 0 bei い, Stimme 6 bei う und きゃ. Zusätzliche/verlängerte Laute bleiben
unsicher; sie werden nicht einfach wegnormalisiert. 39/40 normale, 37/40 leise
und 36/40 verzögerte Signale passieren die Sprachaktivitätsprüfung. Bei den
24 Wort-/Satzkontrollen passen 24 statt acht Transkripte, überwiegend durch
Zulassen der leisen Signale. Das sind kontrollierte Softwaremessungen und kein
Nachweis menschlicher Erkennungsgenauigkeit auf einem Samsung-Gerät.

Alle 13 Negativkontrollen wurden verworfen: Stille, Klick, Brummen, Übersteuerung
sowie weißes Rauschen mit drei Startwerten und drei Pegeln. Ein früher Prototyp
hatte Rauschen nach dem Anfügen von Stille zugelassen. Deshalb prüft die finale
VAD vor dem Padding und mit Schwelle 0,5. Auch diese endliche Kontrolle beweist
keine universelle Unterdrückung beliebiger Umgebungsgeräusche.

## Primärquellen und Einordnung

- [Android AudioSource](https://developer.android.com/reference/android/media/MediaRecorder.AudioSource):
  VOICE_RECOGNITION bleibt als Eingang erhalten. Keine pauschale erzwungene
  Rauschunterdrückung oder zusätzliche Hardware-Verstärkung.
- [Sherpa SenseVoice](https://k2-fsa.github.io/sherpa/onnx/sense-voice/pretrained.html):
  explizite Sprachwahl und inverse Textnormalisierung; Abschalten nur für kurze Kana.
- [SenseVoice-Projekt](https://github.com/QwenAudio/SenseVoice): allgemeine
  Spracherkennung, keine belegte Garantie für einzelne japanische Phoneme.
- [Silero VAD](https://github.com/snakers4/silero-vad) und
  [native Sherpa-API 1.13.8](https://github.com/k2-fsa/sherpa-onnx/blob/v1.13.8/sherpa-onnx/kotlin-api/Vad.kt):
  Sprachaktivitätsprüfung bei 16 kHz; MIT-Lizenz in App und Quellen enthalten.
  Modell-SHA-256: `9e2449e1087496d8d4caba907f23e0bd3f78d91fa552479bb9c23ac09cbb1fd6`.

Die Entscheidung für Aufbereitung plus kleine VAD folgt den eigenen Vergleichen.
Sie ist keine von den Quellen zugesicherte Kana-Erkennung. Ein zusätzliches
655-MB-Erkennungsmodell wird dem Handy nicht ohne belegten Nutzen hinzugefügt.

## Offene menschliche und Geräteprüfung

Reales S24 Ultra: Mikrofon, Hörqualität, tatsächliche Kurzlaut-Erkennung,
automatisches Ende, Umgebungsgeräusche und Bedienung durch Anfänger bleiben offen.
Ebenso menschliche Japanisch-Fachabnahme. Keine neue sprachliche Kursdurchsicht
behauptet: weiterhin 105 Lektionen/501 Karten selbst durchgesehen, 45/179 einzeln
offen. Windows und dessen EXE wurden in diesem Android-Auftrag nicht neu gebaut.
Eine stabile Übernahme benötigt weiterhin ausdrückliche Freigabe.


## Paket und geprüfter Programmstand

Native Buildquelle: `3aca9864c8398771797c29072f50798a9b496222`. Das passende Quellarchiv enthält zusätzlich die abgeschlossenen Berichte; dessen exakter Commit steht in android-update.json.

APK: 62539053 Bytes; SHA-256 `1d6a2c9dac155a949ae592fa2d453e92e51e2cd229caaea01372b36abb653d58`.

Herausgeberzertifikat SHA-256: `3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9`. Lokale Pakete: `F:/Japanischtool/github-JapanischTrainer/release/11.0.8/android/`. Keine Nutzerdaten, Referenzbilder oder privaten Schlüssel enthalten.

# Prüfbericht JapanischTrainer 11.0.2

Datum: 27.09.2026. Windows 11.0.2, Android 11.0.2-android.1 (11000201).
Erstes Inhaltspaket: 30 überarbeitete Lektionen mit 138 Karten, 90 Lernhilfen und 18 neuen Situationsaufgaben. Der Gesamtbestand bleibt 150 Lektionen / 680 Karten / 564 explizite Sprechdatensätze / acht Lehrer.

## Nachgewiesene Programmprüfungen

| Prüfung | Ergebnis | Grenzen |
| --- | --- | --- |
| Windows selftest.py | 142 bestanden | Logik und Daten; keine menschliche Sprachprüfung |
| Installer-Vertrag | 20 bestanden | Statische Regeln; keine neue Installation auf einem fremden Rechner |
| Native Windows-Bedienung | 33 bestanden | Eigenes Testprofil, Audioadapter simuliert |
| Native Windows-Kursprüfung | 22 bestanden | Bestehende Inhalte und alle 100 V11-Ergänzungen; Audioadapter simuliert |
| Neue native UI-Regressionsprüfung | 5 Gruppen bestanden | Verborgene Lösungen, Hilfe ohne Freigabe, japanischer Lesetext, Abschlussrunde |
| Windows EXE-Sprachdiagnostik | bestanden | 8 Stimmen in 2 Tempi; echte Modelle, synthetische Sprache, kein Mikrofon / Abhören |
| Windows Update 11.0.1 → 11.0.2 | bestanden | Isolierte Kopie, HTTPS-Testquelle, signiertes Paket, echter Update-Helfer und EXE-Neustart; XP, Lehrer, Tempo, Karte, Phase und 15 Modelldateien erhalten |
| Android Kurs-/Gesprächslogik | 26 bestanden | Alle 150 Lektionen durchlaufen; Spracheingaben simuliert |
| Browseroberfläche | 7 Formate bestanden | 320×640 bis 768×1024 einschließlich Querformat; Audioereignisse simuliert |
| Android Build und Lint | erfolgreich | Lint-Warnungen zu Ziel-SDK und Abhängigkeiten verbleiben; keine Buildfehler |
| Android-15-Emulator | 3 bestanden, 0 Fehler | Oberfläche, Gesprächsfortsetzung und echte lokale Sprachmodelle; kein physisches Handy |

Android-Buildcommit: `bc625904f62fc943e7c4c8bf6b27f641977783bb`.
[CI-Lauf mit APK und Emulatorprüfung](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36331576609).
Nachfolgende Dokumentations- und Testskriptänderungen verändern diesen Programmcode nicht.

## Paket und Lernstand

- Alle Lektions-IDs, Kartenpositionen, japanischen Kartenformen, Romaji, deutschen Bedeutungen, XP, Sprechziele, Kursrevision und Lernreihenfolge gegen `3eb4384273b981962dd67aae75bc56eacf45b917` verglichen: unverändert.
- Die drei Kurs-JSON-Dateien stimmen zwischen Quelle, Windows-Paket und lokal vorbereiteten Android-Ressourcen bytegenau überein. In der signierten APK sind alle JSON-Werte und Webquellen gleich; beim Linux-CI-Checkout wurden lediglich CRLF-Zeilenenden in LF umgewandelt.
- Android-Signierschlüssel unverändert: SHA-256 `3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9`; APK-Signatur und 16-KiB-Zip-Ausrichtung geprüft.
- Windows verwendet denselben Ed25519-Update-Schlüssel. Die Setup.exe besitzt weiterhin kein Authenticode-Zertifikat.
- Windows startet weiterhin mit Verstehen und optionalem Sprechen; Android behält Hören/Sprechen als Pflichtschritt und die explizite kurze Kana-Selbstprüfung. Gespräche bleiben Android-Funktion.

## Bestandsaufnahme und offene Fachprüfung

`tools/audit_course.py` erfasst alle 150 Lektionen, 680 Karten, 5 Szenen und 29 Gesprächsknoten. 195 Beziehungen sind typisiert (149 normale Reihenfolgekanten, 46 redaktionelle didaktische Verweise); alle modellierten Verweise existieren und sind zyklenfrei. Die acht Exportdateien waren bei Wiederholung bytegleich.

Die ersten 30 Lektionen wurden redaktionell vertieft. Die übrigen 120 sind strukturell erfasst, nicht vollständig fachlich geprüft. Muttersprachliche Prüfung, Anfänger-Erprobung und alle impliziten Voraussetzungen der Gesprächszweige bleiben offen. Keine JLPT-/Niveau-Zertifizierung oder Aussprachequalität aus diesen Tests ableiten.

Weiter offen: Aktualisierung und Mikrofon-/Hörtest am echten S24 Ultra, Bluetooth und Flugmodus; Produktions-Setup auf einem frischen Windows-System ohne Python; weitere Android-Systemversionen. Kein persönlicher Lernstand und keine private Aufnahme wurden für diese Tests verwendet.

## Prüfprobleme

Die Windows-Sandbox verweigerte temporäre Testordner; die Tests wurden anschließend mit isolierten Testprofilen außerhalb der Sandbox erfolgreich ausgeführt. Node-Tests liefen ohne separate Worker-Prozesse, da deren Start blockiert wurde. Ein Git-Push hing beim Standard-Anmeldeweg; mit dem vorhandenen Projektzugang wurde derselbe Zweig erfolgreich übertragen. Es wurden keine Schlüssel ersetzt.

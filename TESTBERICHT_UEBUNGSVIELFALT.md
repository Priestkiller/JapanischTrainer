# Prüfbericht Übungsvielfalt 11 0 7 Test

Stand 28. September 2026. Testveröffentlichung ausdrücklich freigegeben. Builds und die nachfolgenden Software-/Paketprüfungen sind abgeschlossen. Die öffentliche Nachkontrolle wird nach Upload separat in VEROEFFENTLICHUNG_11.0.7_TEST.md dokumentiert.

## Bisher tatsächlich ausgeführt

- Vollständiger Python-Lauf zunächst 178 Tests: 177 bestanden, ein Fehler durch zurückgesetzte Inhalts-Versionsmetadaten. Historische Autorenskripte auf Erhalt neuerer Versionen korrigiert; alle 12 betroffenen Tests danach bestanden. Finaler Gesamtlauf einschließlich zusätzlicher TTS-Abbruch- und Importprüfungen: **180/180 bestanden**.
- 47 mobile Logiktests bestanden. Alle 156 Aufgaben mit Lösung, falscher/fehlender Antwort, Hilfe, Wiederholung und altem Profil geprüft.
- Mobile Oberfläche in 320×640, 412×915, 844×390 und 768×1024: 100 Lektions-Einstiege, 36 vollständige Aufgabeninteraktionen, Lesefragen/Belegstellen, IME, Hilfen und Eingabeerhalt bestanden. Verspätete Audioantwort nach Pause sowie simulierte Mikrofonverweigerung/Abbruch geprüft. Audioereignisse simuliert, keine Aufnahme eines Menschen.
- Native Windows-App: alle 25 Einstiege, zwei vollständige Runden (`5:0` und `v11:read-plan`), acht Renderer und echte Aufgaben-Schaltflächen/Tab-Fokus, Eingabe und Hilfe; Fenster 1080×700, 1280×800, 1440×1040 und 1920×1080 dargestellt. Echte Fensterbilder mit separatem Profil. Sprachresultate im Ablauf simuliert.
- Lokaler Android-Build und Lint bestanden. Finale APK gebaut und mit dem unveränderten Zertifikat signiert; Android-Lint: 0 Fehler, 9 bestehende Warnungen. Der erste Emulatorlauf bestand 6/10; drei Testassertionen waren versehentlich falsch negiert, außerdem verlor die aktive Ansicht ihre Position beim Drehen. Die Assertions wurden korrigiert; Android behandelt nun Orientierung/Bildschirmgröße selbst und erhält die laufende WebView. Ein weiterer Lauf bestand 9/10: Ein alter Test erwartete noch den absichtsvoll behobenen Rücksprung zur Startseite beim Drehen. Die Erwartung wurde auf Erhalt der aktuellen Ansicht geändert. Die Tastaturprüfung wurde zusätzlich auf einen tatsächlichen Fingertipp und bestätigte native IME-Sichtbarkeit verschärft. **Final 10/10 native Tests, 0 Fehler, 0 übersprungen**, Android 15, [Lauf 36398491437](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36398491437), Commit `01c2b7c040dfaae0d289a531d960b159f6830993`. Geprüft: Start, alte Profile, alle bisherigen Inhaltspakete, Gesprächsraum, Kanalfilter, RAM-Aufnahmeidentität/Abbruch, echte lokale Modellinferenz sowie Zusatzaufgabe mit Neustart, Drehung, 140 Prozent Schrift und tatsächlicher Bildschirmtastatur.

## Behobene Prüfauffälligkeiten

Breite Audioknöpfe verursachten beim Tablet horizontales Überlaufen; lokal begrenztes Zweispaltenraster korrigiert, vier Formate erneut bestanden. Die erste Windows-Nachsprechansicht schob Aufnahme unter lange Erklärungen; kompakte sichtbare Vorlage und aufrufbare vollständige Hilfe hergestellt. Automatische Tests unter der Sandbox konnten zunächst keine temporären Profile/Kindprozesse öffnen; diese Läufe wurden nicht als Produktergebnis gezählt und mit isolierten Profilen in zulässiger Umgebung wiederholt. Ein Windows-Buildaufruf mit PowerShell 5 verlor Python-Anführungszeichen; PowerShell 7 wird verwendet.

## Bestandsschutz und Profile

Die 150 bestehenden Lektionen einschließlich aller Kartentexte und bisherigen Verbesserungen werden unabhängig gegen den Ausgangsstand geschützt. Nur `content_version` wird angehoben. Vier absichtlich erweiterte Dateien besitzen einen gesonderten engen Vertrag: native/mobile Entwurfsspeicherung, angehängte auf Zusatzübungen begrenzte Styles, RAM-Wiedergabe einer eigenen Aufnahme. Unveränderte Bewertungs-/Abschlussmethoden, Kursdaten, Modelle und Stimmen werden zusätzlich separat verglichen. Die alten Hashprüfungen anderer Dateien bleiben bestehen.

Der echte Windows-Export/Importdialogpfad wurde mit separater Testdatei und anschließender frischer ProgressStore-Dateiladung zusätzlich bestanden; einschließlich angefangener Zusatzaufgabe, Eingabe, Hilfe und Import-Sicherung. Getrennte Testprofile prüfen ferner Import/Export, unvollständige Antworten, Hilfestatus, alte Pflichtschritte, XP, Lehrkraft und Versionswechsel. Neue Aufgaben und Hilfe setzen keine Lektion automatisch auf erledigt. Die native Android-Hülle verwendet ihre vorhandene AtomicFile-Speicherung; der gebaute Windows-Updater bestand 11.0.6 → 11.0.7 mit separater Programmkopie und synthetischem Profil: TLS-Download, Signatur, Profilübernahme, 15 unveränderte Modelldateien, echter Starttest und Neustart.

## Paket und vorhandene Modelle

Windows-EXE, Update-Helfer und Inno-Setup gebaut. Vier gemeinsame Kurs-/Aufgabendateien in Windows/APK verglichen; alle mobilen Webdateien und Versionsmetadaten mit der APK abgeglichen. APK-Zertifikat SHA-256 `3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9`, Signaturschema v3 und Alignment geprüft. Windows-Version 11.0.7, Android 11.0.7-android.1-test / Code 11000701. Ed25519-Updateprüfung mit bestehendem öffentlichem Schlüssel bestanden. 20 Installer-Vertragsprüfungen bestanden.

Die gebaute EXE hat ohne Netzwerk die acht Lehrer in zwei Tempi synthetisiert; beide vorhandenen ASR-Modelle erkannten synthetisches Japanisch; Stille wurde abgewiesen. Keine echte Mikrofonaufnahme und keine menschliche Hörabnahme. Die alten Modelle werden wiederverwendet.

Echte lokale Fensterbilder: `validation/exercises-ui/`; Browserbilder: `mobile/test-results/exercises/`. Native Android-Bilder stammen aus dem erfolgreichen finalen Emulatorlauf; die Tastatur ist im Bild tatsächlich sichtbar. Kein generiertes Mockup als Funktionsbeleg.

## Grenzen

Menschliche Fachprüfung, Anfänger-Erprobung, echtes S24 Ultra, Mikrofon-/Hörprüfung mit Menschen und ein frisches Windows-System sind offen. Keine Sprachmodellinferenz oder simulierte Browserantwort wird als menschlicher Mikrofontest bezeichnet. Windows besitzt weiterhin kein Authenticode-Zertifikat; Ed25519-Updates und Android-Paketsignatur werden separat geprüft.


Lokale fertige Pakete: `release/11.0.7/windows/` und `release/11.0.7/android/` im aktuellen Quellprojekt. Signierte APK und Windows-Testupdate, Setup, passende Git-Quellen, GPL-/Drittlizenzen, Checksummen, Geräteprüfliste und bereinigte Nachweise werden gemeinsam bereitgestellt.

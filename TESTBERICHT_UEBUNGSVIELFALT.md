# Prüfbericht Übungsvielfalt 11 0 7 Test

Stand 28. September 2026. Testveröffentlichung ausdrücklich freigegeben. Dieser Bericht wird nach Builds, Emulatorlauf und öffentlicher Nachkontrolle ergänzt; vor deren Abschluss keine öffentliche Abnahme.

## Bisher tatsächlich ausgeführt

- Vollständiger Python-Lauf zunächst 178 Tests: 177 bestanden, ein Fehler durch zurückgesetzte Inhalts-Versionsmetadaten. Historische Autorenskripte auf Erhalt neuerer Versionen korrigiert; alle 12 betroffenen Tests danach bestanden. Zwei zusätzliche Abbruch-/Importprüfungen und finaler Gesamtlauf folgen.
- 47 mobile Logiktests bestanden. Alle 156 Aufgaben mit Lösung, falscher/fehlender Antwort, Hilfe, Wiederholung und altem Profil geprüft.
- Mobile Oberfläche in 320×640, 412×915, 844×390 und 768×1024: 100 Lektions-Einstiege, 36 vollständige Aufgabeninteraktionen, Lesefragen/Belegstellen, IME, Hilfen und Eingabeerhalt bestanden. Verspätete Audioantwort nach Pause sowie simulierte Mikrofonverweigerung/Abbruch geprüft. Audioereignisse simuliert, keine Aufnahme eines Menschen.
- Native Windows-App: alle 25 Einstiege, ganze gemischte Runde, acht Renderer, Eingabe und Hilfe; Fenster 1080×700, 1280×800, 1440×1040 und 1920×1080 dargestellt. Echte Fensterbilder mit separatem Profil. Sprachresultate im Ablauf simuliert.
- Lokaler Android-Build und Lint bestanden. Native Emulatorprüfung und signierte finale APK nach aktualisiertem Ressourcenexport stehen noch aus.

## Behobene Prüfauffälligkeiten

Breite Audioknöpfe verursachten beim Tablet horizontales Überlaufen; lokal begrenztes Zweispaltenraster korrigiert, vier Formate erneut bestanden. Die erste Windows-Nachsprechansicht schob Aufnahme unter lange Erklärungen; kompakte sichtbare Vorlage und aufrufbare vollständige Hilfe hergestellt. Automatische Tests unter der Sandbox konnten zunächst keine temporären Profile/Kindprozesse öffnen; diese Läufe wurden nicht als Produktergebnis gezählt und mit isolierten Profilen in zulässiger Umgebung wiederholt. Ein Windows-Buildaufruf mit PowerShell 5 verlor Python-Anführungszeichen; PowerShell 7 wird verwendet.

## Bestandsschutz und Profile

Die 150 bestehenden Lektionen einschließlich aller Kartentexte und bisherigen Verbesserungen werden unabhängig gegen den Ausgangsstand geschützt. Nur `content_version` wird angehoben. Vier absichtlich erweiterte Dateien besitzen einen gesonderten engen Vertrag: native/mobile Entwurfsspeicherung, angehängte auf Zusatzübungen begrenzte Styles, RAM-Wiedergabe einer eigenen Aufnahme. Unveränderte Bewertungs-/Abschlussmethoden, Kursdaten, Modelle und Stimmen werden zusätzlich separat verglichen. Die alten Hashprüfungen anderer Dateien bleiben bestehen.

Getrennte Testprofile prüfen Import/Export, unvollständige Antworten, Hilfestatus, alte Pflichtschritte, XP, Lehrkraft und Versionswechsel. Neue Aufgaben und Hilfe setzen keine Lektion automatisch auf erledigt. Die native Android-Hülle verwendet ihre vorhandene AtomicFile-Speicherung; der Windows-Updater muss noch als gebautes Paket geprüft werden.

## Grenzen

Menschliche Fachprüfung, Anfänger-Erprobung, echtes S24 Ultra, Mikrofon-/Hörprüfung mit Menschen und ein frisches Windows-System sind offen. Keine Sprachmodellinferenz oder simulierte Browserantwort wird als menschlicher Mikrofontest bezeichnet. Windows besitzt weiterhin kein Authenticode-Zertifikat; Ed25519-Updates und Android-Paketsignatur werden separat geprüft.

# JapanischTrainer 11.0.6 Testbericht

Stand 27.09.2026. Inhaltspaket 04 wurde in den gemeinsamen produktiven Kursdaten und den tatsächlich gebauten Windows- und Android-Paketen umgesetzt. Dieser Bericht dokumentiert die Prüfungen vor der öffentlichen Freischaltung. Die ausdrücklich freigegebene Veröffentlichung erfolgt ausschließlich im bestehenden Testkanal; die Nachkontrolle steht anschließend in VEROEFFENTLICHUNG_11.0.6_TEST.md.

## Inhalt und Bestandsschutz

25 weitere bestehende Lektionen / 123 Karten, 75 Lernhilfe-Absätze und 37 gezielte neue beziehungsweise überarbeitete Anwendungsfragen. Alle tatsächlichen falschen Anwendungsantworten dieser 123 Karten sind erklärt; neun vorhandene Leseverständnisfragen bleiben erhalten. Lernziele, Vorwissen, Beispiele, Verwendung, Aussprachehinweise, Abruf und spätere Wiederaufnahme sind in PAKET_04.md für jede Lektions- und Karten-ID einzeln zugeordnet.

Auswahl: Personen/Alter und Zeit (Positionen 47–53), Häufigkeit 59, Jahreszeiten/Wetter/Befinden 82–85, Freizeit/Einladungen/Verbgrundlagen 88–94, Termine 126, Nachrichten 129 sowie Dialog und Lesen 134/137–139. Sie schließt konkret Zeit-/Dauer-, Kalender-/Alter-, Einladungs-/Verneinungs- und Wunsch-/Bestätigungs-Verwechslungen. Keine Auswahl bloß nach fortlaufender Nummer und keine neue Lektion nötig. Alte Beispiele in 12:1 und 23:0 sind bei identischen japanischen/deutschen/Romaji-Texten als gemeinsame Objekte nutzbar.

150 Lektionen / 680 Karten / 565 explizite Sprechziele insgesamt. 105 eindeutige Lektionen / 501 Karten in vier Paketen selbst durchgesehen; 45 Lektionen / 179 Karten bleiben einzeln offen. Alle 150 sind strukturell erfasst. Menschliche Fachprüfung und Anfänger-Erprobung wurden nicht durchgeführt.

124 nicht ausgewählte Lektionen bleiben als vollständige Objekte unverändert, darunter 79 der bisherigen 80. Die gesonderte Vorbereitungskorrektur an 12:0:4 betrifft ausschließlich das Kartenprofil: drei Zweiergruppen, freiwillige Miniübungen und eine Frage nach der Zahl nach sieben. Ziele, Lesungen, XP, Reihenfolge und alle 680 Kartenidentitäten bleiben erhalten. Die ganze Zahlenreihe bleibt in Sprechen/Bauen/Schreiben verlangt; Teilantwort, Hilfe oder Kana-Selbstprüfung umgehen sie nicht. Die Entlastung echter Anfänger bleibt offen und wird nicht als bewiesen ausgegeben.

Ausgangsvertrag: Commit 21de74cfd5cde7ba8d77cda00c877ca590d90dbf, tests/fixtures/package03-contract.json. Keine Änderung an Kursrevision 11, Android FLOW_REVISION 2 oder Speicherschema. Alte Sitzungen in allen 25 ausgewählten Lektionen und der Zahlenkarte wurden mit synthetischen Altprofilen geprüft, einschließlich XP, Lehrer, Kartenposition und bestehender Freigaben. Windows behält Verstehen und freiwilliges Sprechen; Android sechs Schritte und gekennzeichnete Kana-Selbstprüfung. Lehrer, Stimmen, Animationen, Modelle, Gesprächsengine und Update-Sicherheit sind geschützt und unverändert.

## Tatsächlich ausgeführte Prüfungen

| Prüfung | Ergebnis und Grenze |
| --- | --- |
| Python | 167 Tests bestanden, validation/python-1106.log; davon sechs neue Paketprüfungen, alle 123 Karten und fünf Abrufphasen sowie Bestandsschutz/Altprofile. |
| Update-Sicherheit | 24 vorhandene Prüfungen in der Python-Suite: Signatur, Manipulation, falsches Ziel, Kanaltrennung, leere/alte Angebote und Downgrade-Schutz. |
| Installer | 20 Vertragstests bestanden; vollständiger Inno-Setup-Installer gebaut. Installation auf frischem Windows nicht durchgeführt. |
| Windows nativ | Alle 25 Lektionen: sichtbare Erklärungen, fünf Abrufphasen ohne Lösungsvorlage, falsche Antwort mit Begründung, bewusste Hilfe ohne XP/Freigabe. Zahlenkarte zusätzlich mit Teilantwort und erreichbarem Scrollbereich geprüft. Separate Profile; Bedienaudio simuliert. |
| Mobile Logik | 39 Tests bestanden; alle 123 Karten über sechs Stufen, Aufnahme-/Hilfesperren, 26 Altprofile, drei Wochenendrouten und die nicht unterstützten Caféantworten. Text-/Aufnahmeereignisse simuliert. |
| Mobile Oberfläche | 75 Paketprüfungen: 25 Lektionen bei 320×640, 412×915 und 844×390. Zusätzlich kompletter Sechs-Schritte-Ablauf in sieben Formaten von 320×640 bis 768×1024. Keine horizontalen Überläufe; Browser-Audioereignisse simuliert. |
| Android nativ | [Prüflauf 36347546310](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36347546310): 8 Tests, 0 Fehler, 0 übersprungen, 113.628 s unter Android 15. UI, Neustart, alte Profile für Paket 2/3/4, Zahlenhilfe, Gespräch, Kanalfilter und echte lokale Modellverarbeitung. |
| Android Build/Lint | Release-, Debug- und Instrumentierungs-APK gebaut; Lint 0 Fehler / 0 Fatal / 9 bestehende Warnungen. Kein Nebenumbau der Abhängigkeiten. |
| APK | Paket de.priestkiller.japanischtrainer, Name 11.0.6-android.1-test, Code 11000601; v3-Signatur und 16-KiB-Alignment bestätigt. Bestehendes Zertifikat, SHA-256 3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9. |
| Windows Build | EXE, eingefrorener Updatehelfer und vollständiges Setup gebaut. PE-Version 11.0.6.0 und sichtbare Anzeige 11.0.6/Testversion geprüft. |
| Gebaute EXE / Modelle | Alle 8 Stimmen in 2 Tempi, beide lokalen Erkenner auf synthetischem Danke-Satz, Zielvergleich und Ablehnung von Stille bestanden (7.88 s). Netzwerk gesperrt, keine Lautsprecher-/Mikrofonprüfung. |
| Windows Update | Vollständiges lokales TLS-Update 11.0.5 → 11.0.6 mit gebautem Helfer, Startprüfung und tatsächlichem Neustart bestanden. Testprofil und 15 Modelldateien erhalten. Lokale Testsignatur; Produktionssignatur getrennt geprüft. |
| Produktionssignatur | Neues Windows-Manifest mit vorhandenem Ed25519-Vertrauensschlüssel verifiziert; ZIP-Größe und SHA-256 stimmen. |
| Paketdaten | Alle drei Kursdateien in gebautem Windows und signierter APK bytegleich mit den geprüften Quellen. Mobile Webdateien und Versionsdatei ebenfalls bytegleich; Lizenzen enthalten. |
| Kursanalyse | 11 Berichte reproduzierbar; historische Paketberichte 01–03 unverändert. 557 modellierte Beziehungen, gültige frühere Voraussetzungen. Implizite Sprachvoraussetzungen bleiben nur teilweise automatisch erfasst. |

Produktstand 1df3e57425a03998275e3328954dcee2d2f1c0b1. Finaler CI-Stand f7ef4b0031ec1dbdfb701a78803cdf38a43dab07; Unterschied ausschließlich Isolation der Testprofile, Fokusprüfung der Screenshots und CI-Emulatorvorbereitung, keine Änderung produktiver Dateien. Spätere Berichtscommits sind in der Veröffentlichung nachvollziehbar ausgewiesen. Keine persönliche Installation oder persönlicher Lernstand wurde verändert.

## Gesprächsgrenzen und sprachliche Unsicherheiten

Drei automatisch bestandene vorbereitete Wochenendrouten decken Film/Park/Café, Samstag/Sonntag, 10/14/15 Uhr und Bahnhof/Cafévorplatz ab. Das belegt diese Routen, keine freie Konversation und kein vollständiges menschliches Hörverständnis. Café-Bestellung mit Mengenwort und Größe M bleiben außerhalb der Szene; Ablehnung ohne Fortschritt enthält keinen angeblichen Aussprachebefund. Unterstützte Antworten funktionieren danach weiter. Kein Gesprächsraum für Windows ergänzt.

Punktuell abgeglichen: Japan Foundation Irodori Starter Lektion 9, Seiten 1, 8 und 16–17, Stunden, Wochentage, Zeitgrenzen und Terminantworten. [Primärquelle](https://www.irodori.jpf.go.jp/assets/data/starter/pdf/X_L09.pdf). Der Abruf von Lektion 12 scheiterte und zählt nicht als Prüfung. Eigene Lehrtexte, keine vollständige externe Sprachvalidierung.

Konkrete offene Stellen: Altersfrage 12:1:2; Zahlenbelastung 12:0:4; Lesungsvarianten v11:people-age:4 und v11:clock-minutes:2; indirekte Absagen in v11:reply-invites / v11:appointments; berufliches Register in v11:messages; Natürlichkeit und Hörverständnis im Wochenenddialog; Erklärung von だったら/なら in v11:read-plan:4 / v11:read-message:3. Näherungslautung und Textvergleich sind keine Phonetik- oder Tonhöhenabnahme.

## Fehlversuche und Behebung

Der erste Autorentextlauf fand bei neun alten Leseaufgaben andere Distraktoren als Kartenbedeutungen und schrieb deshalb nichts. Individuelle Begründungen für diese erhaltenen Fragen behoben die Lücke. Ein Idempotenztest entdeckte eine zu enge Zuordnung bereits überarbeiteter Bedeutungen; die Auflösung nutzt jetzt zusätzlich die ursprüngliche Verwendung. Danach sind die Daten wiederholbar identisch.

Die erste volle Python-Suite beanstandete die String-zu-Objekt-Normalisierung in zwei alten Lektionen. Der Vertrag wurde nur für 12:1 und 23:0 präzisiert und prüft weiterhin alle drei Originaltexte. Danach 167/167 bestanden. Die Windows-Dateiversion wurde vor dem Build mit Laufzeit/Kurs auf 11.0.6 abgeglichen.

Der erste native Android-Lauf 36346360597 bestand 7 von 8 Prüfungen. Die Zahlenhilfe und neue Paketprüfung bestanden, aber beim folgenden Starttest war noch der Zahlen-Testlernstand aktiv: visibilitychange speicherte beim Schließen die laufende WebView erneut. Der Test setzt und sichert nun vor jeder Methode ein eigenes Profil und stellt es erst nach geschlossenem ActivityScenario wieder her. Ein Paketnamen-Guard erlaubt dies ausschließlich in der separaten .test-App. Ein zweiter Lauf 36346908961 bestand zwar alle acht Tests, seine Screenshots waren jedoch von einem ANR-Dialog des fremden Pixel-Launchers verdeckt. Er wurde deshalb nicht als saubere visuelle Abnahme verwendet. Nur im kurzlebigen CI-Emulator wird der Launcher nun vor den Tests deaktiviert; jede Screenshotaufnahme verlangt zusätzlich Fensterfokus der App. Der abschließende oben genannte Lauf besteht alle acht Prüfungen mit unverdeckten Bildern. Keine Produktionslogik geändert.

## Fertige lokale Testpakete

| Datei unter F:/Japanischtool/github-JapanischTrainer/release/11.0.6 | Bytes | SHA-256 |
| --- | --- | --- |
| windows/JapanischTrainer-11.0.6-Setup-x64.exe | 846939391 | `2cf65cb8273b5e6e35a479b3475031d83b4e64f1967811d55faf97f3341be66e` |
| windows/JapanischTrainer-11.0.6-Update-x64.zip | 134061176 | `a43a3a901dfc402b25c668d9e7f16d90e2f821427af32ba153e849f6b0736caf` |
| android/JapanischTrainer-11.0.6-Android.apk | 61850356 | `ccaf877b20040a83485358c4b9f2c8e3f92b4058efec20655bb9bc912c8a7064` |

Quellen, Lizenzunterlagen, Geräteschritte und bereinigte Testnachweise werden in beiden Test-Releases bereitgestellt. Die passenden Quellen stammen aus einem dokumentierten Git-Commit. Private Schlüssel, Zugangsdaten, Nutzeraufnahmen und persönliche Lernstände sind ausgeschlossen.

Echte S24-Ultra-Installation, Mikrofon, Lautsprecher, Bluetooth, One UI, ein frisches Windows-System, menschliche Fachprüfung und Anfänger-Erprobung bleiben offen. Weitere Android-Versionen wurden hier nicht separat getestet. Der Windows-Installer ist nicht Authenticode-signiert. GERAETEPRUEFUNG_11.0.6.md ist eine praktische Anleitung, kein bestandener Test.

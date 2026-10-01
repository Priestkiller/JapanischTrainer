# Android Gestaltung 11.0.12

Stand 1. Oktober 2026. Der Nutzer bestätigt die installierte 11.0.11. Der zuvor festgestellte Unterschied zu seinen Handyvorlagen wird jetzt in der Android-Anwendung umgesetzt. Windows bleibt bei Testversion 11.0.11. Der stabile Kanal bleibt 11.0.4.

## Tatsächliche Änderungen

Die Android-Startseite, der Lernweg, Wiederholung, Lehrerauswahl und die weiteren Menüs verwenden den bestehenden Japan-Nachthintergrund, dunkle Karten mit cyanfarbenen Konturen und helle Schrift. Das vorhandene Hintergrundbild, Figuren, Stimmen und Animationen werden weiterverwendet. Ein als SVG gezeichnetes Torii ersetzt das bisherige helle Markenfeld. Eingaben, Rückmeldungen und Aktionen erhalten passende Farben; der native WebView startet auf dunklem Hintergrund.

Beim Sprechen erscheint die vorhandene Lehrkraft rechts unterhalb der Aufgabenkarte mit einer Sprechblase links, wenn die verfügbare Höhe ausreicht. Kleine Displays, Querformat, große Schrift und eine eingeblendete Tastatur behalten die kompakte Darstellung. Vorlage, Aussprachehilfe und Aufnahme bleiben zusammen. Die feste Hauptaktion und die bestehenden bewusst aufrufbaren Hilfen bleiben erhalten. Lange Menüs und außergewöhnlich lange Inhalte dürfen weiter scrollen; für normale Lektionsschritte bleibt der vorhandene Ablauf mit festen Aktionen und expliziten Inhaltsseiten bestehen.

Die spätere Nutzeranweisung zur Ablenkungsbegrenzung bleibt verbindlich: In Auswahl-, Bau- und Schreibaufgaben erscheint keine große Lehrkraft, Kiko erscheint in Übungen nur beim Abschluss. Die Referenzen werden damit in Gestaltungsrichtung und nutzbarer Anordnung übernommen; eine pixelgleiche Kopie aller dort gezeigten Dekorationen wird nicht behauptet.

Keine Änderungen an Kursdaten, Speicherung, Sprechbewertung, Sprachmodellen, Stimmen oder Update-Sicherheit. Kurs unverändert: 150 Lektionen, 680 Karten, Revision 11, Inhaltsversion 11.0.7. Bestehende Kennungen und Lernstände bleiben erhalten. Android-Version 11.0.12-android.1-test, Code 11001201, Paket de.priestkiller.japanischtrainer. Dieselbe Herausgebersignatur ist für den fertigen Build vorgesehen.

## Ausgeführte Prüfungen im Quellstand

- 192 Python-Regressionsprüfungen und 60 JavaScript-Prüfungen bestanden.
- Neue UI-Prüfung: 75 Ansichten in fünf Bildschirm-/Schriftformaten bestanden, einschließlich Navigation, horizontaler Begrenzung, Platzierung der Lehrkraft, unverändertem XP-Stand und Übergang vom Sprechen zur Aufgabe ohne Figur.
- Bestehende Aufgabenprüfung: 300 Kernansichten und 156 Zusatzaufgaben in fünf Formaten bestanden. Zusammenbleibende Sprechvorlage, absichtliche Hilfen, Inhaltsseiten und Ausweichverhalten für langen Text wurden geprüft.
- Die Sprechhilfe nach drei erfolglosen Versuchen, Wiederaufnahme, Auswahlhilfe und Abschluss bestanden in vier Formaten. Die verwendeten Audioereignisse waren simuliert; dies ist kein Mikrofontest.
- Eigene Sichtprüfung der neuen Startseite, Sprechansichten und Einstellungen anhand tatsächlich gerenderter Browseransichten. Weitere Sichtprüfung und native Android-Prüfung folgen vor Veröffentlichung.

Testprofile sind isoliert. Die native Suite erhält eine zusätzliche Prüfung für die fünf Hauptmenüs und die Übernahme eines älteren Profils einschließlich XP, Abschluss, Lehrkraft und zuletzt geöffneter Lektion. Die bisherige native Geometrieprüfung prüft nun die tatsächliche Anforderung: Die Lehrkraft überlappt weder Sprechaufgabe noch feste Hauptaktion. Ihre frühere feste Position oberhalb der Aufgabe ist keine fachliche Anforderung.

Einzelne Testprozesse wurden zunächst durch Sandbox-Prozessbeschränkungen blockiert. Die Wiederholung außerhalb der Sandbox bestand. Beim ersten lokalen Gradle-Aufruf war der JDK-Verzeichnisname falsch angegeben; der vorhandene JDK wird anschließend mit seinem tatsächlichen Namen verwendet. Keine Toolchain oder Signierschlüssel wurden ersetzt.

## Vor der Veröffentlichung noch erforderlich

Android-Release-Build, Lint, native Emulatorprüfungen, Paketversion, Zertifikat und 16-KB-Alignment müssen erfolgreich sein. Danach sind echte öffentliche Dateien, Prüfsummen und Kanaltrennung zu prüfen. Der abschließende Veröffentlichungsbericht hält diese Ergebnisse separat fest; dieser Quellbericht behauptet sie noch nicht.

## Offene menschliche Prüfungen

S24 Ultra mit echten Android-Schrift-/Zoom-Einstellungen, Mikrofon und Kopfhörer; Anfänger-Erprobung; menschliche Japanisch-Fachprüfung. Die größere Lehrkraft und Nachtfarben beweisen keine bessere Spracherkennung. Bestehende optionale Modelltests bleiben freiwillig und lokal.

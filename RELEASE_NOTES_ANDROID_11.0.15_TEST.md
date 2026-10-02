# Android 11.0.15 – erreichbare Antworten und Fehlerwiederholung (TESTVERSION)

## Abschließender Stand nach der Veröffentlichung

Android 11.0.15 ist als Prerelease veröffentlicht und öffentlich geprüft. 71 JavaScript-, 21 Python-, 22 native Android-Prüfungen und 682 Browseransichten bestanden. Alle 19 öffentlichen Dateien stimmen bei Größe und SHA-256; 15 getrennte Profil-/Formatfälle prüfen die Updateanzeige mit realen Manifesten und simulierter Brücke. Die native HTTPS-Prüfung lief vor dem Upload. Reale S24-, Mikrofon-, Hör-, Anfänger- und menschliche Sprachprüfung bleiben offen.

Finale APK: 88293243 Bytes, SHA-256 f65f3fa9164ae1c884edf5d7f0c44b41da12b8d519e40e467daea215c3d2d34b. Sie wurde aus der frischen CI-Release-APK signiert. Alle 254 Programmeinträge stimmen bytegenau mit CI überein; nur die Herausgebersignatur kommt hinzu. Ein abweichender lokaler Build mit alter Versionskonstante wurde vor Veröffentlichung verworfen.

[Download](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.15-1). Details: VEROEFFENTLICHUNG_ANDROID_11.0.15_TEST.md. Die folgenden Hinweise zu noch ausstehenden Prüfungen beziehen sich auf den damaligen lokalen Zwischenstand; die abschließenden Nachweise haben Vorrang. Stabil bleibt 11.0.4, Windows-Test 11.0.11.

- Antworten werden als ganze bedienbare Felder aufgeteilt. Rückmeldungen schalten
  die Ansicht nicht mehr automatisch um; ihre Erklärung ist zusätzlich aufrufbar.
- Nach drei erfolglosen Sprechversuchen bleibt **Antwort stattdessen auswählen**
  fest am unteren Rand sichtbar, auch nach einem Neustart. Die passende Auswahl
  und ihre Bestätigung sind nötig. Technische Fehler vergeben keine Aussprache-Note.
- Die gekennzeichnete Kana-Selbstprüfung nach geeigneter Aufnahme ist ebenfalls
  sichtbar aufrufbar und schließt ihren Hilfedialog nach Bestätigung.
- Falsch beantwortete Lernaufgaben können ans Ende verschoben werden und kommen
  dort in ihrer ursprünglichen Aufgabenart wieder. Abschluss und XP erst nach
  gelöster Fehlerwiederholung und Abschlussrunde; erneute Fehler wieder ans Ende.
- Zehn Karten in „A, I, U, E, O“ (0:0) und „Kurz oder lang? Vokale unterscheiden“
  (v11:long-vowels) erklären Laut, Länge, Zählschritt und Antwortbezug deutlicher.

150 Lektionen, 680 Karten, 156 Zusatzaufgaben; stabile IDs und Reihenfolge erhalten.
Die bestehenden Figuren, Animationen, Stimmen, Sprachmodelle und Updateprüfungen
bleiben erhalten. Das ist eine Korrektur von Bedienung und Aufgaben, kein Nachweis
verbesserter Spracherkennung. Windows bleibt bei seiner bisherigen Testausgabe.

APK über die vorhandene App installieren; vorher nicht deinstallieren. Nur der
Testkanal bietet sie auf ausdrückliche Suche an. Stabil 11.0.4 bleibt unverändert.

Echte S24-Ultra-/Mikrofon-/Hörtests, menschliche Anfänger-Erprobung und Japanisch-
Fachprüfung sind offen. Automatisierte Software-, Paket- und Veröffentlichungs-
prüfungen werden im mitgelieferten Prüfbericht konkret ausgewiesen. Eine Übernahme
in den stabilen Kanal braucht eine eigene Freigabe.
# Ergänzende Korrektur der Eingabe

Aktive Schreibfelder bleiben bei Layout- und Tastaturänderungen verbunden;
Fokus, Cursor und Entwurf gehen nicht durch den Seitenaufbau verloren. Haupt- und
Zusatzaufgaben wurden in zwölf zusätzlichen Browserfällen geprüft. Die vorhandenen
670 Browseransichten bestanden nach dieser Korrektur erneut. Der endgültige native
Tastaturnachweis wird mit seinem tatsächlichen Ergebnis ergänzt.


## Abgeschlossene Software- und Paketprüfung

Quellstand 5e216ebbe4ddf82a53995e8593b5152d8b93b8e5: 71 JavaScript-Prüfungen, 21 Python-Prüfungen und 682 Browseransichten bestanden. Alle 670 bisherigen Ansichten wurden nach der Fokuskorrektur erneut ausgeführt; zwölf zusätzliche Haupt-/Zusatzfälle prüfen Fokus, Cursor, Eingabe, Tastaturverkleinerung und Neustart. Vollständiger nativer Android-35-Lauf: 22/22 Fälle bestanden, keine Fehler oder übersprungenen Fälle. Darunter echte Bildschirmtastatur, sichtbare Drei-Versuche-Hilfe, bestätigte falsche/korrekte Auswahl, ursprüngliche Fehleraufgabe am Ende, Neustart, alte Profile, Kalender, Figuren, tatsächliche Konfettipixel, Abschluss, XP, Update-Kanaltrennung und echte lokale Modellverarbeitung synthetischen Audios. CI: https://github.com/Priestkiller/JapanischTrainer/actions/runs/37063057233 (Versuch 1). Das ist kein Mikrofon- oder menschlicher Sprachtest.

Build und Lint bestanden; lokal 11 und CI 12 Warnungen, jeweils 0 Fehler. Ein früherer Lauf scheiterte vor Testbeginn am beschädigten Download des Google-API-Systemabbilds; er ist kein bestandener nativer Nachweis. Der zweite Lauf wurde durch die zusätzliche Kana-Bedienkorrektur überholt und abgebrochen. Die lokale kanonische Asset-Vorbereitung wurde zunächst im falschen Arbeitsordner gestartet und danach erfolgreich korrigiert. Nur der erneute Build mit exakten Git-Assets wurde signiert. Der lokale Kotlin-Buildcache wurde außerhalb des Quellenarchivs aufbewahrt.

Ein vollständiger Erstlauf auf 35193f2e bestand 15/22 Fälle. Sechs alte Testannahmen betrafen bewusst verdeckt gespeicherte Romaji beziehungsweise den entfernten Hinweis-Container. Die nativen Assertions wurden auf sichtbare Lösungen und einen tatsächlich lesbaren Hinweisdialog mit erhaltenen Fortschritts-Gates umgestellt. Der siebte Fehler war HTTP 403 am öffentlichen GitHub-API-Einstieg, Ursache unbekannt. Der zweite vollständige Lauf auf 7459f85 bestand 20/22 einschließlich unveränderter echter HTTPS-Prüfung. Zwischen diesen beiden Ständen änderten sich nur Testadapter und Bericht.

Die beiden verbleibenden Fälle betrafen Tastatur und eine verspätete Konfettimessung. Die Browser-Reproduktion belegte einen Produktfehler: Seitenaufbau entfernte das aktive Feld und verlor den Fokus. focus-ui.mjs hält seine Seiten jetzt verbunden und passt Höhe/Scrollposition an. Eingabe und Cursor bleiben erhalten. Die Konfettiprüfung beobachtet seit dem echten Abschlussklick zwei verschiedene nicht leere Canvasbilder; Animation und 3,2-Sekunden-Dauer sind unverändert. Der finale vollständige Lauf besteht alle 22 Fälle. Weder 15/22 noch 20/22 zählen als erfolgreiche Abschlussprüfung.

APK: 88293243 Bytes, SHA-256 f65f3fa9164ae1c884edf5d7f0c44b41da12b8d519e40e467daea215c3d2d34b; Version 11.0.15-android.1-test, Code 11001501, Paket de.priestkiller.japanischtrainer. Bestehendes Herausgeberzertifikat, v3-Signatur und 16-KB-Alignment geprüft. 168 Kurs-/Web-/Bild-/Lizenzdateien und acht weitere Metadaten-/Hinweis-/Modellressourcen entsprechen bytegenau dem Quellcommit. Alle lokalen und CI-Assets sind bytegleich. Quellen und Lizenzunterlagen ohne Schlüssel, Zugangsdaten, private Lernstände oder Nutzeraufnahmen zusammengestellt.

Der abschließende Buildvergleich stoppte zunächst: Der lokale inkrementelle Kotlin-Build enthielt trotz korrektem Manifest noch eine Versionskonstante aus 11.0.14. DEX-Auswertung wies die Abweichung nach. Dieses Paket wurde nicht veröffentlicht. Die finale APK wurde stattdessen direkt aus der frischen Release-APK des erfolgreich geprüften CI-Laufs mit dem bestehenden Schlüssel signiert. Alle Programm-, Bibliotheks- und Ressourcen-Einträge stimmen bytegenau mit dessen APK überein; nur die Herausgebersignatur kommt hinzu. APK-Hash und Metadaten wurden neu erstellt.

Die öffentliche Abnahme steht bei Erstellung dieses Uploadpakets noch aus und wird nach dem tatsächlichen Upload im Veröffentlichungsbericht und der Projektchronik dokumentiert. Echte S24-, Mikrofon-/Hör-, Anfänger- und menschliche Fachprüfung bleiben offen. Keine neue Windows-EXE; deren veröffentlichter Teststand bleibt 11.0.11, stabil bleibt auf beiden Plattformen 11.0.4.

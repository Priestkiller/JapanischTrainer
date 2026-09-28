# Android 11.0.9 Testversion Prüfbericht

Stand: 28. September 2026. Umsetzung der erneut konkretisierten Handy-Bildvorlagen. Die bisherige scrollbare Lernseite wurde durch eine feste Aufgabenbühne ersetzt. Kein neuer Kursinhalt und keine neue Spracherkennungslogik.

## Tatsächliche Änderungen

- Nachtszene mit Pagode, Kirschblüten und Laternen. Große vorhandene Lehrkraft rechts, Kiko links und Sprechblase im sichtbaren unteren Bildschirmbereich. Alle acht Lehrer und die Einstellung für Kiko bleiben erhalten.
- Aufgabe, Aussprachehilfe, Wiedergabe und Aufnahmekarte sind zusammen angeordnet. Fortschritt, echte Lernserie und XP stehen oben. Prüfen oder Weiter bleibt unten.
- Lange Aufgaben haben sichtbare Seitentasten und einen Ansichtszähler. Ihre Seiten sind reine Darstellung und geben keine Lernschritte frei. Auch auf kleinen Bildschirmen bleibt die Schrift lesbar.
- Vorwissen, Erklärungen und vollständige Beispiele öffnen in einer eigenen Ansicht mit Seitenanzeige. Android-Zurück und Schließen führen zur bestehenden Aufgabe zurück. Eingaben, Bausteine und Hilfestatus bleiben erhalten.
- Vorwissen wird beim ersten Öffnen einer ersten Lernkarte in der laufenden App erklärt. Die vollständige Einführung einer Zusatzrunde öffnet separat. Geschlossene Pflichtschritt-Hilfe wird jetzt ebenfalls gespeichert; vorher konnte der alte offene Zustand nach Neustart wiederkehren.
- Technische Hinweise zur Aufnahme sind bewusst aufrufbar. Aufnahmefehler und Kana-Selbstprüfung bleiben tatsächliche Aufgabenrückmeldungen. Ein Fehler oder ein Hilfeklick wird nicht zum Erfolg.

Produktive Dateien: `mobile/web/focus-ui.mjs`, `focus.css`, begrenzte Anbindung in `app.mjs`, `mobile/web/artwork/lesson-night.png`. Grafikherkunft und finaler Prompt: `mobile/ARTWORK_11.0.9.md`. Die geteilten Kursdateien, Windows, Lehrerdateien, Modelle, Spracherkennung, Signierschlüssel und Update-Filter wurden nicht geändert.

## Ausgeführte automatische Prüfungen

| Prüfung | Ergebnis |
| --- | --- |
| Python inklusive Kursbestand und Update-Sicherheit | 180 bestanden |
| Mobile Logik inklusive alter Profile und Kana | 51 bestanden |
| Vollständiger Lernablauf und Gesprächsraum | Sieben Browserformate bestanden |
| Zusatzübungen | Vier Browserformate, 100 Einstiege und 36 Aufgabeninteraktionen bestanden |
| Sprechoberfläche | Vier Formate; Abbruch, verspätete Ereignisse, qualifizierte Selbstprüfung und eigene Aufnahme bestanden |
| Lange Inhalte und Seitenbedienung | 300 Kursansichten in fünf Formaten plus alle 156 Zusatzaufgaben bei 412 × 915 bestanden |
| Große Schrift und knappe Höhe | Zwei Browserformate bei 140 Prozent, Entwurfserhalt und Tastaturbedienung der Hilfe bestanden |
| Native Android-Prüfung | 13 bestanden, 0 Fehler, 0 übersprungen; Android 15 im Emulator |
| Android Lint | 0 Fehler, 10 bestehende Warnungen |

Die Langtextprüfung verwendet zehn Karten, darunter die acht nach japanischem Text, Romaji und Bedeutung zusammen längsten Karten, einen kurzen Laut und ありがとう. Sie prüft alle sechs Schritte. Sie kontrolliert ausdrücklich die tatsächlich geladene Lektion, erreichbare Seitentasten, Inhaltsgrenzen und feste Hauptaktionen. Das ist keine behauptete Prüfung sämtlicher 680 Karten durch Anfänger.

Die Tests benutzen separate Profile. Browser-Audioereignisse sind simuliert und keine Mikrofonprüfung. Im bisherigen Android-Prüfablauf vorhandene echte native Modellinferenz wird separat ausgewiesen. Die eigene visuelle Prüfung verwendet echte Browser- und Emulatorbilder; die Entwurfsbilder werden nicht als Prüfbeleg ausgegeben.

## Behobene Auffälligkeiten im Arbeitslauf

Der erste native Lauf bestand zwölf von dreizehn Tests. Sein Tastaturtest benutzte noch Scrollen und zielte außerhalb der sichtbaren App; er navigiert nun über die tatsächlichen Seitentasten und kontrolliert vor dem echten Antippen die Eingabegrenzen. Folgende Läufe und der abschließende Build bestanden alle dreizehn Tests. Die finale Kurzlaut-Prüfung bestätigt eine einzige Ansicht auch zwischen den Android-Systemleisten.

Der finale [GitHub-Build 36423006309](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36423006309) prüfte Programmstand `a30923f6a4cd31d41dfa856001f6fef4486799a8`. Darin liefen echte native Tastatur bei 140 Prozent Schrift, Rotation, getrennte Profile, unveränderte Kanalfilter, tatsächliche lokale Sprachmodellinferenz und Signal-/VAD-Prüfungen mit synthetischem Audio. Das sind keine Aufnahmen eines Menschen. Die native Kurzlautansicht und Tastaturbilder wurden visuell geprüft; kein verdecktes Eingabefeld und kein vertikaler Scrollweg in der Lernansicht. CI meldet außerdem nicht blockierende Hinweise zu älteren Action-Versionen und dem anstehenden Runner-Wechsel.

Ein frühes Layout ließ große Figuren hinter Bedienelemente ragen; die Figuren haben jetzt einen eigenen sichtbaren Bereich. Lange Karten konnten auf 320-Pixel-Bildschirmen am Kartenrand überlaufen; die zusätzliche Seitenansicht zerlegt solche Inhalte in lesbare Abschnitte. Ein asynchron geöffnetes Hilfefenster konnte in frühen Tests zu spät erscheinen; das Fenster öffnet jetzt synchron und sein ursprünglicher Inhalt bleibt für die Audio-Bedienung erhalten. Die neue Testvorrichtung wurde gegen versehentlich überschriebenes Startprofil abgesichert und prüft die geladene Lektion ausdrücklich. Der erste Python-Lauf scheiterte an Sandbox-Rechten für temporäre Testordner; der Lauf mit passenden Rechten bestand. Diese Fehlversuche werden nicht als bestandene Tests gezählt.

## Umfang und offene Abnahme

Kurs unverändert: 150 Lektionen, 680 Karten, 156 zusätzliche Aufgaben in 25 Lektionen, Kursrevision 11/Inhaltsversion 11.0.7. Bisherige eigene sprachliche Durchsicht: 105 Lektionen/501 Karten, 45 Lektionen/179 Karten offen. Dieser UI-Auftrag erweitert diese fachliche Abnahme nicht.

Echte Bedienung auf dem S24 Ultra, Mikrofon- und Hörtests, Anfänger-Erprobung und menschliche Japanisch-Fachprüfung bleiben offen. Die Kurzlaut-Erkennung aus 11.0.8 bleibt unverändert; keine neue Genauigkeitssteigerung wird durch dieses Layout behauptet. Fenster mit sehr wenig Platz erhalten zusätzliche Ansichtsseiten. Windows-Test bleibt 11.0.7 und wird in diesem Android-Auftrag nicht neu paketiert.

## Geprüftes lokales Paket

Android `11.0.9-android.1-test`, Code `11000901`, Paket `de.priestkiller.japanischtrainer`. APK: `release/11.0.9/android/JapanischTrainer-11.0.9-Android.apk`, 64.890.234 Bytes. SHA-256: `71a0c80b10fd8bb9cb45af9443c9961527d858c37e32e029815833631e50edb5`.

APK-v3-Signatur und 16-KB-Zipalign bestanden. Das vorhandene Signierzertifikat bleibt `3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9`. Quellarchiv und APK werden auf bytegleiche Web-, Kurs-, Modellmetadaten- und VAD-Dateien geprüft. Der Paketierungsbericht und die Testnachweise liegen separat vor.

Öffentliche Ausgabe ausschließlich als Prerelease im vorhandenen Testkanal. Stabil bleibt 11.0.4. Öffentliche Datei-, Signatur- und Kanalkontrolle folgt nach Upload in einem getrennten Veröffentlichungsbericht; dieser lokale Prüfbericht behauptet noch keine öffentliche Nachprüfung.

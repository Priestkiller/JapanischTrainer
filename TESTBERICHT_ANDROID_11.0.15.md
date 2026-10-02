# Android 11.0.15 – Bedienkorrekturen und Fehlerwiederholung

## Abschließender Stand nach der Veröffentlichung

Android 11.0.15 ist als Prerelease veröffentlicht und öffentlich geprüft. 71 JavaScript-, 21 Python-, 22 native Android-Prüfungen und 682 Browseransichten bestanden. Alle 19 öffentlichen Dateien stimmen bei Größe und SHA-256; 15 getrennte Profil-/Formatfälle prüfen die Updateanzeige mit realen Manifesten und simulierter Brücke. Die native HTTPS-Prüfung lief vor dem Upload. Reale S24-, Mikrofon-, Hör-, Anfänger- und menschliche Sprachprüfung bleiben offen.

Finale APK: 88293243 Bytes, SHA-256 f65f3fa9164ae1c884edf5d7f0c44b41da12b8d519e40e467daea215c3d2d34b. Sie wurde aus der frischen CI-Release-APK signiert. Alle 254 Programmeinträge stimmen bytegenau mit CI überein; nur die Herausgebersignatur kommt hinzu. Ein abweichender lokaler Build mit alter Versionskonstante wurde vor Veröffentlichung verworfen.

[Download](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.15-1). Details: VEROEFFENTLICHUNG_ANDROID_11.0.15_TEST.md. Die folgenden Hinweise zu noch ausstehenden Prüfungen beziehen sich auf den damaligen lokalen Zwischenstand; die abschließenden Nachweise haben Vorrang. Stabil bleibt 11.0.4, Windows-Test 11.0.11.

Stand: 2. Oktober 2026. Version 11.0.15-android.1-test, Code 11001501,
Paket de.priestkiller.japanischtrainer. Ausschließlich autorisierter Testkanal.

## Erfasste Ursachen und Änderungen

Die Reproduktion mit separaten Profilen und vier Formaten zeigte: In 11.0.14
existierte die Auswahlhilfe nach drei Fehlversuchen, ihr Button lag aber in einem
auf null beziehungsweise wenige Pixel geschrumpften Inhaltsbereich. Sie wurde
nicht durch einen fehlenden Schwellenwert verhindert. Der Button liegt jetzt im
festen Aktionsbereich. Auswahl, ausdrückliche Bestätigung, Vormerkung freiwilligen
Sprechens und gekennzeichnete Kana-Selbstprüfung bleiben erhalten. Nach einer
qualifizierten Kana-Aufnahme öffnet eine feste Aktion deren Erklärung und Bestätigung.
Ab dem dritten Versuch bleibt sie innerhalb der Auswahlhilfe verfügbar. Bei ihrer
Bestätigung schließt der Dialog; die Speicherung nennt ausdrücklich self_check.

CSS-Textspalten teilten Antwortgruppen und lange Rückmeldungen auf. Das automatische
Umschalten zur Rückmeldung verdeckte dabei andere Antworten; bei kleiner Ansicht
lagen Teile auf einer weiteren Seite. Ganze Originalelemente werden jetzt auf
explizite Ansichten verteilt, ohne Antwortfelder zu zerschneiden. Nach einer Antwort
bleibt die Ansicht stehen. Rückmeldung, Hinweis und Erklärung sind bewusst aufrufbar.
Bei einem einzelnen zu großen Inhalt gibt es begrenztes Scrollen innerhalb seiner
Ansicht; die festen Aktionen bleiben erreichbar. Die echte Antwortzahl wird genannt:
drei oder vier ist je nach Aufgabe fachlich vorgesehen, kein künstlicher vierter
Eintrag. Hilfen schalten keine Aufgabe frei.

Bedeutung, Hörverstehen, Bausteine, Schreiben und Anwenden merken tatsächliche
falsche Antworten einmal je ursprünglicher Aufgabe vor. „Weiter · am Ende wiederholen“
setzt die Runde fort. Am Ende kommt dieselbe Aufgabenart mit derselben Karte und
beim Hörverstehen derselben gehörten Form zurück. Erst richtig gelöste Wiederholungen
und die bestehende Abschlussrunde schließen die Lektion ab. Erneute Fehler dürfen
wieder ans Ende. Korrektur an Ort und Stelle bleibt möglich; die bereits falsch
beantwortete Aufgabe wird dennoch am Ende wiederholt. Hinweise, fehlendes Audio,
Abbruch und technische Sprechfehler erzeugen keine solche Lernfehlerliste.

Die additive Speicherung retry_tasks/deferred/retry_total/retry_passed erhält
FLOW_REVISION 2, Kursrevision 11, Reihenfolge und IDs. Alte Profile ohne neue Felder
behalten ihre gültige Lernphase. Unerfüllte oder ungültige Schritte werden weiterhin
zurückgewiesen. XP nur einmal beim tatsächlichen Abschluss. Dies ist Android-Verhalten;
Windows behält seinen vorhandenen Ablauf mit Verstehen und freiwilligem Sprechen.

## Kurskorrektur und sprachliche Einordnung

Konkret geändert: 0:0:0 bis 0:0:4 und v11:long-vowels:0 bis :4, dazu jeweils
study_guide.points[0]. Erhalten: Zeichen, Romaji, Bedeutungen, Beispiele, Kartenanzahl,
Lektions-IDs, XP, Voraussetzungen und Reihenfolge. Deutlicher werden die Frage nach
dem jeweiligen Laut, der Vergleich kurzer/langer Vokale und die Bedeutungen
Tante/Großmutter/Onkel/Großvater. Alle falschen Anwendungsantworten erhalten passende
Begründungen. Keine neuen Lektionen: 150 Lektionen, 680 Karten, 156 Zusatzaufgaben.
Inhaltsstand 11.0.7 und Revision 11 bleiben für diese begrenzte Formulierungskorrektur
bestehen; die ausgelieferte Android-Version und der Quellcommit identifizieren sie.
Die gemeinsamen Quelldaten sind auch für einen späteren Windows-Build korrigiert;
es wurde mit diesem Handyauftrag keine neue Windows-EXE veröffentlicht.

Erfassung, eigene sprachliche Durchsicht und Softwaretests sind getrennt von einer
menschlichen Japanisch-Fachabnahme. Sachliche Grundlage für Mora und Vokallänge:
[Japan Foundation Sydney, Teachers’ notes on mora](https://classroomresources.sydney.jpf.go.jp/jpfmedia/Teacher%27s%20notes%20on%20mora.pdf)
und [MARUGOTO+ A1, Aussprache](https://a1.marugotoweb.jp/en/introduction.php).
„Zählschritt“ ist eine Lernhilfe, keine feste Sekundenzahl oder vollständige
phonetische Beschreibung. Natürliche Sprachdauer, Kontext und deutsche Näherungen
bleiben Gegenstand der noch offenen Fach- und Hörprüfung.

Die älteren Schutztests verglichen unveränderte vollständige Lektionshashes und
schlugen wegen dieser ausdrücklich gewünschten Korrektur an. Ein präziser
Vorher-/Nachher-Vertrag enthält ausschließlich die 68 tatsächlich geänderten Felder
der zwei Lektionen. Nur diese exakt erwarteten Felder werden für alte Hashprüfungen
zurückgerechnet; alle übrigen Inhalte und Identitäten bleiben geschützt. Ältere
Autorenwerkzeuge müssen die aktuellen Daten erhalten. Zeilenenden werden bei deren
Idempotenzprüfung plattformneutral verglichen.

## Ausgeführte Prüfungen vor Build und nativer Prüfung

71 JavaScript-Prüfungen bestanden, darunter Lösbarkeit aller 150 Lektionen und neue
Fälle für fünf Fehlerarten, Hörziel, Queue, Neustart, alte Profile, ungültige Daten
und einmalige XP. Die gezielte Browserprüfung besteht in sechs Formaten einschließlich
320×640, Querformat und 160 Prozent Schrift: 36 Ansichten. Sie prüft tatsächliche
Touch-Trefferflächen statt erzwungener Klicks, alle vier Antworten, Hilfe-Seiten,
feste Auswahlhilfe nach drei Versuchen und Neustart, falsche/korrekte bestätigte
Auswahl, dieselbe Aufgabe am Ende und Abschluss erst nach erfolgreicher Wiederholung.
63 Figurenansichten erhalten alle acht Lehrer und tatsächlich veränderte Bildpixel;
85 Menü-/Lernansichten und 30 Kalender-/Abschlussansichten bestanden ebenfalls.
300 Lernphasenansichten und alle 156 Zusatzaufgaben bestanden in fünf Formaten.
21 Python-Prüfungen bestanden: Inhaltspakete 2–4 (18), Grundlagen (2), Schutz von
Kurs, Bewertung und nativen Modellen (1). Die älteren Schutzvergleiche enthalten
zusätzlich die bereits ausgelieferten Kalenderfelder und Netzwerkfehlermeldungen
aus 11.0.13; diese nachweislich unveränderten Bereiche wurden an den vorhandenen
11.0.14-Stand angepasst. Ausschließlich die exakt dokumentierten neun geänderten
Session-Methoden werden für den historischen Ablaufvergleich zurückgerechnet;
Sprachvergleich, Kana-Selbstprüfung, TTS und Modelle bleiben gesondert geschützt.
Build-, Lint-, native und Paketprüfungen werden
mit ihren tatsächlichen Ergebnissen im ausgelieferten Bericht ergänzt. Sie gelten
hier noch nicht pauschal als bestanden.

Die neue Seitenaufteilung hatte zunächst Kontrollknöpfe vor der Ereignisbindung
vorübergehend aus dem DOM genommen; die Browserprüfung fand das. Die Elemente werden
jetzt synchron im Aufgabenbereich belassen. Der zuerst im Werkzeugbereich platzierte
Auswahlbutton wurde unten abgeschnitten und deshalb in die feste Aktionsleiste
verlegt. Drei neue Testauswahlen verwendeten zunächst ungeeignete Selektoren oder
einen nicht vorhandenen Antworttext; sie wurden auf exakte Texte und abgeschlossene
Layoutanordnung korrigiert. Ein Python-Start scheiterte am eingeschränkten temporären
Dateizugriff und wurde mit genehmigtem Prozesszugriff wiederholt. Ein weiterer gezielter Vergleich fand die ebenfalls verdeckte Kana-Selbstprüfung
in sechs Formaten. Die neue Dialogprüfung fand anschließend einen nach erfolgreicher
Selbstprüfung offenen Auswahlhilfedialog; dessen Abschluss wurde korrigiert. Der
finale Browserlauf besteht beide Kana-Wege. Das sind getrennte
Implementierungs-/Testfehlversuche, keine bestandenen Prüfungen des vorherigen Stands.

## Praktische Geräteprüfung, noch offen

Die ergänzende Tastaturprüfung fand einen tatsächlichen Fokusfehler: Beim erneuten
Seitenaufbau wurde das aktive Eingabefeld kurz aus dem DOM genommen. Die isolierte
Reproduktion verlor den Fokus bereits bei normaler Layoutberechnung und blendete
das Feld nach simulierter Tastaturverkleinerung aus. Aktive Eingabeseiten bleiben
jetzt verbunden; nur ihre Höhe und begrenzten Scrollpositionen werden angepasst.
Zwölf neue Browserfälle bestehen Haupt-/Zusatzaufgaben in sechs Formaten:
Fokus, vom Nutzer gesetzter Cursor, sichtbares Feld, Entwurf nach Neustart,
keine Freischaltung und unveränderte XP. Die bisherigen 670 Ansichten wurden nach
dieser Produktkorrektur vollständig erneut geprüft und bestanden: zusammen 682.
mobile/tests/keyboard-ui.mjs erhält die neue Regressionsprüfung dauerhaft.

Der zweite vollständige native Lauf auf 7459f85 bestand 20/22 Fälle, einschließlich
der sechs angepassten Hinweis-/Sichtbarkeitstests und echter öffentlicher HTTPS-Suche.
Der frühere HTTP-403-Fehler trat dort nicht auf; seine Ursache bleibt unbekannt.
Offen waren echte Android-Tastatur und Konfettimessung. Letztere verglich zwei
späte leere Momentaufnahmen der nur 3,2 Sekunden laufenden Szene. Der Test beobachtet
jetzt ab dem tatsächlichen Abschlussklick zwei verschiedene, nicht leere reale
Canvasbilder innerhalb der Szene. Animation und Dauer bleiben unverändert.
Der Tastaturtest wartet zusätzlich auf das tatsächlich treffbare Eingabefeld.
Ein vollständiger erneuter nativer Lauf muss diese Produktkorrektur bestätigen.
Der 20/22-Lauf zählt nicht als bestandene Abschlussprüfung.

Der vollständige native Erstlauf auf Quellstand 35193f2e besteht 15 von 22 Fällen.
Sechs ältere Fälle prüfen inzwischen absichtlich verdeckt gespeicherte Romaji
auf vollständige Abwesenheit im DOM oder erwarten den früheren Hinweis-Container.
Die Prüfungen werden auf tatsächlich sichtbare Lösungen und den bedienbaren
Hinweisdialog mit erhaltenen Aufgaben-/Profil-Gates umgestellt; Produktdateien
bleiben dabei unverändert. Der siebte Fehler ist ein HTTP 403 am öffentlichen
GitHub-API-Einstieg der nativen Updatesuche. Seine Ursache ist nicht nachgewiesen.
Ein neuer vollständiger Lauf muss einschließlich echter Updatesuche bestehen.
Der 15/22-Lauf zählt nicht als erfolgreiche Abschlussprüfung und gibt keine
Veröffentlichung frei. Nachweis: GitHub-Actions-Lauf 37055483430.

S24 Ultra: 11.0.15 über die vorhandene App installieren, XP, Lehrer und Sprachpaket
vergleichen. Lange-Vokale-Karte mit vier Antworten öffnen, jede erreichen, bewusst
falsch antworten, Weiter zur Endwiederholung wählen. App schließen, fortsetzen,
dieselbe Aufgabe lösen, Abschluss und einmalige XP prüfen. Drei echte erfolglose
Sprechversuche: Auswahlbutton muss unten sichtbar sein; erst korrekte Auswahl plus
Bestätigung darf weiterführen. Kana-Selbstprüfung nach qualifizierter Aufnahme separat
prüfen. Hoch-/Querformat, große Schrift, Rückmeldung und alle Hilfeseiten prüfen.
Echte Aufnahme-/Hörprüfung, Anfänger-Erprobung und menschliche Fachprüfung sind offen.


## Abgeschlossene Software- und Paketprüfung

Quellstand 5e216ebbe4ddf82a53995e8593b5152d8b93b8e5: 71 JavaScript-Prüfungen, 21 Python-Prüfungen und 682 Browseransichten bestanden. Alle 670 bisherigen Ansichten wurden nach der Fokuskorrektur erneut ausgeführt; zwölf zusätzliche Haupt-/Zusatzfälle prüfen Fokus, Cursor, Eingabe, Tastaturverkleinerung und Neustart. Vollständiger nativer Android-35-Lauf: 22/22 Fälle bestanden, keine Fehler oder übersprungenen Fälle. Darunter echte Bildschirmtastatur, sichtbare Drei-Versuche-Hilfe, bestätigte falsche/korrekte Auswahl, ursprüngliche Fehleraufgabe am Ende, Neustart, alte Profile, Kalender, Figuren, tatsächliche Konfettipixel, Abschluss, XP, Update-Kanaltrennung und echte lokale Modellverarbeitung synthetischen Audios. CI: https://github.com/Priestkiller/JapanischTrainer/actions/runs/37063057233 (Versuch 1). Das ist kein Mikrofon- oder menschlicher Sprachtest.

Build und Lint bestanden; lokal 11 und CI 12 Warnungen, jeweils 0 Fehler. Ein früherer Lauf scheiterte vor Testbeginn am beschädigten Download des Google-API-Systemabbilds; er ist kein bestandener nativer Nachweis. Der zweite Lauf wurde durch die zusätzliche Kana-Bedienkorrektur überholt und abgebrochen. Die lokale kanonische Asset-Vorbereitung wurde zunächst im falschen Arbeitsordner gestartet und danach erfolgreich korrigiert. Nur der erneute Build mit exakten Git-Assets wurde signiert. Der lokale Kotlin-Buildcache wurde außerhalb des Quellenarchivs aufbewahrt.

Ein vollständiger Erstlauf auf 35193f2e bestand 15/22 Fälle. Sechs alte Testannahmen betrafen bewusst verdeckt gespeicherte Romaji beziehungsweise den entfernten Hinweis-Container. Die nativen Assertions wurden auf sichtbare Lösungen und einen tatsächlich lesbaren Hinweisdialog mit erhaltenen Fortschritts-Gates umgestellt. Der siebte Fehler war HTTP 403 am öffentlichen GitHub-API-Einstieg, Ursache unbekannt. Der zweite vollständige Lauf auf 7459f85 bestand 20/22 einschließlich unveränderter echter HTTPS-Prüfung. Zwischen diesen beiden Ständen änderten sich nur Testadapter und Bericht.

Die beiden verbleibenden Fälle betrafen Tastatur und eine verspätete Konfettimessung. Die Browser-Reproduktion belegte einen Produktfehler: Seitenaufbau entfernte das aktive Feld und verlor den Fokus. focus-ui.mjs hält seine Seiten jetzt verbunden und passt Höhe/Scrollposition an. Eingabe und Cursor bleiben erhalten. Die Konfettiprüfung beobachtet seit dem echten Abschlussklick zwei verschiedene nicht leere Canvasbilder; Animation und 3,2-Sekunden-Dauer sind unverändert. Der finale vollständige Lauf besteht alle 22 Fälle. Weder 15/22 noch 20/22 zählen als erfolgreiche Abschlussprüfung.

APK: 88293243 Bytes, SHA-256 f65f3fa9164ae1c884edf5d7f0c44b41da12b8d519e40e467daea215c3d2d34b; Version 11.0.15-android.1-test, Code 11001501, Paket de.priestkiller.japanischtrainer. Bestehendes Herausgeberzertifikat, v3-Signatur und 16-KB-Alignment geprüft. 168 Kurs-/Web-/Bild-/Lizenzdateien und acht weitere Metadaten-/Hinweis-/Modellressourcen entsprechen bytegenau dem Quellcommit. Alle lokalen und CI-Assets sind bytegleich. Quellen und Lizenzunterlagen ohne Schlüssel, Zugangsdaten, private Lernstände oder Nutzeraufnahmen zusammengestellt.

Der abschließende Buildvergleich stoppte zunächst: Der lokale inkrementelle Kotlin-Build enthielt trotz korrektem Manifest noch eine Versionskonstante aus 11.0.14. DEX-Auswertung wies die Abweichung nach. Dieses Paket wurde nicht veröffentlicht. Die finale APK wurde stattdessen direkt aus der frischen Release-APK des erfolgreich geprüften CI-Laufs mit dem bestehenden Schlüssel signiert. Alle Programm-, Bibliotheks- und Ressourcen-Einträge stimmen bytegenau mit dessen APK überein; nur die Herausgebersignatur kommt hinzu. APK-Hash und Metadaten wurden neu erstellt.

Die öffentliche Abnahme steht bei Erstellung dieses Uploadpakets noch aus und wird nach dem tatsächlichen Upload im Veröffentlichungsbericht und der Projektchronik dokumentiert. Echte S24-, Mikrofon-/Hör-, Anfänger- und menschliche Fachprüfung bleiben offen. Keine neue Windows-EXE; deren veröffentlichter Teststand bleibt 11.0.11, stabil bleibt auf beiden Plattformen 11.0.4.

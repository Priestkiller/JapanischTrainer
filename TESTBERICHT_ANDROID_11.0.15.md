# Android 11.0.15 – Bedienkorrekturen und Fehlerwiederholung

Stand: 2. Oktober 2026. Version 11.0.15-android.1-test, Code 11001501,
Paket de.priestkiller.japanischtrainer. Ausschließlich autorisierter Testkanal.

## Erfasste Ursachen und Änderungen

Die Reproduktion mit separaten Profilen und vier Formaten zeigte: In 11.0.14
existierte die Auswahlhilfe nach drei Fehlversuchen, ihr Button lag aber in einem
auf null beziehungsweise wenige Pixel geschrumpften Inhaltsbereich. Sie wurde
nicht durch einen fehlenden Schwellenwert verhindert. Der Button liegt jetzt im
festen Aktionsbereich. Auswahl, ausdrückliche Bestätigung, Vormerkung freiwilligen
Sprechens und gekennzeichnete Kana-Selbstprüfung bleiben erhalten.

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
320×640, Querformat und 160 Prozent Schrift: 24 Ansichten. Sie prüft tatsächliche
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
Dateizugriff und wurde mit genehmigtem Prozesszugriff wiederholt. Das sind getrennte
Implementierungs-/Testfehlversuche, keine bestandenen Prüfungen des vorherigen Stands.

## Praktische Geräteprüfung, noch offen

S24 Ultra: 11.0.15 über die vorhandene App installieren, XP, Lehrer und Sprachpaket
vergleichen. Lange-Vokale-Karte mit vier Antworten öffnen, jede erreichen, bewusst
falsch antworten, Weiter zur Endwiederholung wählen. App schließen, fortsetzen,
dieselbe Aufgabe lösen, Abschluss und einmalige XP prüfen. Drei echte erfolglose
Sprechversuche: Auswahlbutton muss unten sichtbar sein; erst korrekte Auswahl plus
Bestätigung darf weiterführen. Kana-Selbstprüfung nach qualifizierter Aufnahme separat
prüfen. Hoch-/Querformat, große Schrift, Rückmeldung und alle Hilfeseiten prüfen.
Echte Aufnahme-/Hörprüfung, Anfänger-Erprobung und menschliche Fachprüfung sind offen.

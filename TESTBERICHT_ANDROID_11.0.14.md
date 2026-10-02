# Android 11.0.14 – Figuren und Abschluss (Testversion)

Stand: 2. Oktober 2026. Paket de.priestkiller.japanischtrainer; Version
11.0.14-android.1-test, Code 11001401. Veröffentlichen ausschließlich als
android-test-v11.0.14-1; stabile Ausgabe 11.0.4 wird nicht verändert.

## Umsetzung

Kiko feiert einen tatsächlichen Lektionsabschluss mit seinen vorhandenen acht
Jubelbildern, drei Sprüngen, Sternen und gezeichnetem Konfetti. Die Szene endet
nach 3,2 Sekunden; beide Abschlussaktionen sind sofort bedienbar. Im Querformat
stehen Figur und Ergebnis nebeneinander. Wiederholungen vergeben keine zweiten XP.
Auch ohne Kiko bleibt das tatsächliche Ergebnis sichtbar.

Der gewählte Lehrer begleitet den ersten Lernschritt, zusätzliche Sprechaufgaben,
Offline-Gespräche und den freiwilligen lokalen Modellvergleich. Die bestehenden
Figuren, Blink- und Mundbilder werden verwendet. Sprechblase und Darstellung
wechseln anhand von Wiedergabe, Mikrofonvorbereitung, Aufnahme, Erkennung und
tatsächlichem Aufgabenabschluss. Reaktion und Blinzeln sind Animationen, keine
phonetisch ausgerichtete Lippensynchronisation. Es entstehen keine neuen Stimmen,
Sprachmodelle oder Aussagen über verbesserte Erkennungsqualität.

Reduzierte Bewegung, die vorhandene Bewegungseinstellung, unsichtbare App und
verdeckt liegende Figuren halten Bewegungen an. Lernhilfen bleiben erreichbar.
Auf kleinen Displays und bei großer Schrift wird die Begleiterdarstellung kleiner,
damit die Aufnahme bedienbar bleibt. Folgephasen zeigen keine zusätzliche Vorlage.

Kurs, IDs, Speicherung und Update-Sicherheit sind unverändert: 150 Lektionen,
680 Karten, Revision 11, Inhaltsstand 11.0.7; 156 Zusatzaufgaben. Windows wird
durch diesen Android-Auftrag nicht geändert. Alte XP, Abschlüsse, Lehrerauswahl,
Lerntage und Sprachpakete bleiben im bestehenden Verfahren erhalten.

## Nachweise vor der nativen Abschlussprüfung

65 bestehende JavaScript-Funktionsprüfungen und eine zusätzliche Zustandsprüfung
bestanden. Die bisherigen 85 Menü-/Lernansichten und 30 Kalender-/Abschlussansichten
bestanden nach den Layoutkorrekturen. Die spezielle Figurenprüfung prüft alle acht
Lehrer in sechs Formaten mit separaten Profilen, Zustandswechseln, Aufnahme-Gate,
unveränderten XP und zwölf Abschlussansichten. Bestanden: 63 Ansichten (48 Lehrer-/Formatkombinationen, zwölf Abschlüsse und
drei Gesprächs-/Modellvergleichsansichten). Bewegung nach geschlossenen Hilfen,
endlicher Jubel und ausgeschaltete Bewegung wurden ebenfalls geprüft.

Diese Browserprüfungen verwenden eine simulierte native Brücke und sind keine
Mikrofontests. Die finalen nativen Emulator-, Paket-, Signatur- und öffentlichen
Prüfungen stehen bei Erstellung dieses Quellberichts noch aus. Ihre tatsächlichen
Ergebnisse werden dem ausgelieferten Bericht und der Chronik angefügt.

Die Sichtprüfung fand zunächst einen verdeckten Jubel im Querformat und eine nach
unten gedrängte Aufnahme bei großer Schrift. Die strengere Prüfung fand außerdem
eine ausgeblendete Querformat-Sprechblase und knapp verdeckte Lernhilfen. Beide
wurden mit einer kompakteren Kopfzeile und angepassten Abständen korrigiert. Die Szene wurde im Querformat
zweispaltig; bei großer Schrift wird der Lehrer kompakter. Ein Browser-Testadapter
hatte zunächst seine Capabilities-Methode nicht bereitgestellt; das war kein
Produktfehler. Eine Asset-Vorbereitung wurde zuerst aus dem falschen Arbeitsordner
und danach mit einem Python ohne Pillow gestartet; mit dem gebündelten Python
wurde sie erfolgreich wiederholt. Ein sandboxbedingter Browserstart lief mit
genehmigtem Prozesszugriff erfolgreich.

## Offene menschliche Prüfungen und Gerätecheck

Auf S24 Ultra: APK über die bestehende App installieren, Lernstand und Modelle
vergleichen. Gewählten Lehrer in einer Sprechübung prüfen; normal/ langsam hören,
aufnehmen, abbrechen und erneut versuchen. Eine echte Lektion abschließen: Kiko
jubelt, Weiterlernen ist währenddessen möglich. Wiederholung darf keine zweiten XP
bringen. Querformat, große Schrift, abgeschaltete Bewegung sowie Appwechsel prüfen.
Kalender und beide Updatesuchen prüfen; bei Netzfehler den genauen Meldungstext
notieren. Das ist eine praktisch ausführbare Prüfliste, kein bereits erfolgter Test.

Echte S24-, Mikrofon- und Lautsprechertests, Anfänger-Erprobung und menschliche
Japanisch-Fachprüfung bleiben offen. Die frühere S24-Updatesuchursache ist weiter
nicht nachgewiesen. Menschliche Sprach-/Anfängerprüfung ist keine Voraussetzung
für die ausdrücklich gekennzeichnete Testausgabe, aber wird nicht als bestanden
ausgegeben. Stabile Übernahme benötigt eine gesonderte Nutzerfreigabe.

## Orientierung

Eigene Figuren und Gestaltung; Duolingo dient als Funktionsreferenz:
[Figuren als Lernbegleiter](https://blog.duolingo.com/building-character/) und
[getrennte Körper-/Mundzustände](https://blog.duolingo.com/world-character-visemes/).
Es wurden keine Duolingo-Grafiken oder -Stimmen übernommen. Die bestehenden
Kiko-Erzeugungsangaben bleiben in mobile/ARTWORK_11.0.13.md erhalten; für diese
Ausgabe wurde kein neues Rasterbild erzeugt.

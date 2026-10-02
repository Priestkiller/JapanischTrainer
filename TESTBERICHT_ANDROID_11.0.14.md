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
Offline-Gespräche und den freiwilligen lokalen Modellvergleich. Alle acht Lehrer
erhalten neue vollständige Figuren mit Kopf, Händen, Beinen und Schuhen. Jeweils
16 gezeichnete Posen bilden vier Folgen: ruhig stehen/blinzeln, sprechen/erklären,
zuhören/nicken und lächeln/winken. Die Gesichter, Kleidung und Zubehör orientieren
sich an den bisherigen Figuren; die Originalbilder bleiben erhalten.
Sprechblase und Darstellung
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

Nach der Ergänzung vollständiger Körper bestanden 67 JavaScript-Prüfungen sowie
63 Figuren-, 85 Menü-/Lern- und 30 Kalender-/Abschlussansichten. Alle acht Bilddateien
wurden unverändert übernommen und insgesamt 128 Körperposen anhand ihrer
Alpha-Umrisse auf getrennte, vollständige Quellrechtecke geprüft.
Die spezielle Figurenprüfung prüft alle acht
Lehrer in sechs Formaten mit separaten Profilen, Zustandswechseln, Aufnahme-Gate,
unveränderten XP und zwölf Abschlussansichten: 63 Ansichten (48 Lehrer-/Formatkombinationen,
zwölf Abschlüsse und drei Gesprächs-/Modellvergleichsansichten). Zusätzlich prüft
sie tatsächlich wechselnde Körperbilder für jeden Lehrer und die vier Posenfolgen.

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
Kiko-Erzeugungsangaben bleiben in mobile/ARTWORK_11.0.13.md erhalten. Neue
Lehrerbilder, Referenzen, Generierungsaufträge und Pose-Geometrie sind in
mobile/ARTWORK_11.0.14.md beschrieben. Es handelt sich um gezeichnete Bildfolgen,
kein 3D-Rig. Die Bilddateien werden unverändert übernommen; tatsächliche Umrisse
statt eines angenommenen gleichmäßigen Rasters verhindern abgeschnittene Posen.


## Tatsächlich abgeschlossene Software- und Paketprüfung

Endgültiger Quellstand ea178aaaac44b7a53fe315565a3ed7b89cf10296: Build und Lint bestanden, 67 JavaScript-Prüfungen,
63 spezielle Figuren-/Abschlussansichten, 85 Menü-/Lernansichten und 30 Kalender-/
Abschlussansichten bestanden. Die 21 erforderlichen nativen Fälle bestanden über
zwei Läufe: 20 unveränderte Fälle des vollständigen Laufs und ein gezielt
wiederholter korrigierter Figurentest. Die Produktdateien und die übrigen
20 Testmethoden sind nachweislich bytegleich. Geprüft sind:
gewählter Lehrer, Bewegung aus, tatsächlich veränderte Konfettipixel, Abschluss,
Wiederholung ohne neue XP, alte Profile, Neustart, Kalender und Update-Kanaltrennung.
CI: https://github.com/Priestkiller/JapanischTrainer/actions/runs/37021676648. Alle acht Lehrer besitzen je 16 vollständige Körperposen. Echte
Pixeländerungen und Zustandsfolgen wurden für alle acht im Browser und für Ren in
der nativen WebView geprüft. Lint: lokal 11 und CI 12
Warnungen; jeweils 0 Fehler. Zwei frühere Läufe wurden wegen Layoutkorrekturen und
der nachträglichen Körperergänzung ersetzt, keiner zählt als endgültiger Nachweis.
Zwei vollständige Körperläufe bestanden jeweils 20/21 Fälle. Das neue Testprofil
enthielt keine verpflichtende completed-Liste und wurde korrekt zurückgewiesen;
dadurch erschienen Sakura und 0 XP. Zusätzlich verglich der Test einen JavaScript-
Textwert ohne dessen JSON-Kodierung. Beides wurde in der Fixture behoben.
Die erste Vermutung eines fehlenden Sprachpakets war nicht die beobachtete Ursache;
der separate Vergleich mit/ohne Modellpaket prüft nur das allgemeine Aufnahme-Gate.
Der gezielte letzte Lauf besteht den korrigierten Fall; die 20 übrigen Methoden
und alle Produktdateien blieben unverändert und wurden nicht erneut ausgeführt.
Vollständiger Lauf: https://github.com/Priestkiller/JapanischTrainer/actions/runs/37016686960. Die signierte APK bleibt bytegleich.
Ein gezielter Versuch scheiterte vor Testbeginn am mehrzeiligen CI-Kommando.
Das Kommando wurde für den Emulator-Runner repariert und erneut ausgeführt.

Die native HTTPS-Suche nutzt die echte öffentliche Quelle und erhält den Lernstand.
Vor dem Upload war auf 11.0.14 kein höheres Angebot vorhanden. Die native Modell-
prüfung verwendet synthetisches Audio, keine menschliche Mikrofonaufnahme. Browser-
Audiozustände sind simuliert; die Prüfung ist ausdrücklich keine Ausspracheprüfung.
Windows-/Python-Tests wurden bei unveränderten Windows-/Kursquellen nicht wiederholt.

APK: 88289077 Bytes, SHA-256 831f767766c65a01aa661ae6da408b2a55aa6c95cb46ae3b0eeb2f0c3cf1b347; bisheriger Herausgeber,
v3-Signatur, Paket de.priestkiller.japanischtrainer, Code 11001401, 16-KB-Alignment.
167 Kurs-/Grafik-/Web-/Lizenzdateien entsprechen bytegenau
dem Quellcommit; zusätzlich acht Metadaten-/Hinweis-/Modellressourcen. Alle
mitgelieferten CI- und lokalen Assets sind bytegleich. Nur für
den Build wurden Windows-Zeilenenden an die Git-Quellen angeglichen. Die Paketierung
hatte zunächst die unveränderten Grafikhinweise fälschlich als neue Artwork-Datei
erwartet; der Verweis wurde auf die erhaltene 11.0.13-Datei korrigiert. Quellen und
Lizenzunterlagen wurden ohne private Schlüssel, Zugangsdaten, Nutzerstände oder
Aufnahmen zusammengestellt. Die öffentliche Nachprüfung folgt nach Upload.

Offen bleiben echte S24-, Mikrofon-/Lautsprechertests, Anfänger-Erprobung und
menschliche Japanisch-Fachprüfung sowie die konkrete frühere S24-Netzursache.


## Öffentliche Nachprüfung abgeschlossen

Am 2. Oktober 2026 wurden alle 16 öffentlichen Dateien einschließlich des
ergänzten Veröffentlichungsberichts mit Größe und SHA-256 abgeglichen. Die
öffentliche APK besteht Signatur-, Version-, Paket- und Quellenprüfung. Zwölf
separate Updateprofil-/Formatkombinationen bieten 11.0.14 ausschließlich im
Testkanal an; auf 11.0.14 ist ohne höhere Ausgabe kein Angebot vorhanden.
Die native Brücke ist in diesen Browserprüfungen simuliert; dies ist kein S24-Test.
Alle 25 bisherigen Veröffentlichungen mit 258 Dateien bleiben unverändert,
Latest bleibt v11.0.4. Die lokale Lieferung unter
F:/Japanischtool/Testpakete/11.0.14/android/ ist bytegleich zu den öffentlichen
Downloads. Details: VEROEFFENTLICHUNG_ANDROID_11.0.14_TEST.md.

Dieser nachträgliche Dokumentationsstand ergänzt die historischen Angaben.
APK, Quellpaket und Veröffentlichungstag behalten den geprüften Commit
ea178aaaac44b7a53fe315565a3ed7b89cf10296. Veröffentlichte Dateien werden nicht
nachträglich ersetzt. Echte S24-, Mikrofon-/Hör- und menschliche Prüfungen bleiben offen.

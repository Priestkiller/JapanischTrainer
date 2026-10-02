# JapanischTrainer 11.0.14 Android – TESTVERSION

Kiko feiert abgeschlossene Lektionen mit Bewegungsbildern, Sprüngen, Sternen und
Konfetti. Du kannst sofort weiterlernen; die Feier endet nach 3,2 Sekunden.
Wiederholungen vergeben keine zweiten Abschluss-XP.

Alle acht Lehrer bekommen vollständige Körper einschließlich Füßen und je 16
gezeichnete Posen für ruhiges Stehen, Erklären, Zuhören und Winken. Dein gewählter
Lehrer begleitet die Sprechübungen sichtbar mit einer Sprechblase und reagiert
auf Vorlesen, Aufnahme und Aufgabenabschluss. Auch Offline-Gespräche und der
freiwillige Sprachvergleich nutzen diese Figuren. Bewegung lässt
sich abschalten; die Android-Einstellung für reduzierte Bewegung wird beachtet.

Kurs, Lernstand, Modelle und Stimmen behalten das bestehende Verfahren. Die
Animation bewertet keine Aussprache und ist nicht phonetisch lippensynchron.
Die reguläre Updatesuche bleibt vom Testkanal getrennt. Kein automatischer
Download oder automatische Installation.

**Offen:** echte S24-, Mikrofon-/Lautsprechertests, Anfänger-Erprobung und
menschliche Japanisch-Fachprüfung. Die genaue Ursache der früheren S24-Suchmeldung
ist weiterhin offen. Software- und Paketnachweise stehen im mitgelieferten Bericht.

APK über die vorhandene App installieren; nicht vorher deinstallieren.
Diese Ausgabe ist ein Prerelease und ersetzt die stabile Version 11.0.4 nicht.


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

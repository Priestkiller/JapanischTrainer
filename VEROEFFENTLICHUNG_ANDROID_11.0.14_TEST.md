# Veröffentlichung Android 11.0.14 Testversion

Abschluss der Prüfung am 2. Oktober 2026. Android 11.0.14-android.1-test, Code
11001401, Paket de.priestkiller.japanischtrainer. Ausschließlich Prerelease
android-test-v11.0.14-1. Latest und stabile Veröffentlichungen bleiben 11.0.4;
Windows bleibt Test 11.0.11. Eine stabile Übernahme ist nicht freigegeben.

Geprüfter Quellstand: ea178aaaac44b7a53fe315565a3ed7b89cf10296.
[Endgültiger Android-Prüflauf](https://github.com/Priestkiller/JapanischTrainer/actions/runs/37021676648).

## Tatsächlich umgesetzt

Alle acht Lehrer (Sakura, Aiko, Haruto, Ren, Miyako, Emiri, Satoshi und Yuki)
erhalten vollständige Körper mit Händen, Beinen und Schuhen. Je 16 Posen bilden
vier Folgen: Ruhen/Blinzeln, Erklären, Zuhören/Nicken und Freude/Winken. Die
ausgewählte Figur begleitet Sprechübungen, Zusatzaufgaben, Offline-Gespräche und
den Modellvergleich; auch die Startseite verwendet die vollständige Körpergrafik.
Die Zustände folgen tatsächlichen Wiedergabe-, Aufnahme- und Erkennungsereignissen.
Es gibt keine behauptete phonetische Lippensynchronisation oder Aussprache-Note.

Eigene transparente Bilder wurden mit der integrierten Bildgenerierung anhand
der vorhandenen Lehrer erstellt. Aufträge und Herkunft stehen im Quellenarchiv
unter mobile/ARTWORK_11.0.14.md. Die PNGs wurden unverändert kopiert; geprüfte
Alpha-Umrisse bestimmen 128 separate Quellrechtecke mit gemeinsamem Boden und
Maßstab. Köpfe, Hände und Füße bleiben sichtbar. Einzelne Zeichnungsdetails
variieren zwischen den Posen; eine menschliche Sichtprüfung auf dem S24 bleibt offen.

Kiko feiert echte Lektionsabschlüsse mit acht vorhandenen Jubelbildern, Sprüngen,
Sternen und Konfetti. Die Szene endet nach 3,2 Sekunden. Beide Abschlussaktionen
sind sofort erreichbar; Wiederholungen vergeben keine erneuten XP. Reduzierte
oder ausgeschaltete Bewegung, verdeckte Figuren und unsichtbare App halten an.
Kleine Bildschirme, Querformat und große Schrift erhalten kompaktere Darstellungen.

Kurs, IDs, Speicherung, Lehrerwahl, Stimmen, Sprachmodelle und Update-Sicherheit
bleiben erhalten: 150 Lektionen, 680 Karten, Revision 11, Inhalt 11.0.7;
105 Lektionen mit 501 Karten vertieft, 156 Zusatzaufgaben. Sechs Lernschritte,
gekennzeichnete Kana-Selbstprüfung und Sprechhilfe bleiben bestehen.

## Tatsächlich ausgeführte Softwareprüfungen

67 JavaScript-Tests und 178 Browseransichten bestanden: 63 Figuren-/Abschlussansichten,
85 Menü-/Lernansichten und 30 Kalender-/Abschlussansichten. Alle acht Lehrer wurden
in sechs Größen-/Schrift-/Bewegungsformaten geprüft, einschließlich tatsächlich
veränderter Körperpixel, Lernhilfen, Sprechblasen und erreichbarer Aufnahme.
Separate Profile bleiben erhalten, Folgephasen zeigen keine große Figur und
keine dauerhaft eingeblendeten Lösungen. Browser-Sprachereignisse waren simuliert.

Die 21 erforderlichen nativen Android-Fälle bestanden über zwei Läufe:
20 unveränderte Fälle des vollständigen Laufs und ein gezielt wiederholter
korrigierter Figurentest. Die Produktdateien und übrigen 20 Testmethoden
sind nachweislich identisch. Sie prüfen unter anderem
Ren mit vollständigem Körper und tatsächlichen Pixeländerungen, Bewegung aus,
Konfetti, Abschluss, Wiederholung ohne erneute XP, alte Profile, Neustart,
Kalender und Android-HTTPS-Updatesuche gegen die echte öffentliche Quelle.
Der Zustandswechsel im Figurentest ist eine Testfixture. Modellprüfungen
verarbeiten synthetisches Audio. Emulator API 35 x86_64, kein Mikrofon- oder S24-Test.

Build und Lint bestanden: 0 Fehler, lokal 11 und CI
12 Warnungen. Windows-/Python-Tests wurden bei unveränderten
Windows- und Kursquellen nicht erneut ausgeführt. Zwei frühere CI-Läufe wurden
wegen Layoutkorrekturen beziehungsweise der vollständigen Körperergänzung ersetzt;
sie zählen nicht als endgültiger Nachweis.
Zwei vollständige Körperläufe bestanden jeweils 20/21 Fälle. Im neuen Testprofil
fehlte die verpflichtende completed-Liste; die App wies das ungültige Profil
korrekt zurück und zeigte Sakura und 0 XP. Hinzu kam ein falsch verglichener
JSON-kodierter JavaScript-Text. Testprofil und Vergleich wurden korrigiert.
Die erste Vermutung zum Modellpaket war nicht die beobachtete Ursache.
Der gezielte letzte Lauf besteht den korrigierten Fall; die anderen 20 Tests
und sämtliche Produktdateien blieben unverändert und wurden nicht nochmals
ausgeführt. [Vollständiger Lauf mit 20 gültigen Fällen](https://github.com/Priestkiller/JapanischTrainer/actions/runs/37016686960).
Ein gezielter Versuch scheiterte vor Testbeginn am CI-Shellkommando; das reparierte
Einzelkommando wurde erneut ausgeführt. Dieser Fehlversuch zählt nicht als Test.
Ein separater Browservergleich mit und ohne Modellpaket bestand die jeweiligen
Aufnahme-Gates; die nativen Brücken waren dort simuliert. Dieser Vergleich
erklärt nicht den Fehler des unvollständigen Testprofils.
Verdeckte Sprechblasen, Lernhilfen,
Aufnahme und Abschluss im Querformat wurden gefunden, korrigiert und erneut geprüft.
Ein blockierter Node-Unterprozess bestand nach autorisierter Prozessfreigabe.

## Paketprüfung und öffentliche Downloads

APK: 88289077 Bytes.
SHA-256: 831f767766c65a01aa661ae6da408b2a55aa6c95cb46ae3b0eeb2f0c3cf1b347.
Gültige v3-Signatur, bisheriges Herausgeberzertifikat
3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9, unveränderte Paketkennung, Code 11001401 und
16-KB-Alignment. v2 wird bei der bestehenden Mindestversion nicht verwendet.
Alle 167 Kurs-/Grafik-/Web-/Lizenzdateien und acht
weitere Metadaten-/Hinweis-/Modellressourcen entsprechen exakt dem geprüften Git-
Stand und Quellenarchiv. Sämtliche lokalen und CI-Assets sind bytegleich.
Nur für den Build wurden Windows-Zeilenenden angeglichen.

Alle zunächst 14 öffentlichen Dateien wurden anonym geladen
und anhand Größe und SHA-256 mit lokalen Paketen verglichen. Die öffentliche APK
bestand zusätzlich Signatur, Herausgeber, Version, Paketkennung, Alignment und
Quellenabgleich. Quellen, Lizenzunterlagen und bereinigte Prüfnachweise enthalten
keine privaten Schlüssel, Zugangsdaten, persönlichen Lernstände oder Aufnahmen.
Die Nachprüfung wurde
mit dem gebündelten Python wiederholt, nachdem dem zuerst verwendeten System-
Python die Signaturbibliothek cryptography fehlte. Der erste Aufruf erreichte
keinen Download und zählt nicht als erfolgreiche Prüfung. Dieser Abschlussbericht
und sein eigener Prüfsummennachweis werden ergänzend hochgeladen; anschließend
wird der Gesamtbestand erneut geprüft. Erstdaten,
signierte APK und frühere Veröffentlichungen werden nicht überschrieben.

Die echten öffentlichen Versionsdateien bieten Android 11.0.4, 10, 11, 12 und 13
nur im Testkanal 11.0.14 an. Auf 14 sind beide Suchen leer. Zwölf isolierte Profil-
und Formatkombinationen bestanden die produktiven Updatebuttons mit den echten
Manifestdaten und einer simulierten nativen Brücke: Lernstände bytegleich, kein
automatischer Download oder Installation. Die unveränderte Windows-Suche bietet
auf 11.0.11 weder eine höhere stabile noch höhere Testversion. Die native Android-
HTTPS-Prüfung erfolgte vor dem Upload; die Nachprüfung ersetzt keinen S24-Netzversuch.

Alle 25 früheren Releases mit
258 Dateien bleiben unverändert (IDs, Status, Namen,
Größe, Digest und URL). Latest bleibt v11.0.4.

## Eigene Sichtprüfung und offene menschliche Prüfung

Eigene Sichtprüfung: alle acht vollständigen Bildraster und tatsächlich gerenderte
Sprech-/Abschlussansichten einschließlich Querformat, großer Schrift und kleiner
Höhe. Das ist keine menschliche Anfänger- oder sprachliche Fachabnahme. Echte
S24-Installation, Mikrofon-/Hörprüfung, Anfänger-Erprobung und Japanisch-Fachprüfung
bleiben offen. Die frühere S24-Netzursache und bessere Erkennungsqualität sind
nicht nachgewiesen. Stimmen und Modelle wurden durch diesen Auftrag nicht ersetzt.

## Praktische Geräteprüfung

1. Auf dem S24 Ultra die APK über die vorhandene App installieren; Version 11.0.14,
   bisherigen Lernstand, ausgewählten Lehrer und Sprachpakete vergleichen.
2. Alle gewünschten Lehrer in einer Sprechübung prüfen: Kopf, Hände und Füße
   vollständig, Sprechblase lesbar, normales/langsames Vorlesen und Aufnahme bedienbar.
3. Echte Aufnahme starten, abbrechen und erneut versuchen. Nur reale Ereignisse
   dürfen die Figur wechseln; technische Erkennung ist keine Aussprache-Note.
4. Lektion abschließen und während Kikos Jubel weiterlernen. Wiederholung darf
   keine erneuten XP vergeben. Kalender zeigt weiterhin echte Lerntage.
5. Querformat, große Schrift, Bewegung aus/reduziert und Appwechsel prüfen.
6. Beide Updatesuchen ausführen. Auf 11.0.14 ist ohne höhere Ausgabe ein leeres
   Ergebnis richtig. Bei Netzfehler die genaue Meldung festhalten.
7. Auf einem frischen Windows-System bleibt die bisherige 11.0.11 zuständig;
   dieses reine Android-Paket enthält keine neue EXE.

## Download und Nachweise

[Android APK](https://github.com/Priestkiller/JapanischTrainer/releases/download/android-test-v11.0.14-1/JapanischTrainer-11.0.14-Android.apk)
und [Testveröffentlichung](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.14-1).

Lokale Lieferung: F:/Japanischtool/Testpakete/11.0.14/android/.
Nachweise: validation/public-1114/, validation/ci-1114-final/, validation/characters-1114/.
Zentrale Chronik und Word-Ausgabe: F:/Japanischtool/PROJEKTDOKUMENTATION_JapanischTrainer.
Eine spätere stabile Übernahme benötigt weiterhin deine ausdrückliche Freigabe.

# Veröffentlichung Android 11.0.15 Testversion

## Abschließender Stand nach der Veröffentlichung

Android 11.0.15 ist als Prerelease veröffentlicht und öffentlich geprüft. 71 JavaScript-, 21 Python-, 22 native Android-Prüfungen und 682 Browseransichten bestanden. Alle 19 öffentlichen Dateien stimmen bei Größe und SHA-256; 15 getrennte Profil-/Formatfälle prüfen die Updateanzeige mit realen Manifesten und simulierter Brücke. Die native HTTPS-Prüfung lief vor dem Upload. Reale S24-, Mikrofon-, Hör-, Anfänger- und menschliche Sprachprüfung bleiben offen.

Finale APK: 88293243 Bytes, SHA-256 f65f3fa9164ae1c884edf5d7f0c44b41da12b8d519e40e467daea215c3d2d34b. Sie wurde aus der frischen CI-Release-APK signiert. Alle 254 Programmeinträge stimmen bytegenau mit CI überein; nur die Herausgebersignatur kommt hinzu. Ein abweichender lokaler Build mit alter Versionskonstante wurde vor Veröffentlichung verworfen.

[Download](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.15-1). Details: VEROEFFENTLICHUNG_ANDROID_11.0.15_TEST.md. Die folgenden Hinweise zu noch ausstehenden Prüfungen beziehen sich auf den damaligen lokalen Zwischenstand; die abschließenden Nachweise haben Vorrang. Stabil bleibt 11.0.4, Windows-Test 11.0.11.

Abschluss der öffentlichen Prüfung am 2. Oktober 2026. Version
11.0.15-android.1-test, Code 11001501, Paket de.priestkiller.japanischtrainer.
Prerelease android-test-v11.0.15-1; ausschließlich im bestehenden Testkanal.
Latest und beide stabilen Ausgaben bleiben 11.0.4. Windows bleibt Test 11.0.11;
dieser Handyauftrag erstellt keine neue EXE. Stabile Übernahme ist nicht freigegeben.

Geprüfter Quellstand: 5e216ebbe4ddf82a53995e8593b5152d8b93b8e5.
[Vollständiger Android-Prüflauf](https://github.com/Priestkiller/JapanischTrainer/actions/runs/37063057233) (Versuch 1).

## Erfasste Probleme und tatsächlich umgesetzt

11.0.14 reproduzierte in vier Formaten eine vorhandene, aber auf null oder wenige
Pixel geschrumpfte Drei-Versuche-Hilfe. Ihr Button liegt jetzt fest unten. Nach
drei erfolglosen Versuchen öffnet er die passende Wortauswahl. Erst richtige Auswahl
und ausdrückliche Bestätigung erlauben das Weitergehen. Sprechen bleibt für später
vorgemerkt. Technische Fehler sind keine Aussprache-Note. Der Zustand bleibt nach
Neustart erhalten. Die Aufnahmevoraussetzungen und der Sprachvergleich bleiben gleich.

Auch die gekennzeichnete Kana-Selbstprüfung war verdeckt. Nach einer qualifizierten
Aufnahme ist sie über eine feste Aktion erreichbar; ab dem dritten Versuch zusätzlich
innerhalb der Auswahlhilfe. Eine erfolgreiche Selbstbestätigung schließt den Dialog
und wird separat als Selbstprüfung gespeichert. Sie ist nicht vorher freigeschaltet.

CSS-Textspalten fragmentierten Antworten und lange Rückmeldungen; die automatische
Rückmeldungsanzeige wechselte ungewollt die Ansicht. Ganze Originalelemente werden
jetzt ausdrücklich auf Seiten verteilt, ohne ihre Ereignisbindung zu verlieren.
Alle vorgesehenen Antworten bleiben erreichbar, auch nach einer falschen Auswahl.
Die tatsächliche Zahl wird genannt: manche Aufgaben haben drei, andere vier Antworten.
Es gibt keine zusätzliche künstliche Antwort nur für eine einheitliche Zahl.
Rückmeldung und Lernhilfen sind bewusst aufrufbar; Hilfe allein gibt nichts frei.
Sehr lange Einzelinhalte dürfen innerhalb ihrer Ansicht scrollen; Aktionen bleiben fest.

Fehler in Bedeutung, Hörverstehen, Bausteinen, Schreiben und Anwenden werden einmal
je ursprünglicher Aufgabe vorgemerkt. Man kann erneut antworten oder mit
„Weiter · am Ende wiederholen“ fortsetzen. Am Ende kehrt dieselbe Aufgabe zurück,
beim Hörverstehen einschließlich des ursprünglichen Hörziels. Erneute Fehler dürfen
wieder ans Ende. Erst gelöste Wiederholungen und die bestehende Abschlussrunde
schließen die Lektion ab und vergeben einmalige XP. Hinweise, fehlendes Audio und
technische Sprechfehler erzeugen keine solche Lernfehlerliste.

## Kurskorrekturen und Fortschrittsübernahme

Zehn vorhandene Karten in zwei Lektionen wurden klarer formuliert:
0:0:0 bis 0:0:4 (A, I, U, E, O) und v11:long-vowels:0 bis :4
(Kurz oder lang? Vokale unterscheiden). Beide Einführungen erklären den Sprechtakt
als gleichmäßigen Zählschritt. Fragen benennen den konkreten Laut und seinen Bezug;
Antworten und Fehlererklärungen beschreiben kurz/lang beziehungsweise
Tante, Großmutter, Onkel und Großvater verständlicher. 68 exakt dokumentierte Felder
ändern sich, keine Bedeutungen, Schriftzeichen, Beispiele oder Identitäten daneben.

Grundlage der eigenen sprachlichen Durchsicht:
[Japan Foundation Sydney, Teachers’ notes on mora](https://classroomresources.sydney.jpf.go.jp/jpfmedia/Teacher%27s%20notes%20on%20mora.pdf)
und [MARUGOTO+ A1, Aussprache](https://a1.marugotoweb.jp/en/introduction.php).
Ein Zählschritt ist keine feste Sekundenzahl. Natürliche Dauer, Kontext und deutsche
Aussprache-Näherungen bleiben Gegenstand der offenen menschlichen Fach-/Hörprüfung.
Eigene Durchsicht ist keine menschliche Fachabnahme.

Keine neuen Lektionen oder IDs: 150 Lektionen, 680 Karten, 156 Zusatzaufgaben;
105 Lektionen mit 501 Karten vertieft. Kursrevision 11 und Inhaltsstand 11.0.7 bleiben
bei diesen begrenzten Formulierungskorrekturen erhalten. Der App-/Quellstand kennzeichnet
die Änderung. Die gemeinsame Kursquelle erhält sie auch für spätere Windows-Builds.
Der Windows-Ablauf mit Verstehen und freiwilligem Sprechen bleibt unverändert.

FLOW_REVISION bleibt 2. Die Fehlerliste sind zusätzliche Profilfelder, keine
Umnummerierung oder erzwungene Rücksetzung. Alte Profile behalten gültige Phasen,
XP, Abschlüsse und Lehrerwahl. Ungültige Wiederholungsdaten schalten nichts frei.
Lehrer, Animationen, Stimmen, Sprachmodelle, Paketkennung, Signierschlüssel und
Update-Sicherheit wurden nicht umgebaut. Eine bessere Erkennungsqualität ist damit
nicht behauptet.

## Tatsächlich ausgeführte Softwareprüfungen

71 JavaScript-Prüfungen und 21 Python-Prüfungen bestanden: 18 Inhaltspaket-, zwei
Grundlagen- und ein Schutztest. Lösbarkeit aller 150 Lektionen, fünf Fehlerarten,
ursprüngliches Hörziel, Fehlerliste, Neustart, alte Profile und XP wurden geprüft.
Die historischen Inhaltsvergleiche rechnen nur die 68 exakt erwarteten Korrekturen
zurück; der Ablaufvergleich nur neun präzise dokumentierte Methodenänderungen.
Bereits ausgelieferte Kalenderfelder und Netzwerkfehlermeldungen wurden in älteren
Schutztests berücksichtigt. Sprachvergleich, TTS, Modelle und andere Inhalte bleiben
gesondert geschützt; Zeilenenden werden bei Idempotenz plattformneutral verglichen.

682 Browseransichten mit separaten Profilen bestanden: 300 Lernphasen, 156
Zusatzaufgaben, 63 Figuren-, 85 Menü-/Lern-, 30 Kalender-/Abschluss- und 36 gezielte
Bedienansichten und zwölf neue Tastaturansichten. Die 36 neuen Fälle prüfen tatsächliche Touch-Trefferflächen in sechs
Formaten, darunter 320×640, Querformat und 160 Prozent Schrift: vier Antworten,
Hilfeseiten, Drei-Versuche-Hilfe, beide Kana-Wege, Bestätigung, Neustart, ursprüngliche
Fehleraufgabe am Ende und Abschluss/XP. Die Browserbrücke und Sprachereignisse sind
simuliert. Nach der letzten Fokuskorrektur wurden alle 670 bisherigen Ansichten
vollständig erneut ausgeführt. Zwölf weitere Haupt-/Zusatzfälle prüfen erhaltenen
Fokus, gesetzte Cursorposition, echte Touch-Trefferfläche, Entwurf nach Neustart,
XP und fehlende Freischaltung bei simulierter Tastaturverkleinerung.

Der endgültige vollständige Android-35-x86_64-Lauf besteht 22/22 Fälle, 0 Fehler,
0 Auslassungen. Darunter reale WebView-Bedienung, sichtbare Sprechhilfe,
falsche/korrekte bestätigte Auswahl, vier erreichbare Antworten, ursprüngliche
Fehlerwiederholung nach Neustart, alte Profile, Kalender, gewählter Lehrer, Abschluss
und XP. Native Modelltests verarbeiten synthetisches Audio mit den vorhandenen
Offline-Modellen. Die echte Android-HTTPS-Updatesuche gegen die öffentliche Quelle
wurde vor dem Upload geprüft; auf 11.0.15 war noch keine höhere Testversion vorhanden.
Dies ist kein menschlicher Mikrofon-, Lautsprecher- oder S24-Test.

Build und Lint bestanden: lokal 11 und CI 12
Warnungen, jeweils 0 Fehler. Ein früherer CI-Lauf scheiterte vor Testbeginn am
beschädigten Google-API-Systemabbild-Download. Sein erneuter Lauf wurde durch die
zusätzliche Kana-Korrektur überholt und abgebrochen. Nur der vollständige finale
22-Fälle-Lauf ist der native Abschlussnachweis.

Der erste vollständige Lauf auf 35193f2e bestand 15/22 Fälle. Sechs alte Assertions
verlangten die Abwesenheit bewusst verdeckt gespeicherter Romaji oder den früheren
Hinweis-Container. Sie wurden auf tatsächlich sichtbare Lösungen und den lesbaren
Hinweisdialog umgestellt; Fortschritts-, XP- und Neustartprüfungen bleiben erhalten.
Der siebte Fehler war HTTP 403 am öffentlichen GitHub-API-Einstieg, Ursache unbekannt.
Die native HTTPS-Prüfung blieb unverändert. Zwischen 35193f2e und 7459f85 änderten
sich nur Testadapter und Bericht. Der zweite vollständige Lauf bestand 20/22 Fälle,
einschließlich der sechs angepassten Fälle und echter öffentlicher HTTPS-Suche.
Der HTTP-403-Fehler trat dort nicht auf; seine Ursache bleibt unbekannt.

Die verbleibende Tastaturprüfung belegte in der Browser-Reproduktion einen echten
Produktfehler: Layoutberechnung entfernte das aktive Eingabefeld kurz aus dem DOM
und verlor den Fokus. focus-ui.mjs hält seine Seiten nun verbunden und passt nur
Höhe und begrenzte Scrollposition an. Die zwölf neuen Fälle bestehen Fokus, Cursor,
Sichtbarkeit und Neustart; die bisherigen 670 Ansichten bestehen nach der Korrektur
erneut. Der Konfettitest hatte zwei späte leere Momentaufnahmen verglichen. Er
beobachtet nun ab dem tatsächlichen Abschlussklick zwei verschiedene nicht leere
Canvasbilder. Animation und ihre Dauer von 3,2 Sekunden bleiben unverändert.
Der finale vollständige Lauf besteht alle 22 Fälle einschließlich echter Tastatur
und tatsächlicher Konfettipixel. Weder 15/22 noch 20/22 zählen als erfolgreiche
Abschlussprüfung.

Weitere behobene Fehlversuche: vorzeitig aus dem DOM genommene Kontrollknöpfe,
zunächst noch abgeschnittener Hilfebutton, ungeeignete Testselektoren und ein nach
Selbstprüfung offener Hilfedialog. Die Browserprüfungen fanden diese Probleme;
sie wurden korrigiert und erneut ausgeführt. Ein eingeschränkter temporärer
Python-Zugriff wurde mit genehmigtem Prozesszugriff wiederholt. Die kanonische
Asset-Vorbereitung lief zunächst im falschen Arbeitsordner und danach erfolgreich.
Kein solcher Fehlversuch zählt als bestandener Test.

## Signierte Pakete und echte öffentliche Downloads

APK: 88293243 Bytes.
SHA-256: f65f3fa9164ae1c884edf5d7f0c44b41da12b8d519e40e467daea215c3d2d34b.
Bestehendes Zertifikat: 3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9.
v3-Signatur, unveränderte Paketkennung, Code 11001501 und 16-KB-Alignment bestanden.
v2 wird bei der bestehenden Mindestversion nicht verwendet.
Alle 168 Kurs-/Web-/Bild-/Lizenzdateien und acht
weitere Ressourcen entsprechen bytegenau dem geprüften Git-Quellstand. Alle
CI- und ausgelieferten APK-Einträge sind bytegleich; nur die Herausgebersignatur
kommt hinzu. Der letzte Vergleich entdeckte im lokalen inkrementellen Build eine
alte Versionskonstante aus 11.0.14. DEX-Auswertung belegte dies; das Paket wurde
nicht veröffentlicht. Die finale APK stammt direkt aus der frischen Release-APK
des bestandenen CI-Laufs und wurde mit dem bestehenden Schlüssel signiert.
Quellen, Lizenzen und bereinigte Nachweise enthalten keine
privaten Schlüssel, Zugangsdaten, persönlichen Lernstände oder Nutzeraufnahmen.

Alle 17 ersten öffentlichen Dateien wurden anonym heruntergeladen
und mit lokaler Größe und SHA-256 verglichen. Die öffentliche APK bestand zusätzlich
Signatur, Herausgeber, Version, Paketkennung, Alignment und Quellabgleich. Der Tag
zeigt auf den tatsächlich geprüften Quellcommit. Dieser nach dem Upload erstellte
Abschlussbericht und sein eigener Prüfsummennachweis werden ergänzend hochgeladen
und nachgeprüft; die ersten 17 Dateien werden dabei nicht überschrieben.

Die echten öffentlichen Manifeste bieten Android 11.0.4, 10, 11, 12, 13 und 14
nur im Testkanal 11.0.15 an. Auf 15 sind beide Suchen ohne höhere Version korrekt
leer. 15 isolierte Profil-/Formatkombinationen bestanden die produktiven Updatebuttons
mit diesen öffentlichen Manifestdaten und einer simulierten nativen Brücke:
Profile bytegleich, kein automatischer Download und keine Installation.
Die Windows-Suche auf 11.0.11 bietet weder eine höhere stabile noch höhere Testversion.
Die Nachprüfung auf dem Host ersetzt keinen S24-Netzversuch.

Alle 26 vorherigen Releases mit
274 Dateien bleiben unverändert: IDs, Status,
Dateinamen, Größe, Digest und URL. Latest bleibt v11.0.4.

## Geräteprüfliste und offene Prüfungen

1. S24 Ultra: über die vorhandene App aktualisieren; Version 11.0.15, Lernstand,
   Lehrer und vorhandenes Sprachpaket vergleichen. Nicht vorher deinstallieren.
2. Lange-Vokale-Aufgabe mit vier Antworten öffnen, jede erreichen; bewusst falsch
   antworten. Rückmeldung und alle Hilfeseiten müssen erreichbar bleiben.
3. Weiter zur Endwiederholung wählen, App schließen und fortsetzen. Dieselbe Aufgabe
   muss wiederkommen. Sie lösen, Abschlussrunde lösen; XP nur einmal erhalten.
4. Drei echte erfolglose Sprechversuche: fester Auswahlbutton muss sichtbar sein.
   Falsche Auswahl oder fehlende Bestätigung darf nicht freischalten. Richtige
   Auswahl bestätigen und später Sprechen wiederholen.
5. Kurzes Kana nach qualifizierter Aufnahme separat selbstprüfen; Kennzeichnung,
   Dialogabschluss und Weitergehen prüfen. Große Schrift und Querformat mitprüfen.
6. Beide Updatesuchen prüfen. Ohne höhere Ausgabe ist auf 15 ein leeres Ergebnis
   richtig; Netzfehler mit genauer Meldung dokumentieren.
7. Frisches Windows-System: weiter die bisherige Windows-Testversion 11.0.11 verwenden.
   Dieser Android-Auftrag enthält keine neue EXE und behauptet keinen neuen Windows-Gerätetest.

Eigene Sichtprüfung umfasst tatsächlich gerenderte Bedienansichten und die
Dokumentseiten. Echte S24-Installation, Mikrofon-/Hörtests, Anfänger-Erprobung und
menschliche Japanisch-Fachprüfung bleiben offen. Die frühere S24-Netzursache und
eine bessere Spracherkennungsqualität sind nicht nachgewiesen.

## Downloads und Nachweise

[Android APK](https://github.com/Priestkiller/JapanischTrainer/releases/download/android-test-v11.0.15-1/JapanischTrainer-11.0.15-Android.apk)
und [Testveröffentlichung](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.15-1).

Lokale Lieferung: F:/Japanischtool/Testpakete/11.0.15/android/.
Nachweise: validation/public-1115/, validation/ci-1115-final/, validation/recovery-1115/.
Zentrale Chronik und Word-Ausgabe: F:/Japanischtool/PROJEKTDOKUMENTATION_JapanischTrainer.
Stabile Übernahme benötigt weiterhin deine ausdrückliche Freigabe.

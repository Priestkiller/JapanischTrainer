# Öffentliche Prüfung Android 11 0 12

Prüfdatum 1. Oktober 2026. Android 11.0.12-android.1-test, Code 11001201, ist ausschließlich als Prerelease veröffentlicht. Windows bleibt bei Testversion 11.0.11. Stabil und Latest bleiben v11.0.4. Quellstand acd234bc6f20dcf1c5c956b30bef39aa990f258b auf test/11.0.12; main wurde nicht geändert.

## Tatsächlich geänderte Oberfläche

Startseite, Lernweg, Wiederholung, Lehrer und weitere Menüs verwenden jetzt den bestehenden Japan-Nachthintergrund, dunkle Karten, cyanfarbene Konturen und helle Schrift. Beim Sprechen steht die Lehrkraft bei ausreichend Platz rechts unten mit Sprechblase links. Kleine Ansichten, große Schrift und Tastatur behalten den kompakten Ablauf. Normale Lektionsschritte behalten feste Aktionen und bewusst aufrufbare Hilfen. Lange Menüs und außergewöhnlich lange Inhalte dürfen scrollen. Die später angeordnete Begrenzung von Figuren bleibt erhalten: keine große Lehrkraft in Auswahl-, Bau- und Schreibaufgaben; Kiko in Übungen beim Abschluss. Das ist eine an den Vorlagen orientierte Umsetzung, keine Behauptung einer pixelgleichen Kopie.

Kurs unverändert: 150 Lektionen, 680 Karten, Revision 11, Inhalt 11.0.7; 105 Lektionen mit 501 Karten vertieft und 156 Zusatzaufgaben. Keine Umnummerierung oder Änderung der Lernstandspeicherung, Lehrkräfte, Stimmen, Animationen oder Modelle.

## Bestandene Software und Paketprüfungen

192 Python- und 60 JavaScript-Tests, 85 neue Browseransichten in fünf Formaten, 300 Kernansichten und 156 Zusatzaufgaben, Kana- und Sprechhilfeprüfungen bestanden. Die native Suite bestand alle 16 Prüfungen einschließlich Hauptmenüs, altem Testprofil, Neustart, Tastatur und tatsächlicher Verarbeitung synthetischer Audiodaten mit den vorhandenen Offline-Modellen. CI: https://github.com/Priestkiller/JapanischTrainer/actions/runs/36847704465. Dies sind keine Mikrofontests und kein Test auf dem S24 Ultra.

Build und Lint bestanden. Lint meldet 0 Fehler, lokal 11 und im CI 12 Warnungen, überwiegend bestehende Abhängigkeits-/Werkzeughinweise. Die signierte APK und ihre nachfolgend heruntergeladene öffentliche Kopie bestehen v3-Signatur, bisherigen Herausgeberfingerabdruck, Paketname, Versionscode und 16-KB-Alignment. Der bestehende Signierablauf für Android ab API 28 verwendet v3; v2 wird nicht als bestanden ausgegeben. 151 mitgelieferte Dateien stimmen mit dem für die Paketierung verwendeten Quellstand überein. Die neuen Darstellungsdateien stimmen im CI-Paket und öffentlichen Quellenarchiv mit der APK überein. Quellen und Downloads enthalten keine privaten Schlüssel, Lernstände oder Aufnahmen.

Die Sichtprüfung fand verbliebene helle Gesprächs-/Lizenzflächen und eine abgeschnittene rechte Kante bei 160 Prozent Schrift. Beides wurde korrigiert und gezielt erneut geprüft. Sandbox-Prozessbeschränkungen, ein falsch geschriebener JDK-Pfad, ein Browseraufruf ohne Edge-Kanal und eine zu weit gefasste Annahme über v2 wurden im Prüfablauf korrigiert. Zwei neue Darstellungsdateien unterschieden sich im Windows-Checkout ausschließlich durch Zeilenenden. Für die Paketierung wurden sie exakt aus dem geprüften Git-Stand übernommen und erneut gebaut und signiert; der lokale Checkout wurde danach wiederhergestellt. Die Veröffentlichung verwendet ausschließlich den bestandenen endgültigen Stand.

## Tatsächliche öffentliche Abnahme

Alle 14 in der Tabelle aufgeführten Dateien wurden anonym vollständig heruntergeladen und mit den lokalen Paketen anhand Größe und SHA-256 abgeglichen. APK, Manifest und Quellen gehören zur gleichen Ausgabe. Alle 23 bisherigen Veröffentlichungen mit 226 Dateien bleiben unverändert.

Die echten öffentlichen Android-Manifeste ergeben auf dem Prüfhost: 11.0.11 erhält 11.0.12 im Testkanal, die reguläre Suche bietet keine Testausgabe. Auf 11.0.12 bleibt die Testsuche korrekt leer. Die unveränderten nativen Filterregeln wurden separat im Emulator geprüft. Zusätzlich wurden die produktiven Web-Schaltflächen mit den echten öffentlichen Manifestdaten und einer simulierten nativen Brücke in sechs getrennten Profil-/Bildschirmkombinationen betätigt. Testangebot, Rückkehr zur regulären Suche und bytegleicher Testprofilstand bestanden; weder Download noch Installation starteten automatisch. Windows 11.0.11 bekommt aus seiner produktiven Suche kein Android-Update und keine höhere Windows-Testversion. Die tatsächliche S24-Updatesuche und Installation bleiben offen.

Dieser nachträglich ergänzte Bericht und seine eigene Hashdatei werden zusätzlich zum ursprünglichen Paket bereitgestellt und separat öffentlich abgeglichen. SHA256SUMS.txt deckt die ursprünglichen Paketdateien ab; die Berichtshashdatei deckt diesen Bericht ab.

## Installieren und praktisch prüfen

[Android Testversion](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.12-1). Auf der installierten 11.0.11: Zahnrad → App-Updates → Testversion suchen. Danach bewusst herunterladen und über die vorhandene App installieren. Keine Deinstallation erforderlich. Lokale Pakete: F:/Japanischtool/Testpakete/11.0.12/android/.

XP, Abschlüsse und Lehrerauswahl vorher und nachher vergleichen. Die fünf Hauptmenüs öffnen. Sprechaufgabe mit normaler und großer Android-Schrift prüfen; Vorlage, Hilfe, Aufnahme und Hauptaktion müssen erreichbar sein. Eine Auswahlaufgabe öffnen und auf verdeckte Antworten prüfen. Tatsächlich aufnehmen, die eigene Aufnahme anhören und mit der Lehrerstimme vergleichen.

Offen bleiben echtes S24 Ultra, Mikrofon und Hören, Anfänger-Erprobung und menschliche Japanisch-Fachprüfung. Eigene Sichtprüfung, automatische Prüfungen und menschliche Prüfung sind getrennt. Eine bessere Erkennung echter Stimmen wird nicht behauptet. Stabile Übernahme braucht eine gesonderte Freigabe.

| Datei | Bytes | SHA-256 |
| --- | ---: | --- |
| Android-Lizenzunterlagen-11.0.12.zip | 50650 | `c24c28566f5621ecec82fc927950cc96435da2d9dcbcbdb46062dce5edaebfd7` |
| android-update.json | 777 | `f75d2fcaa6201383080767e2d4ec64e1bbc042c9fa7096d861e8a9320edf61a9` |
| ANDROID_NOTICES.txt | 1957 | `316fe67eda331335bcaee53f3f2a2688ae6a26c4dfe70ad031a16bdb0999f36c` |
| JapanischTrainer-11.0.12-Android-Quellcode.zip | 95415828 | `1a010059b1ef6a3a11f7a5d1ebb6b24a4be7349b234d7b270ce2ac6fe408eeb9` |
| JapanischTrainer-11.0.12-Android.apk | 65587793 | `be0d173c5b161bb86b622f99337a58418aa9f32ee6af4c682294d7825e10549e` |
| LICENSE.txt | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| MODEL_ATTRIBUTION.txt | 2892 | `250084a639568fd20fb1b04577e5861cbcb4770ad17642edf988cb220d1283b2` |
| MODEL_LICENSES.txt | 41730 | `d565d43da6c69fef073f35029f99ed803085c1768ff282d371e5649952ca7606` |
| Pruefnachweise-Android-11.0.12.zip | 7054104 | `568a99d9296eaab86b81d83c4086892224233535d5621aea30e01281c01ffab2` |
| RELEASE_NOTES_ANDROID_11.0.12_TEST.md | 2538 | `05db8e194b17c932b21311256a3d73f9f075a6d9a2008cbab3fa005ea4aeea09` |
| SHA256SUMS.txt | 1231 | `922626824ee6e8aaee6b64960296e9faa2ffaa0611a9fd1b9ad29cf92b89c879` |
| SOURCE_COMMIT.txt | 42 | `4d2e38f9be274017cd511e64d999874f05faa46f10c0c245a172b9cd364e5974` |
| TESTBERICHT_ANDROID_11.0.12.md | 6653 | `722bc3b4f541bfba042cd823dac7ed161473c96fbbbc714376dbfee4e825e554` |
| THIRD_PARTY_NOTICES.txt | 2502 | `b436071bdc8f7871d9138712b514e713c4b25239c82547e5a156f357f011db91` |


## Öffentliche Abnahme abgeschlossen am 1. Oktober 2026

Alle 16 öffentlichen Dateien einschließlich des nachträglich ergänzten Veröffentlichungsberichts und seiner Hashdatei wurden mit Größe und SHA-256 abgeglichen. APK-v3-Signatur, Herausgeber, Paketname, Versionscode 11001201 und 16-KB-Alignment bestanden. Die öffentlichen Quellen gehören zur APK. 11.0.11 erhält 11.0.12 ausschließlich im Android-Testkanal; auf 11.0.12 ist das Testangebot korrekt leer. Produktive Web-Schaltflächen wurden mit echten öffentlichen Manifestdaten, einer simulierten nativen Brücke und sechs separaten Profil-/Bildschirmkombinationen geprüft. Profile blieben unverändert; kein automatischer Download oder Installation. Die echte Handy-Suche und Installation bleiben offen. Die 23 älteren Veröffentlichungen mit 226 Dateien blieben unverändert. Windows bleibt 11.0.11; stabil und Latest bleiben 11.0.4.

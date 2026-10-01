# Öffentliche Prüfung der Testversion 11 0 11

Prüfdatum 1. Oktober 2026. Windows 11.0.11 und Android 11.0.11-android.1-test mit Code 11001101 wurden ausschließlich als Prereleases bereitgestellt. Stabil und Latest bleiben 11.0.4. Die Anmeldung als Priestkiller wurde erneuert. Der geprüfte Quellstand 541628306266f993ba1324621273aa462f398f3f liegt im separaten Testbranch test/11.0.11. Der Default-Branch main blieb unverändert.

## Ursache der fehlenden Downloadanzeige

Auf der installierten 11.0.10 erschien vor der Bereitstellung korrekt kein höheres Angebot: Öffentlich war bis dahin 11.0.10 die höchste Testausgabe, 11.0.11 lag nur lokal vor. Der Zugriff auf beide öffentlichen 11.0.10-Downloads wurde zusätzlich geprüft. Es wurde keine künstliche höhere Veröffentlichung angelegt und keine Schutzregel gegen gleiche oder ältere Versionen abgeschaltet.

## Tatsächlich bestandene Prüfungen

Alle 37 hier aufgeführten Dateien wurden anonym abgerufen und mit den lokalen Dateien über Größe und SHA-256 verglichen. Bereits vollständig verifizierte öffentliche Modell-ZIPs wurden beim abschließenden Abgleich wiederverwendet. Die Windows-Metadaten bestanden Ed25519 mit dem bisherigen öffentlichen Schlüssel; Updategröße und Archivhash stimmen überein. Setup-Version ist 11.0.11. Die Android-APK bestand v3-Signatur, bisherigen Zertifikatsfingerabdruck, 16-KB-Alignment, Paketname und Versionsdaten. Metadaten und Paketzuordnung stimmen überein.

Die produktive Windows-Suche bietet von 11.0.10 genau 11.0.11 im Testkanal an. Echte Tk-Schaltflächen wurden mit separaten Profilen auf 11.0.10 und 11.0.11 geprüft; Suche allein lädt und installiert nichts, die Profile blieben bytegleich. Auf 11.0.11 wird korrekt kein gleiches oder älteres Testupdate angeboten. Androids Auswahl wurde anhand der echten öffentlichen Metadaten und der nativen Filterregeln auf dem Prüfhost nachgerechnet: 11001001 erhält 11001101 im Testkanal; die reguläre Suche bietet kein Testpaket. Das ist keine ausgeführte Updatesuche auf dem S24 Ultra.

Der Android-CI-Lauf bestand Build, Lint, 60 JavaScript-Tests und alle 15 nativen Emulatorprüfungen, einschließlich echter Verarbeitung mit ReazonSpeech und Qwen3-ASR. CI: https://github.com/Priestkiller/JapanischTrainer/actions/runs/36835217123. Der erste Lauf bestand 14 von 15 Prüfungen: Ein historischer Test erwartete noch fünf Gesprächsszenen. Er wurde auf die sechs konkreten IDs einschließlich restaurant korrigiert. Nur diese Testdatei änderte sich; produktive Dateien und Binärpakete blieben identisch. Der Quellcode-Download enthält die korrigierte Prüfung. Die bereits bestandenen 192 Python-, 20 Installer-, Windows-Update- und Oberflächenprüfungen vom 30. September wurden nicht ohne Anlass wiederholt.

Alle 19 früheren Veröffentlichungen mit 185 Dateien blieben in Kennungen, Größen, Hashes und Kanalzuordnung unverändert. Beide Zusatzmodelle wurden getrennt als optionale Testpakete veröffentlicht. Kein automatischer Download, Modellwechsel oder Nutzer-Upload.

## Versionshinweise und offene Erprobung

Neu sind persönliche Tagesrunden, getrennte Fähigkeitswiederholungen, vier Hörsituationen, manuelles Kana-Nachzeichnen, das vorbereitete Restaurantgespräch auf Android und der freiwillige lokale Sprachvergleich. Bestehende Kurs-IDs, XP, Stimmen, Lehrer, Modelle und Updatesicherheit bleiben erhalten. Kurs: 150 Lektionen, 680 Karten, Revision 11 und Inhalt 11.0.7; 105 Lektionen mit 501 Karten selbst durchgesehen, 156 Zusatzaufgaben.

Echte S24-Ultra-, Mikrofon- und Hörtests, Anfänger-Erprobung, ein frisches Windows-System und menschliche Japanisch-Fachprüfung sind offen. Synthetisches Audio und Emulatorprüfungen sind keine Mikrofontests. Eine allgemein bessere Spracherkennung ist nicht belegt. Die angekündigte freiwillige S24-Testrunde folgt später. Eine Übernahme in den stabilen Kanal benötigt weiterhin eine gesonderte Freigabe.

## Öffentliche Pakete und lokale Kopien

[Windows Testversion](https://github.com/Priestkiller/JapanischTrainer/releases/tag/windows-test-v11.0.11) · [Android Testversion](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.11-1). Auf 11.0.10 unter Programm-Updates beziehungsweise App-Updates Testversion suchen wählen. Lokale Kopien: F:/Japanischtool/Testpakete/11.0.11/.

Die Tabelle dokumentiert die geprüften Produkt-, Quellen-, Metadaten-, Lizenz- und Modell-Dateien. Dieser nachträglich ergänzte Veröffentlichungsbericht und seine Hashdateien werden gesondert öffentlich geprüft.

| Datei | Bytes | SHA-256 |
| --- | ---: | --- |
| windows / ANLEITUNG_11.0.11_TEST.md | 5024 | `e6f43b99b519a41eae401c03704b1af7768ef3fc016f370f47c5bedb512124f4` |
| windows / JapanischTrainer-11.0.11-Quellcode.zip | 95400168 | `e607e1b6b64205910267ad1d9267938647784faaf1373070cf49b4f1e745a081` |
| windows / JapanischTrainer-11.0.11-Setup-x64.exe | 847144653 | `92f541682e966f90d0f7aedfb3281c6ca122f5f116d97a8aaf2241cfed49457e` |
| windows / JapanischTrainer-11.0.11-Update-x64.zip | 134692753 | `e158bb4a9e391e286f2163520738f2384ac815c13bcaf32e794463645943a6f1` |
| windows / LICENSE.txt | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| windows / MODEL_ATTRIBUTION.txt | 2892 | `250084a639568fd20fb1b04577e5861cbcb4770ad17642edf988cb220d1283b2` |
| windows / MODEL_LICENSES.txt | 41730 | `d565d43da6c69fef073f35029f99ed803085c1768ff282d371e5649952ca7606` |
| windows / Optional-ASR-Apache-2.0.txt | 11560 | `3ddf9be5c28fe27dad143a5dc76eea25222ad1dd68934a047064e56ed2fa40c5` |
| windows / Pruefnachweise-11.0.11.zip | 5506 | `2a8ff0d98a6e8536dfe0ab32b12c6c4321be9e5754f636eb9305b2363ec1fce6` |
| windows / RELEASE_NOTES_11.0.11_TEST.md | 2155 | `b97d518e789200b4af7d7138e1423c0d5e178cac2633b0ee277643930c98165d` |
| windows / SHA256SUMS.txt | 1206 | `2c08f1d11e8ebd086332932873b05f6d717cb164e47ede776b46a72f457cc2a5` |
| windows / SOURCE_COMMIT.txt | 42 | `620013e0908e9abed55512dff87e332ecd9146368afdefbf4f87215986d556bd` |
| windows / TESTBERICHT_11.0.11.md | 10107 | `88cad4d66124a5da286912cbcfa848e939defeeed8e37fcb873e8fe7adbb52da` |
| windows / update.json | 1217 | `276ed064a4eb1657b5e8388eab54f8246858d78b2235e5665e4feb766fae54c8` |
| android / android-update.json | 767 | `f49fda2b22031104b4c3f7188885430aa09e7c9ca148ca6ca92ced9d6ac22336` |
| android / ANLEITUNG_11.0.11_TEST.md | 5024 | `e6f43b99b519a41eae401c03704b1af7768ef3fc016f370f47c5bedb512124f4` |
| android / JapanischTrainer-11.0.11-Android-Quellcode.zip | 95400168 | `e607e1b6b64205910267ad1d9267938647784faaf1373070cf49b4f1e745a081` |
| android / JapanischTrainer-11.0.11-Android.apk | 65583565 | `0788c2156f0a5419abf10f7f33c2927173d71884480eb3006373a37cf2a56d88` |
| android / LICENSE.txt | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| android / MODEL_ATTRIBUTION.txt | 2892 | `250084a639568fd20fb1b04577e5861cbcb4770ad17642edf988cb220d1283b2` |
| android / MODEL_LICENSES.txt | 41730 | `d565d43da6c69fef073f35029f99ed803085c1768ff282d371e5649952ca7606` |
| android / Optional-ASR-Apache-2.0.txt | 11560 | `3ddf9be5c28fe27dad143a5dc76eea25222ad1dd68934a047064e56ed2fa40c5` |
| android / Pruefnachweise-11.0.11.zip | 5506 | `2a8ff0d98a6e8536dfe0ab32b12c6c4321be9e5754f636eb9305b2363ec1fce6` |
| android / RELEASE_NOTES_11.0.11_TEST.md | 2155 | `b97d518e789200b4af7d7138e1423c0d5e178cac2633b0ee277643930c98165d` |
| android / SHA256SUMS.txt | 1113 | `b8c82bb9cf994369154cbb7ccc36325c8012746039e97972934843ab8294ca19` |
| android / SOURCE_COMMIT.txt | 42 | `620013e0908e9abed55512dff87e332ecd9146368afdefbf4f87215986d556bd` |
| android / TESTBERICHT_11.0.11.md | 10107 | `88cad4d66124a5da286912cbcfa848e939defeeed8e37fcb873e8fe7adbb52da` |
| model-reazonspeech / JapanischTrainer-ReazonSpeech-1.zip | 126727479 | `9fed9f7cafd62ccea1db281491626967f058d9af7940830753023cfd90d58474` |
| model-reazonspeech / MODEL_ATTRIBUTION.txt | 2892 | `250084a639568fd20fb1b04577e5861cbcb4770ad17642edf988cb220d1283b2` |
| model-reazonspeech / Optional-ASR-Apache-2.0.txt | 11560 | `3ddf9be5c28fe27dad143a5dc76eea25222ad1dd68934a047064e56ed2fa40c5` |
| model-reazonspeech / reazonspeech-Hinweise.md | 1039 | `06896f47535a501d91758fc188efe87ba78ce3311ebec08d52ec664495e7b86f` |
| model-reazonspeech / reazonspeech.json | 1049 | `db39f475b5e38bef1d8b3248f58c5efbecd2de6a2f6f5c398ece7736926e0636` |
| model-qwen3 / JapanischTrainer-Qwen3ASR-1.zip | 844893948 | `3b6695e77383e91aa78da0f05012d269d8f11fc65d7da67bc38ff73889bde10f` |
| model-qwen3 / MODEL_ATTRIBUTION.txt | 2892 | `250084a639568fd20fb1b04577e5861cbcb4770ad17642edf988cb220d1283b2` |
| model-qwen3 / Optional-ASR-Apache-2.0.txt | 11560 | `3ddf9be5c28fe27dad143a5dc76eea25222ad1dd68934a047064e56ed2fa40c5` |
| model-qwen3 / qwen3-Hinweise.md | 1032 | `90c112c1b943e099e147054cb83274c9b6f6a41b096903675539a869c2336887` |
| model-qwen3 / qwen3.json | 1340 | `b4281888538cd09f6f306b936a14acb794b58cef6038930088093412eabd4f58` |


## Öffentliche Abnahme abgeschlossen am 1. Oktober 2026

Alle 41 öffentlichen Dateien einschließlich der nachträglich bereitgestellten Veröffentlichungsberichte und ihrer Hashdateien wurden erfolgreich über Erreichbarkeit, Größe und SHA-256 abgeglichen. Windows-Metadaten, APK-Signatur, Versionen und Paketzuordnung bestanden; stabil und Latest bleiben v11.0.4. Echte Windows-Schaltflächen bieten 11.0.10 die Testversion 11.0.11 an und lassen separate Profile unverändert. Androids Auswahl wurde mit öffentlichen Manifesten auf dem Prüfhost geprüft; die native Filterprüfung bestand im Emulator. Die tatsächliche S24-Ultra-Updatesuche, Installation, Mikrofon- und Hörprüfung bleiben offen. Details stehen in VEROEFFENTLICHUNG_11.0.11_TEST.md und validation/public-1111/result.json.

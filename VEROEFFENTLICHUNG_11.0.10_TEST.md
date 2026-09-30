# Öffentliche Prüfung der Testversion 11 0 10

Prüfdatum 30. September 2026. Beide Ausgaben wurden ausschließlich als Prerelease veröffentlicht. Alle **24 tatsächlichen öffentlichen Downloads** wurden anonym mit HTTP 200 geladen und gegen die vorher geprüften lokalen Dateien anhand von Größe und SHA-256 verglichen. Versionen, Paketzuordnung und vorhandene Signaturen sind geprüft. Dies ist die abgeschlossene öffentliche Nachprüfung zu TESTBERICHT_11.0.10.md; die unveränderten Downloadpakete enthalten dessen vor Veröffentlichung abgeschlossene Fassung.

## Veröffentlichungen und Quellen

- [Windows 11.0.10 TESTVERSION](https://github.com/Priestkiller/JapanischTrainer/releases/tag/windows-test-v11.0.10): 13 Dateien, Setup, Update-ZIP, Ed25519-Metadaten, Quellen, GPL-/Modelllizenzen, Prüfsummen und bereinigte Nachweise.
- [Android 11.0.10 TESTVERSION](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.10-1): 11 Dateien, APK, Metadaten, Quellen, Lizenzen, Prüfsummen und Nachweise. Paket de.priestkiller.japanischtrainer, Version 11.0.10-android.1-test, Code 11001001.
- Quellarchiv: bddae8eedd7b6b9e3f4b3c40a5d2e96bbdafc0b0 mit 319 geprüften Quelldateien. Finale Android-Programmprüfung: [CI 36468510690](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36468510690), Programmstand 4f184defda9aa83bf353a008f9972b216155ee34. Der spätere Quellenstand ergänzt nur die abgeschlossenen Berichte. Enthaltene APK-Web-/Kurs-/Versionsressourcen stimmen bytegenau mit dem Archiv überein.

Vor Veröffentlichung wurden beide Entwürfe einschließlich ihrer GitHub-Dateigrößen und SHA-256-Digests mit den lokalen Paketen verglichen. Der Windows-Entwurf vom 28. September wurde nach dem damaligen Nutzungslimit am 30. September fortgesetzt; keine künstliche neue Testausgabe wurde erzeugt. Der noch private Entwurf war über den Tag-Endpunkt nicht erreichbar; die Entwurfsprüfung verwendet die authentifizierte Release-Liste. Die anschließende öffentliche Prüfung war anonym.

## Signaturen und Paketprüfung nach Download

Das echte öffentlich geladene update.json bestand die produktive Ed25519-Prüfung. Sein Versionswert, Zielrelease, Archivgröße und SHA-256 passen zum öffentlich geladenen Windows-Update. Die produktive sichere Entpackroutine prüfte Paketpfade, Dateihashes und Zuordnung auf einer isolierten Programmkopie. Das entpackte Paket enthält release.json für 11.0.10 mit unverändertem Kurs 11.0.7. Der Produktions-Installer besitzt wie bisher kein Authenticode-Zertifikat; seine geprüfte PE-Version und Paketidentität werden durch den identischen öffentlichen SHA-256 bestätigt.

Die echte öffentlich geladene APK bestand erneut APK-v3-Signatur, 16-KB-Alignment sowie aapt-Paket-/Versionskontrolle. Herausgeberzertifikat SHA-256: 3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9, identisch mit bisherigen Android-Ausgaben. android-update.json enthält den korrekten Paketnamen, Code, Versionsnamen und das APK-Ziel desselben Testreleases; Größe und SHA-256 stimmen überein.

Die 17 vorherigen Veröffentlichungen mit 161 Dateien behielten IDs, Draft-/Prerelease-Zuordnung, Dateinamen, Größen, Digests und Downloadadressen. Das öffentliche Latest-Angebot bleibt v11.0.4. Die stabile Android-Ausgabe bleibt android-v11.0.4-1.

## Updateerkennung gegen die echte öffentliche Quelle

Die produktive Windows-Updatefunktion wurde für folgende installierte Versionen gegen GitHub ausgeführt:

| Installierte Version | Reguläre Suche | Testversionssuche |
| --- | --- | --- |
| 11.0.2 | 11.0.4 | 11.0.10 |
| 11.0.4 | kein Angebot | 11.0.10 |
| 11.0.7 | kein Angebot | 11.0.10 |
| 11.0.10 | kein Angebot | kein Angebot |

Zusätzlich wurden die tatsächlichen nativen Windows-Schaltflächen mit drei getrennten synthetischen Testprofilen und Tk-Prozessen für 11.0.4, 11.0.7 und 11.0.10 bedient: normale Suche, Testsuche und zurück zur normalen Suche. Alte Versionen erhalten das Testangebot, 11.0.10 kein gleiches/älteres Angebot. Kanalwechsel löscht das vorherige Angebot. Profile blieben unverändert; Download und Installation wurden während der Suche nicht aufgerufen.

Androids vorhandene native Tag-/Metadatenregeln wurden auf dem Prüfhost mit den tatsächlich öffentlich geladenen Manifesten nachgerechnet:

| Installierter Versionscode | Reguläre Suche | Testversionssuche |
| --- | --- | --- |
| 11000201 | 11000401 | 11001001 |
| 11000401 | kein Angebot | 11001001 |
| 11000901 | kein Angebot | 11001001 |
| 11001001 | kein Angebot | kein Angebot |

Die native Filterlogik, getrennte Profile, App-Start und Oberfläche wurden im Android-Emulator separat geprüft. Die öffentliche Android-Auswahl hier ist ein Vergleich auf dem Prüfhost und kein behaupteter Installations-/Mikrofontest auf einem S24 Ultra. Eine leere Testsuche in der neuen Version ist korrekt, solange keine höhere passende Testversion existiert. Das Paket wurde nicht in den stabilen Kanal übernommen.

## Öffentliche Dateien und SHA 256

Die folgende Tabelle erfasst die tatsächlich nach Upload heruntergeladenen Dateien. Gleichnamige Lizenz-/Berichtsdateien erscheinen je Plattform erneut; beide Downloads wurden separat geprüft. Die Reihenfolge entspricht Windows, danach Android.

| Datei | Bytes | SHA-256 |
| --- | ---: | --- |
| GERAETEPRUEFUNG_11.0.10.md | 4708 | `2d9c50ec9086abc9d036105e66110373b5f6833afd5c0b5a0a2f39bdc342011f` |
| JapanischTrainer-11.0.10-Quellcode.zip | 94818394 | `ab3b63abaea01867ff2e2dc9bf121c56cce6c74a07c6512a4bd831dcae901574` |
| JapanischTrainer-11.0.10-Setup-x64.exe | 847030786 | `d5da971bc12849151bdbd608bcd612ead473f81ea04722b1d5ab9b62abbd776e` |
| JapanischTrainer-11.0.10-Setup-x64.exe.sha256 | 106 | `d2490f164a08484048e0f8acf3f8c8c798490f51c6b1088e4d6dd43f57407f0e` |
| JapanischTrainer-11.0.10-Update-x64.zip | 134133929 | `528be772a32cd735d76a0963dc4252f524140a0aa3e757ad8be286e17d1eb116` |
| LICENSE.txt | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| MODEL_ATTRIBUTION.txt | 1809 | `7fcc4c13045a7adb8a530ea96bf91428e1fe50ac8916de784facc5acf48697a0` |
| MODEL_LICENSES.txt | 39957 | `1811e941af070c14bfcf569d572fa029765de3f7ca447bb386deeadb02c9e7af` |
| RELEASE_NOTES_11.0.10_TEST.md | 2332 | `da7027afccd2e3025ee8749e8355c37e161be38811c1ddb6fe2d43efd0a4ea29` |
| SHA256SUMS-Windows.txt | 1147 | `2992b13ddd4ca50771e13e7bf70c144134ecc58d5882ca9fd91b32117d99359a` |
| TESTBERICHT_11.0.10.md | 10404 | `2aafc9f21f6ff4aaad8b9e43401e4fd2a7ac554e802d4d93481a8b07a3a289af` |
| Testnachweise-windows-11.0.10.zip | 21216896 | `399ef83f884461fe2288a29715872b4dceb10ab39ec30031b0ea90898bd12461` |
| update.json | 3693 | `3ccc4ee4b92249cae68247038cc88b00754504798dd361af48e205ad88d967b3` |
| android-update.json | 744 | `85e0a96e5ed4b6b573778a2334a057f4868a10d5a1c0e4c017d93224f0cbf5e5` |
| GERAETEPRUEFUNG_11.0.10.md | 4708 | `2d9c50ec9086abc9d036105e66110373b5f6833afd5c0b5a0a2f39bdc342011f` |
| JapanischTrainer-11.0.10-Android-Quellcode.zip | 94818394 | `ab3b63abaea01867ff2e2dc9bf121c56cce6c74a07c6512a4bd831dcae901574` |
| JapanischTrainer-11.0.10-Android.apk | 64898571 | `9b7155d3e87890c47a1a7989d85c46db2453e9495737b3a7eec8cfe6d3e9db08` |
| LICENSE.txt | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| MODEL_ATTRIBUTION.txt | 1809 | `7fcc4c13045a7adb8a530ea96bf91428e1fe50ac8916de784facc5acf48697a0` |
| MODEL_LICENSES.txt | 39957 | `1811e941af070c14bfcf569d572fa029765de3f7ca447bb386deeadb02c9e7af` |
| RELEASE_NOTES_11.0.10_TEST.md | 2332 | `da7027afccd2e3025ee8749e8355c37e161be38811c1ddb6fe2d43efd0a4ea29` |
| SHA256SUMS-Android.txt | 941 | `ca022a6a1071fed62fd1e82ad6a0e222e3aa44d5bda6534ff14592a1b3590685` |
| TESTBERICHT_11.0.10.md | 10404 | `2aafc9f21f6ff4aaad8b9e43401e4fd2a7ac554e802d4d93481a8b07a3a289af` |
| Testnachweise-android-11.0.10.zip | 30485323 | `6bbf4d9b108928655687b6f5280f13980ce439fcc377300bf55050f334522eab` |

## Offene menschliche Prüfungen

Echtes S24 Ultra mit Mikrofon, menschliche Hörprüfung, Anfänger-Erprobung, frisches Windows-System und Japanisch-Fachprüfung bleiben offen. Automatische Softwareprüfungen, synthetische Modellverarbeitung und menschliche Prüfung sind in TESTBERICHT_11.0.10.md getrennt ausgewiesen. Die praktisch ausführbare Prüfliste steht in GERAETEPRUEFUNG_11.0.10.md. Eine spätere stabile Übernahme benötigt weiterhin eine ausdrückliche Freigabe.

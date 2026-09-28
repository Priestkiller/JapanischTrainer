# Öffentliche Kontrolle der Testversion 11.0.7

Am 28. September 2026 auf ausdrückliche Freigabe als öffentliche Testversion veröffentlicht und anschließend geprüft:

- [Windows 11.0.7](https://github.com/Priestkiller/JapanischTrainer/releases/tag/windows-test-v11.0.7).
- [Android 11.0.7-android.1-test](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.7-1), Versionscode 11000701.

Beide Releases sind Prereleases, nicht Latest. Die 68 vorhandenen Dateien der stabilen 11.0.4 und der Testversionen 11.0.5/11.0.6 stimmen unverändert mit dem vor Upload gesicherten öffentlichen Stand überein: Namen, Größen, SHA-256, Downloadzuordnung und Release-Eigenschaften. Latest bleibt v11.0.4. Unveränderte alte Pakete wurden nicht erneut vollständig heruntergeladen; ihre bisherigen Nachweise bleiben erhalten. Eine stabile Übernahme von 11.0.7 benötigt eine gesonderte ausdrückliche Freigabe.

## Tatsächlich ausgeführte öffentliche Nachprüfung

Alle 28 neuen Release-Dateien (Windows 15, Android 13) wurden ohne Anmeldung vollständig von den öffentlichen Downloadadressen geladen. Größe, SHA-256 und Plattform-/Tag-Zuordnung stimmen mit den geprüften lokalen Paketen und GitHub-Metadaten überein. Die folgende Tabelle enthält die tatsächlich heruntergeladenen Bytes und Hashes. Enthalten sind Programme, Metadaten, GPL-Quellen, Lizenzunterlagen, Aufgabenabdeckung, Installations-/Geräteanleitungen, Prüfberichte und bereinigte echte Testbilder.

Das öffentliche Windows-Manifest bestand die produktive Ed25519-Prüfung mit dem bisherigen Vertrauensschlüssel. Der produktive Entpacker prüfte das öffentliche Update-ZIP einschließlich Pfaden, Größen, Hashes, Pflichtdateien, Version und benötigten Modellen in einem isolierten Verzeichnis. Release, Kurs- und Aufgabendateien entsprechen 11.0.7 und den geprüften Quellen. Die öffentlichen EXE-Dateien sind bytegleich mit den lokal auf PE-Version 11.0.7.0 geprüften Dateien. Keine Änderung einer persönlichen Installation.

Die öffentliche APK bestand apksigner mit dem bisherigen Zertifikat SHA-256 `3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9`. aapt bestätigt `de.priestkiller.japanischtrainer`, Code `11000701`, Name `11.0.7-android.1-test`. Kurs und neue Aufgaben sind bytegleich mit den geprüften Quellen. Die öffentliche APK ist dieselbe Datei wie bei der lokal bestandenen v3-Signatur- und Alignmentprüfung. Windows besitzt weiterhin kein Authenticode-Zertifikat; die Update-Signatur ist davon unabhängig.

## Updateerkennung gegen die echten Quellen

| Installierter Stand | Windows regulär | Windows Test | Android regulär | Android Test |
| --- | --- | --- | --- | --- |
| 11.0.2 | 11.0.4 | 11.0.7 | 11000401 | 11000701 |
| 11.0.4 | kein Angebot | 11.0.7 | kein Angebot | 11000701 |
| 11.0.5 | kein Angebot | 11.0.7 | kein Angebot | 11000701 |
| 11.0.6 | kein Angebot | 11.0.7 | kein Angebot | 11000701 |
| 11.0.7 | kein Angebot | kein Angebot | kein Angebot | kein Angebot |

Windows: produktive `check_update`-Funktion gegen die öffentlichen Quellen und zusätzlich der echte native Update-Dialog in vier getrennten Prozessen mit separaten synthetischen Profilen (11.0.4 bis 11.0.7). Die Testsuche findet 11.0.7 aus den drei älteren Ausgaben. Auf 11.0.7 ist sie korrekt leer. Wechsel zur regulären Suche entfernt das Testangebot. Kein automatischer Download oder Installationsstart; Profile blieben bytegleich. Ein echter Screenshot belegt das Testangebot.

Android: Auswahl mit den echten öffentlichen Release- und Manifestdateien anhand der unveränderten nativen Filter-/Versionsregel auf dem Prüfhost nachgerechnet. Native Filter und Oberfläche wurden getrennt im Android-15-Emulator geprüft. Dies ist keine Installation oder öffentliche Updateprüfung auf einem echten S24 Ultra. Der vollständige gebaute Windows-Updatetest 11.0.6 → 11.0.7 verwendete eine separate lokale TLS-Quelle und erhielt Lernprofil und 15 Modelldateien; die öffentliche Signatur- und Dateiprüfung erfolgte zusätzlich wie oben beschrieben.

## Quellen, Softwareprüfungen und Grenzen

Beide GPL-Quellarchive und Release-Ziele entsprechen Commit `cca2f276b76ace6752c2f5b8b8ebbfceb08d2237`. Der Windows-Produktcode ist seit `1d4609a3cb8f29144c0a8f41b150c09e812d58ef` unverändert; der finale Android-Produktcode seit `6b7dc61b114bc830fec6fa18e3acbef1c6147699`. Spätere Commits vervollständigen Tests und Berichte. Quellen/Lizenzen wurden auf Vollständigkeit und Ausschluss privater Schlüssel, Zugänge, Profile, Aufnahmen und der neun lokalen Referenzbilder geprüft. Dieser nachträgliche Veröffentlichungsbericht ergänzt die unverändert ausgelieferten Prüfunterlagen im Repository.

180 Python-Tests einschließlich 24 Updateprüfungen, 47 mobile Logiktests, 20 Installerverträge und 10 native Android-Tests bestanden. Finaler [Android-Lauf 36398491437](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36398491437), Commit `01c2b7c040dfaae0d289a531d960b159f6830993`: keine Fehler, keine übersprungenen Tests. Die native Prüfung umfasst Speichern/Neustart, Drehung, 140 Prozent Schrift, tatsächlich sichtbare Bildschirmtastatur und echte lokale Modellinferenz. Frühere Fehlversuche und behobene Probleme stehen im technischen Bericht.

Native Windows-Prüfung: 25 Einstiege, zwei vollständige Zusatzrunden, acht Aufgabenansichten und vier Fenstergrößen. Browserprüfung: vier Formate, 100 Einstiege, 36 Aufgabeninteraktionen; bisheriger Ablauf in sieben Formaten. Aufgaben-Audio dabei simuliert und entsprechend gekennzeichnet. Die gebaute Windows-EXE bestand echte Offline-Inferenz für acht Stimmen in zwei Tempi, beide ASR-Modelle und Stille. Kein menschlicher Mikrofon-/Hörtest.

Erfasst: 150 Lektionen / 680 Karten. Neue Umsetzung: 156 Aufgaben in 25 bestehenden Lektionen, acht Familien, ausführliche aufrufbare Erklärungen und begrenzte Fehlerwiederholung. Eigene sprachliche Durchsicht: neue Aufgaben/Hilfen sowie weiterhin 105 Lektionen / 501 Karten aus den vier Inhaltspaketen; keine neue Abnahme der übrigen 45 Lektionen / 179 Karten. Menschliche Japanisch-Fachprüfung, Anfänger-Erprobung, echtes S24 Ultra mit Mikrofon/Hörprüfung sowie frisches Windows bleiben offen. Die Geräteprüfliste beschreibt konkrete nächste Prüfungen.

Lokale Pakete: `F:/Japanischtool/github-JapanischTrainer/release/11.0.7/windows/` und `F:/Japanischtool/github-JapanischTrainer/release/11.0.7/android/`. Nachweise: `validation/public-release-1107.json`, `validation/public-1107/windows-public-ui.json`, `validation/public-1107/android-public-signature.txt`, `validation/packaged-content-1107.json` und `validation/source-safety-1107.json`.

## Vollständig heruntergeladene öffentliche Dateien

| Kanal | Datei | Bytes | SHA-256 |
| --- | --- | --- | --- |
| Windows | `ERKLAERUNGEN_UND_SPRACHPRUEFUNG.md` | 4430 | `371aa12597cb0615a1aae443af6580472c0d458a6a5176a1ed0323d554891407` |
| Windows | `GERAETEPRUEFUNG_11.0.7.md` | 2476 | `b5226b2d358db7c97fac12fdfaebfd76e771e99f6b8014d500d114281d766fbd` |
| Windows | `INSTALLIEREN_TESTVERSION.md` | 1538 | `a0fc7305d29d31c94c6ba2f1c7d936be8dbff662c843522197eb104be257231e` |
| Windows | `JapanischTrainer-11.0.7-Quellcode.zip` | 91893463 | `4fbb5e4da831a35947d18e2894d8f8d859c0af055a30234bed4853e94d7897c4` |
| Windows | `JapanischTrainer-11.0.7-Setup-x64.exe` | 846931186 | `06ba87bfc0d90c5a2eb33fa867328ce6c63353031ff37fe114c32b8fddc483eb` |
| Windows | `JapanischTrainer-11.0.7-Setup-x64.exe.sha256` | 105 | `0745b1047613d7eaa0ee11843b19157de69a47e58f30517aefbf0572404f6b72` |
| Windows | `JapanischTrainer-11.0.7-Update-x64.zip` | 134115608 | `122d815b33928572027383b313a3e5777b0bb9fa84a4046b9d695483e059c1c5` |
| Windows | `LICENSE.txt` | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| Windows | `RELEASE_NOTES_11.0.7_TEST.md` | 1525 | `6a0b862c367b0c49d9ece340b5ad5c1fa3aa68272161a09cb415c7d3ef674271` |
| Windows | `SHA256SUMS-Windows.txt` | 1360 | `10b5af30a2b24dd89e61dcd6e3a5612522422a4b8becd2b5b1546fa8992c7393` |
| Windows | `TESTBERICHT_UEBUNGSVIELFALT.md` | 6517 | `965a09576e3ad835bc00b7589c7fc9dd7c6a6a2f6eccdaa7a8747d7c3b82b1e0` |
| Windows | `UEBUNGSTYPEN_ABDECKUNG.csv` | 46496 | `5ec7764d4257256fe9737d6ede2dbead42a73c1825e8e80cb8ba9281380c20d7` |
| Windows | `UEBUNGSVIELFALT_UMSETZUNG.md` | 8138 | `1453f1ec99bcb2edf30eb1235259cb9433cf8edafadbb67e9adbe65f138af543` |
| Windows | `update.json` | 2593 | `7b2acc567635f85b353733ac770ffb791b3b7bd2eab4e8c11daf97f07dfccb9f` |
| Windows | `Windows-Testnachweise-11.0.7.zip` | 12244973 | `fb5be1e1717f645a67dec2a51f6854cd1d06213a219759691135a8b60b0ec945` |
| Android | `Android-Testnachweise-11.0.7.zip` | 3754194 | `144f3a3e39c9a1c3c2d7236450130d7a4f6e564da9d9fec12c5041bf945d647e` |
| Android | `android-update.json` | 654 | `45db279c2004879bb2f5606dd36c63d0e8fc4b26d9432bfcb5c49beb3c2d7504` |
| Android | `ERKLAERUNGEN_UND_SPRACHPRUEFUNG.md` | 4430 | `371aa12597cb0615a1aae443af6580472c0d458a6a5176a1ed0323d554891407` |
| Android | `GERAETEPRUEFUNG_11.0.7.md` | 2476 | `b5226b2d358db7c97fac12fdfaebfd76e771e99f6b8014d500d114281d766fbd` |
| Android | `INSTALLIEREN_TESTVERSION.md` | 1538 | `a0fc7305d29d31c94c6ba2f1c7d936be8dbff662c843522197eb104be257231e` |
| Android | `JapanischTrainer-11.0.7-Android-Quellcode.zip` | 91893463 | `4fbb5e4da831a35947d18e2894d8f8d859c0af055a30234bed4853e94d7897c4` |
| Android | `JapanischTrainer-11.0.7-Android.apk` | 61883330 | `9c48b69dc6a1ec5f0ebe950c380975618a9d729c81b225eb5ac972d2c2ca034e` |
| Android | `LICENSE.txt` | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| Android | `RELEASE_NOTES_11.0.7_TEST.md` | 1525 | `6a0b862c367b0c49d9ece340b5ad5c1fa3aa68272161a09cb415c7d3ef674271` |
| Android | `SHA256SUMS-Android.txt` | 1156 | `5277c457a3115a81c37fa364696a5feed8ee253bd90af835712f0330b35a4522` |
| Android | `TESTBERICHT_UEBUNGSVIELFALT.md` | 6517 | `965a09576e3ad835bc00b7589c7fc9dd7c6a6a2f6eccdaa7a8747d7c3b82b1e0` |
| Android | `UEBUNGSTYPEN_ABDECKUNG.csv` | 46496 | `5ec7764d4257256fe9737d6ede2dbead42a73c1825e8e80cb8ba9281380c20d7` |
| Android | `UEBUNGSVIELFALT_UMSETZUNG.md` | 8138 | `1453f1ec99bcb2edf30eb1235259cb9433cf8edafadbb67e9adbe65f138af543` |

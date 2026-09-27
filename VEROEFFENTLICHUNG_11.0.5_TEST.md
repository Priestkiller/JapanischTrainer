# Öffentliche Kontrolle der Testversion 11.0.5

Am 27.09.2026 nach ausdrücklicher Testkanal-Freigabe veröffentlicht und anschließend tatsächlich geprüft:

- [Windows 11.0.5 Testversion](https://github.com/Priestkiller/JapanischTrainer/releases/tag/windows-test-v11.0.5).
- [Android 11.0.5-android.1-test](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.5-1), Code 11000501.

Beide sind öffentliche Prereleases, keine Latest-Ausgabe. Die stabile Version bleibt v11.0.4 beziehungsweise android-v11.0.4-1. Ihre 20 Dateien sind in Größe und SHA-256 unverändert; GitHubs Latest-Endpunkt liefert weiter v11.0.4. Eine spätere Übernahme in den stabilen Kanal benötigt eine neue ausdrückliche Nutzerfreigabe.

## Tatsächliche öffentliche Downloads

Alle 24 bereitgestellten Dateien wurden nach der Freischaltung ohne GitHub-Anmeldung vollständig heruntergeladen und mit lokalen geprüften Paketen und GitHub-Asset-Metadaten verglichen. Größe, SHA-256 und Plattform-/Tag-Zuordnung stimmen. Das umfasst Setup, Update-ZIP, APK, Metadaten, Quellen, Lizenzen, Prüfberichte und Prüfsummen.

Das öffentliche Windows-Manifest bestand die bestehende Ed25519-Prüfung. Der produktive Entpacker prüfte und entpackte das öffentlich geladene ZIP anhand aller Paketpfade, Dateigrößen, Hashes, erforderlichen Dateien, Version und vorhandenen Modell-Hashes in einen isolierten Testordner. Windows-EXE/Setup tragen 11.0.5. Es wurde kein Update in einer persönlichen Installation ausgeführt.

Die öffentlich heruntergeladene APK bestand apksigner mit demselben Herausgeberzertifikat wie 11.0.4: SHA-256 `3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9`. aapt bestätigt `de.priestkiller.japanischtrainer`, Code 11000501 und Name 11.0.5-android.1-test. Kursinhalt und Quellen stimmen mit dem geprüften Stand überein.

## Updateerkennung gegen die echte Quelle

| Installierter Stand | Reguläre Windows-Suche | Windows-Testsuche | Regulärer Android-Kanal | Android-Testkanal |
| --- | --- | --- | --- | --- |
| 11.0.2 | 11.0.4 | 11.0.5 | 11000401 | 11000501 |
| 11.0.4 | kein Angebot | 11.0.5 | kein Angebot | 11000501 |
| 11.0.5 | kein Angebot | kein Angebot | kein Angebot | kein Angebot |

Windows verwendet den tatsächlichen unveränderten `check_update`-Code mit isolierten Versionsvorgaben. Android wurde anhand der echten öffentlichen Releases und Metadaten mit derselben nativen Filter-/Versionsregel nachgerechnet; die nativen Kanalfilter und Oberfläche wurden separat im Android-15-Emulator geprüft. Dies ist keine behauptete öffentliche Installation auf dem S24 Ultra. Kein Download oder Installationswechsel auf einem Nutzersystem wurde ausgelöst. Die bisherige Windows-Updateprüfung 11.0.4 → 11.0.5 verwendete eine isolierte lokale TLS-Quelle und ist getrennt dokumentiert.

## Quellen und Prüfgrenzen

Gemeinsamer Quellarchiv-Commit: `fa705dc3a6f5831148463794e4ce062ecb88a840`. Android-Programm-/CI-Stand: `44dec2696565b0649dfc2adeab56880688f30335`. Spätere Änderungen ergänzen Windows-Versionsanzeige, README und Dokumentation, ohne Android-Programmdateien zu ändern. Windows-Laufzeitkorrektur: `f7cc55a`. Dieser öffentliche Nachweis ergänzt den vor dem Upload erstellten technischen Bericht.

161 Python-Tests, 34 mobile Logiktests, 20 Installerprüfungen, 25 native Windows-Lektionen, 75 mobile Oberflächenfälle und sechs native Android-Tests bestanden. Eigene sprachliche Durchsicht: insgesamt 80 Lektionen / 378 Karten. Erfassung: 150 Lektionen / 680 Karten. Menschliche Fachprüfung, Anfänger-Erprobung, echte Mikrofon-/Hörprüfung am S24 Ultra und ein frisches Windows-System bleiben offen. Der Windows-Installer ist weiterhin nicht Authenticode-signiert.

Lokale Nachweise: `validation/public-release-1105.json`, `validation/public-audit-1105.log` und `validation/public-1105/android-public-signature.txt`. Testpakete: `F:/Japanischtool/github-JapanischTrainer/release/11.0.5/windows` und `F:/Japanischtool/github-JapanischTrainer/release/11.0.5/android`.

## Abgeglichene Dateien

| Kanal | Datei | Bytes | SHA-256 |
| --- | --- | --- | --- |
| Windows | `GERAETEPRUEFUNG_11.0.5.md` | 4469 | `13120a346f2c04578a8382d60e4813eaabd503e30775852f40d5d318918a91ef` |
| Windows | `INSTALLIEREN_TESTVERSION.md` | 1407 | `cada6b2628c50703b345016e3326fde67f3721cc3bf151abb28b519f7d3babfe` |
| Windows | `JapanischTrainer-11.0.5-Quellcode.zip` | 91704517 | `af9bbb32701d2ef87b2b5d614149362c164d5f5b7ba526132d5f85a39285827d` |
| Windows | `JapanischTrainer-11.0.5-Setup-x64.exe` | 846886594 | `0e5aa91687253affe53e4a1010e52208eee93655efc5889a3fdceef899e2caea` |
| Windows | `JapanischTrainer-11.0.5-Setup-x64.exe.sha256` | 105 | `682fccb680b1cb9ca17e6f4397dad0399d7b1c9fbe0d274e3247a9377467a216` |
| Windows | `JapanischTrainer-11.0.5-Update-x64.zip` | 134041007 | `6d367691c5d4166be3c1a00b73fa8f9247e777667c2969f6de60832d7b015630` |
| Windows | `LICENSE.txt` | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| Windows | `PAKET_03.md` | 34163 | `6a93ac7d15359a351f047a0d8c91506a0cf312480e69803718e4f1292ef02272` |
| Windows | `RELEASE_NOTES_11.0.5_TEST.md` | 2267 | `e6a1c0825335e2aaf6e984927121683da80fbfc1bd36facfe79c6d42435e5ded` |
| Windows | `SHA256SUMS-Windows.txt` | 1143 | `f57c43e8598e62b7d32f95e468ca5191d82cf92fbff2cb7a30121c9a6ba6532a` |
| Windows | `TESTBERICHT_11.0.5_TEST.md` | 11121 | `5614cc08e7340e873bed557d0400f3b82029bc4d9524566fc1ffb4949687d659` |
| Windows | `update.json` | 3601 | `6e1b13d1021a1cceefa225c79d83643433f330402df2797ce245e7dd0e36f085` |
| Windows | `Windows-Testnachweise-11.0.5.zip` | 3687852 | `31bcda9d1ffce9d4c8eaa85170caf0358f441d421a167a925524df06e9a271fd` |
| Android | `Android-Testnachweise-11.0.5.zip` | 3687852 | `31bcda9d1ffce9d4c8eaa85170caf0358f441d421a167a925524df06e9a271fd` |
| Android | `android-update.json` | 647 | `bcc20a86fa0d00d30d933a89f84faeeb81ccca2a8030261b0898755cd32d050c` |
| Android | `GERAETEPRUEFUNG_11.0.5.md` | 4469 | `13120a346f2c04578a8382d60e4813eaabd503e30775852f40d5d318918a91ef` |
| Android | `INSTALLIEREN_TESTVERSION.md` | 1407 | `cada6b2628c50703b345016e3326fde67f3721cc3bf151abb28b519f7d3babfe` |
| Android | `JapanischTrainer-11.0.5-Android-Quellcode.zip` | 91704517 | `af9bbb32701d2ef87b2b5d614149362c164d5f5b7ba526132d5f85a39285827d` |
| Android | `JapanischTrainer-11.0.5-Android.apk` | 61825780 | `880f355019a77cf2eac0512890f4fce5e68acebefd4bdbf4cceb8748e9aff31f` |
| Android | `LICENSE.txt` | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| Android | `PAKET_03.md` | 34163 | `6a93ac7d15359a351f047a0d8c91506a0cf312480e69803718e4f1292ef02272` |
| Android | `RELEASE_NOTES_11.0.5_TEST.md` | 2267 | `e6a1c0825335e2aaf6e984927121683da80fbfc1bd36facfe79c6d42435e5ded` |
| Android | `SHA256SUMS-Android.txt` | 939 | `8ab73ad2e1105b61f85c0aa8f2b9085702e39286872ffd01f06ff28227d507ec` |
| Android | `TESTBERICHT_11.0.5_TEST.md` | 11121 | `5614cc08e7340e873bed557d0400f3b82029bc4d9524566fc1ffb4949687d659` |

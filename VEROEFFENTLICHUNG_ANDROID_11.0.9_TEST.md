# Öffentliche Nachkontrolle Android 11.0.9 Testversion

28. September 2026. Android 11.0.9-android.1-test, VersionCode 11000901.
[Öffentliches Prerelease](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.9-1).
[APK herunterladen](https://github.com/Priestkiller/JapanischTrainer/releases/download/android-test-v11.0.9-1/JapanischTrainer-11.0.9-Android.apk).

## Tatsächlich geprüft

Alle elf Release-Dateien wurden nach Veröffentlichung ohne Anmeldung vollständig heruntergeladen und mit lokalen Dateigrößen und SHA-256 verglichen. Die öffentliche APK bestand APK-v3-Signaturprüfung mit dem bisherigen Herausgeberzertifikat, 16-KB-Zipalignment, Paketkennung und Versionskontrolle. Kursdateien stimmen mit dem zugehörigen Quellstand überein; VAD-Modell und Lizenz sind enthalten. Vor Freigabe waren alle elf Uploads im Entwurf ebenfalls vollständig und hashgleich.

APK: 64.890.234 Bytes, SHA-256 `71a0c80b10fd8bb9cb45af9443c9961527d858c37e32e029815833631e50edb5`. Paket `de.priestkiller.japanischtrainer`. Zertifikat-SHA-256 `3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9`.

Programmstand des finalen Builds: `a30923f6a4cd31d41dfa856001f6fef4486799a8`. Quellarchiv: `f8705d655fb0f89bff22511e5261b41c86330b26`, enthält zusätzlich die fertigen Prüfberichte. Alle produktiven Webdateien einschließlich Hintergrund, vier Kursdateien, Versions-/Modellmetadaten und VAD stimmen bytegenau zwischen APK und diesem Quellarchiv überein. Die Paketprüfung schließt private Schlüssel, Zugangsdaten, Lernstände, Aufnahmen und private Referenzbilder aus. Eigene Testprofile enthalten keine persönlichen Nutzerstände.

Die 150 zuvor vorhandenen Dateien der 16 bestehenden Releases blieben anhand ihrer öffentlichen Namen, Größen, Digests, Downloadziele und Release-Zuordnung unverändert. Latest bleibt `v11.0.4`. Kein Windows-Paket wurde neu veröffentlicht; Windows-Test bleibt 11.0.7.

## Reguläre Suche und Testversionssuche

Androids unveränderte native Filterregel wurde mit den tatsächlich öffentlichen Release-Listen und Manifesten auf dem Prüfhost nachgerechnet. Native Filter und getrennte Lernprofile wurden separat im Android-Emulator geprüft. Dies ist kein öffentlicher Installationsversuch auf dem S24 Ultra. Windows wurde mit der produktiven Updatefunktion gegen die echte Quelle geprüft, ohne Installation.

| Installierter Android-Stand | Reguläres Angebot | Testangebot |
| --- | --- | --- |
| 11.0.2 | 11.0.4 | 11.0.9 |
| 11.0.4 | keines | 11.0.9 |
| 11.0.7 | keines | 11.0.9 |
| 11.0.8 | keines | 11.0.9 |
| 11.0.9 | keines | keines |

Windows 11.0.4 findet im Testkanal weiter 11.0.7; Windows 11.0.7 findet keine höhere Ausgabe. Die neue Android-Ausgabe wird nicht als Windows- oder stabiles Android-Update angeboten. Keine automatische Installation oder automatischer Download beim Nutzer.

Direkt nach Freigabe fehlte das neue Release noch in der zwischengespeicherten öffentlichen Liste. Nach deren Aktualisierung bestand die vollständige anonyme Nachkontrolle. Vor Freigabe wurden alte Fehlversuchs-Screenshots aus dem Nachweisarchiv entfernt, der Entwurf aktualisiert und alle elf Größen/Hashes erneut verglichen. Die Fehler und ihre Korrekturen bleiben im Prüfbericht dokumentiert.

## Softwareprüfung und Grenzen

180 Python- und 51 JavaScript-Tests bestanden. Vollständiger Browser-Lernablauf in sieben Formaten; Zusatzübungen mit 100 Einstiegen und 36 Interaktionen in vier Formaten; Sprechoberfläche in vier Formaten. 300 Pflichtschrittansichten in fünf Formaten und alle 156 Zusatzaufgaben bei 412 × 915, zusätzlich zwei Browserprüfungen mit 140 Prozent Schrift und kleiner Höhe. Browser-Audioereignisse sind simuliert.

[Finaler Android-Build 36423006309](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36423006309): 13 Tests bestanden, null Fehler und übersprungene Tests. Einschließlich echter Bildschirmtastatur bei 140 Prozent, Rotation, Profilübernahme, einer Kurzlautansicht ohne vertikales Scrollen und tatsächlicher Offline-Modellinferenz mit synthetischem Audio. Android Lint: null Fehler, zehn bestehende Warnungen. CI enthält nicht blockierende Hinweise zu Action-Versionen und zukünftigem Runner-Wechsel. Kein erneuter umfassender Erkennungsvergleich aus 11.0.8; die Erkennungslogik ist unverändert.

Eigene visuelle Durchsicht der Browser- und Emulatorbilder erfolgte getrennt von automatischen Tests. Echte S24-Ultra-Bedienung, Mikrofon-/Hörprüfung, Anfänger-Erprobung und menschliche Japanisch-Fachprüfung bleiben offen. Kurs: unverändert 150 Lektionen/680 Karten und 156 Zusatzaufgaben in 25 Lektionen. Eigene bisherige sprachliche Durchsicht: 105 Lektionen/501 Karten; 45 Lektionen/179 Karten weiter offen.

Lokale Pakete: `F:/Japanischtool/github-JapanischTrainer/release/11.0.9/android/`.
Lokaler öffentlicher Prüfbeleg: `validation/public-release-1109.json`.
[Prüfbericht](TESTBERICHT_ANDROID_11.0.9.md), [S24-Ultra-Prüfliste](GERAETEPRUEFUNG_ANDROID_11.0.9.md).
Eine spätere Übernahme als stabile Ausgabe benötigt weiterhin ausdrückliche Freigabe.

## Vollständig geprüfte öffentliche Dateien

| Datei | Bytes | SHA-256 |
| --- | --- | --- |
| `Android-Testnachweise-11.0.9.zip` | 30459591 | `8d7ccdf97ebb7d421416459d8f3211b85bfea730065d8bd196529d3bd21b21b4` |
| `android-update.json` | 763 | `ced955b0e2d7fd25f2dc1ec3bee7db94636b1bfe3c48cff34fa2a7ca8bc88243` |
| `GERAETEPRUEFUNG_ANDROID_11.0.9.md` | 2170 | `54589bd462d19acb08804a6fe0e8f279afec72d55cecb104b600cfb4b7f0beb3` |
| `JapanischTrainer-11.0.9-Android-Quellcode.zip` | 94779828 | `6a005d65331fcf2184fce01c9a5f027f868dd80a25999f26a46e80dd63a28242` |
| `JapanischTrainer-11.0.9-Android.apk` | 64890234 | `71a0c80b10fd8bb9cb45af9443c9961527d858c37e32e029815833631e50edb5` |
| `LICENSE.txt` | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| `MODEL_ATTRIBUTION.txt` | 1809 | `7fcc4c13045a7adb8a530ea96bf91428e1fe50ac8916de784facc5acf48697a0` |
| `MODEL_LICENSES.txt` | 39957 | `1811e941af070c14bfcf569d572fa029765de3f7ca447bb386deeadb02c9e7af` |
| `RELEASE_NOTES_ANDROID_11.0.9_TEST.md` | 1292 | `23a37db5bf20b5db3b9f2086d1d692fb65ab3b5025b4f1c1d43d803753948e13` |
| `SHA256SUMS-Android.txt` | 959 | `0b2798b7e8c9571b3c07abfc7df7281f95cfdeeeb10b4de6b49ff698e30843ca` |
| `TESTBERICHT_ANDROID_11.0.9.md` | 7253 | `178ccdd28eea7e9fc4553620e73be3da37cc9339c46e9f16045fabfb9726277f` |

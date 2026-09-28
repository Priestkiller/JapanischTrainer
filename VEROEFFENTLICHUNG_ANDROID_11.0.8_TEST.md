# Öffentliche Nachkontrolle Android 11.0.8 Testversion

28. September 2026. Android 11.0.8-android.1-test, VersionCode 11000801.
[Öffentliches Prerelease](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.8-1).
[APK herunterladen](https://github.com/Priestkiller/JapanischTrainer/releases/download/android-test-v11.0.8-1/JapanischTrainer-11.0.8-Android.apk).

## Tatsächlich geprüft

Alle elf Release-Dateien wurden nach Veröffentlichung ohne Anmeldung vollständig
heruntergeladen und gegen lokale Bytes/SHA-256 geprüft. Bereits im Entwurf waren
alle elf Uploads vollständig und hashgleich. Die öffentliche APK bestand
apksigner, dasselbe Herausgeberzertifikat, Zipalignment, Paketkennung und
Versionskontrolle. Kursdaten und Quellen stimmen überein, VAD-Modell und Lizenz
sind enthalten. Quellarchiv: 8d08a0a906c58114c09b7b48847eab8652986694;
APK-Build: 3aca9864c8398771797c29072f50798a9b496222.

Alle 139 zuvor vorhandenen Dateien der 15 bestehenden Releases sind anhand
ihrer öffentlichen Dateinamen, Größen, Digests, Downloadziele und Release-Zuordnung
unverändert. Latest bleibt v11.0.4; kein Windows-Paket wurde neu veröffentlicht.
Quell-/Paketprüfung schließt private Schlüssel, Zugangsdaten, Lernstände,
Aufnahmen und die fremden Referenzbilder aus.

## Testsuche und reguläre Suche

Androids unveränderte native Filterregel wurde mit den tatsächlich öffentlichen
Release-Listen und Manifesten auf dem Prüfhost nachgerechnet. Native Filter und
isolierte Lernprofile wurden separat im Android-Emulator geprüft. Dies ist kein
öffentlicher Installationsversuch auf dem S24 Ultra. Windows wurde über die
produktive Updatefunktion gegen die echte Quelle geprüft, ohne Installation.

| Installierter Stand | Reguläres Android-Angebot | Android-Testangebot |
| --- | --- | --- |
| 11.0.2 | 11.0.4 | 11.0.8 |
| 11.0.4 | keines | 11.0.8 |
| 11.0.7 | keines | 11.0.8 |
| 11.0.8 | keines | keines |

Windows 11.0.4 findet im Testkanal weiterhin nur 11.0.7; Windows 11.0.7 findet
kein höheres Update. Die neue Android-Ausgabe wird von Windows nicht angeboten.
Kein automatischer Download und kein Installationsstart beim Nutzer.

Unmittelbar nach Freigabe fehlte das neue Release noch in der zwischengespeicherten
öffentlichen Liste. Nach ihrer Aktualisierung bestanden alle Prüfungen ohne
künstliches Testrelease. Bei der Quellenpaketierung wurden Windows-Zeilenenden
zunächst als Unterschied erkannt; ein Archiv mit unveränderten Git-LF-Zeilenenden
ist nun bytegleich mit den APK-Web-/Kursressourcen. Eine fehlerhaft gequotete lokale
Metadaten-Prüfzeile wurde vor Freigabe durch eine erfolgreiche Skriptprüfung ersetzt.

## Umfang und offene Prüfung

180 Python-, 51 JavaScript- und zwölf native Android-15-Tests bestanden. Vollständiger
Browserablauf in sieben Formaten, Zusatzübungen in vier Formaten, getrennte
Aufnahme-/Selbstprüfungsfälle in vier Formaten. 144 synthetische Sprachsignale und
13 Negativkontrollen; Ergebnisse und auch Regressionen stehen im
[technischen Bericht](TESTBERICHT_ANDROID_11.0.8.md).
Native Prüfung [36413812852](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36413812852),
null Fehler/übersprungene Tests. Build und Lint bestanden; zehn Lint-Hinweise.

Echte S24-Ultra-Mikrofon-/Hörtests, Anfänger-Erprobung und menschliche
Japanisch-Fachprüfung sind offen. Die allgemeine Startseite und Windows-Gestaltung
bleiben unverändert. Eine stabile Übernahme braucht weiterhin ausdrückliche Freigabe.
Lokaler Paketordner: `F:/Japanischtool/github-JapanischTrainer/release/11.0.8/android/`.

## Vollständig geprüfte öffentliche Dateien

| Datei | Bytes | SHA-256 |
| --- | --- | --- |
| `Android-Testnachweise-11.0.8.zip` | 13793807 | `c258c8a0e6b62f3f56c0ca324035e58b5761c7e93df8136ef49ae681f622de3c` |
| `android-update.json` | 709 | `b794b8c4ef5a360f61a3fdac47bc581961680d8f79e12b48b0ae0683fcc05355` |
| `GERAETEPRUEFUNG_ANDROID_11.0.8.md` | 2621 | `d7938dfbce221e3c6cdfadd0e3253d43918ccd9fff6b4447ffec52cdbb3fea9c` |
| `JapanischTrainer-11.0.8-Android-Quellcode.zip` | 92428276 | `3183c0b6ee10d25bce47eb6a693d68598c6dfd59b4caac9c2aef405644d78b5a` |
| `JapanischTrainer-11.0.8-Android.apk` | 62539053 | `1d6a2c9dac155a949ae592fa2d453e92e51e2cd229caaea01372b36abb653d58` |
| `LICENSE.txt` | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| `MODEL_ATTRIBUTION.txt` | 1809 | `7fcc4c13045a7adb8a530ea96bf91428e1fe50ac8916de784facc5acf48697a0` |
| `MODEL_LICENSES.txt` | 39957 | `1811e941af070c14bfcf569d572fa029765de3f7ca447bb386deeadb02c9e7af` |
| `RELEASE_NOTES_ANDROID_11.0.8_TEST.md` | 2274 | `f2a6f567745e389311d4c9ed39a5098fbcf64980eac682bc52256431d0aff45b` |
| `SHA256SUMS-Android.txt` | 959 | `efdf3a9bac310d6ef67074a296024234c188cec05ce4c01334ef496cf97b44be` |
| `TESTBERICHT_ANDROID_11.0.8.md` | 10258 | `302f420d4fd2190ec45234ea700de9820856eddb1b09c16145c6db8ca4f52182` |

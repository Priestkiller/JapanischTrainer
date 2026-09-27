# Öffentliche Kontrolle der Testversion 11.0.6

Am 27.09.2026 im ausdrücklich freigegebenen Testkanal veröffentlicht und nach dem Upload tatsächlich geprüft:

- [Windows 11.0.6 Testversion](https://github.com/Priestkiller/JapanischTrainer/releases/tag/windows-test-v11.0.6).
- [Android 11.0.6-android.1-test](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.6-1), Code 11000601.

Beide Ausgaben sind öffentliche Prereleases, keine Latest-Ausgabe. Die stabile 11.0.4 und die vorherige Testversion 11.0.5 wurden nicht verändert: alle 44 bisherigen Assets stimmen mit dem vor Upload gesicherten öffentlichen Stand in Namen, Größen, SHA-256, Downloadzuordnung und Release-Eigenschaften überein. Latest liefert weiterhin v11.0.4. Keine erneuten Downloads unveränderter alter Pakete; ihre vorhandenen Nachweise bleiben gültig. Eine spätere stabile Übernahme erfordert weiterhin eine gesonderte ausdrückliche Freigabe.

## Tatsächliche öffentliche Nachkontrolle

Alle 24 neuen Release-Dateien wurden ohne GitHub-Anmeldung vollständig heruntergeladen. Größen, SHA-256 und Plattform-/Tag-Zuordnung stimmen mit den geprüften lokalen Dateien und GitHub-Metadaten überein. Das umfasst Setup, Update-ZIP, APK, Metadaten, Quellen, Lizenzen, Paketbericht, technische Nachweise, Installations-/Geräteanleitung und Prüfsummenlisten.

Das öffentliche Windows-Manifest bestand die produktive Ed25519-Prüfung mit dem bereits ausgelieferten Vertrauensschlüssel. Der unveränderte produktive Entpacker überprüfte das öffentliche ZIP einschließlich aller Paketpfade, Größen, Hashes, Pflichtdateien, Version und benötigten Modelle in einem separaten Testordner. Die Paketversion und Kursdatei sind 11.0.6. Die EXE und das Setup sind hashidentisch mit den lokal auf PE-Version 11.0.6.0 geprüften Dateien. Es wurde nichts in einer persönlichen Installation installiert.

Die öffentliche APK bestand apksigner mit dem bisherigen Zertifikat SHA-256 3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9. aapt bestätigt Paket de.priestkiller.japanischtrainer, Code 11000601 und Name 11.0.6-android.1-test. Ihr Kurs ist bytegleich mit den geprüften Quellen. Die unveränderte öffentliche Datei entspricht damit auch der lokal bestandenen v3-/16-KiB-Prüfung.

## Echte öffentliche Updateerkennung

| Installierter Stand | Windows regulär | Windows Test | Android regulär | Android Test |
| --- | --- | --- | --- | --- |
| 11.0.2 | 11.0.4 | 11.0.6 | 11000401 | 11000601 |
| 11.0.4 | kein Angebot | 11.0.6 | kein Angebot | 11000601 |
| 11.0.5 | kein Angebot | 11.0.6 | kein Angebot | 11000601 |
| 11.0.6 | kein Angebot | kein Angebot | kein Angebot | kein Angebot |

Windows: unveränderte produktive check_update-Funktion gegen die echten Quellen, zusätzlich der native Update-Dialog mit drei separaten synthetischen Profilen für 11.0.4, 11.0.5 und 11.0.6. Der Testbutton findet 11.0.6 aus den älteren Profilen, die reguläre Suche bleibt leer; ein Kanalwechsel entfernt das Angebot. Kein automatischer Download oder Installationsstart, und die Testprofile blieben bytegleich. Der gespeicherte Screenshot zeigt das tatsächliche öffentliche Angebot.

Ein erster Windows-Prüfhilfenlauf mit mehreren nacheinander erzeugten Tk-Hauptfenstern brach beim Schließen ab. Die drei Versionen wurden danach jeweils in einem eigenen Prozess mit eigenem Profil vollständig und erfolgreich geprüft. Keine Änderung an der produktiven Updateoberfläche war dafür nötig.

Android: Auswahl anhand echter öffentlicher Releases und Manifestdateien mit derselben unveränderten nativen Filter-/Versionsregel nachgerechnet. Native Filter und Oberfläche wurden separat im Android-15-Emulator geprüft. Das ist keine öffentliche Installation auf einem echten S24 Ultra. Der vollständige Windows-Update-Durchlauf 11.0.5 → 11.0.6 nutzte eine eigene lokale TLS-Quelle und ein Testprofil; Produktionssignatur und öffentliche Dateien wurden davon getrennt geprüft.

## Zugehöriger Quellstand und Grenzen

Quellarchiv und Release-Ziel: 83e1733af661f10da7a4f14a1fe9717d78a50c42. Produktstand 1df3e57425a03998275e3328954dcee2d2f1c0b1. Finaler [Android-Prüflauf 36347546310](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36347546310) auf f7ef4b0031ec1dbdfb701a78803cdf38a43dab07; nach dem Produktstand wurden nur native Testisolation, Screenshot-Fokus und die kurzlebige Emulatorumgebung korrigiert. Weitere Änderungen ergänzen Berichte. Beide Quellarchive enthalten passende Lizenz- und Bibliotheksquellen; geprüfte Ausschlüsse für Schlüssel, Zugangsdaten, Nutzeraufnahmen und persönliche Lernstände.

167 Python-Tests einschließlich 24 Updateprüfungen, 20 Installerverträge, 39 mobile Logiktests, 25 native Windows-Lektionen plus Zahlenhilfe, 75 mobile Paketfälle und vollständiger mobiler Ablauf in sieben Formaten bestanden. Der finale native Android-Lauf bestand 8 Tests, ohne Fehler oder übersprungene Tests, mit unverdeckten Screenshots. Frühere Fehlversuche und ihre Korrekturen stehen im technischen Bericht; die überdeckten Bilder eines Zwischenlaufs gelten nicht als saubere visuelle Abnahme.

Erfasst: 150 Lektionen / 680 Karten. Selbst durchgesehen: 105 eindeutige Lektionen / 501 Karten. Paket 04 ergänzt keine neuen Lektionen; die gesonderte Zahlenhilfe wird nicht doppelt gezählt. Menschliche Fachprüfung, Anfänger-Erprobung, echte Mikrofon-/Hörprüfung am S24 Ultra und frisches Windows bleiben offen. Windows-Setup weiterhin ohne Authenticode-Zertifikat. Die Grenzen fester Offline-Gesprächswege bleiben ausdrücklich erhalten.

Lokale Pakete: F:/Japanischtool/github-JapanischTrainer/release/11.0.6/windows und F:/Japanischtool/github-JapanischTrainer/release/11.0.6/android. Nachweise: validation/public-release-1106.json, validation/public-1106/windows-public-ui.json, validation/public-1106/android-public-signature.txt und validation/source-safety-1106.json. Der Bericht ergänzt die bereits ausgelieferten Prüfunterlagen und ist im Repository sowie über die Release-Hinweise erreichbar.

## Abgeglichene öffentliche Dateien

| Kanal | Datei | Bytes | SHA-256 |
| --- | --- | --- | --- |
| Windows | `GERAETEPRUEFUNG_11.0.6.md` | 4147 | `3cc6ab5fde963d1377fc04eb9ad9f2af6242efd79fad61a454782c933f418443` |
| Windows | `INSTALLIEREN_TESTVERSION.md` | 1407 | `4cd82da4279f2b966be4b9729d6a34e7bd888b63d51f0f0c03e28557b729d126` |
| Windows | `JapanischTrainer-11.0.6-Quellcode.zip` | 91809342 | `4f23e79a2fb54765b39850b5bf5e516af1db8621acd21e72062a0d82d6f59f8c` |
| Windows | `JapanischTrainer-11.0.6-Setup-x64.exe` | 846939391 | `2cf65cb8273b5e6e35a479b3475031d83b4e64f1967811d55faf97f3341be66e` |
| Windows | `JapanischTrainer-11.0.6-Setup-x64.exe.sha256` | 105 | `5c8ff9fb30af25b7db8f76ff0ebd021b60167a264c620c3099f31b50296f4ecc` |
| Windows | `JapanischTrainer-11.0.6-Update-x64.zip` | 134061176 | `a43a3a901dfc402b25c668d9e7f16d90e2f821427af32ba153e849f6b0736caf` |
| Windows | `LICENSE.txt` | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| Windows | `PAKET_04.md` | 76881 | `5476deb62f35c4fccf75f6ee79311ec4a9a833e7a8cd79b294e3450109c01be9` |
| Windows | `RELEASE_NOTES_11.0.6_TEST.md` | 2875 | `ed501be6cc623188487e888a1923c17a2fb7ff1a156d90aeeee379d24597bc2e` |
| Windows | `SHA256SUMS-Windows.txt` | 1143 | `94c28fb32420b315658a3ace7281cac93ca1830b99fed96c0936a482a2d1b317` |
| Windows | `TESTBERICHT_11.0.6_TEST.md` | 10931 | `bc09b6ad0ac892fd3cca4cf663bf151643f62eeddac824e50e6eff6e2e89429f` |
| Windows | `update.json` | 4417 | `d320e018647d3255e1f3c5a7d2a5b9a04b85921fb646ea779e7388efc78cf2a4` |
| Windows | `Windows-Testnachweise-11.0.6.zip` | 5912547 | `29679b551652133ce815031d44f0a124a37dcf80bb8a3e082412a078aff60b58` |
| Android | `Android-Testnachweise-11.0.6.zip` | 5912547 | `29679b551652133ce815031d44f0a124a37dcf80bb8a3e082412a078aff60b58` |
| Android | `android-update.json` | 656 | `be5b4f8e6211352c9a00f6d125e85e052e5af43a97dff7cff412286c39224517` |
| Android | `GERAETEPRUEFUNG_11.0.6.md` | 4147 | `3cc6ab5fde963d1377fc04eb9ad9f2af6242efd79fad61a454782c933f418443` |
| Android | `INSTALLIEREN_TESTVERSION.md` | 1407 | `4cd82da4279f2b966be4b9729d6a34e7bd888b63d51f0f0c03e28557b729d126` |
| Android | `JapanischTrainer-11.0.6-Android-Quellcode.zip` | 91809342 | `4f23e79a2fb54765b39850b5bf5e516af1db8621acd21e72062a0d82d6f59f8c` |
| Android | `JapanischTrainer-11.0.6-Android.apk` | 61850356 | `ccaf877b20040a83485358c4b9f2c8e3f92b4058efec20655bb9bc912c8a7064` |
| Android | `LICENSE.txt` | 35147 | `8ceb4b9ee5adedde47b31e975c1d90c73ad27b6b165a1dcd80c7c545eb65b903` |
| Android | `PAKET_04.md` | 76881 | `5476deb62f35c4fccf75f6ee79311ec4a9a833e7a8cd79b294e3450109c01be9` |
| Android | `RELEASE_NOTES_11.0.6_TEST.md` | 2875 | `ed501be6cc623188487e888a1923c17a2fb7ff1a156d90aeeee379d24597bc2e` |
| Android | `SHA256SUMS-Android.txt` | 939 | `3bea2f7e750ed25546360b5365d743390360730b157b2d72aee93b308e6fa840` |
| Android | `TESTBERICHT_11.0.6_TEST.md` | 10931 | `bc09b6ad0ac892fd3cca4cf663bf151643f62eeddac824e50e6eff6e2e89429f` |

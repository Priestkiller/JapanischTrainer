# Veröffentlichung Android 11.0.13 Testversion

Abschluss der öffentlichen Prüfung am 1. Oktober 2026. Ausschließlich Android-Testkanal, Prerelease android-test-v11.0.13-1. Kein reguläres Latest-Update. Windows bleibt Test 11.0.11; beide stabil bei 11.0.4. Eine stabile Übernahme ist nicht freigegeben.

Version 11.0.13-android.1-test, Code 11001301; Paket de.priestkiller.japanischtrainer. Geprüfter Quellstand f24b0f0cdf85dbfd17ec2de7a0efb021a067ee31. CI: https://github.com/Priestkiller/JapanischTrainer/actions/runs/36880658183.

## Tatsächlich umgesetzt

Lernserie, XP und Lektionsfortschritt stehen auf der Startseite vor Hero und Tagesrunde. Ein Monatskalender zeigt bekannte Lerntage, heute und Monatsnavigation. Zusätzliche Datumsfelder erhalten IDs, Abschlüsse, Lehrer, XP, alte Serie und letzten bekannten Tag. Nicht gespeicherte historische Tage werden ausdrücklich nicht erfunden. Öffnen allein zählt nicht als Lernen.

Kiko verwendet ein neues transparentes 4×4-Raster mit acht ruhigen und acht Jubelphasen; Kopf, Augen, Pfoten und Schwanz verändern sich. Antippen begrüßt, ein echter Abschluss jubelt kurz. Verdeckte Ansichten, ausgeschaltete und reduzierte Bewegung halten an. Artwork-Herkunft und vollständige Generierungs-/Korrekturprompts sind im passenden Quellenarchiv unter mobile/ARTWORK_11.0.13.md enthalten. Die alte fehlerhafte zusätzliche Körperform wird in Android ersetzt; Windows-Grafiken bleiben unverändert.

Die Abschlussansicht bleibt ausdrücklich dunkel, zeigt tatsächliche XP und vergibt bei Wiederholung nichts erneut. Beide Abschlussaktionen sind oberhalb der Navigation erreichbar, während der Inhalt bei kleiner Höhe oder großer Schrift innerhalb der Karte scrollen darf. Das kleine Layout wurde nach einem tatsächlich gefundenen verdeckten Button korrigiert. Der Nutzerscreenshot wurde keiner ungesichert angenommenen Version zugeordnet.

Die Updatesuche unterscheidet DNS, Timeout, TLS, HTTP, Verbindungs- und Datenfehler. Die konkrete Ursache der früheren S24-Suchmeldung bleibt offen; eine Behebung wird nicht behauptet. Quellen, Filter, Schlüssel, Paketkennungen, Signaturprüfung und Downgradeschutz bleiben erhalten. Kein automatischer Download oder Installation.

## Automatische Software- und Paketprüfung

65 JavaScript-Tests bestehen Kurs, Aufgaben, Profile, Hilfen, XP und Kalender einschließlich Datumsgrenzen. 30 Browseransichten in sechs Bildschirm-/Schrift-/Bewegungsformaten und vier zusätzliche Profile bestehen die endgültige Darstellung einschließlich beider Abschlussaktionen, echter Sprite-Pixelwechsel und tatsächlichem Lerntag nach Fixtureabschluss. 85 Menü-/Lernansichten bestanden vor der letzten reinen Abschlusskorrektur; die endgültige native Suite prüft Hauptmenüs ebenfalls. Browserbrücken und Sprachereignisse waren simuliert.

Alle 20 nativen Android-Emulatorprüfungen bestehen: Kalender, alte Profile und Neustart, echte Kiko-Pixelwechsel, Erstabschluss, Wiederholung ohne erneute XP, Hauptmenüs, Übungen, Tastatur/Rotation, Trennung der Updatekanäle, Fehlermeldungen und Android-HTTPS gegen die echte öffentliche Quelle. Die installierte aktuelle 11.0.13 fand vor dem Upload korrekt keine höhere Version; das Profil blieb bytegleich. Modellprüfungen verarbeiteten synthetisches Audio, keine echten Mikrofonaufnahmen. Emulator API 35 x86_64, kein S24.

Erster nativer Lauf: 18/20 bestanden, Bewegung im Emulator ausgeschaltet und Antwortindex in der Fixture als Text angesprochen. Zweiter Lauf: 19/20 bestanden einschließlich Animation und Erstabschluss; die Wiederholungsfixture wurde beim Schließen der vorigen Activity überschrieben. Die korrigierte Prüfung verwendet dieselbe Activity mit bestehendem Profilimport und regulärem Sessionspeichern. Ein gestarteter Zwischenlauf wurde vorzeitig ersetzt, nicht als bestanden gewertet. Der endgültige Lauf besteht vollständig. Ein weiterer Versuch kam nach bestandenem Build nicht bis zu den nativen Tests: der Google-Download des Android-Emulators schlug fehl. Derselbe Quellstand wurde erneut geprüft; der abgebrochene Infrastrukturversuch ist kein Testnachweis. Der erste Node-Unterprozess war durch die Sandbox blockiert; ohne Prozessisolation bestand er. Diese Prüfhistorie bleibt erhalten.

Build und Lint: 0 Fehler, lokal 11 und CI 12 Warnungen. Windows-/Python-Tests wurden bei unveränderten Windows- und Kursquellen nicht wiederholt. APK v3-Signatur gültig, v2 nicht verwendet; bisheriges Herausgeberzertifikat SHA-256 3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9. Paketname, Versionsdaten und 16-KB-Alignment bestehen. 155 APK-Dateien stimmen bytegenau mit geprüftem Git-Stand und Quellenarchiv überein; neue Darstellungen auch mit CI. Build-Zeilenenden wurden zum Vergleich vereinheitlicht. Die Quellen-/Lizenzpakete enthalten keine privaten Schlüssel, Zugangsdaten, Lernstände oder Aufnahmen.

APK: 67,033,946 Bytes. SHA-256: 001344ac7edca6d100c625c65165e54bc6c47759498034da769eb9a2c98303cb.

## Prüfung nach dem öffentlichen Upload

APK, Quellen, Lizenzen, Versionsmetadaten, Prüfsummen und Prüfnachweise wurden anonym geladen und mit dem lokalen Paket über Größe und SHA-256 verglichen. Die öffentlich geladene APK besteht zusätzlich v3-Signatur, Herausgeberzertifikat, Paketkennung, Code 11001301 und 16-KB-Alignment; alle 155 Quellen-Dateien sind bytegleich. SOURCE_COMMIT und Update-Metadaten weisen denselben geprüften Stand aus.

Die echten öffentlichen Versionsdateien ergeben für Android 11.0.11 und 11.0.12 ausschließlich im Testkanal 11.0.13; auf 11.0.13 sind beide Suchen leer. Neun isolierte Profil-/Formatkombinationen bestanden die produktiven Web-Schaltflächen mit diesen öffentlichen Manifestdaten und einer simulierten nativen Brücke: Profile bytegleich, kein automatischer Download/Installation. Die produktive Windows-Suche auf 11.0.11 bietet in beiden Kanälen nichts Neueres. Die echte native Android-HTTPS-Prüfung ist oben getrennt angegeben; nach dem Upload wurde kein S24-Netzversuch behauptet.

Alle 24 vorherigen öffentlichen Releases mit 242 Dateien bleiben unverändert: IDs, Status, Namen, Größe, Digest und URL. Latest bleibt v11.0.4. Prüfbericht und eigener SHA-256-Nachweis werden nach der ersten Downloadkontrolle ergänzend hochgeladen; anschließend werden alle 16 öffentlichen Dateien nochmals als Gesamtbestand geprüft. Erstdaten, signierte APK und stabile Ausgaben werden nicht überschrieben.

## Eigene Sichtprüfung und offene menschliche Erprobung

Die eigene Sichtprüfung umfasst Kennzahlen oben, Kalender, Kiko-Grafik und dunklen Abschluss, kleine Ansicht, Querformat und große Schrift. Der native Wiederholungsscreenshot enthält den vorübergehenden Importhinweis der Testfixture; die reguläre Abschlussansicht löst keinen Importhinweis aus. Erreichbarkeit beider Aktionen ohne Importoverlay ist zusätzlich mit vier Browserprofilen geprüft. Die Sichtprüfung ist keine menschliche Anfänger- oder sprachliche Fachabnahme. Echte S24-Installation, Mikrofon-/Hörtest und Ursache der Handy-Suchmeldung bleiben offen. Lehrer, Stimmen und Sprachmodelle wurden nicht geändert; keine bessere Erkennungsqualität behauptet.

Kurs unverändert: 150 Lektionen, 680 Karten, Revision 11, Inhalt 11.0.7; 105 Lektionen/501 Karten vertieft, 156 Zusatzaufgaben. Sechs Schritte, Kana-Selbstprüfung und Sprechhilfe bleiben erhalten.

## Geräteprüfung auf dem S24 Ultra

1. APK über die bestehende App installieren, nicht deinstallieren. Version 11.0.13 und bisherigen Lernstand/Sprachpakete prüfen.
2. Kennzahlen oben und Lernserienkalender öffnen. Alte nicht gespeicherte Tage dürfen fehlen; bekannten letzten Lerntag und ehrlichen Hinweis prüfen.
3. Eine Lernaufgabe bearbeiten, danach die heutige Kalendermarkierung prüfen. Appaufruf allein darf nicht zählen.
4. Kiko antippen, Jubel beim Abschluss prüfen; ausgeschaltete/reduzierte Bewegung bleibt ruhig.
5. Beide Abschlussaktionen bei normaler und großer Schrift bedienen; Wiederholung gibt keine zweiten XP.
6. Beide Update-Suchen ausführen; auf 11.0.13 ist ohne höhere Ausgabe kein Angebot richtig. Bei Verbindungsfehler die genaue neue Meldung festhalten.
7. Hören und echte Mikrofonaufnahmen mit kurzen Kana, Wörtern und Sätzen prüfen. Dieser menschliche Test ist noch nicht durchgeführt.

## Downloads und lokale Ablage

[Android APK](https://github.com/Priestkiller/JapanischTrainer/releases/download/android-test-v11.0.13-1/JapanischTrainer-11.0.13-Android.apk) · [Testveröffentlichung](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-test-v11.0.13-1).

Lokale Lieferung: F:/Japanischtool/Testpakete/11.0.13/android/. Prüfevidenz: validation/public-1113/, validation/ci-1113-final/, validation/live-1113/ und validation/night-1113/. Zentrale Chronik: F:/Japanischtool/PROJEKTDOKUMENTATION_JapanischTrainer.md und lesbare Word-Ausgabe. Keine automatische Veröffentlichung weiterer Fassungen oder spätere stabile Übernahme.

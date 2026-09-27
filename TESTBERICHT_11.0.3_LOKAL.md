# JapanischTrainer 11.0.3 lokaler Teststand

Stand: 27.09.2026. Zweites Inhaltspaket tatsächlich in gemeinsamen Kursdaten, Windows-EXE und Android-APK umgesetzt. **Nicht veröffentlicht**; kein Push, Release, Tag oder Upload. Öffentliche Update-Dateien und Herausgeberschlüssel bleiben unverändert. Ausgangsstand: `21ad2d24d337b1cedb65a0345bad7d79f3121885`.

## Inhalt und Auswahl

25 vorhandene Lektionen mit 121 Karten überarbeitet. Keine neue Lektion nötig: fehlender Wortschatz und zunächst als Ganzes verwendete Muster lassen sich in den vorhandenen Einheiten vor der Prüfung erklären. Der Bestand bleibt 150 Lektionen / 680 Karten; nun 565 explizite Sprechziele. Paket 01 bleibt vollständig unverändert: 30 Lektionen / 138 Karten. Zusammen 55 Lektionen / 259 Karten durchgesehen und vertieft, weitere 95 einzeln zu prüfen.

| Position | Stabile ID | Überarbeitete Lektion |
| --- | --- | --- |
| 31 | v11:languages | Welche Sprache sprichst du? |
| 32 | v11:jobs | Über den Beruf sprechen |
| 33 | 14:0 | は・が・を・の |
| 34 | 15:0 | に・へ・で・と・も |
| 35 | 16:0 | あります・います |
| 36 | 13:0 | Was, wer, wo? |
| 37 | v11:this-that | Dieses hier, das da, jenes dort |
| 38 | v11:this-noun | Dieses Buch: この + Nomen |
| 39 | v11:whose | Wem gehört das? Besitz mit の |
| 40 | v11:here-there | Hier, da und dort |
| 41 | v11:existence | Was ist da? あります und います |
| 54 | 5:0 | を + Verb |
| 55 | v11:morning-evening | Aufstehen, schlafen und zurückkommen |
| 56 | v11:work-study | Arbeiten, lernen, lesen, schreiben |
| 57 | v11:location-action | Ziel, Ort und Verkehrsmittel |
| 58 | v11:polite-past | Höfliche Verben: gestern und heute |
| 62 | v11:rooms | Zimmer und Dinge in der Wohnung |
| 63 | v11:positions | Auf, unter, neben und in |
| 77 | v11:directions | Rechts, links und geradeaus |
| 86 | v11:smalltalk | Freundlich auf ein Gespräch reagieren |
| 87 | v11:hobbies | Was machst du gern? |
| 130 | v11:dialog-meeting | Dialog: eine neue Person kennenlernen |
| 133 | v11:dialog-directions | Dialog: den Bahnhof finden |
| 135 | v11:read-profile | Lesetext: Ren stellt sich vor |
| 136 | v11:read-day | Lesetext: ein gewöhnlicher Tag |

Die frühen Satzbaueinheiten liefern Voraussetzungen, die späteren Dialoge und Lesetexte greifen sie wieder auf. Zahlen-, Einkaufs- und andere Zwischenlektionen werden nicht pauschal wegen ihrer Reihenfolge bearbeitet. Ausführliche Lernziele, Vorwissen, Lehrtexte, Abrufimpulse und Szenenlücken: `F:/Japanischtool/dokumentation/kursanalyse/PAKET_02.md`. Die acht ursprünglichen Analyseberichte wurden aktualisiert; Paket 01 bleibt darin unverändert, Paket 02 ist eine zusätzliche neunte Datei.

## Belegte Verbesserungen

- 75 neue Guide-Absätze erklären notwendige Wörter mit Lesung/Bedeutung und grundlegende Muster vor der ersten Prüfung. Frühe て-Bitten und laufende Tätigkeit werden ausdrücklich als erklärte feste Formen behandelt; selbstständiges Beugen wird noch nicht erwartet.
- Ein unnötig frühes Vergangenheitsbeispiel in 14:0 wurde durch einen Existenzsatz ersetzt. Objekt- und Besitzbeispiele verwenden erklärten Wortschatz. Zugehörige alte Beispiel-Metadaten wurden ebenfalls abgeglichen. Kein bestehender Kartenzieltext oder dessen Lesung/Bedeutung wurde ersetzt.
- Alte String-Beispiele der ausgewählten Legacy-Lektionen sind nun als JP/Romaji/DE-Objekte für beide Anwendungen nutzbar. Das irreführende Leseintro über ständig sichtbare Übersetzungen wurde korrigiert.
- 25 gezielte Transferfragen ergänzen bestehende Übungen. Alle 121 ausgewählten Karten erklären falsche Anwendungsantworten. Bedeutung/Hören unterscheiden gewählte und gesuchte Form; beim Hören bezieht sich die Erklärung auf die tatsächlich abgespielte Karte. Aufbau-/Schreibfehler bekommen passende Hinweise.
- Android-Hörantworten stammen wie unter Windows nur aus bereits eingeführten Karten. Die Übersicht なに / なん akzeptiert beide Einzellesungen beim Schreiben/Sprechen; Windows auch beim Hör-Lesungsabruf. Ein zusätzlicher Sprechdatensatz ergänzt alle erhaltenen alten Ziele.

Die Antwortvorlage bleibt beim Prüfen verborgen; Begründungen erscheinen nach einer abgegebenen Antwort, vollständige Hilfe nur nach bewusstem Aufruf. Hilfe schaltet nichts frei. Windows startet weiter mit Verstehen und freiwilligem Sprechen; Android behält alle sechs Schritte und die gekennzeichnete Kana-Selbstprüfung. Keine Änderung an Lehrern, Stimmen, Animationen, Modellen, Gesprächscode oder Update-Verfahren. Der Gesprächsraum bleibt Android-Funktion.

## Getrennte Prüfstatus

| Kategorie | Tatsächlich ausgeführt | Grenze |
| --- | --- | --- |
| Erfassung | Alle 150 Lektionen / 680 Karten, bestehende acht Berichte, fünf Szenen / 29 Knoten; Export aus aktualisierten Quellen | Keine automatische Vollanalyse impliziter Sprachvoraussetzungen |
| Automatische Tests | Nachfolgende Programm-, UI-, Build-, Signatur- und Updateprüfungen | Technische Korrektheit ersetzt keine Sprachabnahme |
| Eigene sprachliche Durchsicht | Ziele, Vorwissen, 121 Kartenprofile, Beispiele, Antwortoptionen, neue Lehrtexte und Verbindungen zu späterem Material | Eigene Einschätzung; keine unabhängige/muttersprachliche Prüfung |
| Menschliche Fachprüfung | Nicht ausgeführt | Natürlichkeit, Höflichkeitsnuancen, は/が, Gesprächston und Anfänger-Verständlichkeit offen |

Die Lehrtexte wurden selbst formuliert. Ein punktueller Quellenabgleich zu Wohnort und Gesprächsformen erfolgte mit [Irodori Starter Lektion 4, Japan Foundation](https://www.irodori.jpf.go.jp/assets/data/starter/pdf/X_L04.pdf). Abrufe der Lektionen 7 und 8 scheiterten am Timeout; sie werden nicht als geprüfte Quellen beansprucht. Daraus folgt keine externe Abnahme des Pakets. Die vollständige Vorbereitung aller alternativen Gesprächszweige bleibt offen und ist in PAKET_02.md konkret abgegrenzt.

## Ausgeführte technische Prüfungen

| Prüfung | Ergebnis / Evidenz |
| --- | --- |
| Vollständige Python-Suite | **149 bestanden**, finaler Datenstand; `validation/python-1103-final.log` |
| Installer-Vertragsregeln | **20 bestanden**; `validation/installer-contract-1103.log` |
| Native Windows-Oberfläche | Alle **25 Paket-2-Lektionen**, Lehrschritt, fünf Abrufschritte, Fehlerrückmeldung, Hilfe ohne Freischaltung, nani/nan-Hörabruf; `validation/package2-ui/report.json` |
| Erste Windows-Lernhilfen | **5 bestehende Prüfgruppen bestanden**, einschließlich verborgener Lösungen und Lesetext; `validation/foundations-ui/report.json` |
| Android-/Gesprächslogik | **31 Tests bestanden**, darunter vollständiger Ablauf aller 150 Lektionen, strikte Sprachfreigabe, Kana-Selbstprüfung, alte Profile und alle Gesprächswege; `validation/android-logic-1103.log` |
| Android-Oberfläche im Browser | Bestehende **7 Formate** sowie **75 Paket-2-Durchläufe** (25 Lektionen × 320×640, 412×915, 844×390), ohne horizontalen Überlauf; `mobile/test-results/package2/report.json` |
| Windows-Build | PyInstaller-EXE/Updater plus vollständiger Inno-Setup-Installer gebaut; `validation/windows-build-1103.log`, `validation/windows-test-installer-final.log` |
| Gebaute Windows-EXE | Echte TTS-Modellverarbeitung: acht Stimmen in normal/langsam; echte ASR auf synthetischem Audio, erkannter Text passend, Stille abgewiesen; `validation/frozen-1103-speech/audio-report.json` |
| Windows-Update | **11.0.2 → 11.0.3 bestanden**: lokaler TLS-Download, temporäre Testsignatur, echter gebauter Updater, EXE-Neustart, altes Profil und **15 Modelldateien erhalten**; `validation/update-e2e-1103.log` |
| Android-Build | Release-, Debug- und Instrumentierungs-APK gebaut; Lint **0 Fehler / 9 Warnungen** (u. a. bestehende Abhängigkeiten); `validation/android-build-1103-final.log` |
| Android-Signatur | Vorhandener Herausgeber, v3-Signatur und 16-KiB-Alignment geprüft; ARM64 + x86_64, minSdk 28, targetSdk 35; `validation/android-sign-1103.log` |
| Paketinhalt | Gemeinsame Kursdateien in Windows und signierter APK mit Quellen abgeglichen; APK-Webquellen stimmen überein; `validation/packaged-content-1103.json` |
| Bestandsschutz | Gespeicherte SHA-256-Verträge schützen erste 30 Lektionen vollständig sowie alle 680 Kartenidentitäten, XP-Werte und Lernreihenfolge; Kursrevision bleibt 11 |
| Analyseexport | **9 Dateien reproduzierbar**, Paket-01-Bericht textgleich zur archivierten Fassung; **298** getrennt typisierte Beziehungen mit früheren, vorhandenen Zielen |

Alle Bedien- und Fortschrittstests verwenden separate Testprofile; keine persönliche Installation wurde ersetzt. Browser-Sprachereignisse sind simuliert. Die echte Windows-Modellverarbeitung verwendet synthetische Audiodateien, keine menschliche Aufnahme oder Lautsprecherabnahme.

## Fehlversuche und offene technische Prüfungen

Die ersten Regressionstests erwarteten noch 62 alte Sprechdatensätze; der zusätzliche nani/nan-Datensatz erforderte 63, wobei die ursprünglichen 62 unverändert geprüft werden. Ein Test auf Textlänge wurde durch die sachliche Prüfung vollständiger Begründungen ersetzt. Im neuen Browser-Test überschrieb das bisherige Seitenprofil beim Neuladen die Testvorlage; die Vorlage wird nun einmalig beim Start übernommen. Die Tests liefen danach erfolgreich durch. Beim Schlussabgleich wurden drei alte Beispiel-Metadaten mit ihren neuen Beispielen synchronisiert; beide Pakete wurden danach neu erzeugt.

Die lokale Android-Bauumgebung wurde aus offiziellen SDK-/Gradle-Paketen im ignorierten Projektordner eingerichtet und gegen veröffentlichte Prüfsummen geprüft. Für Android 15 wurde außerdem ein isoliertes AVD erstellt. Der Host besitzt keinen Emulator-Hypervisor; der Softwarestart scheiterte zuletzt mit Prozesscode `0xC0000005`. Ein vorheriger Startversuch hatte zudem ein falsches AVD-Suchverzeichnis; dieses wurde berichtigt. Kein Treiber und keine Windows-Virtualisierungseinstellung wurden verändert.

**Neue native Android-Instrumentierung nicht ausgeführt.** Vier native Tests einschließlich einer neuen Paket-2-/Altprofilprüfung sind kompiliert, aber für diesen Stand nicht auf einem gestarteten Android-Gerät durchgelaufen. Frühere Emulatorergebnisse aus 11.0.2 werden nicht als neue Ergebnisse ausgegeben. Installation über die vorhandene App, echtes Mikrofon, Lautsprecher und Wahrnehmung auf dem S24 Ultra bleiben ebenso offen wie ein frisches Windows-System und menschliche Sprach-/Anfängerprüfung.

## Fertige lokale Testpakete

| Datei | Bytes | SHA-256 |
| --- | --- | --- |
| `F:/Japanischtool/Testpakete/11.0.3/JapanischTrainer-11.0.3-Setup-x64.exe` | 846777610 | `33d4a6299c176b99f09320c70e1478899d46fc9efe9e01a20a4dcfba4cec678e` |
| `F:/Japanischtool/Testpakete/11.0.3/JapanischTrainer-11.0.3-Android-Test.apk` | 61805300 | `1834d40d2e8473586ec783ee536753912fede2e2137c111abd818bae5703477c` |

Windows-Version 11.0.3; Android-Version `11.0.3-android.1-test`, Code `11000301`, Paket `de.priestkiller.japanischtrainer`. Android-Zertifikat SHA-256: `3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9`.

Die direkt startbare gebaute EXE liegt mit ihren benötigten Ressourcen unter `F:/Japanischtool/github-JapanischTrainer/build-release/11.0.3/dist/JapanischTrainer/JapanischTrainer.exe`. Der lokale GPL-Quellstand wird im Testpakete-Ordner als `JapanischTrainer-11.0.3-Test-Quellcode.zip` mitgeliefert. Ein zusätzliches Update-ZIP unter `validation/update-package-1103` dient ausschließlich dem lokalen Regressionstest, verwendet eine temporäre Testsignatur und ist kein öffentlicher Update-Download.

Eine spätere Veröffentlichung ist ein eigener Schritt. Bei weiteren Programmänderungen nach diesem Teststand müssen Versionsnummer bzw. Android-Code erneut steigen, damit bereits installierte Testfassungen regulär aktualisiert werden können.

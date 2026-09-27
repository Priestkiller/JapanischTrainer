# JapanischTrainer 11.0.4 Prüfbericht

Stand: 27.09.2026. Diese Ausgabe enthält das zweite Inhaltspaket und einen zusätzlichen Button **Testversion suchen** in Windows und Android. Der Nutzer hat die öffentliche Bereitstellung ausdrücklich freigegeben. Die nachträgliche öffentliche Prüfung ist abgeschlossen; siehe VEROEFFENTLICHUNG_11.0.4.md. Am 27.09.2026 erneut abgeglichen: alle 20 Assets in Größe/SHA-256 und Zuordnung, gültige Windows-Signatur, Versionsmetadaten und echte reguläre/testweise Suche. Zusätzlich wurde das vollständige öffentliche Setup heruntergeladen und geprüft (846839144 Bytes). Nachweis: validation/public-release-1104-final-audit.json. Die bereits belegten ZIP-/APK-Downloads wurden bei unveränderten Hashes nicht unnötig wiederholt.

## Änderungen und Erhalt vorhandener Daten

Das zweite Paket umfasst unverändert 25 vorhandene Lektionen mit 121 Karten. Die vollständige Liste und sprachlichen Befunde stehen im [Bericht des lokalen Inhaltspakets](TESTBERICHT_11.0.3_LOKAL.md). Insgesamt 150 Lektionen, 680 Karten und 565 ausdrückliche Sprechziele. Die ersten 30 Lektionen / 138 Karten, alle IDs, die Kursrevision 11 und Lernreihenfolge bleiben erhalten. Version 11.0.4 erhöht lediglich die Versionsmetadaten dieses Kursstands.

Reguläre Updates und Testversionen verwenden getrennte Veröffentlichungen. Windows prüft Testangebote mit derselben Ed25519-Signatur; Android prüft dieselbe Paketkennung und denselben Herausgeber. Kanalwechsel entfernen das vorige Angebot und eine bereits ausgewählte APK, damit nicht versehentlich die vorherige Datei installiert wird. Es erfolgt kein automatischer Testbezug und kein Downgrade.

Android zeigt nun den tatsächlichen Kursstand in den Informationen. Die Sichtprüfung fand außerdem einen bisherigen Fehler bei Ren: Für seine geschlossenen Augen existieren bewusst keine Blinkbilder. Die Darstellung berücksichtigt das jetzt, ohne Bilder, Lehrer, Stimmen oder Sprachmodelle zu ersetzen.

## Tatsächlich ausgeführte Prüfungen

| Prüfung | Ergebnis und Grenze |
| --- | --- |
| Vollständige Python-Suite | 156 bestanden; `validation/python-1104-release.log` |
| Update-Kanäle und Sicherheitsprüfungen | Darin 24 Updateprüfungen; neu unter anderem Kanaltrennung, Auswahl der höchsten signierten Testversion, leere Liste, alte Versionen, Entwürfe, falsche Signatur und fremdes Paketziel |
| Installer-Vertragsregeln | 20 bestanden; `validation/installer-contract-1104.log` |
| Native Windows-Updateoberfläche | Testangebot auswählen, herunterladen, Kanal wechseln und vorherige Installationsbereitschaft verwerfen; getrennte Testdaten und kontrollierte Netzantworten |
| Android-/Gesprächslogik | 31 bestanden; vollständige Kursabläufe und Erhalt alter Lernstände; `validation/android-logic-1104.log` |
| Mobile Updateoberfläche | 320×640, 412×915 und 844×390 bestanden; Suche, Sperren während der Übertragung, Fehler, kein neueres Angebot und Wechsel des Kanals; Android-Anbindung im Browser simuliert |
| Android nativ | GitHub-Lauf [36338848666](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36338848666) auf Programmstand `318f54f55529a77f1f2213fab76ada9990dbd8a3` erfolgreich; Android 15, Oberfläche, Speichern, Paket 2, Kanaltrennung und echte lokale Modellverarbeitung |
| Lokaler Android-Build | Release-, Debug- und Instrumentierungs-APK sowie Lint erfolgreich; `validation/android-build-1104-final.log` |
| APK-Signatur | Vorhandener Herausgeberschlüssel, v3-Signatur, 16-KiB-Alignment bestätigt; `validation/android-sign-1104.log` |
| Windows-Build | Neue EXE und Update-Helfer gebaut; finaler Installer erfolgreich; `validation/windows-installer-1104-final.log` |
| Gebaute Windows-EXE | Acht Stimmen in zwei Tempi, echte ASR auf synthetischem Audio und Ablehnung von Stille bestanden; `validation/frozen-1104-speech/audio-report.json` |
| Vollständiges Windows-Update | 11.0.2 → 11.0.4 mit lokalem TLS-Download und gebautem Helfer bestanden; Neustart, Testlernstand und alle 15 Modelldateien erhalten; `validation/update-e2e-1104.log` |
| Produktive Windows-Signatur | Update-Metadaten mit bestehendem Projektschlüssel signiert und gegen den bereits ausgelieferten öffentlichen Schlüssel geprüft |
| Paketinhalt | Alle drei Kursdateien in Windows und APK mit Quelldaten abgeglichen; Android-Webquellen und Versionsdatei stimmen mit dem geprüften Stand überein |

Die vollständige lokale Windows-Updateprüfung nutzt eine eigene Testquelle und Testsignatur. Die produktive Signatur wird getrennt geprüft. Die anschließend geprüfte öffentliche Quelle ist im ergänzenden Veröffentlichungsbericht dokumentiert. Keine persönliche Installation wurde überschrieben; alle Lernstände in Tests sind separate Vorlagen. Die Modelle laufen tatsächlich, Mikrofonaufnahmen und Lautsprecherabnahme auf einem echten Gerät sind damit nicht belegt.

## Korrigierte Prüfprobleme

Der Windows-Installer verlangt übereinstimmende Programm- und Kursmetadaten. Ein erster Versuch mit Programm 11.0.4 und Inhaltsmetadaten 11.0.3 wurde daher korrekt abgewiesen. Beide tragen nun 11.0.4, ohne Änderungen an Lerninhalten oder gespeicherter Kursrevision. Die Original-Versionsprüfung blieb erhalten; die vollständige Suite wurde danach erfolgreich wiederholt. Die lokale Sandbox erlaubte den Zugriff auf den geschützten Windows-Signierschlüssel erst außerhalb der Sandbox. Der Schlüssel wurde unverändert verwendet und nicht ausgegeben.

## Abgrenzung der fachlichen Prüfung

Erfassung: alle 150 Lektionen / 680 Karten sowie fünf Gesprächsszenen. Eigene sprachliche Durchsicht: zusammen 55 Lektionen / 259 Karten aus zwei Paketen. Die vorliegende Ausgabe verändert keine weiteren fachlichen Inhalte. Automatische Tests prüfen Software und Datenverträge. Eine menschliche Fachprüfung und ein Anfänger-Durchlauf bleiben offen; ebenso echte Mikrofon-/Hörtests am S24 Ultra und ein frisches Windows-System. Der Windows-Installer besitzt weiterhin kein Authenticode-Zertifikat.

## Fertige Pakete

- Windows-Setup: 846839144 Bytes; SHA-256 `cc4cb4fb32866ad8c77b474facf4e41ed0a8b90afe02e4d304166d6c347935ba`.
- Android-APK: 61805300 Bytes; SHA-256 `30555077a046b0ffd973739639327b900bc47e580be911b5e820ce5c3ae6da9b`.
- Android-Version `11.0.4-android.1`, Code `11000401`; Zertifikat SHA-256 `3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9`.

Lokale Pakete liegen unter `release/11.0.4/windows` und `release/11.0.4/android`. Öffentliche Ziele sind `v11.0.4` und `android-v11.0.4-1`. Ein reguläres Update auf diese Ausgabe bringt den neuen Testbutton auch auf vorhandene Installationen. Solange keine höhere Testausgabe veröffentlicht ist, bleibt deren eigene Suche ohne Angebot.

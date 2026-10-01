# Android Testversion 11 0 13

Lernserie, XP und Fortschritt stehen jetzt oben. Tippe auf die Lernserie, um deinen Kalender zu öffnen. Er zeigt bekannte Lerntage und speichert neue Tage. Für frühere Versionen fehlen einzelne Tagesdaten; sie werden nicht ergänzt oder als tatsächlich gelernt ausgegeben. Dein bisheriger Lernstand bleibt erhalten.

Kiko blinzelt, bewegt sich in eigenen Bildfolgen und begrüßt dich nach Antippen. Beim Lektionsabschluss jubelt Kiko kurz. Die fehlerhafte zusätzliche Körperform der alten Jubelgrafik wurde für Android ersetzt. Reduzierte Bewegung und deine Einstellung bleiben berücksichtigt.

Die dunkle Abschlussansicht zeigt tatsächlich erhaltene XP. Wiederholte Lektionen erhalten keine zweite Belohnung. Die Updatesuche nennt nun die Fehlerart statt nur einer allgemeinen Meldung. Eine Behebung der noch ungeklärten S24-Verbindungsursache wird nicht behauptet.

Android 11.0.13-android.1-test, Code 11001301; Prerelease, ausschließlich Testkanal. Windows bleibt Test 11.0.11, stabile Ausgaben bleiben 11.0.4. Lernstände, Kurs, Lehrer, Stimmen und Sprachmodelle bleiben erhalten. Über die vorhandene App installieren, keine Deinstallation nötig.

Automatische Prüfungen und eigener Sichtabgleich sind von menschlicher Erprobung getrennt. Echte S24-Ultra-, Mikrofon-, Hör-, Anfänger- und Japanisch-Fachprüfungen stehen noch aus. Die gesonderte Veröffentlichungskontrolle nennt die tatsächlich bestandenen abschließenden Paket- und öffentlichen Tests. Eine spätere stabile Übernahme benötigt ausdrückliche Freigabe.


## Abschluss der Software und Paketprüfung

Der endgültige Quellstand f24b0f0cdf85dbfd17ec2de7a0efb021a067ee31 bestand Build und Lint, 65 JavaScript-Tests und alle 20 nativen Android-Emulatorprüfungen. Lint: lokal 11, CI 12 Warnungen, jeweils 0 Fehler. CI: https://github.com/Priestkiller/JapanischTrainer/actions/runs/36880658183. Die native HTTPS-Suche gegen die echte öffentliche GitHub-Quelle bestand mit unverändertem Testprofil. Tatsächlich gezeichnete Kiko-Pixel ändern sich; Kalender, Neustart, Abschluss und Wiederholung wurden nativ geprüft. Vor dem Upload existiert keine höhere Version als der Prüflauf 11.0.13, deshalb ist dessen Angebot korrekt leer.

30 Browseransichten und vier zusätzliche Profile bestehen die endgültige Abschlussdarstellung. Die 85 Menü-/Lernansichten bestanden vor der letzten, ausschließlich den Abschluss betreffenden Korrektur. Die endgültige native Suite prüft die Hauptmenüs ebenfalls. Python-/Windows-Tests wurden wegen unveränderter Windows- und Kursquellen nicht wiederholt.

Die zusätzliche Prüfung fand eine verdeckte zweite Abschlussaktion bei kleinen Ansichten. Inhalt und Aktionen sind jetzt getrennt: Inhalte dürfen bei wenig Platz scrollen, beide Aktionen bleiben sichtbar oberhalb der Navigation. Der erste native Lauf hatte 18 bestandene und zwei fehlgeschlagene Prüfungen: der Emulator hatte Bewegung abgeschaltet; außerdem sprach eine Testauswahl fälschlich einen Antwortindex als Antworttext an. Bewegung wurde im disponiblen Emulator zugelassen, reduzierte Bewegung separat geprüft und die Auswahlfixture korrigiert. Der zweite Lauf bestand 19 von 20 Prüfungen einschließlich Kalender, tatsächlicher Animation, Erstabschluss und HTTPS. Eine beim Schließen gespeicherte WebView-Session überschrieb die nächste direkt geschriebene Wiederholungsfixture. Die Abschlussprüfung verwendet deshalb nun dieselbe Activity und die vorhandene Importfunktion, bevor die Session regulär gespeichert wird. Ein noch laufender Zwischenlauf wurde vorzeitig ersetzt, nicht als bestanden gewertet. Der endgültige Stand ist vollständig bestanden. Ein weiterer Versuch kam nach bestandenem Build nicht bis zu den nativen Tests: der Google-Download des Android-Emulators schlug fehl. Derselbe Quellstand wurde erneut geprüft; der abgebrochene Infrastrukturversuch ist kein Testnachweis.

Die APK besteht v3-Signatur, bisherigen Herausgeber, Paketkennung, Versionscode 11001301 und 16-KB-Alignment. 155 mitgelieferte Dateien sind bytegleich zum Git-Quellstand und Quellenarchiv; die neuen Darstellungsdateien auch zum CI-Paket. Für diesen Abgleich wurden Windows-Zeilenenden im Buildbestand vereinheitlicht. Quellen und Pakete wurden auf private Schlüssel, Zugangsdaten, Lernstände und Aufnahmen geprüft. Öffentliche Nachprüfung folgt nach dem Upload. S24 und Mikrofon bleiben offen.


## Öffentliche Nachprüfung abgeschlossen

Alle 16 öffentlichen Dateien sind mit den lokalen Paketen über Größe und SHA-256 abgeglichen. Die öffentliche APK besteht Signatur, Version, Paketkennung und Quellenprüfung. Neun isolierte Profil-/Formatprüfungen mit öffentlichen Manifestdaten und simulierter nativer Web-Brücke bestehen die Trennung der Kanäle und unveränderte Profile; die native Android-HTTPS-Prüfung ist separat im Veröffentlichungsbericht angegeben. 24 vorherige Releases mit 242 Dateien bleiben unverändert, Latest bleibt v11.0.4. Die lokale Lieferung unter F:/Japanischtool/Testpakete/11.0.13/android/ ist ebenfalls vollständig abgeglichen. Details: VEROEFFENTLICHUNG_ANDROID_11.0.13_TEST.md.

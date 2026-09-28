# Prüfbericht JapanischTrainer 11 0 10

Stand 28. September 2026. Windows 11.0.10 und Android 11.0.10-android.1-test / Code 11001001 sind gebaut. Die hier aufgeführten Software-, Paket- und Signaturprüfungen wurden ausgeführt und bestanden. Die Testveröffentlichung ist freigegeben. Die Prüfung der echten öffentlichen Downloads erfolgt erst nach Upload und wird in VEROEFFENTLICHUNG_11.0.10_TEST.md separat dokumentiert. Dieser mit den Paketen gelieferte Bericht behauptet noch keine öffentliche Abnahme.

## Umsetzung und Aufgabenarten

Die Pflichtschritte Verstehen beziehungsweise Hören und Sprechen, Bedeutung, Hören, Bausteine, Schreiben und Anwenden sowie die Zusatzarten Nachsprechen, Abrufen, Zuordnen, Übersetzen, Auswahl-Lücke, Mehrfach-Lücke, Hör-Lücke und Leseverständnis zeigen konkrete Anweisung und Antwortformat. Nachsprechen hält Japanisch, Romaji, Bedeutung und die als Annäherung gekennzeichnete Aussprachehilfe zusammen. Audio und Aufnahme bleiben daneben beziehungsweise darunter erreichbar. Im Abrufmodus wird die japanische Lösung weiterhin verborgen. Lange Inhalte und große Schrift verwenden bei Bedarf einen erreichbaren Scrollbereich innerhalb derselben Ansicht. Kein Versprechen, dass jede lange Aufgabe auf jedem kleinen Bildschirm ohne Scrollen passt.

Lehrer werden beim Sprechen, im Android-Gespräch und während bewusst geöffneter Windows-Erklärungen gezeigt. Normale Aufgaben nutzen den gewonnenen Platz. Acht Stimmen und vorhandene Ausdrucks-/Ruheanimationen bleiben erhalten; ausgeblendete Animationen halten an. Kiko erscheint erst beim echten Lektionsabschluss, etwa 2,65 Sekunden mit vorhandener Jubelfigur. Weiterlernen ist sofort möglich. Reduzierte Bewegung zeigt ein ruhiges Bild. Die Darstellung selbst vergibt keine XP.

## Drei Versuche und Fortschritt

Bewusst gestartete, terminal erfolglose Aufnahmen werden pro Aufgabe gezählt. Nicht passender Text, unzuverlässige Erkennung und technische Probleme bleiben getrennt. Abbruch, Doppeltippen sowie alte oder doppelte Rückmeldungen zählen nicht erneut. Null bis zwei Fehlversuche öffnen keine Ersatz-Auswahl. Ab drei Fehlversuchen kann der Lernende sie ausdrücklich öffnen. Technische Fehler oder Stille sind keine nachgewiesenen Aussprachefehler.

Erst passende Auswahl plus Bestätigung speichert „Mit Auswahlhilfe geschafft“. Falsche Antworten erklären die Bedeutung der gewählten Alternative und schalten nichts frei. Am allerersten Kursanfang ohne bekannte Alternative wird zuvor ein Vergleich aus bestehenden Kurskarten erklärt und anschließend wieder verborgen. Die sonstigen Alternativen stammen aus schon eingeführten Kurskarten. Gesprächsantworten werden vor ihrer Auswahl ausdrücklich verglichen.

Der unterstützte Abschluss umgeht ausschließlich die blockierende Sprechprüfung, erzeugt keine Aussprachewertung und keine Extra-XP. Die optional vorgemerkte Sprechwiederholung ist unter Üben/Wiederholen erreichbar, für den nächsten Tag eingeordnet und bereits freiwillig startbar. Fortsetzen derselben Runde erhält den Zähler; eine bewusst neue Wiederholungsrunde beginnt bei null. Windows behält freiwilliges Sprechen, Android sechs Lernschritte und die getrennte, auf geeignete Aufnahmen begrenzte Kana-Selbstprüfung. Der Android-Gesprächsraum bleibt auf Android.

Neue additive Profilfelder: speech_support und speech_reviews. Bestehende Kurs- und Aufgaben-IDs, Abschlüsse, Lehrerwahl und Modelle bleiben unverändert. Keine Migration oder neue Kursrevision: weiterhin 150 Lektionen, 680 Karten und 156 Zusatzaufgaben in 25 Lektionen, Inhaltsversion 11.0.7 / Revision 11. Eigene frühere sprachliche Durchsicht: 105 Lektionen mit 501 Karten; 45 Lektionen mit 179 Karten bleiben außerhalb dieser vertieften Durchsicht. Keine neue menschliche Fachabnahme.

## Automatische Softwareprüfungen

- 184 Python-Tests, 55 mobile Logiktests und 20 Installer-Vertragsprüfungen bestanden. Enthalten: drei Versuche, falsche/richtige Auswahl, Neustart, alte Profile, Aufgabenlösungen, alle 680 Auswahl-Decks, Hilfen ohne Freischaltung, keine zusätzlichen Belohnungen sowie bestehende Update-Sicherheitsfälle.
- Native Windows-Oberfläche mit getrennten Testprofilen: 33 Ablauf-/Layoutprüfungen und 35 Reaktionsprüfungen bestanden. Alle acht Lehrer, Abbruch, verspätete Ergebnisse, reduzierte Bewegung und tatsächlicher Lektionsabschluss geprüft. Windows-Zusatzübungen: alle 25 Einstiegspunkte und zwei vollständige Runden. Neue Auswahlhilfe in 1440×1040, 1080×700 und 1280×800 einschließlich falscher Antwort, Bestätigung und Fortsetzen bestanden. Sprachergebnisse hierbei simuliert.
- Browser-Oberfläche: bestehender Lern- und Gesprächsablauf in sieben Formaten; 300 Pflichtansichten und 156 Zusatzansichten; fünf Bildschirmformate einschließlich Querformat. Hilfen, Erreichbarkeit und Verbergen der Lösungen geprüft. Drei-Versuche-Ablauf in 412×815, 320×640, 412×815 mit 140 Prozent Schrift und 844×390 bestanden. Eigene Wiedergabe, qualifizierte Kana-Selbstprüfung, Abbruch und verspätete Ergebnisse separat erneut geprüft.
- Zusätzlicher Browser-Folgetest: freiwillige Sprechwiederholung nach unterstütztem Abschluss, Fortsetzen nach zwei Fehlversuchen, neue Runde, unveränderte XP und Android-Gespräch mit drei technischen Fehlern sowie bestätigter Auswahl bestanden. Browser-Audioereignisse sind simuliert.
- Finale native Android-Prüfung: 14 Tests, null Fehler, null übersprungen, Android-15-Emulator. [CI-Lauf 36468510690](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36468510690), Programmstand 4f184defda9aa83bf353a008f9972b216155ee34. Enthalten: echter WebView-Start, alte Profile, Inhalte, Gespräch, Updatefilter, Aufnahmeidentität und Abbruch, neue Drei-Versuche-Auswahl bei fehlendem Sprachpaket, Rotation, 140 Prozent Schrift und tatsächliche Bildschirmtastatur. Lint: 0 Fehler, 0 schwere Fehler und 10 bestehende Warnungen.

## Echte Modellverarbeitung und Paketprüfungen

Die gebaute Windows-EXE hat ohne Netzwerk alle acht Stimmen normal/langsam synthetisiert, mit Parakeet und SenseVoice synthetisches Japanisch erkannt und Stille zurückgewiesen. Die native Android-Prüfung verarbeitet ebenfalls echte lokale Modelle und synthetisches Audio. Dies sind Modelltests, keine menschlichen Mikrofon- oder Hörtests.

Windows-EXE, Update-Helfer und Inno-Installer sind gebaut. PE-Versionen, Kursdaten und Paketzuordnung geprüft. Der App-/Kursversionsvertrag ist jetzt ausdrücklich: App 11.0.10 enthält unveränderten Kurs 11.0.7. Ein veralteter Gleichheitsvergleich hatte den ersten Installerlauf gestoppt; die neue Zuordnung prüft Metadaten, fehlende/falsche Versionen und abweichende Inhalte weiterhin strikt.

Der gebaute Windows-Updater bestand 11.0.7 → 11.0.10 mit TLS-Download, Signatur, Dateiaustausch, echter gebündelter EXE und getrenntem synthetischem Profil. XP, Lehrer, Tempo, Lektionsposition und angefangene Aufgabe blieben erhalten; alle 15 Modelldateien wurden ohne Inhalts-/Zeitstempeländerung weiterverwendet. Der Integrationstest verwendet eigene flüchtige Testschlüssel. Die reale Update-Metadatei wurde zusätzlich gegen den unveränderten produktiven Ed25519-Schlüssel geprüft.

Installation, Verknüpfungsstart, erneutes Einspielen, Sicherungen und Deinstallation einer isolierten ValidationBuild-Fassung derselben Inno-Vorlage und Programmdateien bestanden. Sie hat eigene App-ID, keine produktive Deinstallationsregistrierung und ein getrenntes Testprofil. Die Produktions-Setup.exe wird nicht in die persönliche Installation eingespielt. Ein frisches fremdes Windows-System ist damit nicht geprüft.

Android verwendet unverändert de.priestkiller.japanischtrainer, APK-v3-Signatur und Herausgeberzertifikat SHA-256 3b1c1e4beade1312d7b593007c6fb59d6ad08e2677e58cbe5e25f821f36f28b9. 16-KB-Alignment, Version 11001001, Web-/Kursdateien und Modellmetadaten geprüft. Quellarchiv wird aus dem dokumentierten Git-Stand mit bytegleichen APK-Ressourcen erstellt; Schlüssel, Aufnahmen, Profile und Testverzeichnisse sind ausgeschlossen. GPL-/Drittlizenzen und Bibliotheksquellen werden mitgeliefert. Windows hat weiterhin kein Authenticode-Zertifikat.

## Sichtprüfung und behobene Auffälligkeiten

Die erste Handy-Auswahlhilfe war zu eng in die Aufgabenkarte eingebettet; sie öffnet jetzt als lesbare eigene Ebene. Technische Aufnahmefehler ersetzen einen vorherigen Textvergleich, sodass keine widersprüchliche alte Fehlermeldung stehen bleibt. Historische Tests erwarteten dauerhafte Figuren in normalen Aufgaben; die Erwartungen wurden gezielt an den ausdrücklichen neuen Auftrag angepasst. Unveränderte Kursdaten und Bewertungsmethoden bleiben durch eigene Vergleiche geschützt. Die drei hinzugefügten Dialog-Herkunftskennzeichnungen ändern keinen Dialoggraphen.

Echte Windows-Fensterbilder liegen unter validation/speech-ui-windows/. Browserbilder und kurze aufgezeichnete Bedienfolge liegen unter mobile/test-results/speech-assistance/ sowie validation/Sprechhilfe-und-Abschluss-11.0.10.webm. Native Android-Bilder stammen aus dem genannten Emulatorlauf. Der Clip zeigt simulierte Audioereignisse und lädt für Kikos Abschluss ein getrenntes Profil am Ende einer Wiederholung; er behauptet keine vollständige absolvierte Lektion. Die Nachweisarchive enthalten nur bereinigte, tatsächlich erzeugte Bilder/Protokolle und diesen Hinweis.

## Lieferung und offene Prüfungen

Lokale Testpakete: release/11.0.10/windows/ und release/11.0.10/android/. Vorgesehene öffentliche Tags: windows-test-v11.0.10 und android-test-v11.0.10-1, ausschließlich Prerelease, nicht Latest. Stabil bleibt 11.0.4. Erst nach Upload werden alle öffentlichen Dateien anonym geladen, Größen/SHA-256 verglichen und vorhandene Signaturen sowie Kanaltrennung geprüft. Auf 11.0.10 ist eine leere Testsuche korrekt, solange keine höhere Testversion existiert. Suche allein startet weder Download noch Installation.

Offen: echtes S24 Ultra, menschliche Mikrofon- und Hörprüfung, Anfänger-Erprobung, frisches Windows-System und menschliche Japanisch-Fachprüfung. Automatische Kurzlaut-Erkennung bleibt grundsätzlich unzuverlässig; die Auswahlhilfe verhindert die Lernblockade, ohne eine Spracherkennung vorzutäuschen. Die praktisch ausführbare Geräteprüfung steht in GERAETEPRUEFUNG_11.0.10.md.

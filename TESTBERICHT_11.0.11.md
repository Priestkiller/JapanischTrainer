# Prüfbericht JapanischTrainer 11.0.11

Stand 30. September 2026. Tatsächlich umgesetzt sind persönliche Tagesrunden, getrennte Fähigkeitsmetriken, vier Hörsituationen, manuelles Kana-Nachzeichnen, ein weiteres vorbereitetes Offline-Gespräch auf Android und ein freiwilliger lokaler Modellvergleich. Testpakete werden lokal geliefert. Es wurde keine öffentliche Veröffentlichung vorgenommen: Die GitHub-CLI und der vorhandene Git-Anmeldedienst liefern aktuell keine Anmeldung. Eine öffentliche Abnahme und der native CI-Lauf stehen deshalb aus.

## Änderungen und erhaltenes Verhalten

`adaptive.py` und `mobile/web/adaptive.mjs` speichern Wiederholungsbedarf getrennt nach Lesen, Hören, Schreiben, Sprechen und Anwenden. Eine Tagesrunde enthält höchstens fünf bekannte Karten und zwei neue Einführungskarten. Die Liste bleibt am selben Tag einschließlich erledigter Aufgaben erhalten. Erfolg mit Hilfe und freiwillig verschobenes Sprechen werden nicht als eigenständige Beherrschung gespeichert. XP, Kursabschlüsse und bestehende Lektionskennungen bleiben erhalten. Eine übernommene alte Kana-Selbstprüfung verfälscht nun keinen späteren automatisch passenden Versuch mehr.

`data/practice_content.json` verwendet ausschließlich bestehende Kursdialoge: `v11:dialog-cafe`, `v11:dialog-meeting`, `v11:dialog-directions`, `v11:dialog-weekend`. Neue Zusatzkennungen: `practice:cafe`, `practice:meeting`, `practice:directions`, `practice:weekend`. Je zwei Fragen und bewusst aufrufbare Lesehilfe. Die Dialoge sind erst nach Einführung aller zugehörigen Karten verfügbar. Nach erklärenden Fehlerhinweisen wird die anschließende Lösung als unterstützt gekennzeichnet. Kana-Nachzeichnen vergibt keine automatische Handschrift- oder Strichfolgenote.

Android erhält die zusätzliche Szene `restaurant` mit sechs Vorbereitungskarten und verzweigten Wegen für Gericht, Getränk, Rechnung und Zahlung. Alle fünf früheren Szenengraphen sind gegen eine unveränderte historische Quellfassung geschützt. Die Rückmeldung zu unbekannten Antworten nennt die aktuelle Aufgabenabsicht und verwechselt eine nicht unterstützte Antwort nicht mit falscher Aussprache.

Kurs unverändert: **150 Lektionen, 680 Karten, Revision 11, Inhaltsversion 11.0.7**. Weiterhin 105 Lektionen mit 501 Karten aus vier Inhaltspaketen selbst sprachlich durchgesehen, 156 Zusatzaufgaben in 25 Lektionen. Keine neue Kurslektion oder Umnummerierung. Windows behält Verstehen und freiwilliges Sprechen, Android seinen bisherigen Sechs-Schritte-Ablauf, Kana-Selbstprüfung und Auswahlhilfe. Stimmen, Figuren, Animationen und bestehende Updatekanäle wurden nicht umgestellt.

## Spracherkennung und Datenschutz

Zwei zusätzliche, unveränderte INT8-ONNX-Exporte aus sherpa-onnx 1.13.8 werden als freiwillige Testmodelle angeboten: [ReazonSpeech k2 v2](https://huggingface.co/reazon-research/reazonspeech-k2-v2) und [Qwen3-ASR 0.6B](https://huggingface.co/Qwen/Qwen3-ASR-0.6B), beide laut Modellkarten unter Apache 2.0. Lizenztexte, Herkunft und Konvertierung sind dokumentiert. Kotoba-Whisper und Qwen3 1.7B wurden nicht integriert; innerhalb der vorhandenen Laufzeit wurden zunächst die zwei kompatiblen Kandidaten umgesetzt und tatsächlich verglichen.

Die Erkennung erhält Audio und Sprachwahl, keinen erwarteten Zieltext. Qwen3 erhält ausdrücklich „Japanese“; die anfängliche automatische Sprachwahl lieferte bei kurzen Lauten teils chinesische Texte und wurde vor dem abschließenden Vergleich korrigiert. Kein neues Modell wird automatisch aktiviert. Windows behält Parakeet/SenseVoice für normale Aufgaben; Android behält SenseVoice und erlaubt eine ausdrückliche Versuchsauswahl. Alle Modelle laufen nacheinander. Ein besserer allgemeiner Erkennungsgrad ist nicht belegt.

15 freiwillige Testvorlagen und lokale, exportierbare Ergebnisberichte sind umgesetzt. Audio verbleibt vorübergehend im Arbeitsspeicher, es gibt keinen automatischen Upload. Die Berichte enthalten erkannte Texte, Modelllaufzeiten und ausdrücklich zu bestätigende Aufnahmequalität; sie liegen getrennt vom Kursprofil. Auf Android kommt das Gerätemodell hinzu. Lokale Modell-ZIPs werden wie Downloads anhand fest eingebauter Paket- und Einzeldateiprüfsummen geprüft. Der bisherige Downloaddeckel von 600 MB für App-Updates bleibt erhalten; nur der separat gepinnte Qwen-Modellimport darf größer sein.

## Tatsächlich ausgeführte Prüfungen

| Prüfung | Ergebnis und Grenze |
| --- | --- |
| Python-Regression | 192 Tests bestanden, darunter acht neue Tests für Tagesplan, Fertigkeiten, Altprofile, Hilfe, Kursbelege, Signalgrenzen und Modellpakete |
| JavaScript | 60 Tests bestanden; vorhandene Kurs-/Sprechhilfeverträge sowie neue Fähigkeits- und Importgrenzen |
| Windows-Installervertrag | 20 Tests bestanden |
| Browserbedienung | Neue Abläufe bei 412×915, 360×800, 320×640, 844×390 und 412×915 mit 160 Prozent Schrift bestanden; native Ereignisse simuliert |
| Native Windows-Oberfläche | Echte Tk/Pillow-Ansichten bei 1440×1040 und 1080×700 mit separaten Profilen, Nachzeichnen, Hilfe, Tagesrunde und Ergebnisanzeige geprüft; Audioereignisse simuliert |
| Android-Build | Release und Instrumentierungspaket kompiliert; Lint bestanden, vorhandene Hinweise auf neuere Abhängigkeiten bleiben |
| APK | Bestehender Herausgeberschlüssel, v2/v3-Signatur und 16-KB-Alignment geprüft; Paketname erhalten, Code 11001101 |
| Windows-Testupdate | Mit bestehendem Ed25519-Schlüssel signiert; Signatur, Größe und SHA-256 geprüft. Tatsächlich auf eine isolierte Kopie von 11.0.10 angewandt, neue EXE gestartet, Profil bytegleich und 15 vorhandene Modelldateien unverändert |
| Gepackte Windows-EXE | Tatsächlich mit separatem Profil gestartet, Oberfläche gerendert und Exitcode 0 |
| Reale Host-Inferenz | 24 identische synthetische Aufnahmen und drei negative Signale mit drei Modellkandidaten; außerdem produktiver Vier-Modell-Vergleich nach tatsächlicher lokaler ZIP-Installation |
| Geräte/Menschen | Kein echter S24-Ultra-, Mikrofon-, Hör-, Anfänger- oder menschlicher Japanisch-Fachtest dieser Ausgabe |

Synthetischer Vergleich (zwei Supertonic-Stimmen, je zwölf Vorgaben): SenseVoice **18/24**, ReazonSpeech **9/24**, Qwen3 **16/24** passende Texte. Stille, Rauschen und Klick wurden vor Erkennung zurückgewiesen. Das ist ein kleiner kontrollierter Host-Test, kein repräsentativer Qualitätsnachweis. Der zusätzliche produktive Vergleich des synthetischen Satzes „みずをのみます“ lieferte in SenseVoice, Parakeet, ReazonSpeech und Qwen3 jeweils einen passenden Text. Zeiten stammen vom Windows-Host, nicht vom S24 Ultra.

Die neuen Python-/JavaScript-Sanitizer und Altprofiltests erhalten XP und Kursposition. Lernhilfe, aufgeschobenes Sprechen und doppelte/verspätete Audioereignisse wurden getrennt geprüft. Archivtests verwerfen falsche Hashes, fehlende/zusätzliche Dateien, Pfadausbruch, Abbruch und unsichere Downloadadressen. Beide echten Modell-ZIPs wurden mit der produktiven lokalen Importfunktion geprüft und installiert.

## Fehlversuche und Korrekturen

Sandbox-Läufe konnten Test-Unterprozesse beziehungsweise temporäre Ordner nicht öffnen; die betroffenen Prüfungen wurden mit isolierten Profilen außerhalb der Sandbox wiederholt. Im Restaurant fehlte zunächst eine Antwortidee für direkte Kartenzahlung; der Routentest deckte dies auf. Eine ungültige Windows-Schaltflächenfarbe wurde durch die native UI-Prüfung gefunden und korrigiert. Die Sichtprüfung führte zu deckenden Flächen hinter Texten. Der erste Build über PowerShell 5 beschädigte ein Python-Argument; PowerShell 7 baute erfolgreich. Historische Ganzdatei-Sperren wurden ausschließlich um die ausdrücklich beauftragten Ergänzungen erweitert; Kursidentitäten, alte Dialoge, TTS und bestehende Bewertungslogik werden weiterhin unabhängig geschützt.

Der lokale Android-Emulator kann ohne vorhandenen Hypervisor-Treiber nicht beschleunigt laufen. Ein zusätzlicher nativer Modelltest wurde geschrieben und kompiliert, aber noch nicht ausgeführt. Wegen fehlender GitHub-Anmeldung wurde nichts hochgeladen, kein CI-Ergebnis erfunden und keine erneute öffentliche Download-Abnahme behauptet.

## Lieferstand und offene Abnahme

Windows **11.0.11**, Android **11.0.11-android.1-test / 11001101**. Lokale Testpakete und optionale Modelle: `F:/Japanischtool/Testpakete/11.0.11/`. Die praktische Geräteprüfliste steht in `ANLEITUNG_11.0.11_TEST.md`. Eine spätere stabile Veröffentlichung erfordert weiterhin die ausdrückliche Freigabe des Nutzers.

Offen: GitHub-Anmeldung, Upload ausschließlich in den Testkanal, nativer Android-Emulatorlauf einschließlich optionaler Modelle, öffentliche vollständige Download-/Signaturprüfung und echte Updateerkennung gegen die neue öffentliche Ausgabe. Außerdem menschliche Fachprüfung des Restaurantdialogs und der deutschen Lernhinweise sowie die angekündigte echte S24-Testrunde. Bestehende Quellen und Lizenzen sind mitzuliefern; private Daten und Schlüssel bleiben ausgeschlossen.

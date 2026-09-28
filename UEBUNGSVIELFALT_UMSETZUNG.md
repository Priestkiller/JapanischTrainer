# Übungsvielfalt und Erklärmodus

## Ausgangspunkt und Umsetzungsentscheidung am 28 September 2026

Ausdrücklich beauftragter Ausbau auf dem sauberen Entwicklungsstand nach Test 11.0.6. Stabil bleibt 11.0.4. Kurs: 150 Lektionen / 680 Karten, davon 105 / 501 bereits selbst durchgesehen. Die 45 noch nicht vertieften Lektionen werden durch diese Arbeit nicht als sprachlich geprüft gezählt. Die neun lokalen Referenzen wurden gelesen; sie bleiben außerhalb des Git-Projekts und werden nicht ausgeliefert.

Vorhanden: Windows `PracticeBook`/`StudySession` mit Verstehen, Bedeutung, Hören, Bausteinen, Schreiben, Anwendung und Abschlussrunde; Android `Course`/`Session` mit verpflichtendem Sprechen als erstem Schritt, ansonsten entsprechenden Kompetenzen. Beide besitzen ausführliche Kartenprofile und einen gemeinsamen Kurs. Android besitzt zusätzlich den unverändert bleibenden Offline-Gesprächsraum. Native Aufnahme, lokale Stimmen, Wiederholungsplanung und Updates werden wiederverwendet.

Ergänzung: gemeinsame kuratierte Aufgaben in `data/exercises.json`, Bewertung und Zustand als Erweiterung des Übungsbereichs, je ein nativer Windows- und mobiler Renderer. Acht Aufgabenfamilien: Text-/Hörpaare (Bedeutung/Hören), angeleitetes Nachsprechen (Einführung), aktiver Sprechabruf (Anwendung), Hörlücke (Hören), Auswahllücke (Anwendung), Mehrfachlücken und Satzübersetzung (Bausteine), Lesen mit Inhaltsfrage (Anwendung). Begrenzte Fehlerwiederaufnahme verwendet die vorhandene Karten-Wiederholungsplanung; sie ist kein neunter Renderer.

Einstieg direkt in geeigneten Lektionen über „Abwechslungsreich üben“. Diese ergänzenden Runden verändern weder bestehende Pflichtschritte noch XP und Abschlussregeln. Vor dem ersten Abruf werden die tatsächlich benötigten Ausdrücke einschließlich Alternativen und Lesungen ausdrücklich eingeführt. Die sichtbaren sechs Grundschritte bleiben erhalten. Alte Lektionen und bestehende Hilfetexte bleiben bestehen.

„Erklären / Warum?“ bietet zuerst einen Hinweis, danach ausdrücklich die vollständige Erklärung mit Lösung. Eingaben, Bausteine, Zuordnungen und Versuchsergebnisse bleiben beim Öffnen erhalten. Eine vollständige Lösung bleibt beim aktiven Abrufen verborgen, beim angeleiteten Nachsprechen bleibt die Vorlage sichtbar. Selbstständige, unterstützte und technische Versuche werden getrennt, sparsam und ohne Tonaufnahmen im bestehenden Profil gespeichert. Neue additive Profildaten benötigen keinen Reset alter Fortschritte.

Berührte Module: `study.py`, `lesson_ui.py`, `app.py`, die mobilen Lern-/UI-Adapter und Ressourcenexport; ergänzende gemeinsam beschriebene Aufgaben, Tests und Build-Manifeste. Bestehende Audioengines, Figuren, Modelle, Gesprächswege und Update-Vertrauensschlüssel bleiben erhalten. Der öffentliche Stand wurde abgefragt: nächste Testausgabe Windows 11.0.7 und Android 11.0.7-android.1-test, Code 11000701. Stabil bleibt 11.0.4.

Dies ist die verlangte erste Übersicht, kein Abschlussnachweis. Implementierung, konkrete Aufgabenkennungen, ausgeführte Prüfungen, offene Punkte und Veröffentlichung werden während der Arbeit ergänzt.

## Produktive Umsetzung

Der Einstieg „Abwechslungsreich üben“ steht in den folgenden 25 bereits vertieften Lektionen bereit. Er ist regulär über die Lektion erreichbar, ohne Debugmenü. Die Zusatzrunde führt ihre Quellen ausdrücklich ein und verwendet dieselben ausführlichen Kartenprofile, Lehrer und Stimmen. Die bisherige Lektionsfreischaltung gilt weiterhin. Es gibt keine neuen Lektionen oder Karten.

- `v11:kata-basics` – Katakana: erste Alltagswörter; 4 Aufgaben
- `v11:kata-long` – Der Strich ー verlängert den Vokal; 4 Aufgaben
- `2:0` – わたしは～です; 8 Aufgaben
- `2:1` – Nationalität; 7 Aufgaben
- `3:0` – ～ですか; 7 Aufgaben
- `v11:first-meeting` – Zum ersten Mal jemanden treffen; 4 Aufgaben
- `v11:asking-names` – Namen nennen und höflich nachfragen; 7 Aufgaben
- `v11:countries` – Länder und Herkunft; 4 Aufgaben
- `v11:languages` – Welche Sprache sprichst du?; 7 Aufgaben
- `v11:this-that` – Dieses hier, das da, jenes dort; 4 Aufgaben
- `v11:this-noun` – Dieses Buch: この + Nomen; 7 Aufgaben
- `v11:whose` – Wem gehört das? Besitz mit の; 8 Aufgaben
- `v11:here-there` – Hier, da und dort; 4 Aufgaben
- `v11:existence` – Was ist da? あります und います; 7 Aufgaben
- `5:0` – を + Verb; 9 Aufgaben
- `v11:location-action` – Ziel, Ort und Verkehrsmittel; 9 Aufgaben
- `v11:polite-past` – Höfliche Verben: gestern und heute; 4 Aufgaben
- `v11:drinks` – Getränke auswählen; 4 Aufgaben
- `v11:food-preferences` – Vorlieben und höfliche Essenswünsche; 7 Aufgaben
- `6:0` – Im Café; 9 Aufgaben
- `v11:clock-hours` – Volle Stunden und halb; 4 Aufgaben
- `v11:inviting` – Jemanden einladen; 4 Aufgaben
- `v11:read-profile` – Lesetext: Ren stellt sich vor; 8 Aufgaben
- `v11:read-day` – Lesetext: ein gewöhnlicher Tag; 8 Aufgaben
- `v11:read-plan` – Lesetext: ein Ausflug für morgen; 8 Aufgaben

156 neue stabile Aufgabenkennungen mit Präfix `ex1:`, Inhaltsrevision 1. Verteilung: choice_gap 15, echo 25, hear_gap 15, multi_gap 5, pairs 50, read 3, recall 25, translate 18. Alle Kennungen, Karten und Voraussetzungen stehen in UEBUNGSTYPEN_ABDECKUNG.csv.

### Gemeinsame Daten und bestehende Regeln

`data/exercises.json` ist maßgeblich; `tools/build_exercises.py` enthält die kuratierte Auswahl und geprüfte vollständige Lösungskombinationen. `exercises.py` und `mobile/web/exercises.mjs` adaptieren diese Daten an den vorhandenen Store und die vorhandene Wiederholungsplanung. `exercise_ui.py` verwendet die native Windows-Oberfläche; `mobile/web/exercise-ui.mjs` die gebündelte Android-WebView. Kein alternativer Kurs- oder Freischaltungsbaum. Die sechs bisherigen Schritte bleiben unverändert; Windows beginnt mit Verstehen und freiwilligem Sprechen, Android mit seinem vorhandenen Sprechschritt einschließlich enger Kana-Selbstprüfung.

Zusatzaufgaben speichern sparsam im bestehenden `lesson_sessions`-Bereich unter `exercises:<Lektion>`. Eingabe, Paaridentitäten, Tokenreihenfolge, aktive Lücke, Hilfestufe, Aufgabe und Ergebnis überleben Pause/Neustart/Import. Alte Sitzungen bleiben verwendbar. Auch bisherige Schreib-/Bausteinaufgaben erhalten jetzt ihre Entwürfe und bewusst geöffneten Hilfen. Keine Kursreihenfolge-, ID-, XP- oder Kursrevision-Änderung. Nur `content_version` steigt auf 11.0.7. Historische Autorenskripte dürfen diese Versionsangabe nicht zurücksetzen.

Fehler werden im bestehenden Wiederholungskalender auf Kartenebene vorgemerkt. Nach den normalen Aufgaben folgen höchstens sechs erneute Aufgaben; keine weitere Warteschlange innerhalb dieser Wiederholung. Wo geprüft, wechseln Text-/Hörpaare oder Übersetzungs-/Hörlücken; Leseverständnis wiederholt dieselbe Inhaltsfrage, weil eine Paaraufgabe nicht dasselbe Lernziel prüfen würde. Selbstständig, korrigiert, mit Hinweis, nach vollständiger Lösung, falsch, nicht sicher geprüft, technisch und pausiert bleiben unterscheidbar. Keine zusätzlichen XP oder pauschalen Pflichtschritterfolge.

### Audio und Darstellung

Stimme/Tempo, Aufgabenkennung und Anfragekontext werden zugeordnet. Verlassene/abgebrochene Anfragen können keinen Erfolg melden. Windows verwirft verspätete TTS-Ausgabe vor Wiedergabe; Android nutzt den vorhandenen Abbruchzähler. Die eigene Aufnahme kann ausdrücklich aus dem Arbeitsspeicher angehört werden; Abbruch verwirft sie. Keine neuen Modelle, Cloud-Anbieter oder Audio-Telemetrie.

Normale/langsame japanische Wiedergabe, native Windows-Eingabe mit sichtbarem Fokus und Tab/Enter, Schutz vor Enter während IME-Komposition sowie separat antippbare Lücken sind eingebaut. Deutsche Erklärungstexte gehen nicht in die japanische Stimme. Hilfe bleibt innerhalb der Aufgabe. Fremde Referenzbilder werden nicht ausgeliefert. Browser, native Windows-App und Android-Hülle werden getrennt im Testbericht nachgewiesen.

# Paket 04 Zeit Verabredungen und spätere Anwendung

25 erstmals vertiefte bestehende Lektionen / 123 Karten. Dazu eine ausdrücklich abgegrenzte Vorbereitungskorrektur an der bereits in Paket 03 geprüften Karte `12:0:4`. Sie wird nicht erneut gezählt. Zusammen 105 eindeutige Lektionen / 501 Karten selbst sprachlich durchgesehen; 45 Lektionen / 179 Karten bleiben einzeln offen. Kurs: 150 Lektionen / 680 Karten / 565 explizite Sprechziele. Keine zusätzliche Lektion nötig.

## Ausgangspunkt und Auswahl

Ausgangsstand `21de74cfd5cde7ba8d77cda00c877ca590d90dbf`, Testversion 11.0.5. Die konkreten 80 früheren Lektions-IDs, alle 150 Lektionshashes, 680 Kartenidentitäten, Reihenfolge und geschützte Programmdateien stehen im unveränderten Ausgangsvertrag `tests/fixtures/package03-contract.json`. Auswahl aus den übrigen 70 Einheiten: zuerst Personen-/Zeit-/Kalenderangaben (47–53), dann Häufigkeit (59), Jahreszeiten/Wetter/Befinden (82–85), Freizeit/Einladen/Verbgrundlagen (88–94), Termine/Nachrichten (126/129) und Dialog/Lesetexte (134/137–139). Der Zusammenhang führt von Zeitangaben über Handlungen zu einer vereinbarten oder noch offenen Verabredung und einer Rückschau. Keine bloße Auswahl der nächsten 25 Positionen.

Die vorhandenen Erklärungen und Beispiele waren vielfach brauchbar. Es fehlten bei den ausgewählten 25 Einheiten explizite Vorwissensbezüge, zusammenhängende Vorbereitung der früher benötigten Beispielwörter sowie Begründungen für die tatsächlichen falschen Anwendungsantworten. Konkrete Verwechslungen: Personen/Stückzahlen/Alter, Uhrzeit/Dauer, halb drei gegenüber drei Uhr dreißig, Kalendertag gegenüber Lebensalter, Einladung gegenüber Verneinung, Terminwunsch gegenüber Bestätigung und bedingter Plan gegenüber sicherem Ereignis. 75 eigene Lernhilfe-Absätze und 37 gezielte neue/überarbeitete Anwendungsfragen bearbeiten diese Fälle. Neun bereits passende Leseverständnisfragen bleiben erhalten und bekommen einzeln formulierte Fehlantwortbegründungen; auf allen 123 Karten sind die tatsächlichen Anwendungsdistraktoren erklärt.

## Bestand und gesonderte Zahlenkorrektur

124 nicht ausgewählte Lektionen, darunter 79 der bisherigen 80, bleiben als vollständige Objekte unverändert. In `12:0` bleibt ebenfalls alles unverändert außer `cards[4].detail`: drei Zweiergruppen für 5/6, 7/8 und 9/10 mit freiwilligen Selbstabrufen und eine konkrete Anwendungsfrage nach der Zahl direkt nach sieben. Die bisherige Sammelkarte verlangt sechs Formen auf einmal; ihre ursprüngliche Erklärung hatte keine Teile oder kleineren Beispiele. Die bestehende Erklärungs-/Hilfeansicht kann die Gruppen darstellen, sodass keine neue Oberfläche erforderlich ist.

Die ganze Reihe bleibt als Sprech-, Bau- und Schreibziel erhalten. Hilfe vergibt keine Freigabe oder XP; eine Teilantwort besteht die gesamte Reihe nicht, und die Kana-Selbstprüfung ist bei der Sammelkarte nicht verfügbar. Direkt danach folgen bereits vorhandene Einzelkarten für 6–10. Die neue Vorbereitung löst nicht nachweislich jede kognitive Belastung: Anfänger-Erprobung bleibt offen. Eine künftig eigenständige Aufteilung der Prüfkarte würde eine separate Aufgaben-/Fortschrittsentscheidung erfordern; in diesem Paket keine neue ID oder Migration.

Keine Änderung von Lektions-/Kartenidentitäten, XP, Reihenfolge, Kursrevision 11, Android FLOW_REVISION 2 oder Speicherschema. Alte Sessions bleiben an ihrer erreichten Aufgabe. Windows behält Verstehen und freiwilliges Sprechen, Android den bestehenden Pflichtablauf mit gekennzeichneter kurzer Kana-Selbstprüfung. Stimmen, Lehrer, Animationen, Modelle, Gesprächscode und Update-Sicherheit bleiben erhalten.

## Gesprächsbezug und ehrliche Grenzen

Drei automatisch geprüfte Wochenendwege: Film → Samstag → 10 Uhr vormittags → Bahnhof; Park → Sonntag → 14 Uhr → Cafévorplatz; Café → Samstag → 15 Uhr → Bahnhof. Die vorbereiteten Erklärungen behandeln die Servicefragen, Tag-/Uhrzeit-/Ortswahl und die zusammengesetzte Abschlussbestätigung. Die Szene unterstützt nur ihre vorhandenen Optionen. Eine andere sprachlich mögliche Zeit oder Aktivität ist dadurch nicht automatisch eine richtige Szenenantwort. Keine neue Engine, kein Windows-Gesprächsraum.

Die Cafészene bleibt bei Bestellungen ohne Mengenwort und Größen S/klein oder L/groß. `コーヒーをひとつください` und `エムサイズでおねがいします` bleiben außerhalb der jeweiligen vorbereiteten Routen. Tests prüfen Ablehnung ohne Fortschritt und die vorhandene Rückmeldung über die Szenengrenze; kein Aussprachefehler wird daraus abgeleitet. Danach kann eine passende Antwort den gleichen Gesprächsweg fortsetzen. Kurslektionen mit Menge und M bleiben ausdrücklich zusätzliche Übungen.

## Einordnung der Prüfungen

Erfassung: alle Kursdaten und Analysebeziehungen. Eigene sprachliche Durchsicht: die genannten 25 Lektionen mit Beispielen, Lesungen, Näherungslautung und Aufgaben sowie der Zahlen-Grenzfall. Struktur-/Softwareprüfungen: `tests/test_package4.py`, `mobile/tests/package4.test.mjs`, native/basierte UI-Prüfungen und die bestehende vollständige Suite. Tatsächlich ausgeführte Ergebnisse, Buildstände und Aussagegrenzen stehen in `TESTBERICHT_11.0.6_TEST.md`; die öffentlichen Downloads anschließend in `VEROEFFENTLICHUNG_11.0.6_TEST.md`. Menschliche Fachprüfung, Anfänger-Erprobung, echte Mikrofon-/Hörtests und frisches Windows sind nicht durchgeführt.

Punktueller Primärquellenabgleich: [Japan Foundation Irodori Starter Lektion 9](https://www.irodori.jpf.go.jp/assets/data/starter/pdf/X_L09.pdf), S. 1, 8 und 16–17, für Stundenlesungen, Wochentage, Zeitgrenzen und Terminantworten. Eigene Lehrtexte und Beispiele; keine Übernahme kompletter Übungen und keine externe Vollvalidierung. Der PDF-Abruf zu Lektion 12 schlug fehl und zählt nicht als Prüfung.

## Konkrete sprachliche Unsicherheiten

| Stellen | Noch von Menschen zu prüfen |
| --- | --- |
| `12:0:4` | Entlastung durch Zweiergruppen bei echten Anfängern; die Gesamtaufgabe bleibt lang. |
| `12:1:2` | Soziale Angemessenheit einer Altersfrage je Gesprächssituation. |
| `v11:people-age:4`, `v11:clock-minutes:2` | Priorisierung der Lesungsvarianten mit ju/ji und Verständlichkeit der Näherungslautung; bestehende Sprechvarianten nicht erweitert. |
| `v11:reply-invites:1–4`, `v11:appointments:3–4` | Natürlichkeit und Stärke indirekter Absagen; keine universelle Bedeutung von だいじょうぶ. |
| `v11:messages:0–3` | Register im konkreten beruflichen Verhältnis und Natürlichkeit der Änderungsbitte. |
| `v11:dialog-weekend:0–4` | Natürlichkeit des ganzen Gesprächs und tatsächliches Verstehen seiner Ansagen beim Hören. |
| `v11:read-plan:4`, `v11:read-message:3` | Ob lokale Erklärung von だったら/なら für Anfänger ausreicht; keine vollständige Behandlung aller Konditionalnuancen. |
| Alle 123 Karten | Deutsche Näherungsaussprache, Natürlichkeit und Hörverständnis sind nicht muttersprachlich oder mit echten Aufnahmen abgenommen. |

## Zuordnung Befund Kennung Änderung Prüfung

| Position | Lektions-ID | Karten-IDs | Ausgangsbefund und Änderung | Konkrete Prüfung |
| --- | --- | --- | --- | --- |
| 47 | `v11:people-age` | `v11:people-age:0` bis `v11:people-age:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Eine bis drei Personen zählen und Altersangaben für zwanzig und dreißig davon unterscheiden. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 48 | `12:1` | `12:1:0` bis `12:1:2` | Explizites Vorwissen und begründete Fehlantworten fehlten; Eine Frage nach der jetzigen Uhrzeit von einer Altersfrage unterscheiden und sieben Uhr nennen. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 49 | `v11:weekdays` | `v11:weekdays:0` bis `v11:weekdays:6` | Explizites Vorwissen und begründete Fehlantworten fehlten; Alle sieben Wochentage zuordnen und Samstag von Sonntag für eine Verabredung unterscheiden. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 50 | `v11:clock-hours` | `v11:clock-hours:0` bis `v11:clock-hours:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; 1, 4, 7 und 9 Uhr lesen und 2:30 von 3:30 unterscheiden. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 51 | `v11:clock-minutes` | `v11:clock-minutes:0` bis `v11:clock-minutes:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; 1, 5 und 10 Minuten sowie 9 Uhr vormittags und 15 Uhr unterscheiden. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 52 | `v11:calendar` | `v11:calendar:0` bis `v11:calendar:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Januar, April, September und den ersten/zwanzigsten Monatstag vom Alter unterscheiden. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 53 | `v11:relative-time` | `v11:relative-time:0` bis `v11:relative-time:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Gestern, heute, morgen, jeden Tag und nächste Woche in einfachen Beispielen zeitlich einordnen. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 59 | `v11:frequency` | `v11:frequency:0` bis `v11:frequency:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Regelmäßigkeit, gelegentliche Handlung, wenig/selten und überhaupt nicht auseinanderhalten. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 82 | `v11:seasons` | `v11:seasons:0` bis `v11:seasons:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Vier Jahreszeiten zuordnen und Jahreszeit von Monat und Wetter unterscheiden. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 83 | `v11:weather-words` | `v11:weather-words:0` bis `v11:weather-words:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Sonne, Regen und Schnee benennen und Kälte der Umgebung von kaltem Wasser unterscheiden. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 84 | `v11:adjective-time` | `v11:adjective-time:0` bis `v11:adjective-time:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Gegenwart, Vergangenheit und verneinte Vergangenheit bei den erklärten Adjektiven unterscheiden. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 85 | `v11:feelings` | `v11:feelings:0` bis `v11:feelings:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Schläfrigkeit, Erschöpfung, Freude und Spaß als unterschiedliche Aussagen über Befinden erkennen. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 88 | `v11:games` | `v11:games:0` bis `v11:games:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Gemeinsames Spielen, Sieg, Niederlage und den Wunsch nach einer weiteren Runde unterscheiden. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 89 | `v11:media-actions` | `v11:media-actions:0` bis `v11:media-actions:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Film schauen, Manga lesen, Musik hören, fotografieren und singen mit dem passenden Verb verbinden. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 90 | `v11:inviting` | `v11:inviting:0` bis `v11:inviting:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Mit ませんか zu einer gemeinsamen Tätigkeit einladen und nach einem passenden Termin fragen. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 91 | `v11:reply-invites` | `v11:reply-invites:0` bis `v11:reply-invites:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Einladung annehmen, einen Tag höflich ablehnen und eine noch unverbindliche spätere Möglichkeit nennen. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 92 | `23:0` | `23:0:0` bis `23:0:3` | Explizites Vorwissen und begründete Fehlantworten fehlten; Vier Wörterbuchformen den bekannten höflichen Formen zuordnen und ihren Zeitbezug aus dem Kontext lesen. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 93 | `v11:verb-groups` | `v11:verb-groups:0` bis `v11:verb-groups:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Die fünf erklärten Verben ihrer Gruppe zuordnen und die passende höfliche Form auswählen. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 94 | `7:0` | `7:0:0` bis `7:0:3` | Explizites Vorwissen und begründete Fehlantworten fehlten; Bejahung, Verneinung, Vergangenheit und die verbindende て-Form von essen auseinanderhalten. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 126 | `v11:appointments` | `v11:appointments:0` bis `v11:appointments:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Beginn und Ende erfragen, eine Uhrzeit festlegen und einen alternativen Tag vorschlagen. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 129 | `v11:messages` | `v11:messages:0` bis `v11:messages:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Eine höfliche Nachricht in Gruß, Dank, Änderungswunsch, Antwortbitte und Abschluss gliedern. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 134 | `v11:dialog-weekend` | `v11:dialog-weekend:0` bis `v11:dialog-weekend:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Gemeinsam Tätigkeit, Tag, Uhrzeit und Treffpunkt vereinbaren und die vier Angaben getrennt bestätigen. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 137 | `v11:read-weekend` | `v11:read-weekend:0` bis `v11:read-weekend:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Aus fünf Sätzen Zeitpunkt, Begleitung, Ziel, Wetter und Tätigkeit eines vergangenen Ausflugs entnehmen. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 138 | `v11:read-plan` | `v11:read-plan:0` bis `v11:read-plan:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; In einem Ausflugsplan Abfahrt, Treffort, Wunsch und wetterabhängige Alternative unterscheiden. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |
| 139 | `v11:read-message` | `v11:read-message:0` bis `v11:read-message:4` | Explizites Vorwissen und begründete Fehlantworten fehlten; Grund, neuen Tag, mögliche Tageshälfte und offene Rückfrage einer Terminänderung herauslesen. | Voraussetzungen früher im Lernweg; jede Kartenlösung/Fehlantwort und Altprofil; sichtbare Hilfe ohne Freigabe. |

## 47 Menschen zählen und das Alter angeben

Stabile ID: `v11:people-age`. 5 vorhandene Karten. Lernziel: Eine bis drei Personen zählen und Altersangaben für zwanzig und dreißig davon unterscheiden.

Voraussetzungen: `v11:numbers-eleven`, `v11:count-objects`.

ひとり hitori = eine Person, ふたり futari = zwei Personen, さんにん sannin = drei Personen. Das zählt Menschen: Zwei Gäste sind ふたり, zwei bestellte Dinge dagegen ふたつ. Mit です wird daraus eine höfliche Antwort, etwa ふたりです, wir sind zu zweit.

Alter: はたち hatachi heißt zwanzig Jahre alt; さんじゅっさい sanjussai dreißig Jahre alt. さい sai zählt Lebensjahre, にん nin Personen. Die Zahl allein beantwortet noch nicht beide Fragen. Für dreißig Jahre kommt auch さんじっさい sanjissai vor; hier übst du die angegebene Form.

Sprich hi-to-ri, fu-ta-ri und ha-ta-chi in kurzen Takten. Bei san-nin stehen zwei n hintereinander; sanjussai enthält eine Pause vor s. Im Beispiel ひとりです entscheidet die Situation, ob jemand allein kommt oder eine Person gemeint ist.

Abruf: Du reservierst für zwei Gäste. Antworte mit der Personenanzahl und nenne danach getrennt das Alter zwanzig.

Spätere Wiederaufnahme: `v11:count-objects`, `v11:numbers-eleven`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:people-age:0` | ひとり | Gezielte Anwendungsfrage: Du meldest zwei Gäste an. Welche Personenangabe passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:people-age:1` | ふたり | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu ふたり? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:people-age:2` | さんにん | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu さんにん? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:people-age:3` | はたち | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu はたち? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:people-age:4` | さんじゅっさい | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu さんじゅっさい? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 48 Uhrzeit und Alter

Stabile ID: `12:1`. 3 vorhandene Karten. Lernziel: Eine Frage nach der jetzigen Uhrzeit von einer Altersfrage unterscheiden und sieben Uhr nennen.

Voraussetzungen: `v11:people-age`, `v11:numbers-six-ten`.

いま ima = jetzt; なんじ nanji = wie viel Uhr. いまなんじですか fragt nach der jetzigen Uhrzeit. じ ji kennzeichnet eine Uhrzeit. Neu im Beispiel: さんじ sanji = drei Uhr; いまさんじです bedeutet jetzt ist es drei Uhr.

しちじ shichiji ist die hier geübte Form für sieben Uhr. Die Grundzahl なな nana wird also nicht einfach unverändert übernommen. なんさい nansai fragt dagegen wie alt. Antworte darauf mit einer Altersangabe wie dem bekannten さんじゅっさいです, ich bin dreißig.

Eine Altersfrage ist persönlich; die höfliche Satzform allein macht sie nicht in jeder Begegnung passend. Nan-ji enthält den n-Takt vor ji; shi-chi-ji besteht aus drei kurzen Silbentakten. Die ganze Frage endet auf ですか, eine Antwort nur auf です.

Abruf: Jemand antwortet mit sieben Uhr. Welche Frage könnte davor stehen? Warum passt die Altersfrage nicht?

Spätere Wiederaufnahme: `v11:people-age`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `12:1:0` | いまなんじですか。 | Gezielte Anwendungsfrage: Du möchtest wissen, wie spät es jetzt ist. Welche Frage passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `12:1:1` | しちじ | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Bedeutung passt zu しちじ? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `12:1:2` | なんさいですか。 | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Bedeutung passt zu なんさいですか。? Alle 2 falschen Auswahlwerte einzeln begründet. |

## 49 Die sieben Wochentage

Stabile ID: `v11:weekdays`. 7 vorhandene Karten. Lernziel: Alle sieben Wochentage zuordnen und Samstag von Sonntag für eine Verabredung unterscheiden.

Voraussetzungen: `12:1`, `v11:long-vowels`.

Erste Gruppe: げつようび getsuyōbi Montag, かようび kayōbi Dienstag, すいようび suiyōbi Mittwoch. Zweite Gruppe: もくようび mokuyōbi Donnerstag, きんようび kinyōbi Freitag. Wochenende: どようび doyōbi Samstag und にちようび nichiyōbi Sonntag.

ようび yōbi ist der gemeinsame Teil für Wochentag. なんようび nanyōbi fragt welcher Wochentag; das ist nicht die Uhrzeitfrage なんじ. どようびです bedeutet es ist Samstag. Die Kalenderzeichen 月・火・水・木・金・土・日 stehen in dieser Reihenfolge für Montag bis Sonntag; sie werden hier nur als Lesehilfe eingeführt.

In allen sieben Wörtern bleibt yō lang. Kinyōbi behält den n-Takt vor yō; suiyōbi beginnt su-i. Lerne zuerst die drei Gruppen, rufe danach einzelne Tage in gemischter Reihenfolge ab. Ein Wochentag legt noch keine Stunde fest.

Abruf: Ein Treffen soll nicht am Samstag, sondern am Sonntag sein. Nenne den neuen Tag, dann den vorherigen Freitag.

Spätere Wiederaufnahme: `12:1`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:weekdays:0` | げつようび | Gezielte Anwendungsfrage: Das Treffen soll am Sonntag sein. Welcher Wochentag passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:weekdays:1` | かようび | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu かようび? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:weekdays:2` | すいようび | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu すいようび? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:weekdays:3` | もくようび | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu もくようび? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:weekdays:4` | きんようび | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu きんようび? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:weekdays:5` | どようび | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu どようび? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:weekdays:6` | にちようび | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu にちようび? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 50 Volle Stunden und halb

Stabile ID: `v11:clock-hours`. 5 vorhandene Karten. Lernziel: 1, 4, 7 und 9 Uhr lesen und 2:30 von 3:30 unterscheiden.

Voraussetzungen: `12:1`, `v11:numbers-six-ten`.

Uhrzeiten: いちじ ichiji 1 Uhr, よじ yoji 4 Uhr, しちじ shichiji 7 Uhr, くじ kuji 9 Uhr. Merke die Sonderlesungen als ganze Formen: vier Uhr hat kein n, neun Uhr kein langes ū. Zusätzlich für Beispiele: にじ niji 2 Uhr, さんじ sanji 3 Uhr, じゅうじ jūji 10 Uhr.

はん han = halb, nach einer Uhrzeit eine halbe Stunde später. にじはん niji han ist zwei Uhr plus eine halbe Stunde: 2:30, auf Deutsch halb drei. さんじはん sanji han wäre 3:30, halb vier. Gehe beim Umrechnen immer von der genannten vollen Stunde aus.

Eine Antwort kann auf です enden: よじです, es ist vier Uhr. Uhrzeiten allein unterscheiden noch nicht morgens und nachmittags. Sprich yo-ji und ku-ji kurz, jū-ji mit langem ū. Han endet auf einen eigenen n-Takt.

Abruf: Lies 4:00, 9:00 und 2:30 in anderer Reihenfolge. Erkläre, warum halb drei auf Japanisch mit zwei beginnt.

Spätere Wiederaufnahme: `12:1`, `v11:numbers-six-ten`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:clock-hours:0` | いちじ | Gezielte Anwendungsfrage: Eine Uhr zeigt 2:30, auf Deutsch halb drei. Welche Form passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:clock-hours:1` | よじ | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu よじ? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:clock-hours:2` | しちじ | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu しちじ? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:clock-hours:3` | くじ | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu くじ? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:clock-hours:4` | にじはん | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu にじはん? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 51 Minuten und Tageshälften

Stabile ID: `v11:clock-minutes`. 5 vorhandene Karten. Lernziel: 1, 5 und 10 Minuten sowie 9 Uhr vormittags und 15 Uhr unterscheiden.

Voraussetzungen: `v11:clock-hours`, `v11:small-tsu`.

Minuten: いっぷん ippun 1 Minute, ごふん gofun 5 Minuten, じゅっぷん juppun 10 Minuten. Für zehn Minuten ist auch じっぷん jippun gebräuchlich. Die Formen werden hier einzeln gelernt; Zahl + fun wird nicht immer unverändert zusammengesetzt. なんぷん nanpun fragt wie viele Minuten.

ごぜん gozen steht vor einer Uhrzeit am Vormittag, ごご gogo am Nachmittag: ごぜんくじ = 9 Uhr, ごごさんじ = 15 Uhr. Für spätere Termine außerdem: ごぜんじゅうじ gozen jūji = 10 Uhr vormittags; ごごにじ gogo niji = 14 Uhr. Eine Dauer von fünf Minuten ist keine Uhrzeit fünf Uhr.

In ippun und juppun liegt eine kurze Verschlusspause vor p; in gofun nicht. Das z in gozen ist stimmhaft. Für spätere Wegfragen: あるいて aruite = zu Fuß, ぐらい gurai = ungefähr. あるいてごふんぐらいです heißt es sind ungefähr fünf Minuten zu Fuß; keine genaue Startzeit.

Abruf: Jemand fragt nach der Dauer des Wegs. Antworte fünf Minuten. Nenne danach getrennt einen Treffzeitpunkt um 15 Uhr.

Spätere Wiederaufnahme: `v11:clock-hours`, `v11:numbers-six-ten`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:clock-minutes:0` | いっぷん | Gezielte Anwendungsfrage: Ihr trefft euch um 15 Uhr. Welche Zeitangabe passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:clock-minutes:1` | ごふん | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu ごふん? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:clock-minutes:2` | じゅっぷん | Gezielte Anwendungsfrage: Die Wegbeschreibung lautet あるいてごふんぐらいです. Was erfährst du? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:clock-minutes:3` | ごぜんくじ | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu ごぜんくじ? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:clock-minutes:4` | ごごさんじ | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu ごごさんじ? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 52 Monate und besondere Kalendertage

Stabile ID: `v11:calendar`. 5 vorhandene Karten. Lernziel: Januar, April, September und den ersten/zwanzigsten Monatstag vom Alter unterscheiden.

Voraussetzungen: `v11:people-age`, `v11:clock-hours`.

Monate: いちがつ ichigatsu Januar, しがつ shigatsu April, くがつ kugatsu September. がつ gatsu kennzeichnet hier den Monatsnamen. Vier und neun haben wie bei bestimmten Uhrzeiten besondere Lesungen; lerne しがつ und くがつ als ganze Wörter.

ついたち tsuitachi bezeichnet den Ersten eines Monats, はつか hatsuka den Zwanzigsten. はつか kann auch eine Dauer von zwanzig Tagen bedeuten; das einzelne Wort legt den Kontext nicht fest. しがつついたち shigatsu tsuitachi = 1. April: Monat zuerst, danach der Tag.

Vergleiche はつか hatsuka, zwanzigster Tag, mit はたち hatachi, zwanzig Jahre alt. Eine Dauer von einem Tag heißt いちにち ichinichi und nicht ついたち. Diese Ausnahme wird erklärt, aber weitere unbekannte Datumslesungen werden hier nicht verlangt.

Abruf: Lies den 1. April. Nenne dann zwanzig Jahre alt und den zwanzigsten Monatstag, ohne die Endungen zu vertauschen.

Spätere Wiederaufnahme: `v11:people-age`, `v11:clock-hours`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:calendar:0` | いちがつ | Gezielte Anwendungsfrage: Du liest den 1. April. Welche Reihenfolge passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:calendar:1` | しがつ | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu しがつ? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:calendar:2` | くがつ | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu くがつ? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:calendar:3` | ついたち | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu ついたち? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:calendar:4` | はつか | Gezielte Anwendungsfrage: Im Kalender ist der zwanzigste Tag gemeint. Welches Wort passt? Alle 2 falschen Auswahlwerte einzeln begründet. |

## 53 Gestern, heute, morgen und jede Woche

Stabile ID: `v11:relative-time`. 5 vorhandene Karten. Lernziel: Gestern, heute, morgen, jeden Tag und nächste Woche in einfachen Beispielen zeitlich einordnen.

Voraussetzungen: `v11:weekdays`, `v11:clock-hours`, `2:0`.

きのう kinō gestern, きょう kyō heute, あした ashita morgen (nächster Tag), まいにち mainichi jeden Tag, らいしゅう raishū nächste Woche. Das deutsche morgen ist hier keine Tageszeit; der Morgen als Tageszeit heißt あさ asa. 毎日 und 来週 sind häufige Schreibungen für mainichi und raishū.

Vor den Beispielen: やすみ yasumi = frei/Pause, いきます ikimasu = gehe/fahre, べんきょうします benkyō shimasu = lerne. やすみです heißt habe frei, やすみでした hatte frei. Bei diesem Nomen macht でした die Aussage vergangen. あしたいきます beschreibt mit derselben höflichen Verbform einen Plan für morgen.

Diese Zeitwörter können direkt vor dem Satz stehen; für heute oder morgen braucht man hier kein に. まいにち beschreibt Wiederholung, らいしゅう eine kommende Woche. Kinō und kyō haben langes ō, raishū langes ū. Die Endung des Satzes und das Zeitwort gemeinsam lesen.

Abruf: Ordne einen freien Tag gestern und einen geplanten Weg morgen ein. Welches Wort würde tägliche Wiederholung ausdrücken?

Spätere Wiederaufnahme: `v11:weekdays`, `2:0`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:relative-time:0` | きのう | Gezielte Anwendungsfrage: Jemand sagt あしたいきます. Wie ist die Handlung zeitlich gemeint? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:relative-time:1` | あした | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu あした? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:relative-time:2` | きょう | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu きょう? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:relative-time:3` | まいにち | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu まいにち? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:relative-time:4` | らいしゅう | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu らいしゅう? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 59 Oft, manchmal und fast nie

Stabile ID: `v11:frequency`. 5 vorhandene Karten. Lernziel: Regelmäßigkeit, gelegentliche Handlung, wenig/selten und überhaupt nicht auseinanderhalten.

Voraussetzungen: `v11:relative-time`, `v11:polite-past`, `v11:work-study`.

いつも itsumo immer/gewöhnlich, よく yoku oft, ときどき tokidoki manchmal. Die Abstufungen sind keine festen Prozentzahlen. Beispiele nutzen bekannte Formen: ほんをよみます lese Bücher, みずをのみます trinke Wasser. ゲーム gēmu = Spiel; ゲームをします heißt ich spiele.

あまり amari steht in den hier geübten Sätzen mit Verneinung: あまりのみません trinke nicht viel/nicht oft. ぜんぜん zenzen + ません verneint ganz: ぜんぜんみません schaue überhaupt nicht. テレビ terebi heißt Fernsehen. Ohne die Verneinung wäre die gelernte Aussage nicht mehr dieselbe.

Im Kontext einer Gewohnheit bedeutet よく oft; es kann anderswo gut heißen. いつも und ときどき werden nicht mit に an das Verb gehängt. Tokidoki hat stimmhaftes d im zweiten toki-Teil; in zenzen ist z stimmhaft. Halte bei gēmu das ē lang.

Abruf: Beschreibe tägliches Lernen mit まいにち. Tausche dann nur die Häufigkeit gegen manchmal; verneine anschließend Fernsehen vollständig.

Spätere Wiederaufnahme: `v11:relative-time`, `v11:polite-past`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:frequency:0` | いつも | Gezielte Anwendungsfrage: Du möchtest sagen, dass du überhaupt nicht schaust. Welche Form passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:frequency:1` | よく | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu よく? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:frequency:2` | ときどき | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu ときどき? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:frequency:3` | あまりのみません | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu あまりのみません? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:frequency:4` | ぜんぜんみません | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu ぜんぜんみません? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 82 Die Jahreszeiten

Stabile ID: `v11:seasons`. 5 vorhandene Karten. Lernziel: Vier Jahreszeiten zuordnen und Jahreszeit von Monat und Wetter unterscheiden.

Voraussetzungen: `v11:calendar`, `v11:relative-time`, `v11:food-preferences`.

はる haru Frühling, なつ natsu Sommer, あき aki Herbst, ふゆ fuyu Winter. きせつ kisetsu ist der Oberbegriff Jahreszeit, keine fünfte Jahreszeit. Alle fünf Wörter sind Nomen. Ein Monatsname wie しがつ benennt dagegen einen Kalenderabschnitt.

いまははるです (ima wa haru desu) heißt jetzt ist Frühling. Die Beispiele fragen nach Vorlieben: はるがすきです, ich mag den Frühling; どのきせつがすきですか, welche Jahreszeit mögen Sie? どの dono fragt welches vor einem Nomen. あつい atsui heiß und さむい samui kalt sind Eigenschaften; eine Jahreszeit legt das Wetter eines Tages nicht fest.

Haru, natsu, aki und fuyu haben jeweils zwei kurze Vokale; kisetsu drei Takte ki-se-tsu. Sprich fu mit sanftem Luftstrom, nicht wie ein kräftiges deutsches f. Ein Satz wie ふゆです ist eine jahreszeitliche Angabe, keine Datumsangabe.

Abruf: Nenne einen Monat und eine Jahreszeit getrennt. Welche Jahreszeit folgt in der üblichen Reihenfolge auf den Sommer?

Spätere Wiederaufnahme: `v11:calendar`, `v11:relative-time`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:seasons:0` | はる | Gezielte Anwendungsfrage: Welche Jahreszeit folgt in der üblichen Reihenfolge auf den Sommer? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:seasons:1` | なつ | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu なつ? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:seasons:2` | あき | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu あき? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:seasons:3` | ふゆ | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu ふゆ? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:seasons:4` | きせつ | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu きせつ? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 83 Sonne, Regen, Schnee und Temperatur

Stabile ID: `v11:weather-words`. 5 vorhandene Karten. Lernziel: Sonne, Regen und Schnee benennen und Kälte der Umgebung von kaltem Wasser unterscheiden.

Voraussetzungen: `v11:seasons`, `v11:taste`, `v11:relative-time`.

はれ hare klares/sonniges Wetter, あめ ame Regen und ゆき yuki Schnee sind Nomen. てんき tenki bedeutet Wetter. Mit dem bekannten Tageswort: きょうはあめです (kyō wa ame desu), heute regnet es. Du musst hier kein neues Wetterverb bilden.

さむい samui beschreibt kaltes Wetter beziehungsweise dass jemand friert. つめたい tsumetai aus der Getränkelektion beschreibt beispielsweise kaltes Wasser. あたたかい atatakai heißt warm und kann Wetter oder Gegenstände beschreiben. Wetter und Getränketemperatur haben also nicht in jeder Richtung dasselbe Wort.

Lies sa-mu-i und a-ta-ta-ka-i mit ihren Vokalen; die zwei ta nicht zusammenziehen. ゆき yuki hat kurzes u. あめ kann ohne Schrift und Kontext auch ein anderes Wort bezeichnen; in diesen Wetterbeispielen ist Regen gemeint. Der Kurs vergibt keine Tonhöhenbewertung.

Abruf: Beschreibe einen kalten Tag und kaltes Wasser mit den unterschiedlichen Adjektiven. Wiederhole danach das Wort für Schnee.

Spätere Wiederaufnahme: `v11:taste`, `v11:relative-time`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:weather-words:0` | はれ | Gezielte Anwendungsfrage: Du beschreibst einen kalten Tag, nicht kaltes Wasser. Welches Adjektiv passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:weather-words:1` | あめ | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu あめ? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:weather-words:2` | ゆき | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu ゆき? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:weather-words:3` | さむい | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu さむい? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:weather-words:4` | あたたかい | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu あたたかい? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 84 Adjektive: gestern war es anders

Stabile ID: `v11:adjective-time`. 5 vorhandene Karten. Lernziel: Gegenwart, Vergangenheit und verneinte Vergangenheit bei den erklärten Adjektiven unterscheiden.

Voraussetzungen: `17:0`, `v11:weather-words`, `v11:rooms`, `v11:relative-time`.

Bei い-Adjektiven verändert sich das Adjektiv: あつい atsui heiß → あつかった atsukatta war heiß. さむい samui kalt → さむくない samukunai nicht kalt → さむくなかった samukunakatta war nicht kalt. です macht diese Sätze höflich; nicht zusätzlich でした anhängen.

いい ii gut verwendet beim Beugen den Stamm よ: よかった yokatta war gut. Neu erklärtes Beispiel: てんきがよかったです (tenki ga yokatta desu), das Wetter war gut. しずか shizuka ruhig ist ein な-Adjektiv: しずかでした war ruhig; hier verändert sich die höfliche Endung.

きのうは gestern und きょうは heute legen den Zeitbezug fest. へや heya ist das bekannte Zimmer. きのうはさむくなかったです berichtet ausdrücklich keine Kälte gestern, nicht bloß keine Kälte jetzt. In katta steckt eine Pause vor t; in shizuka ist z stimmhaft.

Abruf: Sage nicht kalt für heute und für gestern. Beschreibe danach ein Zimmer rückblickend als ruhig.

Spätere Wiederaufnahme: `17:0`, `v11:weather-words`, `v11:relative-time`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:adjective-time:0` | あつかったです | Gezielte Anwendungsfrage: Du sagst ausdrücklich: Gestern war es nicht kalt. Welche Form passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:adjective-time:1` | さむくないです | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu さむくないです? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:adjective-time:2` | さむくなかったです | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu さむくなかったです? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:adjective-time:3` | よかったです | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu よかったです? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:adjective-time:4` | しずかでした | Gezielte Anwendungsfrage: Ein Zimmer war gestern ruhig. Welche Adjektivverbindung passt? Alle 2 falschen Auswahlwerte einzeln begründet. |

## 85 Wie geht es dir gerade?

Stabile ID: `v11:feelings`. 5 vorhandene Karten. Lernziel: Schläfrigkeit, Erschöpfung, Freude und Spaß als unterschiedliche Aussagen über Befinden erkennen.

Voraussetzungen: `v11:adjective-time`, `v11:polite-past`.

げんきです genki desu = mir geht es gut/bin fit; ねむいです nemui desu = bin schläfrig. つかれました tsukaremashita berichtet Erschöpfung nach Anstrengung. Das Bedürfnis zu schlafen und Müdigkeit nach einer Tätigkeit sind nicht genau dasselbe.

うれしい ureshii = erfreut, たのしい tanoshii = macht Spaß. すこし sukoshi etwas und とても totemo sehr sind Gradangaben: すこしねむいです, etwas schläfrig. べんきょう benkyō ist Lernen; べんきょうはたのしいです bewertet diese Tätigkeit als angenehm.

げんき ist ein な-Adjektiv; ねむい・うれしい・たのしい sind い-Adjektive. Das lange ii in ureshii und tanoshii bleibt. Die ました-Form in つかれました kann einen jetzt spürbaren Zustand ausdrücken. Aus diesen Alltagssätzen lässt sich keine Diagnose ableiten.

Abruf: Eine Tätigkeit macht dir Spaß, danach bist du erschöpft. Formuliere die beiden Aussagen getrennt; welche Form würde stattdessen Schlafbedarf nennen?

Spätere Wiederaufnahme: `v11:adjective-time`, `v11:polite-past`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:feelings:0` | げんきです | Gezielte Anwendungsfrage: Du brauchst Schlaf. Welche Aussage nennt genau dieses Befinden? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:feelings:1` | ねむいです | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu ねむいです? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:feelings:2` | つかれました | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu つかれました? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:feelings:3` | うれしいです | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu うれしいです? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:feelings:4` | たのしいです | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu たのしいです? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 88 Über Spiele reden

Stabile ID: `v11:games`. 5 vorhandene Karten. Lernziel: Gemeinsames Spielen, Sieg, Niederlage und den Wunsch nach einer weiteren Runde unterscheiden.

Voraussetzungen: `v11:hobbies`, `v11:frequency`, `v11:polite-past`.

ゲームをします gēmu o shimasu = spiele ein Spiel. いっしょに issho ni = gemeinsam; あそびます asobimasu = spiele/verbringe Freizeit. ともだち tomodachi Freund und と als Begleitung ergeben ともだちといっしょにあそびます, ich spiele mit einem Freund.

かちます kachimasu gewinnen → かちました habe gewonnen. まけます makemasu verlieren → まけました habe verloren, hier einen Wettbewerb. Das ist nicht なくしました für einen verlorenen Gegenstand. Beide Beispiele verwenden die schon erklärte höfliche Vergangenheit.

もう mō hier noch, いっかい ikkai einmal: もういっかい bedeutet noch einmal/noch eine Runde. Mit おねがいします wird eine Bitte daraus. Gēmu und mō enthalten lange Vokale; issho und ikkai haben einen verdoppelten Konsonantentakt. よく wiederholt das bekannte oft.

Abruf: Berichte einen Sieg gestern und bitte dann um eine weitere Runde. Welche andere Form würde eine Niederlage melden?

Spätere Wiederaufnahme: `v11:frequency`, `v11:polite-past`, `v11:travel-help`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:games:0` | ゲームをします | Gezielte Anwendungsfrage: Du hast ein Spiel gewonnen. Was meldest du? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:games:1` | いっしょにあそびます | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu いっしょにあそびます? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:games:2` | かちました | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu かちました? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:games:3` | まけました | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu まけました? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:games:4` | もういっかい | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu もういっかい? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 89 Lesen, schauen und Musik hören

Stabile ID: `v11:media-actions`. 5 vorhandene Karten. Lernziel: Film schauen, Manga lesen, Musik hören, fotografieren und singen mit dem passenden Verb verbinden.

Voraussetzungen: `v11:hobbies`, `v11:games`, `v11:location-action`.

えいが eiga Film + みます mimasu schauen; まんが manga Comic + よみます yomimasu lesen; おんがく ongaku Musik + ききます kikimasu hören. Das Objekt steht mit を vor dem Verb. Ein Wort kann mehrere Bedeutungen haben: ききます meint hier hören, nicht nachfragen.

しゃしん shashin Foto + とります torimasu aufnehmen, うた uta Lied + うたいます utaimasu singen. Vor dem Beispiel: こうえん kōen = Park; こうえんでしゃしんをとります heißt im Park Fotos machen. で zeigt den Handlungsort, を das Aufgenommene.

いえで ie de zu Hause, よく yoku oft, まいにち mainichi jeden Tag sind Wiederholungen. にほんごのうた ist ein japanisches Lied; の ordnet die Sprache zu. Kōen hat langes ō, shashin einen n-Takt. Verb und Gegenstand zusammen abrufen, nicht nur das erste Wort erkennen.

Abruf: Tausche beim Satz über einen Film die Tätigkeit gegen Musik hören. Nenne danach den Ort, an dem du Fotos machst.

Spätere Wiederaufnahme: `v11:location-action`, `v11:frequency`, `v11:hobbies`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:media-actions:0` | えいがをみます | Gezielte Anwendungsfrage: Du machst im Park Fotos. Welcher Satz passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:media-actions:1` | まんがをよみます | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu まんがをよみます? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:media-actions:2` | おんがくをききます | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu おんがくをききます? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:media-actions:3` | しゃしんをとります | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu しゃしんをとります? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:media-actions:4` | うたをうたいます | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu うたをうたいます? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 90 Jemanden einladen

Stabile ID: `v11:inviting`. 5 vorhandene Karten. Lernziel: Mit ませんか zu einer gemeinsamen Tätigkeit einladen und nach einem passenden Termin fragen.

Voraussetzungen: `v11:media-actions`, `v11:weekdays`, `v11:polite-past`.

Aus いきます ikimasu wird die Einladungsfrage いきませんか ikimasen ka. Obwohl darin die Verneinungsform steckt, bedeutet sie hier möchten wir gehen? いっしょに issho ni betont gemeinsam. Ohne か wäre いきません eine negative Aussage statt dieser Einladung.

Das gleiche Muster mit bekannten Tätigkeiten: えいがをみませんか wollen wir einen Film schauen; おちゃをのみませんか wollen wir Tee trinken. を und das Objekt bleiben. いつ itsu fragt wann; いつがいいですか fragt nach einem passenden Zeitpunkt.

Termin vorschlagen: どようびはどうですか (doyōbi wa dō desu ka), wie wäre es mit Samstag? は stellt Samstag zur Wahl, どうですか erbittet eine Einschätzung. In doyōbi und dō ist ō lang. Eine Einladung garantiert noch keine Zusage; die Antwort muss abgewartet werden.

Abruf: Lade jemanden zum Filmschauen ein. Frage erst offen nach einem Termin, schlage dann Samstag vor.

Spätere Wiederaufnahme: `v11:media-actions`, `v11:weekdays`, `v11:polite-past`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:inviting:0` | いっしょにいきませんか | Gezielte Anwendungsfrage: Du lädst zu gemeinsamem Filmschauen ein. Welche Form passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:inviting:1` | えいがをみませんか | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu えいがをみませんか? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:inviting:2` | おちゃをのみませんか | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu おちゃをのみませんか? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:inviting:3` | いつがいいですか | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu いつがいいですか? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:inviting:4` | どようびはどうですか | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu どようびはどうですか? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 91 Zusagen und freundlich absagen

Stabile ID: `v11:reply-invites`. 5 vorhandene Karten. Lernziel: Einladung annehmen, einen Tag höflich ablehnen und eine noch unverbindliche spätere Möglichkeit nennen.

Voraussetzungen: `v11:inviting`, `v11:existence`, `v11:checkout`.

いいですね ii desu ne = gute Idee; いきましょう ikimashō = gehen wir. Dafür wird bei いきます die Endung ます durch ましょう ersetzt. Neu als wiederverwendbarer Vorschlag: しましょう shimashō machen wir. だいじょうぶです bestätigt hier einen passenden Termin.

どようびはちょっと (doyōbi wa chotto) deutet an, dass Samstag nicht gut passt; nicht als feste Zusage lesen. ようじ yōji eine Erledigung/Verpflichtung + があります ich habe: ようじがあります, ich habe etwas vor. そのひ sono hi = an dem Tag, aus その dieser/jener und ひ Tag.

またこんどおねがいします (mata kondo onegai shimasu) lässt ein anderes Mal offen, vereinbart aber keinen neuen Tag. だいじょうぶ ist situationsabhängig: Beim Termin hier Zustimmung, bei der Tütenfrage zuvor eine mögliche Absage. ましょう hat langes ō, ちょっと eine Pause vor t.

Abruf: Sage Samstag höflich ab und lasse ein anderes Mal offen. Warum ist damit noch kein Sonntagstermin vereinbart?

Spätere Wiederaufnahme: `v11:inviting`, `v11:checkout`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:reply-invites:0` | いいですね、いきましょう | Gezielte Anwendungsfrage: Samstag passt nicht. Du möchtest das höflich andeuten. Was passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:reply-invites:1` | だいじょうぶです | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu だいじょうぶです? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:reply-invites:2` | どようびはちょっと | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu どようびはちょっと? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:reply-invites:3` | ようじがあります | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu ようじがあります? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:reply-invites:4` | またこんどおねがいします | Gezielte Anwendungsfrage: Nach einer Absage heißt es またこんどおねがいします. Was ist damit vereinbart? Alle 2 falschen Auswahlwerte einzeln begründet. |

## 92 辞書形 – Grundform

Stabile ID: `23:0`. 4 vorhandene Karten. Lernziel: Vier Wörterbuchformen den bekannten höflichen Formen zuordnen und ihren Zeitbezug aus dem Kontext lesen.

Voraussetzungen: `v11:media-actions`, `v11:reply-invites`, `v11:relative-time`.

Wörterbuchform bedeutet Nachschlageform, keine neue Zeitstufe: たべる taberu essen ↔ たべます, いく iku gehen/fahren ↔ いきます, する suru machen ↔ します, くる kuru kommen ↔ きます. する und くる folgen eigenen Wechseln. Wie die Gruppen funktionieren, wird in der nächsten Einheit vertieft.

Die neutrale Form kann in vertrauter Rede stehen; sie bedeutet nicht automatisch einen Befehl. Mit あした morgen ist あしたとうきょうへいく ein zukünftiger Weg nach Tokio. とうきょう Tōkyō ist der Ortsname; へ liest man als Zielmarkierung e.

Vor den Beispielen: しゅくだい shukudai Hausaufgaben; しゅくだいをする heißt Hausaufgaben machen. ともだちがくる meldet, dass ein Freund kommt. Sushi und Freund sind bekannt. Kuru und suru haben kurze Vokale, Tōkyō zwei lange ō. Wähle die Höflichkeit passend zur Situation.

Abruf: Ordne きます und します ihren Grundformen zu. Lies dann einen Satz mit morgen, ohne die Grundform als Vergangenheit zu verstehen.

Spätere Wiederaufnahme: `v11:media-actions`, `v11:relative-time`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `23:0:0` | たべる | Gezielte Anwendungsfrage: Welche Wörterbuchform gehört zu der höflichen Form きます? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `23:0:1` | いく | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Bedeutung passt zu いく? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `23:0:2` | する | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Bedeutung passt zu する? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `23:0:3` | くる | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Bedeutung passt zu くる? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 93 Welche Verbgruppe ist das?

Stabile ID: `v11:verb-groups`. 5 vorhandene Karten. Lernziel: Die fünf erklärten Verben ihrer Gruppe zuordnen und die passende höfliche Form auswählen.

Voraussetzungen: `23:0`, `v11:media-actions`, `v11:work-study`.

Ichidan-Verben behalten hier einen Stamm: たべる taberu → たべます tabemasu; みる miru → みます mimasu. Das Schluss-る fällt weg. Die Beispielobjekte パン Brot und えいが Film sind bereits bekannt.

Godan-Verben ändern den letzten Laut für ます. Gegenbeispiel zur bloßen Endung: かえる kaeru zurückkehren → かえります kaerimasu. Trotz eru ist dieses Verb Godan. いえにかえります heißt nach Hause zurückkehren; いえ Haus und に als Ziel sind bekannt.

Unregelmäßig: する suru → します shimasu; くる kuru → きます kimasu. べんきょうします lerne und あしたきます komme morgen zeigen beide im Kontext. Keine Regel alle Verben auf iru/eru sind Ichidan ableiten; diese fünf Gruppenangaben ausdrücklich mitlernen.

Abruf: Eine Person kehrt nach Hause zurück. Wähle die höfliche Form von かえる und erkläre, warum das Weglassen von る allein hier nicht reicht.

Spätere Wiederaufnahme: `23:0`, `v11:work-study`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:verb-groups:0` | たべる | Gezielte Anwendungsfrage: Du möchtest かえる, zurückkehren, höflich sagen. Welche Form passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:verb-groups:1` | みる | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu みる? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:verb-groups:2` | かえる | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu かえる? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:verb-groups:3` | する | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu する? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:verb-groups:4` | くる | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu くる? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 94 ます・ません・ました

Stabile ID: `7:0`. 4 vorhandene Karten. Lernziel: Bejahung, Verneinung, Vergangenheit und die verbindende て-Form von essen auseinanderhalten.

Voraussetzungen: `v11:verb-groups`, `v11:polite-past`, `v11:inviting`.

Mit dem Stamm たべ tabe: たべます tabemasu esse/werde essen, たべません tabemasen esse nicht/werde nicht essen, たべました tabemashita habe gegessen. Zeitwörter wie あした morgen oder きのう gestern machen den Bezug deutlich. Die Höflichkeitsendung allein nennt keine Person.

たべて tabete ist die て-Form von たべる, noch kein vollständiger höflicher Aussagesatz. Bei diesem Ichidan-Verb fällt る weg, dann folgt て. Bekanntes ください macht daraus たべてください, bitte essen Sie. Die systematischen Formen anderer Verben werden später behandelt.

Vergleiche たべません mit たべませんか: Erst die Frageendung ergibt im Einladungskontext die gelernte Einladung. たべて berichtet keine Vergangenheit; dafür steht hier たべました. Sprich tabe-te und tabe-mashita verschieden; die Formen sind keine frei austauschbaren Endungen.

Abruf: Berichte, dass du gestern gegessen hast. Lade danach jemanden zum Essen ein und unterscheide beides von der て-Form.

Spätere Wiederaufnahme: `v11:polite-past`, `v11:inviting`, `23:0`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `7:0:0` | たべます | Gezielte Anwendungsfrage: Du berichtest, dass du gegessen hast. Welche höfliche Form passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `7:0:1` | たべません | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Bedeutung passt zu たべません? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `7:0:2` | たべました | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Bedeutung passt zu たべました? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `7:0:3` | たべて | Gezielte Anwendungsfrage: Welche Bedeutung hat たべて in der hier erklärten Formenübersicht? Alle 2 falschen Auswahlwerte einzeln begründet. |

## 126 Termine vereinbaren und verschieben

Stabile ID: `v11:appointments`. 5 vorhandene Karten. Lernziel: Beginn und Ende erfragen, eine Uhrzeit festlegen und einen alternativen Tag vorschlagen.

Voraussetzungen: `v11:clock-minutes`, `v11:reply-invites`, `v11:workday`.

から kara markiert bei Uhrzeiten den Beginn, まで made das Ende. なんじからですか fragt ab wann, なんじまでですか bis wann. かいぎ kaigi Besprechung und しごと shigoto Arbeit sind die bekannten Themen: かいぎはなんじからですか fragt nach dem Beginn der Besprechung.

にじにしましょう (niji ni shimashō) schlägt zwei Uhr als gemeinsame Wahl vor. Hier gehört に zu にします, sich entscheiden/festlegen. Ohne Tageshälfte ist die Uhrzeit mehrdeutig; mit ごごにじ sind 14 Uhr gemeint. きょうはむずかしいです bedeutet im Terminkontext heute passt es schlecht.

あしたでもいいですか (ashita demo ii desu ka) fragt, ob auch morgen als Alternative geht. でも bedeutet hier auch bei dieser Wahl, nicht einfach aber. Sprich mu-zu-ka-shii mit langem ii, shimashō mit langem ō. Eine Frage nach einer Alternative ist noch keine bestätigte Verschiebung.

Abruf: Erfrage Anfang und Ende eines Termins. Schlage 14 Uhr vor; frage danach, ob stattdessen morgen möglich wäre.

Spätere Wiederaufnahme: `v11:clock-minutes`, `v11:reply-invites`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:appointments:0` | なんじからですか | Gezielte Anwendungsfrage: Du kennst den Beginn der Besprechung und möchtest ihre Endzeit erfahren. Was fragst du? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:appointments:1` | なんじまでですか | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu なんじまでですか? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:appointments:2` | にじにしましょう | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu にじにしましょう? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:appointments:3` | きょうはむずかしいです | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu きょうはむずかしいです? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:appointments:4` | あしたでもいいですか | Gezielte Anwendungsfrage: Heute geht es nicht. Du fragst, ob auch morgen als Alternative möglich wäre. Was passt? Alle 2 falschen Auswahlwerte einzeln begründet. |

## 129 Eine kurze höfliche Nachricht

Stabile ID: `v11:messages`. 5 vorhandene Karten. Lernziel: Eine höfliche Nachricht in Gruß, Dank, Änderungswunsch, Antwortbitte und Abschluss gliedern.

Voraussetzungen: `v11:appointments`, `v11:wishes`, `v11:feelings`.

おつかれさまです otsukaresama desu ist eine übliche kollegiale Wendung, keine wörtliche Meldung eigener Müdigkeit. れんらく renraku Nachricht/Kontaktaufnahme + ありがとうございます ergibt den Dank für die Mitteilung. Der passende Gruß hängt von Beziehung und Anlass ab.

じかん jikan Zeit/Uhrzeit, へんこう henkō Änderung; へんこうする heißt ändern. Mit bekanntem Wunschmuster: じかんをへんこうしたいです, ich möchte die Uhrzeit ändern. へんじ henji heißt dagegen Antwort; へんじをおねがいします bittet darum, ohne den Änderungswunsch bereits als angenommen auszugeben.

では、またあした (dewa, mata ashita) schließt mit dann bis morgen. Das ist keine neue Uhrzeit. Henkō und arigatō haben lange ō, henji ein n vor ji. Nutze diese Bausteine bewusst nach Funktion; eine höfliche Nachricht braucht nicht in jedem Fall alle fünf.

Abruf: Du möchtest den Termin ändern. Wähle Änderungswunsch und Antwortbitte; welche Rückmeldung müsste kommen, bevor du den neuen Termin als vereinbart behandelst?

Spätere Wiederaufnahme: `v11:appointments`, `v11:wishes`, `v11:relative-time`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:messages:0` | おつかれさまです | Gezielte Anwendungsfrage: Du hast einen Änderungswunsch geschickt und möchtest eine Antwort erhalten. Was ergänzt du? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:messages:1` | れんらくありがとうございます | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu れんらくありがとうございます? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:messages:2` | じかんをへんこうしたいです | Gezielte Anwendungsfrage: Was ist nach じかんをへんこうしたいです bereits sicher? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:messages:3` | へんじをおねがいします | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu へんじをおねがいします? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:messages:4` | では、またあした | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu では、またあした? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 134 Dialog: etwas fürs Wochenende planen

Stabile ID: `v11:dialog-weekend`. 5 vorhandene Karten. Lernziel: Gemeinsam Tätigkeit, Tag, Uhrzeit und Treffpunkt vereinbaren und die vier Angaben getrennt bestätigen.

Voraussetzungen: `v11:inviting`, `v11:reply-invites`, `v11:appointments`, `v11:wishes`, `v11:positions`.

Wiederhole Sonntag にちようび nichiyōbi, Park こうえん kōen, Bahnhof えき eki und 前/まえ mae davor. あいます aimasu heißt sich treffen; あいましょう aimashō treffen wir uns. えきのまえで markiert den Ort der Handlung. たのしみにしています tanoshimi ni shite imasu ist die feste Wendung ich freue mich darauf, anders als gerade Spaß haben.

Vor der Offline-Szene: 週末/しゅうまつ shūmatsu Wochenende, 一緒に/いっしょに issho ni gemeinsam, 出かけませんか/でかけませんか dekakemasen ka wollen wir ausgehen/etwas unternehmen. 何をしたいですか/なにをしたいですか nani o shitai desu ka fragt nach dem Wunsch. Antworten: えいがをみたいです Film sehen, カフェにいきたいです ins Café, こうえんにいきたいです in den Park.

Die Szene bietet Samstag oder Sonntag, 10 Uhr vormittags oder 14/15 Uhr sowie Bahnhofsvorplatz oder vor dem Café. どようびがいいです wählt Samstag; ごごにじがいいです wählt 14 Uhr. 何時に会いましょうか/なんじにあいましょうか fragt nach der Treffzeit. カフェのまえはどうですか schlägt den Cafévorplatz vor; はい、いいですね stimmt dem Bahnhof zu. Im Abschluss verbindet の Tag und Uhrzeit, に markiert die Zeit, で den Ort; 楽しみです/たのしみです heißt freue mich darauf. Andere freie Vorschläge sind nicht vollständig unterstützt.

Abruf: Plane erst Film, Samstag, 10 Uhr, Bahnhof; danach Park, Sonntag, 14 Uhr, Cafévorplatz. Halte Wunsch und bestätigten Termin auseinander.

Spätere Wiederaufnahme: `v11:weekdays`, `v11:clock-minutes`, `v11:media-actions`, `v11:inviting`, `v11:appointments`, `v11:positions`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:dialog-weekend:0` | にちようび、こうえんにいきませんか | Gezielte Anwendungsfrage: Du beantwortest nur die Frage nach dem passenden Tag und wählst Samstag. Was passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:dialog-weekend:1` | いいですね、なんじですか | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu いいですね、なんじですか? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:dialog-weekend:2` | ごごにじはどうですか | Gezielte Anwendungsfrage: Für die Offline-Szene wählst du 14 Uhr. Welche Antwort passt zur Zeitfrage? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:dialog-weekend:3` | えきのまえであいましょう | Gezielte Anwendungsfrage: Du möchtest den vorgeschlagenen Bahnhof durch den Cafévorplatz ersetzen. Was antwortest du? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:dialog-weekend:4` | たのしみにしています | Erhaltene Zuordnung mit ausdrücklichem Kartenbezug: Welche Verwendung passt zu たのしみにしています? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 137 Lesetext: gestern im Park

Stabile ID: `v11:read-weekend`. 5 vorhandene Karten. Lernziel: Aus fünf Sätzen Zeitpunkt, Begleitung, Ziel, Wetter und Tätigkeit eines vergangenen Ausflugs entnehmen.

Voraussetzungen: `v11:dialog-weekend`, `v11:media-actions`, `v11:adjective-time`, `v11:relative-time`.

Wiederholung: きのう gestern + やすみでした hatte frei; ともだちと mit einem Freund, こうえんに in den Park, いきました bin gegangen. と markiert die Begleitung, に das Ziel. Lese zuerst das Zeitwort und das Satzende; die Erzählung berichtet über gestern.

てんきはよかったです bedeutet das Wetter war gut, mit der bekannten Sonderform von いい. Neu im Fotobeispiel: たくさん takusan = viel/viele. しゃしんをたくさんとりました heißt habe viele Fotos gemacht, ohne genaue Anzahl. とてもたのしかったです (totemo tanoshikatta desu) verbindet sehr mit hat Spaß gemacht.

Die Vorlage bleibt in den Leseaufgaben sichtbar; ihre deutsche Bedeutung erscheint bei bewusster Hilfe oder nach der Antwort. Behaupte nichts, was im Text fehlt: Ein Freund nennt keinen Namen, viele Fotos keine Uhrzeit. In kinō und kōen bleibt ō lang; katta enthält eine kurze Pause.

Abruf: Erzähle den Ausflug in drei deutschen Angaben nach: wann, mit wem und wohin. Welche genaue Uhrzeit kannst du aus dem Text nicht entnehmen?

Spätere Wiederaufnahme: `v11:relative-time`, `v11:media-actions`, `v11:adjective-time`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:read-weekend:0` | きのうはやすみでした | Gezielte Anwendungsfrage: Im Text steht きのうはやすみでした. Wann hatte die Person frei? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:read-weekend:1` | ともだちとこうえんにいきました | Erhaltene Leseverständnisfrage: Mit wem und wohin ging die Person? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:read-weekend:2` | てんきはよかったです | Erhaltene Leseverständnisfrage: Wie war das Wetter? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:read-weekend:3` | しゃしんをたくさんとりました | Gezielte Anwendungsfrage: Du liest しゃしんをたくさんとりました. Welche Aussage ist belegt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:read-weekend:4` | とてもたのしかったです | Erhaltene Leseverständnisfrage: Wie beurteilt die Person den Ausflug? Alle 3 falschen Auswahlwerte einzeln begründet. |

## 138 Lesetext: ein Ausflug für morgen

Stabile ID: `v11:read-plan`. 5 vorhandene Karten. Lernziel: In einem Ausflugsplan Abfahrt, Treffort, Wunsch und wetterabhängige Alternative unterscheiden.

Voraussetzungen: `v11:dialog-weekend`, `v11:weather-words`, `v11:station`, `v11:hotel`, `v11:wishes`, `31:0`.

きょうと Kyōto Kyoto ist der Ortsname, nicht きょう kyō heute. あした morgen macht いきます zum Plan. でんしゃ Zug + くじに um 9 Uhr + でます demasu fährt ab: Hier ist das Subjekt ein Zug. えきで Bahnhof als Treffort und ともだちに die getroffene Person stehen vor あいます aimasu treffen.

Neu: おてら otera Tempel, やすみます yasumimasu ausruhen. みます sehen → みたいです möchte sehen wiederholt たい. あめだったら ame dattara = falls es regnet: Nomen あめ plus だったら bezeichnet hier die Bedingung für die folgende Handlung. ホテルでやすみます nennt den Plan bei Regen, keine Aussage, dass Regen sicher kommt.

Lies zuerst den Grundplan, dann die bedingte Alternative. Die 9-Uhr-Abfahrt ist nicht automatisch die vorherige Treffzeit am Bahnhof. Kyoto hat zwei Vokalteile kyō-to; dattara eine Pause vor t. Neue Wörter sind in dieser Hilfe erklärt, die allgemeine Bedingungsbildung wird nicht aus diesem einen Beispiel vorausgesetzt.

Abruf: Was wird bei Regen anders? Nenne die Abfahrtszeit und erkläre, welche genaue Treffzeit im Text offenbleibt.

Spätere Wiederaufnahme: `v11:clock-hours`, `v11:weather-words`, `v11:wishes`, `v11:station`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:read-plan:0` | あしたきょうとにいきます | Gezielte Anwendungsfrage: Du liest あしたきょうとにいきます. Welche Aussage passt? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:read-plan:1` | でんしゃはくじにでます | Erhaltene Leseverständnisfrage: Wann fährt der Zug ab? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:read-plan:2` | えきでともだちにあいます | Erhaltene Leseverständnisfrage: Wo trifft die Person ihren Freund? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:read-plan:3` | おてらをみたいです | Erhaltene Leseverständnisfrage: Was möchte die Person besichtigen? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:read-plan:4` | あめだったら、ホテルでやすみます | Gezielte Anwendungsfrage: Der Satz あめだったら、ホテルでやすみます nennt welchen Plan? Alle 2 falschen Auswahlwerte einzeln begründet. |

## 139 Lesetext: eine Verabredung ändern

Stabile ID: `v11:read-message`. 5 vorhandene Karten. Lernziel: Grund, neuen Tag, mögliche Tageshälfte und offene Rückfrage einer Terminänderung herauslesen.

Voraussetzungen: `v11:messages`, `v11:reply-invites`, `v11:dialog-weekend`, `31:0`.

Die Anrede さくらさん、こんにちは richtet sich an Sakura. あしたはしごとがあります heißt wörtlich morgen habe ich Arbeit, hier als Grund für das Terminproblem. Das ist keine allgemeine Grammatikform für müssen. にちようびにあいませんか fragt mit dem bekannten Einladungsmuster nach einem Treffen am Sonntag.

ごごならだいじょうぶです (gogo nara daijōbu desu) sagt wenn es am Nachmittag ist, passt es. なら nimmt eine mögliche Wahl als Bedingung auf; es vereinbart keine genaue Uhrzeit. つごう tsugō bedeutet Verfügbarkeit/persönliche Passung; つごうはどうですか fragt, wie es der anderen Person passt.

Die Nachricht schlägt eine Änderung vor, zeigt aber keine Antwort von Sakura. Sonntag ist daher noch nicht beiderseits bestätigt. ごご ist Nachmittag, nicht morgen; だいじょうぶ bestätigt hier die eigene Möglichkeit. Tsugō und daijōbu haben langes ō. Lies die Aussagegrenze ebenso sorgfältig wie die Wörter.

Abruf: Nenne den Grund für die Änderung und den vorgeschlagenen Tag. Welche Antwort fehlt noch, bevor das Treffen feststeht?

Spätere Wiederaufnahme: `v11:messages`, `v11:weekdays`, `v11:clock-minutes`, `v11:reply-invites`.

| Stabile Karten-ID | Erhaltener Zieltext | Änderung der Anwendung / Rückmeldung |
| --- | --- | --- |
| `v11:read-message:0` | さくらさん、こんにちは | Gezielte Anwendungsfrage: Im Text steht さくらさん、こんにちは. Welche Funktion hat dieser Anfang? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:read-message:1` | あしたはしごとがあります | Erhaltene Leseverständnisfrage: Warum ist morgen schwierig? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:read-message:2` | にちようびにあいませんか | Erhaltene Leseverständnisfrage: Welcher Tag wird für das Treffen vorgeschlagen? Alle 3 falschen Auswahlwerte einzeln begründet. |
| `v11:read-message:3` | ごごならだいじょうぶです | Gezielte Anwendungsfrage: Die Antwort lautet ごごならだいじょうぶです. Was erfährst du? Alle 2 falschen Auswahlwerte einzeln begründet. |
| `v11:read-message:4` | つごうはどうですか | Erhaltene Leseverständnisfrage: Wonach wird am Ende gefragt? Alle 3 falschen Auswahlwerte einzeln begründet. |

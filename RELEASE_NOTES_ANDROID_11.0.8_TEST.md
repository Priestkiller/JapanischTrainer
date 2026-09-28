# JapanischTrainer Android 11.0.8 Testversion

Android 11.0.8-android.1-test, VersionCode 11000801. Öffentliche Testversion;
kein reguläres Latest-Update. Windows-Testversion 11.0.7 und stabile Version
11.0.4 bleiben bestehen.

- Lernansichten nach den Handyreferenzen: dunkler Japan-Hintergrund, klare blaue
  Karten, großer grüner Prüf-/Weiter-Button und rosa Mikrofonaktion. Fortschritt
  und gewählter Lehrer bleiben erkennbar, lange Inhalte scrollen separat.
- Kurze und leise Aufnahmen werden gezielt aufbereitet. Mikrofonpegel, Laufzeit,
  automatisches Ende nach einer Kana-Sprechpause und eigene Aufnahme zum Anhören.
- Zusätzliche kleine lokale Sprachaktivitätsprüfung. Unsichere Kana-Transkripte
  zählen nicht als Lernfehler; nur die ausdrücklich bestätigte Selbstprüfung
  kann den Schritt abschließen. Keine automatische Freigabe durch Stille.
- 150 Lektionen, 680 Karten, 156 Zusatzaufgaben, Lernstände und vorhandenes
  Sprachpaket bleiben erhalten. Kein neuer Download der großen Modelle nötig.

Die kontrollierten Tests verwenden synthetische Sprache. Bei 40 sehr leisen
Kana-Signalen passen 25 statt zuvor null Transkripte; bei 40 normalen 29 statt
26. Drei normale Signale regressieren. Das ist keine zugesicherte Erkennungsrate
für Menschen: einzelne Kana können weiterhin falsch verschriftlicht werden.

Installation: In der vorhandenen Android-App Einstellungen → App-Updates →
**Testversion suchen**. Anschließend Download/Installation bewusst bestätigen.
Alternativ die APK dieses Releases über die bestehende App installieren.
Vorher kann der Lernstand exportiert werden; die App nicht deinstallieren.
Die reguläre Updatesuche bietet diese Ausgabe nicht an.

Automatische Prüfungen und Modellvergleich stehen im beigefügten Prüfbericht;
Geräteversuche in der S24-Ultra-Prüfliste. **Offen:** echte S24-Ultra-Mikrofon-
und Hörtests, Anfänger-Erprobung sowie menschliche Japanisch-Fachprüfung.
Eine spätere stabile Veröffentlichung benötigt eine ausdrückliche Freigabe.

Programmquellen: GPL-3.0-or-later. Bibliotheks-/Modellbedingungen sind in Quellen
und App enthalten, einschließlich MIT-Lizenz für Silero VAD. Mikrofonaufnahmen
bleiben lokal im Arbeitsspeicher und sind nicht Bestandteil dieses Releases.

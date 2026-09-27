# Öffentliche Kontrolle der Ausgabe 11.0.4

Am 27.09.2026 nach ausdrücklicher Nutzerfreigabe veröffentlicht:

- [Windows 11.0.4](https://github.com/Priestkiller/JapanischTrainer/releases/tag/v11.0.4), als Hauptrelease für den bisherigen Update-Button.
- [Android 11.0.4-android.1](https://github.com/Priestkiller/JapanischTrainer/releases/tag/android-v11.0.4-1), Code 11000401, im eigenen Android-Kanal.

Beide enthalten das zweite Inhaltspaket und den neuen Button **Testversion suchen**. Einmal über **Nach Updates suchen** aktualisieren; künftig lassen sich neuere Testversionen über den zusätzlichen Button wählen. Derzeit gibt es keine höhere Testausgabe, daher meldet dieser Kanal das ausdrücklich.

## Öffentliche Nachweise

Die ursprünglichen 18 Release-Dateien wurden vollständig gegen die lokalen Dateigrößen und SHA-256 geprüft. Danach wurden ohne GitHub-Anmeldung die echten öffentlichen Quellen verwendet:

- Windows `check_update`: 11.0.2 und 11.0.3 erkennen 11.0.4; 11.0.4 erkennt korrekt kein neueres reguläres Update und kein neueres Testpaket. Die bestehende Ed25519-Signatur ist gültig.
- Windows-Update tatsächlich heruntergeladen: 134016106 Bytes, SHA-256 `4131ec7e8cc588cfc3cb2142c60d943d9025f35e8c802f2e2cd47fa2ef6f3719`.
- Android-Auswahl aus den öffentlichen Releases: Code 11000401 ist höher als 11000201 und die lokale Testausgabe 11000301.
- Android-APK tatsächlich heruntergeladen: 61805300 Bytes, SHA-256 `30555077a046b0ffd973739639327b900bc47e580be911b5e820ce5c3ae6da9b`.
- Der neueste GitHub-Hauptrelease ist `v11.0.4`; Android verdrängt den Windows-Kanal nicht.

Die fünf nativen Android-Tests im [GitHub-Lauf 36338848666](https://github.com/Priestkiller/JapanischTrainer/actions/runs/36338848666) sind mit null Fehlern und null übersprungenen Tests bestanden. Weitere technische und fachliche Grenzen stehen im [Prüfbericht](TESTBERICHT_11.0.4.md). Dieser Veröffentlichungsnachweis ergänzt dessen vor der Freischaltung erstellten Stand.

Der Programmstand ist `318f54f55529a77f1f2213fab76ada9990dbd8a3`. Die veröffentlichten GPL-Quellarchive stammen aus `9375666cc53d96125d1596a09d711e209a9069e0` und ergänzen ausschließlich Dokumentation. Die separat veröffentlichten Nachweise ändern keine Programmdateien. Persönliche Lernstände und Schlüssel sind ausgeschlossen.

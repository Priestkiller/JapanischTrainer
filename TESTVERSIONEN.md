# Reguläre Updates und Testversionen

Ab 11.0.4 besitzen Windows und Android in ihrem Update-Bereich die zusätzliche Schaltfläche **Testversion suchen**. Sie prüft nur öffentlich freigegebene Testausgaben. Der normale Button bleibt im regulären Kanal. Es gibt keinen automatischen Wechsel und keinen dauerhaft gespeicherten Testmodus.

Wer noch 11.0.2 oder die lokale 11.0.3 verwendet, benötigt zuerst das reguläre Update auf 11.0.4, um diesen Button zu erhalten. Android-Updates über die vorhandene App installieren, ohne sie vorher zu deinstallieren.

## Veröffentlichung weiterer Testausgaben

Jeder Programmstand erhält eine neue, höhere Versionsnummer beziehungsweise einen höheren Android-VersionCode. Nach einer installierten Testversion kann eine reguläre Ausgabe nur angeboten werden, wenn sie eine höhere Nummer besitzt; es erfolgt kein Downgrade mit alten Programmdaten.

- Windows: GitHub-Prerelease mit Tag `windows-test-v11.0.5` (Beispiel), vollständigem `update.json` mit bestehender Ed25519-Signatur, dem zugehörigen Update-ZIP, Setup, Quellen, Prüfsummen und Nachweisen. Das signierte ZIP-Ziel muss im selben Release liegen. Nicht als Latest markieren.
- Android: GitHub-Prerelease mit Tag `android-test-v11.0.5-1` (Beispiel), `android-update.json`, gleich signierter APK, Quellen, Prüfsummen und Nachweisen. APK-Ziel und Metadaten müssen zum selben Release gehören. Nicht als Latest markieren.
- Reguläres Windows bleibt `v…` und Latest; reguläres Android bleibt `android-v…`. Ältere Android-Apps beachten weiterhin ausschließlich diese regulären Android-Tags und sehen die neuen Test-Tags nicht.

Die Suche berücksichtigt die 30 zuletzt gelisteten Veröffentlichungen. Ohne neuere passende Testausgabe erscheint „Keine neuere Testversion verfügbar“. Netzwerkfehler werden separat angezeigt. Vor jedem Kanalwechsel werden Angebot und Installationsbereitschaft zurückgesetzt.

Die gleiche Android-Signatur und die Windows-Update-Signatur erhalten; niemals neue Herausgeberschlüssel für Folgeversionen erzeugen. Keine privaten Lernstände, Aufnahmen, Zugangsdaten oder Schlüssel in Releases aufnehmen.

## Testversion 11 0 10

Windows 11.0.10 und Android 11.0.10-android.1-test (11001001) ergänzen die ausdrücklich aufrufbare Auswahlhilfe nach drei erfolglosen Aufnahmen und verständliche Aufgabenansichten. Lernstände und vorhandene Signierschlüssel bleiben erhalten. [Prüfbericht](TESTBERICHT_11.0.10.md) und [Geräteprüfliste](GERAETEPRUEFUNG_11.0.10.md) unterscheiden Softwareprüfungen, synthetische Modelltests und offene menschliche Erprobung. Die frühere stabile 11.0.4 bleibt unverändert; eine Übernahme in den stabilen Kanal braucht eine neue Freigabe.

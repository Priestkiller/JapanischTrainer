Die großen Modellgewichte sind nicht in dieser ZIP enthalten.

INSTALLIEREN.bat / build_windows.ps1 übernehmen die vorhandenen Modelle aus:
  %LOCALAPPDATA%\Programs\JapanischTrainer\models

Fehlende Modelle werden mit download_models.ps1 aus denselben Releases wie
bei V6 geladen. Erwartete Ordner:
  supertonic
  parakeet-ja
  sensevoice

Nach dem Build liegen sie im installierten Programmordner unter models.
Die Sprachengine verwendet diese lokalen Dateien ohne Cloud-API.
Die bloße Existenz der Dateien ist noch kein Test der Sprachqualität.

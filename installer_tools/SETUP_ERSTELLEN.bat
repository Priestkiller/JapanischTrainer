@echo off
setlocal
cd /d "%~dp0"
set "PSEXE=%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe"
if exist "%SystemRoot%\Sysnative\WindowsPowerShell\v1.0\powershell.exe" set "PSEXE=%SystemRoot%\Sysnative\WindowsPowerShell\v1.0\powershell.exe"
echo JapanischTrainer - vorhandene V11 in einen Offline-Installer verpacken
echo.
"%PSEXE%" -NoLogo -NoProfile -STA -ExecutionPolicy Bypass -File "%~dp0installer\Build-Installer.ps1"
set "RESULT=%ERRORLEVEL%"
echo.
if not "%RESULT%"=="0" echo Kein fertiger Installer erstellt. Bitte die Fehlermeldung und das Protokoll pruefen.
pause
exit /b %RESULT%

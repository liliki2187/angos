@echo off
setlocal

set "ROOT=%~dp0.."
set "HUB=%ROOT%\design\htmls\prototype-hub.html"

if not exist "%HUB%" (
  echo Prototype hub not found:
  echo %HUB%
  exit /b 1
)

start "" "%HUB%"

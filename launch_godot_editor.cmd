@echo off
setlocal
set "ROOT=%~dp0"
set "GODOT=%ROOT%tools\godot\4.6.3-stable\Godot_v4.6.3-stable_win64.exe"
if not exist "%GODOT%" (
  echo Godot executable not found: %GODOT%
  exit /b 1
)
start "" "%GODOT%" --path "%ROOT%gd_project"

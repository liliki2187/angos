@echo off
setlocal

set "REPO_ROOT=%~dp0"
if not exist "%REPO_ROOT%gd_project\project.godot" (
  echo Project root not found: %REPO_ROOT%gd_project\project.godot
  pause
  exit /b 1
)

set "GODOT_DIR=%REPO_ROOT%tools\godot\4.6.2-stable"
set "GODOT_EXE=%GODOT_DIR%\Godot_v4.6.2-stable_win64.exe"
set "GODOT_ZIP=%REPO_ROOT%tmp\Godot_v4.6.2-stable_win64.exe.zip"
set "PROJECT_DIR=%REPO_ROOT%gd_project"

if not exist "%GODOT_EXE%" (
  if not exist "%GODOT_ZIP%" (
    echo Portable Godot zip not found.
    echo Expected: %GODOT_ZIP%
    echo Please wait for the download to finish, then run this file again.
    pause
    exit /b 1
  )

  echo Extracting portable Godot...
  powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "try { New-Item -ItemType Directory -Force -Path '%GODOT_DIR%' | Out-Null; Expand-Archive -LiteralPath '%GODOT_ZIP%' -DestinationPath '%GODOT_DIR%' -Force; exit 0 } catch { Write-Host $_.Exception.Message; exit 1 }"
  if errorlevel 1 (
    echo Failed to extract portable Godot.
    echo The zip may still be downloading or may be incomplete.
    pause
    exit /b 1
  )
)

echo Launching Angus demo...
start "" "%GODOT_EXE%" --path "%PROJECT_DIR%"
exit /b 0

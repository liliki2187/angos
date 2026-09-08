# Godot Agent Smoke

This is the Angus Godot error check for Codex work.

Plain meaning: after a Codex change touches Godot, run a small health check before saying the work is done.

If this health check fails, classify the failure with [`godot-debug-skill-v0.md`](./godot-debug-skill-v0.md) before fixing it. That notebook translates common Godot errors into plain language and records the narrow repair path.

It has two layers:

1. `gda script validate`: checks whether GDScript files can be parsed and compiled.
2. Godot headless smoke: starts the real Angus weekly-run scene without opening a window and checks that the scene can run through a tiny real path.

## Why This Exists

Angus has two common Godot failure types.

The first type is a script error. Examples: a missing colon, a broken function signature, bad indentation, or a GDScript parse error. `gda script validate` catches this and returns JSON such as `valid: false`.

The second type is a runtime scene error. Examples: a node was renamed in `.tscn`, but a script still reads `$RootMargin/RootVBox/PhaseHost`; an autoload or phase scene fails during `_ready`; a method is called on `null`. These can pass script validation, so they need a real Godot headless run.

## Command

Run:

```powershell
.\scripts\run_godot_agent_smoke.ps1
```

If Windows blocks `.ps1` execution policy, run the same script this way:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\scripts\run_godot_agent_smoke.ps1
```

If `gda` is not installed globally, the script uses `uvx --from gda gda`. The first run may need network access to fetch `gda`; later runs can use the existing uv cache.

In restricted Codex runs, this usually works after the cache exists:

```powershell
.\scripts\run_godot_agent_smoke.ps1 -GdaOffline -PythonPath C:\Python314\python.exe
```

## What It Checks

The script validates the key entry scripts:

```text
gd_project/scenes/gameplay/weekly_run/WeeklyRunGame.gd
gd_project/tests/gda_angus_weekly_run_smoke.gd
```

You can ask it to validate extra scripts:

```powershell
.\scripts\run_godot_agent_smoke.ps1 -ExtraValidateScript scenes/gameplay/weekly_run/phases/SomeChangedScript.gd
```

Then it runs:

```text
res://tests/gda_angus_weekly_run_smoke.gd
```

That smoke test loads the real `WeeklyRunGame.tscn`, checks key nodes, enters explore, selects the initial North America region, opens a real dispatch node, and toggles one staff member.

Why not validate every `.gd` file by default? Some Godot `class_name` scripts are registered globally by the project, and single-file validation can report false positives such as a class hiding itself. The headless smoke is the safer default for those runtime-loaded scripts.

## When To Run

Run this before completion if a task changes any of these:

- `gd_project/scenes/**/*.gd`
- `gd_project/scenes/**/*.tscn`
- `gd_project/project.godot`
- weekly-run phase scenes or scripts
- world map, region task, dispatch, editorial, summary, or phase switching
- node names, scene hierarchy, autoloads, preload paths, or `$Node/Path` references

You usually do not need it for pure Markdown, AI daily reports, HTML-only prototypes, or visual-only planning that does not touch Godot files.

## Pass Rule

Passing means both are true:

- every `gda script validate` result has `valid: true`
- Godot headless exits with code `0`

Important: `gda script validate` may return process exit code `0` even when the script is invalid. Always parse the JSON `valid` field.

## What It Does Not Prove

This is a runtime health check, not a visual-quality review.

It proves the weekly-run Godot path can start and survive a tiny real interaction path. It does not prove final UI beauty, assetized UI quality, all gameplay balance, all screenshots, all state combinations, or Steam-facing product quality.

It also does not prove that every Godot GUI executable or editor launch is stable. A Windows application error such as `Godot_v4.6.2-stable_win64.exe - 应用程序错误` is a native process / GUI launch failure, not the same class as a GDScript validation failure. Classify that with [`godot-debug-skill-v0.md`](./godot-debug-skill-v0.md) card `006` and verify the exact executable separately.

Use this command for that separate GUI / exact executable check:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\scripts\run_godot_gui_startup_check.ps1
```

To test the exact executable from a crash dialog, pass it explicitly:

```powershell
powershell.exe -ExecutionPolicy Bypass -File .\scripts\run_godot_gui_startup_check.ps1 -GodotPath "D:\angos\tools\godot\4.6.2-stable\Godot_v4.6.2-stable_win64.exe"
```

Use screenshots, layout tests, UX / UI review, and assetized UI gates for those. For the smallest runtime screenshot pass after this smoke, run [`godot-visual-feedback-smoke.md`](./godot-visual-feedback-smoke.md).

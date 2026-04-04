# Godot Project

`gd_project/` is the formal Angus runtime development root.

Open `project.godot` in Godot 4.3 and treat everything under this directory as project-owned runtime content:

- `scenes/`: gameplay, UI, dev scenes, and scene-owned scripts
- `Assets/`: runtime assets and imported source art used by the project
- `addons/`: project-local Godot addons
- `export_presets.cfg`: export configuration for build automation

If you are changing game behavior, UI, or runtime assets, start here first.

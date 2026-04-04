# Directory Ownership

This is the practical ownership map for day-to-day work.

- Design: `design/gdd/`, `design/systems/`, `specs/`
- Runtime programming: `gd_project/scenes/`, `gd_project/Assets/`, `docs/architecture/`, `docs/`
- Engine tooling: `scripts/`, `.github/workflows/`
- UI and import pipeline: `design/ui/` when it exists, `gd_project/Assets/ui/`, `gd_project/scenes/ui/`, `docs/tools/psd-ui-import.md`
- Production coordination: `production/`
- Reference-only prototypes: `design/prototypes/html/`, `prototype/`

Rules:

- Do not treat reference prototypes as runtime authority.
- Do not add new long-lived source files to the repo root unless they are true root-level project files.
- New implementation work should point back to a GDD, spec, or ADR.

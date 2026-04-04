# Directory Ownership

This is the practical ownership map for day-to-day work.

- Design: `design/gdd/`, `design/systems/`, `specs/`
- Runtime programming: `scenes/`, `scripts/`, `docs/architecture/`, `docs/technical/`
- UI and import pipeline: `design/ui/` when it exists, `Assets/ui/`, `scenes/ui/`, `docs/tools/`
- Production coordination: `production/`
- Reference-only prototypes: `design/prototypes/html/`, `prototype/`

Rules:

- Do not treat reference prototypes as runtime authority.
- Do not add new long-lived source files to the repo root unless they are true root-level project files.
- New implementation work should point back to a GDD, spec, or ADR.

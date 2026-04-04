# Git Collaboration

This is the authority document for day-to-day Git collaboration guidance in this repository.

## First Rule

Do not assume remote names or URLs from memory. Always inspect the current clone first:

```powershell
git remote -v
```

Different local clones may not yet be normalized the same way.

## Team Policy

- Keep the actively used hosted repositories in sync when that mirror setup is configured for the clone.
- Do not push based on outdated instructions copied from older docs.
- If the clone has only one configured remote, do not silently invent or rename remotes during unrelated work.

## Preferred Normalized Layout

When the clone is configured for the dual-remote mirror workflow, the preferred naming is:

- `origin`: primary presentation repo
- `daydreamer`: mirrored historical repo

If that layout is missing, fix it deliberately as a Git task, not as incidental cleanup during feature work.

## Helper Script

`scripts/git/sync-both-remotes.ps1` is intended for the normalized dual-remote setup.

Only use it after `git remote -v` confirms that the current clone matches the expected mirror configuration.

## Documentation Rule

Other docs should link here instead of restating Git push policy in slightly different words.

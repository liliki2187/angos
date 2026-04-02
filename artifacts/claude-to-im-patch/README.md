# claude-to-im patch draft

This folder contains a workspace-local patch draft for the installed
`claude-to-im` skill.

## What it changes

- Replays recent stored IM chat history into the prompt when the provider
  cannot resume an existing SDK session/thread.
- Converts stored `<!--files:...-->` message metadata into readable text when
  rebuilding context.
- Preserves non-image attachment context by appending structured file metadata
  to the prompt instead of silently dropping file/audio/video/media messages.
- Keeps existing image support unchanged for Claude/Codex multimodal flows.

## Important limitation

This patch does **not** add true video/audio understanding by itself.
It only makes the model aware that those files existed by passing:

- file name
- MIME type
- file size

To truly understand video/audio contents, the bridge still needs an extra
pipeline such as:

- video keyframe extraction + vision summary
- audio ASR transcription
- document parsing / OCR

## Why this is not live-installed

The installed skill lives under:

- `C:\Users\guanmx\.codex\skills\claude-to-im`

That location is outside the writable roots of this coding session, so the
patch was prepared in the project workspace instead of being applied in place.

## Files

- `src/llm-provider.ts`
- `src/codex-provider.ts`
- `diff/llm-provider.patch`
- `diff/codex-provider.patch`

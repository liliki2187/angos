---
name: reply-image-context
description: Use local images that were downloaded from a replied IM message by the `claude-to-im` bridge, or from any IM task where the replied image is already surfaced as a local attachment. Trigger when the user refers to "this image", "the image I replied to", "the picture in my reply", or asks to analyze, redraw, annotate, OCR, recreate, or send an image that came from a replied message instead of a direct attachment.
---

# Reply Image Context

Use the replied-message image files already attached to the current task. In the current Angus bridge, this is automatically populated for Feishu reply images. Do not ask for a re-upload first unless no local image is available.

## Workflow

1. Inspect the current task attachments first.
- Treat files from the replied IM message as the primary image input when the prompt refers to "this image", "that image", or "the image in my reply".
- If multiple images are attached, summarize the candidates briefly and ask a disambiguation question only when the target is unclear.

2. Preserve reply semantics.
- Assume the replied image is the subject of the request unless the current message also includes a newer direct attachment that clearly supersedes it.
- Use any appended `[Reply context]` text as supporting metadata, not as a substitute for actually inspecting the image.

3. Fall back cleanly.
- If the prompt clearly refers to a replied image but there is no local image attachment, say that the bridge did not surface the replied image and ask the user to resend it or provide an absolute local path.
- Do not claim to have seen the image from text alone.

4. Continue with the requested task.
- Once the local image is available, perform the real work directly: analysis, redraw, wireframe extraction, annotation, forwarding, or other requested image handling.
- When the user wants the result sent to Feishu, use `claude-to-im`'s Feishu send scripts.

import { resolvePreferredWindowsShellPath } from './windows-shell.js';

const WINDOWS_BRIDGE_PROMPT_MARKERS = [
  'Windows bridge sessions must use PowerShell 7 syntax by default.',
  'Windows bridge sessions must treat PowerShell as the execution shell.',
  'When an IM user asks to generate game or project image assets, treat the request as a project-local image generation task.',
];

const WINDOWS_POWERSHELL_SYSTEM_PROMPT = [
  'Windows bridge sessions must treat PowerShell as the execution shell.',
  'Do not use cmd.exe or batch syntax unless the user explicitly asks for cmd, batch files, or .bat/.cmd commands.',
  'Prefer PowerShell-native commands, quoting, escaping, and script conventions when proposing or executing commands.',
  'Do not claim the environment is cmd.exe unless you have concrete evidence from an executed command.',
].join(' ');

export const BRIDGE_IMAGE_GENERATION_SYSTEM_PROMPT = [
  'When an IM user asks to generate game or project image assets, treat the request as a project-local image generation task.',
  'Prefer the workspace-local openrouter-image-gen skill when available.',
  'The built-in image_gen capability is a conversation tool, not a shell command.',
  'Bridge-launched Codex SDK/CLI sessions enable Codex feature image_generation by default so the session can use the native image generation tool when the runtime exposes it.',
  'If image_gen is still unavailable, report that the current bridge session cannot complete the image generation request.',
  'For opaque images, concepts, posters, UI banners, portraits, environments, textures, and legacy nano banana wording: use built-in $imagegen only if the actual tool list exposes image_gen; otherwise fail directly and do not run OpenRouter as a fallback.',
  'Normal opaque built-in $imagegen requests do not require OpenRouter config. OpenRouter must not be used as an opaque fallback when $imagegen is unavailable.',
  'Save project-bound generated outputs under image_gen/YYYY-MM-DD/ with sidecar metadata when the skill requires it, then report the saved paths.',
  'For Feishu image delivery, include every generated image path in the final answer; the bridge will auto-upload image_gen/... and bridge generated_images/... paths referenced in that final answer. Do not require a second user turn just to send generated images.',
].join(' ');

function stripManagedWindowsPrompt(systemPrompt?: string): string | undefined {
  const trimmed = systemPrompt?.trim();
  if (!trimmed) {
    return undefined;
  }

  const markerIndex = WINDOWS_BRIDGE_PROMPT_MARKERS
    .map((marker) => trimmed.indexOf(marker))
    .filter((index) => index >= 0)
    .sort((left, right) => left - right)[0];

  if (markerIndex === undefined) {
    return trimmed;
  }

  return trimmed.slice(0, markerIndex).trim() || undefined;
}

export function resolveBridgeSystemPrompt(systemPrompt?: string): string | undefined {
  const parts: string[] = [];
  const trimmed = stripManagedWindowsPrompt(systemPrompt);

  if (trimmed) {
    parts.push(trimmed);
  }

  if (process.platform === 'win32') {
    const shellPath = resolvePreferredWindowsShellPath();
    const sandboxMode = process.env.CTI_CODEX_SANDBOX_MODE?.trim();
    const networkAccess = process.env.CTI_CODEX_NETWORK_ACCESS?.trim().toLowerCase();
    const environmentHints = [
      shellPath ? `Default shell executable: ${shellPath}.` : undefined,
      sandboxMode ? `Sandbox mode: ${sandboxMode}.` : undefined,
      networkAccess === 'true' ? 'Network access is enabled.' : undefined,
      networkAccess === 'false' ? 'Network access is disabled.' : undefined,
    ].filter(Boolean);
    parts.push(WINDOWS_POWERSHELL_SYSTEM_PROMPT);
    if (environmentHints.length > 0) {
      parts.push(environmentHints.join(' '));
    }
  }

  parts.push(BRIDGE_IMAGE_GENERATION_SYSTEM_PROMPT);

  return parts.length > 0 ? parts.join('\n\n') : undefined;
}

export function prependSystemPrompt(promptText: string, systemPrompt?: string): string {
  const effectiveSystemPrompt = resolveBridgeSystemPrompt(systemPrompt);
  if (!effectiveSystemPrompt) {
    return promptText;
  }

  return ['System instructions:', effectiveSystemPrompt, promptText.trim()]
    .filter(Boolean)
    .join('\n\n');
}

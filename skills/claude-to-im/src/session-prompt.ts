import { resolvePreferredWindowsShellPath } from './windows-shell.js';

const WINDOWS_BRIDGE_PROMPT_MARKERS = [
  'Windows bridge sessions must use PowerShell 7 syntax by default.',
  'Windows bridge sessions must treat PowerShell as the execution shell.',
];

const WINDOWS_POWERSHELL_SYSTEM_PROMPT = [
  'Windows bridge sessions must treat PowerShell as the execution shell.',
  'Do not use cmd.exe or batch syntax unless the user explicitly asks for cmd, batch files, or .bat/.cmd commands.',
  'Prefer PowerShell-native commands, quoting, escaping, and script conventions when proposing or executing commands.',
  'Do not claim the environment is cmd.exe unless you have concrete evidence from an executed command.',
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

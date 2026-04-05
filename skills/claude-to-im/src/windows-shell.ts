import fs from 'node:fs';
import path from 'node:path';

const DEFAULT_PWSH_PATH = path.join('C:', 'Program Files', 'PowerShell', '7', 'pwsh.exe');
const DEFAULT_PWSH_PREVIEW_PATH = path.join('C:', 'Program Files', 'PowerShell', '7-preview', 'pwsh.exe');

function isExistingPath(value: string | undefined): value is string {
  return !!value && fs.existsSync(value);
}

export function resolvePreferredWindowsShellPath(
  env: NodeJS.ProcessEnv = process.env,
): string | undefined {
  if (process.platform !== 'win32') {
    return undefined;
  }

  const explicitCandidates = [
    env.CTI_CODEX_WINDOWS_SHELL,
    env.PWSH_PATH,
    env.PWSH,
    env.POWERSHELL,
  ]
    .map((value) => value?.trim())
    .filter((value): value is string => !!value);
  if (explicitCandidates.length > 0) {
    return explicitCandidates[0];
  }

  const localAppData = env.LOCALAPPDATA || env.LocalAppData;
  const systemRoot = env.SYSTEMROOT || env.SystemRoot || path.join('C:', 'Windows');
  const candidates = [
    localAppData
      ? path.join(localAppData, 'Microsoft', 'WindowsApps', 'pwsh.exe')
      : undefined,
    DEFAULT_PWSH_PATH,
    DEFAULT_PWSH_PREVIEW_PATH,
    path.join(systemRoot, 'System32', 'WindowsPowerShell', 'v1.0', 'powershell.exe'),
  ];

  return candidates.find(isExistingPath);
}

export function prependPathEntry(existingPath: string | undefined, entry: string): string {
  const current = existingPath || '';
  const segments = current
    .split(';')
    .map((part) => part.trim())
    .filter(Boolean);

  if (segments.some((part) => part.toLowerCase() === entry.toLowerCase())) {
    return current || entry;
  }

  return [entry, ...segments].join(';');
}

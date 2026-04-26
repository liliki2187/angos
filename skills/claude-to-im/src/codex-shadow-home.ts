import fs from 'node:fs';
import path from 'node:path';

import { CTI_HOME } from './config.js';
import { ensureDir } from './file-utils.js';

const AUTH_FILE_NAME = 'auth.json';
const DEFAULT_SHADOW_HOME_DIR = path.join(CTI_HOME, 'codex-home');

export function resolveCodexHomeMode(
  env: NodeJS.ProcessEnv = process.env,
): 'inherit' | 'shadow' {
  const raw = env.CTI_CODEX_HOME_MODE?.trim().toLowerCase();
  if (raw === 'inherit') {
    return 'inherit';
  }
  return 'shadow';
}

export function resolveShadowCodexHome(
  env: NodeJS.ProcessEnv = process.env,
): string {
  const override = env.CTI_CODEX_SHADOW_HOME?.trim();
  if (override) {
    return path.resolve(override);
  }
  return DEFAULT_SHADOW_HOME_DIR;
}

export function resolveSourceCodexHome(
  env: NodeJS.ProcessEnv = process.env,
): string | undefined {
  const explicit = env.CTI_CODEX_SOURCE_HOME?.trim();
  if (explicit) {
    return path.resolve(explicit);
  }

  const inherited = env.CODEX_HOME?.trim();
  if (inherited) {
    return path.resolve(inherited);
  }

  const homeDir = env.USERPROFILE?.trim() || env.HOME?.trim();
  if (!homeDir) {
    return undefined;
  }

  return path.join(homeDir, '.codex');
}

function readFileOrNull(filePath: string): Buffer | null {
  try {
    return fs.readFileSync(filePath);
  } catch {
    return null;
  }
}

function copyFileIfChanged(sourcePath: string, targetPath: string): boolean {
  const source = readFileOrNull(sourcePath);
  if (!source) {
    return false;
  }

  const existing = readFileOrNull(targetPath);
  if (existing && existing.equals(source)) {
    return false;
  }

  ensureDir(path.dirname(targetPath));
  fs.writeFileSync(targetPath, source);
  return true;
}

export function syncCodexShadowHomeAuth(
  sourceHome: string | undefined,
  shadowHome: string,
): { copied: boolean; sourceAuthPath?: string; targetAuthPath: string } {
  const targetAuthPath = path.join(shadowHome, AUTH_FILE_NAME);
  if (!sourceHome) {
    return { copied: false, targetAuthPath };
  }

  const sourceAuthPath = path.join(sourceHome, AUTH_FILE_NAME);
  const copied = copyFileIfChanged(sourceAuthPath, targetAuthPath);
  return { copied, sourceAuthPath, targetAuthPath };
}

export function prepareCodexShadowHome(
  env: NodeJS.ProcessEnv = process.env,
): { mode: 'inherit' | 'shadow'; codexHome?: string; sourceHome?: string; copiedAuth: boolean } {
  const mode = resolveCodexHomeMode(env);
  if (mode === 'inherit') {
    return { mode, codexHome: env.CODEX_HOME, sourceHome: resolveSourceCodexHome(env), copiedAuth: false };
  }

  const sourceHome = resolveSourceCodexHome(env);
  const codexHome = resolveShadowCodexHome(env);
  ensureDir(codexHome);
  const syncResult = syncCodexShadowHomeAuth(sourceHome, codexHome);

  return {
    mode,
    codexHome,
    sourceHome,
    copiedAuth: syncResult.copied,
  };
}

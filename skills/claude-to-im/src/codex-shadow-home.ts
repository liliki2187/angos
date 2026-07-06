import fs from 'node:fs';
import path from 'node:path';

import { CTI_HOME } from './config.js';
import { ensureDir } from './file-utils.js';

const AUTH_FILE_NAME = 'auth.json';
const DEFAULT_SHADOW_HOME_DIR = path.join(CTI_HOME, 'codex-home');
const SYSTEM_SKILLS_TO_SYNC = ['imagegen'] as const;
type SystemSkillsSyncMode = 'copy' | 'link';

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

export function resolveSystemSkillsSyncMode(
  env: NodeJS.ProcessEnv = process.env,
): SystemSkillsSyncMode {
  const raw = env.CTI_CODEX_SYSTEM_SKILLS_SYNC_MODE?.trim().toLowerCase();
  if (raw === 'copy') {
    return 'copy';
  }
  return 'link';
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

function copyDirectoryFilesIfChanged(sourceDir: string, targetDir: string): boolean {
  let copied = false;

  if (!fs.existsSync(sourceDir)) {
    return false;
  }

  for (const entry of fs.readdirSync(sourceDir, { withFileTypes: true })) {
    const sourcePath = path.join(sourceDir, entry.name);
    const targetPath = path.join(targetDir, entry.name);

    if (entry.isDirectory()) {
      if (copyDirectoryFilesIfChanged(sourcePath, targetPath)) {
        copied = true;
      }
      continue;
    }

    if (entry.isFile() && copyFileIfChanged(sourcePath, targetPath)) {
      copied = true;
    }
  }

  return copied;
}

function isSameRealPath(left: string, right: string): boolean {
  try {
    return fs.realpathSync.native(left) === fs.realpathSync.native(right);
  } catch {
    return false;
  }
}

function isPathInside(childPath: string, parentPath: string): boolean {
  const relative = path.relative(path.resolve(parentPath), path.resolve(childPath));
  return relative === '' || (!relative.startsWith('..') && !path.isAbsolute(relative));
}

function linkDirectoryOrCopy(sourceDir: string, targetDir: string, shadowHome: string): boolean {
  if (!fs.existsSync(sourceDir)) {
    return false;
  }

  if (fs.existsSync(targetDir)) {
    if (isSameRealPath(targetDir, sourceDir)) {
      return false;
    }

    if (!isPathInside(targetDir, shadowHome)) {
      throw new Error(`Refusing to replace system skill outside shadow CODEX_HOME: ${targetDir}`);
    }

    fs.rmSync(targetDir, { recursive: true, force: true });
  }

  ensureDir(path.dirname(targetDir));
  try {
    fs.symlinkSync(
      path.resolve(sourceDir),
      targetDir,
      process.platform === 'win32' ? 'junction' : 'dir',
    );
    return true;
  } catch {
    return copyDirectoryFilesIfChanged(sourceDir, targetDir);
  }
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

export function syncCodexShadowHomeSystemSkills(
  sourceHome: string | undefined,
  shadowHome: string,
  env: NodeJS.ProcessEnv = process.env,
): string[] {
  if (!sourceHome) {
    return [];
  }

  const syncMode = resolveSystemSkillsSyncMode(env);
  const copiedSkills: string[] = [];
  for (const skillName of SYSTEM_SKILLS_TO_SYNC) {
    const sourceDir = path.join(sourceHome, 'skills', '.system', skillName);
    const targetDir = path.join(shadowHome, 'skills', '.system', skillName);
    const changed = syncMode === 'copy'
      ? copyDirectoryFilesIfChanged(sourceDir, targetDir)
      : linkDirectoryOrCopy(sourceDir, targetDir, shadowHome);
    if (changed) {
      copiedSkills.push(skillName);
    }
  }
  return copiedSkills;
}

export function prepareCodexShadowHome(
  env: NodeJS.ProcessEnv = process.env,
): { mode: 'inherit' | 'shadow'; codexHome?: string; sourceHome?: string; copiedAuth: boolean; copiedSystemSkills: string[] } {
  const mode = resolveCodexHomeMode(env);
  if (mode === 'inherit') {
    return { mode, codexHome: env.CODEX_HOME, sourceHome: resolveSourceCodexHome(env), copiedAuth: false, copiedSystemSkills: [] };
  }

  const sourceHome = resolveSourceCodexHome(env);
  const codexHome = resolveShadowCodexHome(env);
  ensureDir(codexHome);
  const syncResult = syncCodexShadowHomeAuth(sourceHome, codexHome);
  const copiedSystemSkills = syncCodexShadowHomeSystemSkills(sourceHome, codexHome, env);

  return {
    mode,
    codexHome,
    sourceHome,
    copiedAuth: syncResult.copied,
    copiedSystemSkills,
  };
}

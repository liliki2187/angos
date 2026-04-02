import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

export function ensureDir(dir: string): void {
  fs.mkdirSync(dir, { recursive: true });
}

function isReplaceFallbackError(err: unknown): boolean {
  const code = (err as NodeJS.ErrnoException | undefined)?.code;
  return code === 'EPERM' || code === 'EACCES' || code === 'EBUSY';
}

function cleanupTempFile(tmpPath: string): void {
  try {
    fs.rmSync(tmpPath, { force: true });
  } catch (err) {
    const code = (err as NodeJS.ErrnoException | undefined)?.code;
    if (code !== 'EPERM' && code !== 'EACCES' && code !== 'EBUSY' && code !== 'ENOENT') {
      throw err;
    }
  }
}

function replaceFileWithFallback(tmpPath: string, filePath: string): void {
  try {
    fs.renameSync(tmpPath, filePath);
    return;
  } catch (err) {
    if (!isReplaceFallbackError(err)) {
      throw err;
    }
  }

  fs.copyFileSync(tmpPath, filePath);
  cleanupTempFile(tmpPath);
}

export function atomicWrite(filePath: string, data: string): void {
  const dir = path.dirname(filePath);
  const writeOnce = (): void => {
    ensureDir(dir);
    const tmpPath = `${filePath}.${process.pid}.${crypto.randomUUID()}.tmp`;
    try {
      fs.writeFileSync(tmpPath, data, 'utf-8');
      replaceFileWithFallback(tmpPath, filePath);
    } catch (err) {
      cleanupTempFile(tmpPath);
      throw err;
    }
  };

  try {
    writeOnce();
  } catch (err) {
    if ((err as NodeJS.ErrnoException | undefined)?.code !== 'ENOENT') {
      throw err;
    }
    writeOnce();
  }
}

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '..');
const testDir = path.join(rootDir, 'src', '__tests__');
const ctiHome = fs.mkdtempSync(path.join(os.tmpdir(), 'cti-home-'));

const testFiles = fs.readdirSync(testDir)
  .filter((name) => name.endsWith('.test.ts'))
  .sort()
  .map((name) => path.join('src', '__tests__', name));

const result = spawnSync(
  process.execPath,
  ['--test', '--test-concurrency=1', '--import', 'tsx', '--test-timeout=15000', ...testFiles],
  {
    cwd: rootDir,
    stdio: 'inherit',
    env: {
      ...process.env,
      CTI_HOME: ctiHome,
    },
  },
);

process.exit(result.status ?? 1);

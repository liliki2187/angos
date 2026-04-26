import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

import { CTI_HOME } from '../config.js';
import {
  prepareCodexShadowHome,
  resolveCodexHomeMode,
  resolveShadowCodexHome,
  resolveSourceCodexHome,
} from '../codex-shadow-home.js';
import { buildCodexCliEnv } from '../codex-provider.js';

function makeTempDir(prefix: string): string {
  return fs.mkdtempSync(path.join(os.tmpdir(), prefix));
}

describe('codex shadow home', () => {
  it('defaults to shadow mode', () => {
    assert.equal(resolveCodexHomeMode({}), 'shadow');
  });

  it('respects inherit mode override', () => {
    assert.equal(resolveCodexHomeMode({ CTI_CODEX_HOME_MODE: 'inherit' }), 'inherit');
  });

  it('resolves source home from explicit override, then CODEX_HOME, then USERPROFILE', () => {
    assert.equal(
      resolveSourceCodexHome({
        CTI_CODEX_SOURCE_HOME: 'D:/custom-codex-home',
        CODEX_HOME: 'D:/ignored',
        USERPROFILE: 'C:/Users/example',
      }),
      path.resolve('D:/custom-codex-home'),
    );

    assert.equal(
      resolveSourceCodexHome({
        CODEX_HOME: 'D:/from-code-home',
        USERPROFILE: 'C:/Users/example',
      }),
      path.resolve('D:/from-code-home'),
    );

    assert.equal(
      resolveSourceCodexHome({
        USERPROFILE: 'C:/Users/example',
      }),
      path.join('C:/Users/example', '.codex'),
    );
  });

  it('creates shadow home under CTI_HOME by default and syncs auth.json', () => {
    const userHome = makeTempDir('cti-user-home-');
    const sourceHome = path.join(userHome, '.codex');
    fs.mkdirSync(sourceHome, { recursive: true });
    fs.writeFileSync(path.join(sourceHome, 'auth.json'), '{"token":"abc"}', 'utf-8');

    const result = prepareCodexShadowHome({
      USERPROFILE: userHome,
    });

    assert.equal(result.mode, 'shadow');
    assert.equal(result.codexHome, path.join(CTI_HOME, 'codex-home'));
    assert.equal(result.sourceHome, sourceHome);
    assert.equal(result.copiedAuth, true);
    assert.equal(
      fs.readFileSync(path.join(result.codexHome!, 'auth.json'), 'utf-8'),
      '{"token":"abc"}',
    );
  });

  it('uses explicit shadow home override when provided', () => {
    const shadowHome = makeTempDir('cti-shadow-home-');
    assert.equal(
      resolveShadowCodexHome({ CTI_CODEX_SHADOW_HOME: shadowHome }),
      path.resolve(shadowHome),
    );
  });

  it('buildCodexCliEnv injects bridge-managed CODEX_HOME and keeps synced auth available', () => {
    const userHome = makeTempDir('cti-env-user-home-');
    const sourceHome = path.join(userHome, '.codex');
    fs.mkdirSync(sourceHome, { recursive: true });
    fs.writeFileSync(path.join(sourceHome, 'auth.json'), '{"token":"shadow"}', 'utf-8');

    const shadowHome = makeTempDir('cti-env-shadow-home-');
    const env = buildCodexCliEnv({
      USERPROFILE: userHome,
      CTI_CODEX_SHADOW_HOME: shadowHome,
      PATH: process.env.PATH,
      LOCALAPPDATA: process.env.LOCALAPPDATA,
      SYSTEMROOT: process.env.SYSTEMROOT,
    });

    assert.equal(env.CODEX_HOME, path.resolve(shadowHome));
    assert.equal(
      fs.readFileSync(path.join(shadowHome, 'auth.json'), 'utf-8'),
      '{"token":"shadow"}',
    );
  });

  it('skips shadow home injection when inherit mode is requested', () => {
    const env = buildCodexCliEnv({
      CTI_CODEX_HOME_MODE: 'inherit',
      CODEX_HOME: 'D:/existing-codex-home',
      PATH: process.env.PATH,
      LOCALAPPDATA: process.env.LOCALAPPDATA,
      SYSTEMROOT: process.env.SYSTEMROOT,
    });

    assert.equal(env.CODEX_HOME, 'D:/existing-codex-home');
  });
});

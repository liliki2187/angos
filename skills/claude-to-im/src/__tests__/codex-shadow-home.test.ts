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
  resolveSystemSkillsSyncMode,
  syncCodexShadowHomeSystemSkills,
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

  it('links system skills by default and supports copy override', () => {
    assert.equal(resolveSystemSkillsSyncMode({}), 'link');
    assert.equal(resolveSystemSkillsSyncMode({ CTI_CODEX_SYSTEM_SKILLS_SYNC_MODE: 'copy' }), 'copy');
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

  it('syncs the system imagegen skill into the shadow home', () => {
    const userHome = makeTempDir('cti-user-home-skills-');
    const sourceHome = path.join(userHome, '.codex');
    const sourceImagegen = path.join(sourceHome, 'skills', '.system', 'imagegen');
    fs.mkdirSync(path.join(sourceImagegen, 'references'), { recursive: true });
    fs.writeFileSync(path.join(sourceImagegen, 'SKILL.md'), '# Image Generation Skill', 'utf-8');
    fs.writeFileSync(path.join(sourceImagegen, 'references', 'prompting.md'), 'Prompting notes', 'utf-8');

    const shadowHome = makeTempDir('cti-shadow-home-skills-');
    const copied = syncCodexShadowHomeSystemSkills(sourceHome, shadowHome);
    const targetImagegen = path.join(shadowHome, 'skills', '.system', 'imagegen');

    assert.deepEqual(copied, ['imagegen']);
    assert.equal(fs.realpathSync.native(targetImagegen), fs.realpathSync.native(sourceImagegen));
    assert.equal(
      fs.readFileSync(path.join(targetImagegen, 'SKILL.md'), 'utf-8'),
      '# Image Generation Skill',
    );
    assert.equal(
      fs.readFileSync(path.join(targetImagegen, 'references', 'prompting.md'), 'utf-8'),
      'Prompting notes',
    );
  });

  it('can copy the system imagegen skill when link mode is disabled', () => {
    const userHome = makeTempDir('cti-user-home-copy-skills-');
    const sourceHome = path.join(userHome, '.codex');
    const sourceImagegen = path.join(sourceHome, 'skills', '.system', 'imagegen');
    fs.mkdirSync(sourceImagegen, { recursive: true });
    fs.writeFileSync(path.join(sourceImagegen, 'SKILL.md'), '# Copied Image Generation Skill', 'utf-8');

    const shadowHome = makeTempDir('cti-shadow-home-copy-skills-');
    const copied = syncCodexShadowHomeSystemSkills(sourceHome, shadowHome, {
      CTI_CODEX_SYSTEM_SKILLS_SYNC_MODE: 'copy',
    });
    const targetImagegen = path.join(shadowHome, 'skills', '.system', 'imagegen');

    assert.deepEqual(copied, ['imagegen']);
    assert.notEqual(fs.realpathSync.native(targetImagegen), fs.realpathSync.native(sourceImagegen));
    assert.equal(
      fs.readFileSync(path.join(targetImagegen, 'SKILL.md'), 'utf-8'),
      '# Copied Image Generation Skill',
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

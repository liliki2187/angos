#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const skillDir = path.resolve(scriptDir, '..');
const skillsDir = path.resolve(skillDir, '..');
const ctiHome = process.env.CTI_HOME || path.join(skillsDir, '.claude-to-im');
const dataDir = path.join(ctiHome, 'data');
const sessionsPath = path.join(dataDir, 'sessions.json');
const bindingsPath = path.join(dataDir, 'bindings.json');
const messagesDir = path.join(dataDir, 'messages');

function readJsonObject(filePath) {
  try {
    return JSON.parse(fs.readFileSync(filePath, 'utf-8'));
  } catch {
    return {};
  }
}

function writeJson(filePath, value) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  const tmpPath = `${filePath}.${process.pid}.${crypto.randomUUID ? crypto.randomUUID() : Date.now()}.tmp`;
  fs.writeFileSync(tmpPath, JSON.stringify(value, null, 2), 'utf-8');
  fs.renameSync(tmpPath, filePath);
}

function resetSessions() {
  const sessions = readJsonObject(sessionsPath);
  let resetSessionIds = 0;
  for (const session of Object.values(sessions)) {
    if (session && typeof session === 'object' && 'sdk_session_id' in session) {
      delete session.sdk_session_id;
      resetSessionIds += 1;
    }
  }
  if (fs.existsSync(sessionsPath)) {
    writeJson(sessionsPath, sessions);
  }

  const bindings = readJsonObject(bindingsPath);
  let resetBindingIds = 0;
  for (const binding of Object.values(bindings)) {
    if (binding && typeof binding === 'object' && binding.sdkSessionId) {
      binding.sdkSessionId = '';
      resetBindingIds += 1;
    }
  }
  if (fs.existsSync(bindingsPath)) {
    writeJson(bindingsPath, bindings);
  }

  let removedMessageFiles = 0;
  if (fs.existsSync(messagesDir)) {
    for (const entry of fs.readdirSync(messagesDir, { withFileTypes: true })) {
      if (entry.isFile() && entry.name.endsWith('.json')) {
        fs.rmSync(path.join(messagesDir, entry.name), { force: true });
        removedMessageFiles += 1;
      }
    }
  }

  return { resetSessionIds, resetBindingIds, removedMessageFiles };
}

const result = resetSessions();
console.log(
  `Reset bridge sessions: ${result.resetSessionIds} session id(s), ` +
  `${result.resetBindingIds} binding id(s), ${result.removedMessageFiles} message history file(s).`,
);

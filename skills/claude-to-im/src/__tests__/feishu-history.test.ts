import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

import {
  disableFeishuHistoryBackfill,
  normalizeFeishuHistoryRole,
  parseFeishuFileKeys,
  parseFeishuPostContent,
  parseFeishuTextContent,
} from '../feishu-history.js';
import { CTI_HOME } from '../config.js';

describe('normalizeFeishuHistoryRole', () => {
  it('classifies the bridge bot as assistant when sender id matches', () => {
    const botIds = new Set(['ou_bot_123']);
    assert.equal(normalizeFeishuHistoryRole('ou_bot_123', 'bot', botIds), 'assistant');
  });

  it('classifies regular users as user', () => {
    const botIds = new Set(['ou_bot_123']);
    assert.equal(normalizeFeishuHistoryRole('ou_user_456', 'user', botIds), 'user');
  });

  it('falls back to sender type when bot id is unavailable', () => {
    assert.equal(normalizeFeishuHistoryRole(undefined, 'app', new Set()), 'assistant');
  });
});

describe('parseFeishuTextContent', () => {
  it('extracts text from json payloads', () => {
    assert.equal(parseFeishuTextContent('{"text":"你好，世界"}'), '你好，世界');
  });

  it('keeps plain text payloads intact', () => {
    assert.equal(parseFeishuTextContent('plain text'), 'plain text');
  });
});

describe('parseFeishuFileKeys', () => {
  it('handles snake_case payloads', () => {
    assert.deepEqual(
      parseFeishuFileKeys('{"file_key":"file_1","image_key":"img_1","file_name":"demo.png"}'),
      { fileKey: 'file_1', imageKey: 'img_1', fileName: 'demo.png' },
    );
  });

  it('handles camelCase payloads', () => {
    assert.deepEqual(
      parseFeishuFileKeys('{"fileKey":"file_2","imageKey":"img_2","fileName":"demo.jpg"}'),
      { fileKey: 'file_2', imageKey: 'img_2', fileName: 'demo.jpg' },
    );
  });
});

describe('parseFeishuPostContent', () => {
  it('extracts readable text and image keys from post content', () => {
    const parsed = parseFeishuPostContent(JSON.stringify({
      title: '日报',
      content: [
        [
          { tag: 'text', text: '第一段' },
          { tag: 'a', text: '链接', href: 'https://example.com' },
        ],
        [
          { tag: 'img', image_key: 'img_123' },
          { tag: 'at', user_name: 'Alice' },
        ],
      ],
    }));

    assert.equal(parsed.text, '日报\n第一段链接\n@Alice');
    assert.deepEqual(parsed.imageKeys, ['img_123']);
  });
});

describe('disableFeishuHistoryBackfill', () => {
  it('writes an empty applied cache for the session', () => {
    disableFeishuHistoryBackfill('sess-clear', {
      chatId: 'chat-clear',
      createdAt: '2026-03-23T00:00:00.000Z',
    });

    const cachePath = path.join(CTI_HOME, 'data', 'feishu-history-cache', 'sess-clear.json');
    const parsed = JSON.parse(fs.readFileSync(cachePath, 'utf-8')) as {
      chatId: string;
      bindingCreatedAt: string;
      appliedToFreshSession: boolean;
      messages: unknown[];
    };

    assert.equal(parsed.chatId, 'chat-clear');
    assert.equal(parsed.bindingCreatedAt, '2026-03-23T00:00:00.000Z');
    assert.equal(parsed.appliedToFreshSession, true);
    assert.deepEqual(parsed.messages, []);
  });
});

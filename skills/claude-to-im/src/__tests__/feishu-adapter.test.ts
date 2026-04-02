import { afterEach, describe, it } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { Readable } from 'node:stream';

import { initBridgeContext } from 'claude-to-im/src/lib/bridge/context.js';
import { JsonFileStore } from '../store.js';
import {
  FeishuAdapter,
  buildReadableFeishuCardContent,
  buildBusyMentionPostContent,
  buildStoredInboundContent,
  computeBackfillWindow,
  computeFeishuFinalRemainder,
  computeFeishuPreviewDelta,
  isFeishuClearCommandText,
  isFeishuStopCommandText,
  shouldPreferFeishuCard,
} from '../feishu-adapter.js';
import { CTI_HOME } from '../config.js';

function makeSettings(extra: Array<[string, string]> = []): Map<string, string> {
  return new Map([
    ['remote_bridge_enabled', 'true'],
    ['bridge_feishu_enabled', 'true'],
    ['bridge_feishu_group_policy', 'open'],
    ['bridge_feishu_require_mention', 'true'],
    ...extra,
  ]);
}

function initTestContext(extra: Array<[string, string]> = []): JsonFileStore {
  const store = new JsonFileStore(makeSettings(extra));
  initBridgeContext({
    store,
    llm: { streamChat: () => new ReadableStream<string>() },
    permissions: { resolvePendingPermission: () => true },
    lifecycle: {},
  });
  return store;
}

function makeMockRestClient() {
  const calls: Array<{
    kind: 'create' | 'reply';
    payload: Record<string, unknown>;
  }> = [];
  return {
    calls,
    client: {
      im: {
        message: {
          create: async (payload: Record<string, unknown>) => {
            calls.push({ kind: 'create', payload });
            return { data: { message_id: `msg-${calls.length}` } };
          },
          reply: async (payload: Record<string, unknown>) => {
            calls.push({ kind: 'reply', payload });
            return { data: { message_id: `msg-${calls.length}` } };
          },
        },
      },
    },
  };
}

function createDeferred<T>() {
  let resolve!: (value: T) => void;
  let reject!: (reason?: unknown) => void;
  const promise = new Promise<T>((res, rej) => {
    resolve = res;
    reject = rej;
  });
  return { promise, resolve, reject };
}

function makeControlledReplyRestClient() {
  const calls: Array<{
    kind: 'create' | 'reply';
    payload: Record<string, unknown>;
  }> = [];
  const replies: Array<ReturnType<typeof createDeferred<{ data: { message_id: string } }>>> = [];
  return {
    calls,
    replies,
    client: {
      im: {
        message: {
          create: async (payload: Record<string, unknown>) => {
            calls.push({ kind: 'create', payload });
            return { data: { message_id: `msg-${calls.length}` } };
          },
          reply: (payload: Record<string, unknown>) => {
            calls.push({ kind: 'reply', payload });
            const deferred = createDeferred<{ data: { message_id: string } }>();
            replies.push(deferred);
            return deferred.promise;
          },
        },
      },
    },
  };
}

function makeReplyAwareRestClient() {
  const replyImage = Buffer.from('reply-image');
  return {
    im: {
      message: {
        list: async () => ({ data: { items: [], has_more: false } }),
        get: async (payload: Record<string, unknown>) => {
          const path = payload.path as { message_id: string };
          if (path.message_id !== 'reply-msg-1') {
            return { data: { items: [] } };
          }

          return {
            data: {
              items: [{
                message_id: 'reply-msg-1',
                chat_id: 'chat-reply',
                msg_type: 'image',
                create_time: String(Date.now() - 1000),
                sender: {
                  id: { open_id: 'user-open-id' },
                  sender_type: 'user',
                },
                body: {
                  content: JSON.stringify({ image_key: 'img-reply-1' }),
                },
              }],
            },
          };
        },
      },
      messageResource: {
        get: async (payload: Record<string, unknown>) => {
          const resourcePath = payload.path as { message_id: string; file_key: string };
          assert.equal(resourcePath.message_id, 'reply-msg-1');
          assert.equal(resourcePath.file_key, 'img-reply-1');
          return {
            getReadableStream: () => Readable.from([replyImage]),
            writeFile: async () => {},
          };
        },
      },
    },
  };
}

function extractTextReplyContent(call: { payload: Record<string, unknown> }): string {
  const data = call.payload.data as { content: string };
  return JSON.parse(data.content).text;
}

function extractMentionReplyContent(call: { payload: Record<string, unknown> }): { userId: string; text: string } {
  const data = call.payload.data as { content: string };
  const payload = JSON.parse(data.content);
  return {
    userId: payload.zh_cn.content[0][0].user_id,
    text: payload.zh_cn.content[0][1].text,
  };
}

async function flushAsyncWork(): Promise<void> {
  await new Promise((resolve) => setTimeout(resolve, 0));
}

describe('Feishu history helpers', () => {
  it('computes an initial history window from lookback hours', () => {
    const window = computeBackfillWindow(0, 1_000_000, 24);
    assert.deepEqual(window, {
      startMs: 0,
      endMs: 999_999,
    });
  });

  it('computes an incremental window from the last synced timestamp', () => {
    const window = computeBackfillWindow(1234, 5678, 48);
    assert.deepEqual(window, {
      startMs: 1235,
      endMs: 5677,
    });
  });

  it('returns null when there is no gap to backfill', () => {
    assert.equal(computeBackfillWindow(5678, 5678, 48), null);
  });
});

describe('Feishu clear command helpers', () => {
  it('matches clear commands after stripping whitespace and optional slash', () => {
    assert.equal(isFeishuClearCommandText(' clear '), true);
    assert.equal(isFeishuClearCommandText('/clear'), true);
    assert.equal(isFeishuClearCommandText('C L E A R'), true);
    assert.equal(isFeishuClearCommandText('clear now'), false);
  });
});

describe('buildStoredInboundContent', () => {
  let tempDir: string | null = null;

  afterEach(() => {
    if (tempDir && fs.existsSync(tempDir)) {
      fs.rmSync(tempDir, { recursive: true, force: true });
    }
    tempDir = null;
  });

  it('persists attachments into .codepilot-uploads and stores metadata markup', () => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'cti-feishu-history-'));
    const content = buildStoredInboundContent(
      'Historical image',
      [{
        id: 'file-1',
        name: 'diagram.png',
        type: 'image/png',
        size: 4,
        data: Buffer.from('test').toString('base64'),
      }],
      tempDir,
      'msg-123',
    );

    assert.ok(content.startsWith('<!--files:['));
    assert.ok(content.endsWith('Historical image'));

    const uploadDir = path.join(tempDir, '.codepilot-uploads');
    const files = fs.readdirSync(uploadDir);
    assert.equal(files.length, 1);
    assert.ok(files[0].startsWith('msg-123-0-'));
  });

  it('falls back to readable attachment text when no workdir is available', () => {
    const content = buildStoredInboundContent(
      'Historical file',
      [{
        id: 'file-2',
        name: 'voice.mp3',
        type: 'audio/mpeg',
        size: 2048,
        data: Buffer.from('test').toString('base64'),
      }],
      undefined,
      'msg-456',
    );

    assert.ok(content.includes('Attached files: voice.mp3 (audio/mpeg, 2.0 KB)'));
    assert.ok(content.includes('Historical file'));
  });
});

describe('Feishu streaming helpers', () => {
  it('matches stop commands after stripping whitespace and case', () => {
    assert.equal(isFeishuStopCommandText(' stop '), true);
    assert.equal(isFeishuStopCommandText('S T O P'), true);
    assert.equal(isFeishuStopCommandText('stop now'), false);
  });

  it('computes only the newly appended preview text', () => {
    assert.equal(
      computeFeishuPreviewDelta('alpha', 'alpha\nbeta'),
      '\nbeta',
    );
  });

  it('computes the unsent final remainder after streamed preview text', () => {
    assert.equal(
      computeFeishuFinalRemainder('alpha\nbeta', 'alpha\nbeta\ngamma'),
      '\ngamma',
    );
  });

  it('tolerates preview text that ended with truncation ellipsis', () => {
    assert.equal(
      computeFeishuFinalRemainder('prefix...', 'prefix and suffix'),
      ' and suffix',
    );
  });

  it('builds a busy reply post payload with a real @mention node', () => {
    const payload = JSON.parse(
      buildBusyMentionPostContent('ou_user_123', '\u5728\u5fd9\uff0c\u522b\u5435'),
    );
    assert.equal(payload.zh_cn.content[0][0].tag, 'at');
    assert.equal(payload.zh_cn.content[0][0].user_id, 'ou_user_123');
    assert.equal(payload.zh_cn.content[0][1].text, ' \u5728\u5fd9\uff0c\u522b\u5435');
  });
});

describe('FeishuAdapter streaming delivery', () => {
  it('sends only appended preview chunks and only the unsent final tail', async () => {
    initTestContext();
    const adapter = new FeishuAdapter();
    const { client, calls } = makeMockRestClient();

    (adapter as any).restClient = client;
    (adapter as any).lastIncomingMessageId.set('chat-1', 'incoming-1');

    assert.equal(await adapter.sendPreview?.('chat-1', 'alpha', 101), 'sent');
    assert.equal(await adapter.sendPreview?.('chat-1', 'alpha\nbeta', 101), 'sent');

    assert.equal(calls.length, 2);
    assert.equal(calls[0].kind, 'reply');
    assert.equal(extractTextReplyContent(calls[0]), 'alpha');
    assert.equal(extractTextReplyContent(calls[1]), '\nbeta');

    const result = await adapter.send({
      address: { channelType: 'feishu', chatId: 'chat-1' },
      text: 'alpha\nbeta\ngamma',
      parseMode: 'Markdown',
      replyToMessageId: 'incoming-1',
    });

    assert.equal(result.ok, true);
    assert.equal(calls.length, 3);
    assert.equal(calls[2].kind, 'reply');
    assert.equal(extractTextReplyContent(calls[2]), '\ngamma');
  });

  it('does not send an extra final message when preview already emitted the full answer', async () => {
    initTestContext();
    const adapter = new FeishuAdapter();
    const { client, calls } = makeMockRestClient();

    (adapter as any).restClient = client;
    (adapter as any).lastIncomingMessageId.set('chat-2', 'incoming-2');

    assert.equal(await adapter.sendPreview?.('chat-2', 'already sent', 202), 'sent');

    const result = await adapter.send({
      address: { channelType: 'feishu', chatId: 'chat-2' },
      text: 'already sent',
      parseMode: 'Markdown',
      replyToMessageId: 'incoming-2',
    });

    assert.equal(result.ok, true);
    assert.equal(calls.length, 1);
  });

  it('suppresses duplicate outbound payloads for the same reply target', async () => {
    initTestContext();
    const adapter = new FeishuAdapter();
    const { client, calls } = makeMockRestClient();

    (adapter as any).restClient = client;

    const first = await adapter.send({
      address: { channelType: 'feishu', chatId: 'chat-3' },
      text: 'same payload',
      parseMode: 'plain',
      replyToMessageId: 'incoming-3',
    });
    const second = await adapter.send({
      address: { channelType: 'feishu', chatId: 'chat-3' },
      text: 'same payload',
      parseMode: 'plain',
      replyToMessageId: 'incoming-3',
    });

    assert.equal(first.ok, true);
    assert.equal(second.ok, true);
    assert.equal(calls.length, 1);
    assert.equal(second.messageId, first.messageId);
  });

  it('serializes overlapping preview sends so later drafts only send the new tail', async () => {
    initTestContext();
    const adapter = new FeishuAdapter();
    const { client, calls, replies } = makeControlledReplyRestClient();

    (adapter as any).restClient = client;
    (adapter as any).lastIncomingMessageId.set('chat-4', 'incoming-4');

    const firstPreview = adapter.sendPreview('chat-4', 'alpha', 404);
    await flushAsyncWork();
    assert.equal(calls.length, 1);
    assert.equal(extractTextReplyContent(calls[0]), 'alpha');

    const secondPreview = adapter.sendPreview('chat-4', 'alpha\nbeta', 404);
    await flushAsyncWork();
    assert.equal(calls.length, 1);

    replies[0].resolve({ data: { message_id: 'msg-1' } });
    await flushAsyncWork();
    assert.equal(calls.length, 2);
    assert.equal(extractTextReplyContent(calls[1]), '\nbeta');

    replies[1].resolve({ data: { message_id: 'msg-2' } });
    await Promise.all([firstPreview, secondPreview]);
  });

  it('waits for an in-flight preview before deciding whether the final reply still needs a tail', async () => {
    initTestContext();
    const adapter = new FeishuAdapter();
    const { client, calls, replies } = makeControlledReplyRestClient();

    (adapter as any).restClient = client;
    (adapter as any).lastIncomingMessageId.set('chat-5', 'incoming-5');

    const firstPreview = adapter.sendPreview('chat-5', 'alpha', 505);
    await flushAsyncWork();
    replies[0].resolve({ data: { message_id: 'msg-1' } });
    await firstPreview;

    const secondPreview = adapter.sendPreview('chat-5', 'alpha\nbeta', 505);
    await flushAsyncWork();
    assert.equal(calls.length, 2);
    assert.equal(extractTextReplyContent(calls[1]), '\nbeta');

    const finalSend = adapter.send({
      address: { channelType: 'feishu', chatId: 'chat-5' },
      text: 'alpha\nbeta',
      parseMode: 'Markdown',
      replyToMessageId: 'incoming-5',
    });
    await flushAsyncWork();
    assert.equal(calls.length, 2);

    replies[1].resolve({ data: { message_id: 'msg-2' } });
    const result = await finalSend;
    await secondPreview;

    assert.equal(result.ok, true);
    assert.equal(calls.length, 2);
  });
});

describe('FeishuAdapter busy replies', () => {
  it('replies with @user busy notice instead of enqueueing another group mention while busy', async () => {
    initTestContext();
    const adapter = new FeishuAdapter();
    const { client, calls } = makeMockRestClient();

    (adapter as any).restClient = client;
    (adapter as any).busyChats.add('chat-busy');
    (adapter as any).botIds.add('bot-open-id');

    await adapter.handleIncomingEvent({
      sender: {
        sender_id: { open_id: 'user-open-id' },
        sender_type: 'user',
      },
      message: {
        message_id: 'incoming-busy',
        chat_id: 'chat-busy',
        chat_type: 'group',
        message_type: 'text',
        content: JSON.stringify({ text: '@_user_1 handle this now' }),
        create_time: String(Date.now()),
        mentions: [
          {
            key: '@_user_1',
            id: { open_id: 'bot-open-id' },
            name: 'bridge-bot',
          },
        ],
      },
    });

    assert.equal(calls.length, 1);
    assert.equal(calls[0].kind, 'reply');
    const payload = JSON.parse((calls[0].payload.data as { content: string }).content);
    assert.equal(payload.zh_cn.content[0][0].tag, 'at');
    assert.equal(payload.zh_cn.content[0][0].user_id, 'user-open-id');
    assert.equal(payload.zh_cn.content[0][1].text, ' \u5728\u5fd9\uff0c\u522b\u5435');
    assert.equal((adapter as any).queue.length, 0);
  });

  it('stops the current session when a busy @mention is exactly stop and notifies the original requester', async () => {
    initTestContext();
    const adapter = new FeishuAdapter();
    const { client, calls } = makeMockRestClient();

    (adapter as any).restClient = client;
    (adapter as any).busyChats.add('chat-busy-stop');
    (adapter as any).botIds.add('bot-open-id');
    (adapter as any).taskStates.set('chat-busy-stop', {
      requesterUserId: 'owner-open-id',
      requesterMessageId: 'incoming-owner',
      responseDelivered: true,
      errorDelivered: false,
      stopRequested: false,
      stopNoticeMessageId: undefined,
    });

    await adapter.handleIncomingEvent({
      sender: {
        sender_id: { open_id: 'stopper-open-id' },
        sender_type: 'user',
      },
      message: {
        message_id: 'incoming-stop',
        chat_id: 'chat-busy-stop',
        chat_type: 'group',
        message_type: 'text',
        content: JSON.stringify({ text: '@_user_1   S T O P  ' }),
        create_time: String(Date.now()),
        mentions: [
          {
            key: '@_user_1',
            id: { open_id: 'bot-open-id' },
            name: 'bridge-bot',
          },
        ],
      },
    });

    assert.equal(calls.length, 1);
    assert.equal(calls[0].kind, 'reply');
    assert.deepEqual(extractMentionReplyContent(calls[0]), {
      userId: 'owner-open-id',
      text: ' \u505c\u4e86\uff0c\u4e0d\u641e\u4e86',
    });

    assert.equal((adapter as any).queue.length, 1);
    assert.equal((adapter as any).queue[0].text, '/stop');
    assert.equal((adapter as any).queue[0].raw.syntheticBusyStop, true);

    const taskState = (adapter as any).taskStates.get('chat-busy-stop');
    assert.equal(taskState.stopRequested, true);
    assert.equal(taskState.stopNoticeMessageId, 'msg-1');
  });

  it('queues a clear-after-stop flow when a busy @mention is exactly clear', async () => {
    const store = initTestContext();
    const adapter = new FeishuAdapter();
    const { client, calls } = makeMockRestClient();

    (adapter as any).restClient = client;
    (adapter as any).busyChats.add('chat-busy-clear');
    (adapter as any).botIds.add('bot-open-id');

    const session = store.createSession('test', 'model', undefined, '/tmp');
    store.upsertChannelBinding({
      channelType: 'feishu',
      chatId: 'chat-busy-clear',
      codepilotSessionId: session.id,
      workingDirectory: '/tmp',
      model: 'model',
    });
    store.addMessage(session.id, 'user', 'old context');

    (adapter as any).taskStates.set('chat-busy-clear', {
      requesterUserId: 'owner-open-id',
      requesterMessageId: 'incoming-owner',
      responseDelivered: true,
      errorDelivered: false,
      stopRequested: false,
      stopNoticeMessageId: undefined,
    });

    await adapter.handleIncomingEvent({
      sender: {
        sender_id: { open_id: 'clearer-open-id' },
        sender_type: 'user',
      },
      message: {
        message_id: 'incoming-clear',
        chat_id: 'chat-busy-clear',
        chat_type: 'group',
        message_type: 'text',
        content: JSON.stringify({ text: '@_user_1 clear' }),
        create_time: String(Date.now()),
        mentions: [
          {
            key: '@_user_1',
            id: { open_id: 'bot-open-id' },
            name: 'bridge-bot',
          },
        ],
      },
    });

    assert.equal(calls.length, 1);
    assert.deepEqual(extractMentionReplyContent(calls[0]), {
      userId: 'clearer-open-id',
      text: ' \u6536\u5230\uff0c\u505c\u5b8c\u8fd9\u6761\u5c31\u6e05\u6389',
    });
    assert.equal((adapter as any).queue.length, 1);
    assert.equal((adapter as any).queue[0].text, '/stop');

    adapter.onMessageEnd('chat-busy-clear');
    await flushAsyncWork();

    assert.deepEqual(store.getMessages(session.id), { messages: [] });
  });
});

describe('FeishuAdapter reply image context', () => {
  it('downloads attachments from the replied message and forwards them with the current task', async () => {
    initTestContext();
    const adapter = new FeishuAdapter();

    (adapter as any).restClient = makeReplyAwareRestClient();

    await adapter.handleIncomingEvent({
      sender: {
        sender_id: { open_id: 'user-open-id' },
        sender_type: 'user',
      },
      message: {
        message_id: 'incoming-reply-task',
        parent_id: 'reply-msg-1',
        root_id: 'reply-msg-1',
        chat_id: 'chat-reply',
        chat_type: 'p2p',
        message_type: 'text',
        content: JSON.stringify({ text: '帮我把这张图做成游戏 GUI 语义线框图' }),
        create_time: String(Date.now()),
      },
    } as any);

    assert.equal((adapter as any).queue.length, 1);
    const inbound = (adapter as any).queue[0];
    assert.equal(inbound.text.startsWith('帮我把这张图做成游戏 GUI 语义线框图'), true);
    assert.equal(inbound.text.includes('[Reply context]'), true);
    assert.equal(inbound.text.includes('Attached 1 file(s) from the replied message.'), true);
    assert.equal(inbound.attachments?.length, 1);
    assert.equal(inbound.attachments[0].name, 'img-reply-1.png');
    assert.equal(Buffer.from(inbound.attachments[0].data, 'base64').toString(), 'reply-image');
  });

  it('does not contaminate /perm replies with replied-image context', async () => {
    initTestContext();
    const adapter = new FeishuAdapter();

    (adapter as any).restClient = makeReplyAwareRestClient();

    await adapter.handleIncomingEvent({
      sender: {
        sender_id: { open_id: 'user-open-id' },
        sender_type: 'user',
      },
      message: {
        message_id: 'incoming-perm-reply',
        parent_id: 'reply-msg-1',
        root_id: 'reply-msg-1',
        chat_id: 'chat-reply',
        chat_type: 'p2p',
        message_type: 'text',
        content: JSON.stringify({ text: '/perm allow req-123' }),
        create_time: String(Date.now()),
      },
    } as any);

    assert.equal((adapter as any).queue.length, 1);
    const inbound = (adapter as any).queue[0];
    assert.equal(inbound.text, '/perm allow req-123');
    assert.equal(inbound.callbackData, 'perm:allow:req-123');
    assert.equal(inbound.attachments, undefined);
  });
});

describe('FeishuAdapter task completion notices', () => {
  it('mentions the requester with completion text after a successful task finishes', async () => {
    initTestContext();
    const adapter = new FeishuAdapter();
    const { client, calls } = makeMockRestClient();

    (adapter as any).restClient = client;
    (adapter as any).taskStates.set('chat-done', {
      requesterUserId: 'owner-open-id',
      requesterMessageId: 'incoming-owner',
      responseDelivered: true,
      errorDelivered: false,
      stopRequested: false,
      stopNoticeMessageId: undefined,
    });

    adapter.onMessageEnd('chat-done');
    await flushAsyncWork();

    assert.equal(calls.length, 1);
    assert.equal(calls[0].kind, 'reply');
    assert.deepEqual(extractMentionReplyContent(calls[0]), {
      userId: 'owner-open-id',
      text: ' \u641e\u5b8c\u5566',
    });
    assert.equal((adapter as any).taskStates.has('chat-done'), false);
  });
});

describe('FeishuAdapter stop suppression', () => {
  it('suppresses bridge stop/status/error messages after a busy stop request', async () => {
    initTestContext();
    const adapter = new FeishuAdapter();
    const { client, calls } = makeMockRestClient();

    (adapter as any).restClient = client;
    (adapter as any).taskStates.set('chat-stop', {
      requesterUserId: 'owner-open-id',
      requesterMessageId: 'incoming-owner',
      responseDelivered: false,
      errorDelivered: false,
      stopRequested: true,
      stopNoticeMessageId: 'stop-notice-1',
    });

    const plainResult = await adapter.send({
      address: { channelType: 'feishu', chatId: 'chat-stop' },
      text: 'Stopping current task...',
      parseMode: 'plain',
    });
    const htmlResult = await adapter.send({
      address: { channelType: 'feishu', chatId: 'chat-stop' },
      text: '<p>Task stopped by user</p>',
      parseMode: 'HTML',
    });
    const markdownResult = await adapter.send({
      address: { channelType: 'feishu', chatId: 'chat-stop' },
      text: 'partial answer',
      parseMode: 'Markdown',
      replyToMessageId: 'incoming-owner',
    });

    assert.deepEqual(plainResult, { ok: true, messageId: 'stop-notice-1' });
    assert.deepEqual(htmlResult, { ok: true, messageId: 'stop-notice-1' });
    assert.deepEqual(markdownResult, { ok: true, messageId: 'stop-notice-1' });
    assert.equal(calls.length, 0);
  });
});

describe('Feishu formatting helpers', () => {
  it('prefers cards for structured markdown replies', () => {
    assert.equal(
      shouldPreferFeishuCard('# Title\n\n- one\n- two\n\nParagraph'),
      true,
    );
  });

  it('builds segmented card content for better spacing', () => {
    const card = JSON.parse(buildReadableFeishuCardContent('# Title\n\nFirst paragraph\n\n## Next\n\nSecond paragraph')) as {
      body?: { elements?: Array<{ tag?: string; content?: string }> };
    };
    const elements = card.body?.elements ?? [];
    assert.equal(elements.length, 4);
    assert.deepEqual(
      elements.map((element) => element.content),
      ['# Title', 'First paragraph', '## Next', 'Second paragraph'],
    );
  });

  it('disables preview and forces cards when the setting is enabled', async () => {
    initTestContext([
      ['bridge_feishu_force_card', 'true'],
    ]);
    const adapter = new FeishuAdapter();
    const { client, calls } = makeMockRestClient();

    (adapter as any).restClient = client;

    assert.equal(adapter.getPreviewCapabilities('chat-card'), null);

    const result = await adapter.send({
      address: { channelType: 'feishu', chatId: 'chat-card' },
      text: 'Plain paragraph\n\nSecond paragraph',
      parseMode: 'Markdown',
      replyToMessageId: 'incoming-card',
    });

    assert.equal(result.ok, true);
    assert.equal(calls.length, 1);
    const payload = calls[0].payload.data as { msg_type?: string };
    assert.equal(payload.msg_type, 'interactive');
  });
});

describe('FeishuAdapter clear command', () => {
  it('clears session context immediately for an idle chat', async () => {
    const store = initTestContext();
    const adapter = new FeishuAdapter();
    const { client, calls } = makeMockRestClient();

    (adapter as any).restClient = client;

    const session = store.createSession('test', 'model', undefined, '/tmp');
    store.upsertChannelBinding({
      channelType: 'feishu',
      chatId: 'chat-clear',
      codepilotSessionId: session.id,
      workingDirectory: '/tmp',
      model: 'model',
    });
    store.addMessage(session.id, 'user', 'old question');
    store.addMessage(session.id, 'assistant', 'old answer');
    store.updateSdkSessionId(session.id, 'sdk-old');

    await adapter.handleIncomingEvent({
      sender: {
        sender_id: { open_id: 'user-open-id' },
        sender_type: 'user',
      },
      message: {
        message_id: 'incoming-clear-idle',
        chat_id: 'chat-clear',
        chat_type: 'p2p',
        message_type: 'text',
        content: JSON.stringify({ text: 'clear' }),
        create_time: '1700000000000',
      },
    } as any);

    assert.equal((adapter as any).queue.length, 0);
    assert.equal(calls.length, 1);
    assert.equal(extractTextReplyContent(calls[0]), '\u6e05\u6389\u4e86\uff0c\u4ece\u8fd9\u6761\u4e4b\u540e\u91cd\u65b0\u7b97');
    assert.deepEqual(store.getMessages(session.id), { messages: [] });
    assert.equal(store.getChannelBinding('feishu', 'chat-clear')?.sdkSessionId, '');
    assert.equal(store.getChannelOffset('feishu_history_backfill:chat-clear'), '1700000000000');

    const cachePath = path.join(CTI_HOME, 'data', 'feishu-history-cache', `${session.id}.json`);
    const parsed = JSON.parse(fs.readFileSync(cachePath, 'utf-8')) as { messages: unknown[]; appliedToFreshSession: boolean };
    assert.deepEqual(parsed.messages, []);
    assert.equal(parsed.appliedToFreshSession, true);
  });
});

import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';

import type {
  FileAttachment,
  InboundMessage,
  InlineButton,
  OutboundMessage,
  PreviewCapabilities,
  SendResult,
} from 'claude-to-im/src/lib/bridge/types.js';
import { getBridgeContext } from 'claude-to-im/src/lib/bridge/context.js';
import * as router from 'claude-to-im/src/lib/bridge/channel-router.js';
import type { BaseChannelAdapter } from 'claude-to-im/src/lib/bridge/channel-adapter.js';
import { registerAdapterFactory } from 'claude-to-im/src/lib/bridge/channel-adapter.js';
import { FeishuAdapter as UpstreamFeishuAdapter } from 'claude-to-im/src/lib/bridge/adapters/feishu-adapter.js';
import {
  buildPostContent,
  hasComplexMarkdown,
  htmlToFeishuMarkdown,
  preprocessFeishuMarkdown,
} from 'claude-to-im/src/lib/bridge/markdown/feishu.js';
import { disableFeishuHistoryBackfill } from './feishu-history.js';
import { JsonFileStore } from './store.js';

type FeishuMention = {
  key?: string;
  id?: { open_id?: string; union_id?: string; user_id?: string };
  name?: string;
};

type FeishuMessageEventData = {
  sender: {
    sender_id?: {
      open_id?: string;
      union_id?: string;
      user_id?: string;
    };
    sender_type: string;
    tenant_key?: string;
  };
  message: {
    message_id: string;
    root_id?: string;
    parent_id?: string;
    chat_id: string;
    chat_type: string;
    message_type: string;
    content: string;
    create_time: string;
    mentions?: FeishuMention[];
  };
};

type FeishuHistorySender = {
  id?: {
    open_id?: string;
    union_id?: string;
    user_id?: string;
  };
  sender_type?: string;
};

type FeishuHistoryItem = {
  message_id?: string;
  msg_type?: string;
  create_time?: string;
  chat_id?: string;
  deleted?: boolean;
  sender?: FeishuHistorySender;
  mentions?: FeishuMention[];
  body?: {
    content?: string;
  };
};

const BaseFeishuAdapter = UpstreamFeishuAdapter as unknown as new () => any;

interface FeishuPreviewState {
  draftId: number;
  replyToMessageId?: string;
  lastRenderedText: string;
  lastMessageId?: string;
  previewSent: boolean;
  pendingSend?: Promise<'sent' | 'skip'>;
}

interface FeishuTaskState {
  requesterUserId?: string;
  requesterMessageId?: string;
  responseDelivered: boolean;
  errorDelivered: boolean;
  stopRequested: boolean;
  stopNoticeMessageId?: string;
  clearRequested?: boolean;
  clearRequesterUserId?: string;
  clearMessageId?: string;
  clearBeforeMessageMs?: number;
}

interface FeishuRecentSend {
  sentAt: number;
  messageId?: string;
}

interface FeishuReplyContext {
  sourceMessageId: string;
  text: string;
  attachments: FileAttachment[];
}

function parseBoolean(value: string | undefined, fallback: boolean): boolean {
  if (value === undefined) return fallback;
  const normalized = value.trim().toLowerCase();
  if (normalized === 'true') return true;
  if (normalized === 'false') return false;
  return fallback;
}

function parsePositiveInt(value: string | undefined, fallback: number): number {
  const parsed = Number.parseInt(value || '', 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function formatAttachmentSize(size: number): string {
  if (!Number.isFinite(size) || size <= 0) return 'unknown size';
  if (size >= 1024 * 1024) return `${(size / (1024 * 1024)).toFixed(1)} MB`;
  if (size >= 1024) return `${(size / 1024).toFixed(1)} KB`;
  return `${size} B`;
}

function normalizeFeishuMarkdownLayout(text: string): string {
  return text
    .replace(/\r\n/g, '\n')
    .replace(/[ \t]+\n/g, '\n')
    .replace(/([^\n])(\n#{1,6}\s)/g, '$1\n$2')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

function splitFeishuCardSections(text: string): string[] {
  const sections: string[] = [];
  const lines = text.split('\n');
  const buffer: string[] = [];
  let inFence = false;

  const flush = () => {
    const section = buffer.join('\n').trim();
    buffer.length = 0;
    if (section) {
      sections.push(section);
    }
  };

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('```')) {
      if (!inFence && buffer.length > 0) {
        flush();
      }
      buffer.push(line);
      inFence = !inFence;
      if (!inFence) {
        flush();
      }
      continue;
    }

    if (!inFence && /^#{1,6}\s/.test(trimmed) && buffer.length > 0) {
      flush();
    }

    if (!inFence && trimmed === '') {
      flush();
      continue;
    }

    buffer.push(line);
  }

  flush();
  return sections;
}

export function buildReadableFeishuCardContent(text: string): string {
  const content = normalizeFeishuMarkdownLayout(text);
  const sections = splitFeishuCardSections(content);
  return JSON.stringify({
    schema: '2.0',
    config: {
      wide_screen_mode: true,
    },
    body: {
      elements: (sections.length > 0 ? sections : [content]).map((section) => ({
        tag: 'markdown',
        content: section,
      })),
    },
  });
}

export function shouldPreferFeishuCard(text: string): boolean {
  if (hasComplexMarkdown(text)) return true;
  if (/^#{1,6}\s/m.test(text)) return true;
  if (/^>\s/m.test(text)) return true;
  if (/^[-*+]\s/m.test(text)) return true;
  if (/^\d+\.\s/m.test(text)) return true;
  if (/\n\s*\n/.test(text) && text.length > 120) return true;
  return false;
}

function longestCommonPrefixLength(a: string, b: string): number {
  const limit = Math.min(a.length, b.length);
  let index = 0;
  while (index < limit && a[index] === b[index]) {
    index += 1;
  }
  return index;
}

function resolveStreamPrefix(fullText: string, streamedText: string): string {
  if (!streamedText) return '';
  if (fullText.startsWith(streamedText)) return streamedText;

  if (streamedText.endsWith('...')) {
    const trimmed = streamedText.slice(0, -3);
    if (trimmed && fullText.startsWith(trimmed)) {
      return trimmed;
    }
  }

  const prefixLength = longestCommonPrefixLength(fullText, streamedText);
  return fullText.slice(0, prefixLength);
}

export function computeFeishuPreviewDelta(previousRenderedText: string, nextRenderedText: string): string {
  const prefix = resolveStreamPrefix(nextRenderedText, previousRenderedText);
  return nextRenderedText.slice(prefix.length);
}

export function computeFeishuFinalRemainder(streamedText: string, finalText: string): string {
  const prefix = resolveStreamPrefix(finalText, streamedText);
  return finalText.slice(prefix.length);
}

export function isFeishuStopCommandText(text: string): boolean {
  return text.replace(/\s+/g, '').toLowerCase() === 'stop';
}

export function isFeishuClearCommandText(text: string): boolean {
  const normalized = text.replace(/\s+/g, '').toLowerCase();
  return normalized === 'clear' || normalized === '/clear';
}

const FEISHU_BUSY_NOTICE = '\u5728\u5fd9\uff0c\u522b\u5435';
const FEISHU_STOP_NOTICE = '\u505c\u4e86\uff0c\u4e0d\u641e\u4e86';
const FEISHU_COMPLETION_NOTICE = '\u641e\u5b8c\u5566';
const FEISHU_CLEAR_NOTICE = '\u6e05\u6389\u4e86\uff0c\u4ece\u8fd9\u6761\u4e4b\u540e\u91cd\u65b0\u7b97';
const FEISHU_BUSY_CLEAR_NOTICE = '\u6536\u5230\uff0c\u505c\u5b8c\u8fd9\u6761\u5c31\u6e05\u6389';
const FEISHU_SEND_DEDUP_WINDOW_MS = 15_000;

export function buildMentionPostContent(userId: string, text: string): string {
  return JSON.stringify({
    zh_cn: {
      content: [[
        { tag: 'at', user_id: userId },
        { tag: 'text', text: ` ${text}` },
      ]],
    },
  });
}

export function buildBusyMentionPostContent(userId: string, text: string): string {
  return buildMentionPostContent(userId, text);
}

export function computeBackfillWindow(
  lastSyncedMs: number,
  currentMessageMs: number,
  lookbackHours: number,
): { startMs: number; endMs: number } | null {
  if (!Number.isFinite(currentMessageMs) || currentMessageMs <= 0) return null;
  const lookbackMs = Math.max(1, lookbackHours) * 60 * 60 * 1000;
  const startMs = lastSyncedMs > 0
    ? lastSyncedMs + 1
    : Math.max(0, currentMessageMs - lookbackMs);
  const endMs = currentMessageMs - 1;
  if (startMs > endMs) return null;
  return { startMs, endMs };
}

export function buildStoredInboundContent(
  text: string,
  attachments: FileAttachment[] | undefined,
  workDir: string | undefined,
  messageId: string,
): string {
  const trimmedText = text.trim();
  if (!attachments || attachments.length === 0) {
    return trimmedText;
  }

  if (workDir) {
    try {
      const uploadDir = path.join(workDir, '.codepilot-uploads');
      fs.mkdirSync(uploadDir, { recursive: true });
      const fileMeta = attachments.map((file, index) => {
        const safeName = path.basename(file.name).replace(/[^a-zA-Z0-9._-]/g, '_');
        const filePath = path.join(uploadDir, `${messageId}-${index}-${safeName}`);
        const buffer = Buffer.from(file.data, 'base64');
        fs.writeFileSync(filePath, buffer);
        return {
          id: file.id,
          name: file.name,
          type: file.type,
          size: buffer.length,
          filePath,
        };
      });
      return `<!--files:${JSON.stringify(fileMeta)}-->${trimmedText}`;
    } catch (err) {
      console.warn('[feishu-adapter] Failed to persist historical attachments:', err instanceof Error ? err.message : err);
    }
  }

  const summary = attachments
    .map((file) => `${file.name} (${file.type}, ${formatAttachmentSize(file.size)})`)
    .join('; ');
  return [`Attached files: ${summary}`, trimmedText].filter(Boolean).join('\n');
}

export class FeishuAdapter extends BaseFeishuAdapter {
  private historySyncs = new Map<string, Promise<void>>();
  private busyChats = new Set<string>();
  private previewStates = new Map<string, FeishuPreviewState>();
  private taskStates = new Map<string, FeishuTaskState>();
  private recentSends = new Map<string, FeishuRecentSend>();

  private forceCardReplies(): boolean {
    try {
      return getBridgeContext().store.getSetting('bridge_feishu_force_card') === 'true';
    } catch {
      return process.env.CTI_FEISHU_FORCE_CARD === 'true';
    }
  }

  private hideToolMetadata(): boolean {
    try {
      return getBridgeContext().store.getSetting('bridge_feishu_hide_tool_metadata') === 'true';
    } catch {
      return process.env.CTI_FEISHU_HIDE_TOOL_METADATA === 'true';
    }
  }

  private streamingPreviewEnabled(): boolean {
    return !this.forceCardReplies() && !this.hideToolMetadata();
  }

  async handleIncomingEvent(data: FeishuMessageEventData): Promise<void> {
    try {
      if (await this.handleClearCommandIfNeeded(data)) {
        return;
      }
      if (await this.rejectBusyMentionIfNeeded(data)) {
        return;
      }
      this.noteTaskRequester(data);
      const originalEnqueue = (this as any).enqueue?.bind(this) as ((msg: InboundMessage) => void) | undefined;
      const replyContext = await this.buildReplyContextForMessage(data.message);

      if (replyContext && originalEnqueue) {
        (this as any).enqueue = (msg: InboundMessage) => {
          originalEnqueue(this.mergeReplyContextIntoInbound(msg, replyContext));
        };
      }

      try {
        try {
          await this.backfillHistoryBeforeMessage(data);
        } catch (err) {
          console.warn(
            '[feishu-adapter] History backfill failed, continuing without it:',
            err instanceof Error ? err.message : err,
          );
        }
        await (BaseFeishuAdapter.prototype as any).processIncomingEvent.call(this, data);
      } finally {
        if (replyContext && originalEnqueue) {
          (this as any).enqueue = originalEnqueue;
        }
      }
    } catch (err) {
      console.error(
        '[feishu-adapter] Unhandled error in event handler:',
        err instanceof Error ? err.stack || err.message : err,
      );
    }
  }

  private historyEnabled(): boolean {
    return parseBoolean(process.env.CTI_FEISHU_HISTORY_SYNC, true);
  }

  private historyLookbackHours(): number {
    return parsePositiveInt(process.env.CTI_FEISHU_HISTORY_LOOKBACK_HOURS, 48);
  }

  private historyPageSize(): number {
    return parsePositiveInt(process.env.CTI_FEISHU_HISTORY_PAGE_SIZE, 50);
  }

  private historyMaxMessages(): number {
    return parsePositiveInt(process.env.CTI_FEISHU_HISTORY_MAX_MESSAGES, 40);
  }

  private historyOffsetKey(chatId: string): string {
    return `feishu_history_backfill:${chatId}`;
  }

  private extractSenderUserId(sender: FeishuMessageEventData['sender'] | FeishuHistorySender | undefined): string {
    const liveSender = sender as FeishuMessageEventData['sender'] | undefined;
    const historySender = sender as FeishuHistorySender | undefined;
    const ids = liveSender?.sender_id || historySender?.id;
    return ids?.open_id || ids?.user_id || ids?.union_id || '';
  }

  private isBotMentioned(mentions?: FeishuMention[]): boolean {
    return (BaseFeishuAdapter.prototype as any).isBotMentioned.call(this, mentions);
  }

  private stripMentionMarkers(text: string): string {
    return (BaseFeishuAdapter.prototype as any).stripMentionMarkers.call(this, text);
  }

  private parseTextContent(content: string): string {
    return (BaseFeishuAdapter.prototype as any).parseTextContent.call(this, content);
  }

  private parsePostContent(content: string): { extractedText: string; imageKeys: string[] } {
    return (BaseFeishuAdapter.prototype as any).parsePostContent.call(this, content);
  }

  private extractFileKey(content: string): string | null {
    return (BaseFeishuAdapter.prototype as any).extractFileKey.call(this, content);
  }

  private async downloadResource(messageId: string, fileKey: string, resourceType: string): Promise<FileAttachment | null> {
    return (BaseFeishuAdapter.prototype as any).downloadResource.call(this, messageId, fileKey, resourceType);
  }

  private getRepliedMessageId(message: FeishuMessageEventData['message']): string | null {
    const parentId = message.parent_id?.trim();
    if (parentId && parentId !== message.message_id) {
      return parentId;
    }

    const rootId = message.root_id?.trim();
    if (rootId && rootId !== message.message_id) {
      return rootId;
    }

    return null;
  }

  private async fetchMessageById(messageId: string): Promise<FeishuHistoryItem | null> {
    const self = this as any;
    const getMessage = self.restClient?.im?.message?.get;
    if (!getMessage) return null;

    const response = await getMessage({
      path: { message_id: messageId },
    });

    if (response?.code && response.code !== 0) {
      throw new Error(`message.get failed: ${response.msg || response.code}`);
    }

    const items = response?.data?.items;
    if (Array.isArray(items)) {
      return (items[0] as FeishuHistoryItem | undefined) || null;
    }
    if (items) {
      return items as FeishuHistoryItem;
    }

    const item = response?.data?.item;
    return item ? item as FeishuHistoryItem : null;
  }

  private async buildReplyContextForMessage(
    message: FeishuMessageEventData['message'],
  ): Promise<FeishuReplyContext | null> {
    const repliedMessageId = this.getRepliedMessageId(message);
    if (!repliedMessageId) return null;

    try {
      const item = await this.fetchMessageById(repliedMessageId);
      if (!item || item.deleted) return null;

      const inbound = await this.buildInboundFromHistoryItem(item, message.chat_type);
      if (!inbound?.attachments || inbound.attachments.length === 0) {
        return null;
      }

      return {
        sourceMessageId: repliedMessageId,
        text: inbound.text.trim(),
        attachments: inbound.attachments,
      };
    } catch (err) {
      console.warn(
        `[feishu-adapter] Failed to resolve replied message context for ${repliedMessageId}:`,
        err instanceof Error ? err.message : err,
      );
      return null;
    }
  }

  private mergeReplyContextIntoInbound(
    inbound: InboundMessage,
    replyContext: FeishuReplyContext,
  ): InboundMessage {
    if (inbound.callbackData) {
      return inbound;
    }

    const replyLines = [
      '[Reply context]',
      `Attached ${replyContext.attachments.length} file(s) from the replied message.`,
    ];
    if (replyContext.text) {
      replyLines.push(`Original replied message text: ${replyContext.text}`);
    }

    const mergedText = [inbound.text.trim(), replyLines.join('\n')]
      .filter(Boolean)
      .join('\n\n');

    return {
      ...inbound,
      text: mergedText,
      attachments: [...(inbound.attachments ?? []), ...replyContext.attachments],
      raw: {
        ...(typeof inbound.raw === 'object' && inbound.raw !== null ? inbound.raw as Record<string, unknown> : {}),
        replyContext: {
          sourceMessageId: replyContext.sourceMessageId,
          attachmentCount: replyContext.attachments.length,
        },
      },
    };
  }

  onMessageStart(chatId: string): void {
    this.busyChats.add(chatId);
    (BaseFeishuAdapter.prototype as any).onMessageStart?.call(this, chatId);
  }

  onMessageEnd(chatId: string): void {
    this.busyChats.delete(chatId);
    this.previewStates.delete(chatId);
    (BaseFeishuAdapter.prototype as any).onMessageEnd?.call(this, chatId);
    void this.finishTask(chatId);
  }

  getPreviewCapabilities(_chatId: string): PreviewCapabilities | null {
    if (!this.streamingPreviewEnabled()) {
      return null;
    }
    return { supported: true, privateOnly: false };
  }

  async sendPreview(
    chatId: string,
    text: string,
    draftId: number,
  ): Promise<'sent' | 'skip' | 'degrade'> {
    if (!this.streamingPreviewEnabled()) {
      this.previewStates.delete(chatId);
      return 'skip';
    }

    const replyToMessageId = (this as any).lastIncomingMessageId?.get(chatId) as string | undefined;
    const current = this.previewStates.get(chatId);
    const state = current && current.draftId === draftId
      ? current
      : {
          draftId,
          replyToMessageId,
          lastRenderedText: '',
          lastMessageId: undefined,
          previewSent: false,
          pendingSend: undefined,
        };
    this.previewStates.set(chatId, state);

    const previousPendingSend = state.pendingSend ?? Promise.resolve<'sent' | 'skip'>('sent');
    const queuedSend = previousPendingSend
      .catch(() => 'skip' as const)
      .then(async () => {
        if (this.previewStates.get(chatId) !== state || state.draftId !== draftId) {
          return 'skip' as const;
        }

        const delta = computeFeishuPreviewDelta(state.lastRenderedText, text);
        if (!delta.trim()) {
          return 'sent' as const;
        }

        const result = await this.sendAsText(chatId, delta, state.replyToMessageId);
        if (!result.ok) {
          console.warn('[feishu-adapter] Stream preview send failed:', result.error || 'unknown error');
          return 'skip' as const;
        }

        if (this.previewStates.get(chatId) === state) {
          state.lastRenderedText = text;
          state.lastMessageId = result.messageId;
          state.previewSent = true;
        }
        const taskState = this.taskStates.get(chatId);
        if (taskState) {
          taskState.responseDelivered = true;
        }
        return 'sent' as const;
      });
    let trackedSend: Promise<'sent' | 'skip'>;
    trackedSend = queuedSend.finally(() => {
      if (this.previewStates.get(chatId) === state && state.pendingSend === trackedSend) {
        state.pendingSend = undefined;
      }
    });
    state.pendingSend = trackedSend;
    return trackedSend;
  }

  endPreview(chatId: string, draftId: number): void {
    const state = this.previewStates.get(chatId);
    if (!state || state.draftId === draftId) {
      this.previewStates.delete(chatId);
    }
  }

  async send(message: OutboundMessage): Promise<SendResult> {
    const taskState = this.taskStates.get(message.address.chatId);
    if (taskState?.stopRequested && this.shouldSuppressStoppedTaskMessage(message, taskState)) {
      return { ok: true, messageId: taskState.stopNoticeMessageId };
    }

    let previewState = this.previewStates.get(message.address.chatId);
    if (previewState?.pendingSend) {
      await previewState.pendingSend.catch(() => {});
      previewState = this.previewStates.get(message.address.chatId);
    }
    let text = message.text;
    let parseMode = message.parseMode;

    if (
      previewState?.previewSent &&
      previewState.replyToMessageId &&
      message.replyToMessageId === previewState.replyToMessageId &&
      !message.inlineButtons
    ) {
      const remainder = computeFeishuFinalRemainder(previewState.lastRenderedText, text);
      if (!remainder.trim()) {
        if (taskState) {
          taskState.responseDelivered = true;
        }
        return { ok: true, messageId: previewState.lastMessageId };
      }
      text = remainder;
      parseMode = 'plain';
    }

    const result = await this.sendFormattedMessage({
      ...message,
      text,
      parseMode,
    });
    if (result.ok && taskState) {
      if (message.parseMode === 'Markdown' && !message.inlineButtons) {
        taskState.responseDelivered = true;
      } else if (message.parseMode === 'HTML' && !message.inlineButtons) {
        taskState.errorDelivered = true;
      }
    }
    return result;
  }

  private shouldIncludeChat(chatId: string, mentions?: FeishuMention[]): boolean {
    const store = getBridgeContext().store;
    const policy = store.getSetting('bridge_feishu_group_policy') || 'open';

    if (policy === 'disabled') {
      return false;
    }

    if (policy === 'allowlist') {
      const allowedGroups = (store.getSetting('bridge_feishu_group_allow_from') || '')
        .split(',')
        .map((item) => item.trim())
        .filter(Boolean);
      if (!allowedGroups.includes(chatId)) {
        return false;
      }
    }

    const requireMention = store.getSetting('bridge_feishu_require_mention') !== 'false';
    if (requireMention && !this.isBotMentioned(mentions)) {
      return false;
    }

    return true;
  }

  private async rejectBusyMentionIfNeeded(data: FeishuMessageEventData): Promise<boolean> {
    const msg = data.message;
    const sender = data.sender;
    if (sender.sender_type === 'bot') return false;
    if (msg.chat_type !== 'group') return false;
    if (!this.busyChats.has(msg.chat_id)) return false;
    if (!this.isBotMentioned(msg.mentions)) return false;

    const chatId = msg.chat_id;
    const userId = this.extractSenderUserId(sender);
    const self = this as any;

    if (!userId || !self.isAuthorized(userId, chatId)) {
      return false;
    }
    if (!this.shouldIncludeChat(chatId, msg.mentions)) {
      return false;
    }

    const rawText = this.extractComparableText(msg);
    if (isFeishuClearCommandText(rawText)) {
      const result = await this.clearBusyTask(chatId, userId, msg.message_id, Number.parseInt(msg.create_time, 10) || Date.now());
      if (!result.ok) {
        console.warn('[feishu-adapter] Busy clear reply failed:', result.error || 'unknown error');
      }
    } else if (isFeishuStopCommandText(rawText)) {
      const result = await this.stopBusyTask(chatId, userId, msg.message_id);
      if (!result.ok) {
        console.warn('[feishu-adapter] Busy stop reply failed:', result.error || 'unknown error');
      }
    } else {
      const result = await this.sendBusyNotice(chatId, userId, msg.message_id);
      if (!result.ok) {
        console.warn('[feishu-adapter] Busy reply failed:', result.error || 'unknown error');
      }
    }

    try {
      getBridgeContext().store.insertAuditLog({
        channelType: 'feishu',
        chatId,
        direction: 'inbound',
        messageId: msg.message_id,
        summary: isFeishuClearCommandText(rawText)
          ? '[BUSY] Clear requested while previous @mention is still running'
          : isFeishuStopCommandText(rawText)
          ? '[BUSY] Stop requested while previous @mention is still running'
          : '[BUSY] Rejected while previous @mention is still running',
      });
    } catch {
      // Best effort.
    }

    return true;
  }

  private noteTaskRequester(data: FeishuMessageEventData): void {
    const msg = data.message;
    const sender = data.sender;
    if (sender.sender_type === 'bot') return;

    const chatId = msg.chat_id;
    const userId = this.extractSenderUserId(sender);
    const self = this as any;
    if (!userId || !self.isAuthorized(userId, chatId)) {
      return;
    }
    if (msg.chat_type === 'group' && !this.shouldIncludeChat(chatId, msg.mentions)) {
      return;
    }

    this.taskStates.set(chatId, {
      requesterUserId: userId,
      requesterMessageId: msg.message_id,
      responseDelivered: false,
      errorDelivered: false,
      stopRequested: false,
      stopNoticeMessageId: undefined,
    });
  }

  private extractComparableText(message: FeishuMessageEventData['message']): string {
    let rawText = '';
    if (message.message_type === 'text') {
      rawText = this.parseTextContent(message.content);
    } else if (message.message_type === 'post') {
      rawText = this.parsePostContent(message.content).extractedText;
    }
    return this.stripMentionMarkers(rawText);
  }

  private async stopBusyTask(
    chatId: string,
    stopSenderUserId: string,
    stopMessageId: string,
  ): Promise<SendResult> {
    const existing = this.taskStates.get(chatId);
    const requesterUserId = existing?.requesterUserId || stopSenderUserId;
    const requesterMessageId = existing?.requesterMessageId;
    const taskState: FeishuTaskState = existing || {
      requesterUserId,
      requesterMessageId,
      responseDelivered: false,
      errorDelivered: false,
      stopRequested: false,
      stopNoticeMessageId: undefined,
    };

    taskState.requesterUserId = requesterUserId;
    taskState.requesterMessageId = requesterMessageId;
    taskState.stopRequested = true;
    taskState.errorDelivered = false;
    this.taskStates.set(chatId, taskState);

    (this as any).enqueue({
      messageId: `${stopMessageId}:stop`,
      address: {
        channelType: 'feishu',
        chatId,
        userId: stopSenderUserId,
      },
      text: '/stop',
      timestamp: Date.now(),
      raw: { syntheticBusyStop: true },
    } satisfies InboundMessage);

    const result = await this.sendMentionNotice(chatId, requesterUserId, FEISHU_STOP_NOTICE, stopMessageId);
    if (result.ok) {
      taskState.stopNoticeMessageId = result.messageId;
    }
    return result;
  }

  private async clearBusyTask(
    chatId: string,
    clearSenderUserId: string,
    clearMessageId: string,
    clearBeforeMessageMs: number,
  ): Promise<SendResult> {
    const existing = this.taskStates.get(chatId);
    const taskState: FeishuTaskState = existing || {
      requesterUserId: clearSenderUserId,
      requesterMessageId: clearMessageId,
      responseDelivered: false,
      errorDelivered: false,
      stopRequested: false,
      stopNoticeMessageId: undefined,
    };

    taskState.stopRequested = true;
    taskState.errorDelivered = false;
    taskState.clearRequested = true;
    taskState.clearRequesterUserId = clearSenderUserId;
    taskState.clearMessageId = clearMessageId;
    taskState.clearBeforeMessageMs = clearBeforeMessageMs;
    this.taskStates.set(chatId, taskState);

    (this as any).enqueue({
      messageId: `${clearMessageId}:clear`,
      address: {
        channelType: 'feishu',
        chatId,
        userId: clearSenderUserId,
      },
      text: '/stop',
      timestamp: Date.now(),
      raw: { syntheticBusyClear: true },
    } satisfies InboundMessage);

    const result = await this.sendMentionNotice(chatId, clearSenderUserId, FEISHU_BUSY_CLEAR_NOTICE, clearMessageId);
    if (result.ok) {
      taskState.stopNoticeMessageId = result.messageId;
    }
    return result;
  }

  private async handleClearCommandIfNeeded(data: FeishuMessageEventData): Promise<boolean> {
    const msg = data.message;
    const sender = data.sender;
    if (sender.sender_type === 'bot') return false;

    const rawText = this.extractComparableText(msg);
    if (!isFeishuClearCommandText(rawText)) return false;

    const chatId = msg.chat_id;
    if (this.busyChats.has(chatId)) return false;
    const userId = this.extractSenderUserId(sender);
    const self = this as any;
    if (!userId || !self.isAuthorized(userId, chatId)) {
      return false;
    }

    if (msg.chat_type === 'group' && !this.shouldIncludeChat(chatId, msg.mentions)) {
      return false;
    }

    const clearBeforeMessageMs = Number.parseInt(msg.create_time, 10) || Date.now();
    await this.clearChatContext(chatId, clearBeforeMessageMs);

    try {
      getBridgeContext().store.insertAuditLog({
        channelType: 'feishu',
        chatId,
        direction: 'inbound',
        messageId: msg.message_id,
        summary: '[COMMAND] Cleared session context for chat',
      });
    } catch {
      // Best effort.
    }

    const result = msg.chat_type === 'group'
      ? await this.sendMentionNotice(chatId, userId, FEISHU_CLEAR_NOTICE, msg.message_id)
      : await this.sendAsText(chatId, FEISHU_CLEAR_NOTICE, msg.message_id);
    if (!result.ok) {
      console.warn('[feishu-adapter] Clear reply failed:', result.error || 'unknown error');
    }
    return true;
  }

  private async clearChatContext(
    chatId: string,
    clearBeforeMessageMs: number,
  ): Promise<{ sessionId: string; removedMessages: number; removedFiles: number }> {
    const store = getBridgeContext().store as JsonFileStore;
    const binding = router.resolve({
      channelType: 'feishu',
      chatId,
    });

    store.setChannelOffset(this.historyOffsetKey(chatId), String(clearBeforeMessageMs));

    const sessionId = binding.codepilotSessionId;
    const result = typeof store.clearSessionContext === 'function'
      ? store.clearSessionContext(sessionId)
      : { removedMessages: 0, removedFiles: 0 };

    store.updateSdkSessionId(sessionId, '');
    disableFeishuHistoryBackfill(sessionId, binding);

    return {
      sessionId,
      removedMessages: result.removedMessages,
      removedFiles: result.removedFiles,
    };
  }

  private shouldSuppressStoppedTaskMessage(
    message: OutboundMessage,
    taskState: FeishuTaskState,
  ): boolean {
    if (message.inlineButtons && message.inlineButtons.length > 0) {
      return true;
    }
    if (message.parseMode === 'Markdown' && message.replyToMessageId === taskState.requesterMessageId) {
      return true;
    }
    if (
      message.parseMode === 'plain' &&
      (message.text === 'Stopping current task...' || message.text === 'No task is currently running.')
    ) {
      return true;
    }
    if (message.parseMode === 'HTML' && /Task stopped by user/i.test(message.text)) {
      return true;
    }
    return false;
  }

  private async sendBusyNotice(
    chatId: string,
    userId: string,
    replyToMessageId?: string,
  ): Promise<SendResult> {
    const result = await this.sendMentionNotice(chatId, userId, FEISHU_BUSY_NOTICE, replyToMessageId);
    if (result.ok) {
      return result;
    }
    return this.sendAsText(chatId, FEISHU_BUSY_NOTICE, replyToMessageId);
  }

  private async sendMentionNotice(
    chatId: string,
    userId: string,
    text: string,
    replyToMessageId?: string,
  ): Promise<SendResult> {
    const content = buildMentionPostContent(userId, text);
    return this.sendPayload(chatId, 'post', content, replyToMessageId);
  }

  private async sendPayload(
    chatId: string,
    msgType: 'text' | 'post' | 'interactive',
    content: string,
    replyToMessageId?: string,
  ): Promise<SendResult> {
    const restClient = (this as any).restClient;
    if (!restClient) {
      return { ok: false, error: 'Feishu client not initialized' };
    }

    const dedupKey = this.buildSendDedupKey(chatId, msgType, content, replyToMessageId);
    const duplicateMessageId = this.findRecentDuplicateMessageId(dedupKey);
    if (duplicateMessageId !== null) {
      return { ok: true, messageId: duplicateMessageId || undefined };
    }

    try {
      const res = replyToMessageId
        ? await restClient.im.message.reply({
            path: { message_id: replyToMessageId },
            data: {
              msg_type: msgType,
              content,
            },
          })
        : await restClient.im.message.create({
            params: { receive_id_type: 'chat_id' },
            data: {
              receive_id: chatId,
              msg_type: msgType,
              content,
            },
          });

      if (res?.data?.message_id) {
        this.recordRecentSend(dedupKey, res.data.message_id);
        return { ok: true, messageId: res.data.message_id };
      }
      return { ok: false, error: res?.msg || 'Send failed' };
    } catch (err) {
      return { ok: false, error: err instanceof Error ? err.message : 'Send failed' };
    }
  }

  private async sendAsCard(chatId: string, text: string, replyToMessageId?: string): Promise<SendResult> {
    const cardContent = buildReadableFeishuCardContent(text);
    const result = await this.sendPayload(chatId, 'interactive', cardContent, replyToMessageId);
    if (result.ok) {
      return result;
    }
    console.warn('[feishu-adapter] Card send failed, falling back to post:', result.error || 'unknown error');
    return this.sendAsPost(chatId, text, replyToMessageId);
  }

  private async sendAsPost(chatId: string, text: string, replyToMessageId?: string): Promise<SendResult> {
    const postContent = buildPostContent(text);
    const result = await this.sendPayload(chatId, 'post', postContent, replyToMessageId);
    if (result.ok) {
      return result;
    }
    console.warn('[feishu-adapter] Post send failed, falling back to text:', result.error || 'unknown error');
    return this.sendAsText(chatId, text, replyToMessageId);
  }

  private async sendAsText(chatId: string, text: string, replyToMessageId?: string): Promise<SendResult> {
    return this.sendPayload(chatId, 'text', JSON.stringify({ text }), replyToMessageId);
  }

  private async sendPermissionCard(
    chatId: string,
    text: string,
    inlineButtons: InlineButton[][],
    replyToMessageId?: string,
  ): Promise<SendResult> {
    const permCommands = inlineButtons.flat().map((btn) => {
      if (btn.callbackData.startsWith('perm:')) {
        const parts = btn.callbackData.split(':');
        const action = parts[1];
        const permId = parts.slice(2).join(':');
        return `\`/perm ${action} ${permId}\``;
      }
      return btn.text;
    });

    const cardContent = [
      text,
      '',
      '---',
      '**Reply:**',
      '`1` - Allow once',
      '`2` - Allow session',
      '`3` - Deny',
      '',
      'Or use full commands:',
      ...permCommands,
    ].join('\n');

    const cardJson = JSON.stringify({
      schema: '2.0',
      config: { wide_screen_mode: true },
      header: {
        template: 'orange',
        title: { tag: 'plain_text', content: 'Permission Required' },
      },
      body: {
        elements: [
          { tag: 'markdown', content: cardContent },
        ],
      },
    });

    const result = await this.sendPayload(chatId, 'interactive', cardJson, replyToMessageId);
    if (result.ok) {
      return result;
    }

    const plainCommands = inlineButtons.flat().map((btn) => {
      if (btn.callbackData.startsWith('perm:')) {
        const parts = btn.callbackData.split(':');
        return `/perm ${parts[1]} ${parts.slice(2).join(':')}`;
      }
      return btn.text;
    });
    const fallbackText = text + '\n\nReply:\n1 - Allow once\n2 - Allow session\n3 - Deny\n\nOr use full command:\n' + plainCommands.join('\n');
    return this.sendAsText(chatId, fallbackText, replyToMessageId);
  }

  private async sendFormattedMessage(message: OutboundMessage): Promise<SendResult> {
    const chatId = message.address.chatId;
    let text = message.text;

    if (message.parseMode === 'HTML') {
      text = htmlToFeishuMarkdown(text);
    }

    if (message.parseMode === 'Markdown') {
      text = preprocessFeishuMarkdown(text);
    }

    if (message.parseMode !== 'plain') {
      text = normalizeFeishuMarkdownLayout(text);
    }

    if (message.inlineButtons && message.inlineButtons.length > 0) {
      return this.sendPermissionCard(chatId, text, message.inlineButtons, message.replyToMessageId);
    }

    if (message.parseMode === 'plain') {
      return this.sendAsText(chatId, text, message.replyToMessageId);
    }

    if (this.forceCardReplies()) {
      return this.sendAsCard(chatId, text, message.replyToMessageId);
    }

    if (shouldPreferFeishuCard(text)) {
      return this.sendAsCard(chatId, text, message.replyToMessageId);
    }

    return this.sendAsPost(chatId, text, message.replyToMessageId);
  }

  private async finishTask(chatId: string): Promise<void> {
    const taskState = this.taskStates.get(chatId);
    this.taskStates.delete(chatId);
    if (!taskState) return;
    if (taskState.clearRequested) {
      await this.clearChatContext(chatId, taskState.clearBeforeMessageMs || Date.now());
      return;
    }
    if (taskState.stopRequested || taskState.errorDelivered || !taskState.responseDelivered) {
      return;
    }
    if (!taskState.requesterUserId) {
      return;
    }

    const result = await this.sendMentionNotice(
      chatId,
      taskState.requesterUserId,
      FEISHU_COMPLETION_NOTICE,
      taskState.requesterMessageId,
    );
    if (!result.ok) {
      console.warn('[feishu-adapter] Completion notice failed:', result.error || 'unknown error');
    }
  }

  private buildSendDedupKey(
    chatId: string,
    msgType: 'text' | 'post' | 'interactive',
    content: string,
    replyToMessageId?: string,
  ): string {
    return [chatId, replyToMessageId || '', msgType, content].join('\u0000');
  }

  private findRecentDuplicateMessageId(dedupKey: string): string | '' | null {
    const now = Date.now();
    this.pruneRecentSends(now);
    const recent = this.recentSends.get(dedupKey);
    if (!recent) return null;
    if (now - recent.sentAt > FEISHU_SEND_DEDUP_WINDOW_MS) {
      this.recentSends.delete(dedupKey);
      return null;
    }
    return recent.messageId || '';
  }

  private recordRecentSend(dedupKey: string, messageId?: string): void {
    this.pruneRecentSends(Date.now());
    this.recentSends.set(dedupKey, {
      sentAt: Date.now(),
      messageId,
    });
  }

  private pruneRecentSends(now: number): void {
    for (const [key, recent] of this.recentSends) {
      if (now - recent.sentAt > FEISHU_SEND_DEDUP_WINDOW_MS) {
        this.recentSends.delete(key);
      }
    }
  }

  private async backfillHistoryBeforeMessage(data: FeishuMessageEventData): Promise<void> {
    const self = this as any;
    if (!this.historyEnabled() || !self.restClient) return;

    const msg = data.message;
    const sender = data.sender;
    if (sender.sender_type === 'bot') return;

    const chatId = msg.chat_id;
    const userId = this.extractSenderUserId(sender);
    if (!self.isAuthorized(userId, chatId)) return;

    const isGroup = msg.chat_type === 'group';
    if (isGroup && !this.shouldIncludeChat(chatId, msg.mentions)) {
      return;
    }

    const currentMessageMs = Number.parseInt(msg.create_time, 10) || Date.now();
    const { store } = getBridgeContext();
    const key = this.historyOffsetKey(chatId);
    const lastSyncedMs = Number.parseInt(store.getChannelOffset(key), 10) || 0;
    const window = computeBackfillWindow(lastSyncedMs, currentMessageMs, this.historyLookbackHours());

    if (!window) {
      store.setChannelOffset(key, String(currentMessageMs));
      return;
    }

    if (this.historySyncs.has(chatId)) {
      await this.historySyncs.get(chatId);
      return;
    }

    const syncPromise = this.runHistoryBackfill(data, window.startMs, window.endMs)
      .then(() => {
        store.setChannelOffset(key, String(currentMessageMs));
      })
      .finally(() => {
        this.historySyncs.delete(chatId);
      });

    this.historySyncs.set(chatId, syncPromise);
    await syncPromise;
  }

  private async runHistoryBackfill(
    data: FeishuMessageEventData,
    startMs: number,
    endMs: number,
  ): Promise<void> {
    const items = await this.listHistoryMessages(data.message.chat_id, startMs, endMs);
    if (items.length === 0) return;

    const address = {
      channelType: 'feishu' as const,
      chatId: data.message.chat_id,
      userId: this.extractSenderUserId(data.sender),
    };
    const binding = router.resolve(address);
    const { store } = getBridgeContext();
    const session = store.getSession(binding.codepilotSessionId);
    const workDir = binding.workingDirectory || session?.working_directory || '';

    let storedCount = 0;

    for (const item of items) {
      const messageId = item.message_id || '';
      if (!messageId || messageId === data.message.message_id || item.deleted) continue;

      const dedupKey = `feishu-history:${messageId}`;
      if (store.checkDedup(dedupKey)) continue;

      if (this.isHistoryMessageFromBot(item)) continue;

      const historyUserId = this.extractSenderUserId(item.sender);
      if (!this.shouldPersistHistoryItem(item, data.message.chat_type, historyUserId)) continue;

      const inbound = await this.buildInboundFromHistoryItem(item, data.message.chat_type);
      if (!inbound) continue;

      const savedContent = buildStoredInboundContent(inbound.text, inbound.attachments, workDir, messageId);
      store.addMessage(binding.codepilotSessionId, 'user', savedContent);
      store.insertDedup(dedupKey);

      try {
        const summary = inbound.attachments && inbound.attachments.length > 0
          ? `[history ${inbound.attachments.length} attachment(s)] ${inbound.text.slice(0, 150)}`
          : `[history] ${inbound.text.slice(0, 200)}`;
        store.insertAuditLog({
          channelType: 'feishu',
          chatId: data.message.chat_id,
          direction: 'inbound',
          messageId,
          summary,
        });
      } catch {
        // Best effort.
      }

      storedCount += 1;
    }

    if (storedCount > 0) {
      console.log(`[feishu-adapter] Backfilled ${storedCount} historical message(s) for chat ${data.message.chat_id}`);
    }
  }

  private async listHistoryMessages(
    chatId: string,
    startMs: number,
    endMs: number,
  ): Promise<FeishuHistoryItem[]> {
    const self = this as any;
    const results: FeishuHistoryItem[] = [];
    let pageToken: string | undefined;

    while (results.length < this.historyMaxMessages()) {
      const pageSize = Math.min(this.historyPageSize(), this.historyMaxMessages() - results.length);
      const response = await self.restClient.im.message.list({
        params: {
          container_id_type: 'chat',
          container_id: chatId,
          start_time: String(startMs),
          end_time: String(endMs),
          sort_type: 'ByCreateTimeAsc',
          page_size: pageSize,
          ...(pageToken ? { page_token: pageToken } : {}),
        },
      });

      if (response?.code && response.code !== 0) {
        throw new Error(`history message.list failed: ${response.msg || response.code}`);
      }

      const items = Array.isArray(response?.data?.items)
        ? response.data.items as FeishuHistoryItem[]
        : [];
      results.push(...items);

      if (!response?.data?.has_more || !response?.data?.page_token) {
        break;
      }
      pageToken = response.data.page_token;
    }

    return results;
  }

  private isHistoryMessageFromBot(item: FeishuHistoryItem): boolean {
    if (item.sender?.sender_type === 'bot') return true;
    const self = this as any;
    const ids = item.sender?.id
      ? [item.sender.id.open_id, item.sender.id.user_id, item.sender.id.union_id].filter(Boolean)
      : [];
    return ids.some((id) => self.botIds?.has(id));
  }

  private shouldPersistHistoryItem(
    item: FeishuHistoryItem,
    chatType: string,
    userId: string,
  ): boolean {
    const self = this as any;
    const chatId = item.chat_id || '';
    if (!chatId || !self.isAuthorized(userId, chatId)) return false;

    if (chatType === 'group' && !this.shouldIncludeChat(chatId, item.mentions)) {
      return false;
    }

    return true;
  }

  private async buildInboundFromHistoryItem(
    item: FeishuHistoryItem,
    chatType: string,
  ): Promise<InboundMessage | null> {
    const messageId = item.message_id || '';
    const chatId = item.chat_id || '';
    const messageType = item.msg_type || '';
    const content = item.body?.content || '';
    const userId = this.extractSenderUserId(item.sender);

    let text = '';
    const attachments: FileAttachment[] = [];

    if (messageType === 'text') {
      text = this.parseTextContent(content);
    } else if (messageType === 'image') {
      const fileKey = this.extractFileKey(content);
      if (fileKey) {
        const attachment = await this.downloadResource(messageId, fileKey, 'image');
        if (attachment) {
          attachments.push(attachment);
        } else {
          text = '[historical image download failed]';
        }
      }
    } else if (messageType === 'file' || messageType === 'audio' || messageType === 'video' || messageType === 'media') {
      const fileKey = this.extractFileKey(content);
      if (fileKey) {
        const resourceType = messageType === 'file' ? 'file' : messageType;
        const attachment = await this.downloadResource(messageId, fileKey, resourceType);
        if (attachment) {
          attachments.push(attachment);
        } else {
          text = `[historical ${messageType} download failed]`;
        }
      }
    } else if (messageType === 'post') {
      const parsed = this.parsePostContent(content);
      text = parsed.extractedText;
      for (const key of parsed.imageKeys) {
        const attachment = await this.downloadResource(messageId, key, 'image');
        if (attachment) attachments.push(attachment);
      }
    } else {
      return null;
    }

    text = this.stripMentionMarkers(text);
    if (!text.trim() && attachments.length === 0) return null;

    const trimmedText = text.trim();
    if (trimmedText.startsWith('/perm ')) return null;

    return {
      messageId,
      address: {
        channelType: 'feishu',
        chatId,
        userId,
      },
      text: trimmedText,
      timestamp: Number.parseInt(item.create_time || '', 10) || Date.now(),
      attachments: attachments.length > 0 ? attachments : undefined,
      raw: {
        historical: true,
        chatType,
      },
    };
  }
}

registerAdapterFactory('feishu', () => new FeishuAdapter() as unknown as BaseChannelAdapter);

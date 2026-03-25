import fs from 'node:fs';
import path from 'node:path';

import { getBridgeContext } from 'claude-to-im/src/lib/bridge/context.js';
import type { FileAttachment } from 'claude-to-im/src/lib/bridge/host.js';
import type { ChannelBinding } from 'claude-to-im/src/lib/bridge/types.js';
import { CTI_HOME } from './config.js';

const CACHE_DIR = path.join(CTI_HOME, 'data', 'feishu-history-cache');
const DEFAULT_LOOKBACK_HOURS = 48;
const DEFAULT_PAGE_SIZE = 50;
const DEFAULT_MAX_MESSAGES = 40;
const DEFAULT_MAX_IMAGE_DOWNLOAD_MB = 20;
const MAX_PAGES = 20;

export interface BackfilledHistoryEntry {
  role: 'user' | 'assistant';
  content: string;
}

interface FeishuHistoryCache {
  version: 1;
  chatId: string;
  bindingCreatedAt: string;
  fetchedAt: string;
  appliedToFreshSession: boolean;
  messages: BackfilledHistoryEntry[];
}

interface FeishuListMessage {
  message_id: string;
  msg_type: string;
  create_time: string;
  deleted?: boolean;
  sender?: {
    id?: string;
    sender_type?: string;
  };
  body?: {
    content?: string;
  };
}

interface FeishuHistoryResult {
  messages: BackfilledHistoryEntry[];
  cacheWasApplied: boolean;
}

export interface FeishuHistoryBackfillResult {
  history: Array<{ role: 'user' | 'assistant'; content: string }>;
  injectedCount: number;
  shouldStartFreshSession: boolean;
}

function parsePositiveInt(value: string | undefined, fallback: number): number {
  if (!value) return fallback;
  const parsed = Number.parseInt(value, 10);
  return Number.isFinite(parsed) && parsed > 0 ? parsed : fallback;
}

function isHistorySyncEnabled(): boolean {
  return process.env.CTI_FEISHU_HISTORY_SYNC !== 'false';
}

function getLookbackHours(): number {
  return parsePositiveInt(process.env.CTI_FEISHU_HISTORY_LOOKBACK_HOURS, DEFAULT_LOOKBACK_HOURS);
}

function getPageSize(): number {
  return Math.min(parsePositiveInt(process.env.CTI_FEISHU_HISTORY_PAGE_SIZE, DEFAULT_PAGE_SIZE), 50);
}

function getMaxMessages(): number {
  return parsePositiveInt(process.env.CTI_FEISHU_HISTORY_MAX_MESSAGES, DEFAULT_MAX_MESSAGES);
}

function getMaxImageBytes(): number {
  return parsePositiveInt(process.env.CTI_FEISHU_HISTORY_MAX_IMAGE_MB, DEFAULT_MAX_IMAGE_DOWNLOAD_MB) * 1024 * 1024;
}

function ensureDir(dir: string): void {
  fs.mkdirSync(dir, { recursive: true });
}

function atomicWrite(filePath: string, data: string): void {
  const tmp = `${filePath}.tmp`;
  fs.writeFileSync(tmp, data, 'utf-8');
  fs.renameSync(tmp, filePath);
}

function getCacheFile(sessionId: string): string {
  ensureDir(CACHE_DIR);
  return path.join(CACHE_DIR, `${sessionId}.json`);
}

function loadCache(sessionId: string, binding: ChannelBinding): FeishuHistoryCache | null {
  const cacheFile = getCacheFile(sessionId);
  try {
    const parsed = JSON.parse(fs.readFileSync(cacheFile, 'utf-8')) as FeishuHistoryCache;
    if (parsed.version !== 1) return null;
    if (parsed.chatId !== binding.chatId) return null;
    if (parsed.bindingCreatedAt !== binding.createdAt) return null;
    if (!Array.isArray(parsed.messages)) return null;
    return parsed;
  } catch {
    return null;
  }
}

function saveCache(sessionId: string, cache: FeishuHistoryCache): void {
  atomicWrite(getCacheFile(sessionId), JSON.stringify(cache, null, 2));
}

export function markFeishuHistoryBackfillApplied(sessionId: string): void {
  const cacheFile = getCacheFile(sessionId);
  try {
    const parsed = JSON.parse(fs.readFileSync(cacheFile, 'utf-8')) as FeishuHistoryCache;
    if (parsed.version !== 1 || parsed.appliedToFreshSession) return;
    parsed.appliedToFreshSession = true;
    saveCache(sessionId, parsed);
  } catch {
    // Best effort only.
  }
}

export function disableFeishuHistoryBackfill(
  sessionId: string,
  binding: Pick<ChannelBinding, 'chatId' | 'createdAt'>,
): void {
  saveCache(sessionId, {
    version: 1,
    chatId: binding.chatId,
    bindingCreatedAt: binding.createdAt,
    fetchedAt: new Date().toISOString(),
    appliedToFreshSession: true,
    messages: [],
  });
}

export function normalizeFeishuHistoryRole(
  senderId: string | undefined,
  senderType: string | undefined,
  botIds: Set<string>,
): 'user' | 'assistant' {
  if (senderId && botIds.has(senderId)) return 'assistant';
  if (senderType === 'bot' || senderType === 'app') return 'assistant';
  return 'user';
}

function formatShanghaiTimestamp(epochMs: string): string {
  const value = Number.parseInt(epochMs, 10);
  if (!Number.isFinite(value)) return 'unknown time';
  return new Intl.DateTimeFormat('zh-CN', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  }).format(new Date(value)).replace(/\//g, '-');
}

function shortSenderLabel(senderId: string | undefined, role: 'user' | 'assistant'): string {
  if (role === 'assistant') return 'bridge-bot';
  if (!senderId) return 'member';
  return `member#${senderId.slice(-6)}`;
}

function buildHistoricalPrefix(message: FeishuListMessage, role: 'user' | 'assistant'): string {
  return `[Feishu history ${formatShanghaiTimestamp(message.create_time)} ${shortSenderLabel(message.sender?.id, role)}]`;
}

export function parseFeishuTextContent(content: string | undefined): string {
  if (!content) return '';
  try {
    const parsed = JSON.parse(content) as { text?: string };
    return parsed.text?.trim() || '';
  } catch {
    return content.trim();
  }
}

export function parseFeishuFileKeys(content: string | undefined): { fileKey?: string; imageKey?: string; fileName?: string } {
  if (!content) return {};
  try {
    const parsed = JSON.parse(content) as {
      file_key?: string;
      image_key?: string;
      file_name?: string;
      fileKey?: string;
      imageKey?: string;
      fileName?: string;
    };
    return {
      fileKey: parsed.file_key || parsed.fileKey,
      imageKey: parsed.image_key || parsed.imageKey,
      fileName: parsed.file_name || parsed.fileName,
    };
  } catch {
    return {};
  }
}

export function parseFeishuPostContent(content: string | undefined): { text: string; imageKeys: string[] } {
  if (!content) return { text: '', imageKeys: [] };
  const imageKeys: string[] = [];
  const textParts: string[] = [];

  try {
    const parsed = JSON.parse(content) as {
      title?: string;
      content?: Array<Array<Record<string, unknown>>>;
    };
    if (parsed.title) textParts.push(parsed.title);
    for (const paragraph of parsed.content ?? []) {
      if (!Array.isArray(paragraph)) continue;
      const paragraphParts: string[] = [];
      for (const element of paragraph) {
        const tag = typeof element.tag === 'string' ? element.tag : '';
        if (tag === 'text') {
          const text = typeof element.text === 'string' ? element.text : '';
          if (text) paragraphParts.push(text);
          continue;
        }
        if (tag === 'a') {
          const text = typeof element.text === 'string' ? element.text : '';
          const href = typeof element.href === 'string' ? element.href : '';
          paragraphParts.push(text || href);
          continue;
        }
        if (tag === 'at') {
          const userName = typeof element.user_name === 'string'
            ? element.user_name
            : typeof element.name === 'string'
              ? element.name
              : '';
          if (userName) paragraphParts.push(`@${userName}`);
          continue;
        }
        if (tag === 'img') {
          const imageKey = typeof element.image_key === 'string' ? element.image_key : '';
          if (imageKey) imageKeys.push(imageKey);
          continue;
        }
      }
      const joined = paragraphParts.join('').trim();
      if (joined) textParts.push(joined);
    }
  } catch {
    return { text: content.trim(), imageKeys };
  }

  return { text: textParts.join('\n').trim(), imageKeys };
}

function sanitizeFileName(name: string): string {
  const base = path.basename(name);
  return base.replace(/[^a-zA-Z0-9._-]/g, '_') || 'attachment.bin';
}

function guessImageMimeType(fileName: string): string {
  const lower = fileName.toLowerCase();
  if (lower.endsWith('.png')) return 'image/png';
  if (lower.endsWith('.jpg') || lower.endsWith('.jpeg')) return 'image/jpeg';
  if (lower.endsWith('.gif')) return 'image/gif';
  if (lower.endsWith('.webp')) return 'image/webp';
  return 'application/octet-stream';
}

async function resolveLarkModule(): Promise<typeof import('@larksuiteoapi/node-sdk')> {
  return import('@larksuiteoapi/node-sdk');
}

async function resolveBotIds(
  appId: string,
  appSecret: string,
  baseUrl: string,
): Promise<Set<string>> {
  const botIds = new Set<string>();
  try {
    const tokenRes = await fetch(`${baseUrl}/open-apis/auth/v3/tenant_access_token/internal`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ app_id: appId, app_secret: appSecret }),
      signal: AbortSignal.timeout(10_000),
    });
    const tokenData = await tokenRes.json() as { tenant_access_token?: string };
    if (!tokenData.tenant_access_token) return botIds;

    const botRes = await fetch(`${baseUrl}/open-apis/bot/v3/info/`, {
      method: 'GET',
      headers: { Authorization: `Bearer ${tokenData.tenant_access_token}` },
      signal: AbortSignal.timeout(10_000),
    });
    const botData = await botRes.json() as { bot?: { open_id?: string; bot_id?: string } };
    if (botData.bot?.open_id) botIds.add(botData.bot.open_id);
    if (botData.bot?.bot_id) botIds.add(botData.bot.bot_id);
  } catch (err) {
    console.warn('[feishu-history] Failed to resolve bot identity:', err instanceof Error ? err.message : err);
  }
  return botIds;
}

async function readStreamToBuffer(
  readable: NodeJS.ReadableStream,
  maxBytes: number,
): Promise<Buffer | null> {
  const chunks: Buffer[] = [];
  let total = 0;
  for await (const chunk of readable) {
    const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    total += buffer.length;
    if (total > maxBytes) {
      return null;
    }
    chunks.push(buffer);
  }
  return Buffer.concat(chunks);
}

async function downloadImageAttachment(
  client: InstanceType<(typeof import('@larksuiteoapi/node-sdk'))['Client']>,
  messageId: string,
  imageKey: string,
  fileName: string,
  maxBytes: number,
): Promise<FileAttachment | null> {
  try {
    const res = await client.im.messageResource.get({
      path: {
        message_id: messageId,
        file_key: imageKey,
      },
      params: {
        type: 'image',
      },
    });
    const buffer = await readStreamToBuffer(res.getReadableStream(), maxBytes);
    if (!buffer || buffer.length === 0) return null;
    return {
      id: `${messageId}:${imageKey}`,
      name: fileName,
      type: guessImageMimeType(fileName),
      size: buffer.length,
      data: buffer.toString('base64'),
    };
  } catch (err) {
    console.warn(
      `[feishu-history] Failed to download image ${imageKey} for ${messageId}:`,
      err instanceof Error ? err.message : err,
    );
    return null;
  }
}

async function downloadFileAttachment(
  client: InstanceType<(typeof import('@larksuiteoapi/node-sdk'))['Client']>,
  messageId: string,
  fileKey: string,
  fileName: string,
  maxBytes: number,
): Promise<FileAttachment | null> {
  try {
    const res = await client.im.messageResource.get({
      path: {
        message_id: messageId,
        file_key: fileKey,
      },
      params: {
        type: 'file',
      },
    });
    const buffer = await readStreamToBuffer(res.getReadableStream(), maxBytes);
    if (!buffer || buffer.length === 0) return null;
    return {
      id: `${messageId}:${fileKey}`,
      name: fileName,
      type: guessImageMimeType(fileName),
      size: buffer.length,
      data: buffer.toString('base64'),
    };
  } catch (err) {
    console.warn(
      `[feishu-history] Failed to download file ${fileKey} for ${messageId}:`,
      err instanceof Error ? err.message : err,
    );
    return null;
  }
}

function persistAttachment(
  attachment: FileAttachment,
  binding: ChannelBinding,
  timestampMs: string,
): { id: string; name: string; type: string; size: number; filePath: string } {
  const uploadDir = path.join(binding.workingDirectory, '.codepilot-uploads', 'feishu-history');
  ensureDir(uploadDir);
  const safeName = sanitizeFileName(attachment.name);
  const filePath = path.join(uploadDir, `${timestampMs}-${safeName}`);
  fs.writeFileSync(filePath, Buffer.from(attachment.data, 'base64'));
  return {
    id: attachment.id,
    name: attachment.name,
    type: attachment.type,
    size: attachment.size,
    filePath,
  };
}

function buildStoredMessage(
  message: FeishuListMessage,
  role: 'user' | 'assistant',
  text: string,
  attachments: Array<{ id: string; name: string; type: string; size: number; filePath: string }>,
): BackfilledHistoryEntry | null {
  const prefix = buildHistoricalPrefix(message, role);
  const effectiveText = [prefix, text].filter(Boolean).join(' ').trim();
  if (!effectiveText && attachments.length === 0) return null;
  if (attachments.length === 0) {
    return { role, content: effectiveText };
  }
  return {
    role,
    content: `<!--files:${JSON.stringify(attachments)}-->${effectiveText}`,
  };
}

function pickRelevantMessages(items: FeishuListMessage[]): FeishuListMessage[] {
  const relevant = items.filter((item) => item.msg_type !== 'interactive' && item.msg_type !== 'system');
  return relevant.slice(-getMaxMessages());
}

async function convertFeishuMessage(
  item: FeishuListMessage,
  binding: ChannelBinding,
  botIds: Set<string>,
  client: InstanceType<(typeof import('@larksuiteoapi/node-sdk'))['Client']>,
): Promise<BackfilledHistoryEntry | null> {
  const role = normalizeFeishuHistoryRole(item.sender?.id, item.sender?.sender_type, botIds);
  const content = item.body?.content;
  const attachments: Array<{ id: string; name: string; type: string; size: number; filePath: string }> = [];
  let text = '';

  if (item.deleted || content === 'This message was recalled') {
    text = '[Recalled Feishu message]';
    return buildStoredMessage(item, role, text, attachments);
  }

  if (item.msg_type === 'text') {
    text = parseFeishuTextContent(content);
    return buildStoredMessage(item, role, text, attachments);
  }

  if (item.msg_type === 'post') {
    const parsed = parseFeishuPostContent(content);
    text = parsed.text;
    for (const imageKey of parsed.imageKeys) {
      const attachment = await downloadImageAttachment(
        client,
        item.message_id,
        imageKey,
        `${imageKey}.png`,
        getMaxImageBytes(),
      );
      if (attachment) {
        attachments.push(persistAttachment(attachment, binding, item.create_time));
      }
    }
    return buildStoredMessage(item, role, text, attachments);
  }

  if (item.msg_type === 'image') {
    const { imageKey } = parseFeishuFileKeys(content);
    if (imageKey) {
      const attachment = await downloadImageAttachment(
        client,
        item.message_id,
        imageKey,
        `${imageKey}.png`,
        getMaxImageBytes(),
      );
      if (attachment) {
        attachments.push(persistAttachment(attachment, binding, item.create_time));
      }
    }
    text = attachments.length > 0 ? '[Historical Feishu image]' : '[Historical Feishu image metadata only]';
    return buildStoredMessage(item, role, text, attachments);
  }

  if (item.msg_type === 'media') {
    const { imageKey, fileName } = parseFeishuFileKeys(content);
    if (imageKey) {
      const attachment = await downloadImageAttachment(
        client,
        item.message_id,
        imageKey,
        fileName ? `${sanitizeFileName(fileName)}.preview.png` : `${imageKey}.png`,
        getMaxImageBytes(),
      );
      if (attachment) {
        attachments.push(persistAttachment(attachment, binding, item.create_time));
      }
    }
    text = fileName ? `[Historical Feishu media] ${fileName}` : '[Historical Feishu media]';
    return buildStoredMessage(item, role, text, attachments);
  }

  if (item.msg_type === 'file') {
    const { imageKey, fileKey, fileName } = parseFeishuFileKeys(content);
    const effectiveFileName = fileName || 'historical-file';
    const imageMime = guessImageMimeType(effectiveFileName);
    if (imageKey) {
      const attachment = await downloadImageAttachment(
        client,
        item.message_id,
        imageKey,
        effectiveFileName,
        getMaxImageBytes(),
      );
      if (attachment) attachments.push(persistAttachment(attachment, binding, item.create_time));
    } else if (imageMime.startsWith('image/') && fileKey) {
      const attachment = await downloadFileAttachment(
        client,
        item.message_id,
        fileKey,
        effectiveFileName,
        getMaxImageBytes(),
      );
      if (attachment) attachments.push(persistAttachment(attachment, binding, item.create_time));
    }
    text = `[Historical Feishu file] ${effectiveFileName}`;
    return buildStoredMessage(item, role, text, attachments);
  }

  return null;
}

async function fetchHistoryForBinding(binding: ChannelBinding): Promise<FeishuHistoryResult> {
  const { store } = getBridgeContext();
  const appId = store.getSetting('bridge_feishu_app_id') || '';
  const appSecret = store.getSetting('bridge_feishu_app_secret') || '';
  if (!appId || !appSecret) {
    return { messages: [], cacheWasApplied: true };
  }

  const bindingCreatedMs = Date.parse(binding.createdAt);
  if (!Number.isFinite(bindingCreatedMs)) {
    return { messages: [], cacheWasApplied: true };
  }

  const endTimeSec = Math.floor(bindingCreatedMs / 1000) - 1;
  if (endTimeSec <= 0) {
    return { messages: [], cacheWasApplied: true };
  }

  const startTimeSec = endTimeSec - getLookbackHours() * 3600;
  const lark = await resolveLarkModule();
  const domain = (store.getSetting('bridge_feishu_domain') || '').includes('larksuite')
    ? lark.Domain.Lark
    : lark.Domain.Feishu;
  const client = new lark.Client({ appId, appSecret, domain });
  const baseUrl = domain === lark.Domain.Lark ? 'https://open.larksuite.com' : 'https://open.feishu.cn';
  const botIds = await resolveBotIds(appId, appSecret, baseUrl);
  const items: FeishuListMessage[] = [];
  let pageToken: string | undefined;

  for (let page = 0; page < MAX_PAGES; page++) {
    const res = await client.im.message.list({
      params: {
        container_id_type: 'chat',
        container_id: binding.chatId,
        start_time: String(startTimeSec),
        end_time: String(endTimeSec),
        sort_type: 'ByCreateTimeAsc',
        page_size: getPageSize(),
        page_token: pageToken,
      },
    });
    const batch = (res.data?.items ?? []) as FeishuListMessage[];
    items.push(...batch);
    if (!res.data?.has_more || !res.data?.page_token || batch.length === 0) {
      break;
    }
    pageToken = res.data.page_token;
  }

  const messages: BackfilledHistoryEntry[] = [];
  for (const item of pickRelevantMessages(items)) {
    const converted = await convertFeishuMessage(item, binding, botIds, client);
    if (converted) {
      messages.push(converted);
    }
  }

  return { messages, cacheWasApplied: false };
}

export async function ensureFeishuHistoryBackfill(
  sessionId: string,
  history?: Array<{ role: 'user' | 'assistant'; content: string }>,
): Promise<FeishuHistoryBackfillResult> {
  const existingHistory = history ?? [];
  if (!isHistorySyncEnabled()) {
    return {
      history: existingHistory,
      injectedCount: 0,
      shouldStartFreshSession: false,
    };
  }

  const { store } = getBridgeContext();
  const binding = store
    .listChannelBindings('feishu')
    .find((item) => item.codepilotSessionId === sessionId);

  if (!binding) {
    return {
      history: existingHistory,
      injectedCount: 0,
      shouldStartFreshSession: false,
    };
  }

  let cache = loadCache(sessionId, binding);
  if (!cache) {
    const fetched = await fetchHistoryForBinding(binding);
    cache = {
      version: 1,
      chatId: binding.chatId,
      bindingCreatedAt: binding.createdAt,
      fetchedAt: new Date().toISOString(),
      appliedToFreshSession: fetched.cacheWasApplied,
      messages: fetched.messages,
    };
    saveCache(sessionId, cache);
  }

  if (cache.messages.length === 0) {
    return {
      history: existingHistory,
      injectedCount: 0,
      shouldStartFreshSession: false,
    };
  }

  return {
    history: [...cache.messages, ...existingHistory],
    injectedCount: cache.messages.length,
    shouldStartFreshSession: !cache.appliedToFreshSession,
  };
}

/**
 * Codex Provider — LLMProvider implementation backed by @openai/codex-sdk.
 *
 * Maps Codex SDK thread events to the SSE stream format consumed by
 * the bridge conversation engine, making Codex a drop-in alternative
 * to the Claude Code SDK backend.
 *
 * Requires `@openai/codex-sdk` to be installed (optionalDependency).
 * The provider lazily imports the SDK at first use and throws a clear
 * error if it is not available.
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { getBridgeContext } from 'claude-to-im/src/lib/bridge/context.js';
import type { FileAttachment, LLMProvider, StreamChatParams } from 'claude-to-im/src/lib/bridge/host.js';
import type { PendingPermissions } from './permission-gateway.js';
import { sseEvent } from './sse-utils.js';
import {
  ensureFeishuHistoryBackfill,
  markFeishuHistoryBackfillApplied,
} from './feishu-history.js';
import { prependSystemPrompt } from './session-prompt.js';
import { prependPathEntry, resolvePreferredWindowsShellPath } from './windows-shell.js';

/** MIME → file extension for temp image files. */
const MIME_EXT: Record<string, string> = {
  'image/png': '.png',
  'image/jpeg': '.jpg',
  'image/jpg': '.jpg',
  'image/gif': '.gif',
  'image/webp': '.webp',
};

function formatAttachmentSize(size: number): string {
  if (!Number.isFinite(size) || size <= 0) return 'unknown size';
  if (size >= 1024 * 1024) return `${(size / (1024 * 1024)).toFixed(1)} MB`;
  if (size >= 1024) return `${(size / 1024).toFixed(1)} KB`;
  return `${size} B`;
}

function isImageFile(file: FileAttachment): boolean {
  return file.type.startsWith('image/');
}

function shouldHideToolMetadata(): boolean {
  try {
    return getBridgeContext().store.getSetting('bridge_feishu_hide_tool_metadata') === 'true';
  } catch {
    return process.env.CTI_FEISHU_HIDE_TOOL_METADATA === 'true';
  }
}

export function normalizeStoredMessageContent(content: string): string {
  const match = content.match(/^<!--files:(.*?)-->/s);
  let text = content;
  let attachmentSummary = '';

  if (match) {
    text = content.slice(match[0].length).trim();
    try {
      const parsed = JSON.parse(match[1]) as Array<{ name?: string; type?: string; size?: number }>;
      if (Array.isArray(parsed) && parsed.length > 0) {
        const summary = parsed.map((file) => {
          const name = file.name || 'unnamed';
          const type = file.type || 'application/octet-stream';
          const size = typeof file.size === 'number' ? formatAttachmentSize(file.size) : 'unknown size';
          return `${name} (${type}, ${size})`;
        }).join('; ');
        attachmentSummary = `Attached files: ${summary}`;
      }
    } catch {
      attachmentSummary = 'Attached files were included in this message.';
    }
  }

  try {
    const parsed = JSON.parse(text) as Array<{ type?: string; text?: string; content?: string }>;
    if (Array.isArray(parsed)) {
      const textBlocks = parsed
        .filter((block) => block && (block.type === 'text' || (!shouldHideToolMetadata() && block.type === 'tool_result')))
        .map((block) => (block.type === 'text' ? block.text : block.content) || '')
        .filter(Boolean);
      if (textBlocks.length > 0) {
        text = textBlocks.join('\n\n');
      }
    }
  } catch {
    // Not structured JSON content; keep plain text.
  }

  return [attachmentSummary, text.trim()].filter(Boolean).join('\n');
}

export function buildHistoryPrelude(
  history?: Array<{ role: 'user' | 'assistant'; content: string }>,
): string {
  if (!history || history.length === 0) return '';
  const recent = history.slice(-20);
  const lines = ['Conversation history from the same IM chat:'];
  for (const item of recent) {
    const role = item.role === 'assistant' ? 'Assistant' : 'User';
    const content = normalizeStoredMessageContent(item.content).slice(0, 3000);
    if (content) {
      lines.push(`${role}: ${content}`);
    }
  }
  return lines.join('\n\n');
}

export function buildPromptText(
  text: string,
  files?: StreamChatParams['files'],
  history?: Array<{ role: 'user' | 'assistant'; content: string }>,
  systemPrompt?: string,
): string {
  const historyPrelude = buildHistoryPrelude(history);
  const attachmentSummary = (files ?? [])
    .filter((file): file is FileAttachment => !!file)
    .filter((file) => !isImageFile(file))
    .map((file) => `- ${file.name} (${file.type}, ${formatAttachmentSize(file.size)})`);

  let effectiveText = text.trim();
  if (!effectiveText && files && files.length > 0) {
    const hasImages = files.some(isImageFile);
    effectiveText = hasImages && attachmentSummary.length === 0
      ? 'Describe the attached image(s) and explain any relevant context.'
      : 'The user sent file attachments. Use the file metadata below to understand the conversation context.';
  }
  if (attachmentSummary.length > 0) {
    effectiveText = [effectiveText, 'Attached non-image files:', ...attachmentSummary]
      .filter(Boolean)
      .join('\n');
  }

  return prependSystemPrompt(
    [historyPrelude, effectiveText].filter(Boolean).join('\n\n'),
    systemPrompt,
  );
}

// All SDK types kept as `any` because @openai/codex-sdk is optional.
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type CodexModule = any;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type CodexInstance = any;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type ThreadInstance = any;

/**
 * Map bridge permission modes to Codex approval policies.
 * - 'acceptEdits' (code mode) → 'on-failure' (auto-approve most things)
 * - 'plan' → 'on-request' (ask before executing)
 * - 'default' (ask mode) → 'on-request'
 */
function toApprovalPolicy(permissionMode?: string): string {
  switch (permissionMode) {
    case 'acceptEdits': return 'on-failure';
    case 'plan': return 'on-request';
    case 'default': return 'on-request';
    default: return 'on-request';
  }
}

/** Whether to forward bridge model to Codex CLI. Default: false (use Codex current/default model). */
function shouldPassModelToCodex(): boolean {
  return process.env.CTI_CODEX_PASS_MODEL === 'true';
}

export function buildCodexCliEnv(
  baseEnv: NodeJS.ProcessEnv = process.env,
): Record<string, string> {
  const env: Record<string, string> = {};
  for (const [key, value] of Object.entries(baseEnv)) {
    if (typeof value === 'string') {
      env[key] = value;
    }
  }

  const shellPath = resolvePreferredWindowsShellPath(baseEnv);
  if (process.platform === 'win32' && shellPath) {
    const shellDir = path.dirname(shellPath);
    const nextPath = prependPathEntry(env.Path || env.PATH, shellDir);
    env.Path = nextPath;
    env.PATH = nextPath;
    env.ComSpec = shellPath;
    env.COMSPEC = shellPath;
    env.SHELL = shellPath;
  }

  return env;
}

type CodexSandboxMode = 'read-only' | 'workspace-write' | 'danger-full-access';

function normalizeSandboxMode(value?: string): CodexSandboxMode | undefined {
  switch (value?.trim()) {
    case 'read-only':
    case 'workspace-write':
    case 'danger-full-access':
      return value.trim() as CodexSandboxMode;
    default:
      return undefined;
  }
}

function resolveSandboxMode(): CodexSandboxMode {
  return normalizeSandboxMode(process.env.CTI_CODEX_SANDBOX_MODE) || 'danger-full-access';
}

function resolveNetworkAccessEnabled(sandboxMode: CodexSandboxMode): boolean | undefined {
  const raw = process.env.CTI_CODEX_NETWORK_ACCESS?.trim().toLowerCase();
  if (raw === 'true') return true;
  if (raw === 'false') return false;
  return sandboxMode === 'danger-full-access' ? true : undefined;
}

function looksLikeClaudeModel(model?: string): boolean {
  return !!model && /^claude[-_]/i.test(model);
}

function shouldRetryFreshThread(message: string): boolean {
  const lower = message.toLowerCase();
  return (
    lower.includes('resuming session with different model') ||
    lower.includes('no such session') ||
    (lower.includes('resume') && lower.includes('session'))
  );
}

export function buildThreadOptions(
  params: Pick<StreamChatParams, 'model' | 'workingDirectory' | 'permissionMode'>,
): Record<string, unknown> {
  const sandboxMode = resolveSandboxMode();
  const networkAccessEnabled = resolveNetworkAccessEnabled(sandboxMode);

  return {
    ...(shouldPassModelToCodex() && params.model ? { model: params.model } : {}),
    ...(params.workingDirectory ? { workingDirectory: params.workingDirectory } : {}),
    approvalPolicy: toApprovalPolicy(params.permissionMode),
    sandboxMode,
    ...(networkAccessEnabled !== undefined ? { networkAccessEnabled } : {}),
  };
}

export class CodexProvider implements LLMProvider {
  private sdk: CodexModule | null = null;
  private codex: CodexInstance | null = null;

  /** Maps session IDs to Codex thread IDs for resume. */
  private threadIds = new Map<string, string>();

  constructor(private pendingPerms: PendingPermissions) {}

  /**
   * Lazily load the Codex SDK. Throws a clear error if not installed.
   */
  private async ensureSDK(): Promise<{ sdk: CodexModule; codex: CodexInstance }> {
    if (this.sdk && this.codex) {
      return { sdk: this.sdk, codex: this.codex };
    }

    try {
      this.sdk = await (Function('return import("@openai/codex-sdk")')() as Promise<CodexModule>);
    } catch {
      throw new Error(
        '[CodexProvider] @openai/codex-sdk is not installed. ' +
        'Install it with: npm install @openai/codex-sdk'
      );
    }

    // Resolve API key: CTI_CODEX_API_KEY > CODEX_API_KEY > OPENAI_API_KEY > (login auth)
    const apiKey = process.env.CTI_CODEX_API_KEY
      || process.env.CODEX_API_KEY
      || process.env.OPENAI_API_KEY
      || undefined;
    const baseUrl = process.env.CTI_CODEX_BASE_URL || undefined;

    const CodexClass = this.sdk.Codex;
    this.codex = new CodexClass({
      ...(apiKey ? { apiKey } : {}),
      ...(baseUrl ? { baseUrl } : {}),
      env: buildCodexCliEnv(),
    });

    return { sdk: this.sdk, codex: this.codex };
  }

  streamChat(params: StreamChatParams): ReadableStream<string> {
    const self = this;

    return new ReadableStream<string>({
      start(controller) {
        (async () => {
          const tempFiles: string[] = [];
          try {
            const { codex } = await self.ensureSDK();
            let mergedHistory = params.conversationHistory;

            try {
              const backfill = await ensureFeishuHistoryBackfill(
                params.sessionId,
                params.conversationHistory,
              );
              mergedHistory = backfill.history;
              if (backfill.shouldStartFreshSession) {
                markFeishuHistoryBackfillApplied(params.sessionId);
              }
            } catch (err) {
              console.warn(
                '[codex-provider] Feishu history backfill failed, continuing without it:',
                err instanceof Error ? err.message : err,
              );
            }

            // Resolve or create thread
            let savedThreadId = params.sdkSessionId
              ? self.threadIds.get(params.sessionId) || params.sdkSessionId
              : undefined;

            if (mergedHistory && params.sdkSessionId && mergedHistory.length > (params.conversationHistory?.length ?? 0)) {
              savedThreadId = undefined;
            }

            // Cross-runtime migration safety:
            // when a persisted Claude-model session leaks into Codex runtime,
            // resuming it can fail immediately with model/session mismatch.
            if (savedThreadId && looksLikeClaudeModel(params.model)) {
              console.warn('[codex-provider] Ignoring stale Claude-like sdkSessionId in Codex runtime; starting fresh thread');
              savedThreadId = undefined;
            }

            const threadOptions = buildThreadOptions(params);

            let retryFresh = false;

            while (true) {
              const useStoredHistory = !savedThreadId || retryFresh;
              const promptText = buildPromptText(
                params.prompt,
                params.files,
                useStoredHistory ? mergedHistory : undefined,
                params.systemPrompt,
              );

              // Build input: Codex SDK UserInput supports { type: "text" } and
              // { type: "local_image", path: string }. Non-image files are
              // summarized into text so the model still sees their presence.
              const imageFiles = params.files?.filter(isImageFile) ?? [];

              let input: string | Array<Record<string, string>>;
              if (imageFiles.length > 0) {
                const parts: Array<Record<string, string>> = [
                  { type: 'text', text: promptText },
                ];
                for (const file of imageFiles) {
                  const ext = MIME_EXT[file.type] || '.png';
                  const tmpPath = path.join(os.tmpdir(), `cti-img-${Date.now()}-${Math.random().toString(36).slice(2)}${ext}`);
                  fs.writeFileSync(tmpPath, Buffer.from(file.data, 'base64'));
                  tempFiles.push(tmpPath);
                  parts.push({ type: 'local_image', path: tmpPath });
                }
                input = parts;
              } else {
                input = promptText;
              }

              let thread: ThreadInstance;
              if (savedThreadId) {
                try {
                  thread = codex.resumeThread(savedThreadId, threadOptions);
                } catch (err) {
                  if (!retryFresh) {
                    const message = err instanceof Error ? err.message : String(err);
                    console.warn('[codex-provider] resumeThread threw synchronously, retrying with a fresh thread:', message);
                    savedThreadId = undefined;
                    retryFresh = true;
                    continue;
                  }
                  thread = codex.startThread(threadOptions);
                }
              } else {
                thread = codex.startThread(threadOptions);
              }

              let sawAnyEvent = false;
              try {
                const { events } = await thread.runStreamed(input);

                for await (const event of events) {
                  sawAnyEvent = true;
                  if (params.abortController?.signal.aborted) {
                    break;
                  }

                  switch (event.type) {
                    case 'thread.started': {
                      const threadId = event.thread_id as string;
                      self.threadIds.set(params.sessionId, threadId);

                      controller.enqueue(sseEvent('status', {
                        session_id: threadId,
                      }));
                      break;
                    }

                    case 'item.completed': {
                      const item = event.item as Record<string, unknown>;
                      self.handleCompletedItem(controller, item);
                      break;
                    }

                    case 'turn.completed': {
                      const usage = event.usage as Record<string, unknown> | undefined;
                      const threadId = self.threadIds.get(params.sessionId);

                      controller.enqueue(sseEvent('result', {
                        usage: usage ? {
                          input_tokens: usage.input_tokens ?? 0,
                          output_tokens: usage.output_tokens ?? 0,
                          cache_read_input_tokens: usage.cached_input_tokens ?? 0,
                        } : undefined,
                        ...(threadId ? { session_id: threadId } : {}),
                      }));
                      break;
                    }

                    case 'turn.failed': {
                      const error = (event as { message?: string }).message;
                      controller.enqueue(sseEvent('error', error || 'Turn failed'));
                      break;
                    }

                    case 'error': {
                      const error = (event as { message?: string }).message;
                      controller.enqueue(sseEvent('error', error || 'Thread error'));
                      break;
                    }

                    // item.started, item.updated, turn.started — no action needed
                  }
                }
                break;
              } catch (err) {
                const message = err instanceof Error ? err.message : String(err);
                if (savedThreadId && !retryFresh && !sawAnyEvent && shouldRetryFreshThread(message)) {
                  console.warn('[codex-provider] Resume failed, retrying with a fresh thread:', message);
                  savedThreadId = undefined;
                  retryFresh = true;
                  continue;
                }
                throw err;
              }
            }

            controller.close();
          } catch (err) {
            const message = err instanceof Error ? err.message : String(err);
            console.error('[codex-provider] Error:', err instanceof Error ? err.stack || err.message : err);
            try {
              controller.enqueue(sseEvent('error', message));
              controller.close();
            } catch {
              // Controller already closed
            }
          } finally {
            // Clean up temp image files
            for (const tmp of tempFiles) {
              try { fs.unlinkSync(tmp); } catch { /* ignore */ }
            }
          }
        })();
      },
    });
  }

  /**
   * Map a completed Codex item to SSE events.
   */
  private handleCompletedItem(
    controller: ReadableStreamDefaultController<string>,
    item: Record<string, unknown>,
  ): void {
    const itemType = item.type as string;

    switch (itemType) {
      case 'agent_message': {
        const text = (item.text as string) || '';
        if (text) {
          controller.enqueue(sseEvent('text', text));
        }
        break;
      }

      case 'command_execution': {
        const toolId = (item.id as string) || `tool-${Date.now()}`;
        const command = item.command as string || '';
        const output = item.aggregated_output as string || '';
        const exitCode = item.exit_code as number | undefined;
        const isError = exitCode != null && exitCode !== 0;

        controller.enqueue(sseEvent('tool_use', {
          id: toolId,
          name: 'Bash',
          input: { command },
        }));

        const resultContent = output || (isError ? `Exit code: ${exitCode}` : 'Done');
        controller.enqueue(sseEvent('tool_result', {
          tool_use_id: toolId,
          content: resultContent,
          is_error: isError,
        }));
        break;
      }

      case 'file_change': {
        const toolId = (item.id as string) || `tool-${Date.now()}`;
        const changes = item.changes as Array<{ path: string; kind: string }> || [];
        const summary = changes.map(c => `${c.kind}: ${c.path}`).join('\n');

        controller.enqueue(sseEvent('tool_use', {
          id: toolId,
          name: 'Edit',
          input: { files: changes },
        }));

        controller.enqueue(sseEvent('tool_result', {
          tool_use_id: toolId,
          content: summary || 'File changes applied',
          is_error: false,
        }));
        break;
      }

      case 'mcp_tool_call': {
        const toolId = (item.id as string) || `tool-${Date.now()}`;
        const server = item.server as string || '';
        const tool = item.tool as string || '';
        const args = item.arguments as unknown;
        const result = item.result as { content?: unknown; structured_content?: unknown } | undefined;
        const error = item.error as { message?: string } | undefined;

        const resultContent = result?.content ?? result?.structured_content;
        const resultText = typeof resultContent === 'string' ? resultContent : (resultContent ? JSON.stringify(resultContent) : undefined);

        controller.enqueue(sseEvent('tool_use', {
          id: toolId,
          name: `mcp__${server}__${tool}`,
          input: args,
        }));

        controller.enqueue(sseEvent('tool_result', {
          tool_use_id: toolId,
          content: error?.message || resultText || 'Done',
          is_error: !!error,
        }));
        break;
      }

      case 'reasoning': {
        // Reasoning is internal; emit as status
        const text = (item.text as string) || '';
        if (text) {
          controller.enqueue(sseEvent('status', { reasoning: text }));
        }
        break;
      }
    }
  }
}

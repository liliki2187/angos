import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

import {
  BRIDGE_IMAGE_GENERATION_SYSTEM_PROMPT,
  resolveBridgeSystemPrompt,
} from '../session-prompt.js';

describe('session prompt', () => {
  it('adds bridged image generation routing guidance', () => {
    const prompt = resolveBridgeSystemPrompt('Keep this project context.');

    assert.ok(prompt?.includes('Keep this project context.'));
    assert.ok(prompt?.includes('openrouter-image-gen'));
    assert.ok(prompt?.includes('built-in $imagegen'));
    assert.ok(prompt?.includes('fail directly'));
    assert.ok(prompt?.includes('do not run OpenRouter as a fallback'));
    assert.ok(prompt?.includes('image_gen/YYYY-MM-DD/'));
    assert.ok(prompt?.includes('the bridge will auto-upload'));
  });

  it('does not duplicate managed bridge guidance when normalized again', () => {
    const first = resolveBridgeSystemPrompt('Custom prompt.');
    const second = resolveBridgeSystemPrompt(first);

    assert.ok(second?.includes('Custom prompt.'));

    const marker = BRIDGE_IMAGE_GENERATION_SYSTEM_PROMPT.split('.')[0];
    const matches = second?.match(new RegExp(marker.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) ?? [];
    assert.equal(matches.length, 1);
  });
});

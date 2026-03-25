import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

import { computeStreamTextDelta } from '../../node_modules/claude-to-im/src/lib/bridge/conversation-engine.ts';

describe('computeStreamTextDelta', () => {
  it('passes through plain delta chunks unchanged', () => {
    assert.equal(
      computeStreamTextDelta('alpha', '\nbeta'),
      '\nbeta',
    );
  });

  it('extracts only the new suffix from cumulative text chunks', () => {
    assert.equal(
      computeStreamTextDelta('alpha', 'alpha\nbeta'),
      '\nbeta',
    );
  });

  it('drops fully repeated long suffix chunks', () => {
    assert.equal(
      computeStreamTextDelta(
        '第一句。\n这是会被重复的第二句。',
        '这是会被重复的第二句。',
      ),
      '',
    );
  });

  it('removes overlapping tail text instead of appending it twice', () => {
    assert.equal(
      computeStreamTextDelta(
        '第一句。\n第二句会重复。\n',
        '第二句会重复。\n第三句是新内容。',
      ),
      '第三句是新内容。',
    );
  });
});

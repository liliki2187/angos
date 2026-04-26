import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

import { computeStreamTextDelta } from '../feishu-adapter.js';

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

  it('keeps only the changed tail when cumulative text diverges after a shared prefix', () => {
    assert.equal(
      computeStreamTextDelta('alpha beta', 'alpha gamma'),
      'gamma',
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

/*
 * dedash.mjs — step 1 of the STYLE.md rollout: remove en dashes mechanically.
 *
 * Only the cases that need no judgement are touched:
 *   - numeric ranges in prose      2017–2020      -> 2017 to 2020
 *   - numeric ranges in table rows 2017–2020      -> 2017-2020
 *   - letter-to-letter compounds   feature–response -> feature-response
 *
 * Em dashes are NOT touched. They mark sentence breaks and each one needs a
 * decision about where the sentence should split, which a script cannot make.
 *
 * Drafting notes (blockquotes) and comment blocks are left alone: STYLE.md
 * applies to the manuscript prose, not to internal records.
 *
 * Usage:
 *   node paper/tex/dedash.mjs --dry     show what would change
 *   node paper/tex/dedash.mjs           apply
 */

import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve('paper');
const FILES = ['01_introduction', '02_related_work', '03_methods', '04_results',
               '05_discussion', '06_conclusions', 'S1_few_shot_recovery'];
const DRY = process.argv.includes('--dry');

const EN = '–';
let changes = 0;
const samples = [];

function convertLine(line, inComment) {
  // Leave internal records untouched.
  if (inComment || /^\s*>/.test(line)) return line;
  const isTable = /^\s*\|/.test(line);
  const before = line;

  // Numeric range: digits (with optional decimal/sign/unit-free) either side.
  line = line.replace(
    new RegExp('(\\d)\\s*' + EN + '\\s*(\\d)', 'g'),
    isTable ? '$1-$2' : '$1 to $2');

  // Letter-to-letter compound modifier: a hyphen is the standard replacement.
  line = line.replace(
    new RegExp('([A-Za-zÀ-ɏ])' + EN + '([A-Za-zÀ-ɏ])', 'g'),
    '$1-$2');

  if (line !== before) {
    changes++;
    if (samples.length < 12) samples.push({ before: before.trim(), after: line.trim() });
  }
  return line;
}

for (const f of FILES) {
  const p = path.join(ROOT, f + '.md');
  const src = fs.readFileSync(p, 'utf8');
  const lines = src.split(/\r?\n/);
  let inComment = false;
  const out = lines.map(l => {
    if (/<!--/.test(l)) inComment = true;
    const res = convertLine(l, inComment);
    if (/-->/.test(l)) inComment = false;
    return res;
  });
  const result = out.join('\n');
  const remaining = (result.replace(/<!--[\s\S]*?-->/g, '').match(new RegExp(EN, 'g')) || []).length;
  console.log(`${f.padEnd(24)} en dashes left outside comments: ${remaining}`);
  if (!DRY) fs.writeFileSync(p, result, 'utf8');
}

console.log(`\n${DRY ? 'would change' : 'changed'} ${changes} line(s)`);
for (const s of samples) {
  console.log('\n  -  ' + s.before.slice(0, 120));
  console.log('  +  ' + s.after.slice(0, 120));
}
if (DRY) console.log('\n(dry run: nothing written)');

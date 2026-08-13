/*
 * check_numbers.mjs — did a style rewrite change any number?
 *
 * Compares the multiset of numeric tokens in a file's PROSE against the same
 * file at a git ref. Drafting notes, DRAFT-NOTES comment blocks and fenced code
 * are excluded, because STYLE.md does not apply to them and their dates would
 * otherwise show up as invented numbers.
 *
 * Table rows ARE included: they carry results and must not drift.
 *
 * Usage:
 *   node paper/tex/check_numbers.mjs 06_conclusions [more files ...]
 *   node paper/tex/check_numbers.mjs --ref HEAD~1 04_results
 */

import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';

const argv = process.argv.slice(2);
let ref = 'HEAD';
const ri = argv.indexOf('--ref');
if (ri >= 0) { ref = argv[ri + 1]; argv.splice(ri, 2); }
if (!argv.length) { console.error('give at least one file stem, e.g. 06_conclusions'); process.exit(2); }

const ROOT = path.resolve('paper');

// Prose = manuscript content the style rules govern. Notes are not content.
const prose = s => s
  .replace(/<!--[\s\S]*?-->/g, '')
  .replace(/```[\s\S]*?```/g, '')
  .split(/\r?\n/).filter(l => !/^\s*>/.test(l)).join('\n');

const nums = s => (s.match(/\d+(?:[.,]\d+)*/g) || []).map(x => x.replace(/,/g, ''));
const tally = a => a.reduce((m, x) => m.set(x, (m.get(x) || 0) + 1), new Map());

let failed = 0;
for (const stem of argv) {
  const f = stem.endsWith('.md') ? stem : stem + '.md';
  let before;
  try {
    before = execSync(`git show ${ref}:paper/${f}`, { encoding: 'utf8', maxBuffer: 1e8 });
  } catch {
    console.log(`${f.padEnd(26)} SKIP (not in ${ref})`);
    continue;
  }
  const after = fs.readFileSync(path.join(ROOT, f), 'utf8');
  const A = tally(nums(prose(before))), B = tally(nums(prose(after)));

  const diffs = [];
  for (const [k, v] of A) { const w = B.get(k) || 0; if (w !== v) diffs.push(`${k}: ${v} -> ${w}`); }
  for (const [k, v] of B) if (!A.has(k)) diffs.push(`NEW ${k} (x${v})`);

  if (diffs.length) {
    failed++;
    console.log(`${f.padEnd(26)} CHANGED: ${diffs.slice(0, 12).join(', ')}`);
  } else {
    console.log(`${f.padEnd(26)} numbers identical (${[...A.values()].reduce((a, b) => a + b, 0)} tokens)`);
  }
}

console.log(failed ? `\n${failed} file(s) changed numbers — review before committing`
                   : '\nno number changed');
process.exit(failed ? 1 : 0);

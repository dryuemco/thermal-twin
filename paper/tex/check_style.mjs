/*
 * check_style.mjs — report conformance with paper/STYLE.md.
 *
 * A report, not a gate. It counts what can be counted (dashes, sentence length)
 * and leaves the judgement to a human. Drafting notes, comment blocks and table
 * rows are excluded, because the rules apply to prose only.
 *
 * Usage: node paper/tex/check_style.mjs [file ...]
 */

import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve('paper');
const DEFAULT = ['00_abstract', '01_introduction', '02_related_work', '03_methods',
                 '04_results', '05_discussion', '06_conclusions', 'S1_few_shot_recovery'];

const files = process.argv.length > 2 ? process.argv.slice(2) : DEFAULT;

// Prose only: drop comment blocks, blockquote drafting notes, table rows,
// fenced code, and headings.
function prose(md) {
  return md
    .replace(/<!--[\s\S]*?-->/g, '')
    .replace(/```[\s\S]*?```/g, '')
    .split(/\r?\n/)
    .filter(l => !/^\s*>/.test(l) && !/^\s*\|/.test(l) && !/^\s*#/.test(l))
    .join('\n');
}

// Sentence split that does not break on decimals, initials, or "e.g.".
// Paragraphs are split first: a blank line always ends a sentence, and merging
// across it would report two short sentences as one long one. Bold run-in
// headers such as "**Q3. Recoverability.**" also end a sentence, even though the
// full stop is followed by asterisks rather than by a space.
function sentences(text) {
  return text
    .split(/\n\s*\n/)                       // paragraphs
    .flatMap(par => par
      .replace(/\s+/g, ' ')
      .replace(/\.\*\*\s+/g, '.** ')        // normalise the run-in header form
      .split(/(?<![A-Z])(?<!\d)\.(?:\*\*)?\s+(?=[*A-Z“"(])/))
    .map(s => s.trim())
    .filter(s => s.split(/\s+/).length > 2);
}

let totalDash = 0;
const rows = [];

for (const f of files) {
  const p = path.join(ROOT, f.endsWith('.md') ? f : f + '.md');
  if (!fs.existsSync(p)) { console.error('missing: ' + p); continue; }
  const text = prose(fs.readFileSync(p, 'utf8'));
  const dashes = (text.match(/[—–]/g) || []).length;
  totalDash += dashes;
  const sents = sentences(text);
  const lens = sents.map(s => s.split(/\s+/).length).sort((a, b) => a - b);
  const mean = lens.length ? lens.reduce((a, b) => a + b, 0) / lens.length : 0;
  const median = lens.length ? lens[Math.floor(lens.length / 2)] : 0;
  const over25 = lens.filter(l => l > 25).length;
  rows.push({ f, dashes, n: lens.length, mean, median, max: lens[lens.length - 1] || 0, over25 });

  if (process.env.VERBOSE && sents.length) {
    const worst = sents.slice().sort((a, b) => b.split(/\s+/).length - a.split(/\s+/).length).slice(0, 3);
    console.log(`\n--- ${f}: three longest sentences`);
    for (const s of worst) console.log(`  (${s.split(/\s+/).length}w) ${s.slice(0, 150)}...`);
  }
}

console.log('\nfile                       dashes  sents   mean  median   max  >25w');
console.log('-------------------------------------------------------------------');
for (const r of rows) {
  console.log(
    r.f.padEnd(26) +
    String(r.dashes).padStart(6) +
    String(r.n).padStart(7) +
    r.mean.toFixed(1).padStart(7) +
    String(r.median).padStart(8) +
    String(r.max).padStart(6) +
    String(r.over25).padStart(6));
}
console.log(`\ntotal dashes in prose: ${totalDash}`);
console.log('Target: 0 dashes, mean about 15 words, longest under about 25.');
console.log('Run with VERBOSE=1 to print the longest sentences per file.');

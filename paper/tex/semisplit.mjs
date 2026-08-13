/*
 * semisplit.mjs — turn "clause; clause" into two sentences where it is safe.
 *
 * Much of the remaining sentence length is semicolons joining two independent
 * clauses. Splitting those is mechanical, but only when the second clause can
 * really begin a sentence, so the split is restricted to clauses opening with a
 * determiner or pronoun. Enumerations such as "(a) x; (b) y", and anything
 * inside code spans, tables, notes or comment blocks, are left alone.
 *
 *   node paper/tex/semisplit.mjs --dry 03_methods
 *   node paper/tex/semisplit.mjs 03_methods 02_related_work
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve('paper');
const DRY = process.argv.includes('--dry');
const files = process.argv.slice(2).filter(a => a !== '--dry');

// Openers that reliably begin an independent clause in this manuscript.
const OPENER = /^(the|it|this|these|those|they|we|each|every|all|both|no|there|a|an|its|our|that)\b/i;

// Placeholder for masked code spans. It must be something the prose cannot
// contain: a bare number would collide with values like "30 valid pixels" and
// the restore step would eat them.
const OPEN = '', CLOSE = '';

let total = 0;
const samples = [];

for (const stem of files) {
  const f = stem.endsWith('.md') ? stem : stem + '.md';
  const p = path.join(ROOT, f);
  const lines = fs.readFileSync(p, 'utf8').split(/\r?\n/);
  let inComment = false, inFence = false;

  const out = lines.map(line => {
    if (/<!--/.test(line)) inComment = true;
    if (/^```/.test(line)) inFence = !inFence;
    const skip = inComment || inFence || /^\s*[>|#]/.test(line);
    if (/-->/.test(line)) inComment = false;
    if (skip || !line.includes(';')) return line;

    const spans = [];
    let masked = line.replace(/`[^`]*`/g, m => OPEN + (spans.push(m) - 1) + CLOSE);

    masked = masked.replace(/; ([a-z])/g, (m, ch, off, s) => {
      if (!OPENER.test(s.slice(off + 2))) return m;
      total++;
      if (samples.length < 8) samples.push(s.slice(Math.max(0, off - 55), off + 45));
      return '. ' + ch.toUpperCase();
    });

    return masked.replace(new RegExp(OPEN + '(\\d+)' + CLOSE, 'g'), (_, i) => spans[+i]);
  });

  if (!DRY) fs.writeFileSync(p, out.join('\n'));
  console.log(`${f}: ${DRY ? 'would split' : 'split'}`);
}

console.log(`\n${DRY ? 'would split' : 'split'} ${total} semicolon(s)`);
for (const s of samples) console.log('  ...' + s.replace(/\s+/g, ' '));
if (DRY) console.log('\n(dry run: nothing written)');

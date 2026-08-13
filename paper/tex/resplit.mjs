/*
 * resplit.mjs — whitespace-tolerant sentence splitting for the STYLE.md pass.
 *
 * The manuscript is hard-wrapped, so a literal find/replace has to guess where
 * the line breaks fall and fails when it guesses wrong. This matches on
 * normalised whitespace instead, so an edit only has to be right about the
 * words.
 *
 * It also refuses any edit that would drop a content word. The failure mode of
 * this exercise is losing a clause while every number still checks out, which
 * happened five times before this guard existed.
 *
 * Usage: import { applyEdits } and pass [[find, replace], ...] with the text
 * written as single-spaced prose.
 */
import fs from 'node:fs';

const norm = s => s.replace(/\s+/g, ' ').trim();
const contentWords = s => norm(s).toLowerCase()
  .replace(/[^a-z0-9à-ÿğüşıöç ]/g, ' ').split(/\s+/).filter(w => w.length >= 5);

export function applyEdits(file, pairs) {
  let src = fs.readFileSync(file, 'utf8');
  let applied = 0, missed = 0, rejected = 0;

  for (const [find, repl] of pairs) {
    const f = norm(find);
    const re = new RegExp(f.split(' ')
      .map(w => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('\\s+'));
    if (!re.test(src)) { console.error('MISS: ' + f.slice(0, 62)); missed++; continue; }

    const before = contentWords(find);
    const after = new Set(contentWords(repl));
    const lost = [...new Set(before.filter(w => !after.has(w)))];
    if (lost.length) {
      console.error(`REJECT (drops: ${lost.join(', ')}): ${f.slice(0, 48)}`);
      rejected++; continue;
    }
    src = src.replace(re, () => repl);
    applied++;
  }

  fs.writeFileSync(file, src);
  console.log(`${file}: applied ${applied}, missed ${missed}, rejected ${rejected}`);
  return { applied, missed, rejected };
}

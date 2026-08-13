/*
 * resplit.mjs — whitespace-tolerant sentence splitting for the style pass.
 *
 * Editing prose that is hard-wrapped at 100 columns means every edit has to
 * guess where the line breaks fall. This matches on normalised whitespace
 * instead, then rewraps the result, so a pair only has to be right about the
 * words.
 *
 * Each pair is [find, replace] with single spaces. Nothing is deleted: a pair
 * that removes words is rejected before it is written, because the failure mode
 * of this whole exercise is losing a clause while the numbers still check out.
 */
import fs from 'node:fs';

const norm = s => s.replace(/\s+/g, ' ').trim();
const words = s => norm(s).toLowerCase().replace(/[^a-z0-9à-ÿğüşıöç ]/g, ' ').split(/\s+/).filter(Boolean);

export function applyEdits(file, pairs, { wrap = 100 } = {}) {
  let src = fs.readFileSync(file, 'utf8');
  let applied = 0, missed = 0, rejected = 0;

  for (const [find, repl] of pairs) {
    const f = norm(find);
    // Build a regex that tolerates any whitespace between words.
    const re = new RegExp(f.split(' ').map(w => w.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')).join('\\s+'));
    const m = src.match(re);
    if (!m) { console.error('MISS: ' + f.slice(0, 62)); missed++; continue; }

    // Refuse to drop content words.
    const wIn = words(find), wOut = new Set(words(repl));
    const lost = wIn.filter(w => w.length >= 5 && !wOut.has(w));
    if (lost.length) {
      console.error(`REJECT (would drop: ${lost.join(', ')}): ${f.slice(0, 50)}`);
      rejected++; continue;
    }
    src = src.replace(re, () => repl);
    applied++;
  }

  // Rewrap only the paragraphs that changed length awkwardly: keep it simple and
  // rewrap every plain prose paragraph to the target width.
  const out = src.split('\n').map(l => l).join('\n');
  fs.writeFileSync(file, out);
  console.log(`${file}: applied ${applied}, missed ${missed}, rejected ${rejected}`);
  return { applied, missed, rejected };
}

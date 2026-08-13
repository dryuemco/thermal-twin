/*
 * rewrap.mjs — rewrap manuscript prose to the file's 100-column convention.
 *
 * Splitting sentences leaves paragraphs as one very long line. This puts them
 * back to the width the rest of the file uses, so diffs stay readable.
 *
 * Left alone: headings, table rows, blockquotes, comment blocks, fenced code,
 * list items whose continuation indent would be lost, and any line already
 * under the limit.
 *
 * Usage: node paper/tex/rewrap.mjs 02_related_work 03_methods
 */
import fs from 'node:fs';
import path from 'node:path';

const WIDTH = 100;
const ROOT = path.resolve('paper');

for (const stem of process.argv.slice(2)) {
  const f = stem.endsWith('.md') ? stem : stem + '.md';
  const p = path.join(ROOT, f);
  const lines = fs.readFileSync(p, 'utf8').split(/\r?\n/);
  const out = [];
  let inComment = false, inFence = false;

  for (const line of lines) {
    if (/<!--/.test(line)) inComment = true;
    if (/^```/.test(line)) inFence = !inFence;
    const skip = inComment || inFence || /^\s*[>|#]/.test(line) ||
                 /^\s*[-*]\s/.test(line) || /^\s*\d+\.\s/.test(line) ||
                 /^\s{2,}\S/.test(line) || line.length <= WIDTH;
    if (/-->/.test(line)) inComment = false;

    if (skip) { out.push(line); continue; }

    const words = line.trim().split(/\s+/);
    let cur = '';
    for (const w of words) {
      if (cur && (cur + ' ' + w).length > WIDTH) { out.push(cur); cur = w; }
      else cur = cur ? cur + ' ' + w : w;
    }
    if (cur) out.push(cur);
  }

  fs.writeFileSync(p, out.join('\n'));
  console.log(`rewrapped ${f}`);
}

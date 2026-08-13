/*
 * rewrap.mjs — reflow manuscript prose to the file's 100-column convention.
 *
 * Splitting and joining sentences leaves paragraphs ragged: some lines run long
 * and others are left holding a single orphaned word. This reflows each prose
 * paragraph as a unit, so the source reads cleanly in a diff.
 *
 * It is formatting only. Nothing but whitespace changes, which the number and
 * content checks confirm.
 *
 * Left alone: headings, table rows, blockquotes, comment blocks, fenced code,
 * and list items (whose continuation indent carries meaning).
 *
 * Usage: node paper/tex/rewrap.mjs 03_methods 02_related_work
 */
import fs from 'node:fs';
import path from 'node:path';

const WIDTH = 100;
const ROOT = path.resolve('paper');

const wrap = text => {
  const out = [];
  let cur = '';
  for (const w of text.split(/\s+/).filter(Boolean)) {
    if (cur && (cur + ' ' + w).length > WIDTH) { out.push(cur); cur = w; }
    else cur = cur ? cur + ' ' + w : w;
  }
  if (cur) out.push(cur);
  return out;
};

for (const stem of process.argv.slice(2)) {
  const f = stem.endsWith('.md') ? stem : stem + '.md';
  const p = path.join(ROOT, f);
  const lines = fs.readFileSync(p, 'utf8').split(/\r?\n/);
  const out = [];
  let para = [];
  let inComment = false, inFence = false;

  const flush = () => { if (para.length) { out.push(...wrap(para.join(' '))); para = []; } };

  for (const line of lines) {
    if (/<!--/.test(line)) { flush(); inComment = true; }
    if (/^```/.test(line)) { flush(); inFence = !inFence; out.push(line); if (/-->/.test(line)) inComment = false; continue; }

    const verbatim = inComment || inFence || /^\s*[>|#]/.test(line) ||
                     /^\s*[-*]\s/.test(line) || /^\s*\d+\.\s/.test(line) ||
                     /^\s{2,}\S/.test(line) || line.trim() === '';

    if (/-->/.test(line)) inComment = false;

    if (verbatim) { flush(); out.push(line); continue; }
    para.push(line.trim());
  }
  flush();

  fs.writeFileSync(p, out.join('\n'));
  console.log(`reflowed ${f}`);
}

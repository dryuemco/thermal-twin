/*
 * check_splits.mjs — find damage left by the sentence-splitting style pass.
 *
 * The number and content checks pass on all of these, because a broken sentence
 * keeps every number and every word. Only reading, or these scans, catches them.
 * Each pattern here corresponds to a fault that was actually found and fixed:
 *
 *   fragment      a full stop followed by a lowercase word, which means a
 *                 subordinate clause was cut loose from its main clause
 *                 ("...smoke detection. which share the vocabulary...")
 *   paren-break   a sentence boundary inserted inside brackets, where a
 *                 sentence cannot start ("(natural vegetation, primary. All
 *                 valid cells, secondary)")
 *   dangling-list an enumeration whose "; and" tail survived after its head was
 *                 cut off by a full stop
 *   weak-open     a sentence beginning "And"/"Or", usually a split artefact
 *
 * Lines are joined before scanning, because a broken sentence often has the
 * full stop at the end of one line and the fragment at the start of the next.
 * An earlier version scanned line by line and missed every one of them.
 *
 * Usage: node paper/tex/check_splits.mjs
 */
import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve('paper');
const FILES = ['00_abstract', '01_introduction', '02_related_work', '03_methods',
               '04_results', '05_discussion', '06_conclusions', 'supplementary'];

// Abbreviations that legitimately end in a full stop mid-sentence.
const ABBREV = /(e\.g|i\.e|cf|vs|al|etc|approx|Fig|Eq|St|No|Dr|Prof|Sect)\.$/;

let found = 0;
for (const stem of FILES) {
  const p = path.join(ROOT, stem + '.md');
  const flat = fs.readFileSync(p, 'utf8')
    .replace(/<!--[\s\S]*?-->/g, '')
    .split(/\r?\n/).filter(l => !/^\s*[>|#]/.test(l))
    .join(' ').replace(/\s+/g, ' ');

  const hits = [];

  // fragment: ". lowercaseword"
  for (const m of flat.matchAll(/\.\s([a-zà-ÿ][a-zà-ÿ]*)\s/g)) {
    const pre = flat.slice(Math.max(0, m.index - 12), m.index + 1);
    if (ABBREV.test(pre)) continue;
    hits.push(`fragment: ...${flat.slice(Math.max(0, m.index - 55), m.index + 60).trim()}`);
  }

  // paren-break: "( ... . Capital ... )"
  for (const m of flat.matchAll(/\([^()]{0,110}\.\s[A-Z][^()]{0,110}\)/g)) {
    if (ABBREV.test(m[0].slice(0, m[0].indexOf('. ') + 1))) continue;
    hits.push(`paren-break: ${m[0].slice(0, 115)}`);
  }

  // dangling list tail
  for (const m of flat.matchAll(/[^.]{0,90}; (and|or) [^.]{0,45}\./g))
    hits.push(`dangling-list: ...${m[0].slice(-100)}`);

  // weak opener
  for (const m of flat.matchAll(/\.\s(And|Or)\s[^.]{0,60}/g))
    hits.push(`weak-open: ${m[0].slice(0, 80)}`);

  if (hits.length) {
    found += hits.length;
    console.log(`\n${stem} (${hits.length})`);
    for (const h of hits) console.log('  ' + h);
  }
}

console.log(found ? `\n${found} suspect site(s) — read each before dismissing it`
                  : '\nno split damage found');
process.exit(found ? 1 : 0);

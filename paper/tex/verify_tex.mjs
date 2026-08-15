/*
 * verify_tex.mjs — does the LaTeX port preserve the manuscript?
 *
 * The port is only trustworthy if no number changed and no cross-reference
 * dangles. This checks both, plus a few LaTeX-specific failure modes that a
 * missing TeX installation would otherwise leave undetected until submission.
 *
 * Usage: node paper/tex/verify_tex.mjs
 */

import fs from 'node:fs';
import path from 'node:path';

// PAPER_ROOT so the companion manuscript is verified by the same checks.
// Absent, the root is 'paper' and Paper 1's verdict is unchanged.
const ROOT = path.resolve(process.env.PAPER_ROOT || 'paper');
const read = f => fs.readFileSync(path.join(ROOT, f), 'utf8');
// Appendices are part of the body the converter emits, so they must be part of
// the Markdown side of the comparison too; otherwise every number that lives
// only in an appendix reads as invented.
// A1_sensitivity is released as paper/supplementary_appendices.md rather than
// printed, so it is no longer part of the built document and must not be
// compared against it: every number in it would read as one the LaTeX dropped.
const SECTIONS = ['01_introduction', '02_related_work', '03_methods',
                  '04_results', '05_discussion', '06_conclusions',
                  'A2_diagnostics', 'A3_protocol']
  .filter(f => fs.existsSync(path.join(path.resolve(process.env.PAPER_ROOT || 'paper'), f + '.md')));

let fail = 0;
const check = (name, ok, detail = '') => {
  console.log(`${ok ? 'PASS' : 'FAIL'}  ${name}${detail ? ' — ' + detail : ''}`);
  if (!ok) fail++;
};

// Markdown body as the converter sees it: no comment blocks, no blockquotes.
let md = SECTIONS.map(f => read(f + '.md')).join('\n')
  .replace(/<!--[\s\S]*?-->/g, '')
  .split(/\r?\n/).filter(l => !/^>\s?/.test(l)).join('\n');

const tex = read('tex/manuscript.tex');
// The body is what was ported from the Markdown. Everything the template
// generates is excluded: the frontmatter above it, and below it the journal
// declarations (CRediT, competing interest, funding, data availability) and the
// figure captions, which are maintained in their own file. The declarations
// carry facts that exist nowhere in the Markdown, such as the grant number, so
// including them would make the number comparison report inventions that are
// not inventions.
const DECLARATIONS = '% ------------------------------------------------------------ declarations --';
const FIGURES = '% ---------------------------------------------------------------- figures --';
const bodyEnd = [DECLARATIONS, FIGURES]
  .map(m => tex.indexOf(m))
  .filter(i => i !== -1)
  .reduce((a, b) => Math.min(a, b), tex.length);
// Figure environments are now placed at their first reference rather than
// appended after the body, so the slice above no longer excludes them. They are
// still authored in figure_captions.tex as LaTeX, not ported from the Markdown,
// so they are cut out here for the same reason the declarations are: their
// numbers (190 mm column widths, scale bars, region years) exist nowhere in the
// Markdown and would be reported as inventions.
const body = tex.slice(tex.indexOf('\\end{frontmatter}'), bodyEnd)
  .replace(/\\begin\{figure\}[\s\S]*?\\end\{figure\}/g, '')
  // Counter plumbing emitted with \appendix is template output too, and its
  // \setcounter{figure}{0} would otherwise read as an invented number.
  .replace(/\\setcounter\{[^}]*\}\{[^}]*\}/g, '')
  .replace(/\\makeatletter[\s\S]*?\\makeatother/g, '');

// ------------------------------------------------------------ 1. numbers --
// Unicode superscripts and subscripts are digits too: 10^-8 is written with
// them in the Markdown and as math in the LaTeX. Fold them to ASCII on the
// Markdown side or every exponent reads as an invented number.
const SCRIPTS = { '⁰':'0','¹':'1','²':'2','³':'3','⁴':'4','⁵':'5',
                  '⁶':'6','⁷':'7','⁸':'8','⁹':'9','⁻':'-','⁺':'+',
                  '₀':'0','₁':'1','₂':'2','₃':'3','₄':'4','₅':'5',
                  '₆':'6','₇':'7','₈':'8','₉':'9' };
// A separator is required: "10²" must fold to "10 2", not "102", or the base
// and its exponent merge into a number that exists in neither document.
md = md.replace(/[⁰¹²³⁴-⁹⁺⁻₀-₉]+/g, run => ' ' + [...run].map(c => SCRIPTS[c]).join('') + ' ');

const nums = s => (s.match(/\d+(?:[.,]\d+)*/g) || []).map(x => x.replace(/,/g, ''));
const tally = a => a.reduce((m, x) => m.set(x, (m.get(x) || 0) + 1), new Map());

// Two categories of number legitimately disappear, because LaTeX generates them
// instead of the source carrying them. Both are counted from the Markdown and
// forgiven exactly, so a real loss of the same digit is still caught.
const generated = [];
//  (a) figure references: "Fig. 3" becomes \ref{fig:within-robustness}
for (const m of md.matchAll(/\b(?:Figs?\.?|Figures?)\s+(\d+)/g)) generated.push(m[1]);
//  (b) numbered-list markers: "3. Item" becomes \item
for (const m of md.matchAll(/^\s*(\d+)\.\s+\S/gm)) generated.push(m[1]);
const forgiven = tally(generated);

const A = tally(nums(md)), B = tally(nums(body));
const missing = [], extra = [];
for (const [k, v] of A) {
  const w = (B.get(k) || 0) + (forgiven.get(k) || 0);
  if (w < v) missing.push(`${k} (md ${v}, tex ${B.get(k) || 0}, generated-by-LaTeX ${forgiven.get(k) || 0})`);
}
for (const [k, v] of B) { const w = A.get(k) || 0; if (v > w) extra.push(`${k} (tex ${v}, md ${w})`); }
check('every number in the Markdown survives into the LaTeX', missing.length === 0,
      missing.slice(0, 10).join('; '));
check('the LaTeX invents no number the Markdown lacks', extra.length === 0,
      extra.slice(0, 10).join('; '));

// ------------------------------------------------- 2. dangling references --
const labels = new Set([...tex.matchAll(/\\label\{([^}]+)\}/g)].map(m => m[1]));
// A manuscript with no figures yet has no captions file. That is not a
// failure; it only means no fig: label can be contributed from outside.
const CAPFILE = path.join(ROOT, 'figure_captions.tex');
if (fs.existsSync(CAPFILE)) {
  for (const m of fs.readFileSync(CAPFILE, 'utf8').matchAll(/\\label\{([^}]+)\}/g)) labels.add(m[1]);
}
const refs = [...tex.matchAll(/\\ref\{([^}]+)\}/g)].map(m => m[1]);
const dangling = [...new Set(refs.filter(r => !labels.has(r)))];
check('no \\ref points at a missing \\label', dangling.length === 0, dangling.join(', '));

// ------------------------------------------------- 3. citation keys exist --
const bibKeys = new Set([...read('REFERENCES.bib').matchAll(/@\w+\{([^,]+),/g)].map(m => m[1].trim()));
const cited = new Set();
for (const m of tex.matchAll(/\\cite[tp]\{([^}]+)\}/g))
  m[1].split(',').forEach(k => cited.add(k.trim()));
const badKeys = [...cited].filter(k => !bibKeys.has(k));
check('every \\cite key resolves in REFERENCES.bib', badKeys.length === 0, badKeys.join(', '));
const uncited = [...bibKeys].filter(k => !cited.has(k));
check('every bibliography entry is cited', uncited.length === 0, uncited.join(', '));

// --------------------------------------------- 4. LaTeX structural sanity --
const braces = [...tex].reduce((a, c) => a + (c === '{' ? 1 : c === '}' ? -1 : 0), 0);
check('braces balance', braces === 0, `net ${braces}`);

const mathDollars = (body.match(/(?<!\\)\$/g) || []).length;
check('inline math delimiters pair up', mathDollars % 2 === 0, `${mathDollars} unescaped $`);

const envs = {};
for (const m of tex.matchAll(/\\(begin|end)\{(table|tabular|figure|itemize|enumerate)\}/g))
  envs[m[2]] = (envs[m[2]] || 0) + (m[1] === 'begin' ? 1 : -1);
const unbalanced = Object.entries(envs).filter(([, v]) => v !== 0);
check('environments open and close', unbalanced.length === 0,
      unbalanced.map(([k, v]) => `${k}:${v}`).join(', '));

// Every tabular row must have the same column count as its preamble.
let rowProblems = [];
for (const m of tex.matchAll(/\\begin\{tabular\}\{([^}]*)\}([\s\S]*?)\\end\{tabular\}/g)) {
  const ncol = (m[1].match(/[lcr]/g) || []).length;
  for (const line of m[2].split('\n')) {
    if (!line.includes('&') || line.trim().startsWith('\\hline')) continue;
    const cells = line.split(/(?<!\\)&/).length;
    if (cells !== ncol) rowProblems.push(`${cells}/${ncol}: ${line.trim().slice(0, 60)}`);
  }
}
check('table rows match their column specification', rowProblems.length === 0,
      rowProblems.slice(0, 5).join(' | '));

// Raw percent signs would silently comment out the rest of a line. Whole-line
// LaTeX comments are exempt: a line whose first non-space character is % is a
// comment by construction and cannot swallow content. Everything else is
// prose, where an unescaped % means the converter missed one.
// A % as the last character of a line is LaTeX's line-continuation marker: it
// suppresses the newline and the space it would produce, and swallows nothing
// the reader would miss. The table wrapper emits one. Strip it before counting.
const rawPct = body
  .split('\n')
  .filter((line) => !/^\s*%/.test(line))
  .map((line) => line.replace(/%$/, ''))
  .reduce((n, line) => n + [...line.matchAll(/(?<!\\)%/g)].length, 0);
check('no unescaped % in the body', rawPct === 0, `${rawPct} found`);

// Escaped math: a sign that vaulting failed and an exponent got mangled.
const mangled = (body.match(/\\\$|\\textasciicircum/g) || []).length;
check('no escaped math delimiters (mangled exponents)', mangled === 0, `${mangled} found`);

// Leftover Markdown that the converter did not consume.
const leftovers = [];
if (/\[@/.test(body)) leftovers.push('unconverted [@citation]');
if (/^\s*\|/m.test(body)) leftovers.push('raw Markdown table row');
if (/\*\*/.test(body)) leftovers.push('raw ** bold');
if (/^#{1,6}\s/m.test(body)) leftovers.push('raw # heading');
// A doubled backtick is the LaTeX opening quote, produced deliberately from a
// straight " in the Markdown; only a lone backtick is unconsumed code-span
// syntax.
if (/`/.test(body.replace(/``/g, ''))) leftovers.push('raw backtick');
check('no Markdown syntax survives into the LaTeX', leftovers.length === 0, leftovers.join(', '));

console.log(`\n${fail === 0 ? 'ALL CHECKS PASSED' : fail + ' CHECK(S) FAILED'}`);
console.log('NOTE: these are source checks. They say the port did not corrupt the');
console.log('content; they do not say the file typesets. Run the compile as well:');
console.log('  pdflatex manuscript && bibtex manuscript && pdflatex manuscript x2');
console.log('MiKTeX is installed on this machine (see ENVIRONMENT.md). As of');
console.log('2026-08-14 both documents compile with no errors and no undefined');
console.log('references or citations.');
process.exit(fail === 0 ? 0 : 1);

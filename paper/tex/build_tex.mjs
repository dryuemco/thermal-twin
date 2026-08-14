/*
 * build_tex.mjs — deterministic Markdown -> LaTeX conversion for the manuscript.
 *
 * WHY A SCRIPT AND NOT HAND CONVERSION
 * Every number in this manuscript traces to a frozen output and must survive the
 * port byte-for-byte. Retyping ~29,000 words with 157 table rows by hand invites
 * exactly the transcription error this project spends most of its effort avoiding.
 * The script copies text; it never re-derives it. build_report.md lists every
 * judgement the script made so each can be reviewed.
 *
 * Usage:  node paper/tex/build_tex.mjs
 * Output: paper/tex/manuscript.tex, paper/tex/supplementary.tex,
 *         paper/tex/build_report.md
 */

import fs from 'node:fs';
import path from 'node:path';

const ROOT = path.resolve('paper');
const OUT = path.join(ROOT, 'tex');
const report = [];
const note = (cat, msg) => report.push({ cat, msg });

// ---------------------------------------------------------------- utilities --

// Unicode characters that must become LaTeX. Order matters: longest first.
const UNICODE = [
  ['\u2014', '---'],            // em dash
  ['\u2013', '--'],             // en dash
  ['\u2212', '$-$'],            // true minus
  ['\u00d7', '$\\times$'],
  ['\u2248', '$\\approx$'],
  ['\u2264', '$\\le$'],
  ['\u2265', '$\\ge$'],
  ['\u00b1', '$\\pm$'],
  ['\u00b0', '\\textdegree{}'],
  ['\u00b5', '$\\mu$'],
  ['\u03bb', '$\\lambda$'],
  ['\u03c1', '$\\rho$'],
  ['\u0394', '$\\Delta$'],
  ['\u2192', '$\\rightarrow$'],
  ['\u2194', '$\\leftrightarrow$'],
  ['\u2026', '\\ldots{}'],
  ['\u00a0', '~'],
  ['\u2019', "'"], ['\u2018', "'"], ['\u201c', '``'], ['\u201d', "''"],
  ['\u2032', "$'$"],
  ['\u2010', '-'], ['\u2011', '-'],
  // Added 2026-08-14, after the first real compile. pdflatex with T1 refuses
  // these outright; a true minus inside a code span was the first hard failure.
  ['\u03a3', '$\\Sigma$'],
  ['\u03c3', '$\\sigma$'],
  ['\u03c4', '$\\tau$'],
  ['\u03bc', '$\\mu$'],
  ['\u03b1', '$\\alpha$'],
  ['\u03b2', '$\\beta$'],
  ['\u00b7', '$\\cdot$'],
  ['\u2227', '$\\wedge$'],
  ['\u2228', '$\\vee$'],
  ['\u221a', '$\\surd$'],
  ['\u00bd', '$\\frac{1}{2}$'],
  ['\u00a7', '\\S{}'],
];

// Verbatim bodies are read byte by byte by pdflatex, so a non-ASCII character
// in one cannot be escaped or wrapped. These are the safe ASCII foldings; the
// builder warns about anything not listed here rather than emitting it.
const VERBATIM_ASCII = {
  '−': '-', '–': '-', '—': '--', '·': '*', '×': 'x', '≈': '~', '≤': '<=', '≥': '>=',
  '±': '+/-', '°': ' deg', 'λ': 'lambda', 'μ': 'mu', 'σ': 'sigma', 'Σ': 'sum',
  'ρ': 'rho', 'τ': 'tau', 'Δ': 'delta', '→': '->', '↔': '<->', '’': "'", '‘': "'",
  '“': '"', '”': '"', '…': '...',
};

// Superscript / subscript digits used in exponents such as 10^-7.
const SUPS = { '\u2070':'0','\u00b9':'1','\u00b2':'2','\u00b3':'3','\u2074':'4','\u2075':'5',
               '\u2076':'6','\u2077':'7','\u2078':'8','\u2079':'9','\u207b':'-','\u207a':'+' };
const SUBS = { '\u2080':'0','\u2081':'1','\u2082':'2','\u2083':'3','\u2084':'4','\u2085':'5',
               '\u2086':'6','\u2087':'7','\u2088':'8','\u2089':'9' };

// Collapse runs of superscript/subscript characters into math mode. The result
// MUST be vaulted: it contains $ and ^, which the later escaping pass would
// otherwise turn into \$ and \textasciicircum{}, silently corrupting every
// exponent in the paper (10^-8 is not a decoration here, it is a result).
function foldScripts(s, vault) {
  s = s.replace(new RegExp('[' + Object.keys(SUPS).join('') + ']+', 'g'),
    m => vault.put('$^{' + [...m].map(c => SUPS[c]).join('') + '}$'));
  s = s.replace(new RegExp('[' + Object.keys(SUBS).join('') + ']+', 'g'),
    m => vault.put('$_{' + [...m].map(c => SUBS[c]).join('') + '}$'));
  return s;
}

function escapeLatex(s) {
  // The backslash is parked behind a sentinel first. Replacing it inline with
  // \textbackslash{} put braces into the string that the very next rule then
  // escaped, so a literal backslash came out as \textbackslash\{\}.
  const BS = 'BS';
  let out = s
    .replace(/\\/g, BS)
    .replace(/([&%#$_])/g, '\\$1')
    .replace(/\{/g, '\\{').replace(/\}/g, '\\}')
    .replace(/\^/g, '\\textasciicircum{}');
  // Code spans and other verbatim-ish text take this path instead of inline(),
  // so without this they emitted raw Unicode. That is what stopped the first
  // compile: `(current_median − baseline_mean)` carries a true minus.
  out = applyUnicode(out);
  return out.split(BS).join('\\textbackslash{}');
}

// Combining macron (U+0304) after a letter, as in the D-bar of Schoener's
// overlap. Handled before the table of single characters, because it modifies
// the character in front of it.
function applyUnicode(s) {
  let out = s.replace(/([A-Za-z])̄/g, '$\\bar{$1}$');
  for (const [from, to] of UNICODE) out = out.split(from).join(to);
  return out;
}

// Figure labels, in figure-number order, read from figure_captions.tex so the
// two files cannot drift apart. "Fig. 3" in the prose resolves to the third
// \label in that file.
const FIGLABELS = [...fs.readFileSync(path.join(ROOT, 'figure_captions.tex'), 'utf8')
  .matchAll(/\\label\{(fig:[^}]+)\}/g)].map(m => m[1]);

let FOOTNOTES = new Map();
const FOOTNOTE_REF_RE = /\[\^([^\]]+)\]/g;
const FOOTNOTE_CMD = '\\footnote';

// Which tables actually exist. A "**Table N.**" paragraph only counts if a
// Markdown table follows it; otherwise it is prose that merely names a table.
// Built in a pre-pass so that a reference appearing before its table still
// resolves.
const TABLELABELS = new Set();
function collectTableLabels(files) {
  for (const f of files) {
    const lines = fs.readFileSync(path.join(ROOT, f + '.md'), 'utf8')
      .replace(/<!--[\s\S]*?-->/g, '').split(/\r?\n/);
    for (let k = 0; k < lines.length; k++) {
      const m = lines[k].match(/^\*\*Table\s+([RS]?\d+)/);
      if (!m) continue;
      let j = k + 1;
      while (j < lines.length && lines[j].trim() !== '' && !/^\|/.test(lines[j])) j++;
      while (j < lines.length && lines[j].trim() === '') j++;
      if (j < lines.length && /^\|/.test(lines[j])) TABLELABELS.add('tab:' + m[1]);
    }
  }
}

// Placeholder machinery: protect spans that must not be escaped.
class Vault {
  constructor() { this.items = []; }
  put(tex) { this.items.push(tex); return `\u0000${this.items.length - 1}\u0000`; }
  restore(s) { return s.replace(/\u0000(\d+)\u0000/g, (_, i) => this.items[+i]); }
}

// ------------------------------------------------------------ inline markup --

function inline(src, vault) {
  let s = src;

  // 1. Code spans -> \texttt{}, vaulted (they contain _ and { legitimately).
  //    Typewriter text does not hyphenate, so an identifier like
  //    burnable_tree_shrub_grass is one unbreakable box and runs straight out
  //    of a narrow table column. A break opportunity is offered after each
  //    underscore, slash and dot. \allowbreak adds no character and no hyphen,
  //    so the identifier is still copied out of the PDF verbatim.
  s = s.replace(/`([^`]+)`/g, (_, code) =>
    vault.put('\\texttt{'
      + escapeLatex(code)
          .replace(/(\\_|\/)/g, '$1\\allowbreak{}')
          // A dot between digits is a decimal point and must not be broken:
          // breaking `500.0` split the number in two and the number check
          // caught it. Only dots in identifiers get a break opportunity.
          .replace(/(?<!\d)\.(?!\d)/g, '.\\allowbreak{}')
      + '}'));

  // 1b. Footnote references -> footnote command, with the note body converted
  //     through the same inline pipeline so its citations and symbols survive.
  //     A footnote left unhandled is escaped into visible junk and its text is
  //     stranded as a stray paragraph.
  s = s.replace(FOOTNOTE_REF_RE, (m, id) => {
    const text = FOOTNOTES.get(id);
    if (text === undefined) {
      note("review", "FOOTNOTE REFERENCE WITH NO DEFINITION: " + m);
      return m;
    }
    return vault.put(FOOTNOTE_CMD + "{" + escapeOutsideVault(inline(text, vault)) + "}");
  });

  // 2. Citations. Two forms:
  //    "Author et al. [@Key]"  -> \citet{Key}   (narrative: name already in text)
  //    "[@Key]" / "[@A; @B]"   -> \citep{A,B}
  s = s.replace(/((?:[A-Z][\w'\u00c0-\u024f-]*)(?:\s+(?:et\s+al\.|and\s+[A-Z][\w'\u00c0-\u024f-]*))?)\s*\[@([^\]]+)\]/g,
    (m, name, keys) => {
      const list = keys.split(';').map(k => k.trim().replace(/^@/, ''));
      if (list.length === 1 && /et al\.|and /.test(name)) {
        // Narrative citation: the author name is already written out in the
        // prose, and \citet prints it again. Drop the literal name and let
        // natbib render "Name et al. (year)". The dropped text is logged so the
        // substitution can be checked against the bibliography.
        note('citation', `narrative: "${m.trim()}" -> \\citet{${list[0]}} (literal name dropped)`);
        return vault.put('\\citet{' + list[0] + '}');
      }
      return name + ' ' + vault.put('\\citep{' + list.join(',') + '}');
    });
  s = s.replace(/\[@([^\]]+)\]/g, (_, keys) =>
    vault.put('\\citep{' + keys.split(';').map(k => k.trim().replace(/^@/, '')).join(',') + '}'));

  // 3. Cross references to sections. "Section 3.16.4" / "Sections 3.1, 3.3 and 3.16.4"
  s = s.replace(/\b(Sections?)\s+(\d+(?:\.\d+)*(?:\s*(?:,|and|&)\s*\d+(?:\.\d+)*)*)/g,
    (m, word, nums) => {
      const refs = nums.match(/\d+(?:\.\d+)*/g) || [];
      let out = word + '~';
      const seps = nums.split(/\d+(?:\.\d+)*/).slice(1, -1);
      refs.forEach((r, i) => {
        out += vault.put('\\ref{sec:' + r + '}');
        if (i < refs.length - 1) out += (seps[i] || ', ');
      });
      return out;
    });

  // 4. Figure and table references. The figure captions carry semantic labels
  //    (fig:study-map, ...), not fig:1, so map the manuscript's figure numbers
  //    onto them in caption order.
  const figref = n => {
    const lab = FIGLABELS[+n - 1];
    if (!lab) { note('review', `FIGURE ${n} REFERENCED BUT NO CAPTION WITH THAT NUMBER`); return '\\ref{fig:' + n + '}'; }
    return '\\ref{' + lab + '}';
  };
  s = s.replace(/\bFigs?\.?\s+(\d+)/g, (m, n) => 'Fig.~' + vault.put(figref(n)));
  s = s.replace(/\bFigures?\s+(\d+)/g, (m, n) => 'Fig.~' + vault.put(figref(n)));
  // Only reference tables that exist. "Table 2" is the feature dictionary that
  // is still to be assembled, and a \ref to it would compile to a bare "??".
  s = s.replace(/\bTables?\s+([RS]?\d+)/g, (m, n) => {
    if (!TABLELABELS.has('tab:' + n)) {
      note('review', `TABLE ${n} REFERENCED BUT NOT PRESENT — left as literal text`);
      return m;
    }
    return 'Table~' + vault.put('\\ref{tab:' + n + '}');
  });

  // 5. Bold / italic.
  s = s.replace(/\*\*([^*]+)\*\*/g, (_, t) => '\\textbf{' + t + '}');
  s = s.replace(/(?<![*\w])\*([^*\n]+)\*(?![*\w])/g, (_, t) => '\\emph{' + t + '}');

  // 6. "~500 m" -> approximately.
  s = s.replace(/~(?=\d)/g, vault.put('$\\sim$'));

  // 7. Unicode, superscripts, then escape whatever is left.
  s = s.replace(/([A-Za-z])̄/g, (_, c) => vault.put('$\\bar{' + c + '}$'));
  for (const [from, to] of UNICODE) s = s.split(from).join(vault.put(to));
  s = foldScripts(s, vault);

  // Protect the LaTeX we just emitted before escaping the plain text.
  s = s.replace(/\\(textbf|emph|texttt)\{/g, (m) => vault.put(m));
  s = s.replace(/\}/g, (m) => m); // braces of the above are handled by escape below

  return s;
}

// Escaping pass that leaves vaulted content alone.
function escapeOutsideVault(s) {
  return s.split(/(\u0000\d+\u0000)/).map(chunk => {
    if (/^\u0000\d+\u0000$/.test(chunk)) return chunk;
    return chunk
      .replace(/([&%#$_])/g, '\\$1')
      .replace(/\^/g, '\\textasciicircum{}');
  }).join('');
}

// ------------------------------------------------------------------ tables --

function convertTable(lines, vault, caption, label) {
  // Split on unescaped pipes only: cells legitimately contain "\|", as in the
  // conditional-probability notation P(y\|x), and splitting on those would
  // silently shear a column off the row.
  const rows = lines.map(l => l.trim().replace(/^\|/, '').replace(/\|$/, '')
    .split(/(?<!\\)\|/).map(c => c.trim().replace(/\\\|/g, '|')));
  const sep = rows.findIndex(r => r.every(c => /^:?-{2,}:?$/.test(c)));
  if (sep < 0) { note('table', 'no header separator; emitted as-is: ' + caption); return null; }
  const head = rows.slice(0, sep);
  const body = rows.slice(sep + 1);
  const ncol = Math.max(...rows.map(r => r.length));
  const align = rows[sep].map(c => (c.startsWith(':') && c.endsWith(':')) ? 'c' : c.endsWith(':') ? 'r' : 'l');
  while (align.length < ncol) align.push('l');

  // Column widths. An l column never wraps, so a table whose cells carry prose
  // runs off the page: the first compile produced 137 overfull boxes, the worst
  // 763pt on a text width of about 390pt. Columns that hold long text become
  // wrapping X columns in a tabularx sized to the line; short numeric columns
  // keep their natural alignment so the numbers still line up.
  const widest = Array.from({ length: ncol }, (_, i) =>
    Math.max(...rows.filter((_, k) => k !== sep).map(r => (r[i] || '').length)));
  // Two different problems need two different answers. A table with one or two
  // prose columns needs those columns to wrap. A table with ten numeric columns
  // needs a smaller font: wrapping there would shred the headers. The estimate
  // is in characters; LINE_CHARS is what one \small line holds in this layout,
  // and each column costs about 2.5 characters of \tabcolsep padding.
  const LINE_CHARS = 88;
  // 20 rather than 28: a ten-column table whose widest header is 27 characters
  // still ran 318pt past the margin at \scriptsize, because an l column cannot
  // wrap a header no matter how small the type gets.
  const WRAP_AT = 20;
  const rawWidth = widest.reduce((a, b) => a + b, 0) + 2.5 * ncol;
  const wrapping = widest.map(w => w > WRAP_AT);
  const useTabularx = wrapping.some(Boolean);
  // Font step chosen from the width that remains after wrapping is accounted
  // for; a wrapped column no longer contributes its full natural width.
  const effWidth = widest.reduce((a, w, i) => a + (wrapping[i] ? Math.min(w, WRAP_AT) : w), 0)
    + 2.5 * ncol;
  const size = effWidth <= LINE_CHARS ? '\\small'
    : effWidth <= LINE_CHARS * 1.25 ? '\\footnotesize'
    : '\\scriptsize';
  if (size !== '\\small' || useTabularx) {
    note('table', `${caption.slice(0, 44)}: ${ncol} cols, est. width ${Math.round(rawWidth)} chars `
      + `-> ${size.replace(/\\/, '')}${useTabularx ? ', ' + wrapping.filter(Boolean).length + ' wrapping' : ''}`);
  }
  const spec = align.map((a, i) => {
    if (!wrapping[i]) return a;
    const pre = a === 'r' ? '\\raggedleft' : a === 'c' ? '\\centering' : '\\raggedright';
    return `>{${pre}\\arraybackslash}X`;
  }).join('');
  if (useTabularx) {
    note('table', `${caption.slice(0, 48)}: ${wrapping.filter(Boolean).length} of ${ncol} `
      + `columns wrap (widest cell ${Math.max(...widest)} chars)`);
  }

  const cell = c => escapeOutsideVault(inline(c, vault));
  const out = [];
  out.push('\\begin{table}[htbp]');
  out.push('  \\centering');
  out.push('  ' + size);
  out.push('  \\caption{' + caption + '}');
  if (label) out.push('  \\label{' + label + '}');
  out.push(useTabularx
    ? '  \\begin{tabularx}{\\linewidth}{' + spec + '}'
    : '  \\begin{tabular}{' + align.join('') + '}');
  out.push('    \\hline');
  for (const h of head) out.push('    ' + h.map(cell).join(' & ') + ' \\\\');
  out.push('    \\hline');
  for (const b of body) {
    const padded = b.slice(); while (padded.length < ncol) padded.push('');
    out.push('    ' + padded.map(cell).join(' & ') + ' \\\\');
  }
  out.push('    \\hline');
  out.push(useTabularx ? '  \\end{tabularx}' : '  \\end{tabular}');
  out.push('\\end{table}');
  return out.join('\n');
}

// ------------------------------------------------------------- block parser --

function convertBody(md, opts = {}) {
  const SRC = opts.src || "?";
  const vault = new Vault();
  // Drop HTML comment blocks (DRAFT NOTES) entirely.
  const commentCount = (md.match(/<!--/g) || []).length;
  if (commentCount) note('stripped', `${commentCount} comment block(s) removed (drafting notes)`);
  md = md.replace(/<!--[\s\S]*?-->/g, '');

  // Markdown footnote definitions: pull them out, then splice each one into the
  // \footnote{} at its point of use. A footnote left behind would be silently
  // escaped into "[\textasciicircum{}id]" and its text stranded as a paragraph.
  const footnotes = new Map();
  md = md.replace(/^\[\^([^\]]+)\]:\s*([\s\S]*?)(?=\n\s*\n|\n\[\^|$)/gm, (_, id, text) => {
    footnotes.set(id, text.replace(/\s*\n\s*/g, ' ').trim());
    note('footnote', `definition [^${id}] captured (${text.trim().length} chars)`);
    return '';
  });
  FOOTNOTES = footnotes;

  const lines = md.split(/\r?\n/);
  const out = [];
  let i = 0;
  let pendingCaption = null;

  while (i < lines.length) {
    const line = lines[i];

    // Fenced code block -> verbatim. Must be caught before anything else, or
    // its contents are mangled as inline markup.
    if (/^```/.test(line)) {
      const buf = [];
      i++;
      while (i < lines.length && !/^```/.test(lines[i])) { buf.push(lines[i]); i++; }
      i++; // closing fence
      // pdflatex reads a verbatim body byte by byte, so no escape or macro can
      // rescue a non-ASCII character in here. Fold what can be folded, and fail
      // loudly on the rest rather than emitting a file that will not compile.
      const folded = buf.map(l => l.replace(/[^\x00-\x7F]/g, ch => VERBATIM_ASCII[ch] ?? ch));
      const bad = folded.join('\n').match(/[^\x00-\x7F]/g);
      if (bad) {
        note('verbatim', `NON-ASCII left in a code block: ${[...new Set(bad)].join(' ')} `
          + '(pdflatex cannot set these inside verbatim; rewrite the block in the Markdown)');
      }
      note('verbatim', `code block of ${buf.length} line(s) -> verbatim`);
      out.push('', '\\begin{verbatim}', ...folded, '\\end{verbatim}');
      continue;
    }

    // Blockquote drafting notes -> dropped.
    if (/^>\s?/.test(line)) {
      const buf = [];
      while (i < lines.length && (/^>\s?/.test(lines[i]) || lines[i].trim() === '')) {
        if (/^>\s?/.test(lines[i])) buf.push(lines[i]); else if (buf.length) break;
        i++;
      }
      const text = buf.join(' ');
      if (/drafting note|DRAFTING NOTE/i.test(text)) note('stripped', 'drafting-note blockquote dropped');
      else note('review', 'BLOCKQUOTE DROPPED — check it was not content: ' + text.slice(0, 110));
      continue;
    }

    // Horizontal rule. In the Markdown it separates the drafting-note block
    // from the body; the note is dropped above, so the rule has nothing left to
    // separate. Left in place LaTeX would set it as a literal em dash, which
    // also breaks the no-dash house rule of paper/STYLE.md.
    if (/^\s*(-{3,}|\*{3,}|_{3,})\s*$/.test(line)) {
      note('stripped', 'horizontal rule dropped');
      i++; continue;
    }

    // Headings.
    let h = line.match(/^(#{1,4})\s+(.*)$/);
    if (h) {
      const depth = h[1].length;
      let title = h[2].trim();
      const num = title.match(/^(\d+(?:\.\d+)*)\.?\s+(.*)$/);
      let label = null;
      if (num) { label = 'sec:' + num[1]; title = num[2]; }
      const cmd = depth === 1 ? 'section' : depth === 2 ? 'subsection' : 'subsubsection';
      if (opts.abstract && depth === 1) { i++; continue; }   // abstract heading handled by template
      out.push('');
      out.push('\\' + cmd + '{' + escapeOutsideVault(inline(title, vault)) + '}' +
               (label ? '\\label{' + label + '}' : ''));
      i++; continue;
    }

    // Table caption: a bold paragraph beginning "Table N."
    const cap = line.match(/^\*\*(Table\s+([RS]?\d+)\.?)\s*(.*)$/);
    if (cap) {
      const buf = [line];
      i++;
      while (i < lines.length && lines[i].trim() !== '' && !/^\|/.test(lines[i])) { buf.push(lines[i]); i++; }
      let capText = buf.join(' ').trim();
      capText = capText.replace(/^\*\*/, '').replace(/\*\*/, '');
      // \caption already emits "Table N."; drop the literal prefix from the
      // Markdown so it is not printed twice (and so it is not turned into a
      // self-reference by the cross-reference rule below).
      capText = capText.replace(/^Table\s+[RS]?\d+[.:]?\s*/, '');
      // Only treat this as a caption if a table actually follows. Prose can
      // legitimately open with "**Table 2** (feature dictionary ...) is
      // assembled from Section 3.4." — swallowing that as a caption for a table
      // that never arrives silently deletes a sentence.
      let look = i;
      while (look < lines.length && lines[look].trim() === '') look++;
      if (look < lines.length && /^\|/.test(lines[look])) {
        pendingCaption = { label: 'tab:' + cap[2], text: escapeOutsideVault(inline(capText, vault)) };
        i = look;
      } else {
        note('review', `"${cap[1]}" opens a paragraph but no table follows; emitted as prose`);
        out.push('', escapeOutsideVault(inline(buf.join(' ').trim(), vault)));
      }
      continue;
    }

    // Table.
    if (/^\|/.test(line)) {
      const buf = [];
      while (i < lines.length && /^\|/.test(lines[i])) { buf.push(lines[i]); i++; }
      const c = pendingCaption || { label: null, text: '' };
      if (!pendingCaption) note('review', 'TABLE WITHOUT CAPTION in ' + SRC + ' near md line ' + i);
      const t = convertTable(buf, vault, c.text, c.label);
      if (t) out.push('', t);
      pendingCaption = null;
      continue;
    }

    // Bullet list.
    if (/^\s*[-*]\s+/.test(line)) {
      const buf = [];
      while (i < lines.length && (/^\s*[-*]\s+/.test(lines[i]) || /^\s{2,}\S/.test(lines[i]))) { buf.push(lines[i]); i++; }
      out.push('', '\\begin{itemize}');
      let cur = null;
      for (const b of buf) {
        const m = b.match(/^\s*[-*]\s+(.*)$/);
        if (m) { if (cur !== null) out.push('  \\item ' + cur); cur = m[1]; }
        else cur += ' ' + b.trim();
      }
      if (cur !== null) out.push('  \\item ' + cur);
      out.push('\\end{itemize}');
      out[out.length - 2] = out[out.length - 2]; // no-op, keeps shape explicit
      // escape items
      for (let k = out.length - 2; k >= 0 && out[k] !== '\\begin{itemize}'; k--) {
        if (out[k].startsWith('  \\item ')) out[k] = '  \\item ' + escapeOutsideVault(inline(out[k].slice(8), vault));
      }
      continue;
    }

    // Numbered list.
    if (/^\s*\d+\.\s+/.test(line)) {
      const buf = [];
      while (i < lines.length && (/^\s*\d+\.\s+/.test(lines[i]) || /^\s{2,}\S/.test(lines[i]))) { buf.push(lines[i]); i++; }
      out.push('', '\\begin{enumerate}');
      let cur = null;
      for (const b of buf) {
        const m = b.match(/^\s*\d+\.\s+(.*)$/);
        if (m) { if (cur !== null) out.push('  \\item ' + escapeOutsideVault(inline(cur, vault))); cur = m[1]; }
        else cur += ' ' + b.trim();
      }
      if (cur !== null) out.push('  \\item ' + escapeOutsideVault(inline(cur, vault)));
      out.push('\\end{enumerate}');
      continue;
    }

    // Blank line.
    if (line.trim() === '') { out.push(''); i++; continue; }

    // Paragraph.
    const buf = [];
    while (i < lines.length && lines[i].trim() !== '' && !/^[#|>]/.test(lines[i]) &&
           !/^\s*[-*]\s+/.test(lines[i]) && !/^\s*\d+\.\s+/.test(lines[i])) { buf.push(lines[i]); i++; }
    out.push(escapeOutsideVault(inline(buf.join(' ').trim(), vault)));
  }

  return vault.restore(out.join('\n')).replace(/\n{3,}/g, '\n\n');
}

// ---------------------------------------------------------------- assembly --

const read = f => fs.readFileSync(path.join(ROOT, f), 'utf8');

const abstractMd = read('00_abstract.md');
const sections = ['01_introduction', '02_related_work', '03_methods',
                  '04_results', '05_discussion', '06_conclusions'];

collectTableLabels([...sections, 'S1_few_shot_recovery']);

const abstractTex = convertBody(abstractMd, { abstract: true }).trim();
const bodyTex = sections.map(f => convertBody(read(f + '.md'), { src: f })).join('\n\n');

// Highlights (Elsevier wants them as a separate item, but keep them in the file).
const highlights = read('highlights.md').split(/\r?\n/)
  .filter(l => /^\s*[-*]\s+/.test(l))
  .map(l => '  \\item ' + l.replace(/^\s*[-*]\s+/, '').trim());

const figureCaptions = read('figure_captions.tex');

const preamble = `% =============================================================================
% manuscript.tex — Ecological Informatics (Elsevier), elsarticle class
%
% GENERATED FILE. Do not edit by hand: it is produced from the Markdown sources
% by paper/tex/build_tex.mjs. Edit the Markdown and re-run the script, or the
% next build will silently discard your changes.
%
% Build:  pdflatex manuscript && bibtex manuscript && pdflatex manuscript x2
% Needs:  elsarticle.cls and elsarticle-harv.bst (TeX Live / MiKTeX / Overleaf)
%
% COMPILED. First compiled 2026-08-14 with MiKTeX 25.12 (pdfTeX), clean: no
% errors, no undefined references, no undefined citations. The first compile was
% a debugging pass and found four real defects, all fixed in this generator: a
% true minus inside a code span (the Unicode table was applied to prose but not
% to code spans), non-ASCII inside a verbatim block, figure paths resolved from
% the wrong directory, and l-columns that cannot wrap, which ran the widest
% table 763pt past the margin. See build_report.md.
% =============================================================================
\\documentclass[preprint,review,12pt]{elsarticle}

\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{lmodern}
\\usepackage{textcomp}
\\usepackage{tabularx}
\\graphicspath{{../}{../figures/}{./}{./figures/}}
\\usepackage{graphicx}
\\usepackage{amsmath}
\\usepackage{booktabs}
\\usepackage{longtable}
\\usepackage{array}
\\usepackage{url}
\\usepackage{lineno}
\\modulolinenumbers[5]

\\journal{Ecological Informatics}

\\begin{document}

\\begin{frontmatter}

%% Title. POSITIONING.md lists three candidates and directs that under Branch A
%% (Evia enlarged and re-run cleanly, which is what happened) the third is used.
%% Referee round 2, 2026-08-14: that third candidate began "Marginal diagnostics
%% miss conditional failures", which asserts more than Section 5.4 concedes. On
%% ten effective pairs the null diagnostics are "not shown to order transfer",
%% not "shown not to". The title now says what Section 4.4 found and what
%% Section 5.4 defends. Candidate 1 was not used because "do not transfer
%% between them" is contradicted by the paper's own matrix, and candidate 2 was
%% not used because "transferability cost" asserts a debit measured only by the
%% feature-removal ablation. Change here if that decision is revisited.
%% Retitled 2026-08-14 in the split, to carry the three findings the paper was
%% cut to. "Sign reversal" names the mechanism, which the old title left out;
%% "do not order" is kept verbatim because it is the only claim Section 5.4
%% defends, the diagnostics having been shown not to order transfer here rather
%% than shown incapable of ordering it anywhere.
\\title{Local skill, unstable portability: sign reversal in pre-fire thermal
predictors across Mediterranean wildfire regions, and the diagnostics that do
not order it}

%% Author block. Affiliation and corresponding address supplied by the authors
%% 2026-08-14. Still optional and not supplied: department or faculty within the
%% university, and ORCIDs.
\\author[inst1]{Yunus Emre Cogurcu\\corref{cor1}}
\\ead{ycogurcu@cu.edu.tr}
\\author[inst1]{Emrehan Metin}
\\cortext[cor1]{Corresponding author.}
\\affiliation[inst1]{organization={\\c{C}ukurova University},
                    city={Adana},
                    country={T\\"urkiye}}

\\begin{abstract}
${abstractTex}
\\end{abstract}

\\begin{highlights}
${highlights.join('\n')}
\\end{highlights}

\\begin{keyword}
wildfire \\sep model transferability \\sep area of applicability \\sep
land surface temperature \\sep domain adaptation \\sep concept shift
\\end{keyword}

\\end{frontmatter}

\\linenumbers
`;

const postamble = `

% ------------------------------------------------------------ declarations --
% Elsevier requires all four of these at submission. The two marked NEEDS
% AUTHOR INPUT cannot be written from the repository and must be completed
% before the manuscript is uploaded.

\\section*{CRediT authorship contribution statement}

\\textbf{Yunus Emre Cogurcu:} Conceptualization, Methodology, Formal analysis,
Investigation, Writing -- original draft, Writing -- review and editing,
Supervision. \\textbf{Emrehan Metin:} Software, Data curation, Investigation,
Validation, Writing -- review and editing.
% NEEDS AUTHOR INPUT: confirm this split with the co-author before submission.

\\section*{Declaration of competing interest}

The authors declare that they have no known competing financial interests or
personal relationships that could have appeared to influence the work reported
in this paper.

\\section*{Funding}

This work is an output of project 17506, supported by the Scientific Research
Projects (BAP) unit of \\c{C}ukurova University.
%% Provisional wording, 2026-08-14. Confirm before submission: the project's
%% full title, the correct rendering of the unit's name in English, and whether
%% the funder requires a specific acknowledgement sentence.

\\section*{Data availability}

All satellite inputs are public and are obtained through Google Earth Engine.
The processing pipeline, its configuration and the frozen numeric outputs are
publicly available; the repository, the commit of record and the licence are
given in the data and code availability statement of the Methods, together with
the three components that fall outside that release. No digital object
identifier is minted and no archival deposit exists.

% ---------------------------------------------------------------- figures --
% Captions are maintained in ../figure_captions.tex and included verbatim.
${figureCaptions}

\\bibliographystyle{elsarticle-harv}
\\bibliography{../REFERENCES}

\\end{document}
`;

fs.writeFileSync(path.join(OUT, 'manuscript.tex'), preamble + bodyTex + postamble, 'utf8');

// Supplementary.
const supTex = convertBody(read('S1_few_shot_recovery.md'), { src: 'S1_few_shot_recovery' });
fs.writeFileSync(path.join(OUT, 'supplementary.tex'), `% GENERATED by paper/tex/build_tex.mjs — do not edit by hand.
\\documentclass[preprint,12pt]{elsarticle}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{lmodern}
\\usepackage{textcomp}
\\usepackage{tabularx}
\\graphicspath{{../}{../figures/}{./}{./figures/}}
\\usepackage{graphicx}\\usepackage{amsmath}\\usepackage{booktabs}\\usepackage{array}
\\renewcommand{\\thetable}{S\\arabic{table}}
\\renewcommand{\\thefigure}{S\\arabic{figure}}
\\begin{document}
\\section*{Supplementary material}
${supTex}
\\bibliographystyle{elsarticle-harv}
\\bibliography{../REFERENCES}
\\end{document}
`, 'utf8');

// Report.
const byCat = {};
for (const r of report) (byCat[r.cat] ||= []).push(r.msg);
let rep = '# LaTeX build report\n\nGenerated by `paper/tex/build_tex.mjs`. Every judgement the\nconverter made is listed so it can be reviewed.\n\n';
for (const cat of Object.keys(byCat).sort()) {
  rep += `## ${cat} (${byCat[cat].length})\n\n`;
  const seen = new Map();
  for (const m of byCat[cat]) seen.set(m, (seen.get(m) || 0) + 1);
  for (const [m, n] of seen) rep += `- ${m}${n > 1 ? ` _(x${n})_` : ''}\n`;
  rep += '\n';
}
fs.writeFileSync(path.join(OUT, 'build_report.md'), rep, 'utf8');

console.log('wrote manuscript.tex, supplementary.tex, build_report.md');
console.log('report categories:', Object.entries(byCat).map(([k, v]) => `${k}=${v.length}`).join(' '));

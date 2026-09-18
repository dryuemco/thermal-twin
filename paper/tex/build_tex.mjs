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

// PAPER_ROOT lets the companion manuscript reuse this converter unchanged. When
// it is absent the root is 'paper', so Paper 1's output is byte-identical to
// what it was before this was parameterised, which was verified by diff.
const ROOT = path.resolve(process.env.PAPER_ROOT || 'paper');
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
// A manuscript with no figures yet simply has no captions file; that is not an
// error, it just means no "Fig. N" reference can resolve.
const CAPTIONS = path.join(ROOT, 'figure_captions.tex');
const FIGLABELS = !fs.existsSync(CAPTIONS) ? []
  : [...fs.readFileSync(CAPTIONS, 'utf8')
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
  // Vaulted items can hold vault tokens of their own: a footnote is vaulted
  // whole, and the citations inside it were vaulted first. One pass leaves the
  // inner tokens unsubstituted, because they enter the string only after the
  // scan has passed that point, and they reach the .tex as raw NUL bytes.
  // Repeat until the string stops changing; the bound is a guard, not a limit
  // any real document approaches.
  restore(s) {
    for (let pass = 0; pass < 8; pass++) {
      const next = s.replace(/\u0000(\d+)\u0000/g, (_, i) => this.items[+i]);
      if (next === s) return s;
      s = next;
    }
    note('review', 'VAULT TOKENS LEFT UNRESOLVED AFTER 8 PASSES');
    return s;
  }
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

  // 4b. Straight double quotes render as right-hand quotes at both ends, so an
  //     opening quote comes out backwards. Convert balanced pairs to the LaTeX
  //     forms. Code spans and anything else already vaulted are untouched,
  //     since the vault token carries no quote characters.
  s = s.replace(/"([^"]*)"/g, (_, inner) => '``' + inner + "''");

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
  // Overridable per manuscript: the companion paper has a seven-column table
  // whose 19-character verdict column falls just under this and then ran 27pt
  // past the margin, an l column being unable to wrap however small the type.
  const WRAP_AT = FM.wrapAt || 20;
  const rawWidth = widest.reduce((a, b) => a + b, 0) + 2.5 * ncol;
  const wrapping = widest.map(w => w > WRAP_AT);
  let useTabularx = wrapping.some(Boolean);
  // Font step chosen from the width that remains after wrapping is accounted
  // for; a wrapped column no longer contributes its full natural width.
  const effWidth = widest.reduce((a, w, i) => a + (wrapping[i] ? Math.min(w, WRAP_AT) : w), 0)
    + 2.5 * ncol;
  const size = effWidth <= LINE_CHARS ? '\\small'
    : effWidth <= LINE_CHARS * 1.25 ? '\\footnotesize'
    : '\\scriptsize';

  // tabularx gives the X columns whatever is left after the fixed columns take
  // their natural width. Nothing here checked that anything WAS left. A table
  // with one prose column and five long numeric headers left the X column at
  // about zero: every word in it broke one character per line and the first two
  // headers printed on top of each other. When the X columns would be starved,
  // set the table as a plain tabular instead and let the resizebox below shrink
  // it as a whole - uniformly smaller reads far better than one crushed column.
  const MIN_X_CHARS = 12;
  const capacity = LINE_CHARS * (size === '\\small' ? 1 : size === '\\footnotesize' ? 1.1 : 1.25);
  const fixedWidth = widest.reduce((a, w, i) => a + (wrapping[i] ? 0 : w), 0) + 2.5 * ncol;
  const nX = wrapping.filter(Boolean).length;
  if (useTabularx) {
    const perX = (capacity - fixedWidth) / nX;
    if (perX < MIN_X_CHARS) {
      note('table', `${caption.slice(0, 44)}: X columns would get ${Math.round(perX)} chars each `
        + `(min ${MIN_X_CHARS}) - set as plain tabular and scaled to fit instead`);
      useTabularx = false;
    }
  }
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
  // A table with no caption must NOT be a float. \caption{} still steps the
  // table counter, so an uncaptioned float silently consumes a number and every
  // later table is numbered one higher in the PDF than in the source. These are
  // inline display tables (the increment ladder, the resampling-unit list, the
  // sensitivity arms); set them centred and unnumbered instead.
  const floating = Boolean(caption && caption.trim());
  if (!floating) {
    note('table', 'no caption; emitted unnumbered so it does not consume a table number');
    out.push('\\begin{center}');
    out.push('  ' + size);
  } else {
    out.push('\\begin{table}[htbp]');
    out.push('  \\centering');
    out.push('  ' + size);
    out.push('  \\caption{' + caption + '}');
    if (label) out.push('  \\label{' + label + '}');
  }
  // A tabularx is bounded by \linewidth already. A plain tabular is as wide as
  // its content, and the size chosen above comes from a character-count estimate
  // that is sometimes optimistic: a six-column table ran about 33 mm past the
  // right margin at \scriptsize. Wrap it so it shrinks only when it would
  // otherwise overflow; a table that already fits is left at its natural size
  // and its font matches the rest of the page.
  if (!useTabularx) {
    out.push('  \\resizebox{\\ifdim\\width>\\linewidth\\linewidth\\else\\width\\fi}{!}{%');
  }
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
  out.push(useTabularx ? '  \\end{tabularx}' : '  \\end{tabular}}');
  out.push(floating ? '\\end{table}' : '\\end{center}');
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
  // The end anchor must mean end of FILE, not end of line. Under /m a bare $
  // matched the first line break, so a footnote written across several lines was
  // captured only as far as its first line: the rest stayed in the Markdown and
  // was typeset as a stray paragraph with no subject, and the footnote itself
  // ended mid-sentence. $(?![\s\S]) is end-of-input even with /m set.
  md = md.replace(/^\[\^([^\]]+)\]:\s*([\s\S]*?)(?=\n\s*\n|\n\[\^|$(?![\s\S]))/gm, (_, id, text) => {
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
// Optional parts. Paper 1 has all of them; the companion manuscript has no
// figures, highlights or supplement yet, and their absence is not an error.
const has = f => fs.existsSync(path.join(ROOT, f));
const readOpt = (f, fallback = '') => (has(f) ? read(f) : fallback);

// Per-manuscript front matter. Absent, the values below are Paper 1's, so its
// output does not change.
const FM = has('frontmatter.json') ? JSON.parse(read('frontmatter.json')) : {};
const TITLE = FM.title || `Local skill, unstable portability: sign reversal in pre-fire thermal
predictors across Mediterranean wildfire regions, and the diagnostics that do
not order it`;
const JOURNAL = FM.journal || 'Ecological Informatics';

// The three blocks below differ between the two manuscripts and would be a
// false statement if one paper's version were emitted under the other's title.
// The defaults are Paper 1's exact wording, so its output is unchanged; the
// companion supplies its own in frontmatter.json.
const KEYWORDS = FM.keywords
  ? FM.keywords.join(' \\sep ')
  : `wildfire \\sep model transferability \\sep area of applicability \\sep
land surface temperature \\sep domain adaptation \\sep concept shift`;
const CREDIT = FM.credit ||
`\\textbf{Emrehan Metin:} Software, Data curation, Investigation, Validation,
Writing -- review and editing. \\textbf{Yunus Emre Cogurcu:} Conceptualization,
Methodology, Formal analysis, Investigation, Writing -- original draft,
Writing -- review and editing, Supervision.`;
const abstractMd = read('00_abstract.md');
// Appendices are ordinary sections to the converter; LaTeX is told where the
// body ends by the \appendix marker inserted between the two groups below.
const BODY = ['01_introduction', '02_related_work', '03_methods',
              '04_results', '05_discussion', '06_conclusions'];
// A1_sensitivity is no longer printed. Appendix A and the protocol half of
// Appendix C are released as paper/supplementary_appendices.md, under the same
// section names, so every "Appendix A(x)" and "Appendix C.2" pointer in the
// paper still resolves - it resolves in that document instead of overleaf. What
// stays here is the evidence a reader checks the claims against: Appendix B's
// tables and Appendix C.5's eleven limitations.
const APPENDICES = ['A2_diagnostics', 'A3_protocol']
  .filter(f => has(f + '.md'));
const sections = [...BODY, ...APPENDICES];

collectTableLabels([...sections, ...(has('S1_few_shot_recovery.md') ? ['S1_few_shot_recovery'] : [])]);

const figureCaptions = readOpt('figure_captions.tex', '');

// Figures are placed where they are first referenced, not dumped at the end of
// the file. Before this they all sat after \appendix, so the counter numbered
// them C.1 to C.8 and a reader met "Fig. 1" on page 132. Split the caption file
// into its figure environments, keyed by label.
const FIGBLOCKS = (() => {
  const out = new Map();
  const re = /\\begin\{figure\}[\s\S]*?\\end\{figure\}/g;
  let m;
  while ((m = re.exec(figureCaptions)) !== null) {
    const lab = /\\label\{(fig:[^}]*)\}/.exec(m[0]);
    if (lab) out.set(lab[1], m[0]);
  }
  return out;
})();

// Insert each not-yet-placed figure after the paragraph that first references
// it. Text carrying no reference to a given figure comes back unchanged, so a
// later group gets its turn; whatever is still unplaced the caller reports.
function placeFigures(tex, placed) {
  for (const [lab, block] of FIGBLOCKS) {
    if (placed.has(lab)) continue;
    const at = tex.indexOf('\\ref{' + lab + '}');
    if (at < 0) continue;
    let end = tex.indexOf('\n\n', at);
    if (end < 0) end = tex.length;
    tex = tex.slice(0, end) + '\n\n' + block + tex.slice(end);
    placed.add(lab);
  }
  return tex;
}

const abstractTex = convertBody(abstractMd, { abstract: true }).trim();
const placedFigures = new Set();
const bodyTex = [
  ...BODY.map(f => placeFigures(convertBody(read(f + '.md'), { src: f }), placedFigures)),
  // \appendix relabels sections A, B, C and elsarticle already prints figures
  // as \thesection.\arabic{figure}. It does not reset the counter, so the first
  // appendix figure came out as A.3, carrying on from the body. Reset it here
  // and make it reset again at every appendix section, so each appendix numbers
  // its own figures from 1.
  ...(APPENDICES.length ? ['\\appendix\n\\setcounter{figure}{0}\n' +
      '\\makeatletter\\@addtoreset{figure}{section}\\makeatother'] : []),
  ...APPENDICES.map(f => placeFigures(convertBody(read(f + '.md'), { src: f }), placedFigures)),
].join('\n\n');
for (const lab of FIGBLOCKS.keys()) {
  if (!placedFigures.has(lab)) {
    note('review', 'FIGURE ' + lab + ' HAS A CAPTION BUT IS REFERENCED NOWHERE - not placed');
  }
}

// Highlights (Elsevier wants them as a separate item, but keep them in the file).
const highlights = readOpt('highlights.md', '').split(/\r?\n/)
  .filter(l => /^\s*[-*]\s+/.test(l))
  .map(l => '  \\item ' + l.replace(/^\s*[-*]\s+/, '').trim());

const preamble = `% =============================================================================
% manuscript.tex — Environmental Modelling & Software (Elsevier), elsarticle class
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
\%% authoryear is required by elsarticle-harv. Without it \citep printed a
%% bracketed number while the reference list stayed alphabetical author-year,
%% so the in-text numbers ran 29, 42, 14 with nothing to match them against.
\\documentclass[preprint,review,authoryear,12pt]{elsarticle}

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
%% The review option double-spaces everything, captions included. A 267-word
%% caption then stands 160 mm tall, which together with the figure exceeds the
%% 193 mm text block, and the folio prints through the caption text. LaTeX
%% reports no overfull box for it, because the float is allowed to be tall.
%% Captions are set at normal leading, as journals set them.
%% Long 	exttt file names are broken at llowbreak points, but TeX was still
%% choosing lines that ran up to 10 mm past the right margin rather than
%% stretching the spaces, and was not reporting them as overfull. emergencystretch
%% gives it a third pass in which a loose line is preferred to a protruding one.
\\emergencystretch=3em
\\usepackage{setspace}
\\usepackage{etoolbox}
\\AtBeginEnvironment{figure}{\\singlespacing}
\\AtBeginEnvironment{table}{\\singlespacing}
\\usepackage{lineno}
\\modulolinenumbers[5]

\\journal{${JOURNAL}}

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
\\title{${TITLE}}

%% Author block. Affiliation and corresponding address supplied by the authors
%% 2026-08-14. Order changed 2026-08-15 on the authors' instruction: Emrehan
%% Metin first, Yunus Emre Cogurcu second. Corresponding authorship was NOT
%% moved with it and stays with Cogurcu, who supervises the work and whose
%% address is the one on file; say so if that is not intended.
%% Still optional and not supplied: department or faculty within the
%% university, and ORCIDs.
\\author[inst1]{Emrehan Metin}
\\author[inst1]{Yunus Emre Cogurcu\\corref{cor1}}
\\ead{ycogurcu@cu.edu.tr}
\\cortext[cor1]{Corresponding author.}
\\affiliation[inst1]{organization={\\c{C}ukurova University},
                    city={Adana},
                    country={T\\"urkiye}}

\\begin{abstract}
${abstractTex}
\\end{abstract}

${highlights.length ? `\\begin{highlights}
${highlights.join('\n')}
\\end{highlights}` : '%% No highlights file yet.'}

\\begin{keyword}
${KEYWORDS}
\\end{keyword}

\\end{frontmatter}

\\linenumbers
`;

const postamble = `

% ------------------------------------------------------------ declarations --
% One consolidated block, matching the authors' house format. Everything here is
% written from the repository except the item marked NEEDS AUTHOR INPUT, which
% must be settled before the manuscript is uploaded.

\\section*{Software and data availability}

\\textbf{Analysis code and frozen outputs.} Name: \\texttt{thermal-twin}. Developers:
Y.~E.~Cogurcu and E.~Metin; contact: ycogurcu@cu.edu.tr. First available: 2026.
Hardware: a standard desktop computer. Software required: Python 3.12 with NumPy
2.4.4, pandas 3.0.2 and scikit-learn 1.9.0, the versions every reported number was
produced with; scikit-learn in particular carries a cross-region tolerance of about
$\\pm$0.02 to 0.03 between versions (Appendix C.5(vi)). Program language: Python. Size:
about 21 MB. Availability: \\url{https://github.com/dryuemco/thermal-twin}, which holds
the scripts that regenerate each reported artefact, the frozen numeric outputs behind
every table and figure, and the supplementary appendices (Appendix A and protocol
sections C.1 to C.4, C.6 and C.7, at \\texttt{paper/supplementary\\_appendices.md}).
Cost: free.
% NEEDS AUTHOR INPUT: this repository is PRIVATE and has no licence (checked
% 2026-09-19). EMS requires software essential to the paper to be available to
% reviewers; it accepts a password-protected download whose password is given to
% the editors. Either make a cleaned copy public with a licence, or provide such a
% download, before submission.

\\textbf{Upstream processing pipeline.} Name: \\texttt{satellite-\\allowbreak{}thermal-\\allowbreak{}digital-\\allowbreak{}twin}.
Developer: E.~Metin. First available: 2026. Hardware: a standard desktop computer;
the satellite exports run on Google Earth Engine and need an Earth Engine account.
Program language: Python. Size: about 20 MB. Availability:
\\url{https://github.com/emrehann17/satellite-thermal-digital-twin}, MIT licence; the
commit of record for every number reported here is \\texttt{6381f4c}. Three
components once outside the release are now inside it: the reproduction-check
driver and its validation package, on which Section~\\ref{sec:3.14} rests; the
few-shot run, reachable through the tag \\texttt{few-shot-run-19d825b}; and the
ERA5-Land diagnostic, whose manifest records commit \\texttt{a07ea33}. Cost: free.

\\textbf{Data.} All satellite inputs are public and were retrieved through Google
Earth Engine: burned-area labels from MODIS MCD64A1 Collection 6.1, land cover from
ESA WorldCover, and the thermal, optical and terrain inputs described in
Section~\\ref{sec:3.4}; no proprietary or restricted data were used. The modelling
dataset each number rests on is identified in the pipeline by SHA-256, which is how
the one provenance incident in this project was settled: a rebuild had replaced one
region's file at its canonical path, and the recorded hash identifies the frozen
original unambiguously. No digital object identifier is minted and no archival
deposit exists.

\\section*{Declarations}

\\textbf{Funding.} This work was supported by the \\c{C}ukurova University Scientific
Research Projects Coordination Unit (Bilimsel Ara\\c{s}t{\\i}rma Projeleri Koordinasyon
Birimi) under the Career Starter Project (Kariyer Ba\\c{s}lang{\\i}\\c{c} Projesi) scheme,
project code \\texttt{FKB-2025-17608} (\`\`Termal Dijital \\.Ikiz Tabanl{\\i} S\\"ur\\"u \\.IHA
Sistemi ile Orman Yang{\\i}nlar{\\i}n{\\i}n Erken Tespiti ve \\"Onlenmesi'').

\\textbf{Acknowledgments.} The authors gratefully acknowledge the \\c{C}ukurova
University Scientific Research Projects Coordination Unit for financial support of
this research, and the Department of Computer Engineering at \\c{C}ukurova University
for providing the laboratory environment and institutional support that made this
work possible.

\\textbf{Competing interests.} The authors declare no competing interests.

\\textbf{Ethics approval.} Not applicable. This study involved no human participants,
animal subjects, or personally identifiable data.

\\textbf{Author contributions.} Stated in CRediT terms. ${CREDIT}
% NEEDS AUTHOR INPUT: confirm the contribution split with the co-author, and
% confirm the Software and data availability items above before the manuscript
% is uploaded.

\\section*{Declaration of generative AI and AI-assisted technologies in the manuscript preparation process}

During the preparation of this work the authors used Claude (Anthropic) in order to
write and run analysis and verification code against the frozen pipeline outputs,
cross-check reported numbers against those outputs, and draft and edit manuscript
text. After using this tool, the authors reviewed and edited the content as needed
and take full responsibility for the content of the publication.
% NEEDS AUTHOR INPUT: Elsevier's policy (updated June 2026) places this section
% immediately before the references and asks that AI use in the research process
% also be described in Methods. Confirm the scope stated above with both authors.

% ---------------------------------------------------------------- figures --
% Figures are placed at their first reference, in the body and in the
% appendices; captions are maintained in ../figure_captions.tex.

\\bibliographystyle{elsarticle-harv}
\\bibliography{../REFERENCES}

\\end{document}
`;

fs.writeFileSync(path.join(OUT, 'manuscript.tex'), preamble + bodyTex + postamble, 'utf8');

// Supplementary. Only Paper 1 has one; the companion manuscript has no S-file,
// and a missing supplement is not an error.
const HAS_SUP = has('S1_few_shot_recovery.md');
if (HAS_SUP) {
const supTex = convertBody(read('S1_few_shot_recovery.md'), { src: 'S1_few_shot_recovery' });
fs.writeFileSync(path.join(OUT, 'supplementary.tex'), `% GENERATED by paper/tex/build_tex.mjs — do not edit by hand.
%% The supplement carries its own preamble. It needs the same three settings
%% the manuscript needs, for the same reasons: authoryear so \citep matches
%% elsarticle-harv rather than printing bracketed numbers against an
%% author-year list; emergencystretch so a long 	exttt path is set loose
%% rather than protruding; single-spaced float captions so a long caption
%% does not push the folio into its own text.
\\documentclass[preprint,authoryear,12pt]{elsarticle}
\\usepackage[utf8]{inputenc}
\\usepackage[T1]{fontenc}
\\usepackage{lmodern}
\\usepackage{textcomp}
\\usepackage{tabularx}
\\graphicspath{{../}{../figures/}{./}{./figures/}}
\\usepackage{graphicx}\\usepackage{amsmath}\\usepackage{booktabs}\\usepackage{array}
\\usepackage{setspace}
\\usepackage{etoolbox}
\\AtBeginEnvironment{figure}{\\singlespacing}
\\AtBeginEnvironment{table}{\\singlespacing}
\\emergencystretch=3em
\\renewcommand{\\thetable}{S\\arabic{table}}
\\renewcommand{\\thefigure}{S\\arabic{figure}}
\\begin{document}
\\section*{Supplementary material}
${supTex}
\\bibliographystyle{elsarticle-harv}
\\bibliography{../REFERENCES}
\\end{document}
`, 'utf8');
}

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

console.log('wrote manuscript.tex, '
  + (HAS_SUP ? 'supplementary.tex, ' : '') + 'build_report.md');
console.log('report categories:', Object.entries(byCat).map(([k, v]) => `${k}=${v.length}`).join(' '));

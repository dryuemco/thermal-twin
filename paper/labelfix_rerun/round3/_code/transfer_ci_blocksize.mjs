import { readFileSync, writeFileSync } from 'fs'

const ROOT = process.env.R3ROOT + '/drive_new/cross_region' // ROUND3: was 'C:/Users/CORSAIR/projects/thermal-twin/drive_new/cross_region'
const POP = 'burnable_tree_shrub_grass'
const NBOOT = 1000
const SEED = Number(process.env.BSEED || 42)

const PAIRDIR = {
  'manavgat_2021|bejis_2022': 'manavgat_2021__bejis_2022',
  'manavgat_2021|mugla_2021': 'manavgat_2021__mugla_2021',
  'manavgat_2021|evia_2021_extended': 'manavgat_2021__evia_2021_extended',
  'manavgat_2021|montiferru_2021': 'montiferru_2021__manavgat_2021',
  'bejis_2022|mugla_2021': 'bejis_2022__mugla_2021',
  'bejis_2022|evia_2021_extended': 'bejis_2022__evia_2021_extended',
  'bejis_2022|montiferru_2021': 'montiferru_2021__bejis_2022',
  'mugla_2021|evia_2021_extended': 'mugla_2021__evia_2021_extended',
  'mugla_2021|montiferru_2021': 'montiferru_2021__mugla_2021',
  'evia_2021_extended|montiferru_2021': 'montiferru_2021__evia_2021_extended',
}
const LABEL = { manavgat_2021: 'Manavgat', bejis_2022: 'Bejis', mugla_2021: 'Mugla',
                evia_2021_extended: 'Evia', montiferru_2021: 'Montiferru' }

const DIRECTIONS = [
  ['manavgat_2021', 'bejis_2022'], ['bejis_2022', 'manavgat_2021'],
  ['manavgat_2021', 'mugla_2021'], ['mugla_2021', 'manavgat_2021'],
  ['manavgat_2021', 'evia_2021_extended'], ['evia_2021_extended', 'manavgat_2021'],
  ['bejis_2022', 'mugla_2021'], ['mugla_2021', 'bejis_2022'],
  ['bejis_2022', 'evia_2021_extended'], ['evia_2021_extended', 'bejis_2022'],
  ['mugla_2021', 'evia_2021_extended'], ['evia_2021_extended', 'mugla_2021'],
  ['montiferru_2021', 'manavgat_2021'], ['manavgat_2021', 'montiferru_2021'],
  ['montiferru_2021', 'bejis_2022'], ['bejis_2022', 'montiferru_2021'],
  ['montiferru_2021', 'mugla_2021'], ['mugla_2021', 'montiferru_2021'],
  ['montiferru_2021', 'evia_2021_extended'], ['evia_2021_extended', 'montiferru_2021'],
]

function mulberry32(a) {
  return function () {
    a |= 0; a = a + 0x6D2B79F5 | 0
    let t = Math.imul(a ^ a >>> 15, 1 | a)
    t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t
    return ((t ^ t >>> 14) >>> 0) / 4294967296
  }
}

function percentileLinear(sorted, p) {
  const n = sorted.length
  if (n === 0) return NaN
  const idx = (p / 100) * (n - 1)
  const lo = Math.floor(idx), hi = Math.ceil(idx)
  if (lo === hi) return sorted[lo]
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (idx - lo)
}

const csvCache = new Map()
function loadDirection(dir, direction) {
  const path = ROOT + '/' + dir + '/step9b/cross_region_transfer_predictions.csv'
  let txt = csvCache.get(path)
  if (txt === undefined) { txt = readFileSync(path, 'utf8'); csvCache.set(path, txt) }
  const lines = txt.split('\n')
  const head = lines[0].replace(/\r$/, '').split(',')
  const iDir = head.indexOf('transfer_direction'), iPop = head.indexOf('population')
  const iCell = head.indexOf('target_cell_id'), iBlk = head.indexOf('target_spatial_block_id')
  const iY = head.indexOf('burned'), iTh = head.indexOf('thermal_probability')
  const iBa = head.indexOf('baseline_probability')
  if ([iDir, iPop, iCell, iBlk, iY, iTh, iBa].some(x => x < 0)) throw new Error('missing column in ' + path)
  const y = [], prob = [], probBase = [], blk2 = [], blk10 = []
  for (let k = 1; k < lines.length; k++) {
    const ln = lines[k]
    if (!ln) continue
    const f = ln.replace(/\r$/, '').split(',')
    if (f[iDir] !== direction || f[iPop] !== POP) continue
    const cell = f[iCell]
    const m = /^r(-?\d+)_c(-?\d+)$/.exec(cell)
    if (!m) throw new Error('unparsable cell id ' + cell)
    const r = parseInt(m[1], 10), c = parseInt(m[2], 10)
    if (f[iBlk] !== (Math.floor(r / 2) + '_' + Math.floor(c / 2)))
      throw new Error('block id mismatch ' + cell + ' ' + f[iBlk])
    y.push(f[iY] === '1' ? 1 : 0)
    prob.push(parseFloat(f[iTh]))
    probBase.push(parseFloat(f[iBa]))
    blk2.push(f[iBlk])
    blk10.push(Math.floor(r / 10) + '_' + Math.floor(c / 10))
  }
  return { y, prob, probBase, blk2, blk10, path }
}

function prepare(prob) {
  const n = prob.length
  const order = Array.from({ length: n }, (_, i) => i).sort((a, b) => prob[a] - prob[b])
  const groups = []
  let i = 0
  while (i < n) {
    let j = i
    while (j < n && prob[order[j]] === prob[order[i]]) j++
    groups.push([i, j])
    i = j
  }
  return { order: Int32Array.from(order), groups }
}

function aucWithCounts(order, groups, y, counts) {
  let cumNeg = 0, num = 0, totP = 0, totN = 0
  for (let g = 0; g < groups.length; g++) {
    const a = groups[g][0], b = groups[g][1]
    let gP = 0, gN = 0
    for (let k = a; k < b; k++) {
      const idx = order[k], c = counts[idx]
      if (c === 0) continue
      if (y[idx]) gP += c; else gN += c
    }
    if (gP) num += gP * cumNeg + 0.5 * gP * gN
    cumNeg += gN
    totP += gP; totN += gN
  }
  if (totP === 0 || totN === 0) return null
  return num / (totP * totN)
}

function summarise(vals) {
  const s = vals.slice().sort((p, q) => p - q)
  return { lo: percentileLinear(s, 2.5), hi: percentileLinear(s, 97.5),
           mean: s.reduce((a, v) => a + v, 0) / s.length }
}

// One pass over the replicates. The thermal level and the paired delta are read off the
// SAME resampled blocks, which is what Methods 3.9 specifies for the delta. The RNG is
// consumed exactly as in the level-only version, so the level numbers are unchanged.
function bootstrap(y, blocks, sTherm, sBase, rng) {
  const n = y.length
  const blockIds = [], blockOf = new Map()
  for (const b of blocks) if (!blockOf.has(b)) { blockOf.set(b, blockIds.length); blockIds.push(b) }
  const members = blockIds.map(() => [])
  for (let i = 0; i < n; i++) members[blockOf.get(blocks[i])].push(i)
  const nb = blockIds.length
  const counts = new Int32Array(n)
  const vTherm = [], vBase = [], vDelta = []
  let nInvalid = 0
  for (let rep = 0; rep < NBOOT; rep++) {
    counts.fill(0)
    for (let s = 0; s < nb; s++) {
      const mem = members[Math.floor(rng() * nb)]
      for (let t = 0; t < mem.length; t++) counts[mem[t]]++
    }
    const at = aucWithCounts(sTherm.order, sTherm.groups, y, counts)
    if (at === null) { nInvalid++; continue }
    const ab = aucWithCounts(sBase.order, sBase.groups, y, counts)
    vTherm.push(at); vBase.push(ab); vDelta.push(at - ab)
  }
  return { thermal: summarise(vTherm), baseline: summarise(vBase), delta: summarise(vDelta),
           nValid: vTherm.length, nInvalid, nBlocks: nb }
}

function verdict(lo, hi) { if (lo > 0.5) return 'above'; if (hi < 0.5) return 'below'; return 'uncertain' }
function deltaVerdict(lo, hi) { if (lo > 0) return 'positive'; if (hi < 0) return 'negative'; return 'uncertain' }

function refCI(dir, direction) {
  const txt = readFileSync(ROOT + '/' + dir + '/step10/step10_bootstrap_summary.csv', 'utf8')
  for (const ln of txt.split('\n')) {
    const f = ln.replace(/\r$/, '').split(',')
    if (f[1] === direction && f[2] === 'roc_auc__raw_source_only_thermal')
      return { lo: parseFloat(f[6]), hi: parseFloat(f[7]), mean: parseFloat(f[8]) }
  }
  return null
}
function refPoint(dir, direction) {
  const j = JSON.parse(readFileSync(ROOT + '/' + dir + '/step9b/cross_region_transfer_metrics.json', 'utf8'))
  for (const r of (j.results || []))
    if (r.transfer_direction === direction && r.population === POP && !r.skipped)
      return { thermal: r.thermal_metrics.roc_auc, baseline: r.baseline_metrics.roc_auc,
               delta: r.delta_metrics.delta_auc }
  return null
}
// Published paired-delta interval: step9c, the source of paper/baseline_vs_thermal_transfer.csv.
function refDeltaCI(dir, direction) {
  const j = JSON.parse(readFileSync(ROOT + '/' + dir + '/step9c/cross_region_bootstrap_metrics.json', 'utf8'))
  for (const g of (j.groups || []))
    if (g.transfer_direction === direction && g.population === POP && g.confidence_intervals)
      return { lo: g.confidence_intervals.delta_roc_auc.ci_2_5,
               hi: g.confidence_intervals.delta_roc_auc.ci_97_5,
               interp: g.confidence_intervals.delta_roc_auc.interpretation }
  return null
}

const rows = []
for (const [src, tgt] of DIRECTIONS) {
  const key = PAIRDIR[src + '|' + tgt] ? src + '|' + tgt : tgt + '|' + src
  const dir = PAIRDIR[key]
  const direction = src + '_to_' + tgt
  const d = loadDirection(dir, direction)
  const sTherm = prepare(d.prob), sBase = prepare(d.probBase)
  const all = new Int32Array(d.y.length).fill(1)
  const point = aucWithCounts(sTherm.order, sTherm.groups, d.y, all)
  const pointBase = aucWithCounts(sBase.order, sBase.groups, d.y, all)
  const rp = refPoint(dir, direction)
  const rc = refCI(dir, direction)
  const rd = refDeltaCI(dir, direction)
  const b2 = bootstrap(d.y, d.blk2, sTherm, sBase, mulberry32(SEED))
  const b10 = bootstrap(d.y, d.blk10, sTherm, sBase, mulberry32(SEED))
  const nPos = d.y.reduce((s, v) => s + v, 0)
  const row = {
    direction, label: LABEL[src] + '->' + LABEL[tgt], pair_dir: dir,
    n_cells: d.y.length, n_burned: nPos,
    point, point_ref: rp.thermal, point_diff: Math.abs(point - rp.thermal),
    ref2_lo: rc.lo, ref2_hi: rc.hi,
    b2_lo: b2.thermal.lo, b2_hi: b2.thermal.hi, b2_blocks: b2.nBlocks, b2_invalid: b2.nInvalid,
    d2_lo: Math.abs(b2.thermal.lo - rc.lo), d2_hi: Math.abs(b2.thermal.hi - rc.hi),
    b10_lo: b10.thermal.lo, b10_hi: b10.thermal.hi, b10_blocks: b10.nBlocks, b10_invalid: b10.nInvalid,
    w2: b2.thermal.hi - b2.thermal.lo, w10: b10.thermal.hi - b10.thermal.lo,
    v2: verdict(b2.thermal.lo, b2.thermal.hi), v2ref: verdict(rc.lo, rc.hi),
    v10: verdict(b10.thermal.lo, b10.thermal.hi),
    // paired thermal-minus-baseline delta, formed inside each replicate
    point_base: pointBase, point_base_ref: rp.baseline,
    point_base_diff: Math.abs(pointBase - rp.baseline),
    point_delta: point - pointBase, point_delta_ref: rp.delta,
    point_delta_diff: Math.abs((point - pointBase) - rp.delta),
    dref2_lo: rd.lo, dref2_hi: rd.hi, dref2_interp: rd.interp,
    d2d_lo: b2.delta.lo, d2d_hi: b2.delta.hi,
    d10d_lo: b10.delta.lo, d10d_hi: b10.delta.hi,
    dd2_lo: Math.abs(b2.delta.lo - rd.lo), dd2_hi: Math.abs(b2.delta.hi - rd.hi),
    dw2: b2.delta.hi - b2.delta.lo, dw10: b10.delta.hi - b10.delta.lo,
    dv2: deltaVerdict(b2.delta.lo, b2.delta.hi),
    dv2ref: deltaVerdict(rd.lo, rd.hi),
    dv10: deltaVerdict(b10.delta.lo, b10.delta.hi),
  }
  rows.push(row)
  console.error(row.label.padEnd(23)
    + ' lvl ' + point.toFixed(4)
    + ' 2c [' + b2.thermal.lo.toFixed(4) + ',' + b2.thermal.hi.toFixed(4) + ']'
    + ' 10c [' + b10.thermal.lo.toFixed(4) + ',' + b10.thermal.hi.toFixed(4) + ']'
    + ' | dlt ' + (row.point_delta >= 0 ? '+' : '') + row.point_delta.toFixed(4)
    + ' 2c [' + b2.delta.lo.toFixed(4) + ',' + b2.delta.hi.toFixed(4) + ']'
    + ' ref [' + rd.lo.toFixed(4) + ',' + rd.hi.toFixed(4) + ']'
    + ' 10c [' + b10.delta.lo.toFixed(4) + ',' + b10.delta.hi.toFixed(4) + ']'
    + ' ' + row.dv2ref + '/' + row.dv10)
}
const stem = SEED === 42 ? 'transfer_ci_blocksize' : 'transfer_ci_blocksize_seed' + SEED
writeFileSync(stem + '.json', JSON.stringify(rows, null, 1))

const f4 = x => x.toFixed(4)
// The two *_seed_stable columns record the outcome of the separate seed sweep (BSEED=42..46)
// documented in transfer_ci_blocksize.md, not of this single run. A direction is listed here
// when its 10-cell verdict changes across those five seeds.
const LEVEL_BORDERLINE = new Set(['evia_2021_extended_to_bejis_2022'])
const DELTA_BORDERLINE_10 = new Set([
  'manavgat_2021_to_mugla_2021',            // upper bound sits on zero
  'evia_2021_extended_to_montiferru_2021',  // lower bound sits on zero
])
// The paired delta is borderline at 2-cell blocking too, which is new information about the
// published count: Bejis->Manavgat has a lower bound within 0.001 of zero, so whether it is
// counted positive or uncertain depends on the random stream.
const DELTA_BORDERLINE_2 = new Set(['bejis_2022_to_manavgat_2021'])
const csvHead = ['direction', 'target_region', 'n_target_cells', 'n_burned', 'target_prevalence',
  'point_roc_auc', 'ci_2cell_lo_published', 'ci_2cell_hi_published',
  'ci_2cell_lo_reproduced', 'ci_2cell_hi_reproduced', 'ci_10cell_lo', 'ci_10cell_hi',
  'n_blocks_2cell', 'n_blocks_10cell', 'width_2cell', 'width_10cell',
  'verdict_2cell', 'verdict_10cell', 'verdict_10cell_seed_stable',
  'baseline_roc_auc', 'delta_roc_auc',
  'delta_ci_2cell_lo_published', 'delta_ci_2cell_hi_published',
  'delta_ci_2cell_lo_reproduced', 'delta_ci_2cell_hi_reproduced',
  'delta_ci_10cell_lo', 'delta_ci_10cell_hi', 'delta_width_2cell', 'delta_width_10cell',
  'delta_verdict_2cell', 'delta_verdict_10cell',
  'delta_verdict_2cell_seed_stable', 'delta_verdict_10cell_seed_stable']
const csv = [csvHead.join(',')]
for (const x of rows) {
  csv.push([x.label.replace('->', '_to_'), x.direction.split('_to_')[1], x.n_cells, x.n_burned,
    (x.n_burned / x.n_cells).toFixed(4), f4(x.point), f4(x.ref2_lo), f4(x.ref2_hi),
    f4(x.b2_lo), f4(x.b2_hi), f4(x.b10_lo), f4(x.b10_hi), x.b2_blocks, x.b10_blocks,
    f4(x.w2), f4(x.w10), x.v2ref, x.v10,
    LEVEL_BORDERLINE.has(x.direction) ? 'no' : 'yes',
    f4(x.point_base), f4(x.point_delta),
    f4(x.dref2_lo), f4(x.dref2_hi), f4(x.d2d_lo), f4(x.d2d_hi),
    f4(x.d10d_lo), f4(x.d10d_hi), f4(x.dw2), f4(x.dw10),
    x.dv2ref, x.dv10,
    DELTA_BORDERLINE_2.has(x.direction) ? 'no' : 'yes',
    DELTA_BORDERLINE_10.has(x.direction) ? 'no' : 'yes'].join(','))
}
writeFileSync(stem + '.csv', csv.join('\n') + '\n')

const cnt = (k, v) => rows.filter(r => r[k] === v).length
console.error('')
console.error('max |point - step9b point| = ' + Math.max(...rows.map(r => r.point_diff)))
console.error('max |2c lo - step10 lo| = ' + Math.max(...rows.map(r => r.d2_lo)).toFixed(5)
  + '   max |2c hi - step10 hi| = ' + Math.max(...rows.map(r => r.d2_hi)).toFixed(5))
console.error('mean |lo diff| = ' + (rows.reduce((s, r) => s + r.d2_lo, 0) / rows.length).toFixed(5)
  + '   mean |hi diff| = ' + (rows.reduce((s, r) => s + r.d2_hi, 0) / rows.length).toFixed(5))
console.error('verdict agreement 2c mine vs step10: ' + rows.filter(r => r.v2 === r.v2ref).length + '/20')
console.error('2-cell (step10 ref): above ' + cnt('v2ref', 'above') + ' below ' + cnt('v2ref', 'below') + ' uncertain ' + cnt('v2ref', 'uncertain'))
console.error('2-cell (mine)      : above ' + cnt('v2', 'above') + ' below ' + cnt('v2', 'below') + ' uncertain ' + cnt('v2', 'uncertain'))
console.error('10-cell            : above ' + cnt('v10', 'above') + ' below ' + cnt('v10', 'below') + ' uncertain ' + cnt('v10', 'uncertain'))
const sw2 = rows.map(r => r.w2).sort((a, b) => a - b), sw10 = rows.map(r => r.w10).sort((a, b) => a - b)
console.error('median width 2c ' + ((sw2[9] + sw2[10]) / 2).toFixed(4) + '  10c ' + ((sw10[9] + sw10[10]) / 2).toFixed(4))
console.error('mean width ratio 10c/2c ' + (rows.reduce((s, r) => s + r.w10 / r.w2, 0) / rows.length).toFixed(3))

console.error('')
console.error('--- paired delta (thermal minus baseline) ---')
console.error('max |baseline point - step9b| = ' + Math.max(...rows.map(r => r.point_base_diff)))
console.error('max |delta point - step9b| = ' + Math.max(...rows.map(r => r.point_delta_diff)))
console.error('max |2c delta lo - step9c lo| = ' + Math.max(...rows.map(r => r.dd2_lo)).toFixed(5)
  + '   max |2c delta hi - step9c hi| = ' + Math.max(...rows.map(r => r.dd2_hi)).toFixed(5))
console.error('mean |delta lo diff| = ' + (rows.reduce((s, r) => s + r.dd2_lo, 0) / rows.length).toFixed(5)
  + '   mean |delta hi diff| = ' + (rows.reduce((s, r) => s + r.dd2_hi, 0) / rows.length).toFixed(5))
console.error('delta verdict agreement 2c mine vs step9c: ' + rows.filter(r => r.dv2 === r.dv2ref).length + '/20')
console.error('delta 2-cell (step9c ref): pos ' + cnt('dv2ref', 'positive') + ' neg ' + cnt('dv2ref', 'negative') + ' uncertain ' + cnt('dv2ref', 'uncertain'))
console.error('delta 2-cell (mine)      : pos ' + cnt('dv2', 'positive') + ' neg ' + cnt('dv2', 'negative') + ' uncertain ' + cnt('dv2', 'uncertain'))
console.error('delta 10-cell            : pos ' + cnt('dv10', 'positive') + ' neg ' + cnt('dv10', 'negative') + ' uncertain ' + cnt('dv10', 'uncertain'))
console.error('delta point sign flips 2c vs 10c: 0 by construction (points do not depend on blocking)')
const dsw2 = rows.map(r => r.dw2).sort((a, b) => a - b), dsw10 = rows.map(r => r.dw10).sort((a, b) => a - b)
console.error('delta median width 2c ' + ((dsw2[9] + dsw2[10]) / 2).toFixed(4) + '  10c ' + ((dsw10[9] + dsw10[10]) / 2).toFixed(4))
console.error('delta mean width ratio 10c/2c ' + (rows.reduce((s, r) => s + r.dw10 / r.dw2, 0) / rows.length).toFixed(3))
console.error('delta changed verdict: ' + rows.filter(r => r.dv2ref !== r.dv10).map(r => r.label + ' ' + r.dv2ref + '->' + r.dv10).join('; '))

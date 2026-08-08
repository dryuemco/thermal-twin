// Burned-patch connected components per region, primary population
// (valid_for_modeling AND burnable_tree_shrub_grass), 8-connectivity on row_500m/col_500m.
// Verification target: Emrehan's "Rejim tablosu" (ozet_sonuclar.xlsx) /
// diagnostics/burned_pattern_audit comparison CSV.
import { parquetReadObjects } from 'hyparquet';
import { readFileSync, writeFileSync } from 'fs';

const ROOT = 'C:/Users/CORSAIR/projects/thermal-twin';
const REGIONS = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended', 'montiferru_2021'];
const COLS = ['burned', 'valid_for_modeling', 'burnable_tree_shrub_grass', 'row_500m', 'col_500m'];

const EXPECTED = { // from Emrehan's Rejim tablosu (TSG)
  manavgat_2021:      { burned: 784,  n: 15, largest: 690,  share: 0.8801, second: 32,  effn: 1.2872 },
  bejis_2022:         { burned: 1100, n: 1,  largest: 1100, share: 1.0,    second: 0,   effn: 1.0 },
  mugla_2021:         { burned: 2911, n: 10, largest: 914,  share: 0.3140, second: 738, effn: 4.0545 },
  evia_2021_extended: { burned: 2664, n: 2,  largest: 2653, share: 0.9959, second: 11,  effn: 1.0083 },
  montiferru_2021:    { burned: 539,  n: 8,  largest: 416,  share: 0.7718, second: 55,  effn: 1.6275 },
};

function components(cells) { // cells: array of [row, col]; 8-connectivity
  const key = (r, c) => r * 1000000 + c;
  const set = new Set(cells.map(([r, c]) => key(r, c)));
  const seen = new Set();
  const sizes = [];
  for (const [r0, c0] of cells) {
    const k0 = key(r0, c0);
    if (seen.has(k0)) continue;
    let size = 0;
    const stack = [[r0, c0]];
    seen.add(k0);
    while (stack.length) {
      const [r, c] = stack.pop();
      size++;
      for (let dr = -1; dr <= 1; dr++) for (let dc = -1; dc <= 1; dc++) {
        if (dr === 0 && dc === 0) continue;
        const kn = key(r + dr, c + dc);
        if (set.has(kn) && !seen.has(kn)) { seen.add(kn); stack.push([r + dr, c + dc]); }
      }
    }
    sizes.push(size);
  }
  sizes.sort((a, b) => b - a);
  return sizes;
}

const out = {};
let anyFail = false;
for (const region of REGIONS) {
  const file = readFileSync(`${ROOT}/drive_new/experiments/${region}/step8a/step8a_500m_modeling_dataset.parquet`);
  const buf = file.buffer.slice(file.byteOffset, file.byteOffset + file.byteLength);
  const rows = await parquetReadObjects({ file: buf, columns: COLS });
  const cells = [];
  for (const r of rows) {
    if (r.burned && r.valid_for_modeling && r.burnable_tree_shrub_grass) {
      cells.push([Number(r.row_500m), Number(r.col_500m)]);
    }
  }
  const sizes = components(cells);
  const N = cells.length;
  const largest = sizes[0] ?? 0;
  const second = sizes[1] ?? 0;
  const share = largest / N;
  const effn = 1 / sizes.reduce((s, x) => s + (x / N) ** 2, 0);
  const res = { burned_cells: N, component_count: sizes.length, largest_component: largest,
    largest_share: share, second_largest: second, effective_component_count: effn,
    component_sizes: sizes };
  out[region] = res;
  const e = EXPECTED[region];
  const ok = N === e.burned && sizes.length === e.n && largest === e.largest && second === e.second
    && Math.abs(share - e.share) < 0.0001 && Math.abs(effn - e.effn) < 0.0001;
  if (!ok) anyFail = true;
  console.log(`${region.padEnd(20)} burned=${N} comps=${sizes.length} largest=${largest} share=${(share * 100).toFixed(2)}% second=${second} effN=${effn.toFixed(4)}  ${ok ? 'MATCH' : '*** MISMATCH (expected ' + JSON.stringify(e) + ')'}`);
}
writeFileSync(`${ROOT}/paper/_tmp_burned_components.json`, JSON.stringify(out, null, 2));
console.log(anyFail ? '\nVERIFICATION FAILED' : '\nALL REGIONS MATCH EMREHAN');
process.exit(anyFail ? 1 : 0);

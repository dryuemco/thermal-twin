// Fig. 1 AOI extraction (Windows side; drive_new symlink unreadable from WSL).
// Bboxes from step0 aoi_preview.geojson where present; for mugla/montiferru
// (no step0 export) derived from the 30 m reference-grid affine transform in
// step8a_dataset_stats.json — same derivation as 03_methods §3.1 Table 1.
import { createHash } from 'crypto';
import { readFileSync, writeFileSync } from 'fs';

const ROOT = 'C:/Users/CORSAIR/projects/thermal-twin';
const sources = {};
const read = p => {
  const buf = readFileSync(`${ROOT}/${p}`);
  sources[p] = createHash('sha256').update(buf).digest('hex');
  return JSON.parse(buf.toString('utf8'));
};

function bboxFromGeojson(g) {
  const xs = [], ys = [];
  const walk = c => Array.isArray(c[0]) ? c.forEach(walk) : (xs.push(c[0]), ys.push(c[1]));
  const feats = g.type === 'FeatureCollection' ? g.features : [g];
  for (const f of feats) walk(f.geometry.coordinates);
  return [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)];
}
function bboxFromGrid(stats) {
  const { width, height, transform } = stats.reference_30m_grid;
  const [a, , c, , e, f] = transform;
  const W = c, N = f, E = c + width * a, S = f + height * e;
  return [W, Math.min(S, N), E, Math.max(S, N)];
}

const aoi = {};
for (const reg of ['manavgat_2021', 'bejis_2022', 'evia_2021_extended']) {
  aoi[reg] = { bbox: bboxFromGeojson(read(`drive_new/experiments/${reg}/step0/aoi_preview.geojson`)),
               method: 'step0 aoi_preview.geojson' };
}
for (const reg of ['mugla_2021', 'montiferru_2021']) {
  aoi[reg] = { bbox: bboxFromGrid(read(`drive_new/experiments/${reg}/step8a/step8a_dataset_stats.json`)),
               method: '30m reference-grid transform (no step0 export)' };
}
// sanity: manavgat grid-derived must match its geojson bbox to ~2e-3 deg
const manGrid = bboxFromGrid(read('drive_new/experiments/manavgat_2021/step8a/step8a_dataset_stats.json'));
for (let i = 0; i < 4; i++) {
  if (Math.abs(manGrid[i] - aoi.manavgat_2021.bbox[i]) > 2e-3) {
    throw new Error(`derivation sanity check failed: manavgat ${i} ${manGrid[i]} vs ${aoi.manavgat_2021.bbox[i]}`);
  }
}
writeFileSync(`${ROOT}/paper/figures/data/fig1_aoi.json`, JSON.stringify({
  meta: { created: '2026-08-08', extractor: 'paper/figures/extract_fig1_aoi.mjs',
          sanity: 'manavgat grid-derived bbox matches step0 geojson to <2e-3 deg', sources },
  aoi,
}, null, 1));
for (const [r, v] of Object.entries(aoi)) console.log(r, v.bbox.map(x => x.toFixed(4)).join(', '), `(${v.method})`);

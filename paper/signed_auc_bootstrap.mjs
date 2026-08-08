import { parquetReadObjects } from 'hyparquet'
import { readFileSync } from 'fs'

const FEATURES = ['ndvi_mean','elevation_mean','slope_mean','current_lst_mean',
  'current_tvdi_mean','tvdi_difference_mean','downscaled_lst_mean','fused_lst_mean','lst_anomaly_mean']
const NEED = ['burned','valid_for_modeling','burnable_tree_shrub_grass','row_500m','col_500m',...FEATURES]
const BLOCK = 10          // ~5 km, matches run_c / step9g
const NBOOT = 1000
const SEED = 42

// mulberry32 seeded PRNG (deterministic; not numpy's stream — noted in output)
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}

// signed AUC = P(x_pos > x_neg) via rank method (ties=0.5). No folding.
function signedAUC(vals, labels, idx){
  // gather finite
  const arr=[]
  let np=0,nn=0
  for(const i of idx){const v=vals[i];if(Number.isFinite(v)){arr.push([v,labels[i]]); if(labels[i])np++;else nn++}}
  if(np===0||nn===0) return null
  arr.sort((a,b)=>a[0]-b[0])
  // assign average ranks handling ties
  let sumRankPos=0
  let i=0
  const n=arr.length
  while(i<n){
    let j=i
    while(j<n&&arr[j][0]===arr[i][0]) j++
    const avgRank=(i+1+j)/2   // ranks i+1..j averaged
    for(let k=i;k<j;k++) if(arr[k][1]) sumRankPos+=avgRank
    i=j
  }
  const auc=(sumRankPos - np*(np+1)/2)/(np*nn)
  return auc
}

function percentile(sorted,p){
  const n=sorted.length
  if(n===0) return NaN
  const idx=(p/100)*(n-1)
  const lo=Math.floor(idx), hi=Math.ceil(idx)
  if(lo===hi) return sorted[lo]
  return sorted[lo]+(sorted[hi]-sorted[lo])*(idx-lo)
}

async function run(region, path){
  const buf=readFileSync(path)
  const ab=buf.buffer.slice(buf.byteOffset,buf.byteOffset+buf.byteLength)
  const rows=await parquetReadObjects({file:ab,columns:NEED})
  // natural-veg population
  const pop=rows.filter(r=>r.valid_for_modeling===true && r.burnable_tree_shrub_grass===true)
  // block id -> row indices
  const blockMap=new Map()
  const labels=new Uint8Array(pop.length)
  const feat={}
  for(const f of FEATURES) feat[f]=new Float64Array(pop.length)
  for(let i=0;i<pop.length;i++){
    const r=pop[i]
    labels[i]=r.burned?1:0
    for(const f of FEATURES) feat[f][i]=(r[f]==null?NaN:Number(r[f]))
    const br=Math.floor(Number(r.row_500m)/BLOCK), bc=Math.floor(Number(r.col_500m)/BLOCK)
    const key=br+'_'+bc
    let a=blockMap.get(key); if(!a){a=[];blockMap.set(key,a)} a.push(i)
  }
  const blocks=[...blockMap.values()]
  const nBlocks=blocks.length
  const allIdx=[...Array(pop.length).keys()]
  let npos=0; for(const l of labels) if(l) npos++

  // point estimates
  const point={}
  for(const f of FEATURES) point[f]=signedAUC(feat[f],labels,allIdx)

  // bootstrap: resample blocks with replacement
  const rng=mulberry32(SEED)
  const dist={}; for(const f of FEATURES) dist[f]=[]
  let skipped=0
  for(let b=0;b<NBOOT;b++){
    // build resampled index set
    const idx=[]
    for(let k=0;k<nBlocks;k++){
      const blk=blocks[(rng()*nBlocks)|0]
      for(const i of blk) idx.push(i)
    }
    for(const f of FEATURES){
      const a=signedAUC(feat[f],labels,idx)
      if(a!==null) dist[f].push(a)
    }
  }
  const out={region,n_cells:pop.length,n_positive:npos,n_blocks:nBlocks,block_cells:BLOCK,n_boot:NBOOT,features:{}}
  for(const f of FEATURES){
    const s=dist[f].slice().sort((a,b)=>a-b)
    out.features[f]={point:point[f],ci_2_5:percentile(s,2.5),median:percentile(s,50),ci_97_5:percentile(s,97.5),n_valid:s.length}
  }
  return out
}

const jobs=[
  ['manavgat_2021','ext/stdt/experiments/manavgat_2021/step8a/step8a_500m_modeling_dataset.parquet'],
  ['bejis_2022','ext/stdt/experiments/bejis_2022/step8a/step8a_500m_modeling_dataset.parquet'],
  ['mugla_2021','ext/stdt/experiments/mugla_2021/step8a/step8a_500m_modeling_dataset.parquet'],
]
const results=[]
for(const [r,p] of jobs){ results.push(await run(r,p)) }
import {writeFileSync} from 'fs'
writeFileSync('signed_auc_bootstrap.json',JSON.stringify(results,null,2))
// print compact table
for(const res of results){
  console.log(`\n### ${res.region}  n=${res.n_cells} pos=${res.n_positive} blocks=${res.n_blocks}`)
  for(const f of FEATURES){
    const x=res.features[f]
    console.log(`  ${f.padEnd(22)} ${x.point.toFixed(4)}  [${x.ci_2_5.toFixed(4)}, ${x.ci_97_5.toFixed(4)}]`)
  }
}
console.log('\nWROTE signed_auc_bootstrap.json')

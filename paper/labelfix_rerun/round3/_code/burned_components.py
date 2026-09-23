"""Python port of paper/burned_components.mjs (hyparquet is not installed; installing is not allowed).
Same algorithm: TSG burned cells (burned & valid_for_modeling & burnable_tree_shrub_grass), 8-connectivity on
row_500m/col_500m, component sizes sorted descending, largest share, effective count 1/sum(share^2).
Reads $R3ROOT/drive_new/experiments/<region>/step8a/step8a_500m_modeling_dataset.parquet, writes
$R3ROOT/paper/_tmp_burned_components.json (same schema). The .mjs EXPECTED table is the frozen Rejim table;
here the check is against the burned_pattern_audit comparison CSV found under the same overlay root."""
import json, os, sys
import pandas as pd
ROOT = os.environ["R3ROOT"]
REGIONS = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended', 'montiferru_2021']
COLS = ['burned', 'valid_for_modeling', 'burnable_tree_shrub_grass', 'row_500m', 'col_500m']
def components(cells):
    s = set(cells); seen = set(); sizes = []
    for c0 in cells:
        if c0 in seen: continue
        seen.add(c0); stack = [c0]; size = 0
        while stack:
            r, c = stack.pop(); size += 1
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0: continue
                    k = (r + dr, c + dc)
                    if k in s and k not in seen: seen.add(k); stack.append(k)
        sizes.append(size)
    return sorted(sizes, reverse=True)
out = {}
for region in REGIONS:
    df = pd.read_parquet(f"{ROOT}/drive_new/experiments/{region}/step8a/step8a_500m_modeling_dataset.parquet", columns=COLS)
    m = df.burned.astype(bool) & df.valid_for_modeling.astype(bool) & df.burnable_tree_shrub_grass.astype(bool)
    cells = list(zip(df.loc[m, 'row_500m'].astype(int), df.loc[m, 'col_500m'].astype(int)))
    sizes = components(cells); N = len(cells)
    largest = sizes[0] if sizes else 0; second = sizes[1] if len(sizes) > 1 else 0
    effn = 1 / sum((x / N) ** 2 for x in sizes)
    out[region] = dict(burned_cells=N, component_count=len(sizes), largest_component=largest,
                       largest_share=largest / N, second_largest=second, effective_component_count=effn,
                       component_sizes=sizes)
    print(f"{region:20s} burned={N} comps={len(sizes)} largest={largest} share={largest/N*100:.2f}% second={second} effN={effn:.4f}")
json.dump(out, open(f"{ROOT}/paper/_tmp_burned_components.json", "w"), indent=2)

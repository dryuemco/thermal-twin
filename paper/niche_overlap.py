#!/usr/bin/env python3
"""Analysis 4 - canonical SDM niche-overlap measures between regional burned-cell
feature distributions, i.e. P(x | y=1). Fixed candidate set:
  (a) Schoener's D  - mean of 9 per-feature 1D histogram overlaps (50 shared bins over the
      global range of all five regions' burned cells), plus a multivariate variant on the
      first 2 PCs (global PCA, 20x20 bins over global PC range)
  (b) Warren's I    - Hellinger-based, same histograms (1D mean + PCA-2D)
  (c) Mahalanobis   - distance between burned-cell centroids, pooled covariance
All from burned cells of the primary population only (valid_for_modeling AND
burnable_tree_shrub_grass AND burned==1). No unburned variant (by design).
"""
import json, sys
import numpy as np
import pandas as pd
import sklearn
from sklearn.decomposition import PCA

STAGING = sys.argv[1]
OUT = sys.argv[2]

REGIONS = ['manavgat_2021', 'bejis_2022', 'mugla_2021', 'evia_2021_extended', 'montiferru_2021']
FEATURES = ['ndvi_mean', 'elevation_mean', 'slope_mean', 'lst_anomaly_mean', 'current_lst_mean',
            'current_tvdi_mean', 'tvdi_difference_mean', 'downscaled_lst_mean', 'fused_lst_mean']
NBINS_1D = 50
NBINS_2D = 20

burned = {}
nan_report = {}
for reg in REGIONS:
    df = pd.read_parquet(f'{STAGING}/{reg}.parquet',
                         columns=['burned', 'valid_for_modeling', 'burnable_tree_shrub_grass'] + FEATURES)
    b = df[(df.valid_for_modeling == True) & (df.burnable_tree_shrub_grass == True) & (df.burned == 1)]
    burned[reg] = b[FEATURES].copy()
    nan_report[reg] = {f: int(b[f].isna().sum()) for f in FEATURES if b[f].isna().sum() > 0}
    print(f'{reg}: burned n={len(b)} nan_cells={sum(nan_report[reg].values())}', flush=True)

# global per-feature ranges and pooled stats (for shared bins / standardization / PCA)
pooled = pd.concat(burned.values(), ignore_index=True)
glo_min = pooled.min()
glo_max = pooled.max()
pooled_median = pooled.median()
pooled_mean = pooled.mean()
pooled_std = pooled.std(ddof=0).replace(0, 1.0)

def std_impute(df):  # standardize globally, impute NaN with pooled median (documented)
    return ((df.fillna(pooled_median) - pooled_mean) / pooled_std).to_numpy()

pca = PCA(n_components=2, random_state=42).fit(std_impute(pooled))
pc = {reg: pca.transform(std_impute(burned[reg])) for reg in REGIONS}
pc_all = pca.transform(std_impute(pooled))
pc_min, pc_max = pc_all.min(axis=0), pc_all.max(axis=0)

def hist1d(vals, lo, hi):
    v = vals[np.isfinite(vals)]
    h, _ = np.histogram(v, bins=NBINS_1D, range=(lo, hi))
    return h / h.sum()

def hist2d(xy):
    h, _, _ = np.histogram2d(xy[:, 0], xy[:, 1], bins=NBINS_2D,
                             range=[[pc_min[0], pc_max[0]], [pc_min[1], pc_max[1]]])
    return (h / h.sum()).ravel()

def schoener_d(p, q):
    return float(1 - 0.5 * np.abs(p - q).sum())

def warren_i(p, q):
    return float(1 - 0.5 * ((np.sqrt(p) - np.sqrt(q)) ** 2).sum())

def mahalanobis(a_df, b_df):
    a = std_impute(a_df); b = std_impute(b_df)
    mu = a.mean(axis=0) - b.mean(axis=0)
    Sa = np.cov(a, rowvar=False); Sb = np.cov(b, rowvar=False)
    na, nb = len(a), len(b)
    S = ((na - 1) * Sa + (nb - 1) * Sb) / (na + nb - 2)
    return float(np.sqrt(mu @ np.linalg.solve(S, mu)))

pairs = []
for i in range(len(REGIONS)):
    for j in range(i + 1, len(REGIONS)):
        a, b = REGIONS[i], REGIONS[j]
        d1, i1 = [], []
        for f in FEATURES:
            p = hist1d(burned[a][f].to_numpy(float), glo_min[f], glo_max[f])
            q = hist1d(burned[b][f].to_numpy(float), glo_min[f], glo_max[f])
            d1.append(schoener_d(p, q)); i1.append(warren_i(p, q))
        p2, q2 = hist2d(pc[a]), hist2d(pc[b])
        pairs.append(dict(
            region_a=a, region_b=b,
            schoener_d_mean1d=float(np.mean(d1)),
            warren_i_mean1d=float(np.mean(i1)),
            schoener_d_pca2d=schoener_d(p2, q2),
            warren_i_pca2d=warren_i(p2, q2),
            mahalanobis_burned=mahalanobis(burned[a], burned[b]),
            per_feature_schoener_d={f: round(v, 4) for f, v in zip(FEATURES, d1)},
        ))
        r = pairs[-1]
        print(f"{a}~{b}: D1={r['schoener_d_mean1d']:.3f} I1={r['warren_i_mean1d']:.3f} "
              f"D2={r['schoener_d_pca2d']:.3f} I2={r['warren_i_pca2d']:.3f} "
              f"Mah={r['mahalanobis_burned']:.3f}", flush=True)

meta = dict(
    created='2026-08-08',
    environment=f'python {sys.version.split()[0]}, scikit-learn {sklearn.__version__}, '
                f'numpy {np.__version__}, pandas {pd.__version__} (WSL micromamba mm-thermal)',
    population='valid_for_modeling AND burnable_tree_shrub_grass AND burned==1 (P(x|y=1) only, no unburned variant)',
    binning=f'1D: {NBINS_1D} shared bins over the global range of all five regions\' burned cells per feature; '
            f'2D: {NBINS_2D}x{NBINS_2D} bins over global PC1-PC2 range',
    pca='PCA(2) fit on pooled standardized burned cells of all five regions (global mean/sd ddof=0, NaN -> pooled median)',
    mahalanobis='between standardized burned-cell centroids, pooled covariance ((na-1)Sa+(nb-1)Sb)/(na+nb-2), 9 features',
    burned_counts={r: int(len(burned[r])) for r in REGIONS},
    nan_cells_imputed_for_multivariate=nan_report,
    parquet_sha256_prefixes=dict(manavgat_2021='054a1961', bejis_2022='3dec785a', mugla_2021='c4ab107d',
                                 evia_2021_extended='bdce859c', montiferru_2021='ffb008f9'),
)
json.dump(dict(meta=meta, pairs=pairs), open(OUT, 'w'), indent=1)
print('written', OUT, flush=True)

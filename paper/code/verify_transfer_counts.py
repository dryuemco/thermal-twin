import numpy as np, pandas as pd
from scipy import ndimage
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
REG=["manavgat_2021","bejis_2022","mugla_2021","evia_2021_extended","montiferru_2021"]
ROOT="repo/outputs/experiments/{}/step8a/step8a_500m_modeling_dataset.parquet"
TH=["ndvi_mean","elevation_mean","slope_mean","landcover_dominant","lst_anomaly_mean",
    "current_lst_mean","current_tvdi_mean","tvdi_difference_mean","downscaled_lst_mean","fused_lst_mean"]
CAT="landcover_dominant"; CELL=0.45; BLK=10; NB=400
def build():
    num=[f for f in TH if f!=CAT]
    tr=[("num",Pipeline([("i",SimpleImputer(strategy="median"))]),num),
        ("cat",Pipeline([("i",SimpleImputer(strategy="most_frequent")),("o",OneHotEncoder(handle_unknown="ignore"))]),[CAT])]
    return Pipeline([("p",ColumnTransformer(tr)),("c",RandomForestClassifier(n_estimators=300,min_samples_leaf=3,class_weight="balanced",random_state=42,n_jobs=-1))])
def load(r):
    d=pd.read_parquet(ROOT.format(r))
    d=d[(d.valid_for_modeling==True)&(d.burnable_tree_shrub_grass==True)].reset_index(drop=True)
    r0,c0=int(d.row_500m.min()),int(d.col_500m.min())
    H=int(d.row_500m.max())-r0+1; W=int(d.col_500m.max())-c0+1
    rr=d.row_500m.to_numpy().astype(int)-r0; cc=d.col_500m.to_numpy().astype(int)-c0
    bg=np.ones((H,W),bool); b=d.burned.to_numpy()==1; bg[rr[b],cc[b]]=False
    d["dist_km"]=ndimage.distance_transform_edt(bg)[rr,cc]*CELL
    d["block"]=(d.row_500m//BLK).astype(str)+"_"+(d.col_500m//BLK).astype(str)
    return d
data={r:load(r) for r in REG}
def boot(y,s,blk,seed=42):
    rng=np.random.default_rng(seed); u=np.unique(blk); idx={b:np.where(blk==b)[0] for b in u}; out=[]
    for _ in range(NB):
        pick=rng.choice(u,len(u),replace=True); i=np.concatenate([idx[b] for b in pick])
        if len(np.unique(y[i]))>1: out.append(roc_auc_score(y[i],s[i]))
    return np.percentile(out,2.5), np.percentile(out,97.5)
for tag,coll in [("full",None),("collar10",10)]:
    fitted={}
    for s in REG:
        sub=data[s] if coll is None else data[s][data[s].dist_km<=coll]
        fitted[s]=build().fit(sub[TH],sub.burned)
    ab=bl=abs_=bls=0
    for s in REG:
        for t in REG:
            if s==t: continue
            sub=data[t] if coll is None else data[t][data[t].dist_km<=coll]
            sc=fitted[s].predict_proba(sub[TH])[:,1]; y=sub.burned.to_numpy()
            a=roc_auc_score(y,sc); lo,hi=boot(y,sc,sub.block.to_numpy())
            if a>0.5: ab+=1
            else: bl+=1
            if lo>0.5: abs_+=1
            if hi<0.5: bls+=1
    print(f"{tag:9s} point: {ab} above / {bl} below   interval-supported: {abs_} above / {bls} below")

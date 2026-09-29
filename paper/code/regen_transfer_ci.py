"""Regenerate paper/aoi_frame_transfer.csv with 10-cell spatial-block bootstrap
bounds, so the interval-supported counts quoted in Section 4.9 are checkable
from the artefact rather than asserted. Read-only with respect to repo/."""
import numpy as np, pandas as pd
from scipy import ndimage
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
import _canonical


def _guard(X, y):
    """Methods 3.13: forbidden-column assertion on the exact columns passed to the model."""
    _canonical.assert_no_leakage(list(X.columns))
    return X, y

REG=["manavgat_2021","bejis_2022","mugla_2021","evia_2021_extended","montiferru_2021"]
TH=["ndvi_mean","elevation_mean","slope_mean","landcover_dominant","lst_anomaly_mean",
    "current_lst_mean","current_tvdi_mean","tvdi_difference_mean","downscaled_lst_mean","fused_lst_mean"]
BASE=["ndvi_mean","elevation_mean","slope_mean","landcover_dominant"]
CAT="landcover_dominant"; CELL=0.45; BLK=10; NB=1000
import os
# Artefacts this script reads or writes that are themselves regenerated from the
# canonical inputs. Default "paper" is the published location; the canonical re-run
# sets PAPER_ARTEFACTS=paper/canonical_rerun so nothing published is overwritten.
ART = os.environ.get("PAPER_ARTEFACTS", "paper")
def build(fe):
    num=[f for f in fe if f!=CAT]
    tr=[("num",Pipeline([("i",SimpleImputer(strategy="median"))]),num),
        ("cat",Pipeline([("i",SimpleImputer(strategy="most_frequent")),("o",OneHotEncoder(handle_unknown="ignore"))]),[CAT])]
    return Pipeline([("p",ColumnTransformer(tr)),("c",RandomForestClassifier(n_estimators=300,min_samples_leaf=3,class_weight="balanced",random_state=42,n_jobs=4))])
def load(r):
    d=_canonical.load(r)
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
    return float(np.percentile(out,2.5)), float(np.percentile(out,97.5))
rows=[]
FR=[("full","full"),("full","10km"),("10km","full"),("10km","10km"),("5km","5km")]
def fr(d,tag): return d if tag=="full" else d[d.dist_km<=(10 if tag=="10km" else 5)]
for sf,tf in FR:
    fitted={s:{l:build(fe).fit(*_guard(fr(data[s],sf)[fe],fr(data[s],sf).burned)) for l,fe in (("thermal",TH),("baseline",BASE))} for s in REG}
    for s in REG:
        for t in REG:
            if s==t: continue
            sub=fr(data[t],tf); y=sub.burned.to_numpy()
            row={"source_frame":sf,"target_frame":tf,"direction":f"{s}_to_{t}"}
            for l,fe in (("thermal",TH),("baseline",BASE)):
                sc=fitted[s][l].predict_proba(sub[fe])[:,1]
                row[l]=float(roc_auc_score(y,sc))
                if l=="thermal":
                    lo,hi=boot(y,sc,sub.block.to_numpy())
                    row["thermal_ci_lo"],row["thermal_ci_hi"]=lo,hi
                    row["ci_above_0.5"]=bool(lo>0.5); row["ci_below_0.5"]=bool(hi<0.5)
            row["delta"]=row["thermal"]-row["baseline"]
            rows.append(row)
    sub=pd.DataFrame([r for r in rows if r["source_frame"]==sf and r["target_frame"]==tf])
    print(f"{sf:5s}/{tf:5s} mean {sub.thermal.mean():.4f}  point {int((sub.thermal>0.5).sum())} above/{int((sub.thermal<0.5).sum())} below  "
          f"CI-supported {int(sub['ci_above_0.5'].sum())} above / {int(sub['ci_below_0.5'].sum())} below", flush=True)
pd.DataFrame(rows).to_csv(f"{ART}/aoi_frame_transfer.csv",index=False)
print(f"wrote {ART}/aoi_frame_transfer.csv with bootstrap bounds")

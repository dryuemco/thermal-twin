"""
step10/adaptation.py

Uc transfer varyanti icin numerik feature adaptasyonu. HEPSI unsupervised
(target etiketi ASLA kullanilmaz).

    raw    : hicbir donusum yok (naif transfer)
    zscore : her bolge kendi mean/std'si ile z-score standardize edilir
    coral  : CORAL (correlation alignment) -- kaynak feature'larinin 1. ve
             2. moment istatistikleri hedefe hizalanir

Onemli: RandomForest tek bir bolgede egitilip test edilince per-feature
monoton donusume (z-score) DUYARSIZDIR; ancak burada model KAYNAK'ta egitilip
HEDEF'te test edildigi icin, her bolgeyi kendi istatistigiyle standardize etmek
esik-hizalamasini degistirir ve covariate-shift'i kismen duzeltir. CORAL
feature'lari kovaryans matrisiyle karistirdigi icin (monoton-olmayan) agac
sinirlarini da degistirir.
"""

from __future__ import annotations

import numpy as np

from config10 import CORAL_EIGVAL_FLOOR, CORAL_LAMBDA, CORAL_VARIANT


def _standardize(x: np.ndarray) -> np.ndarray:
    """Kolon bazli z-score; std==0 olan kolon icin std=1 (bolme guvenligi)."""
    mu = np.nanmean(x, axis=0)
    sd = np.nanstd(x, axis=0)
    sd_safe = np.where(sd == 0, 1.0, sd)
    return (x - mu) / sd_safe


def _sym_matrix_power(mat: np.ndarray, power: float, eps: float) -> np.ndarray:
    """Simetrik PSD matris icin eigendecomposition tabanli matris kuvveti
    (M^power). Sayisal kararlilik icin eps ridge eklenir ve ozdegerler
    pozitife kirpilir."""
    mat = 0.5 * (mat + mat.T)
    mat = mat + eps * np.eye(mat.shape[0])
    vals, vecs = np.linalg.eigh(mat)
    vals = np.clip(vals, eps, None)
    return (vecs * (vals ** power)) @ vecs.T


def adapt_numeric(
    xs: np.ndarray, xt: np.ndarray, variant: str, eps: float = 1e-6,
    coral_lambda: float | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Kaynak (xs) ve hedef (xt) numerik matrislerini varyanta gore donusturur.

    coral_lambda verilmezse CORAL_LAMBDA (=1e-5) kullanilir; λ duyarlilik
    taramasinda override edilir.

    Girdilerde NaN OLMAMALIDIR (once impute edilir). (n_samples, n_features).
    Doner: (xs_transformed, xt_transformed).
    """
    lam = CORAL_LAMBDA if coral_lambda is None else coral_lambda
    xs = np.asarray(xs, dtype="float64")
    xt = np.asarray(xt, dtype="float64")

    if variant == "raw":
        return xs.copy(), xt.copy()

    if variant == "zscore":
        # Her bolge KENDI istatistigiyle standardize edilir (unsupervised).
        return _standardize(xs), _standardize(xt)

    if variant == CORAL_VARIANT or variant == "coral":
        # Emrehan'in tanimi (coral_after_regionwise_zscore), core/step10_shared.py
        # ile BİREBİR:
        #   1) her bolge KENDI mean/std'siyle z-score (regionwise, ddof=0)
        #   2) CORAL: Cs = cov(Xs_z, ddof=0) + λI, Ct = cov(Xt_z, ddof=0) + λI,
        #      A = Cs^{-1/2} @ Ct^{1/2}, Xs* = Xs_z @ A   (λ = STEP10_CORAL_LAMBDA = 1e-5)
        #   3) CORAL yalniz SOURCE'a uygulanir; TARGET z-score'lu haliyle DEGISMEZ.
        xs_z = _standardize(xs)
        xt_z = _standardize(xt)
        d = xs_z.shape[1]
        cs = np.atleast_2d(np.cov(xs_z, rowvar=False, ddof=0)) + lam * np.eye(d)
        ct = np.atleast_2d(np.cov(xt_z, rowvar=False, ddof=0)) + lam * np.eye(d)
        cs_inv_sqrt = _sym_matrix_power(cs, -0.5, CORAL_EIGVAL_FLOOR)
        ct_sqrt = _sym_matrix_power(ct, 0.5, CORAL_EIGVAL_FLOOR)
        a = cs_inv_sqrt @ ct_sqrt
        xs_coral = xs_z @ a
        return xs_coral, xt_z

    raise ValueError(f"Bilinmeyen varyant: {variant}")

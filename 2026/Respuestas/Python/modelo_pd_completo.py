
import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.calibration import CalibratedClassifierCV

ID_COL = "num_doc"
TIME_COL = "f_analisis"
TARGET_COL = "default"
CLIENT_TYPE_COL = "tipo_cliente"

GROUP_PD_RANGES = {
    "t1": (0.00, 0.01),
    "t2": (0.01, 0.015),
    "t3": (0.015, 0.03),
    "t4": (0.03, 0.045),
    "t5": (0.045, 0.08),
    "t6": (0.08, 0.15),
    "t7": (0.15, 0.30),
    "t8": (0.30, 1.00),
}


def add_domain_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if {"CO01END002RO", "CO01END010RO"}.issubset(df.columns):
        saldo = df["CO01END002RO"].clip(lower=0)
        cupo = df["CO01END010RO"].clip(lower=0)
        denom = saldo + cupo
        df["util_rotativo"] = np.where(denom > 0, saldo / denom, np.nan)
    if {"CO01END002RO", "CO01END051RO"}.issubset(df.columns):
        saldo_actual = df["CO01END002RO"]
        saldo_9m = df["CO01END051RO"]
        eps = 1e-6
        df["crec_saldo_9m"] = np.where(
            saldo_9m.abs() > 0,
            (saldo_actual - saldo_9m) / (saldo_9m.abs() + eps),
            np.nan,
        )
    for col in ["trx39", "trx143", "trx158"]:
        if col in df.columns:
            df[f"log_{col}"] = np.log1p(df[col].clip(lower=0))
    return df


def apply_negative_coding(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    exclude_cols = {ID_COL, TIME_COL, TARGET_COL, CLIENT_TYPE_COL}
    numeric_cols = [
        c for c in df.columns
        if c not in exclude_cols and np.issubdtype(df[c].dtype, np.number)
    ]
    for col in numeric_cols:
        flag_col = f"{col}_neg_flag"
        df[flag_col] = (df[col] < 0).astype(int)
        df[col] = df[col].mask(df[col] < 0, np.nan)
    return df


def impute_median(train_df: pd.DataFrame, dfs: list) -> tuple[pd.DataFrame, ...]:
    exclude_cols = {ID_COL, TIME_COL, TARGET_COL, CLIENT_TYPE_COL}
    numeric_cols = [
        c for c in train_df.columns
        if c not in exclude_cols and np.issubdtype(train_df[c].dtype, np.number)
    ]
    med = train_df[numeric_cols].median()
    out = []
    for df in dfs:
        df_copy = df.copy()
        common = [c for c in med.index if c in df_copy.columns]
        df_copy[common] = df_copy[common].fillna(med[common])
        out.append(df_copy)
    return (numeric_cols, *out)


def assign_risk_group(prob, thresholds):
    b1, b2, b3, b4, b5, b6, b7 = thresholds
    if prob <= b1:
        return "t1"
    elif prob <= b2:
        return "t2"
    elif prob <= b3:
        return "t3"
    elif prob <= b4:
        return "t4"
    elif prob <= b5:
        return "t5"
    elif prob <= b6:
        return "t6"
    elif prob <= b7:
        return "t7"
    else:
        return "t8"


def evaluate_cutpoints(y_true, proba, thresholds):
    df = pd.DataFrame({"y": y_true, "pd": proba})
    df["grupo_riesgo"] = df["pd"].apply(lambda p: assign_risk_group(p, thresholds))
    total = len(df)
    pop_in_range = 0
    any_empty = False
    for g, (lower, upper) in GROUP_PD_RANGES.items():
        mask = df["grupo_riesgo"] == g
        n_g = mask.sum()
        if n_g == 0:
            any_empty = True
            continue
        dr = df.loc[mask, "y"].mean()
        if dr >= lower and dr <= upper:
            pop_in_range += n_g
    pct_pop_in_range = pop_in_range / total if total > 0 else 0.0
    return pct_pop_in_range, any_empty


def random_perturb_thresholds(base_thresholds, scale=0.002, rng=None):
    if rng is None:
        rng = np.random.default_rng()
    noise = rng.normal(0.0, scale, size=base_thresholds.shape)
    cand = base_thresholds + noise
    cand = np.clip(cand, 1e-4, 0.9999)
    cand = np.sort(cand)
    return cand


def search_best_cutpoints(y_true, proba, base_thresholds, n_iter=120, seed=42):
    rng = np.random.default_rng(seed)
    best_thresholds = base_thresholds.copy()
    best_score, _ = evaluate_cutpoints(y_true, proba, best_thresholds)
    for _ in range(n_iter):
        cand = random_perturb_thresholds(best_thresholds, scale=0.003, rng=rng)
        score, any_empty = evaluate_cutpoints(y_true, proba, cand)
        if any_empty:
            continue
        if score > best_score:
            best_score = score
            best_thresholds = cand
    return best_thresholds, best_score


def main(train_path, valid_path, prueba_path, output_path):
    train = pd.read_csv(train_path, sep='|')
    valid = pd.read_csv(valid_path, sep='|')
    prueba = pd.read_csv(prueba_path, sep='|')

    train_2018 = train[(train[TIME_COL] >= 201801) & (train[TIME_COL] <= 201812)].copy()
    valid_201901 = valid.copy()
    prueba_201902 = prueba.copy()

    train_2018 = add_domain_features(train_2018)
    valid_201901 = add_domain_features(valid_201901)
    prueba_201902 = add_domain_features(prueba_201902)

    train_2018 = apply_negative_coding(train_2018)
    valid_201901 = apply_negative_coding(valid_201901)
    prueba_201902 = apply_negative_coding(prueba_201902)

    feature_cols, train_2018_proc, valid_201901_proc, prueba_201902_proc = impute_median(
        train_2018, [train_2018, valid_201901, prueba_201902]
    )

    X_train_full = train_2018_proc[feature_cols]
    y_train_full = train_2018_proc[TARGET_COL]

    mask_obj_train = train_2018_proc[CLIENT_TYPE_COL] == 'objetivo'
    X_train_obj = X_train_full[mask_obj_train]
    y_train_obj = y_train_full[mask_obj_train]

    mask_obj_valid = valid_201901_proc[CLIENT_TYPE_COL] == 'objetivo'
    X_valid_obj = valid_201901_proc.loc[mask_obj_valid, feature_cols]
    y_valid_obj = valid_201901_proc.loc[mask_obj_valid, TARGET_COL]

    gbm = GradientBoostingClassifier(
        random_state=42,
        n_estimators=220,
        learning_rate=0.05,
        max_depth=3,
        min_samples_leaf=60,
        subsample=0.9,
        max_features='sqrt',
    )
    gbm.fit(X_train_full, y_train_full)

    calib = CalibratedClassifierCV(estimator=gbm, method='isotonic', cv=3)
    calib.fit(X_train_obj, y_train_obj)

    proba_valid_cal = calib.predict_proba(X_valid_obj)[:, 1]

    base_thresholds = np.array([0.01, 0.015, 0.03, 0.045, 0.08, 0.15, 0.30])
    best_thresholds, best_score = search_best_cutpoints(
        y_valid_obj.values, proba_valid_cal, base_thresholds, n_iter=120, seed=42
    )

    X_prueba = prueba_201902_proc[feature_cols]
    pd_cal_prueba = calib.predict_proba(X_prueba)[:, 1]

    prueba_201902_proc['pd_calibrada'] = pd_cal_prueba
    prueba_201902_proc['grupo_riesgo'] = prueba_201902_proc['pd_calibrada'].apply(
        lambda p: assign_risk_group(p, best_thresholds)
    )

    final_df = prueba_201902_proc[[ID_COL, CLIENT_TYPE_COL, 'grupo_riesgo']].copy()
    final_df.to_csv(output_path, index=False)

    return best_thresholds, best_score


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', default='base_train-2.csv')
    parser.add_argument('--valid', default='base_validacion-3.csv')
    parser.add_argument('--prueba', default='base_prueba.csv')
    parser.add_argument('--out', default='salida_grupo_riesgo_201902.csv')
    args = parser.parse_args()
    bt, score = main(args.train, args.valid, args.prueba, args.out)
    print('Best thresholds:', bt)
    print('Best % in range:', score)

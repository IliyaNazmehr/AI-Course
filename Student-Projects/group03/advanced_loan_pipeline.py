"""
Advanced Loan Creditworthiness Training Pipeline
------------------------------------------------
This script trains and evaluates multiple machine learning models for bank-loan
creditworthiness prediction, using leakage-safe preprocessing pipelines.

Run:
    python advanced_loan_pipeline.py --data loan.csv --out models/model.joblib
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import (
    StratifiedKFold,
    train_test_split,
    cross_validate,
    RandomizedSearchCV,
)
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, HistGradientBoostingClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report,
)
from sklearn.calibration import CalibratedClassifierCV
from sklearn.inspection import permutation_importance
import joblib


@dataclass(frozen=True)
class Config:
    target_col: str = "Loan_Status"
    id_col: str = "Loan_ID"
    test_size: float = 0.2
    random_state: int = 42
    cv_splits: int = 5


def load_data(path: str | Path, cfg: Config) -> pd.DataFrame:
    df = pd.read_csv(path)
    if cfg.target_col not in df.columns:
        raise ValueError(f"Target column '{cfg.target_col}' not found in dataset columns: {list(df.columns)}")
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    if "ApplicantIncome" in df.columns and "CoapplicantIncome" in df.columns:
        df["TotalIncome"] = df["ApplicantIncome"].fillna(0) + df["CoapplicantIncome"].fillna(0)
    if "LoanAmount" in df.columns and "TotalIncome" in df.columns:
        denom = df["TotalIncome"].replace(0, np.nan)
        df["LoanAmount_to_Income"] = df["LoanAmount"] / denom
    return df


def split_xy(df: pd.DataFrame, cfg: Config) -> Tuple[pd.DataFrame, pd.Series]:
    df = df.copy()
    if cfg.id_col in df.columns:
        df = df.drop(columns=[cfg.id_col])

    y = df[cfg.target_col].map({"Y": 1, "N": 0})
    if y.isna().any():
        raise ValueError("Target contains values outside {Y, N}. Please normalize labels before training.")

    X = df.drop(columns=[cfg.target_col])
    return X, y


def build_preprocessor(X: pd.DataFrame) -> Tuple[ColumnTransformer, List[str], List[str]]:
    categorical_cols = [c for c in X.columns if X[c].dtype == "object"]
    numeric_cols = [c for c in X.columns if c not in categorical_cols]

    numeric_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_pipe = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipe, numeric_cols),
            ("cat", categorical_pipe, categorical_cols),
        ],
        remainder="drop",
        verbose_feature_names_out=False,
    )
    return preprocessor, numeric_cols, categorical_cols


def get_models(random_state: int) -> Dict[str, object]:
    models: Dict[str, object] = {
        "logreg_balanced": LogisticRegression(max_iter=20000, class_weight="balanced", solver="lbfgs"),
        "random_forest": RandomForestClassifier(
            n_estimators=600,
            random_state=random_state,
            class_weight="balanced_subsample",
            n_jobs=-1,
        ),
        "grad_boosting": GradientBoostingClassifier(random_state=random_state),
        "hist_gbdt": HistGradientBoostingClassifier(random_state=random_state),
    }
    return models


def make_pipeline(preprocessor: ColumnTransformer, model: object) -> Pipeline:
    return Pipeline(steps=[("preprocess", preprocessor), ("model", model)])


def cv_benchmark(
    X: pd.DataFrame,
    y: pd.Series,
    preprocessor: ColumnTransformer,
    models: Dict[str, object],
    cfg: Config,
) -> pd.DataFrame:
    cv = StratifiedKFold(n_splits=cfg.cv_splits, shuffle=True, random_state=cfg.random_state)
    scoring = {
        "accuracy": "accuracy",
        "precision": "precision",
        "recall": "recall",
        "f1": "f1",
        "roc_auc": "roc_auc",
    }

    rows = []
    for name, model in models.items():
        pipe = make_pipeline(preprocessor, model)
        scores = cross_validate(pipe, X, y, cv=cv, scoring=scoring, n_jobs=-1, error_score="raise")
        row = {"model": name}
        for k, v in scores.items():
            if k.startswith("test_"):
                row[k.replace("test_", "")] = float(np.mean(v))
        rows.append(row)

    out = pd.DataFrame(rows).sort_values(by="roc_auc", ascending=False).reset_index(drop=True)
    return out


def tune_logreg(X: pd.DataFrame, y: pd.Series, preprocessor: ColumnTransformer, cfg: Config) -> RandomizedSearchCV:
    pipe = make_pipeline(preprocessor, LogisticRegression(max_iter=20000, class_weight="balanced", solver="lbfgs"))
    param_distributions = {
        "model__C": np.logspace(-3, 3, 80),
    }
    cv = StratifiedKFold(n_splits=cfg.cv_splits, shuffle=True, random_state=cfg.random_state)
    search = RandomizedSearchCV(
        pipe,
        param_distributions=param_distributions,
        n_iter=25,
        scoring="roc_auc",
        cv=cv,
        random_state=cfg.random_state,
        n_jobs=-1,
        verbose=0,
    )
    search.fit(X, y)
    return search


def fit_final_and_report(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    best_estimator: Pipeline,
) -> Dict[str, float]:
    best_estimator.fit(X_train, y_train)

    proba = best_estimator.predict_proba(X_test)[:, 1]
    pred = (proba >= 0.5).astype(int)

    report = {
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred, zero_division=0)),
        "recall": float(recall_score(y_test, pred, zero_division=0)),
        "f1": float(f1_score(y_test, pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, proba)),
    }

    print("\n=== Holdout Evaluation (threshold=0.5) ===")
    print("Confusion Matrix:\n", confusion_matrix(y_test, pred))
    print("\nClassification Report:\n", classification_report(y_test, pred, digits=4))
    print("Metrics:", report)

    return report


def tune_threshold(y_true: np.ndarray, proba: np.ndarray, metric: str = "f1") -> Tuple[float, float]:
    thresholds = np.linspace(0.05, 0.95, 91)
    best_t, best_score = 0.5, -1.0

    for t in thresholds:
        pred = (proba >= t).astype(int)
        if metric == "f1":
            score = f1_score(y_true, pred, zero_division=0)
        elif metric == "recall":
            score = recall_score(y_true, pred, zero_division=0)
        elif metric == "precision":
            score = precision_score(y_true, pred, zero_division=0)
        else:
            raise ValueError("metric must be one of: f1, recall, precision")
        if score > best_score:
            best_t, best_score = float(t), float(score)

    return best_t, best_score


def export_model(model: Pipeline, out_path: str | Path) -> None:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, out_path)
    print(f"\nSaved model to: {out_path.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, default="loan.csv", help="Path to dataset CSV.")
    parser.add_argument("--out", type=str, default="models/loan_model.joblib", help="Output path for saved model.")
    parser.add_argument("--no_tune", action="store_true", help="Skip hyperparameter tuning.")
    parser.add_argument("--calibrate", action="store_true", help="Calibrate probabilities (Platt scaling).")
    parser.add_argument("--threshold_metric", type=str, default="f1", choices=["f1", "precision", "recall"])
    args = parser.parse_args()

    cfg = Config()

    df = load_data(args.data, cfg)
    df = add_features(df)
    X, y = split_xy(df, cfg)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=cfg.test_size, random_state=cfg.random_state, stratify=y
    )

    preprocessor, _, _ = build_preprocessor(X_train)

    models = get_models(cfg.random_state)
    bench = cv_benchmark(X_train, y_train, preprocessor, models, cfg)
    print("\n=== Cross-Validation Benchmark (train split) ===")
    print(bench.to_string(index=False))

    if args.no_tune:
        top_name = str(bench.iloc[0]["model"])
        best_model = make_pipeline(preprocessor, models[top_name])
        best_model.fit(X_train, y_train)
        best_estimator = best_model
        print(f"\nSelected (no-tune): {top_name}")
    else:
        search = tune_logreg(X_train, y_train, preprocessor, cfg)
        best_estimator = search.best_estimator_
        print("\n=== Logistic Regression Tuning (ROC-AUC) ===")
        print("Best params:", search.best_params_)
        print("Best CV ROC-AUC:", search.best_score_)

    if args.calibrate:
        calibrated = CalibratedClassifierCV(best_estimator, method="sigmoid", cv=3)
        calibrated.fit(X_train, y_train)
        final_model = calibrated
        print("\nProbability calibration enabled (sigmoid).")
    else:
        final_model = best_estimator


    final_model.fit(X_train, y_train)
    proba = final_model.predict_proba(X_test)[:, 1]

    best_t, best_s = tune_threshold(y_test.to_numpy(), proba, metric=args.threshold_metric)
    pred_tuned = (proba >= best_t).astype(int)

    print(f"\n=== Threshold Tuning ({args.threshold_metric}) ===")
    print(f"Best threshold: {best_t:.2f} | Best {args.threshold_metric}: {best_s:.4f}")
    print("Confusion Matrix (tuned):\n", confusion_matrix(y_test, pred_tuned))


    print("\nMetrics at tuned threshold:")
    print("accuracy:", accuracy_score(y_test, pred_tuned))
    print("precision:", precision_score(y_test, pred_tuned, zero_division=0))
    print("recall:", recall_score(y_test, pred_tuned, zero_division=0))
    print("f1:", f1_score(y_test, pred_tuned, zero_division=0))
    print("roc_auc:", roc_auc_score(y_test, proba))


    base_for_importance = best_estimator
    base_for_importance.fit(X_train, y_train)

    print("\n=== Permutation Importance (Top 15) ===")

    preprocess = base_for_importance.named_steps["preprocess"]
    model = base_for_importance.named_steps["model"]
    X_test_trans = preprocess.transform(X_test)
    feature_names = preprocess.get_feature_names_out()

    r = permutation_importance(model, X_test_trans, y_test, n_repeats=10, random_state=cfg.random_state, n_jobs=-1)
    imp = pd.DataFrame({"feature": feature_names, "importance_mean": r.importances_mean})
    imp = imp.sort_values("importance_mean", ascending=False).head(15)
    print(imp.to_string(index=False))


    export_model(final_model, args.out)


if __name__ == "__main__":
    main()

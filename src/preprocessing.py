"""Leakage-controlled preprocessing and model pipeline construction."""

from __future__ import annotations

from collections.abc import Sequence

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

NUMERIC_FEATURES = [
    "ENROLL_AGE",
    "baseline_NP3TOT",
    "derived_years_since_PD_diagnosis",
    "part2_NP2PTOT",
    "part1_NP1RTOT",
    "moca_MCATOT",
]

CATEGORICAL_FEATURES = ["baseline_NHY"]


def validate_predictor_columns(
    data: pd.DataFrame,
    *,
    numeric_features: Sequence[str] = NUMERIC_FEATURES,
    categorical_features: Sequence[str] = CATEGORICAL_FEATURES,
) -> None:
    required = set(numeric_features).union(categorical_features)
    missing = sorted(required.difference(data.columns))
    if missing:
        raise KeyError(f"Missing predictor columns: {missing}")


def build_preprocessor(
    *,
    numeric_features: Sequence[str] = NUMERIC_FEATURES,
    categorical_features: Sequence[str] = CATEGORICAL_FEATURES,
) -> ColumnTransformer:
    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("continuous", numeric_transformer, list(numeric_features)),
            ("categorical", categorical_transformer, list(categorical_features)),
        ],
        remainder="drop",
    )


def build_logistic_pipeline(
    *,
    random_state: int = 42,
    c_value: float = 1.0,
    numeric_features: Sequence[str] = NUMERIC_FEATURES,
    categorical_features: Sequence[str] = CATEGORICAL_FEATURES,
) -> Pipeline:
    preprocessor = build_preprocessor(
        numeric_features=numeric_features,
        categorical_features=categorical_features,
    )
    model = LogisticRegression(
        penalty="l2",
        C=float(c_value),
        class_weight="balanced",
        solver="liblinear",
        max_iter=5000,
        random_state=int(random_state),
    )
    return Pipeline([("preprocessor", preprocessor), ("model", model)])

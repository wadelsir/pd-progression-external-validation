"""Model-performance and calibration utilities."""

from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def evaluate_binary_predictions(
    y_true: pd.Series | np.ndarray,
    y_probability: pd.Series | np.ndarray,
    *,
    threshold: float = 0.50,
) -> dict[str, float | int]:
    y_true_array = np.asarray(y_true, dtype=int)
    y_prob_array = np.asarray(y_probability, dtype=float)

    if y_true_array.shape[0] != y_prob_array.shape[0]:
        raise ValueError("y_true and y_probability must have the same length")
    if not np.isfinite(y_prob_array).all():
        raise ValueError("Predicted probabilities contain non-finite values")
    if ((y_prob_array < 0) | (y_prob_array > 1)).any():
        raise ValueError("Predicted probabilities must be between 0 and 1")

    y_pred = (y_prob_array >= float(threshold)).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true_array, y_pred, labels=[0, 1]).ravel()

    return {
        "threshold": float(threshold),
        "ROC_AUC": float(roc_auc_score(y_true_array, y_prob_array)),
        "PR_AUC": float(average_precision_score(y_true_array, y_prob_array)),
        "Brier_score": float(brier_score_loss(y_true_array, y_prob_array)),
        "Accuracy": float(accuracy_score(y_true_array, y_pred)),
        "Balanced_accuracy": float(balanced_accuracy_score(y_true_array, y_pred)),
        "Sensitivity": float(recall_score(y_true_array, y_pred, zero_division=0)),
        "Specificity": float(tn / (tn + fp)) if (tn + fp) else float("nan"),
        "Precision": float(precision_score(y_true_array, y_pred, zero_division=0)),
        "F1": float(f1_score(y_true_array, y_pred, zero_division=0)),
        "TN": int(tn),
        "FP": int(fp),
        "FN": int(fn),
        "TP": int(tp),
    }


def calibration_table(
    y_true: pd.Series | np.ndarray,
    y_probability: pd.Series | np.ndarray,
    *,
    n_bins: int = 8,
) -> pd.DataFrame:
    frame = pd.DataFrame(
        {
            "observed": np.asarray(y_true, dtype=int),
            "predicted_probability": np.asarray(y_probability, dtype=float),
        }
    )
    unique_probabilities = frame["predicted_probability"].nunique()
    bins = max(2, min(int(n_bins), int(unique_probabilities)))
    frame["probability_group"] = pd.qcut(
        frame["predicted_probability"],
        q=bins,
        duplicates="drop",
    )
    table = (
        frame.groupby("probability_group", observed=True)
        .agg(
            n=("observed", "size"),
            mean_predicted_probability=("predicted_probability", "mean"),
            observed_event_rate=("observed", "mean"),
        )
        .reset_index(drop=True)
    )
    return table


def generalization_gap(
    internal_metrics: dict[str, float | int],
    external_metrics: dict[str, float | int],
) -> pd.DataFrame:
    rows = []
    for metric in [
        "ROC_AUC",
        "PR_AUC",
        "Balanced_accuracy",
        "Sensitivity",
        "Specificity",
        "Precision",
        "F1",
        "Brier_score",
    ]:
        internal = float(internal_metrics[metric])
        external = float(external_metrics[metric])
        rows.append(
            {
                "metric": metric,
                "internal": internal,
                "external": external,
                "external_minus_internal": external - internal,
                "absolute_difference": abs(external - internal),
            }
        )
    return pd.DataFrame(rows)

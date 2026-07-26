"""Publication-oriented plotting utilities."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.calibration import calibration_curve
from sklearn.metrics import precision_recall_curve, roc_curve


def _prepare_output_path(output_path: str | Path) -> Path:
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def plot_roc_curve(y_true, y_probability, output_path: str | Path, *, title: str) -> Path:
    false_positive_rate, true_positive_rate, _ = roc_curve(y_true, y_probability)
    path = _prepare_output_path(output_path)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(false_positive_rate, true_positive_rate, label="Model")
    ax.plot([0, 1], [0, 1], linestyle="--", label="Chance")
    ax.set_xlabel("False-positive rate")
    ax.set_ylabel("True-positive rate")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_precision_recall_curve(
    y_true,
    y_probability,
    output_path: str | Path,
    *,
    title: str,
) -> Path:
    precision, recall, _ = precision_recall_curve(y_true, y_probability)
    prevalence = float(np.mean(y_true))
    path = _prepare_output_path(output_path)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(recall, precision, label="Model")
    ax.axhline(prevalence, linestyle="--", label="Outcome prevalence")
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_calibration(
    y_true,
    y_probability,
    output_path: str | Path,
    *,
    title: str,
    n_bins: int = 8,
) -> Path:
    observed, predicted = calibration_curve(
        y_true,
        y_probability,
        n_bins=int(n_bins),
        strategy="quantile",
    )
    path = _prepare_output_path(output_path)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(predicted, observed, marker="o", label="Model")
    ax.plot([0, 1], [0, 1], linestyle="--", label="Ideal")
    ax.set_xlabel("Mean predicted probability")
    ax.set_ylabel("Observed event rate")
    ax.set_title(title)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=300, bbox_inches="tight")
    plt.close(fig)
    return path

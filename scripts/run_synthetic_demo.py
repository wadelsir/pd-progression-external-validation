"""Run the locked-style pipeline on synthetic data only."""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.evaluation import evaluate_binary_predictions
from src.plotting import plot_calibration, plot_precision_recall_curve, plot_roc_curve
from src.preprocessing import CATEGORICAL_FEATURES, NUMERIC_FEATURES, build_logistic_pipeline


def main() -> None:
    data_path = ROOT / "synthetic_data" / "synthetic_example_dataset.csv"
    data = pd.read_csv(data_path)

    development = data[data["cohort"] == "SYNTHETIC_PPMI"].copy()
    external = data[data["cohort"] == "SYNTHETIC_PDBP"].copy()

    features = NUMERIC_FEATURES + CATEGORICAL_FEATURES
    X = development[features]
    y = development["rapid_progression"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        stratify=y,
        random_state=42,
    )

    pipeline = build_logistic_pipeline(random_state=42)
    pipeline.fit(X_train, y_train)

    internal_probability = pipeline.predict_proba(X_test)[:, 1]
    external_probability = pipeline.predict_proba(external[features])[:, 1]

    rows = []
    for cohort, truth, probability in [
        ("Synthetic internal test", y_test, internal_probability),
        ("Synthetic external validation", external["rapid_progression"], external_probability),
    ]:
        for threshold in [0.50, 0.45]:
            metrics = evaluate_binary_predictions(truth, probability, threshold=threshold)
            metrics["cohort"] = cohort
            rows.append(metrics)

    output_table = ROOT / "results" / "aggregate_tables" / "synthetic_demo_metrics.csv"
    output_table.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(output_table, index=False)

    figure_dir = ROOT / "results" / "figures"
    plot_roc_curve(
        external["rapid_progression"],
        external_probability,
        figure_dir / "synthetic_demo_external_roc.png",
        title="Synthetic external-validation ROC curve",
    )
    plot_precision_recall_curve(
        external["rapid_progression"],
        external_probability,
        figure_dir / "synthetic_demo_external_pr.png",
        title="Synthetic external-validation precision–recall curve",
    )
    plot_calibration(
        external["rapid_progression"],
        external_probability,
        figure_dir / "synthetic_demo_external_calibration.png",
        title="Synthetic external-validation calibration",
    )

    print(f"Synthetic demo completed. Metrics: {output_table}")


if __name__ == "__main__":
    main()

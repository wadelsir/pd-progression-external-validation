# Reproducibility guide

## 1. Scope

This guide describes how an authorized researcher can reconstruct the PPMI development cohort, build the locked harmonized model, and reproduce independent PDBP validation. The public repository does not contain controlled participant-level data.

## 2. Obtain authorization

Obtain separate authorization for:

- PPMI/LONI controlled-access data.
- AMP-PD/PDBP controlled-access data.

Comply with all applicable data-use agreements, publication policies, acknowledgement requirements, and restrictions on redistribution.

## 3. Record data provenance

Copy the manifest templates from `config/` to private local files and complete every field:

- exact source filename or BigQuery export;
- dataset-specific version or release;
- download/access date;
- participant and visit identifiers;
- secure local path;
- required variables and transformations.

PPMI versions should be documented at the individual source-table level. The PDBP external-validation data used in this project were obtained through AMP-PD release `amp-pd-research.2023_v4release_1027`.

## 4. Protect controlled data

Store raw and participant-level derived data outside the public repository. Confirm that local paths are covered by `.gitignore`. Do not commit raw tables, participant identifiers, individual predictions, fitted pipelines containing restricted metadata, or notebook outputs containing participant-level rows.

## 5. Create the software environment

Using `pip`:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Using Conda:

```bash
conda env create -f environment.yml
conda activate pd-progression-external-validation
```

Run `python scripts/capture_environment.py` after the final analysis to create a machine-readable environment lock.

## 6. Configure paths

Copy `config/analysis_config_example.yml` to `config/analysis_config_local.yml`. Replace example paths with private secure locations and verify the source-column mappings against `metadata/harmonization_mapping.csv`.

## 7. Execute the notebooks

Add the final notebooks to `notebooks/` and run them in the order specified in `metadata/notebook_execution_order.csv`. Notebooks 01–15 cover data verification, cohort construction, exploratory clinical/multimodal analysis, and manuscript drafting. Notebook 16 constructs and locks the final harmonized PPMI model. Notebook 17 performs prediction-only PDBP validation. Notebook 18 consolidates final reporting outputs.

## 8. Required outcome rules

- Resolve duplicate participant–visit MDS-UPDRS Part III records using the predefined exam-state priority.
- Require valid baseline and V06 outcome records under the prespecified exam-state rules.
- Calculate annualized change using assessment dates and 365.25 days/year when valid dates are available; otherwise use the expected two-year V06 interval.
- Apply the locked rapid-progression threshold of 5.0793 points/year to both cohorts.

## 9. Required predictor rules

Use the seven predictors in the exact order documented in `metadata/harmonization_mapping.csv`. Numeric variables are imputed and standardized using parameters estimated exclusively from the PPMI training subset. Hoehn and Yahr stage is categorical, with training-mode imputation and one-hot encoding. Apply the fitted transformer unchanged to PPMI test and PDBP data.

## 10. External-validation restrictions

PDBP must not be used for:

- model retraining;
- feature reselection;
- preprocessing refitting;
- recalibration;
- hyperparameter tuning;
- threshold optimization.

Use the locked PPMI pipeline to generate PDBP probabilities and report performance at 0.50 and the locked exploratory threshold of 0.45.

## 11. Public synthetic test

Run:

```bash
python scripts/run_synthetic_demo.py
```

This verifies imports, preprocessing, fitting, prediction, metrics, and plotting without accessing controlled data.

## 12. Verification checklist

Before release, confirm that:

- participant identifiers are unique in each analytic dataset;
- the binary outcome contains both classes;
- the final PPMI cohort contains 856 participants and 215 rapid progressors;
- the final PDBP cohort contains 349 participants and 54 rapid progressors;
- predictor names and order match the metadata file;
- no PDBP information influenced model development;
- model and threshold metadata match `metadata/model_metadata.json`;
- participant-level files are absent from Git history;
- exact software versions have been archived;
- the final repository release has a permanent DOI or archived identifier.

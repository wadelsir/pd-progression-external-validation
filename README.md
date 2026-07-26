# PD Progression External Validation

Reproducible code and documentation for the development, internal validation, and independent external validation of a harmonized seven-predictor model for rapid motor progression in Parkinson's disease.

## Study design

- **Development/internal validation cohort:** Parkinson's Progression Markers Initiative (PPMI).
- **Independent external-validation cohort:** Parkinson's Disease Biomarkers Program (PDBP), accessed through AMP-PD.
- **Outcome:** annualized change in MDS-UPDRS Part III from baseline to V06.
- **Rapid-progression threshold:** at least **5.0793 points/year**, derived from the upper quartile in PPMI and locked before PDBP validation.
- **Final predictors:** baseline age, baseline MDS-UPDRS Part III, years since Parkinson's disease diagnosis, MDS-UPDRS Part II, MDS-UPDRS Part I, MoCA total score, and Hoehn and Yahr stage.
- **Selected algorithm:** class-weighted L2-regularized logistic regression.

## Repository status

This repository contains reusable source code, configuration templates, data manifests, metadata, synthetic data, and reproducibility documentation. Controlled participant-level PPMI and PDBP data are **not included** and must never be committed to a public repository.

The final executed notebooks should be copied into `notebooks/` using the names listed in `metadata/notebook_execution_order.csv`. A `notebooks/README.md` file explains the expected naming convention.

## Quick start with synthetic data

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python scripts/run_synthetic_demo.py
```

The demo writes aggregate metrics to `results/aggregate_tables/` and figures to `results/figures/`. Synthetic outputs are for pipeline testing only and do not reproduce the manuscript results.

## Controlled-data reconstruction

1. Obtain independent authorization for PPMI and AMP-PD/PDBP.
2. Complete the manifest templates in `config/` with exact filenames, versions, and download dates.
3. Place controlled data outside the repository, preferably under a protected project directory.
4. Copy the final executed notebooks into `notebooks/`.
5. Update `config/analysis_config_example.yml` or create a private local configuration file.
6. Execute notebooks in the order specified in `metadata/notebook_execution_order.csv`.
7. Capture the software environment using `python scripts/capture_environment.py`.

Detailed instructions are provided in `docs/reproducibility_guide.md` and `docs/data_access_instructions.md`.

## Reproducibility safeguards

- Random seed fixed at 42.
- Stratified training/test split.
- Preprocessing fitted only on the PPMI training subset.
- PDBP used for prediction and evaluation only.
- No external retraining, feature reselection, preprocessing refitting, recalibration, hyperparameter tuning, or threshold optimization.

## Repository structure

```text
pd-progression-external-validation/
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
├── environment.yml
├── notebooks/
├── src/
├── scripts/
├── config/
├── metadata/
├── synthetic_data/
├── results/
└── docs/
```

## Data availability

PPMI and PDBP participant-level data are controlled-access resources and are not redistributed here. Authorized researchers must obtain the original datasets independently and reconstruct the analytic cohorts using the provided manifests, mapping files, configuration, source code, and notebook workflow.

## Citation

Use the citation metadata in `CITATION.cff`. Update the author list, repository URL, and release identifier before public release.

## License

Code and documentation are released under the MIT License. This license does not apply to PPMI, PDBP, AMP-PD, or any third-party controlled-access data.

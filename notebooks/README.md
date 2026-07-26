# Analysis notebooks

"
    "This directory contains the final public-release notebooks for the Parkinson's disease motor-progression project. "
    "The workflow consists of Notebooks 01–18, with Notebook 07b retained as an additional DaTSCAN screening-feature verification step.

"
    "## Public-release preparation

"
    "- All notebooks were validated as Jupyter Notebook format version 4.
"
    "- Stored cell outputs and execution counts were removed to prevent redistribution of controlled participant-level information.
"
    "- No raw PPMI or PDBP participant-level data are included.
"
    "- The analytical code and markdown were preserved; only transient execution metadata was normalized.
"
    "- The notebooks retain the original Google Colab/Google Drive project-directory conventions used during analysis. Authorized users should update paths through the provided configuration and manifest templates before reconstruction.

"
    "Execute the notebooks in the order specified in `../metadata/notebook_execution_order.csv`. "
    "Notebook release hashes and source-name mappings are recorded in `../metadata/notebook_release_inventory.csv`.
",
    encoding='utf-8',
)

# Release inventory
inventory_path = REPO / 'metadata' / 'notebook_release_inventory.csv'
with inventory_path.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(inventory[0].keys()))
    writer.writeheader()
    writer.writerows(inventory)

# Update README status and reconstruction steps.
readme_path = REPO / 'README.md'
readme = readme_path.read_text(encoding='utf-8')
readme = readme.replace(
    "This repository contains reusable source code, configuration templates, data manifests, metadata, synthetic data, and reproducibility documentation. Controlled participant-level PPMI and PDBP data are **not included** and must never be committed to a public repository.

The final executed notebooks should be copied into `notebooks/` using the names listed in `metadata/notebook_execution_order.csv`. A `notebooks/README.md` file explains the expected naming convention.",
    "This repository contains the final public-release analysis notebooks, reusable source code, configuration templates, data manifests, metadata, synthetic data, and reproducibility documentation. Controlled participant-level PPMI and PDBP data are **not included** and must never be committed to a public repository.

The `notebooks/` directory includes Notebooks 01–18 plus the supplemental Notebook 07b. Stored notebook outputs and execution counts were removed before release, while analytical code and markdown were preserved."
)
readme = readme.replace(
    "4. Copy the final executed notebooks into `notebooks/`.
5. Update `config/analysis_config_example.yml` or create a private local configuration file.
6. Execute notebooks in the order specified in `metadata/notebook_execution_order.csv`.
7. Capture the software environment using `python scripts/capture_environment.py`.",
    "4. Update `config/analysis_config_example.yml` or create a private local configuration file.
5. Execute notebooks in the order specified in `metadata/notebook_execution_order.csv`.
6. Capture the software environment using `python scripts/capture_environment.py`."
)
readme = readme.replace(
    "├── notebooks/
",
    "├── notebooks/                 # Notebooks 01–18 plus 07b
"
)
readme_path.write_text(readme, encoding='utf-8')

# Add release notes.
(REPO / 'RELEASE_NOTES.md').write_text(
    ## Notebook package

This release adds the verified final project notebooks to the repository scaffold. It contains 18 primary numbered notebooks (01–18) and one supplemental verification notebook (07b).

For public sharing, stored outputs, execution counts, widget state, and transient execution metadata were removed. Notebook code and markdown content were otherwise preserved. The notebooks were structurally validated with `nbformat`.

## Data protection

No raw or derived participant-level PPMI or PDBP data are included. Users must obtain controlled-access data independently and comply with the applicable PPMI and AMP-PD/PDBP data-use agreements.

## Reproducibility scope

The repository provides the notebook workflow, source modules, configuration templates, manifests, harmonization metadata, synthetic demonstration data, and supplementary documentation. Exact reconstruction of manuscript results requires authorized access to the source cohorts and completion of the local manifest/configuration files.

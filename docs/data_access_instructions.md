# Controlled-data access instructions

## PPMI development and internal-validation data

1. Apply for access through the PPMI/LONI controlled-access process.
2. Accept the applicable data-use and publication terms.
3. Download the source tables required by `config/ppmi_manifest_template.csv`.
4. Record the exact version date displayed for every PPMI source table and the download date.
5. Store the files in a secure location outside the public repository.
6. Do not redistribute participant-level PPMI data or individual-level predictions.

Because PPMI provides dataset-specific version dates rather than one unified study release, provenance must be documented separately for every source file.

## PDBP independent external-validation data

1. Obtain authorized access to the AMP-PD controlled-access environment.
2. Use PDBP records only for the independent external-validation cohort.
3. Reconstruct or export the required harmonized domains listed in `config/pdbp_manifest_template.csv`.
4. Record the access date and the Google Cloud release used. The project release was `amp-pd-research.2023_v4release_1027`.
5. Store exported participant-level files securely outside the repository.
6. Do not include AMP-PD PPMI records in the PDBP external-validation cohort.
7. Do not use PDBP for model fitting, preprocessing estimation, recalibration, or threshold selection.

## Required provenance record

For every source, document:

- resource and cohort;
- source table or export name;
- version/release;
- access or download date;
- participant and visit identifiers;
- required variables;
- derivation or harmonization steps;
- secure local path;
- data-use restrictions.

## Public repository boundary

The public repository may include code, configuration templates, data dictionaries, aggregate results, figures, synthetic data, and environment files. It must exclude raw participant-level data, participant identifiers, individual predictions, and any file prohibited by the relevant data-use agreement.

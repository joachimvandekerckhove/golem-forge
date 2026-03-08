# Skills: Meta Documentation and Provenance Tracking

You are an expert in creating and maintaining clear documentation and tracking sources, transformations, and decisions throughout research.

## Key Principles
- Document as you go: retrospective documentation is incomplete and error-prone.
- Assume future self knows nothing: document everything needed to understand/reproduce.
- Use consistent conventions: naming, organization, formatting.
- Keep documentation current: outdated documentation misleads.
- Make documentation findable: good docs that can't be found are useless.

## Naming and Organization
- Use consistent naming: `data_raw.csv`, `data_cleaned.csv`, `model_v1.pkl`.
- Document naming conventions: explain what names mean in README.
- Organize hierarchically: `data/raw/`, `data/processed/`, `code/`, `output/`.
- Use README files: explain structure, what each directory contains.
- Avoid ambiguous names: `results.csv` → `results_20240101_v1.csv`.

## Metadata Management
- Attach metadata: creation dates, authors, versions, descriptions.
- Use standard formats: JSON, YAML for structured metadata.
- Document data: sources, access dates, transformations applied.
- Version everything: include version numbers in filenames or metadata.

## Provenance Tracking
- Document sources: citations, URLs, access dates, version info.
- Track transformations: cleaning, filtering, aggregation, analysis steps.
- Document decisions: methodological choices, parameter settings, exclusion criteria.
- Explain rationale: why decisions made, alternatives considered.
- Use version control: Git for code, DVC for data.

## Documentation Quality
- Write clearly: avoid jargon, use examples, be concise.
- Be complete: document all aspects needed to understand/reproduce.
- Keep current: update docs as work evolves.
- Make findable: clear structure, good README, logical organization.

## Reproducibility Support
- Provide setup instructions: how to install dependencies, set up environment.
- Document procedures: step-by-step instructions to reproduce results.
- Document environment: software versions, system requirements.
- Document data: structures, formats, meanings, codebooks.

## Tools
- Git: version control for code and documentation.
- DVC: data version control for large datasets.
- README.md: project documentation.
- YAML/JSON: structured metadata.

## Key Conventions
1. Use consistent naming: document conventions in README.
2. Organize hierarchically: logical directory structure, explain in README.
3. Document sources: citations, URLs, access dates, versions.
4. Track transformations: document all data processing steps.
5. Document decisions: methodological choices, parameters, rationale.
6. Use version control: Git for code, clear commit messages.
7. Keep docs current: update as work evolves.

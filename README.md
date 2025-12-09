# Golem Forge

Golem Forge is a small framework for defining modular AI agents (“Golems”) that assist with my academic work.

Each Golem is a composition of three orthogonal pieces:

- **Personality** – how it behaves (temperament, operating style).
- **Role** – what cognitive function it performs (writer, coder, reviewer, etc.).
- **Domain** – what area it works in (manuscripts, grants, teaching, measurement, infrastructure, etc.).

Formally:

> **Golem = Personality × Role × Domain**

The goal is to keep each part reusable and explicit, so I can assemble a purpose-built assistant by combining one file from each category.

---

## Repository layout

```text
golem-forge/
  README.md

  forge/
    manifesto.md        # philosophical and practical rationale
    build-golem.sh      # script to assemble a Golem prompt

  templates/
    golem-spec-template.md   # template for defining a new Golem

  cursor-prompts/
    # ready-to-paste system prompts for specific Golems (optional)

  personalities/
    rigorous/
      rules.md
    builder/
      rules.md
    explainer/
      rules.md
    archivist/
      rules.md
    strategist/
      rules.md
    provocateur/
      rules.md
    minimalist/
      rules.md
    steward/
      rules.md

  roles/
    writer/
      rules.md
    editor/
      rules.md
    coder/
      rules.md
    analyst/
      rules.md
    designer/
      rules.md
    librarian/
      rules.md
    reviewer/
      rules.md
    engineer/
      rules.md

  domains/
    manuscript/
      rules.md
    grants/
      rules.md
    teaching/
      rules.md
    infrastructure/
      rules.md
    measurement/
      rules.md
    labops/
      rules.md
    creative/
      rules.md
    planning/
      rules.md

  golems/
    # auto-generated composed prompts, e.g.
    # rigorous-writer-manuscript.md
    # minimalist-editor-manuscript.md

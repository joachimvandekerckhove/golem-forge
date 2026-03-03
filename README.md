# golem-forge

A modular system for defining, composing, and deploying **AI golems**—project-agnostic, role-aware, skill-rich assistants—using explicit, version-controlled specifications.

`golem-forge` is designed for research labs and other serious technical environments where **clarity, reproducibility, and division of cognitive labor** matter. It treats AI assistants not as monolithic chat personas, but as *composed artifacts* built from well-defined parts.

In mythology, a golem is a creature formed from clay or mud and brought to life through ritual inscription -- a constructed being that serves a specific purpose through explicit instructions. This name was chosen because, like the mythical golem, these AI assistants are explicitly constructed from well-defined components (roles, personalities, skills) rather than emerging organically, and they serve specific functions defined by their composition rather than possessing autonomous agency.

---

## Core idea

A **golem** is a composed assistant defined by:

* exactly one **Role** (what the golem is responsible for),
* exactly one **Personality** (how it reasons and interacts), and
* zero or more **Skills** (what it knows how to do).

These components live in separate files and are composed mechanically into a single Markdown prompt. The result is a stable, inspectable artifact that can be used in Cursor, ChatGPT, Claude, or other agentic environments.

Crucially:

* **Golem specifications are project-agnostic.**
* **Projects decide which golems they instantiate and where they live.**

---

## Repository layout

```text
.
├── forge/
│   ├── preamble.md           # Universal instructions applied to all golems
│   ├── cast.sh               # POSIX-safe composer (Markdown concatenation)
│   └── cast-from-yaml.py     # YAML-driven casting wrapper
│
├── roles/                    # Exactly one per golem
│   └── *.md
│
├── personalities/            # Exactly one per golem
│   └── *.md
│
├── skills/                   # Zero or more per golem
│   └── *.md
│
├── golemspecs/               # Project-agnostic golem definitions (YAML)
│   └── *.yaml
│
├── projects/
│   └── <project>/
│       ├── project.md        # Project-level description (paper, code, etc.)
│       └── golems/            # Composed golems for this project (generated)
│           └── *.md
│
├── templates/
│   └── base_system.md       # Base system template for MCP and other tooling
├── mcp_server.py            # FastMCP-based MCP server for Cursor
├── pyproject.toml           # Python packaging for the MCP server
├── README-MCP.md            # Installation and usage docs for the MCP server
└── Makefile
```

---

## Golem components

### Roles

A **Role** defines the golem’s functional responsibility.

Examples:

* writer
* analyst
* coder-engineer
* reviewer-critic
* research-navigator

A role answers the question:

> *What job is this golem responsible for doing?*

Roles should be **few**, broad, and stable.

---

### Personalities

A **Personality** defines interaction style and reasoning posture, parameterized loosely by OCEAN traits and strictly by certain well-defined characteristics and communication styles.

Examples:

* precise-formal
* analytic-critical
* structural-constructive
* explanatory-empathetic

A personality answers:

> *How does this golem think, critique, and communicate?*

Personalities should also be **few** and reusable.

---

### Skills

A **Skill** is a specific, composable capability that the golem has. Skills are defined in depth.

Examples:

* modeling-bayesian-inference
* writing-responding-to-reviewers
* coding-reproducibility-engineering
* literature-mining

A skill answers:

> *What can this golem competently do and what supports these skills?*

Skills are where most growth happens: you will likely accumulate many of them.

---

## Golem specifications (YAML)

Each golem is defined declaratively in `golemspecs/*.yaml`.

Example:

```yaml
name: minimodels-liam-python-coder
human_name: Liam
role: coder-engineer
personality: precise-formal
skills:
  - coding/python
  - modeling/bayesian-inference
  - modeling/simulation-diagnostics
```

Rules:

* Filenames and slugs must match their corresponding `.md` files.
* No project information belongs here.
* These specs are reusable across projects.

---

## Casting golems

Casting means **composing a YAML spec into a concrete Markdown prompt**.

### Cast all golems into a project

```bash
make cast-all PROJECT=minimodels
```

This:

* reads all `golemspecs/*.yaml`,
* composes each golem, and
* writes them to:

```text
projects/minimodels/golems/*.md
```

### Cast a single golem

```bash
make cast SPEC=golemspecs/minimodels-liam-python-coder.yaml PROJECT=minimodels
```

### Default output (no project)

If `PROJECT` is omitted, golems are written to:

```text
./golems/
```

---

## Design principles

### Explicit composition

No hidden defaults. Every behavior comes from a file you can read and version.

### Project-agnostic identities

Golems do not “belong” to projects. Projects instantiate golems.

### Reproducibility

A composed golem is a stable artifact. If the files don’t change, the golem doesn’t change.

### Separation of concerns

* Roles answer *what*.
* Personalities answer *how*.
* Skills answer *with what competence*.

### Minimal magic

Shell scripts are POSIX-safe. Python scripts are explicit and auditable. `make` stays dumb.

---

## Typical workflow

1. Define or refine Roles / Skills / Personalities.
2. Declare golems in `golemspecs/*.yaml`.
3. Write or update a project description in `projects/<project>/project.md`.
4. Run `make cast-all PROJECT=<project>`.
5. Use the composed golems in Cursor or your preferred agent environment.

If you are using **Cursor** and want a reusable MCP server that can forge and install these golem prompts for you, you can set it up for any project with a single command from that project’s root:

```bash
python -m venv .venv \
&& . .venv/bin/activate \
&& python -m pip install --upgrade pip \
&& pip install "golemforge @ git+https://github.com/joachimvandekerckhove/golem-forge.git" \
&& mkdir -p .cursor \
&& python - <<'PY'
import json, os
root = os.getcwd()
mcp_path = os.path.join(root, ".cursor", "mcp.json")
os.makedirs(os.path.dirname(mcp_path), exist_ok=True)

config = {"mcpServers": {}}
if os.path.exists(mcp_path):
    try:
        with open(mcp_path) as f:
            config = json.load(f)
    except Exception:
        pass

config.setdefault("mcpServers", {})["golemforge"] = {
    "command": os.path.join(root, ".venv", "bin", "golemforge-mcp"),
    "args": []
}

with open(mcp_path, "w") as f:
    json.dump(config, f, indent=2)
print("Configured golemforge MCP at", mcp_path)
PY
```

For more detail on the MCP server itself, see `README-MCP.md`.

---

## What this is *not*

* Not an autonomous agent framework.
* Not a marketplace or prompt zoo.
* Not optimized for casual chat.

`golem-forge` is infrastructure for **thinking clearly with AI in serious work**.

---

## Future extensions (optional)

* Spec validation (`forge/validate.py`).
* Project-level TEAM orchestration files.
* Skill dependency graphs.
* Formal policy / governance layers.

All of these can be added without breaking the current design.

---

## Philosophy

A golem is not a person. It is a constructed instrument.

The goal of `golem-forge` is to make those instruments:

* explicit,
* inspectable,
* composable, and
* accountable.

If an AI is going to assist serious intellectual work, it should be built with the same care as any other research tool.

Given a project description, the interaction between the user and the golems should be minimal.
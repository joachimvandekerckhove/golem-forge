# golem-forge

`golem-forge` is an MCP server for Cursor that assembles AI assistant "golems" from composable plain-text files — **roles**, **personalities**, and **skills** — into a single system prompt.

In Terry Pratchett's Discworld, golems are clay workers animated by a written scroll. Changing the scroll changes who they are. The markdown files in `golemforge/roles/`, `golemforge/personalities/`, and `golemforge/skills/` play the same role here.

---

## Install into a Cursor project

From any Cursor project terminal — no local clone required:

```bash
uvx --from "git+https://github.com/joachimvandekerckhove/golem-forge.git" golemforge-install-cursor
```

Requires [`uv`](https://docs.astral.sh/uv/). If not installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

After the command finishes, reload the Cursor window (Ctrl+Shift+P → **Reload Window**) to activate the server.

The install command does three things:
1. Downloads the package from GitHub and runs the installer — no virtual environment needed in the target project.
2. Creates or updates `.cursor/mcp.json` with a `"golemforge"` entry that launches the server via `uvx`.
3. Creates `.cursor/rules/golem-constitution.mdc` so that `cast_and_install` works immediately.

> `installation-prompt.md` in this repo contains the same instructions in a form you can paste directly into a Cursor chat window, for AI-assisted installation.

---

## Concepts

- **Roles** — what the assistant is responsible for (e.g. `writer`, `analyst`, `reviewer`). Defined in `golemforge/roles/*.md`.
- **Personalities** — how the assistant communicates (e.g. `precise-formal`, `explanatory-empathetic`). Defined in `golemforge/personalities/*.md`.
- **Skills** — concrete capabilities or procedures (e.g. `coding/python`, `modeling/bayesian-inference`). Defined in `golemforge/skills/**/*.md`.

Any combination of skills, with an optional role and personality, can be forged into a single composed system prompt.

---

## Repository layout

```text
.
├── golemforge/               # Installable Python package
│   ├── __init__.py           # MCP server (FastMCP)
│   ├── roles/                # Role markdown files
│   ├── personalities/        # Personality markdown files
│   ├── skills/               # Skill markdown files
│   ├── templates/
│   │   └── base_system.md    # Base system prompt template
│   └── names.json            # Pool of golem persona names
├── tests/                    # Direct and STDIO transport tests
├── pyproject.toml            # Package definition
├── installation-prompt.md    # Paste into a Cursor chat to install
└── README.md
```

---

## MCP tools

| Tool | Description |
|---|---|
| `list_skills()` | List available skill IDs |
| `list_roles()` | List available role IDs |
| `list_personalities()` | List available personality IDs |
| `cast(skills, ...)` | Forge a full prompt package with provenance |
| `cast_pasteblock(skills, ...)` | Forge only the paste-ready block |
| `cast_and_install(skills, ...)` | Forge and write to `.cursor/golem-system.md` |
| `explain_cast(skills)` | Dry-run preview: files, sizes, missing skills |

All casting tools accept `skills` (list of IDs), `extra_instructions` (string), `role` (optional ID), and `personality` (optional ID).

`cast_and_install` writes the compiled prompt to `.cursor/golem-system.md` in the current Cursor project. The constitution rule installed by `golemforge-install-cursor` tells Cursor to apply that file as the system prompt for every new chat in the project.

---

## Development

Clone the repo, create a virtual environment, and install in editable mode:

```bash
git clone https://github.com/joachimvandekerckhove/golem-forge.git
cd golem-forge
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

Run tests:

```bash
python tests/test_mcp_server.py
python tests/test_mcp_stdio.py
```

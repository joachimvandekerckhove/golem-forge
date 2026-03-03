# golem-forge

`golem-forge` is a small set of files for describing AI "golems" as **roles**, **personalities**, and **skills**, plus an MCP server so Cursor can assemble prompts from those markdown files.

The aim is practical: keep the pieces that define an assistant in plain text, under version control, and easy to inspect.

In Terry Pratchett's Discworld books, golems are clay workers animated by a written scroll in their head. Changing the words on that scroll changes who they are and what they care about. This repository plays a similar role for AI helpers: the markdown files in `roles/`, `personalities/`, and `skills/` are the "scroll", and the MCP server simply reads and stitches them together.

---

## Concepts

- **Roles**: describe what the assistant is responsible for (for example: writer, analyst, reviewer). Role definitions live in `roles/*.md`.
- **Personalities**: describe how the assistant communicates and reasons (for example: precise-formal, explanatory-empathetic). These live in `personalities/*.md`.
- **Skills**: describe concrete capabilities or procedures (for example: `coding/python`, `modeling/bayesian-inference`). These live in `skills/*.md`.

The MCP server can include any combination of skills, and optionally a role and personality, into a single composed system prompt. Users should edit or add skills, roles, and personalities to the `skills/`, `roles/`, and `personalities/` directories to match their own needs and preferences.

---

## Repository layout

```text
.
├── roles/                    # Role markdown files (optional in MCP casts)
├── personalities/            # Personality markdown files (optional in MCP casts)
├── skills/                   # Skill markdown files used by the MCP server
├── templates/
│   └── base_system.md        # Base system template for composed prompts
├── mcp_server.py             # FastMCP-based MCP server entrypoint
├── pyproject.toml            # Python packaging for the MCP server
├── names.json                # Deterministic list of golem names
├── tests/                    # MCP server tests (direct + STDIO transport)
├── README.md                 # This file: overview and reference
└── installation-prompt.md    # Paste-ready prompt for AI-driven installation
```

---

## Installation and Cursor setup

From a clean environment with Python >= 3.10, in your Cursor project:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "golemforge @ git+https://github.com/joachimvandekerckhove/golem-forge.git"
golemforge-install-cursor
```

This installs the MCP server into `.venv` and creates or updates `.cursor/mcp.json` so Cursor can discover the `golemforge` MCP server.

If you only want a library-style install (no project wiring), you can stop after the `pip install` step. The `golemforge-mcp` executable will still be available in the virtual environment.

To run the server manually (for testing or use with another MCP client):

```bash
golemforge-mcp
```

---

## MCP tools

All tools live under the `golemforge` MCP server.

- **`list_skills()`**: returns available skill IDs from `skills/*.md`.
- **`list_roles()`**: returns available role IDs from `roles/*.md`.
- **`list_personalities()`**: returns available personality IDs from `personalities/*.md`.

- **`cast(skills, extra_instructions="", role=None, personality=None)`**  
  Builds a full prompt package:
  - includes the base template, selected skills, and optional role and personality;
  - returns `golem_name`, `compiled_prompt`, `paste_block`, `skill_hashes`, and a small manifest (including optional `role`, `role_hash`, `personality`, `personality_hash`).

- **`cast_pasteblock(skills, extra_instructions="", role=None, personality=None)`**  
  Lighter version of `cast` that returns only `golem_name` and `paste_block`.

- **`cast_and_install(skills, extra_instructions="", role=None, personality=None)`**  
  Like `cast`, but also writes the compiled system prompt to `.cursor/golem-system.md` in the current project so that Cursor can treat it as a persistent "constitution" (assuming the project includes the `.cursor/rules/golem-constitution.mdc` rule file).

- **`explain_cast(skills)`**  
  Shows which files would be included, which skills are missing, and an approximate character-count for the resulting prompt.

When a requested skill, role, or personality is missing, the tools return a small error payload with a short code (for example, `missing_skills`, `missing_role`, `missing_personality`) and a suggestion about which listing tool to call.

---

## Self-checks

If you are working from a local clone of this repository, you can run a few quick checks:

```bash
python -m py_compile mcp_server.py
python tests/test_mcp_server.py
```

The test script exercises the main tools directly and prints a short summary.
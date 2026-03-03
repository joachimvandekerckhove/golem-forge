# golemforge MCP Server

`golemforge` is a local Cursor-compatible MCP server that forges a reusable system prompt from a base template plus selected local skill markdown files.

## Features

- MCP over **STDIO** for Cursor integration.
- Tools:
  - `list_skills()`
  - `cast(skills, extra_instructions="")`
  - `cast_pasteblock(skills, extra_instructions="")`
  - `cast_and_install(skills, extra_instructions="")` — cast and write constitution to `.cursor/golem-system.md`
  - `explain_cast(skills)`
- Deterministic skill listing and manifest normalization.
- Provenance hashes for included skills + compiled prompt.
- Prompt truncation safety if output exceeds 100k characters.

## Project layout (top level)

```text
.
├── mcp_server.py       # MCP server entrypoint (FastMCP)
├── pyproject.toml      # Python package metadata (name: "golemforge")
├── names.json          # Deterministic skill naming
├── templates/
│   └── base_system.md  # Base system prompt template
├── skills/             # Local skill markdown files (optional)
├── README.md           # Core golem-forge spec system
└── README-MCP.md       # This file: MCP server docs
```

The MCP server is packaged as a **single-module project** (`mcp_server.py`) with a console script entrypoint `golemforge-mcp`.

## Installation

### Simple Python install (no Cursor wiring)

From a clean environment with Python ≥ 3.10:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install "golemforge @ git+https://github.com/joachimvandekerckhove/golem-forge.git"
```

This exposes a `golemforge-mcp` executable in your virtual environment.

### One-shot project setup for Cursor

To set up `golemforge` as a **project-scoped MCP server for Cursor** from an existing environment, run this from the root of your Cursor project (not necessarily this repo):

```bash
golemforge-install-cursor
```

After this, open the project in Cursor; it will detect the `golemforge` MCP server automatically.

## Running locally (STDIO)

If you want to run the server manually (for testing, or outside Cursor), use:

```bash
golemforge-mcp
```

This starts the MCP server in STDIO mode for a host client (such as Cursor).

## Cursor setup

Create/update `.cursor/mcp.json` in your project (or global Cursor MCP config) with a `command` + `args` entry. Cursor can also configure MCP servers via Settings UI. The one-shot script above does this automatically, but you can also edit it manually:

```json
{
  "mcpServers": {
    "golemforge": {
      "command": "<ABSOLUTE_OR_PROJECT_LOCAL_PATH_TO>/golemforge-mcp",
      "args": []
    }
  }
}
```

> Note: You can keep this config in project `.cursor/mcp.json` for repo-scoped behavior, or in Cursor global settings for all workspaces.

## Tool behavior

### `list_skills()`
Lists skill IDs from markdown files under `golemforge/skills/*.md` and `golemforge/skills/*/*.md`, ignoring dotfiles and non-markdown files.

### `cast(skills, extra_instructions="")`
Returns:

- `golem_name`
- `invocation_id`
- `skills_requested`
- `skills_included`
- `skill_hashes`
- `compiled_prompt`
- `paste_block`
- `character_count`
- `compiled_prompt_sha256`
- `forge_version`
- optional `warning` when truncated

If requested skills are missing, returns structured error details with suggested next action (`list_skills`).

### `cast_pasteblock(skills, extra_instructions="")`
Returns only `golem_name` and `paste_block`.

### `cast_and_install(skills, extra_instructions="")`
Same as `cast`, but also writes the compiled system prompt to `.cursor/golem-system.md`. The project rule `.cursor/rules/golem-constitution.mdc` (always applied) tells Cursor to read that file and use it as the system prompt for every new chat. Use this to make the cast golem your **persistent constitution**: it survives context limits and chat restarts. Response includes `installed_path` and `installed: true` on success, or `install_error` if the write failed.

### `explain_cast(skills)`
Shows which files would be included and estimated total character count.

## Example usage in Cursor

1. Ask Cursor to call `list_skills`.
2. Call `cast` with selected skill IDs and optional extra instructions.
3. Paste the returned `paste_block` into a new chat if not auto-inserted.

## Persistent golem (constitution)

To use the generated prompt as the **system prompt for every new chat** in this project (so you don’t lose the golem when context runs out):

1. Use **`cast_and_install`** instead of `cast`, e.g. *“Cast and install a golem with skills: writing/academic-structuring, writing/narrative-clarity, …”*
2. The tool writes the compiled prompt to `.cursor/golem-system.md`.
3. The rule in `.cursor/rules/golem-constitution.mdc` is always applied and instructs the AI to read that file and treat it as the system prompt when present.
4. New chats (and new conversations) in this workspace will then load the golem automatically. To change the active golem, run `cast_and_install` again with different skills; to clear it, delete `.cursor/golem-system.md`.

`.cursor/golem-system.md` is in `.gitignore` by default so the active golem stays local; you can force-add it if you want to share a default golem with the repo.

## Self-test

### 1) Quick syntax check

If you are working from a local clone of this repository, you can sanity-check the module with:

```bash
python -m py_compile mcp_server.py
```

### 2) Smoke-run server

From the same clone (with dependencies installed):

```bash
golemforge-mcp
```

Use an MCP client (Cursor or compatible inspector) to call:

- `list_skills`
- `cast` with sample skills (after you add skill files)

### 3) Minimal JSON-RPC style probe (example)

If you have an MCP inspector/runner installed, start the server with `golemforge-mcp` and then call tools interactively from the inspector UI. (Transport is STDIO.)

## Notes

- The server resolves paths relative to `mcp_server.py`, so it works regardless of current working directory.
- Cursor cannot always create a new chat automatically from a tool result; if not, manually paste the `paste_block` into a new chat.

# golemforge MCP Server

`golemforge` is a local Cursor-compatible MCP server that forges a reusable system prompt from a base template plus selected local skill markdown files.

## Features

- MCP over **STDIO** for Cursor integration.
- Tools:
  - `list_skills()`
  - `cast(skills, extra_instructions="")`
  - `cast_pasteblock(skills, extra_instructions="")`
  - `explain_cast(skills)`
- Deterministic skill listing and manifest normalization.
- Provenance hashes for included skills + compiled prompt.
- Prompt truncation safety if output exceeds 100k characters.

## Project layout

```text
golemforge/
  mcp_server.py
  names.json
  templates/
    base_system.md
  skills/
    .gitkeep
  README.md
  pyproject.toml
  .gitignore
```

## Installation

From repository root:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ./golemforge
```

Or install dependencies only:

```bash
pip install fastmcp
```

## Running locally (STDIO)

From repository root:

```bash
python golemforge/mcp_server.py
```

This starts the MCP server in STDIO mode for a host client (such as Cursor).

## Cursor setup

Create/update `.cursor/mcp.json` in your project (or global Cursor MCP config) with a `command` + `args` entry. Cursor can also configure MCP servers via Settings UI.

Example project-level config:

```json
{
  "mcpServers": {
    "golemforge": {
      "command": "python",
      "args": ["golemforge/mcp_server.py"]
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

### `explain_cast(skills)`
Shows which files would be included and estimated total character count.

## Example usage in Cursor

1. Ask Cursor to call `list_skills`.
2. Call `cast` with selected skill IDs and optional extra instructions.
3. Paste the returned `paste_block` into a new chat if not auto-inserted.

## Self-test

### 1) Quick syntax check

```bash
python -m py_compile golemforge/mcp_server.py
```

### 2) Smoke-run server

```bash
python golemforge/mcp_server.py
```

Use an MCP client (Cursor or compatible inspector) to call:

- `list_skills`
- `cast` with sample skills (after you add skill files)

### 3) Minimal JSON-RPC style probe (example)

If you have an MCP inspector/runner installed, start server with:

```bash
python golemforge/mcp_server.py
```

Then call tools interactively from the inspector UI. (Transport is STDIO.)

## Notes

- The server resolves paths relative to `mcp_server.py`, so it works regardless of current working directory.
- Cursor cannot always create a new chat automatically from a tool result; if not, manually paste the `paste_block` into a new chat.

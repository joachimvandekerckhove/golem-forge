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

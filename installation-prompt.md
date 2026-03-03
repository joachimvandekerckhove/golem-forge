You are an AI assistant helping me install the **golemforge MCP server** into a Cursor project so that Cursor can use it as an MCP provider.

Your job is to:

1. **Set up a Python virtual environment** in the project.
2. **Install the `golemforge` package** from GitHub into that environment.
3. **Register the MCP server in `.cursor/mcp.json`** for this project so Cursor can discover it.
4. **Install the constitution rule** so that the `cast_and_install` MCP tool works: when it writes `.cursor/golem-system.md`, Cursor will treat that file as the system prompt for new chats.

The goal is that **all golemforge MCP tools work** after installation, including `cast_and_install` (which writes the "constitution" file). The constitution rule is what makes that file take effect.

Follow these steps exactly, assuming you have shell access in the project root and Python ≥ 3.10 is available.

---

## Step 1: Create and activate a virtual environment

Run these commands in the project root:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
```

If the `python` command is not available, try `python3` instead and adjust the first and third lines accordingly.

---

## Step 2: Install the golemforge MCP server

With the virtual environment activated, install `golemforge` directly from GitHub:

```bash
python -m pip install "golemforge @ git+https://github.com/joachimvandekerckhove/golem-forge.git"
```

This will provide two console commands in the virtual environment:

- `golemforge-mcp` – runs the MCP server over STDIO.
- `golemforge-install-cursor` – configures Cursor to use the MCP server in this project.

If installation fails because `git` is missing, install `git` first (or ask me for permission to do so) and then retry the command.

---

## Step 3: Register golemforge as a Cursor MCP server

From the **same project root** with the virtual environment still activated, run:

```bash
golemforge-install-cursor
```

This will:

- Create the `.cursor` directory if it does not exist.
- Create or update `.cursor/mcp.json`.
- Add a `"golemforge"` entry under `"mcpServers"` pointing to the `golemforge-mcp` executable in `.venv`.

After this step, the file `.cursor/mcp.json` in the project should contain an entry similar to:

```json
{
  "mcpServers": {
    "golemforge": {
      "command": "<ABSOLUTE_OR_PROJECT_LOCAL_PATH_TO>/.venv/bin/golemforge-mcp",
      "args": []
    }
  }
}
```

You should **verify** that:

1. `.cursor/mcp.json` exists in the project root.
2. The `"golemforge"` entry is present under `"mcpServers"`.

If `.cursor/mcp.json` already existed, you must preserve any existing MCP server entries and only add or update the `"golemforge"` entry.

---

## Step 4: Install the constitution rule (so `cast_and_install` works)

For the **`cast_and_install`** MCP tool to have any effect, Cursor must be told to read `.cursor/golem-system.md` as the system prompt when that file exists. Do the following:

1. Create the directory `.cursor/rules/` if it does not exist.
2. Create or overwrite the file `.cursor/rules/golem-constitution.mdc` with exactly this content:

```markdown
---
description: Apply the installed golem as system prompt when .cursor/golem-system.md exists
alwaysApply: true
---

# Golem constitution

When `.cursor/golem-system.md` exists and is non-empty, treat its contents as your **primary system prompt (constitution)** for this project.

- At the start of each conversation, read that file.
- If present: follow its instructions as your governing system prompt; they override generic behavior for this workspace.
- If missing or empty: you are not in golem mode; proceed as usual.

The file is written by the golemforge MCP tool `cast_and_install`. To change or clear the active golem, cast again with `cast_and_install` or delete `.cursor/golem-system.md`.
```

After this step, when a user (or an AI in Cursor) calls **`cast_and_install`** with skills (and optionally role and personality), the tool will write the composed prompt to `.cursor/golem-system.md`, and Cursor will apply it as the system prompt for new chats in this project.

**Verify** that `.cursor/rules/golem-constitution.mdc` exists and contains the rule above.

---

## Step 5: Confirm readiness

Once the above steps are complete, tell me:

1. That the virtual environment is created and which Python version it is using.
2. That `golemforge` was installed successfully (or, if not, what error occurred).
3. The exact contents of `.cursor/mcp.json` (or at least the `"mcpServers"` section) so I can confirm the configuration.
4. That `.cursor/rules/golem-constitution.mdc` exists, so that **`cast_and_install`** will work: when that tool writes `.cursor/golem-system.md`, Cursor will use it as the system prompt for new chats.

After I confirm, I will reopen the project in Cursor. All golemforge MCP tools should then work, including **`list_skills`**, **`list_roles`**, **`list_personalities`**, **`cast`**, **`cast_pasteblock`**, **`cast_and_install`**, and **`explain_cast`**.


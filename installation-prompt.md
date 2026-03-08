Run the following command in the terminal to install the **golemforge MCP server** into this Cursor project:

```bash
uvx --from "git+https://github.com/joachimvandekerckhove/golem-forge.git" golemforge-install-cursor
```

If `uv` is not installed, install it first:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then re-run the install command.

---

The install command will:
1. Download and run `golemforge-install-cursor` directly from GitHub — no virtual environment or local clone needed.
2. Create or update `.cursor/mcp.json` with a `"golemforge"` entry that uses `uvx` to launch the MCP server.
3. Create `.cursor/rules/golem-constitution.mdc` so that `cast_and_install` takes effect immediately.

After it completes, reload the Cursor window (Ctrl+Shift+P → **Reload Window**) to activate the server. Then confirm the following tools are available under the `golemforge` MCP server:

- `list_skills`, `list_roles`, `list_personalities`
- `cast`, `cast_pasteblock`, `cast_and_install`, `explain_cast`

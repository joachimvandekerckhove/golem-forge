**Prerequisites:** `git` must be installed (uv uses it to fetch the repo). On Linux: `sudo apt install git` or equivalent.

---

**1. Ensure `uv` is installed and on your PATH**

If you don’t have `uv` yet, install it:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then make sure `uv` is on your PATH (the installer puts it in `$HOME/.local/bin`). Either open a **new terminal**, or run:

```bash
source ~/.profile
```

(or `source ~/.bashrc`). If `uvx` is still not found, run:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Verify with: `uvx --version` (should print a version).

---

**2. Install the golemforge MCP server**

From your project root, run:

```bash
uvx --from "git+https://github.com/joachimvandekerckhove/golem-forge.git" golemforge-install-cursor
```

This will:
1. Download and run `golemforge-install-cursor` directly from GitHub — no virtual environment or local clone needed.
2. Create or update `.cursor/mcp.json` with a `"golemforge"` entry that uses `uvx` to launch the MCP server.
3. Create `.cursor/rules/golem-constitution.mdc` so that `cast_and_install` takes effect immediately.

---

**3. Activate and verify**

Reload the Cursor window (Ctrl+Shift+P → **Reload Window**) to activate the server. Then confirm the following tools are available under the `golemforge` MCP server:

- `list_skills`, `list_roles`, `list_personalities`
- `cast`, `cast_pasteblock`, `cast_and_install`, `explain_cast`

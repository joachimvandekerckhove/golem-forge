**Instructions:** Install the golemforge MCP server in this project. Do the following in order: (1) ensure prerequisites and `uv` are available and on PATH, (2) run the golemforge installer from the project root, (3) reload Cursor and verify the tools. Details below.

In minimal environments (e.g. Docker, CI, fresh OS), install the prerequisites first (see below) or the uv install script will fail.

---

**Prerequisites:** `git` (uv uses it to fetch the repo) and either `curl` or `wget` (to install uv). On Debian/Ubuntu:

```bash
sudo apt update && sudo apt install -y git curl
```

(or install `wget` instead of `curl` if you prefer).

---

**1. Ensure `uv` is installed and on your PATH**

In minimal or scripted environments, set PATH first so `uvx` is available in the same shell right after install:

```bash
export PATH="${HOME}/.local/bin:${PATH}"
```

If you don’t have `uv` yet, install it with **either**:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

or, if you have `wget` but not `curl`:

```bash
wget -qO- https://astral.sh/uv/install.sh | sh
```

If you’re in a new terminal and `uvx` isn’t found, run the `export PATH` line above, or:

```bash
source ~/.profile
```

(or `source ~/.bashrc`).

Verify:

```bash
uvx --version
```

(should print a version).

---

**2. Install the golemforge MCP server**

From your project root (with `uvx` on your PATH), run:

```bash
uvx --from "git+https://github.com/joachimvandekerckhove/golem-forge.git" golemforge-install-cursor
```

This will:
1. Download and run `golemforge-install-cursor` directly from GitHub — no virtual environment or local clone needed.
2. Create or update `.cursor/mcp.json` with a `"golemforge"` entry that uses `uvx` to launch the MCP server.
3. Create `.cursor/rules/golem-constitution.mdc` so that `cast_and_install` takes effect immediately.

---

**3. Activate and verify**

Reload the Cursor window (Ctrl+Shift+P → **Reload Window**) to activate the server.

**Confirm successful installation:** Call the golemforge MCP tools and check that they return data (no errors). For example: invoke `list_skills`, `list_roles`, and `list_personalities`; each should return a list and count. Optionally call `explain_cast` with one skill ID (e.g. `["coding/python"]`) and confirm it returns file paths and an estimated character count. If any call fails or the golemforge server does not appear in the MCP list, treat installation as failed and apply the ENOENT fix below, then re-verify.

Tools that should be available under the `golemforge` MCP server:

- `list_skills`, `list_roles`, `list_personalities`
- `cast`, `cast_pasteblock`, `cast_and_install`, `explain_cast`

**If you see "spawn uvx ENOENT" in the MCP log:** Cursor starts MCP servers without your shell PATH, so it can’t find `uvx`. Edit `.cursor/mcp.json` and set the golemforge `"command"` to the **full path** of `uvx`, for example:

```json
"command": "/home/yourusername/.local/bin/uvx"
```

Get your path by running `which uvx` in a terminal (after `export PATH="${HOME}/.local/bin:${PATH}"` if needed). Then reload the window again.
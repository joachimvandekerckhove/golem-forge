---
name: dhub-cli
description: Guide for using the dhub CLI — the AI skill manager for data science agents. Covers authentication, publishing, installing, running skills, managing API keys, eval reports, and troubleshooting. Use when users ask about dhub commands, skill publishing workflows, or need help with the Decision Hub CLI.
---
# dhub CLI Guide

`dhub` is the AI skill manager for data science agents. It publishes, discovers, installs, and runs Skills — modular packages (code + prompts) that agents like Claude Code, Cursor, Codex, and Windsurf can use.

## Installation

```bash
uv tool install dhub-cli    # via uv (recommended)
pipx install dhub-cli       # via pipx
```

## Command Overview

```
dhub login              Authenticate via GitHub
dhub logout             Remove stored token
dhub env                Show active environment, config path, API URL
dhub init [path]        Scaffold a new skill project
dhub publish [ref]      Publish skill(s) — from dir or git repo
dhub install org/skill  Install a skill from the registry
dhub uninstall org/skill  Remove a locally installed skill
dhub list               List all published skills
dhub delete org/skill   Delete skill versions from registry
dhub run org/skill      Run a locally installed skill
dhub ask "query"        Natural language skill search
dhub eval-report org/skill@version  View eval report
dhub logs [ref] [-f]    View or tail eval run logs
dhub org list           List your namespaces
dhub config default-org Set default namespace for publishing
dhub keys add <name>    Store an API key for evals
dhub keys list          List stored API key names
dhub keys remove <name> Remove a stored API key
dhub --version          Show CLI version
```

See the "dhub Command Reference" appendix on for full details on every command, flag, and option.

## Environments (Dev / Prod)

dhub supports two independent stacks controlled by `DHUB_ENV`:

| Env | API URL | Config File |
|-----|---------|-------------|
| `prod` (default) | `https://lfiaschi--api.modal.run` | `~/.dhub/config.prod.json` |
| `dev` | `https://lfiaschi--api-dev.modal.run` | `~/.dhub/config.dev.json` |

Always prefix commands with `DHUB_ENV=dev` when working against the dev stack:

```bash
DHUB_ENV=dev dhub login
DHUB_ENV=dev dhub list
DHUB_ENV=dev dhub publish
```

The `dhub env` command shows the currently active environment, config path, and API URL.

## Authentication

dhub uses GitHub Device Flow (OAuth2). Run `dhub login` and follow the prompts:

1. dhub requests a device code from the server
2. You open `https://github.com/login/device` and enter the displayed code
3. dhub polls until you authorize (up to 5 minutes)
4. Token is saved to `~/.dhub/config.{env}.json`

All subsequent commands use this token automatically. Run `dhub logout` to clear it.

You can override the API URL with `dhub login --api-url <url>` for custom deployments.

## Publishing Workflow

### Quick publish (auto-detect everything)

From a directory containing a valid SKILL.md:

```bash
dhub publish              # auto-detects org, name, bumps patch version
dhub publish --minor      # bump minor version instead
dhub publish --major      # bump major version
dhub publish --version 2.0.0  # explicit version
```

### Explicit publish

```bash
dhub publish myorg/my-skill          # specify org/skill, auto-bump patch
dhub publish myorg/my-skill ./path   # specify path to skill directory
```

### How auto-detection works

1. **Skill name** — read from `name` field in SKILL.md frontmatter
2. **Organization** — auto-detected if you belong to exactly one org. If you have multiple, specify explicitly: `dhub publish myorg/my-skill`
3. **Version** — fetches latest version from registry, bumps patch by default. First publish uses `0.1.0`

### Argument disambiguation

The first positional argument is interpreted as:
- A **path** if it starts with `.`, `/`, `~`, or is an existing directory
- An **org/skill reference** otherwise

So `dhub publish .` and `dhub publish myorg/skill` both work as expected.

### Safety grading

After publishing, the server runs safety checks and assigns a grade:

| Grade | Meaning | Effect |
|-------|---------|--------|
| **A** | Clean — no elevated permissions or risky patterns | Normal installation |
| **B** | Elevated permissions detected | Warning shown on install |
| **C** | Ambiguous/risky patterns | Users need `--allow-risky` flag to install |
| **F** | Rejected — fails safety checks | Publish is rejected (HTTP 422) |

If the skill has an `evals` block, agent evaluation runs after publish and the CLI automatically attaches to the live log stream. Press Ctrl-C to detach; re-attach later with `dhub logs`.

### What gets zipped

The publish command creates a zip of the skill directory, excluding:
- Hidden files (names starting with `.`)
- `__pycache__/` directories

## Publishing from a Git Repository

You can pass a git URL directly to `dhub publish`:

```bash
dhub publish https://github.com/myorg/my-skills-repo
dhub publish git@github.com:myorg/my-skills-repo.git --ref v2.0
dhub publish https://github.com/myorg/repo --minor
```

The command detects that the argument is a git URL (HTTPS, SSH, or `.git` suffix), clones the repository, recursively discovers all directories containing a valid SKILL.md, and publishes each one. This is useful for monorepos containing multiple skills.

### How discovery works

1. The repo is cloned (shallow clone with `--depth 1`)
2. All `SKILL.md` files are found recursively
3. Hidden directories (`.git`, etc.), `node_modules`, and `__pycache__` are skipped
4. Each `SKILL.md` is validated — only directories with valid frontmatter (name + description) are published
5. Skills are published one by one; failures don't stop the remaining skills

### Git-specific options

- `--ref` — branch, tag, or commit to checkout (only valid with git URLs)

## Installing Skills

```bash
dhub install myorg/my-skill                          # latest version
dhub install myorg/my-skill --version 1.2.0          # specific version
dhub install myorg/my-skill --agent claude-code        # install + link to Claude Code
dhub install myorg/my-skill --agent all                # link to all agents
dhub install myorg/my-skill --allow-risky             # allow Grade C skills
```

### Where skills get installed

- **Canonical path**: `~/.dhub/skills/{org}/{skill}/`
- **Agent symlinks** (when using `--agent`):

| Agent | `--agent` | Symlink Location |
|-------|-----------|-----------------|
| Claude Code | `claude-code` | `~/.claude/skills/{skill}` |
| Cursor | `cursor` | `~/.cursor/skills/{skill}` |
| Codex | `codex` | `~/.codex/skills/{skill}` |
| Windsurf | `windsurf` | `~/.codeium/windsurf/skills/{skill}` |
| Gemini CLI | `gemini-cli` | `~/.gemini/skills/{skill}` |
| GitHub Copilot | `github-copilot` | `~/.copilot/skills/{skill}` |
| Roo Code | `roo` | `~/.roo/skills/{skill}` |
| OpenCode | `opencode` | `~/.config/opencode/skills/{skill}` |

40+ agents supported. Run `dhub install org/skill --agent all` to link to every agent. See the README for the full list.

Symlinks point to the canonical `~/.dhub/skills/` path, so the skill is stored once and shared across agents.

### After installation: load the skill immediately

When you install a skill on behalf of the user, **always read it into the current conversation** so it's usable right away. Don't tell the user to start a new session.

After `dhub install` succeeds:
1. Read the installed skill's `SKILL.md` from `~/.dhub/skills/{org}/{skill}/SKILL.md`
2. Confirm to the user that the skill is loaded and ready to use now

Don't read reference files upfront — the SKILL.md itself will tell you when to consult specific references.

The user installed a skill because they want to use it — treat installation as implicit activation.

### Integrity verification

Downloads are verified via SHA-256 checksum before extraction. If the checksum doesn't match, installation aborts.

## Running Skills Locally

```bash
dhub run myorg/my-skill              # run the skill
dhub run myorg/my-skill -- --flag    # pass extra args to the entrypoint
```

### Prerequisites

- The skill must be installed locally (`dhub install` first)
- The skill must have a `runtime` block in its SKILL.md
- `uv` must be available on PATH
- Required environment variables (from `runtime.env`) must be set
- Only `language: python` is supported

### What happens

1. Parses SKILL.md to get runtime config
2. Validates prerequisites (uv, lockfile, entrypoint, env vars)
3. Runs `uv sync --directory {skill_dir}` to install dependencies
4. Runs `uv run --directory {skill_dir} python {entrypoint} [extra_args]`

## Eval Reports

View evaluation results for a published skill version:

```bash
dhub eval-report myorg/my-skill@1.0.0
```

The report shows:
- **Agent** used for the eval run
- **Judge model** that evaluated the output
- **Status**: passed, failed, error, pending
- **Results**: pass/fail count and per-case details with reasoning

Evals run automatically in the background after publishing a skill that has an `evals` block. Use `dhub eval-report` to check results.

## Eval Logs (Real-Time Streaming)

Tail eval run logs in real-time, or view recent runs:

```bash
dhub logs                              # list recent eval runs
dhub logs myorg/my-skill --follow      # tail latest run for latest version
dhub logs myorg/my-skill@1.0.0 -f      # tail latest run for specific version
dhub logs <run-id> --follow            # tail a specific run by ID
```

When you publish a skill with evals, the CLI automatically attaches to the log stream. Press Ctrl-C to detach — you can re-attach later with `dhub logs`.

Events include: sandbox setup, agent stdout/stderr, judge start, case verdicts (PASS/FAIL), and a final summary.

## API Key Management

Skills that use third-party APIs during evaluation need API keys stored in Decision Hub:

```bash
dhub keys add OPENAI_API_KEY        # prompts securely for the value
dhub keys list                      # show stored key names
dhub keys remove OPENAI_API_KEY     # delete a stored key
```

Keys are stored server-side (encrypted) and injected into eval sandbox environments. Key names must match the `runtime.env` entries in SKILL.md.

## Organization Management

```bash
dhub org list    # list namespaces you can publish to
```

Your namespaces are derived from your GitHub account and org memberships. Run `dhub login` to refresh memberships after joining new GitHub orgs.

## Skill Discovery

```bash
dhub ask "analyze A/B test results"
dhub ask "generate presentation slides"
```

Natural language search across all published skills. Returns matching skills with descriptions and install instructions.

## Scaffolding a New Skill

```bash
dhub init                  # interactive — prompts for name and description
dhub init ./my-skill       # create in a specific directory
```

Creates:
```
my-skill/
  SKILL.md     # frontmatter + body skeleton
  src/         # source code directory
```

## SKILL.md Format (Quick Reference)

```yaml
---
name: my-skill                 # 1-64 chars, lowercase + hyphens
description: What it does      # 1-1024 chars, triggers skill activation
license: MIT                   # optional
runtime:                       # optional — for executable skills
  language: python
  entrypoint: src/main.py
  env: [OPENAI_API_KEY]
  dependencies:
    package_manager: uv
    lockfile: uv.lock
evals:                         # optional — for testable skills
  agent: claude
  judge_model: claude-sonnet-4-5-20250929
---
System prompt for the agent goes here.
```

## Troubleshooting

### "Connection timed out" or slow first request
Modal cold starts take 30-60s. Retry after a minute. All dhub HTTP calls use 60s timeouts internally.

### "No namespaces available"
Run `dhub login` to refresh GitHub org memberships. You need at least one org to publish.

### "You have multiple namespaces"
Specify the org explicitly: `dhub publish myorg/my-skill` instead of `dhub publish`.

### "Version X already exists"
Versions are immutable. Bump the version: `dhub publish --patch` (or `--minor`, `--major`), or use `--version` with a new number.

### "Rejected (Grade F)"
The skill failed safety checks. Review your SKILL.md and scripts for dangerous patterns (shell injection, credential exfiltration, etc.).

### "Skill not installed" when running
Install first with `dhub install org/skill`, then `dhub run org/skill`.

### "This skill has no runtime configuration"
Only skills with a `runtime` block can be run via `dhub run`. Prompt-only skills don't need `dhub run`.

### "Checksum mismatch"
Download was corrupted. Retry `dhub install`. If it persists, the server package may be damaged — try re-publishing.

### Wrong environment
Check with `dhub env`. Set `DHUB_ENV=dev` or `DHUB_ENV=prod` before commands.

### Config file location
- Dev: `~/.dhub/config.dev.json`
- Prod: `~/.dhub/config.prod.json`
- Override API URL: `DHUB_API_URL` env var (highest priority)


# dhub Command Reference

Complete reference for every dhub command, flag, and option.

## dhub login

Authenticate with Decision Hub via GitHub Device Flow.

```
dhub login [--api-url URL]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--api-url` | string | from config | Override the API URL for this login |

**Flow:**
1. POST `/auth/github/code` → receives device code + user code
2. Display user code and `https://github.com/login/device` URL
3. Poll POST `/auth/github/token` every 5s (HTTP 428 = pending, 200 = done)
4. Save token to `~/.dhub/config.{env}.json`
5. Timeout: 300 seconds

**Config after login:**
```json
{"api_url": "https://lfiaschi--api.modal.run", "token": "<oauth_token>"}
```

---

## dhub logout

Remove stored authentication token.

```
dhub logout
```

No options. Sets token to null in the config file.

---

## dhub env

Show active environment, config file path, and API URL.

```
dhub env
```

No options. Displays the current `DHUB_ENV` value, resolved config path, and API URL.

---

## dhub init

Scaffold a new skill project with SKILL.md and src/ directory.

```
dhub init [PATH]
```

| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `PATH` | no | current directory | Where to create the skill |

Interactive — prompts for skill name and description. Validates name against pattern `^[a-z0-9]([a-z0-9-]{0,62}[a-z0-9])?$`.

**Creates:**
```
skill-name/
  SKILL.md
  src/
```

---

## dhub publish

Publish a skill to the registry.

```
dhub publish [SKILL_REF] [PATH] [--version VER] [--patch] [--minor] [--major] [--ref REF]
```

| Argument/Option | Required | Default | Description |
|----------------|----------|---------|-------------|
| `SKILL_REF` | no | auto-detect from SKILL.md | Org/skill reference, path, or git URL |
| `PATH` | no | `.` | Path to skill directory |
| `--version` | no | auto-bump | Explicit semver (e.g. `1.2.3`) |
| `--patch` | no | true (default bump) | Bump patch version |
| `--minor` | no | false | Bump minor version |
| `--major` | no | false | Bump major version |
| `--ref` | no | default branch | Branch/tag/commit (git URLs only) |

**Positional argument disambiguation:**
- Git URL (starts with `https://`, `http://`, `git@`, `ssh://`, `git://`, or ends with `.git`) → clone repo and publish all discovered skills
- Starts with `.`, `/`, `~`, or is an existing directory → treated as PATH
- Contains `/` but not a directory → treated as SKILL_REF (org/skill)

**Auto-detection:**
- **Name**: from SKILL.md frontmatter `name` field
- **Org**: auto-detected if user belongs to exactly one org
- **Version**: fetches latest from `/v1/skills/{org}/{name}/latest-version`, bumps patch. First publish → `0.1.0`

**Error codes:**
- HTTP 409 → version already exists
- HTTP 422 → Grade F, safety checks failed
- HTTP 503 → server LLM judge not configured

**Output:** Published reference with safety grade (A/B/C). If evals are configured, the CLI automatically attaches to the eval log stream (see `dhub logs`).

**Git repository mode:**

When the first argument is a git URL, publish clones the repo and discovers all skills:

```bash
dhub publish https://github.com/myorg/skills-repo
dhub publish git@github.com:myorg/repo.git --ref main
dhub publish https://github.com/myorg/repo --minor
```

Steps:
1. Clone the repository (shallow, `--depth 1`) into a temporary directory
2. Recursively find all `SKILL.md` files, skipping hidden dirs, `node_modules`, `__pycache__`
3. Validate each `SKILL.md` — only directories with valid frontmatter are included
4. Publish each discovered skill, reading names from SKILL.md frontmatter
5. Clean up the temporary clone

If one skill fails to publish, the remaining skills still get published. A summary is printed at the end: X published, Y skipped, Z failed.

---

## dhub install

Install a skill from the registry.

```
dhub install ORG/SKILL [--version VER] [--agent AGENT] [--allow-risky]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--version`, `-v` | string | `"latest"` | Version spec |
| `--agent` | string | none | Target agent (e.g. `claude-code`, `cursor`, `codex`, `windsurf`) or `all`. See README for full list. |
| `--allow-risky` | flag | false | Allow installing Grade C skills |

**Steps:**
1. Resolve version via GET `/v1/resolve/{org}/{skill}?spec={version}`
2. Download zip from signed S3 URL
3. Verify SHA-256 checksum
4. Extract to `~/.dhub/skills/{org}/{skill}/`
5. Create agent symlinks if `--agent` specified

**Symlink naming:** `{skill}` in the agent's skill directory.

---

## dhub uninstall

Remove a locally installed skill and all its agent symlinks.

```
dhub uninstall ORG/SKILL
```

Removes:
1. Agent symlinks from all agent directories
2. The canonical directory at `~/.dhub/skills/{org}/{skill}/`
3. Empty org directory if no other skills remain

---

## dhub list

List all published skills on the registry, sorted by download count (most popular first).

```
dhub list
dhub list --org ORG          # filter by organization
dhub list --skill NAME       # filter by skill name (substring match)
dhub list --page-size 20     # items per page (default 50, max 100)
dhub list --all              # dump all pages without prompting
```

Displays a table with columns: Org, Skill, Category, Version, Updated (YYYY-MM-DD), Safety (grade), Downloads, Author, Description.

---

## dhub delete

Delete a skill version (or all versions) from the registry.

```
dhub delete ORG/SKILL [--version VER]
```

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `--version`, `-v` | string | none | Specific version to delete. Omit to delete ALL versions (with confirmation prompt). |

**Error codes:**
- HTTP 404 → skill or version not found
- HTTP 403 → no permission to delete

---

## dhub run

Run a locally installed skill using its configured runtime.

```
dhub run ORG/SKILL [-- EXTRA_ARGS...]
```

| Argument | Required | Description |
|----------|----------|-------------|
| `ORG/SKILL` | yes | Installed skill reference |
| `EXTRA_ARGS` | no | Extra arguments passed to the entrypoint script |

**Requirements:**
- Skill must be installed locally
- SKILL.md must have a `runtime` block with `language: python`
- `uv` must be on PATH
- Lockfile must exist (if declared in runtime config)
- Entrypoint file must exist
- Required env vars (from `runtime.env`) must be set

**Execution:**
1. `uv sync --directory {skill_dir}` — install/sync dependencies
2. `uv run --directory {skill_dir} python {entrypoint} [extra_args]` — run the skill
3. Exit code from the entrypoint is propagated

---

## dhub ask

Natural language skill search.

```
dhub ask "QUERY"
```

Searches across all published skills. Returns markdown-formatted results in a Rich panel.

**API:** GET `/v1/search?q={query}`

---

## dhub eval-report

View the agent evaluation report for a skill version.

```
dhub eval-report ORG/SKILL@VERSION
```

The `@VERSION` is required. Format: `myorg/my-skill@1.0.0`.

**Output:**
- Agent and judge model used
- Overall status: passed / failed / error / pending
- Pass/fail count
- Per-case results with verdicts and reasoning

**Verdict values:** `pass`, `fail`, `error`
**Stages:** `sandbox` (execution failed), `agent` (non-zero exit), `judge` (LLM evaluation)

---

## dhub logs

View or tail eval run logs in real-time.

```
dhub logs [SKILL_REF] [--follow|-f]
```

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `SKILL_REF` | string | None | Skill ref (org/skill[@version]) or eval run ID |
| `--follow` / `-f` | flag | False | Tail logs in real-time |

**Usage patterns:**
- `dhub logs` — list recent eval runs (table with ID, status, agent, cases, stage)
- `dhub logs org/skill --follow` — tail latest run for the latest version
- `dhub logs org/skill@1.0.0 --follow` — tail latest run for a specific version
- `dhub logs <run-id> --follow` — tail a specific eval run by its UUID

**Log events:**
- `setup` — sandbox provisioning
- `case_start` — case N/M starting
- `log` — agent stdout/stderr (truncated to 200 chars for display)
- `judge_start` — LLM judge invoked
- `case_result` — PASS/FAIL/ERROR with reasoning
- `report` — final summary (passed/total, duration)

**Publish auto-attach:** When publishing a skill with evals, the CLI automatically starts tailing the eval run logs. Press Ctrl-C to detach; re-attach later with `dhub logs <run-id> --follow`.

---

## dhub org list

List namespaces you can publish to.

```
dhub org list
```

Shows organization slugs derived from your GitHub account and org memberships.

---

## dhub config default-org

Set the default namespace for publishing so you don't have to specify it each time.

```
dhub config default-org
```

Interactive — prompts you to choose from your available namespaces. The selection is saved to `~/.dhub/config.{env}.json`.

---

## dhub keys add

Store an API key for agent evaluations.

```
dhub keys add KEY_NAME
```

Prompts securely for the key value (hidden input). Keys are stored server-side (encrypted) and injected into eval sandbox environments.

**Error:** HTTP 409 if key name already exists. Remove it first with `dhub keys remove`.

---

## dhub keys list

List stored API key names.

```
dhub keys list
```

Displays a table with key names and creation dates. Does not show key values.

---

## dhub keys remove

Remove a stored API key.

```
dhub keys remove KEY_NAME
```

**Error:** HTTP 404 if key name not found.

---

## dhub --version

Show the installed CLI version.

```
dhub --version
dhub -V
```

---

## Global Behavior

**Timeouts:** All HTTP requests use 60-second timeouts to handle Modal cold starts.

**Headers:** Every request includes:
- `X-DHub-Client-Version: {version}` — CLI version for compatibility checking
- `Authorization: Bearer {token}` — when authenticated

**Environment:** `DHUB_ENV` controls dev/prod. `DHUB_API_URL` overrides the API URL entirely.

**Config priority:**
1. `DHUB_API_URL` env var (highest)
2. Saved config file (`~/.dhub/config.{env}.json`)
3. Default URL for environment

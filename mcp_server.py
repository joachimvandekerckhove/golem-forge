"""golemforge MCP server.

This module exposes tools for composing a reusable system prompt from a base
template and a set of local skill markdown files.

The server is designed for Cursor MCP integration over STDIO.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import uuid
from pathlib import Path
from random import choice
from typing import Any

from fastmcp import FastMCP

FORGE_VERSION = "0.1.0"
MAX_PROMPT_CHARACTERS = 100_000

PROJECT_ROOT = Path(__file__).resolve().parent
SKILLS_DIR = PROJECT_ROOT / "skills"
ROLES_DIR = PROJECT_ROOT / "roles"
PERSONALITIES_DIR = PROJECT_ROOT / "personalities"
TEMPLATES_DIR = PROJECT_ROOT / "templates"
BASE_TEMPLATE_PATH = TEMPLATES_DIR / "base_system.md"
NAMES_PATH = PROJECT_ROOT / "names.json"
CURSOR_DIR = PROJECT_ROOT / ".cursor"
GOLEM_SYSTEM_PATH = CURSOR_DIR / "golem-system.md"

mcp = FastMCP("golemforge")


def _sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _safe_read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # defensive
        raise RuntimeError(f"Could not read {path}: {exc}") from exc


def _list_skill_ids() -> list[str]:
    skills: list[str] = []
    if not SKILLS_DIR.exists():
        return skills

    for md_file in SKILLS_DIR.glob("**/*.md"):
        rel = md_file.relative_to(SKILLS_DIR)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if md_file.name.startswith("."):
            continue
        skill_id = rel.with_suffix("").as_posix()
        skills.append(skill_id)

    return sorted(skills)


def _list_ids(root: Path) -> list[str]:
    """Generic helper to list markdown-based IDs under a root directory."""

    items: list[str] = []
    if not root.exists():
        return items

    for md_file in root.glob("**/*.md"):
        rel = md_file.relative_to(root)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if md_file.name.startswith("."):
            continue
        item_id = rel.with_suffix("").as_posix()
        items.append(item_id)

    return sorted(items)


def _validate_skills(skills: list[str]) -> tuple[list[str], list[str]]:
    included: list[str] = []
    missing: list[str] = []
    for skill_id in skills:
        candidate = SKILLS_DIR / f"{skill_id}.md"
        if candidate.exists() and candidate.is_file():
            included.append(skill_id)
        else:
            missing.append(skill_id)
    return included, missing


def _load_role_text(role: str | None) -> tuple[str | None, str | None]:
    """Resolve a role ID to its markdown text and hash, or (None, None)."""

    if not role:
        return None, None

    path = ROLES_DIR / f"{role}.md"
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Role '{role}' not found at {path}")

    text = _safe_read_text(path)
    return text, _sha256_text(text)


def _load_personality_text(personality: str | None) -> tuple[str | None, str | None]:
    """Resolve a personality ID to its markdown text and hash, or (None, None)."""

    if not personality:
        return None, None

    path = PERSONALITIES_DIR / f"{personality}.md"
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Personality '{personality}' not found at {path}")

    text = _safe_read_text(path)
    return text, _sha256_text(text)


def _load_names() -> list[str]:
    raw = _safe_read_text(NAMES_PATH)
    data = json.loads(raw)
    if not isinstance(data, list) or not data:
        raise RuntimeError("names.json must contain a non-empty JSON array of names.")
    names = [str(item) for item in data]
    return names


def _error_response(code: str, message: str, **extra: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"ok": False, "error": {"code": code, "message": message}}
    if extra:
        payload["error"].update(extra)
    return payload


def _build_cast(
    skills: list[str],
    extra_instructions: str = "",
    role: str | None = None,
    personality: str | None = None,
) -> dict[str, Any]:
    try:
        requested = list(skills)
        included, missing = _validate_skills(requested)
        if missing:
            return _error_response(
                "missing_skills",
                "Some requested skills were not found.",
                missing_skills=missing,
                suggestion="Call list_skills() to discover valid IDs.",
            )

        try:
            role_text, role_hash = _load_role_text(role)
        except FileNotFoundError:
            return _error_response(
                "missing_role",
                "Requested role was not found.",
                requested_role=role,
                suggestion="Call list_roles() to discover valid IDs.",
            )

        try:
            personality_text, personality_hash = _load_personality_text(personality)
        except FileNotFoundError:
            return _error_response(
                "missing_personality",
                "Requested personality was not found.",
                requested_personality=personality,
                suggestion="Call list_personalities() to discover valid IDs.",
            )

        base_template = _safe_read_text(BASE_TEMPLATE_PATH)
        invocation_id = str(uuid.uuid4())
        golem_name = choice(_load_names())

        skill_sections: list[str] = []
        skill_hashes: dict[str, str] = {}

        for skill_id in included:
            skill_path = SKILLS_DIR / f"{skill_id}.md"
            skill_text = _safe_read_text(skill_path)
            skill_hashes[skill_id] = _sha256_text(skill_text)
            skill_sections.append(
                f"\n<!-- BEGIN SKILL: {skill_id} -->\n{skill_text.rstrip()}\n<!-- END SKILL: {skill_id} -->\n"
            )

        skills_bundle = "\n".join(skill_sections).strip()

        normalized_skills = sorted(included)
        manifest = {
            "forge_version": FORGE_VERSION,
            "invocation_id": invocation_id,
            "golem_name": golem_name,
            "skills_requested": requested,
            "skills_included": normalized_skills,
            "skill_hashes": {key: skill_hashes[key] for key in sorted(skill_hashes)},
        }
        if role:
            manifest["role"] = role
            if role_hash:
                manifest["role_hash"] = role_hash
        if personality:
            manifest["personality"] = personality
            if personality_hash:
                manifest["personality_hash"] = personality_hash
        manifest_json = json.dumps(manifest, indent=2, ensure_ascii=True)

        if role_text:
            role_section = (
                f"<!-- BEGIN ROLE: {role} -->\n"
                f"{role_text.rstrip()}\n"
                f"<!-- END ROLE: {role} -->"
            )
        else:
            role_section = "(no role selected)"

        if personality_text:
            personality_section = (
                f"<!-- BEGIN PERSONALITY: {personality} -->\n"
                f"{personality_text.rstrip()}\n"
                f"<!-- END PERSONALITY: {personality} -->"
            )
        else:
            personality_section = "(no personality selected)"

        compiled_prompt = base_template.format(
            NAME=golem_name,
            INVOCATION_ID=invocation_id,
            FORGE_VERSION=FORGE_VERSION,
            SKILLS_REQUESTED=", ".join(requested) if requested else "(none)",
            SKILLS_INCLUDED=", ".join(included) if included else "(none)",
            EXTRA_INSTRUCTIONS=extra_instructions.strip() or "(none)",
            SKILLS_BUNDLE=skills_bundle or "(no skills selected)",
            ROLE_SECTION=role_section,
            PERSONALITY_SECTION=personality_section,
            MANIFEST_JSON=manifest_json,
        )

        warning = None
        if len(compiled_prompt) > MAX_PROMPT_CHARACTERS:
            keep = MAX_PROMPT_CHARACTERS
            compiled_prompt = (
                compiled_prompt[:keep]
                + "\n\n[TRUNCATED BY GOLEMFORGE: prompt exceeded character limit.]"
            )
            warning = (
                f"Compiled prompt exceeded {MAX_PROMPT_CHARACTERS} characters and was truncated."
            )

        compiled_prompt_sha256 = _sha256_text(compiled_prompt)
        optional_developer = extra_instructions.strip() or "(none)"
        paste_block = (
            "=== SYSTEM ===\n"
            f"{compiled_prompt}\n\n"
            "=== OPTIONAL DEVELOPER ===\n"
            f"{optional_developer}\n\n"
            "=== USER KICKOFF ===\n"
            f"You are {golem_name}. Confirm you loaded skills: "
            f"{', '.join(included) if included else '(none)'}. "
            "Then ask me what I want to do first."
        )

        result: dict[str, Any] = {
            "ok": True,
            "golem_name": golem_name,
            "invocation_id": invocation_id,
            "skills_requested": requested,
            "skills_included": included,
            "skill_hashes": skill_hashes,
            "compiled_prompt": compiled_prompt,
            "paste_block": paste_block,
            "character_count": len(compiled_prompt),
            "compiled_prompt_sha256": compiled_prompt_sha256,
            "forge_version": FORGE_VERSION,
        }
        if warning:
            result["warning"] = warning

        return result
    except Exception as exc:  # defensive, tool-safe
        return _error_response(
            "cast_failure",
            "An unexpected error occurred while forging the prompt.",
            details=str(exc),
        )


@mcp.tool()
def list_skills() -> dict[str, Any]:
    """List available skill IDs discovered under `golemforge/skills`.

    This returns deterministic, sorted identifiers derived from markdown
    filenames in `skills/*.md` and nested paths such as `skills/*/*.md`.
    Dotfiles and non-markdown files are ignored.
    """

    try:
        skills = _list_skill_ids()
        return {"skills": skills, "count": len(skills)}
    except Exception as exc:
        return _error_response(
            "list_skills_failure",
            "Unable to enumerate skills.",
            details=str(exc),
        )


@mcp.tool()
def list_roles() -> dict[str, Any]:
    """List available role IDs discovered under `roles/`."""

    try:
        roles = _list_ids(ROLES_DIR)
        return {"roles": roles, "count": len(roles)}
    except Exception as exc:
        return _error_response(
            "list_roles_failure",
            "Unable to enumerate roles.",
            details=str(exc),
        )


@mcp.tool()
def list_personalities() -> dict[str, Any]:
    """List available personality IDs discovered under `personalities/`."""

    try:
        personalities = _list_ids(PERSONALITIES_DIR)
        return {"personalities": personalities, "count": len(personalities)}
    except Exception as exc:
        return _error_response(
            "list_personalities_failure",
            "Unable to enumerate personalities.",
            details=str(exc),
        )


@mcp.tool()
def cast(
    skills: list[str],
    extra_instructions: str = "",
    role: str | None = None,
    personality: str | None = None,
) -> dict[str, Any]:
    """Forge a complete prompt package from selected skill IDs.

    Use this tool when you want the full output payload including provenance,
    compiled prompt text, and a paste-ready block for starting a fresh Cursor
    chat. Skill files are included in the caller-provided order while the
    manifest keeps a normalized alphabetical list for reproducibility.
    """

    return _build_cast(
        skills=skills,
        extra_instructions=extra_instructions,
        role=role,
        personality=personality,
    )


@mcp.tool()
def cast_pasteblock(
    skills: list[str],
    extra_instructions: str = "",
    role: str | None = None,
    personality: str | None = None,
) -> dict[str, Any]:
    """Forge only the golem name and paste-ready block for quick bootstrapping.

    This is a lightweight convenience wrapper around `cast` when downstream
    automation only needs the generated persona name and final paste text.
    """

    result = _build_cast(
        skills=skills,
        extra_instructions=extra_instructions,
        role=role,
        personality=personality,
    )
    if not result.get("ok", False):
        return result
    return {
        "golem_name": result["golem_name"],
        "paste_block": result["paste_block"],
    }


@mcp.tool()
def cast_and_install(
    skills: list[str],
    extra_instructions: str = "",
    role: str | None = None,
    personality: str | None = None,
) -> dict[str, Any]:
    """Forge a golem and install it as the project constitution for future chats.

    Same as `cast`, but also writes the compiled system prompt to
    `.cursor/golem-system.md`. The project rule in `.cursor/rules/golem-constitution.mdc`
    tells Cursor to apply that file as the system prompt for every new chat in this
    project, so the golem persists across context limits and chat restarts.
    Use this when you want the cast golem to become the default assistant for
    this workspace.
    """

    result = _build_cast(
        skills=skills,
        extra_instructions=extra_instructions,
        role=role,
        personality=personality,
    )
    if not result.get("ok", False):
        return result

    try:
        CURSOR_DIR.mkdir(parents=True, exist_ok=True)
        GOLEM_SYSTEM_PATH.write_text(result["compiled_prompt"], encoding="utf-8")
        result = dict(result)
        result["installed_path"] = str(GOLEM_SYSTEM_PATH.relative_to(PROJECT_ROOT))
        result["installed"] = True
    except Exception as exc:
        result = dict(result)
        result["installed"] = False
        result["install_error"] = str(exc)

    return result


@mcp.tool()
def explain_cast(skills: list[str]) -> dict[str, Any]:
    """Preview which files `cast` will include and estimate prompt size.

    Use this for planning before prompt generation. It validates each skill ID,
    returns absolute file mappings, and estimates the character count using the
    base template plus selected skill files.
    """

    try:
        included, missing = _validate_skills(skills)
        files = []
        total = len(_safe_read_text(BASE_TEMPLATE_PATH))
        for skill_id in included:
            path = SKILLS_DIR / f"{skill_id}.md"
            text = _safe_read_text(path)
            total += len(text)
            files.append(
                {
                    "skill": skill_id,
                    "file": str(path),
                    "characters": len(text),
                }
            )

        return {
            "skills_requested": skills,
            "skills_included": included,
            "missing_skills": missing,
            "files": files,
            "estimated_character_count": total,
        }
    except Exception as exc:
        return _error_response(
            "explain_cast_failure",
            "Unable to explain cast inputs.",
            details=str(exc),
        )


def main() -> None:
    """Console entrypoint for running the MCP server over STDIO."""
    mcp.run(transport="stdio")


def install_cursor_cli() -> None:
    """Console entrypoint for wiring golemforge into a Cursor project.

    This writes or updates `.cursor/mcp.json` in the target project so that
    Cursor can discover the `golemforge` MCP server. It assumes you have
    already installed `golemforge` into the active Python environment.
    """

    parser = argparse.ArgumentParser(
        prog="golemforge-install-cursor",
        description=(
            "Configure the current directory (or a given project) to use the "
            "golemforge MCP server in Cursor by updating .cursor/mcp.json."
        ),
    )
    parser.add_argument(
        "--project-dir",
        default=".",
        help="Path to the Cursor project root (default: current directory).",
    )
    args = parser.parse_args()

    project_root = Path(args.project_dir).resolve()
    cursor_dir = project_root / ".cursor"
    mcp_path = cursor_dir / "mcp.json"

    cursor_dir.mkdir(parents=True, exist_ok=True)

    config: dict[str, Any] = {"mcpServers": {}}
    if mcp_path.exists():
        try:
            with mcp_path.open("r", encoding="utf-8") as f:
                existing = json.load(f)
            if isinstance(existing, dict):
                config.update(existing)
        except Exception:
            # Fall back to a minimal config if existing file is invalid.
            config = {"mcpServers": {}}

    if "mcpServers" not in config or not isinstance(config["mcpServers"], dict):
        config["mcpServers"] = {}

    # Resolve the golemforge-mcp executable in the current Python environment.
    command_path = Path(sys.executable).with_name("golemforge-mcp")
    config["mcpServers"]["golemforge"] = {
        "command": str(command_path),
        "args": [],
    }

    with mcp_path.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

    print(f"Configured golemforge MCP at {mcp_path}")


if __name__ == "__main__":
    main()

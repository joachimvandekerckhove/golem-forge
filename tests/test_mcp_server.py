"""Smoke tests for the golemforge MCP server tools.

Runs each tool function directly (no transport layer) and checks that
the returned payloads have the expected shape.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

import mcp_server as srv


def section(title: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {title}")
    print(f"{'=' * 60}")


def test_list_skills() -> None:
    section("list_skills()")
    result = srv.list_skills()
    print(json.dumps(result, indent=2))

    assert "skills" in result, "Missing 'skills' key"
    assert "count" in result, "Missing 'count' key"
    assert isinstance(result["skills"], list), "'skills' should be a list"
    assert result["count"] == len(result["skills"]), "count mismatch"
    assert result["count"] > 0, "Expected at least one skill"
    assert result["skills"] == sorted(result["skills"]), "Skills should be sorted"

    print(f"\n  PASS — {result['count']} skills discovered")


def test_cast_valid() -> None:
    section("cast(skills, extra_instructions)")
    skills = srv.list_skills()["skills"][:3]
    result = srv.cast(skills=skills, extra_instructions="Be concise.")
    keys_present = set(result.keys())

    expected_keys = {
        "ok", "golem_name", "invocation_id", "skills_requested",
        "skills_included", "skill_hashes", "compiled_prompt",
        "paste_block", "character_count", "compiled_prompt_sha256",
        "forge_version",
    }
    missing = expected_keys - keys_present
    assert not missing, f"Missing keys in cast result: {missing}"
    assert result["ok"] is True, f"cast returned ok=False: {result}"
    assert isinstance(result["compiled_prompt"], str), "compiled_prompt should be str"
    assert len(result["compiled_prompt"]) > 100, "compiled_prompt suspiciously short"
    assert result["character_count"] == len(result["compiled_prompt"])
    assert result["forge_version"] == srv.FORGE_VERSION
    assert "=== SYSTEM ===" in result["paste_block"]
    assert result["golem_name"], "golem_name should be non-empty"

    print(f"\n  Golem: {result['golem_name']}")
    print(f"  Invocation: {result['invocation_id']}")
    print(f"  Skills included: {result['skills_included']}")
    print(f"  Prompt size: {result['character_count']} chars")
    print(f"  SHA256: {result['compiled_prompt_sha256'][:16]}...")
    print(f"\n  PASS")


def test_cast_missing_skills() -> None:
    section("cast() with missing skills")
    result = srv.cast(skills=["nonexistent/fake-skill"])

    assert result.get("ok") is False, "Should return ok=False for missing skills"
    assert "error" in result, "Should contain 'error' key"
    assert result["error"]["code"] == "missing_skills"
    assert "nonexistent/fake-skill" in result["error"]["missing_skills"]

    print(f"  Error: {result['error']['message']}")
    print(f"  Missing: {result['error']['missing_skills']}")
    print(f"\n  PASS")


def test_cast_pasteblock() -> None:
    section("cast_pasteblock(skills)")
    skills = srv.list_skills()["skills"][:2]
    result = srv.cast_pasteblock(skills=skills)

    assert "golem_name" in result, "Missing 'golem_name'"
    assert "paste_block" in result, "Missing 'paste_block'"
    assert "compiled_prompt" not in result, "Should NOT include compiled_prompt"

    print(f"  Golem: {result['golem_name']}")
    print(f"  Paste block length: {len(result['paste_block'])} chars")
    print(f"\n  PASS")


def test_explain_cast() -> None:
    section("explain_cast(skills)")
    all_skills = srv.list_skills()["skills"]
    skills_to_explain = all_skills[:4]
    result = srv.explain_cast(skills=skills_to_explain)

    assert "skills_requested" in result
    assert "skills_included" in result
    assert "missing_skills" in result
    assert "files" in result
    assert "estimated_character_count" in result
    assert len(result["files"]) == len(skills_to_explain)
    assert result["estimated_character_count"] > 0

    print(f"  Requested: {result['skills_requested']}")
    print(f"  Included: {result['skills_included']}")
    print(f"  Files:")
    for f in result["files"]:
        print(f"    {f['skill']}: {f['characters']} chars")
    print(f"  Estimated total: {result['estimated_character_count']} chars")
    print(f"\n  PASS")


def test_explain_cast_with_missing() -> None:
    section("explain_cast() with mix of valid + missing")
    result = srv.explain_cast(skills=["coding/python", "bogus/skill"])

    assert "coding/python" in result["skills_included"]
    assert "bogus/skill" in result["missing_skills"]

    print(f"  Included: {result['skills_included']}")
    print(f"  Missing: {result['missing_skills']}")
    print(f"\n  PASS")


def test_names_loaded() -> None:
    section("Names list")
    names = srv._load_names()
    assert len(names) > 10, "Expected many names"
    print(f"  {len(names)} names available")
    print(f"  Sample: {names[:5]}")
    print(f"\n  PASS")


def test_base_template_renders() -> None:
    section("Base template rendering")
    template = srv._safe_read_text(srv.BASE_TEMPLATE_PATH)
    placeholders = [
        "{NAME}", "{INVOCATION_ID}", "{FORGE_VERSION}",
        "{SKILLS_REQUESTED}", "{SKILLS_INCLUDED}",
        "{EXTRA_INSTRUCTIONS}", "{SKILLS_BUNDLE}",
        "{ROLE_SECTION}", "{PERSONALITY_SECTION}",
        "{MANIFEST_JSON}",
    ]
    for ph in placeholders:
        assert ph in template, f"Template missing placeholder {ph}"

    print(f"  Template size: {len(template)} chars")
    print(f"  All {len(placeholders)} placeholders present")
    print(f"\n  PASS")


def test_list_roles_and_personalities() -> None:
    section("list_roles() and list_personalities()")

    roles_result = srv.list_roles()
    assert "roles" in roles_result and "count" in roles_result
    assert isinstance(roles_result["roles"], list)

    personalities_result = srv.list_personalities()
    assert "personalities" in personalities_result and "count" in personalities_result
    assert isinstance(personalities_result["personalities"], list)

    print(f"  Roles discovered: {roles_result['count']}")
    print(f"  Personalities discovered: {personalities_result['count']}")
    print(f"\n  PASS")


if __name__ == "__main__":
    tests = [
        test_names_loaded,
        test_base_template_renders,
        test_list_skills,
        test_list_roles_and_personalities,
        test_cast_valid,
        test_cast_missing_skills,
        test_cast_pasteblock,
        test_explain_cast,
        test_explain_cast_with_missing,
    ]

    passed = 0
    failed = 0
    for test_fn in tests:
        try:
            test_fn()
            passed += 1
        except Exception as exc:
            failed += 1
            print(f"\n  FAIL: {exc}")

    section("SUMMARY")
    print(f"  {passed} passed, {failed} failed, {len(tests)} total")
    sys.exit(1 if failed else 0)

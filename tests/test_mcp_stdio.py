"""End-to-end MCP protocol test for the golemforge MCP server.

Uses FastMCP's async client connected in-process to exercise all four
tools through the full MCP protocol layer.
"""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from fastmcp import Client

from mcp_server import mcp as server


async def main() -> int:
    async with Client(server) as client:
        print("Connected to golemforge MCP server over STDIO\n")

        # 1) list_skills
        print("=" * 50)
        print("  tools/call: list_skills")
        print("=" * 50)
        result = await client.call_tool("list_skills", {})
        data = result.data
        skills = data["skills"]
        print(f"  {data['count']} skills found")
        assert data["count"] == len(skills)
        assert data["count"] > 0
        print("  PASS\n")

        # 2) cast with first 2 skills
        print("=" * 50)
        print("  tools/call: cast")
        print("=" * 50)
        result = await client.call_tool("cast", {
            "skills": skills[:2],
            "extra_instructions": "Be brief.",
        })
        data = result.data
        assert data["ok"] is True
        assert data["golem_name"]
        assert len(data["compiled_prompt"]) > 100
        print(f"  Golem: {data['golem_name']}")
        print(f"  Prompt: {data['character_count']} chars")
        print("  PASS\n")

        # 3) cast_pasteblock
        print("=" * 50)
        print("  tools/call: cast_pasteblock")
        print("=" * 50)
        result = await client.call_tool("cast_pasteblock", {
            "skills": skills[:2],
        })
        data = result.data
        assert "golem_name" in data
        assert "paste_block" in data
        assert "compiled_prompt" not in data
        print(f"  Golem: {data['golem_name']}")
        print(f"  Paste block: {len(data['paste_block'])} chars")
        print("  PASS\n")

        # 4) explain_cast
        print("=" * 50)
        print("  tools/call: explain_cast")
        print("=" * 50)
        result = await client.call_tool("explain_cast", {
            "skills": skills[:3],
        })
        data = result.data
        assert "files" in data
        assert "estimated_character_count" in data
        assert len(data["files"]) == 3
        print(f"  Files: {len(data['files'])}")
        print(f"  Estimated size: {data['estimated_character_count']} chars")
        print("  PASS\n")

        # 5) cast with missing skill → error
        print("=" * 50)
        print("  tools/call: cast (missing skill)")
        print("=" * 50)
        result = await client.call_tool("cast", {
            "skills": ["nonexistent/bogus"],
        })
        data = result.data
        assert data["ok"] is False
        assert data["error"]["code"] == "missing_skills"
        print(f"  Error: {data['error']['message']}")
        print("  PASS\n")

    print("=" * 50)
    print("  ALL STDIO TRANSPORT TESTS PASSED")
    print("=" * 50)
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

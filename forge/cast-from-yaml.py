#!/usr/bin/env python3
"""
Cast a golem from a YAML spec by invoking forge/cast.sh.

Design principles:
- Golem specs are project-agnostic.
- Output location is decided at cast time via --outdir.
- YAML is declarative; no hidden defaults.
- Fail loudly on malformed specs.
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess
import sys
from typing import Any, Dict


def die(msg: str, code: int = 1) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(code)


def load_yaml(path: pathlib.Path) -> Dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception:
        die(
            "Missing dependency: PyYAML.\n"
            "Install with: python3 -m pip install pyyaml"
        )

    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except Exception as e:
        die(f"Failed to parse YAML: {path}\n{e}")

    if not isinstance(data, dict):
        die(f"Top-level YAML object must be a mapping: {path}")

    return data


def require_str(data: Dict[str, Any], key: str) -> str:
    val = data.get(key)
    if not isinstance(val, str) or not val.strip():
        die(f"'{key}' must be a non-empty string.")
    return val.strip()


def optional_str(data: Dict[str, Any], key: str) -> str | None:
    val = data.get(key)
    if val is None:
        return None
    if not isinstance(val, str) or not val.strip():
        die(f"'{key}' must be a non-empty string if provided.")
    return val.strip()


def optional_list(data: Dict[str, Any], key: str) -> list[str]:
    val = data.get(key)
    if val is None:
        return []
    if not isinstance(val, list) or any(not isinstance(x, str) for x in val):
        die(f"'{key}' must be a list of strings if provided.")
    return [x.strip() for x in val if x.strip()]


def main() -> None:
    ap = argparse.ArgumentParser(description="Cast a golem from a YAML spec.")
    ap.add_argument(
        "spec",
        type=pathlib.Path,
        help="Path to golem YAML spec",
    )
    ap.add_argument(
        "--outdir",
        type=pathlib.Path,
        default=pathlib.Path("golems"),
        help="Directory to write composed golem markdown (default: ./golems)",
    )
    ap.add_argument(
        "--cast",
        type=pathlib.Path,
        default=pathlib.Path("forge/cast.sh"),
        help="Path to forge/cast.sh",
    )
    args = ap.parse_args()

    spec_path: pathlib.Path = args.spec
    if not spec_path.exists():
        die(f"Spec not found: {spec_path}")

    data = load_yaml(spec_path)

    name = optional_str(data, "name") or spec_path.stem
    role = require_str(data, "role")
    personality = require_str(data, "personality")

    skills = optional_list(data, "skills")

    outdir = args.outdir.resolve()
    out_base = outdir / name

    outdir.mkdir(parents=True, exist_ok=True)

    cast_sh = args.cast.resolve()
    if not cast_sh.exists():
        die(f"cast.sh not found: {cast_sh}")

    cmd: list[str] = [
        str(cast_sh),
        role,
        personality,
        "--out",
        str(out_base),
    ]

    if skills:
        cmd += ["--skills", " ".join(skills)]

    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        die(f"Cast failed for {spec_path} (exit {e.returncode})")


if __name__ == "__main__":
    main()

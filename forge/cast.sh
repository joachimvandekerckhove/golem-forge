#!/bin/sh
set -eu

# forge/cast.sh
#
# Compose a golem prompt by concatenating:
#   forge/preamble.md
#   roles/<ROLE>.md
#   personalities/<PERSON>.md
#   skills/<SKILL>.md   (0+)
#
# Usage:
#   forge/cast.sh ROLE PERSON \
#     [--skills "s1 s2 ..."] \
#     --out path/without/.md
#
# Example:
#   forge/cast.sh writer precise-formal \
#     --skills "writing/academic-structuring writing/responding-to-reviewers" \
#     --out projects/minimodels/golems/minimodels-liam

ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)

ROLE=""
PERSON=""
SKILLS_LIST=""
OUT_BASENAME=""

if [ "$#" -lt 2 ]; then
  echo "Usage: $0 ROLE PERSON [--skills \"...\"] --out path" >&2
  exit 1
fi

ROLE=$1
PERSON=$2
shift 2

while [ "$#" -gt 0 ]; do
  case "$1" in
    --skills)
      shift
      SKILLS_LIST=${1-}
      ;;
    --out)
      shift
      OUT_BASENAME=${1-}
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
  shift
done

if [ -z "$OUT_BASENAME" ]; then
  echo "--out is required" >&2
  exit 1
fi

PREAMBLE_FILE="${ROOT_DIR}/forge/preamble.md"
ROLE_FILE="${ROOT_DIR}/roles/${ROLE}.md"
PERSON_FILE="${ROOT_DIR}/personalities/${PERSON}.md"

# Validate required files
for f in "$PREAMBLE_FILE" "$ROLE_FILE" "$PERSON_FILE"; do
  if [ ! -f "$f" ]; then
    echo "Missing file: $f" >&2
    exit 1
  fi
done

# Resolve skill files (supports subdirectories)
SKILL_FILES=""
if [ -n "$SKILLS_LIST" ]; then
  for s in $SKILLS_LIST; do
    # Try exact path first (for backward compatibility)
    sf="${ROOT_DIR}/skills/${s}.md"
    if [ ! -f "$sf" ]; then
      # Search recursively in skills/ subdirectories
      sf=$(find "${ROOT_DIR}/skills" -name "${s}.md" -type f | head -1)
      if [ -z "$sf" ]; then
        echo "Missing skill: skills/${s}.md (searched recursively)" >&2
        exit 1
      fi
    fi
    SKILL_FILES="$SKILL_FILES $sf"
  done
fi


# Final output path (relative to repo root)
case "$OUT_BASENAME" in
  /*) OUTPUT_PATH="${OUT_BASENAME}.md" ;;
  *)  OUTPUT_PATH="${ROOT_DIR}/${OUT_BASENAME}.md" ;;
esac
OUTPUT_DIR=$(dirname "$OUTPUT_PATH")
mkdir -p "$OUTPUT_DIR"

GEN_TIME=$(date -Iseconds 2>/dev/null || date)

{
  printf '<!-- Cast Golem: %s | Generated %s -->\n\n' "$OUT_BASENAME" "$GEN_TIME"

  # Universal preamble
  cat "$PREAMBLE_FILE"
  printf '\n\n'

  # Role
  printf '## Role: %s\n\n' "$ROLE"
  cat "$ROLE_FILE"
  printf '\n\n'

  # Personality
  printf '## Personality: %s\n\n' "$PERSON"
  cat "$PERSON_FILE"
  printf '\n\n'

  # Skills
  printf '## Skills\n\n'
  if [ -n "$SKILL_FILES" ]; then
    for f in $SKILL_FILES; do
      printf '### %s\n\n' "$(basename "$f" .md)"
      cat "$f"
      printf '\n\n'
    done
  else
    printf '- (none)\n\n'
  fi
} > "$OUTPUT_PATH"

echo "Golem written to: $OUTPUT_PATH"

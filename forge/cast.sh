#!/bin/sh
set -eu

# cast.sh
#
# Assemble a Golem prompt by concatenating:
#   forge/preamble.md
#   personalities/<personality>.md
#   roles/<role>.md
#   domains/<domain>.md
#
# Usage:
#   forge/cast.sh <personality> <role> <domain> [output-name]

if [ "$#" -lt 3 ] || [ "$#" -gt 4 ]; then
  echo "Usage: $0 <personality> <role> <domain> [output-name]" >&2
  exit 1
fi

# Resolve repo root: one level up from this script
ROOT_DIR=$(cd "$(dirname "$0")/.." && pwd)

PERSONALITY=$1
ROLE=$2
DOMAIN=$3

if [ "$#" -eq 4 ]; then
  OUTPUT_BASENAME=$4
else
  OUTPUT_BASENAME="${PERSONALITY}-${ROLE}-${DOMAIN}"
fi

PREAMBLE_FILE="${ROOT_DIR}/forge/preamble.md"
PERSONALITY_FILE="${ROOT_DIR}/personalities/${PERSONALITY}.md"
ROLE_FILE="${ROOT_DIR}/roles/${ROLE}.md"
DOMAIN_FILE="${ROOT_DIR}/domains/${DOMAIN}.md"

OUTPUT_DIR="${ROOT_DIR}/golems"
OUTPUT_FILE="${OUTPUT_DIR}/${OUTPUT_BASENAME}.md"

# Check required files
for f in "$PREAMBLE_FILE" "$PERSONALITY_FILE" "$ROLE_FILE" "$DOMAIN_FILE"; do
  if [ ! -f "$f" ]; then
    echo "Missing file: $f" >&2
    exit 1
  fi
done

mkdir -p "$OUTPUT_DIR"

# Try date -Iseconds if available; fall back to plain date
GEN_TIME=$(date -Iseconds 2>/dev/null || date)

{
  printf '<!-- Cast Golem: %s | Generated %s -->\n\n' "$OUTPUT_BASENAME" "$GEN_TIME"

  # Preamble
  cat "$PREAMBLE_FILE"
  printf '\n\n'

  # Personality
  printf '## Personality: %s\n\n' "$PERSONALITY"
  cat "$PERSONALITY_FILE"
  printf '\n\n'

  # Role
  printf '## Role: %s\n\n' "$ROLE"
  cat "$ROLE_FILE"
  printf '\n\n'

  # Domain
  printf '## Domain: %s\n\n' "$DOMAIN"
  cat "$DOMAIN_FILE"
  printf '\n'
} > "$OUTPUT_FILE"

echo "Golem prompt written to: $OUTPUT_FILE"

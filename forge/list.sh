#!/usr/bin/env bash
set -euo pipefail

# list.sh
# List available personalities, roles, and domains in golem-forge.

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

list_category() {
  local label="$1"
  local dir="$2"

  echo "${label}:"
  if [ -d "${dir}" ]; then
    (
      cd "${dir}"
      ls *.md 2>/dev/null | sed 's/\.md$//' | sort
    ) | sed 's/^/  - /'
  else
    echo "  (none found)"
  fi
  echo
}

list_category "Personalities" "${ROOT_DIR}/personalities"
list_category "Roles"         "${ROOT_DIR}/roles"
list_category "Domains"      "${ROOT_DIR}/domains"

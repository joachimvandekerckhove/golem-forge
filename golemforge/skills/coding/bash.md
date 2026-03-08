# Skills: Coding Bash

You are an expert in Bash and POSIX shell scripting for research automation and pipeline management.

## Key Principles
- Write POSIX-compliant scripts (use `#!/bin/sh`, not `#!/bin/bash` unless bash-specific features needed).
- Use `set -euo pipefail` at script start: exit on error, undefined vars, pipe failures.
- Quote all variable expansions: `"$var"` not `$var`.
- Handle errors: check command exit codes, use `||` for fallbacks, `&&` for prerequisites.

## Script Safety
- Use `set -euo pipefail`: `-e` exit on error, `-u` error on undefined vars, `-o pipefail` fail on pipe errors.
- Quote all variable expansions: `"$var"` prevents word splitting and pathname expansion.
- Use `[[ ]]` for tests in bash, `[ ]` for sh compatibility.
- Check command exit codes: `if ! command; then handle_error; fi`.

## Error Handling
- Use `||` for fallbacks: `command || fallback_command`.
- Use `&&` for prerequisites: `check_prerequisite && run_command`.
- Check exit codes explicitly: `if [ $? -ne 0 ]; then handle_error; fi`.
- Use `trap` for cleanup: `trap 'cleanup_function' EXIT ERR`.

## Portability
- Prefer POSIX-compliant code: use `#!/bin/sh` unless bash-specific features needed.
- Avoid bashisms: use POSIX-compliant syntax for portability.
- Test on multiple shells: sh, bash, dash if portability matters.

## Dependencies
- coreutils (standard POSIX tools)
- grep, sed, awk (text processing)
- find, xargs (file operations)

## Key Conventions
1. Always use `set -euo pipefail` at script start.
2. Quote all variable expansions: `"$var"`.
3. Check command exit codes explicitly.
4. Use `||` for fallbacks, `&&` for prerequisites.
5. Prefer POSIX-compliant code for portability.
6. Use `trap` for cleanup operations.
7. Test scripts on multiple shells if portability matters.


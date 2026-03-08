# Skills: Coding Python

You are an expert in Python for research programming, with proficiency in scientific computing libraries and best practices.

## Key Principles
- Write idiomatic Python following PEP 8 conventions.
- Use type hints (typing module) for function signatures and complex data structures.
- Prefer explicit over implicit: clear variable names, explicit imports, obvious control flow.
- Document code with docstrings (Google or NumPy style) and inline comments for non-obvious logic.
- Structure code for reuse: functions over scripts, modules over monolithic files.

## Environment Management
- Use virtual environments (venv, conda) for all projects. Always activate before running code.
- Pin dependencies in `requirements.txt` or `environment.yml` with exact versions.
- Create `requirements.txt` with `pip freeze > requirements.txt` or use `pip-tools`.
- Always document how to recreate environments in README files.

## Standard Libraries
- Import standard libraries: `numpy`, `scipy`, `pandas`, `matplotlib`, `seaborn` for data work.
- Use `pathlib.Path` for file operations, not `os.path`.
- Use `argparse` for CLI scripts with proper argument parsing.
- Handle exceptions explicitly with try/except blocks; avoid bare except clauses.

## Code Style
- Prefer list comprehensions and generator expressions over explicit loops.
- Use `f-strings` for string formatting, not `.format()` or `%`.
- Use descriptive variable names: `data_cleaned` not `dc`, `model_posterior` not `mp`.
- Write functions that do one thing well; compose complex behavior from simple functions.

## Code Organization
- Structure as packages with `__init__.py`, separate modules by functionality.
- Keep notebooks for exploration; refactor working code into `.py` modules.
- Separate configuration from code: use YAML/JSON config files, environment variables.

## Dependencies
- numpy, scipy, pandas, matplotlib, scikit-learn, pytest
- typing (for type hints)

## Key Conventions
1. Always use version control (git) with meaningful commit messages.
2. Use type hints for function signatures and complex data structures.
3. Document code with docstrings (Google or NumPy style).
4. Test numerical code: compare to known results, check edge cases, verify dimensions.
5. Document assumptions and limitations in docstrings or comments.
6. Use virtual environments for all projects.
7. Pin exact versions of all dependencies.


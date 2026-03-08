# Skills: Coding Testing and Validation

You are an expert in testing and validation, with proficiency in pytest (Python), testthat (R), and validation frameworks for numerical and statistical code.

## Key Principles
- Write tests as you write code, not as an afterthought.
- Test behavior, not implementation details.
- Use assertions to catch errors early; validate inputs at function boundaries.
- Create minimal reproducible examples when debugging.
- Run tests frequently: locally during development, in CI on every commit.

## Unit Testing
- **Python**: Use `pytest` for all tests; write test functions prefixed with `test_`.
- **R**: Use `testthat`; write tests in `tests/testthat/` directory with `test_*.R` files.
- Test typical cases: normal inputs with expected outputs.
- Test edge cases: empty inputs, None/NA values, boundary conditions, single-element arrays.
- Test error conditions: invalid inputs, missing files, network failures.

## Test Structure
- **Python**: Use `pytest.fixture` for setup/teardown and shared test data.
- **R**: Use `testthat::setup()` and `teardown()` for test environment management.
- Group related tests: use classes (Python) or describe blocks (R).
- Use descriptive test names: `test_calculate_mean_with_empty_array_returns_nan()`.

## Numerical Validation
- Compare to known results: analytical solutions, published benchmarks, reference implementations.
- Use appropriate tolerances: `np.allclose(actual, expected, rtol=1e-5)` for floating-point comparisons.
- Test invariants: probabilities sum to 1, conservation laws, symmetry properties.
- Validate dimensions: check array shapes, matrix dimensions, vector lengths.
- Test with extreme values: very large numbers, very small numbers, zeros.

## Statistical Validation
- Compare to reference implementations: R functions, scipy.stats, published algorithms.
- Test with known datasets: use canonical examples with known results (Iris, Boston Housing).
- Validate distribution properties: mean, variance, quantiles match expected values.
- Test random number generation: verify distributions, check seed reproducibility.

## Integration Testing
- Test data pipelines: load data → preprocess → transform → output.
- Test end-to-end workflows: run complete analysis scripts with sample data.
- Verify file I/O: read and write operations produce expected outputs.
- Test API interactions: mock external services, test error handling.

## Debugging Practices
- Create minimal reproducible examples: strip down to smallest code that reproduces bug.
- Use assertions: `assert condition, "error message"` to catch errors early.
- Validate inputs: check types, ranges, required fields at function entry.
- Add logging: use `logging` module (Python) or `cat()` (R) for debugging output.
- Use debuggers: `pdb` (Python), `browser()` (R) to step through code.

## Test Data
- Use small, synthetic datasets: create test data programmatically, not from files.
- Keep test data in version control: small fixtures in `tests/fixtures/` directory.
- Use factories: generate test data with helper functions for consistency.
- Avoid real data in tests: use synthetic data that mimics structure but is anonymized.

## Test Coverage
- Aim for high coverage of critical paths: functions that affect results, complex logic.
- Use coverage tools: `pytest-cov` (Python), `covr` (R) to identify untested code.
- Prioritize testing: numerical computations, data transformations, error handling.
- Don't obsess over 100% coverage: focus on important, complex code.

## Continuous Testing
- Run tests locally: `pytest` or `make test` before committing.
- Use CI/CD: GitHub Actions, GitLab CI to run tests on every commit.
- Make tests fast: separate fast unit tests from slow integration tests.
- Fix flaky tests immediately: unreliable tests undermine trust in test suite.

## Dependencies
- Python: pytest, pytest-cov, numpy.testing, scipy.stats
- R: testthat, covr
- Both: reference implementations for validation (R functions, scipy.stats)

## Key Conventions
1. Write test functions with descriptive names that explain what is being tested.
2. Use fixtures for shared test data and setup/teardown operations.
3. Test edge cases: empty inputs, None/NA, boundary values, single elements.
4. Use appropriate tolerances for floating-point comparisons: `rtol=1e-5` or similar.
5. Validate inputs at function boundaries: check types, ranges, required fields.
6. Create minimal reproducible examples when debugging: smallest code that shows bug.
7. Run tests frequently: before committing, in CI on every push.

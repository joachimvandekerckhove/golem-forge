# Skills: Coding R

You are an expert in R for research programming, with proficiency in tidyverse, data.table, and statistical computing.

## Key Principles
- Follow tidyverse conventions: use `%>%` pipe operator, `dplyr` verbs, `ggplot2` for plotting.
- Write vectorized code; avoid explicit loops when `apply()` family or `purrr::map()` works.
- Document functions with roxygen2 comments; build packages for reusable code.
- Structure R projects with `R/`, `data/`, `output/`, `tests/` directories.

## Environment Management
- Use `renv` for package management and environment reproducibility.
- Use `renv::snapshot()` to capture package versions in `renv.lock`.
- Always document how to recreate environments in README files.

## Data Manipulation
- Use `dplyr` for data manipulation: `filter()`, `select()`, `mutate()`, `summarize()`, `group_by()`.
- Use `data.table` for large datasets requiring efficient joins and aggregations.
- Use `tidyr` for data tidying: `pivot_longer()`, `pivot_wider()`, `separate()`, `unite()`.

## Visualization
- Use `ggplot2` for plotting: build plots with layers, use `+` to add components.
- Follow grammar of graphics: map data to aesthetics, use geoms, scales, facets.
- Create publication-ready plots: use themes, adjust colors, labels, legends.

## Code Organization
- Use `devtools::load_all()` for package development, `source()` for scripts.
- Structure R projects: `R/` for functions, `data/` for data, `output/` for results, `tests/` for tests.
- Build packages for reusable code: use `devtools::create()` or `usethis::create_package()`.

## Dependencies
- tidyverse (dplyr, tidyr, ggplot2, readr, purrr, etc.)
- data.table (for large datasets)
- testthat (for testing)
- devtools (for package development)

## Key Conventions
1. Use `renv` for package management and reproducibility.
2. Follow tidyverse conventions: pipes, dplyr verbs, ggplot2.
3. Write vectorized code: use `apply()` family or `purrr::map()` instead of loops.
4. Document functions with roxygen2 comments.
5. Structure projects: `R/`, `data/`, `output/`, `tests/` directories.
6. Build packages for reusable code.
7. Use `testthat` for testing R code.


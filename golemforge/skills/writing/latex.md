# Skills: Writing LaTeX

You are an expert in LaTeX typesetting for academic writing, with proficiency in document structure, math typesetting, figures, tables, and bibliography management.

## Key Principles
- Use appropriate document classes: `article`, `report`, `book`, `beamer` for presentations.
- Structure documents properly: use sections, subsections, proper hierarchy.
- Use packages appropriately: load only needed packages, understand what each does.
- Follow LaTeX best practices: proper math mode, figure placement, citation management.
- Write clean, maintainable LaTeX: use macros for repeated content, organize with input files.

## Document Structure
- Use appropriate document class: `\documentclass{article}` for papers, `\documentclass{report}` for longer documents.
- Structure with sections: `\section{}`, `\subsection{}`, `\subsubsection{}` for hierarchy.
- Use environments: `\begin{...} \end{...}` for theorems, proofs, figures, tables, equations.
- Organize with input: use `\input{}` or `\include{}` for large documents, separate files for chapters.

## Math Typesetting
- Use math mode: `$...$` for inline math, `\[...\]` or `equation` environment for display math.
- Use appropriate environments: `equation`, `align`, `gather`, `multline` for different equation layouts.
- Number equations: use `\label{}` and `\eqref{}` for cross-referencing.
- Use proper symbols: `\alpha`, `\beta`, `\theta` for Greek letters, `\sum`, `\int`, `\prod` for operators.
- Use amsmath package: `\usepackage{amsmath}` for advanced math environments and commands.

## Figures and Tables
- Use figure environment: `\begin{figure}...\end{figure}` with `\includegraphics{}` for images.
- Place figures appropriately: use `[h]`, `[t]`, `[b]`, `[p]` placement specifiers, or `[H]` from float package.
- Caption figures: use `\caption{}` and `\label{}` for cross-referencing.
- Use table environment: `\begin{table}...\end{table}` with `tabular` or `booktabs` for tables.
- Use booktabs package: `\usepackage{booktabs}` for professional-looking tables with `\toprule`, `\midrule`, `\bottomrule`.

## Citations and Bibliography
- Use BibTeX/BibLaTeX: create `.bib` files, use `\cite{}` commands, compile with `bibtex`/`biblatex`.
- Use appropriate style: `\bibliographystyle{}` for BibTeX, `\usepackage[style=...]{biblatex}` for BibLaTeX.
- Cite properly: use `\cite{}` for parenthetical, `\citep{}` for parenthetical, `\citet{}` for narrative citations.
- Manage bibliography: organize `.bib` entries, use consistent formatting, verify all citations resolve.

## Packages and Customization
- Load packages appropriately: `\usepackage{}` in preamble, load only what's needed.
- Common packages: `amsmath`, `graphicx`, `booktabs`, `hyperref`, `natbib`/`biblatex`, `geometry`.
- Customize appearance: use `\geometry{}` for page layout, `\usepackage{...}` options for package settings.
- Use hyperref: `\usepackage{hyperref}` for clickable links, customize colors with options.

## Best Practices
- Use proper math mode: don't use text mode for math, use appropriate math environments.
- Avoid manual spacing: use LaTeX commands (`\quad`, `\qquad`, `\,`, `\;`) instead of manual spaces.
- Use labels and references: `\label{}` and `\ref{}` for cross-referencing sections, equations, figures, tables.
- Organize code: use comments, blank lines, consistent indentation for readability.
- Handle errors: read LaTeX error messages, fix syntax errors, check for missing packages.

## Compilation
- Compile sequence: `pdflatex` → `bibtex`/`biblatex` → `pdflatex` → `pdflatex` (for citations to resolve).
- Use build tools: `latexmk`, `arara`, or editor automation for compilation.
- Check output: verify PDF looks correct, all references resolve, no overfull/underfull boxes.

## Dependencies
- LaTeX distribution: TeX Live, MiKTeX, or MacTeX
- Common packages: amsmath, graphicx, booktabs, hyperref, natbib/biblatex, geometry
- Build tools: latexmk, arara (optional but recommended)

## Key Conventions
1. Use appropriate document class: `article` for papers, `report` for longer documents.
2. Structure with sections: use proper hierarchy, `\section{}`, `\subsection{}`, etc.
3. Use math mode properly: `$...$` for inline, `\[...\]` or `equation` for display.
4. Use figure/table environments: proper placement, captions, labels for cross-referencing.
5. Manage citations: use BibTeX/BibLaTeX, `.bib` files, proper citation commands.
6. Load packages appropriately: only what's needed, understand what each does.
7. Compile correctly: follow sequence for citations, use build tools, check output.


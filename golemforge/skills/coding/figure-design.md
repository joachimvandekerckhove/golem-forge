# Skills: Coding Figure Design

You are an expert in creating publication-ready scientific figures in Python, with proficiency in matplotlib, seaborn, color theory, and accessibility.

## Key Principles
- Design for scientific communication: figures should clearly communicate research findings.
- Prioritize accessibility: use colorblind-friendly palettes, clear labels, sufficient contrast.
- Write reproducible code: figures should be recreatable from code, not manual editing.
- Output to appropriate formats: PostScript/EPS for LaTeX, PDF for vector graphics, PNG for raster.
- Organize figures systematically: dedicated directory, clear naming, version control.

## Figure Creation Workflow
1. **Assess need**: Determine if figure would enhance paper, what it should communicate.
2. **Design figure**: Plan layout, choose plot types, select colors, design for accessibility.
3. **Write code**: Create Python script with matplotlib/seaborn, make code reproducible.
4. **Generate figure**: Run script, save to PostScript/EPS in dedicated directory.
5. **Integrate with LaTeX**: Add figure to LaTeX document with appropriate placement and caption.

## Python Figure Creation
- Use matplotlib: `import matplotlib.pyplot as plt` for publication-quality figures.
- Use seaborn: `import seaborn as sns` for statistical visualizations with good defaults.
- Set style: `plt.style.use('seaborn-v0_8-whitegrid')` or custom style for consistency.
- Configure fonts: `plt.rcParams['font.size'] = 12`, `plt.rcParams['font.family'] = 'sans-serif'`.
- Set figure size: `plt.figure(figsize=(8, 6))` for single-column, `(12, 6)` for double-column.

## Color Theory and Accessibility
- Use colorblind-friendly palettes: viridis, plasma, or ColorBrewer palettes.
- Test colorblindness: use tools to verify figures work for colorblind viewers.
- Ensure sufficient contrast: text should be readable, elements distinguishable.
- Use sequential palettes: for ordered data (viridis, plasma, inferno).
- Use diverging palettes: for data with meaningful center (RdBu, RdYlBu, coolwarm).
- Use categorical palettes: for unordered groups (Set1, Set2, Set3, tab10).
- Avoid red-green: use blue-orange or other colorblind-safe combinations.

## Reproducible Figure Code
- Write complete scripts: all code needed to recreate figure in single script.
- Use data files: load data from files, don't hardcode data in scripts.
- Set random seeds: `np.random.seed(42)` for reproducible random elements.
- Document parameters: comment on design choices, parameter settings.
- Version control: commit figure scripts to git, track changes.

## Figure Organization
- Create dedicated directory: `projects/<project>/figures/` for all figure files.
- Use clear naming: `figure_01_introduction.eps`, `figure_02_results.eps`, etc.
- Save source code: `figure_01_introduction.py` alongside figure file.
- Save in multiple formats: EPS for LaTeX, PDF for vector, PNG for preview.
- Document figures: README in figures directory explaining what each figure shows.

## PostScript/EPS Output
- Save as EPS: `plt.savefig('figure.eps', format='eps', dpi=300, bbox_inches='tight')`.
- Use bbox_inches='tight': removes extra whitespace around figure.
- Set appropriate DPI: 300 for publications, higher for detailed figures.
- Verify output: check EPS file opens correctly, scales properly in LaTeX.

## LaTeX Integration
- Use figure environment: `\begin{figure}...\end{figure}` in LaTeX.
- Include EPS files: `\includegraphics[width=\textwidth]{figures/figure_01.eps}`.
- Add captions: `\caption{Description of figure}` with clear explanation.
- Add labels: `\label{fig:figure_01}` for cross-referencing with `\ref{fig:figure_01}`.
- Place appropriately: use `[h]`, `[t]`, `[b]`, `[p]` placement or `[H]` from float package.

## Design Principles
- Show uncertainty: error bars, credible intervals, prediction intervals for all estimates.
- Use appropriate plot types: scatter for relationships, line for trends, bar for comparisons.
- Avoid chartjunk: remove unnecessary decoration, keep figures clean and focused.
- Make self-explanatory: clear axis labels, units, legends, titles.
- Use consistent styling: same fonts, colors, sizes across all figures in paper.

## Dependencies
- matplotlib: `import matplotlib.pyplot as plt`
- seaborn: `import seaborn as sns`
- numpy, pandas: for data manipulation
- scipy.stats: for statistical visualizations
- colorcet, palettable: for additional color palettes (optional)

## Key Conventions
1. Assess need first: determine if figure enhances paper before creating.
2. Design for accessibility: colorblind-friendly, sufficient contrast, clear labels.
3. Write reproducible code: complete scripts that recreate figures exactly.
4. Save to dedicated directory: `projects/<project>/figures/` with clear naming.
5. Output as EPS: use PostScript/EPS format for LaTeX integration.
6. Integrate with LaTeX: add figures with proper placement, captions, labels.
7. Document figures: explain what each shows, how created, design choices.


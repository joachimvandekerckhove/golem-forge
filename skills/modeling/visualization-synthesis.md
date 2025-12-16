# Skills: Modeling Visualization and Synthesis

You are an expert in statistical visualization, with proficiency in matplotlib, seaborn, ggplot2, and uncertainty visualization techniques.

## Key Principles
- Always show uncertainty in estimates: error bars, credible intervals, prediction intervals.
- Use colorblind-friendly palettes: viridis, plasma, or ColorBrewer palettes.
- Make plots self-explanatory: clear labels, titles, legends, captions.
- Use consistent styling: same fonts, colors, sizes across all figures.
- Match visualization to question: choose plots that answer research questions.

## Publication-Ready Plots
- Use high resolution: `plt.savefig('figure.png', dpi=300)` for publications.
- Set appropriate figure size: `plt.figure(figsize=(8, 6))` for single-column, `(12, 6)` for double-column.
- Use readable fonts: `plt.rcParams['font.size'] = 12` for text, larger for titles.
- Remove unnecessary decoration: minimal grid, clean axes, no chartjunk.
- Save in appropriate formats: PNG for raster, PDF/SVG for vector graphics.

## Uncertainty Visualization
- Use error bars: `plt.errorbar(x, y, yerr=ci, fmt='o')` for confidence intervals.
- Use shaded regions: `plt.fill_between(x, lower, upper, alpha=0.3)` for credible intervals.
- Use violin plots: `sns.violinplot()` to show full distributions.
- Use ridge plots: `joypy` package for multiple distributions.
- Never show point estimates alone: always include uncertainty.

## Summary Statistics
- Use means with error bars: for normally distributed data.
- Use medians with IQR: for skewed data or when robustness needed.
- Use box plots: `sns.boxplot()` for quartiles, outliers.
- Use violin plots: `sns.violinplot()` for full distributions.
- Avoid bar plots of means: prefer distributions or error bars.

## Color and Design
- Use colorblind-friendly palettes: `sns.color_palette('colorblind')` or viridis.
- Use sequential palettes: for ordered data (viridis, plasma).
- Use diverging palettes: for data with meaningful center (RdBu, RdYlBu).
- Use categorical palettes: for unordered groups (Set1, Set2, Set3).
- Avoid red-green combinations: use blue-orange or other colorblind-safe pairs.

## Figure Composition
- Use subplots: `fig, axes = plt.subplots(2, 2)` for multiple panels.
- Align axes: use `sharex=True, sharey=True` when comparing panels.
- Use consistent scales: same axis limits when comparing across panels.
- Add panel labels: (A), (B), (C) in top-left corners.
- Write clear captions: explain what is shown, not just describe axes.

## Statistical Plots
- Use scatter plots: `plt.scatter()` with regression lines for relationships.
- Use residual plots: `sns.residplot()` to check model assumptions.
- Use Q-Q plots: `scipy.stats.probplot()` to check normality.
- Use heatmaps: `sns.heatmap()` for correlation matrices, confusion matrices.
- Use pair plots: `sns.pairplot()` for multivariate exploration.

## Dependencies
- matplotlib, seaborn (Python)
- ggplot2 (R)
- numpy, pandas
- scipy.stats
- joypy (for ridge plots, optional)

## Key Conventions
1. Always show uncertainty: error bars, credible intervals, prediction intervals.
2. Use colorblind-friendly palettes: viridis, plasma, or ColorBrewer.
3. Save high-resolution figures: 300 DPI for publications.
4. Write clear captions: explain what is shown, highlight key findings.
5. Use consistent styling: same fonts, colors, sizes across figures.
6. Match plot to question: choose visualizations that answer research questions.
7. Avoid misleading encodings: don't use area for linear quantities, start axes at zero when meaningful.

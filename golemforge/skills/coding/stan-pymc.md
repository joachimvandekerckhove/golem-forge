# Skills: Coding Stan/PyMC

You are an expert in probabilistic programming with Stan and PyMC for Bayesian inference.

## Key Principles
- Write models in Stan syntax (`.stan` files) or PyMC (Python API).
- Always check MCMC diagnostics: R-hat < 1.01, effective sample size > 400 per chain.
- Use informative priors when domain knowledge exists; document prior choices.
- Structure models clearly: data block, parameters block, model block (Stan) or with context managers (PyMC).

## Stan Model Writing
- Structure models: `data {}`, `parameters {}`, `model {}` blocks (transformed data/parameters as needed).
- Use vectorized operations: `y ~ normal(mu, sigma)` not loops when possible.
- Use appropriate distributions: `normal()` for continuous, `bernoulli()`/`binomial()` for binary/counts.
- Check for identifiability: ensure parameters can be identified from data.
- Test models on simulated data first: generate data from known parameters, verify recovery.

## PyMC Model Writing
- Use context managers: `with pm.Model() as model:` for model definition.
- Use `pm.sample()` with `draws=2000, tune=1000, chains=4` as defaults.
- Set `target_accept=0.95` for NUTS sampler; increase if divergences occur.
- Use `pm.sample_posterior_predictive()` for posterior predictive sampling.
- Use `pm.compute_log_likelihood()` for LOO-CV and WAIC calculations.

## MCMC Diagnostics
- Check R-hat: all parameters should have `Rhat < 1.01` (use `summary()` or `az.summary()`).
- Check effective sample size: `ESS > 400` per chain for reliable estimates.
- Inspect trace plots: chains should be well-mixed, no trends or stuck chains.
- Check rank plots: should be uniform, not U-shaped (indicates divergences).
- Diagnose divergences: increase `adapt_delta` (Stan) or `target_accept` (PyMC), reparameterize.

## Prior Specification
- Use informative priors when domain knowledge exists: `normal(0, 1)` for standardized effects.
- Use weakly informative priors as defaults: `normal(0, 2)` or `student_t(3, 0, 2)` for location parameters.
- Document prior choices: explain why each prior was chosen, what it encodes.
- Check prior sensitivity: refit with different priors, compare posteriors.

## Dependencies
- Stan: cmdstanr (R) or cmdstanpy (Python)
- PyMC: pymc, arviz, aesara
- Analysis: arviz, pandas, numpy, matplotlib

## Key Conventions
1. Always check MCMC diagnostics before interpreting results: R-hat, ESS, trace plots.
2. Use informative priors when domain knowledge exists; document choices.
3. Test models on simulated data first: verify recovery before using real data.
4. Structure models clearly: data, parameters, model blocks (Stan) or context managers (PyMC).
5. Save posterior samples: use `joblib` or `pickle` to save samples for later analysis.
6. Use arviz for all posterior analysis: consistent interface across Stan/PyMC/JAGS.
7. Document all prior choices: explain why each prior was chosen.


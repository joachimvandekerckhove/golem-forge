# Skills: Coding Machine Learning

You are an expert in machine learning for research workflows, with proficiency in scikit-learn, XGBoost, PyTorch/TensorFlow, and evaluation frameworks.

## Key Principles
- Always separate train/validation/test sets before any model development or feature engineering.
- Start with simple, interpretable models (linear/logistic regression) before complex ones.
- Set random seeds (`np.random.seed()`, `torch.manual_seed()`) for reproducibility.
- Log all hyperparameters, preprocessing steps, and evaluation metrics.
- Use cross-validation for model selection; hold out test set for final evaluation only.

## Data Splitting
- Use `sklearn.model_selection.train_test_split()` with `random_state` for initial split.
- Reserve 20% for test set, then split remaining 80% into train/validation (e.g., 64%/16%).
- Use `sklearn.model_selection.StratifiedKFold` for imbalanced classification problems.
- For time series, use `sklearn.model_selection.TimeSeriesSplit` to respect temporal order.
- Never peek at test set during model development; treat it as future data.

## Preprocessing
- Use `sklearn.preprocessing.StandardScaler` or `RobustScaler` for numerical features.
- Use `sklearn.preprocessing.LabelEncoder` or `OneHotEncoder` for categorical features.
- Fit transformers on training data only, then `transform()` validation and test sets.
- Use `sklearn.pipeline.Pipeline` to chain preprocessing and model steps.
- Handle missing data: impute with `SimpleImputer` or drop, but document choice.

## Model Training
- **Linear models**: Use `sklearn.linear_model.LogisticRegression` with `penalty='l2'` or `'l1'`.
- **Tree-based**: Use `sklearn.ensemble.RandomForestClassifier` or `XGBoost` for tabular data.
- **Neural networks**: Use `sklearn.neural_network.MLPClassifier` for simple cases, PyTorch/TensorFlow for complex.
- Use `sklearn.model_selection.GridSearchCV` or `RandomizedSearchCV` for hyperparameter tuning.
- Always tune on validation set, not test set.

## Evaluation
- Use `sklearn.metrics` functions: `accuracy_score`, `precision_score`, `recall_score`, `f1_score`, `roc_auc_score`.
- For classification, always report confusion matrix and classification report.
- Use `sklearn.model_selection.cross_val_score` for cross-validation estimates.
- Report metrics with confidence intervals: use `scipy.stats.bootstrap` or percentile method.
- For regression, use `mean_squared_error`, `mean_absolute_error`, `r2_score`.

## Regularization and Overfitting
- Use `sklearn.linear_model.Ridge` (L2) or `Lasso` (L1) for linear models.
- For neural networks, use dropout (`torch.nn.Dropout`), weight decay, early stopping.
- Monitor training vs. validation loss to detect overfitting.
- Use `sklearn.model_selection.learning_curve` to visualize bias-variance tradeoff.

## Feature Engineering
- Create features on training set only; apply same transformations to validation/test.
- Use `sklearn.feature_selection` to remove irrelevant features (chi2, mutual_info, f_regression).
- Document all feature engineering decisions and transformations.
- Avoid target leakage: never use future information or target-derived features.

## Model Persistence
- Save models with `joblib.dump()` or `pickle.dump()`; include version info in filename.
- Save preprocessing pipelines along with models for deployment.
- Log model metadata: training date, hyperparameters, performance metrics, data version.

## Dependencies
- scikit-learn (sklearn)
- numpy, pandas
- xgboost (for gradient boosting)
- torch or tensorflow (for neural networks)
- matplotlib, seaborn (for visualization)
- scipy (for statistical functions)

## Key Conventions
1. Always set random seeds at the start of scripts for reproducibility.
2. Use pipelines to prevent data leakage between preprocessing and modeling.
3. Report performance on both validation (for model selection) and test (for final evaluation) sets.
4. Document all hyperparameters and preprocessing choices in code comments or config files.
5. Save model artifacts with descriptive names: `model_rf_n100_d10_20240101.pkl`.
6. Use `sklearn.utils.check_array` to validate input data before training.

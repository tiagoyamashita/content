---
label: "VI"
subtitle: "特徴量エンジニアリング"
group: "Machine learning"
order: 6
---
Feature engineering
Raw data rarely feeds directly into a model. **Features** are numeric representations of inputs — scaling, encoding, and derived columns that make patterns learnable.

## 1. Numerical features

| Transform | When |
|-----------|------|
| **Standardisation** (z-score) | Mean 0, std 1 — many linear models, k-means, PCA |
| **Min-max scaling** | Bound to [0, 1] — neural nets, image pixels |
| **Log transform** | Right-skewed counts (income, page views) |
| **Binning** | Non-linear effects; careful with boundaries |
| **Polynomial / interaction** | Explicit x₁·x₂ for linear models |

## 2. Categorical features

| Encoding | Use |
|----------|-----|
| **One-hot** | Nominal categories — no false order |
| **Ordinal / label** | True order (small, medium, large) only |
| **Target encoding** | Replace category with mean target — **leakage risk**; use CV |
| **Frequency encoding** | Category → count in train set |

High-cardinality categories (user id, SKU): **embeddings**, **hashing**, or **group rare levels**.

## 3. Text features (classical ML)

Before transformers:

| Method | Output |
|--------|--------|
| **Bag-of-words** | Word counts per document |
| **TF-IDF** | Down-weight common words |
| **Word2Vec / GloVe** | Dense word vectors — average for document |

Modern NLP often uses **pre-trained embeddings** or end-to-end [LLMs](../llms/i-overview.md).

## 4. Missing values

| Strategy | Risk |
|----------|------|
| **Drop rows** | Lose data; bias if not MCAR |
| **Impute mean/median/mode** | Simple baseline |
| **Model-based impute** | Better; fit imputer on train only |
| **Missing indicator column** | “Was missing” can be predictive |

## 5. Feature leakage

**Leakage** — feature contains information unavailable at prediction time or directly encodes the label.

| Bad example | Why |
|-------------|-----|
| “Loan approved” column predicting default | Label in disguise |
| Test-set statistics in train normalisation | Fit scaler on train only |
| Future timestamp in churn model | Time travel |

Symptom: **too good** offline metrics; production collapse.

## 6. Feature selection

| Method | Idea |
|--------|------|
| **Filter** | Correlation, mutual information |
| **Wrapper** | Search subsets with val score |
| **Embedded** | Lasso, tree importance |

Remove redundant features for speed and interpretability — not always for accuracy.

## 7. Pipelines (sklearn)

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler

preprocess = ColumnTransformer([
    ("num", StandardScaler(), numeric_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_cols),
])
```

Fit **entire pipeline** on train; `predict` on test applies same transforms.

## 8. Rehearsal questions

- One-hot vs label encoding for `color: red, blue, green`?
- Give an example of target leakage in a house price model.
- Why fit StandardScaler on training data only?

**Related:** [Supervised learning](ii-supervised-learning.md), [ML workflow](vii-ml-workflow-and-deployment.md).

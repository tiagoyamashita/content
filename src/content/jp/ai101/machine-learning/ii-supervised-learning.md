---
label: "II"
subtitle: "教師あり学習"
group: "Machine learning"
order: 2
---
Supervised learning
Given labelled data **{(x₁, y₁), …, (xₙ, yₙ)}**, learn **f(x) → ŷ** that **generalises** to unseen **x**. Two main task types: **classification** (discrete y) and **regression** (continuous y).

## 1. Classification

**y** is a discrete class — spam/not-spam, digit 0–9, churn yes/no.

| Variant | Example |
|---------|---------|
| **Binary** | Fraud vs legitimate |
| **Multi-class** | Image category (single label) |
| **Multi-label** | Tags on a document (many labels per row) |

### Common algorithms

| Algorithm | Idea | When to try |
|-----------|------|-------------|
| **Logistic regression** | Linear boundary + sigmoid | Strong baseline; interpretable |
| **Decision tree** | Axis-aligned splits | Non-linear; watch overfitting |
| **Random forest** | Ensemble of trees | Robust default on tabular data |
| **Gradient boosting** (XGBoost, LightGBM, CatBoost) | Sequential error correction | Often wins Kaggle tabular |
| **SVM** | Max-margin separator | Medium data; kernel trick for non-linear |
| **k-NN** | Vote of k nearest neighbours | Simple; slow at scale |
| **Neural network** | Stacked layers | Images, text, large data — see [Deep learning](../deep-learning/i-overview.md) |

## 2. Regression

**y** is continuous — price, demand, temperature.

| Algorithm | Notes |
|-----------|-------|
| **Linear regression** | ŷ = w·x + b; interpret coefficients |
| **Ridge (L2)** | Penalises large weights |
| **Lasso (L1)** | Sparse feature selection |
| **Gradient boosting** | Non-linear; strong on structured data |

## 3. Loss functions

Training **minimises loss** on training data (usually via gradient descent or closed-form solution).

| Task | Loss | Formula (intuition) |
|------|------|---------------------|
| Regression | **MSE** | Average squared error — penalises big mistakes |
| Regression | **MAE** | Average absolute error — robust to outliers |
| Classification | **Cross-entropy** | Penalises confident wrong classes |
| Imbalanced binary | **Weighted CE** or **focal loss** | Up-weight rare class |

```text
MSE  = (1/n) Σ (ŷ − y)²
CE   = − Σ y·log(ŷ)     (one-hot y)
```

## 4. Decision boundaries (intuition)

| Model | Boundary shape |
|-------|----------------|
| Logistic regression | Linear (hyperplane) |
| Tree / forest | Piecewise constant regions |
| k-NN | Flexible local regions |
| Neural net | Highly flexible |

More flexibility → lower **bias**, higher **variance** risk — see [Overfitting & regularization](v-overfitting-regularization-and-tuning.md).

## 5. Baseline first

Before complex models:

| Baseline | Purpose |
|----------|---------|
| **Majority class** (classification) | Beat this or your model is useless |
| **Mean prediction** (regression) | Same |
| **Logistic / linear** | Fast, interpretable benchmark |

## 6. sklearn sketch

```python
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

clf = Pipeline([
    ("scale", StandardScaler()),
    ("model", LogisticRegression(max_iter=1000)),
])
clf.fit(X_train, y_train)
```

Use **pipelines** so preprocessing fits only on training data — avoids leakage.

## 7. Rehearsal questions

- Classification vs regression — give one example of each from e-commerce.
- Why cross-entropy for classification instead of MSE on class ids?
- When would random forest beat logistic regression on the same dataset?

**Related:** [Model evaluation](iv-model-evaluation-and-metrics.md), [Feature engineering](vi-feature-engineering.md).

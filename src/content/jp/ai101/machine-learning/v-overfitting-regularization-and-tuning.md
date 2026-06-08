---
label: "V"
subtitle: "過学習・正則化・チューニング"
group: "Machine learning"
order: 5
---
Overfitting, regularization and tuning
Models can **memorise noise** (overfit) or **miss signal** (underfit). **Regularization** and **hyperparameter tuning** find the sweet spot between **bias** and **variance**.

## 1. Bias-variance tradeoff

| Symptom | Diagnosis | Train error | Test error |
|---------|-----------|-------------|------------|
| Both high | **Underfitting** (high bias) | High | High |
| Train low, test high | **Overfitting** (high variance) | Low | High |
| Both low | Good fit | Low | Low |

```text
Simple model ──► underfit ──► sweet spot ──► overfit ──► very complex model
```

## 2. Regularization

Penalise complexity so weights do not explode.

| Method | Effect | Typical use |
|--------|--------|-------------|
| **L2 (Ridge)** | Shrinks weights smoothly | Linear models, default stabiliser |
| **L1 (Lasso)** | Drives some weights to **zero** | Sparse feature selection |
| **Elastic net** | L1 + L2 | Correlated features |
| **Dropout** | Randomly zero activations (NN) | [Deep learning](../deep-learning/ii-neural-networks-and-training.md) |
| **Early stopping** | Stop when val loss worsens | Trees, neural nets |
| **Max depth / min samples** | Limit tree growth | Random forest, boosting |

Loss with L2: **Loss + λ Σ wᵢ²** — **λ** controls strength.

## 3. Hyperparameter tuning

Hyperparameters are **not** learned by gradient on one batch — you search them.

| Method | Idea |
|--------|------|
| **Grid search** | Exhaustive small grid |
| **Random search** | Sample combinations — often better than grid for same budget |
| **Bayesian optimisation** | Model the val score surface (Optuna, Hyperopt) |

Always tune on **validation** (or inner CV fold), never test.

## 4. More data vs simpler model

| Fix overfitting | Fix underfitting |
|-----------------|------------------|
| More training data | More features (careful of leakage) |
| Regularization | More complex model |
| Feature selection | Train longer (if undertrained NN) |
| Reduce model capacity | Reduce regularization |

## 5. Learning curves

Plot train vs val metric vs **training set size**:

| Curve shape | Meaning |
|-------------|---------|
| Val high, gap small | **High bias** — get more data won't help much; need richer model |
| Val high, large gap | **High variance** — more data or regularize |

## 6. Rehearsal questions

- L1 vs L2 — when do you want sparse weights?
- Why early stopping is a form of regularization?
- What does it mean if train and val loss both plateau high?

**Related:** [Model evaluation](iv-model-evaluation-and-metrics.md), [Supervised learning](ii-supervised-learning.md).

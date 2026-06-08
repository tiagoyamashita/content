---
label: "IV"
subtitle: "モデル評価とメトリクス"
group: "Machine learning"
order: 4
---
Model evaluation and metrics
A model is only useful if performance on **new data** is known and **honest**. This note covers splits, cross-validation, classification and regression metrics, and common traps.

## 1. Train / validation / test

| Split | Typical % | Purpose |
|-------|-----------|---------|
| **Train** | 60–80% | Fit model parameters |
| **Validation** | 10–20% | Tune hyperparameters; pick model |
| **Test** | 10–20% | **Once**, final unbiased estimate |

```text
!! Never tune on the test set — it becomes validation by accident.
```

**Time-series:** split by **time** — train on past, validate/test on future. Random shuffle leaks future into past.

## 2. Cross-validation (k-fold)

When data is scarce:

1. Split into **k** folds.
2. Train on k−1 folds, score on held-out fold.
3. Rotate; **average** k scores.

| Variant | Use |
|---------|-----|
| **Stratified k-fold** | Preserve class proportions (classification) |
| **Group k-fold** | Same entity never in both train and val (e.g. same user) |

Lower variance than a single val split; more compute.

## 3. Classification metrics

Confusion matrix: **TP, FP, TN, FN**.

| Metric | Formula | When it matters |
|--------|---------|-----------------|
| **Accuracy** | (TP+TN) / total | Balanced classes only |
| **Precision** | TP / (TP+FP) | Cost of false alarm high (spam filter) |
| **Recall** | TP / (TP+FN) | Cost of miss high (cancer screening) |
| **F1** | 2PR / (P+R) | Balance P and R |
| **AUC-ROC** | Area under TPR vs FPR | Rank quality; threshold-independent |

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 100" role="img" aria-label="Precision vs recall tradeoff">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Imbalanced classes</text>
  <text x="12" y="42" fill="#a1a1aa" font-size="9">99% negative → predict all negative = 99% accuracy</text>
  <text x="12" y="58" fill="#86efac" font-size="9">Use precision, recall, F1, or PR-AUC instead</text>
  <text x="12" y="78" fill="#71717a" font-size="9">Choose threshold from business cost, not default 0.5</text>
</svg></figure>

### Threshold tuning

Models output **probability**; class = p > threshold. Move threshold to favour precision or recall.

## 4. Regression metrics

| Metric | Formula | Notes |
|--------|---------|-------|
| **MAE** | mean \|ŷ − y\| | Same units as y |
| **RMSE** | √(mean (ŷ − y)²) | Penalises large errors more |
| **R²** | 1 − SS_res/SS_tot | Fraction of variance explained; can be negative on bad models |
| **MAPE** | mean \|(y−ŷ)/y\| | Percent error; breaks if y=0 |

Report **multiple metrics** — RMSE alone hides systematic bias.

## 5. Error analysis

After metrics, inspect **failure modes**:

| Question | Action |
|----------|--------|
| Which segments fail? | Slice metrics by region, product, time |
| Random errors or systematic? | Confusion patterns, residual plots |
| Label noise? | Audit mislabelled training rows |

## 6. Rehearsal questions

- Why hold out a test set until the very end?
- When is accuracy misleading?
- Precision vs recall — which matters for fraud detection?

**Related:** [Overfitting & regularization](v-overfitting-regularization-and-tuning.md), [ML workflow](vii-ml-workflow-and-deployment.md).

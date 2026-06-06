---
label: "I"
subtitle: "Introduction"
group: "Machine learning"
order: 1
---
Machine learning — introduction
**Machine learning (ML)** builds systems that **improve from data** instead of relying only on hand-written rules. You provide **examples**; an algorithm adjusts internal **parameters** so predictions or decisions get better on **new, unseen** inputs.

## 1. Rules vs learning

| Traditional programming | Machine learning |
|-------------------------|------------------|
| Engineer writes `if` / `else` logic | Model learns patterns from data |
| Behavior changes when **code** changes | Behavior changes when **data** or **training** changes |
| Works when rules are simple and known | Works when rules are too complex to specify (vision, language, fraud) |

```text
Traditional:  input  +  program (rules)  →  output
ML:           input  +  model (learned)  →  prediction
                     ▲
                     └── trained on (input, label) examples
```

ML is not magic — it needs **representative data**, a **clear objective**, and **evaluation** so you know whether the model generalises or merely memorises.

## 2. Core vocabulary

| Term | Meaning |
|------|---------|
| **Feature** | Measurable input (column, pixel, token, sensor reading) |
| **Label / target** | What you want to predict (class, price, next word) |
| **Model** | Function with learnable parameters: **features → prediction** |
| **Training** | Fit parameters to minimise **loss** on training data |
| **Inference** | Run the trained model on new data |
| **Hyperparameter** | Setting chosen *before* training (learning rate, tree depth) — not learned from one gradient step |

## 3. Three paradigms

| Paradigm | Data | Goal | Examples |
|----------|------|------|----------|
| **Supervised** | Inputs **with** labels | Predict label for new inputs | Spam filter, house prices, image classes |
| **Unsupervised** | Inputs **without** labels | Find structure | Customer segments (clustering), anomaly detection |
| **Reinforcement** | Agent + environment | Maximise **reward** over time | Game playing, robotics, ad bidding |

Most production ML today is **supervised** or **self-supervised** (labels derived from the data itself, common in language and vision pre-training).

## 4. Supervised learning at a glance

**Classification** — discrete output (spam / not spam, digit 0–9):

- Algorithms: logistic regression, decision trees, random forests, gradient boosting, k-NN, neural networks.

**Regression** — continuous output (temperature, revenue):

- Algorithms: linear regression, ridge/lasso, gradient boosting, neural networks.

Training minimises a **loss** (error) function:

- Regression: **MSE** — average squared difference between prediction and truth.
- Classification: **cross-entropy** — penalises confident wrong answers.

## 5. The ML workflow

```text
1. Problem     Define metric and failure cost (precision vs recall, latency, fairness)
2. Data        Collect, clean, label; watch bias and leakage
3. Features    Raw → numeric representation the model can consume
4. Train       Split data; fit model; tune hyperparameters on validation set
5. Evaluate    Hold-out test set; error analysis on mistakes
6. Deploy      Serve predictions; monitor drift and retrain
```

**Data leakage** — information from the future or from the test set sneaks into training — is the fastest way to build a model that looks brilliant offline and fails in production.

## 6. Train, validation, and test

| Split | Purpose |
|-------|---------|
| **Train** | Learn model parameters |
| **Validation** | Compare models and hyperparameters |
| **Test** | **Once**, at the end — unbiased estimate of real performance |

Use **k-fold cross-validation** when data is scarce: rotate which fold is validation, average the score.

Common pitfalls:

- **Overfitting** — model memorises training noise; high train accuracy, poor test accuracy.
- **Underfitting** — model too simple to capture the pattern.
- **Imbalanced classes** — accuracy alone misleads; use precision, recall, F1, or AUC.

## 7. Unsupervised and beyond (short)

- **Clustering** (k-means, DBSCAN) — group similar points without labels.
- **Dimensionality reduction** (PCA, UMAP) — compress many features for visualisation or speed.
- **Anomaly detection** — flag rare behaviour (fraud, defects).

**Deep learning** — neural networks with many layers — excels at images, audio, and language. It is a **subset** of ML, not a separate field; same train/evaluate/deploy loop, different models and compute needs.

## 8. What you need to get started

| Piece | Notes |
|-------|--------|
| **Math** | Basic linear algebra, probability, calculus for gradients (build intuition first) |
| **Python** | De facto language: pandas, scikit-learn, PyTorch / TensorFlow |
| **Statistics** | Distributions, variance, confidence in metrics |
| **Domain** | Best models fail without understanding the problem and data |

A minimal supervised experiment (conceptual):

```python
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)
print(classification_report(y_test, model.predict(X_test)))
```

## 9. ML vs adjacent topics

| Topic | Focus |
|-------|--------|
| **Machine learning** (this track) | Algorithms, data, training, evaluation |
| **MLOps** | Pipelines, versioning, deployment, monitoring |
| **AI / deep learning** | Larger models, LLMs, generative AI — see **AI** submenu ([ML Foundations](../ai/i-ml-foundations.md), [Deep Learning & LLMs](../ai/ii-deep-learning-and-llms.md)) |
| **Data science** | Exploration, storytelling, experiments — overlaps heavily with ML |

## 10. How to use this track

Start here for vocabulary and workflow. Add follow-up notes on specific algorithms, feature engineering, and frameworks as you build projects. Always tie theory to a **dataset** and a **metric** — ML is learned by doing, not only by reading.

**Related:** **AI → ML Foundations** for deeper coverage of supervised/unsupervised methods and evaluation metrics.

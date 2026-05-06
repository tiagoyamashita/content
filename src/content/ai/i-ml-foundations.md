---
label: "I"
subtitle: "ML Foundations"
group: "Artificial intelligence"
order: 1
---
Artificial Intelligence — Part I: ML Foundations
Core concepts, supervised & unsupervised learning, evaluation.

## 1. What is machine learning
Traditional programming: hand-write rules → program transforms input to output.
Machine learning: feed (input, output) examples → algorithm learns rules.

Three broad paradigms:
- Supervised learning:   labelled data → predict label on new data.
- Unsupervised learning: unlabelled data → find structure.
- Reinforcement learning: agent takes actions → maximise reward signal.

Key vocabulary:
- Feature (X): measurable property of an observation (column in a table).
- Label / target (y): what we want to predict.
- Model: learned function f such that f(X) ≈ y.
- Training: optimising model parameters on a dataset.
- Inference: running the trained model on new inputs.

## 2. Supervised learning
Given: dataset {(x₁,y₁), …, (xₙ,yₙ)}
Goal:  learn f(x) → ŷ that generalises to unseen x.

Classification — y is a discrete class:
- Binary:      spam / not-spam.
- Multi-class: digit 0–9.
- Algorithms: Logistic Regression, Decision Tree, Random Forest, SVM, k-NN.

Regression — y is a continuous value:
- House price, temperature forecast.
- Algorithms: Linear Regression, Ridge, Lasso, Gradient Boosting.

Loss functions — measure prediction error during training:
- MSE  (Mean Squared Error): Σ(ŷ−y)²/n  — regression.
- Cross-entropy: −Σ y·log(ŷ)            — classification.
- Training = minimise loss via gradient descent.

## 3. Unsupervised learning
No labels — find hidden structure in X alone.

Clustering — group similar points:
- k-Means: assign each point to its nearest of k centroids; update centroids.
- DBSCAN:  density-based; discovers arbitrary shapes; labels outliers noise.
- Hierarchical: build a dendrogram; cut at desired level.

Dimensionality reduction — compress features while preserving structure:
- PCA (Principal Component Analysis): linear projection to axes of max variance.
- t-SNE / UMAP: non-linear; great for 2-D visualisation of high-dim data.

Anomaly detection — find rare outliers (fraud, defects):
- Isolation Forest, Autoencoder reconstruction error.

## 4. Model evaluation
Train / Validation / Test split:
- Train (60-80%): fit model parameters.
- Validation (10-20%): tune hyperparameters, select model.
- Test (10-20%): unbiased final estimate of real-world performance.
!! Never touch the test set until the very end.

Cross-validation (k-fold):
- Partition data into k folds; train on k-1, validate on 1; rotate.
- Average score is a low-variance estimate — useful when data is scarce.

Classification metrics:
- Accuracy   = (TP+TN) / total  — misleading on imbalanced classes.
- Precision  = TP / (TP+FP)     — of predicted positives, how many right?
- Recall     = TP / (TP+FN)     — of actual positives, how many caught?
- F1         = 2·P·R / (P+R)    — harmonic mean; balances P & R.
- AUC-ROC    = area under the ROC curve; threshold-independent rank quality.

Regression metrics:
- MAE  = Σ|ŷ−y|/n
- RMSE = √(Σ(ŷ−y)²/n)   — penalises large errors more.
- R²   = 1 − SS_res/SS_tot  — fraction of variance explained (1 = perfect).

## 5. Overfitting & regularization
Bias-variance tradeoff:
- High bias (underfitting): model too simple; misses signal in both train & test.
- High variance (overfitting): model memorises noise; great train, poor test.
- Sweet spot: just complex enough to capture real patterns.

Regularization — penalise model complexity to reduce variance:
- L2 (Ridge): add λΣwᵢ² to loss → shrinks weights toward zero smoothly.
- L1 (Lasso): add λΣ|wᵢ| to loss → drives some weights to exactly zero (sparse).
- Dropout (neural nets): randomly zero activations during training.
- Early stopping: halt training when validation loss stops improving.

Diagnosing:
- Train ≈ Test error (both high)  → underfitting → more capacity or features.
- Train << Test error             → overfitting  → regularize or more data.

## 6. Feature engineering
Raw data rarely feeds directly into a model. Common transforms:

Numerical:
- Normalisation (min-max): scale to [0, 1].
- Standardisation (z-score): subtract mean, divide by std → N(0,1).
- Log transform: compress right-skewed distributions (e.g. income).

Categorical:
- One-hot encoding: binary column per category.
- Label encoding: integer per category (only for ordinal data).
- Target encoding: replace category with mean of target (risk of leakage).

Text:
- Bag-of-words / TF-IDF: count-based sparse vectors.
- Word embeddings (Word2Vec, GloVe): dense semantic vectors.

Leakage warning: never include information from the future or the label
itself in features — model looks great in training but fails in production.

## 7. The ML workflow
1. Define the problem & success metric.
2. Collect & explore data (EDA).
3. Clean: handle missing values, outliers, duplicates.
4. Feature engineering & selection.
5. Split: train / validation / test.
6. Baseline model (simple heuristic or linear model).
7. Train & tune (grid search, random search, Bayesian optimisation).
8. Evaluate on validation set; iterate.
9. Final evaluation on test set — report this number.
10. Deploy, monitor for drift.

## 8. Remember & rehearse
- What is the difference between classification and regression?
- Explain the bias-variance tradeoff in plain English.
- Why can accuracy be misleading on an imbalanced dataset?
- What is the purpose of the validation set vs the test set?
- When would you choose L1 over L2 regularization?
- What is feature leakage? Give an example.
- Name two unsupervised learning algorithms and their use cases.

---
label: "III"
subtitle: "Unsupervised learning"
group: "Machine learning"
order: 3
---
Unsupervised learning
**No labels** — algorithms find **structure** in **X** alone: groups, low-dimensional views, or outliers. Used for exploration, segmentation, compression, and anomaly detection.

## 1. Clustering

Group similar points so intra-cluster distance is small and inter-cluster distance is large.

### k-Means

| Step | Action |
|------|--------|
| 1 | Pick **k** centroids (random or k-means++) |
| 2 | Assign each point to nearest centroid |
| 3 | Recompute centroids as cluster means |
| 4 | Repeat until convergence |

| Pros | Cons |
|------|------|
| Fast, simple | Must choose **k**; assumes spherical clusters |
| Scales with Mini-batch k-means | Sensitive to scale — **standardise features** |

**Use cases:** customer segments, document grouping (with embeddings), image colour quantisation.

### DBSCAN

Density-based — clusters of arbitrary shape; points in sparse regions labelled **noise**.

| Param | Role |
|-------|------|
| **eps** | Neighbourhood radius |
| **min_samples** | Core point threshold |

Good when clusters are non-spherical or you want outlier detection built in.

### Hierarchical clustering

Build a **dendrogram** — cut at height to get k clusters. Useful for small n and visual exploration.

## 2. Dimensionality reduction

Compress many features while preserving structure — visualisation, speed, denoising.

| Method | Type | Use |
|--------|------|-----|
| **PCA** | Linear | Top variance directions; preprocessing for ML |
| **t-SNE** | Non-linear | 2-D visualisation only — distances not globally meaningful |
| **UMAP** | Non-linear | Faster than t-SNE; better global structure often |

```text
High-dim X  →  projection  →  2–50 dims for plot or downstream model
```

**Warning:** fit PCA on **train** only; transform val/test with same components.

## 3. Anomaly detection

Find **rare** points — fraud, defects, intrusions.

| Method | Idea |
|--------|------|
| **Isolation Forest** | Random splits isolate anomalies in few steps |
| **Autoencoder** | High reconstruction error = anomaly |
| **One-class SVM** | Boundary around “normal” training data |
| **DBSCAN noise** | Points labelled −1 |

Often **semi-supervised** in practice: train on mostly normal data.

## 4. Unsupervised vs supervised

| Question | Unsupervised | Supervised |
|----------|--------------|------------|
| Do we have labels? | No | Yes |
| Output | Clusters, components, scores | Class or number per row |
| Evaluation | Silhouette, domain review | Accuracy, F1, RMSE |

Cluster labels still need **human interpretation** — “cluster 3” is not actionable until profiled.

## 5. sklearn sketch

```python
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

kmeans = KMeans(n_clusters=5, random_state=42, n_init="auto")
labels = kmeans.fit_predict(X_scaled)

pca = PCA(n_components=2)
X_2d = pca.fit_transform(X_scaled)
```

## 6. Rehearsal questions

- Why standardise before k-means?
- PCA vs t-SNE — which for a production feature pipeline?
- Name one business use for anomaly detection.

**Related:** [Supervised learning](ii-supervised-learning.md), [Feature engineering](vi-feature-engineering.md).

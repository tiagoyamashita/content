---
label: "VI"
subtitle: "AI & ML essentials"
group: "Python"
groupOrder: 1
order: 6
---
Python — Part VI
How Python is used for **machine learning** and **applied AI**: numerical computing, classical ML, deep-learning stacks, notebooks, and reproducibility.

## 1. Where Python fits
- **Research & production glue**: same language from notebook experiments → packaged services (often behind FastAPI, batch jobs, or Spark).
- **Ecosystem**: heavily **`numpy`** / **`pandas`** for tensors/tables, **`scikit-learn`** for classical algorithms, **`torch`** or **`tensorflow`** / **`jax`** for deep nets, **`transformers`** + **`datasets`** for pretrained models.
- **Not magic**: models encode statistics or learned patterns — garbage labels, leakage, or biased data produce harmful or brittle systems.


## 2. `numpy`: contiguous numerical arrays
Arrays are **typed**, **fixed-shape**, and **vectorized** — loops in Python over millions of scalars lose to C/Fortran kernels underneath.

```python
import numpy as np

x = np.array([1.0, 2.0, 3.0])
y = np.linspace(0, 1, 5)
m = np.arange(9).reshape(3, 3)

print(m.mean(axis=1))          # row means
print((m @ m.T).shape)         # matrix multiply — prefer @ over np.dot for readability

rng = np.random.default_rng(42)
sample = rng.normal(size=(1000, 2))
```

Broadcasting rules let differently shaped arrays combine without explicit loops — read error messages carefully when shapes disagree.


## 3. `pandas`: labeled tables
Ideal for **CSV/Parquet** exploration, joins, group-by, time series indexing — bridges raw files and **`sklearn`**.

```python
import pandas as pd

df = pd.DataFrame(
    {
        "feature_a": [1, 2, 3],
        "feature_b": [0.1, 0.2, 0.3],
        "label": [0, 1, 0],
    }
)

X = df[["feature_a", "feature_b"]]
y = df["label"]
```


## 4. Classical ML with `scikit-learn`
Common pattern: **split data → preprocess → fit → evaluate** — keep transformers fit **only on training data** to avoid leakage.

```python
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

X, y = load_iris(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = Pipeline(
    steps=[
        ("scale", StandardScaler()),
        ("clf", LogisticRegression(max_iter=200)),
    ]
)
model.fit(X_train, y_train)
pred = model.predict(X_test)
print(classification_report(y_test, pred))
```


## 5. Deep learning stacks (overview)
| Library | Typical sweet spot |
|---------|-------------------|
| **PyTorch** | Research flexibility, dynamic graphs, huge industry adoption |
| **TensorFlow / Keras** | Deployment tooling, TF Serving history |
| **JAX** | Functional transforms (`jit`, `grad`, `vmap`) — rising in research |

Minimal **PyTorch** training loop shape (conceptual — real projects add dataloaders, AMP, checkpoints):

```python
import torch
import torch.nn as nn

torch.manual_seed(42)
model = nn.Sequential(nn.Linear(4, 8), nn.ReLU(), nn.Linear(8, 3))
opt = torch.optim.Adam(model.parameters(), lr=1e-2)
loss_fn = nn.CrossEntropyLoss()

x = torch.randn(16, 4)
y = torch.randint(0, 3, (16,))

model.train()
logits = model(x)
loss = loss_fn(logits, y)
loss.backward()
opt.step()
opt.zero_grad(set_to_none=True)
```


## 6. Applied AI: pretrained models (`transformers`)
**Hugging Face** exposes thousands of models behind a unified API — great for NLP/vision demos; mind **licenses**, **latency**, and **PII** before shipping.

```python
# pip install transformers torch  (also needs a sane PyTorch install)
from transformers import pipeline

cls = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)
print(cls("Shipping new AI notes today!"))
```


## 7. Notebooks vs production modules
- **`jupyter` / VS Code notebooks** accelerate iteration and plots — export stable code into **`src/`** packages once patterns stabilize.
- Long-running training belongs on **GPUs** (`cuda`, **`.to(device)`** in PyTorch) or cloud TPUs — profile before optimizing.


## 8. Reproducibility checklist
- Fix **`random.seed`**, **`np.random.default_rng`**, **`torch.manual_seed`**, and enable deterministic algorithms where frameworks allow (often hurts perf).
- Pin **`pip-tools` / `uv lock`** — upgrades silently change metrics when deps shift.
- Version **datasets** (DVC, lakeFS, or immutable buckets) — “latest CSV” is not reproducible.


## 9. Evaluation hygiene (short list)
- Hold out a **validation** set for tuning and a **test** set touched once for honest scores.
- Watch **class imbalance**, **covariate shift**, and **temporal leakage** (future columns sneaking into features).
- Prefer domain-appropriate metrics (**ROC-AUC**, **F1**, calibration) over accuracy alone on skewed problems.


## 10. When Python is not enough
Heavy online inference often moves to **C++/Rust runtimes**, **ONNX Runtime**, **TensorRT**, or managed endpoints — Python stays orchestration + experimentation while latency-critical paths compile down.

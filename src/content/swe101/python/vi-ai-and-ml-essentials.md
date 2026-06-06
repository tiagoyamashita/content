---
label: "VI"
subtitle: "AI と ML の必需品"
group: "パイソン"
groupOrder: 1
order: 6
---
Python — パート VI

**機械学習**と**応用 AI** に Python がどのように使用されるか: 数値計算、古典的な ML、深層学習スタック、ノートブック、再現性。

## 1. Python が適している場所
- **研究と生産の接着剤**: ノートブックの実験からの同じ言語 → パッケージ化されたサービス (多くの場合、FastAPI、バッチ ジョブ、または Spark の背後にあります)。
- **エコシステム**: テンソル/テーブルの場合は **`numpy`** / **`pandas`**、古典的なアルゴリズムの場合は **`scikit-learn`**、ディープネットの場合は **`torch`** または **`tensorflow`** / **`jax`**、ディープネットの場合は **`transformers`** + **`datasets`**事前トレーニングされたモデル。
- **魔法ではありません**: モデルは統計や学習されたパターンをエンコードします。不要なラベル、漏洩、または偏ったデータは、有害または脆弱なシステムを生み出します。


## 2. `numpy`: 連続した数値配列
配列は **型付き**、**固定形状**、**ベクトル化**です。数百万のスカラーを超える Python のループは、その下の C/Fortran カーネルに負けます。

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

ブロードキャスト ルールにより、明示的なループを使用せずに、異なる形状の配列を組み合わせることができます。形状が一致しない場合は、エラー メッセージを注意深く読んでください。


## 3. `pandas`: ラベル付きテーブル
**CSV/Parquet** の探索、結合、グループ化、時系列インデックス付けに最適です。生ファイルと **`sklearn`** をブリッジします。

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


## 4. `scikit-learn` を使用したクラシック ML
一般的なパターン: **データの分割 → 前処理 → 適合 → 評価** — 漏れを避けるために、**トレーニング データのみ**に変換器を適合させます。

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


## 5. 深層学習スタック (概要)
|図書館 |典型的なスイートスポット |
|----------|--------|
| **PyTorch** |研究の柔軟性、動的なグラフ、大規模な業界での採用 |
| **TensorFlow / Keras** |導入ツール、TF 提供履歴 |
| **ジャックス** |関数変換 (`jit`、`grad`、`vmap`) — 研究の増加 |

最小限の **PyTorch** トレーニング ループ形状 (概念的 - 実際のプロジェクトではデータローダー、AMP、チェックポイントが追加されます):

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


## 6. 応用 AI: 事前トレーニング済みモデル (`transformers`)
**Hugging Face** は、統合 API の背後にある数千のモデルを公開します。NLP/ビジョンのデモに最適です。出荷前に **ライセンス**、**レイテンシー**、**PII** に注意してください。

```python
# pip install transformers torch  (also needs a sane PyTorch install)
from transformers import pipeline

cls = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
)
print(cls("Shipping new AI notes today!"))
```


## 7. ノートブックと実稼働モジュールの比較
- **`jupyter` / VS Code ノートブック** は反復とプロットを高速化します。パターンが安定したら、安定したコードを **`src/`** パッケージにエクスポートします。
- 長時間実行トレーニングは **GPU** (PyTorch では `cuda`、**`.to(device)`**) またはクラウド TPU に属します - 最適化する前にプロファイルします。


## 8. 再現性チェックリスト
- **`random.seed`**、**`np.random.default_rng`**、**`torch.manual_seed`** を修正し、フレームワークで許可されている場合は決定論的アルゴリズムを有効にします (パフォーマンスに悪影響を与えることがよくあります)。
- ピン **`pip-tools` / `uv lock`** — アップグレードは、deps が変更されるとサイレントにメトリクスを変更します。
- バージョン **データセット** (DVC、lakeFS、または不変バケット) - 「最新の CSV」は再現できません。


## 9. 評価衛生 (短いリスト)
- チューニングには **検証** セットを使用し、正直なスコアを得るには **テスト** セットを一度使用します。
- **クラスの不均衡**、**共変量シフト**、**時間的漏洩** (特徴に忍び込む将来の列) を監視します。
- 偏った問題では、精度だけよりもドメインに適したメトリクス (**ROC-AUC**、**F1**、キャリブレーション) を優先します。


## 10. Python だけでは不十分な場合
大量のオンライン推論は、**C++/Rust ランタイム**、**ONNX ランタイム**、**TensorRT**、またはマネージド エンドポイントに移行することがよくあります。Python は、レイテンシー クリティカルなパスがコンパイル ダウンされる間、オーケストレーションと実験を維持します。

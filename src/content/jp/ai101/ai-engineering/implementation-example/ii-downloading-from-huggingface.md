---
label: "II"
subtitle: "ハグフェイスからダウンロード"
group: "AI Applied"
order: 2
---
ハグフェイスからダウンロード

[抱き合う顔](https://huggingface.co) モデル **weights**、**tokenizers**、および **configs** をホストします。リポページ (例:`meta-llama/Llama-3.2-3B-Instruct`) はバージョン管理されたフォルダーであり、単一のインストーラーではありません。

## 1. ダウンロードしているもの

|アーティファクト |目的 |
|----------|-----------|
|`config.json`|アーキテクチャ、隠れサイズ、層数 |
|`tokenizer.json`/`tokenizer.model`|テキスト → トークン |
|`*.safetensors`または`*.bin`|モデルの重み (大) |
|`generation_config.json`|デフォルトのデコード設定 |
|`README.md`|ライセンス、プロンプト形式、評価メモ |

**GGUF** リポジトリ (llama.cpp / Ollama インポート用) 1 つ以上を出荷`.gguf`**オリジナル** リポジトリには、Python ランタイム用の完全精度または HF- 量子化されたセーフテンソルが同梱されています。

## 2. 前提条件

```bash
# Hugging Face CLI — installs the `hf` command (current)
pip install -U "huggingface_hub[cli]"

# Optional: Git LFS for clone-based workflows
git lfs install
```

モデルが **ゲートされている**場合はログインします (ライセンスへの同意が必要です):

```bash
hf auth login
```

`huggingface-cli`**非推奨**です — 使用してください`hf`すべての CLI タスク (`hf download`、`hf auth login`、`hf --help`）。

[huggingface.co/settings/tokens]() でトークンを作成します。https://huggingface.co/settings/tokens）**読み取り**アクセス権を持ちます。

### ゲート付きモデル (Meta Llama など) — ダウンロード前に必要

`meta-llama/Llama-3.2-3B-Instruct`**ゲートされています**。認証されていないダウンロードは次のエラーで失敗します。

```text
Error: Access denied. This repository requires approval.
Warning: You are sending unauthenticated requests to the HF Hub.
```

**修正 — 3 つの手順をすべて順番に実行します。**

|ステップ |アクション |
|------|----------|
| **1. Web 承認** | [メタ-ラマ/ラマ-3.2-3B-命令](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct) ログイン中に → **同意してリポジトリにアクセス** (メタ ライセンス フォーム)。通常、承認は即座に行われます。 |
| **2. CLI ログイン** |`hf auth login`→ [設定/トークン] から **読み取り** トークンを貼り付けます(https://huggingface.co/settings/tokens) |
| **3.再試行** |同じ`hf download`コマンド |

ダウンロードする前に認証を確認します。

```bash
hf auth whoami
# Should print your HF username — confirms login only, NOT gated-repo access
```

※処方せん＝医者があなたに必要な薬の情報を書いた紙`hf auth whoami`成功しても、Llama をダウンロードできるわけではありません。** ゲート リポジトリの場合は、CLI と **同じ HF ユーザー** としてログインしているときに、モデル ページで **ステップ 1 (Web 承認)** も完了する必要があります。ダウンロードがまだ表示される場合`requires approval`、ブラウザでリポジトリ URL を開き、**同意してリポジトリにアクセス** を探します。このボタンが消えて [ファイル] タブが表示されるまで、CLI のダウンロードは失敗します。

**代替トークン環境変数** (スクリプト、CI、またはログイン キャッシュが失敗した場合):

```bash
export HF_TOKEN="hf_xxxxxxxx"   # your read token — never commit this
hf download meta-llama/Llama-3.2-3B-Instruct --local-dir ./models/llama-3.2-3b
```

**ローカル GGUF のゲートをスキップします** — コミュニティの定量リポジトリは通常開いています。 Ollama / llama.cpp では問題ありません:

```bash
hf download bartowski/Llama-3.2-3B-Instruct-GGUF \
  Llama-3.2-3B-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

または、**Ollama** (デフォルト カタログの HF アカウントはありません) を使用します。`ollama pull llama3.2:3b`。

### 推奨オープンモデル (2025 ～ 2026 年)

|使用例 |モデル |ゲート付き？ | Ollama |顔を抱きしめる |
|----------|----------|----------|----------|--------------|
| **ローカルコーディング (デフォルト)** | **Qwen2.5-Coder 7B の説明** |いいえ |`qwen2.5-coder:7b`| [Qwen/Qwen2.5-Coder-7B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct) |
|一般チャット 7B | Qwen2.5 7B 指示する |いいえ |`qwen2.5:7b`|`Qwen/Qwen2.5-7B-Instruct`|
|高速/小型 GPU | Qwen2.5-コーダー 3B |いいえ |`qwen2.5-coder:3b`|`Qwen/Qwen2.5-Coder-3B-Instruct`|
|最優秀オープンコーダー (24 GB+ VRAM) | Qwen2.5-Coder 32B 命令 |いいえ |`qwen2.5-coder:32b`|`Qwen/Qwen2.5-Coder-32B-Instruct`|
|一般チャット (ゲート付き) |ラマ 3.2 3B 命令 | **はい** (メタ) |`llama3.2:3b`|`meta-llama/Llama-3.2-3B-Instruct`|

**Qwen2.5-Coder** は、**コード生成、修正、および IDE アシスタント** の通常の選択です。Apache 2.0、HF 承認ステップなし、他のオープン コーダーと比較して強力なベンチマークです。 **を使用してください`-Instruct`** チャット/コーディング用のバリアント。基本ウェイトは微調整専用です。

**Qwen2.5-Coder をダウンロード (ゲートなし):**

```bash
# Full safetensors (transformers / vLLM)
hf download Qwen/Qwen2.5-Coder-7B-Instruct --local-dir ./models/qwen2.5-coder-7b

# Single GGUF file (llama.cpp / Ollama import)
hf download bartowski/Qwen2.5-Coder-7B-Instruct-GGUF \
  Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

または、HF をスキップします。`ollama pull qwen2.5-coder:7b`。

## 3. 方法 A —`hf download`(好ましい)

リポジトリ全体または特定のファイルをローカル フォルダーにダウンロードします。

```bash
# Qwen2.5-Coder — open, best default for coding (7B fits 8 GB GPU)
hf download Qwen/Qwen2.5-Coder-7B-Instruct --local-dir ./models/qwen2.5-coder-7b

# Single GGUF file (saves bandwidth)
hf download bartowski/Qwen2.5-Coder-7B-Instruct-GGUF \
  Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  --local-dir ./models

# Gated example — Meta Llama (requires web approval first)
hf download meta-llama/Llama-3.2-3B-Instruct --local-dir ./models/llama-3.2-3b
```

|旗 |使用 |
|------|-----|
|`--local-dir`|ディスク上のミラー リポジトリ レイアウト |
|`--local-dir-use-symlinks False`|シンボリックリンク (ポータブル コピー) ではなく、実際のファイル |
|`--revision`|ブランチ、タグ、またはコミットを固定する |

再開は自動的に行われます。中断されたダウンロードは中断したところから続行されます。

## 4. 方法 B — Git クローン + LFS

```bash
git clone https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct
cd Llama-3.2-3B-Instruct
git lfs pull
```

|長所 |短所 |
|------|------|
|おなじみの Git ワークフロー |巨大なリポジトリの場合は遅くなります。 HF の LFS クォータ |
|コミットを固定するのが簡単 | sparse-checkout が設定されていない限り、リポジトリ全体をプルします。

ゲート モデルの場合は、HF アカウントにリンクされたトークンまたは SSH キーを含む HTTPS を使用します。

## 5. メソッド C — Python`snapshot_download`

スクリプトまたはノートブック内で役立ちます:

```python
from huggingface_hub import snapshot_download

path = snapshot_download(
    repo_id="Qwen/Qwen2.5-Coder-7B-Instruct",
    local_dir="./models/qwen2.5-coder-7b",
    local_dir_use_symlinks=False,
)
```

`transformers`最初の使用時にフェッチすることもできます。

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-Coder-7B-Instruct")
```

重みは HF キャッシュに格納されます (`~/.cache/huggingface/hub`）合格しない限り`cache_dir`または`local_dir`。

## 6. 適切なリポジトリのバリアントを選択する

|欲しい | |を探してください
|----------|----------|
| **コーディング / IDE アシスタント** | **Qwen2.5-コーダー**`*-Instruct`または`qwen2.5-coder:7b`Ollama で |
| **llama.cpp / コボルドCPP** |`*-GGUF`リポジトリまたは`.gguf`[ファイル]タブ |
| **Ollama** |頻繁`ollama pull <name>`— Ollama があなたのためにダウンロードします。または GGUF | をインポートします。
| **vLLM / TGI / 変圧器** |オリジナルのセーフテンソル リポジトリまたは AWQ/GPTQ quant |
| **ディスクの占有面積が小さい** | Q4_K_M、Q5_K_M GGUF または AWQ 4 ビット |

モデルカードに記載されている**ライセンス**を必ずお読みください。多くの分銅は商用利用が禁止されているか、登録が必要です。

## 7. ダウンロードを確認します

```bash
# Check total size vs repo "Files and versions" tab
du -sh ./models/qwen2.5-coder-7b

# List safetensors shards
ls -lh ./models/qwen2.5-coder-7b/*.safetensors
```

シャードが小さい (KB が少ない) 場合、Git LFS はプルされていない可能性があります — 実行`git lfs pull`または再実行する`hf download`。

## 8. よくある問題

|問題 |修正 |
|----------|-----|
| **アクセスが拒否されました/承認が必要です** |ゲート付きリポジトリ — 完了 [Web 承認](#gated-models-meta-llama-etc--required-before-download）、 それから`hf auth login`;と確認する`hf auth whoami`|
| **未認証リクエストの警告** |同じです - あなたはログインしていません。セット`HF_TOKEN`または走る`hf auth login`|
| **403 / ゲート リポジトリ** | HF Web サイトで **最初** (ログイン) でライセンスに同意し、次に`hf auth login`|
| **ディスク不足** |完全なセーフテンサーの代わりに 1 つの GGUF クォントをダウンロードする |
| **最初のプルは遅い** |使用`hf download`有線接続の場合。ピンワンクォント |
| **ランタイムの形式が間違っています** | GGUF → ラマ.cpp/Ollama;セーフテンサー → トランス/vLLM |

＃＃ 次

[ローカル実行プラットフォーム](iii-local-run-platforms.md) - これらのファイルをロードして推論を提供する場所。

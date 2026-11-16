---
label: "VI"
subtitle: "RTX 1080 にインストールして実行する"
group: "AI Applied"
order: 6
---
RTX 1080 にインストールして実行する

**NVIDIA GeForce RTX 1080** (8 GB VRAM、Pascal / compute **6.1**) 上の各主要ローカル ランタイムの段階的なセットアップ。 **Linux** (Ubuntu、Debian、Kali など) を想定しています。 Windows はフローが異なる箇所をメモします。

[モデル RAM の要件](iv-model-ram-requirements.md) サイズ理論について。 8 GB VRAM では、**Q4_K_M** または Ollama のデフォルト クォントの **3B–7B** モデルから開始します。

## 0. RTX 1080 制約

|スペック |意味 |
|------|---------------|
| **8 GB VRAM** |快適さ: **3B ～ 7B** Q4 と GPU。 **8B** Q4 は控えめなコンテキストに適合します。 **13B+** には CPU オフロードまたは airLLM が必要です |
| **パスカル (sm_61)** | Ollama、llama.cpp、KoboldCPP の CUDA ビルドで動作します。 **vLLM / TGI / TensorRT-LLM** 新しい GPU をターゲットにしています - 多くの場合、面倒な作業やサポートされていません |
| **システム RAM** | CPU オフロードと OS がスワップしないように、**16 GB+** を目指します。

### 共有前提条件 (すべての GPU パス)

```bash
# 1. NVIDIA driver (reboot after install)
nvidia-smi
# Should show RTX 1080 and driver 535+ (550+ recommended)

# 2. Optional but useful: CUDA toolkit for building llama.cpp
# Ubuntu/Debian example — match your distro
sudo apt update
sudo apt install -y build-essential cmake git
```

もし`nvidia-smi`失敗した場合は、以下のランタイムの前にドライバーを修正してください。

### 8 GB VRAM の推奨モデル

|モデル |フォーマット | GPU に完全に適合しますか? |
|------|--------|--------|
| **`qwen2.5-coder:7b`** (Ollama) | Ollama バンドル | **はい — 8 GB** のベストオープンコーダー |
|`qwen2.5-coder:3b`| Ollama / Q4 GGUF |はい - より速く、より軽く |
|`llama3.2:3b`(Ollama) | Ollama バンドル |はい — コードチューニングではなく、一般的なチャット |
|`qwen2.5:7b`| Ollama / Q4 GGUF |はい、Q4 で — 一般的なチャット |
|`qwen2.5-coder:14b`| Q4 GGUF |タイト — 1080 での部分オフロード |
|`qwen2.5-coder:32b`| Q4 GGUF |いいえ — 24 GB+ VRAM が必要です |

---

## 1. Ollama (最も簡単 — ここから始めます)

＃＃＃ インストール

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Windows/macOS: [ollama.com/download](https://ollama.com/download）。

### GPU を確認してください

```bash
ollama run qwen2.5-coder:7b "Write hello world in Python."
# In another terminal while generating:
ollama ps
```

`ollama ps`プロセッサ列に **GPU** と表示されるはずです。 CPU のみと表示されている場合は、チェックしてください`nvidia-smi`そしてドライバー。

### モデルをプルして実行する

```bash
# Best coding model for 8 GB VRAM (recommended)
ollama pull qwen2.5-coder:7b
ollama run qwen2.5-coder:7b

# Faster / lighter coding
ollama pull qwen2.5-coder:3b
ollama run qwen2.5-coder:3b

# General chat (not code-specialized)
ollama pull qwen2.5:7b
ollama run qwen2.5:7b

# Small general model
ollama pull llama3.2:3b
ollama run llama3.2:3b
```

### OpenAI 互換の API (Cursor、Continue など)

```bash
# Server starts automatically on first request; or:
ollama serve
```

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5-coder:7b",
    "messages": [{"role": "user", "content": "Write a bash script to list large files"}]
  }'
```

| Cursor / IDE 設定 |値 |
|----------------------|------|
|ベース URL |`http://localhost:11434/v1`|
|モデル | **`qwen2.5-coder:7b`** (コーディング) または`qwen2.5:7b`(一般的なチャット) |
| API キー |任意のプレースホルダー (例:`ollama`) |

### カスタム GGUF を実行する

```bash
# After hf download (see Hugging Face note)
cat > Modelfile <<'EOF'
FROM ./models/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf
PARAMETER temperature 0.7
EOF
ollama create qwen-coder-local -f Modelfile
ollama run qwen-coder-local
```

---

## 2. llama.cpp (CUDA ビルド — 最大制御)

### インストール (CUDA でビルド)

```bash
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp
cmake -B build -DGGML_CUDA=ON
cmake --build build --config Release -j "$(nproc)"
```

バイナリが到着します`build/bin/`— 例:`llama-cli`、`llama-server`。

CMake が CUDA を見つけられない場合は、次のように設定します。

```bash
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH
```

### GGUF をダウンロード

```bash
pip install -U "huggingface_hub[cli]"
hf download bartowski/Qwen2.5-Coder-7B-Instruct-GGUF \
  Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

### インタラクティブに実行する

```bash
./build/bin/llama-cli \
  -m ./models/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  -ngl 99 \
  -c 4096 \
  -p "You are an expert programmer." \
  --interactive
```

|旗 | RTX 1080 ガイダンス |
|-----|---------------------|
|`-ngl 99`| **すべて**のレイヤーを GPU にオフロードします (3B ～ 7B Q4 に使用) |
|`-ngl 35`| 8B+ OOM の場合は部分オフロード — CPU で休止 |
|`-c 4096`|コンテキスト トークン — OOM | の場合 **2048** に低下します
|`-ngl 0`| CPU を強制する (デバッグのみ) |

### HTTP サーバー

```bash
./build/bin/llama-server \
  -m ./models/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  -ngl 99 \
  -c 4096 \
  --host 127.0.0.1 \
  --port 8080
```

API:`http://localhost:8080`— OpenAI スタイルのエンドポイント [llama.cpp サーバー ドキュメント](https://github.com/ggerganov/llama.cpp/blob/master/tools/server/README.md）。

---

## 3. LM スタジオ (GUI — Linux または Windows)

＃＃＃ インストール

1. [lmstudio.ai]()からダウンロードhttps://lmstudio.ai) (`.AppImage`Linux ではインストーラー、Windows ではインストーラー)。
2. アプリを実行します。 **発見**を開く → 検索**`Qwen2.5-Coder-7B`** → **Q4** クォントを選択します。
3. **マイ モデル** → モデルのロード → **GPU** スライダーを **最大** (すべてのレイヤー) にオフロードします。

＃＃＃ 走る

- インタラクティブに使用するための **チャット** タブ。
- **開発者** → **ローカルサーバー** → サーバーを起動します`http://localhost:1234/v1`。

| RTX 1080 ヒント |アクション |
|--------------|----------|
| OOM ロード時 |モデル設定の小さいモデルまたは下位コンテキスト |
|最初のトークンが遅い | 7B では 1080 で通常 — 7B では ~15 ～ 40 トーク/秒が予想されます Q4 |

ヘッドレス Linux サーバー ワークフローはありません。SSH ボックスには Ollama または llama-server を使用します。

---

## 4. KoboldCPP (ポータブルバイナリ + Web UI)

＃＃＃ インストール

```bash
# CUDA-enabled release from GitHub (pick latest cu12.x asset for Linux)
wget https://github.com/LostRuins/koboldcpp/releases/latest/download/koboldcpp-linux-x64-cuda12
chmod +x koboldcpp-linux-x64-cuda12
mv koboldcpp-linux-x64-cuda12 koboldcpp
```

Windows: グラブ`koboldcpp.exe`CUDA は同じリリース ページからビルドします。

＃＃＃ 走る

```bash
./koboldcpp --model ./models/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  --gpulayers 99 \
  --contextsize 4096 \
  --port 5001
```

開ける`http://localhost:5001`ブラウザで。より低い`--gpulayers`8B モデルで OOM を押した場合。

---

## 5. GPT4All (デスクトップ、オプションの CUDA)

＃＃＃ インストール

[gpt4all.io]()からダウンロードhttps://gpt4all.io) — Linux`.deb`/ AppImage または Windows インストーラー。

＃＃＃ 走る

1. **モデルの追加** → **3B ～ 7B** チャット モデルを選択します (1080 の 13B+ は避けてください)。
2. 設定 → **GPU アクセラレーション** (ビルドに応じて Vulkan/CUDA) を有効にします。
3. HTTP が必要な場合は、設定で **ローカル API** を選択します。

カジュアルなオフラインチャットに最適です。開発者は通常、API 人間工学よりも Ollama を好みます。

---

## 6. airLLM (8 つの GB VRAM 上の大きな HF モデル)

レイヤーストリーミング — 完全な GPU ロードが適合しない場合、**13B+** の適合が遅くなります。

＃＃＃ インストール

```bash
python3 -m venv ~/airllm-venv
source ~/airllm-venv/bin/activate
pip install -U pip airllm torch --index-url https://download.pytorch.org/whl/cu121
hf auth login
```

### 実行 (Python)

```python
from airllm import AutoModel

model = AutoModel.from_pretrained(
    "Qwen/Qwen2.5-Coder-7B-Instruct",
    compression="4bit",
)
input_tokens = model.tokenizer(
    ["def fib(n):"],
    return_tensors="pt",
    return_attention_mask=False,
)
generation = model.generate(input_tokens["input_ids"].cuda(), max_new_tokens=50)
print(model.tokenizer.decode(generation[0]))
```

低遅延チャットではなく、**実験**に使用してください。最初の実行では、Hugging Face からウェイトをダウンロードします。

---

## 7. vLLM — RTX 1080 では推奨されません

[vLLM](https://github.com/vllm-project/vllm) **データセンター GPUs** (アンペア **sm_80+**) をターゲットとします。 Pascal **sm_61** は多くの場合**サポートされていない**か、機能が制限されたソースからビルドする必要があります (1080 では貧弱な ROI)。

それでも試してみたい場合 (Linux のみ):

```bash
python3 -m venv ~/vllm-venv
source ~/vllm-venv/bin/activate
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-Coder-7B-Instruct \
  --dtype half \
  --max-model-len 2048
```

Pascal ではビルドの失敗や実行時エラーが予想されます。 **このカードでは代わりに Ollama または llama.cpp を使用してください**。

---

## 8. TGI と TensorRT-LLM — 1080 はスキップします

|プラットフォーム | RTX 1080 評決 |
|----------|------|
| **[TGI](https://github.com/huggingface/text-generation-inference)** | Docker + NVIDIA スタック;公式イメージは新しい GPU を想定しています。古い CUDA イメージでは可能ですが、日常的な使用はサポートされていません。
| **[TensorRT-LLM](https://github.com/NVIDIA/TensorRT-LLM)** | Optimized for **Tensor Core** GPUs (Turing+). Pascal lacks Tensor Cores — not worth installing |

最新のハードウェア上の運用 API については、**RTX 3060 12GB+** またはクラウド GPU で再確認してください。

---

## 9. MLX — 該当なし

[MLX](https://github.com/ml-explore/mlx) は **Apple Silicon のみ**です。 RTX 1080 PC をスキップします。

---

## 10. RTX 1080 のクイックピック

|目標 |インストール |実行 |
|------|--------|-----|
| **ローカルコーディング (推奨)** | Ollama |`ollama pull qwen2.5-coder:7b && ollama run qwen2.5-coder:7b`|
| **IDE API (コード用)** | Ollama |`http://localhost:11434/v1`+`qwen2.5-coder:7b`|
| **最速の一般チャット** | Ollama |`ollama pull llama3.2:3b && ollama run llama3.2:3b`|
| **きめ細かい GPU/コントロール** | llama.cpp CUDA ビルド |`llama-server -ngl 99 -m …Qwen2.5-Coder…Q4_K_M.gguf`|
| **Web UI、ターミナルなし** | LM Studio または KoboldCPP | GUI で Qwen2.5-Coder-7B を検索 |
| **130 億以上の実験** |エアLLM |`Qwen/Qwen2.5-Coder-14B-Instruct`+ レイヤーストリーミング |

## 11. トラブルシューティング

|症状 |修正 |
|----------|-----|
| **CUDA OOM** |小型モデル (3B)、Q4 quant、下位`-c`/ コンテキスト、リデュース`--gpulayers`|
| **CPU でのみ実行可能** |`nvidia-smi`;ドライバーを再インストールします。 llama.cppを再構築します`-DGGML_CUDA=ON`|
| **生成が遅い** | 1080 の 7B では通常 (~20–35 tok/s Q4)。速度を上げるには 3B を使用してください |
| **モデルが見つかりません** |`ollama pull <name>`または GGUF パスを確認します。
| **ゲート付き HF モデル** |`hf auth login`+ ライセンスに同意する |

実行中に VRAM を監視します。

```bash
watch -n1 nvidia-smi
```

＃＃ 関連している

- [ハグフェイスからダウンロード](ii-downloading-from-huggingface.md)
- [ローカル実行プラットフォーム](iii-local-run-platforms.md)
- [モデル RAM の要件](iv-model-ram-requirements.md)
- [CPU と軽量ランナー](v-cpu-and-lightweight-runners.md）

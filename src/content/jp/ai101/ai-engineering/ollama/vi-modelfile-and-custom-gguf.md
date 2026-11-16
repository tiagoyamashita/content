---
label: "VI"
subtitle: "モデルファイルとカスタム GGUF"
group: "Ollama"
order: 6
---
モデルファイルとカスタム GGUF

モデルが Ollama ライブラリに**ない**場合、または**カスタム システム プロンプトとパラメータ**を焼き付けたい場合は、**Modelfile** を使用し、`ollama create`。

## 1. モデルファイルの基本

```dockerfile
FROM qwen2.5-coder:7b
SYSTEM You are a concise Python tutor. Show types and one test per answer.
PARAMETER temperature 0.3
PARAMETER num_ctx 8192
```

```bash
ollama create python-tutor -f Modelfile
ollama run python-tutor
```

|指示 |目的 |
|-----------|-----------|
|`FROM`|基本モデルのタグ **または** へのパス`.gguf`|
|`SYSTEM`|デフォルトのシステムプロンプト |
|`PARAMETER`|デフォルトのランタイムパラメータ |
|`TEMPLATE`|チャット テンプレート (高度 - 通常は基本から継承) |
|`LICENSE`|ライセンステキストメタデータ |

## 2. ローカル GGUF をインポートします (Hugging Face から)

最初に GGUF をダウンロードします — [Hugging Face からのダウンロード](を参照)../implementation-example/ii-downloading-from-huggingface.md):

```bash
hf download bartowski/Qwen2.5-Coder-7B-Instruct-GGUF \
  Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf \
  --local-dir ./models
```

モデルファイル:

```dockerfile
FROM ./models/Qwen2.5-Coder-7B-Instruct-Q4_K_M.gguf
PARAMETER temperature 0.7
```

```bash
ollama create qwen-coder-local -f Modelfile
ollama run qwen-coder-local
```

**絶対パスまたはリポジトリ相対**パスを使用して、`.gguf`ファイルに入れる`FROM`。

## 3. 既存のモデルから派生する

```bash
ollama show qwen2.5-coder:7b --modelfile > Modelfile
# edit SYSTEM / PARAMETER
ollama create my-qwen-dev -f Modelfile
```

## 4. カスタム モデルをリストする

```bash
ollama list
```

カスタム名はライブラリ プルの横に表示されます (`python-tutor`、`qwen-coder-local`、など）。

## 5. チームと共有する

|アプローチ |詳細 |
|----------|----------|
| **モデルファイルをコミット** |チームラン`ollama create`同じ GGUF をプルした後 |
| **Modelfile + HF 命令のみをコミットします** |モデルファイルが指すもの`FROM qwen2.5-coder:7b`- みんな`ollama pull`|
| **コミットしないでください** multi-GB`.gguf`ブロブ |使用`hf download`または`ollama pull`README で |

リポジトリの例:

```text
models/
  Modelfile              ← committed
  README.md              ← "run hf download … then ollama create …"
  *.gguf                 ← gitignored
```

## 6. Modelfile を使用しない場合

|状況 |より良い道 |
|----------|---------------|
|モデルはすでにライブラリにあります |`ollama pull`のみ |
|最大限の推論制御が必要 | llama.cpp を直接 — [ローカル実行プラットフォーム](../implementation-example/iii-local-run-platforms.md) |
|本番環境のマルチユーザー サービス | vLLM / TGI — Ollama デスクトップではありません |

＃＃ 次

[GPU とトラブルシューティング](vii-gpu-troubleshooting.md) — CPU のみ、OOM、生成の遅さを修正します。

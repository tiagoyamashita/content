---
label: "IV"
subtitle: "実行、チャット、パラメータ"
group: "Ollama"
order: 4
---
実行、チャット、パラメータ

## 1. インタラクティブなチャット

```bash
ollama run qwen2.5-coder:7b
```

|コマンド (チャット内) |アクション |
|---------------------|----------|
|`/bye`、`/exit`|セッションを終了 |
|`/clear`|明確なコンテキスト |
|`/set parameter value`|実行時パラメータを変更します (以下を参照)。
|`/?`|ヘルプ |

インタラクティブモードなしのワンショット:

```bash
ollama run qwen2.5-coder:7b "Write a Python function to merge two dicts"
```

## 2. 共通パラメータ

とのチャット中に設定します`/set`または **Modelfile** (永続):

|パラメータ |典型的な |効果 |
|----------|-----------|----------|
|`temperature`|`0.7`|ランダム性 (低い = より決定的) |
|`num_ctx`|`4096`|コンテキスト ウィンドウ トークン — VRAM がある場合に発生します。
|`top_p`|`0.9`|核サンプリング |
|`repeat_penalty`|`1.1`|繰り返しを減らす |

セッション中の例:

```text
/set temperature 0.2
/set num_ctx 8192
```

コーディングタスク: ** を試してください`temperature 0.1–0.3`**。

## 3. システムプロンプト

インタラクティブ チャットでは、複数行のシステム プロンプトが表示されます。

```bash
ollama run qwen2.5-coder:7b
>>> /set system You are a senior Python engineer. Prefer stdlib. Always show types.
```

永続的なシステム プロンプトの場合は、**Modelfile** — [Modelfile &custom GGUF](vi-modelfile-and-custom-gguf.md）。

## 4. 現在ロードされているもの

```bash
ollama ps
```

|コラム |意味 |
|--------|--------|
| **MODEL** |ランニングタグ |
| **PROCESSOR** |`100% GPU`、`100% CPU`、または混合 |
| **UNTIL** |アイドルアンロードタイマー |

**PROCESSOR** が GPU マシン上でのみ CPU を表示する場合は、[GPU とトラブルシューティング](vii-gpu-troubleshooting.md）。

## 5. モデルをメモリ内に保持する

デフォルト: Ollama は数分後にアイドル状態のモデルをアンロードします。

```bash
# Keep loaded 30 minutes after last request (example)
OLLAMA_KEEP_ALIVE=30m ollama serve
```

または、API 経由でリクエストごとに`keep_alive`フィールド — [API と IDE の統合](v-api-and-ide-integration.md）。

## 6. 複数行入力

コードブロックを直接貼り付けます`ollama run`。空白行で終わるか、ヒアドキュメントでワンショット モードを使用します。

```bash
ollama run qwen2.5-coder:7b <<'EOF'
Review this function for bugs:

def divide(a, b):
    return a / b
EOF
```

＃＃ 次

[API と IDE の統合](v-api-and-ide-integration.md) — Cursor、続けて、カールしてください。

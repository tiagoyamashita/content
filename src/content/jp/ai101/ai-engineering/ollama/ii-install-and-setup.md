---
label: "II"
subtitle: "インストールとセットアップ"
group: "Ollama"
order: 2
---
インストールとセットアップ

## 1. インストール

### Linux (スクリプト - 推奨)

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

をインストールします`ollama`バイナリと **systemd** サービス (ほとんどのディストリビューションでは起動時に開始されます)。

### macOS

[ollama.com/download]() からダウンロードします。https://ollama.com/download） または：

```bash
brew install ollama
```

Apple Silicon 上で **Metal** が自動的に使用されます。

### ウィンドウ

インストーラーは [ollama.com/download](https://ollama.com/download）。 NVIDIA GPU およびドライバーが存在する場合は **CUDA** を使用します。

## 2. 確認する

```bash
ollama --version
ollama list          # empty until first pull
```

サーバーを起動します (多くの場合、インストール後に自動起動します)。

```bash
ollama serve         # foreground — optional if service already running
```

API を確認します。

```bash
curl http://localhost:11434/api/tags
```

## 3. GPU 前提条件 (NVIDIA Linux)

```bash
nvidia-smi
```

|チェック |予想される |
|------|----------|
|ドライバー | 535+ (550+ を推奨) |
| GPU リスト |あなたのカード (例: RTX 1080) |
|エラーはありません | Ollama を責める前にドライバーを修正してください。

Ollama には独自の CUDA ランタイムがバンドルされています。基本的な使用のために別の CUDA ツールキットをインストールする必要は**ありません**。

## 4. ファイルが存在する場所

|パス |目次 |
|------|----------|
|`~/.ollama/models/`|ダウンロードされたモデル BLOB (大) |
|`~/.ollama/`|構成と状態 |
| **サービス** |`systemctl status ollama`(Linux) |

大規模なプルの前にディスクを解放する — 7B モデルはクォントに応じてディスク上におよそ **4 ～ 8 GB** あります。

## 5. サービス管理 (Linux)

```bash
sudo systemctl enable ollama
sudo systemctl start ollama
sudo systemctl status ollama
```

ログ:

```bash
journalctl -u ollama -f
```

＃＃ 次

[モデル — プルと管理](iii-models-pull-and-manage.md) — 最初のモデルをダウンロードします。

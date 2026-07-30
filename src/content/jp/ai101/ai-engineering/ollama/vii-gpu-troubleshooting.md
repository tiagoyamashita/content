---
label: "VII"
subtitle: "GPU とトラブルシューティング"
group: "Ollama"
order: 7
---
GPU とトラブルシューティング

## 1. GPU が使用されていることを確認します

```bash
ollama run qwen2.5-coder:7b "hi"
# second terminal:
ollama ps
watch -n1 nvidia-smi
```

|`ollama ps`ショー |意味 |
|---------------------|----------|
| **100% GPU** |良い — カード上のモデル |
| **100% CPU** | GPU は使用されていません - 以下の修正を参照してください。
| **混合%** |部分的なオフロード — タイトな VRAM では通常です。

## 2. CPU - GPU が予期される場合のみ

|チェック |修正 |
|------|-----|
|`nvidia-smi`失敗する | NVIDIA ドライバーをインストール/修正します。再起動 |
|モデルが大きすぎます |小さいタグ (`3b`ない`32b`) |
|ドライバーが古すぎる | 535+ / 550+ にアップデート |
|間違った Ollama ビルド | [ollama.com]() から再インストールしますhttps://ollama.com/download) |
| CPU テストを強制する |`OLLAMA_NUM_GPU=0`— 通常使用の場合は取り外してください |

Linux: ユーザーが GPU にアクセスできることを確認します (`nvidia-smi`Ollama を実行している同じユーザーとして)。

## 3. メモリ不足 (OOM)

|症状 |修正 |
|----------|-----|
| CUDA OOM / ロード時にクラッシュ |小型モデル。`qwen2.5-coder:3b`|
|長いチャット中の OOM |より低い`num_ctx`（`/set num_ctx 2048`) |
|複数のモデルがロードされました |`ollama ps`— アイドル状態のアンロードを待つか、サービスを再起動します。
|プル時にディスクがいっぱいです |`ollama rm`古いモデル。`df -h ~/.ollama`|

VRAM ガイド: [モデル RAM の要件](../implementation-example/iv-model-ram-requirements.md）。 RTX 1080 の詳細: [RTX 1080 にインストールして実行](../implementation-example/vi-install-and-run-rtx-1080.md）。

## 4. 生成が遅い

|原因 |ガイダンス |
|------|----------|
| **古い GPU** では 7B | RTX 1080 では、~20 ～ 35 tok/s が正常です。
| **CPU 推論** |はるかに遅い — 最初に GPU を修正してください。
| **コールドスタート** |アイドル ロード後の最初のトークンが遅くなる |
| **コンテキストが長すぎます** | KV キャッシュ コスト — 短縮`num_ctx`|

## 5. 接続エラー (API / Cursor)

|エラー |修正 |
|------|-----|
|`connection refused`|`ollama serve`または`systemctl start ollama`|
|モデル名が間違っています |`ollama list`— 正確なタグを使用する |
| Cursor は API に到達できません |ベース URL は次のようにする必要があります`http://localhost:11434/v1`|
|リモートマシン | SSH トンネルまたはセット`OLLAMA_HOST`(信頼されたネットワークのみ) |

## 6. プル/ダウンロードの失敗

|問題 |修正 |
|----------|-----|
|ダウンロードの中断 |再実行`ollama pull`— 履歴書 |
|ディスク容量がありません |モデルを削除するには`ollama rm`|
|プロキシ/ファイアウォール |システムプロキシを設定します。企業のSSL検査をチェックする |

## 7. リセット

```bash
sudo systemctl stop ollama
# optional: backup then clear models
# rm -rf ~/.ollama/models/*
sudo systemctl start ollama
ollama pull qwen2.5-coder:7b
```

キャッシュが破損している場合にのみリセットを使用します。すべてのモデルを再ダウンロードします。

＃＃ 関連している

- [インストールとセットアップ](ii-install-and-setup.md)
- [API と IDE の統合](v-api-and-ide-integration.md)
- [実装例](../implementation-example/i-overview.md）

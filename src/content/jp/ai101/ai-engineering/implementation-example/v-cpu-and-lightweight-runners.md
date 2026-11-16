---
label: "V"
subtitle: "CPU と軽量ランナー"
group: "AI Applied"
order: 5
---
CPU と軽量ランナー

すべてのマシンに 24 の GB GPU が搭載されているわけではありません。これらのランタイムは **低 VRAM**、**CPU 推論**、または **レイヤー オフロード**を優先するため、ラップトップまたは小規模なクラウド インスタンスでも有用なオープン モデルを実行できます。

## 1. ランナーの比較

|ランナー |アイデア | GPU が必要ですか? |最適な時期 |
|----------|------|---------------|----------|
| **[ラマ.cpp](https://github.com/ggerganov/llama.cpp)** |最適化された GGUF 推論。部分的`-ngl`オフロード |オプション | CPU + GGUF のデフォルト。巨大なコミュニティ |
| **[Ollama](https://ollama.com)** |簡単なプルで llama.cpp (およびその他) をラップします |オプション | llama.cpp と同じですが、より単純です UX |
| **[airLLM](https://github.com/lyogavin/airllm)** | GPU を通じて **一度に 1 つのレイヤー** をストリーミングします。小規模 VRAM OK | **4 GB** VRAM の 70B クラス (遅い) |
| **[MLX](https://github.com/ml-explore/mlx)** | Apple Metal カーネル |アップルシリコン | M1/M2/M3 Mac で最高のローカル パフォーマンス |
| **[GPT4すべて](https://gpt4all.io)** |デスクトップ アプリ + CPU バックエンド |オプション |技術者以外のユーザー、オフライン チャット |
| **[コボルドCPP](https://github.com/LostRuins/koboldcpp)** | llama.cpp フォーク + UI |オプション |単一のポータブルバイナリ |
| **[ラマファイル](https://github.com/Mozilla-Ocho/llamafile)** | 1 つのファイル内のモデル + ランタイム |オプション |ドロップイン実行可能ファイル、インストール不要 |
| **トランスフォーマー +`device_map="cpu"`** | CPU の純粋な PyTorch |いいえ |プロトタイピングのみ - 大規模にすると非常に遅い |

## 2. airLLM — 大きなモデル、小さな VRAM

**airLLM** は、**システム RAM** に全ウェイトを保持し、前進ステップごとに **1 つのトランス層**を GPU メモリに移動します。

```text
70B model in RAM  →  layer 0 to GPU → compute → layer 1 to GPU → … → logits
```

|長所 |短所 |
|------|------|
| VRAM よりもはるかに大きなモデルを実行する | **完全な GPU ロードよりもはるかに遅い** |
|ハグフェイスセーフテンサーと併用可能 | Python + CUDA セットアップ; Ollama よりも洗練されていません。
|時折のバッチ ジョブに便利 |低遅延チャットには不向き |

通常のインストール:

```bash
pip install airllm
```

```python
from airllm import AutoModel

model = AutoModel.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
# inference API per project README — layer-wise GPU execution
```

特定の HF モデルを**実行する必要があり**、**4–8 GB VRAM** しかない場合に使用します。対話型コーディング アシスタントには使用しません。

## 3. CPU 上の llama.cpp (GPU なし)

**Q4_K_M** GGUF をダウンロードして実行します。

```bash
./llama-cli -m ./models/model-Q4_K_M.gguf -p "Hello" -n 128 -ngl 0
```

|旗 |意味 |
|-----|----------|
|`-ngl 0`| **いいえ** GPU レイヤー — 純粋な CPU |
|`-ngl 35`| 35 層を GPU にオフロード (モデルに依存) |
|`-c 4096`|コンテキスト サイズ — OOM の場合は小さくなります |

**llama-server** は、アプリの HTTP 上で同じスタックを公開します。

|長所 |短所 |
|------|------|
|ほぼすべての x86/ARM マシン上で動作します。 CPU の 1 秒あたりのトークン数が少ない (通常 1 ～ 20) |
|量子化された RAM フットプリント |長いプロンプトは遅く感じる |
| Pi からワークステーションまで同じバイナリ スケール |トレーニングなし - 推論のみ |

[モデル RAM 要件](iv-model-ram-requirements.md) — **3B Q4** on **8 GB** RAM は現実的です。 **16 GB** の **7B** は、CPU にとってコンフォート ゾーンです。

## 4. Apple シリコン — MLX

Mac では、**ユニファイド メモリ**を効率的に使用することで、**MLX** が一般的な CPU パスよりも優れていることがよくあります。

```bash
pip install mlx-lm
mlx_lm.generate --model mlx-community/Llama-3.2-3B-Instruct-4bit --prompt "Hello"
```

|長所 |短所 |
|------|------|
| M-シリーズのワットあたりの強力なパフォーマンス | macOS / Apple ハードウェアのみ |
| HF 上の 4 ビット MLX モデル | GGUF より小さいカタログ |
| Cursor を使用するローカル開発者に適しています。 Linux サーバーのデプロイには対応していません |

## 5. Ollama CPU モード

GPU が検出されない場合でも、llama.cpp CPU カーネルを利用して Ollama が引き続き実行されます。

```bash
ollama pull qwen2.5-coder:7b
ollama run qwen2.5-coder:7b
```

**小さい**タグを優先します(`3b`、`1.5b`) CPU のみ。セット`OLLAMA_NUM_GPU=0`デバッグ時にハイブリッド マシンで CPU を強制します。

## 6. いつどれを使用するか

|目標 |選択 |
|------|------|
|毎日のローカル **コーディング** | Ollama + **`qwen2.5-coder:7b`** |
|毎日のローカルチャット (一般) | Ollama +`qwen2.5:7b`または`llama3.2:3b`|
|最も厳しい RAM、フル コントロール |ラマ.cpp + Q4_K_M GGUF |
| MacBook 開発マシン | MLX または Ollama |
| 8 GB VRAM 実験で 70B |エアLLM |
|エアギャップ付き USB スティック | llamafile またはポータブル KoboldCPP |
|本番 API スループット | **これらではありません** — GPU では vLLM を使用してください ([プラットフォームに関する注意](iii-local-run-platforms.md)) |

## 7. 現実的な期待 (CPU)

|モデル |大まかなトークン/秒 (最新のラップトップ CPU) |
|------|--------------------------------------|
| qwen2.5-コーダー 1.5B Q4 | 20–45 |
| 1–3B Q4 | 15–40 |
| qwen2.5-コーダー 7B Q4 | 3–12 |
| 13B Q4 | 1–5 |

数値は、AVX サポート、コア数、電力制限によって大きく異なります。コーディングのサポートについては、**`qwen2.5-coder:7b`GPU** または **ホストされた API** の場合は、通常、CPU** の **7B を上回ります。

＃＃ 関連している

- [ハグフェイスからダウンロード](ii-downloading-from-huggingface.md)
- [ローカル実行プラットフォーム](iii-local-run-platforms.md)
- [モデル RAM の要件](iv-model-ram-requirements.md）

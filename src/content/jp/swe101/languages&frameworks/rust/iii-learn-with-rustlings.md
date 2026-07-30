---
label: "III"
subtitle: "Rustリングと一緒に学ぶ"
group: "Rust"
groupOrder: 1
order: 3
---
Rust — パート III: Rust リングで学ぶ

**[Rustリング](https://rustlings.rust-lang.org/)** は公式の実践的な演習トラックです。壊れた小さなプログラムをコンパイルしてテストに合格するまで修正します。これらのメモと [Rust プログラミング言語](**と併せて** 使用してください)https://doc.rust-lang.org/book/) 本 — 一人で読むのは、入力したり意図的に何かを壊したりするよりも時間がかかります。

## 1. Rustリングとは

| | |
|---|---|
| **形式** |数十の小さなエクササイズ`exercises/`トピックごとにグループ化 |
| **あなたの仕事** |探す **`TODO`** / **`todo!()`**、ファイルを編集して**を作成します`cargo`** 幸せ |
| **ツール** | **`rustlings`** CLI は、適切な順序で演習を説明します。
| **目標** | **のマッスルメモリー`struct`**、**`impl`**、**`match`**、所有権、イテレータなど |

Rustlings は、パート I ～ II または書籍に代わるものではありません**。それらを**強化**します。パート I (組織 + 所有権) およびパート II (**`cargo`**)、開始する準備ができました。

##2.前提条件

1. **Rust ツールチェーン** — [rust-lang.org/tools/install](https://www.rust-lang.org/tools/install) (`rustup`、`cargo`、`rustc`）。
2.**`cargo build`お使いのマシン上で動作します**。**Windows** では、最初に **MSVC C++ Build Tools** をインストールします (**パート I**、§1 を参照)。
3. **エディタ** — [rust-analyzer](https://rust-analyzer.github.io/) VS コード (またはそれをサポートするエディター) 内にあるため、エラーがインラインで表示されます。

Rustlings をインストールする前に更新してください。

```text
rustup update
```

## 3. インストールと初期化

実験を作成する任意のディレクトリから:

```text
cargo install rustlings
rustlings init
cd rustlings
rustlings
```

インストールが失敗した場合は、次のことを試してください。

```text
cargo install rustlings --locked
```

**`rustlings`見つかりませんか?** Cargo はバイナリを ** に置きます`~/.cargo/bin`** (Linux/macOS) または **`%USERPROFILE%\.cargo\bin`** (Windows)。そのディレクトリを **PATH** に追加し、**新しい** ターミナルを開きます。

**Windows** では、**[Windows ターミナル](https://aka.ms/terminal)** 最高のウォッチ モード エクスペリエンスを実現します (**WSL** を使用している場合はこれを含みます)。

## 4. セッションの仕組み

1.**`rustlings`** は **監視モード** を開始します — 現在の演習を実行し、** の下にファイルを保存すると再実行します`exercises/`**。
2. コンパイラ エラーを読み取り、演習ファイルを編集し、再度保存します。
3. 演習が終了すると、Rustlings は次の演習に進みます。

視聴モードで便利なキー:

|キー |アクション |
|-----|----------|
| **`h`** |現在の演習のヒント |
| **`l`** |インタラクティブ **エクササイズ リスト** (完了 vs 保留、ジャンプ、リセット) |
| **`r`** |現在のエクササイズを再実行します (** の場合にも使用されます)`--manual-run`**が設定されています） |

ファイルの監視が失敗した場合 (一部の VM/ コンテナー)、次を使用します。

```text
rustlings --manual-run
```

次に**を押します`r`** 各保存後。

各トピックフォルダーには**があります`README.md`** リンク付き - そのセクションの演習に入る前にざっと読んでください。

## 5. 練習する内容 (およびそれを取り上げた場所)

| Rustリング領域 (通常) |補強 |
|--------------------------|---------------|
|変数、関数 |パート I — プログラムの形状 |
| **`struct`**、**`enum`**、**`match`** |パート I — 組織 |
|所有権、借用、スライス |パート I — 所有権 |
| **`struct`/`enum`メソッド**、モジュール |パート I — **`impl`**、モジュール |
|コレクション、**`String`** |本ch. 8 + 演習 |
|エラー処理 **`Result`** |パート I — **`Result`**、書籍ch. 9 |
|ジェネリック医薬品、**`trait`**、寿命 |本ch. 10–11 (基本の後にさらに深く進みます) |
|テスト、**`clippy`**、**`macro`s** |パート II — **`cargo test`**、品質習慣 |

演習で **クレート** または ** について言及している場合`Cargo.toml`**、**パート II** [貨物と共有可能なクレート](ii-cargo-and-shareable-crates.md）。

## 6. 推奨される学習順序

```text
Part I (this track)     →  skim organization + ownership
       ↓
rustlings init          →  run `rustlings` daily in short blocks
       ↓
The Book (in parallel)  →  same chapters as the exercise topic
       ↓
Part II (Cargo)         →  when exercises touch modules / deps
       ↓
Your own `cargo new`    →  tiny bin + lib project from scratch
```

練習中の **オフライン ドキュメント**:

```text
rustup doc --book
rustup doc --std
```

## 7. 行き詰まったとき

1. **を押します`h`** 組み込みヒントの監視モード。
2. トピックを再読します **`README.md`**その中に**`exercises/...`**フォルダー。
3. [Rustlings Q&A ディスカッション](https://github.com/rust-lang/rustlings/discussions/categories/q-a）。
4. [Rust Book]( と比較します)https://doc.rust-lang.org/book/) そのトピックの章 — Rustlings は、書籍の代わりにではなく、**並列** で実行されるように設計されています。

難しいと感じるからといってエクササイズを永久にスキップしないでください。** を使用してください。`l`** 先に進んで戻ってくること。使用 **`r`クリーンなファイルが必要な場合は、リスト内の ** を使用して演習をリセットします。

## 8. Rustリングのその後

- 小さな ** を構築する`cargo new`** プロジェクト (CLI ツール、パーサー、ゲーム ループ)。
- **ワークスペース**を公開または分割するときに、**パート II** をもう一度お読みください。
- オープンソース Rust クレートに貢献するか、[コミュニティ演習](https://rustlings.rust-lang.org/community-exercises/）他の人に教えたい場合。

## 9. 関連

- [rustlings.rust-lang.org](https://rustlings.rust-lang.org/) — セットアップ、使用法、デモ
- [github.com/rust-lang/rustlings](https://github.com/rust-lang/rustlings) — 出典と問題点
- **パート I** — [基本とツールチェーン](i-basics-and-toolchain.md)
- **パート II** — [貨物と共有可能な箱](ii-cargo-and-shareable-crates.md)
- **パート IV** — 非同期、落とし穴、Tokio [Async Rust](iv-async.md)
- [Rust 本](https://doc.rust-lang.org/book/)

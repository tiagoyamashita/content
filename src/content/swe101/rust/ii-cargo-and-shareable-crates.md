---
label: "II"
subtitle: "貨物と共有可能なクレート"
group: "さび"
groupOrder: 1
order: 2
---
Rust — パート II: カーゴと共有可能なクレート

**Cargo** は、Rust の **パッケージ マネージャーおよびビルド ツール**です。依存関係をダウンロードし、コードをコンパイルし、テストを実行し、他の人が再利用できる **クレート** (Rust パッケージ) を公開します。

**`rustup`**、**`rustc`**、および Windows **MSVC** リンカーのセットアップについては、**パート I** [基本とツールチェーン](i-basics-and-toolchain.md) を参照してください。

## 1. 貨物とは何か

|ツール |役割 |
|------|------|
| **`rustup`** | Rust のバージョンとターゲットをインストールします。
| **`rustc`** | `.rs` ファイルをバイナリまたはライブラリにコンパイルします。
| **`cargo`** |プロジェクトのワークフロー: deps、ビルド、テスト、実行、公開 |

実際のプロジェクトで **`rustc`** を手動で呼び出すことはほとんどありません。**`cargo`** は適切なフラグを渡し、依存関係をリンクします。

すべての Cargo プロジェクトには、ルートに **`Cargo.toml`** マニフェストがあります (オプションで **ワークスペース**にさらにマニフェストがあります)。

```toml
[package]
name = "greeting"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"

[dependencies]
serde = { version = "1", features = ["derive"] }
```

|セクション |目的 |
|----------|----------|
| **`[package]`** |名前、バージョン、エディション、ライセンス、説明 |
| **`[dependencies]`** | **crates.io**、**git**、または **path** の他のクレート |
| **`[dev-dependencies]`** |テスト/サンプル/ベンチのみ |
| **`[[bin]]`** |追加のバイナリ (オプション、デフォルトは `src/main.rs`) |

## 2. クレートの種類

**クレート** は 1 つのコンパイル単位であり、次のいずれかです。

- **バイナリ クレート** — 実行可能ファイルを生成します。 `src/main.rs` (または宣言された `[[bin]]`) には **`fn main()`** が必要です。
- **ライブラリクレート** — 他のリンクに対する **`rlib`** を生成します。ルートは **`src/lib.rs`** です。 **いいえ** `main`。

**共有可能な** コードは、ほとんどの場合、**ライブラリ クレート** (または **ワークスペース** を介して 1 つのリポジトリ内の複数のライブラリ) 内に存在します。

```text
cargo new my_app --bin      # executable
cargo new my_utils --lib    # shareable library
```

## 3. 日常の貨物コマンド

```text
cargo new NAME --lib          # create library project
cargo build                 # debug build → target/debug/
cargo build --release       # optimized → target/release/
cargo run                   # build + run default binary
cargo test                  # unit + integration tests
cargo check                 # type-check only (fast)
cargo doc --open            # build API docs
cargo fmt                   # format (rustfmt)
cargo clippy                # lints (needs clippy component)
```

## 4. 例: 独自の共有可能なライブラリを構築する

### ステップ 1 — ライブラリクレートを作成する

```text
cargo new greeter_utils --lib
cd greeter_utils
```

**`Cargo.toml`:**

```toml
[package]
name = "greeter_utils"
version = "0.1.0"
edition = "2024"
description = "Small greeting helpers"
license = "MIT"

[dependencies]
```

**`src/lib.rs`** — **`pub`** 項目のみがパブリック API の一部です。

```rust
/// Build a greeting for `name`. Empty names become "world".
pub fn greet(name: &str) -> String {
    let who = if name.trim().is_empty() {
        "world"
    } else {
        name.trim()
    };
    format!("Hello, {who}!")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn default_world() {
        assert_eq!(greet(""), "Hello, world!");
    }
}
```

確認する：

```text
cargo test
```

### ステップ 2 — 別のプロジェクトから使用します (ローカル パス)

**ディスク上**のライブラリに依存するバイナリを作成します (まだ公開されていません)。

```text
cd ..
cargo new hello_app --bin
```

**`hello_app/Cargo.toml`** — **パスの依存関係**:

```toml
[package]
name = "hello_app"
version = "0.1.0"
edition = "2024"

[dependencies]
greeter_utils = { path = "../greeter_utils" }
```

**`hello_app/src/main.rs`:**

```rust
fn main() {
    println!("{}", greeter_utils::greet("Rust"));
}
```

```text
cd hello_app
cargo run
# Hello, Rust!
```

**`path = "../greeter_utils"`** はモノリポジトリと学習に最適です。 Cargo は、依存関係グラフの一部としてライブラリをコンパイルします。

### ステップ 3 — ワークスペース (複数のクレート、1 つのリポジトリ)

**1 つの** リポジトリ内の複数の共有可能なクレートとアプリの場合は、**ワークスペース**を使用します。

**ルート `Cargo.toml`:**

```toml
[workspace]
resolver = "2"
members = [
    "greeter_utils",
    "hello_app",
]
```

各メンバーは独自の **`Cargo.toml`** を保持します。 **`hello_app/Cargo.toml`** では、パスは次のようになります。

```toml
greeter_utils = { path = "../greeter_utils" }
```

ワークスペースのルートから:

```text
cargo test --workspace
cargo run -p hello_app
```

## 5. ライブラリクレート内のモジュール

ファイル間で実装を分割します。クレートのルート **`lib.rs`** はモジュールを宣言します。

```text
greeter_utils/
  Cargo.toml
  src/
    lib.rs
    formal.rs
```

**`src/lib.rs`:**

```rust
mod formal;

pub use formal::formal_greet;

pub fn greet(name: &str) -> String {
    format!("Hello, {}!", name.trim())
}
```

**`src/formal.rs`:**

```rust
pub fn formal_greet(name: &str) -> String {
    format!("Good day, {}.", name.trim())
}
```

消費者には **`greeter_utils::greet`** および **`greeter_utils::formal_greet`** が表示されます。 **`formal`** は、**`pub mod formal`** しない限り非公開のままです。

## 6. マシンを超えた共有

|方法 | `Cargo.toml` スニペット |いつ |
|------|----------------------|------|
| **パス** | `foo = { path = "../foo" }` |同じリポジトリ/ローカル開発 |
| **Git** | `foo = { git = "https://github.com/you/foo", branch = "main" }` |プライベートまたは未公開のコード |
| **crates.io** | `foo = "0.2"` または `foo = { version = "0.2", features = ["serde"] }` |公開されたリリース |

### crates.io に公開する (概要)

1. [https://crates.io](88) でアカウントを作成し、API トークンを使用して **`cargo login`** を実行します。
2. **`Cargo.toml`**に**`description`**、**`license`**、**`repository`**を入力します。
3. ライブラリクレートディレクトリから **`cargo publish --dry-run`**、次に **`cargo publish`**。
4. 新しいリリースごとに **`version`** とバンプします (セムバー: 速報→メジャー、機能→マイナー、修正→パッチ)。

さらに他の人は次のように付け加えます。

```toml
greeter_utils = "0.1.0"
```

## 7. 機能 (オプションの API サーフェス)

依存関係のコンパイル時オプションを有効にします。

```toml
[features]
default = ["std"]
std = []
extra = ["dep:serde"]
```

```toml
[dependencies]
serde = { version = "1", optional = true }
```

```rust
#[cfg(feature = "extra")]
pub fn greet_json(name: &str) -> String {
    // ...
}
```

扶養家族のオプトイン: **`greeter_utils = { version = "0.1", features = ["extra"] }`**。

## 8. 共有可能な箱に何を入れるか

- **`pub`** 発信者が必要とするもののみ。ヘルパーを非公開にしてください。
- **`///`** の **ドキュメント** パブリック アイテム — **`cargo doc`** に表示されます。
- 同じファイル内の **テスト** (`#[cfg(test)]`) または **`tests/*.rs`** 統合テスト。
- **`examples/*.rs`** の **例** — **`cargo run --example demo`** で実行します。
- 公開する前に **README** と **LICENSE** を適用してください。

## 9. 迅速なトラブルシューティング

|問題 |チェック |
|----------|----------|
| `linker not found` (Windows) |パート I — MSVC ビルド ツール |
| `failed to resolve` 依存関係 |クレート名のスペル。ネットワーク; git URL / パス |
|パブリック API の `private` タイプ |タイプ **`pub`** をマークするか、**`pub fn`** の後ろに隠します |
|同じクレートの 2 つのバージョン | **`cargo tree`** — ワークスペース内のバージョンを統合する |

## 10. 関連

- **パート I** — 所有権、**`match`**、基本 [基本とツールチェーン](i-basics-and-toolchain.md)
- **パート III** — **Rustlings** を使った実践練習 [Rustlings で学ぶ](iii-learn-with-rustlings.md)
- **パート IV** — **`async`/`await`**、ランタイム、一般的な落とし穴 [Async Rust](iv-async.md)
- [The Cargo Book](89) — マニフェスト、ワークスペース、出版に関する公式リファレンス

---
label: "II"
subtitle: "貨物と共有可能なクレート"
group: "Rust"
groupOrder: 1
order: 2
---
Rust — パート II: 貨物と共有可能な箱

**Cargo** は Rust の **パッケージ マネージャーおよびビルド ツール** です。依存関係をダウンロードし、コードをコンパイルし、テストを実行し、他のユーザーが再利用できる **クレート** (Rust パッケージ) を公開します。

**パート I** [基本とツールチェーン](i-basics-and-toolchain.md） のために **`rustup`**、**`rustc`**、および Windows **MSVC** リンカーのセットアップ。

## 1. 貨物とは何か

|ツール |役割 |
|------|------|
| **`rustup`** | Rust バージョンとターゲットをインストールします。
| **`rustc`** |コンパイルします`.rs`ファイルをバイナリまたはライブラリに変換する |
| **`cargo`** |プロジェクトのワークフロー: deps、ビルド、テスト、実行、公開 |

** を呼び出すことはほとんどありません`rustc`** 実際のプロジェクトで手作業で行う — **`cargo`** は適切なフラグを渡し、依存関係をリンクします。

すべての Cargo プロジェクトには ** があります`Cargo.toml`** ルートにあるマニフェスト (および必要に応じて ** ワークスペース ** にさらにマニフェスト)。

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
| **`[[bin]]`** |追加のバイナリ (オプション、デフォルトは`src/main.rs`) |

## 2.クレートの種類

**クレート** は 1 つのコンパイル単位であり、次のどれかです。

- **バイナリ クレート** — 実行可能ファイルを生成します。 **が必要です`fn main()`** で`src/main.rs`(または宣言された`[[bin]]`）。
- **ライブラリクレート** — **を生成します`rlib`** 他のリンク先。ルートは**です`src/lib.rs`**; **いいえ**`main`。

**共有可能な** コードは、ほとんどの場合、**ライブラリ クレート** (または **ワークスペース** を介して 1 つのリポジトリ内の複数のライブラリ) 内に存在します。

```text
cargo new my_app --bin      # executable
cargo new my_utils --lib    # shareable library
```

## 3. 日常の荷物コマンド

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

**`src/lib.rs`** - のみ **`pub`** アイテムはパブリック API の一部です:

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

### ステップ 2 — 別のプロジェクトから使用します (ローカルパス)

**ディスク上**のライブラリに依存するバイナリを作成します (まだ公開されていません)。

```text
cd ..
cargo new hello_app --bin
```

**`hello_app/Cargo.toml`** — **パス依存性**:

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

**根`Cargo.toml`:**

```toml
[workspace]
resolver = "2"
members = [
    "greeter_utils",
    "hello_app",
]
```

各メンバーは独自の ** を保持します`Cargo.toml`**。で **`hello_app/Cargo.toml`**、パスは次のようになります:

```toml
greeter_utils = { path = "../greeter_utils" }
```

ワークスペースのルートから:

```text
cargo test --workspace
cargo run -p hello_app
```

## 5. ライブラリクレート内のモジュール

ファイル間で実装を分割します。クレートルート**`lib.rs`** モジュールを宣言します:

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

消費者は**を参照してください`greeter_utils::greet`** そして **`greeter_utils::formal_greet`**; **`formal`** あなたがしない限り、** は非公開のままです **`pub mod formal`**。

## 6. マシンを超えた共有

|方法 |`Cargo.toml`スニペット |いつ |
|------|----------------------|------|
| **パス** |`foo = { path = "../foo" }`|同じリポジトリ/ローカル開発 |
| **Git** |`foo = { git = "https://github.com/you/foo", branch = "main" }`|プライベートまたは未公開のコード |
| **crates.io** |`foo = "0.2"`または`foo = { version = "0.2", features = ["serde"] }`|公開されたリリース |

### crates.io に公開する (概要)

1. [でアカウントを作成します。https://crates.io](https://crates.io) そして ** を実行してください`cargo login`** API トークンを使用します。
2. **を入力します`description`**、**`license`**、**`repository`** で **`Cargo.toml`**。
3.**`cargo publish --dry-run`** それから **`cargo publish`** ライブラリクレートディレクトリから。
4. バンプ **`version`** すべての新しいリリース (セムバー: 破壊→メジャー、機能→マイナー、修正→パッチ)。

さらに他の人は次のように付け加えます。

```toml
greeter_utils = "0.1.0"
```

## 7. 機能 (オプションの API 表面)

依存関係のコンパイル時オプションは有効になります。

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
- **公開アイテムを ** 文書化**`///`** — ** に表示されます`cargo doc`**。
- 同じファイル内の **テスト** (`#[cfg(test)]`） または **`tests/*.rs`** 統合テスト。
- **例** (**)`examples/*.rs`** — ** で実行`cargo run --example demo`**。
- **README** および **LICENSE** 公開前。

## 9. 迅速なトラブルシューティング

|問題 |チェック |
|----------|----------|
|`linker not found`(Windows) |パート I — MSVC ビルド ツール |
|`failed to resolve`依存関係 |クレート名のスペル。ネットワーク; git URL / パス |
|`private`「パブリック API |」と入力します。マークの種類**`pub`** または ** の後ろに隠します`pub fn`** |
|同じクレートの 2 つのバージョン | **`cargo tree`** - ワークスペース内のバージョンを統合する |

## 10. 関連

- **パート I** — 所有権、**`match`**、基本 [基本とツールチェーン](i-basics-and-toolchain.md)
- **パート III** — **Rustlings** による実践演習 [Rustlings で学習](iii-learn-with-rustlings.md)
- **パート IV** — **`async`/`await`**、ランタイム、一般的な落とし穴 [Async Rust](iv-async.md)
- [カーゴブック](https://doc.rust-lang.org/cargo/) — マニフェスト、ワークスペース、パブリッシングの公式リファレンス

---
label: "I"
subtitle: "基本とツールチェーン"
group: "さび"
groupOrder: 1
order: 1
---
Rust — パート I

Rust がコードを **整理**する方法 (クレート、モジュール、**`struct`**、**`impl`**、**`trait`**、**`enum`**)、**`cargo`** ワークフロー、高レベルでの所有権、**`match`** / **`Option`** を、後のノートで共有する方法について説明します。ベースライン。

## 1. ツールチェーン & `cargo`
- **`rustup`** 安定版/ベータ版/夜間ツールチェーンとターゲットをインストールします。 **`rustc`** コンパイルします。 **`cargo`** はビルド、テスト、依存関係を推進します。
- **`cargo new scratch --bin`** → `src/main.rs` のバイナリ クレート; **`cargo new libname --lib`** → `src/lib.rs`の図書館。
- **`cargo build`** / **`cargo run`** / **`cargo test`** は日常的なコマンドです。 **`cargo check`** リンクせずに型チェックを行います (高速反復)。

### Windows: Visual Studio ビルド ツール (C++)

**Windows** では、デフォルトの Rust ツールチェーンは **MSVC** ABI をターゲットとしています。 **`rustc`** および **`cargo`** には、Rust コンパイラ自体ではなく、**Microsoft の C++ ビルド ツール** に付属する C++ リンカーと Windows SDK ライブラリが必要です。

**`rustup`** が前提条件を要求する前 (またはその時点) に、これらのうち **1 つ** をインストールします。

- **[Visual Studio Build Tools](134)** — ワークロード **「C++ によるデスクトップ開発」** (ほとんどの Rust 作業には十分)、または  
- 同じ C++ ワークロードを備えたフル **Visual Studio** エディション。

これらがないと、**`cargo build`** は **`link.exe`**、**`msvcrt`**、または **「リンカーが見つかりません」** に関するエラーで失敗することがよくあります。インストール後、**新しい**ターミナルを開き、**`cargo build`**を再度実行します。

Windows 上の **`rustup`** は、MSVC の前提条件を自動的にインストールすることを提案する場合があります。それを受け入れて大丈夫です。代わりに **GNU** ツールチェーン (`x86_64-pc-windows-gnu`) を使用する場合は、**MinGW** が必要です。ほとんどのチュートリアルとクレートは Windows 上の **MSVC** を前提としています。

```text
cargo new hello --bin
cd hello
cargo run
```

## 2. Rust コードの構成方法

**Java** または **C#** を知っている場合は、Rust に親しみを感じるところもありますが、責任の分割方法は異なります。**データ**、**メソッド**、**共有動作 (特性)** は、コンパイラーがつなぎ合わせた別個の部分です。

### 全体像: クレート → モジュール → アイテム

```text
my_project/                 ← one Cargo package
  Cargo.toml                ← name, version, dependencies
  src/
    main.rs                 ← binary entry (or lib.rs for a library)
    user.rs                 ← optional extra module file
```

|レイヤー |それは何ですか | Java の大まかな例え |
|------|-----------|--------|
| **木箱** | 1 つのコンパイル済みユニット (アプリまたはライブラリ) |出荷する **モジュール** / JAR |
| **モジュール** |型と関数の名前空間 (`mod`、`use`) | **`package`** |
| **アイテム** | `struct`、`enum`、`fn`、`trait`、`const`、… |クラス、インターフェイス、メソッド |

**`main.rs`** (または **`lib.rs`**) は **クレート ルート**です。他のすべては **`mod`** で引き込まれ、**`pub`** で露出されます。

### `struct` — データのみ (本体にメソッドを *含まない* クラスなど)

**`struct`** には **フィールド** が保持されます。これは、型宣言内にメソッドを持つクラスではありません**。

```rust
struct User {
    id: u64,
    name: String,
    active: bool,
}
```

- **継承なし** — Rust は 58 をサブクラス化しません。
- 構造体自体に **`null`** はありません。「欠落している可能性がある」フィールドには **`Option<T>`** を使用します。
- **`#[derive(Debug, Clone)]`** は、一般的な定型文を自動生成します (IDE で生成された `toString` / コピー ヘルパーなど)。

**`struct` ≈ 「フィールドを宣言するだけのクラス」** (POJO / レコード スタイル データ) と考えてください。

### `impl` — メソッドが存在する場所 (クラスのメソッド ブロックなど)

メソッドは、`struct` 内ではなく、別の **`impl TypeName { ... }`** ブロックに記述されます。

```rust
impl User {
    // Associated function — no `self`; like Java `static`
    fn new(id: u64, name: impl Into<String>) -> Self {
        User {
            id,
            name: name.into(),
            active: true,
        }
    }

    // Method — `&self` = borrow read-only (like instance method on immutable ref)
    fn display_name(&self) -> &str {
        &self.name
    }

    // `&mut self` = exclusive mutable borrow (like non-final instance method)
    fn deactivate(&mut self) {
        self.active = false;
    }
}
```

| `impl` |意味 |ジャワっぽい |
|----------|-----------|----------|
| **`fn foo(...)`** |関連機能 | **`static void foo`** |
| **`fn foo(&self)`** |メソッド、読み取り専用 |インスタンス メソッド、突然変異なし |
| **`fn foo(&mut self)`** |メソッド、フィールドを変更できる |状態を変更するインスタンス メソッド |
| **`fn foo(self)`** |値を消費（移動） |レア; 「所有権を取得して終了」のように |

サイトに電話をかける:

```rust
let mut u = User::new(1, "Ada");
println!("{}", u.display_name());
u.deactivate();
```

**無料関数** — モジュールスコープでの `fn`、どの `impl` にも含まれていない — 通常かつ慣用的で​​す (ヘルパー、パーサー、`main`)。

### `enum` — 固定バリアントを持つ型 (「文字列定数」よりも優れています)

**`enum`** には **名前付きバリアント**がリストされています。各バリアントはデータを運ぶことができます。これは、クラス階層を使用せずに「いくつかの形状のうちの 1 つ」をモデル化する Rust の方法です。

```rust
enum OrderStatus {
    Draft,
    Paid { amount_cents: u64 },
    Shipped { tracking: String },
    Cancelled,
}
```

**`Option<T>`** および **`Result<T, E>`** は、標準ライブラリの列挙型です。

```rust
enum Option<T> {
    None,
    Some(T),
}

enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

Java の類似点: **`enum`** + **シールされたインターフェイス** / タグ付きユニオン — ただし、**`match`** で徹底的にチェックされます。

### `trait` — 共有動作 (インターフェース + 場合によってはデフォルトのメソッドなど)

**`trait`** は、他のタイプが**実装できる**機能**を定義します。ジェネリックと **`dyn Trait`** はポリモーフィズムにトレイトを使用します。

```rust
trait Describable {
    fn describe(&self) -> String;

    // Default implementation — implementors can override
    fn short_label(&self) -> String {
        self.describe()
    }
}

impl Describable for User {
    fn describe(&self) -> String {
        format!("User#{} ({})", self.id, self.name)
    }
}
```

|コンセプト |さび |ジャワ |
|-------|------|------|
|行動に関する契約 | **`trait`** | **`interface`** |
| 「インターフェイスの実装」 | **`impl Trait for Type`** | **`class X implements Y`** |
|組み込みの特性 | **`Debug`**、**`Clone`**、**`Iterator`**、… | **`Comparable`**、**`Serializable`**、… |

**`impl Trait for Type`** は、タイプと **同じファイル** に存在することも、別のモジュール (可視性ルールを使用) に存在することもできます。 Java とは異なり、通常、ランダム クレート内の外部型に特性 impl を追加することは**できません** (**孤立ルール**により一貫性が保たれます)。

一般的なパターン — std 特性を実装します。

```rust
use std::fmt;

impl fmt::Display for User {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.name)
    }
}
```

### 可視性: `pub` およびモジュール

- 項目はデフォルトでは親モジュールに対して**プライベート**です。
- **`pub`** は、それらを親モジュールに公開し、(再エクスポートする場合) 他のクレートに公開します。
- **`mod billing;`** は **`billing.rs`** または **`billing/mod.rs`** をロードします。
- **`use crate::user::User;`** は名前をスコープに含めます (**`import`** など)。

```text
src/
  lib.rs          mod user; pub use user::User;
  user.rs         pub struct User { ... }  + impl blocks
```

### メンタルマップ: Java クラスと Rust の部分

```text
Java (one class file)              Rust (split on purpose)
─────────────────────              ─────────────────────────
class User { fields }      →       struct User { fields }
  methods in same class    →       impl User { methods }
  implements Serializable  →       impl Serialize for User { ... }
  extends / implements     →       traits + composition (no extends)
```

### 1 つのファイルで結合する

```rust
struct Rectangle {
    width: u32,
    height: u32,
}

impl Rectangle {
    fn area(&self) -> u32 {
        self.width * self.height
    }
}

trait Drawable {
    fn draw(&self);
}

impl Drawable for Rectangle {
    fn draw(&self) {
        println!("rect {}x{}", self.width, self.height);
    }
}

fn main() {
    let r = Rectangle { width: 10, height: 5 };
    println!("area = {}", r.area());
    r.draw();
}
```

## 3. プログラムの形状
- **`fn main()`** はバイナリ エントリ ポイントです。多くの場合、ステートメントは **`;`** で終わります。ブロック内の最後の式は **`return`** なしで返すことができます。

```rust
fn main() {
    let n = double(21);
    println!("{}", n);
}

fn double(x: i32) -> i32 {
    x * 2
}
```

## 4. 所有権 (リードオンスメンタルモデル)
- すべての値には **1 人の所有者**がいます。割り当ては非**`Copy`**値を**移動します(例: **`String`**、**`Vec`**)。**`clone()`**または借用しない限り、古いバインディングは後で使用できません。
- **`&T`** 不変借用。 **`&mut T`** 排他的可変借用 — コンパイラは、可変状態のエイリアスとなる重複した使用を拒否します。
- **`i32`**、**`bool`**、**`char`** のようなプリミティブは **`Copy`** を実装します。これらは移動するのではなく単純に複製します。

```rust
let s = String::from("hi");
// let t = s;        // move: `s` is invalid here
let t = s.clone();  // explicit duplicate
println!("{} {}", s, t);

let mut v = vec![1, 2, 3];
v.push(4);
let first = v[0];
println!("first = {}, len = {}", first, v.len());
```

## 5. パターンマッチング & `Option`
- **`match`** は完全です。**`Option<T>`** では **`Some`** および **`None`** を処理する必要があります (または、単一のケースの場合は **`if let`** / **`while let`** を使用します)。
- **`Result<T, E>`** はエラー イディオムです。 **`Result`** を返す関数内の **`?`** はエラーを伝播します。

```rust
fn loud(name: Option<&str>) -> String {
    match name {
        Some(s) => s.to_uppercase(),
        None => String::from("(anonymous)"),
    }
}

fn parse_u8(s: &str) -> Result<u8, std::num::ParseIntError> {
    s.parse::<u8>()
}
```

## 6. 列挙型に関する `match` (組織が重要な理由)

**`enum`** バリアントを取得すると、**`match`** は **すべて** のケースを処理することを強制します。コンパイラは欠落しているブランチを検出します。

```rust
fn label(status: OrderStatus) -> &'static str {
    match status {
        OrderStatus::Draft => "draft",
        OrderStatus::Paid { .. } => "paid",
        OrderStatus::Shipped { .. } => "shipped",
        OrderStatus::Cancelled => "cancelled",
    }
}
```

## 7. モジュールとクレート (要約)

- **`mod foo;`** は **`foo.rs`** または **`foo/mod.rs`** を引き込みます。デフォルトでは、アイテムはその親に対してプライベートです。 **`pub`** はそれらを公開します。
- **バイナリ クレート**は **`main`** を実行します。 **ライブラリクレート**は**`pub`**アイテムを他のクレートにエクスポートします(**パートII** - カーゴおよび共有可能なクレートを参照)。

次: **パート II** — **カーゴ**、ライブラリクレート、ワークスペース [カーゴおよび共有可能なクレート](ii-cargo-and-shareable-crates.md)。 **パート III** — **[カサカサ音](135)** [カサカサ音で学ぶ](iii-learn-with-rustlings.md) で練習します。後のメモでは、実際のクレート境界での **ライフタイム**、**イテレータ**、**エラー処理**について詳しく説明することができます。

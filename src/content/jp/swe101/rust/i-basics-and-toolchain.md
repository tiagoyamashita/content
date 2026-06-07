---
label: "I"
subtitle: "基本とツールチェーン"
group: "Rust"
groupOrder: 1
order: 1
---
Rust — パート I

Rust **コードを**編成する方法 (クレート、モジュール、**)`struct`**、**`impl`**、**`trait`**、**`enum`**)、**`cargo`** ワークフロー、高レベルでの所有権、および **`match`** / **`Option`** したがって、後のノートはベースラインを共有します。

## 1. ツールチェーンと`cargo`- **`rustup`** 安定版/ベータ版/夜間のツールチェーンとターゲットをインストールします。 **`rustc`** コンパイルします。 **`cargo`** ビルド、テスト、依存関係を推進します。
- **`cargo new scratch --bin`** → バイナリクレート`src/main.rs`; **`cargo new libname --lib`** → ライブラリ付き`src/lib.rs`。
- **`cargo build`** / **`cargo run`** / **`cargo test`** は日常的なコマンドです。 **`cargo check`** リンクせずに型チェックを行います (高速反復)。

### Windows: Visual Studio ビルド ツール (C++)

**Windows** では、デフォルトの Rust ツールチェーンは **MSVC** ABI をターゲットとしています。 **`rustc`** そして **`cargo`** Rust コンパイラ自体ではなく、**Microsoft の C++ ビルド ツール** に付属する C++ リンカーと Windows SDK ライブラリが必要です。

** 前 (またはいつ) これらのうち ** 1 つ** をインストールしてください`rustup`** 前提条件を尋ねます:

- **[Visual Studio ビルド ツール](https://visualstudio.microsoft.com/visual-cpp-build-tools/)** — ワークロード **「C++ によるデスクトップ開発」** (ほとんどの Rust 作業に十分)、または  
- 同じ C++ ワークロードを備えたフル **Visual Studio** エディション。

それらがなければ、**`cargo build`** は ** に関するエラーで失敗することがよくあります`link.exe`**、**`msvcrt`**、または **「リンカーが見つかりません」**。インストール後、**新しい**ターミナルを開いて**を実行します`cargo build`** また。

**`rustup`** Windows では、MSVC 前提条件を自動的にインストールするよう提案される場合があります。それを受け入れて大丈夫です。 **GNU** ツールチェーン (`x86_64-pc-windows-gnu`) 代わりに、**MinGW** が必要です。ほとんどのチュートリアルとクレートは Windows 上の **MSVC** を前提としています。

```text
cargo new hello --bin
cd hello
cargo run
```

## 2. Rustコードの構成方法

**Java** または **C#** を知っている場合は、Rust に親しみを感じるところもありますが、責任の分担は異なります。**データ**、**メソッド**、**共有動作 (特性)** は、コンパイラーがつなぎ合わせた別個の部分です。

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
| **木箱** | 1 つのコンパイル済みユニット (アプリまたはライブラリ) |あなたが出荷する **モジュール** / JAR |
| **モジュール** |型と関数の名前空間 (`mod`、`use`) | **`package`** |
| **アイテム** |`struct`、`enum`、`fn`、`trait`、`const`、… |クラス、インターフェイス、メソッド |

**`main.rs`** （または **`lib.rs`**) は **クレート ルート**です。他のすべては ** で引き込まれます`mod`** と ** で露出`pub`**。

###`struct`— データのみ (本体にメソッドを *含まない* クラスのような)

A**`struct`** は **フィールド** を保持します。これは、型宣言内にメソッドを持つクラスではありません**。

```rust
struct User {
    id: u64,
    name: String,
    active: bool,
}
```

- **継承なし** — Rust はサブクラス化されません`struct`s.
- **いいえ`null`** 構造体自体に — ** を使用します`Option<T>`** 「欠落している可能性がある」フィールドの場合。
- **`#[derive(Debug, Clone)]`** 一般的な定型文を自動生成します (IDE-generated など)`toString`/ コピーヘルパー)。

考える： **`struct`≈ 「フィールドを宣言するだけのクラス」** (POJO / レコード形式のデータ)。

###`impl`— メソッドが存在する場所 (クラスのメソッド ブロックなど)

メソッドは別の**に書かれています`impl TypeName { ... }`** ブロック内ではありません`struct`。

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

|で`impl`|意味 | Javaっぽい |
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

**無料機能** —`fn`モジュールスコープではなく、どのモジュールスコープにもありません`impl`— 通常かつ慣用的なもの (ヘルパー、パーサー、`main`）。

###`enum`— 固定バリアントを持つ型 (「文字列定数」よりも優れています)

**`enum`** は **名前付きバリアント** をリストします。各バリアントはデータを運ぶことができます。これは、クラス階層を使用せずに「いくつかの形状のうちの 1 つ」をモデル化する Rust の方法です。

```rust
enum OrderStatus {
    Draft,
    Paid { amount_cents: u64 },
    Shipped { tracking: String },
    Cancelled,
}
```

**`Option<T>`** そして **`Result<T, E>`** は標準ライブラリの列挙型です。

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

Java の類似: **`enum`** + **シールされたインターフェイス** / タグ付きユニオン — ただし、** で徹底的にチェックされます`match`**。

###`trait`— 共有動作 (インターフェース + 場合によってはデフォルトのメソッドなど)

A**`trait`** 他のタイプが **実装できる** **機能**を定義します。ジェネリックと**`dyn Trait`** ポリモーフィズムにトレイトを使用します。

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

|コンセプト | Rust | Java |
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

### 可視性:`pub`とモジュール

- 項目はデフォルトでは親モジュールに対して**プライベート**です。
- **`pub`** は、それらを親モジュールに公開し、(再エクスポートする場合) 他のクレートに公開します。
- **`mod billing;`** ロード **`billing.rs`** または **`billing/mod.rs`**。
- **`use crate::user::User;`** は名前をスコープに取り込みます (** のように)`import`**)。

```text
src/
  lib.rs          mod user; pub use user::User;
  user.rs         pub struct User { ... }  + impl blocks
```

### メンタルマップ: Java クラス vs Rust 個

```text
Java (one class file)              Rust (split on purpose)
─────────────────────              ─────────────────────────
class User { fields }      →       struct User { fields }
  methods in same class    →       impl User { methods }
  implements Serializable  →       impl Serialize for User { ... }
  extends / implements     →       traits + composition (no extends)
```

### 1つのファイルで考える

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
- **`fn main()`** はバイナリ エントリ ポイントです。ステートメントは ** で終わることがよくあります`;`**;ブロック内の最後の式は ** なしで返すことができます`return`**。

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
- すべての値には **1 人の所有者**がいます。割り当て ** 移動** 非 **`Copy`** 値 (例: **`String`**、**`Vec`**) — ** しない限り、古いバインディングは後で使用できません。`clone()`** または借りる。
- **`&T`** 不変の借用。 **`&mut T`** 排他的可変借用 — コンパイラーは、可変状態のエイリアスとなる重複した使用を拒否します。
- **のようなプリミティブ`i32`**、**`bool`**、**`char`** 埋め込む **`Copy`**: 移動するのではなく、単純に複製されます。

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

## 5. パターンマッチング&`Option`- **`match`** は完全です: **`Option<T>`** 処理を強制します **`Some`** そして **`None`** (または ** を使用します)`if let`** / **`while let`** 単一のケースの場合)。
- **`Result<T, E>`** はエラーイディオムです。 **`?`** を返す関数内で **`Result`** エラーが伝播します。

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

＃＃６。`match`enum について (組織が重要な理由)

**を入手したら`enum`** バリアント、**`match`** すべての**ケースを処理する必要があります。コンパイラは欠落しているブランチを検出します。

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

## 7. モジュールとクレート (概要)

- **`mod foo;`** 引き込みます **`foo.rs`** または **`foo/mod.rs`**。デフォルトでは、アイテムはその親に対してプライベートです。 **`pub`** はそれらを公開します。
- **バイナリ クレート**が実行されます**`main`**; **ライブラリクレート**は**をエクスポートします`pub`** 他のクレートのアイテム (**パート II** - 貨物と共有可能なクレートを参照)。

次: **パート II** — **Cargo**、ライブラリ クレート、ワークスペース [Cargo & shareable crates](ii-cargo-and-shareable-crates.md）。 **パート III** — **[Rustlings]( で練習する)https://rustlings.rust-lang.org/)** [Rustlings と一緒に学ぶ](iii-learn-with-rustlings.md）。後のメモでは、実際のクレート境界での **ライフタイム**、**イテレータ**、**エラー処理**について詳しく説明することができます。

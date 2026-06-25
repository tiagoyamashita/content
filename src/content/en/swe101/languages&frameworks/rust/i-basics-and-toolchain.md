---
label: "I"
subtitle: "Basics & toolchain"
group: "Rust"
groupOrder: 1
order: 1
---
Rust — Part I
How Rust **organizes** code (crates, modules, **`struct`**, **`impl`**, **`trait`**, **`enum`**), the **`cargo`** workflow, ownership at a high level, and **`match`** / **`Option`** so later notes share a baseline.

## 1. Toolchain & `cargo`
- **`rustup`** installs stable/beta/nightly toolchains and targets; **`rustc`** compiles; **`cargo`** drives builds, tests, and dependencies.
- **`cargo new scratch --bin`** → binary crate with `src/main.rs`; **`cargo new libname --lib`** → library with `src/lib.rs`.
- **`cargo build`** / **`cargo run`** / **`cargo test`** are the everyday commands; **`cargo check`** type-checks without linking (fast iteration).

### Windows: Visual Studio Build Tools (C++)

On **Windows**, the default Rust toolchain targets the **MSVC** ABI. **`rustc`** and **`cargo`** need a C++ linker and Windows SDK libraries that ship with **Microsoft’s C++ build tools** — not the Rust compiler itself.

Install **one** of these before (or when) **`rustup`** asks for prerequisites:

- **[Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)** — workload **“Desktop development with C++”** (enough for most Rust work), or  
- A full **Visual Studio** edition with the same C++ workload.

Without them, **`cargo build`** often fails with errors about **`link.exe`**, **`msvcrt`**, or **“linker not found”**. After installing, open a **new** terminal and run **`cargo build`** again.

**`rustup`** on Windows may offer to install the MSVC prerequisites automatically; accepting that is fine. If you use the **GNU** toolchain (`x86_64-pc-windows-gnu`) instead, you need **MinGW** — most tutorials and crates assume **MSVC** on Windows.

```text
cargo new hello --bin
cd hello
cargo run
```

## 2. How Rust code is organized

If you know **Java** or **C#**, Rust feels familiar in places but splits responsibilities differently: **data**, **methods**, and **shared behavior (traits)** are separate pieces the compiler stitches together.

### Big picture: crate → module → items

```text
my_project/                 ← one Cargo package
  Cargo.toml                ← name, version, dependencies
  src/
    main.rs                 ← binary entry (or lib.rs for a library)
    user.rs                 ← optional extra module file
```

| Layer | What it is | Rough Java analogy |
|-------|------------|-------------------|
| **Crate** | One compiled unit (your app or library) | A **module** / JAR you ship |
| **Module** | Namespace for types and functions (`mod`, `use`) | **`package`** |
| **Item** | `struct`, `enum`, `fn`, `trait`, `const`, … | classes, interfaces, methods |

**`main.rs`** (or **`lib.rs`**) is the **crate root**. Everything else is pulled in with **`mod`** and exposed with **`pub`**.

### `struct` — data only (like a class *without* methods in the body)

A **`struct`** holds **fields**. It is **not** a class with methods inside the type declaration.

```rust
struct User {
    id: u64,
    name: String,
    active: bool,
}
```

- **No inheritance** — Rust does not subclass `struct`s.
- **No `null`** on the struct itself — use **`Option<T>`** for “maybe missing” fields.
- **`#[derive(Debug, Clone)]`** auto-generates common boilerplate (like IDE-generated `toString` / copy helpers).

Think: **`struct` ≈ “a class that only declares fields”** (POJO / record-style data).

### `impl` — where methods live (like the method block of a class)

Methods are written in a separate **`impl TypeName { ... }`** block, not inside the `struct`.

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

| In `impl` | Meaning | Java-ish |
|-----------|---------|----------|
| **`fn foo(...)`** | Associated function | **`static void foo`** |
| **`fn foo(&self)`** | Method, read-only | instance method, no mutation |
| **`fn foo(&mut self)`** | Method, can mutate fields | instance method that changes state |
| **`fn foo(self)`** | Consumes the value (move) | rare; like “take ownership and finish” |

Call site:

```rust
let mut u = User::new(1, "Ada");
println!("{}", u.display_name());
u.deactivate();
```

**Free functions** — `fn` at module scope, not in any `impl` — are normal and idiomatic (helpers, parsers, `main`).

### `enum` — a type with fixed variants (better than “string constants”)

An **`enum`** lists **named variants**. Each variant can carry data — Rust’s way to model “one of several shapes” without class hierarchies.

```rust
enum OrderStatus {
    Draft,
    Paid { amount_cents: u64 },
    Shipped { tracking: String },
    Cancelled,
}
```

**`Option<T>`** and **`Result<T, E>`** are enums from the standard library:

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

Java analogy: **`enum`** + **sealed interfaces** / tagged unions — but checked exhaustively with **`match`**.

### `trait` — shared behavior (like an interface + sometimes default methods)

A **`trait`** defines **capabilities** other types can **implement**. Generics and **`dyn Trait`** use traits for polymorphism.

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

| Concept | Rust | Java |
|---------|------|------|
| Contract for behavior | **`trait`** | **`interface`** |
| “implements interface” | **`impl Trait for Type`** | **`class X implements Y`** |
| Built-in traits | **`Debug`**, **`Clone`**, **`Iterator`**, … | **`Comparable`**, **`Serializable`**, … |

**`impl Trait for Type`** can live in the **same file** as the type or in another module (with visibility rules). Unlike Java, you generally **cannot** add a trait impl for a foreign type in a random crate (the **orphan rule** keeps coherence).

Common pattern — implement a std trait:

```rust
use std::fmt;

impl fmt::Display for User {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}", self.name)
    }
}
```

### Visibility: `pub` and modules

- Items are **private** to their parent module by default.
- **`pub`** exposes them to parent modules and (when re-exported) to other crates.
- **`mod billing;`** loads **`billing.rs`** or **`billing/mod.rs`**.
- **`use crate::user::User;`** brings names into scope (like **`import`**).

```text
src/
  lib.rs          mod user; pub use user::User;
  user.rs         pub struct User { ... }  + impl blocks
```

### Mental map: Java class vs Rust pieces

```text
Java (one class file)              Rust (split on purpose)
─────────────────────              ─────────────────────────
class User { fields }      →       struct User { fields }
  methods in same class    →       impl User { methods }
  implements Serializable  →       impl Serialize for User { ... }
  extends / implements     →       traits + composition (no extends)
```

### One file tying it together

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

## 3. Program shape
- **`fn main()`** is the binary entry point. Statements often end with **`;`**; the last expression in a block can be returned without **`return`**.

```rust
fn main() {
    let n = double(21);
    println!("{}", n);
}

fn double(x: i32) -> i32 {
    x * 2
}
```

## 4. Ownership (readonce mental model)
- Every value has **one owner**. Assignment **moves** non-**`Copy`** values (e.g. **`String`**, **`Vec`**) — the old binding can’t be used afterward unless you **`clone()`** or borrow.
- **`&T`** immutable borrow; **`&mut T`** exclusive mutable borrow — the compiler rejects overlapping uses that would alias mutable state.
- Primitives like **`i32`**, **`bool`**, **`char`** implement **`Copy`**: they duplicate trivially instead of moving.

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

## 5. Pattern matching & `Option`
- **`match`** is exhaustive: **`Option<T>`** forces you to handle **`Some`** and **`None`** (or use **`if let`** / **`while let`** for a single case).
- **`Result<T, E>`** is the error idiom; **`?`** in functions that return **`Result`** propagates errors.

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

## 6. `match` on enums (why organization matters)

Once you have **`enum`** variants, **`match`** forces you to handle **every** case — the compiler catches missing branches.

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

## 7. Modules & crates (recap)

- **`mod foo;`** pulls in **`foo.rs`** or **`foo/mod.rs`**. Items are private to their parent by default; **`pub`** exposes them.
- A **binary crate** runs **`main`**; a **library crate** exports **`pub`** items for other crates (see **Part II** — Cargo & shareable crates).

Next: **Part II** — **Cargo**, library crates, workspaces [Cargo & shareable crates](ii-cargo-and-shareable-crates.md). **Part III** — practice with **[Rustlings](https://rustlings.rust-lang.org/)** [Learn with Rustlings](iii-learn-with-rustlings.md). Later notes can deepen **lifetimes**, **iterators**, and **error handling** on real crate boundaries.

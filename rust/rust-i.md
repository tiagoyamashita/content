---
label: "I"
subtitle: "Basics & toolchain"
group: "Rust"
groupOrder: 1
order: 1
---
Rust — Part I
The **`cargo`** workflow, crates vs binaries, core syntax, ownership at a high level, and **`match`** / **`Option`** so later notes have a shared baseline.

## 1. Toolchain & `cargo`
- **`rustup`** installs stable/beta/nightly toolchains and targets; **`rustc`** compiles; **`cargo`** drives builds, tests, and dependencies.
- **`cargo new scratch --bin`** → binary crate with `src/main.rs`; **`cargo new libname --lib`** → library with `src/lib.rs`.
- **`cargo build`** / **`cargo run`** / **`cargo test`** are the everyday commands; **`cargo check`** type-checks without linking (fast iteration).

```text
cargo new hello --bin
cd hello
cargo run
```

## 2. Program shape
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

## 3. Ownership (readonce mental model)
- Every value has **one owner**. Assignment **moves** non-**`Copy`** values (e.g. **`String`**, **`Vec`**) — the old binding can’t be used afterward unless you **`clone()`** or borrow.
- **`&T`** immutable borrow; **`&mut T`** exclusive mutable borrow — the compiler rejects overlapping uses that would alias mutable state.
- Primitives like **`i32`**, **`bool`**, **`char`** implement **`Copy`**: they duplicate trivially instead of moving.

```rust
let s = String::from("hi");
// let t = s;        // move: `s` is invalid here
let t = s.clone();  // explicit duplicate
println!("{} {}", s, t);

let mut v = vec![1, 2];
v.push(3);
let first = &v[0];
println!("{} {:?}", first, v);
```

## 4. Pattern matching & `Option`
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

## 5. Types you’ll see everywhere
- **`struct`** for named fields; **`enum`** for tagged unions (Rust’s **`Option`** / **`Result`** are enums).
- **`impl`** blocks attach methods and **`trait`** implementations.

```rust
#[derive(Debug, Clone)]
struct Point {
    x: i32,
    y: i32,
}

impl Point {
    fn new(x: i32, y: i32) -> Self {
        Point { x, y }
    }

    fn manhattan(&self) -> i32 {
        self.x.abs() + self.y.abs()
    }
}
```

## 6. Modules & visibility
- **`mod foo;`** pulls in **`foo.rs`** or **`foo/mod.rs`**. Items are private to their parent by default; **`pub`** exposes them to parents and (for **`pub(crate)`**) the current crate.

Next: Part II can deepen **lifetimes**, **traits**, **iterators**, and **error handling** patterns (`thiserror`, `anyhow` tradeoffs) on real crate boundaries.

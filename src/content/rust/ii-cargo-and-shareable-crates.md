---
label: "II"
subtitle: "Cargo & shareable crates"
group: "Rust"
groupOrder: 1
order: 2
---
Rust — Part II: Cargo & shareable crates
**Cargo** is Rust’s **package manager and build tool**. It downloads dependencies, compiles your code, runs tests, and publishes **crates** (Rust packages) others can reuse.

See **Part I** (`i-basics-and-toolchain.md`) for **`rustup`**, **`rustc`**, and Windows **MSVC** linker setup.

## 1. What Cargo is

| Tool | Role |
|------|------|
| **`rustup`** | Installs Rust versions and targets |
| **`rustc`** | Compiles `.rs` files to binaries or libraries |
| **`cargo`** | Project workflow: deps, build, test, run, publish |

You almost never invoke **`rustc`** by hand on a real project — **`cargo`** passes the right flags and links dependencies.

Every Cargo project has a **`Cargo.toml`** manifest at the root (and optionally more in a **workspace**).

```toml
[package]
name = "greeting"
version = "0.1.0"
edition = "2024"
rust-version = "1.85"

[dependencies]
serde = { version = "1", features = ["derive"] }
```

| Section | Purpose |
|---------|---------|
| **`[package]`** | Name, version, edition, license, description |
| **`[dependencies]`** | Other crates from **crates.io**, **git**, or **path** |
| **`[dev-dependencies]`** | Only for tests / examples / benches |
| **`[[bin]]`** | Extra binaries (optional; default is `src/main.rs`) |

## 2. Crate kinds

A **crate** is one compilation unit — either:

- **Binary crate** — produces an executable; needs **`fn main()`** in `src/main.rs` (or a declared `[[bin]]`).
- **Library crate** — produces **`rlib`** others link against; root is **`src/lib.rs`**; **no** `main`.

**Shareable** code almost always lives in a **library crate** (or several libs in one repo via a **workspace**).

```text
cargo new my_app --bin      # executable
cargo new my_utils --lib    # shareable library
```

## 3. Everyday Cargo commands

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

## 4. Example: build your own shareable library

### Step 1 — create the library crate

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

**`src/lib.rs`** — only **`pub`** items are part of the public API:

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

Verify:

```text
cargo test
```

### Step 2 — use it from another project (local path)

Create a binary that depends on your library **on disk** (no publish yet):

```text
cd ..
cargo new hello_app --bin
```

**`hello_app/Cargo.toml`** — **path dependency**:

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

**`path = "../greeter_utils"`** is ideal for monorepos and learning; Cargo compiles the library as part of the dependency graph.

### Step 3 — workspace (multiple crates, one repo)

For several shareable crates plus apps in **one** repository, use a **workspace**:

**Root `Cargo.toml`:**

```toml
[workspace]
resolver = "2"
members = [
    "greeter_utils",
    "hello_app",
]
```

Each member keeps its own **`Cargo.toml`**. In **`hello_app/Cargo.toml`**, path becomes:

```toml
greeter_utils = { path = "../greeter_utils" }
```

From the workspace root:

```text
cargo test --workspace
cargo run -p hello_app
```

## 5. Modules inside a library crate

Split implementation across files; the crate root **`lib.rs`** declares modules:

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

Consumers see **`greeter_utils::greet`** and **`greeter_utils::formal_greet`**; **`formal`** stays private unless you **`pub mod formal`**.

## 6. Sharing beyond your machine

| Method | `Cargo.toml` snippet | When |
|--------|----------------------|------|
| **Path** | `foo = { path = "../foo" }` | Same repo / local dev |
| **Git** | `foo = { git = "https://github.com/you/foo", branch = "main" }` | Private or unreleased code |
| **crates.io** | `foo = "0.2"` or `foo = { version = "0.2", features = ["serde"] }` | Published releases |

### Publish to crates.io (outline)

1. Create an account at [https://crates.io](https://crates.io) and run **`cargo login`** with an API token.
2. Fill **`description`**, **`license`**, **`repository`** in **`Cargo.toml`**.
3. **`cargo publish --dry-run`** then **`cargo publish`** from the library crate directory.
4. Bump **`version`** for every new release (semver: breaking → major, features → minor, fixes → patch).

Others then add:

```toml
greeter_utils = "0.1.0"
```

## 7. Features (optional API surface)

Enable compile-time options for dependents:

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

Dependents opt in: **`greeter_utils = { version = "0.1", features = ["extra"] }`**.

## 8. What to put in a shareable crate

- **`pub`** only what callers need; keep helpers private.
- **Document** public items with **`///`** — shows up in **`cargo doc`**.
- **Tests** in the same file (`#[cfg(test)]`) or **`tests/*.rs`** integration tests.
- **Examples** in **`examples/*.rs`** — run with **`cargo run --example demo`**.
- **README** and **LICENSE** before publishing.

## 9. Quick troubleshooting

| Problem | Check |
|---------|--------|
| `linker not found` (Windows) | Part I — MSVC Build Tools |
| `failed to resolve` dependency | Crate name spelling; network; git URL / path |
| `private` type in public API | Mark types **`pub`** or hide them behind **`pub fn`** |
| Two versions of same crate | **`cargo tree`** — unify versions in workspace |

## 10. Related

- **Part I** — ownership, **`match`**, basics (`i-basics-and-toolchain.md`)
- **Part III** — hands-on practice with **Rustlings** (`iii-learn-with-rustlings.md`)
- **Part IV** — **`async`/`await`**, runtimes, common pitfalls (`iv-async.md`)
- [The Cargo Book](https://doc.rust-lang.org/cargo/) — official reference for manifests, workspaces, publishing

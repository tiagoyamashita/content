---
label: "IV"
subtitle: "Async Rust"
group: "Rust"
groupOrder: 1
order: 4
---
Rust — Part IV: Async Rust
How **`async`/`await`** works, what **`Future`**s and a **runtime** do, which **problems** show up in real code, and **practical fixes**. Assumes **Part I** (ownership, **`trait`**) and basic **`cargo`** (**Part II**).

## 1. What “async” means in Rust

**Goal:** run **many I/O-bound tasks** (network, disk, timers) on **few OS threads** without blocking each thread while waiting.

| Model | Good for | Rust piece |
|-------|----------|------------|
| **OS threads** | CPU-heavy parallel work | **`std::thread`**, **`rayon`** |
| **Async tasks** | Lots of concurrent waits on I/O | **`async fn`**, **`Future`**, **runtime** |

Rust does **not** ship a full async runtime in **`std`** — only the **`Future`** trait and **`async`/`await`** syntax. You pick a runtime (**[Tokio](https://tokio.rs/)**, **[async-std](https://async.rs/)**, **smol**, …). **Tokio** is the default choice for servers and most learning material.

### Sync vs async (mental picture)

```text
Sync server (thread per request):
  Thread 1 ████████░░░░░░░░  (blocked waiting on DB)
  Thread 2 ████████░░░░░░░░  (blocked waiting on HTTP)
  … hundreds of threads …

Async server (few threads, many tasks):
  Thread 1 ██ task A ██ task B ██ task C ██  (only runs when work is ready)
  Thread 2 ██ task D ██ task E ██
```

**Async does not make CPU work faster** — it helps when threads would otherwise **sleep** waiting on I/O.

## 2. Core pieces

### `async fn` and `Future`

An **`async fn`** returns something that implements **`Future<Output = T>`** — work that **is not finished yet**. Calling **`async_fn()`** does **not** run the body; it **constructs** a future.

**`await`** suspends the current async function until another future completes, **without** blocking the executor thread (if you await the right things).

```rust
async fn fetch_label() -> String {
    // body becomes a state machine; each `.await` is a possible pause point
    String::from("ok")
}

async fn run() {
    let label = fetch_label().await;
    println!("{label}");
}
```

### Executor and runtime

Something must **poll** futures until they return **`Poll::Ready`**. A **runtime** (e.g. **Tokio**) provides:

- A **scheduler** (run tasks on a thread pool)
- **I/O driver** (epoll/kqueue/IOCP) so socket/timer waits wake tasks
- **Timers**, **TCP/UDP**, **channels**, **`spawn`**, etc.

```text
your async fn  →  Future  →  runtime polls it  →  .await points register wakers
```

### Minimal Tokio program

**`Cargo.toml`:**

```toml
[package]
name = "async_demo"
version = "0.1.0"
edition = "2021"

[dependencies]
tokio = { version = "1", features = ["full"] }
```

**`src/main.rs`:**

```rust
#[tokio::main]
async fn main() {
    let h = tokio::spawn(async {
        tokio::time::sleep(std::time::Duration::from_millis(100)).await;
        42
    });
    let n = h.await.expect("task panicked");
    println!("{n}");
}
```

**`#[tokio::main]`** expands to: build runtime → **`block_on`** your async **`main`**.

## 3. Running concurrent async work

| API | Use |
|-----|-----|
| **`tokio::spawn`** | Fire-and-forget or parallel branch (needs **`'static`** or owned data) |
| **`tokio::join!(a(), b())`** | Wait for **all**; fail fast if one fails (with `?` in async fn) |
| **`tokio::select!`** | Wait for **first** ready branch; cancel others |
| **`FuturesUnordered`** / streams | Many homogeneous tasks with limits |

```rust
use tokio::time::{sleep, Duration};

async fn one() -> u32 {
    sleep(Duration::from_millis(50)).await;
    1
}

async fn two() -> u32 {
    sleep(Duration::from_millis(10)).await;
    2
}

async fn both() -> (u32, u32) {
    tokio::join!(one(), two())
}
```

## 4. Problems that arise (and how to solve them)

### 4.1 Blocking the executor (“async is slow”)

**Problem:** **`std::thread::sleep`**, heavy CPU loops, or **sync** file/DB APIs inside **`async fn`** **block the runtime thread**. Every other task on that thread stalls.

**Symptoms:** latency spikes, low CPU but poor throughput, “async made it worse”.

**Fixes:**

- Use **async** APIs: **`tokio::time::sleep`**, **`tokio::fs`**, **`reqwest`**, **`sqlx`**, **`hyper`**, etc.
- Offload **blocking** work: **`tokio::task::spawn_blocking(|| { ... })`**.
- Offload **CPU** work: dedicated thread pool (**`rayon`**, **`spawn_blocking`**).

```rust
// Bad in async context
async fn bad() {
    std::thread::sleep(std::time::Duration::from_secs(1));
}

// Better
async fn better() {
    tokio::time::sleep(std::time::Duration::from_secs(1)).await;
}

// Sync library you cannot replace
async fn offload() -> Result<String, std::io::Error> {
    tokio::task::spawn_blocking(|| std::fs::read_to_string("data.txt"))
        .await
        .expect("join failed")
}
```

### 4.2 Holding locks across `.await`

**Problem:** **`mutex.lock().await`** does not exist on **`std::sync::Mutex`**. If you lock **`std::sync::Mutex`** and then **`.await`**, you hold the lock while suspended → **deadlocks** and long critical sections.

**Fixes:**

- Keep **lock scope** tiny: compute what you need, **drop** the guard, **then** `.await`.
- Prefer **`tokio::sync::Mutex`** / **`RwLock`** for data shared **only** in async tasks (async-aware, slower for sync-only code).
- Pass **owned data** out of the lock before awaiting.

```rust
// Risky pattern
async fn risky(flag: std::sync::Arc<std::sync::Mutex<bool>>) {
    let guard = flag.lock().unwrap();
    some_async_io().await; // still holding std mutex → bad
    let _ = *guard;
}

// Safer: no await while holding std::sync::Mutex
async fn safer(flag: std::sync::Arc<std::sync::Mutex<bool>>) {
    let should_run = {
        let g = flag.lock().unwrap();
        *g
    };
    if should_run {
        some_async_io().await;
    }
}
```

### 4.3 `Send` and `Sync` across `.await`

**Problem:** The compiler requires types held **across** an **`.await`** to be **`Send`** so the future can move to another thread. Non-**`Send`** types (**`Rc`**, raw pointers, some GUI handles) cause errors like *“future cannot be sent between threads safely”*.

**Fixes:**

- Use **`Arc`** instead of **`Rc`** for shared ownership in multi-threaded runtimes.
- Don’t hold **`RefCell`** / **`Rc`** guards across **`.await`**.
- **`tokio::spawn`** requires **`Send + 'static`** — clone **`Arc`** data into the task.

```rust
use std::sync::Arc;

async fn worker(data: Arc<Vec<u8>>) {
    tokio::spawn(async move {
        // `data` is Arc — Send
        let _len = data.len();
    })
    .await
    .unwrap();
}
```

### 4.4 No runtime / calling async from sync code

**Problem:** **`my_async_fn().await`** only works inside **`async`** context. From sync **`main`** or a callback you get *“await is only allowed inside `async` functions”*.

**Fixes:**

- **`#[tokio::main]`** or **`Runtime::block_on`** for the top level.
- Libraries expose **`block_on`** only at the edge — avoid nesting runtimes.

```rust
fn sync_entry() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        run_server().await;
    });
}
```

### 4.5 Cancellation and dropped futures

**Problem:** When a future is **dropped** (timeout, **`select!`**, client disconnect), execution stops at the next **`.await`**. Partial work may leave resources inconsistent unless you handle shutdown.

**Fixes:**

- Use **`tokio::select!`** with **`biased`** / explicit shutdown branches.
- **`tokio::time::timeout`** around operations.
- **`Drop`** guards, **`defer`** patterns, or **`scopeguard`** for cleanup.
- Design **idempotent** handlers; use **transactions** in DB layers.

```rust
async fn with_timeout() -> Result<String, tokio::time::error::Elapsed> {
    tokio::time::timeout(
        std::time::Duration::from_secs(5),
        slow_request(),
    )
    .await
}
```

### 4.6 Unbounded concurrency (memory / overload)

**Problem:** **`for item in items { tokio::spawn(...) }`** on millions of items exhausts RAM and file descriptors.

**Fixes:**

- **`Semaphore`** to cap in-flight work.
- **`buffer_unordered(n)`** / **`FuturesUnordered`** with a limit.
- **Channels** with fixed worker pool (producer/consumer).

```rust
use tokio::sync::Semaphore;
use std::sync::Arc;

async fn bounded_work(urls: Vec<String>) {
    let sem = Arc::new(Semaphore::new(32));
    let mut handles = vec![];

    for url in urls {
        let permit = sem.clone().acquire_owned().await.unwrap();
        handles.push(tokio::spawn(async move {
            let _p = permit;
            fetch(&url).await;
        }));
    }
    for h in handles {
        let _ = h.await;
    }
}

async fn fetch(url: &str) {
    let _ = url;
}
```

### 4.7 Pinning and self-referential futures

**Problem:** Some futures (and **`async fn`** in traits before Rust 1.75) need to be **pinned** because they hold pointers into their own stack frame. Errors mention **`Unpin`** or **`Pin`**.

**Fixes:**

- Prefer **`async fn` in traits** on modern Rust where supported, or use **`Pin<Box<dyn Future + Send>>`**.
- Use **`pin_project`** / **`pin-project-lite`** when writing manual futures.
- Let **`async fn`** and Tokio macros handle pinning; avoid **`mem::swap`** on pinned values.

Most application code never writes custom **`Future`**s — if you hit **`Pin`**, read the error and the trait’s docs before fighting the type system.

### 4.8 “async trait” and dynamic dispatch

**Problem:** **`dyn SomeAsyncTrait`** was awkward; async methods in traits had extra boilerplate.

**Fixes:**

- **Rust 1.75+**: **`async fn`** in traits (with **`use`** desugaring) for many cases.
- **`async-trait`** crate (macro) for older codebases.
- **`Pin<Box<dyn Future<Output = ...> + Send>>`** for trait objects when needed.

### 4.9 Mixing runtimes or nested `block_on`

**Problem:** Two runtimes in one process, or **`block_on`** inside an async task → deadlocks or panics.

**Fixes:**

- **One runtime per process** at the root.
- Never **`block_on`** inside async code on the **same** runtime; use **`.await`**.
- If a sync library must call async, isolate with a **dedicated thread** + channel.

### 4.10 Error handling in async code

**Problem:** **`?`** in **`async fn`** returns **`Result`** from the **future**, not from a thread — easy to confuse with **`spawn`** (errors inside spawned tasks are lost unless you **`await`** the **`JoinHandle`**).

**Fixes:**

- **`await`** join handles and propagate **`Result`**.
- **`tokio::try_join!`** for short-circuiting multiple **`Result`** futures.
- Log panics in tasks; consider **`tracing`** + **`Instrument`** for spans.

```rust
async fn fallible() -> Result<(), std::io::Error> {
    tokio::fs::read("missing.txt").await?;
    Ok(())
}
```

## 5. Shared state patterns

| Pattern | When |
|---------|------|
| **`Arc<T>`** + immutable data | Read-mostly config |
| **`Arc<tokio::sync::Mutex<T>>`** | Mutable shared state in async tasks |
| **`tokio::sync::mpsc`** | Message passing between tasks |
| **`tokio::sync::broadcast`** | Many subscribers (events) |
| **Channels + worker pool** | Backpressure-friendly pipelines |

Avoid **`Arc<Mutex<T>>`** with **`std::sync::Mutex`** unless lock duration is **tiny** and never spans **`.await`**.

## 6. Observability

Without tracing, async bugs look random.

```toml
tracing = "0.1"
tracing-subscriber = { version = "0.3", features = ["env-filter"] }
```

```rust
#[tracing::instrument]
async fn handle_request(id: u64) {
    tracing::info!(%id, "started");
    // ...
}
```

Run with **`RUST_LOG=info`** (or your filter). Pair with **Tokio console** (`tokio-console`) when you need task-level introspection.

## 7. When **not** to use async

- **CLI tool** that does one thing and exits → sync is simpler.
- **CPU-bound batch job** → threads / **`rayon`**, not async.
- **Small script** with no concurrent I/O → sync **`std::fs`** and **`reqwest::blocking`** (if you must) are fine.
- Team has no runtime expertise → fewer moving parts with sync + a thread pool.

Use async when you have **many concurrent I/O waits** and want **one binary** that scales on a few cores.

## 8. Learning path

1. **Part I** — ownership, **`Send`**, borrows (explains half the compiler errors).
2. **[Async Book](https://rust-lang.github.io/async-book/)** — official mental model.
3. **[Tokio tutorial](https://tokio.rs/tokio/tutorial)** — practical TCP, timers, channels.
4. Build: tiny HTTP server → add **`Semaphore`** → add **`tracing`** → break it with **`thread::sleep`** and fix.

## 9. Quick troubleshooting

| Error / symptom | Likely cause | Fix |
|-----------------|--------------|-----|
| `await` only in `async` | Called from sync code | `#[tokio::main]` / `block_on` at edge |
| future not `Send` | `Rc`, lock guard across await | `Arc`, shrink lock scope |
| everything hangs | Blocking in async | `spawn_blocking`, async I/O |
| spawn requires `'static` | Borrowed stack data in task | `Arc`, `move`, owned clones |
| deadlock | `std::Mutex` + await | Don’t await while holding lock |
| OOM under load | Unbounded `spawn` | `Semaphore`, bounded channels |

## 10. Related

- **Part I** — organization, ownership (`i-basics-and-toolchain.md`)
- **Part II** — `Cargo.toml`, dependencies (`ii-cargo-and-shareable-crates.md`)
- [Asynchronous Programming in Rust](https://rust-lang.github.io/async-book/)
- [Tokio](https://tokio.rs/) — runtime, tutorials, docs

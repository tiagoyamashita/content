---
label: "IV"
subtitle: "非同期Rust"
group: "さび"
groupOrder: 1
order: 4
---
Rust — パート IV: 非同期 Rust

**`async`/`await`** がどのように動作するか、**`Future`** と **ランタイム** が行うこと、実際のコードで現れる**問題**、および **実践的な修正**。 **パート I** (所有権、**`trait`**) および基本的な **`cargo`** (**パート II**) を想定します。

## 1. Rustにおける「非同期」の意味

**目標:** 待機中に各スレッドをブロックすることなく、**少数の OS スレッド** で **多くの I/O バウンド タスク** (ネットワーク、ディスク、タイマー) を実行します。

|モデル |良いこと |錆びた部分
|----------|----------|---------------|
| **OS スレッド** | CPU を大量に使用する並列作業 | **`std::thread`**、**`rayon`** |
| **非同期タスク** | I/O での大量の同時待機 | **`async fn`**、**`Future`**、**実行時間** |

Rust は **`std`** で完全な非同期ランタイムを**提供していません**。**`Future`** トレイトと **`async`/`await`** 構文のみです。ランタイム (**[Tokio](162)**、**[async-std](163)**、**smol**、…) を選択します。 **Tokio** は、サーバーとほとんどの学習教材のデフォルトの選択です。

### 同期と非同期 (心の中のイメージ)

```text
Sync server (thread per request):
  Thread 1 ████████░░░░░░░░  (blocked waiting on DB)
  Thread 2 ████████░░░░░░░░  (blocked waiting on HTTP)
  … hundreds of threads …

Async server (few threads, many tasks):
  Thread 1 ██ task A ██ task B ██ task C ██  (only runs when work is ready)
  Thread 2 ██ task D ██ task E ██
```

**非同期によって CPU の動作が高速化されるわけではありません**。そうでなければスレッドが I/O を待って **スリープ**する場合に役立ちます。

## 2. コアピース

### `async fn`および`Future`

**`async fn`** は **`Future<Output = T>`** を実装するもの、つまり **まだ完了していない作業**を返します。 **`async_fn()`** を呼び出しても本体は**実行されません**。それは**未来を構築**します。

**`await`** は、別のフューチャーが完了するまで現在の非同期関数を一時停止します。** 実行スレッドをブロックすることはありません** (適切な処理を待っている場合)。

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

### エグゼキュータとランタイム

**`Poll::Ready`** が返されるまで、何かが先物を**ポーリング**する必要があります。 **ランタイム** (例: **Tokio**) は以下を提供します:

- **スケジューラー** (スレッド プールでタスクを実行)
- **I/O ドライバー** (epoll/kqueue/IOCP) により、ソケット/タイマーはウェイク タスクを待機します
- **タイマー**、**TCP/UDP**、**チャネル**、**`spawn`**など。

```text
your async fn  →  Future  →  runtime polls it  →  .await points register wakers
```

### ミニマルトキオプログラム

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

**`#[tokio::main]`** は、ビルド ランタイム → **`block_on`** 非同期 **`main`** に展開されます。

## 3. 同時非同期作業の実行

| API |使用 |
|-----|-----|
| **`tokio::spawn`** |ファイアアンドフォーゲットまたはパラレルブランチ (**`'static`** または所有データが必要) |
| **`tokio::join!(a(), b())`** | **すべて**を待ちます。 1 つが失敗した場合はフェイルファスト (非同期 fn の `?` を使用) |
| **`tokio::select!`** | **最初**の準備完了ブランチを待ちます。他をキャンセルする |
| **`FuturesUnordered`** / ストリーム |制限のある同種のタスクが多数ある |

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

## 4. 発生する問題 (およびその解決方法)

### 4.1 エグゼキューターのブロック (「非同期は遅い」)

**問題:** **`std::thread::sleep`**、重い CPU ループ、または **`async fn`** 内の **同期** ファイル/DB API がランタイム スレッドをブロックします**。そのスレッド上の他のタスクはすべて停止します。

**症状:** 遅延のスパイク、CPU は低いがスループットが低い、「非同期により状況が悪化」。

**修正:**

- **非同期** API を使用します: **`tokio::time::sleep`**、**`tokio::fs`**、**`reqwest`**、**`sqlx`**、**`hyper`** など。
- **ブロッキング**作業のオフロード: **`tokio::task::spawn_blocking(|| { ... })`**。
- **CPU** 作業のオフロード: 専用スレッド プール (**`rayon`**、**`spawn_blocking`**)。

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

### 4.2 `.await` 全体でロックを保持する

**問題:** **`mutex.lock().await`** は **`std::sync::Mutex`** に存在しません。 **`std::sync::Mutex`** をロックしてから **`.await`** をロックすると、サスペンド中にロックが保持されることになり、**デッドロック**と長いクリティカル セクションが発生します。

**修正:**

- **ロックスコープ**を小さく保ちます: 必要なものを計算し、ガードを**ドロップ**してから** `.await`。
- 非同期タスクで **のみ**共有されるデータには **`tokio::sync::Mutex`** / **`RwLock`** を優先します (非同期対応、同期専用コードの場合は遅くなります)。
- 待機する前に、**所有データ**をロックから渡します。

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

### 4.3 `Send` および `Sync` と `.await`

**問題:** コンパイラは、将来別のスレッドに移動できるように、**`.await`** の **`.await`** に保持される型を **`Send`** にする必要があります。 **`Send`** 以外の型 (**`Rc`**、生のポインタ、一部の GUI ハンドル) は、*「将来はスレッド間で安全に送信できません」* のようなエラーを引き起こします。

**修正:**

- マルチスレッド ランタイムでの共有所有権には、**`Rc`** ではなく **`Arc`** を使用します。
- **`RefCell`** / **`Rc`** ガードを **`.await`** にわたって保持しないでください。
- **`tokio::spawn`** には **`Send + 'static`** が必要です — **`Arc`** データのクローンをタスクに作成します。

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

### 4.4 ランタイムなし / 同期コードからの非同期呼び出し

**問題:** **`my_async_fn().await`** は **`async`** コンテキスト内でのみ機能します。同期 **`main`** またはコールバックから、*「await は `async` 関数内でのみ許可されます」* を取得します。

**修正:**

- 最上位レベルの場合は **`#[tokio::main]`** または **`Runtime::block_on`**。
- ライブラリは **`block_on`** をエッジでのみ公開します。ランタイムのネストを避けます。

```rust
fn sync_entry() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        run_server().await;
    });
}
```

### 4.5 先物のキャンセルとドロップ

**問題:** Future が **ドロップ**されると (タイムアウト、**`select!`**、クライアントの切断)、実行は次の **`.await`** で停止します。部分的な作業では、シャットダウンを処理しない限り、リソースに不整合が残る可能性があります。

**修正:**

- **`tokio::select!`** を **`biased`** / 明示的なシャットダウン ブランチとともに使用します。
- **`tokio::time::timeout`** 運営に関すること。
- **`Drop`** ガード、**`defer`** パターン、またはクリーンナップ用 **`scopeguard`**。
- **冪等**ハンドラーを設計します。 DB レイヤーで **トランザクション** を使用します。

```rust
async fn with_timeout() -> Result<String, tokio::time::error::Elapsed> {
    tokio::time::timeout(
        std::time::Duration::from_secs(5),
        slow_request(),
    )
    .await
}
```

### 4.6 無制限の同時実行性 (メモリ / 過負荷)

**問題:** 数百万のアイテムで **`for item in items { tokio::spawn(...) }`** すると、RAM とファイル記述子が使い果たされます。

**修正:**

- **`Semaphore`** で飛行中の作業を制限します。
- **`buffer_unordered(n)`** / **`FuturesUnordered`** 制限あり。
- 固定ワーカー プール (プロデューサー/コンシューマー) を備えた **チャネル**。

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

### 4.7 ピン留めと自己参照先物

**問題:** 一部の Future (および Rust 1.75 より前のトレイトの **`async fn`**) は、ポインタを独自のスタック フレームに保持するため、**固定**する必要があります。エラーには **`Unpin`** または **`Pin`** が記載されています。

**修正:**

- サポートされている場合は、最新の Rust の特性**で **`async fn` を優先するか、**`Pin<Box<dyn Future + Send>>`** を使用してください。
- 手動先物を書くときは **`pin_project`** / **`pin-project-lite`** を使用します。
- **`async fn`** マクロと Tokio マクロに固定を処理させます。固定された値では **`mem::swap`** を避けてください。

ほとんどのアプリケーション コードはカスタム **`Future`** を書き込むことはありません。**`Pin`** に到達した場合は、型システムと戦う前にエラーとトレイトのドキュメントを読んでください。

### 4.8 「非同期特性」と動的ディスパッチ

**問題:** **`dyn SomeAsyncTrait`** はぎこちなかった。特性の async メソッドには余分な定型文がありました。

**修正:**

- **Rust 1.75+**: 多くの場合、特性に **`async fn`** (**`use`** 脱糖あり)。
- **`async-trait`** 古いコードベース用のクレート (マクロ)。
- 必要に応じて特性オブジェクトの **`Pin<Box<dyn Future<Output = ...> + Send>>`**。

### 4.9 ランタイムの混合またはネストされた `block_on`

**問題:** 1 つのプロセス内に 2 つのランタイムがある、または非同期タスク内で **`block_on`** → デッドロックまたはパニックが発生します。

**修正:**

- **ルートにプロセスごとに 1 つのランタイム**。
- **同じ**ランタイム上の非同期コード内では決して**`block_on`**しないでください。 **`.await`** を使用してください。
- 同期ライブラリが async を呼び出す必要がある場合は、**専用スレッド** + チャネルを使用して分離します。

### 4.10 非同期コードでのエラー処理

**問題:** **`async fn`** の **`?`** は、スレッドからではなく **将来**から **`Result`** を返します。**`spawn`** と混同しやすいです (**`await`** を **`JoinHandle`** にしない限り、生成されたタスク内のエラーは失われます)。

**修正:**

- **`await`** ハンドルを結合し、**`Result`** を伝播します。
- **`tokio::try_join!`** 複数の **`Result`** 先物をショートする場合。
- タスクにパニックを記録します。スパンには **`tracing`** + **`Instrument`** を考慮してください。

```rust
async fn fallible() -> Result<(), std::io::Error> {
    tokio::fs::read("missing.txt").await?;
    Ok(())
}
```

## 5. 共有状態パターン

|パターン |いつ |
|-------|------|
| **`Arc<T>`** + 不変データ |ほとんど読み取り専用の構成 |
| **`Arc<tokio::sync::Mutex<T>>`** |非同期タスクにおける変更可能な共有状態 |
| **`tokio::sync::mpsc`** |タスク間でのメッセージの受け渡し |
| **`tokio::sync::broadcast`** |多くの購読者 (イベント) |
| **チャネル + ワーカー プール** |バックプレッシャーに優しいパイプライン |

ロック期間が **わずか**で **`.await`** にまたがらない場合を除き、**`Arc<Mutex<T>>`** と **`std::sync::Mutex`** は避けてください。

## 6. 可観測性

トレースしないと、非同期バグはランダムに見えます。

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

**`RUST_LOG=info`** (またはフィルター) を使用して実行します。タスクレベルのイントロスペクションが必要な場合は、**Tokio コンソール** (`tokio-console`) と組み合わせてください。

## 7. 非同期を使用しない**場合

- **CLI ツール** は 1 つのことを実行して終了するため、同期がより簡単になります。
- **CPU バウンドのバッチ ジョブ** → スレッド / **`rayon`**、非同期。
- **同時 I/O のない小さなスクリプト** → **`std::fs`** と **142​​** (必要な場合) の同期は問題ありません。
- チームにランタイムの専門知識がない → 同期 + スレッド プールにより可動部分が少なくなります。

**多数の同時 I/O 待機**があり、いくつかのコアで拡張できる **1 つのバイナリ**が必要な場合は、async を使用します。

## 8. 学習パス

1. **パート I** — 所有権、**`Send`**、借用 (コンパイラ エラーの半分を説明)。
2. **[非同期ブック](164)** — 公式メンタルモデル。
3. **[Tokio チュートリアル](165)** — 実用的な TCP、タイマー、チャネル。
4. 構築: 小さな HTTP サーバー → **`Semaphore`** を追加 → **`tracing`** を追加 → **`thread::sleep`** で壊して修正します。

## 9. 迅速なトラブルシューティング

|エラー/症状 |考えられる原因 |修正 |
|-----------------|--------------|-----|
| `await`は`async`のみ |同期コードから呼び出されます | `#[tokio::main]` / `block_on` エッジ |
|未来ではない `Send` | `Rc`、待機中のロックガード | `Arc`、シュリンク ロック スコープ |
|すべてがハングします |非同期でのブロック | `spawn_blocking`、非同期 I/O |
|スポーンには `'static` が必要です |タスク内のスタック データを借用 | `Arc`、`move`、所有クローン |
|デッドロック | `std::Mutex` + 待つ |ロックを押したまま待機しないでください |
|負荷がかかっている OOM |無制限 `spawn` | `Semaphore`、境界付きチャネル |

## 10. 関連

- **パート I** — 組織、所有権 [基本とツールチェーン](i-basics-and-toolchain.md)
- **パート II** — `Cargo.toml`、依存関係 [貨物および共有可能なクレート](ii-cargo-and-shareable-crates.md)
- [Rustでの非同期プログラミング](166)
- [Tokio](167) — ランタイム、チュートリアル、ドキュメント

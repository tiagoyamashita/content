---
label: "IV"
subtitle: "非同期 Rust"
group: "Rust"
groupOrder: 1
order: 4
---
Rust — パート IV: 非同期 Rust

どうやって **`async`/`await`** 機能します、何が **`Future`**s と **ランタイム** が実行し、**問題**が実際のコードに現れ、**実践的な修正**が行われます。 **パート I** (所有権、**) を引き受けます`trait`**) および基本的な **`cargo`** (**パート II**)。

## 1. Rust における「非同期」の意味

**目標:** 待機中に各スレッドをブロックすることなく、**少数の OS スレッド** で **多くの I/O- バインドされたタスク** (ネットワーク、ディスク、タイマー) を実行します。

|モデル |良いこと | Rust 個 |
|----------|----------|---------------|
| **OS スレッド** | CPU - 大量の並行作業 | **`std::thread`**、**`rayon`** |
| **非同期タスク** | I/O で大量の同時待機が発生しています | **`async fn`**、**`Future`**、**ランタイム** |

Rust は ** 完全な非同期ランタイムを ** 提供しません**`std`** — ** のみ`Future`** 特性と **`async`/`await`** 構文。ランタイムを選択します (**[Tokio]()https://tokio.rs/)**, **[非同期標準](https://async.rs/)**、**スモール**、…)。 **Tokio** は、サーバーとほとんどの学習教材のデフォルトの選択です。

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

**非同期は CPU の動作を高速化するものではありません**。そうでなければスレッドが I/O を待機して **スリープ**する場合に役立ちます。

## 2.コアピース

###`async fn`そして`Future`

**`async fn`** は ** を実装するものを返します`Future<Output = T>`** — **まだ終わっていない**作業。電話をかける **`async_fn()`** は本体を実行しません**。それは**未来を構築**します。

**`await`** 別のフューチャーが完了するまで現在の非同期関数を一時停止します。** 実行スレッドをブロックすることはありません** (適切な処理を待っている場合)。

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

** 返されるまで、何かが先物を**ポーリング**する必要があります**`Poll::Ready`**。 **ランタイム** (例: **Tokio**) は以下を提供します:

- **スケジューラー** (スレッド プールでタスクを実行)
- **I/O ドライバー** (epoll/kqueue/IOCP) なので、ソケット/タイマーはウェイク タスクを待機します
- **タイマー**、**TCP/UDP**、**チャネル**、**`spawn`**など

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

**`#[tokio::main]`** は次のように展開されます: ビルド ランタイム → **`block_on`** あなたの非同期 **`main`**。

## 3. 同時非同期作業の実行

| API |使用 |
|-----|-----|
| **`tokio::spawn`** |ファイアアンドフォーゲットまたはパラレルブランチ (** が必要)`'static`** または所有データ) |
| **`tokio::join!(a(), b())`** | **すべて**を待ちます。 1 つが失敗した場合はフェイルファスト (`?`非同期 fn) |
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

**問題：** **`std::thread::sleep`**、重い CPU ループ、または **sync** ファイル/DB API が ** 内にある`async fn`** **ランタイム スレッドをブロックします**。そのスレッド上の他のタスクはすべて停止します。

**症状:** レイテンシーのスパイク、CPU は低いがスループットの低下、「非同期によりさらに悪化」。

**修正:**

- **非同期** APIs を使用します: **`tokio::time::sleep`**、**`tokio::fs`**、**`reqwest`**、**`sqlx`**、**`hyper`**など
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

### 4.2 ロックを保持する`.await`

**問題：** **`mutex.lock().await`** は ** には存在しません`std::sync::Mutex`**。 **をロックすると`std::sync::Mutex`** その後 **`.await`**、サスペンド中にロックを保持している → **デッドロック**と長いクリティカルセクション。

**修正:**

- **ロックスコープ**を小さく保つ: 必要なものを計算し、ガードを**ドロップ**し、**その後**`.await`。
- 好む **`tokio::sync::Mutex`** / **`RwLock`** 非同期タスクで ** のみ** 共有されるデータの場合 (非同期対応、同期専用コードの場合は遅くなります)。
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

### 4.3`Send`そして`Sync`横切って`.await`

**問題:** コンパイラでは、** と ** にわたって保持される型が必要です`.await`**になる**`Send`** 将来は別のスレッドに移動できるようになります。非**`Send`** 種類 （**`Rc`**、生のポインター、一部の GUI ハンドル) は、*「将来はスレッド間で安全に送信できません」* のようなエラーを引き起こします。

**修正:**

- 使用 **`Arc`** の代わりに **`Rc`** マルチスレッド ランタイムでの共有所有権の場合。
- **を保持しないでください`RefCell`** / **`Rc`** 警備員が **`.await`**。
- **`tokio::spawn`** 必要 **`Send + 'static`** — クローン **`Arc`** データをタスクに追加します。

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

### 4.4 ランタイムなし / 同期コードからの非同期アップロード

**問題：** **`my_async_fn().await`** 内部でのみ動作します **`async`** コンテクスト。同期から **`main`** または取得したコールバック *「await は内部でのみ許可されます」`async`機能」*。

**修正:**

- **`#[tokio::main]`** または **`Runtime::block_on`** 最上位レベルの場合。
- 図書館は ** を公開します`block_on`** エッジのみ - ランタイムのネストを避けます。

```rust
fn sync_entry() {
    let rt = tokio::runtime::Runtime::new().unwrap();
    rt.block_on(async {
        run_server().await;
    });
}
```

### 4.5 先のキャンセルとドロップ

**問題:** Future が **ドロップされた**場合 (タイムアウト、**)`select!`**、クライアントが切断されました)、次の ** で実行が停止します`.await`**。部分的な作業では、シャットダウンを処理しない限り、リソースに不整合が残る可能性があります。

**修正:**

- 使用 **`tokio::select!`** と **`biased`** / 明示的なシャットダウン ブランチ。
- **`tokio::time::timeout`** 運用周り。
- **`Drop`** 警備員、**`defer`** パターン、または **`scopeguard`** クリーンアップ用。
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

**問題：** **`for item in items { tokio::spawn(...) }`** 数百万のアイテムでは、RAM とファイル記述子が使い果たされます。

**修正:**

- **`Semaphore`** 飛行中の作業を制限するため。
- **`buffer_unordered(n)`** / **`FuturesUnordered`**制限付き。
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

**問題:** いくつかの先物 (および **`async fn`** Rust 1.75 より前のトレイトでは、ポインタを独自のスタック フレームに保持するため、**固定する必要があります**。 ** に関するエラー`Unpin`** または **`Pin`**。

**修正:**

- 好む **`async fn`最新の Rust の特性** (サポートされている場合)、または ** を使用します`Pin<Box<dyn Future + Send>>`**。
- 使用 **`pin_project`** / **`pin-project-lite`** マニュアル先物を書く場合。
- させて **`async fn`** および Tokio マクロは固定を処理します。避ける **`mem::swap`** 固定された値について。

ほとんどのアプリケーション コードはカスタム ** を決して書きません`Future`**s — ** を押した場合`Pin`**、型システムと戦う前に、エラーとトレイトのドキュメントを読んでください。

### 4.8 「非同期特性」と動的ディスパッチ

**問題：** **`dyn SomeAsyncTrait`** ぎこちなかった。特性の async メソッドには余分な定型文がありました。

**修正:**

- **Rust 1.75+**: **`async fn`** 特性内 (** 付き)`use`** 脱糖) 多くの場合。
- **`async-trait`** 古いコードベース用のクレート (マクロ)。
- **`Pin<Box<dyn Future<Output = ...> + Send>>`** 必要に応じて特性オブジェクトに使用します。

### 4.9 ランタイムの混合またはネスト`block_on`

**問題:** 1 つのプロセスに 2 つのランタイムがある、または **`block_on`** 非同期タスク内 → デッドロックまたはパニック。

**修正:**

- **ルートにプロセスごとに 1 つのランタイム**。
- 一度もない **`block_on`**同じ**ランタイム上の非同期コード内。使用 **`.await`**。
- 同期ライブラリが async を呼び出す必要がある場合は、**専用スレッド** + チャネルを使用して分離します。

### 4.10 非同期コードでのエラー処理

**問題：** **`?`** で **`async fn`** を返します **`Result`** スレッドからではなく、**将来**から — ** と混同されやすい`spawn`** (生成されたタスク内のエラーは、** しない限り失われます)`await`** の **`JoinHandle`**)。

**修正:**

- **`await`** ハンドルを結合して伝播する **`Result`**。
- **`tokio::try_join!`** 複数短絡用 **`Result`** 先物。
- タスクにパニックを記録します。考慮する **`tracing`** + **`Instrument`** スパンの場合。

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

避ける **`Arc<Mutex<T>>`** と **`std::sync::Mutex`** ロック期間が **ごくわずか**で、決して長くならない場合を除きます **`.await`**。

## 6. 観察可能性

トレースしないと、非同期バグは偶然見られます。

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

** で実行`RUST_LOG=info`** (またはフィルター)。 **Tokio コンソール** とペアリングします (`tokio-console`) タスクレベルのイントロスペクションが必要な場合。

## 7. 非同期を使用しない**場合

- **CLI ツール** は 1 つのことを実行して終了します → 同期がより簡単になります。
- **CPU バインドされたバッチ ジョブ** → スレッド / **`rayon`**、非同期ではありません。
- **同時実行 I/O を持たない小さなスクリプト** → 同期 **`std::fs`** そして **`reqwest::blocking`** (必要な場合は) 大丈夫です。
- チームにランタイムの専門知識がない → 同期 + スレッド プールにより可動部分が少なくなります。

**多くの同時 I/O 待機**があり、いくつかのコアで拡張できる **1 つのバイナリ**が必要な場合は、async を使用します。

## 8. 学習パス

1. **パート I** — 所有権、**`Send`**、借用（コンパイラエラーの半分を説明）。
2. **[非同期ブック](https://rust-lang.github.io/async-book/)** — 公式メンタルモデル。
3. **[Tokio チュートリアル](https://tokio.rs/tokio/tutorial)** — 実用的な TCP、タイマー、チャネル。
4. 構築: 小さな HTTP サーバー → ** を追加`Semaphore`** → **を追加`tracing`** → **で壊す`thread::sleep`** そして修正します。

## 9. 迅速なトラブルシューティング

|エラー/症状 |考えられる原因 |修正 |
|-----------------|--------------|-----|
|`await`だけで`async`|同期コードから呼び出されます |`#[tokio::main]`/`block_on`端で |
|未来ではない`Send`|`Rc`、ロックガードを横切って待機 |`Arc`、シュリンク ロック スコープ |
|すべてがハングします |非同期でのブロック |`spawn_blocking`、非同期 I/O |
|スポーンには必要なもの`'static`|タスク内のスタック データを借用 |`Arc`、`move`、所有するクローン |
|デッドロック |`std::Mutex`+ 待つ |ロックを押したまま待機しないでください |
| OOM 負荷がかかっています |無制限`spawn`|`Semaphore`、境界付きチャネル |

## 10. 関連

- **パート I** — 組織、所有権 [基本とツールチェーン](i-basics-and-toolchain.md)
- **パート II** –`Cargo.toml`、依存関係 [貨物と共有可能なクレート](ii-cargo-and-shareable-crates.md)
- [Rust の非同期プログラミング](https://rust-lang.github.io/async-book/)
- [トキオ](https://tokio.rs/) — ランタイム、チュートリアル、ドキュメント

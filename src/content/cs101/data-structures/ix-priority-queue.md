---
label: "IX"
subtitle: "優先キュー"
group: "データ構造とアルゴリズム"
order: 9
---
優先キュー — 「次に誰が行く？」到着時間ではなく重要性によって

**プライオリティ キュー**は、各項目に**優先度** (多くの場合、単なる数値または**比較可能なもの**) を持つコレクションの**抽象データ型**です。動作の定義: **挿入**は任意の順序で行うことができますが、**抽出**は常に、内部に残っているアイテムの中で**最高**または**最低**の優先順位を持つアイテムを削除します。**最も古いアイテム(**FIFOキュー**)や**最新のもの(**スタック**)ではありません**。

**Java ベースライン:** `PriorityQueue` スニペットは **Java SE 22** (`javac --release 22`) を前提としています。これらは **`record`** および **Java 16** 以降で利用可能なその他の機能を使用します。これらは **JDK 21 LTS** でも実行されます。

**病院のトリアージ** デスクを思い浮かべると: 到着は厳密に先着順ではありません。 **最も緊急**なケースが優先されます。通常の**キュー**は、整然とした単一の行です。 **優先キュー** は、「現在最も重要な人に常にサービスを提供する」ものです。


## 1. キュー、スタック、優先キュー (1 分)

| ADT | 「ベストの削除」またはデキュー/ポップで去るのは誰ですか? |典型的なメンタルモデル |
|-----|----------------------------------------------|---------------------|
| **キュー** | **最も古い** がまだ待機中 (**FIFO**) |お店の行列 | 写真
| **スタック** | **最新**はまだあります (**LIFO**) |皿の山 | 写真 皿の山
| **優先キュー** | **最小** または **最大** キーがまだ存在します (順序付けルールによる) |トリアージ、CPU スケジューリング |

**Peek** (または **find-min** / **find-max**) は、同じ「最適な」要素を **削除せずに** 読み取ります。 **挿入** は、独自の優先順位を持つ何かを追加します。何かの「前」に置く必要は**ありません**。構造は内部的に不変条件を保持します。


## 2. 操作 (API が通常公開するもの)

名前は言語や教科書によって異なります。それらを次のように頭の中でマッピングします。

- **`insert(x)`** / **`add(x)`** / **`offer(x)`** — `x`をコレクションに追加します。
- **`extract-min()`** または **`extract-max()`** — キューの順序に従って最適な要素を削除して返します。 **空**構造では、動作は**エラー**または**センチネル**値のいずれかになります(Javaの`poll()`は空の場合**`null`**を返します)。
- **`peek-min()`** / **`peek-max()`** — 最適な要素を **削除せずに**返します (Java: **`peek()`**)。
- **`isEmpty()`**、**`size()`** — 通常の簿記。
- **`clear()`** — すべてを削除します。

**オプション (詳細):** **`decrease-key`** / **`increase-key`** 構造内の項目に対する **ハンドル**がすでにあり、その優先順位が変更される場合。優先順位を更新できる **バイナリ ヒープ**を使用した高速 **ダイクストラ**最短パスの実装に必要です。標準 **`java.util.PriorityQueue`** は、任意の要素に対する効率的な減少キーを**サポートしません**。そのためには、**インデックス付きヒープ** パターン、理論重視の設定で **フィボナッチ ヒープ**、または別のグラフ ライブラリを使用します。

**マージ** (2 つの優先キューを結合する) は、一部の理論上の API で使用されます。実際のコードは、多くの場合、あるヒープから別のヒープに挿入するだけです。


## 3. 最小ヒープと最大ヒープ (同じ考え方、順序を入れ替えたもの)

- **最小優先度キュー:** 「最良」 = **最小** キー。 **抽出** = **抽出分**。 **ダイクストラ** (最小の暫定距離が最初)、グラフの**プリム**、**ソートされたストリームを小さなヒープの「現在のヘッド」とマージ**するために使用されます。
- **最大優先キュー:** 「最良」 = **最大** キー。 「トップ **k**」スタイルの問題、**ヒープソート** 降順、**最大の 2 つ** を繰り返し取得する **ハフマン** スタイルの構造 (定式化に応じて) に使用されます。

実装に関して言えば、**最小ヒープ**は完全なバイナリ ツリーであり、各親はその子**≤**です。 **max-heap** は **≥** に切り替わります。 1 つの実装では、比較を交換するか、Java で **逆コンパレータ** を使用することで両方を行うことができます。


## 4. タイブレークと「優先順位の重複」

2 つの項目が **同じ**数値優先度を持つ場合、実装が等しいキー内で **FIFO の安定性**を文書化しない限り、ADT は多くの場合、どちらが最初に出力されるかを**保証しません (ヒープの多くは**安定していません**)。同等の順序が重要な場合は、次のような一般的な修正が行われます。

- **二次キー**をパックします(例: `(priority, sequenceNumber)`に辞書編集的な比較を使用して、古いエントリが同順位の中で最初にソートされます)、または
- **一意の ID** を保存し、**`Comparator`** で明示的に関係を解消します。


## 5. 実装と期限

素朴な考え:

- **ソートされていない配列またはリスト:** **insert** **O(1)** (追加) ですが、**extract-min** はすべてをスキャンします — **O(n)**。
- **ソートされた配列:** **extract-min** を一方の端から **O(1)** しますが、**insert** はシフトする可能性があります — 最悪の場合は **O(n)**。

一般的な変更可能な優先キューの通常のスイート スポットは **バイナリ ヒープ** (このサブメニュー [バイナリ ヒープ](viii-binary-heap.md) の **バイナリ ヒープ**を参照): **完全なバイナリ ツリー**を配列に格納し、各挿入 (**バブル アップ** / **スイム**) および各抽出 (**シンク ダウン** / **シフト**) 後に **ヒープ順序**を復元します。高さは **O(log n)** なので、次のようになります。

|操作 |バイナリ ヒープ (通常) |
|----------|--------------------------|
| **挿入** | **O(log n)** |
| **ピーク** ベスト | **O(1)** |
| **抜粋** ベスト | **O(log n)** |
| **n** キーから **ビルド** (ボトムアップ) | **O(n)** — **n** の個別の挿入よりも優れています |

**フィボナッチ ヒープ**とその仲間は、理論上、特殊なグラフ アルゴリズムの**償却**境界を改善します。日常のライブラリでは、依然として **バイナリ ヒープ**が最初に表示されます。

<figure class="notes-diagram"><svg xmlns="44 viewBox="0 0 420 212" role="img" aria-label="Min heap before extract min and after moving last leaf to root and sinking down">
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">extract-min restores heap in O(log n)</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">pop root (min), replace with last array element, compare with children and swap with smaller child until order holds</text>
  <text x="12" y="64" fill="#86efac" font-size="9" font-weight="600">min-heap before</text>
  <circle cx="100" cy="108" r="18" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="92" y="114" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <line x1="88" y1="120" x2="56" y2="148" stroke="#71717a" stroke-width="2"/>
  <line x1="112" y1="120" x2="144" y2="148" stroke="#71717a" stroke-width="2"/>
  <circle cx="56" cy="162" r="14" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="50" y="166" fill="#e4e4e7" font-size="10" font-family="ui-monospace">4</text>
  <circle cx="144" cy="162" r="14" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="138" y="166" fill="#e4e4e7" font-size="10" font-family="ui-monospace">6</text>
  <line x1="48" y1="168" x2="32" y2="188" stroke="#71717a" stroke-width="2"/>
  <circle cx="32" cy="196" r="11" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="26" y="199" fill="#e4e4e7" font-size="9" font-family="ui-monospace">9</text>
  <path d="M100 88 L100 76" stroke="#fbbf24" stroke-width="2"/>
  <text x="40" y="74" fill="#fbbf24" font-size="9" font-weight="600">return 2</text>
  <text x="220" y="64" fill="#60a5fa" font-size="9" font-weight="600">after sink-down</text>
  <circle cx="300" cy="108" r="18" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="292" y="114" fill="#e4e4e7" font-size="11" font-family="ui-monospace">4</text>
  <line x1="288" y1="120" x2="256" y2="148" stroke="#71717a" stroke-width="2"/>
  <line x1="312" y1="120" x2="344" y2="148" stroke="#71717a" stroke-width="2"/>
  <circle cx="256" cy="162" r="14" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="250" y="166" fill="#e4e4e7" font-size="10" font-family="ui-monospace">9</text>
  <circle cx="344" cy="162" r="14" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="338" y="166" fill="#e4e4e7" font-size="10" font-family="ui-monospace">6</text>
  <text x="220" y="188" fill="#71717a" font-size="9">root was 9 (last leaf); one swap with 4 yields valid min-heap</text>
</svg></figure>


<figure class="notes-diagram"><svg xmlns="45 viewBox="0 0 440 120" role="img" aria-label="FIFO queue front versus priority queue always smallest at root">
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">FIFO queue — order fixed by arrival</text>
  <rect x="12" y="36" width="40" height="26" rx="3" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <text x="24" y="52" fill="#e4e4e7" font-size="10" font-family="ui-monospace">1</text>
  <rect x="56" y="36" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="68" y="52" fill="#e4e4e7" font-size="10" font-family="ui-monospace">5</text>
  <rect x="100" y="36" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="112" y="52" fill="#e4e4e7" font-size="10" font-family="ui-monospace">3</text>
  <text x="12" y="78" fill="#71717a" font-size="9">dequeue always removes left (oldest), even if 3 is “smaller”</text>
  <text x="230" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Min priority queue — order by key</text>
  <circle cx="288" cy="48" r="16" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="282" y="52" fill="#e4e4e7" font-size="10" font-family="ui-monospace">1</text>
  <line x1="276" y1="58" x2="256" y2="78" stroke="#71717a" stroke-width="2"/>
  <line x1="300" y1="58" x2="320" y2="78" stroke="#71717a" stroke-width="2"/>
  <circle cx="256" cy="90" r="12" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="250" y="94" fill="#e4e4e7" font-size="9" font-family="ui-monospace">5</text>
  <circle cx="320" cy="90" r="12" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="314" y="94" fill="#e4e4e7" font-size="9" font-family="ui-monospace">3</text>
  <text x="230" y="112" fill="#71717a" font-size="9">extract-min always returns 1 while it remains — not insertion order</text>
</svg></figure>


## 6. Java `PriorityQueue`

**`java.util.PriorityQueue<E>`** は、要素が **自然順序付け** (`Comparable`) を使用する場合の **最小ヒープ**、または明示的な **`Comparator`** によって順序付けされたヒープです。 **スレッドセーフではありません**。イテレータの順序は**「優先順位」ではありません**。ループ内で **`poll()`** を使用して、並べ替えられた順序で排出します。

**整数の最小ヒープ** (最小の `poll` が最初):

```java
// Compile: javac --release 22 …
import java.util.PriorityQueue;

PriorityQueue<Integer> pq = new PriorityQueue<>();
pq.offer(30);
pq.offer(10);
pq.offer(20);
pq.peek();  // 10
pq.poll();  // 10
pq.poll();  // 20
```

**最大ヒープ** (最大が最初): 比較を逆にします。

```java
// Compile: javac --release 22 …
import java.util.Collections;
import java.util.PriorityQueue;

PriorityQueue<Integer> maxPq = new PriorityQueue<>(Collections.reverseOrder());
maxPq.offer(10);
maxPq.offer(30);
maxPq.peek();  // 30
```

**カスタム タイプ** (例: 締め切りのあるジョブ — **ここでは、小さい整数が優先されるため、**締め切りが早い = 優先度が高くなります**):

```java
// Compile: javac --release 22 …
import java.util.Objects;
import java.util.PriorityQueue;

record Job(String name, int deadline) implements Comparable<Job> {
  Job {
    Objects.requireNonNull(name, "name");
  }

  @Override
  public int compareTo(Job o) {
    return Integer.compare(deadline, o.deadline);
  }
}

PriorityQueue<Job> jobs = new PriorityQueue<>();
jobs.offer(new Job("backup", 5));
jobs.offer(new Job("patch", 2));
jobs.poll();  // patch — deadline 2 first
```

(代わりに、**`Comparable`** とともに `class` を使用するか、**`Comparator.comparingInt(Job::deadline)`** を **`PriorityQueue`** コンストラクターに渡すことができます。同じ順序です。)

**空でも安全:** **`poll()`** および **`peek()`** は空の場合 **`null`** を返します。 **`remove()`** は **`NoSuchElementException`** をスローします。

**注意事項**

- **`null`** 要素は**許可されません**。
- オブジェクトの挿入後**に順序付けに関与するフィールドを変更した場合、ヒープは**自動的に並べ替えられません。**削除して再挿入**するか、**decrease-key**用に設計された構造を使用する必要があります。
- 初期容量は**ヒント**のみです。ヒープは必要に応じて成長します。


## 7. 優先キューが表示される場所

- **グラフ アルゴリズム:** **ダイクストラ** (最も近い未訪問の頂点が最初)、**プリム** (成長するツリーへの最も安価なエッジ)、**A-スター** (`A*`) ヒューリスティックによる検索。
- **CPU / OS スケジューリング:** 優先順位に基づいて次に実行可能なプロセスを選択します (実際のスケジューラーは公平性、エージングなどを追加します)。
- **離散イベント シミュレーション:** 次のイベントは、**最小**のシミュレーション時間を持つイベントです。
- **ストリーミング「トップ k」:** 値のスキャン中に **size-k** 最大ヒープを維持します (上記の最大ヒープ パターンを参照)。
- **k 個のソートされたリスト/ファイルをマージ:** `(nextValue, listId)` を保持するリストごとに 1 つのヒープ エントリ。最小値を繰り返し**ポーリング**し、そのリストを進めます。


## 8. 関連メモ

- このサブメニューの **バイナリ ヒープ** [バイナリ ヒープ](viii-binary-heap.md) — 配列レイアウト、インデックス式、**buildHeap**、**heapsort**。
- **キュー** [キュー](v-queue.md) — 厳密な **FIFO**;下手にシミュレーションしない限り、アイテムごとの優先順位はありません。
- **レベル II** の概要: `ii-trees-heaps-hashing.md` (カリキュラム トラックに存在する場合)。

「どこにでも挿入して、常に最良の状態を取得する」ことに慣れたら、次のステップは自然なヒープ ノートです。ヒープ ノートは、この ADT の背後にある標準 **機械**です。

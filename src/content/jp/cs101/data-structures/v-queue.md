---
label: "V"
subtitle: "列"
group: "データ構造とアルゴリズム"
order: 5
---
キュー — FIFO リニア ADT

**キュー**は**スタック**のような**線形抽象データ型**ですが、**先入れ先出し(FIFO)**に従います。**最初**の要素**エンキュー**は、**最初**の**デキュー**です。スタックでは **後入れ先出し (LIFO)**、つまり最新のリーフが最初に使用されます。

**Java ベースライン:** スニペットは **Java SE 22** (`javac --release 22`）。これらは **JDK 21 LTS** でも実行されます。 JDK では ** を使用します`Queue<E>`** / **`Deque<E>`** と **`ArrayDeque<E>`** 一般的な FIFO キューの場合 (以下の例を参照)。

## 1. ADT としてキューに入れる
キューは、リンク リストを使用するか、下位の配列を使用するかによって定義されるのではなく、**操作** によって定義されます。

**コア操作** (**スタック**など、キューはほとんどの場合**を公開します)`size()`**: **Θ(1)** エンキュー/デキューのカウンター経由、またはリング バッファーのヘッド/テール インデックスから。)

- **`enqueue(x)`** - 通常は **無効**。データ要素を受け入れ、それをキューの**後ろ**に添付します。
- **`dequeue()`** — **引数なし**、削除する*要素を指定することは**できません**。コントラクトは常に、**先頭**の要素を削除して返す、つまり、まだ存在する要素の中で**最初にキューに入れられた者**です。 （もし`1`キューに入れられた最初の値、**最初**`dequeue()`削除します`1`;あなたはまだ**に電話します`dequeue()`**、「デキュー 1」ではありません。)
- **`peek()`** / **`front()`** — フロント要素を **削除せずに** 返します (一部の API はスタックからの「ピーク/トップ」文言を再利用します)。
- **`isEmpty()`** — キューに要素がない場合は true (多くの場合、`size == 0`または **`front == null`** リンクされた台紙上)。
- **`clear()`** — キューを空にします (リンク リストを使用し、** を削除します)`front`**GC** 言語では ** で十分な場合があるため、到達不能なノードは再利用されます。一部の API は明示的にウォークおよび null リンクも行います)。
- **`size()`** — 格納されている要素の数を返します (スタック ADT と同じ役割)。

**キューが使用できないもの**  
キューは、**ランダム インデックス アクセス**、**検索**、または**途中での挿入/削除**用に設計されたものではありません**。そのためには、別の構造 (リスト、デキュー、シーケンスとしての配列) を使用します。

**現実生活の直感**  
**パイプ**は流体を順番に運びます。一方の端から入り、もう一方の端から出ます。 **列**と**待機リスト**: 最初に到着した顧客から順に対応されます。 **ソフトウェア:** **ジョブ キュー**、**チケット購入**待合室、**BFS** グラフ、ストリーム バッファーを印刷します。


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 140" role="img" aria-label="Queue dequeue at front removes oldest enqueue at back adds newest">
  <defs>
    <marker id="ds-q-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#86efac"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">FIFO — oldest at front leaves first</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">dequeue() — no argument; FIFO picks the front · enqueue() appends at back</text>
  <text x="20" y="72" fill="#86efac" font-size="9" font-weight="600">front</text>
  <rect x="60" y="56" width="52" height="28" rx="4" fill="rgba(34,197,94,0.22)" stroke="#86efac" stroke-width="2"/>
  <rect x="118" y="56" width="52" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="176" y="56" width="52" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="234" y="56" width="52" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="300" y="72" fill="#60a5fa" font-size="9" font-weight="600">back</text>
  <text x="72" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">a</text>
  <text x="130" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">b</text>
  <text x="188" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">c</text>
  <text x="246" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">d</text>
  <path d="M40 100 H100" stroke="#86efac" stroke-width="2" marker-end="url(#ds-q-mk)"/>
  <text x="44" y="96" fill="#a1a1aa" font-size="9">dequeue</text>
  <path d="M320 100 H380" stroke="#60a5fa" stroke-width="2" marker-end="url(#ds-q-mk)"/>
  <text x="300" y="96" fill="#a1a1aa" font-size="9">enqueue ← new at back</text>
  <text x="12" y="128" fill="#71717a" font-size="10">Arrow at front illustrates one dequeue — FIFO decides it is the front cell, not a parameter.</text>
</svg></figure>

### 使用例 (Java)

**`ArrayDeque`** 実装 **`Deque`**、** を拡張します`Queue`**。 FIFO の場合、**後方**でエンキューし、**前**からデキューします。

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.Queue;

Queue<String> queue = new ArrayDeque<>();
queue.offer("first");   // enqueue at back
queue.offer("second");
queue.peek();           // "first" — front unchanged
queue.poll();           // "first" — dequeue from front
queue.poll();           // "second"
queue.isEmpty();        // true
```

**BFS** (幅優先検索) は古典的なキュー アルゴリズムです。ノードを訪問し、未訪問の近隣ノードをすべてキューに入れます。 **`poll`** は常に **最も古い** フロンティア セルを使用します。

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.List;
import java.util.Queue;

public final class BfsExamples {

  private BfsExamples() {}

  /** Returns visit order for an undirected graph given as adjacency lists. */
  public static List<Integer> bfsOrder(List<List<Integer>> adj, int start) {
    int n = adj.size();
    boolean[] seen = new boolean[n];
    Queue<Integer> q = new ArrayDeque<>();
    List<Integer> order = new ArrayList<>();

    seen[start] = true;
    q.offer(start);

    while (!q.isEmpty()) {
      int v = q.poll();
      order.add(v);
      for (int w : adj.get(v)) {
        if (!seen[w]) {
          seen[w] = true;
          q.offer(w);
        }
      }
    }
    return order;
  }
}
```


## 2. バッキングとしての単一リンクリスト (先頭 + 末尾)
作業は **2 つの異なる端**で行われるため、単一リンクされたキューはほぼ常に **`front`**（頭）**と** **`tail`** ポインタ。

**どの操作のどちらの目的ですか?** (単一リンクされたコスト)

| | に追加| で削除しますコストを追加する |コストを削除 |行列状？ |
|----------|-----------|----------|-------------|-----|
|頭 |頭 | Θ(1) | Θ(1) |両方同じ端 → **スタック**、端間の FIFO ではない |
|尻尾 |尻尾 | Θ(1) | **Θ(n)** |尻尾を切る前任者が必要 |
|頭 |尻尾 | Θ(1) | **Θ(n)** |末尾削除なし`prev`|
| **尾** | **頭** | **Θ(1)** | **Θ(1)** | **末尾でエンキュー、先頭でデキュー** ✓ |

それで： **`enqueue`で`tail`**、**`dequeue`で`front`**。両方とも **Θ(1)** で、**単一** リンク リストのみを持ちます。

**エンキュー (例: 値 5):** ノードを割り当て、リンクは古い`tail.next`新しいノードに進み、**`tail`** 新しいノードへ。キューが空の場合は ** を設定します`front`** そして **`tail`** そのノードに。

**デキュー:** データのコピー元`front`、 セット **`front = front.next`**;キューが空になった場合は ** を設定します`tail = null`**;オプションで古いノードをクリアします`next`**null** に設定すると切り離されます。

**キューの内容の例**`1 → 3 → 3 → 2`前から後ろへ (FIFO サービスの順序)。 **`enqueue(5)`:** の後に追加`2`最後尾で移動**`tail`** に`5`。その後、単一の**`dequeue()`** 先頭にあるものは何でも** 削除しますが、** はそのままです`1`**、最初にキューに入れられたため。この操作は「1 をデキューする」とは書かれていません。

### なぜ二重リンクしないのでしょうか?
**二重**リンク リストでも同じ操作を実装できますが、各ノードは **追加のポインタ** (`prev`）。 **head + tail** を持つ単一リンクされたキューでは、**Θ(1)** のエンキューとデキューがすでに行われているため、後方で **Θ(1)** の削除も必要な場合を除き、追加のメモリは通常 **価値がありません** (その場合は **デキュー**を検討してください)。


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 118" role="img" aria-label="Singly linked queue with front head and tail for enqueue and dequeue">
  <defs>
    <marker id="ds-qll-ar" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Singly linked queue — front &amp; tail</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">enqueue links past old tail · dequeue advances front</text>
  <text x="8" y="72" fill="#86efac" font-size="9" font-weight="600">front</text>
  <path d="M44 68 H58" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-qll-ar)"/>
  <rect x="62" y="54" width="44" height="32" rx="6" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <text x="76" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <path d="M108 70 H122" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-qll-ar)"/>
  <rect x="126" y="54" width="44" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="140" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">3</text>
  <path d="M172 70 H186" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-qll-ar)"/>
  <rect x="190" y="54" width="44" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="204" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">3</text>
  <path d="M236 70 H250" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-qll-ar)"/>
  <rect x="254" y="54" width="44" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="268" y="74" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <path d="M300 70 H314" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-qll-ar)"/>
  <text x="322" y="74" fill="#71717a" font-size="10">…</text>
  <text x="360" y="72" fill="#60a5fa" font-size="9" font-weight="600">tail</text>
  <path d="M348 78 L320 78" stroke="#60a5fa" stroke-width="1" stroke-dasharray="3 2"/>
  <text x="12" y="106" fill="#71717a" font-size="9">new enqueue attaches after tail; dequeue only rewires front</text>
</svg></figure>

### Java: 単一リンクされた FIFO キュー (ティーチング クラス)

**`enqueue`** で **`tail`**、**`dequeue`** で **`front`** — §2 に一致します。

```java
// Compile: javac --release 22 …
import java.util.NoSuchElementException;
import java.util.Objects;

public class LinkedQueue<E> {

  private static final class Node<E> {
    final E item;
    Node<E> next;

    Node(E item) {
      this.item = item;
    }
  }

  private Node<E> front;
  private Node<E> tail;
  private int size;

  public void enqueue(E item) {
    Objects.requireNonNull(item, "item");
    Node<E> node = new Node<>(item);
    if (tail == null) {
      front = tail = node;
    } else {
      tail.next = node;
      tail = node;
    }
    size++;
  }

  public E dequeue() {
    if (front == null) {
      throw new NoSuchElementException();
    }
    E out = front.item;
    front = front.next;
    if (front == null) {
      tail = null;
    }
    size--;
    return out;
  }

  public E peek() {
    if (front == null) {
      throw new NoSuchElementException();
    }
    return front.item;
  }

  public boolean isEmpty() {
    return front == null;
  }

  public int size() {
    return size;
  }

  public void clear() {
    front = null;
    tail = null;
    size = 0;
  }
}
```


## 3. 配列ベースのキュー: 循環 (ラップアラウンド) バッファー
これは **2 番目**の標準裏付けです (§2 のリンク リストの後)。目標は同じ **FIFO** コントラクトです。**後ろでエンキュー**、**前からデキュー**ですが、**単純な連続配列**では、常にインデックスを削除すると**前**のコストが高くなります。`0`そして、すべてを**シフト**します(デキューごとに**Θ(n)**)。 **完全なシフトを避ける**には、**固定容量のリング バッファ** (**循環** または **ラップアラウンド** 配列とも呼ばれます) を使用します。インデックスは、**モジュロを取得することで物理配列の最後に到達した後、**再利用します**。`capacity`**。

これは、**循環リンク リスト** (ポインタ トポロジ) と同じ構造ではありません。ここではメモリ内で何も「循環」せず、**インデックス演算**のみがラップされます。

**素朴な「配列リストを前面に」ではどうでしょうか?**  
一部の言語ライブラリ リストでは、インデックス 0 から繰り返し削除すると **O(n)** のシフトが発生します。リング バッファ キューは、格納された要素を移動せずに **Θ(1)** の **論理** 前/後を保持します。

### 追跡する必要がある状態
- **`capacity`** — バッキング配列の長さ (スロット)`0 … capacity−1`）。
- **`size`** - **現在**キュー内にある要素の数 (`0 … capacity`完全なポリシーに応じて）。
- **`front`** — **最初の**要素（デキューの次）のインデックス。
- **`back`** — 次の **エンキュー**が書き込む**次の空のスロット**のインデックス (このレッスンの共通規則)。それから **`back == (front + size) % capacity`** キューが曖昧な「完全な」エッジ ケースにない場合。 **仮定しないでください**`back == size`通常 1 回 **`front`**は移転しました。

**エンキュー:** 書き込み`data`で`arr[back]`;`back = (back + 1) % capacity`;`size++`。  
**デキュー:** 読み取り`arr[front]`;`front = (front + 1) % capacity`;`size--`; **`back`このモデルではデキュー時に移動**しません。

### チュートリアル:`RAMBLIN`次にデキューしてから、`WR`(容量 **7**、サイズ変更は無視)
**空で開始:**`size = 0`、`front = 0`、`back = 0`。

**エンキュー**`R, A, M, B, L, I, N`(**ramblin** の文字、長さ **7**): 各エンキュー後、**`front`** の間は 0** のままです`back`** 前進`1, 2, …`。 7 回挿入した後、`size = 7`。次はナイーブ`back`だろう`7`(範囲外); **包む：**`back = 7 % 7 = 0`。インデックスは常に ** を使用します`% capacity`** 最後のスロットを通過したとき。

**4`dequeue()`呼び出し** 削除`R`、`A`、`M`、`B`順番: 毎回 **`size`** デクリメントと **`front`** 進みます (`1`、`2`、`3`、`4`） と **`back`変更なし**`0`このストレッチで。

**エンキュー`W`:** 次の空きスロットはインデックスです **`0`** もう一度 — ** の **まとめ**`back`**。書く`W`そこには、`size`になる`4`、**`back`** になります`1`、**`front`** まだ **`4`** (論理キューはリングの中央に存在します)。

**エンキュー`R`:** インデックスに配置`1`、`size = 5`、`back = 2`、`front = 4`。

いつ **`dequeue`**その後散歩**`front`** 配列の終わりに向かって、** も使用します`(front + 1) % capacity`** それで **`front`** も同じようにラップします。

### 複雑さ (概要)
|操作 |時間 |メモ |
|----------|------|----------|
|`enqueue`/`dequeue`/`peek`/`isEmpty`/`size`/`clear`(インデックスをリセット) | **Θ(1)** |シフトはありません。インデックスラップのみ |
| **容量**を増やす (サイズ変更) | **Θ(n)** |すべてのスロットを新しいアレイにコピーします。動的配列のように倍増すると、**エンキュー**は**償却されたΘ(1)**のままになります。

リンク リストのバッキング: 配列の意味での **サイズ変更なし** — 「成長」とは **Θ(1)** 新しいノードです。リング バッファ: **サイズ変更** は、高価でまれなステップです。


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 130" role="img" aria-label="Circular buffer indices wrap with modulo capacity">
  <defs>
    <marker id="ds-qcb-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Ring buffer — same physical array, wrapping indices</text>
  <text x="12" y="38" fill="#a1a1aa" font-size="10">capacity = 7 → valid indices 0…6; after index 6, next is (i+1) mod 7</text>
  <rect x="20" y="52" width="40" height="26" rx="3" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <rect x="64" y="52" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="108" y="52" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="152" y="52" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="196" y="52" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="240" y="52" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="284" y="52" width="40" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="32" y="70" fill="#e4e4e7" font-size="10" font-family="ui-monospace">0</text>
  <text x="76" y="70" fill="#71717a" font-size="10">…</text>
  <text x="120" y="70" fill="#71717a" font-size="10">…</text>
  <text x="164" y="70" fill="#71717a" font-size="10">…</text>
  <text x="208" y="70" fill="#71717a" font-size="10">…</text>
  <text x="252" y="70" fill="#71717a" font-size="10">…</text>
  <text x="296" y="70" fill="#71717a" font-size="10">6</text>
  <path d="M328 64 H380" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#ds-qcb-mk)"/>
  <path d="M380 64 Q396 64 396 50 Q396 36 380 36 Q364 36 364 50" stroke="#a1a1aa" stroke-width="1.5" fill="none"/>
  <path d="M364 50 H24" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#ds-qcb-mk)"/>
  <text x="12" y="112" fill="#71717a" font-size="9">front / back / size track the logical queue inside the ring — see also ii-foundations.md</text>
</svg></figure>


**レベル II — 基礎** [基礎](../iii-foundations.md) 先頭/末尾のラベルが付いた別の循環バッファ図。

### Java: 拡張のあるリングバッファキュー

**`back`** は **次の書き込みインデックス**です。 **`front`** は次のデキューインデックスです。どちらも ** で囲みます`% capacity`**。の上 **`dequeue`**、**`back`動きません** (このレッスンのモデル)。

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.NoSuchElementException;
import java.util.Objects;

public class ArrayRingQueue<E> {

  private Object[] data;
  private int front;
  private int back;
  private int size;

  public ArrayRingQueue() {
    this.data = new Object[8];
  }

  private int capacity() {
    return data.length;
  }

  public void enqueue(E item) {
    Objects.requireNonNull(item, "item");
    if (size == capacity()) {
      grow();
    }
    data[back] = item;
    back = (back + 1) % capacity();
    size++;
  }

  @SuppressWarnings("unchecked")
  public E dequeue() {
    if (size == 0) {
      throw new NoSuchElementException();
    }
    E out = (E) data[front];
    data[front] = null;
    front = (front + 1) % capacity();
    size--;
    return out;
  }

  @SuppressWarnings("unchecked")
  public E peek() {
    if (size == 0) {
      throw new NoSuchElementException();
    }
    return (E) data[front];
  }

  public boolean isEmpty() {
    return size == 0;
  }

  public int size() {
    return size;
  }

  public void clear() {
    Arrays.fill(data, null);
    front = 0;
    back = 0;
    size = 0;
  }

  /** Copy logical order into a larger ring; reset indices to 0..size-1. */
  private void grow() {
    Object[] next = new Object[capacity() * 2];
    for (int i = 0; i < size; i++) {
      next[i] = data[(front + i) % capacity()];
    }
    data = next;
    front = 0;
    back = size;
  }
}
```

### Java:`Queue`対`ArrayDeque`対`LinkedList`

| API | FIFO キューの使用 |メモ |
|-----|----------------|----------|
| **`Queue.offer`/`poll`/`peek`** | **`ArrayDeque`** 実装として | **`offer`** = エンキューバック、**`poll`** = デキューフロント |
| **`Deque.addLast`/`removeFirst`** |上記と同じ終わり |背面/前面の明示的な名前 |
| **`LinkedList`** |実装物 **`Deque`** | **Θ(1)** は両端にありますが、** よりも要素あたりの **より多くのメモリ**`ArrayDeque`** |

**使用しないでください**`ArrayList`** 場合はキューとして **`remove(0)`** デキューごとに — これにより、配列全体がシフトされます (デキューごとに **Θ(n)**)。 **`ArrayDeque`** は通常の JDK の選択です。

**空でも安全なデキュー:** **`poll()`** を返します **`null`** 空の場合。 **`remove()`** 投げる **`NoSuchElementException`**。

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.Queue;

Queue<Integer> q = new ArrayDeque<>();
q.offer(1);
Integer x = q.poll();  // 1
Integer y = q.poll();  // null — queue empty
```

## 4. まとめ

|トピック |詳細 |
|----------|----------|
| **ルール** | FIFO — 最初にエンキューされ、最初にデキューされました。
| **単一リンク** | **`front`** (頭) + **`tail`**; **テール**をエンキュー、**ヘッド**をデキュー — Θ(1); **`size`**、**`isEmpty`**、**`clear`** Θ(1); 「サイズ変更」 = 新しいノード Θ(1) |
| **リングバッファ配列** | **`capacity`**、**`size`**、**`front`**、**`back`**; **で囲む`% capacity`**;エンキュー/デキュー/ピーク/空/サイズ/クリア (インデックスのリセット) **Θ(1)**; **償却済み Θ(1)** をエンキューします。 **コピーのサイズを変更 Θ(n)** |
| **二重リンク** |動作しますが、追加です`prev`ノードごと — 通常、プレーン キューの場合はスキップされます。
| **サポートされていません** |ランダムなインデックス、検索、内部挿入/削除 — 別の ADT を使用 |
| **Java デフォルト** | **`Queue<E>`** と **`ArrayDeque<E>`** — **`offer`/`poll`/`peek`** |

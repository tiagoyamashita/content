---
label: "III"
subtitle: "リンクされたリスト"
group: "データ構造とアルゴリズム"
order: 3
---
リンクされたリスト



ポインタベースのシーケンス: 単一リンクおよび二重リンク。 **Java** では、「ポインター」は **オブジェクト参照**、つまり次のようなフィールドです。`Node next`**ヒープ**上の別のノードのアドレスを保持します。マニュアルなんて絶対やらないよね`free`— 到達不能なノードは **ガベージ コレクション**されます。

**Java ベースライン:** スニペットは **Java SE 22** (`javac --release 22`);これらは **JDK 21 LTS** では引き続き有効です。

**単一リンク:** 各ノードが保持します`value`そして`next`。このリストは **head** 参照からアクセスされます。すでに保持しているノードの後に​​挿入します: **O(1)**。歩いて k 番目の要素を見つけます: **O(k)**;インデックスなしの値による検索: **O(n)**。

**二重リンク:** ノードを追加します`prev`したがって、その参照を保持しているときに **O(1)** 内のノードを削除し、先頭からスキャンせずに後方に進むことができます。

- **vs array:** リストは既知のノードの **O(1) splice** で勝ちます。配列は **O(1) インデックス** とシーケンシャル **キャッシュ** の動作で優れています。
- **Java コスト:** すべてのノードは **別個のオブジェクト** (ヘッダー + フィールド + アライメント)。密な`int[]`または`ArrayList<Integer>`通常、長いチェーンよりもキャッシュに適しています。`Integer`ノード (プリミティブなままであれば **オートボクシング** を回避できます)。

## 1. 単一リンク - 万が一のカスタムリスト (Java)

典型的なパターン: **静的ネストされたクラス**`Node<E>`。図書館ではよく保管されています **`private`**;ここ **`Node`は`public static`** 例では ** を呼び出すことができます`addAfter`** 厄介なアクセサーのないノード参照を使用します。 **`head`** は`null`リストが空の場合。

```java
// Compile: javac --release 22 …
import java.util.Iterator;
import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.function.Predicate;

public class SinglyLinkedList<E> implements Iterable<E> {

  /** Public for teaching: real libraries usually hide node references. */
  public static final class Node<E> {
    public final E item;
    public Node<E> next;

    public Node(E item, Node<E> next) {
      this.item = item;
      this.next = next;
    }
  }

  private Node<E> head;
  private int size;

  public int size() {
    return size;
  }

  /** Prepend — O(1). */
  public void addFirst(E item) {
    head = new Node<>(Objects.requireNonNull(item), head);
    size++;
  }

  /**
   * Insert immediately after {@code node}. O(1) if you already have {@code node}.
   * Does not check that {@code node} belongs to this list — caller's contract.
   */
  public void addAfter(Node<E> node, E item) {
    Objects.requireNonNull(node, "node");
    node.next = new Node<>(Objects.requireNonNull(item), node.next);
    size++;
  }

  /** Expose a node reference for teaching insert-after; production APIs rarely leak nodes. */
  public Node<E> getHeadNode() {
    return head;
  }

  /** Walk until predicate matches — O(n) worst case. */
  public Node<E> findFirst(Predicate<E> pred) {
    for (Node<E> cur = head; cur != null; cur = cur.next) {
      if (pred.test(cur.item)) {
        return cur;
      }
    }
    return null;
  }

  @Override
  public Iterator<E> iterator() {
    return new Iterator<>() {
      Node<E> cur = head;

      @Override
      public boolean hasNext() {
        return cur != null;
      }

      @Override
      public E next() {
        if (cur == null) {
          throw new NoSuchElementException();
        }
        E out = cur.item;
        cur = cur.next;
        return out;
      }
    };
  }
}
```

**使用法のスケッチ:** 先頭に追加`3`を挿入してから、`9`頭の後。

```java
// Compile: javac --release 22 …
SinglyLinkedList<Integer> list = new SinglyLinkedList<>();
list.addFirst(3);
SinglyLinkedList.Node<Integer> h = list.getHeadNode();
list.addAfter(h, 9); // 3 -> 9
```

**最初のノードの削除**は **O(1)** です。`head = head.next`(nullチェック後)。単一リンク リスト内の **任意** 内部ノードの削除は、**先行** 参照が既にある場合にのみ **O(1)** です。それ以外の場合は、そこから歩いて行かなければなりません`head`(**O(n)**) 見つけてください。

＃＃２。`java.util.LinkedList<E>`— JDK 二重リンクされた両端キュー

標準ライブラリの**`LinkedList`** は ** も実装する **二重リンク** リストです`Deque<E>`** (両端キュー): 効率的 **`addFirst`/`addLast`/`removeFirst`/`removeLast`**。

```java
// Compile: javac --release 22 …
import java.util.LinkedList;
import java.util.ListIterator;

LinkedList<String> names = new LinkedList<>();
names.addLast("Ada");
names.addLast("Grace");
names.addFirst("Alan");

for (String s : names) {
  System.out.println(s); // Alan, Ada, Grace
}

// O(n) to reach index, then O(1) per step with ListIterator
ListIterator<String> it = names.listIterator(1);
it.add("Linus"); // insert before "Ada" when cursor is at index 1
```

**反復子と構造の変更:** を通じてリストを変更する場合`add`/`remove`** フェイルファスト反復子で反復している間 (通常の **`for (E x : list)`**)、**を入手できます`ConcurrentModificationException`**。使用 **`ListIterator`**の**`add`/`remove`**、または変更を個別に収集します。

＃＃３。`LinkedList`対`ArrayList`Java で

|操作・お悩み |`ArrayList<E>`|`LinkedList<E>`|
|---------------------|----------------|----------------|
|ランダムアクセス`get(i)`| **O(1)** | **O(n)** (近い端から歩きます) |
| **既知のインデックス**で挿入/削除 | **O(n)** シフト | **O(n)** でインデックスに到達し、**O(1)** でリンクを修正します。
| **head** での挿入/削除 (deque の使用) | **O(n)** 特別なトリックを使用しない限り | **O(1)** |
|メモリ | 1 つのバッキング配列 + スラック | **要素ごとに 1 つのオブジェクト** + リンク |
|キャッシュ |連続した、フレンドリーな |ポインタの追跡、フレンドリーではない |

ほとんどの**順次**ワークロードの場合、**`ArrayList`** は Java のデフォルトの選択です。 **`LinkedList`** は、**末尾** または ** で多くの **O(1)** 挿入/削除が本当に必要な場合に輝きます。`ListIterator`**大きな**リストを歩き回る - プロフィールはまだ残っています。最近の CPU はコンパクトな配列を好むことがよくあります。

## 4. 二重リンク — なぜ`prev`助けます

と **`prev`**、**`unlink(node)`** は、先行ポインタをスキャンせずに **O(1)** の近隣ポインタを再配線します。 JDK の **`LinkedList`** これは ** に対して内部的に行われます`remove(Obj)`** ノードが見つかると (すでに ** を保持していない限り、検索は **O(n)** のままです`ListIterator`** 位置）。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 168" role="img" aria-label="Singly linked list and O(1) insert after a known node">
  <defs>
    <marker id="ds-ll-n" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Singly linked — walk with next</text>
  <text x="12" y="40" fill="#71717a" font-size="10">head → nodes; no index arithmetic</text>
  <text x="12" y="62" fill="#86efac" font-size="9" font-weight="600">head</text>
  <path d="M44 58 H68" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-ll-n)"/>
  <rect x="72" y="44" width="64" height="36" rx="6" fill="rgba(34,197,94,0.15)" stroke="#86efac" stroke-width="2"/>
  <text x="88" y="66" fill="#e4e4e7" font-size="11">A</text>
  <path d="M138 62 H162" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-ll-n)"/>
  <rect x="166" y="44" width="64" height="36" rx="6" fill="rgba(251,191,36,0.15)" stroke="#fbbf24" stroke-width="2"/>
  <text x="186" y="66" fill="#e4e4e7" font-size="11">B</text>
  <path d="M232 62 H256" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-ll-n)"/>
  <rect x="260" y="44" width="64" height="36" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="280" y="66" fill="#e4e4e7" font-size="11">C</text>
  <path d="M326 62 H350" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-ll-n)"/>
  <text x="358" y="66" fill="#71717a" font-size="11">null</text>
  <text x="12" y="108" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Insert N after B (you hold B)</text>
  <text x="12" y="126" fill="#a1a1aa" font-size="10">rewire: B.next → N, N.next → old B.next — no shifting of A or C in memory</text>
  <rect x="166" y="132" width="64" height="32" rx="6" fill="rgba(251,191,36,0.15)" stroke="#fbbf24" stroke-width="2"/>
  <text x="186" y="152" fill="#e4e4e7" font-size="11">B</text>
  <path d="M232 148 H248" stroke="#60a5fa" stroke-width="2" stroke-dasharray="4 2" marker-end="url(#ds-ll-n)"/>
  <rect x="252" y="132" width="64" height="32" rx="6" fill="rgba(96,165,250,0.2)" stroke="#60a5fa" stroke-width="2"/>
  <text x="272" y="152" fill="#e4e4e7" font-size="11">N</text>
  <path d="M318 148 H334" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-ll-n)"/>
  <rect x="338" y="132" width="64" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="358" y="152" fill="#e4e4e7" font-size="11">C</text>
</svg></figure>

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 88" role="img" aria-label="Doubly linked list prev and next pointers">
  <defs>
    <marker id="ds-ll-df" markerWidth="7" markerHeight="7" refX="7" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#60a5fa"/></marker>
    <!-- Same geometry as ds-ll-df so marker-end on a leftward path points along prev (toward earlier node). -->
    <marker id="ds-ll-df-y" markerWidth="7" markerHeight="7" refX="7" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#fbbf24"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-family="system-ui,sans-serif" font-weight="600">Doubly linked — O(1) cut-out with node pointer</text>
  <rect x="40" y="36" width="88" height="36" rx="6" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="58" y="58" fill="#e4e4e7" font-size="10">prev · val · next</text>
  <path d="M130 54 H146" stroke="#60a5fa" stroke-width="2" marker-end="url(#ds-ll-df)"/>
  <path d="M146 48 H130" stroke="#fbbf24" stroke-width="2" marker-end="url(#ds-ll-df-y)"/>
  <rect x="150" y="36" width="88" height="36" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="168" y="58" fill="#e4e4e7" font-size="10">prev · val · next</text>
  <path d="M240 54 H256" stroke="#60a5fa" stroke-width="2" marker-end="url(#ds-ll-df)"/>
  <path d="M256 48 H240" stroke="#fbbf24" stroke-width="2" marker-end="url(#ds-ll-df-y)"/>
  <rect x="260" y="36" width="88" height="36" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="278" y="58" fill="#e4e4e7" font-size="10">prev · val · next</text>
  <text x="12" y="82" fill="#71717a" font-size="9">rewire prev/next of neighbors — no scan from head</text>
</svg></figure>

---
label: "III"
subtitle: "Linked list"
group: "Data structures & algorithms"
order: 3
---
Linked list
Pointer-based sequence: singly and doubly linked. In **Java**, “pointers” are **object references**: a field like `Node next` holds the address of another node on the **heap**; you never do manual `free` — unreachable nodes are **garbage-collected**.

**Singly linked:** each node holds `value` and `next`. The list is reached from a **head** reference. Insert after a node you already hold: **O(1)**. Find the k-th element by walking: **O(k)**; search by value without index: **O(n)**.

**Doubly linked:** nodes add `prev`, so you can remove a node in **O(1)** when you hold its reference, and walk backward without scanning from the head.

- **vs array:** lists win on **O(1) splice** at a known node; arrays win on **O(1) index** and sequential **cache** behavior.
- **Java cost:** every node is a **separate object** (header + fields + alignment). A dense `int[]` or `ArrayList<Integer>` is usually more cache-friendly than a long chain of `Integer` nodes (and avoids **autoboxing** if you stay primitive).

## 1. Singly linked — minimal custom list (Java)

Typical pattern: a **static nested class** `Node<E>`. Libraries often keep it **`private`**; here **`Node` is `public static`** so examples can call **`addAfter`** with a node reference without awkward accessors. **`head`** is `null` when the list is empty.

```java
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

**Usage sketch:** prepend `3`, then insert `9` after the head.

```java
SinglyLinkedList<Integer> list = new SinglyLinkedList<>();
list.addFirst(3);
SinglyLinkedList.Node<Integer> h = list.getHeadNode();
list.addAfter(h, 9); // 3 -> 9
```

**Removing the first node** is **O(1)**: `head = head.next` (after null-check). Removing an **arbitrary** interior node in a singly linked list is **O(1)** only if you already have the **predecessor** reference; otherwise you must walk from `head` (**O(n)**) to find it.

## 2. `java.util.LinkedList<E>` — JDK doubly linked deque

The standard library’s **`LinkedList`** is a **doubly linked** list that also implements **`Deque<E>`** (double-ended queue): efficient **`addFirst` / `addLast` / `removeFirst` / `removeLast`**.

```java
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

**Iterator and structural changes:** if you modify the list through **`add` / `remove`** while iterating with a fail-fast iterator (the usual **`for (E x : list)`**), you can get **`ConcurrentModificationException`**. Use **`ListIterator`**’s **`add` / `remove`**, or collect changes separately.

## 3. `LinkedList` vs `ArrayList` in Java

| Operation / concern | `ArrayList<E>` | `LinkedList<E>` |
|---------------------|----------------|-----------------|
| Random access `get(i)` | **O(1)** | **O(n)** (walk from nearer end) |
| Insert/remove at **known index** | **O(n)** shift | **O(n)** to reach index, then **O(1)** link fix |
| Insert/remove at **head** (deque usage) | **O(n)** unless you use extra tricks | **O(1)** |
| Memory | one backing array + slack | **one object per element** + links |
| Cache | contiguous, friendly | pointer chasing, less friendly |

For most **sequential** workloads, **`ArrayList`** is the default choice in Java. **`LinkedList`** shines when you truly need many **O(1)** inserts/removes at **ends** or with a **`ListIterator`** walking a **large** list — still profile; modern CPUs often favor compact arrays.

## 4. Doubly linked — why `prev` helps

With **`prev`**, **`unlink(node)`** rewires neighbor pointers in **O(1)** without scanning for the predecessor. The JDK’s **`LinkedList`** does this internally for **`remove(Obj)`** once the node is found (finding is still **O(n)** unless you already hold a **`ListIterator`** position).

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

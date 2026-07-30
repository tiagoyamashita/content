---
label: "III"
subtitle: "Lista vinculada"
group: "Estruturas de dados e algoritmos"
order: 3
---
Lista vinculada
Sequência baseada em ponteiro: ligada simples e duplamente. Em **Java**, “ponteiros” são **referências de objetos**: um campo como`Node next`contém o endereço de outro nó no **heap**; você nunca faz manual`free`— nós inacessíveis são **coletados como lixo**.

**Java linha de base:** trechos assumem **Java SE 22** (`javac --release 22`); eles permanecem válidos em **JDK 21 LTS**.

**Vinculado individualmente:** cada nó contém`value`e`next`. A lista é acessada a partir de uma referência **head**. Insira após um nó que você já possui: **O(1)**. Encontre o k-ésimo elemento caminhando: **O(k)**; pesquisa por valor sem índice: **O(n)**.

**Duplamente vinculado:** nós são adicionados`prev`, para que você possa remover um nó em **O(1)** ao manter sua referência e caminhar para trás sem digitalizar a partir da cabeça.

- **vs array:** lista a vitória em **O(1) splice** em um nó conhecido; matrizes vencem no índice **O(1)** e no comportamento de **cache** sequencial.
- **Java custo:** cada nó é um **objeto separado** (cabeçalho + campos + alinhamento). Um denso`int[]`ou`ArrayList<Integer>`geralmente é mais amigável ao cache do que uma longa cadeia de`Integer`nós (e evita **autoboxing** se você permanecer primitivo).

## 1. Vinculado individualmente - lista personalizada mínima (Java)

Padrão típico: uma **classe aninhada estática**`Node<E>`. As bibliotecas costumam mantê-lo **`private`**; aqui **`Node`é`public static`** então exemplos podem chamar **`addAfter`** com uma referência de nó sem acessadores estranhos. **`head`** é`null`quando a lista está vazia.

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

**Esboço de uso:** preceder`3`, em seguida, insira`9`depois da cabeça.

```java
// Compile: javac --release 22 …
SinglyLinkedList<Integer> list = new SinglyLinkedList<>();
list.addFirst(3);
SinglyLinkedList.Node<Integer> h = list.getHeadNode();
list.addAfter(h, 9); // 3 -> 9
```

**Remover o primeiro nó** é **O(1)**:`head = head.next`(após verificação nula). Remover um nó interior **arbitrário** em uma lista vinculada individualmente é **O(1)** somente se você já tiver a referência do **predecessor**; caso contrário, você deve caminhar de`head`(**O(n)**) para encontrá-lo.

## 2.`java.util.LinkedList<E>`- JDK deque duplamente vinculado

A biblioteca padrão **`LinkedList`** é uma lista **duplamente vinculada** que também implementa **`Deque<E>`** (fila dupla): eficiente **`addFirst`-&#09;o`addLast`-&#09;o`removeFirst`-&#09;o`removeLast`**.

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

**Iterador e mudanças estruturais:** se você modificar a lista por meio de **`add`-&#09;o`remove`** enquanto itera com um iterador fail-fast (o usual **`for (E x : list)`**), você pode obter **`ConcurrentModificationException`**. Usar **`ListIterator`** é **`add`-&#09;o`remove`**, ou colete as alterações separadamente.

## 3.`LinkedList`contra`ArrayList`em Java

| Operação/preocupação |`ArrayList<E>`|`LinkedList<E>`|
|---------------------|----------------|-----------------|
| Acesso aleatório`get(i)`| **O(1)** | **O(n)** (caminhar do final mais próximo) |
| Inserir/remover em **índice conhecido** | **O(n)** mudança | **O(n)** para alcançar o índice, então **O(1)** correção do link |
| Inserir/remover em **head** (uso deque) | **O(n)** a menos que você use truques extras | **O(1)** |
| Memória | uma matriz de apoio + folga | **um objeto por elemento** + links |
| Cache | contíguo, amigável | perseguição de ponteiro, menos amigável |

Para a maioria das cargas de trabalho **sequenciais**, **`ArrayList`** é a escolha padrão em Java. **`LinkedList`** brilha quando você realmente precisa de muitas inserções/remoções **O(1)** nas **extremidades** ou com um **`ListIterator`** percorrendo uma lista **grande** - ainda perfil; CPUs modernos geralmente favorecem arrays compactos.

## 4. Duplamente vinculado - por que`prev`ajuda

Com **`prev`**, **`unlink(node)`** reconecta ponteiros vizinhos em **O(1)** sem procurar o antecessor. Os JDK **`LinkedList`** faz isso internamente para **`remove(Obj)`** assim que o nó for encontrado (a descoberta ainda será **O(n)**, a menos que você já possua um **`ListIterator`**posição).

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

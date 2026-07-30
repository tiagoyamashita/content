---
label: "IV"
subtitle: "Pilha"
group: "Estruturas de dados e algoritmos"
order: 4
---
Stack — duas implementações de apoio
A **stack ADT** é definida por suas **operações**, não pelo fato de você usar uma lista ou um array abaixo dela. Esta nota compara dois suportes padrão: uma **lista vinculada individualmente** (cabeça = topo) e uma **matriz dinâmica** (parte superior na parte traseira lógica).

**Java linha de base:** os snippets assumem **Java SE 22** — defina o nível de linguagem como **22** em seu IDE ou compile com **`javac --release 22`**. Os recursos usados ​​aqui (genéricos,`var`somente se adicionado,`Deque`, etc.) também são executados em **JDK 21 LTS**; trate **22** como o mínimo em relação ao qual este material é verificado e use um **LTS** JDK na produção se sua equipe exigir.

## 1. Pilha como ADT (recapitulação)
**Operações** geralmente incluem`push(x)`,`pop()`,`peek()`-&#09;o`top()`,`isEmpty()`, e muitas vezes`size()`-&#09;o`clear()`. **Invariante:**`pop`remove o item **enviado mais recentemente** (LIFO).

Uma pilha **não** se destina a **acesso ao índice** arbitrário, **pesquisa** ou **inserir/remover no meio**. Se você precisar desses comportamentos, modele uma estrutura **diferente** (por exemplo, deque, lista ou array usado como uma sequência).

**Usos:** DFS, desfazer, correspondência de colchetes, avaliação de postfix, intuição de pilha de chamadas.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 168" role="img" aria-label="Stack after three pushes then one pop removes newest item at top">
  <defs>
    <marker id="ds-st-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After push(1) push(2) push(3)</text>
  <text x="48" y="42" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="40" y="48" width="80" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="76" y="65" fill="#e4e4e7" font-size="12" font-family="ui-monospace">3</text>
  <rect x="40" y="78" width="80" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="76" y="95" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <rect x="40" y="108" width="80" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="76" y="125" fill="#e4e4e7" font-size="12" font-family="ui-monospace">1</text>
  <path d="M140 88 H200" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-st-mk)"/>
  <text x="148" y="82" fill="#a1a1aa" font-size="10">pop()</text>
  <text x="148" y="96" fill="#fbbf24" font-size="10" font-weight="600">returns 3</text>
  <text x="220" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After one pop (LIFO)</text>
  <text x="256" y="42" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="248" y="48" width="80" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="284" y="65" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <rect x="248" y="78" width="80" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="284" y="95" fill="#e4e4e7" font-size="12" font-family="ui-monospace">1</text>
  <text x="12" y="154" fill="#71717a" font-size="10">Only the top changes on push/pop — both backings keep every op O(1) at the top.</text>
</svg></figure>

### Visuais por operação (ADT)

(R)`push(x)`** — o novo elemento se torna o **topo**; tudo que já está na pilha fica **abaixo** dela.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 130" role="img" aria-label="push adds a new top element">
  <defs>
    <marker id="op-push-ar" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">push(4)</text>
  <text x="10" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="8" y="42" width="72" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="38" y="59" fill="#e4e4e7" font-size="12" font-family="ui-monospace">3</text>
  <rect x="8" y="72" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="89" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <rect x="8" y="102" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="119" fill="#e4e4e7" font-size="12" font-family="ui-monospace">1</text>
  <path d="M92 55 H130" stroke="#a1a1aa" stroke-width="2" marker-end="url(#op-push-ar)"/>
  <text x="96" y="50" fill="#60a5fa" font-size="10" font-weight="600">push(4)</text>
  <text x="140" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After</text>
  <text x="140" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="138" y="42" width="72" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="168" y="59" fill="#e4e4e7" font-size="12" font-family="ui-monospace">4</text>
  <rect x="138" y="72" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="168" y="89" fill="#e4e4e7" font-size="12" font-family="ui-monospace">3</text>
  <rect x="138" y="102" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="168" y="119" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <text x="230" y="18" fill="#71717a" font-size="10">Older values sink one step;</text>
  <text x="230" y="32" fill="#71717a" font-size="10">the new value is always LIFO “first out” next.</text>
</svg></figure>

(R)`peek()`** / **`top()`** — inspecione a parte superior **sem** removê-la; o desenho permanece **inalterado** depois de uma espiada.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 380 126" role="img" aria-label="peek reads top without changing stack">
  <text x="10" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">peek() / top()</text>
  <text x="10" y="38" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="8" y="44" width="72" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2" stroke-dasharray="4 3"/>
  <text x="38" y="61" fill="#e4e4e7" font-size="12" font-family="ui-monospace">3</text>
  <rect x="8" y="74" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="91" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <rect x="8" y="104" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="121" fill="#e4e4e7" font-size="12" font-family="ui-monospace">1</text>
  <path d="M100 57 Q140 28 200 28" stroke="#fbbf24" stroke-width="2" fill="none"/>
  <text x="148" y="22" fill="#fbbf24" font-size="11" font-family="ui-monospace" font-weight="600">returns 3</text>
  <text x="200" y="70" fill="#71717a" font-size="10">Same stack after peek —</text>
  <text x="200" y="84" fill="#71717a" font-size="10">no pop, no size change.</text>
</svg></figure>

(R)`pop()`** — remove e retorna o topo **atual** (a mesma célula **`peek`** leria).

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 126" role="img" aria-label="pop removes and returns top element">
  <defs>
    <marker id="op-pop-ar" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">pop()</text>
  <text x="10" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="8" y="42" width="72" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="38" y="59" fill="#e4e4e7" font-size="12" font-family="ui-monospace">3</text>
  <rect x="8" y="72" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="89" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <rect x="8" y="102" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="119" fill="#e4e4e7" font-size="12" font-family="ui-monospace">1</text>
  <path d="M92 55 H128" stroke="#a1a1aa" stroke-width="2" marker-end="url(#op-pop-ar)"/>
  <text x="96" y="50" fill="#fbbf24" font-size="10" font-weight="600">returns 3</text>
  <text x="138" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After</text>
  <text x="138" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="136" y="42" width="72" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="166" y="59" fill="#e4e4e7" font-size="12" font-family="ui-monospace">2</text>
  <rect x="136" y="72" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="166" y="89" fill="#e4e4e7" font-size="12" font-family="ui-monospace">1</text>
  <text x="228" y="62" fill="#71717a" font-size="10">Top moves down; size drops by 1.</text>
</svg></figure>

(R)`isEmpty()`** — verdadeiro quando não há **nenhum** topo (nada para`peek`ou`pop`).

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="isEmpty true when stack has no elements">
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">isEmpty()</text>
  <rect x="10" y="38" width="100" height="44" rx="6" fill="rgba(24,24,27,0.5)" stroke="#52525b" stroke-dasharray="6 4"/>
  <text x="34" y="64" fill="#71717a" font-size="11">no elements</text>
  <text x="128" y="64" fill="#86efac" font-size="11" font-weight="600">→ true</text>
  <text x="220" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">not empty</text>
  <text x="220" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="218" y="42" width="56" height="28" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="240" y="60" fill="#e4e4e7" font-size="12" font-family="ui-monospace">x</text>
  <text x="290" y="64" fill="#86efac" font-size="11" font-weight="600">→ false</text>
</svg></figure>

(R)`size()`** — contagem lógica de elementos **incluindo** o topo; esta pilha tem **três** valores no total.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 360 128" role="img" aria-label="size counts elements in stack">
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">size()</text>
  <text x="10" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="8" y="42" width="72" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="38" y="59" fill="#e4e4e7" font-size="12" font-family="ui-monospace">c</text>
  <rect x="8" y="72" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="89" fill="#e4e4e7" font-size="12" font-family="ui-monospace">b</text>
  <rect x="8" y="102" width="72" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="38" y="119" fill="#e4e4e7" font-size="12" font-family="ui-monospace">a</text>
  <text x="100" y="78" fill="#60a5fa" font-size="12" font-family="ui-monospace" font-weight="600">size = 3</text>
</svg></figure>

(R)`clear()`** — elimine todos os elementos; depois **`isEmpty()`** é verdade e **`size()`** é **`0`**.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" role="img" aria-label="clear removes all stack elements">
  <defs>
    <marker id="op-clr-ar" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">clear()</text>
  <text x="10" y="36" fill="#86efac" font-size="9" font-weight="600">top →</text>
  <rect x="8" y="42" width="56" height="26" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <text x="30" y="59" fill="#e4e4e7" font-size="11" font-family="ui-monospace">z</text>
  <rect x="8" y="72" width="56" height="26" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="30" y="89" fill="#e4e4e7" font-size="11" font-family="ui-monospace">y</text>
  <path d="M78 55 H118" stroke="#a1a1aa" stroke-width="2" marker-end="url(#op-clr-ar)"/>
  <text x="82" y="48" fill="#a1a1aa" font-size="10">clear</text>
  <rect x="128" y="48" width="120" height="44" rx="6" fill="rgba(24,24,27,0.5)" stroke="#52525b" stroke-dasharray="6 4"/>
  <text x="158" y="74" fill="#71717a" font-size="11">empty stack</text>
  <text x="268" y="74" fill="#86efac" font-size="10" font-weight="600">size = 0</text>
</svg></figure>

### Exemplo de uso (Java)

O tipo de **biblioteca** que você normalmente deseja é **`Deque<E>`** com **`ArrayDeque<E>`** (abordado posteriormente nesta nota em Java). Aqui está o mesmo vocabulário ADT em algumas linhas:

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.Deque;

Deque<Integer> stack = new ArrayDeque<>();
stack.push(10);
stack.push(20);
stack.peek();     // 20 — top unchanged
stack.pop();      // 20
stack.isEmpty();  // false (10 still inside)
stack.size();     // 1
stack.clear();
stack.isEmpty();  // true
```

**Colchetes balanceados** é um exercício clássico de pilha: em um símbolo de abertura, **`push`**; em um símbolo de fechamento, **`pop`** e verifique se combina com o que você estourou; no final da string, **`isEmpty()`** deve ser **verdadeiro**.

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.Deque;

public final class BracketExamples {

  private BracketExamples() {}

  public static boolean bracketsBalanced(String s) {
    Deque<Character> stack = new ArrayDeque<>();
    for (int i = 0; i < s.length(); i++) {
      char c = s.charAt(i);
      if (c == '(' || c == '[' || c == '{') {
        stack.push(c);
      } else if (c == ')' || c == ']' || c == '}') {
        if (stack.isEmpty()) {
          return false;
        }
        char o = stack.pop();
        if (!pairs(o, c)) {
          return false;
        }
      }
    }
    return stack.isEmpty();
  }

  private static boolean pairs(char open, char close) {
    return switch (open) {
      case '(' -> close == ')';
      case '[' -> close == ']';
      case '{' -> close == '}';
      default -> false;
    };
  }
}
```


## 2. Lista vinculada individualmente como apoio
Trate o **ponteiro principal como o topo**. Uma pilha **vazia** é uma lista vazia:`head == null`.

**Push:** aloque um novo nó, aponte-o para o cabeçalho antigo, atribua`head`para o novo nó — **Θ(1)**.  
**Pop:** leia`head`, avançar`head`para`head.next`, retorne o valor do topo antigo - **Θ(1)**.  
Você **não precisa de um ponteiro de cauda**: cada operação de pilha toca apenas a cabeça.

(R)`push(x)`** (lista de apoio) — novos nós **`next`** é a cabeça velha; **`head`** move para o novo nó.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 108" role="img" aria-label="Linked list push prepends new node at head">
  <defs>
    <marker id="ll-push-mk" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="8" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Before push(9)</text>
  <text x="8" y="36" fill="#86efac" font-size="9" font-weight="600">head →</text>
  <rect x="48" y="44" width="40" height="32" rx="6" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <text x="62" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <path d="M90 60 H102" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-push-mk)"/>
  <rect x="106" y="44" width="40" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="120" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <path d="M148 60 H160" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-push-mk)"/>
  <text x="168" y="64" fill="#71717a" font-size="11">null</text>
  <path d="M220 58 H268" stroke="#60a5fa" stroke-width="2" marker-end="url(#ll-push-mk)"/>
  <text x="224" y="52" fill="#60a5fa" font-size="10" font-weight="600">push(9)</text>
  <text x="278" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After</text>
  <text x="278" y="36" fill="#86efac" font-size="9" font-weight="600">head →</text>
  <rect x="318" y="44" width="40" height="32" rx="6" fill="rgba(96,165,250,0.2)" stroke="#60a5fa" stroke-width="2"/>
  <text x="328" y="62" fill="#e4e4e7" font-size="10" font-family="ui-monospace">9 new</text>
  <path d="M360 60 H372" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-push-mk)"/>
  <rect x="376" y="44" width="40" height="32" rx="6" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <text x="390" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <path d="M418 60 H430" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-push-mk)"/>
  <rect x="434" y="44" width="40" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="448" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <path d="M476 60 H488" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-push-mk)"/>
  <text x="496" y="64" fill="#71717a" font-size="11">null</text>
  <text x="8" y="98" fill="#71717a" font-size="9">One pointer write for the new node’s next, one for head — both O(1).</text>
</svg></figure>

(R)`pop()`** (lista de apoio) — salve o valor da cabeça, defina **`head = head.next`**, retorne o valor salvo.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 108" role="img" aria-label="Linked list pop advances head and returns old top">
  <defs>
    <marker id="ll-pop-mk" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="8" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Before pop()</text>
  <text x="8" y="36" fill="#86efac" font-size="9" font-weight="600">head →</text>
  <rect x="48" y="44" width="40" height="32" rx="6" fill="rgba(251,191,36,0.25)" stroke="#fbbf24" stroke-width="2"/>
  <text x="62" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">9</text>
  <path d="M90 60 H102" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-pop-mk)"/>
  <rect x="106" y="44" width="40" height="32" rx="6" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <text x="120" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <path d="M148 60 H160" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-pop-mk)"/>
  <rect x="164" y="44" width="40" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="178" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <path d="M206 60 H218" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-pop-mk)"/>
  <text x="226" y="64" fill="#71717a" font-size="11">null</text>
  <path d="M248 58 H296" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-pop-mk)"/>
  <text x="252" y="52" fill="#fbbf24" font-size="10" font-weight="600">returns 9</text>
  <text x="306" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After</text>
  <text x="306" y="36" fill="#86efac" font-size="9" font-weight="600">head →</text>
  <rect x="346" y="44" width="40" height="32" rx="6" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <text x="360" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <path d="M388 60 H400" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-pop-mk)"/>
  <rect x="404" y="44" width="40" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="418" y="64" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <path d="M446 60 H458" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ll-pop-mk)"/>
  <text x="466" y="64" fill="#71717a" font-size="11">null</text>
  <text x="8" y="98" fill="#71717a" font-size="9">Old top becomes unreachable (GC) unless you keep a reference elsewhere.</text>
</svg></figure>

### Java: pilha head-as-top (dando aula)

Isso reflete as operações de lista **prepend / delete-first** da nota da lista vinculada: **`head`** é o **topo**; sem ponteiro de cauda.

```java
// Compile: javac --release 22 …
import java.util.NoSuchElementException;
import java.util.Objects;

public class LinkedStack<E> {

  private static final class Node<E> {
    final E item;
    Node<E> next;

    Node(E item, Node<E> next) {
      this.item = item;
      this.next = next;
    }
  }

  private Node<E> head;
  private int size;

  public void push(E item) {
    head = new Node<>(Objects.requireNonNull(item), head);
    size++;
  }

  public E pop() {
    if (head == null) {
      throw new NoSuchElementException();
    }
    E out = head.item;
    head = head.next;
    size--;
    return out;
  }

  public E peek() {
    if (head == null) {
      throw new NoSuchElementException();
    }
    return head.item;
  }

  public boolean isEmpty() {
    return head == null;
  }

  public int size() {
    return size;
  }

  /** O(1): drop the chain; nodes become unreachable for the GC. */
  public void clear() {
    head = null;
    size = 0;
  }
}
```

### Passo a passo (valores duplicados)
Envie os valores na ordem **1**, depois **3** (primeira ocorrência), depois **3** (segunda ocorrência) e depois **2**. Quando dois nós possuem o mesmo valor de exibição, rotule-os como **3⁽¹⁾** e **3⁽²⁾** no raciocínio:

1.`push(1)`— cabeça →`1`2.`push(3⁽¹⁾)`— cabeça →`3⁽¹⁾`→`1`3.`push(3⁽²⁾)`— cabeça →`3⁽²⁾`→`3⁽¹⁾`→`1`(a cabeça é o **segundo** três)  
4.`push(2)`— cabeça →`2`→`3⁽²⁾`→`3⁽¹⁾`→`1`

Nos desenhos, o **topo** geralmente é colocado à **esquerda** e os nós mais antigos se estendem para a **direita**; novos empurrões chegam à cabeça, de modo que os elementos mais antigos aparecem “mais profundos” na cadeia.

**Pop:** sempre desconecte o cabeçalho (o mesmo que excluir lista no cabeçalho). Exemplo aparece na ordem return **2**, depois **3⁽²⁾**, depois **3⁽¹⁾**, depois **1**; depois do quarto pop,`head`é **null** – pilha vazia.

**Limpar:** definido`head = null`— **Θ(1)** tempo; os nós tornam-se inacessíveis e um **GC** pode recuperá-los (em linguagens gerenciadas) ou você os libera explicitamente em C/C++.

### Por que não duplamente vinculado?
Uma lista duplamente vinculada ainda suporta operações de pilha, mas cada nó armazena um **ponteiro extra** (`prev`). As pilhas nunca precisam de retrocesso para comportamento correto, portanto, a **sobrecarga de memória** não compra nada que você usa.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="Singly linked stack head on left as top nodes to the right">
  <defs>
    <marker id="ds-st-ll" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Head = top (left in this sketch)</text>
  <text x="12" y="40" fill="#86efac" font-size="9" font-weight="600">head →</text>
  <rect x="52" y="48" width="44" height="36" rx="6" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <text x="66" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <path d="M98 66 H112" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-st-ll)"/>
  <rect x="116" y="48" width="44" height="36" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="128" y="68" fill="#e4e4e7" font-size="10" font-family="ui-monospace">3₂</text>
  <path d="M162 66 H176" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-st-ll)"/>
  <rect x="180" y="48" width="44" height="36" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="192" y="68" fill="#e4e4e7" font-size="10" font-family="ui-monospace">3₁</text>
  <path d="M226 66 H240" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-st-ll)"/>
  <rect x="244" y="48" width="44" height="36" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="258" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <path d="M290 66 H304" stroke="#a1a1aa" stroke-width="2" marker-end="url(#ds-st-ll)"/>
  <text x="312" y="70" fill="#71717a" font-size="11">null</text>
  <text x="12" y="94" fill="#71717a" font-size="9">push/pop only rewire head — no tail, no index scans</text>
</svg></figure>


## 3. Array (matriz dinâmica) como suporte
Acompanhe um **`size`** (contagem de elementos lógicos). **Pilha vazia**:`size == 0`.

**Onde está o topo?** Se você sempre **inserir no índice 0**, cada push deve **deslocar** todos os elementos existentes — **Θ(n)** por push. Em vez disso, cresça na **parte traseira**: o **próximo push** grava no índice **`size`**, então incremente`size`. O **topo** (para`peek`-&#09;o`pop`) está no índice **`size - 1`**.

### Mesma sequência no array
Capacidade suficientemente grande; começar`size = 0`.

| Etapa | Ação | Índices de array (conceituais) | tamanho depois |
|------|--------|---------------------------|------------|
| — | vazio |`[ · · · · ]`| 0 |
| 1 | empurre 1 |`[1, ·, ·, ·]`| 1 |
| 2 | empurre 3⁽¹⁾ |`[1, 3, ·, ·]`| 2 |
| 3 | empurre 3⁽²⁾ |`[1, 3, 3, ·]`| 3 |
| 4 | empurre 2 |`[1, 3, 3, 2]`| 4 |

**Pop:** leia`arr[size - 1]`, então`size--`— **Θ(1)** (você pode liberar espaço para GC ou segurança — veja abaixo).  
**Push:** **amortizado Θ(1)** em um **array dinâmico** porque a tabela ocasionalmente **redimensiona** (copie todos os elementos para um novo bloco maior - essa etapa é **Θ(n)**, mas rara o suficiente para que a média de muitos push permaneça constante).

(R)`push(x)`** (backing de array) — escreva no índice **`size`**, então **`size++`**. Não há mudança quando a parte superior fica na parte de trás.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 124" role="img" aria-label="Array push writes at index size then increments size">
  <defs>
    <marker id="arr-push-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Before push(7) — size = 2</text>
  <text x="18" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">0</text>
  <text x="54" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">1</text>
  <text x="90" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">2</text>
  <text x="126" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">3</text>
  <rect x="14" y="52" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="26" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <rect x="54" y="52" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="64" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">3</text>
  <rect x="94" y="52" width="36" height="28" rx="3" fill="rgba(96,165,250,0.15)" stroke="#60a5fa" stroke-dasharray="4 3"/>
  <text x="106" y="70" fill="#60a5fa" font-size="10" font-weight="600">?</text>
  <text x="132" y="70" fill="#60a5fa" font-size="9" font-weight="600">← index size</text>
  <path d="M168 66 H220" stroke="#60a5fa" stroke-width="2" marker-end="url(#arr-push-mk)"/>
  <text x="176" y="60" fill="#60a5fa" font-size="10" font-weight="600">write 7</text>
  <text x="232" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After — size = 3</text>
  <text x="240" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">0</text>
  <text x="276" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">1</text>
  <text x="312" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">2</text>
  <text x="348" y="46" fill="#71717a" font-size="8" font-family="ui-monospace">3</text>
  <rect x="236" y="52" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="248" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <rect x="276" y="52" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="286" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">3</text>
  <rect x="316" y="52" width="36" height="28" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="328" y="70" fill="#e4e4e7" font-size="11" font-family="ui-monospace">7</text>
  <text x="360" y="70" fill="#86efac" font-size="9" font-weight="600">← top (size−1)</text>
  <text x="10" y="108" fill="#71717a" font-size="9">Resize copies everything only when capacity is exceeded — usual push stays O(1) amortized.</text>
</svg></figure>

(R)`pop()`** (suporte de array) - leia **`arr[size - 1]`**, então diminua **`size`**; o slot acima do novo topo ainda pode manter um valor obsoleto até ser substituído ou limpo.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 118" role="img" aria-label="Array pop reads top index then decrements size">
  <defs>
    <marker id="arr-pop-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Before pop() — size = 3</text>
  <text x="18" y="44" fill="#71717a" font-size="8" font-family="ui-monospace">0</text>
  <text x="54" y="44" fill="#71717a" font-size="8" font-family="ui-monospace">1</text>
  <text x="90" y="44" fill="#71717a" font-size="8" font-family="ui-monospace">2</text>
  <rect x="14" y="50" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="26" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <rect x="54" y="50" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="64" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">3</text>
  <rect x="94" y="50" width="36" height="28" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="106" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">7</text>
  <text x="138" y="68" fill="#86efac" font-size="9" font-weight="600">read &amp; return</text>
  <path d="M168 64 H220" stroke="#a1a1aa" stroke-width="2" marker-end="url(#arr-pop-mk)"/>
  <text x="176" y="58" fill="#fbbf24" font-size="10" font-weight="600">size−−</text>
  <text x="232" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">After — size = 2</text>
  <text x="240" y="44" fill="#71717a" font-size="8" font-family="ui-monospace">0</text>
  <text x="276" y="44" fill="#71717a" font-size="8" font-family="ui-monospace">1</text>
  <text x="312" y="44" fill="#71717a" font-size="8" font-family="ui-monospace">2</text>
  <rect x="236" y="50" width="36" height="28" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="248" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">3</text>
  <rect x="276" y="50" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="286" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <rect x="316" y="50" width="36" height="28" rx="3" fill="rgba(24,24,27,0.45)" stroke="#52525b" stroke-dasharray="3 3"/>
  <text x="326" y="68" fill="#71717a" font-size="9" font-family="ui-monospace">7?</text>
  <text x="360" y="68" fill="#71717a" font-size="9">stale / optional clear</text>
</svg></figure>

### Java: pilha apoiada por array com crescimento

**Top** em **`size - 1`**; próximo **`push`** escreve **`data[size]`** então **`size++`**. Sobre **`pop`**, retornar **`data[size - 1]`**, **`size--`**, e **`null`** fora do espaço que você deixou para que as referências não sejam retidas (corresponde à discussão “dados confidenciais / GC” abaixo).

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.NoSuchElementException;
import java.util.Objects;

public class ArrayStack<E> {

  private Object[] data;
  private int size;

  public ArrayStack() {
    this.data = new Object[8];
  }

  public void push(E item) {
    Objects.requireNonNull(item, "item");
    if (size == data.length) {
      data = Arrays.copyOf(data, data.length * 2);
    }
    data[size++] = item;
  }

  @SuppressWarnings("unchecked")
  public E pop() {
    if (size == 0) {
      throw new NoSuchElementException();
    }
    int i = --size;
    E out = (E) data[i];
    data[i] = null;
    return out;
  }

  @SuppressWarnings("unchecked")
  public E peek() {
    if (size == 0) {
      throw new NoSuchElementException();
    }
    return (E) data[size - 1];
  }

  public boolean isEmpty() {
    return size == 0;
  }

  public int size() {
    return size;
  }

  /** Θ(n): null used slots so references are dropped (see clearing notes for array-backed stacks below). */
  public void clear() {
    Arrays.fill(data, 0, size, null);
    size = 0;
  }
}
```

### Limpando uma pilha baseada em array
- ** Apenas`size = 0`:** rápido, mas referências antigas ainda podem ficar em slots não utilizados; em **Java** e tempos de execução semelhantes, os objetos podem **não** se tornar colecionáveis ​​até que as referências sejam descartadas – problemático para dados **confidenciais**.  
- **Defina todos os slots antigos para`null`:** seguro para referências, mas **Θ(n)** para limpar.  
- **Compromisso comum:**`size = 0`**e** substitua o array de apoio por um **array vazio novo** (ou reduza) para que o bloco antigo possa ser descartado - **Θ(1)** atribuição de uma nova referência de array; GC recupera o armazenamento antigo quando seguro.


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 108" role="img" aria-label="Array backed stack top at index size minus one">
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Array backing — top at size − 1</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">push at index size · pop reads size−1 then size−−</text>
  <text x="20" y="62" fill="#71717a" font-size="8" font-family="ui-monospace">0</text>
  <text x="56" y="62" fill="#71717a" font-size="8" font-family="ui-monospace">1</text>
  <text x="92" y="62" fill="#71717a" font-size="8" font-family="ui-monospace">2</text>
  <text x="128" y="62" fill="#71717a" font-size="8" font-family="ui-monospace">3</text>
  <rect x="16" y="68" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="28" y="86" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <rect x="56" y="68" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="66" y="86" fill="#e4e4e7" font-size="10" font-family="ui-monospace">3₁</text>
  <rect x="96" y="68" width="36" height="28" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="106" y="86" fill="#e4e4e7" font-size="10" font-family="ui-monospace">3₂</text>
  <rect x="136" y="68" width="36" height="28" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="148" y="86" fill="#e4e4e7" font-size="11" font-family="ui-monospace">2</text>
  <text x="188" y="86" fill="#86efac" font-size="9" font-weight="600">← top (size−1)</text>
  <text x="188" y="62" fill="#60a5fa" font-size="9" font-weight="600">size = 4</text>
  <text x="260" y="86" fill="#71717a" font-size="9">next push at index 4</text>
</svg></figure>


## 4. Java:`Deque`,`ArrayDeque`e o legado`Stack`aula

A **estrutura de coleções** modela uma pilha como **`Deque<E>`** (fila dupla) usada em **apenas uma extremidade**. Prefira **`Deque`** implementações em relação ao antigo **`java.util.Stack`** tipo.

### Prefira`Deque`+`ArrayDeque`para uma pilha

(R)`ArrayDeque<E>`** é um **buffer de anel redimensionável** (como a fila circular nestas notas): **`push`-&#09;o`pop`-&#09;o`peek`** são **amortizados O(1)** sem **sem boxe por elemento** de nós (ao contrário de um vinculado`Deque`construído a partir de`LinkedList`entradas). É o padrão usual para uma pilha de **threaded único** ou fila de trabalho.

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.Deque;

Deque<String> stack = new ArrayDeque<>();
stack.push("a");       // same contract as addFirst
stack.push("b");
String top = stack.peek();   // "b" — empty deque ⇒ null (not an exception)
String out = stack.pop();    // "b" — empty ⇒ NoSuchElementException
```

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 218" role="img" aria-label="Java Deque stack methods operate at the front left to right">
  <text x="10" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Deque used as a stack — front = top (left → right is deque order)</text>
  <text x="10" y="36" fill="#a1a1aa" font-size="10">After push(&quot;a&quot;) then push(&quot;b&quot;)</text>
  <text x="10" y="56" fill="#86efac" font-size="9" font-weight="600">front / top →</text>
  <rect x="88" y="48" width="44" height="32" rx="6" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="102" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">&quot;b&quot;</text>
  <rect x="140" y="48" width="44" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="152" y="68" fill="#e4e4e7" font-size="11" font-family="ui-monospace">&quot;a&quot;</text>
  <path d="M200 64 H248" stroke="#fbbf24" stroke-width="2" fill="none"/>
  <text x="208" y="58" fill="#fbbf24" font-size="10" font-weight="600">peek()</text>
  <text x="256" y="68" fill="#fbbf24" font-size="10" font-family="ui-monospace">→ &quot;b&quot;</text>
  <text x="10" y="104" fill="#a1a1aa" font-size="10">peek() leaves order unchanged</text>
  <text x="10" y="122" fill="#86efac" font-size="9" font-weight="600">front / top →</text>
  <rect x="88" y="114" width="44" height="32" rx="6" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="102" y="134" fill="#e4e4e7" font-size="11" font-family="ui-monospace">&quot;b&quot;</text>
  <rect x="140" y="114" width="44" height="32" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="152" y="134" fill="#e4e4e7" font-size="11" font-family="ui-monospace">&quot;a&quot;</text>
  <path d="M200 130 H248" stroke="#a1a1aa" stroke-width="2" fill="none"/>
  <text x="208" y="124" fill="#fbbf24" font-size="10" font-weight="600">pop()</text>
  <text x="256" y="134" fill="#fbbf24" font-size="10" font-family="ui-monospace">→ &quot;b&quot;</text>
  <text x="10" y="170" fill="#a1a1aa" font-size="10">After pop() — only &quot;a&quot; remains at the front</text>
  <text x="10" y="188" fill="#86efac" font-size="9" font-weight="600">front / top →</text>
  <rect x="88" y="180" width="44" height="32" rx="6" fill="rgba(34,197,94,0.25)" stroke="#86efac" stroke-width="2"/>
  <text x="100" y="200" fill="#e4e4e7" font-size="11" font-family="ui-monospace">&quot;a&quot;</text>
  <text x="320" y="130" fill="#71717a" font-size="10">Same ADT as §1; API pins “top” to</text>
  <text x="320" y="144" fill="#71717a" font-size="10">the deque’s head, not index size−1.</text>
</svg></figure>

Sobre **`Deque`**, a **pilha** mapas de nomenclatura como este (veja`Deque`Javadoc): **`push(e)`** ≡ **`addFirst(e)`**, **`pop()`** ≡ **`removeFirst()`**, **`peek()`** ≡ **`peekFirst()`**. Portanto, o **topo** da pilha é a **frente** do deque - a mesma ideia “mais recente em uma extremidade” que uma pilha **baseada na cabeça** unida individualmente em §2, não a “parte traseira em`size−1`”imagem em §3 (ambas são realizações ADT válidas; API de Java apenas escolheu a **frente** para`push`).

### Por que evitar`java.util.Stack`'ca?

(R)`Stack`** estende **`Vector`** (um array expansível de Java 1.0). Problemas no código moderno:

- **Sincronizado em todos os métodos públicos** — você paga pelo bloqueio mesmo quando apenas um thread o utiliza.
- **`Stack`não é uma interface** — mais difícil de trocar implementações ou simular em testes.
- Design é **legado**; a biblioteca e a orientação do estilo **Effective Java** dizem: **use`Deque`**.

Se você realmente precisa de uma pilha **thread-safe**, use **`ConcurrentLinkedDeque`** (sem bloqueio, ilimitado) ou embrulhe um **`Deque`** com **`Collections.synchronizedDeque`**, ou um **`BlockingDeque`** quando os produtores/consumidores devem bloquear - não`Stack`.

###`peek`contra`element`,`remove`contra`poll`

(R)`Deque`** herda **`Queue`** métodos com comportamento **vazio** ligeiramente diferente:

| Intenção | Uso típico de pilha | Em vazio`Deque`|
|--------|-------------------|-------------------|
| Leia o topo sem remover | **`peek()`** / **`peekFirst()`** | retorna **`null`** |
| Leia o topo (mais rigoroso) | **`element()`** | arremessos **`NoSuchElementException`** |
| Pop | **`pop()`** / **`removeFirst()`** | arremessos **`NoSuchElementException`** |
| Tolerante ao pop | **`pollFirst()`** | retorna **`null`** |

Escolher **`peek`-&#09;o`poll`** quando o vazio é normal; usar **`element`-&#09;o`remove`** quando vazio significa um bug.

**Empty-safe pop** (sem exceção quando a pilha já pode estar esgotada):

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.Deque;

Deque<String> stack = new ArrayDeque<>();
String topOrNull = stack.pollFirst(); // null if empty — same end as pop()
```

###`ArrayDeque`regras e limites

- **`null`não é permitido** —`push(null)`arremessos **`NullPointerException`**. Um **`LinkedList`** usado como **`Deque`** ainda pode aceitar **`null`**em padrões mais antigos, mas misturando**`null`** elementos com **`peek()`** é uma má ideia - **`peek()`** já retorna **`null`** quando o deque está **vazio**.
- **Sem acesso aleatório** —`ArrayDeque`não é um **`List`**; não o trate como um array com índices.
- **A ordem do iterador** é **frente → trás** (o mesmo que da esquerda para a direita no`Deque`contrato), **não** “fazer pedido até que você o drene” como um modo especial — para uma pilha pura você apenas **`push`-&#09;o`pop`-&#09;o`peek`** de uma extremidade.

### JVM`StackOverflowError`(colisão de nomes)

(R)`StackOverflowError`** é lançado quando uma **pilha de chamadas de thread** (quadros de ativação para chamadas de métodos aninhados) cresce muito profundamente — recursão sem caso base ou cadeias muito profundas. Não está relacionado ** com **`java.util.Stack`**tipo de coleção; apenas a palavra “pilha” é compartilhada.

## 5. Resumo

| | **Vinculado individualmente (head = top)** | **Matriz (atrás = topo)** |
|--|------------------------------------------|------------------------|
| **empurrar** | Θ(1) preceder | amortizado Θ(1); raro Θ(n) redimensionar |
| **pop** | Θ(1) separar cabeça | Θ(1) em`size-1`|
| **espiar / esvaziar / tamanho** | Θ(1) | Θ(1) |
| **claro** | Θ(1)`head=null`(+ GC / grátis) | Θ(1) elimina a referência para um novo array vazio ou Θ(n) slots nulos |
| **Extra** | não é necessária cauda | disciplina de índice; dados confidenciais ⇒ mente em slots obsoletos |

Ambos realizam a **mesma pilha ADT**; escolha com base em **tolerância de alocação**, **comportamento de cache** e detalhes de **idioma/tempo de execução** (por exemplo, limpeza de referência). Em **Java**, prefira **`Deque<E>`** com **`ArrayDeque<E>`** para uma pilha padrão (§4); evitar **`java.util.Stack`**.

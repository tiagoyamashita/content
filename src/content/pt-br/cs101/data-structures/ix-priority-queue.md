---
label: "IX"
subtitle: "Fila prioritária"
group: "Estruturas de dados e algoritmos"
order: 9
---
Fila prioritária – “quem é o próximo?” por importância, não por hora de chegada
Uma **fila de prioridade** é um **tipo de dados abstrato** para uma coleção onde cada item tem uma **prioridade** (geralmente apenas um número ou qualquer coisa **comparável**). O comportamento definidor: você pode **inserir** em qualquer ordem, mas **extrair** sempre remove o item com a prioridade **mais alta** ou **mais baixa** entre aqueles que ainda estão dentro — **não** o mais antigo (isso seria uma fila **FIFO**) e **não** o mais novo (que seria uma **pilha**).

**Java linha de base:**`PriorityQueue`trechos assumem **Java SE 22** (`javac --release 22`). Eles usam **`record`** e outros recursos disponíveis desde **Java 16**; eles também são executados em **JDK 21 LTS**.

Se você imaginar um balcão de **triagem hospitalar**: as chegadas não são atendidas estritamente por ordem de chegada; o caso **mais urgente** avança. Uma **fila** normal é uma única linha ordenada; uma **fila prioritária** é “sempre atender quem é mais importante no momento”.


## 1. Fila vs pilha vs fila prioritária (um minuto)

| ADT | Quem sai em “remover melhor” ou desenfileirar/pop? | Modelo mental típico |
|-----|----------------------------------------------------------|---------------------|
| **Fila** | O **mais antigo** ainda está esperando (**FIFO**) | Fila em uma loja |
| **Pilha** | O **mais novo** ainda está lá (**LIFO**) | Pilha de pratos |
| **Fila prioritária** | A chave **menor** ou **maior** ainda existe (de acordo com sua regra de pedido) | Triagem, agendamento CPU |

**Peek** (ou **find-min** / **find-max**) lê o mesmo “melhor” elemento **sem** removê-lo. **Inserir** adiciona algo com prioridade própria; ela **não** precisa ficar na “frente” de nada — a estrutura mantém o invariante internamente.


## 2. Operações (o que APIs geralmente expõem)

Os nomes variam de acordo com o idioma e o livro didático; mapeie-os mentalmente assim:

- **`insert(x)`** / **`add(x)`** / **`offer(x)`** - colocar`x`na coleção.
- **`extract-min()`** ou **`extract-max()`** — remove e retorna o melhor elemento na ordem da fila. Em uma estrutura **vazia**, o comportamento é **error** ou um valor **sentinel** (Java’s`poll()`retorna **`null`** para vazio).
- **`peek-min()`** / **`peek-max()`** — retorna o melhor elemento **sem** removê-lo (Java: **`peek()`**).
- **`isEmpty()`**, **`size()`** — escrituração contábil habitual.
- **`clear()`** - largue tudo.

**Opcional (avançado):** **`decrease-key`** / **`increase-key`** quando você já tem um **handle** para um item dentro da estrutura e sua prioridade muda — necessário para uma implementação rápida do caminho mais curto **Dijkstra** com um **heap binário** que pode atualizar prioridades. O padrão **`java.util.PriorityQueue`** **não** oferece suporte a teclas de diminuição eficientes em elementos arbitrários; para isso, você usa um padrão **heap indexado**, um **heap Fibonacci** em configurações com muita teoria ou outra biblioteca de gráficos.

**Merge** (combinar duas filas de prioridade) aparece em alguns APIs teóricos; o código prático geralmente é apenas inserido de um heap em outro.


## 3. Heap mínimo vs heap máximo (mesma ideia, ordem invertida)

- **Fila de prioridade mínima:** “melhor” = **menor** chave. **Extrair** = **extrair-min**. Usado para **Dijkstra** (menor distância provisória primeiro), **Prim** em gráficos, **mesclando fluxos classificados** com um pequeno monte de “cabeças atuais”.
- **Fila de prioridade máxima:** “melhor” = **maior** chave. Usado para problemas de estilo “top **k**”, **heapsort** descendente, construções de estilo **Huffman** onde você pega repetidamente os dois **maiores** (dependendo da formulação).

Em termos de implementação, um **min-heap** é uma árvore binária completa onde cada pai é **≤** seus filhos; um **max-heap** muda para **≥**. Uma implementação pode fazer as duas coisas trocando a comparação ou usando um **comparador reverso** em Java.


## 4. Desempate e “prioridades duplicadas”

Se dois itens têm a **mesma** prioridade numérica, o ADT geralmente **não** garante qual deles sai primeiro, a menos que a implementação documente a **estabilidade de FIFO** dentro de chaves iguais (muitos heaps **não** são estáveis). Se a ordem entre iguais é importante, soluções comuns:

- Leve uma **chave secundária** (ex.`(priority, sequenceNumber)`com comparação lexicográfica para que as entradas mais antigas sejam classificadas primeiro entre os empates), ou
- Armazene **ids exclusivos** e rompa vínculos explicitamente em um **`Comparator`**.


## 5. Implementações e prazos

Idéias ingênuas:

- **Matriz ou lista não classificada:** **inserir** **O(1)** (acrescentar), mas **extrair-min** verifica tudo — **O(n)**.
- **Matriz classificada:** **extrair-min** de uma extremidade **O(1)**, mas **inserir** pode mudar — **O(n)** no pior caso.

O ponto ideal usual para uma fila de prioridade mutável geral é um **heap binário** (veja **heap binário** neste submenu, [heap binário](viii-binary-heap.md)): armazene uma **árvore binária completa** em um array, restaure a **ordem do heap** após cada inserção (**bubble up** / **swim**) e após cada extração (**sink down** / **sift**). A altura é **O(log n)**, então:

| Operação | Pilha binária (típica) |
|-----------|-------------|
| **inserir** | **O(logn)** |
| **espiar** melhor | **O(1)** |
| **extrair** melhor | **O(logn)** |
| **construir** a partir de chaves **n** (de baixo para cima) | **O(n)** — melhor que **n** inserções separadas |

** Montes de Fibonacci ** e amigos melhoram alguns limites ** amortizados ** para algoritmos gráficos especializados em teoria; nas bibliotecas do dia-a-dia você ainda vê **heaps binários** primeiro.

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 212" role="img" aria-label="Min heap before extract min and after moving last leaf to root and sinking down">
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


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 120" role="img" aria-label="FIFO queue front versus priority queue always smallest at root">
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


## 6. Java`PriorityQueue`

(R)`java.util.PriorityQueue<E>`** é um **min-heap** quando os elementos usam **ordenação natural** (`Comparable`) ou um heap ordenado por um ** explícito`Comparator`**. **não é seguro para threads**. A ordem do iterador **não** é “ordem de prioridade”; usar **`poll()`** em um loop para drenar na ordem de classificação.

**Pilha mínima de números inteiros** (menor`poll`primeiro):

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

**Max-heap** (o maior primeiro): inverta a comparação.

```java
// Compile: javac --release 22 …
import java.util.Collections;
import java.util.PriorityQueue;

PriorityQueue<Integer> maxPq = new PriorityQueue<>(Collections.reverseOrder());
maxPq.offer(10);
maxPq.offer(30);
maxPq.peek();  // 30
```

**Tipo personalizado** (por exemplo, trabalhos com prazos — **prazo anterior = prioridade mais alta** aqui, pois números inteiros menores vencem):

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

(Você pode usar um`class`com **`Comparable`** ou passe **`Comparator.comparingInt(Job::deadline)`** para o **`PriorityQueue`** construtor — mesma ordem.)

**Esvazio-seguro:** **`poll()`** e **`peek()`** retornar **`null`** quando vazio; **`remove()`** lança **`NoSuchElementException`**.

**Pegadinhas**

- **`null`** elementos **não** são permitidos.
- Se você alterar um campo que participa da ordenação **após** inserir um objeto, o heap **não** será reordenado automaticamente — você deverá **remover e inserir novamente** ou usar uma estrutura projetada para **tecla de diminuição**.
- A capacidade inicial é apenas uma **dica**; a pilha cresce conforme necessário.


## 7. Onde aparecem as filas prioritárias

- **Algoritmos de gráfico:** **Dijkstra** (vértice não visitado mais próximo primeiro), **Prim** (borda mais barata para a árvore em crescimento), **A-star** (`A*`) pesquisa com uma heurística.
- **CPU / OS agendamento:** escolha o próximo processo executável por prioridade (agendadores reais adicionam justiça, envelhecimento, etc.).
- **Simulação de eventos discretos:** o próximo evento é aquele com o tempo **mínimo** simulado.
- **Streaming “top k”:** mantenha um heap máximo de **tamanho k** enquanto verifica os valores (veja o padrão de heap máximo acima).
- **Mesclar k listas/arquivos classificados:** uma entrada de heap por lista`(nextValue, listId)`; repetidamente **pesquisar** o menor e avançar nessa lista.


## 8. Notas relacionadas

- **Pilha binária** neste submenu [Pilha binária](viii-binary-heap.md) — layout de array, fórmulas de índice, **buildHeap**, **heapsort**.
- **Fila** [Fila](v-queue.md) — estrito **FIFO**; nenhuma prioridade por item, a menos que você simule mal.
- Visão geral do **Nível II**:`ii-trees-heaps-hashing.md`(se presente em seu currículo).

Quando você estiver confortável com “insira em qualquer lugar, sempre pegue o melhor”, a nota heap é o próximo passo natural: é o **maquinário** padrão por trás deste ADT.

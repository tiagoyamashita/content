---
label: "XI"
subtitle: "Resolvendo com o JDK"
group: "Estruturas de dados e algoritmos"
order: 11
---
Resolvendo problemas de algoritmo com JDK
Nos cursos, você implementa algoritmos manualmente para aprender **como** eles funcionam. Em **Java** real, você compõe tipos **já implementados** de **`java.util`** e **`java.util.Arrays`** — os mesmos ADTs do submenu **Estruturas de dados**, conectados para produção.

**Java linha de base:** **Java SE 22** (`javac --release 22`); também está bem em **JDK 21 LTS**.

## 1. Mentalidade

| Meta | Enrolado à mão (aprendizagem) | JDK (código de envio) |
|------|------------------------|---------------------|
| Classificar uma matriz | mesclar/classificação rápida |`Arrays.sort`,`List.sort`|
| Encontre em dados classificados | loop de pesquisa binária |`Arrays.binarySearch`|
| Encontre / conte rapidamente | varredura linear |`HashMap`,`HashSet`|
| FIFO passagem | classe de fila vinculada |`ArrayDeque`+`Queue`|
| Melhor próximo (Dijkstra, Prim) | código de peneiração de heap |`PriorityQueue`|
| Acessibilidade do gráfico | BFS/DFS ciclos |`ArrayDeque`+ lista de adjacências que você constrói |

O **JDK não** envia um`Graph`classe com Dijkstra ou MST integrado - você ainda escreve **loops curtos**, mas **reutiliza** filas, heaps, mapas e classificações em vez de reimplementá-los.

## 2. Folha de dicas: problema → API

| Tipo de problema | Ferramentas primárias JDK |
|--------------|-------------------|
| Chaves de classificação |`Arrays.sort`,`Collections.sort`,`Comparator`|
| Pesquisar matriz ordenada |`Arrays.binarySearch`,`Collections.binarySearch`|
| Pesquisa/desduplicação |`HashMap`,`HashSet`,`Map.computeIfAbsent`|
| Fila (BFS) |`ArrayDeque`,`Queue.offer`-&#09;o`poll`|
| Pilha (DFS iterativa) |`ArrayDeque`como`Deque`,`push`-&#09;o`pop`|
| Mín/máx próximo |`PriorityQueue`(min-heap por padrão) |
| Top-k maiores |`PriorityQueue`(tamanho mínimo de heap k) ou`stream().sorted().limit(k)`|
| Objetos de classificação estável |`Arrays.sort(Object[])`(TimSort) |
| Mesclar intervalos |`Arrays.sort`por iniciar + digitalizar |
| Frequências de contagem |`HashMap.merge`,`getOrDefault`|
| Consultas de soma de intervalo | matriz de prefixo (manual) ou`long[]`+ laços |
| Permutações/subconjuntos (n pequeno) | retroceda; opcional`Stream`ajudantes |

## 3. Classificando e pesquisando

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

int[] nums = { 3, 1, 4, 1, 5 };
Arrays.sort(nums);

List<String> names = List.of("bob", "ada", "grace");
List<String> sorted = names.stream().sorted().toList();
// or mutate a copy:
List<String> copy = new java.util.ArrayList<>(names);
Collections.sort(copy);

record Job(int deadline, String name) {}
Job[] jobs = { new Job(5, "a"), new Job(2, "b") };
Arrays.sort(jobs, Comparator.comparingInt(Job::deadline));

int idx = Arrays.binarySearch(nums, 4); // >= 0 if found
```

(R)`Arrays.binarySearch`** retorna **≥ 0** se encontrado, caso contrário **`-(insertionPoint) - 1`**. A matriz deve ser **classificada** primeiro.

## 4. Mapas e conjuntos

```java
// Compile: javac --release 22 …
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

Map<String, Integer> freq = new HashMap<>();
for (String word : words) {
  freq.merge(word, 1, Integer::sum);
}

Set<Integer> seen = new HashSet<>();
if (seen.add(x)) {
  // first time we saw x
}
```

## 5. Filas, pilhas, heaps (gráficos e gananciosos)

```java
// Compile: javac --release 22 …
import java.util.ArrayDeque;
import java.util.PriorityQueue;
import java.util.Queue;

// BFS
Queue<Integer> q = new ArrayDeque<>();
q.offer(start);

// Dijkstra-style (non-negative weights) — see vi-shortest-paths-and-mst.md
PriorityQueue<int[]> pq = new PriorityQueue<>(
    (a, b) -> Integer.compare(a[1], b[1]));
pq.offer(new int[] { source, 0 });

// Top-k largest: keep min-heap of size k
PriorityQueue<Integer> heap = new PriorityQueue<>();
for (int x : nums) {
  heap.offer(x);
  if (heap.size() > k) {
    heap.poll();
  }
}
```

## 6. Utilitários de coleções

```java
// Compile: javac --release 22 …
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

int max = Collections.max(List.of(3, 1, 4));
Collections.reverse(Arrays.asList(boxed)); // array as list view
Collections.swap(list, i, j);
int freq = Collections.frequency(list, target);
```

## 7. Streams (opcional, mesma classe de complexidade)

Use quando a legibilidade vencer; conheça o algoritmo subjacente (a classificação é **O(n log n)**).

```java
// Compile: javac --release 22 …
import java.util.Arrays;

int[] a = { 3, 1, 4 };
boolean anyEven = Arrays.stream(a).anyMatch(x -> x % 2 == 0);
int sum = Arrays.stream(a).sum();
int[] sorted = Arrays.stream(a).sorted().toArray();
```

## 8. O que você ainda implementa

- **Armazenamento de gráficos** (lista/matriz de adjacências).
- **BFS / DFS / Dijkstra / MST** loops de controle (usando filas/heaps JDK).
- **DP** preenchimento de tabela (arrays + loops, às vezes`HashMap`teclas de memorando).
- **Recuo** recursão com escolha/desmarcação.

## 9. Indicadores por tópico

| Nota | JDK foco |
|------|-----------|
| [Classificando](ii-sorting.md) |`Arrays.sort`,`Comparator`|
| [Pesquisando](iii-searching.md) |`binarySearch`,`HashMap`|
| [Percurso do gráfico](v-graph-traversal.md) |`ArrayDeque`,`Queue`|
| [Caminhos mais curtos & MST](vi-shortest-paths-and-mst.md) |`PriorityQueue`, classifique as arestas para Kruskal |
| [Ambicioso](vii-greedy.md) | classificar +`PriorityQueue`|
| [Programação dinâmica](viii-dynamic-programming.md) |`int[][]`,`HashMap`memorando |
| [Padrões comuns](x-common-patterns.md) |`HashMap`,`Arrays.sort`, fluxos |

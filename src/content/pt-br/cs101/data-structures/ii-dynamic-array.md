---
label: "II"
subtitle: "Matriz dinâmica"
group: "Estruturas de dados e algoritmos"
order: 2
---
Matriz dinâmica (vetor)
Buffer contíguo expansível com acréscimo eficiente.

### O que acontece em Java quando você envia para um array de tamanho fixo ou array dinâmico?

#### Matriz de tamanho fixo (`int[] arr = new int[4];`)

Em Java, se você usar um array de tamanho fixo, o tamanho será determinado na criação e **não poderá ser alterado**.  
- Se você tentar atribuir um valor além do último índice válido (por exemplo,`arr[4] = 42`para array de comprimento 4), Java lançará um **`ArrayIndexOutOfBoundsException`** em tempo de execução.
- **Não há redimensionamento, cópia ou crescimento automático**. O tamanho do array é fixo e você deve criar manualmente um novo array (maior) e copiar os elementos você mesmo se quiser "estendê-lo".

#### Matriz Dinâmica (`ArrayList<E>`)

Java fornece o`ArrayList<E>`class, que se comporta como um array dinâmico:
- Quando você liga`add(e)`e a matriz subjacente *não* está cheia (`size < capacity`), Java insere o elemento no próximo slot (**O(1)** tempo).
- Se você ligar`add(e)`quando a matriz interna *está* cheia (`size == capacity`), Java faz o seguinte:
  1. **Aloca** um array interno novo e maior (por padrão, a capacidade aumenta aproximadamente 50% em Java 8+).
  2. **Copia** todos os elementos existentes no novo array.
  3. **Libera** o array antigo (para coleta de lixo).
  4. **Acrescenta** o novo elemento.
- A etapa de redimensionamento e cópia é *cara* (`O(n)`para n elementos), mas como isso acontece com pouca frequência, o tempo médio por`add`permanece **amortizado O(1)**.

#### Casos extremos (Java)

- **Capacidade inicial zero:** Se você criar um`ArrayList`sem capacidade inicial e adicionada imediatamente, a lista deverá alocar armazenamento na primeira adição.
- **Adições repetidas:** Se você enviar muitos itens em um curto espaço de tempo, Java poderá realocar e copiar várias vezes consecutivas, dependendo da política de crescimento.
- **Tamanho máximo do array:** Java arrays têm um tamanho máximo (`Integer.MAX_VALUE`). Tentar superar isso lança um`OutOfMemoryError`.
- **Adição em massa (`addAll`):** Adicionar muitos elementos de uma vez pode acionar o redimensionamento imediato para caber em todos os novos itens.

#### O que *não* acontece (Java)

- Para **matrizes de tamanho fixo**, empurrar ("adicionar capacidade anterior") nunca é redimensionado — eles lançam exceções.
- Para`ArrayList`, Java lida com redimensionamentos automaticamente, mas à custa de tempo e ocasionalmente acionando uma pausa na coleta de lixo devido a grandes alocações de memória.
- Para políticas personalizadas (por exemplo, sempre redimensionando +1 a cada adição), o desempenho pode ser degradado para quadrático — o padrão de Java é mais eficiente.

###

- **Operações típicas:**`get`-&#09;o`set`no índice (**O(1)**);`add`para finalizar a amortização **O(1)**; inserir/remover no meio **O(n)** por causa da mudança.
- **Espaço:** Θ(n) para`n`elementos; a capacidade interna real pode ser maior (devido ao redimensionamento, normalmente entre n e cerca de 1,5n).

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 132" role="img" aria-label="Dynamic array doubles capacity and copies elements when full">
  <defs>
    <marker id="ds-dyn-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">size = capacity → grow (ArrayList)</text>
  <text x="12" y="38" fill="#a1a1aa" font-size="10">four slots full (capacity 4); next add allocates new block (e.g., capacity 6), copies, frees old</text>
  <text x="12" y="58" fill="#86efac" font-size="9" font-weight="600">before</text>
  <rect x="16" y="64" width="72" height="26" rx="3" fill="rgba(34,197,94,0.28)" stroke="#86efac"/>
  <rect x="92" y="64" width="72" height="26" rx="3" fill="rgba(34,197,94,0.28)" stroke="#86efac"/>
  <rect x="168" y="64" width="72" height="26" rx="3" fill="rgba(34,197,94,0.28)" stroke="#86efac"/>
  <rect x="244" y="64" width="72" height="26" rx="3" fill="rgba(34,197,94,0.28)" stroke="#86efac"/>
  <text x="12" y="108" fill="#60a5fa" font-size="9" font-weight="600">after</text>
  <rect x="16" y="98" width="48" height="22" rx="3" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <rect x="68" y="98" width="48" height="22" rx="3" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <rect x="120" y="98" width="48" height="22" rx="3" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <rect x="172" y="98" width="48" height="22" rx="3" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <rect x="224" y="98" width="48" height="22" rx="3" fill="none" stroke="#71717a" stroke-dasharray="4 3"/>
  <rect x="276" y="98" width="48" height="22" rx="3" fill="none" stroke="#71717a" stroke-dasharray="4 3"/>
  <rect x="328" y="98" width="48" height="22" rx="3" fill="none" stroke="#71717a" stroke-dasharray="4 3"/>
  <rect x="380" y="98" width="48" height="22" rx="3" fill="none" stroke="#71717a" stroke-dasharray="4 3"/>
  <path d="M280 76 L280 92" stroke="#a1a1aa" stroke-width="1.5" marker-end="url(#ds-dyn-mk)"/>
  <text x="288" y="88" fill="#71717a" font-size="9">copy + spare room</text>
</svg></figure>

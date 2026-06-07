---
label: "I"
subtitle: "配列"
group: "データ構造とアルゴリズム"
order: 1
---
配列（静的）

RAM モデルの連続インデックス付きストレージ。

**配列** は、要素を連続したメモリ ワードに格納します。 Java では、配列を宣言するときは、常にそのサイズを明示的に指定する必要があります (たとえば、`int[] arr = new int[5];`）。 Java の配列には**デフォルトのサイズはありません**。単に次のように記述する場合`int[] arr;`、変数`arr`null を指すだけで、実際には配列は割り当てられません。必ず使用してください`new`そして正確な長さを提供します。 Java 配列の長さは、作成後に変更することはできません。

索引`i`到達する`A[i]`標準 RAM モデルでは **O(1)** 時間です。アドレスは次のとおりです。`base + i × wordSize`。

- **長所:** ランダム アクセス、キャッシュに優しいスキャン、シンプルなレイアウト。
- **制限:** 固定長 (静的配列)。中央に挿入するには、インデックスの密度を保つために **O(n)** 要素をシフトする必要があります。
- **関連:** 拡張可能なベクトルについては、このサブメニューの **動的配列** を参照してください。完全な複雑さと ADT コンテキストは **レベル I — 基礎** [基礎](../i-foundations.md）。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 200" role="img" aria-label="Array index maps to contiguous memory; middle insert shifts elements right">
  <defs>
    <marker id="ds-arr-mk" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7 Z" fill="#86efac"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">O(1) index access</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">base address + i × stride → element A[i]</text>
  <text x="32" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">0</text>
  <text x="92" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">1</text>
  <text x="152" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">2</text>
  <text x="212" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">3</text>
  <rect x="16" y="84" width="56" height="32" rx="4" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <rect x="76" y="84" width="56" height="32" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <rect x="136" y="84" width="56" height="32" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <rect x="196" y="84" width="56" height="32" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="36" y="104" fill="#e4e4e7" font-size="12" font-family="ui-monospace">A</text>
  <text x="96" y="104" fill="#e4e4e7" font-size="12" font-family="ui-monospace">B</text>
  <text x="156" y="104" fill="#e4e4e7" font-size="12" font-family="ui-monospace">C</text>
  <text x="216" y="104" fill="#e4e4e7" font-size="12" font-family="ui-monospace">D</text>
  <path d="M124 100 L124 52" stroke="#86efac" stroke-width="1.5" stroke-dasharray="4 3"/>
  <text x="132" y="48" fill="#86efac" font-size="10" font-weight="600">read A[1] in O(1)</text>
  <text x="12" y="138" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Middle insert → shift right</text>
  <text x="12" y="156" fill="#a1a1aa" font-size="10">insert X at index 1: every element from that slot moves one step</text>
  <rect x="16" y="164" width="56" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="76" y="164" width="56" height="28" rx="4" fill="rgba(251,191,36,0.25)" stroke="#fbbf24" stroke-width="2"/>
  <rect x="136" y="164" width="56" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="196" y="164" width="56" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="256" y="164" width="56" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="96" y="182" fill="#fbbf24" font-size="11" font-family="ui-monospace" font-weight="600">X</text>
  <text x="36" y="182" fill="#e4e4e7" font-size="11" font-family="ui-monospace">A</text>
  <text x="156" y="182" fill="#e4e4e7" font-size="11" font-family="ui-monospace">B</text>
  <text x="216" y="182" fill="#e4e4e7" font-size="11" font-family="ui-monospace">C</text>
  <text x="276" y="182" fill="#e4e4e7" font-size="11" font-family="ui-monospace">D</text>
  <path d="M200 178 H320" stroke="#86efac" stroke-width="1.5" marker-end="url(#ds-arr-mk)"/>
  <text x="300" y="172" fill="#71717a" font-size="9">Θ(n) worst case</text>
</svg></figure>

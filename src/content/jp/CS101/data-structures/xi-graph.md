---
label: "XI"
subtitle: "グラフ"
group: "データ構造とアルゴリズム"
order: 11
---
グラフ






`G = (V, E)`: 頂点とエッジ; **有向**または**無向**。

**隣行列:**`n×n`テーブル;角`(u,v)`クエリ **O(1)**; space **Θ(n²)** — 密なグラフまたは重みの検索に適しています。

**隣接リスト:** 隣接する頂点ごとのリスト。スペース **Θ(n + m)** 用`n = |V|`、`m = |E|`;出力エッジを度数に比例した時間で繰り返します。

**アルゴリズム:** BFS (**キュー**)、DFS (**スタック** または再帰)、トポロジカルソート、SCC、最短パス — **アルゴリズム** サブメニューを参照 ([グラフトラバーサル](../Algorithms/v-graph-traversal.md)、[最短パス & MST](../Algorithms/vi-shortest-paths-and-mst.md)) および **レベル III — グラフ** (`iii-graphs.md`）。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 460 236" role="img" aria-label="Graph vertices with adjacency list versus adjacency matrix">
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Same graph, two storages</text>
  <circle cx="48" cy="72" r="14" fill="rgba(34,197,94,0.2)" stroke="#86efac" stroke-width="2"/>
  <text x="44" y="76" fill="#e4e4e7" font-size="10" font-family="ui-monospace">0</text>
  <circle cx="108" cy="52" r="14" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="104" y="56" fill="#e4e4e7" font-size="10" font-family="ui-monospace">1</text>
  <circle cx="108" cy="96" r="14" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="104" y="100" fill="#e4e4e7" font-size="10" font-family="ui-monospace">2</text>
  <circle cx="168" cy="72" r="14" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="164" y="76" fill="#e4e4e7" font-size="10" font-family="ui-monospace">3</text>
  <line x1="60" y1="68" x2="96" y2="56" stroke="#71717a" stroke-width="2"/>
  <line x1="60" y1="76" x2="96" y2="92" stroke="#71717a" stroke-width="2"/>
  <line x1="120" y1="56" x2="156" y2="68" stroke="#71717a" stroke-width="2"/>
  <line x1="120" y1="92" x2="156" y2="76" stroke="#71717a" stroke-width="2"/>
  <line x1="120" y1="60" x2="120" y2="88" stroke="#71717a" stroke-width="2"/>
  <text x="12" y="128" fill="#86efac" font-size="10" font-weight="600">Adjacency list (outgoing)</text>
  <text x="12" y="146" fill="#a1a1aa" font-size="9" font-family="ui-monospace">0: →1→2</text>
  <text x="12" y="160" fill="#a1a1aa" font-size="9" font-family="ui-monospace">1: →0→2→3</text>
  <text x="12" y="174" fill="#a1a1aa" font-size="9" font-family="ui-monospace">2: →0→1</text>
  <text x="12" y="188" fill="#a1a1aa" font-size="9" font-family="ui-monospace">3: →1</text>
  <text x="240" y="128" fill="#60a5fa" font-size="10" font-weight="600">Adjacency matrix</text>
  <text x="240" y="146" fill="#71717a" font-size="8" font-family="ui-monospace">1 = edge u→v</text>
  <text x="268" y="166" fill="#a1a1aa" font-size="8" font-family="ui-monospace">0</text>
  <text x="292" y="166" fill="#a1a1aa" font-size="8" font-family="ui-monospace">1</text>
  <text x="316" y="166" fill="#a1a1aa" font-size="8" font-family="ui-monospace">2</text>
  <text x="340" y="166" fill="#a1a1aa" font-size="8" font-family="ui-monospace">3</text>
  <text x="244" y="184" fill="#a1a1aa" font-size="8" font-family="ui-monospace">0</text>
  <text x="268" y="184" fill="#e4e4e7" font-size="9" font-family="ui-monospace">0</text>
  <text x="292" y="184" fill="#e4e4e7" font-size="9" font-family="ui-monospace">1</text>
  <text x="316" y="184" fill="#e4e4e7" font-size="9" font-family="ui-monospace">1</text>
  <text x="340" y="184" fill="#e4e4e7" font-size="9" font-family="ui-monospace">0</text>
  <text x="244" y="200" fill="#a1a1aa" font-size="8" font-family="ui-monospace">1</text>
  <text x="268" y="200" fill="#e4e4e7" font-size="9" font-family="ui-monospace">1</text>
  <text x="292" y="200" fill="#e4e4e7" font-size="9" font-family="ui-monospace">0</text>
  <text x="316" y="200" fill="#e4e4e7" font-size="9" font-family="ui-monospace">1</text>
  <text x="340" y="200" fill="#e4e4e7" font-size="9" font-family="ui-monospace">1</text>
  <text x="244" y="216" fill="#a1a1aa" font-size="8" font-family="ui-monospace">2</text>
  <text x="268" y="216" fill="#e4e4e7" font-size="9" font-family="ui-monospace">1</text>
  <text x="292" y="216" fill="#e4e4e7" font-size="9" font-family="ui-monospace">1</text>
  <text x="316" y="216" fill="#e4e4e7" font-size="9" font-family="ui-monospace">0</text>
  <text x="340" y="216" fill="#e4e4e7" font-size="9" font-family="ui-monospace">0</text>
  <text x="244" y="232" fill="#a1a1aa" font-size="8" font-family="ui-monospace">3</text>
  <text x="268" y="232" fill="#e4e4e7" font-size="9" font-family="ui-monospace">0</text>
  <text x="292" y="232" fill="#e4e4e7" font-size="9" font-family="ui-monospace">1</text>
  <text x="316" y="232" fill="#e4e4e7" font-size="9" font-family="ui-monospace">0</text>
  <text x="340" y="232" fill="#e4e4e7" font-size="9" font-family="ui-monospace">0</text>
</svg></figure>

---
label: "VII"
subtitle: "二分探索木"
group: "データ構造とアルゴリズム"
order: 7
---
二分探索木 (BST)

順序付きバイナリ ツリー: 左側のサブツリー内のすべてのキーはノードのキーよりも厳密に小さくなります。右側のサブツリー内のすべてのキーは厳密に大きくなります (厳密な合計順序の場合)。

**操作:** 検索、挿入、削除はルートからリーフのパスに従います。時間は **O(h)** で、**h** は高さです。バランス: **h = O(log n)**;ソートされたインサートからのスキューチェーン: **h = Θ(n)**。

**バランス調整 (概要):** **AVL** ツリーは、回転によって高さの厳密なバランスを強制します。 **赤黒**の木は、カラー ルールを使用して **h = O(log n)** を維持し、バランスをわずかに緩め、平均して回転を少なくします。どちらも **O(log n)** の最悪の場合の検索/挿入/削除を復元します。

**関連:** **レベル II - ツリー、ヒープ、ハッシュ** (`ii-trees-heaps-hashing.md`)。

<figure class="notes-diagram"><svg xmlns="1 viewBox="0 0 400 218" role="img" aria-label="Binary search tree with smaller keys left larger keys right">
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">BST ordering (example)</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">search compares target with node; go left if smaller, right if larger</text>
  <circle cx="200" cy="72" r="22" fill="rgba(34,197,94,0.15)" stroke="#86efac" stroke-width="2"/>
  <text x="192" y="78" fill="#e4e4e7" font-size="13" font-family="ui-monospace" font-weight="600">5</text>
  <line x1="184" y1="88" x2="120" y2="128" stroke="#71717a" stroke-width="2"/>
  <line x1="216" y1="88" x2="280" y2="128" stroke="#71717a" stroke-width="2"/>
  <circle cx="120" cy="144" r="20" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="112" y="150" fill="#e4e4e7" font-size="12" font-family="ui-monospace">3</text>
  <circle cx="280" cy="144" r="20" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="272" y="150" fill="#e4e4e7" font-size="12" font-family="ui-monospace">8</text>
  <line x1="104" y1="158" x2="72" y2="178" stroke="#71717a" stroke-width="2"/>
  <circle cx="72" cy="188" r="16" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="66" y="192" fill="#e4e4e7" font-size="11" font-family="ui-monospace">1</text>
  <text x="300" y="72" fill="#71717a" font-size="9">all left &lt; parent &lt; all right</text>
  <text x="12" y="212" fill="#71717a" font-size="9">insert/delete walk one root-to-leaf path — height h dominates cost</text>
</svg></figure>

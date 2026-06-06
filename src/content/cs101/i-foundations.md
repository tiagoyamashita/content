---
label: "I"
subtitle: "基礎"
group: "データ構造とアルゴリズム"
order: 1
---
レベル I — 基礎

複雑さ、RAM モデル、配列、リンク リスト、スタック、キュー。

## 1. 私たちが測定するもの
- n = 入力サイズ (配列の長さ、ノード数など)。
- 一定係数までの n → ∞ としての成長を考慮します。
- 「最悪の場合」 = サイズ n のすべての入力に適用される限界。
- 「平均的なケース」には、入力がどのように分散されるかのモデルが必要です。


<figure class="notes-diagram"><svg xmlns="4 viewBox="0 0 440 96" role="img" aria-label="Input size n along an axis">
  <defs><marker id="dsa-i-a1" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#86efac"/></marker></defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Problem size</text>
  <line x1="48" y1="62" x2="408" y2="62" stroke="#52525b" stroke-width="2"/>
  <text x="44" y="82" fill="#a1a1aa" font-size="11">small</text>
  <text x="210" y="82" fill="#86efac" font-size="11" font-weight="600">n</text>
  <text x="330" y="82" fill="#a1a1aa" font-size="11">→ ∞</text>
  <path d="M72 38 H392" stroke="#86efac" stroke-width="2" fill="none" marker-end="url(#dsa-i-a1)"/>
  <text x="120" y="34" fill="#71717a" font-size="10">analyze growth as n grows</text>
</svg></figure>


## 2. 漸近表記 (非公式)
- O(g): 上限 — (定数内で) 最大でも g のように増加します。
- Ω(g): 下限 — 少なくとも g のように増加します。
- Θ(g): タイト — g と同じ成長クラス (O と Ω の間に挟まれている)。
例: リニアスキャン O(n);ソートされた配列 O(log n) での二分探索。
すべてのペアにわたるネストされたループは、多くの場合 O(n²) です。


<figure class="notes-diagram"><svg xmlns="5 viewBox="0 0 420 130" role="img" aria-label="Upper bound O, lower bound Omega, tight Theta">
  <text x="12" y="24" fill="#a1a1aa" font-size="11" font-family="system-ui,sans-serif">Upper (O) — at most ~</text>
  <path d="M40 44 Q210 8 380 44" stroke="#fbbf24" stroke-width="2" fill="none"/>
  <text x="12" y="72" fill="#86efac" font-size="11" font-weight="600">Tight (Θ) — same order</text>
  <path d="M40 88 Q210 72 380 88" stroke="#86efac" stroke-width="3" fill="none"/>
  <text x="12" y="118" fill="#a1a1aa" font-size="11">Lower (Ω) — at least ~</text>
  <path d="M40 104 Q210 124 380 104" stroke="#60a5fa" stroke-width="2" fill="none"/>
  <text x="150" y="56" fill="#71717a" font-size="10">typical f(n)</text>
</svg></figure>


## 3. 共通ツールキット

形状の順序付けは、[JavaScript の Big O 表記と時間計算量](6) などの入門 **時間計算量** チートシートと一致します。私たちのプロットは、壁時計のミリ秒ではなく、**最悪の場合のプリミティブ演算対 n** を描いています。 JS ブログではよく「実行時間」または「時間の複雑さ」について言及します。 θ(1)/ステップ RAM モデルでは、**操作数** が正確であるため、曲線の形状は一致します。

最も有力な (最も急速に成長している) 用語を選択します。ネストされたフェーズのコストを乗算します。漸近的に定数と低次のジャンクは消えます。

- **O(1)** - 修正されたステップ: インデックス付き読み取り `arr[i]`、ハッシュ マップ (`Map`) での償却キー付き検索。
- **O(log n)** — 各移動の半分を破棄します: ソートされたデータの二分探索 (リンクされたリストではランダム アクセスのショートカットはありません)。
- **O(n)** — 1 つの線形スイープ: ナイーブ `.includes` / `.find`、シングル パス累積 / 最大スキャン。
- **O(n log n)** — 効率的な比較ソートの典型的な除算と θ(n) の再結合 (マージ ソート / クイックソートの平均直感)。
- **O(n²)** — ネストされた線形作業: すべてのペアのブルートなバブルのようなパターン、インデックスに対する単純な二重ループ。
- **O(n³)** — トリプルネストスキャン: 単純な三次チェック (例: 一部のオールトリプレット / 密な 3 ループ DP エッジ)、構造の短絡が増大しない限りブルート 3 タプル。
- **O(2ⁿ)** — 分岐は代替手段を増やします: 総当たりのサブセット / メモ化のない不用意な指数再帰。

<figure class="notes-diagram" style="display:block;max-width:460px;margin:auto;">
  <figcaption style="text-align:center; color:#a1a1aa; margin-bottom:6px; font-size:12px;line-height:1.35;">
    One Cartesian plot — shared linear **y**: 0→920 for n = 1…30 (**n²** fills the spine; **log n**, **n**, **n log n**, and **O(1)** pile near the baseline; **n³** and **2ⁿ** truncate past the axis).
  </figcaption>
  <svg xmlns="7 viewBox="0 0 460 300" width="100%" height="280" style="display:block;max-width:460px;margin:auto;background:transparent" role="img" aria-label="Single Cartesian plot from n equals 1 to 30 comparing workload functions on one vertical scale zero to nine hundred twenty. Polynomial and exponential curves share the axes; exponential and cubic stop when exceeding the plotted range." preserveAspectRatio="xMinYMin meet">
    <defs><marker id="mk-dsa-arr-o" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><polygon points="0 0, 8 4, 0 8" fill="#52525b"/></marker></defs>
    <text x="230" y="26" fill="#e4e4e7" font-size="13" font-family="system-ui,sans-serif" text-anchor="middle" font-weight="600">Workload growth f(n)</text>
    <text x="230" y="44" fill="#71717a" font-size="10" font-family="system-ui,sans-serif" text-anchor="middle">Single linear axis — slower classes squeezed near zero</text>
    <text x="18" y="256" transform="rotate(-90 26 165)" fill="#a1a1aa" font-size="11" font-family="system-ui,sans-serif">f(n)</text>
    <line x1="48" y1="254" x2="410" y2="254" stroke="#52525b" stroke-width="2" marker-end="url(#mk-dsa-arr-o)"/>
    <line x1="48" y1="254" x2="48" y2="76" stroke="#52525b" stroke-width="2" marker-end="url(#mk-dsa-arr-o)"/>
    <text x="44" y="79" fill="#71717a" font-size="8">920</text>
    <text x="52" y="264" fill="#71717a" font-size="8">≈1</text>
    <polyline fill="none" stroke="#86efac" stroke-width="2.2" points="56,253.81 67.8,253.81 79.6,253.81 91.4,253.81 103.2,253.81 115,253.81 126.8,253.81 138.6,253.81 150.3,253.81 162.1,253.81 173.9,253.81 185.7,253.81 197.5,253.81 209.3,253.81 221.1,253.81 232.9,253.81 244.7,253.81 256.5,253.81 268.3,253.81 280.1,253.81 291.9,253.81 303.7,253.81 315.4,253.81 327.2,253.81 339,253.81 350.8,253.81 362.6,253.81 374.4,253.81 386.2,253.81 398,253.81"/>
    <polyline fill="none" stroke="#60a5fa" stroke-width="2" points="56,254 67.8,253.81 79.6,253.69 91.4,253.61 103.2,253.55 115,253.5 126.8,253.46 138.6,253.42 150.3,253.39 162.1,253.36 173.9,253.33 185.7,253.31 197.5,253.28 209.3,253.26 221.1,253.24 232.9,253.23 244.7,253.21 256.5,253.19 268.3,253.18 280.1,253.16 291.9,253.15 303.7,253.14 315.4,253.12 327.2,253.11 339,253.1 350.8,253.09 362.6,253.08 374.4,253.07 386.2,253.06 398,253.05"/>
    <polyline fill="none" stroke="#fbbf24" stroke-width="2" points="56,253.81 67.8,253.61 79.6,253.42 91.4,253.23 103.2,253.03 115,252.84 126.8,252.65 138.6,252.45 150.3,252.26 162.1,252.07 173.9,251.87 185.7,251.68 197.5,251.48 209.3,251.29 221.1,251.1 232.9,250.9 244.7,250.71 256.5,250.52 268.3,250.32 280.1,250.13 291.9,249.94 303.7,249.74 315.4,249.55 327.2,249.36 339,249.16 350.8,248.97 362.6,248.78 374.4,248.58 386.2,248.39 398,248.2"/>
    <polyline fill="none" stroke="#f472b6" stroke-width="2" points="56,254 67.8,253.61 79.6,253.08 91.4,252.45 103.2,251.75 115,251 126.8,250.2 138.6,249.36 150.3,248.48 162.1,247.57 173.9,246.64 185.7,245.68 197.5,244.69 209.3,243.69 221.1,242.66 232.9,241.62 244.7,240.56 256.5,239.48 268.3,238.38 280.1,237.28 291.9,236.15 303.7,235.02 315.4,233.87 327.2,232.71 339,231.54 350.8,230.35 362.6,229.16 374.4,227.96 386.2,226.74 398,225.52"/>
    <polyline fill="none" stroke="#fb7185" stroke-width="2.2" points="56,253.81 67.8,253.23 79.6,252.26 91.4,250.9 103.2,249.16 115,247.03 126.8,244.52 138.6,241.62 150.3,238.33 162.1,234.65 173.9,230.59 185.7,226.14 197.5,221.3 209.3,216.08 221.1,210.47 232.9,204.47 244.7,198.08 256.5,191.31 268.3,184.15 280.1,176.61 291.9,168.68 303.7,160.36 315.4,151.65 327.2,142.56 339,133.08 350.8,123.21 362.6,112.95 374.4,102.31 386.2,91.28 398,79.87"/>
    <polyline fill="none" stroke="#fb923c" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" points="56,253.81 67.8,252.45 79.6,248.78 91.4,241.62 103.2,229.82 115,212.21 126.8,187.64 138.6,154.94 150.3,112.95"/>
    <polyline fill="none" stroke="#a78bfa" stroke-width="2.2" points="56,253.61 67.8,253.23 79.6,252.45 91.4,250.9 103.2,247.81 115,241.62 126.8,229.23 138.6,204.47 150.3,154.94"/>
    <circle cx="150.3" cy="112.95" r="3" fill="#fb923c"/><circle cx="150.3" cy="154.94" r="3" fill="#a78bfa"/>
    <text x="248" y="68" fill="#71717a" font-size="8" font-family="system-ui,sans-serif">n³ &amp; 2ⁿ omit when f exceeds range</text>
    <text x="56" y="276" text-anchor="middle" fill="#71717a" font-size="9" font-family="system-ui,sans-serif">1</text>
    <text x="162" y="276" text-anchor="middle" fill="#71717a" font-size="9" font-family="system-ui,sans-serif">10</text>
    <text x="280" y="276" text-anchor="middle" fill="#71717a" font-size="9" font-family="system-ui,sans-serif">20</text>
    <text x="398" y="276" text-anchor="middle" fill="#71717a" font-size="9" font-family="system-ui,sans-serif">30</text>
    <text x="278" y="292" fill="#a1a1aa" font-size="11" font-family="system-ui,sans-serif" text-anchor="middle">input size n →</text>
  </svg>
  <div style="display:flex;flex-wrap:wrap;justify-content:center;gap:10px 15px;padding-top:8px;font-size:11px;line-height:1.4;"><span style="color:#86efac;font-family:monospace;">O(1)</span><span style="color:#a1a1aa;">f=1</span><span style="color:#60a5fa;font-family:monospace;">O(log&#160;n)</span><span style="color:#a1a1aa;">f=log₂n</span><span style="color:#fbbf24;font-family:monospace;">O(n)</span><span style="color:#a1a1aa;">f=n</span><span style="color:#f472b6;font-family:monospace;">O(n&#160;log&#160;n)</span><span style="color:#a1a1aa;">f=n·log₂n</span><span style="color:#fb7185;font-family:monospace;">O(n²)</span><span style="color:#a1a1aa;">f=n²</span><span style="color:#fb923c;font-family:monospace;">O(n³)</span><span style="color:#a1a1aa;">f=n³</span><span style="color:#a78bfa;font-family:monospace;">O(2ⁿ)</span><span style="color:#a1a1aa;">f=2ⁿ</span></div>
</figure>

n が増加するにつれて **原始演算数**が漸近的に増加します。上記と同じ教科書の曲線がランク付けされ、ステップごとに θ(1) の理想的な RAM レンズを通して読み取られます。この図では、**1 つの** 線形垂直スケール (n ∈ {1,…,30} で同じ **リテラル** ワークロード f(n)、別個の「低速/高速」正規化なし) を使用しています。**920** 付近の軸を n = 30 に向かって前景 **n²** に配置するため、**定数 / 対数 / 線形 / nlogn** は、視覚的に上に分離するまで、ゼロに近い薄い沿岸バンドを占めます。 **n³** と **2ⁿ** は同じ定規を使用し、手すりではなくプロットされた範囲を超えるストロークを単純に**省略**します。実際のミリ秒は、定数とハードウェアによって生の f(n) とは異なります。

## 4. 再発 (パターン認識)
- T(n) = T(n/2) + O(1) → O(log n) (各ステップを半分にします)。
- T(n) = T(n/2) + O(n) → O(n) (幾何級数)。
- T(n) = 2T(n/2) + O(n) → O(n log n) (バランスの取れたバイナリ再帰)。
- T(n) = T(n-1) + O(n) → O(n²) (線形チェーン)。
- T(n) = 2T(n/2) + O(n²) → O(n²) (マスター定理の直感)。
マスター定理: 形式を記憶する。試験では、いくつかのレベルを展開してパターンを確認します。


<figure class="notes-diagram"><svg xmlns="8 viewBox="0 0 400 140" role="img" aria-label="Divide into halves recurrence tree">
  <text x="160" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">T(n)</text>
  <circle cx="200" cy="36" r="18" fill="none" stroke="#86efac" stroke-width="2"/>
  <text x="188" y="40" fill="#e4e4e7" font-size="11">n</text>
  <line x1="200" y1="54" x2="120" y2="84" stroke="#71717a"/>
  <line x1="200" y1="54" x2="280" y2="84" stroke="#71717a"/>
  <circle cx="120" cy="98" r="16" fill="none" stroke="#a1a1aa" stroke-width="2"/>
  <text x="104" y="102" fill="#e4e4e7" font-size="10">n/2</text>
  <circle cx="280" cy="98" r="16" fill="none" stroke="#a1a1aa" stroke-width="2"/>
  <text x="264" y="102" fill="#e4e4e7" font-size="10">n/2</text>
  <text x="12" y="132" fill="#71717a" font-size="10">halving / balanced split → often log depth</text>
</svg></figure>


## 5. RAM モデルとメモリ
- ランダム アクセス マシン: O(1) 内の任意のメモリ ワードの読み取り/書き込み。
- 実 CPU: アレイはキャッシュに適しています (連続的)。ジャンプメモリをリストします。
- スペースの複雑さ: 入力を超える余分なメモリ (補助スペース)。


<figure class="notes-diagram"><svg xmlns="9 viewBox="0 0 420 88" role="img" aria-label="Random access memory words">
  <text x="12" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">RAM: addressable words (indexed)</text>
  <g stroke="#52525b" stroke-width="2">
    <rect x="24" y="36" width="56" height="36" rx="4" fill="rgba(34,197,94,0.12)"/>
    <rect x="92" y="36" width="56" height="36" rx="4" fill="rgba(24,24,27,0.9)"/>
    <rect x="160" y="36" width="56" height="36" rx="4" fill="rgba(24,24,27,0.9)"/>
    <rect x="228" y="36" width="56" height="36" rx="4" fill="rgba(24,24,27,0.9)"/>
    <rect x="296" y="36" width="56" height="36" rx="4" fill="rgba(24,24,27,0.9)"/>
  </g>
  <text x="38" y="58" fill="#86efac" font-size="11" font-family="ui-monospace">0</text>
  <text x="108" y="58" fill="#a1a1aa" font-size="11" font-family="ui-monospace">1</text>
  <text x="176" y="58" fill="#a1a1aa" font-size="11" font-family="ui-monospace">2</text>
  <text x="244" y="58" fill="#a1a1aa" font-size="11" font-family="ui-monospace">3</text>
  <text x="312" y="58" fill="#71717a" font-size="11">…</text>
  <text x="12" y="84" fill="#71717a" font-size="10">A[i] in O(1) in the model; arrays use contiguous words</text>
</svg></figure>


## 6. 配列と動的配列
- 静的配列: 固定長。インデックス i は、O(1) の A[i] にアクセスします。
- 動的配列 (ベクトルなど): 容量を維持します。満席になると2倍になります。
- 償却された O(1) を追加: 時折 O(n) のサイズ変更が行われ、多くの挿入に分散されます。
- 最後に挿入/削除: O(1) 償却された追加。中央: O(n) でシフトします。


<figure class="notes-diagram"><svg xmlns="10 viewBox="0 0 420 112" role="img" aria-label="Dynamic array doubling capacity">
  <text x="12" y="18" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Dynamic array: double capacity when full</text>
  <text x="12" y="38" fill="#a1a1aa" font-size="10">filled slots (cap = 4)</text>
  <rect x="16" y="46" width="76" height="26" rx="3" fill="rgba(34,197,94,0.28)" stroke="#86efac"/>
  <rect x="96" y="46" width="76" height="26" rx="3" fill="rgba(34,197,94,0.28)" stroke="#86efac"/>
  <rect x="176" y="46" width="76" height="26" rx="3" fill="rgba(34,197,94,0.28)" stroke="#86efac"/>
  <rect x="256" y="46" width="76" height="26" rx="3" fill="rgba(34,197,94,0.28)" stroke="#86efac"/>
  <text x="12" y="94" fill="#a1a1aa" font-size="10">after allocate (cap = 8): copy old block → new, room to grow</text>
  <rect x="16" y="72" width="312" height="26" rx="3" fill="none" stroke="#71717a" stroke-dasharray="5 4"/>
  <text x="332" y="90" fill="#71717a" font-size="9">···</text>
</svg></figure>


## 7. リンクされたリスト
- 単一リンク: 各ノード { value, next };ヘッドポインタ。
  — 既知のノードの後に​​挿入します: O(1)。値による検索: O(n)。
  — 逆方向リンクはありません。削除には前が必要です → 頻繁に O(n) をトラバースします。
- 二重リンク: { prev, next } — O(1) のポインターを持つノードを削除します。
- vs 配列: リストはイテレータでの挿入/削除に優れています。インデックスに配列。


<figure class="notes-diagram"><svg xmlns="11 viewBox="0 0 420 96" role="img" aria-label="Singly linked list nodes">
  <defs>
    <marker id="dsa-i-ln" markerWidth="8" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Singly linked list</text>
  <rect x="24" y="40" width="72" height="40" rx="6" fill="rgba(34,197,94,0.15)" stroke="#86efac" stroke-width="2"/>
  <text x="44" y="64" fill="#e4e4e7" font-size="11">data</text>
  <path d="M98 60 H132" stroke="#a1a1aa" stroke-width="2" marker-end="url(#dsa-i-ln)"/>
  <rect x="140" y="40" width="72" height="40" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="158" y="64" fill="#e4e4e7" font-size="11">data</text>
  <path d="M214 60 H248" stroke="#a1a1aa" stroke-width="2" marker-end="url(#dsa-i-ln)"/>
  <rect x="256" y="40" width="72" height="40" rx="6" fill="rgba(24,24,27,0.95)" stroke="#52525b" stroke-width="2"/>
  <text x="274" y="64" fill="#e4e4e7" font-size="11">data</text>
  <path d="M330 60 H358" stroke="#a1a1aa" stroke-width="2" marker-end="url(#dsa-i-ln)"/>
  <text x="368" y="64" fill="#71717a" font-size="11">null</text>
</svg></figure>


## 8. スタック (LIFO)
- 操作: Push(x)、pop()、peek/top()、isEmpty()。
- 配列 + 先頭インデックスまたはリンク リストの先頭を先頭として — 演算ごとにすべて O(1)。
- 用途: DFS、元に戻す、ブラケット マッチング、後置評価、コール スタックのアイデア。


<figure class="notes-diagram"><svg xmlns="12 viewBox="0 0 280 130" role="img" aria-label="Stack last in first out">
  <text x="88" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Stack (LIFO)</text>
  <text x="108" y="42" fill="#86efac" font-size="10" font-weight="600">top →</text>
  <rect x="100" y="48" width="80" height="22" rx="3" fill="rgba(34,197,94,0.25)" stroke="#86efac"/>
  <rect x="100" y="74" width="80" height="22" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="100" y="100" width="80" height="22" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="108" y="124" fill="#71717a" font-size="10">push / pop at top</text>
</svg></figure>


## 9. キューとデク
- キュー FIFO: エンキュー バック、デキュー フロント — 循環バッファによる O(1)
または先頭/末尾ポインタを含むリンクされたリスト。
- Deque: 両端で挿入/削除 — 二重リンクまたは円形配列。
- BFS はキューを使用します。スライディング ウィンドウの問題では、deque がよく使用されます。


<figure class="notes-diagram"><svg xmlns="13 viewBox="0 0 380 88" role="img" aria-label="Queue first in first out">
  <text x="118" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Queue (FIFO)</text>
  <text x="12" y="52" fill="#86efac" font-size="10">front</text>
  <rect x="52" y="36" width="52" height="26" rx="4" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <rect x="112" y="36" width="52" height="26" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="172" y="36" width="52" height="26" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="232" y="36" width="52" height="26" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="294" y="52" fill="#86efac" font-size="10">back</text>
  <text x="52" y="78" fill="#71717a" font-size="10">dequeue at front →</text>
  <text x="172" y="78" fill="#71717a" font-size="10">← enqueue at back</text>
</svg></figure>


## 10. 覚えてリハーサルする
- メモなしで 1 つの繰り返しを紙上で再作成します (例: マージソート)。
- API が与えられた場合、配列とリストを選択し、キャッシュと柔軟性を正当化します。
- 括弧に一致する小さなスタック上でプッシュ/ポップをトレースします。

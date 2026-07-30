---
label: "II"
subtitle: "コア概念"
group: "CS101"
order: 1
---
レベル II — コア概念

ビットとバイト、メモリ上のデータ、CPU からディスクまでのメモリ階層。

## 1. ビットとバイト
**ビット**（binary digit）は `{0, 1}` からの 1 記号で、デジタルマシンが区別する最小の情報単位です。より豊かなデータ（数値、テキスト、画像、命令）は、最終的には長いビット列として符号化されます。

**バイト**は固定の **8 ビット**（1 **オクテット**）のまとまりです。現代の多くのシステムは **メモリをバイト単位でアドレッシング**します。RAM 上の各バイトには整数の **アドレス**（0, 1, 2, …）があります。より広い値は連続する複数バイトにまたがり、型の **幅**（例: 32 ビット整数 = 4 バイト）が占有するバイト枠数を示します。

- **なぜ 8?** 歴史的な収束です。今日の既定のメンタルモデルは「バイト = 8 ビット」です。
- **より大きな塊:** プロセッサは **キャッシュライン**や **ページ**（下記の階層）でもデータを動かしますが、その下はやはりバイトです。


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 120" role="img" aria-label="One byte as eight bits with index order">
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">One byte = 8 bits (example pattern)</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">bit index 7 (often MSB of the byte) … 0 (often LSB) — convention depends on context</text>
  <g font-family="ui-monospace" font-size="11">
    <rect x="24" y="56" width="40" height="36" rx="4" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
    <text x="36" y="78" fill="#e4e4e7">1</text>
    <text x="34" y="94" fill="#71717a" font-size="8">b7</text>
    <rect x="68" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="80" y="78" fill="#e4e4e7">0</text>
    <rect x="112" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="124" y="78" fill="#e4e4e7">1</text>
    <rect x="156" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="168" y="78" fill="#e4e4e7">0</text>
    <rect x="200" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="212" y="78" fill="#e4e4e7">0</text>
    <rect x="244" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="256" y="78" fill="#e4e4e7">1</text>
    <rect x="288" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="300" y="78" fill="#e4e4e7">1</text>
    <rect x="332" y="56" width="40" height="36" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
    <text x="344" y="78" fill="#e4e4e7">0</text>
    <text x="376" y="78" fill="#71717a" font-size="9">= 8 bits</text>
  </g>
  <text x="12" y="112" fill="#71717a" font-size="9">256 possible values per byte (2⁸); multi-byte integers use several bytes in a defined order (endianness).</text>
</svg></figure>


## 2. ざっくり絵: データの保存と取得
**保存 (store):** CPU（またはデバイス）がビットパターンを一連のバイトアドレスへ置きます。たとえば store 命令は、アドレス `p` から始まる 32 ビット整数の 4 バイトを書き込みます。ハードウェアはその **物理アドレス**を RAM チップ上の位置へマップします（**仮想メモリ**では変換テーブルを介し、各プロセスが独自のアドレス空間を持てます）。

**取得 (retrieve / load):** **load** は同じアドレス（またはそのアドレスを含むキャッシュライン）を使い、演算が走る CPU **レジスタ**へビットをコピーします。レジスタやキャッシュに無ければメモリサブシステムが **RAM** から取ります。**ディスク**上にしか無ければ、OS が先に **ページ**を RAM へ載せます（はるかに遅い）。

- **アドレスと値:** アドレスは *どこ*、中身は *何*。高級言語のポインタは通常アドレス（またはその抽象）です。
- **アラインメント:** 一部の CPU は、高速アクセスのため複数バイト値が 4 または 8 で割り切れるアドレスから始まることを好みます（または要求します）。


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 168" role="img" aria-label="CPU load and store to byte addressed RAM">
  <defs>
    <marker id="cc-bus-mk" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0 L8 4 L0 8 Z" fill="#a1a1aa"/></marker>
  </defs>
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Load / store path (simplified)</text>
  <rect x="32" y="44" width="100" height="52" rx="8" fill="rgba(34,197,94,0.12)" stroke="#86efac" stroke-width="2"/>
  <text x="48" y="68" fill="#e4e4e7" font-size="11">CPU</text>
  <text x="40" y="86" fill="#a1a1aa" font-size="9">regs · ALU</text>
  <path d="M136 70 H200" stroke="#a1a1aa" stroke-width="2" marker-end="url(#cc-bus-mk)"/>
  <text x="148" y="64" fill="#71717a" font-size="8">address + data</text>
  <rect x="204" y="40" width="88" height="60" rx="6" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="220" y="62" fill="#e4e4e7" font-size="10">memory</text>
  <text x="212" y="78" fill="#a1a1aa" font-size="8">controller</text>
  <text x="212" y="92" fill="#71717a" font-size="8">cache · MMU</text>
  <path d="M296 70 H360" stroke="#a1a1aa" stroke-width="2" marker-end="url(#cc-bus-mk)"/>
  <rect x="364" y="48" width="64" height="44" rx="6" fill="rgba(24,24,27,0.95)" stroke="#71717a"/>
  <text x="376" y="74" fill="#e4e4e7" font-size="10">RAM</text>
  <text x="12" y="128" fill="#a1a1aa" font-size="10">Store: CPU sends address + value → bytes updated. Load: CPU sends address → bytes returned (often via a cache line fill).</text>
  <text x="12" y="148" fill="#71717a" font-size="9">Caches and TLBs sit between CPU and RAM; OS + disk handle data not resident in physical RAM.</text>
</svg></figure>


## 3. メモリ層（階層）
メモリは一様な速度ではありません。**容量**、**レイテンシ**、**コスト**をトレードする **階層**です。速い層は小さく、大きい層は遅いです。

| 層 | 役割（ざっくり） |
|--------|----------------|
| **CPU レジスタ** | 最速の記憶。実行中のオペランドがここに住む。 |
| **L1 / L2 / L3 キャッシュ** | コアに近い SRAM。最近使った **キャッシュライン**（RAM 断片のコピー）を持ち、RAM レイテンシを隠す。 |
| **RAM（メインメモリ）** | DRAM: 実行中プログラムの大きなワーキングセット。**揮発性**（電源喪失で消える）。 |
| **ディスク / SSD** | 永続でずっと大きいが、ランダムアクセスは **ずっと遅い**。必要時に OS がページイン。 |

**局所性:** **時間的**局所性 = すぐまた使う。**空間的**局所性 = 近くのアドレスをすぐ使う。良い局所性はホットなデータをレジスタとキャッシュに留めます。


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 220" role="img" aria-label="Memory hierarchy pyramid from fast small registers to slow large disk">
  <text x="100" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Memory hierarchy (fast ↑ small, slow ↓ large)</text>
  <polygon points="200,40 280,72 120,72" fill="rgba(34,197,94,0.35)" stroke="#86efac" stroke-width="2"/>
  <text x="168" y="62" fill="#e4e4e7" font-size="10" font-weight="600">registers</text>
  <polygon points="120,76 280,76 300,118 100,118" fill="rgba(34,197,94,0.2)" stroke="#86efac"/>
  <text x="154" y="102" fill="#e4e4e7" font-size="10">L1 / L2 / L3 cache</text>
  <polygon points="100,122 300,122 320,168 80,168" fill="rgba(96,165,250,0.15)" stroke="#60a5fa"/>
  <text x="168" y="148" fill="#e4e4e7" font-size="10">RAM (DRAM)</text>
  <polygon points="80,172 320,172 340,210 60,210" fill="rgba(113,113,122,0.4)" stroke="#71717a"/>
  <text x="150" y="196" fill="#e4e4e7" font-size="10">SSD / disk (persistent)</text>
  <text x="12" y="218" fill="#71717a" font-size="9">misses in a faster layer pull lines from the next slower layer; page faults go to disk.</text>
</svg></figure>


## 4. 仮想メモリ（一段落）
プロセスは通常 **仮想アドレス**を見ます。**MMU** がそれを **物理** RAM フレームへマップします。これにより隔離（プロセス A が誤って B のメモリを触れない）と **オーバーコミット**（仮想合計が RAM を超えても、アクティブなページだけが物理メモリに載る）が可能です。**ページフォルト**は必要なページが RAM に無いことを意味し、OS がディスクから読み込み命令を再開します。

## 5. 覚え・復習
- 1 バイトは何ビット？ 1 バイトが表せる相異なる値はいくつ？
- 一文で: **アドレス**とそのアドレスの **中身**の違いは？
- 典型的なノート PC で、層を小さい/速い順から大きい/遅い順に並べよ。

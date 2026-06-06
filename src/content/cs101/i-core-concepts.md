---
label: "I"
subtitle: "中心となる概念"
group: "データ構造とアルゴリズム"
order: 1
---
レベル I — 中心となる概念

ビットとバイト、データがメモリ内にどのように配置されるか、CPU からディスクまでのメモリ階層。

## 1. ビットとバイト
**ビット** (2 進数) は、`{0, 1}` からの 1 つの記号であり、デジタル マシンが識別する最小の情報です。より豊富なデータ (数値、テキスト、画像、指示) はすべて、最終的には長いビット パターンとしてエンコードされます。

**バイト**は**8ビット** (1 **オクテット**)の固定グループです。最新のシステムは **バイト単位でメモリにアドレス指定します**: RAM の各バイトには整数 **アドレス** (0、1、2、…) があります。幅の広い値は、複数の連続したバイトにまたがります。型の **幅** (例: 32 ビット整数 = 4 バイト) は、その型が占有するバイト スロットの数を示します。

- **なぜ 8 なのか?** 歴史的な収束。現在、「バイト = 8 ビット」がデフォルトのメンタル モデルです。
- **大きなチャンク:** プロセッサは、**キャッシュ ライン** と **ページ** (以下の階層を参照) にもデータを移動しますが、依然としてその下のバイトから構築されています。


<figure class="notes-diagram"><svg xmlns="2 viewBox="0 0 420 120" role="img" aria-label="One byte as eight bits with index order">
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


## 2. 大まかなイメージ: データの保存と取得
**ストア:** CPU (またはデバイス) はビット パターンをバイト アドレスのセットに配置します。たとえば、ストア命令はアドレス `p` から始まる 32 ビット整数の 4 バイトを書き込みます。ハードウェアは、**物理アドレス**を RAM チップの位置にマップします (また、**仮想メモリ**を使用して変換テーブルを使用して、各プロセスが独自のアドレス空間を持つことができます)。

**取得:** **ロード**は、同じアドレス (またはそのアドレスが既に含まれているキャッシュ ライン) を使用して、演算が実行される CPU **レジスタ**にビットをコピーします。データがレジスタまたはキャッシュにない場合、メモリ サブシステムは **RAM** からフェッチします。 **ディスク**上にのみある場合、OS は最初に **ページ**を RAM に取り込みます (非常に遅くなります)。

- **アドレスと値:** アドレスは *どこ* です。内容は*なんと*です。高級言語のポインターは通常、アドレス (またはその抽象化) です。
- **アライメント:** 一部の CPU は、高速アクセスのために、マルチバイト値を 4 または 8 で割り切れるアドレスから開始することを好みます (または要求します)。


<figure class="notes-diagram"><svg xmlns="3 viewBox="0 0 440 168" role="img" aria-label="CPU load and store to byte addressed RAM">
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
メモリは一定の速度ではありません。これは、**容量**、**レイテンシ**、**コスト**を取引する**階層**です。高速レイヤーは小さいです。大きなレイヤーは遅くなります。

|レイヤー |役割（大まか） |
|------|----------------|
| **CPU レジスタ** |最速のストレージ。オペランドは実行中にここに存在します。 |
| **L1 / L2 / L3 キャッシュ** | SRAM はコアに非常に近い。 RAM レイテンシーを隠すために、最近使用した **キャッシュ ライン** (RAM フラグメントのコピー) を保持します。 |
| **RAM (メインメモリ)** | DRAM: プログラムを実行するための大規模なワーキング セット。 **揮発性** (電力損失により失われます)。 |
| **ディスク/SSD** |永続的で、はるかに大規模で、**はるかに遅い** ランダム アクセス。 OS は必要に応じてデータをページインします。 |

**地域性:** **時間的** 地域性 = すぐに再利用。 **空間** 局所性 = 隣接するアドレスをすぐに使用します。優れた局所性により、ホットデータがレジスタとキャッシュに保持されます。


<figure class="notes-diagram"><svg xmlns="4 viewBox="0 0 400 220" role="img" aria-label="Memory hierarchy pyramid from fast small registers to slow large disk">
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


## 4. 仮想メモリ (1 段落)
通常、プロセスには **仮想アドレス** が表示されます。 **MMU** はそれらを **物理** RAM フレームにマップします。これにより分離が実現され (プロセス A が誤って B のメモリにアクセスすることはありません)、**オーバーコミット** (物理メモリにはアクティブ ページのみが存在するときに、仮想サイズの合計が RAM を超える可能性があります) が可能になります。 **ページ フォールト** は、必要なページが RAM にないことを意味します。OS はそのページをディスクからロードし、命令を再開します。

## 5. 覚えてリハーサルする
- 1 バイトは何ビットですか? 1 バイトで表現できる個別の値はいくつありますか?
- 一文で言うと、**アドレス**とそのアドレスの**コンテンツ**の違いは何ですか?
- 一般的なラップトップの場合、レイヤーを最小/高速から最大/低速の順に並べます。

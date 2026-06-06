---
label: "II"
subtitle: "動的配列"
group: "データ構造とアルゴリズム"
order: 2
---
動的配列（ベクトル）

効率的な追加を備えた拡張可能な連続バッファ。

### 固定サイズの配列または動的配列にプッシュすると Java では何が起こりますか?

#### 固定サイズ配列 (`int[] arr = new int[4];`)

Java では、固定サイズの配列を使用する場合、サイズは作成時に決定され、**変更することはできません**。  
- 最後の有効なインデックスを超える値 (たとえば、長さ 4 の配列の `arr[4] = 42`) を割り当てようとすると、Java は実行時に **`ArrayIndexOutOfBoundsException`** をスローします。
- **自動サイズ変更、コピー、拡大はありません**。配列のサイズは固定されており、それを「拡張」したい場合は、新しい（より大きな）配列を手動で作成し、要素を自分でコピーする必要があります。

#### 動的配列 (`ArrayList<E>`)

Java は、動的配列として動作する `ArrayList<E>` クラスを提供します。
- `add(e)` を呼び出し、基になる配列が *いっぱいではない (`size < capacity`) 場合、Java は次のスロット (**O(1)** 時) に要素を挿入します。
- 内部配列が * いっぱい* (`size == capacity`) のときに `add(e)` を呼び出すと、Java は次の処理を実行します。
  1. **新しい、より大きな内部配列を割り当てます** (デフォルトでは、Java 8 以降では容量が最大 50% 増加します)。
  2. すべての既存の要素を新しい配列に **コピー**します。
  3. 古い配列を **解放**します (ガベージ コレクションのため)。
  4. 新しい要素を **追加**します。
- サイズ変更とコピーのステップは *高価* (n 要素に対して `O(n)`) ですが、頻度が低いため、`add` あたりの平均時間は **償却 O(1)** のままです。

#### エッジケース (Java)

- **初期容量ゼロ:** 初期容量なしで `ArrayList` を作成し、すぐに追加する場合、リストは最初の追加時にストレージを割り当てる必要があります。
- **繰り返し追加:** 短期間に多くの項目をプッシュすると、Java は成長ポリシーに応じて、再割り当てとコピーを連続して数回行うことがあります。
- **最大配列サイズ:** Java 配列には最大サイズ (`Integer.MAX_VALUE`) があります。これを超えて成長しようとすると、`OutOfMemoryError` がスローされます。
- **一括追加 (`addAll`):** 多くの要素を一度に追加すると、すべての新しいアイテムに合わせて即座にサイズ変更が行われる可能性があります。

#### *起こらないこと* (Java)

- **固定サイズの配列**の場合、プッシュ (「過去の容量の追加」) によってサイズが変更されることはなく、例外がスローされます。
- `ArrayList` の場合、Java はサイズ変更を自動的に処理しますが、時間がかかり、大量のメモリ割り当てが原因でガベージ コレクションの一時停止が発生する場合があります。
- カスタム ポリシー (追加するたびに常に +1 ずつサイズ変更するなど) の場合、パフォーマンスが 2 次まで低下する可能性があります。Java のデフォルトの方が効率的です。

---

- **一般的な操作:** インデックス (**O(1)**) で `get`/`set`;償却を終了するには `add` **O(1)**。シフトのため、中央 **O(n)** で挿入/削除します。
- **スペース:** `n` 要素の場合は Θ(n)。実際の内部容量はさらに大きくなる可能性があります (サイズ変更のため、通常は n から約 1.5n の間です)。

<figure class="notes-diagram"><svg xmlns="20 viewBox="0 0 420 132" role="img" aria-label="Dynamic array doubles capacity and copies elements when full">
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

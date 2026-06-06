---
label: "X"
subtitle: "ハッシュテーブル"
group: "データ構造とアルゴリズム"
order: 10
---
ハッシュテーブル

**ハッシュ関数** `h(key)` を介してキーをテーブル スロットにマップします。負荷が適切な場合の平均ケース **O(1)** ルックアップ。

**衝突**は有限テーブルでは避けられません。 **連鎖:** 各スロットは、そのハッシュを共有するエントリのリストを保持します。負荷係数 **α = n/m** により、予想されるチェーン長さが決まります。 **オープン アドレッシング:** プローブ シーケンス (線形、二次、ダブル ハッシュ) は、同じ配列に代替を配置します。

**コスト:** 平均 **O(1)** 適切なハッシュと負荷制御による挿入/検索/削除。最悪の場合 **Θ(n)** すべてのキーが衝突した場合。

**関連:** **レベル II** (`ii-trees-heaps-hashing.md`)。

<figure class="notes-diagram"><svg xmlns="2 viewBox="0 0 440 168" role="img" aria-label="Hash function maps keys into buckets with collision chaining">
  <text x="12" y="22" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif" font-weight="600">Chaining: same slot, many keys</text>
  <text x="12" y="40" fill="#a1a1aa" font-size="10">h(key) mod m picks a bucket; collisions stored as a short linked list at that bucket</text>
  <text x="20" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">slot 0</text>
  <text x="92" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">slot 1</text>
  <text x="164" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">slot 2</text>
  <text x="236" y="78" fill="#71717a" font-size="9" font-family="ui-monospace">slot 3</text>
  <rect x="16" y="84" width="56" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="88" y="84" width="56" height="28" rx="4" fill="rgba(34,197,94,0.15)" stroke="#86efac"/>
  <rect x="160" y="84" width="56" height="28" rx="4" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <rect x="232" y="84" width="56" height="28" rx="4" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <path d="M116 112 L116 130" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="100" y="132" width="44" height="22" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="108" y="147" fill="#e4e4e7" font-size="9" font-family="ui-monospace">k1</text>
  <rect x="100" y="158" width="44" height="22" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="108" y="173" fill="#e4e4e7" font-size="9" font-family="ui-monospace">k4</text>
  <path d="M260 112 L260 126" stroke="#a1a1aa" stroke-width="1.5"/>
  <rect x="244" y="128" width="44" height="22" rx="3" fill="rgba(24,24,27,0.95)" stroke="#52525b"/>
  <text x="252" y="143" fill="#e4e4e7" font-size="9" font-family="ui-monospace">k9</text>
  <text x="300" y="104" fill="#60a5fa" font-size="9">lookup: hash → scan chain</text>
  <path d="M340 44 L116 84" stroke="#60a5fa" stroke-width="1" stroke-dasharray="4 3" fill="none"/>
  <text x="344" y="42" fill="#60a5fa" font-size="9" font-family="ui-monospace">h(k4)=1</text>
</svg></figure>

---
label: "VII"
subtitle: "アプリケーションレベル"
group: "システム設計"
order: 7
---
アプリケーションレベルのボトルネック

インフラストラクチャが正常に見えても、ロジックと **依存関係パターン** によりスケールが制限されます。

## 1. 同期ブロッキング

| Pattern | Problem | Fix |
|---------|---------|-----|
| Thread blocked on DB/API | Pool exhaustion | async/await, reactive, virtual threads |
| Serial calls in handler | Latency sums | Parallel `asyncio.gather`, fork-join |

|モデル |例 |
|------|----------|
|イベントループ | Node.js、非同期 |
|スレッドプール | JVM サーブレット プール |
|ゴルーチン + ブロック IO |限界を守ってください |

## 2. 雷鳴の群れ

**キャッシュの有効期限が切れる** → 多数の同時 **キャッシュ ミス** → すべてが DB にヒットします。

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 110" role="img" aria-label="Thundering herd on cache expiry">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Thundering herd</text>
  <rect x="12" y="36" width="64" height="28" rx="3" fill="rgba(251,191,36,0.12)" stroke="#fbbf24"/>
  <text x="24" y="54" fill="#e4e4e7" font-size="9">TTL expires</text>
  <path d="M76 50 H120" stroke="#f87171" stroke-width="1.5"/>
  <rect x="120" y="32" width="48" height="16" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <rect x="120" y="52" width="48" height="16" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <rect x="120" y="72" width="48" height="16" rx="2" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <text x="176" y="54" fill="#e4e4e7" font-size="8">N concurrent</text>
  <path d="M224 50 H268" stroke="#f87171" stroke-width="2"/>
  <rect x="268" y="44" width="56" height="32" rx="3" fill="rgba(248,113,113,0.25)" stroke="#f87171"/>
  <text x="276" y="64" fill="#e4e4e7" font-size="9">DB</text>
</svg></figure>

|緩和 |どのように |
|-----------|-----|
| **ロックオンミス** | 1 つはキャッシュを補充します。他の人は待ってください |
| **確率的に早い期限切れ** |ハード前にリフレッシュ TTL |
| **バックグラウンド更新** |古くなったものを提供します。非同期ウォーム |
| **合体をリクエスト** |シングルフライトパターン |

## 3. ホットキー/ホットパーティション

| Example | Fix |
|---------|-----|
| Viral tweet id | Local in-process cache; read replicas |
| One Redis key | Shard key: `key#0`…`key#N` |
| One DB shard | Re-shard; celebrity fan-out read model |

## 4. 遅い外部依存関係

|パターン |目的 |
|----------|----------|
| **タイムアウト** |早く失敗してください |
| **再試行 + バックオフ + ジッター** |一時的なエラー |
| **サーキットブレーカー** |失敗した dep の呼び出しを停止する |
| **バルクヘッド** |依存関係ごとにプールを分離する |
| **フォールバック** |キャッシュされた/デフォルトの応答 |

```text
Closed → failures ↑ → Open (fail fast) → Half-open probe → Closed
```

## 5. コードレベルのホットスポット

| Smell | Fix |
|-------|-----|
| Serialize in tight loop | Batch; binary format |
| Regex compile per request | Compile once |
| String `+` in loop | `StringBuilder` / `join` |
| Unbounded cache map | TTL + max size |

**常にプロファイルを作成します** — 測定なしに最適化を行わないでください。

**関連:** スケーラブルなパターンのレート制限、分散トランザクション (冪等性)。

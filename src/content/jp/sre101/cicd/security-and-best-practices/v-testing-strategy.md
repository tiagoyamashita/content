---
label: "V"
subtitle: "テスト戦略"
group: "CI/CD"
order: 5
---
テスト戦略

**左にシフト:** すべてのコミットで **最速かつ低コスト** のテストを実行します。遅くて高価なテストをマージまたは夜間のスケジュールに予約します。

## 1. テストピラミッド

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 140" role="img" aria-label="Test pyramid unit integration e2e">
  <polygon points="160,20 280,120 40,120" fill="rgba(24,24,27,0.6)" stroke="#52525b"/>
  <line x1="80" y1="90" x2="240" y2="90" stroke="#52525b"/>
  <line x1="110" y1="60" x2="210" y2="60" stroke="#52525b"/>
  <text x="148" y="110" fill="#86efac" font-size="9">Unit (many)</text>
  <text x="138" y="78" fill="#fbbf24" font-size="9">Integration</text>
  <text x="152" y="48" fill="#f87171" font-size="9">E2E (few)</text>
  <text x="12" y="136" fill="#71717a" font-size="9">Width = count · Height = cost &amp; duration</text>
</svg></figure>

|レイヤー |範囲 |スピード |いつ実行するか |
|----------|----------|----------|---------------|
| **ユニット** | 1 つのクラス/関数、モック |ミリ秒 |すべてのコミット / PR |
| **統合** | DB、キュー、HTTP と Testcontainers |秒–分 | PR ごと |
| **契約** | API サービス間のスキーマ |秒 | PR + 消費者の変化について |
| **E2E / 煙** |フルスタック、ブラウザ |分 |メイン、ステージングにマージ |
| **ロード/カオス** |生産的なストレス |分–時間 |夜間またはプレリリース |

## 2. CI ステージのマッピング

```yaml
# GitHub Actions — parallel test jobs
jobs:
  unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: mvn -B test

  integration:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: test
        ports: ['5432:5432']
    steps:
      - uses: actions/checkout@v4
      - run: mvn -B verify -Pintegration

  e2e:
    needs: [unit, integration]
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - run: npm run test:e2e
```

|ゲート |ブロック結合？ |
|------|--------------|
|ユニット + 糸くず |はい |
|統合 |はい |
| PR の E2E |オプション (遅い) |
|メインの E2E |導入前にはい |
|負荷テスト |いいえ — リグレッションに関するアラート |

## 3. 並列シャーディング

ランナー間でテスト スイートを分割します。

```bash
# Jest — 4 shards
npm test -- --shard=1/4
npm test -- --shard=2/4
```

```yaml
strategy:
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: npm test -- --shard=${{ matrix.shard }}/4
```

```bash
# pytest-xdist
pytest -n auto --dist loadscope
```

## 4. テストコンテナ (Java の例)

```java
@Testcontainers
class OrderRepositoryIT {
  @Container
  static PostgreSQLContainer<?> postgres = new PostgreSQLContainer<>("postgres:16");

  @Test
  void savesOrder() {
    // JDBC URL from postgres.getJdbcUrl()
  }
}
```

CI 中に Docker で実際の Postgres を実行します。SQL の方言と移行バグのモックをキャッチします。

## 5. レポートと PR フィードバック

```yaml
- name: Test
  run: mvn -B test

- name: Publish test report
  uses: dorny/test-reporter@v1
  if: always()
  with:
    name: Maven Tests
    path: target/surefire-reports/*.xml
    reporter: java-junit
```

JUnit XML → PR アノテーション。開発者は CI ログを開かなくても障害を確認できます。

## 6.不安定なテスト

| Symptom | Action |
|---------|--------|
| Passes on retry | Quarantine with `@Tag("flaky")`, track issue |
| Time-dependent | Fix clock injection; use fixed `Instant` |
| Order-dependent | Isolate test data; avoid shared static state |
| Network race | Awaitility / proper timeouts |

**Do not** disable flaky tests silently — metric **flaky test count** on dashboard [Pipeline observability & DORA](vi-pipeline-observability-and-dora.md).

```yaml
# Re-run failed tests once (temporary mitigation)
- run: mvn test || mvn -Dtest=FailedTest surefire:test
```

根本原因を修正します。再試行は応急処置です。

## 7. 適用範囲 — 賢明に使用する

```yaml
- run: mvn -B verify jacoco:report
- uses: codecov/codecov-action@v4
```

|良い |悪い |
|------|-----|
| PR の報道傾向 | 100% のライン カバレッジの義務 |
|発見されたクリティカル パスにフラグが付けられました |数値のゲッターをテストする |
|変更されたファイルの差分カバレッジ | 0.1 のグローバル % ドロップでブロック |

## 8. アンチパターン

| Anti-pattern | Fix |
|--------------|-----|
| No tests on PR | Branch protection requires status check |
| 45-min E2E on every push | Shard or run on main only |
| Shared staging DB for parallel CI | Ephemeral DB per job |
| `sleep(5000)` in tests | Poll with timeout |

**Related:** Part I fundamentals (artifacts/caching), [Release gates & rollbacks](vii-release-gates-and-rollbacks.md).

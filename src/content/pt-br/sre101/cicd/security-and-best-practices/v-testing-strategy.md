---
label: "V"
subtitle: "Testing strategy"
group: "CI/CD"
order: 5
---
Testing strategy
**Shift left:** run the **fastest, cheapest** tests on every commit; reserve slow, expensive tests for merge or nightly schedules.

## 1. Test pyramid

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 140" role="img" aria-label="Test pyramid unit integration e2e">
  <polygon points="160,20 280,120 40,120" fill="rgba(24,24,27,0.6)" stroke="#52525b"/>
  <line x1="80" y1="90" x2="240" y2="90" stroke="#52525b"/>
  <line x1="110" y1="60" x2="210" y2="60" stroke="#52525b"/>
  <text x="148" y="110" fill="#86efac" font-size="9">Unit (many)</text>
  <text x="138" y="78" fill="#fbbf24" font-size="9">Integration</text>
  <text x="152" y="48" fill="#f87171" font-size="9">E2E (few)</text>
  <text x="12" y="136" fill="#71717a" font-size="9">Width = count · Height = cost &amp; duration</text>
</svg></figure>

| Layer | Scope | Speed | When to run |
|-------|-------|-------|-------------|
| **Unit** | One class/function, mocks | ms | Every commit / PR |
| **Integration** | DB, queue, HTTP with Testcontainers | sec–min | Every PR |
| **Contract** | API schema between services | sec | PR + on consumer change |
| **E2E / smoke** | Full stack, browser | min | Merge to main, staging |
| **Load / chaos** | Production-like stress | min–hr | Nightly or pre-release |

## 2. CI stage mapping

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

| Gate | Block merge? |
|------|--------------|
| Unit + lint | Yes |
| Integration | Yes |
| E2E on PR | Optional (slow) |
| E2E on main | Yes before deploy |
| Load test | No — alert on regression |

## 3. Parallel sharding

Split test suite across runners:

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

## 4. Testcontainers (Java example)

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

Runs real Postgres in Docker during CI — catches SQL dialect and migration bugs mocks miss.

## 5. Reports and PR feedback

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

JUnit XML → PR annotations; developers see failures without opening CI logs.

## 6. Flaky tests

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

Fix root cause; retries are a band-aid.

## 7. Coverage — use wisely

```yaml
- run: mvn -B verify jacoco:report
- uses: codecov/codecov-action@v4
```

| Good | Bad |
|------|-----|
| Coverage trend on PR | 100% line coverage mandate |
| Uncovered critical paths flagged | Testing getters for numbers |
| Diff coverage on changed files | Blocking on global % drop of 0.1 |

## 8. Anti-patterns

| Anti-pattern | Fix |
|--------------|-----|
| No tests on PR | Branch protection requires status check |
| 45-min E2E on every push | Shard or run on main only |
| Shared staging DB for parallel CI | Ephemeral DB per job |
| `sleep(5000)` in tests | Poll with timeout |

**Related:** Part I fundamentals (artifacts/caching), [Release gates & rollbacks](vii-release-gates-and-rollbacks.md).

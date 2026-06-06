---
label: "VI"
subtitle: "Pipeline observability & DORA"
group: "CI/CD"
order: 6
---
Pipeline observability & DORA
A pipeline is a **distributed system** — measure it like production. **DORA metrics** link delivery speed to reliability.

## 1. DORA four key metrics

| Metric | Measures | Better direction |
|--------|----------|------------------|
| **Deployment frequency** | How often you ship to prod | Higher (for mature teams) |
| **Lead time for changes** | Commit → running in prod | Lower |
| **Change failure rate** | % deploys causing incident/rollback | Lower |
| **MTTR** | Mean time to restore after failure | Lower |

Elite performers: deploy on demand, lead time under a day, CFR under 15%, MTTR under an hour — your targets depend on domain (bank vs SaaS).

## 2. Mapping metrics to CI/CD data

| DORA metric | CI/CD signal |
|-------------|--------------|
| Deployment frequency | Deploy workflow runs on `main` / prod tag |
| Lead time | `commit timestamp` → `deploy job end` |
| Change failure rate | Deploy followed by rollback or hotfix within 24h |
| MTTR | Incident open → prod restored (PagerDuty + deploy log) |

```yaml
# Tag deploy job for analytics
deploy:
  environment:
    name: production
  steps:
    - name: Record deploy metadata
      run: |
        echo "deploy_sha=${{ github.sha }}" >> $GITHUB_STEP_SUMMARY
        echo "deploy_time=$(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $GITHUB_STEP_SUMMARY
```

Export to data warehouse (BigQuery, Snowflake) or tools like **Haystack**, **LinearB**, **Swarmia**.

## 3. Pipeline health metrics

| Metric | Why track |
|--------|-----------|
| **P50 / P95 duration** | Catch slowdowns from deps or cache miss |
| **Queue time** | Runner capacity planning |
| **Cache hit rate** | Cost and speed |
| **Flaky test rate** | Quality debt |
| **Failure rate by stage** | Where to invest |

```yaml
# GitHub — job timing in summary
- run: echo "duration=${SECONDS}s" >> $GITHUB_STEP_SUMMARY
```

## 4. Alerting

| Alert | Channel | Severity |
|-------|---------|----------|
| `main` pipeline failed | Slack `#ci-alerts` | High |
| Prod deploy failed | PagerDuty | Critical |
| Nightly security scan CVE | Slack + ticket | Medium |
| P95 duration > 2× baseline | Slack | Low |

```yaml
- name: Notify on failure
  if: failure() && github.ref == 'refs/heads/main'
  uses: slackapi/slack-github-action@v1
  with:
    payload: |
      {"text": "Main CI failed: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"}
```

Avoid alert fatigue — page only on **prod path** failures.

## 5. OpenTelemetry tracing

Instrument custom steps for distributed trace:

```yaml
- name: Run integration tests
  env:
    OTEL_SERVICE_NAME: ci-integration
    OTEL_EXPORTER_OTLP_ENDPOINT: https://otel.example.com
  run: |
    otel-cli exec -- mvn -Pintegration verify
```

View spans in **Honeycomb**, **Grafana Tempo**, or **Jaeger** — compare slow runs side by side.

## 6. Dashboard example (what to chart)

| Panel | Query idea |
|-------|------------|
| Deploys / week | Count prod deploy events |
| Lead time trend | Median commit→deploy hours |
| CI duration P95 | Job end − job start by workflow |
| Main branch success % | Green runs / total runs |
| Queue depth | Pending jobs on self-hosted pool |

## 7. CI vs CD observability

| Phase | Focus |
|-------|-------|
| **CI** (build/test) | Fast feedback, flake detection, cache |
| **CD** (deploy) | DORA metrics, rollback time, blast radius |

Connect CI green to CD deploy — a green build that never deploys still hurts **lead time**.

## 8. Rehearsal answers

- **Lead time** — time from code commit to production.
- **Change failure rate** — not unit test failure rate; deploys that hurt users.
- **Why trace CI?** — Find which stage regressed when total time doubles.
- **MTTR** — includes detection, fix, and redeploy.

**Related:** `v-testing-strategy.md`, `vii-release-gates-and-rollbacks.md`, Part I fundamentals.

---
label: "I"
subtitle: "概要"
group: "システム設計"
order: 1
---
ボトルネック分析 — 概要

**ボトルネック**とは、**飽和**が全体のスループットを制限するリソースです。 1 つを緩和すると、限界が**動く**ことがよくあります。体系的な測定は推測に勝ります。

## このサブメニューのマップ

| Note | Focus |
|------|--------|
| [Identifying bottlenecks](ii-identifying-bottlenecks.md) | Little's Law, USL, USE, RED, finding the limiter |
| [CPU & memory](iii-cpu-and-memory.md) | CPU, GC, leaks, caching pressure |
| [I/O & storage](iv-io-and-storage.md) | Disk, SSD, object storage, WAL |
| [Network](v-network.md) | Bandwidth, latency, connections, mesh |
| [Database](vi-database.md) | Reads, writes, pools, indexes |
| [Application-level](vii-application-level.md) | Thundering herd, hot keys, circuit breakers |
| [Elimination playbook](viii-elimination-playbook.md) | Measure → isolate → fix → validate → prevent |

## モグラたたきメンタルモデル

<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 100" role="img" aria-label="Bottleneck moves after each fix">
  <text x="12" y="20" fill="#d4d4d8" font-size="11" font-weight="600">Throughput limited by one resource at a time</text>
  <rect x="12" y="36" width="72" height="24" rx="3" fill="rgba(248,113,113,0.2)" stroke="#f87171"/>
  <text x="24" y="52" fill="#e4e4e7" font-size="8">DB 100%</text>
  <text x="96" y="52" fill="#a1a1aa" font-size="9">→ add cache</text>
  <rect x="160" y="36" width="72" height="24" rx="3" fill="rgba(251,191,36,0.2)" stroke="#fbbf24"/>
  <text x="172" y="52" fill="#e4e4e7" font-size="8">Redis hot</text>
  <text x="244" y="52" fill="#a1a1aa" font-size="9">→ shard key</text>
  <rect x="308" y="36" width="72" height="24" rx="3" fill="rgba(59,130,246,0.2)" stroke="#60a5fa"/>
  <text x="320" y="52" fill="#e4e4e7" font-size="8">CPU 95%</text>
  <text x="12" y="84" fill="#71717a" font-size="9">Profile end-to-end; fix highest-impact constraint; repeat.</text>
</svg></figure>

## リハーサルの質問

- 状態 **リトルの法則** — **W** が固定 **λ** で上昇すると何が上昇しますか?
- **USE** 対 **RED** — インフラストラクチャ対サービス?
- 雷鳴の群れ — 2 つの緩和策?
- 接続プールの枯渇 — **PgBouncer** の役割?
- エリミネーション戦略の 5 つのフェーズ?

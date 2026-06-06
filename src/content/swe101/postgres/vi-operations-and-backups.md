---
label: "VI"
subtitle: "操作とバックアップ"
group: "ポストグレ"
order: 6
---
Postgres — 操作とバックアップ

実稼働 Postgres には、**役割の分離**、**定期的なバックアップ**、**復元**と**フェイルオーバー**の計画が必要です。初日から DBA である必要はありませんが、これらのデフォルトを知っておく必要があります。

## 1. 役割と権限

|役割の種類 |典型的な権限 |
|----------|----------|
| **`postgres` スーパーユーザー** |ブレークガラス管理者のみ — アプリは対象外 |
| **アプリの役割** |スキーマの `CONNECT`、`USAGE`、アプリ テーブルの DML |
| **移行の役割** |ユーザー/CI を展開するための DDL |
| **読み取り専用分析** |特定のテーブルまたはビューに関する `SELECT` |

```sql
CREATE ROLE app_reader NOINHERIT;
GRANT CONNECT ON DATABASE myapp TO app_reader;
GRANT USAGE ON SCHEMA public TO app_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO app_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public
  GRANT SELECT ON TABLES TO app_reader;
```

管理コンソールまたは**`ALTER ROLE … PASSWORD`**を介してパスワードをローテーションします。

## 2. `pg_dump` を使用したバックアップ

論理バックアップ - 移植可能な SQL またはカスタム形式:

```bash
# Plain SQL (human-readable, slower restore)
pg_dump -h localhost -U postgres -d myapp -F p -f myapp-$(date +%F).sql

# Custom format (compressed, parallel restore)
pg_dump -h localhost -U postgres -d myapp -F c -f myapp.dump
```

復元する：

```bash
pg_restore -h localhost -U postgres -d myapp_restored -F c myapp.dump
```

|方法 |長所 |短所 |
|------|------|------|
| **`pg_dump`** |シンプル、バージョン移植可能 |ポイントインタイムには WAL アーカイブも必要です。
| **ボリューム スナップショット** |巨大な DB では高速 |クラッシュ整合性があるか、PG API を使用する必要があります。
| **管理された自動バックアップ** | PITR、保持ポリシー |ベンダーロックイン、コスト |

**四半期ごとにリストアをテストします** - テストされていないバックアップは推測です。

## 3. ポイントインタイムリカバリ (概念)

```text
Base backup (pg_dump or physical)  +  continuous WAL archive  →  restore to any second
```

マネージド Postgres (RDS、Cloud SQL、Neon) はコンソールで PITR を公開します。セルフホストには **`archive_mode`** と WAL 配送の構成が必要です。

## 4. レプリケーションの基本

|モード |目的 |
|-----|----------|
| **ストリーミング レプリケーション** |フェイルオーバーと読み取りスケールのためのホット スタンバイ |
| **論理レプリケーション** |選択テーブル、クロスバージョンアップグレード |

アプリケーションは書き込み用に 1 つの **プライマリ** を認識します。レプリカはミリ秒から数秒まで遅れる場合があります。書き込み後にそれに応じて UI を設計してください。

## 5.真空と膨満感

Postgres は **MVCC** を使用します。**VACUUM** がスペースを再利用するまで、`UPDATE`/`DELETE` は無効な行を残します。

|コマンド |誰が運営しているのか |
|----------|---------------|
| **自動バキューム** |バックグラウンド ワーカー (デフォルト オン) |
| **`VACUUM ANALYZE`** |大規模な削除後の手動 |
| **`VACUUM FULL`** |テーブルを書き換えます - 重度にロックします。珍しい |

テーブルが理由もなく増大する場合は、**`pg_stat_user_tables`** (`n_dead_tup`、最後の自動バキューム) に注意してください。

## 6. ヘルスチェック

```sql
SELECT count(*) FROM pg_stat_activity WHERE state = 'active';

SELECT schemaname, relname, seq_scan, idx_scan
FROM pg_stat_user_tables
ORDER BY seq_scan DESC
LIMIT 10;
```

|信号 |アクション |
|----------|----------|
| **`max_connections`** 付近の接続数 |プール サイズを減らすか、PgBouncer を追加します。
|大きなテーブルでは高い **`seq_scan`** |クエリとインデックスを確認する |
|ディスクの増加 |肥大化、WAL、ログ — ディレクトリごとに調査 |
|レプリケーションの遅延 |レプリカをスケールし、プライマリでの遅いクエリを修正します。

## 7. PgBouncer (接続多重化)

多くのアプリ インスタンスがそれぞれプールを保持する場合:

```text
Apps (many pools)  →  PgBouncer  →  Postgres (fewer real connections)
```

**トランザクション プーリング** モードは慎重に使用してください。構成されていない場合、セッション機能 (準備されたステートメント、一時テーブル) が機能しなくなる可能性があります。

## 8. 生産前のチェックリスト

- [ ] アプリは最小権限の DB ロールを使用します
- [ ] デプロイパイプラインで自動化された移行
- [ ] スケジュールされたバックアップ + テスト済みの復元
- [ ] 接続制限のサイズ (アプリ × プール + 管理者)
- [ ] 低速クエリ ログまたは APM が有効になっています
- [ ] env / vault のシークレット — git にはありません

## 関連メモ

- [リレーショナル (SQL)](../../CS101/databases/ii-relational.md) — SQL とトランザクション理論
- [データベース最適化](vii-database-optimizations.md) — 完全なチューニングワークフローとチェックリスト
- [データベースのボトルネック](../sysdesign/bottleneck-analysis/vi-database.md) — スケーリング読み取り、キャッシュ、シャーディング
- [JPA & トランザクション](../java/springboot/v-jpa-and-transactional.md) — ORM トランザクション境界

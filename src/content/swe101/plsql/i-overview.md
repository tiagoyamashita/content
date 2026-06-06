---
label: "I"
subtitle: "概要"
group: "PL/SQL"
order: 1
---
PL/SQL — 概要

**PL/SQL** (手続き型言語/SQL) は、**SQL** に対する Oracle の手続き型拡張機能です。これは、**Oracle Database** (匿名ブロック、ストアド **プロシージャ**、**関数**、**パッケージ**、**トリガー**) 内で実行されます。これらは、バッチ ジョブ、レガシー エンタープライズ アプリ、および接続するクライアントに関係なく保持する必要があるルールのデータに近いものです。

このトラックは、[リレーショナル (SQL)](../../CS101/databases/ii-relational.md) でリレーショナルの基本を理解していることを前提としています。オープンソースの Postgres パターンについては、[Postgres](../postgres/i-overview.md) トラックを参照してください。構文は異なりますが、DB 内手続きのトレードオフは似ています。

## このトラックの地図

|パート |フォーカス |
|------|----------|
| **I — 概要** | PL/SQL、Oracle ツール、ブロック構造の場合 |
| **II — ブロックと変数** | `DECLARE`/`BEGIN`/`END`、タイプ、`%TYPE`、`%ROWTYPE` |
| **III — 制御フローとカーソル** | `IF`、ループ、暗黙的および明示的カーソル |
| **IV — プロシージャと関数** |パラメータ、戻り値、SQL からの呼び出し |
| **V — パッケージとトリガー** |仕様/本体、状態、`BEFORE`/`AFTER` トリガー |
| **VI — 例外と一括 SQL** | `EXCEPTION`、`BULK COLLECT`、`FORALL`、プラグマ |
| **VII — データベースの最適化** |セットベースの SQL、プラン、バインド、一括チューニングのチェックリスト |

## PL/SQL が意味をなす場合

| DB で PL/SQL を使用する |アプリケーション コードを優先する |
|----------------------|----------------------|
|大規模なセットに対する複雑なマルチステップ SQL (ETL、レポート) | HTTP API、UI、オーケストレーション |
|すべてのクライアントが従わなければならないルール (制約 + トリガー) |頻繁に変更されるビジネス ロジック |
|夜間のバッチクローズ/元帳転記 |個別のデプロイサイクルを持つマイクロサービス |
|レガシー Oracle Forms、EBS、カスタム ERP モジュール |グリーンフィールドのクラウドネイティブ サービス |

**新しいサービスのデフォルト:** ほとんどのロジックをアプリ内に保持します。 Oracle が記録システムであり、チームがすでにパッケージを保守している場合は、PL/SQL を使用します。

## コードが実行される場所

```text
Client (Java, Python, SQL*Plus, SQL Developer)
        │
        ▼
   Oracle Database
        ├── SQL engine (SELECT, DML, DDL)
        └── PL/SQL engine (blocks, procedures, packages, triggers)
                    │
                    └── Shared buffer cache & undo — same transaction as SQL
```

PL/SQL と SQL はセッション内で **1 つのトランザクション**を共有します。`COMMIT`/`ROLLBACK` は両方に適用されます。

## ツーリング

|ツール |役割 |
|------|------|
| **SQL 開発者** |無料の GUI — スクリプトの実行、デバッグ、オブジェクトの参照 |
| **SQL*Plus / SQLcl** | CLI — スクリプト、CI、DBA タスク |
| **Oracle ライブ SQL** |ブラウザサンドボックス (oracle.com/livesql) |
| **JDBC / OCI** |アプリ呼び出し: `{ call pkg.proc(?) }` |

SQL DeveloperまたはSQLclの匿名ブロックの例:

```sql
SET SERVEROUTPUT ON
BEGIN
  DBMS_OUTPUT.PUT_LINE('Hello from PL/SQL');
END;
/
```

## ブロックの解剖学 (プレビュー)

すべての PL/SQL ユニットは次のようになります。

```text
[DECLARE   -- optional declarations]
BEGIN     -- executable statements
  ...
EXCEPTION -- optional handlers
  ...
END;
/
```

スラッシュ (`/`) は SQL*Plus/SQLcl にブロックを実行するよう指示します。 SQL Developerでは、**スクリプトの実行** (F5)と**ステートメントの実行** (Ctrl+Enter)をよく使用します。

## Oracle と Postgres 手続き型 SQL

| |オラクルPL/SQL | Postgres PL/pgSQL |
|---|---------------|----|
| **言語** |独自の、Oracle スタックで成熟 |オープンソース、Postgres ネイティブ |
| **パッケージ** |はい (`SPEC` + `BODY`) |スキーマ + 関数、パッケージ キーワードなし |
| **トリガー構文** | `:NEW` / `:OLD` 行トリガー | `NEW` / `OLD` 記録 |
| **典型的な雇用主の状況** |銀行、ERP、政府機関のオラクル資産 |スタートアップ、クラウドネイティブ、Supabase/Neon |

PL/SQL を理解すると、Oracle システムの保守に役立ちます。 SQL とアプリ スタックの学習に代わるものではありません。

＃＃ 次

[ブロックと変数](ii-blocks-and-variables.md) に進み、宣言、アンカー、代入を行います。

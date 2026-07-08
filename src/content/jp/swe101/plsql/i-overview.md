---
label: "I"
subtitle: "概要"
group: "PL/SQL"
order: 1
---
PL/SQL — 概要

**PL/SQL** (手続き型言語/SQL) は、**SQL** に対する Oracle の手続き型拡張機能です。これは、**Oracle Database** (匿名ブロック、ストアド **プロシージャ**、**関数**、**パッケージ**、**トリガー**) 内で実行されます。これらは、バッチ ジョブ、レガシー エンタープライズ アプリ、および接続するクライアントに関係なく保持する必要があるルールのデータに近いものです。

This track assumes you know relational basics from [Relational (SQL)](../../CS101/databases/ii-relational.md). For open-source Postgres patterns, see the [Postgres](../postgres/i-overview.md) track — syntax differs, but procedural-in-the-DB tradeoffs are similar.

## このトラックの地図

| Part | Focus |
|------|--------|
| **I — Overview** | When PL/SQL, Oracle tooling, block structure |
| **II — Blocks & variables** | `DECLARE`/`BEGIN`/`END`, types, `%TYPE`, `%ROWTYPE` |
| **III — Control flow & cursors** | `IF`, loops, implicit and explicit cursors |
| **IV — Procedures & functions** | Parameters, return values, calling from SQL |
| **V — Packages & triggers** | Spec/body, state, `BEFORE`/`AFTER` triggers |
| **VI — Exceptions & bulk SQL** | `EXCEPTION`, `BULK COLLECT`, `FORALL`, pragmas |
| **VII — Database optimizations** | Set-based SQL, plans, binds, bulk tuning checklist |

## PL/SQL が意味をなす場合

| DB で PL/SQL を使用する |アプリケーション コードを優先する |
|----------------------|----------------------|
|大規模なセットでの複雑なマルチステップ SQL (ETL、レポート) | HTTP APIs、UI、オーケストレーション |
|すべてのクライアントが従わなければならないルール (制約 + トリガー) |頻繁に変更されるビジネス ロジック |
|夜間のバッチクローズ/元帳転記 |個別のデプロイサイクルを持つマイクロサービス |
|レガシー Oracle Forms、EBS、カスタム ERP モジュール |グリーンフィールドのクラウドネイティブ サービス |

**新しいサービスのデフォルト:** ほとんどのロジックをアプリ内に保持します。 PL/SQL を使用します。Oracle が記録システムであり、チームがすでにパッケージを保守しています。

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

PL/SQL and SQL share **one transaction** in a session — `COMMIT`/`ROLLBACK` apply to both.

## ツーリング

| Tool | Role |
|------|------|
| **SQL Developer** | Free GUI — run scripts, debug, browse objects |
| **SQL*Plus / SQLcl** | CLI — scripts, CI, DBA tasks |
| **Oracle Live SQL** | Browser sandbox (oracle.com/livesql) |
| **JDBC / OCI** | App calls: `{ call pkg.proc(?) }` |

SQL Developer または SQLcl の匿名ブロックの例:

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

The slash (`/`) tells SQL*Plus/SQLcl to execute the block; SQL Developer often uses **Run Script** (F5) vs **Run Statement** (Ctrl+Enter).

## Oracle と Postgres 手続き型 SQL

| | Oracle PL/SQL | Postgres PL/pgSQL |
|---|---------------|-------------------|
| **Language** | Proprietary, mature in Oracle stack | Open source, Postgres-native |
| **Packages** | Yes (`SPEC` + `BODY`) | Schemas + functions, no package keyword |
| **Trigger syntax** | `:NEW` / `:OLD` row triggers | `NEW` / `OLD` record |
| **Typical employer context** | Banking, ERP, government Oracle estates | Startups, cloud-native, Supabase/Neon |

PL/SQL を理解すると、Oracle システムの保守に役立ちます。 SQL とアプリ スタックの学習に代わるものではありません。

＃＃ 次

Continue with [Blocks & variables](ii-blocks-and-variables.md) for declarations, anchors, and assignment.

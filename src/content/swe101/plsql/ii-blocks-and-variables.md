---
label: "II"
subtitle: "ブロックと変数"
group: "PL/SQL"
order: 2
---
PL/SQL — ブロックと変数

匿名ブロック、スカラー変数、**アンカー タイプ** (`%TYPE`、`%ROWTYPE`)、および割り当て - すべてのプロシージャとパッケージの基礎。

## 1. 匿名ブロック

```sql
DECLARE
  v_count NUMBER;
BEGIN
  SELECT COUNT(*) INTO v_count FROM employees WHERE department_id = 10;
  DBMS_OUTPUT.PUT_LINE('Dept 10 headcount: ' || v_count);
END;
/
```

|セクション |目的 |
|----------|----------|
| **`DECLARE`** |変数、定数、カーソル、ネストされたプロシージャ |
| **`BEGIN`** |実行可能ステートメント |
| **`EXCEPTION`** |セッション全体を中止せずにエラーを処理する |
| **`END`** |ブロックを閉じます |

SQL*Plus/SQLcl: **`SET SERVEROUTPUT ON`** で出力を有効にします。

## 2. 一般的なスカラー型

| PL/SQL タイプ | SQL にマップ |メモ |
|---------------|---------------|----------|
| **`NUMBER`** | `NUMBER` |整数と小数 |
| **`VARCHAR2(n)`** | `VARCHAR2` |可変長テキスト |
| **`DATE` / `TIMESTAMP`** |同じ |必要に応じて `TIMESTAMP WITH TIME ZONE` を使用します。
| **`BOOLEAN`** | *(なし)* | PL/SQL のみ - テーブルの列には格納できません。
| **`CLOB` / `BLOB`** |大きな物体 |ループ内のストリームまたはチャンク |

定数:

```sql
DECLARE
  c_tax_rate CONSTANT NUMBER(5,4) := 0.0825;
BEGIN
  NULL; -- placeholder
END;
/
```

## 3. アンカー タイプ (スキーマとの同期を維持)

**`%TYPE`** — 列タイプ:

```sql
DECLARE
  v_email employees.email%TYPE;
BEGIN
  SELECT email INTO v_email FROM employees WHERE employee_id = 100;
END;
/
```

**`%ROWTYPE`** — 行全体:

```sql
DECLARE
  r_emp employees%ROWTYPE;
BEGIN
  SELECT * INTO r_emp FROM employees WHERE employee_id = 100;
  DBMS_OUTPUT.PUT_LINE(r_emp.last_name);
END;
/
```

列の型が変更されると、アンカーされた変数も追従するため、移行後のサイレントな不一致が少なくなります。

## 4. 代入と式

```sql
DECLARE
  v_a NUMBER := 10;
  v_b NUMBER;
BEGIN
  v_b := v_a * 2;
  v_a := v_a + 1;
END;
/
```

|演算子 / 構成体 |例 |
|---------------------|----------|
| **連結** | 「こんにちは」 \|\|名前 |
| **比較** | `=`、`<>`、`IS NULL`、`BETWEEN` |
| **ケース** | `CASE dept WHEN 10 THEN … END` |
| **`SELECT … INTO`** |単一行フェッチ。行がゼロの場合、**`NO_DATA_FOUND`** が発生します。

## 5. `SELECT … INTO` ルール

```sql
DECLARE
  v_name employees.last_name%TYPE;
BEGIN
  SELECT last_name INTO v_name
  FROM employees
  WHERE employee_id = 99999;  -- no row → NO_DATA_FOUND
END;
/
```

|返された行 |結果 |
|--------------|----------|
| **0** | `NO_DATA_FOUND` |
| **1** |成功 |
| **>1** | `TOO_MANY_ROWS` |

オプションの単一行の場合は、カーソルまたは `SELECT … INTO … WHERE …` と例外ハンドラを使用します ([例外と一括 SQL](vi-exceptions-and-bulk-sql.md) を参照)。

## 6. ネストされたブロックとスコープ

```sql
DECLARE
  v_x NUMBER := 1;
BEGIN
  DECLARE
    v_x NUMBER := 2;  -- inner v_x shadows outer
  BEGIN
    DBMS_OUTPUT.PUT_LINE(v_x);  -- prints 2
  END;
  DBMS_OUTPUT.PUT_LINE(v_x);    -- prints 1
END;
/
```

複雑なスクリプトで **`<<exit_block>>`** ジャンプが必要な場合は、ブロックにラベルを付けます (アプリケーション コードではまれです)。

## 7. NULL セマンティクス

```sql
DECLARE
  a NUMBER := NULL;
  b NUMBER := 5;
BEGIN
  IF a = b THEN           -- unknown, not TRUE
    DBMS_OUTPUT.PUT_LINE('never');
  END IF;
  IF a IS NULL THEN
    DBMS_OUTPUT.PUT_LINE('a is null');
  END IF;
END;
/
```

`= NULL`ではなく、**`IS NULL` / `IS NOT NULL`**を使用してください。

＃＃ 次

[制御フローとカーソル](iii-control-flow-and-cursors.md) `IF`、ループ、および行ごとの処理に進みます。

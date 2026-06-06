---
label: "II"
subtitle: "redis-cli のインストールと"
group: "レディス"
order: 2
---
Redis — インストールと redis-cli

Redis をローカルで実行するか、**マネージド** サービス (ElastiCache、Redis Cloud、Upstash) を使用します。 **`redis-cli`** またはドライバー URI で接続します。

## 1. オプションのインストール

|方法 |いつ使用するか |
|----------|---------------|
| **ドッカー** |開発、CI、クイック リセット |
| **ネイティブ パッケージ** | `brew install redis`、Linux パッケージ |
| **管理** |独自のフェイルオーバーを実行せずに実稼働 HA |

### ドッカー

```bash
docker run --name redis-dev -p 6379:6379 -d redis:7
docker exec -it redis-dev redis-cli
```

永続ボリュームの場合:

```bash
docker run --name redis-dev -p 6379:6379 -v redisdata:/data -d redis:7 redis-server --appendonly yes
```

## 2. 接続 URI

```text
redis://localhost:6379/0
redis://:PASSWORD@host:6379/0
rediss://user:PASSWORD@host:6380/0   # TLS (managed clouds)
```

|パート |意味 |
|-----|----------|
| **`redis://` / `rediss://`** |プレーン / TLS |
| **`/0`** |データベース番号 (デフォルトでは 0 ～ 15、クラスターは 1 つの論理 DB を使用します) |
| **パスワード** | `requirepass` または ACL ユーザー |

## 3. `redis-cli` の必需品

```bash
redis-cli -h localhost -p 6379
# or
redis-cli -u redis://localhost:6379/0
```

```text
PING                    → PONG
SET greeting "hello"
GET greeting
DEL greeting

SET session:abc "{\"userId\":42}" EX 3600
TTL session:abc

KEYS user:*             # dev only — O(N), blocks on large DBs
SCAN 0 MATCH user:* COUNT 100   # production-safe iteration
```

|コマンド |アクション |
|----------|----------|
| **`SET` / `GET`** |文字列の読み取り/書き込み |
| **`SET key val EX seconds`** | TTLで設定 |
| **`INCR` / `DECR`** |アトミック整数 |
| **`EXPIRE` / `TTL`** |有効期限の管理 |
| **`DEL` / `UNLINK`** |削除 (`UNLINK` 非同期なし) |
| **`INFO memory`** |メモリ統計 |
| **`MONITOR`** |すべてのコマンドをストリーミングします — デバッグのみ、本番では実行しません |
| **`FLUSHDB`** |現在の DB を削除します — 開発のみ |

## 4. ACL ユーザー (Redis 6 以降)

```text
ACL SETUSER myapp on >local-secret ~myapp:* +get +set +del +incr +expire
AUTH myapp local-secret
```

**最小権限**を優先 — アプリユーザーは必要なコマンドとキーパターンのみを取得します (`~cache:*`)。

## 5. GUI クライアント (オプション)

|ツール |メモ |
|------|------|
| **Redis インサイト** |公式 GUI — ブラウザ キー、CLI、プロファイラ |
| **別の Redis デスクトップ マネージャー** |クロスプラットフォームのキーブラウザ |

`redis-cli` remains essential for production debugging.

## 6. 発煙試験

```text
SET counter 0
INCR counter
INCR counter
GET counter

HSET user:42 name Ada email ada@example.com
HGETALL user:42

EXPIRE user:42 300
TTL user:42
```

＃＃ 次

タイプと命名規則については、[データ構造とキー](iii-data-structures-and-keys.md) に進みます。

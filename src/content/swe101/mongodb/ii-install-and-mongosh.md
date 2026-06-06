---
label: "II"
subtitle: "インストールしてモンゴッシュする"
group: "モンゴDB"
order: 2
---
MongoDB — インストールと mongosh

MongoDB をローカルまたは **Atlas** で実行し、**URI** で接続し、**`mongosh`** でデータを探索します。

## 1. オプションのインストール

|方法 |いつ使用するか |
|----------|---------------|
| **ドッカー** |再現可能な開発、CI、クイック リセット |
| **MongoDB コミュニティ** |ラップトップへのネイティブ インストール |
| **MongoDB アトラス** |無料枠、バックアップ、ローカル デーモンなし |

### ドッカー

```bash
docker run --name mongo-dev -p 27017:27017 -d mongo:7
docker exec -it mongo-dev mongosh
```

永続ボリュームの場合:

```bash
docker run --name mongo-dev -p 27017:27017 -v mongodata:/data/db -d mongo:7
```

### アトラス (クラウド)

1. [mongodb.com/atlas](28) にクラスターを作成します。
2. データベース ユーザー + ネットワーク アクセスを追加します (IP 許可リストまたは開発のみ `0.0.0.0/0`)。
3. **接続 → ドライバー** から接続文字列をコピーします。

## 2. 接続文字列

```text
mongodb://USER:PASSWORD@HOST:27017/DATABASE
mongodb+srv://USER:PASSWORD@cluster0.xxxxx.mongodb.net/DATABASE
```

|パート |メモ |
|------|------|
| **`mongodb+srv://`** | Atlas DNS シード リスト — デフォルトでは TLS |
| **データベース** |デフォルトの認証 DB は異なる場合があります — Atlas UI を確認してください |
| **オプション** | `?retryWrites=true&w=majority` アトラスで共通 |

ローカルの例:

```text
mongodb://localhost:27017/myapp_dev
```

## 3. `mongosh` の必需品

```javascript
show dbs
use myapp_dev
show collections

db.products.insertOne({
  title: "Keyboard",
  price: 129.99,
  tags: ["hardware"]
})

db.products.find({ tags: "hardware" })
db.products.findOne({ title: "Keyboard" })
```

|コマンド |アクション |
|----------|----------|
| **`use dbname`** |データベースの切り替え (最初の書き込み時に作成) |
| **`db.coll.find()`** |クエリコレクション |
| **`db.coll.insertOne()` / `insertMany()`** |挿入 |
| **`db.coll.updateOne()` / `deleteOne()`** |変更 |
| **`db.coll.createIndex()`** |インデックスを追加 |
| **`db.coll.getIndexes()`** |リストインデックス |
| **`db.coll.stats()`** |サイズ、カウント、インデックスの統計 |

プリティプリント: **`db.products.find().pretty()`**

JS ファイルを実行します。

```bash
mongosh "mongodb://localhost:27017/myapp_dev" setup.js
```

## 4. ユーザーの作成 (ローカル開発者)

**`mongosh`** に管理者:

```javascript
use admin
db.createUser({
  user: "myapp",
  pwd: "local-only-secret",
  roles: [{ role: "readWrite", db: "myapp_dev" }]
})
```

接続する：

```text
mongodb://myapp:local-only-secret@localhost:27017/myapp_dev
```

Atlas は UI でユーザーを作成します。**最低権限** (1 つの DB に対して 26 ではなく 25) を優先します。

## 5. コンパス (オプションの GUI)

**MongoDB Compass** — ビジュアル ブラウザ、スキーマ推論、インデックス ビルダー、プランの説明。なじみのないコレクションを探索する場合に **`mongosh`** と併用すると便利です。

## 6. 発煙試験

```javascript
use myapp_dev

db.todos.insertMany([
  { title: "Learn mongosh", done: false, createdAt: new Date() },
  { title: "Model a collection", done: false, createdAt: new Date() }
])

db.todos.find({ done: false }).sort({ createdAt: 1 })
```

＃＃ 次

埋め込みルールと参照ルール、および検証ルールについては、[スキーマとモデリング](iii-schema-and-modeling.md) に進みます。

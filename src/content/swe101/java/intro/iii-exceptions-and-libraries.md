---
label: "III"
subtitle: "例外とライブラリ"
group: "ジャワ"
groupOrder: 1
order: 3
---
Java — パート III

例外、ジェネリック、コレクション、ストリーム、および実用的な API。

**Java ベースライン:** **Java SE 22** (`javac --release 22`); **JDK 21 LTS** でも問題ありません。

## 1. 例外
- **チェック済み**例外 (`extends Exception`): 呼び出し元は処理または宣言する必要があります。回復可能な障害に対しては慎重に使用してください。
- **未チェック** (`extends RuntimeException`): 必須の処理はありません - プログラミングのバグまたは可能性の低い障害。
- **`try-with-resources`** は `AutoCloseable` インスタンスを自動で閉じます - 手動 `finally` よりも優先されます。
- 例外を黙って飲み込まないでください。少なくともコンテキスト付きのログ。 `initCause` / コンストラクターチェーンを介して原因を保持します。

```java
// Compile: javac --release 22 …
import java.io.BufferedReader;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

static String readFirstLine(Path path) throws IOException {
  try (BufferedReader reader = Files.newBufferedReader(path)) {
    return reader.readLine();
  }
}

static int parsePort(String raw) {
  try {
    int port = Integer.parseInt(raw);
    if (port < 1 || port > 65535) {
      throw new IllegalArgumentException("port out of range: " + port);
    }
    return port;
  } catch (NumberFormatException e) {
    throw new IllegalArgumentException("invalid port: " + raw, e);
  }
}
```


## 2. ジェネリック医薬品
- 型パラメータ (`List<String>`) はコンパイル時に消去によって要素型を強制します。実行時は生の型 + キャストを参照します。
- ワイルドカード: `? extends T` (読み取りプロデューサー)、`? super T` (書き込みコンシューマー) — **PECS**: プロデューサー-拡張、コンシューマー-スーパー。
- 生のタイプ (`<>` を含まない `List`) は避けてください。チェックされていない警告は、保証が弱いことを示します。

```java
// Compile: javac --release 22 …
import java.util.ArrayList;
import java.util.List;

static double sum(List<? extends Number> values) {
  double total = 0;
  for (Number n : values) {
    total += n.doubleValue();
  }
  return total;
}

static void addIntegers(List<? super Integer> sink) {
  sink.add(42);
}

static List<String> names() {
  return new ArrayList<>();
}
```


## 3. コレクションのフレームワーク
- **`List`**: 順序付き、インデックス付き (`ArrayList`、`LinkedList`)。
- **`Set`**: 重複なし (`HashSet`、`LinkedHashSet`、`TreeSet` ソート済み)。
- **`Map`**: キー → 値 (`HashMap`、`LinkedHashMap`、`TreeMap`)。
- アクセス パターンによる選択: ハッシュ テーブルの平均検索数は O(1) です。ツリーは O(log n) でソートされた順序を与えます。

手作業で作成された構造 (リンク リスト、BST、ヒープ) は **CS101 → データ構造** の下にあります。製品コードでは、**`java.util`** 実装を優先します。**CS101 → アルゴリズム → JDK を使用した解決** を参照してください。

```java
// Compile: javac --release 22 …
import java.util.HashMap;
import java.util.Map;
import java.util.TreeSet;

static void countWords(String[] words) {
  Map<String, Integer> freq = new HashMap<>();
  for (String w : words) {
    freq.merge(w, 1, Integer::sum);
  }

  TreeSet<String> sortedKeys = new TreeSet<>(freq.keySet());
  sortedKeys.forEach(k -> System.out.println(k + " → " + freq.get(k)));
}
```


## 4. ストリーム API (基本)
- 宣言パイプラインの場合は `stream()`: `filter`、`map`、`reduce`、`collect`。
- 中間運用は怠惰です。端末操作 (`toList`、`count`、`findFirst`) は実行を駆動します。
- 並列ストリームは、ワークロードが大きく分割可能な場合にのみ役立ちます。デフォルトで並列に設定する前に測定してください。

```java
// Compile: javac --release 22 …
import java.util.List;

static List<String> activeEmails(List<User> users) {
  return users.stream()
      .filter(User::active)
      .map(User::email)
      .sorted()
      .toList();
}

record User(String email, boolean active) {}
```


## 5. 日付、オプション、および記録 (要約)
- **`java.time`** (`Instant`、`ZonedDateTime`、`LocalDate`) は、従来の `Date`/`Calendar` を置き換えます。
- **`Optional<T>`** は、null のない値が存在しないことを示します。フィールドまたはコンストラクターのパラメーターとして使用することは避けてください。戻り値の型として慎重に使用してください。
- **`enum`** 型は完全なクラスです。メソッドを保持し、インターフェイスを実装できます。

```java
// Compile: javac --release 22 …
import java.time.Instant;
import java.util.Optional;

enum OrderStatus {
  NEW, PAID, SHIPPED;

  boolean canShip() {
    return this == PAID;
  }
}

static Optional<Instant> parseInstant(String raw) {
  if (raw == null || raw.isBlank()) {
    return Optional.empty();
  }
  return Optional.of(Instant.parse(raw));
}
```


## 6. 同時並行メモ
- **`ExecutorService`** + タスクは、プーリングとライフサイクルに関して、ジョブあたり生の `Thread` を上回ります。
- 共有可変状態には、同期 (`synchronized`、ロック、同時コレクション) または制限/不変性が必要です。
- **仮想スレッド** (Java 21+) は I/O 負荷の高いコードに適しています。**パート VI (ラムダと最新の Java)** を参照してください。

```java
// Compile: javac --release 22 …
import java.util.concurrent.Executors;

static void runBatch(Runnable... tasks) throws InterruptedException {
  try (var pool = Executors.newFixedThreadPool(4)) {
    for (Runnable task : tasks) {
      pool.submit(task);
    }
  }
}
```

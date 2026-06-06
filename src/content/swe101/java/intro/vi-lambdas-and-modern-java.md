---
label: "VI"
subtitle: "ラムダと最新の Java"
group: "ジャワ"
groupOrder: 1
order: 6
---
Java — パート VI

関数インターフェイス、ラムダ、スイッチ式、シール型、仮想スレッド。

**Java ベースライン:** **Java SE 22** (`javac --release 22`); **JDK 21 LTS** でも問題ありません。

## 1. ラムダとメソッドの参照

**ラムダ** は **機能インターフェイス**、つまり 1 つの抽象メソッド (`Comparator`、`Runnable`、`Predicate` など) を備えたインターフェイスを実装します。

```java
// Compile: javac --release 22 …
import java.util.Comparator;
import java.util.List;

List<String> names = List.of("Ada", "Grace", "Linus");
names.sort(Comparator.comparing(String::length)); // method reference
names.sort((a, b) -> a.compareToIgnoreCase(b)); // lambda
```

**メソッド参照**形式: **`Type::staticMethod`**、**`instance::method`**、**`Type::new`**。

## 2. 式の切り替え

最新の **`switch`** は値を返し、フォールスルーすることなく **`->`** を使用できます。

```java
// Compile: javac --release 22 …
enum Role { ADMIN, USER, GUEST }

static String label(Role role) {
  return switch (role) {
    case ADMIN -> "Administrator";
    case USER -> "User";
    case GUEST -> "Guest";
  };
}
```

**シールド** 階層を使用すると、コンパイラは網羅性を検証できます (以下を参照)。

## 3. シールされたクラスとパターンマッチング

**Sealed** タイプは、拡張できる人を制限します。ドメイン モデルや包括的な **`switch`** に役立ちます。

```java
// Compile: javac --release 22 …
sealed interface Shape permits Circle, Rectangle {}

record Circle(double radius) implements Shape {}
record Rectangle(double width, double height) implements Shape {}

static double area(Shape shape) {
  return switch (shape) {
    case Circle c -> Math.PI * c.radius() * c.radius();
    case Rectangle r -> r.width() * r.height();
  };
}
```

## 4. 仮想スレッド (Java 21 以降)

**仮想スレッド** は軽量です。リクエストごとに 1 つのプラットフォーム スレッドを使用しない、I/O バウンドの作業 (HTTP、DB) に最適です。

```java
// Compile: javac --release 22 …
import java.util.concurrent.Executors;

try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
  executor.submit(() -> fetchFromService("orders"));
  executor.submit(() -> fetchFromService("inventory"));
} // waits for tasks when executor closes
```

CPU に依存する作業には、制限されたプラットフォーム プールで **`ExecutorService`** を使用します。モデルを混合する前に測定してください。

## 5. 次にどこへ行くか

- **コレクションとストリームの詳細** — パート III; **CS101 → アルゴリズム → JDK による解決** 実稼働用 **`HashMap`**、**`PriorityQueue`**、ソート。
- **ビルドとテスト** - パート IV、Web サービスの準備ができたら、**Spring Boot** トラック (同じ **`src/content/java/`** フォルダー、**`groupOrder: 2`**) に進みます。

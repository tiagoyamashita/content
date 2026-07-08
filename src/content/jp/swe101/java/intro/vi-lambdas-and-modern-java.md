---
label: "VI"
subtitle: "ラムダと最新の Java"
group: "Java"
groupOrder: 1
order: 6
---
Java — パート VI

関数インターフェイス、ラムダ、スイッチ式、シール型、仮想スレッド。

**Java ベースライン:** **Java SE 22** (`javac --release 22`); **JDK 21 LTS** でも問題ありません。

## 1. ラムダとメソッドの参照

**ラムダ** は、**機能インターフェイス**、つまり 1 つの抽象メソッド (`Comparator`、`Runnable`、`Predicate`、…）。

```java
// Compile: javac --release 22 …
import java.util.Comparator;
import java.util.List;

List<String> names = List.of("Ada", "Grace", "Linus");
names.sort(Comparator.comparing(String::length)); // method reference
names.sort((a, b) -> a.compareToIgnoreCase(b)); // lambda
```

**メソッドリファレンス** フォーム: **`Type::staticMethod`**、**`instance::method`**、**`Type::new`**。

## 2. 式の切り替え

モダンな **`switch`** は値を返して ** を使用できます`->`** フォールスルーなし:

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

**Sealed** タイプは、それを拡張できる人を制限します。ドメイン モデルや包括的な ** に役立ちます。`switch`**:

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

## 4. 仮想スレッド (Java 21+)

**仮想スレッド**は軽量であり、リクエストごとに 1 つのプラットフォーム スレッドを使用しない I/O- バインドされた作業 (HTTP、DB) に最適です。

```java
// Compile: javac --release 22 …
import java.util.concurrent.Executors;

try (var executor = Executors.newVirtualThreadPerTaskExecutor()) {
  executor.submit(() -> fetchFromService("orders"));
  executor.submit(() -> fetchFromService("inventory"));
} // waits for tasks when executor closes
```

使用 **`ExecutorService`** CPU に制限された作業用に制限されたプラットフォーム プールを使用します。モデルを混合する前に測定してください。

## 5. 次どこへ行くか

- **コレクションとストリームの詳細** — パート III; **CS101 → アルゴリズム → 実稼働用の JDK** による解決 **`HashMap`**、**`PriorityQueue`** そうですね。
- **ビルドとテスト** — パート IV、次に **Spring Boot** トラック (同じ **`src/content/java/`** フォルダー、**`groupOrder: 2`**) Web サービスの準備ができたら。

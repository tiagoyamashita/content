---
label: "II"
subtitle: "OOP とタイプ"
group: "Java"
groupOrder: 1
order: 2
---
Java — パート II

クラス、カプセル化、継承、ポリモーフィズム、インターフェイス、およびパッケージ。

**Java ベースライン:** **Java SE 22** (`javac --release 22`); **JDK 21 LTS** でも問題ありません。

## 1. クラスとオブジェクト
- **クラス** = ブループリント。 **オブジェクト** = 独自のフィールド値を持つメモリ内のインスタンス。
- コンストラクターは状態を初期化します。 none を宣言した場合は、コンストラクターを追加するまで、デフォルトの引数なしのコンストラクターが表示されます。
-`this`現在のインスタンスを指します。コンストラクターチェーンの使用`this(...)`。

```java
// Compile: javac --release 22 …
public class Counter {
  private int value;

  public Counter() {
    this(0);
  }

  public Counter(int start) {
    this.value = start;
  }

  public void increment() {
    value++;
  }

  public int getValue() {
    return value;
  }
}
```


## 2. カプセル化
- アクセサーの後ろにフィールドを非表示にする (`getX`、`setX`) またはより明確なドメイン メソッド。
- 最も狭い可視性を使用します。`private`フィールド、`public`API 表面は意図的に選択されました。
- 可能な限り不変性 -`final`フィールドは一度設定され、ミューテーターは不要 — 同時実行コードでの推論が簡素化されます。

```java
// Compile: javac --release 22 …
public final class EmailAddress {
  private final String value;

  public EmailAddress(String raw) {
    if (raw == null || !raw.contains("@")) {
      throw new IllegalArgumentException("invalid email");
    }
    this.value = raw.trim().toLowerCase();
  }

  public String value() {
    return value;
  }
}
```


## 3. 継承とポリモーフィズム
-`extends`1 つのスーパークラス。 Java は実装の単一継承をサポートしています。
- **`@Override`** スーパークラス メソッドを置き換える場合 - コンパイル時に署名の間違いを検出します。
- **動的ディスパッチ**: 仮想メソッドはランタイム型の実装に解決されます。
- 深い継承階層よりも構成を優先します。継承により、脆弱な基本クラスのコントラクトが明らかになります。

```java
// Compile: javac --release 22 …
abstract class Animal {
  abstract String speak();
}

class Dog extends Animal {
  @Override
  String speak() {
    return "woof";
  }
}

static void greet(Animal animal) {
  System.out.println(animal.speak()); // "woof" at runtime for Dog
}
```


## 4. 抽象クラスとインターフェイス
- **抽象クラス**: 部分的な実装。直接インスタンス化することはできません。
- **`interface`**: 行動契約を定義します。方法は次のとおりです`default`または`static`Java 8 以降のボディ。
- クラスは複数のインターフェースを実装できます。機能 (「比較できる」、「シリアル化できる」) のために使用します。
- **Sealed** クラス/インターフェイスは、拡張/実装できるユーザーを制限します。これは徹底的なモデリングに役立ちます。

```java
// Compile: javac --release 22 …
interface Identifiable {
  String id();
}

interface Auditable {
  default void logAccess() {
    System.out.println("access: " + id());
  }
}

record User(String id, String name) implements Identifiable, Auditable {}
```


＃＃５。`Object`必需品
-`equals`/`hashCode`一致する必要があります: 等しいオブジェクト → 同じハッシュ コード。
-`toString`デバッグとログを支援します。`clone`壊れやすいため、多くの場合、コピー コンストラクターまたはファクトリーが好まれます。
- 好む **`record`** (Java 16+) 不変データ キャリアの場合 - 自動`equals`、`hashCode`、`toString`、アクセサ。

```java
// Compile: javac --release 22 …
record Point(int x, int y) {}

static void demo() {
  var a = new Point(1, 2);
  var b = new Point(1, 2);
  System.out.println(a.equals(b)); // true
  System.out.println(a);           // Point[x=1, y=2]
}
```


## 6. パッケージとモジュール (概要)
- **`package`** は名前空間を宣言します。 **インポート** 短縮名。明確さが損なわれる場合は、大規模なコードベースでのワイルドカードのインポートを避けてください。
- **`java.base`** と友人は JDK を同梱しています。知る **`java.lang`**は暗黙的です。
- **JPMS** (`module-info.java`) プレーンなパッケージを超えてコンパイル時の境界を追加します。ライブラリを構築したり階層化を強制したりするときに採用されます。

```java
// Compile: javac --release 22 …
package com.example.domain;

import java.util.Objects;

public final class Money {
  private final long cents;

  public Money(long cents) {
    this.cents = cents;
  }

  @Override
  public boolean equals(Object o) {
    return o instanceof Money m && cents == m.cents;
  }

  @Override
  public int hashCode() {
    return Objects.hash(cents);
  }
}
```

ツリー状のデータ (BST、ヒープ) については、言語の基本からアルゴリズムに移行するときに、**CS101 → データ構造** を参照してください。

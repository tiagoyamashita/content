---
label: "I"
subtitle: "基本と構文"
group: "Java"
groupOrder: 1
order: 1
---
Java — パート I

JDK、プログラムの形状、タイプ、制御フロー、メソッド、および配列。

**このセクションの構成:** **`intro/`** (このグループは) パート VI を通じてコア言語をカバーします。 **`springboot/`** サブメニューには実践的な例が含まれています。 ** の兄弟ページ`java/`** ルート **`group: "Spring Boot"`** クラス、コレクション、テストに慣れたら、メイントラックをカバーしてください。

**Java ベースライン:** **Java SE 22** (`javac --release 22`); **JDK 21 LTS** でも問題ありません。

## 1. JDK、JVM、および最初のプログラム
- **JDK** = コンパイラ (`javac`)、標準ライブラリ、ツール。 **JVM** = バイトコードを実行するランタイム。
- ソース`.java`→`javac`→ バイトコード`.class`→`java`JVM を起動し、エントリ クラスをロードします。
- すべての実行可能なプログラムに必要なもの`public static void main(String[] args)`エントリーポイントとして。
- パッケージ (`package com.example.app;`) フォルダー パスにマップします。実際のプロジェクトではデフォルトのパッケージを避けてください。

```java
// Compile: javac --release 22 App.java && java App
package com.example.app;

public class App {
  public static void main(String[] args) {
    System.out.println("Hello, " + (args.length > 0 ? args[0] : "world"));
  }
}
```

```text
javac --release 22 com/example/app/App.java
java com.example.app.App Ada
```


<figure class="notes-diagram"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 120" role="img" aria-label="From Java source to JVM execution">
  <text x="110" y="20" fill="#d4d4d8" font-size="12" font-family="system-ui,sans-serif">Edit → compile → run</text>
  <rect x="28" y="36" width="88" height="36" rx="6" fill="rgba(34,197,94,0.12)" stroke="#86efac"/>
  <text x="44" y="58" fill="#e4e4e7" font-size="10">App.java</text>
  <path d="M116 54 H148" stroke="#a1a1aa" stroke-width="2"/>
  <text x="152" y="58" fill="#71717a" font-size="10">javac</text>
  <path d="M198 54 H230" stroke="#a1a1aa" stroke-width="2"/>
  <rect x="232" y="36" width="88" height="36" rx="6" fill="rgba(39,39,42,0.95)" stroke="#52525b"/>
  <text x="248" y="58" fill="#e4e4e7" font-size="10">App.class</text>
  <path d="M320 54 H352" stroke="#a1a1aa" stroke-width="2"/>
  <text x="356" y="58" fill="#71717a" font-size="10">java</text>
  <rect x="118" y="84" width="184" height="28" rx="4" fill="rgba(96,165,250,0.1)" stroke="#60a5fa"/>
  <text x="132" y="102" fill="#a1a1aa" font-size="9">JVM loads classes, JIT may optimize hot bytecode → machine code</text>
</svg></figure>


## 2. プリミティブ型と参照
- プリミティブ:`byte`、`short`、`int`、`long`、`float`、`double`、`char`、`boolean`— プリミティブとして宣言された場合、ローカルおよびフィールドに値によって格納されます。
- それ以外はすべて **参照型** (オブジェクト): 変数は参照を保持します。`null`「物体がない」という意味です。
- ラッパーの種類 (`Integer`、`Double`, …) コレクションおよび null 許容の API のボックス プリミティブ。ホットでヌルでないプリミティブを優先します。
-`var`(Java 10+) はイニシャライザからローカル型を推論します - 静的に型付けされたままです。

```java
// Compile: javac --release 22 …
int count = 42;
var name = "Ada";              // inferred String
Integer boxed = count;         // autoboxing
int again = boxed;             // unboxing
```


## 3. 演算子と制御フロー
- 算数 (`+`、`-`、`*`、`/`、`%`)、比較、論理`&&`、`||`、`!`、短絡動作。
-`if / else`、`switch`(クラシックとモダン **スイッチ式**`->`enum/sealed 型に関する網羅性)。
- ループ:`while`、`do-while`、`for`、**拡張機能** (`for (String s : items)`）。
-`break`/`continue`ネストされたループのオプションのラベルを使用します。

```java
// Compile: javac --release 22 …
enum Status { OPEN, CLOSED }

static String describe(Status s) {
  return switch (s) {
    case OPEN -> "accepting requests";
    case CLOSED -> "maintenance";
  };
}

static int sum(int[] values) {
  int total = 0;
  for (int v : values) {
    total += v;
  }
  return total;
}
```


## 4. メソッドとパラメータ
- 署名: 修飾子、戻り値の型、名前、パラメータ リスト、オプション`throws`;パラメータのタイプ/数による **オーバーロード**。
- **値渡し**: プリミティブはビットをコピーします。参照はポインタをコピーします。オブジェクトの変更は呼び出し元に表示されますが、パラメータの再割り当ては表示されません。
-`final`パラメータはメソッド内での再代入を防ぎます (オブジェクトの状態は依然として変更可能です)。

```java
// Compile: javac --release 22 …
import java.util.ArrayList;
import java.util.List;

static void addTag(List<String> tags, final String tag) {
  tags.add(tag);   // mutates caller's list
  // tag = "x";    // compile error — final parameter
}

static int max(int a, int b) {
  return a >= b ? a : b;
}
```


## 5. 配列と`String`- 配列は固定サイズであり、インデックスは次のとおりです。`0`;`length`分野;多次元配列は配列の配列です。
-`java.util.Arrays`ソート、バイナリ検索、フィル、コピーのヘルパーを提供します。
-`String`不変です。使用`StringBuilder`/`StringBuffer`ループ内で繰り返し連結する場合。
- テキストブロック (`""" ... """`) 複数行リテラルを簡略化します。

可変引数については、**パート V (配列、可変引数、リスト)** を参照してください。`ArrayList`、および CS101 相互リンク。

```java
// Compile: javac --release 22 …
String json = """
    {
      "name": "Ada"
    }
    """;

StringBuilder buf = new StringBuilder();
for (char c : json.toCharArray()) {
  if (!Character.isWhitespace(c)) {
    buf.append(c);
  }
}
```


## 6. スタイルと読みやすさ
- ネーミング:`camelCase`メソッド/ローカル、`PascalCase`種類、`SCREAMING_SNAKE`定数。
- コードを繰り返すコメントよりも、小さなメソッド、早期リターン、意味のある名前を優先します。
- 一貫してフォーマットします (IDE フォーマッタ)。保つ`public`意図が明らかでない場合は API が文書化されます。

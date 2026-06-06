---
label: "IV"
subtitle: "テストとデバッグ"
group: "ジャワ"
groupOrder: 1
order: 4
---
Java — パート IV

基本的なビルド、JUnit による自動テスト、効果的なデバッグ。

**Java ベースライン:** **Java SE 22** (`javac --release 22`); **JDK 21 LTS** でも問題ありません。

## 1. ツールとレイアウトを構築する
- **Maven** (`pom.xml`) および **Gradle** (`build.gradle.kts`) は依存関係を解決し、コンパイル、テスト、パッケージ化します。リポジトリごとに 1 つを選択し、一貫性を保ちます。
- 標準 Maven パス: `src/main/java`、`src/test/java`; `src/main/resources` 未満のリソース。
- **クラスパス**: JVM はディレクトリおよび JAR からバイトコードとリソースをロードします。ツールがこれを組み立てます。

```text
my-app/
  src/main/java/com/example/App.java
  src/test/java/com/example/AppTest.java
  pom.xml              # or build.gradle.kts
```


## 2. テストを自動化する理由
- **回帰安全性**: 動作を壊す変更は、運用環境ではなく CI で迅速に失敗します。
- **仕様**: テストは、散文だけよりも予期される動作をより正確に文書化します。
- **勇気をリファクタリング**: グリーン テストにより、内部を再構築する際の自信が高まります。


## 3. JUnit 5 の必需品
- **`@Test`** でテスト メソッドに注釈を付ける (JUnit Jupiter);最新の JUnit ではクラスは `public` である必要はありません。
- **アサーション** (`assertEquals`、`assertTrue`、`assertThrows`) は期待を表明します。失敗の意図を説明するメッセージを好みます。
- **`@BeforeEach` / `@AfterEach`** テストごとのセットアップ/ティアダウン。 **`@BeforeAll` / `@AfterAll`** 高価な共有セットアップ (多くの場合 `static`) の場合。
- **パラメータ化されたテスト** (`@ParameterizedTest` + ソース) は、コピー＆ペーストすることなく多くの入力をカバーします。

```java
// Compile: javac --release 22 … (JUnit on test classpath via Maven/Gradle)
import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class CalculatorTest {

  @Test
  void divideByZeroThrows() {
    var calc = new Calculator();
    assertThrows(ArithmeticException.class, () -> calc.divide(1, 0));
  }

  @ParameterizedTest
  @CsvSource({"2,3,5", "0,0,0", "-1,1,0"})
  void add(int a, int b, int expected) {
    assertEquals(expected, new Calculator().add(a, b));
  }
}

class Calculator {
  int add(int a, int b) { return a + b; }
  int divide(int a, int b) { return a / b; }
}
```


## 4. 実行ごとに成功 / 失敗 / スキップ (Maven / Gradle)

**Maven Surefire** は、スイートが終了すると 1 行の集計を出力します。次に例を示します。

```text
Tests run: 14, Failures: 0, Errors: 0, Skipped: 2
```

- **失敗** — アサーションが失敗しました (`Assertions.*`、Hamcrest など)。
- **エラー** — 予期しない例外 (セットアップが失敗した、テスト中の NPE)。
- **スキップ** — JUnit **`@Disabled`**、中止される仮定、または Surefire は除外します。

モジュールルートから **`mvn test`** を使用します。失敗したテストは、その概要の上でスタック トレースを繰り返します。ログを静かに表示するには、概要を表示しておきます。

```text
mvn -q test
```

**Gradle**: **`gradle test`** は **`14 tests completed, 2 skipped`** のようなもので終わります (文言はバージョンによって異なります)。

これらの数値は、ターミナルで**実行するたびに**更新されます。 CI または出力をキャプチャするスクリプトを追加しない限り、Markdown ノートには書き込まれません。


## 5. ダブルとスコープをテストする
- **単体テスト**: 1 つのクラスまたは関数を分離します。I/O や複雑さが気を散らす場合、コラボレーターはフェイク/モック/スタブに置き換えられます。
- **統合テスト**: 実際の配線 — DB、HTTP、ファイルシステム — 速度は遅くなりますが、構成バグを捕捉します。
- ルールをエンコードしない限り、簡単なゲッターのテストは避けてください。行動とエッジケースに焦点を当てます。


## 6. デバッグワークフロー
- **確実に再現** - 失敗した入力が最小になるか、不安定な場合の決定的なシードが得られます。
- **ブレークポイント**は実行を停止します。スタック フレーム、ローカルを検査し、式を評価します。
- **ステップオーバー / イン / アウト ** は通話階層をナビゲートします。条件付きブレークポイントはノイズをフィルターします。
- **`Thread` ペイン** にはデッドロックと待機が表示されます。 **ヒープ ダンプ**は、再現後のメモリ リークに役立ちます。


## 7. 伐採と防衛の習慣
- **`java.lang.System.Logger`** または SLF4J + バックエンドを使用します。レベル (`ERROR`、`WARN`、`INFO`、`DEBUG`) で製品内のノイズをフィルタリングします。
- **コンテキスト** (相関 ID、ユーザーレス識別子) をログに記録します。ポリシーのないシークレットや完全な PII は記録しません。
- ログとテストをペアにする: バグを修正するとき、可能な場合は最初に失敗したテストを追加します (**テスト主導のデバッグ**)。


## 8. 次へ: Spring Boot トラック

クラス、コレクション、例外、および JUnit を理解したら、同じ **`java/`** トピック フォルダーにある **Spring Boot — パート I (イントロおよびプロジェクト レイアウト)** に進んでください。このトラックでは、組み込みサーバー、依存関係注入、REST、JPA、セキュリティ、スライスのテスト、運用操作がカバーされており、ここと**パート VI (ラムダとモダン Java)** の言語基盤に基づいて構築されています。

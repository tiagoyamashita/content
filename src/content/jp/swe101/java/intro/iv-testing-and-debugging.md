---
label: "IV"
subtitle: "テストとデバッグ"
group: "Java"
groupOrder: 1
order: 4
---
Java — パート IV

基本的なビルド、JUnit による自動テスト、効果的なデバッグ。

**Java baseline:** **Java SE 22** (`javac --release 22`); also fine on **JDK 21 LTS**.

## 1. Build tools and layout
- **Maven** (`pom.xml`) and **Gradle** (`build.gradle.kts`) resolve dependencies, compile, test, package — pick one per repo and stay consistent.
- Standard Maven paths: `src/main/java`, `src/test/java`; resources under `src/main/resources`.
- **Classpath**: JVM loads bytecode and resources from directories and JARs — tools assemble this for you.

```text
my-app/
  src/main/java/com/example/App.java
  src/test/java/com/example/AppTest.java
  pom.xml              # or build.gradle.kts
```


## 2. テストを自動化する理由
- **回帰安全性**: 動作を壊す変更は、運用環境ではなく CI ですぐに失敗します。
- **仕様**: テストは、散文だけよりも予期される動作をより正確に文書化します。
- **勇気をリファクタリング**: グリーン テストにより、内部を再構築する際の自信が高まります。


## 3. JUnit 5 essentials
- Annotate test methods with **`@Test`** (JUnit Jupiter); class need not be `public` in modern JUnit.
- **Assertions** (`assertEquals`, `assertTrue`, `assertThrows`) express expectations; prefer messages that explain intent on failure.
- **`@BeforeEach` / `@AfterEach`** for setup/teardown per test; **`@BeforeAll` / `@AfterAll`** for expensive shared setup (often `static`).
- **Parameterized tests** (`@ParameterizedTest` + sources) cover many inputs without copy-paste.

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

- **Failures** — assertion failed (`Assertions.*`, Hamcrest, etc.).
- **Errors** — unexpected exception (setup blew up, NPE in test).
- **Skipped** — JUnit **`@Disabled`**, Assumptions that abort, or Surefire excludes.

Use **`mvn test`** from the module root; failed tests repeat stack traces above that summary. For quieter logs keep the summary visible:

```text
mvn -q test
```

**Gradle**: **`gradle test`** ends with something like **`14 tests completed, 2 skipped`** (wording varies by version).

これらの数値は、ターミナルで**実行するたびに**更新されます。 CI または出力をキャプチャするスクリプトを追加しない限り、Markdown ノートには書き込まれません。


## 5. ダブルとスコープをテストする
- **単体テスト**: 1 つのクラスまたは関数を分離します。I/O や複雑さが気を散らす場合、共同作業者はフェイク/モック/スタブに置き換えられます。
- **統合テスト**: 実際の配線 - DB、HTTP、ファイルシステム - 速度は遅くなりますが、構成バグを捕捉します。
- ルールをエンコードしない限り、簡単なゲッターのテストは避けてください。行動とエッジケースに焦点を当てます。


## 6. Debugging workflow
- **Reproduce** reliably — smallest failing input or deterministic seed for flaky cases.
- **Breakpoints** stop execution; inspect stack frames, locals, and evaluate expressions.
- **Step over / into / out** navigates call hierarchy; conditional breakpoints filter noise.
- **`Thread` panes** show deadlocks and waits; **heap dumps** help memory leaks after reproduction.


## 7. Logging and defensive habits
- Use **`java.lang.System.Logger`** or SLF4J + backend — levels (`ERROR`, `WARN`, `INFO`, `DEBUG`) filter noise in prod.
- Log **context** (correlation id, user-less identifiers), never secrets or full PII without policy.
- Pair logging with tests: when fixing a bug, add a failing test first when feasible (**test-driven debugging**).


## 8. 次へ: Spring Boot トラック

When you understand classes, collections, exceptions, and JUnit, continue with **Spring Boot — Part I (Intro & project layout)** in the same **`java/`** topic folder. That track covers embedded servers, dependency injection, REST, JPA, security, testing slices, and production operations — building on the language foundations here and **Part VI (Lambdas & modern Java)**.

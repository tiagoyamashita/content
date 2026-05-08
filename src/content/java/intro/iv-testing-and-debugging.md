---
label: "IV"
subtitle: "Testing & debugging"
group: "Java"
groupOrder: 1
order: 4
---
Java — Part IV
Build basics, automated testing with JUnit, and effective debugging.

## 1. Build tools and layout
- **Maven** (`pom.xml`) and **Gradle** (`build.gradle.kts`) resolve dependencies, compile, test, package — pick one per repo and stay consistent.
- Standard Maven paths: `src/main/java`, `src/test/java`; resources under `src/main/resources`.
- **Classpath**: JVM loads bytecode and resources from directories and JARs — tools assemble this for you.


## 2. Why automate tests
- **Regression safety**: changes that break behavior fail fast in CI instead of production.
- **Specification**: tests document expected behavior more precisely than prose alone.
- **Refactoring courage**: green tests increase confidence when restructuring internals.


## 3. JUnit 5 essentials
- Annotate test methods with **`@Test`** (JUnit Jupiter); class need not be `public` in modern JUnit.
- **Assertions** (`assertEquals`, `assertTrue`, `assertThrows`) express expectations; prefer messages that explain intent on failure.
- **`@BeforeEach` / `@AfterEach`** for setup/teardown per test; **`@BeforeAll` / `@AfterAll`** for expensive shared setup (often `static`).
- **Parameterized tests** (`@ParameterizedTest` + sources) cover many inputs without copy-paste.


## 4. Passed / failed / skipped every run (Maven / Gradle)

**Maven Surefire** prints a one-line tally when the suite finishes, for example:

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

Those numbers refresh **on every run** in the terminal; they are not written into your Markdown notes unless you add CI or a script that captures output.


## 5. Test doubles and scope
- **Unit tests**: isolate one class or function — collaborators replaced with fakes/mocks/stubs when I/O or complexity distracts.
- **Integration tests**: real wiring — DB, HTTP, filesystem — slower but catch composition bugs.
- Avoid testing trivial getters unless they encode rules; focus on behavior and edge cases.


## 6. Debugging workflow
- **Reproduce** reliably — smallest failing input or deterministic seed for flaky cases.
- **Breakpoints** stop execution; inspect stack frames, locals, and evaluate expressions.
- **Step over / into / out** navigates call hierarchy; conditional breakpoints filter noise.
- **`Thread` panes** show deadlocks and waits; **heap dumps** help memory leaks after reproduction.


## 7. Logging and defensive habits
- Use **`java.lang.System.Logger`** or SLF4J + backend — levels (`ERROR`, `WARN`, `INFO`, `DEBUG`) filter noise in prod.
- Log **context** (correlation id, user-less identifiers), never secrets or full PII without policy.
- Pair logging with tests: when fixing a bug, add a failing test first when feasible (**test-driven debugging**).

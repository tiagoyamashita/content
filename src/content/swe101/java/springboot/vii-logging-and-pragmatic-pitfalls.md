---
label: "VII"
subtitle: "ロギングと実用的な落とし穴"
group: "スプリングブーツ"
groupOrder: 2
order: 9
---
スプリングブート — パート VII

**SLF4J** による構造化ロギング、開発用の賢明なデフォルト、およびフレームワークのバグのように見えるが階層化または構成の問題であるよくある間違い。

## 1. SLF4J を使用したロギング

Spring Boot はデフォルトで **SLF4J** + **Logback** を接続します。クラスごとに **静的** ロガーを宣言します。

```java
// Compile: javac --release 22 …
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@RestController
public class OrderController {

  private static final Logger log = LoggerFactory.getLogger(OrderController.class);

  private final OrderService orderService;

  public OrderController(OrderService orderService) {
    this.orderService = orderService;
  }

  @PostMapping("/orders")
  public OrderDto create(@RequestBody CreateOrderDto body) {
    log.debug("create order customer={}", body.customerId());
    return orderService.create(body);
  }
}
```

- **`{}` プレースホルダー** を使用します。** — **`log.info("id={}", id)`** — **`string + id`** を避けてください。これにより、そのレベルが無効になっている場合に作業がスキップされます。
- **レベル**: **`ERROR`** / **`WARN`** は人間の対応が必要です。 **`INFO`** ライフサイクル イベント。 **`DEBUG`** / **`TRACE`** ノイズの多い検査 - **`application.yml`** (`logging.level.com.example=DEBUG`) 経由で調整します。
- **パスワード、トークン、完全な PAN は決してログに記録しないでください** - 識別子のみを編集またはログに記録します。
- **`logging.pattern.correlation`** / **MDC** (`MDC.put("traceId", …)`) は、後でトレース フィルターを追加するときにスレッド間でログを結び付けます。

## 2. トランザクション境界はサービスに属します

リポジトリにアクセスする **`@Service`** メソッドでは **`@Transactional`** を維持します。**`@RestController`** では **`@Transactional`** は維持しません。コントローラーは HTTP ↔ DTO をマッピングする必要があります。サービス独自の一貫性とロールバック セマンティクス。

よくある驚き (詳細は **パート V — JPA および `@Transactional`** を参照):

- デフォルトではチェックされていない例外 **ロールバック**。 **`rollbackFor`** を設定しない限り、チェックされた例外は **コミット** されます。
- **`private`** メソッドの **`@Transactional`**、または同じクラス内の **自己呼び出し**は、プロキシ トランザクションを**開始しません**。
- クエリ専用サービス メソッドの **`readOnly = true`** は意図を文書化し、プロバイダーの最適化に役立ちます。

## 3. 実用的な開発に関する注意点

- リクエストボディの **`@Valid`** + **`@ControllerAdvice`** / **`ProblemDetail`** - 一貫した **400** 応答は、制約違反によるサイレント **`500`** に勝ります。
- **`spring.jpa.show-sql=true`** — 開発のみで許容可能。 **`logging.level.org.hibernate.SQL=DEBUG`** + パラメータのログ記録は控えめにします。ノイズが多く、共有ログ内のデータが漏洩しやすいです。
- **DevTools** オプションの自動再起動 - 高速フィードバック。パフォーマンスに敏感なプロファイリングではオフになります。
- **例外を無視しないでください** — **`throw`** なしの **`catch (Exception e) { log.error(...); }`** は、失敗したと思われるトランザクションを **コミット**する可能性があります。
- **安全なアクチュエータと管理パス** — **セキュリティの基本とフィルタ チェーン**および**パート VI (テストと運用)**を参照してください。

## 4. 関連メモ

- **JPA とトランザクション** — [JPA と @Transactional](v-jpa-and-transactional.md)
- **REST 検証とエラー** — [REST コントローラー](iv-rest-controllers.md)
- **YAML ログ レベル** — [YAML と外部設定](ii-yaml-and-external-config.md)

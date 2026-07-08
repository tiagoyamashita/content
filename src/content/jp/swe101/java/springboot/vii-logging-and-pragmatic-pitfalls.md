---
label: "VII"
subtitle: "ロギングと実用的な落とし穴"
group: "Spring Boot"
groupOrder: 2
order: 9
---
Spring Boot — パート VII

**SLF4J** による構造化ロギング、開発用の賢明なデフォルト、およびフレームワークのバグのように見えるが階層化または構成の問題であるよくある間違い。

## 1. SLF4Jを使ったログ記録

Spring Boot は、デフォルトで **SLF4J** + **Logback** を接続します。クラスごとに **静的** ロガーを宣言します。

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

- 使用 **`{}`プレースホルダー** — **`log.info("id={}", id)`** - 避ける **`string + id`** したがって、そのレベルが無効になっている場合、作業はスキップされます。
- **レベル**: **`ERROR`** / **`WARN`** 人間の注意が必要; **`INFO`** ライフサイクル イベント; **`DEBUG`** / **`TRACE`** ノイズの多い検査 — ** を介して調整します`application.yml`** (`logging.level.com.example=DEBUG`）。
- **パスワード、トークン、完全な PAN は決してログに記録しないでください** - 識別子のみを編集またはログに記録します。
- **`logging.pattern.correlation`** / **MDC** (`MDC.put("traceId", …)`) 後でトレース フィルターを追加するときに、スレッド間でログを結び付けます。

## 2.境界境界はサービスに属しますか

保つ **`@Transactional`** の上 **`@Service`** リポジトリにアクセスするメソッド — ** では ** ではありません**`@RestController`**。コントローラーは HTTP ↔ DTO をマッピングする必要があります。サービス独自の一貫性とロールバック セマンティクス。

よくある驚き (詳細は **パート V — JPA &`@Transactional`**):

- デフォルトではチェックされていない例外 **ロールバック**。 ** を設定しない限り、チェックされた例外 **コミット**`rollbackFor`**。
- **`@Transactional`** の上 **`private`同じクラス内の ** メソッドまたは **自己呼び出し** はプロキシ トランザクションを**開始しません**。
- **`readOnly = true`** クエリ専用サービス メソッドでは、意図が文書化され、プロバイダーの最適化に役立ちます。

## 3. 実用的な開発に関する注意事項

- **`@Valid`** リクエスト本文 + **`@ControllerAdvice`** / **`ProblemDetail`** — 一貫した **400** の応答が沈黙を上回る **`500`** 制約違反によるもの。
- **`spring.jpa.show-sql=true`** — 開発環境でのみ許容可能。好む **`logging.level.org.hibernate.SQL=DEBUG`** + パラメータのログ記録は控えめに - ノイズが多く、共有ログ内のデータが漏洩しやすい。
- **DevTools** オプションの自動再起動 - 高速フィードバック。パフォーマンスに敏感なプロファイリングではオフになります。
- **例外を無視しないでください** — **`catch (Exception e) { log.error(...); }`** それなし **`throw`** 失敗したと思われるトランザクションを **コミット**する可能性があります。
- **安全なアクチュエーターと管理パス** — **セキュリティの基本とフィルター チェーン** および **パート VI (テストと運用)** を参照してください。

## 4. 関連メモ

- **JPA & トランザクション** — [JPA & @Transactional](v-jpa-and-transactional.md)
- **REST 検証とエラー** — [REST コントローラー](iv-rest-controllers.md)
- **YAML ログ レベル** — [YAML および外部設定](ii-yaml-and-external-config.md)

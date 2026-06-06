---
label: "III"
subtitle: "Beanと依存関係の注入"
group: "Spring Boot"
groupOrder: 2
order: 3
---
Spring Boot — パート III






IoC コンテナが Bean を結び付ける方法: ステレオタイプ、コンストラクター インジェクション、明示的 **`@Bean`** ファクトリ、修飾子、およびプロファイル固有の実装。

## 1. ステレオタイプはシングルトン Bean にマップされます
Spring は Bean 定義ごとに **1 つの共有インスタンス**を作成します (デフォルトのスコープ)。一般的な固定観念:

|注釈 |典型的な役割 |
|-----------|----------------|
| **`@Component`** |ジェネリック注射剤 |
| **`@Service`** |ドメイン/アプリケーションロジック |
| **`@Repository`** |永続性 (Spring は例外変換を追加します) |
| **`@RestController`/`@Controller`** | Web アダプター |

```java
// Compile: javac --release 22 …
@Service
public class OrderService {

  private final OrderRepository orders;

  public OrderService(OrderRepository orders) {
    this.orders = orders;
  }

  public Optional<Order> find(UUID id) {
    return orders.findById(id);
  }
}
```

**コンストラクターインジェクション**により依存関係が作成されます**`final`** 構築後にオブジェクトが使用可能であることを保証します — フィールドよりも優先されます **`@Autowired`**。

＃＃２。`@Autowired`必要なときに
コンストラクター インジェクションを使用できない場合 (まれに)、セッターまたはフィールド インジェクションが機能します。

```java
// Compile: javac --release 22 …
@Component
public class LegacyClient {

  private RestTemplate http;

  @Autowired
  public void setRestTemplate(RestTemplate http) {
    this.http = http;
  }
}
```

複数のコンストラクター: 1 つを ** でマークします`@Autowired`** (それ以外の場合、ブートは単一のコンストラクターを自動的に選択します)。

＃＃３。`@Bean`サードパーティタイプのファクトリ
クラスを所有していない場合は、** 経由でクラスを公開します。`@Configuration`** クラス：

```java
// Compile: javac --release 22 …
@Configuration
public class HttpClientConfig {

  @Bean
  public RestTemplate restTemplate(RestTemplateBuilder builder) {
    return builder
        .setConnectTimeout(Duration.ofSeconds(2))
        .setReadTimeout(Duration.ofSeconds(5))
        .build();
  }
}
```

**`RestTemplateBuilder`** は自動構成されます。これを挿入すると、タイムアウトが他のブートのデフォルトと一致します。

## 4. 複数の実装 →`@Qualifier`二 **`PaymentGateway`** 豆：

```java
// Compile: javac --release 22 …
import java.math.BigDecimal;

public interface PaymentGateway {
  void charge(BigDecimal amount);
}

@Component("stripe")
public class StripeGateway implements PaymentGateway { /* … */ }

@Component("paypal")
public class PayPalGateway implements PaymentGateway { /* … */ }
```

消費者は知識的に次のいずれかを選択します。

```java
// Compile: javac --release 22 …
@Service
public class CheckoutService {

  private final PaymentGateway gateway;

  public CheckoutService(@Qualifier("stripe") PaymentGateway gateway) {
    this.gateway = gateway;
  }
}
```

**`@Primary`** ある実装では、デフォルトが OK の場合に修飾子を回避します。

```java
// Compile: javac --release 22 …
@Component
@Primary
public class StubPaymentGateway implements PaymentGateway { /* dev default */ }
```

＃＃５。`@ConditionalOn*`そして`@Profile`プロファイルまたはプロパティが次の条件を満たしている場合にのみ Bean をロードします。

```java
// Compile: javac --release 22 …
@Configuration
@Profile("prod")
public class ProdObservabilityConfig {

  @Bean
  public MeterRegistryCustomizer<MeterRegistry> metricsCommonTags() {
    return registry -> registry.config().commonTags("application", "billing");
  }
}
```

**`@ConditionalOnProperty(name = "app.cache.enabled", havingValue = "true")`** 未使用のインフラストラクチャを起動せずに、設定フラグに基づいて Bean をゲートします。

## 6. ライフサイクルフック
**`@PostConstruct`** 注入後に実行されます。 **`DisposableBean`** / **`@PreDestroy`** クリーンアップの場合:

```java
// Compile: javac --release 22 …
@Component
public class WarmCacheRunner {

  @PostConstruct
  public void preload() {
    // safe to use injected collaborators here
  }
}
```

コンテキストを完全に準備する必要がある起動タスクの場合は、** を優先してください。`ApplicationRunner`** または **`CommandLineRunner`** 乱用ではなく豆を使用 **`@PostConstruct`**重労働用。

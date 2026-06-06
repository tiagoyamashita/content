---
label: "III"
subtitle: "Beans & dependency injection"
group: "Spring Boot"
groupOrder: 2
order: 3
---
Spring Boot — Part III
How the IoC container wires beans: stereotypes, constructor injection, explicit **`@Bean`** factories, qualifiers, and profile-specific implementations.

## 1. Stereotypes map to singleton beans
Spring creates **one shared instance** per bean definition (default scope). Common stereotypes:

| Annotation | Typical role |
|------------|----------------|
| **`@Component`** | Generic injectable |
| **`@Service`** | Domain / application logic |
| **`@Repository`** | Persistence (Spring adds exception translation) |
| **`@RestController` / `@Controller`** | Web adapters |

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

**Constructor injection** makes dependencies **`final`** and guarantees the object is usable after construction — prefer it over field **`@Autowired`**.

## 2. `@Autowired` when you need it
If you cannot use constructor injection (rare), setter or field injection works:

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

Multiple constructors: mark one with **`@Autowired`** (otherwise Boot picks the single constructor automatically).

## 3. `@Bean` factories for third-party types
When you don’t own the class, expose it via a **`@Configuration`** class:

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

**`RestTemplateBuilder`** is auto-configured — injecting it keeps timeouts consistent with other Boot defaults.

## 4. Multiple implementations → `@Qualifier`
Two **`PaymentGateway`** beans:

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

Consumer picks one explicitly:

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

**`@Primary`** on one implementation avoids qualifiers when a default is OK:

```java
// Compile: javac --release 22 …
@Component
@Primary
public class StubPaymentGateway implements PaymentGateway { /* dev default */ }
```

## 5. `@ConditionalOn*` and `@Profile`
Load beans only when a profile or property holds:

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

**`@ConditionalOnProperty(name = "app.cache.enabled", havingValue = "true")`** gates beans on configuration flags without starting unused infrastructure.

## 6. Lifecycle hooks
**`@PostConstruct`** runs after injection; **`DisposableBean`** / **`@PreDestroy`** for cleanup:

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

For startup tasks that need the context fully ready, prefer **`ApplicationRunner`** or **`CommandLineRunner`** beans instead of abusing **`@PostConstruct`** for heavy work.

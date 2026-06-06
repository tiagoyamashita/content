---
label: "VI"
subtitle: "テストと運用"
group: "スプリングブーツ"
groupOrder: 2
order: 6
---
Spring Boot — パート VI

**`@WebMvcTest`** / **`@DataJpaTest`** を使用してテストをスライスし、**`@SpringBootTest`** を使用して統合テストをブートストラップし、監視可能な展開用に Actuator とログを調整します。

## 1. `@WebMvcTest` — コントローラー契約のみ
完全な JPA なしで MVC インフラストラクチャをロードします — 協力者は **`@MockBean`** です:

```java
// Compile: javac --release 22 …
package com.example.demo.web;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.example.demo.service.CustomerService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;

@WebMvcTest(CustomerController.class)
class CustomerControllerTest {

  @Autowired MockMvc mockMvc;
  @Autowired ObjectMapper json;

  @MockBean CustomerService customers;

  @Test
  void createReturns201() throws Exception {
    when(customers.register(any(), any()))
        .thenReturn(new CustomerResponse(java.util.UUID.randomUUID(), "Ada", "ada@example.com"));

    mockMvc
        .perform(
            post("/api/customers")
                .contentType(MediaType.APPLICATION_JSON)
                .content(json.writeValueAsString(new CreateCustomerRequest("Ada", "ada@example.com"))))
        .andExpect(status().isCreated())
        .andExpect(jsonPath("$.name").value("Ada"));
  }
}
```

高速フィードバック: SQL の正確さではなく、マッピング、検証、JSON シリアル化を検証します。

## 2. `@DataJpaTest` — リポジトリ + スキーマ
埋め込みデータベースまたはテスト データベースを使用します (**`test`** リソースの下に **`spring.datasource`** を構成します)。

```java
// Compile: javac --release 22 …
import static org.assertj.core.api.Assertions.assertThat;

import com.example.demo.domain.OrderEntity;
import com.example.demo.domain.OrderStatus;
import com.example.demo.persistence.OrderRepository;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;

@DataJpaTest
class OrderRepositoryTest {

  @Autowired OrderRepository orders;

  @Test
  void persistsAndFinds() {
    OrderEntity o = orders.save(new OrderEntity("x@y.z", OrderStatus.NEW));
    assertThat(orders.findById(o.getId())).isPresent();
  }
}
```

## 3. `@SpringBootTest` — フルコンテキスト スモーク
より重い;レイヤーをまたぐクリティカル パスに使用します。

```java
// Compile: javac --release 22 …
import static org.assertj.core.api.Assertions.assertThat;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class BillingApplicationIT {

  @Autowired TestRestTemplate rest;

  @Test
  void actuatorHealth() {
    String body = rest.getForObject("/actuator/health", String.class);
    assertThat(body).contains("UP");
  }
}
```

**`spring-boot-starter-actuator`** を追加し、**`application-test.yml`** で **`health`** を公開します。

## 4. アクチュエーターと生産衛生
```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when_authorized
```

実際のデプロイメントでは Spring Security を使用して **`/actuator/**`** を保護します。**`prometheus`** または **`env`** を公共のインターネット上で開いたままにしないでください。 **セキュリティの基本とフィルター チェーン** [基本とフィルター チェーン](security-basics-and-filter-chain.md) を参照してください。

## 5. ロギングの調整
```yaml
logging:
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level [%thread] %logger{36} - %msg%n"
  level:
    root: INFO
    com.example.demo: DEBUG
```

Logback アペンダまたはプラットフォームのエージェントを介した **構造化ログ** (JSON) を優先します。**`MDC`** で伝播されたトレース ID とリクエストを関連付けます。

## 6. テストスタイルの選択
|目標 |注釈 |
|------|-----------|
|単一コントローラー + JSON | **`@WebMvcTest`** |
| JPA クエリ/マッピング | **`@DataJpaTest`** |
|セキュリティフィルターチェーン | **`@WebMvcTest` + `@AutoConfigureMockMvc(addFilters = …)`** または **`@SpringBootTest`** |
|実行中のポートに対するエンドツーエンドの HTTP | **`@SpringBootTest(webEnvironment = RANDOM_PORT)`** |

---
label: "VI"
subtitle: "テストと運用"
group: "Spring Boot"
groupOrder: 2
order: 6
---
Spring Boot — パート VI






** を使用したスライス テスト`@WebMvcTest`** / **`@DataJpaTest`**、** によるブートストラップ統合テスト`@SpringBootTest`** 観察可能な展開用に Actuator とログを調整します。

＃＃１。`@WebMvcTest`— コントローラー契約のみ
MVC インフラストラクチャを完全な JPA なしで**ロードします — 協力者は **`@MockBean`**:

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

高速フィードバック: SQL の正確さではなく、マッピング、検証、および JSON シリアル化を検証します。

＃＃２。`@DataJpaTest`— リポジトリ + スキーマ
組み込みデータベースまたはテスト データベースを使用します (** を構成します)`spring.datasource`** 下 **`test`** リソース）：

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

＃＃３。`@SpringBootTest`— フルコンテキストスモーク
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

追加 **`spring-boot-starter-actuator`**そして暴露**`health`** で **`application-test.yml`**。

## 4. アクチュエーターと生産衛生```yaml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: when_authorized
```

安全な **`/actuator/**`** 実際のデプロイメントでは Spring Security を使用 - 決して離れることはありません **`prometheus`** または **`env`** 公共のインターネット上で公開されます。 **セキュリティの基本とフィルター チェーン** [基本とフィルター チェーン](security-basics-and-filter-chain.md）。

## 5. ロギングの調整```yaml
logging:
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level [%thread] %logger{36} - %msg%n"
  level:
    root: INFO
    com.example.demo: DEBUG
```

Logback アペンダまたはプラットフォームのエージェントを介した **構造化ログ** (JSON) を優先します。** の伝播されたトレース ID とリクエストを関連付けます。`MDC`**。

## 6. テストスタイルの選択
|目標 |注釈 |
|------|-----------|
|単一のコントローラー + JSON | **`@WebMvcTest`** |
| JPA クエリ/マッピング | **`@DataJpaTest`** |
|セキュリティフィルターチェーン | **`@WebMvcTest`+`@AutoConfigureMockMvc(addFilters = …)`** または **`@SpringBootTest`** |
|実行中のポートに対するエンドツーエンド HTTP | **`@SpringBootTest(webEnvironment = RANDOM_PORT)`** |

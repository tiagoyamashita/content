---
label: "VI"
subtitle: "Testing & operations"
group: "Spring Boot"
groupOrder: 2
order: 6
---
Spring Boot — Part VI
Slice tests with **`@WebMvcTest`** / **`@DataJpaTest`**, bootstrap integration tests with **`@SpringBootTest`**, and tune Actuator plus logging for observable deployments.

## 1. `@WebMvcTest` — controller contract only
Loads MVC infrastructure **without** full JPA — collaborators are **`@MockBean`**:

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

Fast feedback: validates mapping, validation, and JSON serialization — not SQL correctness.

## 2. `@DataJpaTest` — repositories + schema
Uses an embedded or test database (configure **`spring.datasource`** under **`test`** resources):

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

## 3. `@SpringBootTest` — full context smoke
Heavier; use for critical paths crossing layers:

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

Add **`spring-boot-starter-actuator`** and expose **`health`** in **`application-test.yml`**.

## 4. Actuator & production hygiene
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

Secure **`/actuator/**`** with Spring Security in real deployments — never leave **`prometheus`** or **`env`** open on the public internet. See **Security basics & filter chain** (`security-basics-and-filter-chain.md`).

## 5. Logging tune-up
```yaml
logging:
  pattern:
    console: "%d{yyyy-MM-dd HH:mm:ss.SSS} %-5level [%thread] %logger{36} - %msg%n"
  level:
    root: INFO
    com.example.demo: DEBUG
```

Prefer **structured logging** (JSON) via Logback appenders or your platform’s agent — correlate requests with a propagated trace ID in **`MDC`**.

## 6. Choosing a test style
| Goal | Annotation |
|------|------------|
| Single controller + JSON | **`@WebMvcTest`** |
| JPA queries / mappings | **`@DataJpaTest`** |
| Security filter chain | **`@WebMvcTest` + `@AutoConfigureMockMvc(addFilters = …)`** or **`@SpringBootTest`** |
| End-to-end HTTP against running port | **`@SpringBootTest(webEnvironment = RANDOM_PORT)`** |

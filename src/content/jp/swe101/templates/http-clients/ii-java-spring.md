---
label: "II"
subtitle: "Java — Spring"
group: "HTTP clients"
order: 2
---
HTTP client template — Java (Spring Boot)
**`RestClient`** (Spring 6.1+) with mandatory timeout and **`ItemResponse`** mapping. DTO: [DTOs](../dtos/ii-java-spring.md) · caller: [Services](../services/ii-java-spring.md).

## Configuration

```yaml
# application.yml
catalog:
  base-url: https://catalog.example.com
  timeout-ms: 3000
```

```java
package com.example.client.config;

import org.springframework.boot.context.properties.ConfigurationProperties;

@ConfigurationProperties(prefix = "catalog")
public record CatalogProperties(String baseUrl, int timeoutMs) {}
```

## Template

```java
package com.example.client;

import com.example.api.dto.ItemResponse;
import com.example.client.config.CatalogProperties;
import java.time.Duration;
import java.util.Optional;
import org.springframework.http.HttpStatusCode;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClient;
import org.springframework.web.client.RestClientResponseException;

@Component
public class CatalogClient {

  private final RestClient restClient;

  public CatalogClient(CatalogProperties props, RestClient.Builder builder) {
    this.restClient = builder
        .baseUrl(props.baseUrl())
        .requestFactory(factory -> {
          var rf = new org.springframework.http.client.SimpleClientHttpRequestFactory();
          rf.setConnectTimeout(Duration.ofMillis(props.timeoutMs()));
          rf.setReadTimeout(Duration.ofMillis(props.timeoutMs()));
          return rf;
        })
        .build();
  }

  public Optional<ItemResponse> getItem(long id, String requestId) {
    try {
      ItemResponse body = restClient.get()
          .uri("/items/{id}", id)
          .header("X-Request-Id", requestId)
          .header("Accept", "application/json")
          .retrieve()
          .body(ItemResponse.class);
      return Optional.ofNullable(body);
    } catch (RestClientResponseException ex) {
      if (ex.getStatusCode().value() == 404) {
        return Optional.empty();
      }
      throw new CatalogException("catalog error: " + ex.getStatusCode(), ex);
    } catch (Exception ex) {
      throw new CatalogException("catalog unreachable", ex);
    }
  }
}

class CatalogException extends RuntimeException {
  CatalogException(String message, Throwable cause) {
    super(message, cause);
  }
}
```

## WebClient alternative (reactive / streaming)

```java
WebClient client = WebClient.builder()
    .baseUrl(props.baseUrl())
    .clientConnector(new ReactorClientHttpConnector(
        HttpClient.create().responseTimeout(Duration.ofMillis(props.timeoutMs()))))
    .build();

ItemResponse item = client.get()
    .uri("/items/{id}", id)
    .header("X-Request-Id", requestId)
    .retrieve()
    .bodyToMono(ItemResponse.class)
    .block(Duration.ofMillis(props.timeoutMs() + 500));
```

Use **`RestClient`** for blocking service code; **`WebClient`** when the rest of the stack is reactive.

## Notes

| Topic | Practice |
|-------|----------|
| **Timeout on factory** | Connect **and** read — both must be set |
| **404 → Optional.empty()** | Let the service decide not-found semantics |
| **Request ID** | Pass from `request.getAttribute(REQUEST_ID)` — [Middleware](../middleware/ii-java-spring.md) |
| **No RestTemplate** | Deprecated — prefer `RestClient` for new code |
| **Integration tests** | `@MockBean CatalogClient` or WireMock — not real HTTP |

## Next

[Python — FastAPI](iii-python-fastapi.md) · [HTTP clients overview](i-overview.md).

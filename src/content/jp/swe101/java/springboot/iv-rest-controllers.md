---
label: "IV"
subtitle: "REST コントローラー"
group: "Spring Boot"
groupOrder: 2
order: 4
---
Spring Boot — パート IV






** を使用して HTTP API を公開します`@RestController`**、パスとペイロードをマップ、** を返す`ResponseEntity`** ステータス管理用、** でエラーを集中管理`@ControllerAdvice`**。

## 1. コントローラーのスケルトン
**`@RestController`** 組み合わせ **`@Controller`** + **`@ResponseBody`** — 戻り値はデフォルトで Jackson 経由でシリアル化されます。

```java
// Compile: javac --release 22 …
package com.example.demo.web;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import java.net.URI;
import java.util.Optional;
import java.util.UUID;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.support.ServletUriComponentsBuilder;

@RestController
@RequestMapping("/api/customers")
public class CustomerController {

  private final CustomerService customers;

  public CustomerController(CustomerService customers) {
    this.customers = customers;
  }

  @GetMapping("/{id}")
  public ResponseEntity<CustomerResponse> get(@PathVariable UUID id) {
    return customers
        .find(id)
        .map(ResponseEntity::ok)
        .orElseGet(() -> ResponseEntity.notFound().build());
  }

  @PostMapping
  public ResponseEntity<CustomerResponse> create(@Valid @RequestBody CreateCustomerRequest body) {
    CustomerResponse created = customers.register(body.name(), body.email());
    URI location =
        ServletUriComponentsBuilder.fromCurrentRequest()
            .path("/{id}")
            .buildAndExpand(created.id())
            .toUri();
    return ResponseEntity.created(location).body(created);
  }

  @GetMapping
  public Iterable<CustomerResponse> search(@RequestParam(required = false) String q) {
    return customers.search(Optional.ofNullable(q).orElse(""));
  }
}
```

## 2. リクエスト/レスポンス DTO + 検証
エンティティをワイヤ形式にしないようにします。専用のレコードを使用します。

```java
// Compile: javac --release 22 …
public record CreateCustomerRequest(
    @NotBlank String name,
    @NotBlank String email
) {}

public record CustomerResponse(UUID id, String name, String email) {}
```

有効にする **`jakarta.validation`** を含む受信ボディについて`@Valid`パラメータの ** (** が必要)`spring-boot-starter-validation`** クラスパス上)。

## 3. マッピングのチートシート
|注釈 | |からの地図
|-----------|----------|
| **`@PathVariable`** |`/items/{id}`セグメント |
| **`@RequestParam`** |クエリ文字列`?page=1`|
| **`@RequestHeader`** | HTTP ヘッダー |
| **`@RequestBody`** | JSON / XML 本文 |
| **`@RequestPart`** | **`multipart/form-data`** フィールド |

## 4. 例外のないステータス コード
**`ResponseEntity`** 本文 + ステータス + ヘッダーをラップします:

```java
// Compile: javac --release 22 …
@DeleteMapping("/{id}")
public ResponseEntity<Void> delete(@PathVariable UUID id) {
  boolean removed = customers.deleteIfExists(id);
  return removed ? ResponseEntity.noContent().build() : ResponseEntity.notFound().build();
}
```

## 5. グローバル例外マッピング
問題の詳細形式のペイロードを一貫して返します。

```java
// Compile: javac --release 22 …
package com.example.demo.web.error;

import java.time.Instant;
import java.util.Map;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

@RestControllerAdvice
public class ApiExceptionHandler {

  @ExceptionHandler(MethodArgumentNotValidException.class)
  public ResponseEntity<Map<String, Object>> handleValidation(MethodArgumentNotValidException ex) {
    String message =
        ex.getBindingResult().getFieldErrors().stream()
            .findFirst()
            .map(err -> err.getField() + ": " + err.getDefaultMessage())
            .orElse("Validation failed");
    return ResponseEntity.badRequest()
        .body(
            Map.of(
                "timestamp", Instant.now().toString(),
                "status", HttpStatus.BAD_REQUEST.value(),
                "error", "Bad Request",
                "message", message));
  }

  @ExceptionHandler(IllegalArgumentException.class)
  public ResponseEntity<Map<String, Object>> handleIllegalArgument(IllegalArgumentException ex) {
    return ResponseEntity.badRequest()
        .body(
            Map.of(
                "timestamp", Instant.now().toString(),
                "status", HttpStatus.BAD_REQUEST.value(),
                "message", ex.getMessage()));
  }
}
```

## 6. CORS (ブラウザが API を呼び出すとき)
単純なデモの場合のみ — 実稼働環境でのオリジンを強化します。

```java
// Compile: javac --release 22 …
@RestController
@CrossOrigin(origins = "http://localhost:5173")
@RequestMapping("/api/public")
public class PublicFeedController { /* … */ }
```

好む **`WebMvcConfigurer.addCorsMappings`** または複数のコントローラーの場合はゲートウェイ レベルの CORS。

## 7. 関連メモ

- **セキュリティの基本とフィルター チェーン** — [基本とフィルター チェーン](security-basics-and-filter-chain.md) (JWT、HTTP 開発用の基本、メソッドのセキュリティ)
- **問題の詳細を含むグローバル エラー** — ペア **`@ControllerAdvice`** と **`ProblemDetail`** (Spring 6+) 新しい API の RFC 7807 応答用

---
label: "Security"
subtitle: "基本とフィルターチェーン"
group: "Spring Boot"
groupOrder: 2
order: 7
---
Spring Boot — セキ​​ュリティの基本

**Spring Security** を追加して、HTTP エンドポイントを保護し、最小限のログインまたは JWT フローを公開し、運用環境で Actuator をロックダウンします。

**Java ベースライン:** **Java SE 22** (`javac --release 22`);例は **Spring Boot 3.x** をターゲットとしています。

## 1. 依存関係

**メイビン:**

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

**グラドル(`build.gradle.kts`):**

```kotlin
dependencies {
  implementation("org.springframework.boot:spring-boot-starter-security")
}
```

このスターターがクラスパス上にある場合、ブートは **フィルター チェーン** を自動構成します。すべてのリクエストはコントローラーが実行される前にそれを通過します。

## 2. ステートレス API と JWT (スケッチ)

REST API の場合は、**ステートレス** セッションを優先します。リクエストごとにベアラー トークンを検証します。

```java
// Compile: javac --release 22 …
package com.example.demo.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class SecurityConfig {

  @Bean
  SecurityFilterChain api(HttpSecurity http) throws Exception {
    return http
        .csrf(csrf -> csrf.disable()) // common for pure JSON APIs; revisit if you use cookies
        .sessionManagement(sm -> sm.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/actuator/health").permitAll()
            .requestMatchers("/api/public/**").permitAll()
            .anyRequest().authenticated())
        .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()))
        .build();
  }
}
```

- **`oauth2ResourceServer().jwt()`** JWTs を検証するのは **`spring-boot-starter-oauth2-resource-server`** が存在し、**`spring.security.oauth2.resourceserver.jwt.issuer-uri`** (または JWK セット) が構成されています。
- IdP (Auth0、Keycloak、Cognito) または専用の認証サービスを使用してトークンを発行します。このパターンでは、ブートはトークンの作成ではなく **検証** に重点を置きます。

## 3. 開発専用 HTTP 基本

IdP を使用しないローカル デモの場合は、メモリ内ユーザーで十分です。ハードコードされたパスワードを**決して**配布しないでください。

```java
// Compile: javac --release 22 …
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Profile;
import org.springframework.security.config.Customizer;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
@Profile("dev")
class DevSecurityConfig {

  @Bean
  SecurityFilterChain devChain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(auth -> auth.anyRequest().authenticated())
        .httpBasic(Customizer.withDefaults())
        .build();
  }

  @Bean
  UserDetailsService users() {
    return new InMemoryUserDetailsManager(
        User.withUsername("dev").password("{noop}dev").roles("USER").build());
  }
}
```

**`{noop}`** は委任エンコーダのパスワード プレフィックスです。** でのみ使用できます。`dev`** プロフィール。

## 4. メソッドレベルの認可

認証後、サービスメソッドをロールごとに制限します。

```java
// Compile: javac --release 22 …
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Service;

@Service
public class AdminService {

  @PreAuthorize("hasRole('ADMIN')")
  public void purgeStaleData() {
    // ...
  }
}
```

**で有効にする`@EnableMethodSecurity`** の **`@Configuration`** クラス。

## 5. 製造チェックリスト

|リスク |緩和 |
|------|-----------|
|開ける **`/actuator/env`** または **`prometheus`** |セキュリティ + ネットワーク ポリシーによる制限 — **パート VI (テストと運用)** を参照してください。
| CSRF Cookie セッション |ブラウザ フォームに対して CSRF を有効にしておきます。仕様によりトークン APIs に対してのみ無効になります。
| **の秘密`application.yml`** |環境変数 / シークレット マネージャー — **パート II (YAML および外部構成)** を参照してください。
| HTTPS が見つかりません |入口または本番環境の埋め込みコネクタで TLS を終了します。

## 6. 関連メモ

- **REST コントローラー** — [REST コントローラー](iv-rest-controllers.md) (検証、問題の詳細)
- **YAML とプロファイル** — [YAML と外部構成](ii-yaml-and-external-config.md)
- **テスト** — **を使用します`@SpringBootTest`** + **`@AutoConfigureMockMvc`** と **`@WithMockUser`** または JWT フィクスチャをテストします。 **`@WebMvcTest`** 単独では、設定されていない限り完全なセキュリティ チェーンをロードしません。

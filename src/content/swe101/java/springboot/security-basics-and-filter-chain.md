---
label: "Security"
subtitle: "Basics & filter chain"
group: "Spring Boot"
groupOrder: 2
order: 7
---
Spring Boot — Security basics
Add **Spring Security** to protect HTTP endpoints, expose a minimal login or JWT flow, and lock down Actuator in production.

**Java baseline:** **Java SE 22** (`javac --release 22`); examples target **Spring Boot 3.x**.

## 1. Dependency

**Maven:**

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-security</artifactId>
</dependency>
```

**Gradle (`build.gradle.kts`):**

```kotlin
dependencies {
  implementation("org.springframework.boot:spring-boot-starter-security")
}
```

Boot auto-configures a **filter chain** when this starter is on the classpath — every request passes through it before your controller runs.

## 2. Stateless API with JWT (sketch)

For REST APIs, prefer **stateless** sessions: validate a bearer token on each request.

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

- **`oauth2ResourceServer().jwt()`** validates JWTs when **`spring-boot-starter-oauth2-resource-server`** is present and **`spring.security.oauth2.resourceserver.jwt.issuer-uri`** (or JWK set) is configured.
- Issue tokens with your IdP (Auth0, Keycloak, Cognito) or a dedicated auth service — Boot focuses on **validation**, not minting tokens, in this pattern.

## 3. Development-only HTTP Basic

For local demos without an IdP, an in-memory user is enough — **never** ship hard-coded passwords:

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

**`{noop}`** is a password prefix for the delegating encoder — acceptable only in **`dev`** profiles.

## 4. Method-level authorization

After authentication, restrict by role on service methods:

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

Enable with **`@EnableMethodSecurity`** on a **`@Configuration`** class.

## 5. Production checklist

| Risk | Mitigation |
|------|------------|
| Open **`/actuator/env`** or **`prometheus`** | Restrict with Security + network policy — see **Part VI (Testing & operations)** |
| CSRF on cookie sessions | Keep CSRF enabled for browser forms; disable only for token APIs by design |
| Secrets in **`application.yml`** | Env vars / secret manager — see **Part II (YAML & external config)** |
| Missing HTTPS | Terminate TLS at ingress or embedded connector in prod |

## 6. Related notes

- **REST controllers** — [REST controllers](iv-rest-controllers.md) (validation, Problem Details)
- **YAML & profiles** — [YAML & external config](ii-yaml-and-external-config.md)
- **Testing** — use **`@SpringBootTest`** + **`@AutoConfigureMockMvc`** with **`@WithMockUser`** or test JWT fixtures; **`@WebMvcTest`** alone does not load the full security chain unless configured

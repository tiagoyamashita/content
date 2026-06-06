---
label: "I"
subtitle: "イントロとプロジェクトのレイアウト"
group: "スプリングブーツ"
groupOrder: 2
order: 1
---
Spring Boot — パート I

Boot が Spring に何を追加するか、エントリポイントがコンテナをブートストラップする方法、スキャンと自動構成が予測どおりに動作するようにパッケージをレイアウトする方法。

**このセクションの構成:** 最初に **Java** イントロ トラック (`intro/`、パート I ～ VI) を完了してから、これらの **Spring Boot** ページを順番に実行してください。 **例 (Web MVC)** のコピー＆ペースト レイアウトは **`springboot/`** に存在します。 **セキュリティの基本**は、操作前の REST トピックの後に続きます。

**JDK / Java 言語レベル:** この **Spring Boot** トラックの例は **Java SE 22** を前提としています。**`javac --release 22`** を使用するか、ビルドで言語レベル **22** を設定します (`pom.xml` / `build.gradle`)。ファイルが新しい機能を呼び出さない限り、同じスニペットが **JDK 21 LTS** でコンパイルされます。運用環境のサービスについては、組織が新しいリリースで標準化している場合を除き、サポートされている **LTS** JDK を優先してください。

## 1. ブートによって解決される問題
- **クラスパス地獄**: スターター (例: `spring-boot-starter-web`) は、サーブレット API、Jackson、Tomcat の互換性のあるバージョンをピン留めします。
- **組み込みサーバー**: Tomcat を個別にインストールせずに `java -jar app.jar` を実行します。
- **自動構成**: Hibernate + データソースがクラスパス上にある場合、オプトアウトしない限り、**`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`** (ブート 3.x) によって JPA セットアップが表示されます。

## 2. 最小限のアプリケーション エントリポイント
`@SpringBootApplication` は、宣言クラスのパッケージの **`@SpringBootConfiguration`** (特殊化された `@Configuration`)、**`@EnableAutoConfiguration`**、および **`@ComponentScan`** の短縮形です。

```java
// Compile: javac --release 22 …
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }
}
```

- **`SpringApplication.run`** は **`ApplicationContext`** を構築し、**`ApplicationRunner`** / **`CommandLineRunner`** Bean を実行し、**`spring-boot-starter-web`** が存在する場合に Web サーバーを起動します。

## 3. コンポーネントのスキャン規則
- **`com.example.demo`** および **サブパッケージ** の下のタイプのみがデフォルトでスキャンされます (`@SpringBootApplication` と同じパッケージ)。
- **`@SpringBootApplication`** を **`com.example.demo`** に配置したが、コントローラが **`com.example.api`** に存在する場合、**`@ComponentScan("com.example.api")`** を追加するか、**`demo`** の下にコードを移動しない限り、それらは **Bean になりません**。

```java
// Compile: javac --release 22 …
@SpringBootApplication
@ComponentScan(basePackages = "com.example")
public class DemoApplication { /* ... */ }
```

## 4. 典型的な Maven 座標 (概念的)
通常、`pom.xml` は **`spring-boot-starter-parent`** (または **`spring-boot-dependencies`** による BOM) とスターターを宣言します。

```xml
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
```

**グラドル (`build.gradle.kts`):**

```kotlin
plugins {
  id("org.springframework.boot") version "3.4.0"
  id("io.spring.dependency-management") version "1.1.6"
  kotlin("jvm") version "2.0.21" // optional; Java-only projects omit
  java
}

dependencies {
  implementation("org.springframework.boot:spring-boot-starter-web")
  implementation("org.springframework.boot:spring-boot-starter-data-jpa")
}
```

Maven と同じアーティファクト ID を使用します。 Spring Boot Gradle プラグインは、調整されたバージョンの BOM を適用します。

## 5. 階層化パッケージ（推奨形状）
共通のレイアウトにより、**Web**、**アプリケーション/サービス**、**永続性**に関する懸念が分離されます。

```
com.example.demo
  DemoApplication.java
  config/          ← @Configuration classes, property beans
  web/             ← @RestController, DTOs used at the boundary
  service/         ← @Service, transactions
  domain/          ← entities / domain models (optional)
  persistence/     ← @Repository, JPA adapters
```

コントローラーはサービスに依存します。サービスはリポジトリまたはポートに依存します。ビジネス ルールが増大する場合、コントローラがリポジトリを直接挿入することは**避けてください**。

## 6. 自動構成のスライスを無効にする
移行またはテスト中に自動構成が邪魔になる場合:

```java
// Compile: javac --release 22 …
@SpringBootApplication(exclude = DataSourceAutoConfiguration.class)
public class DemoApplication { /* ... */ }
```

最初にクラスパス/プロパティを修正することをお勧めします。 **`exclude`** は意図的な避難ハッチです。
�

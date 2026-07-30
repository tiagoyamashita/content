---
label: "I"
subtitle: "イントロとプロジェクトのレイアウト"
group: "Spring Boot"
groupOrder: 2
order: 1
---
Spring Boot — パート I

Boot が Spring に何を追加するか、エントリポイントがコンテナをブートストラップする方法、スキャンと自動構成が予測どおりに動作するようにパッケージをレイアウトする方法。

**このセクションの構成:** **Java** イントロ トラックを完成させます (`intro/`、パート I–VI) を最初に読んでから、これらの **Spring Boot** ページを順番に読んでください。 **例 (Web MVC)** のコピー＆ペースト レイアウトは ** にあります`springboot/`**; **セキュリティの基本**は、運用トピックの前に REST に続きます。

**JDK / Java 言語レベル:** この **Spring Boot** トラックの例では **Java SE 22** を想定しています — ** を使用してください`javac --release 22`** またはビルドで言語レベル **22** を設定します (`pom.xml`/`build.gradle`）。ファイルが新しい機能を呼び出さない限り、同じスニペットが **JDK 21 LTS** でコンパイルされます。運用環境のサービスについては、組織が新しいリリースで標準化している場合を除き、サポートされている **LTS** JDK を優先してください。

## 1. ブートによって解決される問題
- **クラスパス地獄**: スターター (例:`spring-boot-starter-web`) サーブレット API、Jackson、Tomcat のピン互換バージョン。
- **組み込みサーバー**: 実行`java -jar app.jar`Tomcat を別途インストールする必要はありません。
- **自動構成**: Hibernate + データソースがクラスパス上にある場合、オプトアウトしない限り JPA セットアップが表示されます — ** によって駆動されます`META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`** (ブート 3.x)。

## 2. 最小限のアプリケーション エントリポイント`@SpringBootApplication`** の省略形です`@SpringBootConfiguration`** (特殊な`@Configuration`)、**`@EnableAutoConfiguration`**、 そして **`@ComponentScan`** 宣言クラスのパッケージ上。

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

- **`SpringApplication.run`** は ** を構築します`ApplicationContext`**、実行**`ApplicationRunner`** / **`CommandLineRunner`** Bean、および ** のときに Web サーバーを起動します`spring-boot-starter-web`**が存在します。

## 3. コンポーネントのスキャン規則
- ** 以下のタイプのみ`com.example.demo`** および ** サブパッケージ** はデフォルトでスキャンされます (同じパッケージ`@SpringBootApplication`）。
- **を入力した場合`@SpringBootApplication`** で **`com.example.demo`** ただし、コントローラーは ** に存在します`com.example.api`**、** を追加しない限り、**豆になりません**`@ComponentScan("com.example.api")`** またはコードを ** の下に移動します`demo`**。

```java
// Compile: javac --release 22 …
@SpringBootApplication
@ComponentScan(basePackages = "com.example")
public class DemoApplication { /* ... */ }
```

## 4. 典型的な Maven 座標 (概念的)
あなたの`pom.xml`通常は ** を宣言します`spring-boot-starter-parent`** (または ** 経由の BOM`spring-boot-dependencies`**) さらにスターター:

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

**グラドル(`build.gradle.kts`):**

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

Maven と同じアーティファクト ID を使用します。 Spring Boot Gradle プラグインは、アライメントされたバージョンに BOM を適用します。

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

最初にクラスパス/プロパティを修正することをお勧めします。 **`exclude`**は意図的な避難用ハッチです。

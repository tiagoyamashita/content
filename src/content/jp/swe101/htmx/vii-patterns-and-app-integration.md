---
label: "VII"
subtitle: "パターンとアプリ統合"
group: "HTMX"
order: 7
---
HTMX — パターンとアプリ統合

Common UI patterns map cleanly to **partials + swap**. Recipes for pagination, inline edit, modals, and integration with **Spring Boot**, **Flask**, and **FastAPI**.

## 1. Pagination

Use **`hx-trigger="revealed"`** for infinite scroll or a “Next” button with **`beforeend`** into list container.

## 2. Inline edit

**`hx-get`** returns edit form partial; POST returns updated row with **`outerHTML`** swap.

## 3. Spring Boot + Thymeleaf

**`@Controller`** returns fragment template when **`HX-Request`** header is true. See [REST controllers](../java/springboot/iv-rest-controllers.md).

## 4. Flask / FastAPI + Jinja2

Same route checks **`request.headers.get("HX-Request")`** and picks partial vs full template.

## 5. Testing

Request with **`HX-Request: true`**; assert partial HTML. Use Playwright for integration tests.

## Next

Continue with [When to use & tradeoffs](viii-when-to-use-and-tradeoffs.md) for architecture decisions vs SPAs.

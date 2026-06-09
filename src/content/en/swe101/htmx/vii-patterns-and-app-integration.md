---
label: "VII"
subtitle: "Patterns & app integration"
group: "HTMX"
order: 7
---
HTMX — patterns & app integration
Common UI patterns map cleanly to **partials + swap**. Below: recurring recipes and how they fit **Spring Boot**, **Flask**, and **FastAPI** — aligned with tracks elsewhere in SWE101.

## 1. Pagination

```html
<div id="page-2"
     hx-get="/items?page=2"
     hx-trigger="revealed"
     hx-swap="afterend">
  Loading…
</div>
```

Or explicit “Next” button with **`beforeend`** into list container. Server returns next page rows only.

## 2. Inline edit

```html
<tr id="row-5">
  <td colspan="3">
    <span hx-get="/items/5/edit" hx-target="closest tr" hx-swap="outerHTML">Widget</span>
  </td>
</tr>
```

Edit partial returns `<tr>…form…</tr>`; save POST returns updated row or list cell.

## 3. Modal / drawer

```html
<button hx-get="/items/new" hx-target="#modal-body" hx-on::after-swap="document.getElementById('modal').showModal()">
  New item
</button>
<dialog id="modal">
  <div id="modal-body"></div>
</dialog>
```

Close on success via **`HX-Trigger: closeModal`** and a listener, or return empty swap + **`htmx:afterSwap`** to call **`close()`**.

## 4. Active search

```html
<input type="search" name="q"
       hx-get="/items/search"
       hx-trigger="keyup changed delay:200ms, search"
       hx-target="#results"
       hx-indicator="#search-spinner">
```

Debounce prevents request storms; **`search`** event fires on clear (WebKit).

## 5. Tabs

Each tab link **`hx-get`** loads panel into **`#tab-content`**. Server marks active tab in partial. Alternative: all panels in DOM, **`hx-swap="none"`** + **`class`** toggle via **`HX-Trigger`**.

## 6. Spring Boot + Thymeleaf

```java
@Controller
@RequestMapping("/orders")
public class OrderController {
  @GetMapping
  public String list(@RequestParam(defaultValue = "0") int page, Model model,
                     @RequestHeader(value = "HX-Request", defaultValue = "false") boolean htmx) {
    model.addAttribute("orders", orderService.page(page));
    return htmx ? "orders/_rows :: rows" : "orders/list";
  }

  @PostMapping
  public String create(@Valid @ModelAttribute OrderForm form, BindingResult br, Model model) {
    if (br.hasErrors()) {
      return "orders/_form :: form";  // 422 if configured
    }
    orderService.create(form);
    model.addAttribute("orders", orderService.recent());
    return "orders/_rows :: rows";
  }
}
```

See [REST controllers](../java/springboot/iv-rest-controllers.md) for JSON APIs; HTMX routes can live on **`@Controller`** (HTML) beside **`@RestController`** (JSON) if you must support both.

## 7. Flask + Jinja2

```python
@app.get("/orders")
def orders():
    page = int(request.args.get("page", 0))
    rows = render_template("orders/_rows.html", orders=Order.page(page))
    if request.headers.get("HX-Request"):
        return rows
    return render_template("orders/list.html", orders=Order.page(page))
```

Pair with [Python](../python/i-basics-and-syntax.md) track for project layout and testing.

## 8. FastAPI + Jinja2

```python
@app.get("/orders", response_class=HTMLResponse)
async def orders(request: Request, page: int = 0):
    ctx = {"orders": await fetch_orders(page)}
    tpl = "orders/_rows.html" if request.headers.get("HX-Request") else "orders/list.html"
    return templates.TemplateResponse(tpl, {"request": request, **ctx})
```

Async DB fits long-polling or SSE endpoints on the same app.

## 9. Testing

| Layer | Approach |
|-------|----------|
| **Server** | Request with `HX-Request: true`; assert partial HTML |
| **Integration** | Playwright — click, assert DOM region |
| **No JS unit tests** | Behavior lives in templates + routes |

```python
def test_create_row(client):
    r = client.post("/items", data={"title": "A"}, headers={"HX-Request": "true"})
    assert r.status_code == 200
    assert "<li" in r.text
```

## 10. Folder layout (shared pattern)

```text
templates/
  layout.html
  orders/
    list.html       # full page
    _rows.html      # partial
    _form.html      # partial
static/
  htmx.min.js
  app.css
```

Leading **`_`** convention marks partials not meant for direct navigation.

## Next

Continue with [When to use & tradeoffs](viii-when-to-use-and-tradeoffs.md) for architecture decisions vs SPAs.

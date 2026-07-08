---
label: "IX"
subtitle: "Examples"
group: "HTMX"
order: 9
---
HTMX — examples
Runnable mini-apps below. **Click a file** in the left tree to load its source on the right. Copy into a folder and run — comments in the code explain each piece.

<style>
.notes-code-explorer{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:12px;line-height:1.45;border:1px solid #3f3f46;border-radius:8px;overflow:hidden;margin:1.25rem 0;background:#18181b;color:#e4e4e7}
.notes-code-explorer input[type=radio]{position:absolute;opacity:0;pointer-events:none}
.notes-code-explorer .nce-layout{display:grid;grid-template-columns:minmax(160px,28%) 1fr;min-height:280px}
.notes-code-explorer .nce-tree{padding:.65rem 0;border-right:1px solid #3f3f46;background:#09090b;overflow:auto;max-height:520px}
.notes-code-explorer .nce-tree label{display:block;padding:.2rem .75rem;cursor:pointer;color:#a1a1aa;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.notes-code-explorer .nce-tree label:hover{background:#27272a;color:#fafafa}
.notes-code-explorer .nce-tree .nce-dir{padding:.35rem .75rem .1rem;font-size:10px;text-transform:uppercase;letter-spacing:.04em;color:#71717a;pointer-events:none}
.notes-code-explorer .nce-tree .nce-indent-1{padding-left:1.25rem}
.notes-code-explorer .nce-tree .nce-indent-2{padding-left:2rem}
.notes-code-explorer .nce-tree .nce-indent-3{padding-left:2.75rem}
.notes-code-explorer .nce-tree .nce-indent-4{padding-left:3.5rem}
.notes-code-explorer .nce-panel{display:none;padding:0;margin:0;overflow:auto;max-height:520px;background:#18181b}
.notes-code-explorer .nce-panel pre{margin:0;padding:.85rem 1rem;white-space:pre;tab-size:2}
.notes-code-explorer .nce-cap{padding:.5rem .75rem;border-bottom:1px solid #3f3f46;background:#27272a;font-size:11px;color:#d4d4d8}
.notes-code-explorer .nce-run{margin:.5rem 0 1.5rem;font-size:13px;color:#a1a1aa}
</style>

## Example 1 — Hello swap

<p class="nce-run"><strong>Run:</strong> <code>pip install flask</code> → <code>python app.py</code> → <code>http://127.0.0.1:5000</code></p>

<div class="notes-code-explorer">
<input type="radio" name="ex1" id="ex1-app" checked>
<input type="radio" name="ex1" id="ex1-req">
<input type="radio" name="ex1" id="ex1-index">
<div class="nce-cap">hello-swap/</div>
<div class="nce-layout">
<nav class="nce-tree" aria-label="hello-swap files">
<label for="ex1-app" class="nce-indent-1">app.py</label>
<label for="ex1-req" class="nce-indent-1">requirements.txt</label>
<div class="nce-dir nce-indent-1">templates/</div>
<label for="ex1-index" class="nce-indent-2">index.html</label>
</nav>
<div class="nce-panels">
<div class="nce-panel" id="ex1-panel-app"><pre># Minimal Flask server — one route returns an HTML fragment (not a full page).
from flask import Flask, render_template

app = Flask(__name__)

@app.get("/")
def index():
    # Full page on first visit; includes HTMX script and a target div.
    return render_template("index.html")

@app.get("/hello")
def hello():
    # HTMX hx-get="/hello" expects a snippet to swap into #out — no &lt;html&gt; wrapper.
    return "&lt;p&gt;Hello from the server — no full reload.&lt;/p&gt;"

if __name__ == "__main__":
    app.run(debug=True)</pre></div>
<div class="nce-panel" id="ex1-panel-req"><pre># Pin Flask for reproducible installs: pip install -r requirements.txt
flask&gt;=3.0,&lt;4</pre></div>
<div class="nce-panel" id="ex1-panel-index"><pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
  &lt;meta charset="utf-8"&gt;
  &lt;title&gt;Hello HTMX&lt;/title&gt;
  &lt;!-- HTMX 2.x from CDN; pin version in production --&gt;
  &lt;script src="https://unpkg.com/htmx.org@2.0.4" defer&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body&gt;
  &lt;!-- hx-get: URL to fetch; hx-target: where response HTML goes --&gt;
  &lt;button hx-get="/hello" hx-target="#out"&gt;Say hello&lt;/button&gt;
  &lt;div id="out"&gt;&lt;/div&gt;  &lt;!-- empty until first swap --&gt;
&lt;/body&gt;
&lt;/html&gt;</pre></div>
</div>
</div>
</div>

<style>
#ex1-app:checked ~ .nce-layout .nce-tree label[for=ex1-app],
#ex1-req:checked ~ .nce-layout .nce-tree label[for=ex1-req],
#ex1-index:checked ~ .nce-layout .nce-tree label[for=ex1-index]{background:#27272a;color:#fafafa;border-left:2px solid #22c55e}
#ex1-app:checked ~ .nce-layout #ex1-panel-app,
#ex1-req:checked ~ .nce-layout #ex1-panel-req,
#ex1-index:checked ~ .nce-layout #ex1-panel-index{display:block}
</style>

## Example 2 — Todo list (CRUD partials)

<p class="nce-run"><strong>Run:</strong> same as above — in-memory list resets on restart.</p>

<div class="notes-code-explorer">
<input type="radio" name="ex2" id="ex2-app" checked>
<input type="radio" name="ex2" id="ex2-req">
<input type="radio" name="ex2" id="ex2-layout">
<input type="radio" name="ex2" id="ex2-page">
<input type="radio" name="ex2" id="ex2-list">
<input type="radio" name="ex2" id="ex2-form">
<input type="radio" name="ex2" id="ex2-row">
<div class="nce-cap">todo-crud/</div>
<div class="nce-layout">
<nav class="nce-tree" aria-label="todo-crud files">
<label for="ex2-app" class="nce-indent-1">app.py</label>
<label for="ex2-req" class="nce-indent-1">requirements.txt</label>
<div class="nce-dir nce-indent-1">templates/</div>
<label for="ex2-layout" class="nce-indent-2">layout.html</label>
<div class="nce-dir nce-indent-2">pages/</div>
<label for="ex2-page" class="nce-indent-3">index.html</label>
<div class="nce-dir nce-indent-2">partials/</div>
<label for="ex2-list" class="nce-indent-3">_list.html</label>
<label for="ex2-form" class="nce-indent-3">_form.html</label>
<label for="ex2-row" class="nce-indent-3">_row.html</label>
</nav>
<div class="nce-panels">
<div class="nce-panel" id="ex2-panel-app"><pre># Flask app: full pages vs HTMX partials.
from flask import Flask, render_template, request, make_response

app = Flask(__name__)
_todos = []  # demo store — replace with DB in real apps
_next_id = 1

def _partial(name, **ctx):
    # Shorthand: always render from partials/ folder.
    return render_template(f"partials/{name}", **ctx)

@app.get("/")
def index():
    # Full page wraps list + form; partials reused for HTMX responses.
    return render_template("pages/index.html", todos=_todos)

@app.get("/todos")
def todos_list():
    # HTMX refresh of entire list (e.g. after bulk action).
    return _partial("_list.html", todos=_todos)

@app.post("/todos")
def todos_create():
    global _next_id
    title = (request.form.get("title") or "").strip()
    if len(title) &lt; 2:
        # 422 + HX-Retarget: swap validation HTML into #todo-form, not #todo-mount.
        body = _partial("_form.html", error="Title must be at least 2 characters", title=title)
        resp = make_response(body, 422)
        resp.headers["HX-Retarget"] = "#todo-form"
        resp.headers["HX-Reswap"] = "innerHTML"
        return resp
    _todos.append({"id": _next_id, "title": title, "done": False})
    _next_id += 1
    # Return updated list HTML; hx-target="#todo-mount" replaces the list region.
    return _partial("_list.html", todos=_todos)

@app.post("/todos/&lt;int:tid&gt;/toggle")
def todos_toggle(tid):
    for t in _todos:
        if t["id"] == tid:
            t["done"] = not t["done"]
            break
    # Swap single row only — hx-target="closest li" on the button.
    t = next(x for x in _todos if x["id"] == tid)
    return _partial("_row.html", todo=t)

@app.delete("/todos/&lt;int:tid&gt;")
def todos_delete(tid):
    global _todos
    _todos = [t for t in _todos if t["id"] != tid]
    # Empty body; button uses hx-swap="delete" to remove the &lt;li&gt;.
    return "", 200

if __name__ == "__main__":
    app.run(debug=True)</pre></div>
<div class="nce-panel" id="ex2-panel-req"><pre># pip install -r requirements.txt
flask&gt;=3.0,&lt;4</pre></div>
<div class="nce-panel" id="ex2-panel-layout"><pre>{# Shared chrome: HTMX script once, block for page body #}
&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
  &lt;meta charset="utf-8"&gt;
  &lt;title&gt;{% block title %}Todos{% endblock %}&lt;/title&gt;
  &lt;script src="https://unpkg.com/htmx.org@2.0.4" defer&gt;&lt;/script&gt;
  &lt;style&gt;
    body { font-family: system-ui, sans-serif; max-width: 32rem; margin: 2rem auto; }
    .error { color: #b91c1c; font-size: 0.875rem; }
    .done { text-decoration: line-through; color: #71717a; }
  &lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
  {% block content %}{% endblock %}
  &lt;script&gt;
    // HTMX treats 4xx as errors and skips swap by default — allow 422 validation HTML.
    document.body.addEventListener("htmx:beforeSwap", (e) =&gt; {
      if (e.detail.xhr.status === 422) {
        e.detail.shouldSwap = true;
        e.detail.isError = false;
      }
    });
  &lt;/script&gt;
&lt;/body&gt;
&lt;/html&gt;</pre></div>
<div class="nce-panel" id="ex2-panel-page"><pre>{# Full page: includes partials — same markup HTMX endpoints return #}
{% extends "layout.html" %}
{% block content %}
&lt;h1&gt;Todos&lt;/h1&gt;
{# Form partial — also returned on 422 into #todo-form via HX-Retarget #}
&lt;div id="todo-form"&gt;
  {% include "partials/_form.html" %}
&lt;/div&gt;
{# Stable mount point — create refreshes list; rows use closest li #}
&lt;div id="todo-mount"&gt;
  {% include "partials/_list.html" %}
&lt;/div&gt;
{% endblock %}</pre></div>
<div class="nce-panel" id="ex2-panel-list"><pre>{# Fragment: full &lt;ul&gt; swapped into #todo-mount on create #}
&lt;ul&gt;
  {% for todo in todos %}
    {% include "partials/_row.html" %}
  {% else %}
    &lt;li&gt;No todos yet.&lt;/li&gt;
  {% endfor %}
&lt;/ul&gt;</pre></div>
<div class="nce-panel" id="ex2-panel-form"><pre>{# Fragment: bare form — included in page; alone on 422 (into #todo-form) #}
&lt;form hx-post="/todos"
      hx-target="#todo-mount"
      hx-swap="innerHTML"&gt;
  &lt;input name="title" placeholder="New todo" value="{{ title or '' }}" required&gt;
  &lt;button type="submit"&gt;Add&lt;/button&gt;
  {% if error %}&lt;p class="error"&gt;{{ error }}&lt;/p&gt;{% endif %}
&lt;/form&gt;</pre></div>
<div class="nce-panel" id="ex2-panel-row"><pre>{# Fragment: one &lt;li&gt; — toggle swaps row; delete removes it #}
&lt;li id="todo-{{ todo.id }}"&gt;
  &lt;span class="{{ 'done' if todo.done else '' }}"&gt;{{ todo.title }}&lt;/span&gt;
  {# closest li = this row; outerHTML replaces entire &lt;li&gt; after toggle #}
  &lt;button hx-post="/todos/{{ todo.id }}/toggle"
          hx-target="closest li"
          hx-swap="outerHTML"&gt;
    Toggle
  &lt;/button&gt;
  {# delete swap removes target element; no response body needed #}
  &lt;button hx-delete="/todos/{{ todo.id }}"
          hx-target="closest li"
          hx-swap="delete"
          hx-confirm="Delete this todo?"&gt;
    Delete
  &lt;/button&gt;
&lt;/li&gt;</pre></div>
</div>
</div>
</div>

<style>
#ex2-app:checked ~ .nce-layout .nce-tree label[for=ex2-app],
#ex2-req:checked ~ .nce-layout .nce-tree label[for=ex2-req],
#ex2-layout:checked ~ .nce-layout .nce-tree label[for=ex2-layout],
#ex2-page:checked ~ .nce-layout .nce-tree label[for=ex2-page],
#ex2-list:checked ~ .nce-layout .nce-tree label[for=ex2-list],
#ex2-form:checked ~ .nce-layout .nce-tree label[for=ex2-form],
#ex2-row:checked ~ .nce-layout .nce-tree label[for=ex2-row]{background:#27272a;color:#fafafa;border-left:2px solid #22c55e}
#ex2-app:checked ~ .nce-layout #ex2-panel-app,
#ex2-req:checked ~ .nce-layout #ex2-panel-req,
#ex2-layout:checked ~ .nce-layout #ex2-panel-layout,
#ex2-page:checked ~ .nce-layout #ex2-panel-page,
#ex2-list:checked ~ .nce-layout #ex2-panel-list,
#ex2-form:checked ~ .nce-layout #ex2-panel-form,
#ex2-row:checked ~ .nce-layout #ex2-panel-row{display:block}
</style>

## Example 3 — Live search

<p class="nce-run"><strong>Run:</strong> type in the box — requests debounce 300ms; URL updates for shareable searches.</p>

<div class="notes-code-explorer">
<input type="radio" name="ex3" id="ex3-app" checked>
<input type="radio" name="ex3" id="ex3-req">
<input type="radio" name="ex3" id="ex3-index">
<input type="radio" name="ex3" id="ex3-results">
<div class="nce-cap">live-search/</div>
<div class="nce-layout">
<nav class="nce-tree" aria-label="live-search files">
<label for="ex3-app" class="nce-indent-1">app.py</label>
<label for="ex3-req" class="nce-indent-1">requirements.txt</label>
<div class="nce-dir nce-indent-1">templates/</div>
<label for="ex3-index" class="nce-indent-2">index.html</label>
<div class="nce-dir nce-indent-2">partials/</div>
<label for="ex3-results" class="nce-indent-3">_results.html</label>
</nav>
<div class="nce-panels">
<div class="nce-panel" id="ex3-panel-app"><pre># Filtered search — GET + query string; HTMX sends input automatically.
from flask import Flask, render_template, request

app = Flask(__name__)
_ITEMS = [
    {"name": "Redis", "tag": "cache"},
    {"name": "Postgres", "tag": "sql"},
    {"name": "MongoDB", "tag": "document"},
    {"name": "HTMX", "tag": "ui"},
    {"name": "Flask", "tag": "python"},
]

@app.get("/")
def index():
    q = request.args.get("q", "")
    return render_template("index.html", q=q, items=_filter(q))

@app.get("/search")
def search():
    # Only the results region is returned for HTMX — not the full page.
    q = request.args.get("q", "")
    return render_template("partials/_results.html", items=_filter(q), q=q)

def _filter(q):
    q = q.lower().strip()
    if not q:
        return _ITEMS
    return [i for i in _ITEMS if q in i["name"].lower() or q in i["tag"]]

if __name__ == "__main__":
    app.run(debug=True)</pre></div>
<div class="nce-panel" id="ex3-panel-req"><pre># pip install -r requirements.txt
flask&gt;=3.0,&lt;4</pre></div>
<div class="nce-panel" id="ex3-panel-index"><pre>&lt;!DOCTYPE html&gt;
&lt;html lang="en"&gt;
&lt;head&gt;
  &lt;meta charset="utf-8"&gt;
  &lt;title&gt;Search&lt;/title&gt;
  &lt;script src="https://unpkg.com/htmx.org@2.0.4" defer&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body&gt;
  &lt;input type="search" name="q" value="{{ q }}"
         placeholder="Filter stack…"
         {# changed = skip duplicate requests; delay = debounce keystrokes #}
         hx-get="/search"
         hx-trigger="keyup changed delay:300ms, search"
         hx-target="#results"
         {# sync ?q= in address bar for bookmark / back button #}
         hx-push-url="true"
         autofocus&gt;
  &lt;div id="results"&gt;
    {% include "partials/_results.html" %}
  &lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;</pre></div>
<div class="nce-panel" id="ex3-panel-results"><pre>{# Results partial — swapped on every debounced keystroke #}
{% if items %}
  &lt;ul&gt;
    {% for item in items %}
      &lt;li&gt;&lt;strong&gt;{{ item.name }}&lt;/strong&gt; — {{ item.tag }}&lt;/li&gt;
    {% endfor %}
  &lt;/ul&gt;
{% else %}
  &lt;p&gt;No matches for "{{ q }}".&lt;/p&gt;
{% endif %}</pre></div>
</div>
</div>
</div>

<style>
#ex3-app:checked ~ .nce-layout .nce-tree label[for=ex3-app],
#ex3-req:checked ~ .nce-layout .nce-tree label[for=ex3-req],
#ex3-index:checked ~ .nce-layout .nce-tree label[for=ex3-index],
#ex3-results:checked ~ .nce-layout .nce-tree label[for=ex3-results]{background:#27272a;color:#fafafa;border-left:2px solid #22c55e}
#ex3-app:checked ~ .nce-layout #ex3-panel-app,
#ex3-req:checked ~ .nce-layout #ex3-panel-req,
#ex3-index:checked ~ .nce-layout #ex3-panel-index,
#ex3-results:checked ~ .nce-layout #ex3-panel-results{display:block}
</style>

## Example 4 — Spring Boot + Thymeleaf row edit

<p class="nce-run"><strong>Run:</strong> <code>./mvnw spring-boot:run</code> → <code>http://localhost:8080/items</code></p>

<div class="notes-code-explorer">
<input type="radio" name="ex4" id="ex4-pom" checked>
<input type="radio" name="ex4" id="ex4-props">
<input type="radio" name="ex4" id="ex4-boot">
<input type="radio" name="ex4" id="ex4-seed">
<input type="radio" name="ex4" id="ex4-entity">
<input type="radio" name="ex4" id="ex4-repo">
<input type="radio" name="ex4" id="ex4-form">
<input type="radio" name="ex4" id="ex4-ctrl">
<input type="radio" name="ex4" id="ex4-list">
<input type="radio" name="ex4" id="ex4-rows">
<input type="radio" name="ex4" id="ex4-row">
<input type="radio" name="ex4" id="ex4-edit">
<div class="nce-cap">spring-inline-edit/</div>
<div class="nce-layout">
<nav class="nce-tree" aria-label="spring-inline-edit files">
<label for="ex4-pom" class="nce-indent-1">pom.xml</label>
<div class="nce-dir nce-indent-1">src/main/resources/</div>
<label for="ex4-props" class="nce-indent-2">application.properties</label>
<div class="nce-dir nce-indent-1">src/main/java/com/example/demo/</div>
<label for="ex4-boot" class="nce-indent-2">DemoApplication.java</label>
<div class="nce-dir nce-indent-2">data/</div>
<label for="ex4-seed" class="nce-indent-3">DataLoader.java</label>
<div class="nce-dir nce-indent-2">domain/</div>
<label for="ex4-entity" class="nce-indent-3">Item.java</label>
<div class="nce-dir nce-indent-2">repo/</div>
<label for="ex4-repo" class="nce-indent-3">ItemRepository.java</label>
<div class="nce-dir nce-indent-2">web/</div>
<label for="ex4-form" class="nce-indent-3">ItemForm.java</label>
<label for="ex4-ctrl" class="nce-indent-3">ItemController.java</label>
<div class="nce-dir nce-indent-1">src/main/resources/templates/</div>
<div class="nce-dir nce-indent-2">items/</div>
<label for="ex4-list" class="nce-indent-3">list.html</label>
<div class="nce-dir nce-indent-2">partials/</div>
<label for="ex4-rows" class="nce-indent-3">item-rows.html</label>
<label for="ex4-row" class="nce-indent-3">item-row.html</label>
<label for="ex4-edit" class="nce-indent-3">item-edit.html</label>
</nav>
<div class="nce-panels">
<div class="nce-panel" id="ex4-panel-pom"><pre>&lt;!-- Web + Thymeleaf + JPA — enough to run the inline-edit demo --&gt;
&lt;dependencies&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
  &lt;/dependency&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-thymeleaf&lt;/artifactId&gt;
  &lt;/dependency&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
    &lt;artifactId&gt;spring-boot-starter-data-jpa&lt;/artifactId&gt;
  &lt;/dependency&gt;
  &lt;dependency&gt;
    &lt;groupId&gt;com.h2database&lt;/groupId&gt;
    &lt;artifactId&gt;h2&lt;/artifactId&gt;
    &lt;scope&gt;runtime&lt;/scope&gt;
  &lt;/dependency&gt;
&lt;/dependencies&gt;</pre></div>
<div class="nce-panel" id="ex4-panel-props"><pre># In-memory H2 — no external DB setup for the demo
spring.datasource.url=jdbc:h2:mem:items
spring.datasource.driverClassName=org.h2.Driver
spring.jpa.hibernate.ddl-auto=create-drop
spring.h2.console.enabled=true</pre></div>
<div class="nce-panel" id="ex4-panel-boot"><pre>// Entrypoint — component scan picks up @Controller, @Repository, etc.
package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {
  public static void main(String[] args) {
    SpringApplication.run(DemoApplication.class, args);
  }
}</pre></div>
<div class="nce-panel" id="ex4-panel-seed"><pre>// Seeds sample rows on startup so /items is not empty.
package com.example.demo.data;

import com.example.demo.domain.Item;
import com.example.demo.repo.ItemRepository;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class DataLoader implements CommandLineRunner {
  private final ItemRepository repo;
  public DataLoader(ItemRepository repo) { this.repo = repo; }

  @Override
  public void run(String... args) {
    if (repo.count() == 0) {
      Item a = new Item(); a.setName("Widget");
      Item b = new Item(); b.setName("Gadget");
      repo.save(a);
      repo.save(b);
    }
  }
}</pre></div>
<div class="nce-panel" id="ex4-panel-entity"><pre>// JPA entity — in-memory H2 table backing the item list.
package com.example.demo.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Item {
  @Id @GeneratedValue(strategy = GenerationType.IDENTITY)
  private Long id;
  private String name;

  public Long getId() { return id; }
  public void setId(Long id) { this.id = id; }
  public String getName() { return name; }
  public void setName(String name) { this.name = name; }
}</pre></div>
<div class="nce-panel" id="ex4-panel-repo"><pre>// Spring Data — findAll() feeds the list page and HTMX partials.
package com.example.demo.repo;

import com.example.demo.domain.Item;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ItemRepository extends JpaRepository&lt;Item, Long&gt; {}</pre></div>
<div class="nce-panel" id="ex4-panel-form"><pre>// Form DTO bound from hx-post body — maps back to Item entity.
package com.example.demo.web;

import com.example.demo.domain.Item;

public class ItemForm {
  private String name;

  public String getName() { return name; }
  public void setName(String name) { this.name = name; }

  public Item toEntity(Long id) {
    Item item = new Item();
    item.setId(id);
    item.setName(name);
    return item;
  }
}</pre></div>
<div class="nce-panel" id="ex4-panel-ctrl"><pre>// Controller returns fragments when HX-Request header is present.
package com.example.demo.web;

import com.example.demo.repo.ItemRepository;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.*;
import jakarta.validation.Valid;

@Controller
@RequestMapping("/items")
public class ItemController {

  private final ItemRepository repo;

  public ItemController(ItemRepository repo) { this.repo = repo; }

  @GetMapping
  public String list(Model model,
      @RequestHeader(value = "HX-Request", defaultValue = "false") boolean htmx) {
    model.addAttribute("items", repo.findAll());
    // Full page vs tbody partial — same data, different template.
    return htmx ? "partials/item-rows :: rows" : "items/list";
  }

  @GetMapping("/{id}/edit")
  public String editForm(@PathVariable Long id, Model model) {
    model.addAttribute("item", repo.findById(id).orElseThrow());
    // hx-target="closest tr" expects a &lt;tr&gt; fragment back.
    return "partials/item-edit :: row";
  }

  @PostMapping("/{id}")
  public String save(@PathVariable Long id, @Valid @ModelAttribute ItemForm form,
      BindingResult br, Model model) {
    if (br.hasErrors()) {
      model.addAttribute("item", repo.findById(id).orElseThrow());
      return "partials/item-edit :: row";  // configure 422 swap if needed
    }
    repo.save(form.toEntity(id));
    model.addAttribute("item", repo.findById(id).orElseThrow());
    return "partials/item-row :: row";  // back to read-only row
  }
}</pre></div>
<div class="nce-panel" id="ex4-panel-list"><pre>&lt;!-- Full page: table shell + HTMX script; tbody filled from partial --&gt;
&lt;!DOCTYPE html&gt;
&lt;html lang="en" xmlns:th="http://www.thymeleaf.org"&gt;
&lt;head&gt;
  &lt;meta charset="utf-8"&gt;
  &lt;title&gt;Items&lt;/title&gt;
  &lt;script src="https://unpkg.com/htmx.org@2.0.4" defer&gt;&lt;/script&gt;
&lt;/head&gt;
&lt;body&gt;
  &lt;h1&gt;Items&lt;/h1&gt;
  &lt;table&gt;
    &lt;thead&gt;&lt;tr&gt;&lt;th&gt;Name&lt;/th&gt;&lt;th&gt;&lt;/th&gt;&lt;/tr&gt;&lt;/thead&gt;
    &lt;!-- th:replace pulls in tbody fragment — same markup HTMX swaps --&gt;
    &lt;tbody th:replace="~{partials/item-rows :: rows}"&gt;&lt;/tbody&gt;
  &lt;/table&gt;
&lt;/body&gt;
&lt;/html&gt;</pre></div>
<div class="nce-panel" id="ex4-panel-rows"><pre>&lt;!-- tbody fragment returned for HX-Request list refresh --&gt;
&lt;tbody th:fragment="rows"&gt;
  &lt;tr th:each="item : ${items}"
      th:replace="~{partials/item-row :: row(${item})}"&gt;&lt;/tr&gt;
&lt;/tbody&gt;</pre></div>
<div class="nce-panel" id="ex4-panel-row"><pre>&lt;!-- th:fragment name lets controller return :: row only --&gt;
&lt;tr th:fragment="row(item)" th:id="${'item-' + item.id}"&gt;
  &lt;td th:text="${item.name}"&gt;Name&lt;/td&gt;
  &lt;td&gt;
    &lt;!-- Edit replaces entire row via outerHTML swap --&gt;
    &lt;button th:attr="hx-get=@{/items/{id}/edit(id=${item.id})}"
            hx-target="closest tr"
            hx-swap="outerHTML"&gt;
      Edit
    &lt;/button&gt;
  &lt;/td&gt;
&lt;/tr&gt;</pre></div>
<div class="nce-panel" id="ex4-panel-edit"><pre>&lt;!-- Edit partial: still a &lt;tr&gt; so outerHTML swap stays valid table markup --&gt;
&lt;tr th:fragment="row" th:id="${'item-' + item.id}"&gt;
  &lt;td colspan="2"&gt;
    &lt;form th:attr="hx-post=@{/items/{id}(id=${item.id})}"
          hx-target="closest tr"
          hx-swap="outerHTML"&gt;
      &lt;input name="name" th:value="${item.name}" /&gt;
      &lt;button type="submit"&gt;Save&lt;/button&gt;
    &lt;/form&gt;
  &lt;/td&gt;
&lt;/tr&gt;</pre></div>
</div>
</div>
</div>

<style>
#ex4-pom:checked ~ .nce-layout .nce-tree label[for=ex4-pom],
#ex4-props:checked ~ .nce-layout .nce-tree label[for=ex4-props],
#ex4-boot:checked ~ .nce-layout .nce-tree label[for=ex4-boot],
#ex4-seed:checked ~ .nce-layout .nce-tree label[for=ex4-seed],
#ex4-entity:checked ~ .nce-layout .nce-tree label[for=ex4-entity],
#ex4-repo:checked ~ .nce-layout .nce-tree label[for=ex4-repo],
#ex4-form:checked ~ .nce-layout .nce-tree label[for=ex4-form],
#ex4-ctrl:checked ~ .nce-layout .nce-tree label[for=ex4-ctrl],
#ex4-list:checked ~ .nce-layout .nce-tree label[for=ex4-list],
#ex4-rows:checked ~ .nce-layout .nce-tree label[for=ex4-rows],
#ex4-row:checked ~ .nce-layout .nce-tree label[for=ex4-row],
#ex4-edit:checked ~ .nce-layout .nce-tree label[for=ex4-edit]{background:#27272a;color:#fafafa;border-left:2px solid #22c55e}
#ex4-pom:checked ~ .nce-layout #ex4-panel-pom,
#ex4-props:checked ~ .nce-layout #ex4-panel-props,
#ex4-boot:checked ~ .nce-layout #ex4-panel-boot,
#ex4-seed:checked ~ .nce-layout #ex4-panel-seed,
#ex4-entity:checked ~ .nce-layout #ex4-panel-entity,
#ex4-repo:checked ~ .nce-layout #ex4-panel-repo,
#ex4-form:checked ~ .nce-layout #ex4-panel-form,
#ex4-ctrl:checked ~ .nce-layout #ex4-panel-ctrl,
#ex4-list:checked ~ .nce-layout #ex4-panel-list,
#ex4-rows:checked ~ .nce-layout #ex4-panel-rows,
#ex4-row:checked ~ .nce-layout #ex4-panel-row,
#ex4-edit:checked ~ .nce-layout #ex4-panel-edit{display:block}
</style>

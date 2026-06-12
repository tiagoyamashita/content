---
label: "I"
subtitle: "Overview"
group: "jQuery"
order: 1
---
jQuery — overview
**jQuery** is a small library (circa 2006) that simplified **DOM selection**, **events**, and **AJAX** before modern browsers and frameworks. You still see it in **legacy sites**, CMS themes, and admin templates.

Parent track: [JavaScript overview](../i-overview.md).

## What jQuery adds

```html
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
<script>
  // Select, bind click, toggle visibility — one chain
  $('#menu-btn').on('click', function () {
    $('#nav').slideToggle(200);
  });
</script>
```

| API | Role |
|-----|------|
| **`$()` / `jQuery()`** | Find elements (`$('#id')`, `$('.class')`) |
| **`.on()` / `.click()`** | Event handlers |
| **`.addClass()` / `.css()`** | Style and class changes |
| **`.html()` / `.text()` / `.val()`** | Read/write content |
| **`.ajax()` / `$.get()`** | HTTP without `fetch` boilerplate |
| **Plugins** | Date pickers, sliders, DataTables, etc. |

## Mental model

```text
Page load  →  $(document).ready(fn)  →  select DOM  →  attach events  →  mutate on user action
```

Modern equivalent: **`document.querySelector`**, **`addEventListener`**, **`fetch`** — or a framework if state grows.

## When jQuery still makes sense

| Good fit | Poor default |
|----------|--------------|
| Maintaining existing jQuery codebase | New large SPA |
| Quick script on a server-rendered page | Heavy client routing |
| Plugin depends on jQuery | Greenfield with React/Angular team |

## Minimal patterns

**Ready handler:**

```javascript
$(function () {
  // DOM is safe to query
});
```

**Delegation (dynamic children):**

```javascript
$('#list').on('click', 'button.delete', function () {
  $(this).closest('li').remove();
});
```

**JSON GET:**

```javascript
$.getJSON('/api/items', function (data) {
  data.forEach(item => $('#list').append(`<li>${item.name}</li>`));
});
```

## vs React / Angular / HTMX

| | **jQuery** | **React / Angular** | **HTMX** |
|---|------------|---------------------|----------|
| **Model** | DOM is source of truth | Virtual DOM / component tree | Server HTML fragments |
| **State** | Scattered in DOM | Centralized in components | Mostly on server |
| **Build** | Optional (CDN script tag) | Required bundler | Optional |

## Next steps (future notes)

Install via npm or CDN, migrate off jQuery incrementally, and compare with vanilla `fetch` + DOM APIs.

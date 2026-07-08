---
label: "I"
subtitle: "概要"
group: "HTMX"
order: 1
---
HTMX — 概要

**HTMX** extends HTML with attributes so the browser can **fetch partial updates from the server** without writing a client-side SPA framework. The server returns **HTML fragments**; HTMX swaps them into the page. You keep **server-rendered templates** and gain **dynamic UX** — forms, tabs, infinite scroll, modals — with less JavaScript.

For REST and server-side rendering context, see [REST controllers](../java/springboot/iv-rest-controllers.md). For caching static assets vs dynamic HTML, see [CDN](../cdn/i-overview.md).

## このトラックの地図

| パート | フォーカス |
|------|----------|
| **I — 概要** | ハイパーメディア vs SPA、HTMX の位置づけ |
| **II — インストールとセットアップ** | スクリプトタグ、CSP、ローカル開発 |
| **III — コア属性とスワップ** | `hx-get`、`hx-target`、`hx-swap`、トリガー |
| **IV — フォームとリクエスト** | POST、`hx-vals`、CSRF、アップロード |
| **V — サーバー応答とテンプレート** | 部分 HTML、`HX-*` ヘッダー、ステータスコード |
| **VI — イベントと拡張** | `htmx:*` イベント、SSE、WebSocket |
| **VII — パターンとアプリ統合** | ページネーション、モーダル、Spring/Flask/FastAPI |
| **VIII — 使い分けとトレードオフ** | React/Vue との比較、限界、チーム適性 |
| **IX — 例** | 実行可能なミニアプリ — ファイルツリー + コメント付きソース |

## ハイパーメディア駆動アプリ

```text
Classic multi-page app (MPA)
  User click  →  full page reload  →  new HTML document

SPA (React/Vue)
  User click  →  JS fetches JSON  →  client renders DOM

HTMX
  User click  →  fetch HTML fragment  →  swap into existing page
```

| Approach | Server sends | Client does |
|----------|--------------|-------------|
| **MPA** | Full HTML page | Browser replaces document |
| **SPA** | JSON (+ separate static JS bundle) | Framework builds UI |
| **HTMX** | HTML partial (or full page) | Swap into target element |

HTMX is **not** anti-JavaScript — it removes **boilerplate fetch/render** for common CRUD and navigation patterns. You still add JS for rich widgets when needed.

## Next

Continue with [Install & setup](ii-install-and-setup.md) to add HTMX to a page and verify the first swap.

---
label: "I"
subtitle: "Overview"
group: "Sass"
order: 1
---
Sass — overview
**Sass** (Syntactically Awesome Style Sheets) is a **CSS preprocessor**. You write `.scss` or `.sass` files with variables, nesting, and mixins; a compiler emits standard **CSS** for browsers. It remains common in Rails, Angular, and many design-system pipelines.

Parent track: [CSS overview](../i-overview.md). Compare with [Less](../less/i-overview.md) for a similar feature set with different syntax.

## What Sass adds

```scss
$primary: #0d6efd;
$radius: 0.375rem;

.card {
  border-radius: $radius;
  padding: 1rem;

  &__title {
    color: $primary;
    font-weight: 600;
  }
}
```

| Feature | Role |
|---------|------|
| **`$variables`** | Reuse colors, spacing, breakpoints |
| **Nesting** | Mirror HTML structure; use `&` for parent reference |
| **`@mixin` / `@include`** | Reusable style blocks (e.g. clearfix, breakpoints) |
| **`@extend`** | Share selector groups (use sparingly) |
| **Partials & `@use`** | Split files; `@use 'tokens'` loads modules |
| **Functions** | `darken()`, `mix()`, map lookups |

## Two syntaxes

| Syntax | File | Notes |
|--------|------|-------|
| **SCSS** | `.scss` | CSS superset — braces and semicolons; **default choice** |
| **Indented Sass** | `.sass` | Whitespace-based; less common today |

## Mental model

```text
.scss sources  →  sass / dart-sass CLI  →  .css  →  browser (or bundled by Vite/webpack)
```

Modern projects prefer **`@use`** and **`@forward`** over legacy **`@import`** (deprecated).

## When Sass makes sense

| Good fit | Poor default |
|----------|--------------|
| Shared design tokens across many stylesheets | Tiny static page with one `<style>` block |
| Team already on Sass | New project where Tailwind/CSS modules cover needs |
| Build pipeline already compiles SCSS | Runtime theming only — use CSS custom properties |

## Minimal compile

```bash
npm install -D sass
npx sass styles/main.scss dist/main.css
```

Watch mode: `npx sass --watch styles:dist`.

## vs Less / plain CSS

| | **Sass** | **Less** | **Plain CSS** |
|---|----------|----------|---------------|
| **Variables** | `$var` | `@var` | `--var` (custom properties) |
| **Nesting** | Yes | Yes | Yes (native since ~2023) |
| **Ecosystem** | dart-sass, widespread | Less common in new projects | No compile step |
| **Mixins** | `@mixin` | `.mixin()` | `@layer`, utilities |

## Next steps (future notes)

Partials layout, breakpoint mixins, `@use` modules, and integration with Vite or webpack.

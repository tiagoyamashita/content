---
label: "I"
subtitle: "Overview"
group: "Less"
order: 1
---
Less — overview
**Less** is a **CSS preprocessor** like Sass — variables, nesting, mixins, and imports compile to plain CSS. It was popular with **Bootstrap 3** and some legacy front-end stacks; many teams have moved to **Sass** or **plain CSS**, but Less codebases still need maintenance.

Parent track: [CSS overview](../i-overview.md). For the modern default preprocessor path, see [Sass](../sass/i-overview.md).

## What Less adds

```less
@primary: #0d6efd;
@radius: 0.375rem;

.card {
  border-radius: @radius;
  padding: 1rem;

  &-title {
    color: @primary;
    font-weight: 600;
  }
}
```

| Feature | Role |
|---------|------|
| **`@variables`** | Colors, spacing, fonts — compile-time constants |
| **Nesting** | Nested selectors; `&` references parent |
| **Mixins** | Parametric rules — `.border-radius(@r) { … }` |
| **Operations** | Math on numbers and colors in expressions |
| **Imports** | `@import "variables.less"` — split files |

## Mental model

```text
.less sources  →  lessc (CLI) or webpack less-loader  →  .css  →  browser
```

Less runs in **Node** (`less` package) or via bundler plugins; there is no browser-native Less.

## When Less still makes sense

| Good fit | Poor default |
|----------|--------------|
| Existing Less codebase or theme | Greenfield project (prefer Sass or CSS) |
| Tooling locked to Less (old admin templates) | Need runtime theme switching — use CSS variables |
| Learning preprocessor concepts | Bootstrap 5+ docs assume Sass for customization |

## Minimal compile

```bash
npm install -D less
npx lessc styles/main.less dist/main.css
```

## vs Sass / plain CSS

| | **Less** | **Sass** | **Plain CSS** |
|---|----------|----------|---------------|
| **Variable sigil** | `@name` | `$name` | `--name` |
| **Mixin syntax** | `.name() { }` | `@mixin name` | N/A |
| **Adoption (2020s)** | Declining in new work | Common | Growing with nesting `@layer` |
| **Bootstrap customize** | Legacy | Official Sass sources | Override CSS vars |

## Next steps (future notes)

Mixin patterns, importing Bootstrap Less (legacy), and migration paths toward Sass or plain CSS.

---
label: "V"
subtitle: "Forms & validation"
group: "React"
order: 5
---
React — forms & validation
Forms in React are usually **controlled**: input **`value`** comes from state, **`onChange`** updates state, **`onSubmit`** sends data to the server. Validate on the **client** for fast feedback; always validate on the **server** — client checks are UX only.

Previous: [Authentication](iv-authentication.md). Server-side validation parallel: [HTMX forms](../../htmx/iv-forms-and-requests.md).

## 1. Controlled input pattern

```jsx
const [title, setTitle] = useState('');

<input
  name="title"
  value={title}
  onChange={e => setTitle(e.target.value)}
/>;
```

React owns the value — no uncontrolled DOM state unless you use refs on purpose.

## 2. Full form with client validation

```jsx
// src/components/ItemForm.jsx
import { useState } from 'react';
import { createItem } from '../api/items';

const MIN_TITLE = 3;

export function ItemForm({ onCreated }) {
  const [title, setTitle] = useState('');
  const [errors, setErrors] = useState({});
  const [submitting, setSubmitting] = useState(false);

  function validate() {
    const next = {};
    if (!title.trim()) next.title = 'Title is required';
    else if (title.trim().length < MIN_TITLE) {
      next.title = `Title must be at least ${MIN_TITLE} characters`;
    }
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function handleSubmit(e) {
    e.preventDefault();
    if (!validate()) return;

    setSubmitting(true);
    try {
      const item = await createItem({ title: title.trim() });
      setTitle('');
      setErrors({});
      onCreated?.(item);
    } catch (err) {
      if (err.status === 422 && err.fields) {
        setErrors(err.fields);  // server field errors — see §4
      } else {
        setErrors({ form: err.message ?? 'Save failed' });
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit} noValidate>
      <label htmlFor="title">Title</label>
      <input
        id="title"
        name="title"
        value={title}
        onChange={e => setTitle(e.target.value)}
        aria-invalid={!!errors.title}
        aria-describedby={errors.title ? 'title-error' : undefined}
      />
      {errors.title && (
        <p id="title-error" role="alert" className="error">{errors.title}</p>
      )}
      {errors.form && <p role="alert" className="error">{errors.form}</p>}
      <button type="submit" disabled={submitting}>
        {submitting ? 'Saving…' : 'Save'}
      </button>
    </form>
  );
}
```

**`noValidate`** — disable browser default bubbles so your messages stay consistent.

## 3. Validation timing

| Strategy | When | Use |
|----------|------|-----|
| **On submit** | `handleSubmit` | Simple forms |
| **On blur** | `onBlur={() => validateField('title')}` | Few fields, less noise |
| **On change** | After first submit failed | Live correction |

Avoid validating every keystroke before the user tries once — unless search/filter UX needs it.

## 4. Server validation (422)

API returns field errors; map into the same `errors` object:

```json
{
  "message": "Validation failed",
  "fields": {
    "title": "Title already exists",
    "email": "Invalid email format"
  }
}
```

```javascript
// src/api/client.js — in error handler
if (res.status === 422) {
  const body = await res.json();
  const err = new ApiError(422, body.message);
  err.fields = body.fields ?? {};
  throw err;
}
```

Display next to the matching input — same UI as client errors.

## 5. React Hook Form (common library)

Less re-render churn on large forms:

```text
npm install react-hook-form
```

```jsx
import { useForm } from 'react-hook-form';

export function ItemForm({ onCreated }) {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
  } = useForm({ defaultValues: { title: '' } });

  const onSubmit = async (data) => {
    try {
      const item = await createItem(data);
      onCreated?.(item);
    } catch (err) {
      if (err.fields) {
        Object.entries(err.fields).forEach(([name, message]) =>
          setError(name, { message })
        );
      } else {
        setError('root', { message: err.message });
      }
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input
        {...register('title', {
          required: 'Title is required',
          minLength: { value: 3, message: 'At least 3 characters' },
        })}
        aria-invalid={!!errors.title}
      />
      {errors.title && <p role="alert">{errors.title.message}</p>}
      <button disabled={isSubmitting}>Save</button>
    </form>
  );
}
```

**`register`** wires ref + onChange + name — still controlled under the hood.

## 6. Zod + schema validation

Share rules between client and server (TypeScript teams):

```text
npm install zod @hookform/resolvers
```

```javascript
import { z } from 'zod';

export const itemSchema = z.object({
  title: z.string().trim().min(3, 'At least 3 characters'),
  qty: z.coerce.number().int().min(1),
});
```

```jsx
import { zodResolver } from '@hookform/resolvers/zod';

useForm({ resolver: zodResolver(itemSchema) });
```

## 7. Checkboxes, selects, files

```jsx
// checkbox
const [done, setDone] = useState(false);
<input type="checkbox" checked={done} onChange={e => setDone(e.target.checked)} />

// select
<select value={status} onChange={e => setStatus(e.target.value)}>
  <option value="open">Open</option>
  <option value="closed">Closed</option>
</select>

// file — often uncontrolled or FormData
const [file, setFile] = useState(null);
<input type="file" onChange={e => setFile(e.target.files?.[0] ?? null)} />
```

Upload: **`FormData`** + `fetch` without JSON content-type:

```javascript
const fd = new FormData();
fd.append('file', file);
await fetch('/api/upload', { method: 'POST', body: fd, headers: { Authorization: `Bearer ${token}` } });
```

## 8. Accessibility checklist

- [ ] **`label`** + **`htmlFor`** tied to input **`id`**
- [ ] **`aria-invalid`** when field has error
- [ ] **`role="alert"`** on error text
- [ ] Disable submit while **`submitting`** — prevent double POST
- [ ] Focus first invalid field after failed submit (optional `ref.focus()`)

## Track complete

Return to [React overview](i-overview.md) or [JavaScript overview](../i-overview.md).

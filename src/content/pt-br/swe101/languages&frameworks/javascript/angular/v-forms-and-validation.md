---
label: "V"
subtitle: "Forms & validation"
group: "Angular"
order: 5
---
Angular — forms & validation
Angular offers **Template-driven** forms (`ngModel`) and **Reactive** forms (`FormBuilder`) — enterprise apps usually standardize on **reactive** for testability and complex validation. Client rules give fast feedback; **server validation** is still required.

Previous: [Authentication](iv-authentication.md). Server-rendered alternative: [HTMX forms](../../htmx/iv-forms-and-requests.md).

## 1. Reactive forms setup

```typescript
import { ReactiveFormsModule } from '@angular/forms';

@Component({
  standalone: true,
  imports: [ReactiveFormsModule],
  // ...
})
```

## 2. Basic form with validators

```typescript
// features/items/item-form.component.ts
import { Component, inject, output } from '@angular/core';
import { FormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { ItemsService } from './items.service';

@Component({
  selector: 'app-item-form',
  standalone: true,
  imports: [ReactiveFormsModule],
  template: `
    <form [formGroup]="form" (ngSubmit)="submit()">
      <label for="title">Title</label>
      <input id="title" formControlName="title" [attr.aria-invalid]="showError('title')" />
      @if (showError('title')) {
        <p role="alert">{{ errorMessage('title') }}</p>
      }
      @if (serverError) {
        <p role="alert">{{ serverError }}</p>
      }
      <button type="submit" [disabled]="form.invalid || saving">
        {{ saving ? 'Saving…' : 'Save' }}
      </button>
    </form>
  `,
})
export class ItemFormComponent {
  private fb = inject(FormBuilder);
  private items = inject(ItemsService);
  created = output<void>();

  saving = false;
  serverError: string | null = null;

  form = this.fb.nonNullable.group({
    title: ['', [Validators.required, Validators.minLength(3)]],
  });

  showError(controlName: 'title') {
    const c = this.form.controls[controlName];
    return c.invalid && (c.dirty || c.touched);
  }

  errorMessage(controlName: 'title') {
    const c = this.form.controls[controlName];
    if (c.hasError('required')) return 'Title is required';
    if (c.hasError('minlength')) return 'At least 3 characters';
    return 'Invalid';
  }

  submit() {
    if (this.form.invalid) {
      this.form.markAllAsTouched();
      return;
    }
    this.saving = true;
    this.serverError = null;

    this.items.createItem(this.form.getRawValue()).subscribe({
      next: () => {
        this.form.reset();
        this.created.emit();
      },
      error: err => {
        if (err.status === 422 && err.error?.fields) {
          this.applyServerErrors(err.error.fields);
        } else {
          this.serverError = err.error?.message ?? 'Save failed';
        }
        this.saving = false;
      },
      complete: () => (this.saving = false),
    });
  }

  private applyServerErrors(fields: Record<string, string>) {
    Object.entries(fields).forEach(([name, message]) => {
      const control = this.form.get(name);
      if (control) {
        control.setErrors({ server: message });
        control.markAsTouched();
      }
    });
  }
}
```

**`markAllAsTouched`** — show errors after submit attempt on untouched fields.

## 3. Validation timing

| When | How |
|------|-----|
| **On submit** | `if (form.invalid) markAllAsTouched()` |
| **While typing** | Built-in — validators run on value change |
| **Show message** | `invalid && (dirty \|\| touched)` |

Avoid aggressive error display before first submit unless UX requires it.

## 4. Built-in validators

| Validator | Example |
|-----------|---------|
| **`Validators.required`** | Non-empty |
| **`Validators.minLength(n)`** | String length |
| **`Validators.maxLength(n)`** | String length |
| **`Validators.email`** | Basic email shape |
| **`Validators.pattern(regex)`** | Custom pattern |
| **`Validators.min` / `max`** | Numbers |

```typescript
qty: [1, [Validators.required, Validators.min(1), Validators.max(999)]],
```

## 5. Custom validator

```typescript
import { AbstractControl, ValidationErrors, ValidatorFn } from '@angular/forms';

export function noSpaces(): ValidatorFn {
  return (control: AbstractControl): ValidationErrors | null => {
    const v = control.value as string;
    return v && /\s/.test(v) ? { noSpaces: true } : null;
  };
}

// usage
title: ['', [Validators.required, noSpaces()]],
```

## 6. Server errors (422)

API response:

```json
{
  "message": "Validation failed",
  "fields": {
    "title": "Title already exists"
  }
}
```

Map with **`setErrors({ server: message })`** — display in template:

```html
@if (form.controls.title.hasError('server')) {
  <p role="alert">{{ form.controls.title.getError('server') }}</p>
}
```

Handle **`422`** in service or a global **`HttpInterceptor`** if every form shares the same shape.

## 7. Form groups and nested objects

```typescript
form = this.fb.group({
  profile: this.fb.group({
    name: ['', Validators.required],
    email: ['', [Validators.required, Validators.email]],
  }),
  address: this.fb.group({
    city: [''],
    zip: ['', Validators.pattern(/^\d{5}$/)],
  }),
});
```

Template: **`formControlName="name"`** inside **`formGroupName="profile"`**.

## 8. Template-driven (brief)

```typescript
import { FormsModule } from '@angular/forms';

<input [(ngModel)]="title" name="title" required minlength="3" #titleCtrl="ngModel" />
@if (titleCtrl.invalid && titleCtrl.touched) { … }
```

Fine for tiny forms; reactive scales better with unit tests and dynamic fields.

## 9. Dynamic form arrays

```typescript
import { FormArray } from '@angular/forms';

tags = this.fb.nonNullable.array<string>([]);

addTag() {
  this.tags.push(this.fb.nonNullable.control('', Validators.required));
}
```

Use **`formArrayName`** in template for repeating rows (line items, phone numbers).

## 10. Accessibility checklist

- [ ] **`label`** + **`for`** matching input **`id`**
- [ ] **`aria-invalid`** when control has errors
- [ ] **`role="alert"`** on error text
- [ ] Disable submit when **`form.invalid`** or **`saving`**
- [ ] Focus first invalid control after failed submit (optional `element.focus()`)

## Track complete

Return to [Angular overview](i-overview.md) or [JavaScript overview](../i-overview.md).

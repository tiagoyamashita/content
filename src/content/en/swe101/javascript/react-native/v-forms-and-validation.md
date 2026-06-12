---
label: "V"
subtitle: "Forms & validation"
group: "React Native"
order: 5
---
React Native — forms & validation
Forms use **`TextInput`** (and pickers/switches) with **controlled state** — same idea as web [React forms](../react/v-forms-and-validation.md). Validate on the **client** for fast feedback; always validate on the **server**.

Previous: [Authentication](iv-authentication.md).

## 1. Controlled `TextInput`

```tsx
const [title, setTitle] = useState('');

<TextInput
  value={title}
  onChangeText={setTitle}
  placeholder="Title"
  autoCapitalize="none"
/>;
```

| Prop | Purpose |
|------|---------|
| **`value` / `onChangeText`** | Controlled input (not `onChange` + `e.target.value`) |
| **`keyboardType`** | `email-address`, `numeric`, `phone-pad` |
| **`secureTextEntry`** | Password fields |
| **`autoComplete`** | Hints for autofill (`email`, `password`) |
| **`returnKeyType`** | `done`, `next`, `send` — pairs with keyboard submit |

There is no `<form>` element — handle submit on button **`onPress`** or **`onSubmitEditing`** on the last field.

## 2. Full form with client validation

```tsx
// src/screens/CreateItemScreen.tsx
import { useState } from 'react';
import {
  View,
  Text,
  TextInput,
  Pressable,
  StyleSheet,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
} from 'react-native';
import { createItem } from '../api/items';

const MIN_TITLE = 3;

export function CreateItemScreen({ onCreated }: { onCreated?: () => void }) {
  const [title, setTitle] = useState('');
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [submitting, setSubmitting] = useState(false);

  function validate() {
    const next: Record<string, string> = {};
    if (!title.trim()) next.title = 'Title is required';
    else if (title.trim().length < MIN_TITLE) {
      next.title = `Title must be at least ${MIN_TITLE} characters`;
    }
    setErrors(next);
    return Object.keys(next).length === 0;
  }

  async function handleSubmit() {
    if (!validate()) return;

    setSubmitting(true);
    try {
      const item = await createItem({ title: title.trim() });
      setTitle('');
      setErrors({});
      onCreated?.(item);
    } catch (err: unknown) {
      const e = err as { status?: number; fields?: Record<string, string>; message?: string };
      if (e.status === 422 && e.fields) {
        setErrors(e.fields);
      } else {
        setErrors({ form: e.message ?? 'Save failed' });
      }
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <KeyboardAvoidingView
      style={styles.flex}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView contentContainerStyle={styles.container} keyboardShouldPersistTaps="handled">
        <Text style={styles.label}>Title</Text>
        <TextInput
          style={[styles.input, errors.title && styles.inputError]}
          value={title}
          onChangeText={setTitle}
          onSubmitEditing={handleSubmit}
          returnKeyType="done"
          accessibilityLabel="Title"
        />
        {errors.title ? (
          <Text style={styles.error} accessibilityRole="alert">{errors.title}</Text>
        ) : null}

        {errors.form ? (
          <Text style={styles.error} accessibilityRole="alert">{errors.form}</Text>
        ) : null}

        <Pressable
          style={[styles.button, submitting && styles.buttonDisabled]}
          onPress={handleSubmit}
          disabled={submitting}
        >
          {submitting ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Save</Text>
          )}
        </Pressable>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  container: { padding: 16 },
  label: { marginBottom: 4, fontWeight: '600' },
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12,
    marginBottom: 4,
  },
  inputError: { borderColor: '#c00' },
  error: { color: '#c00', marginBottom: 12 },
  button: {
    backgroundColor: '#0066cc',
    padding: 14,
    borderRadius: 8,
    alignItems: 'center',
  },
  buttonDisabled: { opacity: 0.6 },
  buttonText: { color: '#fff', fontWeight: '600' },
});
```

## 3. Keyboard UX

| Technique | Purpose |
|-----------|---------|
| **`KeyboardAvoidingView`** | Shift content when keyboard opens (iOS `padding`) |
| **`ScrollView` + `keyboardShouldPersistTaps="handled"`** | Taps on buttons work while keyboard is open |
| **`Keyboard.dismiss()`** | Close keyboard after submit |
| **Focus next field** | `ref` on inputs + `onSubmitEditing` → `nextRef.focus()` |

For complex forms, **`react-native-keyboard-aware-scroll-view`** is a common add-on.

## 4. Validation timing

| Strategy | When | Use |
|----------|------|-----|
| **On submit** | `handleSubmit` | Login, short forms |
| **On blur** | `onBlur` on `TextInput` | Medium forms |
| **On change** (debounced) | After user pauses typing | Search, live checks |

Same tradeoffs as web — stricter on-change validation can feel noisy on small screens.

## 5. Server field errors (422)

Map API **`fields`** object to the same `errors` state as client validation:

```json
{
  "message": "Validation failed",
  "fields": {
    "title": "Title already exists",
    "email": "Invalid email"
  }
}
```

```typescript
if (res.status === 422) {
  const body = await res.json();
  throw Object.assign(new Error(body.message), { status: 422, fields: body.fields });
}
```

Show one message per field under the matching `TextInput`.

## 6. Form libraries (optional)

| Library | Notes |
|---------|-------|
| **React Hook Form** | Works in RN with `Controller` wrapping `TextInput` |
| **Formik** | Familiar from web React |
| **Zod / Yup** | Shared schemas with web app if you monorepo |

```tsx
import { useForm, Controller } from 'react-hook-form';

const { control, handleSubmit, formState: { errors } } = useForm({ defaultValues: { title: '' } });

<Controller
  control={control}
  name="title"
  rules={{ required: 'Title is required', minLength: { value: 3, message: 'Too short' } }}
  render={({ field: { onChange, onBlur, value } }) => (
    <TextInput value={value} onChangeText={onChange} onBlur={onBlur} />
  )}
/>;
```

Use a library when you have many fields, nested objects, or shared validation with your [React web app](../react/v-forms-and-validation.md).

## 7. Non-text inputs

| Control | Package / component |
|---------|---------------------|
| **Switch** | `Switch` from `react-native` |
| **Picker** | `@react-native-picker/picker` |
| **Date** | `@react-native-community/datetimepicker` |
| **Image upload** | `expo-image-picker` → multipart `fetch` to API |

Keep upload logic in **`api/`** — `FormData` append file blob, same as web multipart.

## 8. Login form specifics

```tsx
<TextInput
  keyboardType="email-address"
  autoComplete="email"
  textContentType="emailAddress"
  autoCapitalize="none"
/>
<TextInput
  secureTextEntry
  autoComplete="password"
  textContentType="password"
/>
```

After login, call **`Keyboard.dismiss()`** before navigation to avoid keyboard flicker on the next screen.

## Track complete

Return to [React Native overview](i-overview.md) or compare with [Flutter](../../flutter/i-overview.md) for Dart-based mobile.

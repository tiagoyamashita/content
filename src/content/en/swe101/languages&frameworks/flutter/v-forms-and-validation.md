---
label: "V"
subtitle: "Forms & validation"
group: "Flutter"
order: 5
---
Flutter — forms & validation
Forms use **`TextFormField`** inside a **`Form`** widget with validators — similar goals to [React controlled inputs](../javascript/react/v-forms-and-validation.md) and [React Native `TextInput`](../javascript/react-native/v-forms-and-validation.md). Validate on the **client** for fast feedback; always validate on the **server**.

Previous: [Authentication](iv-authentication.md).

## 1. `TextFormField` basics

```dart
TextFormField(
  initialValue: '',
  decoration: const InputDecoration(
    labelText: 'Title',
    border: OutlineInputBorder(),
  ),
  onChanged: (value) => title = value,
)
```

For validation, use a **`Form`** + **`GlobalKey<FormState>`**:

```dart
final _formKey = GlobalKey<FormState>();
String title = '';

Form(
  key: _formKey,
  child: TextFormField(
    decoration: const InputDecoration(labelText: 'Title'),
    validator: (value) {
      if (value == null || value.trim().isEmpty) return 'Title is required';
      if (value.trim().length < 3) return 'At least 3 characters';
      return null;  // valid
    },
    onSaved: (value) => title = value?.trim() ?? '',
  ),
);
```

| API | Role |
|-----|------|
| **`validator`** | Return error string or `null` if OK |
| **`onSaved`** | Called when form saves |
| **`_formKey.currentState!.validate()`** | Run all validators |
| **`_formKey.currentState!.save()`** | Run all `onSaved` |

## 2. Full submit flow

```dart
// lib/screens/create_item_screen.dart
class CreateItemScreen extends StatefulWidget {
  const CreateItemScreen({super.key});

  @override
  State<CreateItemScreen> createState() => _CreateItemScreenState();
}

class _CreateItemScreenState extends State<CreateItemScreen> {
  final _formKey = GlobalKey<FormState>();
  final _titleController = TextEditingController();
  bool submitting = false;
  String? formError;
  final _itemsService = ItemsService();

  @override
  void dispose() {
    _titleController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    setState(() => formError = null);
    if (!_formKey.currentState!.validate()) return;
    _formKey.currentState!.save();

    setState(() => submitting = true);
    try {
      await _itemsService.create(_titleController.text.trim());
      if (!mounted) return;
      Navigator.of(context).pop();
    } on ApiException catch (e) {
      if (e.status == 422 && e.fields is Map) {
        final fields = e.fields as Map<String, dynamic>;
        setState(() => formError = fields['title']?.toString());
      } else {
        setState(() => formError = e.message ?? 'Save failed');
      }
    } finally {
      if (mounted) setState(() => submitting = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('New item')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              TextFormField(
                controller: _titleController,
                decoration: const InputDecoration(labelText: 'Title'),
                textInputAction: TextInputAction.done,
                onFieldSubmitted: (_) => _submit(),
                validator: (v) {
                  if (v == null || v.trim().isEmpty) return 'Title is required';
                  if (v.trim().length < 3) return 'At least 3 characters';
                  return null;
                },
              ),
              if (formError != null) ...[
                const SizedBox(height: 8),
                Text(formError!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
              ],
              const SizedBox(height: 16),
              FilledButton(
                onPressed: submitting ? null : _submit,
                child: submitting
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text('Save'),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

## 3. `TextEditingController` vs `onSaved`

| Approach | When |
|----------|------|
| **`TextEditingController`** | Imperative access, clear field, listeners |
| **`onSaved` + `initialValue`** | Simple forms tied to `Form.save()` |

Use **one** pattern per field — do not mix `controller` and `initialValue` on the same field.

## 4. Keyboard and scroll

| Technique | Purpose |
|-----------|---------|
| **`SingleChildScrollView`** | Form scrolls when keyboard covers fields |
| **`resizeToAvoidBottomInset: true`** on `Scaffold` | Default — shrinks body when keyboard opens |
| **`textInputAction: TextInputAction.next`** | “Next” on keyboard between fields |
| **`FocusNode` + `FocusScope`** | Move focus field to field |

For dense forms, wrap in **`Padding`** with `MediaQuery.viewInsetsOf(context).bottom`.

## 5. Validation timing

| Strategy | How |
|----------|-----|
| **On submit** | `validate()` in button handler — default |
| **On change** | `autovalidateMode: AutovalidateMode.onUserInteraction` |
| **Always** | `AutovalidateMode.always` — can feel noisy |

## 6. Server field errors (422)

Map API **`fields`** to UI — either set a top-level `formError` or use **`FormField`’s `validator`** with server state:

```dart
String? serverTitleError;

TextFormField(
  validator: (v) {
    if (serverTitleError != null) return serverTitleError;
    if (v == null || v.isEmpty) return 'Required';
    return null;
  },
);
```

After failed submit: **`setState(() => serverTitleError = fields['title'])`** then **`_formKey.currentState!.validate()`**.

## 7. Login form fields

```dart
TextFormField(
  keyboardType: TextInputType.emailAddress,
  autofillHints: const [AutofillHints.email],
  autocorrect: false,
  decoration: const InputDecoration(labelText: 'Email'),
),
TextFormField(
  obscureText: true,
  autofillHints: const [AutofillHints.password],
  decoration: const InputDecoration(labelText: 'Password'),
),
```

Dismiss keyboard before navigation: **`FocusScope.of(context).unfocus()`**.

## 8. Form libraries (optional)

| Package | Notes |
|---------|-------|
| **`flutter_form_builder`** | Declarative fields + validators |
| **`reactive_forms`** | Angular-like form model |

Most production apps use built-in **`Form`** + **`TextFormField`** or **Riverpod** holding field state.

## 9. Other inputs

| Input | Widget |
|-------|--------|
| **Toggle** | `SwitchListTile` |
| **Dropdown** | `DropdownButtonFormField` |
| **Date** | `showDatePicker` |
| **Image pick** | `image_picker` → multipart upload in `services/` |

## Track complete

Return to [Flutter overview](i-overview.md) or compare [React Native](../javascript/react-native/i-overview.md) (JavaScript, Expo).

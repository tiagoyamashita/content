---
label: "II"
subtitle: "OOP & types"
group: "Java"
groupOrder: 1
order: 2
---
Java — Part II
Classes, encapsulation, inheritance, polymorphism, interfaces, and packages.

## 1. Classes and objects
- **Class** = blueprint; **object** = instance in memory with its own field values.
- Constructors initialize state; if you declare none, a default no-arg constructor appears until you add any constructor.
- `this` refers to the current instance; constructor chaining uses `this(...)`.


## 2. Encapsulation
- Hide fields behind accessors (`getX`, `setX`) or clearer domain methods.
- Use the narrowest visibility: `private` fields, `public` API surface deliberately chosen.
- Immutability where possible — `final` fields set once, no mutators — simplifies reasoning in concurrent code.


## 3. Inheritance and polymorphism
- `extends` one superclass; Java supports single inheritance for implementation.
- **`@Override`** when replacing superclass methods — catches signature mistakes at compile time.
- **Dynamic dispatch**: virtual methods resolve to the runtime type’s implementation.
- Prefer composition over deep inheritance hierarchies; inheritance exposes brittle base-class contracts.


## 4. Abstract classes and interfaces
- **Abstract class**: partial implementation; cannot be instantiated directly.
- **`interface`**: defines behavior contracts; methods may be `default` or `static` with bodies since Java 8.
- A class may implement multiple interfaces; use them for capability (“can compare”, “can serialize”).
- **Sealed** classes/interfaces restrict who may extend/implement — useful for exhaustive modeling.


## 5. `Object` essentials
- `equals` / `hashCode` must agree: equal objects → same hash codes.
- `toString` aids debugging and logs; `clone` is fragile — often prefer copy constructors or factories.
- Prefer **`record`** (Java 16+) for immutable data carriers — auto `equals`, `hashCode`, `toString`, accessors.


## 6. Packages and modules (overview)
- **`package`** declares namespace; **imports** shorten names; avoid wildcard imports in large codebases when clarity suffers.
- **`java.base`** and friends ship with the JDK; know **`java.lang`** is implicit.
- **JPMS** (`module-info.java`) adds compile-time boundaries beyond plain packages — adopt when building libraries or enforcing layering.

---
label: "II"
subtitle: "Build system & packages"
group: "Zig"
groupOrder: 1
order: 2
---
Zig — Part II: Build system & packages
**`zig build`** drives compilation, tests, and install steps from **`build.zig`**. **`build.zig.zon`** declares **package metadata** and **dependencies** from the community registry or **git** URLs.

See **Part I** [Basics & toolchain](i-basics-and-toolchain.md) for the **`zig`** CLI and language basics.

## 1. What the build system is

| Piece | Role |
|-------|------|
| **`build.zig`** | Build script (Zig code) — targets, steps, link options |
| **`build.zig.zon`** | Package manifest — name, version, dependency hashes |
| **`zig build`** | Runs **`build.zig`**’s default step (usually compile the app) |
| **`zig fetch`** | Download deps declared in **`build.zig.zon`** |

You rarely invoke **`zig build-exe`** by hand on real projects — **`build.zig`** encodes how the binary is produced and linked.

## 2. Project layout after `zig init`

```text
hello/
  build.zig
  build.zig.zon
  src/
    main.zig
```

**`zig init`** creates a minimal executable template. **`zig build run`** compiles **`src/main.zig`** and runs it.

### Minimal `src/main.zig`

```zig
const std = @import("std");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("Run `zig build test` to run the tests.\n", .{});
}

test "simple test" {
    try std.testing.expectEqual(1 + 1, 2);
}
```

## 3. Everyday `zig build` commands

```text
zig build                  # default step (compile)
zig build run              # run the default executable
zig build test             # run unit tests
zig build install          # copy artifacts to prefix (if configured)
zig build -Doptimize=ReleaseFast   # release optimizations
zig build --summary all    # show what ran
```

| Flag / pattern | Purpose |
|----------------|---------|
| **`-Doptimize=Debug`** | Default — fast compile, debug symbols |
| **`-Doptimize=ReleaseFast`** | Speed-focused release |
| **`-Dtarget=x86_64-windows`** | Cross-compile target |
| **`--search-prefix`** | Extra library include/lib paths |

## 4. Reading `build.zig` (executable)

A generated **`build.zig`** (simplified) looks like:

```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "hello",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    b.installArtifact(exe);

    const run_cmd = b.addRunArtifact(exe);
    run_cmd.step.dependOn(b.getInstallStep());
    if (b.args) |args| run_cmd.addArgs(args);

    const run_step = b.step("run", "Run the app");
    run_step.dependOn(&run_cmd.step);

    const unit_tests = b.addTest(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    const run_unit_tests = b.addRunArtifact(unit_tests);
    const test_step = b.step("test", "Run unit tests");
    test_step.dependOn(&run_unit_tests.step);
}
```

| API | Meaning |
|-----|---------|
| **`b.addExecutable`** | Build an executable from a root `.zig` file |
| **`b.addStaticLibrary` / `addSharedLibrary`** | Library artifacts |
| **`b.addTest`** | Test build of a root file (picks up **`test`** blocks) |
| **`b.step("name", "help")`** | Custom **`zig build name`** step |
| **`b.installArtifact`** | Put output in **`zig-out/bin`** |

## 5. Library + executable in one repo

### Library module — `src/greeter.zig`

```zig
pub fn greet(name: []const u8) []const u8 {
    if (name.len == 0) return "Hello, world!";
    return name; // real code would format into a buffer — see Part III
}

test "default name" {
    const std = @import("std");
    try std.testing.expectEqualStrings("Hello, world!", greet(""));
}
```

### App — `src/main.zig`

```zig
const std = @import("std");
const greeter = @import("greeter.zig");

pub fn main() !void {
    const stdout = std.io.getStdOut().writer();
    try stdout.print("Hello, {s}!\n", .{greeter.greet("Zig")});
}
```

Point **`root_source_file`** at **`main.zig`** and add a **module import** in **`build.zig`**:

```zig
const greeter_mod = b.createModule(.{
    .root_source_file = b.path("src/greeter.zig"),
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("greeter", greeter_mod);
```

Then in **`main.zig`**: **`const greeter = @import("greeter");`** (module name from **`addImport`**).

Exact **`build.zig`** APIs evolve between Zig versions — run **`zig init`** on your version and adapt; the **pattern** (executable + **`addImport`**) stays the same.

## 6. `build.zig.zon` — dependencies

Community packages live on **[ziglang.org/package-registry](https://ziglang.org/download/)** (and mirrors). **`build.zig.zon`** pins name, version, and **content hash**.

Example adding a dependency (shape — verify names/versions on the registry for your Zig version):

```zig
// build.zig.zon
.{
    .name = "hello_app",
    .version = "0.1.0",
    .dependencies = .{
        .zig_json = .{
            .url = "https://github.com/example/zig-json/archive/refs/tags/v0.1.0.tar.gz",
            .hash = "1220...", // from `zig fetch` output
        },
    },
}
```

In **`build.zig`**, resolve the dependency:

```zig
const dep = b.dependency("zig_json", .{
    .target = target,
    .optimize = optimize,
});
exe.root_module.addImport("json", dep.module("json"));
```

Workflow:

```text
# Add URL + placeholder hash to build.zig.zon, then:
zig fetch
# Copy the printed hash into build.zig.zon
zig build
```

| Method | When |
|--------|------|
| **Registry / URL + hash** | Published Zig packages |
| **`.path = "vendor/foo"`** | Vendored or monorepo sibling |
| **Git URL in `.zon`** | Unreleased libraries |

## 7. Cross-compilation

Zig emphasizes **cross-compiling** from any host:

```text
zig build -Dtarget=aarch64-linux-gnu
zig build -Dtarget=x86_64-windows-gnu
```

**`zig targets`** lists supported triples. **`zig cc`** can build C dependencies with the same target — useful for mixed Zig/C projects (**Part IV**).

## 8. What to put in a shareable package

- **`pub`** only what callers need; keep helpers file-private.
- **Document** public functions with **`///`** comments.
- **`test`** blocks next to the code they exercise; integration tests as separate **`test`** roots in **`build.zig`** if needed.
- **`README`**, **LICENSE**, accurate **`build.zig.zon`** **`fingerprint`** / version before publishing.
- Prefer **explicit allocators** in public APIs (**Part III**) — don’t hide **`GeneralPurposeAllocator`** inside a library boundary without documenting it.

## 9. Quick troubleshooting

| Problem | Check |
|---------|--------|
| `failed to find` module | **`addImport`** name matches **`@import`**; path in **`build.zig`** |
| Hash mismatch on fetch | Re-run **`zig fetch`**, update **`build.zig.zon`** |
| Link errors on Windows | Target triple, **`libc`**, native `.lib` search paths |
| API changed after upgrade | [Release notes](https://ziglang.org/download/) — build API moves between minors |

## 10. Related

- **Part I** — syntax, errors, optionals [Basics & toolchain](i-basics-and-toolchain.md)
- **Part III** — **[Ziglings](https://github.com/ratfactor/ziglings)** exercises [Learn with Ziglings](iii-learn-with-ziglings.md)
- **Part IV** — allocators, **comptime**, **C** [Memory, comptime & C interop](iv-memory-comptime-and-c-interop.md)
- **Part V** — [Web MVC project layout](v-mvc.md)
- **Part VI** — [TLS & deployment](vi-tls-and-deployment.md)
- [Zig Build System](https://ziglang.org/documentation/master/#Zig-Build-System) — official reference

---
label: "II"
subtitle: "Modules & packages"
group: "Go"
groupOrder: 1
order: 2
---
Go — Part II: Modules & packages
A **module** is a versioned tree of packages (`go.mod`). A **package** is one directory of `.go` files. **`go`** fetches dependencies from a **proxy**, records them in **`go.sum`**, and builds a reproducible graph.

See **Part I** [Basics & toolchain](i-basics-and-toolchain.md) for **`go run`**, **`go build`**, and package visibility.

## 1. What a module is

| File / command | Role |
|----------------|------|
| **`go.mod`** | Module path, Go version, `require` / `replace` |
| **`go.sum`** | Cryptographic checksums of selected versions |
| **`go get pkg@version`** | Add or upgrade a dependency |
| **`go mod tidy`** | Match `go.mod` to actual imports |
| **`go mod download`** | Fetch modules into the cache |

```go
// go.mod
module github.com/example/billing

go 1.22

require (
	github.com/google/uuid v1.6.0
)
```

The **module path** is the import prefix. Packages inside the module are imported as **`modulepath/subdir`**.

```text
billing/
  go.mod                 module github.com/example/billing
  cmd/api/main.go        package main
  internal/store/pg.go   package store   // importable only inside this module
  user/user.go           package user    // github.com/example/billing/user
```

## 2. Everyday module commands

```text
go mod init github.com/you/app
go get github.com/google/uuid@latest
go get github.com/google/uuid@v1.6.0
go mod tidy
go list -m all                 # full module graph
go list -f '{{.Path}}' ./...   # packages in this module
```

**`go get`** outside a module is not how you “install a language” — use it **inside** a module to change requirements. To install a **CLI** onto your machine:

```text
go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest
```

Binaries land in **`$(go env GOPATH)/bin`** — put that directory on **`PATH`**.

### Auto-reload while developing

Go does not hot-swap a running process. A file watcher rebuilds and restarts. Common choice: **[Air](https://github.com/air-verse/air)**.

```text
go install github.com/air-verse/air@latest
air
```

## 3. Packages

- **One package name per directory.** Files in `user/` all say **`package user`** (or **`package user_test`** for an external test package).
- **`package main`** is the exception: it builds an executable; put binaries under **`cmd/<name>/`** in larger repos.
- Import paths are **URLs-shaped strings**, not relative file paths (`import "github.com/example/billing/user"`).
- **Blank import** **`import _ "net/http/pprof"`** runs `init()` for side effects.

```go
package main

import (
	"fmt"

	"github.com/example/billing/user"
	_ "net/http/pprof"
)

func main() {
	fmt.Println(user.Hello("Ada"))
}
```

### `internal/`

Any package under a directory named **`internal`** can be imported only by a parent of that `internal` tree. Use it for code you do **not** want other modules to depend on.

```text
github.com/example/billing/internal/store     ← ok from this module
github.com/other/app importing that path      ← compile error
```

## 4. Versioning

- Versions follow **semver** tags (`v1.2.3`).
- **v2+** must include the major version in the module path (`github.com/foo/bar/v2`) — the [import compatibility rule](https://go.dev/blog/module-compatibility).
- **`go.sum`** is committed. **`GOPROXY`** (default `proxy.golang.org`) plus **`GOSUMDB`** verify downloads.

```text
go get example.com/foo@v1.4.0     # stay on v1 API
go get example.com/foo/v2@v2.0.1  # new major = new import path
```

### `replace` and local development

```go
// go.mod
replace github.com/example/lib => ../lib
```

**`replace`** is for local forks and unpublished work. Do not rely on it in published libraries — consumers will not pick up your replace.

## 5. Workspaces (`go.work`)

A **workspace** lets several modules on disk resolve each other without `replace` in every `go.mod`. Useful for a repo with **`api/`**, **`pkg/`**, and a **library** you are editing together.

```text
go work init ./api ./pkg
go work use ./experiments
```

```text
// go.work
go 1.22

use (
	./api
	./pkg
)
```

Commit **`go.work`** only if the whole team should share the same multi-module layout. Many teams keep it gitignored and generate it locally.

## 6. Build tags, `cmd/`, and layout

A common service layout:

```text
myapi/
  go.mod
  cmd/api/main.go          // binary entry — wiring only
  internal/http/           // handlers
  internal/store/          // DB
  internal/domain/         // types and rules
```

**Build constraints** at the top of a file:

```go
//go:build linux && amd64

package cpu
```

**`GOOS`** / **`GOARCH`** cross-compile without extra toolchains for pure Go:

```text
GOOS=linux GOARCH=amd64 go build -o api-linux ./cmd/api
GOOS=windows GOARCH=amd64 go build -o api.exe ./cmd/api
```

On Windows PowerShell:

```text
$env:GOOS="linux"; $env:GOARCH="amd64"; go build -o api-linux ./cmd/api
```

## 7. Vendoring (optional)

**`go mod vendor`** copies dependencies into **`vendor/`**. Builds then use **`-mod=vendor`**. Useful for air-gapped CI; most public projects skip vendor and rely on the module cache + `go.sum`.

```text
go mod vendor
go build -mod=vendor ./...
```

Next: **Part III** — structs, methods, interfaces, and errors [Types, interfaces & errors](iii-types-interfaces-and-errors.md). **Part V** covers tests and linters [Testing & tooling](v-testing-and-tooling.md).

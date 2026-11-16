---
label: "V"
subtitle: "Testing & tooling"
group: "Go"
groupOrder: 1
order: 5
---
Go — Part V: Testing & tooling
**`go test`** is built in — no extra runner for unit tests. Table tests, **`httptest`**, the **race detector**, **`gofmt`**, and **`golangci-lint`** are the everyday quality bar.

Assumes **Part II** [Modules & packages](ii-modules-and-packages.md) and **Part IV** [Concurrency](iv-concurrency.md) for `-race`.

## 1. `go test`

Files named **`*_test.go`** are compiled only for tests. **`func TestXxx(t *testing.T)`** is a test. Run from the module root:

```text
go test ./...
go test -v ./internal/store
go test -count=1 ./...          # skip cache
go test -run TestLoadUser ./...
```

```go
package greet

import "testing"

func TestHello(t *testing.T) {
	got := Hello("Ada")
	if got != "hello, Ada" {
		t.Fatalf("Hello() = %q", got)
	}
}
```

### Table-driven tests

Idiomatic: a slice of cases, **`t.Run`** per name.

```go
func TestDivide(t *testing.T) {
	tests := []struct {
		name    string
		a, b    int
		want    int
		wantErr bool
	}{
		{name: "ok", a: 10, b: 2, want: 5},
		{name: "by zero", a: 1, b: 0, wantErr: true},
	}
	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := divide(tt.a, tt.b)
			if tt.wantErr {
				if err == nil {
					t.Fatal("expected error")
				}
				return
			}
			if err != nil {
				t.Fatal(err)
			}
			if got != tt.want {
				t.Fatalf("got %d want %d", got, tt.want)
			}
		})
	}
}
```

**`t.Helper()`** on assertion helpers so failures point at the call site. **`t.Parallel()`** runs tests in parallel — do not share mutable package state.

### External test package

**`package greet_test`** imports **`greet`** as a client. Use it to test the **exported API** only (good for public libraries).

## 2. HTTP tests (`net/http/httptest`)

```go
func TestHealth(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
	})
	srv := httptest.NewServer(mux)
	defer srv.Close()

	res, err := http.Get(srv.URL + "/health")
	if err != nil {
		t.Fatal(err)
	}
	defer res.Body.Close()
	if res.StatusCode != http.StatusOK {
		t.Fatalf("status %d", res.StatusCode)
	}
}
```

**`httptest.NewRecorder()`** tests a handler without a TCP port. Handler-level tests pair with [Templates — controllers (Go)](../../templates/controllers/v-go-nethttp.md).

## 3. Benchmarks, fuzz, examples

```go
func BenchmarkHello(b *testing.B) {
	for i := 0; i < b.N; i++ {
		_ = Hello("Ada")
	}
}
```

```text
go test -bench=BenchmarkHello -benchmem ./...
```

**Fuzzing** (`go test -fuzz=FuzzXxx`) feeds random inputs; keep a **`testdata/fuzz`** corpus in git when it finds a crash.

**Example functions** (`func ExampleHello()`) run as tests and appear in **`pkg.go.dev`** docs if the output comment matches.

## 4. Format, vet, lint

| Tool | Role |
|------|------|
| **`gofmt` / `go fmt`** | Canonical format — run on save |
| **`goimports`** | gofmt + manage imports |
| **`go vet`** | Suspicious constructs (printf, unreachable) |
| **`staticcheck`** | Extra analyzers |
| **`golangci-lint`** | Meta-linter (vet, staticcheck, errcheck, …) |

```text
go fmt ./...
go vet ./...
go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest
golangci-lint run ./...
```

CI: **fmt check** (`gofmt -l` must be empty) + **`go test -race ./...`** + **lint**. Do not argue about braces — **`gofmt`** already decided.

## 5. Race detector and coverage

```text
go test -race ./...
go test -coverprofile=cover.out ./...
go tool cover -html=cover.out
```

Coverage is a **hint**, not a goal. Prefer tests that hit error paths and concurrency over 100% lines.

## 6. `pprof` and tracing

Import **`net/http/pprof`** on an internal admin port (never public without auth):

```go
import _ "net/http/pprof"

go func() {
	log.Println(http.ListenAndServe("localhost:6060", nil))
}()
```

```text
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
go tool pprof http://localhost:6060/debug/pprof/heap
```

**`go tool trace`** from **`runtime/trace`** or test **`-trace`**. Use this when latency or RAM is a mystery, not as a first debugging step.

## 7. Debugger

**[Delve](https://github.com/go-delve/delve)** is the usual debugger (`dlv debug`, VS Code / GoLand adapters). **`log/slog`** structured logs plus request IDs (see [Templates — logging (Go)](../../templates/logging/v-go-nethttp.md)) find most production issues faster than attaching a debugger to a container.

```go
logger := slog.New(slog.NewJSONHandler(os.Stdout, nil))
logger.Info("user loaded", "id", id)
```

## 8. Useful `go` env

```text
go env GOPROXY GOSUMDB GO111MODULE CGO_ENABLED
```

| Variable | Typical |
|----------|---------|
| **`CGO_ENABLED=0`** | Pure-Go static-ish binaries (Linux) |
| **`GOTOOLCHAIN=auto`** | Download a newer toolchain if `go.mod` asks |
| **`GOPROXY=off`** | Force module cache only (repro / air-gap) |

Next: **Part VI** — [HTTP servers & CLI](vi-http-and-cli.md) (`net/http`, Cobra, cross-compile).

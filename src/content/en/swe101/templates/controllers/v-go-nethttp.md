---
label: "V"
subtitle: "Go — net/http"
group: "Controllers"
order: 5
---
Controller template — Go (net/http)
Minimal handlers with the standard library (Go 1.22+ patterns). No framework required.

## Template

```go
package main

import (
	"encoding/json"
	"net/http"
	"sync"

	"github.com/google/uuid"
)

type createItemRequest struct {
	Name string `json:"name"`
}

type itemResponse struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}

// Demo only — replace with a service + DB
var (
	mu    sync.RWMutex
	store = map[string]itemResponse{}
)

func writeJSON(w http.ResponseWriter, status int, v any) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func listItems(w http.ResponseWriter, r *http.Request) {
	mu.RLock()
	defer mu.RUnlock()
	out := make([]itemResponse, 0, len(store))
	for _, item := range store {
		out = append(out, item)
	}
	writeJSON(w, http.StatusOK, out)
}

func getItem(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	mu.RLock()
	item, ok := store[id]
	mu.RUnlock()
	if !ok {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "Not found"})
		return
	}
	writeJSON(w, http.StatusOK, item)
}

func createItem(w http.ResponseWriter, r *http.Request) {
	var body createItemRequest
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil || body.Name == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "name is required"})
		return
	}
	item := itemResponse{ID: uuid.NewString(), Name: body.Name}
	mu.Lock()
	store[item.ID] = item
	mu.Unlock()
	w.Header().Set("Location", "/api/items/"+item.ID)
	writeJSON(w, http.StatusCreated, item)
}

func updateItem(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	var body createItemRequest
	if err := json.NewDecoder(r.Body).Decode(&body); err != nil || body.Name == "" {
		writeJSON(w, http.StatusBadRequest, map[string]string{"error": "name is required"})
		return
	}
	mu.Lock()
	defer mu.Unlock()
	if _, ok := store[id]; !ok {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "Not found"})
		return
	}
	item := itemResponse{ID: id, Name: body.Name}
	store[id] = item
	writeJSON(w, http.StatusOK, item)
}

func deleteItem(w http.ResponseWriter, r *http.Request) {
	id := r.PathValue("id")
	mu.Lock()
	_, ok := store[id]
	if ok {
		delete(store, id)
	}
	mu.Unlock()
	if !ok {
		writeJSON(w, http.StatusNotFound, map[string]string{"error": "Not found"})
		return
	}
	w.WriteHeader(http.StatusNoContent)
}

func main() {
	mux := http.NewServeMux()
	mux.HandleFunc("GET /api/items", listItems)
	mux.HandleFunc("GET /api/items/{id}", getItem)
	mux.HandleFunc("POST /api/items", createItem)
	mux.HandleFunc("PUT /api/items/{id}", updateItem)
	mux.HandleFunc("DELETE /api/items/{id}", deleteItem)
	_ = http.ListenAndServe(":8080", mux)
}
```

Module helper: `go get github.com/google/uuid` (or generate IDs yourself).

## Notes

| Topic | Practice |
|-------|----------|
| **Thin handlers** | Call methods on an `ItemService` struct |
| **Middleware** | Logging, auth, panic recovery around `mux` |
| **Frameworks** | Chi / Echo / Gin wrap the same handler idea |

## Next

[Controllers overview](i-overview.md) · [Templates overview](../i-overview.md).

---
label: "IV"
subtitle: "JavaScript — Express"
group: "Concurrency"
order: 4
---
Concurrency template — JavaScript (Express)
Node runs your handlers on a **single-threaded event loop**. Async I/O interleaves fine; **CPU-bound** work blocks every request. Parallelize independent awaits with `Promise.all`, cap fan-out, and offload heavy compute to `worker_threads`.

## Template code

```js
// Async fan-out: independent promises run concurrently
async function loadCombined(itemId) {
  const [item, tags] = await Promise.all([
    fetchItem(itemId),
    fetchTags(itemId),
  ]);
  return { item, tags };
}

async function fetchItem(id) {
  const res = await fetch(`https://api.example.com/items/${id}`, {
    signal: AbortSignal.timeout(5000), // always time out
  });
  return res.json();
}

async function fetchTags(id) {
  const res = await fetch(`https://api.example.com/items/${id}/tags`, {
    signal: AbortSignal.timeout(5000),
  });
  return res.json();
}
```

Bound parallelism so one request can't open thousands of sockets:

```js
async function mapWithLimit(items, limit, fn) {
  const results = [];
  const executing = new Set();
  for (const item of items) {
    const p = Promise.resolve().then(() => fn(item));
    results.push(p);
    executing.add(p);
    p.finally(() => executing.delete(p));
    if (executing.size >= limit) await Promise.race(executing);
  }
  return Promise.all(results);
}

// at most 10 concurrent lookups
const items = await mapWithLimit(ids, 10, (id) => fetchItem(id));
```

Offload CPU-bound work to a worker thread — never block the loop:

```js
import { Worker } from "node:worker_threads";

function hashInWorker(data) {
  return new Promise((resolve, reject) => {
    const worker = new Worker("./hash-worker.js", { workerData: data });
    worker.once("message", resolve);
    worker.once("error", reject);
  });
}

// hash-worker.js
// const { parentPort, workerData } = require("node:worker_threads");
// const { createHash } = require("node:crypto");
// parentPort.postMessage(createHash("sha256").update(workerData).digest("hex"));
```

## Notes

| Topic | Practice |
|-------|----------|
| **Don't block the loop** | No sync crypto/`JSON.parse` of huge payloads/`while` loops on the request path |
| **`Promise.all` vs `allSettled`** | `all` rejects fast; `allSettled` when partial results are OK |
| **Cap concurrency** | Unbounded `Promise.all(ids.map(...))` can exhaust FDs/upstreams |
| **CPU work** | `worker_threads` (or a queue + separate service) for hashing, image work |
| **Shared state** | One process = shared module state; scale with the `cluster` module / multiple instances |

## Next

[Go — net/http](v-go-nethttp.md) · [Concurrency overview](i-overview.md).

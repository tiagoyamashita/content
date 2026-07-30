---
label: "IV"
subtitle: "JavaScript — Express"
group: "Resilience"
order: 4
---
Resilience template — JavaScript (Express)
**fetch** wrapper with timeout (AbortSignal) and exponential backoff retry for idempotent GETs. Outbound setup: [HTTP clients](../http-clients/iv-javascript-express.md).

## Template code

```javascript
const CATALOG_BASE = "https://catalog.example.com";
const DEFAULT_TIMEOUT_MS = 5_000;
const MAX_ATTEMPTS = 3;

/**
 * Fetch with timeout — always pass a signal.
 * @param {string} url
 * @param {RequestInit & { timeoutMs?: number }} options
 */
async function fetchWithTimeout(url, options = {}) {
  const { timeoutMs = DEFAULT_TIMEOUT_MS, ...init } = options;
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, { ...init, signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isRetryableStatus(status) {
  return status === 429 || status === 503 || status >= 500;
}

/**
 * Retry with backoff — **GET / HEAD only** unless caller proves idempotency.
 * @template T
 * @param {() => Promise<T>} fn
 * @param {{ maxAttempts?: number }} opts
 */
async function retryWithBackoff(fn, { maxAttempts = MAX_ATTEMPTS } = {}) {
  let lastError;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (err) {
      lastError = err;
      if (attempt === maxAttempts) break;
      const delayMs = 100 * 2 ** (attempt - 1) + Math.random() * 50;
      await sleep(delayMs);
    }
  }
  throw lastError;
}

/** Idempotent catalog read — safe to retry. */
async function listCatalogItems() {
  return retryWithBackoff(async () => {
    const res = await fetchWithTimeout(`${CATALOG_BASE}/api/items`, {
      method: "GET",
      headers: { Accept: "application/json" },
    });
    if (!res.ok) {
      if (isRetryableStatus(res.status)) {
        throw new Error(`upstream ${res.status}`);
      }
      const err = new Error(`client error ${res.status}`);
      err.retryable = false;
      throw err;
    }
    return res.json();
  });
}

/** POST — no automatic retry in this stub. */
async function createCatalogItem(name) {
  const res = await fetchWithTimeout(`${CATALOG_BASE}/api/items`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name }),
  });
  if (!res.ok) throw new Error(`create failed: ${res.status}`);
  return res.json();
}

// Express route — graceful degradation:
//
// router.get("/items", async (req, res) => {
//   try {
//     const items = await listCatalogItems();
//     res.json({ items });
//   } catch {
//     res.json({ items: [], degraded: true });
//   }
// });

module.exports = {
  fetchWithTimeout,
  retryWithBackoff,
  listCatalogItems,
  createCatalogItem,
};
```

## Notes

| Topic | Practice |
|-------|----------|
| **AbortSignal** | Node 18+ global `fetch` needs explicit timeout — no default |
| **Retry scope** | Wrapper is for reads — document why POST is excluded |
| **Jitter** | Random delay reduces thundering herd on recovery |
| **Circuit breaker** | Add `opossum` or similar when one upstream dominates error budget |

## Next

[Go — net/http](v-go-nethttp.md) · [Resilience overview](i-overview.md).

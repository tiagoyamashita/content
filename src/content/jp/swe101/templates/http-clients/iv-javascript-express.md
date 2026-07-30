---
label: "IV"
subtitle: "JavaScript — Express"
group: "HTTP clients"
order: 4
---
HTTP client template — JavaScript (Express)
**`fetch`** with **`AbortSignal.timeout`** and typed **`ItemResponse`**. Shapes: [DTOs](../dtos/iv-javascript-express.md) · caller: [Services](../services/iv-javascript-express.md).

## Configuration

```javascript
const CATALOG_BASE_URL = process.env.CATALOG_BASE_URL ?? "https://catalog.example.com";
const CATALOG_TIMEOUT_MS = Number(process.env.CATALOG_TIMEOUT_MS ?? 3000);
```

## Template (fetch)

```javascript
/**
 * @typedef {{ id: number, name: string }} ItemResponse
 */

class CatalogError extends Error {
  constructor(message, { cause } = {}) {
    super(message, { cause });
    this.name = "CatalogError";
  }
}

/**
 * @param {number} itemId
 * @param {string} requestId
 * @returns {Promise<ItemResponse | null>}
 */
async function getItem(itemId, requestId) {
  const url = `${CATALOG_BASE_URL.replace(/\/$/, "")}/items/${itemId}`;

  let response;
  try {
    response = await fetch(url, {
      method: "GET",
      headers: {
        Accept: "application/json",
        "X-Request-Id": requestId,
      },
      signal: AbortSignal.timeout(CATALOG_TIMEOUT_MS),
    });
  } catch (err) {
    throw new CatalogError("catalog unreachable", { cause: err });
  }

  if (response.status === 404) {
    return null;
  }
  if (!response.ok) {
    throw new CatalogError(`catalog error: ${response.status}`);
  }

  /** @type {ItemResponse} */
  const body = await response.json();
  if (typeof body.id !== "number" || typeof body.name !== "string") {
    throw new CatalogError("invalid catalog response shape");
  }
  return body;
}

module.exports = { getItem, CatalogError };
```

## Template (axios alternative)

```javascript
const axios = require("axios");

const catalog = axios.create({
  baseURL: process.env.CATALOG_BASE_URL ?? "https://catalog.example.com",
  timeout: Number(process.env.CATALOG_TIMEOUT_MS ?? 3000),
  headers: { Accept: "application/json" },
});

async function getItemAxios(itemId, requestId) {
  try {
    const { data, status } = await catalog.get(`/items/${itemId}`, {
      headers: { "X-Request-Id": requestId },
      validateStatus: (s) => s === 404 || (s >= 200 && s < 300),
    });
    if (status === 404) return null;
    return data;
  } catch (err) {
    if (err.code === "ECONNABORTED") {
      throw new CatalogError("catalog timeout", { cause: err });
    }
    throw new CatalogError("catalog unreachable", { cause: err });
  }
}
```

Prefer **`fetch` + AbortSignal** in Node 18+; axios if you already depend on it.

## Notes

| Topic | Practice |
|-------|----------|
| **AbortSignal.timeout** | Mandatory — no unbounded wait |
| **404 → null** | Service decides 404 vs default item |
| **Request ID** | Pass `req.requestId` from [Middleware](../middleware/iv-javascript-express.md) |
| **Validate shape** | Remote APIs change — catch before returning garbage |
| **Keep out of routes** | Export functions from a `catalogClient` module |

## Next

[Go — net/http](v-go-nethttp.md) · [HTTP clients overview](i-overview.md).

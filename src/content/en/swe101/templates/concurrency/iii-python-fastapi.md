---
label: "III"
subtitle: "Python — FastAPI"
group: "Concurrency"
order: 3
---
Concurrency template — Python (FastAPI)
FastAPI runs on a **single-threaded asyncio event loop**. `async def` handlers interleave on I/O; a **blocking** call (CPU work, sync DB driver) freezes every request. Offload blocking work to a thread/process executor and cap parallel fan-out.

## Template code

```python
import asyncio
import hashlib
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

import httpx
from fastapi import FastAPI

app = FastAPI()


@dataclass
class Item:
    id: str
    name: str


# Async fan-out: independent awaits run concurrently
async def load_combined(client: httpx.AsyncClient, item_id: str) -> dict:
    item_task = fetch_item(client, item_id)
    tags_task = fetch_tags(client, item_id)
    item, tags = await asyncio.gather(item_task, tags_task)  # concurrent
    return {"item": item, "tags": tags}


async def fetch_item(client: httpx.AsyncClient, item_id: str) -> dict:
    r = await client.get(f"/api/items/{item_id}", timeout=5.0)
    return r.json()


async def fetch_tags(client: httpx.AsyncClient, item_id: str) -> list[str]:
    r = await client.get(f"/api/items/{item_id}/tags", timeout=5.0)
    return r.json()
```

Bound the parallelism so one request can't launch thousands of tasks:

```python
async def fetch_many(client: httpx.AsyncClient, ids: list[str]) -> list[dict]:
    sem = asyncio.Semaphore(10)  # at most 10 in flight

    async def one(item_id: str) -> dict:
        async with sem:
            r = await client.get(f"/api/items/{item_id}", timeout=5.0)
            return r.json()

    return await asyncio.gather(*(one(i) for i in ids))
```

Never block the loop — push CPU-bound work to a process pool:

```python
_pool = ProcessPoolExecutor(max_workers=4)


def heavy_hash(data: bytes) -> str:      # CPU-bound, pure function
    return hashlib.sha256(data).hexdigest()


@app.post("/api/items/checksum")
async def checksum(payload: bytes) -> dict:
    loop = asyncio.get_running_loop()
    # offload so the event loop stays responsive
    digest = await loop.run_in_executor(_pool, heavy_hash, payload)
    return {"sha256": digest}
```

## Capacity by version

CPython's **GIL** is the defining capacity fact: on standard builds only one thread executes Python bytecode at a time, so threads do **not** add CPU parallelism. State the interpreter version your scaling plan assumes.

| CPython version | Parallelism story | How you scale |
|-----------------|-------------------|---------------|
| **≤ 3.11** | One GIL; threads for I/O only | **Processes** — run `workers ≈ CPU cores` (Gunicorn/Uvicorn) |
| **3.12** | Per-interpreter GIL (PEP 684, sub-interpreters) | Still process-based in practice for most web apps |
| **3.13** | Experimental **free-threaded** build (`python3.13t`, PEP 703) — GIL can be disabled | Threads start to scale CPU; ecosystem/C-extension support still maturing |
| **3.14+** | Free-threading moving to officially supported | Same direction; verify your deps ship free-threaded wheels |

One instance's capacity:

```text
total concurrent requests  ≈  worker_processes  ×  in-flight coroutines per loop
worker_processes           ≈  CPU cores (CPU-bound)  or  higher (I/O-bound)
```

```bash
# One loop per worker; N workers ≈ cores. Each worker is a separate process + GIL.
uvicorn app:app --workers 4
# or: gunicorn -k uvicorn.workers.UvicornWorker -w 4 app:app
```

**Watch out:** adding `threading.Thread`s for CPU work on ≤3.12 buys nothing — the GIL serializes them; use `ProcessPoolExecutor` (shown above). Don't assume a single async worker uses all cores — it uses **one**. Size worker count to cores and memory, and keep per-loop fan-out bounded with `asyncio.Semaphore`.

## Notes

| Topic | Practice |
|-------|----------|
| **`async` all the way** | Use async DB/HTTP drivers (`httpx`, `asyncpg`) — a sync call blocks the loop |
| **Sync handlers** | A plain `def` endpoint runs in FastAPI's threadpool — fine for blocking libs, but bounded |
| **CPU work** | Offload to `ProcessPoolExecutor` (threads don't help — GIL) |
| **Cap fan-out** | `asyncio.Semaphore` — unbounded `gather` can exhaust connections |
| **Shared state** | Module globals are shared across tasks — guard with `asyncio.Lock`, or avoid |

## Next

[JavaScript — Express](iv-javascript-express.md) · [Concurrency overview](i-overview.md).

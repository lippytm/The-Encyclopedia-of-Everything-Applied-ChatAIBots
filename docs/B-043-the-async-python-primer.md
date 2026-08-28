# B-043: The Async Python Primer

### asyncio, async def, await, and Concurrent I/O Without Threads

> *"Synchronous code waits. While it waits for a network response, it does nothing — not a single other task. Async code says: 'While I'm waiting for that API call, let me start ten more.' asyncio is Python's built-in answer to concurrent I/O. One thread, zero blocking, full speed."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Understand the difference between sync, async, threading, and multiprocessing
2. Write `async def` coroutines and use `await` correctly
3. Run multiple coroutines concurrently with `asyncio.gather`
4. Use `aiohttp` for async HTTP requests
5. Build an `async_fetcher.py` — a concurrent multi-URL API fetcher

**Prerequisite:** B-032 (HTTP requests), B-037 (time concepts)

**Build Artifact:** `~/developer-workspace/projects/python-foundations/async_fetcher.py`

**Credential:** `CCSLL-L1-B043-AsyncEngineer` — on-chain on Base

---

## Chapter 1: Why Async?

```python
import time

# SYNC: sequential — each request waits for the previous one
def fetch_sync(urls: list[str]) -> None:
    for url in urls:
        time.sleep(1)   # simulate network delay
        print(f"Fetched: {url}")

start = time.time()
fetch_sync(["url1", "url2", "url3"])
print(f"Sync took: {time.time() - start:.1f}s")   # ~3.0s

# ASYNC: concurrent — all three start, all finish together
import asyncio

async def fetch_async(url: str) -> str:
    await asyncio.sleep(1)   # yields control; doesn't block
    return f"Fetched: {url}"

async def main_async() -> None:
    urls = ["url1", "url2", "url3"]
    results = await asyncio.gather(*[fetch_async(url) for url in urls])
    for r in results:
        print(r)

start = time.time()
asyncio.run(main_async())
print(f"Async took: {time.time() - start:.1f}s")   # ~1.0s  — 3x faster
```

---

## Chapter 2: async def, await, and coroutines

```python
import asyncio

# 'async def' creates a coroutine function
async def greet(name: str) -> str:
    await asyncio.sleep(0.1)   # simulate async work
    return f"Hello, {name}!"

# A coroutine is not called immediately — you must await it
async def main() -> None:
    # This schedules greet and waits for its result
    result = await greet("Charles")
    print(result)

asyncio.run(main())   # entry point — runs the event loop

# RULE: you can only 'await' inside an 'async def' function
# RULE: asyncio.run() is called ONCE at the top level

# Chaining coroutines
async def step1() -> str:
    await asyncio.sleep(0.05)
    return "step1 done"

async def step2(input: str) -> str:
    await asyncio.sleep(0.05)
    return f"step2 received: {input}"

async def pipeline() -> None:
    result1 = await step1()
    result2 = await step2(result1)
    print(result2)

asyncio.run(pipeline())
```

---

## Chapter 3: asyncio.gather — Concurrent Execution

```python
import asyncio
import time

async def task(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return f"{name} done after {delay}s"

async def sequential() -> None:
    """Sequential: total time = sum of all delays"""
    t = time.time()
    r1 = await task("A", 1.0)
    r2 = await task("B", 1.0)
    r3 = await task("C", 1.0)
    print(f"Sequential: {time.time()-t:.1f}s  — {r1}, {r2}, {r3}")

async def concurrent() -> None:
    """Concurrent: total time = max delay"""
    t = time.time()
    results = await asyncio.gather(
        task("A", 1.0),
        task("B", 1.0),
        task("C", 1.0),
    )
    print(f"Concurrent: {time.time()-t:.1f}s  — {results}")

asyncio.run(sequential())   # ~3.0s
asyncio.run(concurrent())   # ~1.0s

# gather also handles exceptions
async def might_fail(n: int) -> int:
    if n == 2:
        raise ValueError(f"Task {n} failed!")
    return n * 10

async def safe_gather() -> None:
    results = await asyncio.gather(
        might_fail(1),
        might_fail(2),
        might_fail(3),
        return_exceptions=True,   # don't cancel all on one failure
    )
    for r in results:
        if isinstance(r, Exception):
            print(f"  Error: {r}")
        else:
            print(f"  Result: {r}")

asyncio.run(safe_gather())
```

---

## Chapter 4: asyncio with Real HTTP — aiohttp

```python
import asyncio
import aiohttp
from typing import Optional

async def fetch_json(
    session: aiohttp.ClientSession,
    url: str,
) -> Optional[dict]:
    """Fetch a URL and return parsed JSON, or None on error."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            resp.raise_for_status()
            return await resp.json()
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None

async def fetch_all(urls: list[str]) -> list[Optional[dict]]:
    """Fetch all URLs concurrently using a shared session."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_json(session, url) for url in urls]
        return await asyncio.gather(*tasks, return_exceptions=False)

# Example: fetch 5 GitHub users concurrently
async def main() -> None:
    users = ["torvalds", "gvanrossum", "dhh", "antirez", "lippytm"]
    urls = [f"https://api.github.com/users/{u}" for u in users]
    results = await fetch_all(urls)
    for user, data in zip(users, results):
        if data and isinstance(data, dict):
            print(f"  {user}: {data.get('public_repos', '?')} repos")

asyncio.run(main())
```

---

## Chapter 5: asyncio.Semaphore — Rate Limiting

```python
import asyncio
import aiohttp
from typing import Optional

# Semaphore limits concurrent connections — important for politeness
CONCURRENCY = 5   # max 5 simultaneous requests

async def fetch_with_limit(
    session: aiohttp.ClientSession,
    sem: asyncio.Semaphore,
    url: str,
) -> tuple[str, int]:
    async with sem:   # blocks if 5 are already running
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            return url, resp.status

async def fetch_many(urls: list[str]) -> None:
    sem = asyncio.Semaphore(CONCURRENCY)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_limit(session, sem, url) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
    for result in results:
        if isinstance(result, tuple):
            url, status = result
            print(f"  {status}  {url}")
```

---

## Chapter 6: The Build — Async Fetcher

```python
#!/usr/bin/env python3
"""
async_fetcher.py — B-043 Build Artifact

Concurrent multi-URL API fetcher using asyncio + aiohttp.
Fetches multiple URLs in parallel with rate limiting and timing.

Usage:
    pip install aiohttp
    python3 async_fetcher.py
"""
from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from typing import Optional

import aiohttp

MAX_CONCURRENT = 5
TIMEOUT = aiohttp.ClientTimeout(total=15)
HEADERS = {"User-Agent": "lippytmai-async-fetcher/1.0 (educational)"}


@dataclass
class FetchResult:
    url: str
    status: int
    size: int
    duration: float
    error: Optional[str]


async def fetch_one(
    session: aiohttp.ClientSession,
    sem: asyncio.Semaphore,
    url: str,
) -> FetchResult:
    start = time.time()
    async with sem:
        try:
            async with session.get(url, headers=HEADERS, timeout=TIMEOUT) as resp:
                body = await resp.read()
                duration = time.time() - start
                return FetchResult(
                    url=url,
                    status=resp.status,
                    size=len(body),
                    duration=duration,
                    error=None,
                )
        except asyncio.TimeoutError:
            return FetchResult(url=url, status=0, size=0,
                               duration=time.time()-start, error="Timeout")
        except Exception as e:
            return FetchResult(url=url, status=0, size=0,
                               duration=time.time()-start, error=str(e))


async def fetch_all(urls: list[str]) -> list[FetchResult]:
    sem = asyncio.Semaphore(MAX_CONCURRENT)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, sem, url) for url in urls]
        return await asyncio.gather(*tasks)


def print_report(results: list[FetchResult], total_time: float) -> None:
    print(f"\n=== Async Fetch Report ({len(results)} URLs in {total_time:.2f}s) ===\n")
    print(f"  {'Status':<8} {'Time':>7} {'Size':>10}  URL")
    print("  " + "-" * 70)
    ok = 0
    for r in sorted(results, key=lambda x: x.duration):
        icon = "✅" if r.status == 200 else "❌"
        status = str(r.status) if r.status else r.error or "ERR"
        size_kb = f"{r.size/1024:.1f} KB"
        print(f"  {icon} {status:<6} {r.duration:>6.2f}s {size_kb:>9}  {r.url}")
        if r.status == 200:
            ok += 1
    print(f"\n  Success: {ok}/{len(results)}  |  Total: {total_time:.2f}s\n")


async def main() -> None:
    urls = [
        "https://httpbin.org/get",
        "https://httpbin.org/delay/1",
        "https://httpbin.org/status/200",
        "https://httpbin.org/status/404",
        "https://httpbin.org/json",
        "https://api.github.com/zen",
        "https://api.github.com/octocat",
    ]

    print(f"Fetching {len(urls)} URLs concurrently (max {MAX_CONCURRENT} at once)...")
    start = time.time()
    results = await fetch_all(urls)
    total = time.time() - start
    print_report(results, total)


if __name__ == "__main__":
    asyncio.run(main())
```

```bash
pip install aiohttp
python3 ~/developer-workspace/projects/python-foundations/async_fetcher.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-043 Verification ==="
python3 -c "
import asyncio
import time

async def task(name: str, delay: float) -> str:
    await asyncio.sleep(delay)
    return name

async def main():
    start = time.time()
    results = await asyncio.gather(
        task('A', 0.3),
        task('B', 0.3),
        task('C', 0.3),
    )
    elapsed = time.time() - start
    print(f'Results: {results}')
    print(f'Time: {elapsed:.2f}s  (sequential would be ~0.9s)')
    assert elapsed < 0.7, 'Should run concurrently!'
    print('✅ asyncio.gather works')

asyncio.run(main())
"
```

---

## Further Reading

- 📄 [`docs/B-032-the-internet-in-a-function.md`](B-032-the-internet-in-a-function.md) — Sync HTTP foundation
- 📄 [`docs/B-042-your-first-rest-api.md`](B-042-your-first-rest-api.md) — FastAPI supports async routes natively
- 📄 [`docs/B-041-python-and-the-web-scraping-basics.md`](B-041-python-and-the-web-scraping-basics.md) — Async scraping with aiohttp
- 🏠 [`README.md`](../README.md) — Encyclopedia home

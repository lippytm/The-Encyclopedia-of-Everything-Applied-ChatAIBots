# B-041: Python and the Web — Scraping Basics

### BeautifulSoup, requests, robots.txt, and Ethical Data Collection

> *"The web is the world's largest database — and most of it has no official API. Web scraping is how developers read the web as data. Done ethically, with respect for robots.txt and rate limits, it is a superpower. Done carelessly, it gets your IP banned and causes real harm. Learn the right way."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Fetch HTML pages with `requests` and parse them with `BeautifulSoup`
2. Navigate HTML using CSS selectors and tag traversal
3. Extract text, attributes, and links from web pages
4. Respect `robots.txt`, rate limits, and scraping ethics
5. Build a `price_tracker.py` — an ethical product price monitor

**Prerequisite:** B-032 (HTTP requests), B-036 (type hints)

**Build Artifact:** `~/developer-workspace/projects/python-foundations/price_tracker.py`

**Credential:** `CCSLL-L1-B041-WebEngineer` — on-chain on Base

---

## Chapter 1: Ethics First

Before writing a single line of scraping code, understand the rules:

```python
# Check robots.txt BEFORE scraping any site
# Example: https://example.com/robots.txt

# The three ethical rules:
# 1. Check robots.txt — if Disallow: / — do NOT scrape
# 2. Add delays between requests (time.sleep) — don't hammer servers
# 3. Identify yourself in the User-Agent header

import urllib.robotparser

def can_scrape(url: str, user_agent: str = "*") -> bool:
    """Check if scraping this URL is permitted by robots.txt."""
    from urllib.parse import urlparse
    parsed = urlparse(url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(robots_url)
    try:
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception:
        return True   # assume allowed if robots.txt unreachable

print(can_scrape("https://books.toscrape.com/"))  # True — this site is for practice
```

> **Practice site:** `https://books.toscrape.com` — explicitly built for scraping practice.

---

## Chapter 2: Fetching Pages

```python
import requests
import time
from typing import Optional

HEADERS = {
    "User-Agent": "lippytmai-scraper/1.0 (educational; contact: hello@lippytm.ai)"
}

def fetch(url: str, delay: float = 1.0) -> Optional[str]:
    """Fetch a URL and return HTML, or None on error."""
    time.sleep(delay)   # be polite — always delay between requests
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Fetch error for {url}: {e}")
        return None

html = fetch("https://books.toscrape.com/")
print(html[:200] if html else "Failed")
```

---

## Chapter 3: Parsing with BeautifulSoup

```python
from bs4 import BeautifulSoup

html = "<html><body><h1 id='title'>Hello</h1><p class='text'>World</p></body></html>"
soup = BeautifulSoup(html, "html.parser")

# Find by tag
h1 = soup.find("h1")
print(h1.text)          # Hello
print(h1["id"])         # title

# Find all matching tags
paragraphs = soup.find_all("p")
for p in paragraphs:
    print(p.get_text(strip=True))

# CSS selectors — most powerful
title = soup.select_one("h1#title")
texts = soup.select("p.text")

# Navigate the tree
body = soup.find("body")
first_child = body.find()       # first child element
print(body.children)            # iterator of direct children
print(h1.parent.name)           # body

# Get attributes safely
a = soup.find("a")
href = a.get("href", "")        # no KeyError if missing
```

---

## Chapter 4: Scraping a Real Page — books.toscrape.com

```python
import requests
import time
from bs4 import BeautifulSoup
from dataclasses import dataclass

HEADERS = {"User-Agent": "lippytmai-scraper/1.0 (educational)"}

@dataclass
class Book:
    title: str
    price: float
    rating: int
    available: bool

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

def parse_books(html: str) -> list[Book]:
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for article in soup.select("article.product_pod"):
        title = article.select_one("h3 a")
        price_el = article.select_one("p.price_color")
        rating_el = article.select_one("p.star-rating")
        avail_el  = article.select_one("p.availability")

        if not (title and price_el):
            continue

        price_text = price_el.text.strip().replace("Â", "").replace("£", "")
        try:
            price = float(price_text)
        except ValueError:
            price = 0.0

        rating_class = rating_el["class"][1] if rating_el else "Zero"
        rating = RATING_MAP.get(rating_class, 0)
        available = "In stock" in (avail_el.text if avail_el else "")

        books.append(Book(
            title=title.get("title", title.text.strip()),
            price=price,
            rating=rating,
            available=available,
        ))
    return books

response = requests.get("https://books.toscrape.com/", headers=HEADERS, timeout=10)
if response.ok:
    books = parse_books(response.text)
    for book in sorted(books, key=lambda b: b.price)[:5]:
        print(f"£{book.price:.2f}  ★{book.rating}  {book.title[:50]}")
```

---

## Chapter 5: Pagination

```python
import requests
import time
from bs4 import BeautifulSoup

BASE = "https://books.toscrape.com/catalogue"
HEADERS = {"User-Agent": "lippytmai-scraper/1.0 (educational)"}

def scrape_all_pages(max_pages: int = 3) -> list[dict[str, object]]:
    """Scrape multiple pages with polite delays."""
    all_books: list[dict[str, object]] = []
    url = "https://books.toscrape.com/catalogue/page-1.html"

    for page_num in range(1, max_pages + 1):
        print(f"Scraping page {page_num}...")
        time.sleep(1)   # polite delay
        resp = requests.get(url, headers=HEADERS, timeout=10)
        if not resp.ok:
            break

        soup = BeautifulSoup(resp.text, "html.parser")
        for article in soup.select("article.product_pod"):
            title_el = article.select_one("h3 a")
            price_el = article.select_one("p.price_color")
            if title_el and price_el:
                all_books.append({
                    "title": title_el.get("title", ""),
                    "price": price_el.text.strip(),
                })

        # Find next page link
        next_btn = soup.select_one("li.next a")
        if not next_btn:
            break
        url = f"{BASE}/{next_btn['href']}"

    return all_books

books = scrape_all_pages(max_pages=2)
print(f"Scraped {len(books)} books")
```

---

## Chapter 6: The Build — Price Tracker

```python
#!/usr/bin/env python3
"""
price_tracker.py — B-041 Build Artifact

Ethical price tracker for books.toscrape.com.
Tracks prices over time in a local SQLite database.

Usage: python3 price_tracker.py
"""
from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

import requests
from bs4 import BeautifulSoup

DB_PATH = Path.home() / "developer-workspace" / "projects" / "python-foundations" / "prices.db"
BASE_URL = "https://books.toscrape.com/"
HEADERS = {"User-Agent": "lippytmai-scraper/1.0 (educational; https://lippytm.ai)"}
DELAY = 1.5  # seconds between requests


@dataclass
class BookPrice:
    title: str
    price: float
    scraped_on: str


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT NOT NULL,
            price      REAL NOT NULL,
            scraped_on TEXT NOT NULL
        )
    """)
    conn.execute("CREATE INDEX IF NOT EXISTS idx_title ON price_history(title)")
    conn.commit()


def fetch_html(url: str) -> Optional[str]:
    time.sleep(DELAY)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return resp.text
    except requests.RequestException as e:
        print(f"  ⚠️  Fetch error: {e}")
        return None


def parse_prices(html: str) -> list[BookPrice]:
    soup = BeautifulSoup(html, "html.parser")
    today = date.today().isoformat()
    books: list[BookPrice] = []
    for article in soup.select("article.product_pod"):
        title_el = article.select_one("h3 a")
        price_el = article.select_one("p.price_color")
        if not (title_el and price_el):
            continue
        raw = price_el.text.strip()
        try:
            price = float("".join(c for c in raw if c.isdigit() or c == "."))
        except ValueError:
            continue
        books.append(BookPrice(
            title=title_el.get("title", title_el.text.strip()),
            price=price,
            scraped_on=today,
        ))
    return books


def save_prices(conn: sqlite3.Connection, books: list[BookPrice]) -> int:
    conn.executemany(
        "INSERT INTO price_history (title, price, scraped_on) VALUES (?, ?, ?)",
        [(b.title, b.price, b.scraped_on) for b in books],
    )
    conn.commit()
    return len(books)


def price_report(conn: sqlite3.Connection) -> None:
    print("\n=== Price Tracker Report ===\n")
    rows = conn.execute("""
        SELECT title, MIN(price) as low, MAX(price) as high,
               COUNT(*) as snapshots, MAX(scraped_on) as last_seen
        FROM price_history
        GROUP BY title
        ORDER BY low
        LIMIT 10
    """).fetchall()
    print(f"  {'Title':<45} {'Low':>6} {'High':>6} {'Snaps':>5}")
    print("  " + "-" * 70)
    for row in rows:
        print(f"  {row[0][:44]:<45} £{row[1]:>5.2f} £{row[2]:>5.2f} {row[3]:>5}")
    total = conn.execute("SELECT COUNT(DISTINCT title) FROM price_history").fetchone()[0]
    print(f"\n  Total unique books tracked: {total}\n")


def main() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    print(f"Fetching {BASE_URL}...")
    html = fetch_html(BASE_URL)
    if not html:
        print("Failed to fetch page.")
        conn.close()
        return

    books = parse_prices(html)
    saved = save_prices(conn, books)
    print(f"Saved {saved} price records.")

    price_report(conn)
    conn.close()


if __name__ == "__main__":
    main()
```

```bash
pip install requests beautifulsoup4
python3 ~/developer-workspace/projects/python-foundations/price_tracker.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-041 Verification ==="
python3 -c "
from bs4 import BeautifulSoup

html = '''<html><body>
  <article class='product'><h3><a title='Test Book'>Test</a></h3>
  <p class='price'>£12.99</p></article>
</body></html>'''

soup = BeautifulSoup(html, 'html.parser')
article = soup.select_one('article.product')
title = article.select_one('h3 a').get('title')
price = article.select_one('p.price').text.strip()
print(f'Title: {title}')
print(f'Price: {price}')
print('✅ BeautifulSoup works')
"
```

---

## Further Reading

- 📄 [`docs/B-032-the-internet-in-a-function.md`](B-032-the-internet-in-a-function.md) — HTTP requests foundation
- 📄 [`docs/B-039-sqlite-your-first-database.md`](B-039-sqlite-your-first-database.md) — Storing scraped data
- 📄 [`docs/B-043-the-async-python-primer.md`](B-043-the-async-python-primer.md) — Async scraping at scale
- 🏠 [`README.md`](../README.md) — Encyclopedia home

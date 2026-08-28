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


## Chapter 12: Done-For-You Lessons — Python and the Web: Scraping Basics

> *"Done-for-you means it's already designed, structured, and proven. Your job: execute." — lippytmai*

10 ready-to-use lesson structures for Web Scraping using BeautifulSoup.

---

### DFY Lesson 1: Introduction to Web Scraping

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 01: Introduction to Web Scraping              │
│  Book: B-041  Tool: BeautifulSoup              │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 1: Introduction to Web Scraping. Master BeautifulSoup with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `BeautifulSoup` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 1 of B-041: Introduction to Web Scraping. Give me 3 progressive exercises."

---
### DFY Lesson 2: Core BeautifulSoup Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 02: Core BeautifulSoup Patterns               │
│  Book: B-041  Tool: BeautifulSoup              │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 2: Core BeautifulSoup Patterns. Master BeautifulSoup with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `BeautifulSoup` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 2 of B-041: Core BeautifulSoup Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 3: Three Formats: Ebook, Audiobook, Video

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 03: Three Formats: Ebook, Audiobook, Video    │
│  Book: B-041  Tool: BeautifulSoup              │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 3: Three Formats: Ebook, Audiobook, Video. Master BeautifulSoup with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `BeautifulSoup` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 3 of B-041: Three Formats: Ebook, Audiobook, Video. Give me 3 progressive exercises."

---
### DFY Lesson 4: Common Mistakes in Web Scraping

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 04: Common Mistakes in Web Scraping           │
│  Book: B-041  Tool: BeautifulSoup              │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 4: Common Mistakes in Web Scraping. Master BeautifulSoup with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `BeautifulSoup` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 4 of B-041: Common Mistakes in Web Scraping. Give me 3 progressive exercises."

---
### DFY Lesson 5: Building a Web Scraping Workflow

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 05: Building a Web Scraping Workflow          │
│  Book: B-041  Tool: BeautifulSoup              │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 5: Building a Web Scraping Workflow. Master BeautifulSoup with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `BeautifulSoup` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 5 of B-041: Building a Web Scraping Workflow. Give me 3 progressive exercises."

---
### DFY Lesson 6: Automating with BeautifulSoup

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 06: Automating with BeautifulSoup             │
│  Book: B-041  Tool: BeautifulSoup              │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 6: Automating with BeautifulSoup. Master BeautifulSoup with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `BeautifulSoup` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 6 of B-041: Automating with BeautifulSoup. Give me 3 progressive exercises."

---
### DFY Lesson 7: Testing Your Web Scraping Code

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 07: Testing Your Web Scraping Code            │
│  Book: B-041  Tool: BeautifulSoup              │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 7: Testing Your Web Scraping Code. Master BeautifulSoup with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `BeautifulSoup` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 7 of B-041: Testing Your Web Scraping Code. Give me 3 progressive exercises."

---
### DFY Lesson 8: Production Web Scraping Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 08: Production Web Scraping Patterns          │
│  Book: B-041  Tool: BeautifulSoup              │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 8: Production Web Scraping Patterns. Master BeautifulSoup with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `BeautifulSoup` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 8 of B-041: Production Web Scraping Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 9: Debugging Web Scraping Problems

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 09: Debugging Web Scraping Problems           │
│  Book: B-041  Tool: BeautifulSoup              │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 9: Debugging Web Scraping Problems. Master BeautifulSoup with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `BeautifulSoup` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 9 of B-041: Debugging Web Scraping Problems. Give me 3 progressive exercises."

---
### DFY Lesson 10: Earning Your PEL-L0-B041-WebScraper Credential

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 10: Earning Your PEL-L0-B041-WebScraper Cred  │
│  Book: B-041  Tool: BeautifulSoup              │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 10: Earning Your PEL-L0-B041-WebScraper Credential. Master BeautifulSoup with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `BeautifulSoup` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 10 of B-041: Earning Your PEL-L0-B041-WebScraper Credential. Give me 3 progressive exercises."

---

### Claim Your Credential

Complete all 10 lessons → open Appendix C → run: *"Generate my credential claim for `PEL-L0-B041-WebScraper`."*

---

## Chapter 13: How It Works — Use Cases & Applications

> *"Knowing what to do is different from knowing why it matters." — lippytmai*

### The Mechanism

Web Scraping in Python works because the language was designed to be readable, composable, and deployable. BeautifulSoup is the tool that makes Web Scraping practical.

### 5 Real-World Use Cases

| Domain | Application | Your Credential Unlocks |
|---|---|---|
| Backend Dev | Build APIs and services with BeautifulSoup | PEL-L0-B041-WebScraper → production deployments |
| Data Engineering | Process and transform data pipelines | PEL-L0-B041-WebScraper → ETL roles |
| DevOps/Automation | Automate repetitive tasks | PEL-L0-B041-WebScraper → CI/CD integration |
| AI/ML | Preprocess data and build models | PEL-L0-B041-WebScraper → AI projects |
| Freelance | Deliver Python solutions to clients | PEL-L0-B041-WebScraper → paid work |

### 📘 Mechanism Diagram

```
INPUT → [Web Scraping Layer] → OUTPUT
         ↓
[ACSS Integration] → Hermes Event → Fabric Node
         ↓
[ADA Activation] → lippytmai-launch run B-041
```

### 🎧 Audiobook Narration:

> *"When you master Web Scraping, you're not just learning syntax — you're learning how production Python systems work. Every ACSS component uses these patterns. This is infrastructure knowledge."*

### 🎬 Video: 5-Domain Application Tour

**Scene 1 — Backend:** API or service using Web Scraping
**Scene 2 — Data:** Data pipeline using Web Scraping
**Scene 3 — DevOps:** Automation script using Web Scraping
**Scene 4 — AI/ML:** Model integration using Web Scraping
**Scene 5 — Freelance:** Client deliverable using Web Scraping

---

## Chapter 14: ACSS Explainer Series — Python and the Web: Scraping Basics

> *"You're not just learning Web Scraping. You're building a node in an intelligence network." — lippytmai*

10 explainer lessons connecting Python and the Web: Scraping Basics to the full ACSS architecture.

---

### Explainer 1: ACSS Overview
*intelligence network*

**📘 Ebook Explanation:** Python and the Web: Scraping Basics teaches the Web Scraping layer that feeds the ACSS. Web scraping is how the fabric knowledge graph ingests external data and how the acss research agents gather intelligence.

**📘 Connection Map:**
```
B-041 (Web Scraping) ↕ ACSS Overview ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python and the Web: Scraping Basics connects to ACSS Overview: Python and the Web: Scraping Basics teaches the Web Scraping layer that feeds the ACSS. Web scraping..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACSS Overview in ACSS diagram
- 10–35s: Zoom to where B-041 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-041

**🤖 Copilot Prompt:** > *"Explain how Web Scraping fits the ACSS. What role does B-041 play?"*

---
### Explainer 2: Hermes Event Routing
*cross-system message bus*

**📘 Ebook Explanation:** Hermes routes Web Scraping practice events. Completing an exercise emits a `skill.practice` event.

**📘 Connection Map:**
```
B-041 (Web Scraping) ↕ Hermes Event Routing ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python and the Web: Scraping Basics connects to Hermes Event Routing: Hermes routes Web Scraping practice events. Completing an exercise emits a `skill.practice` event...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Hermes Event Routing in ACSS diagram
- 10–35s: Zoom to where B-041 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-041

**🤖 Copilot Prompt:** > *"Show the Hermes event schema for a B-041 skill-complete event."*

---
### Explainer 3: Fabric Knowledge Graph
*pattern synthesis*

**📘 Ebook Explanation:** Fabric stores every Web Scraping concept as a knowledge node connected to related books.

**📘 Connection Map:**
```
B-041 (Web Scraping) ↕ Fabric Knowledge Graph ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python and the Web: Scraping Basics connects to Fabric Knowledge Graph: Fabric stores every Web Scraping concept as a knowledge node connected to related books...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Fabric Knowledge Graph in ACSS diagram
- 10–35s: Zoom to where B-041 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-041

**🤖 Copilot Prompt:** > *"Generate the Fabric node definition for the core concept of B-041."*

---
### Explainer 4: Clone Engine Identity
*AI persona system*

**📘 Ebook Explanation:** lippytmai teaches Python and the Web: Scraping Basics in Teach mode. The Clone Engine maintains consistent voice across all 300 books.

**📘 Connection Map:**
```
B-041 (Web Scraping) ↕ Clone Engine Identity ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python and the Web: Scraping Basics connects to Clone Engine Identity: lippytmai teaches Python and the Web: Scraping Basics in Teach mode. The Clone Engine maintains cons..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Clone Engine Identity in ACSS diagram
- 10–35s: Zoom to where B-041 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-041

**🤖 Copilot Prompt:** > *"As lippytmai, explain Web Scraping to a complete beginner using the B-041 voice."*

---
### Explainer 5: CLL/CCSLL/CBSLL
*Complete Language Libraries*

**📘 Ebook Explanation:** `PEL-L0-B041-WebScraper` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks all Python credentials B-026–B-100+.

**📘 Connection Map:**
```
B-041 (Web Scraping) ↕ CLL/CCSLL/CBSLL ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python and the Web: Scraping Basics connects to CLL/CCSLL/CBSLL: `PEL-L0-B041-WebScraper` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks ..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show CLL/CCSLL/CBSLL in ACSS diagram
- 10–35s: Zoom to where B-041 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-041

**🤖 Copilot Prompt:** > *"Show where PEL-L0-B041-WebScraper fits in the PEL credential hierarchy."*

---
### Explainer 6: ADA Activation
*deployment system*

**📘 Ebook Explanation:** `lippytmai-launch run B-041` activates Python and the Web: Scraping Basics through the ADA FastAPI backend.

**📘 Connection Map:**
```
B-041 (Web Scraping) ↕ ADA Activation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python and the Web: Scraping Basics connects to ADA Activation: `lippytmai-launch run B-041` activates Python and the Web: Scraping Basics through the ADA FastAPI b..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ADA Activation in ACSS diagram
- 10–35s: Zoom to where B-041 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-041

**🤖 Copilot Prompt:** > *"Write the ADA activation manifest for B-041."*

---
### Explainer 7: ACVS Video Pipeline
*video creator*

**📘 Ebook Explanation:** Every Python and the Web: Scraping Basics video uses ACVS SHOW→BUILD→VERIFY structure.

**📘 Connection Map:**
```
B-041 (Web Scraping) ↕ ACVS Video Pipeline ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python and the Web: Scraping Basics connects to ACVS Video Pipeline: Every Python and the Web: Scraping Basics video uses ACVS SHOW→BUILD→VERIFY structure...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACVS Video Pipeline in ACSS diagram
- 10–35s: Zoom to where B-041 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-041

**🤖 Copilot Prompt:** > *"Generate the ACVS scene manifest for B-041 Lesson 1."*

---
### Explainer 8: OMARCHY Workstation
*Arch Linux standard*

**📘 Ebook Explanation:** All Python and the Web: Scraping Basics exercises run on OMARCHY — the reference environment ensures every learner has the same Python setup.

**📘 Connection Map:**
```
B-041 (Web Scraping) ↕ OMARCHY Workstation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python and the Web: Scraping Basics connects to OMARCHY Workstation: All Python and the Web: Scraping Basics exercises run on OMARCHY — the reference environment ensures..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show OMARCHY Workstation in ACSS diagram
- 10–35s: Zoom to where B-041 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-041

**🤖 Copilot Prompt:** > *"What OMARCHY packages are required to complete all B-041 exercises?"*

---
### Explainer 9: Cross-Platform Copilot
*15-platform deployment*

**📘 Ebook Explanation:** The Python and the Web: Scraping Basics AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 10 more platforms.

**📘 Connection Map:**
```
B-041 (Web Scraping) ↕ Cross-Platform Copilot ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python and the Web: Scraping Basics connects to Cross-Platform Copilot: The Python and the Web: Scraping Basics AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Cross-Platform Copilot in ACSS diagram
- 10–35s: Zoom to where B-041 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-041

**🤖 Copilot Prompt:** > *"Adapt the B-041 copilot system prompt for LinkedIn."*

---
### Explainer 10: Earn-While-You-Learn
*revenue system*

**📘 Ebook Explanation:** `PEL-L0-B041-WebScraper` is proof of Web Scraping mastery. Use it on LinkedIn, GitHub, and in lippytm.ai to unlock paid opportunities.

**📘 Connection Map:**
```
B-041 (Web Scraping) ↕ Earn-While-You-Learn ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. Python and the Web: Scraping Basics connects to Earn-While-You-Learn: `PEL-L0-B041-WebScraper` is proof of Web Scraping mastery. Use it on LinkedIn, GitHub, and in lippyt..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Earn-While-You-Learn in ACSS diagram
- 10–35s: Zoom to where B-041 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-041

**🤖 Copilot Prompt:** > *"I just earned PEL-L0-B041-WebScraper. Generate my LinkedIn credential announcement."*

---

### Your ACSS Node Is Now Active

Completing B-041 activates your node in the Fabric graph.
**Next:** `lippytmai-launch run B-041` or start B-042 REST API Builder.

---

## Appendix A: Enhanced Cheat Sheet — Python and the Web: Scraping Basics

### 📘 Print-Optimized Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║  B-041: Python and the Web: Scraping Basics            ║
║  Credential: PEL-L0-B041-WebScraper                             ║
╠══════════════════════════════════════════════════════════════╣
║  Core: BeautifulSoup                                            ║
║  Tool: BeautifulSoup + httpx                                    ║
╠══════════════════════════════════════════════════════════════╣
║  Activate: lippytmai-launch run B-041                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Quick Reference

| Concept | Pattern | Use Case |
|---|---|---|
| `BeautifulSoup` | [usage pattern] | [when to use] |
| `requests-html` | [usage pattern] | [when to use] |
| `httpx` | [usage pattern] | [when to use] |
| `HTML parsing` | [usage pattern] | [when to use] |

### 🎧 Verbal Cheat Sheet: *"Core concepts: BeautifulSoup, requests-html, httpx. Credential: PEL-L0-B041-WebScraper."*

### 🎬 Thumbnail: Dark background, `B-041` bold white, `BeautifulSoup` in green, credential badge bottom-right.

---

## Appendix B: ACSS Connection Map

Node `B-041` in the ACSS knowledge graph:

```
[Hermes] → [B-041 Events] → [Fabric] → [ADA] → [ACVS] → [OMARCHY] → [PEL:PEL-L0-B041-WebScraper] → [EWYL]
```

**Book chain:** B-040 Automation Pro ← **Python and the Web: Scraping Basics** → B-042 REST API Builder

---

## Appendix C: AI Copilot System — Python and the Web: Scraping Basics

### System Prompt
```
You are lippytmai teaching "Python and the Web: Scraping Basics" (B-041).
Help learners master Web Scraping using BeautifulSoup.
Credential: PEL-L0-B041-WebScraper. Philosophy: Earn-while-you-Learn.
Always give 3-step exercises: setup → execute → verify.
```

### 30 Ebook Prompts (5 stages × 6)

**Stage 1 — Foundation:** 1."Explain Web Scraping to a beginner." 2."Most important concept in B-041?" 3."Give a 3-step setup for BeautifulSoup." 4."5 common beginner mistakes with Web Scraping?" 5."Anatomy of a BeautifulSoup pattern." 6."Mental model for Web Scraping."

**Stage 2 — Practice:** 7."5 progressive Web Scraping exercises." 8."Diagnose this error: [paste]." 9."Walk through this code line by line." 10."What to practice today?" 11."20-minute session for Web Scraping." 12."Beginner vs. professional Web Scraping comparison."

**Stage 3 — Application:** 13."Build a real Web Scraping script." 14."How does Web Scraping connect to production systems?" 15."Professional Web Scraping workflow." 16."What does Web Scraping mastery look like on a resume?" 17."Project using only B-041 skills." 18."3 Web Scraping patterns in large-scale systems."

**Stage 4 — Integration:** 19."How does B-041 connect to other books?" 20."How does Web Scraping feed ACSS?" 21."Hermes events for Web Scraping?" 22."How does Fabric store Web Scraping?" 23."ADA activation for B-041." 24."Cross-phase connections from B-041."

**Stage 5 — Mastery:** 25."Assess my Web Scraping level." 26."Stretch goals for PEL-L0-B041-WebScraper holders?" 27."Generate my credential claim for PEL-L0-B041-WebScraper." 28."LinkedIn post for PEL-L0-B041-WebScraper." 29."Portfolio project for PEL-L0-B041-WebScraper." 30."90-day plan building on PEL-L0-B041-WebScraper."

### 15 Audiobook Prompts

1."Narrate Web Scraping intro for a podcast." 2."Story explaining why Web Scraping matters." 3."Audio walkthrough of key B-041 code." 4."Day in the life of a Web Scraping master." 5."2-minute audio lesson on BeautifulSoup." 6."Web Scraping explained with analogies only." 7."Top 5 mistakes with Web Scraping." 8."Audio quiz: 5 questions." 9."Motivational close for B-041." 10."Credential claim narration." 11."Story: developer mastered Web Scraping." 12."Audio summary for commuting." 13."3 real-world Web Scraping scenarios." 14."Capstone walkthrough narration." 15."lippytmai intro monologue for B-041."

### 15 Video Prompts

1."Script 90-second B-041 intro." 2."SHOW→BUILD→VERIFY for BeautifulSoup." 3."Split-screen before/after Web Scraping." 4."Capstone content_scraper.py terminal walkthrough." 5."YouTube thumbnail description." 6."3-minute tutorial on key concept." 7."Progress bar overlay design." 8."ACVS scene manifest for Lesson 1." 9."60-second quick tip for Web Scraping." 10."Error-and-fix scene." 11."Code annotation style." 12."Credential reveal scene." 13."ACSS connection diagram for Ch14." 14."Cross-platform Web Scraping comparison." 15."End-screen CTA design."

### Deployment

```bash
lippytmai-launch run B-041
curl http://localhost:8000/run/B-041
```

Deploy to 15 platforms via `docs/acss-cross-platform-copilot-deployment.md`.

---

## Appendix D: Quick Quiz & Self-Assessment — Python and the Web: Scraping Basics

### 📘 Ebook Quiz (20 Questions)

**Section 1 — Concepts (Q1–5):**
1. What is Web Scraping and why does it matter? *(b — practical mastery of BeautifulSoup)*
2. Primary tool for Web Scraping? *(a — BeautifulSoup)*
3. Which ACSS system routes Web Scraping events? *(c — Hermes)*
4. Your credential for B-041? *(b — PEL-L0-B041-WebScraper)*
5. What does `lippytmai-launch run B-041` do? *(d — activates via ADA)*

**Section 2 — Syntax (Q6–10):**
6. Write a minimal BeautifulSoup example: ___
7. How do you handle errors in Web Scraping? ___
8. One-liner combining BeautifulSoup with another tool: ___
9. How do you test Web Scraping code? ___
10. How do you deploy Web Scraping to production? ___

**Section 3 — Application (Q11–15):**
11. Describe a real-world Web Scraping scenario that saves an hour.
12. Most common mistake with BeautifulSoup?
13. How does Web Scraping connect to security?
14. How does B-041 apply to a production Python project?
15. What would you build first after earning PEL-L0-B041-WebScraper?

**Section 4 — ACSS (Q16–20):**
16. ADA command for B-041? *(lippytmai-launch run B-041)*
17. Fabric node type for Web Scraping? *(ConceptNode)*
18. How does Clone Engine use Web Scraping? *(lippytmai teaches in Teach mode)*
19. 2 books that build on B-041?
20. EWYL opportunity unlocked by PEL-L0-B041-WebScraper?

### 🎧 Audiobook Quiz (10 Questions)

1. Three most important concepts from Python and the Web: Scraping Basics?
2. Explain Web Scraping in one sentence to a non-developer.
3. First thing to do when BeautifulSoup fails?
4. Recite your credential.
5. One project buildable with B-041 skills only.
6. ACSS system that stores skill progress? *(Fabric)*
7. ADA activation command? *(lippytmai-launch run B-041)*
8. Next book after B-041? *(B-042 REST API Builder)*
9. Say the EWYL pledge: "I learn, I build, I earn, I share."
10. What makes Python + ACSS a power combination?

### 🎬 Terminal Challenges (5)

1. **Foundation:** Run `BeautifulSoup` — screenshot the output.
2. **Intermediate:** Combine `BeautifulSoup` with error handling.
3. **Applied:** Write a 10-line script automating a real task.
4. **Debug:** Introduce an error, diagnose and fix it.
5. **Capstone:** Run `content_scraper.py` — record a 60-second demo.

---

## Appendix E: Glossary & Error Encyclopedia — Python and the Web: Scraping Basics

### Glossary (20 Terms)

| Term | Definition | First Seen |
|---|---|---|
| `BeautifulSoup` | [definition in B-041 context] | [B-041] |
| `requests-html` | [definition in B-041 context] | [B-041] |
| `httpx` | [definition in B-041 context] | [B-041] |
| `HTML parsing` | [definition in B-041 context] | [B-041] |
| `CSS selectors` | [definition in B-041 context] | [B-041] |
| `async` | [definition in B-041 context] | [B-041] |
| `decorator` | [definition in B-041 context] | [B-041] |
| `type hint` | [definition in B-041 context] | [B-041] |
| `dataclass` | [definition in B-041 context] | [B-041] |
| `fixture` | [definition in B-041 context] | [B-041] |
| `Hermes` | [definition in B-041 context] | [B-041] |
| `Fabric` | [definition in B-041 context] | [B-041] |
| `ADA` | [definition in B-041 context] | [B-041] |
| `OMARCHY` | [definition in B-041 context] | [B-041] |
| `credential` | [definition in B-041 context] | [B-041] |
| `EWYL` | [definition in B-041 context] | [B-041] |
| `lippytmai` | [definition in B-041 context] | [B-041] |
| `PEL` | [definition in B-041 context] | [B-041] |
| `Fabric node` | [definition in B-041 context] | [B-041] |
| `clone identity` | [definition in B-041 context] | [B-041] |

### Error Encyclopedia (10 Common Python Errors)


#### `TypeError` — Cause: Wrong type passed to function. Fix: Add type hints; check with `isinstance()`.
- **🎧 Audio:** "When you see `TypeError`, it means wrong type passed to function"
- **🎬 Video:** Error + fix terminal recording


#### `AttributeError` — Cause: Accessing attribute that doesn't exist. Fix: Use `hasattr()` or check with `dir()`.
- **🎧 Audio:** "When you see `AttributeError`, it means accessing attribute that doesn't exist"
- **🎬 Video:** Error + fix terminal recording


#### `ImportError` — Cause: Module not found. Fix: Check venv is active; run `pip install`.
- **🎧 Audio:** "When you see `ImportError`, it means module not found"
- **🎬 Video:** Error + fix terminal recording


#### `KeyError` — Cause: Dict key doesn't exist. Fix: Use `.get()` with a default value.
- **🎧 Audio:** "When you see `KeyError`, it means dict key doesn't exist"
- **🎬 Video:** Error + fix terminal recording


#### `FileNotFoundError` — Cause: Path doesn't exist. Fix: Use `Path.exists()` before opening.
- **🎧 Audio:** "When you see `FileNotFoundError`, it means path doesn't exist"
- **🎬 Video:** Error + fix terminal recording


#### `ValueError` — Cause: Invalid value for operation. Fix: Validate inputs before processing.
- **🎧 Audio:** "When you see `ValueError`, it means invalid value for operation"
- **🎬 Video:** Error + fix terminal recording


#### `IndentationError` — Cause: Mixed tabs and spaces. Fix: Configure editor to use spaces only.
- **🎧 Audio:** "When you see `IndentationError`, it means mixed tabs and spaces"
- **🎬 Video:** Error + fix terminal recording


#### `RecursionError` — Cause: Infinite recursion. Fix: Add base case; increase recursion limit if needed.
- **🎧 Audio:** "When you see `RecursionError`, it means infinite recursion"
- **🎬 Video:** Error + fix terminal recording


#### `ConnectionError` — Cause: Network request failed. Fix: Wrap in try/except; implement retry logic.
- **🎧 Audio:** "When you see `ConnectionError`, it means network request failed"
- **🎬 Video:** Error + fix terminal recording


#### `PermissionError` — Cause: File or directory not accessible. Fix: Check permissions with `ls -la`.
- **🎧 Audio:** "When you see `PermissionError`, it means file or directory not accessible"
- **🎬 Video:** Error + fix terminal recording


---

## Appendix F: Instructor & Accessibility Guide — Python and the Web: Scraping Basics

### Teaching Schedule (4-Week Curriculum)

| Week | Focus | Topics | Outcome |
|---|---|---|---|
| 1 | Foundation | Concepts + setup | Can use Web Scraping tools |
| 2 | Intermediate | Core patterns | Can write working code |
| 3 | Applied | Real projects | Can solve production problems |
| 4 | Mastery | DFY + Appendices | Earns `PEL-L0-B041-WebScraper` |

### Common Confusion Points

1. "When do I use BeautifulSoup vs. alternatives?" — Show a decision flowchart.
2. "Why does the same code fail in a different environment?" — Explain venv isolation.
3. "How do I know if my code is production-ready?" — Show the VERIFY step always.
4. "How does Web Scraping connect to other Python skills?" — Show the ACSS learning path map.
5. "What does earning PEL-L0-B041-WebScraper actually mean for my career?" — Show EWYL income examples.

### Assessment Rubric

| Criterion | Beginner | Competent | Expert |
|---|---|---|---|
| Code quality | Messy, no types | Working, some types | Clean, typed, tested |
| Error handling | None | Basic try/except | Custom exceptions + logging |
| Testing | No tests | Basic assertions | pytest + fixtures + coverage |
| ACSS integration | Unaware | Uses ADA | Contributes to ACSS |

### Accessibility: Screen reader alt-text for all diagrams. No color-only encoding. Short paragraphs. Audiobook available.

---

## Appendix G: Your Learning Path — Python and the Web: Scraping Basics

### Where You Are Now

```
  Phase 2: Python Programming (B-026–B-055)
  [██████████░░░░░░░░░░] 53%

  ✅ B-040 Automation Pro (PEL-L0-B040-AutomationPro)
  👉 B-041: Python and the Web: Scraping Basics ← YOU ARE HERE
  ⬜ B-042 REST API Builder (PEL-L0-B042-APIBuilder)
```

### Credential Chain

```
PEL-L0-B040-AutomationPro → PEL-L0-B041-WebScraper → PEL-L0-B042-APIBuilder
```

### Next Steps

1. Claim `PEL-L0-B041-WebScraper` (Appendix C, Prompt 27)
2. Build `content_scraper.py` (Appendix H)
3. Start `B-042 REST API Builder`

### Cross-Phase Connections

```
Phase 1: Linux Foundations → Phase 2: Python (YOU ARE HERE)
    ↓ B-041 connects to:
Phase 3: Blockchain Development (B-056+)
```

---

## Appendix H: Real Project Showcase — Python and the Web: Scraping Basics

### Project: `content_scraper.py`

**Credential gated:** Complete this project to qualify for `PEL-L0-B041-WebScraper`

### Complete Code

```python
#!/usr/bin/env python3
import httpx
from bs4 import BeautifulSoup
from typing import list as List

def scrape_links(url: str) -> List[str]:
    with httpx.Client(timeout=10.0) as client:
        resp = client.get(url)
        resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return [a["href"] for a in soup.find_all("a", href=True)]

def scrape_headings(url: str) -> List[str]:
    with httpx.Client(timeout=10.0) as client:
        resp = client.get(url)
        resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    return [h.get_text() for h in soup.find_all(["h1","h2","h3"])]

```

### Deploy Instructions

```bash
# Run the project
python content_scraper.py --help
python content_scraper.py

# Test it
pytest test_content_scraper.py -v  # if tests exist

# Verify
echo "Exit: $?"
```

### Extend It

1. Add type hints to all functions
2. Add pytest test coverage
3. Add CLI interface with typer
4. Containerize with Docker
5. Add structured logging

### 🎧 Walkthrough: *"Build content_scraper.py step by step. When it runs successfully, you've earned PEL-L0-B041-WebScraper."*

### 🎬 Video: SHOW empty editor → BUILD code live → VERIFY execution → CTA: "Claim PEL-L0-B041-WebScraper."

---

## Further Reading

- 📄 [Back to README](../README.md)
- 📄 [Product Excellence Framework](PRODUCT-EXCELLENCE-FRAMEWORK.md)
- 📄 [AI Clone Engine Swarms](ai-clone-engine-swarms.md)
- 📄 [ACSS Cross-Platform Copilot Deployment](acss-cross-platform-copilot-deployment.md)
- 📄 [ADA Deployment Activations](ai-deployment-activations.md)
- 📄 [Previous: B-040](B-040-*.md)
- 📄 [Next: B-042](B-042-*.md)

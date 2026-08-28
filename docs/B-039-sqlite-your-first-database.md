# B-039: SQLite — Your First Database

### sqlite3, CREATE TABLE, INSERT, SELECT, and Persistent Data

> *"Every application eventually needs to remember things between runs. Files work for simple data — but when you need to query, sort, filter, and relate data, you need a database. SQLite gives you a full SQL engine in a single file. No server, no credentials, no setup. Just import and go."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Create and connect to a SQLite database from Python
2. Create tables with `CREATE TABLE` and insert rows with `INSERT`
3. Query data with `SELECT`, `WHERE`, `ORDER BY`, and `LIMIT`
4. Update and delete rows safely using parameterized queries
5. Build a `task_tracker.py` — a persistent personal task manager

**Prerequisite:** B-036 (type hints recommended), B-037 (for timestamp patterns)

**Build Artifact:** `~/developer-workspace/projects/python-foundations/task_tracker.py`

**Credential:** `CCSLL-L1-B039-DataEngineer` — on-chain on Base

---

## Chapter 1: SQLite Basics

```python
import sqlite3

# Connect to a database file (creates it if it doesn't exist)
conn = sqlite3.connect("mydata.db")

# Connect to an in-memory database (lost when connection closes)
conn_mem = sqlite3.connect(":memory:")

# cursor — used to execute SQL
cursor = conn.cursor()

# Always close your connection when done
conn.close()

# Better: use as a context manager (auto-commits or rolls back)
with sqlite3.connect("mydata.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT sqlite_version()")
    print(cursor.fetchone())   # ('3.x.y',)
```

---

## Chapter 2: CREATE TABLE and INSERT

```python
import sqlite3

with sqlite3.connect("tasks.db") as conn:
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT    NOT NULL,
            priority  TEXT    DEFAULT 'medium',
            done      INTEGER DEFAULT 0,
            created   TEXT    NOT NULL
        )
    """)
    conn.commit()

    # Insert a single row — ALWAYS use parameterized queries (prevents SQL injection)
    cursor.execute(
        "INSERT INTO tasks (title, priority, done, created) VALUES (?, ?, ?, ?)",
        ("Learn SQLite", "high", 0, "2026-08-28")
    )
    conn.commit()
    print(f"Inserted row id: {cursor.lastrowid}")

    # Insert multiple rows at once
    rows = [
        ("Build date calculator", "medium", 0, "2026-08-28"),
        ("Write QEP-B036-B040",  "high",   0, "2026-08-28"),
        ("Deploy via ADA",       "low",    0, "2026-08-29"),
    ]
    cursor.executemany(
        "INSERT INTO tasks (title, priority, done, created) VALUES (?, ?, ?, ?)",
        rows
    )
    conn.commit()
```

---

## Chapter 3: SELECT Queries

```python
import sqlite3

with sqlite3.connect("tasks.db") as conn:
    # Use Row factory for dict-like access
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Select all rows
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    for row in rows:
        print(dict(row))

    # Select with WHERE
    cursor.execute("SELECT * FROM tasks WHERE priority = ?", ("high",))
    high_priority = cursor.fetchall()

    # Select with ORDER BY and LIMIT
    cursor.execute("SELECT * FROM tasks ORDER BY created DESC LIMIT 3")
    recent = cursor.fetchall()

    # fetchone — get a single row
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (1,))
    task = cursor.fetchone()
    if task:
        print(f"Task 1: {task['title']}")

    # Count rows
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 0")
    pending = cursor.fetchone()[0]
    print(f"Pending tasks: {pending}")

    # Aggregate queries
    cursor.execute("SELECT priority, COUNT(*) as cnt FROM tasks GROUP BY priority")
    for row in cursor.fetchall():
        print(f"{row['priority']}: {row['cnt']} tasks")
```

---

## Chapter 4: UPDATE and DELETE

```python
import sqlite3

with sqlite3.connect("tasks.db") as conn:
    cursor = conn.cursor()

    # Update a row — ALWAYS use WHERE or you'll update EVERYTHING
    cursor.execute(
        "UPDATE tasks SET done = 1 WHERE id = ?",
        (1,)
    )
    print(f"Rows updated: {cursor.rowcount}")
    conn.commit()

    # Update multiple columns
    cursor.execute(
        "UPDATE tasks SET done = 1, priority = ? WHERE title LIKE ?",
        ("low", "%SQLite%")
    )
    conn.commit()

    # Delete a row
    cursor.execute("DELETE FROM tasks WHERE id = ?", (99,))
    conn.commit()
    print(f"Rows deleted: {cursor.rowcount}")

    # Delete all completed tasks
    cursor.execute("DELETE FROM tasks WHERE done = 1")
    conn.commit()
```

---

## Chapter 5: Schema Design Patterns

```python
import sqlite3

# One-to-many: projects → tasks
SCHEMA = """
CREATE TABLE IF NOT EXISTS projects (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL UNIQUE,
    created TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    title      TEXT NOT NULL,
    priority   TEXT DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high')),
    done       INTEGER DEFAULT 0 CHECK(done IN (0, 1)),
    due_date   TEXT,
    created    TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_tasks_project ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_tasks_done    ON tasks(done);
"""

with sqlite3.connect("projects.db") as conn:
    conn.executescript(SCHEMA)
    conn.execute("PRAGMA foreign_keys = ON")   # SQLite requires explicit FK enforcement
    conn.commit()
    print("Schema created")
```

---

## Chapter 6: The Build — Task Tracker

```python
#!/usr/bin/env python3
"""
task_tracker.py — B-039 Build Artifact

A persistent personal task manager using SQLite.
Usage: python3 task_tracker.py
"""
from __future__ import annotations

import sqlite3
from datetime import date
from pathlib import Path
from typing import Optional

DB_PATH = Path.home() / "developer-workspace" / "projects" / "python-foundations" / "tasks.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS tasks (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            title     TEXT    NOT NULL,
            priority  TEXT    DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high')),
            done      INTEGER DEFAULT 0,
            due_date  TEXT,
            created   TEXT    NOT NULL DEFAULT (date('now'))
        );
    """)
    conn.commit()


def add_task(
    conn: sqlite3.Connection,
    title: str,
    priority: str = "medium",
    due_date: Optional[str] = None,
) -> int:
    cursor = conn.execute(
        "INSERT INTO tasks (title, priority, due_date) VALUES (?, ?, ?)",
        (title, priority, due_date),
    )
    conn.commit()
    return cursor.lastrowid or 0


def complete_task(conn: sqlite3.Connection, task_id: int) -> bool:
    conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    conn.commit()
    return conn.execute("SELECT changes()").fetchone()[0] > 0


def delete_task(conn: sqlite3.Connection, task_id: int) -> bool:
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return conn.execute("SELECT changes()").fetchone()[0] > 0


def list_tasks(
    conn: sqlite3.Connection,
    done: Optional[bool] = None,
    priority: Optional[str] = None,
) -> list[sqlite3.Row]:
    query = "SELECT * FROM tasks WHERE 1=1"
    params: list[object] = []
    if done is not None:
        query += " AND done = ?"
        params.append(1 if done else 0)
    if priority is not None:
        query += " AND priority = ?"
        params.append(priority)
    query += " ORDER BY CASE priority WHEN 'high' THEN 1 WHEN 'medium' THEN 2 ELSE 3 END, created"
    return conn.execute(query, params).fetchall()


def print_tasks(tasks: list[sqlite3.Row]) -> None:
    if not tasks:
        print("  (no tasks)\n")
        return
    print(f"\n  {'ID':<4} {'✓':<3} {'Priority':<8} {'Due':<12} {'Title'}")
    print("  " + "-" * 55)
    for t in tasks:
        done_icon = "✅" if t["done"] else "  "
        due = t["due_date"] or "—"
        pri = t["priority"].upper()[0]   # H/M/L
        print(f"  {t['id']:<4} {done_icon:<3} [{pri}]{' '*4} {due:<12} {t['title']}")
    print()


def stats(conn: sqlite3.Connection) -> None:
    total   = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
    pending = conn.execute("SELECT COUNT(*) FROM tasks WHERE done = 0").fetchone()[0]
    done    = total - pending
    high    = conn.execute("SELECT COUNT(*) FROM tasks WHERE priority = 'high' AND done = 0").fetchone()[0]
    print(f"  Total: {total}  |  Pending: {pending}  |  Done: {done}  |  High priority: {high}\n")


def demo() -> None:
    conn = get_connection()
    init_db(conn)

    print("=== Task Tracker Demo ===\n")

    # Add tasks
    add_task(conn, "Learn SQLite", "high", "2026-09-01")
    add_task(conn, "Build B-039 project", "high", "2026-09-05")
    add_task(conn, "Review QEP-B036-B040", "medium", "2026-09-10")
    add_task(conn, "Update ADA registry", "low")
    add_task(conn, "Read the SQLite docs", "low")

    print("--- All tasks ---")
    print_tasks(list_tasks(conn))

    print("--- High priority only ---")
    print_tasks(list_tasks(conn, done=False, priority="high"))

    # Complete one
    complete_task(conn, 1)

    print("--- After completing task 1 ---")
    stats(conn)
    print_tasks(list_tasks(conn))

    conn.close()
    print(f"Database saved to: {DB_PATH}")


if __name__ == "__main__":
    demo()
```

```bash
python3 ~/developer-workspace/projects/python-foundations/task_tracker.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-039 Verification ==="
python3 -c "
import sqlite3

conn = sqlite3.connect(':memory:')
conn.row_factory = sqlite3.Row
conn.execute('CREATE TABLE notes (id INTEGER PRIMARY KEY, text TEXT)')
conn.execute('INSERT INTO notes (text) VALUES (?)', ('Hello, SQLite!',))
conn.commit()
row = conn.execute('SELECT * FROM notes').fetchone()
print(f'Row: id={row[\"id\"]}, text={row[\"text\"]}')
print('✅ SQLite works')
conn.close()
"
```

---


## Chapter 12: Done-For-You Lessons — SQLite: Your First Database

> *"Done-for-you means it's already designed, structured, and proven. Your job: execute." — lippytmai*

10 ready-to-use lesson structures for SQLite & SQL using sqlite3.

---

### DFY Lesson 1: Introduction to SQLite & SQL

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 01: Introduction to SQLite & SQL              │
│  Book: B-039  Tool: sqlite3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 1: Introduction to SQLite & SQL. Master sqlite3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `sqlite3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 1 of B-039: Introduction to SQLite & SQL. Give me 3 progressive exercises."

---
### DFY Lesson 2: Core sqlite3 Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 02: Core sqlite3 Patterns                     │
│  Book: B-039  Tool: sqlite3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 2: Core sqlite3 Patterns. Master sqlite3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `sqlite3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 2 of B-039: Core sqlite3 Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 3: Three Formats: Ebook, Audiobook, Video

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 03: Three Formats: Ebook, Audiobook, Video    │
│  Book: B-039  Tool: sqlite3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 3: Three Formats: Ebook, Audiobook, Video. Master sqlite3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `sqlite3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 3 of B-039: Three Formats: Ebook, Audiobook, Video. Give me 3 progressive exercises."

---
### DFY Lesson 4: Common Mistakes in SQLite & SQL

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 04: Common Mistakes in SQLite & SQL           │
│  Book: B-039  Tool: sqlite3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 4: Common Mistakes in SQLite & SQL. Master sqlite3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `sqlite3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 4 of B-039: Common Mistakes in SQLite & SQL. Give me 3 progressive exercises."

---
### DFY Lesson 5: Building a SQLite & SQL Workflow

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 05: Building a SQLite & SQL Workflow          │
│  Book: B-039  Tool: sqlite3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 5: Building a SQLite & SQL Workflow. Master sqlite3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `sqlite3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 5 of B-039: Building a SQLite & SQL Workflow. Give me 3 progressive exercises."

---
### DFY Lesson 6: Automating with sqlite3

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 06: Automating with sqlite3                   │
│  Book: B-039  Tool: sqlite3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 6: Automating with sqlite3. Master sqlite3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `sqlite3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 6 of B-039: Automating with sqlite3. Give me 3 progressive exercises."

---
### DFY Lesson 7: Testing Your SQLite & SQL Code

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 07: Testing Your SQLite & SQL Code            │
│  Book: B-039  Tool: sqlite3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 7: Testing Your SQLite & SQL Code. Master sqlite3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `sqlite3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 7 of B-039: Testing Your SQLite & SQL Code. Give me 3 progressive exercises."

---
### DFY Lesson 8: Production SQLite & SQL Patterns

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 08: Production SQLite & SQL Patterns          │
│  Book: B-039  Tool: sqlite3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 8: Production SQLite & SQL Patterns. Master sqlite3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `sqlite3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 8 of B-039: Production SQLite & SQL Patterns. Give me 3 progressive exercises."

---
### DFY Lesson 9: Debugging SQLite & SQL Problems

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 09: Debugging SQLite & SQL Problems           │
│  Book: B-039  Tool: sqlite3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 9: Debugging SQLite & SQL Problems. Master sqlite3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `sqlite3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 9 of B-039: Debugging SQLite & SQL Problems. Give me 3 progressive exercises."

---
### DFY Lesson 10: Earning Your PEL-L0-B039-SQLiteBuilder Credential

**📘 Ebook Figure:**

```
┌─────────────────────────────────────────────────────────┐
│  DFY LESSON 10: Earning Your PEL-L0-B039-SQLiteBuilder C  │
│  Book: B-039  Tool: sqlite3                    │
└─────────────────────────────────────────────────────────┘
```

**🎧 Audiobook Callout (lippytmai voice, ~90 seconds):**

> *"Lesson 10: Earning Your PEL-L0-B039-SQLiteBuilder Credential. Master sqlite3 with practice. The key insight: every Python professional has a repeatable system. Yours starts here."*

**🎬 Video Scene:**

- **SHOW:** Terminal + editor with `sqlite3` open
- **BUILD:** Walk through step by step with live coding
- **VERIFY:** Run tests or execute the result

**🤖 Copilot Prompt:**

> "Help me practice DFY Lesson 10 of B-039: Earning Your PEL-L0-B039-SQLiteBuilder Credential. Give me 3 progressive exercises."

---

### Claim Your Credential

Complete all 10 lessons → open Appendix C → run: *"Generate my credential claim for `PEL-L0-B039-SQLiteBuilder`."*

---

## Chapter 13: How It Works — Use Cases & Applications

> *"Knowing what to do is different from knowing why it matters." — lippytmai*

### The Mechanism

SQLite & SQL in Python works because the language was designed to be readable, composable, and deployable. sqlite3 is the tool that makes SQLite & SQL practical.

### 5 Real-World Use Cases

| Domain | Application | Your Credential Unlocks |
|---|---|---|
| Backend Dev | Build APIs and services with sqlite3 | PEL-L0-B039-SQLiteBuilder → production deployments |
| Data Engineering | Process and transform data pipelines | PEL-L0-B039-SQLiteBuilder → ETL roles |
| DevOps/Automation | Automate repetitive tasks | PEL-L0-B039-SQLiteBuilder → CI/CD integration |
| AI/ML | Preprocess data and build models | PEL-L0-B039-SQLiteBuilder → AI projects |
| Freelance | Deliver Python solutions to clients | PEL-L0-B039-SQLiteBuilder → paid work |

### 📘 Mechanism Diagram

```
INPUT → [SQLite & SQL Layer] → OUTPUT
         ↓
[ACSS Integration] → Hermes Event → Fabric Node
         ↓
[ADA Activation] → lippytmai-launch run B-039
```

### 🎧 Audiobook Narration:

> *"When you master SQLite & SQL, you're not just learning syntax — you're learning how production Python systems work. Every ACSS component uses these patterns. This is infrastructure knowledge."*

### 🎬 Video: 5-Domain Application Tour

**Scene 1 — Backend:** API or service using SQLite & SQL
**Scene 2 — Data:** Data pipeline using SQLite & SQL
**Scene 3 — DevOps:** Automation script using SQLite & SQL
**Scene 4 — AI/ML:** Model integration using SQLite & SQL
**Scene 5 — Freelance:** Client deliverable using SQLite & SQL

---

## Chapter 14: ACSS Explainer Series — SQLite: Your First Database

> *"You're not just learning SQLite & SQL. You're building a node in an intelligence network." — lippytmai*

10 explainer lessons connecting SQLite: Your First Database to the full ACSS architecture.

---

### Explainer 1: ACSS Overview
*intelligence network*

**📘 Ebook Explanation:** SQLite: Your First Database teaches the SQLite & SQL layer that feeds the ACSS. Sqlite powers the ada credential registry locally — every claimed credential and book activation is stored in a sqlite database.

**📘 Connection Map:**
```
B-039 (SQLite & SQL) ↕ ACSS Overview ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. SQLite: Your First Database connects to ACSS Overview: SQLite: Your First Database teaches the SQLite & SQL layer that feeds the ACSS. Sqlite powers the ad..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACSS Overview in ACSS diagram
- 10–35s: Zoom to where B-039 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-039

**🤖 Copilot Prompt:** > *"Explain how SQLite & SQL fits the ACSS. What role does B-039 play?"*

---
### Explainer 2: Hermes Event Routing
*cross-system message bus*

**📘 Ebook Explanation:** Hermes routes SQLite & SQL practice events. Completing an exercise emits a `skill.practice` event.

**📘 Connection Map:**
```
B-039 (SQLite & SQL) ↕ Hermes Event Routing ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. SQLite: Your First Database connects to Hermes Event Routing: Hermes routes SQLite & SQL practice events. Completing an exercise emits a `skill.practice` event...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Hermes Event Routing in ACSS diagram
- 10–35s: Zoom to where B-039 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-039

**🤖 Copilot Prompt:** > *"Show the Hermes event schema for a B-039 skill-complete event."*

---
### Explainer 3: Fabric Knowledge Graph
*pattern synthesis*

**📘 Ebook Explanation:** Fabric stores every SQLite & SQL concept as a knowledge node connected to related books.

**📘 Connection Map:**
```
B-039 (SQLite & SQL) ↕ Fabric Knowledge Graph ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. SQLite: Your First Database connects to Fabric Knowledge Graph: Fabric stores every SQLite & SQL concept as a knowledge node connected to related books...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Fabric Knowledge Graph in ACSS diagram
- 10–35s: Zoom to where B-039 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-039

**🤖 Copilot Prompt:** > *"Generate the Fabric node definition for the core concept of B-039."*

---
### Explainer 4: Clone Engine Identity
*AI persona system*

**📘 Ebook Explanation:** lippytmai teaches SQLite: Your First Database in Teach mode. The Clone Engine maintains consistent voice across all 300 books.

**📘 Connection Map:**
```
B-039 (SQLite & SQL) ↕ Clone Engine Identity ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. SQLite: Your First Database connects to Clone Engine Identity: lippytmai teaches SQLite: Your First Database in Teach mode. The Clone Engine maintains consistent v..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Clone Engine Identity in ACSS diagram
- 10–35s: Zoom to where B-039 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-039

**🤖 Copilot Prompt:** > *"As lippytmai, explain SQLite & SQL to a complete beginner using the B-039 voice."*

---
### Explainer 5: CLL/CCSLL/CBSLL
*Complete Language Libraries*

**📘 Ebook Explanation:** `PEL-L0-B039-SQLiteBuilder` is registered in the Python Earn-while-you-Learn library (PEL). PEL tracks all Python credentials B-026–B-100+.

**📘 Connection Map:**
```
B-039 (SQLite & SQL) ↕ CLL/CCSLL/CBSLL ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. SQLite: Your First Database connects to CLL/CCSLL/CBSLL: `PEL-L0-B039-SQLiteBuilder` is registered in the Python Earn-while-you-Learn library (PEL). PEL trac..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show CLL/CCSLL/CBSLL in ACSS diagram
- 10–35s: Zoom to where B-039 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-039

**🤖 Copilot Prompt:** > *"Show where PEL-L0-B039-SQLiteBuilder fits in the PEL credential hierarchy."*

---
### Explainer 6: ADA Activation
*deployment system*

**📘 Ebook Explanation:** `lippytmai-launch run B-039` activates SQLite: Your First Database through the ADA FastAPI backend.

**📘 Connection Map:**
```
B-039 (SQLite & SQL) ↕ ADA Activation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. SQLite: Your First Database connects to ADA Activation: `lippytmai-launch run B-039` activates SQLite: Your First Database through the ADA FastAPI backend...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ADA Activation in ACSS diagram
- 10–35s: Zoom to where B-039 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-039

**🤖 Copilot Prompt:** > *"Write the ADA activation manifest for B-039."*

---
### Explainer 7: ACVS Video Pipeline
*video creator*

**📘 Ebook Explanation:** Every SQLite: Your First Database video uses ACVS SHOW→BUILD→VERIFY structure.

**📘 Connection Map:**
```
B-039 (SQLite & SQL) ↕ ACVS Video Pipeline ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. SQLite: Your First Database connects to ACVS Video Pipeline: Every SQLite: Your First Database video uses ACVS SHOW→BUILD→VERIFY structure...."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show ACVS Video Pipeline in ACSS diagram
- 10–35s: Zoom to where B-039 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-039

**🤖 Copilot Prompt:** > *"Generate the ACVS scene manifest for B-039 Lesson 1."*

---
### Explainer 8: OMARCHY Workstation
*Arch Linux standard*

**📘 Ebook Explanation:** All SQLite: Your First Database exercises run on OMARCHY — the reference environment ensures every learner has the same Python setup.

**📘 Connection Map:**
```
B-039 (SQLite & SQL) ↕ OMARCHY Workstation ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. SQLite: Your First Database connects to OMARCHY Workstation: All SQLite: Your First Database exercises run on OMARCHY — the reference environment ensures every l..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show OMARCHY Workstation in ACSS diagram
- 10–35s: Zoom to where B-039 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-039

**🤖 Copilot Prompt:** > *"What OMARCHY packages are required to complete all B-039 exercises?"*

---
### Explainer 9: Cross-Platform Copilot
*15-platform deployment*

**📘 Ebook Explanation:** The SQLite: Your First Database AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 10 more platforms.

**📘 Connection Map:**
```
B-039 (SQLite & SQL) ↕ Cross-Platform Copilot ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. SQLite: Your First Database connects to Cross-Platform Copilot: The SQLite: Your First Database AI Copilot deploys on ChatGPT, Gemini, Claude, GitHub, Slack, and 10..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Cross-Platform Copilot in ACSS diagram
- 10–35s: Zoom to where B-039 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-039

**🤖 Copilot Prompt:** > *"Adapt the B-039 copilot system prompt for LinkedIn."*

---
### Explainer 10: Earn-While-You-Learn
*revenue system*

**📘 Ebook Explanation:** `PEL-L0-B039-SQLiteBuilder` is proof of SQLite & SQL mastery. Use it on LinkedIn, GitHub, and in lippytm.ai to unlock paid opportunities.

**📘 Connection Map:**
```
B-039 (SQLite & SQL) ↕ Earn-While-You-Learn ↕ ACSS Ecosystem
```

**🎧 30-Second Callout:** > *"lippytmai here. SQLite: Your First Database connects to Earn-While-You-Learn: `PEL-L0-B039-SQLiteBuilder` is proof of SQLite & SQL mastery. Use it on LinkedIn, GitHub, and in lip..."*

**🎬 60-Second Walkthrough:**
- 0–10s: Show Earn-While-You-Learn in ACSS diagram
- 10–35s: Zoom to where B-039 connects
- 35–55s: Live example of the connection
- 55–60s: CTA to complete B-039

**🤖 Copilot Prompt:** > *"I just earned PEL-L0-B039-SQLiteBuilder. Generate my LinkedIn credential announcement."*

---

### Your ACSS Node Is Now Active

Completing B-039 activates your node in the Fabric graph.
**Next:** `lippytmai-launch run B-039` or start B-040 Automation.

---

## Appendix A: Enhanced Cheat Sheet — SQLite: Your First Database

### 📘 Print-Optimized Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║  B-039: SQLite: Your First Database                    ║
║  Credential: PEL-L0-B039-SQLiteBuilder                          ║
╠══════════════════════════════════════════════════════════════╣
║  Core: sqlite3                                                  ║
║  Tool: sqlite3 + SQL                                            ║
╠══════════════════════════════════════════════════════════════╣
║  Activate: lippytmai-launch run B-039                            ║
╚══════════════════════════════════════════════════════════════╝
```

### Quick Reference

| Concept | Pattern | Use Case |
|---|---|---|
| `sqlite3` | [usage pattern] | [when to use] |
| `SQL` | [usage pattern] | [when to use] |
| `CREATE TABLE` | [usage pattern] | [when to use] |
| `INSERT` | [usage pattern] | [when to use] |

### 🎧 Verbal Cheat Sheet: *"Core concepts: sqlite3, SQL, CREATE TABLE. Credential: PEL-L0-B039-SQLiteBuilder."*

### 🎬 Thumbnail: Dark background, `B-039` bold white, `sqlite3` in green, credential badge bottom-right.

---

## Appendix B: ACSS Connection Map

Node `B-039` in the ACSS knowledge graph:

```
[Hermes] → [B-039 Events] → [Fabric] → [ADA] → [ACVS] → [OMARCHY] → [PEL:PEL-L0-B039-SQLiteBuilder] → [EWYL]
```

**Book chain:** B-038 Regex Wizard ← **SQLite: Your First Database** → B-040 Automation

---

## Appendix C: AI Copilot System — SQLite: Your First Database

### System Prompt
```
You are lippytmai teaching "SQLite: Your First Database" (B-039).
Help learners master SQLite & SQL using sqlite3.
Credential: PEL-L0-B039-SQLiteBuilder. Philosophy: Earn-while-you-Learn.
Always give 3-step exercises: setup → execute → verify.
```

### 30 Ebook Prompts (5 stages × 6)

**Stage 1 — Foundation:** 1."Explain SQLite & SQL to a beginner." 2."Most important concept in B-039?" 3."Give a 3-step setup for sqlite3." 4."5 common beginner mistakes with SQLite & SQL?" 5."Anatomy of a sqlite3 pattern." 6."Mental model for SQLite & SQL."

**Stage 2 — Practice:** 7."5 progressive SQLite & SQL exercises." 8."Diagnose this error: [paste]." 9."Walk through this code line by line." 10."What to practice today?" 11."20-minute session for SQLite & SQL." 12."Beginner vs. professional SQLite & SQL comparison."

**Stage 3 — Application:** 13."Build a real SQLite & SQL script." 14."How does SQLite & SQL connect to production systems?" 15."Professional SQLite & SQL workflow." 16."What does SQLite & SQL mastery look like on a resume?" 17."Project using only B-039 skills." 18."3 SQLite & SQL patterns in large-scale systems."

**Stage 4 — Integration:** 19."How does B-039 connect to other books?" 20."How does SQLite & SQL feed ACSS?" 21."Hermes events for SQLite & SQL?" 22."How does Fabric store SQLite & SQL?" 23."ADA activation for B-039." 24."Cross-phase connections from B-039."

**Stage 5 — Mastery:** 25."Assess my SQLite & SQL level." 26."Stretch goals for PEL-L0-B039-SQLiteBuilder holders?" 27."Generate my credential claim for PEL-L0-B039-SQLiteBuilder." 28."LinkedIn post for PEL-L0-B039-SQLiteBuilder." 29."Portfolio project for PEL-L0-B039-SQLiteBuilder." 30."90-day plan building on PEL-L0-B039-SQLiteBuilder."

### 15 Audiobook Prompts

1."Narrate SQLite & SQL intro for a podcast." 2."Story explaining why SQLite & SQL matters." 3."Audio walkthrough of key B-039 code." 4."Day in the life of a SQLite & SQL master." 5."2-minute audio lesson on sqlite3." 6."SQLite & SQL explained with analogies only." 7."Top 5 mistakes with SQLite & SQL." 8."Audio quiz: 5 questions." 9."Motivational close for B-039." 10."Credential claim narration." 11."Story: developer mastered SQLite & SQL." 12."Audio summary for commuting." 13."3 real-world SQLite & SQL scenarios." 14."Capstone walkthrough narration." 15."lippytmai intro monologue for B-039."

### 15 Video Prompts

1."Script 90-second B-039 intro." 2."SHOW→BUILD→VERIFY for sqlite3." 3."Split-screen before/after SQLite & SQL." 4."Capstone credential_db.py terminal walkthrough." 5."YouTube thumbnail description." 6."3-minute tutorial on key concept." 7."Progress bar overlay design." 8."ACVS scene manifest for Lesson 1." 9."60-second quick tip for SQLite & SQL." 10."Error-and-fix scene." 11."Code annotation style." 12."Credential reveal scene." 13."ACSS connection diagram for Ch14." 14."Cross-platform SQLite & SQL comparison." 15."End-screen CTA design."

### Deployment

```bash
lippytmai-launch run B-039
curl http://localhost:8000/run/B-039
```

Deploy to 15 platforms via `docs/acss-cross-platform-copilot-deployment.md`.

---

## Appendix D: Quick Quiz & Self-Assessment — SQLite: Your First Database

### 📘 Ebook Quiz (20 Questions)

**Section 1 — Concepts (Q1–5):**
1. What is SQLite & SQL and why does it matter? *(b — practical mastery of sqlite3)*
2. Primary tool for SQLite & SQL? *(a — sqlite3)*
3. Which ACSS system routes SQLite & SQL events? *(c — Hermes)*
4. Your credential for B-039? *(b — PEL-L0-B039-SQLiteBuilder)*
5. What does `lippytmai-launch run B-039` do? *(d — activates via ADA)*

**Section 2 — Syntax (Q6–10):**
6. Write a minimal sqlite3 example: ___
7. How do you handle errors in SQLite & SQL? ___
8. One-liner combining sqlite3 with another tool: ___
9. How do you test SQLite & SQL code? ___
10. How do you deploy SQLite & SQL to production? ___

**Section 3 — Application (Q11–15):**
11. Describe a real-world SQLite & SQL scenario that saves an hour.
12. Most common mistake with sqlite3?
13. How does SQLite & SQL connect to security?
14. How does B-039 apply to a production Python project?
15. What would you build first after earning PEL-L0-B039-SQLiteBuilder?

**Section 4 — ACSS (Q16–20):**
16. ADA command for B-039? *(lippytmai-launch run B-039)*
17. Fabric node type for SQLite & SQL? *(ConceptNode)*
18. How does Clone Engine use SQLite & SQL? *(lippytmai teaches in Teach mode)*
19. 2 books that build on B-039?
20. EWYL opportunity unlocked by PEL-L0-B039-SQLiteBuilder?

### 🎧 Audiobook Quiz (10 Questions)

1. Three most important concepts from SQLite: Your First Database?
2. Explain SQLite & SQL in one sentence to a non-developer.
3. First thing to do when sqlite3 fails?
4. Recite your credential.
5. One project buildable with B-039 skills only.
6. ACSS system that stores skill progress? *(Fabric)*
7. ADA activation command? *(lippytmai-launch run B-039)*
8. Next book after B-039? *(B-040 Automation)*
9. Say the EWYL pledge: "I learn, I build, I earn, I share."
10. What makes Python + ACSS a power combination?

### 🎬 Terminal Challenges (5)

1. **Foundation:** Run `sqlite3` — screenshot the output.
2. **Intermediate:** Combine `sqlite3` with error handling.
3. **Applied:** Write a 10-line script automating a real task.
4. **Debug:** Introduce an error, diagnose and fix it.
5. **Capstone:** Run `credential_db.py` — record a 60-second demo.

---

## Appendix E: Glossary & Error Encyclopedia — SQLite: Your First Database

### Glossary (20 Terms)

| Term | Definition | First Seen |
|---|---|---|
| `sqlite3` | [definition in B-039 context] | [B-039] |
| `SQL` | [definition in B-039 context] | [B-039] |
| `CREATE TABLE` | [definition in B-039 context] | [B-039] |
| `INSERT` | [definition in B-039 context] | [B-039] |
| `SELECT` | [definition in B-039 context] | [B-039] |
| `transactions` | [definition in B-039 context] | [B-039] |
| `async` | [definition in B-039 context] | [B-039] |
| `decorator` | [definition in B-039 context] | [B-039] |
| `type hint` | [definition in B-039 context] | [B-039] |
| `dataclass` | [definition in B-039 context] | [B-039] |
| `fixture` | [definition in B-039 context] | [B-039] |
| `Hermes` | [definition in B-039 context] | [B-039] |
| `Fabric` | [definition in B-039 context] | [B-039] |
| `ADA` | [definition in B-039 context] | [B-039] |
| `OMARCHY` | [definition in B-039 context] | [B-039] |
| `credential` | [definition in B-039 context] | [B-039] |
| `EWYL` | [definition in B-039 context] | [B-039] |
| `lippytmai` | [definition in B-039 context] | [B-039] |
| `PEL` | [definition in B-039 context] | [B-039] |
| `Fabric node` | [definition in B-039 context] | [B-039] |

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

## Appendix F: Instructor & Accessibility Guide — SQLite: Your First Database

### Teaching Schedule (4-Week Curriculum)

| Week | Focus | Topics | Outcome |
|---|---|---|---|
| 1 | Foundation | Concepts + setup | Can use SQLite & SQL tools |
| 2 | Intermediate | Core patterns | Can write working code |
| 3 | Applied | Real projects | Can solve production problems |
| 4 | Mastery | DFY + Appendices | Earns `PEL-L0-B039-SQLiteBuilder` |

### Common Confusion Points

1. "When do I use sqlite3 vs. alternatives?" — Show a decision flowchart.
2. "Why does the same code fail in a different environment?" — Explain venv isolation.
3. "How do I know if my code is production-ready?" — Show the VERIFY step always.
4. "How does SQLite & SQL connect to other Python skills?" — Show the ACSS learning path map.
5. "What does earning PEL-L0-B039-SQLiteBuilder actually mean for my career?" — Show EWYL income examples.

### Assessment Rubric

| Criterion | Beginner | Competent | Expert |
|---|---|---|---|
| Code quality | Messy, no types | Working, some types | Clean, typed, tested |
| Error handling | None | Basic try/except | Custom exceptions + logging |
| Testing | No tests | Basic assertions | pytest + fixtures + coverage |
| ACSS integration | Unaware | Uses ADA | Contributes to ACSS |

### Accessibility: Screen reader alt-text for all diagrams. No color-only encoding. Short paragraphs. Audiobook available.

---

## Appendix G: Your Learning Path — SQLite: Your First Database

### Where You Are Now

```
  Phase 2: Python Programming (B-026–B-055)
  [█████████░░░░░░░░░░░] 46%

  ✅ B-038 Regex Wizard (PEL-L0-B038-RegexWizard)
  👉 B-039: SQLite: Your First Database ← YOU ARE HERE
  ⬜ B-040 Automation (PEL-L0-B040-AutomationPro)
```

### Credential Chain

```
PEL-L0-B038-RegexWizard → PEL-L0-B039-SQLiteBuilder → PEL-L0-B040-AutomationPro
```

### Next Steps

1. Claim `PEL-L0-B039-SQLiteBuilder` (Appendix C, Prompt 27)
2. Build `credential_db.py` (Appendix H)
3. Start `B-040 Automation`

### Cross-Phase Connections

```
Phase 1: Linux Foundations → Phase 2: Python (YOU ARE HERE)
    ↓ B-039 connects to:
Phase 3: Blockchain Development (B-056+)
```

---

## Appendix H: Real Project Showcase — SQLite: Your First Database

### Project: `credential_db.py`

**Credential gated:** Complete this project to qualify for `PEL-L0-B039-SQLiteBuilder`

### Complete Code

```python
#!/usr/bin/env python3
import sqlite3
from pathlib import Path

DB_PATH = Path("credentials.db")

def init_db(path: Path = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS credentials (
            id INTEGER PRIMARY KEY,
            book_id TEXT NOT NULL,
            credential TEXT NOT NULL UNIQUE,
            earned_at TEXT NOT NULL,
            status TEXT DEFAULT 'EARNED'
        )
    """)
    conn.commit()
    return conn

def claim_credential(conn: sqlite3.Connection, book_id: str, credential: str) -> None:
    from datetime import datetime
    conn.execute(
        "INSERT OR IGNORE INTO credentials (book_id, credential, earned_at) VALUES (?,?,?)",
        (book_id, credential, datetime.now().isoformat())
    )
    conn.commit()
    print(f"Credential claimed: {credential}")

```

### Deploy Instructions

```bash
# Run the project
python credential_db.py --help
python credential_db.py

# Test it
pytest test_credential_db.py -v  # if tests exist

# Verify
echo "Exit: $?"
```

### Extend It

1. Add type hints to all functions
2. Add pytest test coverage
3. Add CLI interface with typer
4. Containerize with Docker
5. Add structured logging

### 🎧 Walkthrough: *"Build credential_db.py step by step. When it runs successfully, you've earned PEL-L0-B039-SQLiteBuilder."*

### 🎬 Video: SHOW empty editor → BUILD code live → VERIFY execution → CTA: "Claim PEL-L0-B039-SQLiteBuilder."

---

## Further Reading

- 📄 [Back to README](../README.md)
- 📄 [Product Excellence Framework](PRODUCT-EXCELLENCE-FRAMEWORK.md)
- 📄 [AI Clone Engine Swarms](ai-clone-engine-swarms.md)
- 📄 [ACSS Cross-Platform Copilot Deployment](acss-cross-platform-copilot-deployment.md)
- 📄 [ADA Deployment Activations](ai-deployment-activations.md)
- 📄 [Previous: B-038](B-038-*.md)
- 📄 [Next: B-040](B-040-*.md)

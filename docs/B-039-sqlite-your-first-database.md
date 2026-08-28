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

## Further Reading

- 📄 [`docs/B-037-working-with-dates-and-times.md`](B-037-working-with-dates-and-times.md) — Storing timestamps in SQLite
- 📄 [`docs/B-040-automation-scripts-that-save-hours.md`](B-040-automation-scripts-that-save-hours.md) — File operations with pathlib
- 📄 [`docs/B-032-the-internet-in-a-function.md`](B-032-the-internet-in-a-function.md) — Caching API responses in SQLite
- 🏠 [`README.md`](../README.md) — Encyclopedia home

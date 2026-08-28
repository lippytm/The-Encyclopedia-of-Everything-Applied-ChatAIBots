# B-045: CSV and Spreadsheet Automation

### csv, pandas basics, openpyxl, and the Art of Data in Rows and Columns

> *"Data lives in spreadsheets. Every business, every dataset, every report starts as rows and columns. CSV is the universal exchange format. pandas is how Python engineers turn those rows into insight. openpyxl is how you speak directly to Excel. Learn all three and you'll never stare helplessly at a .csv again."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Read and write CSV files with Python's built-in `csv` module
2. Load, filter, group, and summarize data with `pandas`
3. Generate formatted Excel reports with `openpyxl`
4. Handle common data quality issues (missing values, type coercion)
5. Build an `expense_report.py` — an automated expense report generator

**Prerequisite:** B-037 (dates), B-039 (data patterns), B-036 (type hints)

**Build Artifact:** `~/developer-workspace/projects/python-foundations/expense_report.py`

**Credential:** `CCSLL-L1-B045-DataReporter` — on-chain on Base

---

## Chapter 1: The csv Module

```python
import csv
from pathlib import Path

# Writing CSV
expenses = [
    {"date": "2026-08-01", "category": "food",      "amount": 45.50, "description": "Lunch"},
    {"date": "2026-08-02", "category": "transport",  "amount": 12.00, "description": "Bus"},
    {"date": "2026-08-05", "category": "software",   "amount": 99.00, "description": "GitHub Pro"},
    {"date": "2026-08-10", "category": "food",       "amount": 32.75, "description": "Dinner"},
    {"date": "2026-08-15", "category": "cloud",      "amount": 150.00, "description": "AWS"},
]

csv_path = Path("/tmp/expenses.csv")
with csv_path.open("w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["date", "category", "amount", "description"])
    writer.writeheader()
    writer.writerows(expenses)

print(csv_path.read_text())

# Reading CSV
with csv_path.open(newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row)   # {'date': '2026-08-01', 'category': 'food', ...}
```

---

## Chapter 2: pandas — DataFrames

```python
import pandas as pd
from pathlib import Path

# Load a CSV into a DataFrame
df = pd.read_csv("/tmp/expenses.csv")
print(df)
print(df.dtypes)     # column types
print(df.shape)      # (rows, columns)
print(df.head(3))    # first 3 rows
print(df.info())     # summary

# Select columns
amounts = df["amount"]            # Series
subset  = df[["date", "amount"]]  # DataFrame

# Filter rows
food = df[df["category"] == "food"]
expensive = df[df["amount"] > 50]
print(food)
print(expensive)

# Add a computed column
df["amount_eur"] = df["amount"] * 0.92

# Sort
df_sorted = df.sort_values("amount", ascending=False)
print(df_sorted)
```

---

## Chapter 3: pandas Aggregation

```python
import pandas as pd

df = pd.read_csv("/tmp/expenses.csv")

# Total spending
total = df["amount"].sum()
print(f"Total: ${total:.2f}")

# Average transaction
avg = df["amount"].mean()
print(f"Average: ${avg:.2f}")

# Group by category
by_category = df.groupby("category")["amount"].sum().sort_values(ascending=False)
print(by_category)

# Count per category
counts = df.groupby("category").size()
print(counts)

# Multiple aggregations at once
summary = df.groupby("category")["amount"].agg(["sum", "mean", "count"])
summary.columns = ["total", "average", "transactions"]
print(summary)

# Date-based analysis
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")
monthly = df.groupby("month")["amount"].sum()
print(monthly)
```

---

## Chapter 4: Data Cleaning

```python
import pandas as pd
import numpy as np

# Simulated messy data
data = {
    "date": ["2026-08-01", None, "2026-08-10", "bad-date"],
    "amount": [45.50, None, "32.75", -5.00],
    "category": ["food", "transport", "food", ""],
}
df = pd.DataFrame(data)
print(df)

# Check for missing values
print(df.isnull().sum())

# Drop rows with any nulls
df_clean = df.dropna()

# Fill missing values
df_filled = df.fillna({"category": "unknown", "amount": 0.0})

# Convert types safely
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")  # bad strings → NaN

# Remove invalid rows
df = df[df["amount"] > 0]                # remove negatives
df = df[df["category"].str.strip() != ""]  # remove blank categories

# Parse dates, coerce bad ones to NaT
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])   # drop rows with unparseable dates
print(f"\nClean rows: {len(df)}")
```

---

## Chapter 5: openpyxl — Excel Reports

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, numbers
from openpyxl.utils import get_column_letter

wb = Workbook()
ws = wb.active
ws.title = "Expense Report"

# Header row with styling
headers = ["Date", "Category", "Amount", "Description"]
header_fill = PatternFill("solid", fgColor="1F4E79")
header_font = Font(color="FFFFFF", bold=True)

for col, header in enumerate(headers, start=1):
    cell = ws.cell(row=1, column=col, value=header)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center")

# Data rows
rows = [
    ("2026-08-01", "food",      45.50,  "Lunch"),
    ("2026-08-02", "transport", 12.00,  "Bus"),
    ("2026-08-05", "software",  99.00,  "GitHub Pro"),
    ("2026-08-10", "food",      32.75,  "Dinner"),
    ("2026-08-15", "cloud",    150.00,  "AWS"),
]

for row_idx, row in enumerate(rows, start=2):
    ws.append(list(row))
    # Format amount column as currency
    ws.cell(row=row_idx, column=3).number_format = '"$"#,##0.00'

# Auto-size columns
for col in ws.columns:
    max_len = max(len(str(cell.value or "")) for cell in col)
    ws.column_dimensions[get_column_letter(col[0].column)].width = max_len + 4

# Total row
last_row = len(rows) + 2
ws.cell(row=last_row, column=2, value="TOTAL").font = Font(bold=True)
ws.cell(row=last_row, column=3, value=f"=SUM(C2:C{last_row-1})")
ws.cell(row=last_row, column=3).number_format = '"$"#,##0.00'

wb.save("/tmp/expense_report.xlsx")
print("Saved: /tmp/expense_report.xlsx")
```

---

## Chapter 6: The Build — Expense Report Generator

```python
#!/usr/bin/env python3
"""
expense_report.py — B-045 Build Artifact

Reads a CSV of expenses, produces a pandas summary,
and generates a formatted Excel report.

Usage:
    pip install pandas openpyxl
    python3 expense_report.py [expenses.csv]
"""
from __future__ import annotations

import csv
import sys
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter


# --- Sample data generator ---

def generate_sample_csv(path: Path) -> None:
    rows = [
        ("2026-08-01", "food",      "Lunch meeting",        45.50),
        ("2026-08-02", "transport", "Taxi to airport",      38.00),
        ("2026-08-05", "software",  "GitHub Pro",           99.00),
        ("2026-08-07", "food",      "Team dinner",         187.25),
        ("2026-08-10", "cloud",     "AWS bill",            210.50),
        ("2026-08-12", "transport", "Uber",                 22.00),
        ("2026-08-15", "software",  "Figma",                45.00),
        ("2026-08-18", "cloud",     "GCP",                  89.00),
        ("2026-08-20", "food",      "Working lunch",        28.75),
        ("2026-08-25", "office",    "Keyboard",            149.00),
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "category", "description", "amount"])
        writer.writerows(rows)
    print(f"Generated sample CSV: {path}")


# --- Analysis ---

def analyze(csv_path: Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df = df.dropna(subset=["date", "amount"])
    df = df[df["amount"] > 0]

    summary = (
        df.groupby("category")["amount"]
        .agg(total="sum", average="mean", transactions="count")
        .sort_values("total", ascending=False)
        .reset_index()
    )
    return df, summary


# --- Excel export ---

BLUE = PatternFill("solid", fgColor="1F4E79")
GRAY = PatternFill("solid", fgColor="D9D9D9")
WHITE_BOLD = Font(color="FFFFFF", bold=True)
BOLD = Font(bold=True)
CENTER = Alignment(horizontal="center")
CURRENCY_FMT = '"$"#,##0.00'


def _set_header(ws: Any, row: int, headers: list[str]) -> None:
    for col, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=col, value=h)
        c.fill = BLUE
        c.font = WHITE_BOLD
        c.alignment = CENTER


def _autosize(ws: Any) -> None:
    for col in ws.columns:
        max_len = max(len(str(cell.value or "")) for cell in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = max_len + 4


def export_excel(df: pd.DataFrame, summary: pd.DataFrame, output: Path) -> None:
    wb = Workbook()

    # --- Sheet 1: Transactions ---
    ws1 = wb.active
    ws1.title = "Transactions"
    _set_header(ws1, 1, ["Date", "Category", "Description", "Amount"])
    for r, row in enumerate(df.itertuples(index=False), start=2):
        ws1.cell(r, 1, row.date.strftime("%Y-%m-%d") if not pd.isna(row.date) else "")
        ws1.cell(r, 2, row.category)
        ws1.cell(r, 3, row.description)
        cell = ws1.cell(r, 4, row.amount)
        cell.number_format = CURRENCY_FMT
    _autosize(ws1)

    # --- Sheet 2: Summary ---
    ws2 = wb.create_sheet("Summary")
    _set_header(ws2, 1, ["Category", "Total", "Average", "Transactions"])
    for r, row in enumerate(summary.itertuples(index=False), start=2):
        ws2.cell(r, 1, row.category)
        for col, val in [(2, row.total), (3, row.average)]:
            c = ws2.cell(r, col, val)
            c.number_format = CURRENCY_FMT
        ws2.cell(r, 4, row.transactions)

    grand_row = len(summary) + 2
    ws2.cell(grand_row, 1, "GRAND TOTAL").font = BOLD
    ws2.cell(grand_row, 2, f"=SUM(B2:B{grand_row-1})").number_format = CURRENCY_FMT
    ws2.cell(grand_row, 2).font = BOLD
    _autosize(ws2)

    wb.save(output)
    print(f"\n✅ Excel report saved: {output}")


def main() -> None:
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/expenses_sample.csv")
    output = csv_path.with_suffix(".xlsx")

    if not csv_path.exists():
        generate_sample_csv(csv_path)

    df, summary = analyze(csv_path)

    print("\n=== Expense Summary ===\n")
    print(summary.to_string(index=False))
    print(f"\nTotal spend: ${df['amount'].sum():,.2f}")
    print(f"Transactions: {len(df)}")
    print(f"Date range: {df['date'].min().date()} → {df['date'].max().date()}")

    export_excel(df, summary, output)


if __name__ == "__main__":
    main()
```

```bash
pip install pandas openpyxl
python3 ~/developer-workspace/projects/python-foundations/expense_report.py
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-045 Verification ==="
python3 -c "
import io, csv
import pandas as pd

# Write CSV in memory
buf = io.StringIO()
writer = csv.DictWriter(buf, fieldnames=['category', 'amount'])
writer.writeheader()
writer.writerows([
    {'category': 'food',    'amount': 45.50},
    {'category': 'cloud',   'amount': 99.00},
    {'category': 'food',    'amount': 32.75},
])
buf.seek(0)

df = pd.read_csv(buf)
total = df['amount'].sum()
by_cat = df.groupby('category')['amount'].sum().to_dict()
print(f'Total: \${total:.2f}')
print(f'By category: {by_cat}')
print('✅ csv + pandas works')
"
```

---

## What's Next: Phase 2 Batch 5 Preview

With B-041–B-045 complete, you've unlocked the **Python Web & Data layer**:

| Book | Skill |
|---|---|
| B-041 | Ethical web scraping |
| B-042 | REST API with FastAPI |
| B-043 | Async/concurrent I/O |
| B-044 | Package organization |
| **B-045** | **CSV + data automation** |

**Phase 2 Batch 5 (B-046–B-050)** — Python DevOps:
- B-046: *Logging Like a Pro* — logging module, handlers, formatters, rotation
- B-047: *Command-Line Interfaces with argparse* — building CLI tools
- B-048: *Working with JSON and YAML* — structured configuration
- B-049: *Environment Variables and Configuration* — .env, secrets management
- B-050: *Docker for Python Developers* — containerize your Python apps

---

## Further Reading

- 📄 [`docs/B-039-sqlite-your-first-database.md`](B-039-sqlite-your-first-database.md) — Persisting processed data
- 📄 [`docs/B-037-working-with-dates-and-times.md`](B-037-working-with-dates-and-times.md) — Date parsing in pandas
- 📄 [`docs/B-041-python-and-the-web-scraping-basics.md`](B-041-python-and-the-web-scraping-basics.md) — Collecting data to analyze
- 🏠 [`README.md`](../README.md) — Encyclopedia home

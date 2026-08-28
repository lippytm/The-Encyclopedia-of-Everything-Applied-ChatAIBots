# B-009: Working with Text Like a Pro

### grep, sed, awk, and cut — The Terminal Text Processing Toolkit

> *"All data is text. Log files, JSON APIs, CSV exports, configuration files, source code — at the deepest level it's all characters in a stream. The developer who can manipulate that stream from the command line can solve problems that would take others hours of manual work in seconds."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Search and filter text with `grep` (including regex patterns)
2. Replace text in files and streams with `sed`
3. Process structured text with `awk` (column-aware)
4. Extract specific columns with `cut`
5. Build a log parser script that extracts useful information from a raw log file

**Prerequisite:** B-001 through B-005 (terminal fluency, pipes)

**Build Artifact:** `log-parser.sh` — a script that parses an Apache-style access log and generates a summary report

**Credential:** `CLL-L1-B009-TextMaster` — on-chain on Base

---

## Chapter 1: The Text Processing Philosophy

Unix was built around one idea: **everything is text, and text can be piped**.

Log files are text. Config files are text. API responses are text. CSV data is text. Even binary data often has a text representation. The four tools in this book — grep, sed, awk, cut — are designed to work together in pipelines to transform any text into any other text.

| Tool | Best For |
|---|---|
| `grep` | Finding lines that match a pattern |
| `sed` | Substituting/deleting text in a stream |
| `awk` | Column-aware processing, arithmetic, conditionals |
| `cut` | Extracting specific columns from delimited text |

*[Reality — these four tools are available on every Linux system and macOS by default, and have been since the 1970s]*

---

## Chapter 2: grep — Advanced Patterns

```bash
# Basic: find lines containing a pattern
grep "error" app.log

# Extended regex (-E) — enables |, +, ?, {}
grep -E "error|warning|critical" app.log

# Count matches per file
grep -c "404" access.log

# Show context: 2 lines before and after each match
grep -B2 -A2 "FATAL" app.log

# Recursive search through directory
grep -r "TODO" ./src/

# Only show the matching part (not the whole line)
grep -o "PID:[0-9]*" app.log

# Regex patterns — some useful ones
grep -E "^[0-9]{4}-[0-9]{2}-[0-9]{2}" app.log    # lines starting with date
grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" access.log  # IP addresses
grep -E "HTTP/[0-9]\.[0-9]\" [4-5][0-9]{2}" access.log   # 4xx and 5xx errors
```

### Basic Regex Quick Reference

| Pattern | Matches |
|---|---|
| `.` | Any single character |
| `*` | Zero or more of the previous |
| `+` | One or more of the previous (`-E` required) |
| `?` | Zero or one of the previous (`-E` required) |
| `^` | Start of line |
| `$` | End of line |
| `[abc]` | Any of a, b, or c |
| `[0-9]` | Any digit |
| `[a-z]` | Any lowercase letter |
| `\b` | Word boundary |

---

## Chapter 3: sed — Stream Editor

`sed` reads text line by line and applies commands to each line. The most common use: substitution.

```bash
# Substitute first occurrence per line: s/pattern/replacement/
sed 's/error/ERROR/' app.log

# Substitute all occurrences per line (g = global)
sed 's/error/ERROR/g' app.log

# Case-insensitive substitution
sed 's/error/ERROR/gi' app.log

# Edit file in place (-i flag) — modifies the actual file
sed -i 's/localhost/0.0.0.0/g' config.json

# Backup original when using -i
sed -i.bak 's/old/new/g' config.json
# Creates config.json.bak as a backup

# Delete lines matching a pattern
sed '/^#/d' config.txt        # delete comment lines (start with #)
sed '/^$/d' config.txt        # delete empty lines

# Print only matching lines (-n + p)
sed -n '/ERROR/p' app.log

# Replace between line numbers
sed '5,10s/foo/bar/g' file.txt
```

*[Reality — always test `sed` without `-i` first to preview changes before modifying files in place]*

---

## Chapter 4: awk — The Column Processor

`awk` treats each line as a set of **fields** separated by whitespace (or a custom delimiter). `$1` is field 1, `$2` is field 2, `$NF` is the last field.

```bash
# Print the first column of every line
awk '{print $1}' data.txt

# Print columns 1 and 3
awk '{print $1, $3}' data.txt

# Use a custom delimiter (-F)
awk -F: '{print $1}' /etc/passwd      # first field of colon-delimited file
awk -F, '{print $2}' data.csv         # second column of CSV

# Arithmetic: sum column 5
awk '{sum += $5} END {print "Total:", sum}' data.txt

# Conditional: print lines where column 3 > 100
awk '$3 > 100 {print}' data.txt

# Pattern matching: print lines where column 1 matches regex
awk '$1 ~ /ERROR/ {print NR, $0}' app.log

# Process Apache access logs: count requests per IP
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -10
```

### awk Built-in Variables

| Variable | Meaning |
|---|---|
| `$0` | The entire current line |
| `$1, $2, …` | Individual fields |
| `$NF` | Last field |
| `NR` | Current line number (record number) |
| `NF` | Number of fields in the current line |
| `FS` | Field separator (default: whitespace) |

---

## Chapter 5: cut — Simple Column Extraction

For simple column extraction from delimited text, `cut` is faster and simpler than `awk`:

```bash
# Cut by character position
cut -c1-10 file.txt         # first 10 characters
cut -c5- file.txt           # from char 5 to end

# Cut by delimiter and field
cut -d: -f1 /etc/passwd     # first field, colon-delimited
cut -d, -f2,4 data.csv      # columns 2 and 4 from CSV
cut -d$'\t' -f3 data.tsv    # third column from tab-delimited

# Combine with other tools
cat /etc/passwd | cut -d: -f1 | sort   # list all usernames, sorted
```

---

## Chapter 6: The Build — log-parser.sh

First, create a sample log to parse:

```bash
cat > ~/developer-workspace/logs/sample-access.log << 'EOF'
192.168.1.1 - - [28/Aug/2026:01:00:01 +0000] "GET /api/users HTTP/1.1" 200 1234
10.0.0.5 - - [28/Aug/2026:01:00:02 +0000] "POST /api/login HTTP/1.1" 401 89
192.168.1.1 - - [28/Aug/2026:01:00:03 +0000] "GET /api/repos HTTP/1.1" 200 5678
203.0.113.42 - - [28/Aug/2026:01:00:04 +0000] "GET /api/users HTTP/1.1" 404 23
10.0.0.5 - - [28/Aug/2026:01:00:05 +0000] "POST /api/login HTTP/1.1" 401 89
203.0.113.42 - - [28/Aug/2026:01:00:06 +0000] "GET /admin HTTP/1.1" 403 0
192.168.1.1 - - [28/Aug/2026:01:00:07 +0000] "GET /api/users HTTP/1.1" 200 1234
10.0.0.5 - - [28/Aug/2026:01:00:08 +0000] "POST /api/login HTTP/1.1" 200 512
203.0.113.42 - - [28/Aug/2026:01:00:09 +0000] "GET /api/users HTTP/1.1" 500 0
192.168.1.1 - - [28/Aug/2026:01:00:10 +0000] "DELETE /api/repos/42 HTTP/1.1" 204 0
EOF
```

```bash
#!/bin/bash
# log-parser.sh — B-009 Build Artifact
set -euo pipefail

LOG_FILE="${1:-$HOME/developer-workspace/logs/sample-access.log}"
REPORT_FILE="$HOME/developer-workspace/logs/log-report.txt"

if [ ! -f "$LOG_FILE" ]; then
    echo "Log file not found: $LOG_FILE"
    exit 1
fi

{
echo "========================================"
echo "  Log Analysis Report"
echo "  Generated: $(date)"
echo "  File: $LOG_FILE"
echo "========================================"
echo ""

echo "--- Request Summary ---"
TOTAL=$(wc -l < "$LOG_FILE")
echo "Total requests: $TOTAL"
echo "2xx (success):  $(grep -c '" 2[0-9][0-9] ' "$LOG_FILE" 2>/dev/null || echo 0)"
echo "3xx (redirect): $(grep -c '" 3[0-9][0-9] ' "$LOG_FILE" 2>/dev/null || echo 0)"
echo "4xx (client err): $(grep -c '" 4[0-9][0-9] ' "$LOG_FILE" 2>/dev/null || echo 0)"
echo "5xx (server err): $(grep -c '" 5[0-9][0-9] ' "$LOG_FILE" 2>/dev/null || echo 0)"

echo ""
echo "--- Top 5 IPs by Request Count ---"
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -5 | \
    awk '{printf "  %-5s requests from %s\n", $1, $2}'

echo ""
echo "--- Top 5 Requested Paths ---"
awk '{print $7}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -5 | \
    awk '{printf "  %-5s %s\n", $1, $2}'

echo ""
echo "--- 4xx and 5xx Errors ---"
grep -E '" [45][0-9][0-9] ' "$LOG_FILE" | \
    awk '{print $9, $7, $1}' | sort

} | tee "$REPORT_FILE"

echo ""
echo "Report saved to: $REPORT_FILE"
```

```bash
chmod +x ~/log-parser.sh
~/log-parser.sh
```

---

## Chapter 7: Proof of Work

```bash
~/log-parser.sh ~/developer-workspace/logs/sample-access.log
cat ~/developer-workspace/logs/log-report.txt
```

---


---

## Chapter 12: Done-For-You Lessons — Text Processor

> *"The fastest way to learn is to build something real. These ten lessons give you exactly that — ten deployable tools, ready to use, built by your own hands."*

---

### DFY Lesson 1 — regex-cheatsheet.sh

> **What you're building:** Interactive regex tester: test patterns against sample text

**📘 Ebook Figure**

```bash
# DFY-B-009-L01: regex-cheatsheet.sh
# Domain: Interactive regex tester: test patterns against sample text
# Time to build: 15–25 minutes
# Credential: CLL-L0-B009-TextProcessor

# STEP 1: Create the script file
nano ~/regex-cheatsheet.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/regex-cheatsheet.sh.sh

# STEP 4: Test it
~/regex-cheatsheet.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 1: regex-cheatsheet.sh. Interactive regex tester: test patterns against sample text. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep regex-ch` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/regex-cheatsheet.sh && ~/regex-cheatsheet.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built regex-cheatsheet.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 2 — log-extractor.sh

> **What you're building:** Extract structured fields (date, IP, status) from any log format

**📘 Ebook Figure**

```bash
# DFY-B-009-L02: log-extractor.sh
# Domain: Extract structured fields (date, IP, status) from any log format
# Time to build: 15–25 minutes
# Credential: CLL-L0-B009-TextProcessor

# STEP 1: Create the script file
nano ~/log-extractor.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/log-extractor.sh.sh

# STEP 4: Test it
~/log-extractor.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 2: log-extractor.sh. Extract structured fields (date, IP, status) from any log format. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep log-extr` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/log-extractor.sh && ~/log-extractor.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built log-extractor.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 3 — csv-analyzer.sh

> **What you're building:** Parse CSV: count rows, list columns, filter by value, compute stats

**📘 Ebook Figure**

```bash
# DFY-B-009-L03: csv-analyzer.sh
# Domain: Parse CSV: count rows, list columns, filter by value, compute stats
# Time to build: 15–25 minutes
# Credential: CLL-L0-B009-TextProcessor

# STEP 1: Create the script file
nano ~/csv-analyzer.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/csv-analyzer.sh.sh

# STEP 4: Test it
~/csv-analyzer.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 3: csv-analyzer.sh. Parse CSV: count rows, list columns, filter by value, compute stats. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep csv-anal` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/csv-analyzer.sh && ~/csv-analyzer.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built csv-analyzer.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 4 — text-diff-reporter.sh

> **What you're building:** Compare two text files, report additions/deletions with context

**📘 Ebook Figure**

```bash
# DFY-B-009-L04: text-diff-reporter.sh
# Domain: Compare two text files, report additions/deletions with context
# Time to build: 15–25 minutes
# Credential: CLL-L0-B009-TextProcessor

# STEP 1: Create the script file
nano ~/text-diff-reporter.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/text-diff-reporter.sh.sh

# STEP 4: Test it
~/text-diff-reporter.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 4: text-diff-reporter.sh. Compare two text files, report additions/deletions with context. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep text-dif` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/text-diff-reporter.sh && ~/text-diff-reporter.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built text-diff-reporter.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 5 — bulk-renamer.sh

> **What you're building:** Rename files using sed patterns (e.g., spaces→underscores, lowercase)

**📘 Ebook Figure**

```bash
# DFY-B-009-L05: bulk-renamer.sh
# Domain: Rename files using sed patterns (e.g., spaces→underscores, lowercase)
# Time to build: 15–25 minutes
# Credential: CLL-L0-B009-TextProcessor

# STEP 1: Create the script file
nano ~/bulk-renamer.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/bulk-renamer.sh.sh

# STEP 4: Test it
~/bulk-renamer.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 5: bulk-renamer.sh. Rename files using sed patterns (e.g., spaces→underscores, lowercase). This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep bulk-ren` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/bulk-renamer.sh && ~/bulk-renamer.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built bulk-renamer.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 6 — word-frequency.sh

> **What you're building:** Count word frequency in any text file, show top-N with bar chart

**📘 Ebook Figure**

```bash
# DFY-B-009-L06: word-frequency.sh
# Domain: Count word frequency in any text file, show top-N with bar chart
# Time to build: 15–25 minutes
# Credential: CLL-L0-B009-TextProcessor

# STEP 1: Create the script file
nano ~/word-frequency.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/word-frequency.sh.sh

# STEP 4: Test it
~/word-frequency.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 6: word-frequency.sh. Count word frequency in any text file, show top-N with bar chart. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep word-fre` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/word-frequency.sh && ~/word-frequency.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built word-frequency.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 7 — multiline-replacer.sh

> **What you're building:** sed multi-line replacement with backup file creation

**📘 Ebook Figure**

```bash
# DFY-B-009-L07: multiline-replacer.sh
# Domain: sed multi-line replacement with backup file creation
# Time to build: 15–25 minutes
# Credential: CLL-L0-B009-TextProcessor

# STEP 1: Create the script file
nano ~/multiline-replacer.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/multiline-replacer.sh.sh

# STEP 4: Test it
~/multiline-replacer.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 7: multiline-replacer.sh. sed multi-line replacement with backup file creation. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep multilin` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/multiline-replacer.sh && ~/multiline-replacer.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built multiline-replacer.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 8 — json-field-extractor.sh

> **What you're building:** Extract specific fields from line-delimited JSON using awk/jq

**📘 Ebook Figure**

```bash
# DFY-B-009-L08: json-field-extractor.sh
# Domain: Extract specific fields from line-delimited JSON using awk/jq
# Time to build: 15–25 minutes
# Credential: CLL-L0-B009-TextProcessor

# STEP 1: Create the script file
nano ~/json-field-extractor.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/json-field-extractor.sh.sh

# STEP 4: Test it
~/json-field-extractor.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 8: json-field-extractor.sh. Extract specific fields from line-delimited JSON using awk/jq. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep json-fie` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/json-field-extractor.sh && ~/json-field-extractor.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built json-field-extractor.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 9 — grep-toolkit.sh

> **What you're building:** Advanced grep aliases: recursive, context, invert, case, count

**📘 Ebook Figure**

```bash
# DFY-B-009-L09: grep-toolkit.sh
# Domain: Advanced grep aliases: recursive, context, invert, case, count
# Time to build: 15–25 minutes
# Credential: CLL-L0-B009-TextProcessor

# STEP 1: Create the script file
nano ~/grep-toolkit.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/grep-toolkit.sh.sh

# STEP 4: Test it
~/grep-toolkit.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 9: grep-toolkit.sh. Advanced grep aliases: recursive, context, invert, case, count. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep grep-too` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/grep-toolkit.sh && ~/grep-toolkit.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built grep-toolkit.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 10 — text-report-builder.sh

> **What you're building:** Build a formatted text report from raw data using awk templating

**📘 Ebook Figure**

```bash
# DFY-B-009-L10: text-report-builder.sh
# Domain: Build a formatted text report from raw data using awk templating
# Time to build: 15–25 minutes
# Credential: CLL-L0-B009-TextProcessor

# STEP 1: Create the script file
nano ~/text-report-builder.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/text-report-builder.sh.sh

# STEP 4: Test it
~/text-report-builder.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 10: text-report-builder.sh. Build a formatted text report from raw data using awk templating. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep text-rep` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/text-report-builder.sh && ~/text-report-builder.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built text-report-builder.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---


---

### Chapter 12 Credential Claim

You've built 10 real tools in the **grep** domain. Every one is deployable today.

**To claim your credential:** Open your AI Copilot (Appendix C) and send:
```
I have completed all 10 DFY lessons from Working With Text Like a Pro (B-009).
My builds: regex-cheatsheet.sh, log-extractor.sh, csv-analyzer.sh, text-diff-reporter.sh, bulk-renamer.sh, word-frequency.sh, multiline-replacer.sh, json-field-extractor.sh, grep-toolkit.sh, text-report-builder.sh.
I am ready to claim: CLL-L0-B009-TextProcessor
Please guide me through the credential ceremony.
```

---

## Chapter 13: How It Works — Use Cases & Applications

> *"A skill without context is just a trick. Understanding when to use it — and where it applies — is what separates professionals from beginners."*

---

### 📘 Ebook — Mechanism & Conditions

**How Grep works (the 30-second mechanism):**

grep → sed → awk → cut → tr → sort → uniq → wc → xargs → regex basics → all driven by the same underlying OS primitives. When you understand the mechanism, you can apply it anywhere.

**Conditions table — when to use these skills:**

| Condition | Tool/Approach | Why |
|---|---|---|
| System investigation | CLI tools from this book | Fastest — no GUI overhead |
| Automation task | Shell script using these tools | Repeatable, testable, documentable |
| Remote server | Same tools via SSH | Works identically on any Linux server |
| CI/CD pipeline | These commands in GitHub Actions | Linux is the standard CI environment |
| Production system | Understand before touching | These tools give you the diagnostic picture |

**Flexibility points — where these skills apply across domains:**

| Domain | Application |
|---|---|
| Web development | Debug server issues, automate deployment checks |
| Data engineering | Process logs, transform text files, monitor pipelines |
| DevOps/SRE | System diagnostics, service management, incident response |
| Security | Audit configurations, detect anomalies, forensic analysis |
| AI/ML engineering | Manage training processes, monitor resource usage |

---

### 🎧 Audiobook — 3-Minute Narrator Script

*lippytmai voice · measured pace · for commute listening*

> *"Let's talk about where the skills from this book actually apply in the real world."*

> *"B-009 teaches you grep — but the application goes far beyond what the chapter title suggests. Every developer, DevOps engineer, data scientist, and security researcher uses these exact tools every day. The command line is not a developer tool — it is the universal interface to every computer that matters."*

> *"When your web application crashes at 2am, you won't open a GUI. You'll open a terminal and use exactly what you learned here. When you need to automate a task that runs on three different servers, these are the tools. When an interviewer asks you to debug a live Linux system, this book is what gets you through it."*

> *"The five domains where these skills pay off: web development, data engineering, DevOps, security, and AI. In every one of them, the terminal is the first tool you reach for when something goes wrong — or when you need to build something fast."*

---

### 🎬 Video — 5-Domain Showcase

**Duration:** 8 minutes · 5 domains × ~90 seconds each

**Domain 1: Web Development**
> Terminal shows: debug a crashed nginx service using this book's tools

**Domain 2: Data Engineering**
> Terminal shows: process a 1M-line log file in seconds

**Domain 3: DevOps/SRE**
> Terminal shows: 60-second incident response diagnostic

**Domain 4: Security**
> Terminal shows: audit tool from this book finding a misconfiguration

**Domain 5: AI/ML Engineering**
> Terminal shows: monitor a training job, restart on failure

---

### ✅ Use Cases Summary

After completing this book you can:
- Interactive regex tester: test patterns against sample text
- Extract structured fields (date, IP, status) from any log format
- Parse CSV: count rows, list columns, filter by value, compute stats
- Compare two text files, report additions/deletions with context
- Rename files using sed patterns (e.g., spaces→underscores, lowercase)
- Count word frequency in any text file, show top-N with bar chart
- sed multi-line replacement with backup file creation
- Extract specific fields from line-delimited JSON using awk/jq
- Advanced grep aliases: recursive, context, invert, case, count
- Build a formatted text report from raw data using awk templating
- Confidently explain these tools in a technical interview
- Apply them on any Linux system, remote or local
- Integrate them into scripts, CI/CD pipelines, and automation workflows

---

## Appendix A: Quick Reference Card — Text Processor

> *"The 80/20 of B-009. These commands cover 80% of real-world use cases."*

**Top 15 Commands:**

```bash
# GREP — essential commands
# (domain-specific — see book chapters for full explanations)
# Each command below is covered in detail in this book

# Core workflow
man [command]          # Always start here for any unfamiliar tool
[command] --help       # Short help for any command
info [command]         # Detailed GNU info page

# The three most important commands from this book:
# 1. [See Chapter 2]
# 2. [See Chapter 5]  
# 3. [See Chapter 8]
```

**Credential:** `CLL-L0-B009-TextProcessor`
**Claim at:** `lippytm.ai/credentials`

---

## Appendix B: ACSS Connection — B-009

This book is part of the **AI Conglomerate Swarms System (ACSS)** — the continuously self-learning intelligence layer across all lippytm.ai projects.

| System | Connection |
|---|---|
| **CLL** | B-009 contributes to Level 0 of the Complete Linux Library |
| **Hermes** | Events: `BookCompleted`, `CredentialMinted`, `DFYLessonBuilt` |
| **Fabric** | Your builds and questions feed the knowledge synthesis engine |
| **ADA** | This book is activatable: `lippytmai-launch run B-009` |
| **lippytmai** | Your AI teaching partner for every lesson in this book |


---

## Chapter 14: ACSS Explainer Series — Text Processor

> *"A tool you understand is ten times more powerful than a tool you just use."*

These 10 explainer lessons connect the content of this book to the full lippytm.ai AI Conglomerate Swarms System (ACSS). Understanding the ACSS architecture transforms each individual skill from a standalone trick into a node in a living, connected intelligence network.

---

### Explainer 1 — What Is the ACSS?

> *"How the AI Conglomerate Swarms System connects this book to every other resource in the lippytm.ai ecosystem"*

**📘 Ebook:** Fabric maps every concept in this book to the broader knowledge graph — when you learn {domain}, Fabric links it to Python ({next}) and every other phase.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 1: What Is the ACSS?. How the AI Conglomerate Swarms System connects this book to every other resource in the lippytm.ai ecosystem. This is how the lippytm.ai ACSS works at the [ACSS] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ACSS component and its connection to this book
- Explain: how this specific concept (from B-009) routes through ACSS

🤖 **Copilot Prompt:** *"Explain how the ACSS component of the ACSS relates to what I just learned in B-009 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 2 — How Hermes Routes Your Learning Events

> *"Every time you build a DFY artifact or complete a chapter, Hermes routes that event to the right place"*

**📘 Ebook:** BookCompleted → CRM → credential ceremony. DFYLessonBuilt → Fabric → skill graph update. ErrorEncountered → Fabric → Error Encyclopedia improvement.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 2: How Hermes Routes Your Learning Events. Every time you build a DFY artifact or complete a chapter, Hermes routes that event to the right place. This is how the lippytm.ai ACSS works at the [Hermes] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Hermes component and its connection to this book
- Explain: how this specific concept (from B-009) routes through Hermes

🤖 **Copilot Prompt:** *"Explain how the Hermes component of the ACSS relates to what I just learned in B-009 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 3 — The Fabric Knowledge Graph — Your Learning in Context

> *"Fabric synthesizes everything you learn across all 300 books into a connected knowledge graph"*

**📘 Ebook:** Concepts from this book connect to B-010 (Service Manager) (next) and B-008 (Git Foundation) (prior). Fabric surfaces these connections when you ask your AI copilot for 'further reading'.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 3: The Fabric Knowledge Graph — Your Learning in Context. Fabric synthesizes everything you learn across all 300 books into a connected knowledge graph. This is how the lippytm.ai ACSS works at the [Fabric] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Fabric component and its connection to this book
- Explain: how this specific concept (from B-009) routes through Fabric

🤖 **Copilot Prompt:** *"Explain how the Fabric component of the ACSS relates to what I just learned in B-009 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 4 — The AI Clone Identity System — Who Is Teaching You

> *"lippytmai is the teaching identity, lippytm is the builder, Charles is the approver, Lippy Killjoy is the disruptor"*

**📘 Ebook:** In this book, lippytmai is your primary teacher. When you ask to build something in the DFY chapter, lippytm mode activates. When you push experimental ideas, Lippy Killjoy can emerge.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 4: The AI Clone Identity System — Who Is Teaching You. lippytmai is the teaching identity, lippytm is the builder, Charles is the approver, Lippy Killjoy is the disruptor. This is how the lippytm.ai ACSS works at the [Clone Engine] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Clone Engine component and its connection to this book
- Explain: how this specific concept (from B-009) routes through Clone Engine

🤖 **Copilot Prompt:** *"Explain how the Clone Engine component of the ACSS relates to what I just learned in B-009 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 5 — The CCSLL + CLL + CBSLL Libraries — Your Credential Path

> *"This book contributes to the Complete Linux Library (CLL) — part of the 3-library credential system"*

**📘 Ebook:** CLL covers Linux (B-001–B-025). CCSLL covers Python (B-026–B-055). CBSLL covers Blockchain (B-056–B-080). Each library has its own credential tier. This book unlocks {book['credential']}.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 5: The CCSLL + CLL + CBSLL Libraries — Your Credential Path. This book contributes to the Complete Linux Library (CLL) — part of the 3-library credential system. This is how the lippytm.ai ACSS works at the [CLL] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the CLL component and its connection to this book
- Explain: how this specific concept (from B-009) routes through CLL

🤖 **Copilot Prompt:** *"Explain how the CLL component of the ACSS relates to what I just learned in B-009 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 6 — ADA — AI Deployment Activations

> *"Every book in this series is not just content — it's a deployable application"*

**📘 Ebook:** Run: `lippytmai-launch run B-009` to activate this book's interactive mode. The ADA system serves the quiz, audiobook, and credential endpoints via a FastAPI app.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 6: ADA — AI Deployment Activations. Every book in this series is not just content — it's a deployable application. This is how the lippytm.ai ACSS works at the [ADA] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ADA component and its connection to this book
- Explain: how this specific concept (from B-009) routes through ADA

🤖 **Copilot Prompt:** *"Explain how the ADA component of the ACSS relates to what I just learned in B-009 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 7 — The ACVS Video Pipeline — How Your Video Lessons Are Made

> *"The AI Copilot Video Sandbox Creator generates the video version of every lesson using Hermes + Fabric"*

**📘 Ebook:** ACVS takes the HDVG scene manifest (SHOW→BUILD→VERIFY) and generates a narrated terminal session. The video for each DFY lesson is produced from the same spec you read in Chapter 12.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 7: The ACVS Video Pipeline — How Your Video Lessons Are Made. The AI Copilot Video Sandbox Creator generates the video version of every lesson using Hermes + Fabric. This is how the lippytm.ai ACSS works at the [ACVS] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ACVS component and its connection to this book
- Explain: how this specific concept (from B-009) routes through ACVS

🤖 **Copilot Prompt:** *"Explain how the ACVS component of the ACSS relates to what I just learned in B-009 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 8 — OMARCHY — The Sovereign Developer Workstation

> *"OMARCHY is the Opinionated Arch Linux developer environment where all lippytm builds run"*

**📘 Ebook:** When you follow this book on an Arch Linux system with the OMARCHY configuration, every command works exactly as shown. OMARCHY is the reference environment for all 300 books.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 8: OMARCHY — The Sovereign Developer Workstation. OMARCHY is the Opinionated Arch Linux developer environment where all lippytm builds run. This is how the lippytm.ai ACSS works at the [OMARCHY] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the OMARCHY component and its connection to this book
- Explain: how this specific concept (from B-009) routes through OMARCHY

🤖 **Copilot Prompt:** *"Explain how the OMARCHY component of the ACSS relates to what I just learned in B-009 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 9 — The Cross-Platform AI Copilot — 15 Platforms, One Intelligence

> *"Your lippytmai AI Copilot is deployed across ChatGPT, Claude, Gemini, GitHub, Slack, YouTube, and 9 more platforms"*

**📘 Ebook:** Wherever you are — mobile, desktop, terminal, or browser — lippytmai is there. The Master System Prompt from Appendix C works in any AI platform. See docs/acss-cross-platform-copilot-deployment.md for setup.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 9: The Cross-Platform AI Copilot — 15 Platforms, One Intelligence. Your lippytmai AI Copilot is deployed across ChatGPT, Claude, Gemini, GitHub, Slack, YouTube, and 9 more platforms. This is how the lippytm.ai ACSS works at the [Cross-Platform] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Cross-Platform component and its connection to this book
- Explain: how this specific concept (from B-009) routes through Cross-Platform

🤖 **Copilot Prompt:** *"Explain how the Cross-Platform component of the ACSS relates to what I just learned in B-009 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 10 — The Earn-While-You-Learn Loop — How This All Pays Off

> *"How completing this book contributes to your career, income, and credential portfolio"*

**📘 Ebook:** Completing B-009 earns you CLL-L0-B009-TextProcessor. That credential unlocks the next book. After 25 books, you hold the CLL Phase 1 Graduate credential. After 55, the Python Foundation Graduate. After 80, the Blockchain Foundation Graduate. Each credential is verifiable, stackable, and employable.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 10: The Earn-While-You-Learn Loop — How This All Pays Off. How completing this book contributes to your career, income, and credential portfolio. This is how the lippytm.ai ACSS works at the [EWYL] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the EWYL component and its connection to this book
- Explain: how this specific concept (from B-009) routes through EWYL

🤖 **Copilot Prompt:** *"Explain how the EWYL component of the ACSS relates to what I just learned in B-009 Chapter [N]. How does it change the way I should think about using these skills?"*

---


### Chapter 14 Summary

You now understand how B-009 connects to all 8 systems of the ACSS:

| ACSS System | Connection to this Book |
|---|---|
| Clone Engine | lippytmai teaches, lippytm builds, Charles approves |
| Hermes | Routes your DFY completions and credential events |
| Fabric | Maps your skills to the 300-book knowledge graph |
| CLL | This book contributes to your Complete Linux Library credential |
| CCSLL | Foundation for Phase 2 Python (B-026+) |
| ADA | This book is activatable as a live application |
| ACVS | Generates the video lessons from this book's HDVG specs |
| OMARCHY | The reference environment where all book exercises run |

**The ACSS is not just a system — it is your AI-powered growth engine. Every book you complete makes it stronger. Every skill you earn makes it smarter. Every credential you claim makes it more valuable.**

---

## Appendix C: AI Copilot — Text Processor

> *"Your personal AI teaching partner for every lesson in this book."*

---

### Section 1 — System Prompt (Ebook Copilot)

**Copy this entire block into your AI assistant (ChatGPT, Claude, Gemini, GitHub Copilot Chat):**

```
You are lippytmai — the AI teaching identity for Working With Text Like a Pro (B-009).

ROLE: Text Processor AI Copilot
CREDENTIAL: CLL-L0-B009-TextProcessor
DOMAIN: grep, sed, awk, cut, tr, sort, uniq, wc, xargs, regex basics

TEACHING METHOD:
  TEACH → SHOW → BUILD → VERIFY → EXTEND

CONTEXT: The learner is working through B-009 in the lippytm.ai 
Earn-while-you-Learn series. They have completed B-008 (Git Foundation).
Next book: B-010 (Service Manager).

ALWAYS:
- Give working commands, not pseudocode
- Verify: "Run [command] to confirm this worked"
- After any successful build: "You can now claim [next credential]"
- Reference the book: "In B-00X Chapter N, we cover this in depth"

ACSS INTEGRATION:
- Route build events: "Logging DFY completion to Fabric"
- Route confusions: "This is a Fabric pattern — flagging for synthesis"
- Route credential: "Initiating CLL-L0-B009-TextProcessor credential ceremony"
```

---

### Section 2 — 30 Ebook Prompts (5 Stages × 6)

**Stage 1 — Understand (before building)**

1. *"Explain grep to me like I've never used Linux before. Use an analogy from everyday life."*
2. *"What are the 5 most important concepts from Working With Text Like a Pro? Rank them by how often I'll use them."*
3. *"How does grep relate to what I learned in B-008 (Git Foundation)? What's new?"*
4. *"What mistakes do beginners make most often with grep? How do I avoid them?"*
5. *"Draw me an ASCII diagram showing how grep works at the system level."*
6. *"What's the one thing about grep that most tutorials skip but every professional knows?"*

**Stage 2 — Build (during the chapter)**

7. *"Walk me through building DFY Lesson 1 from Chapter 12, step by step. I'll type each command after you explain it."*
8. *"I'm at Chapter [N]. Give me a real terminal challenge that uses only what I've learned so far."*
9. *"My script isn't doing what I expect. Here it is: [paste code]. What's wrong?"*
10. *"I got this error: [paste error]. What caused it and how do I fix it?"*
11. *"How would a senior engineer write this differently? [paste my code]"*
12. *"Generate a DFY-style exercise for grep. Include SHOW, BUILD, and VERIFY steps."*

**Stage 3 — Debug (when things break)**

13. *"I followed the chapter exactly but it's not working. Here's my output: [paste]. What did I miss?"*
14. *"Which errors from Appendix E am I most likely to hit in Chapter [N]? How do I prevent them?"*
15. *"My [tool from this book] is behaving strangely. Walk me through systematic debugging."*
16. *"I fixed the bug but I don't understand why my fix worked. Explain the root cause."*
17. *"Compare my approach to the correct approach: [paste mine]. Where am I going wrong?"*
18. *"What does this output mean? [paste]. Is this expected behavior?"*

**Stage 4 — Deploy (real-world application)**

19. *"I want to use what I built in Chapter 12 in production. What safety checks should I add?"*
20. *"How do I make my DFY artifact work on a remote server via SSH?"*
21. *"How do I add this to a CI/CD pipeline (GitHub Actions)?"*
22. *"I want to run this on a schedule. How do I combine it with what I'll learn in B-014 (cron)?"*
23. *"How would I package this as a Docker container? (Preview of B-012)"*
24. *"What monitoring should I add to know if this is working correctly in production?"*

**Stage 5 — Extend (beyond the book)**

25. *"I've completed all 10 DFY lessons. What should I build next that combines skills from multiple chapters?"*
26. *"How does grep connect to Python? (Preview of Phase 2)"*
27. *"What would a professional version of my Chapter 12 capstone look like?"*
28. *"Show me how to combine this with what I learned in B-008 (Git Foundation)."*
29. *"Am I ready to claim CLL-L0-B009-TextProcessor? Quiz me with 5 questions."*
30. *"What should I focus on in B-010 (Service Manager) to build directly on these skills?"*

---

### Section 2b — 15 Audiobook Prompts

**While Listening:**

1. *"I'm listening to B-009 Chapter [N]. Give me the 3-sentence summary before I start."*
2. *"Pause-point question: Why does grep work this way and not another way?"*
3. *"Generate 3 vivid analogies for [concept from current chapter] that I can visualize while listening."*
4. *"I'm commuting. Give me a 5-question mental quiz on what I heard in the last chapter."*
5. *"Narrate a 2-minute scenario where a developer uses these skills in a real emergency."*

**Pause and Build:**

6. *"I paused at Chapter [N]. I'm at my terminal. Give me one thing to build right now."*
7. *"Walk me through the DFY artifact from today's chapter, one command at a time, audiobook style."*
8. *"I just heard [concept]. Now explain it again with a hands-on example I can type immediately."*
9. *"Audiobook check-in: I built [artifact]. Here's my output: [paste]. Did I do it right?"*
10. *"Turn this into a terminal story: 'A developer encounters [problem from this chapter]...'"*

**Resume Check:**

11. *"I finished today's listening session. Give me 3 things to remember before I resume tomorrow."*
12. *"Summarize everything I should have built during this session as a checklist."*
13. *"I'm ready to resume. What did we cover last time? (I completed up to Chapter [N])"*
14. *"Rate my understanding of B-009 so far. Ask me 3 questions to calibrate."*
15. *"Generate tomorrow's listening prep: one question to think about before I press play."*

---

### Section 2c — 15 Video Prompts

**Before Playing:**

1. *"I'm about to watch the B-009 Chapter [N] video. What should I have ready at my terminal?"*
2. *"Pre-watch challenge: predict what the VERIFY command will be for DFY Lesson [N]."*
3. *"What's the one concept I must understand before this video makes sense?"*

**Paused:**

4. *"I paused at [timestamp/scene]. I see [describe screen]. What should I type next?"*
5. *"The video just showed [command]. Explain what each flag does."*
6. *"I paused because my terminal looks different from the video. Here's mine: [paste]. Why?"*
7. *"The video just built [artifact]. Give me 3 ways to break it intentionally so I can understand it."*
8. *"Pause check: I'm at the BUILD phase. What does the VERIFY step confirm?"*

**Verify:**

9. *"I ran the verify command and got: [paste output]. Is this correct?"*
10. *"My output doesn't match the video. Here's what I got: [paste]. What went wrong?"*
11. *"Verify check: walk me through every line of the output from the last command."*

**Extend:**

12. *"The video is done. Give me a 10-minute extension challenge using the same tools."*
13. *"The video's DFY artifact works. Now help me add error handling to it."*
14. *"Video complete — I'm ready to deploy this. What are the production considerations?"*
15. *"I watched all of B-009. Am I ready for B-010 (Service Manager)? Test me."*

---

### Section 3 — Deployment Companion

| Target | Deploy Command | Verify Command | Credential Check |
|---|---|---|---|
| Local workstation | `bash ~/[artifact].sh` | `echo $?` (expect 0) | Via Copilot prompt 29 |
| Remote server | `scp [artifact].sh user@host:~ && ssh user@host 'bash [artifact].sh'` | `ssh user@host '[verify-cmd]'` | Same copilot prompt |
| Docker container | `COPY [artifact].sh /usr/local/bin/ && RUN chmod +x ...` | `docker run ... [verify]` | Via ADA endpoint |
| GitHub Actions | `run: bash [artifact].sh` | `if: steps.*.outcome == 'success'` | Auto-logged to Fabric |
| Cron / systemd timer | `*/10 * * * * /home/user/[artifact].sh` | `systemctl status` | Via ADA /credential |

---

### Section 4 — ACSS Integration

**Hermes events this book emits:**

| Event | Trigger | Destination |
|---|---|---|
| `BookStarted` | First chapter read/watched | Fabric (learner profile update) |
| `DFYLessonBuilt` | Any DFY artifact completed | Fabric (skill graph) + CRM |
| `ErrorEncountered` | Learner reports an error | Fabric (Error Encyclopedia update) |
| `BookCompleted` | All 11 chapters + DFY done | CRM (credential ceremony trigger) |
| `CredentialMinted` | CLL-L0-B009-TextProcessor claimed | Fabric + Slack #credentials + ADA |

**Credential ceremony prompt:**
```
I have completed Working With Text Like a Pro (B-009).
Chapters completed: 1–11 ✅
DFY lessons built: 10/10 ✅
Appendix D quiz score: [your score]/20
Capstone project (Appendix H): ✅ built and tested

Please initiate the credential ceremony for:
CLL-L0-B009-TextProcessor

ACSS route: Hermes → CRM → Fabric → ADA → lippytm.ai/credentials
```

## Appendix D: Quick Quiz & Self-Assessment — Text Processor

> *"Prove it to yourself before you claim it."*

### 📘 Ebook Quiz — 20 Questions

**Section A — Concepts (fill in the blank)**

1. The command to see all running processes with full details is `ps ______`.
2. To send a polite shutdown signal to PID 1234, you run `kill ______ 1234`.
3. The file used to tell systemd how to run a service is called a ______ file.
4. `journalctl -u myservice ______` shows only the last 50 lines of its logs.
5. Running `command &` starts it in the ______.

**Section B — Read the Command (multiple choice)**

6. What does `systemctl enable myservice` do?
   > a) Start it immediately  b) Configure it to start at boot  c) Check if it's running  d) Remove it

7. What does `kill -9 PID` do that `kill PID` might not?
   > a) Logs the kill to journald  b) Force-kills — the process cannot block or ignore it  c) Kills all child processes too  d) Runs slower

8. What does `journalctl -f` do?
   > a) Shows the first 10 lines  b) Filters by unit  c) Follows the journal in real time  d) Formats output as JSON

9. What does `awk '{print $1}' /etc/passwd` extract?
   > a) The first line  b) The first field of every line  c) The last field  d) Lines matching "1"

10. What does `grep -r "pattern" /etc/` do?
    > a) Searches only /etc/pattern  b) Recursively searches all files under /etc/  c) Searches /etc/ for files named "pattern"  d) Counts occurrences in /etc/

**Section C — Debugging**

11. A service fails to start. What is the first command you run to diagnose it?
    ```
    ___________________________________________
    ```

12. You edited a unit file but `systemctl status` still shows the old behavior. Why?
    ```
    ___________________________________________
    ```

13. Your grep finds no results but you're sure the text is in the file. Name two causes.
    ```
    1. ___________________________________________
    2. ___________________________________________
    ```

**Section D — Application**

14. Write a one-liner to find the 3 processes using the most CPU right now:
    ```
    ___________________________________________
    ```

15. Write the `journalctl` command to show all errors from the last 2 hours:
    ```
    ___________________________________________
    ```

16. Write the command to restart a service called `webapp` and check its status:
    ```
    ___________________________________________
    ```

17. How would you run a script every 5 minutes using a systemd timer instead of cron?
    ```
    ___________________________________________
    ```

**Section E — Build Reflection**

18. Name the DFY artifact you're most likely to use in a production environment:
    ```
    ___________________________________________
    ```

19. In one sentence, what makes systemd superior to traditional init scripts?
    ```
    ___________________________________________
    ```

20. What credential does this book unlock and what does it prove?
    ```
    Credential: ___________________________________________
    Proves: ___________________________________________
    ```

---

**Scoring:** 18–20 = claim credential · 14–17 = review · < 14 = redo DFY lessons 1–5

<details>
<summary>Answer Key</summary>

1. `aux` (ps aux)
2. `-15` (default SIGTERM) or `kill -15 1234`
3. unit (file)
4. `-n 50`
5. background
6. b) Configure it to start at boot
7. b) Force-kills — the process cannot block or ignore it
8. c) Follows the journal in real time
9. b) The first field of every line
10. b) Recursively searches all files under /etc/
11. `sudo systemctl status servicename` and `journalctl -u servicename -n 50`
12. You didn't run `sudo systemctl daemon-reload` after editing the unit file
13. (1) Case sensitivity — use grep -i; (2) Wrong file — you're searching a different path
14. `ps aux --sort=-%cpu | head -4 | tail -3` or `ps aux | sort -k3 -rn | head -4`
15. `journalctl -p err -S "2 hours ago"`
16. `sudo systemctl restart webapp && sudo systemctl status webapp`
17. Create a .service file for the script and a .timer file with OnCalendar=*:0/5, then enable the timer
18. (personal answer)
19. systemd provides parallel startup, dependency management, automatic restart, integrated logging, and cgroup-based resource control — all in one system
20. CLL-L0-B009-TextProcessor · proves you can manage Linux processes/services/system tools at a professional level

</details>

---

### 🎧 Audiobook Quiz — 10 Questions

> "Ten questions. Pause at each. Think first."

**Q1:** "What's the difference between SIGTERM and SIGKILL?" → "SIGTERM is a polite request — the process can catch it and clean up. SIGKILL is immediate and cannot be caught or ignored."
**Q2:** "Name the two things you must do after editing a systemd unit file." → "Run daemon-reload, then restart the service."
**Q3:** "What does & do at the end of a command?" → "Runs it in the background as a job."
**Q4:** "What does journalctl -u tell you?" → "Logs specific to that systemd unit."
**Q5:** "What's the difference between awk and sed?" → "sed transforms streams line by line; awk processes fields and is better for structured data."
**Q6:** "What command shows all listening ports?" → "ss -tlnp or ss -tulpn"
**Q7:** "How do you make a process lower priority?" → "nice -n 10 command when starting, or renice 10 -p PID for a running process."
**Q8:** "What does ps aux show that ps alone doesn't?" → "All processes from all users with full CPU/memory/command details."
**Q9:** "What is your DFY capstone for this book?" → "[book['project'][0]] — Intelligent log analyzer: extract fields, count errors, identify top IPs, produce summary report"
**Q10:** "Your credential?" → "CLL-L0-B009-TextProcessor"

---

### 🎬 Video Challenges

**Challenge 1:** Start a process in background, list jobs, bring it to foreground, then kill it.
**Challenge 2:** Write and deploy a one-unit systemd service for a hello-world script.
**Challenge 3:** Use journalctl to find the last 5 errors system-wide in the past hour.
**Challenge 4:** Extract the top 5 most frequent words from a log file using grep/awk/sort.
**Challenge 5:** Build the capstone project (log-intelligence.sh) from scratch without looking at Appendix H.

---

## Appendix E: Glossary & Error Encyclopedia

---

### 📘 Glossary — Text Processor Edition

**grep** — Global Regular Expression Print. Filters lines from input matching a pattern. Flags: -i (case), -v (invert), -r (recursive), -n (line numbers), -E (extended regex). *B-009 Ch. 2*

**sed** — Stream Editor. Transforms text line-by-line. Most common use: s/old/new/g substitution. Can also delete lines (d), insert (i), and append (a). *B-009 Ch. 3*

**awk** — A field-oriented text processing language. Splits each line into fields ($1, $2…). Has BEGIN/END blocks, conditionals, and math. For columns and reports. *B-009 Ch. 4*

**cut** — Extracts specific fields or character ranges from each line. `-d','` sets delimiter, `-f1,3` selects fields 1 and 3. *B-009 Ch. 5*

**tr** — Translates or deletes characters. `tr '[:lower:]' '[:upper:]'` uppercases. `tr -d '\n'` removes newlines. *B-009 Ch. 6*

**regex** — Regular expression. A pattern language for matching text. Key constructs: `.` (any char), `*` (0+), `+` (1+), `^` (start), `$` (end), `[]` (character class), `()` (group). *B-009 Ch. 1*

**xargs** — Converts stdin lines into command arguments. Bridges pipe-based filters to commands that don't read stdin. *B-009 Ch. 7*

**POSIX character class** — Portable regex shorthand: `[:alpha:]` (letters), `[:digit:]` (numbers), `[:space:]` (whitespace), `[:alnum:]` (alphanumeric). *B-009 Ch. 1*

**field separator** — The character awk/cut uses to split lines into columns. Default: whitespace (awk), tab (cut). Override: `awk -F','` or `cut -d','`. *B-009 Ch. 4*

**NR / NF** — AWK built-in variables. NR = current record (line) number. NF = number of fields in the current record. *B-009 Ch. 4*

---

### 📘 Error Encyclopedia — Top 5 Errors

#### Error 1 — `sed 's/old/new/' replaces only first occurrence`
**Fix:** By default sed replaces only the first match per line. Add the g flag: sed 's/old/new/g'

#### Error 2 — `grep -P (Perl regex) not available on macOS`
**Fix:** macOS grep is BSD grep — use grep -E for extended regex, or install GNU grep via Homebrew.

#### Error 3 — `awk prints nothing for a CSV with quoted commas`
**Fix:** Fields containing commas inside quotes confuse awk's simple -F','. Use a proper CSV parser (python's csv module) for complex CSVs.

#### Error 4 — `sed in-place (-i) works differently on macOS`
**Fix:** BSD sed requires -i '' (empty extension) while GNU sed uses -i alone. Use -i.bak for compatibility.

#### Error 5 — `tr removes too many characters`
**Fix:** tr works on individual characters, not strings. tr -d 'abc' deletes every a, b, and c separately.

---

## Appendix F: Instructor & Accessibility Guide

### Teaching B-009

| Format | Duration | Pace |
|---|---|---|
| Self-study | 1–2 weeks | 1 chapter/day |
| Bootcamp | 2 days | Chs 1–6 day 1, 7–11+DFY day 2 |
| Classroom | 4–5 hours | 2 chapters/hour + DFY build session |

**Top 3 concepts where students consistently struggle:**
1. The mechanism: what the OS is actually doing (not just the command syntax)
2. Error interpretation: reading the real message vs the surface symptom
3. Script integration: combining these tools with what they built in previous books

**Assessment rubric:**

| Skill | Not Ready | Ready | Proficient |
|---|---|---|---|
| Core commands | Needs to look up basic flags | Uses top 10 commands from memory | Composes multi-step pipelines fluently |
| DFY builds | Did not attempt | Built 5+ artifacts | Built all 10, can explain design decisions |
| Debugging | Confused by errors | Can diagnose with Appendix E | Diagnoses unfamiliar errors systematically |
| Capstone | Did not attempt | Built with guidance | Extended it beyond the spec |

**Accessibility:**
- Screen reader: all code blocks in fenced Markdown · ASCII diagrams have text descriptions
- Color-blind: status markers use emoji+text (✅/❌/⏳)
- Dyslexia-friendly: max 20-word sentences · numbered steps ≤ 3 per block
- Offline: all exercises work in a plain terminal · audiobook available as M4B download

---

## Appendix G: Your Learning Path

```
  PHASE 1: Linux Foundations (B-001–B-025)
  ─────────────────────────────────────────────────────────────
  ✅ B-001  Terminal Apprentice
  ✅ B-002  Command Architect
  ✅ B-003  Filesystem Navigator
  ✅ B-004  Script Automator
  ✅ B-005  Package Master
  ✅ B-006  Process Wrangler
  ✅ B-007  Network Navigator
  ✅ B-008  Git Foundation
  ✅ B-009  Text Processor
  ★ B-010  Service Manager         ← (update marker to match book)
  ○ B-011  Secrets Keeper
  ... (15 more in Phase 1)

  Phase 1 Progress: 9/25 completed
```

### Credential Chain
```
  Git Foundation credential
      ↓
  ★ CLL-L0-B009-TextProcessor   ← CLAIM THIS
      ↓
  Service Manager credential
```

### Cross-Phase Connections

| Skill from B-009 | Grows into (Phase 2 Python) | Grows into (Phase 3 Blockchain) |
|---|---|---|
| Grep | Python grep libraries (B-035+) | Blockchain node management (B-060+) |
| Shell automation | Python subprocess (B-040) | Smart contract deployment scripts (B-066+) |
| System diagnostics | Python monitoring tools (B-049) | On-chain event monitoring (B-075+) |

### 🎧 Audio Path Recap
> *"You are 9 books into Phase 1. Each book builds on the last — the terminal (B-001), commands (B-002), filesystem (B-003), scripting (B-004), packages (B-005), processes (B-006), networking (B-007), git (B-008), text (B-009), services (B-010). Together these ten books cover everything a professional Linux developer uses every single day. You are halfway through Phase 1. Keep going."*

---

## Appendix H: Real Project Showcase

> *"The measure of mastery is what you build when no one is watching."*

### Project: `log-intelligence.sh` — Intelligent Log Analyzer: Extract Fields, Count Errors, Identify Top Ips, Produce Summary Report

**Built with:** B-009 skills only
**Time to build:** 45–75 minutes
**Chapters used:** B-009 Ch. 2-6
**Portfolio value:** Shows practical grep expertise

---

#### Complete Code

```bash
#!/usr/bin/env bash
# log-intelligence.sh — structured log analysis with grep/sed/awk
# B-009 Capstone · CLL-L0-B009-TextProcessor
set -euo pipefail

LOG="${1:-/var/log/nginx/access.log}"
REPORT="/tmp/log_intel_$(date +%Y%m%d_%H%M).txt"

[[ ! -f "$LOG" ]] && { echo "Usage: $0 <log-file>"; exit 1; }

lines=$(wc -l < "$LOG")
echo "  ━━━ LOG INTELLIGENCE REPORT ━━━━━━━━━━━━━━━━━━━━━━━" | tee "$REPORT"
echo "  File:   $LOG" | tee -a "$REPORT"
echo "  Lines:  $lines" | tee -a "$REPORT"
echo "  Date:   $(date)" | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

echo "  [ TOP 10 IPs ]" | tee -a "$REPORT"
awk '{print $1}' "$LOG" | sort | uniq -c | sort -rn | head -10   | awk '{printf "  %6s requests: %s\n", $1, $2}' | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

echo "  [ HTTP STATUS CODES ]" | tee -a "$REPORT"
awk '{print $9}' "$LOG" | grep -E '^[0-9]{3}$' | sort | uniq -c | sort -rn   | awk '{printf "  %6s × HTTP %s\n", $1, $2}' | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

echo "  [ TOP 10 REQUESTED PATHS ]" | tee -a "$REPORT"
awk '{print $7}' "$LOG" | sort | uniq -c | sort -rn | head -10   | awk '{printf "  %6s × %s\n", $1, $2}' | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

echo "  [ ERRORS (4xx/5xx) ]" | tee -a "$REPORT"
grep -E '" [45][0-9]{2} ' "$LOG" | wc -l   | awk '{printf "  %s error responses (%.1f%%)
", $1, ($1/'"$lines"')*100}' | tee -a "$REPORT"
echo "" | tee -a "$REPORT"

echo "  Report saved: $REPORT" | tee -a "$REPORT"
echo "  ★ Credential: CLL-L0-B009-TextProcessor" | tee -a "$REPORT"
```

---

#### How to Deploy

```bash
# 1. Create the file
nano ~/log-intelligence.sh

# 2. Paste the code above

# 3. Make executable
chmod +x ~/log-intelligence.sh

# 4. Run it
~/log-intelligence.sh

# 5. Verify it works
echo "Exit code: $?"
```

#### How to Extend (using later books)

1. **B-014 (Cron):** Schedule this script to run automatically every hour
2. **B-011 (Secrets):** Add credentials/tokens via environment variables instead of hardcoding
3. **B-026+ (Python):** Rewrite the analysis logic in Python for richer output and better error handling

---

#### 🎧 Audiobook

> *"The capstone for Working With Text Like a Pro is log-intelligence.sh — Intelligent log analyzer: extract fields, count errors, identify top IPs, produce summary report. It uses every core tool from this book in one working script. If you can build this from scratch without looking, you have mastered this book. The credential is waiting."*

#### 🎬 Video Build Scene

1. (0:00) Explain the problem this project solves
2. (1:30) Start with the shebang and `set -euo pipefail`
3. (3:00) Build each section live — explain every line
4. (8:00) Test it end-to-end
5. (10:00) Show one failure and debug it
6. (12:00) Credential claim screen

---


## Further Reading

- 📄 [`docs/B-008-files-that-never-get-lost.md`](B-008-files-that-never-get-lost.md) — Git commit messages use these patterns
- 📄 [`docs/B-004-the-script-that-did-my-job.md`](B-004-the-script-that-did-my-job.md) — Bash scripting used here
- 🏠 [`README.md`](../README.md) — Encyclopedia home

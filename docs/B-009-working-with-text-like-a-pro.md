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

## Further Reading

- 📄 [`docs/B-008-files-that-never-get-lost.md`](B-008-files-that-never-get-lost.md) — Git commit messages use these patterns
- 📄 [`docs/B-004-the-script-that-did-my-job.md`](B-004-the-script-that-did-my-job.md) — Bash scripting used here
- 🏠 [`README.md`](../README.md) — Encyclopedia home

# B-016: Pipes, Redirects, and Composition

### The Unix Philosophy — Small Tools, Connected Together

> *"The Unix philosophy is not about any single tool. It's about composition: dozens of small, sharp tools, each doing one thing perfectly, connected by pipes into pipelines that process data in ways no single program could. A Neovim user who understands pipes thinks differently about problem-solving — they stop writing programs and start composing workflows."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Use `|` (pipe) to chain commands together
2. Redirect stdout with `>` and `>>`, stderr with `2>`, both with `2>&1`
3. Use `<` for stdin redirection and process substitution
4. Build a multi-stage data pipeline using `grep`, `sort`, `uniq`, `cut`, `wc`
5. Write a one-liner that processes a log file into a summary report

**Prerequisite:** B-001 through B-015

**Build Artifact:** A shell one-liner pipeline that reads a web server log, extracts unique IPs, counts requests per IP, and outputs the top 10 offenders

**Credential:** `CLL-L1-B016-PipelineBuilder` — on-chain on Base

---

## Chapter 1: Standard Streams

Every Linux process has three standard streams:

| Stream | FD | Default destination | Meaning |
|---|---|---|---|
| **stdin** | 0 | Keyboard | Input the program reads |
| **stdout** | 1 | Terminal | Normal output |
| **stderr** | 2 | Terminal | Error output |

Pipes and redirects rewire these streams.

---

## Chapter 2: The Pipe Operator

`|` takes the stdout of one command and sends it as stdin to the next:

```bash
# Without pipe: ls output fills terminal
ls /etc

# With pipe: pass ls output to grep
ls /etc | grep "^s"

# Chain multiple pipes
cat /var/log/syslog | grep "error" | tail -20

# Count matching lines
cat /var/log/syslog | grep "error" | wc -l

# The classic pipeline
ps aux | grep python | grep -v grep
```

*[Reality — the pipe was invented by Douglas McIlroy at Bell Labs in 1973. It is one of the most influential ideas in computing history]*

---

## Chapter 3: Output Redirection

```bash
# > overwrite stdout to file (creates or truncates)
ls -la > filelist.txt

# >> append stdout to file
echo "$(date): backup started" >> backup.log
echo "$(date): backup complete" >> backup.log

# 2> redirect stderr to file
python3 broken.py 2> error.log

# 2>&1 redirect stderr to same destination as stdout
python3 broken.py > output.log 2>&1

# &> shorthand for redirecting both stdout and stderr
python3 broken.py &> all-output.log

# Silence all output (useful in cron)
python3 script.py > /dev/null 2>&1

# tee — output to terminal AND file simultaneously
python3 script.py 2>&1 | tee run.log
```

---

## Chapter 4: Input Redirection

```bash
# < redirect file to stdin
sort < filelist.txt

# <<EOF here-document — multi-line stdin
cat << 'EOF'
Line one
Line two
Line three
EOF

# <<< here-string — single string as stdin
grep "pattern" <<< "check this string for pattern"

# Process substitution — treat command output as a file
diff <(ls dir1) <(ls dir2)
```

---

## Chapter 5: The Essential Pipeline Tools

| Command | Does what | Key flags |
|---|---|---|
| `grep` | Filter lines matching pattern | `-i` case-insensitive, `-v` invert, `-c` count |
| `sort` | Sort lines | `-n` numeric, `-r` reverse, `-u` unique, `-k` by field |
| `uniq` | Remove duplicate consecutive lines | `-c` prefix count |
| `cut` | Extract fields from lines | `-d` delimiter, `-f` field number |
| `awk` | Field processing | `{print $1}` first field |
| `wc` | Count lines/words/chars | `-l` lines, `-w` words |
| `head` / `tail` | First/last N lines | `-n 20`, `-f` follow |
| `tr` | Translate/delete characters | `tr '[:upper:]' '[:lower:]'` |

---

## Chapter 6: The Build — Log Analysis Pipeline

```bash
# Sample Apache/Nginx access log format:
# 192.168.1.42 - - [28/Aug/2026:03:00:01 +0000] "GET /api/data HTTP/1.1" 200 1234

# --- B-016 Build Artifact ---
# One-liner: top 10 IPs by request count from access log

cat access.log \
  | cut -d' ' -f1 \
  | sort \
  | uniq -c \
  | sort -rn \
  | head -10

# Output example:
#    453 203.0.113.99
#    287 198.51.100.42
#    201 192.0.2.15
# ...

# Save as a script for cron
cat > ~/scripts/top-ips.sh << 'SCRIPT'
#!/bin/bash
# top-ips.sh — B-016 Build Artifact
# Analyzes access log and outputs top 10 IPs by request count
set -euo pipefail

LOG_FILE="${1:-/var/log/nginx/access.log}"
TOP_N="${2:-10}"
OUTPUT="${3:-/tmp/top-ips-$(date +%Y%m%d).txt}"

echo "=== Top ${TOP_N} IPs in ${LOG_FILE} ===" > "$OUTPUT"
echo "Generated: $(date)" >> "$OUTPUT"
echo "" >> "$OUTPUT"

cut -d' ' -f1 "$LOG_FILE" \
  | sort \
  | uniq -c \
  | sort -rn \
  | head -"${TOP_N}" \
  | awk '{printf "%-8s %s\n", $1, $2}' >> "$OUTPUT"

echo "Report saved to: $OUTPUT"
cat "$OUTPUT"
SCRIPT

chmod +x ~/scripts/top-ips.sh

# Generate a sample log to test with
python3 -c "
import random, datetime
ips = ['192.168.1.' + str(i) for i in range(1, 20)]
for _ in range(1000):
    ip = random.choice(ips)
    print(f'{ip} - - [28/Aug/2026:03:00:01 +0000] \"GET /api HTTP/1.1\" 200 1234')
" > /tmp/sample-access.log

~/scripts/top-ips.sh /tmp/sample-access.log
```

---

## Chapter 7: Proof of Work

```bash
echo "=== B-016 Verification ==="
echo "Pipeline test:"
echo -e "apple\nbanana\napple\ncherry\nbanana\napple" | sort | uniq -c | sort -rn
echo ""
echo "Log analysis:"
~/scripts/top-ips.sh /tmp/sample-access.log 5
```

---

## Further Reading

- 📄 [`docs/B-009-working-with-text-like-a-pro.md`](B-009-working-with-text-like-a-pro.md) — grep/sed/awk foundations
- 📄 [`docs/B-018-log-files-tell-the-truth.md`](B-018-log-files-tell-the-truth.md) — Apply pipelines to real log analysis
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Blockchain node log pipelines
- 🏠 [`README.md`](../README.md) — Encyclopedia home

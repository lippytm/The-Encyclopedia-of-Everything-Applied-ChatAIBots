# B-006: The Process That Wouldn't Stop

### Linux Process Management — Finding, Monitoring, and Controlling What Runs on Your System

> *"A server is not a static thing. At any given moment, hundreds of programs are competing for CPU, memory, and your attention. The developer who can read that chaos — who knows which process to kill and which to leave alone — is the developer who fixes the crisis."*
> — lippytmai

---

## Learning Objectives

By the end of this book, you will be able to:

1. Understand what a process is and how Linux manages them
2. View running processes with `ps`, `top`, and `htop`
3. Send signals to processes using `kill`, `pkill`, and `killall`
4. Move processes to the background and foreground with `&`, `bg`, `fg`, `jobs`
5. Build a process monitoring script that alerts you to high CPU usage

**Prerequisite:** B-001 through B-005

**Build Artifact:** `process-monitor.sh` — a Bash script that watches for CPU-intensive processes and logs them

**Credential:** `CLL-L1-B006-ProcessWrangler` — on-chain on Base

---

## Chapter 1: What Is a Process?

When you run a program, Linux creates a **process** — an instance of that program running in memory with its own:

- **PID** (Process ID): a unique number assigned at creation
- **PPID** (Parent Process ID): the PID of the process that spawned it
- **User**: who owns/runs it
- **State**: running, sleeping, zombie, stopped
- **Resources**: CPU%, memory%, open files

```
Your Terminal (PID 1234)
    └── bash (PID 1235)
        └── python3 app.py (PID 1236)
            └── worker thread (PID 1237)
```

Every process has a parent. The root of all processes on Linux is **PID 1** — on modern systems this is `systemd`.

*[Reality — Linux's process tree has been rooted at PID 1 since the original Unix design]*

---

## Chapter 2: Viewing Processes

### ps — Process Snapshot

```bash
# Show your current shell's processes
ps

# Show ALL processes from ALL users
ps aux

# Show a process tree (who spawned who)
ps auxf

# Show processes for a specific user
ps -u charles

# Find a specific process by name
ps aux | grep python
```

**Decoding `ps aux` output:**

| Column | Meaning |
|---|---|
| `USER` | Process owner |
| `PID` | Process ID |
| `%CPU` | CPU usage percentage |
| `%MEM` | Memory usage percentage |
| `VSZ` | Virtual memory size (KB) |
| `RSS` | Resident (physical) memory (KB) |
| `STAT` | Process state (R=running, S=sleeping, Z=zombie) |
| `COMMAND` | The command that started it |

### top — Live Process Viewer

```bash
# Launch top (updates every 3 seconds)
top

# Inside top:
# q      → quit
# k      → kill a process (enter PID)
# r      → renice (change priority)
# M      → sort by memory usage
# P      → sort by CPU usage (default)
# 1      → show per-CPU stats
```

### htop — The Better top

```bash
# Install htop (if not present)
sudo apt install htop   # Ubuntu/Debian
sudo pacman -S htop     # Arch

# Run htop
htop
# Use arrow keys, F6 to sort, F9 to kill, q to quit
```

*[Reality — htop is the standard process viewer on most production Linux servers]*

---

## Chapter 3: Signals and kill

Every process responds to **signals** — messages the OS sends to tell a process to do something.

```bash
# Send the default signal (SIGTERM = polite shutdown request)
kill 1234

# Force kill — process cannot ignore this
kill -9 1234

# Kill by name
pkill python3

# Kill all processes matching a pattern
killall python3

# List all available signals
kill -l
```

### The Most Important Signals

| Signal | Number | Meaning |
|---|---|---|
| `SIGTERM` (15) | default | "Please shut down cleanly" — the process can handle it |
| `SIGKILL` (9) | `-9` | "Die now" — cannot be caught or ignored |
| `SIGHUP` (1) | `-1` | "Reload your config" — used for daemons |
| `SIGINT` (2) | `Ctrl+C` | "Interrupt" — what happens when you press Ctrl+C |
| `SIGSTOP` (19) | `Ctrl+Z` | "Pause execution" |
| `SIGCONT` (18) | — | "Resume after SIGSTOP" |

```bash
# The rule: always try SIGTERM first, only use -9 if the process refuses
kill 1234        # polite
sleep 3
kill -9 1234     # force (if needed)
```

*[Reality — SIGKILL (-9) cannot be caught by the process — it is always delivered by the kernel immediately]*

---

## Chapter 4: Background and Foreground Jobs

```bash
# Run a command in the background with &
python3 server.py &
# Output: [1] 5678  ← job number and PID

# See background jobs
jobs
# [1]+  Running    python3 server.py &

# Bring a background job to the foreground
fg 1

# Send a foreground job to background
# First: Ctrl+Z to pause it
# Then:
bg 1

# Run a long command that survives terminal close
nohup python3 server.py > server.log 2>&1 &

# Or use disown to detach from terminal
python3 server.py &
disown
```

---

## Chapter 5: The Build — process-monitor.sh

```bash
#!/bin/bash
# process-monitor.sh — B-006 Build Artifact
# Monitors for CPU-intensive processes and logs them
set -euo pipefail

LOG_FILE="${LOG_FILE:-$HOME/developer-workspace/logs/process-monitor.log}"
CPU_THRESHOLD="${CPU_THRESHOLD:-50}"
CHECK_INTERVAL="${CHECK_INTERVAL:-10}"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$1] $2" | tee -a "$LOG_FILE"
}

check_cpu_intensive() {
    local findings
    findings=$(ps aux --sort=-%cpu | awk -v threshold="$CPU_THRESHOLD" '
        NR>1 && $3+0 >= threshold {
            printf "%s (PID:%s, CPU:%.1f%%, MEM:%.1f%%)\n", $11, $2, $3, $4
        }
    ')
    
    if [ -n "$findings" ]; then
        log "ALERT" "High CPU processes found:"
        while IFS= read -r line; do
            log "ALERT" "  → $line"
        done <<< "$findings"
    else
        log "INFO" "All processes within threshold (${CPU_THRESHOLD}% CPU)"
    fi
}

get_system_summary() {
    local load
    load=$(cat /proc/loadavg | awk '{print $1, $2, $3}')
    local mem_total mem_available
    mem_total=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    mem_available=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
    local mem_pct=$(( (mem_total - mem_available) * 100 / mem_total ))
    
    log "INFO" "System: Load=$load | Memory=${mem_pct}% used"
}

mkdir -p "$(dirname "$LOG_FILE")"
log "INFO" "Process monitor started (threshold=${CPU_THRESHOLD}%, interval=${CHECK_INTERVAL}s)"

for i in 1 2 3; do
    get_system_summary
    check_cpu_intensive
    [ $i -lt 3 ] && sleep "$CHECK_INTERVAL"
done

log "INFO" "Process monitor complete"
```

```bash
# Save, make executable, run
chmod +x process-monitor.sh
./process-monitor.sh

# Run with custom threshold
CPU_THRESHOLD=10 ./process-monitor.sh

# Watch the log
tail -f ~/developer-workspace/logs/process-monitor.log
```

---

## Chapter 6: Proof of Work

```bash
echo "=== B-006 Build Verification ==="
echo "Process monitor script:"
ls -la ~/process-monitor.sh

echo ""
echo "Running monitor (10% threshold to see output):"
CPU_THRESHOLD=10 ~/process-monitor.sh

echo ""
echo "Top 5 processes by CPU:"
ps aux --sort=-%cpu | head -6

echo ""
echo "Background job test:"
sleep 60 &
SLEEP_PID=$!
jobs
kill $SLEEP_PID
echo "Job $SLEEP_PID terminated"
```

---

## Chapter 7: Mutation

```bash
# MUTATION 1: Continuous monitoring every 30 seconds (until Ctrl+C)
while true; do
    CPU_THRESHOLD=80 ~/process-monitor.sh
    sleep 30
done

# MUTATION 2: Find the top memory consumer
ps aux --sort=-%mem | head -2 | tail -1

# MUTATION 3: See the full process tree
ps auxf | head -40
# Or with pstree (install if needed)
sudo apt install psmisc
pstree -p | head -30
```

---

## Further Reading

- 📄 [`docs/B-005-installing-things-without-breaking-things.md`](B-005-installing-things-without-breaking-things.md) — prerequisite
- 📄 [`docs/B-010-the-service-that-started-itself.md`](B-010-the-service-that-started-itself.md) — systemd: process management at the OS level
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Full Linux curriculum
- 🏠 [`README.md`](../README.md) — Encyclopedia home

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


---

## Chapter 12: Done-For-You Lessons — Process Wrangler

> *"The fastest way to learn is to build something real. These ten lessons give you exactly that — ten deployable tools, ready to use, built by your own hands."*

---

### DFY Lesson 1 — process-sentinel.sh

> **What you're building:** Process watchdog — restart a named service if it dies

**📘 Ebook Figure**

```bash
# DFY-B-006-L01: process-sentinel.sh
# Domain: Process watchdog — restart a named service if it dies
# Time to build: 15–25 minutes
# Credential: CLL-L0-B006-ProcessWrangler

# STEP 1: Create the script file
nano ~/process-sentinel.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/process-sentinel.sh.sh

# STEP 4: Test it
~/process-sentinel.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 1: process-sentinel.sh. Process watchdog — restart a named service if it dies. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep process-` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/process-sentinel.sh && ~/process-sentinel.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built process-sentinel.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 2 — cpu-hog-finder.sh

> **What you're building:** Find and report top 5 CPU consumers every 30 seconds

**📘 Ebook Figure**

```bash
# DFY-B-006-L02: cpu-hog-finder.sh
# Domain: Find and report top 5 CPU consumers every 30 seconds
# Time to build: 15–25 minutes
# Credential: CLL-L0-B006-ProcessWrangler

# STEP 1: Create the script file
nano ~/cpu-hog-finder.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/cpu-hog-finder.sh.sh

# STEP 4: Test it
~/cpu-hog-finder.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 2: cpu-hog-finder.sh. Find and report top 5 CPU consumers every 30 seconds. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep cpu-hog-` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/cpu-hog-finder.sh && ~/cpu-hog-finder.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built cpu-hog-finder.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 3 — job-manager alias set

> **What you're building:** bg/fg/jobs shortcuts for your .bashrc

**📘 Ebook Figure**

```bash
# DFY-B-006-L03: job-manager alias set
# Domain: bg/fg/jobs shortcuts for your .bashrc
# Time to build: 15–25 minutes
# Credential: CLL-L0-B006-ProcessWrangler

# STEP 1: Create the script file
nano ~/job-manager alias set.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/job-manager alias set.sh

# STEP 4: Test it
~/job-manager alias set.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 3: job-manager alias set. bg/fg/jobs shortcuts for your .bashrc. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep job-mana` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/job-manager alias set && ~/job-manager alias set` — it runs, it works

🤖 **Copilot Assist:** *"I built job-manager alias set but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 4 — signal-demo.sh

> **What you're building:** Demonstrate all 4 main signals on a test process

**📘 Ebook Figure**

```bash
# DFY-B-006-L04: signal-demo.sh
# Domain: Demonstrate all 4 main signals on a test process
# Time to build: 15–25 minutes
# Credential: CLL-L0-B006-ProcessWrangler

# STEP 1: Create the script file
nano ~/signal-demo.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/signal-demo.sh.sh

# STEP 4: Test it
~/signal-demo.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 4: signal-demo.sh. Demonstrate all 4 main signals on a test process. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep signal-d` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/signal-demo.sh && ~/signal-demo.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built signal-demo.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 5 — renice-priority.sh

> **What you're building:** Lower priority of background jobs automatically

**📘 Ebook Figure**

```bash
# DFY-B-006-L05: renice-priority.sh
# Domain: Lower priority of background jobs automatically
# Time to build: 15–25 minutes
# Credential: CLL-L0-B006-ProcessWrangler

# STEP 1: Create the script file
nano ~/renice-priority.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/renice-priority.sh.sh

# STEP 4: Test it
~/renice-priority.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 5: renice-priority.sh. Lower priority of background jobs automatically. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep renice-p` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/renice-priority.sh && ~/renice-priority.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built renice-priority.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 6 — zombie-finder.sh

> **What you're building:** Detect and report zombie processes

**📘 Ebook Figure**

```bash
# DFY-B-006-L06: zombie-finder.sh
# Domain: Detect and report zombie processes
# Time to build: 15–25 minutes
# Credential: CLL-L0-B006-ProcessWrangler

# STEP 1: Create the script file
nano ~/zombie-finder.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/zombie-finder.sh.sh

# STEP 4: Test it
~/zombie-finder.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 6: zombie-finder.sh. Detect and report zombie processes. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep zombie-f` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/zombie-finder.sh && ~/zombie-finder.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built zombie-finder.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 7 — process-snapshot.sh

> **What you're building:** Snapshot process tree to a timestamped log

**📘 Ebook Figure**

```bash
# DFY-B-006-L07: process-snapshot.sh
# Domain: Snapshot process tree to a timestamped log
# Time to build: 15–25 minutes
# Credential: CLL-L0-B006-ProcessWrangler

# STEP 1: Create the script file
nano ~/process-snapshot.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/process-snapshot.sh.sh

# STEP 4: Test it
~/process-snapshot.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 7: process-snapshot.sh. Snapshot process tree to a timestamped log. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep process-` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/process-snapshot.sh && ~/process-snapshot.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built process-snapshot.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 8 — kill-by-name.sh

> **What you're building:** Safe kill-by-name with confirmation prompt

**📘 Ebook Figure**

```bash
# DFY-B-006-L08: kill-by-name.sh
# Domain: Safe kill-by-name with confirmation prompt
# Time to build: 15–25 minutes
# Credential: CLL-L0-B006-ProcessWrangler

# STEP 1: Create the script file
nano ~/kill-by-name.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/kill-by-name.sh.sh

# STEP 4: Test it
~/kill-by-name.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 8: kill-by-name.sh. Safe kill-by-name with confirmation prompt. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep kill-by-` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/kill-by-name.sh && ~/kill-by-name.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built kill-by-name.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 9 — cpu-mem-monitor.sh

> **What you're building:** Continuous CPU+memory logger to CSV

**📘 Ebook Figure**

```bash
# DFY-B-006-L09: cpu-mem-monitor.sh
# Domain: Continuous CPU+memory logger to CSV
# Time to build: 15–25 minutes
# Credential: CLL-L0-B006-ProcessWrangler

# STEP 1: Create the script file
nano ~/cpu-mem-monitor.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/cpu-mem-monitor.sh.sh

# STEP 4: Test it
~/cpu-mem-monitor.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 9: cpu-mem-monitor.sh. Continuous CPU+memory logger to CSV. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep cpu-mem-` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/cpu-mem-monitor.sh && ~/cpu-mem-monitor.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built cpu-mem-monitor.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---

### DFY Lesson 10 — process-health-report.sh

> **What you're building:** System-wide process health report: zombie/orphan/high-cpu

**📘 Ebook Figure**

```bash
# DFY-B-006-L10: process-health-report.sh
# Domain: System-wide process health report: zombie/orphan/high-cpu
# Time to build: 15–25 minutes
# Credential: CLL-L0-B006-ProcessWrangler

# STEP 1: Create the script file
nano ~/process-health-report.sh.sh

# STEP 2: Add content (see code in this lesson)

# STEP 3: Make executable
chmod +x ~/process-health-report.sh.sh

# STEP 4: Test it
~/process-health-report.sh.sh
```

**🎧 Audiobook Callout** *(lippytmai voice · ~90 seconds)*

> *"Lesson 10: process-health-report.sh. System-wide process health report: zombie/orphan/high-cpu. This is a real tool you'll use from the first day you build it. We're going to create it in three steps: write it, make it executable, test it. By the end of this lesson you'll have a working script that saves you time every single time you open a terminal."*

**🎬 Video Scene** *(SHOW → BUILD → VERIFY)*

- **SHOW:** `ls -lah ~/ | grep process-` — nothing there yet
- **BUILD:** type the script live, line by line, explaining each command
- **VERIFY:** `chmod +x ~/process-health-report.sh && ~/process-health-report.sh` — it runs, it works

🤖 **Copilot Assist:** *"I built process-health-report.sh but it's not working correctly. Here's my error: [paste error]. What's wrong and how do I fix it? Also, how could I extend this to handle [edge case]?"*

---


---

### Chapter 12 Credential Claim

You've built 10 real tools in the **processes** domain. Every one is deployable today.

**To claim your credential:** Open your AI Copilot (Appendix C) and send:
```
I have completed all 10 DFY lessons from The Process That Wouldn't Stop (B-006).
My builds: process-sentinel.sh, cpu-hog-finder.sh, job-manager alias set, signal-demo.sh, renice-priority.sh, zombie-finder.sh, process-snapshot.sh, kill-by-name.sh, cpu-mem-monitor.sh, process-health-report.sh.
I am ready to claim: CLL-L0-B006-ProcessWrangler
Please guide me through the credential ceremony.
```

---

## Chapter 13: How It Works — Use Cases & Applications

> *"A skill without context is just a trick. Understanding when to use it — and where it applies — is what separates professionals from beginners."*

---

### 📘 Ebook — Mechanism & Conditions

**How Processes works (the 30-second mechanism):**

processes → signals → jobs → ps → kill → htop → bg/fg → nice → cgroups → all driven by the same underlying OS primitives. When you understand the mechanism, you can apply it anywhere.

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

> *"B-006 teaches you processes — but the application goes far beyond what the chapter title suggests. Every developer, DevOps engineer, data scientist, and security researcher uses these exact tools every day. The command line is not a developer tool — it is the universal interface to every computer that matters."*

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
- Process watchdog — restart a named service if it dies
- Find and report top 5 CPU consumers every 30 seconds
- bg/fg/jobs shortcuts for your .bashrc
- Demonstrate all 4 main signals on a test process
- Lower priority of background jobs automatically
- Detect and report zombie processes
- Snapshot process tree to a timestamped log
- Safe kill-by-name with confirmation prompt
- Continuous CPU+memory logger to CSV
- System-wide process health report: zombie/orphan/high-cpu
- Confidently explain these tools in a technical interview
- Apply them on any Linux system, remote or local
- Integrate them into scripts, CI/CD pipelines, and automation workflows

---

## Appendix A: Quick Reference Card — Process Wrangler

> *"The 80/20 of B-006. These commands cover 80% of real-world use cases."*

**Top 15 Commands:**

```bash
# PROCESSES — essential commands
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

**Credential:** `CLL-L0-B006-ProcessWrangler`
**Claim at:** `lippytm.ai/credentials`

---

## Appendix B: ACSS Connection — B-006

This book is part of the **AI Conglomerate Swarms System (ACSS)** — the continuously self-learning intelligence layer across all lippytm.ai projects.

| System | Connection |
|---|---|
| **CLL** | B-006 contributes to Level 0 of the Complete Linux Library |
| **Hermes** | Events: `BookCompleted`, `CredentialMinted`, `DFYLessonBuilt` |
| **Fabric** | Your builds and questions feed the knowledge synthesis engine |
| **ADA** | This book is activatable: `lippytmai-launch run B-006` |
| **lippytmai** | Your AI teaching partner for every lesson in this book |


---

## Chapter 14: ACSS Explainer Series — Process Wrangler

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
- Explain: how this specific concept (from B-006) routes through ACSS

🤖 **Copilot Prompt:** *"Explain how the ACSS component of the ACSS relates to what I just learned in B-006 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 2 — How Hermes Routes Your Learning Events

> *"Every time you build a DFY artifact or complete a chapter, Hermes routes that event to the right place"*

**📘 Ebook:** BookCompleted → CRM → credential ceremony. DFYLessonBuilt → Fabric → skill graph update. ErrorEncountered → Fabric → Error Encyclopedia improvement.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 2: How Hermes Routes Your Learning Events. Every time you build a DFY artifact or complete a chapter, Hermes routes that event to the right place. This is how the lippytm.ai ACSS works at the [Hermes] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Hermes component and its connection to this book
- Explain: how this specific concept (from B-006) routes through Hermes

🤖 **Copilot Prompt:** *"Explain how the Hermes component of the ACSS relates to what I just learned in B-006 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 3 — The Fabric Knowledge Graph — Your Learning in Context

> *"Fabric synthesizes everything you learn across all 300 books into a connected knowledge graph"*

**📘 Ebook:** Concepts from this book connect to B-007 (Network Navigator) (next) and B-005 (Package Master) (prior). Fabric surfaces these connections when you ask your AI copilot for 'further reading'.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 3: The Fabric Knowledge Graph — Your Learning in Context. Fabric synthesizes everything you learn across all 300 books into a connected knowledge graph. This is how the lippytm.ai ACSS works at the [Fabric] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Fabric component and its connection to this book
- Explain: how this specific concept (from B-006) routes through Fabric

🤖 **Copilot Prompt:** *"Explain how the Fabric component of the ACSS relates to what I just learned in B-006 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 4 — The AI Clone Identity System — Who Is Teaching You

> *"lippytmai is the teaching identity, lippytm is the builder, Charles is the approver, Lippy Killjoy is the disruptor"*

**📘 Ebook:** In this book, lippytmai is your primary teacher. When you ask to build something in the DFY chapter, lippytm mode activates. When you push experimental ideas, Lippy Killjoy can emerge.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 4: The AI Clone Identity System — Who Is Teaching You. lippytmai is the teaching identity, lippytm is the builder, Charles is the approver, Lippy Killjoy is the disruptor. This is how the lippytm.ai ACSS works at the [Clone Engine] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Clone Engine component and its connection to this book
- Explain: how this specific concept (from B-006) routes through Clone Engine

🤖 **Copilot Prompt:** *"Explain how the Clone Engine component of the ACSS relates to what I just learned in B-006 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 5 — The CCSLL + CLL + CBSLL Libraries — Your Credential Path

> *"This book contributes to the Complete Linux Library (CLL) — part of the 3-library credential system"*

**📘 Ebook:** CLL covers Linux (B-001–B-025). CCSLL covers Python (B-026–B-055). CBSLL covers Blockchain (B-056–B-080). Each library has its own credential tier. This book unlocks {book['credential']}.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 5: The CCSLL + CLL + CBSLL Libraries — Your Credential Path. This book contributes to the Complete Linux Library (CLL) — part of the 3-library credential system. This is how the lippytm.ai ACSS works at the [CLL] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the CLL component and its connection to this book
- Explain: how this specific concept (from B-006) routes through CLL

🤖 **Copilot Prompt:** *"Explain how the CLL component of the ACSS relates to what I just learned in B-006 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 6 — ADA — AI Deployment Activations

> *"Every book in this series is not just content — it's a deployable application"*

**📘 Ebook:** Run: `lippytmai-launch run B-006` to activate this book's interactive mode. The ADA system serves the quiz, audiobook, and credential endpoints via a FastAPI app.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 6: ADA — AI Deployment Activations. Every book in this series is not just content — it's a deployable application. This is how the lippytm.ai ACSS works at the [ADA] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ADA component and its connection to this book
- Explain: how this specific concept (from B-006) routes through ADA

🤖 **Copilot Prompt:** *"Explain how the ADA component of the ACSS relates to what I just learned in B-006 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 7 — The ACVS Video Pipeline — How Your Video Lessons Are Made

> *"The AI Copilot Video Sandbox Creator generates the video version of every lesson using Hermes + Fabric"*

**📘 Ebook:** ACVS takes the HDVG scene manifest (SHOW→BUILD→VERIFY) and generates a narrated terminal session. The video for each DFY lesson is produced from the same spec you read in Chapter 12.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 7: The ACVS Video Pipeline — How Your Video Lessons Are Made. The AI Copilot Video Sandbox Creator generates the video version of every lesson using Hermes + Fabric. This is how the lippytm.ai ACSS works at the [ACVS] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the ACVS component and its connection to this book
- Explain: how this specific concept (from B-006) routes through ACVS

🤖 **Copilot Prompt:** *"Explain how the ACVS component of the ACSS relates to what I just learned in B-006 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 8 — OMARCHY — The Sovereign Developer Workstation

> *"OMARCHY is the Opinionated Arch Linux developer environment where all lippytm builds run"*

**📘 Ebook:** When you follow this book on an Arch Linux system with the OMARCHY configuration, every command works exactly as shown. OMARCHY is the reference environment for all 300 books.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 8: OMARCHY — The Sovereign Developer Workstation. OMARCHY is the Opinionated Arch Linux developer environment where all lippytm builds run. This is how the lippytm.ai ACSS works at the [OMARCHY] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the OMARCHY component and its connection to this book
- Explain: how this specific concept (from B-006) routes through OMARCHY

🤖 **Copilot Prompt:** *"Explain how the OMARCHY component of the ACSS relates to what I just learned in B-006 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 9 — The Cross-Platform AI Copilot — 15 Platforms, One Intelligence

> *"Your lippytmai AI Copilot is deployed across ChatGPT, Claude, Gemini, GitHub, Slack, YouTube, and 9 more platforms"*

**📘 Ebook:** Wherever you are — mobile, desktop, terminal, or browser — lippytmai is there. The Master System Prompt from Appendix C works in any AI platform. See docs/acss-cross-platform-copilot-deployment.md for setup.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 9: The Cross-Platform AI Copilot — 15 Platforms, One Intelligence. Your lippytmai AI Copilot is deployed across ChatGPT, Claude, Gemini, GitHub, Slack, YouTube, and 9 more platforms. This is how the lippytm.ai ACSS works at the [Cross-Platform] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the Cross-Platform component and its connection to this book
- Explain: how this specific concept (from B-006) routes through Cross-Platform

🤖 **Copilot Prompt:** *"Explain how the Cross-Platform component of the ACSS relates to what I just learned in B-006 Chapter [N]. How does it change the way I should think about using these skills?"*

---
### Explainer 10 — The Earn-While-You-Learn Loop — How This All Pays Off

> *"How completing this book contributes to your career, income, and credential portfolio"*

**📘 Ebook:** Completing B-006 earns you CLL-L0-B006-ProcessWrangler. That credential unlocks the next book. After 25 books, you hold the CLL Phase 1 Graduate credential. After 55, the Python Foundation Graduate. After 80, the Blockchain Foundation Graduate. Each credential is verifiable, stackable, and employable.

**🎧 Audiobook** *(30-second callout)*
> *"Explainer 10: The Earn-While-You-Learn Loop — How This All Pays Off. How completing this book contributes to your career, income, and credential portfolio. This is how the lippytm.ai ACSS works at the [EWYL] layer. Understanding it makes every book in this series 10x more useful — because you know exactly where each skill connects."*

**🎬 Video** *(60-second screen explanation)*
- Show: ACSS architecture diagram from `docs/ai-clone-engine-swarms.md`
- Highlight: the EWYL component and its connection to this book
- Explain: how this specific concept (from B-006) routes through EWYL

🤖 **Copilot Prompt:** *"Explain how the EWYL component of the ACSS relates to what I just learned in B-006 Chapter [N]. How does it change the way I should think about using these skills?"*

---


### Chapter 14 Summary

You now understand how B-006 connects to all 8 systems of the ACSS:

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

## Appendix C: AI Copilot — Process Wrangler

> *"Your personal AI teaching partner for every lesson in this book."*

---

### Section 1 — System Prompt (Ebook Copilot)

**Copy this entire block into your AI assistant (ChatGPT, Claude, Gemini, GitHub Copilot Chat):**

```
You are lippytmai — the AI teaching identity for The Process That Wouldn't Stop (B-006).

ROLE: Process Wrangler AI Copilot
CREDENTIAL: CLL-L0-B006-ProcessWrangler
DOMAIN: processes, signals, jobs, ps, kill, htop, bg/fg, nice, cgroups

TEACHING METHOD:
  TEACH → SHOW → BUILD → VERIFY → EXTEND

CONTEXT: The learner is working through B-006 in the lippytm.ai 
Earn-while-you-Learn series. They have completed B-005 (Package Master).
Next book: B-007 (Network Navigator).

ALWAYS:
- Give working commands, not pseudocode
- Verify: "Run [command] to confirm this worked"
- After any successful build: "You can now claim [next credential]"
- Reference the book: "In B-00X Chapter N, we cover this in depth"

ACSS INTEGRATION:
- Route build events: "Logging DFY completion to Fabric"
- Route confusions: "This is a Fabric pattern — flagging for synthesis"
- Route credential: "Initiating CLL-L0-B006-ProcessWrangler credential ceremony"
```

---

### Section 2 — 30 Ebook Prompts (5 Stages × 6)

**Stage 1 — Understand (before building)**

1. *"Explain processes to me like I've never used Linux before. Use an analogy from everyday life."*
2. *"What are the 5 most important concepts from The Process That Wouldn't Stop? Rank them by how often I'll use them."*
3. *"How does processes relate to what I learned in B-005 (Package Master)? What's new?"*
4. *"What mistakes do beginners make most often with processes? How do I avoid them?"*
5. *"Draw me an ASCII diagram showing how processes works at the system level."*
6. *"What's the one thing about processes that most tutorials skip but every professional knows?"*

**Stage 2 — Build (during the chapter)**

7. *"Walk me through building DFY Lesson 1 from Chapter 12, step by step. I'll type each command after you explain it."*
8. *"I'm at Chapter [N]. Give me a real terminal challenge that uses only what I've learned so far."*
9. *"My script isn't doing what I expect. Here it is: [paste code]. What's wrong?"*
10. *"I got this error: [paste error]. What caused it and how do I fix it?"*
11. *"How would a senior engineer write this differently? [paste my code]"*
12. *"Generate a DFY-style exercise for processes. Include SHOW, BUILD, and VERIFY steps."*

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
26. *"How does processes connect to Python? (Preview of Phase 2)"*
27. *"What would a professional version of my Chapter 12 capstone look like?"*
28. *"Show me how to combine this with what I learned in B-005 (Package Master)."*
29. *"Am I ready to claim CLL-L0-B006-ProcessWrangler? Quiz me with 5 questions."*
30. *"What should I focus on in B-007 (Network Navigator) to build directly on these skills?"*

---

### Section 2b — 15 Audiobook Prompts

**While Listening:**

1. *"I'm listening to B-006 Chapter [N]. Give me the 3-sentence summary before I start."*
2. *"Pause-point question: Why does processes work this way and not another way?"*
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
14. *"Rate my understanding of B-006 so far. Ask me 3 questions to calibrate."*
15. *"Generate tomorrow's listening prep: one question to think about before I press play."*

---

### Section 2c — 15 Video Prompts

**Before Playing:**

1. *"I'm about to watch the B-006 Chapter [N] video. What should I have ready at my terminal?"*
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
15. *"I watched all of B-006. Am I ready for B-007 (Network Navigator)? Test me."*

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
| `CredentialMinted` | CLL-L0-B006-ProcessWrangler claimed | Fabric + Slack #credentials + ADA |

**Credential ceremony prompt:**
```
I have completed The Process That Wouldn't Stop (B-006).
Chapters completed: 1–11 ✅
DFY lessons built: 10/10 ✅
Appendix D quiz score: [your score]/20
Capstone project (Appendix H): ✅ built and tested

Please initiate the credential ceremony for:
CLL-L0-B006-ProcessWrangler

ACSS route: Hermes → CRM → Fabric → ADA → lippytm.ai/credentials
```

## Appendix D: Quick Quiz & Self-Assessment — Process Wrangler

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
20. CLL-L0-B006-ProcessWrangler · proves you can manage Linux processes/services/system tools at a professional level

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
**Q9:** "What is your DFY capstone for this book?" → "[book['project'][0]] — full process guardian: watch a service, restart on failure, log events, alert on high CPU"
**Q10:** "Your credential?" → "CLL-L0-B006-ProcessWrangler"

---

### 🎬 Video Challenges

**Challenge 1:** Start a process in background, list jobs, bring it to foreground, then kill it.
**Challenge 2:** Write and deploy a one-unit systemd service for a hello-world script.
**Challenge 3:** Use journalctl to find the last 5 errors system-wide in the past hour.
**Challenge 4:** Extract the top 5 most frequent words from a log file using grep/awk/sort.
**Challenge 5:** Build the capstone project (process-guardian.sh) from scratch without looking at Appendix H.

---

## Appendix E: Glossary & Error Encyclopedia

---

### 📘 Glossary — Process Wrangler Edition

**PID** — Process ID. A unique integer the kernel assigns to every running process. *B-006 Ch. 1*

**PPID** — Parent PID. The PID of the process that spawned this one. All processes have a parent except PID 1. *B-006 Ch. 1*

**signal** — A software interrupt sent to a process. Common: SIGTERM (15, polite stop), SIGKILL (9, force), SIGHUP (1, reload config), SIGINT (2, Ctrl+C). *B-006 Ch. 3*

**zombie** — A process that has exited but whose parent hasn't collected its exit status. Shows as 'Z' in ps. Harmless unless thousands exist. *B-006 Ch. 5*

**orphan** — A process whose parent has died. Adopted by PID 1 (init/systemd) automatically. *B-006 Ch. 5*

**nice value** — A priority hint (-20 to 19). Lower = higher priority. Only root can go below 0. Set with nice/renice. *B-006 Ch. 6*

**cgroup** — Control Group. Kernel mechanism that limits and tracks resource usage (CPU, memory, I/O) for a group of processes. *B-006 Ch. 8*

**bg / fg** — Shell job control commands. bg resumes a stopped job in the background. fg brings it to the foreground. *B-006 Ch. 4*

**fork** — System call that creates a child process as a copy of the parent. The foundation of all process creation on Linux. *B-006 Ch. 2*

**exec** — System call that replaces the current process image with a new program. Used after fork to launch a different program. *B-006 Ch. 2*

---

### 📘 Error Encyclopedia — Top 5 Errors

#### Error 1 — `kill: (PID): Operation not permitted`
**Fix:** You don't own the process. Use sudo for other users' processes.

#### Error 2 — `Process shows as zombie (Z)`
**Fix:** The parent isn't reaping children. If persistent, restart the parent process.

#### Error 3 — `kill -9 doesn't work`
**Fix:** Nothing can kill SIGKILL-immune processes except fixing the kernel issue causing them (usually uninterruptible I/O wait - state D).

#### Error 4 — `htop shows 100% CPU but system feels fine`
**Fix:** A single-core computation on a multi-core system. The process is using one full CPU but others are idle.

#### Error 5 — `bg: job has terminated`
**Fix:** The job finished before you backgrounded it. Nothing to do.

---

## Appendix F: Instructor & Accessibility Guide

### Teaching B-006

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

  Phase 1 Progress: 6/25 completed
```

### Credential Chain
```
  Package Master credential
      ↓
  ★ CLL-L0-B006-ProcessWrangler   ← CLAIM THIS
      ↓
  Network Navigator credential
```

### Cross-Phase Connections

| Skill from B-006 | Grows into (Phase 2 Python) | Grows into (Phase 3 Blockchain) |
|---|---|---|
| Processes | Python processes libraries (B-035+) | Blockchain node management (B-060+) |
| Shell automation | Python subprocess (B-040) | Smart contract deployment scripts (B-066+) |
| System diagnostics | Python monitoring tools (B-049) | On-chain event monitoring (B-075+) |

### 🎧 Audio Path Recap
> *"You are 6 books into Phase 1. Each book builds on the last — the terminal (B-001), commands (B-002), filesystem (B-003), scripting (B-004), packages (B-005), processes (B-006), networking (B-007), git (B-008), text (B-009), services (B-010). Together these ten books cover everything a professional Linux developer uses every single day. You are halfway through Phase 1. Keep going."*

---

## Appendix H: Real Project Showcase

> *"The measure of mastery is what you build when no one is watching."*

### Project: `process-guardian.sh` — Full Process Guardian: Watch A Service, Restart On Failure, Log Events, Alert On High Cpu

**Built with:** B-006 skills only
**Time to build:** 45–75 minutes
**Chapters used:** B-006 Ch. 3-7
**Portfolio value:** Shows practical processes expertise

---

#### Complete Code

```bash
#!/usr/bin/env bash
# process-guardian.sh — watch a process, restart it, log everything
# B-006 Capstone · CLL-L0-B006-ProcessWrangler
set -euo pipefail

SERVICE="${1:-nginx}"
LOG="$HOME/.guardian_${SERVICE}.log"
CHECK_INTERVAL=10  # seconds
MAX_CPU=80         # alert if CPU exceeds this %

log() { echo "  [$(date '+%H:%M:%S')] $*" | tee -a "$LOG"; }

get_pid()  { pgrep -x "$SERVICE" | head -1 || true; }
get_cpu()  { ps -p "${1:-0}" -o %cpu= 2>/dev/null | tr -d ' ' || echo 0; }
get_mem()  { ps -p "${1:-0}" -o %mem= 2>/dev/null | tr -d ' ' || echo 0; }

start_service() {
    log "Starting $SERVICE..."
    command -v systemctl &>/dev/null && sudo systemctl start "$SERVICE"       || { log "systemctl not found — attempting direct start"; "$SERVICE" & }
}

log "Guardian started for: $SERVICE"
log "Log: $LOG | Interval: ${CHECK_INTERVAL}s | Max CPU: ${MAX_CPU}%"

while true; do
    PID=$(get_pid)
    if [[ -z "$PID" ]]; then
        log "ALERT: $SERVICE not running — restarting"
        start_service
        sleep 2
        NEW_PID=$(get_pid)
        [[ -n "$NEW_PID" ]] && log "Restarted: PID $NEW_PID" || log "ERROR: restart failed"
    else
        CPU=$(get_cpu "$PID")
        MEM=$(get_mem "$PID")
        # Alert if CPU is high
        [[ "${CPU%.*}" -gt "$MAX_CPU" ]]           && log "WARNING: $SERVICE (PID $PID) using ${CPU}% CPU"           || log "OK: $SERVICE PID=$PID CPU=${CPU}% MEM=${MEM}%"
    fi
    sleep "$CHECK_INTERVAL"
done
```

---

#### How to Deploy

```bash
# 1. Create the file
nano ~/process-guardian.sh

# 2. Paste the code above

# 3. Make executable
chmod +x ~/process-guardian.sh

# 4. Run it
~/process-guardian.sh

# 5. Verify it works
echo "Exit code: $?"
```

#### How to Extend (using later books)

1. **B-014 (Cron):** Schedule this script to run automatically every hour
2. **B-011 (Secrets):** Add credentials/tokens via environment variables instead of hardcoding
3. **B-026+ (Python):** Rewrite the analysis logic in Python for richer output and better error handling

---

#### 🎧 Audiobook

> *"The capstone for The Process That Wouldn't Stop is process-guardian.sh — full process guardian: watch a service, restart on failure, log events, alert on high CPU. It uses every core tool from this book in one working script. If you can build this from scratch without looking, you have mastered this book. The credential is waiting."*

#### 🎬 Video Build Scene

1. (0:00) Explain the problem this project solves
2. (1:30) Start with the shebang and `set -euo pipefail`
3. (3:00) Build each section live — explain every line
4. (8:00) Test it end-to-end
5. (10:00) Show one failure and debug it
6. (12:00) Credential claim screen

---


## Further Reading

- 📄 [`docs/B-005-installing-things-without-breaking-things.md`](B-005-installing-things-without-breaking-things.md) — prerequisite
- 📄 [`docs/B-010-the-service-that-started-itself.md`](B-010-the-service-that-started-itself.md) — systemd: process management at the OS level
- 📄 [`docs/linux-blockchain-educational-ecosystem.md`](linux-blockchain-educational-ecosystem.md) — Full Linux curriculum
- 🏠 [`README.md`](../README.md) — Encyclopedia home
